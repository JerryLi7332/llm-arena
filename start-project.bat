@echo off
REM 项目启动脚本
REM 使用方法: start-project.bat

echo 🚀 启动 Vue FastAPI Admin 项目...

REM 检查是否在项目根目录
if not exist "src\__init__.py" (
    echo ❌ 错误: 请在项目根目录下运行此脚本
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ❌ 错误: 请在项目根目录下运行此脚本
    pause
    exit /b 1
)

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ 错误: 未找到Python，请先安装Python
        pause
        exit /b 1
    )
)

REM 检查Node.js环境
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Node.js，请先安装Node.js
    pause
    exit /b 1
)

REM 检查前端是否已构建
if not exist "frontend\dist\index.html" (
    echo 📦 前端未构建，开始构建前端...
    cd frontend
    call npm install
    if errorlevel 1 (
        echo ❌ 错误: 前端依赖安装失败
        pause
        exit /b 1
    )
    call npm run build
    if errorlevel 1 (
        echo ❌ 错误: 前端构建失败
        pause
        exit /b 1
    )
    cd ..
    echo ✅ 前端构建完成
) else (
    echo ✅ 前端已构建，跳过构建步骤
)

REM 检查Python依赖
if not exist "venv" (
    if not exist ".venv" (
        echo 📦 创建Python虚拟环境...
        python -m venv venv
        if errorlevel 1 (
            echo ❌ 错误: 虚拟环境创建失败
            pause
            exit /b 1
        )
    )
)

REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM 安装Python依赖
echo 📦 安装Python依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 错误: Python依赖安装失败
    pause
    exit /b 1
)

REM 启动后端服务
echo 🚀 启动后端服务...
echo 📝 服务地址: http://localhost:8000
echo 📚 API文档: http://localhost:8000/docs
echo 🔑 默认管理员账号: admin / abcd1234
echo.
echo 按 Ctrl+C 停止服务

uvicorn src:app --host 0.0.0.0 --port 8000 --reload


