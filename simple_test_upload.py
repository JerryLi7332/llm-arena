#!/usr/bin/env python3
"""
简单的AI代码上传测试脚本
"""

import asyncio
import httpx
from pathlib import Path

async def test_simple_upload():
    """简单的上传测试"""
    print("🧪 开始简单上传测试...")
    
    # 创建测试文件
    test_file = Path("simple_test.py")
    test_content = "print('Hello, AI!')"
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        # 测试文件读取
        print(f"📁 测试文件信息:")
        print(f"  - 文件名: {test_file.name}")
        print(f"  - 文件大小: {test_file.stat().st_size} 字节")
        print(f"  - 文件内容: {test_content}")
        
        # 模拟文件上传过程
        print(f"\n📤 模拟文件上传过程...")
        
        # 1. 读取文件内容
        with open(test_file, "rb") as f:
            content = f.read()
            print(f"  ✅ 文件读取成功，内容长度: {len(content)} 字节")
        
        # 2. 验证文件大小
        if len(content) < 1024 * 1024:  # 1MB
            print(f"  ✅ 文件大小验证通过")
        else:
            print(f"  ❌ 文件大小超过限制")
            return
        
        # 3. 生成文件哈希
        import hashlib
        file_hash = hashlib.md5(f"{test_file.name}_{len(content)}".encode()).hexdigest()
        print(f"  ✅ 文件哈希生成成功: {file_hash[:16]}...")
        
        # 4. 模拟保存文件
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        safe_filename = f"test_{file_hash[:8]}.py"
        upload_path = upload_dir / safe_filename
        
        with open(upload_path, "wb") as f:
            f.write(content)
        print(f"  ✅ 文件保存成功: {upload_path}")
        
        print(f"\n🎉 模拟上传流程完成！")
        print(f"  - 原始文件: {test_file}")
        print(f"  - 上传路径: {upload_path}")
        print(f"  - 文件哈希: {file_hash}")
        
        # 清理测试文件
        if upload_path.exists():
            upload_path.unlink()
            print(f"  🧹 已清理测试文件")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理原始测试文件
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    asyncio.run(test_simple_upload())
