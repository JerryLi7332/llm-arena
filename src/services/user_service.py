"""用户服务层 - 统一用户业务逻辑"""

from tortoise.expressions import Q

from repositories.dept import dept_repository
from repositories.user import user_repository
from schemas.base import Fail, Success, SuccessExtra
from schemas.users import UserCreate, UserUpdate, ProfileUpdate
from services.base_service import BaseService
from utils.cache import cached, clear_user_cache


class UserService(BaseService):
    """用户服务类 - 专门处理用户相关业务逻辑"""

    def __init__(self):
        super().__init__(user_repository)

    async def get_user_list(
        self,
        page: int = 1,
        page_size: int = 10,
        username: str = "",
        email: str = "",
        dept_id: int | None = None,
    ) -> SuccessExtra:
        """获取用户列表 - 包含搜索过滤和部门信息关联"""
        try:
            # 构建搜索过滤条件
            search_filters = self._build_user_search_filters(
                username=username, email=email, dept_id=dept_id
            )

            # 获取分页数据
            total, items = await self.repository.list(
                page=page,
                page_size=page_size,
                search=search_filters,
                order=["-created_at"],
            )

            # 转换数据并关联部门信息
            data = await self._transform_user_list_with_dept(items)

            return SuccessExtra(data=data, total=total, page=page, page_size=page_size)

        except Exception as e:
            self.logger.error(f"获取用户列表失败: {str(e)}")
            return Fail(msg="获取用户列表失败")

    @cached("user_detail", ttl=300)
    async def get_user_detail(self, user_id: int) -> Success:
        """获取用户详情 - 带缓存"""
        try:
            user_obj = await user_repository.get(id=user_id)
            if not user_obj:
                return Fail(msg="用户不存在")

            user_dict = await user_obj.to_dict(m2m=True, exclude_fields=["password"])
            return Success(data=user_dict)

        except Exception as e:
            self.logger.error(f"获取用户详情失败: {str(e)}")
            return Fail(msg="获取用户详情失败")

    async def create_user(self, user_in: UserCreate) -> Success:
        """创建用户 - 包含邮箱唯一性检查和角色分配"""
        try:
            # 检查邮箱是否已存在
            existing_user = await user_repository.get_by_email(user_in.email)
            if existing_user:
                return Fail(
                    code=400,
                    msg="The user with this email already exists in the system.",
                )

            # 创建用户
            new_user = await user_repository.create_user(obj_in=user_in)

            # 更新用户角色
            await user_repository.update_roles(new_user, user_in.role_ids)

            return Success(msg="Created Successfully")

        except Exception as e:
            self.logger.error(f"创建用户失败: {str(e)}")
            return Fail(msg="创建用户失败")

    async def update_user(self, user_in: UserUpdate) -> Success:
        """更新用户 - 包含角色更新和缓存清理"""
        try:
            # 处理密码更新
            update_data = user_in.model_dump(exclude_unset=True)
            if update_data.get('password'):
                from utils.password import get_password_hash
                update_data['password'] = get_password_hash(password=update_data['password'])
            
            # 更新用户基础信息
            user = await user_repository.update(id=user_in.id, obj_in=UserUpdate(**update_data))

            # 更新用户角色
            await user_repository.update_roles(user, user_in.role_ids)

            # 清除相关缓存
            await clear_user_cache(user_in.id)

            return Success(msg="Updated Successfully")

        except Exception as e:
            self.logger.error(f"更新用户失败: {str(e)}")
            return Fail(msg="更新用户失败")

    async def delete_user(self, user_id: int) -> Success:
        """删除用户 - 包含缓存清理"""
        try:
            await user_repository.remove(id=user_id)

            # 清除相关缓存
            await clear_user_cache(user_id)

            return Success(msg="Deleted Successfully")

        except Exception as e:
            self.logger.error(f"删除用户失败: {str(e)}")
            return Fail(msg="删除用户失败")

    async def reset_user_password(self, user_id: int) -> Success:
        """重置用户密码"""
        try:
            await user_repository.reset_password(user_id)
            return Success(msg="密码已重置")

        except Exception as e:
            self.logger.error(f"重置密码失败: {str(e)}")
            return Fail(msg="重置密码失败")

    def _build_user_search_filters(
        self,
        username: str = "",
        email: str = "",
        dept_id: int | None = None,
    ) -> Q:
        """构建用户搜索过滤条件"""
        filters = Q()

        if username:
            filters &= Q(username__contains=username)

        if email:
            filters &= Q(email__contains=email)

        if dept_id is not None:
            filters &= Q(dept_id=dept_id)

        return filters

    async def _transform_user_list_with_dept(self, items) -> list[dict]:
        """转换用户列表数据并关联部门信息"""
        data = []

        for obj in items:
            # 转换用户数据，排除密码字段
            user_dict = await obj.to_dict(m2m=True, exclude_fields=["password"])

            # 关联部门信息
            dept_id = user_dict.pop("dept_id", None)
            if dept_id:
                dept_obj = await dept_repository.get(id=dept_id)
                user_dict["dept"] = await dept_obj.to_dict() if dept_obj else {}
            else:
                user_dict["dept"] = {}

            data.append(user_dict)

        return data

    async def update_user_avatar(self, user_id: int, avatar_url: str) -> Success:
        """更新用户头像"""
        try:
            # 验证用户是否存在
            user = await user_repository.get(id=user_id)
            if not user:
                return Fail(msg="用户不存在")
            
            # 验证头像URL
            if not avatar_url:
                return Fail(msg="头像URL不能为空")
            
            # 更新用户头像
            await user_repository.update(id=user_id, obj_in={"avatar": avatar_url})
            
            # 清除相关缓存
            await clear_user_cache(user_id)
            
            self.logger.info(f"用户 {user_id} 头像已更新为: {avatar_url}")
            
            return Success(msg="头像更新成功", data={"avatar": avatar_url})
            
        except Exception as e:
            self.logger.error(f"更新用户头像失败: {str(e)}")
            return Fail(msg="更新用户头像失败")

    async def update_user_profile(self, user_id: int, profile_data: ProfileUpdate) -> Success:
        """更新用户个人资料"""
        try:
            # 过滤掉空值
            update_data = {k: v for k, v in profile_data.model_dump().items() if v is not None}
            
            if not update_data:
                return Fail(msg="没有需要更新的数据")
            
            await user_repository.update(id=user_id, obj_in=update_data)
            
            # 清除相关缓存
            await clear_user_cache(user_id)
            
            return Success(msg="个人资料更新成功")
            
        except Exception as e:
            self.logger.error(f"更新用户个人资料失败: {str(e)}")
            return Fail(msg="更新用户个人资料失败")

    async def delete_user_avatar(self, user_id: int) -> Success:
        """删除用户头像"""
        try:
            await user_repository.update(id=user_id, obj_in={"avatar": None})
            
            # 清除相关缓存
            await clear_user_cache(user_id)
            
            return Success(msg="头像删除成功")
            
        except Exception as e:
            self.logger.error(f"删除用户头像失败: {str(e)}")
            return Fail(msg="删除用户头像失败")

    async def change_user_password(self, user_id: int, old_password: str, new_password: str) -> Success:
        """用户修改密码"""
        try:
            from utils.password import verify_password, get_password_hash
            
            # 获取用户信息
            user = await user_repository.get(id=user_id)
            if not user:
                return Fail(msg="用户不存在")
            
            # 验证旧密码
            if not verify_password(old_password, user.password):
                return Fail(code=400, msg="旧密码验证错误")
            
            # 检查新密码是否与旧密码相同
            if verify_password(new_password, user.password):
                return Fail(code=400, msg="新密码不能与旧密码相同")
            
            # 更新密码
            hashed_new_password = get_password_hash(new_password)
            await user_repository.update(id=user_id, obj_in={"password": hashed_new_password})
            
            # 清除相关缓存
            await clear_user_cache(user_id)
            
            return Success(msg="密码修改成功")
            
        except Exception as e:
            self.logger.error(f"修改密码失败: {str(e)}")
            return Fail(msg="修改密码失败")


# 全局实例
user_service = UserService()
