"""
AI系统诊断脚本
Diagnostic script for AI system
"""

import sys
import os
import io

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

print("=" * 60)
print("AI系统诊断 | AI System Diagnosis")
print("=" * 60)

# 1. 检查Python版本
print("\n1. Python版本检查 | Python Version Check")
print(f"   Python版本: {sys.version}")

# 2. 检查必需的库
print("\n2. 库安装检查 | Library Installation Check")
required_libs = {
    'anthropic': 'Claude API',
    'openai': 'OpenAI API',
    'streamlit': 'Streamlit',
    'PIL': 'Pillow (图像处理)',
    'cv2': 'OpenCV'
}

installed_libs = {}
for lib, desc in required_libs.items():
    try:
        if lib == 'PIL':
            import PIL
            installed_libs[lib] = True
            print(f"   ✅ {desc} - 已安装 (版本: {PIL.__version__})")
        elif lib == 'cv2':
            import cv2
            installed_libs[lib] = True
            print(f"   ✅ {desc} - 已安装 (版本: {cv2.__version__})")
        elif lib == 'anthropic':
            import anthropic
            installed_libs[lib] = True
            print(f"   ✅ {desc} - 已安装 (版本: {anthropic.__version__})")
        elif lib == 'openai':
            import openai
            installed_libs[lib] = True
            print(f"   ✅ {desc} - 已安装 (版本: {openai.__version__})")
        elif lib == 'streamlit':
            import streamlit
            installed_libs[lib] = True
            print(f"   ✅ {desc} - 已安装 (版本: {streamlit.__version__})")
    except ImportError:
        installed_libs[lib] = False
        print(f"   ❌ {desc} - 未安装")

# 3. 检查AI服务模块
print("\n3. AI服务模块检查 | AI Service Module Check")
try:
    from ai_services import AIServiceManager, ClaudeService, OpenAIService
    print("   ✅ ai_services.py - 导入成功")

    # 检查可用服务
    services = AIServiceManager.get_available_services()
    print("\n   可用服务 | Available Services:")
    for service, available in services.items():
        status = "✅ 可用" if available else "❌ 不可用"
        print(f"   - {service}: {status}")
except Exception as e:
    print(f"   ❌ ai_services.py - 导入失败: {e}")

# 4. 检查环境变量
print("\n4. 环境变量检查 | Environment Variables Check")
claude_key = os.getenv('ANTHROPIC_API_KEY', '')
openai_key = os.getenv('OPENAI_API_KEY', '')

if claude_key:
    print(f"   ✅ ANTHROPIC_API_KEY - 已设置 (前20字符: {claude_key[:20]}...)")
else:
    print("   ⚠️  ANTHROPIC_API_KEY - 未设置")

if openai_key:
    print(f"   ✅ OPENAI_API_KEY - 已设置 (前20字符: {openai_key[:20]}...)")
else:
    print("   ⚠️  OPENAI_API_KEY - 未设置")

# 5. 测试Claude API连接
print("\n5. Claude API连接测试 | Claude API Connection Test")
if installed_libs.get('anthropic', False):
    test_key = claude_key  # 直接使用环境变量中的密钥

    if test_key:
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=test_key)

            # 简单测试
            print("   正在测试API连接...")
            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=50,
                messages=[
                    {"role": "user", "content": "Say hello in Chinese"}
                ]
            )

            response = message.content[0].text
            print(f"   ✅ API连接成功!")
            print(f"   测试响应: {response}")
        except Exception as e:
            print(f"   ❌ API连接失败: {str(e)}")
    else:
        print("   ⏭️  跳过API测试")
else:
    print("   ❌ anthropic库未安装，无法测试")

# 6. 测试图像分析功能
print("\n6. 图像分析功能测试 | Image Analysis Function Test")
try:
    from PIL import Image
    from ai_services import AIServiceManager, ClaudeService

    # 创建测试图像
    test_image = Image.new('RGB', (300, 300), color=(200, 180, 160))
    print("   ✅ 测试图像创建成功")

    # 测试Claude分析（如果有API密钥）
    if test_key and installed_libs.get('anthropic', False):
        print("   正在测试图像分析...")
        try:
            claude_service = ClaudeService(test_key)
            result = claude_service.analyze_scalp_image(test_image, language='zh')

            if 'error' in result:
                print(f"   ❌ 图像分析失败: {result.get('error')}")
            else:
                print(f"   ✅ 图像分析成功!")
                print(f"   头皮类型: {result.get('scalp_type', 'Unknown')}")
                print(f"   健康评分: {result.get('health_score', 0)}")
        except Exception as e:
            print(f"   ❌ 图像分析失败: {str(e)}")
    else:
        print("   ⏭️  跳过图像分析测试（无API密钥）")

except Exception as e:
    print(f"   ❌ 图像分析功能测试失败: {str(e)}")

# 7. 诊断总结
print("\n" + "=" * 60)
print("诊断总结 | Diagnosis Summary")
print("=" * 60)

issues = []
if not installed_libs.get('anthropic', False):
    issues.append("anthropic库未安装 - 运行: pip install anthropic")
if not installed_libs.get('openai', False):
    issues.append("openai库未安装 - 运行: pip install openai")
if not claude_key and not openai_key:
    issues.append("未设置API密钥 - 在AI Settings页面配置或设置环境变量")

if issues:
    print("\n⚠️  发现以下问题 | Issues Found:")
    for i, issue in enumerate(issues, 1):
        print(f"   {i}. {issue}")

    print("\n建议修复步骤 | Recommended Fix Steps:")
    print("   1. 安装缺失的库: pip install anthropic openai")
    print("   2. 在Streamlit应用的AI Settings页面配置API密钥")
    print("   3. 或设置环境变量: set ANTHROPIC_API_KEY=your-key-here")
else:
    print("\n✅ 所有检查通过! AI系统应该可以正常工作")

print("\n" + "=" * 60)
print("诊断完成 | Diagnosis Complete")
print("=" * 60)
