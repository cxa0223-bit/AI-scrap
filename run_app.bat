@echo off
echo ================================
echo 启动头皮分析应用
echo Starting Scalp Analyzer App
echo ================================
echo.

REM 检查是否已设置API密钥
if "%ANTHROPIC_API_KEY%"=="" (
    echo 警告：Claude API密钥未设置
    echo Warning: Claude API key not set
    echo.
    echo 请先运行 set_claude_key.bat 设置API密钥
    echo Please run set_claude_key.bat first to set API key
    echo.
    echo 或者在应用内的AI Settings页面进行设置
    echo Or configure it in the AI Settings page within the app
    echo.
)

echo 正在启动应用... / Starting app...
echo.
python -m streamlit run app.py

pause