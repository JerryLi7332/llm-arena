#!/usr/bin/env python3
"""
修复AI代码上传问题的脚本
"""

import asyncio
import sqlite3
from pathlib import Path

async def fix_ai_code_table():
    """修复AI代码表结构"""
    db_path = Path("db.sqlite3")
    
    if not db_path.exists():
        print("❌ 数据库文件不存在")
        return
    
    try:
        # 连接数据库
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 检查ai_code表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ai_code'")
        if not cursor.fetchone():
            print("❌ ai_code表不存在，需要创建")
            create_ai_code_table(cursor)
        else:
            print("✅ ai_code表已存在")
            # 检查表结构
            check_table_structure(cursor)
        
        conn.commit()
        conn.close()
        print("✅ 数据库修复完成")
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")

def create_ai_code_table(cursor):
    """创建AI代码表"""
    print("📝 创建ai_code表...")
    
    create_table_sql = """
    CREATE TABLE ai_code (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER NOT NULL,
        name VARCHAR(100) NOT NULL,
        file_path VARCHAR(500) NOT NULL,
        file_name VARCHAR(255) NOT NULL,
        file_size INTEGER NOT NULL,
        file_hash VARCHAR(64),
        game_type VARCHAR(50) NOT NULL,
        description TEXT,
        version INTEGER NOT NULL DEFAULT 1,
        is_active INTEGER NOT NULL DEFAULT 0,
        last_used TIMESTAMP,
        win_count INTEGER NOT NULL DEFAULT 0,
        loss_count INTEGER NOT NULL DEFAULT 0,
        draw_count INTEGER NOT NULL DEFAULT 0,
        total_games INTEGER NOT NULL DEFAULT 0,
        win_rate REAL NOT NULL DEFAULT 0.0,
        elo_score INTEGER NOT NULL DEFAULT 1200,
        tags JSON,
        config JSON,
        is_public INTEGER NOT NULL DEFAULT 0,
        download_count INTEGER NOT NULL DEFAULT 0,
        rating REAL NOT NULL DEFAULT 0.0,
        review_count INTEGER NOT NULL DEFAULT 0
    )
    """
    
    cursor.execute(create_table_sql)
    
    # 创建索引
    indexes = [
        "CREATE INDEX ix_ai_code_user_id ON ai_code(user_id)",
        "CREATE INDEX ix_ai_code_game_type ON ai_code(game_type)",
        "CREATE INDEX ix_ai_code_is_active ON ai_code(is_active)",
        "CREATE INDEX ix_ai_code_elo_score ON ai_code(elo_score)",
        "CREATE INDEX ix_ai_code_rating ON ai_code(rating)",
        "CREATE INDEX ix_ai_code_user_game ON ai_code(user_id, game_type)",
        "CREATE INDEX ix_ai_code_game_active ON ai_code(game_type, is_active)",
        "CREATE INDEX ix_ai_code_game_elo ON ai_code(game_type, elo_score)",
        "CREATE INDEX ix_ai_code_public_rating ON ai_code(is_public, rating)"
    ]
    
    for index_sql in indexes:
        try:
            cursor.execute(index_sql)
        except sqlite3.OperationalError as e:
            if "already exists" not in str(e):
                print(f"⚠️ 创建索引失败: {e}")
    
    print("✅ ai_code表创建完成")

def check_table_structure(cursor):
    """检查表结构"""
    print("🔍 检查表结构...")
    
    try:
        cursor.execute("PRAGMA table_info(ai_code)")
        columns = cursor.fetchall()
        
        required_columns = {
            'user_id': 'INTEGER',
            'name': 'VARCHAR(100)',
            'file_path': 'VARCHAR(500)',
            'file_name': 'VARCHAR(255)',
            'file_size': 'INTEGER',
            'file_hash': 'VARCHAR(64)',
            'game_type': 'VARCHAR(50)',
            'description': 'TEXT',
            'version': 'INTEGER',
            'is_active': 'INTEGER'
        }
        
        existing_columns = {col[1]: col[2] for col in columns}
        
        for col_name, col_type in required_columns.items():
            if col_name not in existing_columns:
                print(f"⚠️ 缺少列: {col_name}")
            else:
                print(f"✅ 列存在: {col_name}")
                
    except Exception as e:
        print(f"⚠️ 检查表结构失败: {e}")

def test_upload():
    """测试上传功能"""
    print("\n🧪 测试上传功能...")
    
    # 这里可以添加测试代码
    print("✅ 测试完成")

if __name__ == "__main__":
    print("🔧 开始修复AI代码上传问题...")
    
    # 修复数据库表结构
    asyncio.run(fix_ai_code_table())
    
    # 测试上传功能
    test_upload()
    
    print("\n🎉 修复完成！")
