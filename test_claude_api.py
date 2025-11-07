"""
测试Claude API密钥
Test Claude API Key
"""

import sys
import io

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 60)
print("Claude API密钥测试 | Claude API Key Test")
print("=" * 60)

# 测试API密钥（请替换为你的实际密钥）
import os
api_key = os.getenv("ANTHROPIC_API_KEY", "your-claude-api-key-here")

print(f"\n密钥预览: {api_key[:25]}...")
print(f"密钥长度: {len(api_key)} 字符")

# 检查anthropic库
print("\n1. 检查anthropic库...")
try:
    from anthropic import Anthropic
    print("   ✅ anthropic库已安装")
except ImportError as e:
    print(f"   ❌ anthropic库未安装: {e}")
    print("   请运行: pip install anthropic")
    sys.exit(1)

# 测试API连接
print("\n2. 测试API连接...")
print("   正在发送测试请求到Claude API...")

try:
    client = Anthropic(api_key=api_key)

    # 发送简单的测试消息
    message = client.messages.create(
        model="claude-3-haiku-20240307",  # 使用Claude 3 Haiku模型（你的账户可用）
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": "请用中文回复'API测试成功！你的Claude账户工作正常。'"
            }
        ]
    )

    response = message.content[0].text

    print("\n" + "=" * 60)
    print("✅ 测试成功！| Test Successful!")
    print("=" * 60)
    print(f"\nClaude响应: {response}")
    print(f"\n使用模型: {message.model}")
    print(f"使用Token数: {message.usage.input_tokens} (输入) + {message.usage.output_tokens} (输出)")
    print(f"总计: {message.usage.input_tokens + message.usage.output_tokens} tokens")

    # 测试图像分析能力
    print("\n3. 测试图像分析能力...")
    from PIL import Image
    import base64
    import io as io_module

    # 创建测试图像
    test_image = Image.new('RGB', (300, 300), color=(200, 180, 160))
    buffered = io_module.BytesIO()
    test_image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    print("   正在测试图像分析...")

    message = client.messages.create(
        model="claude-3-haiku-20240307",  # 使用Claude 3 Haiku模型（你的账户可用）
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": "这是一张测试图片。请简短描述你看到了什么颜色。"
                    }
                ]
            }
        ]
    )

    response = message.content[0].text
    print(f"\n   ✅ 图像分析成功！")
    print(f"   Claude响应: {response}")

    print("\n" + "=" * 60)
    print("🎉 所有测试通过！| All Tests Passed!")
    print("=" * 60)
    print("\n你的Claude API密钥完全正常，可以用于:")
    print("   ✅ 文本分析")
    print("   ✅ 图像分析（头皮照片分析）")
    print("   ✅ 医学诊断")
    print("\n现在可以在Streamlit应用中使用这个密钥了！")

except Exception as e:
    error_msg = str(e)
    print("\n" + "=" * 60)
    print("❌ 测试失败！| Test Failed!")
    print("=" * 60)
    print(f"\n错误信息: {error_msg}")

    # 错误分析
    if "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
        print("\n🔑 问题分析: API密钥认证失败")
        print("   可能原因:")
        print("   1. 密钥无效或已过期")
        print("   2. 密钥被撤销")
        print("   3. 账户余额不足")
        print("\n   解决方案:")
        print("   - 访问 https://console.anthropic.com/")
        print("   - 检查账户状态")
        print("   - 生成新的API密钥")

    elif "rate" in error_msg.lower() or "quota" in error_msg.lower():
        print("\n⏰ 问题分析: API配额限制")
        print("   - 请检查账户余额和使用限制")
        print("   - 访问 https://console.anthropic.com/settings/billing")

    elif "network" in error_msg.lower() or "connection" in error_msg.lower():
        print("\n🌐 问题分析: 网络连接问题")
        print("   - 请检查网络连接")
        print("   - 确认可以访问 https://api.anthropic.com/")

    else:
        print("\n❓ 未知错误，请查看详细错误信息")

    sys.exit(1)

print("\n" + "=" * 60)
