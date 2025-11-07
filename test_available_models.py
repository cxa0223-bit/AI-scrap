"""
测试可用的Claude模型
Test Available Claude Models
"""

import sys
import io

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from anthropic import Anthropic
import os

# 从环境变量读取API密钥
api_key = os.getenv("ANTHROPIC_API_KEY", "your-claude-api-key-here")
if api_key == "your-claude-api-key-here":
    print("错误：请设置环境变量 ANTHROPIC_API_KEY")
    print("或修改此文件中的 api_key 变量")
    sys.exit(1)

client = Anthropic(api_key=api_key)

# 尝试的模型列表
models_to_test = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-2.1",
    "claude-2.0",
]

print("=" * 60)
print("测试可用的Claude模型 | Testing Available Models")
print("=" * 60)

successful_model = None

for model in models_to_test:
    print(f"\n正在测试模型: {model}")
    try:
        message = client.messages.create(
            model=model,
            max_tokens=50,
            messages=[
                {
                    "role": "user",
                    "content": "Hi"
                }
            ]
        )
        print(f"   ✅ {model} - 可用！")
        print(f"   响应: {message.content[0].text}")
        successful_model = model
        break  # 找到可用的模型就停止
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not_found" in error_msg:
            print(f"   ❌ {model} - 模型不可用")
        elif "permission" in error_msg.lower() or "access" in error_msg.lower():
            print(f"   ❌ {model} - 无访问权限")
        else:
            print(f"   ❌ {model} - 错误: {error_msg[:100]}")

if successful_model:
    print("\n" + "=" * 60)
    print(f"✅ 找到可用模型: {successful_model}")
    print("=" * 60)
else:
    print("\n" + "=" * 60)
    print("❌ 未找到可用模型")
    print("=" * 60)
    print("\n可能的原因:")
    print("1. 账户类型限制")
    print("2. 账户余额不足")
    print("3. API密钥权限限制")
    print("\n请访问 https://console.anthropic.com/ 检查账户状态")
