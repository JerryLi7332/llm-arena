from fastapi import APIRouter, Body, Query, UploadFile, File, Depends, HTTPException
from typing import Optional
import os

from schemas.users import UserCreate, UserUpdate, AvatarUpload, ProfileUpdate, UpdatePassword
from services.user_service import user_service
from services.file_service import file_service
from core.dependency import DependAuth, DependPermisson
from core.ctx import CTX_USER_ID
from models import User

router = APIRouter()


@router.get("/list", summary="查看用户列表", dependencies=[DependPermisson])
async def list_user(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    username: str = Query("", description="用户名称，用于搜索"),
    email: str = Query("", description="邮箱地址"),
    dept_id: int = Query(None, description="部门ID"),
):
    return await user_service.get_user_list(
        page=page,
        page_size=page_size,
        username=username,
        email=email,
        dept_id=dept_id,
    )


@router.get("/get", summary="查看用户", dependencies=[DependPermisson])
async def get_user(
    user_id: int = Query(..., description="用户ID"),
):
    return await user_service.get_user_detail(user_id)


@router.post("/create", summary="创建用户", dependencies=[DependPermisson])
async def create_user(
    user_in: UserCreate,
):
    return await user_service.create_user(user_in)


@router.post("/update", summary="更新用户", dependencies=[DependPermisson])
async def update_user(
    user_in: UserUpdate,
):
    return await user_service.update_user(user_in)


@router.delete("/delete", summary="删除用户", dependencies=[DependPermisson])
async def delete_user(
    user_id: int = Query(..., description="用户ID"),
):
    return await user_service.delete_user(user_id)


@router.post("/reset_password", summary="重置密码", dependencies=[DependPermisson])
async def reset_password(user_id: int = Body(..., description="用户ID", embed=True)):
    return await user_service.reset_user_password(user_id)


@router.post("/upload_avatar", summary="上传用户头像")
async def upload_avatar(
    file: UploadFile = File(..., description="头像文件"),
    current_user: User = DependAuth
):
    """
    上传用户头像
    
    Args:
        file: 头像文件
        current_user: 当前用户
        
    Returns:
        头像上传结果
    """
    # 验证文件是否存在
    if not file.filename:
        raise HTTPException(status_code=400, detail="请选择要上传的文件")
    
    # 验证文件类型
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="只支持 JPG、PNG、GIF、WebP 格式的图片")
    
    # 验证文件大小 (2MB)
    max_size = 2 * 1024 * 1024
    if file.size and file.size > max_size:
        raise HTTPException(status_code=400, detail="头像文件大小不能超过 2MB")
    
    try:
        # 设置用户上下文，供文件服务使用
        CTX_USER_ID.set(current_user.id)
        
        # 上传文件
        file_info = await file_service.upload_file(file)
        
        # 检查上传结果 - Success对象没有success属性，需要检查状态码
        if hasattr(file_info, 'status_code') and file_info.status_code != 200:
            raise HTTPException(status_code=500, detail="文件上传失败")
        
        # 获取文件路径 - 直接使用文件服务返回的数据
        # file_service.upload_file() 返回的是 Success 对象，直接访问 data 属性
        file_path = ""
        
        try:
            # 从Success对象的data属性中获取文件路径
            if hasattr(file_info, 'data') and file_info.data:
                data = file_info.data
                if isinstance(data, dict) and 'file_path' in data:
                    file_path = data['file_path']
                    print(f"DEBUG: 从文件服务获取路径: {file_path}")
        except Exception as e:
            print(f"DEBUG: 解析文件信息失败: {e}")
        
        if not file_path:
            # 如果还是没找到，使用文件映射来获取路径
            try:
                from repositories.file_mapping import file_mapping_repository
                # 获取最新的文件映射记录
                latest_file = await file_mapping_repository.get_latest_by_user(current_user.id)
                if latest_file:
                    file_path = latest_file.file_path
                    print(f"DEBUG: 从文件映射获取路径: {file_path}")
            except Exception as e:
                print(f"DEBUG: 从文件映射获取路径失败: {e}")
        
        if not file_path:
            raise HTTPException(status_code=500, detail="文件上传失败，未获取到文件路径")
        
        # 更新用户头像
        result = await user_service.update_user_avatar(current_user.id, file_path)
        if hasattr(result, 'status_code') and result.status_code != 200:
            raise HTTPException(status_code=500, detail=result.msg)
        
        # 确保路径使用正斜杠，兼容前端
        normalized_path = file_path.replace('\\', '/')
        
        return AvatarUpload(
            avatar_url=normalized_path,
            message="头像上传成功"
        )
        
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        # 记录详细错误信息
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"头像上传失败: {str(e)}")


@router.put("/profile", summary="更新个人资料")
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = DependAuth
):
    """
    更新个人资料
    
    Args:
        profile_data: 个人资料数据
        current_user: 当前用户
        
    Returns:
        更新结果
    """
    try:
        # 更新用户资料
        result = await user_service.update_user_profile(current_user.id, profile_data)
        if hasattr(result, 'status_code') and result.status_code != 200:
            raise HTTPException(status_code=500, detail=result.msg)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新个人资料失败: {str(e)}")


@router.delete("/avatar", summary="删除用户头像")
async def delete_avatar(current_user: User = DependAuth):
    """
    删除用户头像
    
    Args:
        current_user: 当前用户
        
    Returns:
        删除结果
    """
    try:
        # 删除用户头像
        result = await user_service.delete_user_avatar(current_user.id)
        if hasattr(result, 'status_code') and result.status_code != 200:
            raise HTTPException(status_code=500, detail=result.msg)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除头像失败: {str(e)}")


@router.put("/password", summary="修改密码")
async def change_password(
    password_data: UpdatePassword,
    current_user: User = DependAuth
):
    """
    修改用户密码
    
    Args:
        password_data: 密码修改数据（包含旧密码和新密码）
        current_user: 当前用户
        
    Returns:
        修改结果
    """
    try:
        # 修改用户密码
        result = await user_service.change_user_password(
            user_id=current_user.id,
            old_password=password_data.old_password,
            new_password=password_data.new_password
        )
        
        if hasattr(result, 'status_code') and result.status_code != 200:
            # 根据错误代码返回不同的HTTP状态码
            status_code = result.status_code if result.status_code != 200 else 500
            raise HTTPException(status_code=status_code, detail=result.msg)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修改密码失败: {str(e)}")
