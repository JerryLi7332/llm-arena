-- LLM Arena 数据库初始化脚本

-- 设置字符集
SET client_encoding = 'UTF8';

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 输出初始化信息
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'LLM Arena 数据库初始化完成';
    RAISE NOTICE '数据库: %', current_database();
    RAISE NOTICE '用户: %', current_user();
    RAISE NOTICE '========================================';
END $$;
