"""
AI Settings Page
Configure AI services and API keys
"""

import streamlit as st
import os
import json
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'utils'))

from ai_services import AIServiceManager

# Page config
st.set_page_config(
    page_title="AI Settings",
    page_icon="🤖",
    layout="wide"
)

def save_api_keys(config):
    """Save API keys to session state and optionally to file"""
    st.session_state['ai_config'] = config
    # You can also save to a config file if needed
    # But for security, it's better to use environment variables

def load_api_keys():
    """Load API keys from session state or environment"""
    if 'ai_config' in st.session_state:
        return st.session_state['ai_config']

    # Try loading from environment variables
    config = {
        'service': 'Local Analysis (Rule-based)',
        'claude_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
        'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
        'enable_ai': False,
        'combine_results': True,
        'language': 'zh'
    }
    return config

# Main UI
st.title("🤖 AI Service Configuration")
st.markdown("---")

# Load current configuration
config = load_api_keys()

# Service availability check
st.subheader("📊 Service Availability")
services = AIServiceManager.get_available_services()

cols = st.columns(3)
for idx, (service, available) in enumerate(services.items()):
    with cols[idx % 3]:
        if available:
            st.success(f"✅ {service}")
        else:
            st.warning(f"⚠️ {service} (Needs installation)")

st.markdown("---")

# AI Service Selection
st.subheader("⚙️ AI Service Settings")

col1, col2 = st.columns(2)

with col1:
    # Enable AI enhancement
    enable_ai = st.checkbox(
        "Enable AI-Enhanced Analysis",
        value=config.get('enable_ai', False),
        help="Use AI services for more accurate scalp analysis"
    )

    if enable_ai:
        # Select AI service
        selected_service = st.selectbox(
            "Select AI Service",
            list(services.keys()),
            index=list(services.keys()).index(config.get('service', 'Local Analysis (Rule-based)')),
            help="Choose which AI service to use for analysis"
        )

        # Combine with local analysis
        combine_results = st.checkbox(
            "Combine with Local Analysis",
            value=config.get('combine_results', True),
            help="Combine AI results with rule-based local analysis for better accuracy"
        )
    else:
        selected_service = "Local Analysis (Rule-based)"
        combine_results = False

with col2:
    # Language preference
    language = st.selectbox(
        "Analysis Language",
        ["Chinese (中文)", "English"],
        index=0 if config.get('language', 'zh') == 'zh' else 1,
        help="Language for AI analysis results"
    )
    language_code = 'zh' if language == "Chinese (中文)" else 'en'

st.markdown("---")

# API Key Configuration
# Initialize both key variables to prevent NameError
claude_key = config.get('claude_api_key', '')
openai_key = config.get('openai_api_key', '')

if enable_ai:
    st.subheader("🔑 API Key Configuration")

    if selected_service == "Claude (Anthropic)":
        st.info("📝 Get your Claude API key from: https://console.anthropic.com/")

        claude_key = st.text_input(
            "Claude API Key",
            value=config.get('claude_api_key', ''),
            type="password",
            placeholder="sk-ant-api03-..."
        )

        # Installation instructions
        if not services["Claude (Anthropic)"]:
            st.warning("⚠️ Please install anthropic library:")
            st.code("pip install anthropic", language="bash")

    elif selected_service == "GPT-4 Vision (OpenAI)":
        st.info("📝 Get your OpenAI API key from: https://platform.openai.com/api-keys")

        openai_key = st.text_input(
            "OpenAI API Key",
            value=config.get('openai_api_key', ''),
            type="password",
            placeholder="sk-..."
        )

        # Installation instructions
        if not services["GPT-4 Vision (OpenAI)"]:
            st.warning("⚠️ Please install openai library:")
            st.code("pip install openai", language="bash")

st.markdown("---")

# Save Configuration
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("💾 Save Settings", type="primary", use_container_width=True):
        # Prepare configuration
        new_config = {
            'service': selected_service if enable_ai else 'Local Analysis (Rule-based)',
            'claude_api_key': claude_key,
            'openai_api_key': openai_key,
            'enable_ai': enable_ai,
            'combine_results': combine_results,
            'language': language_code
        }

        # Save configuration
        save_api_keys(new_config)
        st.success("✅ Settings saved successfully!")
        st.balloons()

st.markdown("---")

# Usage Instructions
with st.expander("📖 How to Use AI Services", expanded=False):
    st.markdown("""
    ### 🚀 Quick Start Guide

    1. **Choose an AI Service:**
       - **Claude (Anthropic)**: Best for detailed medical analysis with high accuracy
       - **GPT-4 Vision (OpenAI)**: Good for general scalp analysis with fast response
       - **Local Analysis**: Free rule-based analysis without API requirements

    2. **Get API Keys:**
       - For Claude: Sign up at [Anthropic Console](https://console.anthropic.com/)
       - For OpenAI: Sign up at [OpenAI Platform](https://platform.openai.com/)

    3. **Install Required Libraries:**
       ```bash
       # For Claude
       pip install anthropic

       # For OpenAI
       pip install openai
       ```

    4. **Configure Settings:**
       - Enable AI-Enhanced Analysis
       - Select your preferred service
       - Enter your API key
       - Save settings

    5. **Start Analyzing:**
       - Go back to the main page
       - Upload a scalp image
       - The AI will provide detailed analysis

    ### 💡 Tips
    - **Combine Results**: Enable this for best accuracy - AI + local analysis
    - **Language**: Choose your preferred language for results
    - **Security**: API keys are stored in session only (not saved to disk)

    ### 💰 Pricing
    - **Claude**: ~$0.01-0.03 per image analysis
    - **GPT-4 Vision**: ~$0.01-0.02 per image analysis
    - **Local Analysis**: Free
    """)

# Testing Section
with st.expander("🧪 Test AI Connection", expanded=False):
    st.markdown("Test your API configuration:")

    test_col1, test_col2 = st.columns(2)

    with test_col1:
        if st.button("Test Current Configuration"):
            if enable_ai and selected_service != "Local Analysis (Rule-based)":
                with st.spinner("Testing connection..."):
                    try:
                        if selected_service == "Claude (Anthropic)":
                            if not claude_key:
                                st.error("❌ Please provide Claude API key")
                            else:
                                # 实际测试API连接
                                try:
                                    from anthropic import Anthropic
                                    client = Anthropic(api_key=claude_key)

                                    # 发送测试请求
                                    message = client.messages.create(
                                        model="claude-3-haiku-20240307",  # 使用可用的Haiku模型
                                        max_tokens=50,
                                        messages=[
                                            {"role": "user", "content": "Say 'API test successful' in Chinese"}
                                        ]
                                    )

                                    response = message.content[0].text
                                    st.success("✅ Claude API连接成功!")
                                    st.info(f"测试响应: {response}")
                                    st.balloons()
                                except Exception as api_error:
                                    error_msg = str(api_error)
                                    st.error(f"❌ API连接失败: {error_msg}")

                                    # 提供具体建议
                                    if "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
                                        st.warning("🔑 API密钥无效，请检查密钥是否正确")
                                        st.info("获取新密钥: https://console.anthropic.com/")
                                    elif "rate" in error_msg.lower() or "quota" in error_msg.lower():
                                        st.warning("⏰ API配额已用完，请检查账户余额")
                                    elif "network" in error_msg.lower():
                                        st.warning("🌐 网络连接问题，请检查网络")
                                    else:
                                        with st.expander("查看详细错误"):
                                            st.code(error_msg)

                        elif selected_service == "GPT-4 Vision (OpenAI)":
                            if not openai_key:
                                st.error("❌ Please provide OpenAI API key")
                            else:
                                # 实际测试OpenAI API
                                try:
                                    from openai import OpenAI
                                    client = OpenAI(api_key=openai_key)

                                    # 尝试多个模型进行测试
                                    models_to_test = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
                                    success = False
                                    used_model = None

                                    for model in models_to_test:
                                        try:
                                            response = client.chat.completions.create(
                                                model=model,
                                                messages=[
                                                    {"role": "user", "content": "Say 'API test successful'"}
                                                ],
                                                max_tokens=20
                                            )
                                            result = response.choices[0].message.content
                                            used_model = model
                                            success = True
                                            break
                                        except Exception as e:
                                            if "model_not_found" in str(e) or "does not exist" in str(e):
                                                continue
                                            else:
                                                raise e

                                    if success:
                                        st.success(f"✅ OpenAI API连接成功! (使用模型: {used_model})")
                                        st.info(f"测试响应: {result}")
                                        st.balloons()
                                    else:
                                        st.error("❌ 所有测试的模型都不可用")
                                        st.warning("您的账户可能没有访问这些模型的权限")

                                except Exception as api_error:
                                    st.error(f"❌ API连接失败: {str(api_error)}")
                                    with st.expander("查看详细错误"):
                                        st.code(str(api_error))
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.info("ℹ️ Using local analysis - no API key required")

# Display current status
st.sidebar.markdown("### 📊 Current Status")
if enable_ai:
    st.sidebar.success(f"🤖 AI Enabled: {selected_service}")
else:
    st.sidebar.info("🔧 Using Local Analysis")

st.sidebar.markdown("### 📝 Notes")
st.sidebar.markdown("""
- API keys are not permanently saved
- Set as environment variables for persistence
- Costs apply for AI services
- Local analysis is always free
""")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
        <small>AI-Enhanced Scalp Analysis System v2.0</small>
    </div>
    """,
    unsafe_allow_html=True
)