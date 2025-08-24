from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
import os

from core.dependency import DependAuth, DependPermisson
from core.crud import CRUD
from models.games import AICode
from models import User
from schemas.games import AICodeCreate, AICodeUpdate, AICodeResponse
from services.file_service import file_service
from services.user_service import user_service

ai_codes_router = APIRouter()

# 获取当前用户
async def get_current_user_id(current_user: User = DependAuth):
    return current_user.id

@ai_codes_router.get(
    "/{game_type}",
    summary="获取指定游戏的AI代码列表",
    response_model=List[AICodeResponse]
)
async def get_game_ai_codes(
    game_type: str,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    获取指定游戏类型的AI代码列表
    
    Args:
        game_type: 游戏类型 (rock_paper_scissors, avalon)
        current_user_id: 当前用户ID
    
    Returns:
        AI代码列表
    """
    # 验证游戏类型
    valid_game_types = ["rock_paper_scissors", "avalon"]
    if game_type not in valid_game_types:
        raise HTTPException(status_code=400, detail="不支持的游戏类型")
    
    # 获取用户的AI代码
    ai_codes = await CRUD(AICode).get_multi(
        user_id=current_user_id,
        game_type=game_type
    )
    
    return ai_codes

@ai_codes_router.post(
    "/{game_type}/upload",
    summary="上传游戏AI代码",
    response_model=AICodeResponse
)
async def upload_game_ai_code(
    game_type: str,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    上传游戏AI代码
    
    Args:
        game_type: 游戏类型
        name: AI代码名称
        description: AI代码描述
        file: 代码文件
        current_user_id: 当前用户ID
    
    Returns:
        上传成功的AI代码信息
    """
    # 验证游戏类型
    valid_game_types = ["rock_paper_scissors", "avalon"]
    if game_type not in valid_game_types:
        raise HTTPException(status_code=400, detail="不支持的游戏类型")
    
    # 验证文件类型
    allowed_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.zip', '.rar']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    # 验证文件大小 (10MB)
    max_size = 10 * 1024 * 1024
    if file.size > max_size:
        raise HTTPException(status_code=400, detail="文件大小不能超过10MB")
    
    try:
        # 在文件服务读取文件之前，先保存文件信息
        original_filename = file.filename
        original_size = file.size
        
        # 上传文件
        file_info = await file_service.upload_file(file)
        
        # 计算文件哈希值（使用已保存的文件信息）
        import hashlib
        file_hash = hashlib.md5(f"{original_filename}_{original_size}".encode()).hexdigest()
        
        # 从Success响应中获取文件路径
        # file_info是一个Success对象，需要通过content属性访问数据
        file_path = ""
        if hasattr(file_info, 'content') and isinstance(file_info.content, dict):
            file_path = file_info.content.get("data", {}).get("file_path", "")
        
        # 创建AI代码记录
        ai_code_data = AICodeCreate(
            user_id=current_user_id,
            name=name,
            description=description,
            game_type=game_type,
            file_path=file_path,
            file_name=original_filename,
            file_size=original_size,
            file_hash=file_hash,
            version=1,
            is_active=False
        )
        
        # 保存到数据库
        ai_code = await CRUD(AICode).create(ai_code_data.model_dump())
        
        return ai_code
        
    except Exception as e:
        # 记录详细错误信息
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"上传AI代码失败: {str(e)}")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"错误详情: {e}")
        
        # 如果是数据库错误，提供更具体的错误信息
        if "database" in str(e).lower() or "sql" in str(e).lower():
            raise HTTPException(status_code=500, detail="数据库操作失败，请检查数据格式")
        elif "validation" in str(e).lower():
            raise HTTPException(status_code=400, detail="数据验证失败，请检查输入参数")
        else:
            raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")

@ai_codes_router.post(
    "/{ai_code_id}/activate",
    summary="激活AI代码",
    response_model=AICodeResponse
)
async def activate_ai_code(
    ai_code_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    激活指定的AI代码
    
    Args:
        ai_code_id: AI代码ID
        current_user_id: 当前用户ID
    
    Returns:
        激活后的AI代码信息
    """
    # 获取AI代码
    ai_code = await CRUD(AICode).get(ai_code_id)
    if not ai_code:
        raise HTTPException(status_code=404, detail="AI代码不存在")
    
    # 验证所有权
    if ai_code.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="无权限操作此AI代码")
    
    try:
        # 先停用同游戏类型的其他AI代码
        await CRUD(AICode).update_multi(
            {"user_id": current_user_id, "game_type": ai_code.game_type},
            {"is_active": False}
        )
        
        # 激活当前AI代码
        updated_ai_code = await CRUD(AICode).update(
            ai_code_id,
            {"is_active": True}
        )
        
        return updated_ai_code
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"激活失败: {str(e)}")

@ai_codes_router.get(
    "/{ai_code_id}/download",
    summary="下载AI代码文件"
)
async def download_ai_code(
    ai_code_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    下载AI代码文件
    
    Args:
        ai_code_id: AI代码ID
        current_user_id: 当前用户ID
    
    Returns:
        文件内容
    """
    # 获取AI代码
    ai_code = await CRUD(AICode).get(ai_code_id)
    if not ai_code:
        raise HTTPException(status_code=404, detail="AI代码不存在")
    
    # 验证所有权
    if ai_code.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="无权限下载此AI代码")
    
    try:
        # 从文件服务下载文件
        file_content = await file_service.download_file(ai_code.file_path)
        
        # 更新最后使用时间
        await CRUD(AICode).update(
            ai_code_id,
            {"last_used": "now()"}
        )
        
        return file_content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载失败: {str(e)}")

@ai_codes_router.get(
    "/{ai_code_id}",
    summary="获取AI代码详情",
    response_model=AICodeResponse
)
async def get_ai_code_detail(
    ai_code_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    获取AI代码详情
    
    Args:
        ai_code_id: AI代码ID
        current_user_id: 当前用户ID
    
    Returns:
        AI代码详情
    """
    # 获取AI代码
    ai_code = await CRUD(AICode).get(ai_code_id)
    if not ai_code:
        raise HTTPException(status_code=404, detail="AI代码不存在")
    
    # 验证所有权
    if ai_code.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="无权限查看此AI代码")
    
    return ai_code

@ai_codes_router.put(
    "/{ai_code_id}",
    summary="更新AI代码信息",
    response_model=AICodeResponse
)
async def update_ai_code(
    ai_code_id: int,
    ai_code_update: AICodeUpdate,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    更新AI代码信息
    
    Args:
        ai_code_id: AI代码ID
        ai_code_update: 更新的AI代码信息
        current_user_id: 当前用户ID
    
    Returns:
        更新后的AI代码信息
    """
    # 获取AI代码
    ai_code = await CRUD(AICode).get(ai_code_id)
    if not ai_code:
        raise HTTPException(status_code=404, detail="AI代码不存在")
    
    # 验证所有权
    if ai_code.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="无权限更新此AI代码")
    
    try:
        # 更新AI代码
        updated_ai_code = await CRUD(AICode).update(
            ai_code_id,
            ai_code_update.model_dump(exclude_unset=True)
        )
        
        return updated_ai_code
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新失败: {str(e)}")

@ai_codes_router.delete(
    "/{ai_code_id}",
    summary="删除AI代码"
)
async def delete_ai_code(
    ai_code_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    删除AI代码
    
    Args:
        ai_code_id: AI代码ID
        current_user_id: 当前用户ID
    
    Returns:
        删除结果
    """
    # 获取AI代码
    ai_code = await CRUD(AICode).get(ai_code_id)
    if not ai_code:
        raise HTTPException(status_code=404, detail="AI代码不存在")
    
    # 验证所有权
    if ai_code.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="无权限删除此AI代码")
    
    try:
        # 删除文件
        if ai_code.file_path:
            await file_service.delete_file(ai_code.file_path)
        
        # 删除数据库记录
        await CRUD(AICode).delete(ai_code_id)
        
        return {"message": "删除成功"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")
