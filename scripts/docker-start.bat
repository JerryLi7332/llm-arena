@echo off
REM ============================================
REM LLM Arena - Windows Docker 一键启动脚本
REM ============================================

REM 切换到项目根目录（脚本所在目录的上级）
cd /d "%~dp0\.."

echo ============================================
echo 🚀 LLM Arena Docker 部署脚本
echo ============================================
echo.
echo 📁 工作目录: %CD%
echo.

REM 检查 Docker 是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到 Docker，请先安装 Docker Desktop
    echo    下载地址: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到 docker-compose
    echo    请确保 Docker Desktop 正确安装
    pause
    exit /b 1
)

echo ✅ Docker 环境检查通过
echo.

REM 检查 .env 文件
if not exist ".env" (
    echo ⚠️  警告: 未找到 .env 文件
    if exist "config\docker\.env.docker" (
        echo    正在从 config\docker\.env.docker 复制...
        copy config\docker\.env.docker .env
    ) else if exist ".env.example" (
        echo    正在从 .env.example 复制...
        copy .env.example .env
    ) else (
        echo    ❌ 错误: 找不到任何环境配置模板
        pause
        exit /b 1
    )
    echo.
    echo ⚠️  请编辑 .env 文件，配置以下项目：
    echo    - SECRET_KEY ^(必须修改^)
    echo    - DEEPSEEK_API_KEY ^(必须配置^)
    echo    - DB_PASSWORD ^(建议修改^)
    echo.
    pause
)

REM 选择操作
echo 请选择操作:
echo [1] 首次部署 ^(构建镜像 + 启动服务^)
echo [2] 启动服务 ^(使用现有镜像^)
echo [3] 重新构建并启动
echo [4] 停止服务
echo [5] 查看日志
echo [6] 清理所有数据 ^(危险操作^)
echo [0] 退出
echo.

set /p choice=请输入选项 [0-6]: 

if "%choice%"=="1" goto first_deploy
if "%choice%"=="2" goto start
if "%choice%"=="3" goto rebuild
if "%choice%"=="4" goto stop
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto clean
if "%choice%"=="0" goto end
goto invalid

:first_deploy
echo.
echo 🔨 首次部署: 构建镜像并启动服务...
echo.
docker-compose -f config\docker\docker-compose.yml build --no-cache
if errorlevel 1 (
    echo ❌ 镜像构建失败
    pause
    exit /b 1
)
docker-compose -f config\docker\docker-compose.yml up -d
if errorlevel 1 (
    echo ❌ 服务启动失败
    pause
    exit /b 1
)
goto success

:start
echo.
echo 🚀 启动服务...
echo.
docker-compose -f config\docker\docker-compose.yml up -d
if errorlevel 1 (
    echo ❌ 服务启动失败
    pause
    exit /b 1
)
goto success

:rebuild
echo.
echo 🔨 重新构建镜像并启动...
echo.
docker-compose -f config\docker\docker-compose.yml down
docker-compose -f config\docker\docker-compose.yml build --no-cache
docker-compose -f config\docker\docker-compose.yml up -d
if errorlevel 1 (
    echo ❌ 操作失败
    pause
    exit /b 1
)
goto success

:stop
echo.
echo 🛑 停止服务...
echo.
docker-compose -f config\docker\docker-compose.yml down
echo ✅ 服务已停止
pause
goto end

:logs
echo.
echo 📋 查看实时日志 ^(Ctrl+C 退出^)...
echo.
docker-compose -f config\docker\docker-compose.yml logs -f
goto end

:clean
echo.
echo ⚠️  警告: 此操作将删除所有容器、镜像和数据卷！
echo    数据库数据将会丢失，请谨慎操作！
echo.
set /p confirm=确认清理? [y/N]: 
if /i not "%confirm%"=="y" (
    echo 操作已取消
    pause
    goto end
)
echo.
echo 🗑️  清理中...
docker-compose -f config\docker\docker-compose.yml down -v
docker rmi llm-arena-backend 2>nul
echo ✅ 清理完成
pause
goto end

:invalid
echo ❌ 无效选项
pause
goto end

:success
echo.
echo ============================================
echo ✅ 操作成功！
echo ============================================
echo.
echo 📊 服务状态:
docker-compose -f config\docker\docker-compose.yml ps
echo.
echo 🌐 访问地址:
echo    - 后端 API:      http://localhost:8000
echo    - API 文档:      http://localhost:8000/docs
echo    - 前端页面:      http://localhost (如果启用了 nginx)
echo.
echo 💡 常用命令:
echo    查看日志:        docker-compose -f config\docker\docker-compose.yml logs -f
echo    进入容器:        docker-compose -f config\docker\docker-compose.yml exec backend bash
echo    重启服务:        docker-compose -f config\docker\docker-compose.yml restart
echo    停止服务:        docker-compose -f config\docker\docker-compose.yml down
echo.
pause

:end
