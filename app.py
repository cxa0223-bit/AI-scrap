"""
头皮健康AI分析系统 - 马来西亚版
Scalp Health AI Analysis System - Malaysia Edition
"""
import streamlit as st
import pandas as pd
from PIL import Image
import sys
import os

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from ai_analyzer import analyze_scalp_image, get_care_recommendations
from recommender import load_products, recommend_products, format_product_card, save_recommendation_history
from database import init_database, AnalysisHistoryDB, RecommendationDB, setup_database
from ai_services import AIServiceManager
from image_annotator import ScalpImageAnnotator
import uuid
from datetime import datetime

# 初始化数据库
setup_database()

# 页面配置
st.set_page_config(
    page_title="Scalp Health AI Analyzer | 头皮健康分析",
    page_icon="💆‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS - 增强版
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* 主标题卡片 */
    .main-header {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: fadeInDown 0.8s ease-out;
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .main-header h3 {
        font-size: 1.3rem;
        font-weight: 400;
        opacity: 0.95;
    }

    /* 按钮样式 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        padding: 0.85rem;
        border-radius: 10px;
        border: none;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* 产品卡片容器 */
    .product-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
        border: 2px solid transparent;
    }

    .product-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #667eea;
    }

    /* 诊断卡片 */
    .diagnosis-card {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #e74c3c;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(231, 76, 60, 0.2);
    }

    /* 健康评分进度条 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #e74c3c 0%, #f39c12 50%, #27ae60 100%);
    }

    /* 信息卡片 */
    .info-box {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 4px solid #3498db;
    }

    /* 警告框美化 */
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe4a3 100%);
        border-left: 5px solid #ffc107;
        border-radius: 8px;
    }

    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        border-radius: 8px;
    }

    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        border-radius: 8px;
    }

    /* 侧边栏美化 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }

    /* 标签页美化 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* 图片容器 */
    .stImage {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* 指标卡片 */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }

    /* 动画效果 */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* 加载动画 */
    .stSpinner > div {
        border-color: #667eea !important;
        border-right-color: transparent !important;
    }

    /* 展开器美化 */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        font-weight: 600;
    }

    /* 链接按钮 */
    .stLinkButton > a {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        text-decoration: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        display: inline-block;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }

    .stLinkButton > a:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("""
<div class="main-header">
    <h1>🔬 头皮健康AI分析系统</h1>
    <h3>Scalp Health AI Analysis System</h3>
    <p>Upload your scalp image for professional AI analysis | 上传头皮照片获取专业AI分析</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    # Logo区域
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1.5rem;
        background: white;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    ">
        <h2 style="color: #667eea; margin: 0; font-weight: 800;">
            🔬 Scalp Analyzer
        </h2>
        <p style="color: #764ba2; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Medical-Grade AI Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 使用指南
    st.markdown("### 📋 使用指南 | How to Use")
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    ">
        <p><strong>🖼️ 步骤 1：</strong> 上传清晰的头皮照片</p>
        <p><strong>🤖 步骤 2：</strong> 等待AI分析（5-10秒）</p>
        <p><strong>📊 步骤 3：</strong> 查看医学诊断报告</p>
        <p><strong>🛒 步骤 4：</strong> 购买推荐产品</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 特色功能
    st.markdown("### ⭐ 核心功能 | Features")
    st.markdown("""
    <div style="color: white; font-size: 0.9rem;">
        ✅ 8种疾病智能识别<br>
        ✅ 18项医学级检测<br>
        ✅ 中英文专业术语<br>
        ✅ 严重程度评级<br>
        ✅ 个性化治疗建议<br>
        ✅ 产品智能推荐
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 地区信息
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.15);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
    ">
        <p style="font-size: 1.1rem; margin: 0;">
            📍 <strong>Service Region</strong>
        </p>
        <p style="font-size: 1.3rem; margin: 0.5rem 0 0 0; font-weight: bold;">
            🇲🇾 Malaysia
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 联系信息
    st.markdown("### 📞 联系我们 | Contact")
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        font-size: 0.9rem;
    ">
        <p>📧 <strong>Email:</strong><br>support@scalpanalyzer.my</p>
        <p>📱 <strong>WhatsApp:</strong><br>+60 12-345 6789</p>
        <p>🕐 <strong>Hours:</strong><br>Mon-Fri: 9AM-6PM</p>
    </div>
    """, unsafe_allow_html=True)

# 生成或获取session_id
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())

# 主界面
tab1, tab2, tab3 = st.tabs(["🔍 Analysis | 分析", "📊 History | 历史记录", "ℹ️ Information | 信息"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Image | 上传照片")

        # 添加清除结果按钮
        if 'analyzed' in st.session_state and st.session_state['analyzed']:
            if st.button("🔄 Clear Results | 清除结果", help="Clear current analysis results | 清除当前分析结果"):
                st.session_state['analyzed'] = False
                st.session_state['result'] = None
                st.session_state['previous_file'] = None
                st.rerun()

        # 多图上传模式选择
        upload_mode = st.radio(
            "Upload Mode | 上传模式",
            options=["Single Image | 单张图片", "Multiple Images (up to 4) | 多张图片(最多4张)"],
            horizontal=True,
            help="单张模式：上传一张头皮照片 | 多张模式：上传最多4张不同角度的头皮照片进行综合分析"
        )

        is_multi_mode = "Multiple" in upload_mode

        if is_multi_mode:
            uploaded_files = st.file_uploader(
                "Choose your scalp images (up to 4) | 选择头皮照片 (最多4张)",
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True,
                help="Upload up to 4 images from different angles | 上传最多4张不同角度的照片",
                key="file_uploader_multi"
            )

            # 限制最多4张
            if uploaded_files and len(uploaded_files) > 4:
                st.warning("⚠️ Maximum 4 images allowed. Only the first 4 will be used. | 最多允许4张图片，将只使用前4张。")
                uploaded_files = uploaded_files[:4]

            # 检测是否上传了新图片
            if uploaded_files:
                # 生成文件ID列表
                current_file_ids = [f"{f.name}_{f.size}" for f in uploaded_files]
                current_file_id = "_".join(current_file_ids)

                # 如果是新图片，清除之前的分析结果
                if 'previous_file' not in st.session_state or st.session_state['previous_file'] != current_file_id:
                    st.session_state['analyzed'] = False
                    st.session_state['result'] = None
                    st.session_state['previous_file'] = current_file_id

                # 显示所有上传的图片
                st.markdown(f"### 📸 Uploaded Images ({len(uploaded_files)}) | 已上传图片 ({len(uploaded_files)})")
                cols = st.columns(min(len(uploaded_files), 2))
                images = []
                for idx, uploaded_file in enumerate(uploaded_files):
                    img = Image.open(uploaded_file)
                    images.append(img)
                    with cols[idx % 2]:
                        st.image(img, caption=f"Image {idx+1}: {uploaded_file.name}", use_container_width=True)

                # 保存到session state
                st.session_state['uploaded_images'] = images
                st.session_state['uploaded_filenames'] = [f.name for f in uploaded_files]
                image = images[0]  # 主图像用于后续处理
        else:
            uploaded_file = st.file_uploader(
                "Choose your scalp image | 选择头皮照片",
                type=['jpg', 'jpeg', 'png'],
                help="Supports JPG, PNG formats | 支持JPG、PNG格式",
                key="file_uploader_single"
            )

            # 检测是否上传了新图片
            if uploaded_file:
                # 获取当前文件的标识信息
                current_file_id = f"{uploaded_file.name}_{uploaded_file.size}"

                # 如果是新图片，清除之前的分析结果
                if 'previous_file' not in st.session_state or st.session_state['previous_file'] != current_file_id:
                    st.session_state['analyzed'] = False
                    st.session_state['result'] = None
                    st.session_state['previous_file'] = current_file_id

                image = Image.open(uploaded_file)
                st.session_state['uploaded_images'] = [image]
                st.session_state['uploaded_filenames'] = [uploaded_file.name]
                st.image(image, caption="Uploaded Image | 上传的照片", use_container_width=True)

        # 添加AI配置选项 - 移到外层，适用于所有上传模式
        if uploaded_files if is_multi_mode else uploaded_file:
            # 添加AI配置选项
            st.markdown("---")
            st.markdown("### 🤖 AI分析选项 | AI Analysis Options")

            # AI服务选择 - 默认启用
            use_ai = st.checkbox("🚀 **使用AI增强分析** (获得最精准的医学诊断)", value=True)

            if use_ai:
                # 选择AI服务 - GPT-4 为默认选项
                ai_service = st.radio(
                    "选择AI服务 | Select AI Service",
                    ["GPT-4 (OpenAI)", "Claude (Anthropic)"],
                    index=0,  # GPT-4 为默认选项
                    help="GPT-4o: 最新的OpenAI模型，视觉分析能力强 | Claude: Anthropic的医学分析专家",
                    horizontal=True
                )

                # 根据选择的服务配置API密钥
                if ai_service == "GPT-4 (OpenAI)":
                    # GPT-4 配置 - 按优先级尝试加载密钥
                    # 1. 从 Streamlit secrets 读取（本地开发和云部署）
                    # 2. 从环境变量读取
                    # 3. 从 session_state 读取（用户手动输入）
                    existing_key = (
                        st.secrets.get("OPENAI_API_KEY", "") or
                        os.getenv('OPENAI_API_KEY', '') or
                        st.session_state.get('ai_config', {}).get('openai_api_key', '')
                    )

                    if not existing_key:
                        st.warning("⚠️ 请输入您的 OpenAI API 密钥 | 或在 .streamlit/secrets.toml 中配置永久保存")
                        openai_api_key = st.text_input(
                            "OpenAI API密钥",
                            type="password",
                            placeholder="sk-...",
                            help="获取密钥: https://platform.openai.com/api-keys\n\n💡 提示：可在 .streamlit/secrets.toml 中永久保存密钥"
                        )

                        if openai_api_key:
                            # 保存API密钥到session
                            if 'ai_config' not in st.session_state:
                                st.session_state['ai_config'] = {}
                            st.session_state['ai_config']['openai_api_key'] = openai_api_key
                            st.session_state['ai_config']['enable_ai'] = True
                            st.session_state['ai_config']['service'] = 'GPT-4 Vision (OpenAI)'
                            st.session_state['ai_config']['combine_results'] = False
                            st.session_state['ai_config']['language'] = 'zh'
                            st.success("✅ GPT-4 API密钥已配置")
                    else:
                        # 显示密钥来源
                        if st.secrets.get("OPENAI_API_KEY", ""):
                            st.success(f"✅ GPT-4 API已就绪 (来源: secrets.toml) | 密钥: {existing_key[:20]}...")
                        elif os.getenv('OPENAI_API_KEY', ''):
                            st.success(f"✅ GPT-4 API已就绪 (来源: 环境变量) | 密钥: {existing_key[:20]}...")
                        else:
                            st.success(f"✅ GPT-4 API已就绪 (来源: 手动输入) | 密钥: {existing_key[:20]}...")

                        # 存储到 session_state
                        if 'ai_config' not in st.session_state:
                            st.session_state['ai_config'] = {}
                        st.session_state['ai_config']['openai_api_key'] = existing_key
                        # 确保使用GPT-4
                        st.session_state['ai_config']['enable_ai'] = True
                        st.session_state['ai_config']['service'] = 'GPT-4 Vision (OpenAI)'
                        st.session_state['ai_config']['combine_results'] = False

                elif ai_service == "Claude (Anthropic)":
                    # Claude 配置 - 先尝试从环境变量加载
                    existing_key = st.session_state.get('ai_config', {}).get('claude_api_key', '') or os.getenv('ANTHROPIC_API_KEY', '')

                    if not existing_key:
                        st.warning("请输入您的 Claude API 密钥")
                        claude_api_key = st.text_input(
                            "Claude API密钥",
                            type="password",
                            placeholder="sk-ant-api03-...",
                            help="获取密钥: https://console.anthropic.com/"
                        )

                        if claude_api_key:
                            # 保存API密钥到session
                            if 'ai_config' not in st.session_state:
                                st.session_state['ai_config'] = {}
                            st.session_state['ai_config']['claude_api_key'] = claude_api_key
                            st.session_state['ai_config']['enable_ai'] = True
                            st.session_state['ai_config']['service'] = 'Claude (Anthropic)'
                            st.session_state['ai_config']['combine_results'] = False
                            st.session_state['ai_config']['language'] = 'zh'
                            st.success("✅ Claude API密钥已配置")
                    else:
                        st.success(f"✅ 已配置 Claude API (密钥: {existing_key[:20]}...)")
                        # 确保使用Claude
                        if 'ai_config' not in st.session_state:
                            st.session_state['ai_config'] = {}
                        st.session_state['ai_config']['claude_api_key'] = existing_key
                        st.session_state['ai_config']['enable_ai'] = True
                        st.session_state['ai_config']['service'] = 'Claude (Anthropic)'
                        st.session_state['ai_config']['combine_results'] = False

            # 显示AI配置状态（调试信息）
            st.markdown("---")

            # 添加调试模式开关
            debug_mode = st.checkbox("🐛 启用调试模式 (Debug Mode)", value=False,
                                    help="显示详细的 AI 分析过程和原始响应")

            with st.expander("🔍 AI配置状态 | AI Configuration Status", expanded=False):
                ai_config = st.session_state.get('ai_config', {})
                st.write(f"**AI启用状态**: {'✅ 已启用' if ai_config.get('enable_ai', False) else '❌ 未启用'}")
                st.write(f"**选择的服务**: {ai_config.get('service', '未设置')}")

                # 显示正确的 API 密钥状态
                has_openai = bool(ai_config.get('openai_api_key', ''))
                has_claude = bool(ai_config.get('claude_api_key', ''))
                st.write(f"**OpenAI API密钥**: {'✅ 已配置' if has_openai else '❌ 未配置'}")
                st.write(f"**Claude API密钥**: {'✅ 已配置' if has_claude else '❌ 未配置'}")

                if has_openai:
                    st.write(f"**OpenAI密钥预览**: {ai_config.get('openai_api_key', '')[:25]}...")
                if has_claude:
                    st.write(f"**Claude密钥预览**: {ai_config.get('claude_api_key', '')[:25]}...")

                st.write(f"**分析语言**: {ai_config.get('language', 'zh')}")
                st.write(f"**合并本地分析**: {'是' if ai_config.get('combine_results', False) else '否'}")
                st.write(f"**调试模式**: {'✅ 开启' if debug_mode else '❌ 关闭'}")

            # 保存调试模式到 session
            if 'ai_config' not in st.session_state:
                st.session_state['ai_config'] = {}
            st.session_state['ai_config']['debug_mode'] = debug_mode

            # 分析按钮 - 允许重新分析
            button_text = "🔄 Re-analyze | 重新分析" if st.session_state.get('analyzed', False) else "🚀 Start AI Analysis | 开始AI分析"

            # 检查是否配置了API密钥
            ai_config = st.session_state.get('ai_config', {})
            has_api_key = ai_config.get('claude_api_key') or ai_config.get('openai_api_key')
            button_disabled = use_ai and not has_api_key

            if st.button(button_text, type="primary", disabled=button_disabled):
                with st.spinner("正在分析您的头皮状况... | Analyzing your scalp condition..."):
                    # Check if AI service is enabled
                    ai_config = st.session_state.get('ai_config', {})

                    result = None  # 初始化结果

                    # 如果启用了AI服务，优先使用AI分析
                    if ai_config.get('enable_ai', False):
                        service_type = ai_config.get('service', 'Claude (Anthropic)')

                        # 显示分析进度
                        progress_text = st.empty()

                        # 根据服务类型获取正确的API密钥
                        if service_type == 'GPT-4 Vision (OpenAI)':
                            api_key = ai_config.get('openai_api_key', '')
                            progress_text.text("🤖 正在使用 GPT-4o 进行深度分析...")
                        else:
                            api_key = ai_config.get('claude_api_key', '')
                            progress_text.text("🤖 正在使用 Claude AI 进行深度分析...")

                        try:
                            if api_key:
                                # Create AI service
                                ai_service = AIServiceManager.create_service(service_type, api_key)

                                if ai_service:
                                    # Get AI analysis
                                    language = ai_config.get('language', 'zh')

                                    # 调试信息
                                    if ai_config.get('debug_mode', False):
                                        st.info(f"🔧 调试: 正在调用 {service_type}")
                                        st.info(f"🔧 调试: 语言设置 = {language}")

                                    ai_result = ai_service.analyze_scalp_image(image, language)

                                    # 保存调试信息到 session
                                    if ai_config.get('debug_mode', False):
                                        st.session_state['debug_ai_result'] = ai_result
                                        st.session_state['debug_service'] = service_type

                                    # 如果不合并结果，直接使用AI结果
                                    if not ai_config.get('combine_results', False):
                                        result = ai_result.copy()

                                        # Map AI conditions to diagnosed_conditions and normalize
                                        if 'conditions' in result:
                                            from utils.ai_services import AIServiceManager
                                            normalized_conditions = [
                                                AIServiceManager._normalize_condition(cond)
                                                for cond in result.get('conditions', [])
                                            ]
                                            result['diagnosed_conditions'] = normalized_conditions

                                        # Map recommendations to concerns
                                        if 'recommendations' in result:
                                            result['concerns'] = result['recommendations']

                                        # Calculate overall confidence from diagnosed conditions
                                        if 'diagnosed_conditions' in result and result['diagnosed_conditions']:
                                            # Calculate average confidence from all diagnosed conditions
                                            confidences = [
                                                cond.get('confidence', 0)
                                                for cond in result['diagnosed_conditions']
                                            ]
                                            if confidences:
                                                result['confidence'] = int(sum(confidences) / len(confidences))
                                            else:
                                                result['confidence'] = 0
                                        else:
                                            result['confidence'] = 0

                                        result['ai_service_used'] = service_type
                                        result['debug_mode'] = ai_config.get('debug_mode', False)

                                        # 根据服务类型设置分析方法
                                        if service_type == 'GPT-4 Vision (OpenAI)':
                                            result['analysis_method'] = 'GPT-4o Direct Analysis'
                                            progress_text.text("✅ GPT-4o 分析完成！")
                                        else:
                                            result['analysis_method'] = 'Claude AI Direct Analysis'
                                            progress_text.text("✅ Claude AI 分析完成！")
                                    else:
                                        # 合并本地和AI结果
                                        progress_text.text("🔄 正在执行本地分析...")
                                        local_result = analyze_scalp_image(image)
                                        result = AIServiceManager.combine_analyses(ai_result, local_result)
                                        result['ai_service_used'] = service_type

                                        # 根据服务类型设置分析方法
                                        if service_type == 'GPT-4 Vision (OpenAI)':
                                            result['analysis_method'] = 'GPT-4o + Local Combined'
                                        else:
                                            result['analysis_method'] = 'Claude AI + Local Combined'
                                        progress_text.text("✅ 综合分析完成！")
                                else:
                                    progress_text.text("⚠️ AI服务不可用，使用本地分析...")
                                    result = analyze_scalp_image(image)
                                    result['analysis_method'] = 'Local Analysis (Fallback)'

                        except Exception as e:
                            error_msg = str(e)
                            st.error(f"❌ AI分析错误: {error_msg}")

                            # 提供具体的错误建议
                            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                                st.warning("🔑 API密钥问题：请检查您的 API 密钥是否正确")
                                if service_type == 'GPT-4 Vision (OpenAI)':
                                    st.info("💡 获取 OpenAI API密钥: https://platform.openai.com/api-keys")
                                    st.info("💡 检查账户余额: https://platform.openai.com/usage")
                                else:
                                    st.info("💡 获取 Claude API密钥: https://console.anthropic.com/")
                            elif "rate" in error_msg.lower() or "quota" in error_msg.lower():
                                st.warning("⏰ API配额问题：您的API配额可能已用完")
                                st.info("💡 请充值或检查账户余额")
                            elif "model" in error_msg.lower():
                                st.warning("🤖 模型访问问题：您可能没有访问此模型的权限")
                                st.info("💡 确认账户已升级到付费版并有 GPT-4 访问权限")
                            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                                st.warning("🌐 网络连接问题：请检查网络连接是否正常")
                            else:
                                st.warning("⚠️ 未知错误：请查看错误详情")

                            # 显示详细错误（可展开）
                            with st.expander("🔍 查看详细错误信息和完整堆栈", expanded=True):
                                st.code(error_msg)
                                st.markdown("**解决建议：**")
                                st.markdown("1. 检查 API 密钥是否正确（无多余空格）")
                                st.markdown("2. 确认账户有余额")
                                st.markdown("3. 尝试切换到其他 AI 服务")
                                st.markdown("4. 如果问题持续，使用本地分析")

                            # 创建错误结果，不自动回退到本地分析
                            progress_text.text("❌ AI分析失败")
                            result = {
                                'scalp_type': 'API Error',
                                'diagnosed_conditions': [],
                                'concerns': [
                                    f"❌ AI分析失败: {error_msg[:100]}...",
                                    "请检查 API 密钥和账户余额",
                                    "或尝试使用其他 AI 服务"
                                ],
                                'confidence': 0,
                                'health_score': 0,
                                'recommendations': [
                                    "检查 API 配置",
                                    "尝试切换 AI 服务",
                                    "或取消勾选 'AI 增强分析' 使用本地分析"
                                ],
                                'ai_error': error_msg,
                                'analysis_method': 'AI Analysis Failed'
                            }
                    else:
                        # 没有配置AI，使用本地分析
                        result = analyze_scalp_image(image)
                        result['analysis_method'] = 'Local Analysis Only'

                        if use_ai:
                            st.warning("请先配置 API 密钥才能使用 AI 分析")

                    # 保存分析历史到数据库
                    scalp_type = result.get('scalp_type', 'normal')
                    analysis_data = {
                        'session_id': st.session_state['session_id'],
                        'scalp_type': scalp_type,
                        'confidence': result.get('confidence', 0),
                        'health_score': result.get('health_score', 0),
                        'concerns': result.get('concerns', []),
                        'diagnosed_conditions': result.get('diagnosed_conditions', []),
                        'recommendations': get_care_recommendations(scalp_type),
                        'image_path': '',  # 可以保存图片路径
                        'user_id': st.session_state.get('user_id', '')
                    }

                    # 保存到数据库
                    try:
                        analysis_id = AnalysisHistoryDB.save_analysis(analysis_data)
                        result['analysis_id'] = analysis_id
                    except Exception as e:
                        st.warning(f"保存分析历史失败: {e}")

                    # 生成标注图像（总是执行以显示检测结果）
                    annotated_images = []
                    if 'uploaded_images' in st.session_state:
                        annotator = ScalpImageAnnotator()
                        for idx, img in enumerate(st.session_state['uploaded_images']):
                            try:
                                # 执行本地分析以获取检测结果
                                local_analysis = analyze_scalp_image(img)

                                # 调试：记录检测到的问题数量
                                red_count = len(local_analysis.get('red_dots', []))
                                flake_count = len(local_analysis.get('white_flakes', []))
                                follicle_count = 0
                                if 'follicle_info' in local_analysis:
                                    follicle_count = len(local_analysis['follicle_info'].get('detected_follicles', []))

                                print(f"[DEBUG] Image {idx+1} - Detected: {red_count} red dots, {flake_count} flakes, {follicle_count} follicles")

                                # 标注图像
                                annotated_img = annotator.annotate_analysis_results(
                                    img,
                                    local_analysis,
                                    show_labels=True,
                                    show_legend=True
                                )
                                annotated_images.append(annotated_img)
                            except Exception as e:
                                print(f"[ERROR] Failed to annotate image {idx+1}: {e}")
                                # 如果标注失败，使用原图
                                annotated_images.append(img)

                        st.session_state['annotated_images'] = annotated_images
                        print(f"[DEBUG] Total annotated images: {len(annotated_images)}")

                    # 保存到session state
                    st.session_state['analyzed'] = True
                    st.session_state['result'] = result
                    st.rerun()
    
    with col2:
        st.markdown("### 📊 Analysis Results | 分析结果")
        
        if 'analyzed' in st.session_state and st.session_state['analyzed']:
            result = st.session_state['result']
            
            # 显示分析结果
            st.success("✅ Analysis Complete! | 分析完成！")

            # 显示标注图像（如果有）
            if 'annotated_images' in st.session_state and st.session_state['annotated_images']:
                st.markdown("---")
                st.markdown("### 🎯 问题标注图 | Annotated Images with Detected Issues")
                st.info("📍 图中标注了检测到的问题区域：🔴 红色圆圈=炎症/红斑，🟡 黄色方框=鳞屑/头皮屑，🟢 绿色圆圈=毛囊")

                annotated_imgs = st.session_state['annotated_images']
                uploaded_filenames = st.session_state.get('uploaded_filenames', [f"Image {i+1}" for i in range(len(annotated_imgs))])

                # 如果是多张图片，显示对比
                if len(annotated_imgs) > 1:
                    # 创建tabs显示每张标注图
                    tabs = st.tabs([f"📷 {name}" for name in uploaded_filenames])
                    for idx, (tab, annotated_img, filename) in enumerate(zip(tabs, annotated_imgs, uploaded_filenames)):
                        with tab:
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.markdown("**原始图像**")
                                st.image(st.session_state['uploaded_images'][idx], use_container_width=True)
                            with col_b:
                                st.markdown("**标注图像**")
                                st.image(annotated_img, use_container_width=True)
                else:
                    # 单张图片，并排显示
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**原始图像 | Original Image**")
                        st.image(st.session_state['uploaded_images'][0], use_container_width=True)
                    with col_b:
                        st.markdown("**标注图像 | Annotated Image**")
                        st.image(annotated_imgs[0], use_container_width=True)

            # 显示调试信息（在最顶部，不会被刷新隐藏）
            if result.get('debug_mode', False) and 'debug_ai_result' in st.session_state:
                st.markdown("---")
                with st.expander("🐛 **调试: AI 完整返回数据**", expanded=True):
                    st.write(f"**使用的服务**: {st.session_state.get('debug_service', 'Unknown')}")
                    st.write(f"**返回时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    st.markdown("**完整 JSON 数据：**")
                    st.json(st.session_state['debug_ai_result'])

                    # 提取关键字段显示
                    debug_result = st.session_state['debug_ai_result']
                    st.markdown("**关键字段：**")
                    col_d1, col_d2, col_d3 = st.columns(3)
                    with col_d1:
                        st.metric("Scalp Type", debug_result.get('scalp_type', 'N/A'))
                    with col_d2:
                        st.metric("Health Score", f"{debug_result.get('health_score', 0)}/100")
                    with col_d3:
                        st.metric("Conditions", len(debug_result.get('conditions', [])))

                    # Display calculated overall confidence
                    st.markdown("---")
                    st.markdown("**🎯 计算后的整体置信度：**")
                    st.info(f"Overall Confidence (calculated from conditions): **{result.get('confidence', 0)}%**")

                    # 显示每个 condition 的 confidence
                    if debug_result.get('conditions'):
                        st.markdown("**Conditions 详细信息（原始数据）：**")
                        for i, cond in enumerate(debug_result.get('conditions', []), 1):
                            with st.expander(f"Condition {i}: {cond.get('name_cn', 'N/A')}", expanded=False):
                                st.write(f"**Name (CN)**: {cond.get('name_cn', 'N/A')}")
                                st.write(f"**Name (EN)**: {cond.get('name_en', 'N/A')}")
                                st.write(f"**Severity**: {cond.get('severity', 'N/A')}")
                                st.write(f"**Confidence (原始值)**: {cond.get('confidence', 'MISSING')} (类型: {type(cond.get('confidence')).__name__})")
                                st.write(f"**Description**: {cond.get('description', 'N/A')[:100]}...")
                st.markdown("---")

            # 显示分析方法和使用的模型
            if 'analysis_method' in result:
                if 'GPT-4' in result['analysis_method']:
                    # 显示使用的具体模型
                    if 'model_display_name' in result:
                        st.info(f"🤖 **分析方法**: {result['analysis_method']} | 模型: {result['model_display_name']}")
                    else:
                        st.info(f"🤖 **分析方法**: {result['analysis_method']}")
                    st.markdown("*OpenAI GPT 提供专业的医学级视觉分析结果*")
                elif 'Claude' in result['analysis_method']:
                    st.info(f"🤖 **分析方法**: {result['analysis_method']}")
                    st.markdown("*Claude AI 提供专业的医学级分析结果*")
                else:
                    st.info(f"🔬 **分析方法**: {result['analysis_method']}")

            # 显示AI综合分析总结
            if 'analysis_summary' in result and result['analysis_summary']:
                st.markdown("---")
                st.markdown("#### 📊 综合分析报告 | Comprehensive Analysis")
                st.success(result['analysis_summary'])

            # 显示头皮分区分析（新增）
            if 'scalp_zone_analysis' in result and result['scalp_zone_analysis']:
                st.markdown("---")
                st.markdown("#### 🗺️ 头皮分区分析 | Scalp Zone Analysis")
                zones = result['scalp_zone_analysis']

                col1, col2 = st.columns(2)
                with col1:
                    if 'frontal' in zones and zones['frontal']:
                        with st.expander("📍 前额区域 (Frontal)", expanded=False):
                            st.write(zones['frontal'])
                    if 'vertex' in zones and zones['vertex']:
                        with st.expander("📍 头顶区域 (Vertex)", expanded=False):
                            st.write(zones['vertex'])
                with col2:
                    if 'temporal' in zones and zones['temporal']:
                        with st.expander("📍 颞部区域 (Temporal)", expanded=False):
                            st.write(zones['temporal'])
                    if 'occipital' in zones and zones['occipital']:
                        with st.expander("📍 枕部区域 (Occipital)", expanded=False):
                            st.write(zones['occipital'])

            # 显示评分细分（新增）
            if 'score_breakdown' in result and result['score_breakdown']:
                st.markdown("---")
                st.markdown("#### 📈 健康评分细分 | Score Breakdown")
                breakdown = result['score_breakdown']

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    score1 = breakdown.get('scalp_condition', 'N/A')
                    st.metric("头皮状态", f"{score1}/30")
                with col2:
                    score2 = breakdown.get('hair_health', 'N/A')
                    st.metric("毛发健康", f"{score2}/30")
                with col3:
                    score3 = breakdown.get('inflammation', 'N/A')
                    st.metric("炎症情况", f"{score3}/20")
                with col4:
                    score4 = breakdown.get('overall_hygiene', 'N/A')
                    st.metric("整体卫生", f"{score4}/20")

            # 显示建议的进一步检查（新增）
            if 'suggested_tests' in result and result['suggested_tests']:
                st.markdown("---")
                st.markdown("#### 🔬 建议的进一步检查 | Suggested Tests")
                for i, test in enumerate(result['suggested_tests'], 1):
                    st.info(f"{i}. {test}")

            # 显示紧急程度（新增）
            if 'urgency_level' in result and result['urgency_level']:
                urgency = result['urgency_level']
                st.markdown("---")
                if urgency == '紧急':
                    st.error(f"⚠️ **就医建议**: {urgency} - 请立即前往医院皮肤科就诊")
                elif urgency == '尽快':
                    st.warning(f"⚡ **就医建议**: {urgency} - 建议尽快预约皮肤科医生")
                elif urgency == '建议':
                    st.info(f"ℹ️ **就医建议**: {urgency} - 建议咨询专业医生")
                else:
                    st.success(f"✅ **就医建议**: {urgency} - 继续观察，注意日常护理")

            # 如果是AI直接分析，显示AI的详细响应
            if 'ai_service_used' in result:
                if result.get('ai_service_used') == 'Claude (Anthropic)' and 'ai_raw_response' in result:
                    with st.expander("🤖 **Claude AI 原始分析结果**", expanded=False):
                        st.markdown(result.get('ai_raw_response', ''))
                elif result.get('ai_service_used') == 'GPT-4 Vision (OpenAI)' and 'ai_raw_response' in result:
                    with st.expander("🤖 **GPT-4o 原始分析结果**", expanded=False):
                        st.markdown(result.get('ai_raw_response', ''))

            # 头皮类型和置信度
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric(
                    label="Scalp Type | 头皮类型",
                    value=result['scalp_type']
                )
            with col_b:
                st.metric(
                    label="Confidence | 置信度",
                    value=f"{result.get('confidence', 0)}%"
                )
            
            # 健康评分
            st.markdown("#### 🏥 Health Score | 健康评分")
            health_score = result.get('health_score', 0)
            if health_score > 0:
                st.progress(health_score / 100)
                st.write(f"**{health_score}/100**")
            else:
                st.info("健康评分待评估 | Health score pending")

            # 详细分析结果（新增）
            if 'detailed_analysis' in result and result['detailed_analysis']:
                st.markdown("---")
                st.markdown("#### 🔬 Detailed Analysis | 详细分析")

                detailed = result['detailed_analysis']

                # 显示头皮层分析
                with st.expander("📊 **头皮层分析 | Scalp Layer Analysis**", expanded=True):
                    if 'layer_analysis' in detailed:
                        layers = detailed['layer_analysis']

                        # 表皮层分析
                        st.markdown("**表皮层 (Epidermis):**")
                        epidermis = layers.get('epidermis', {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"• 厚度: {epidermis.get('thickness', 'N/A')}")
                            st.write(f"• 角质化: {epidermis.get('keratinization', 'N/A')}")
                        with col2:
                            st.write(f"• 屏障功能: {epidermis.get('barrier_function', 'N/A')}")
                            st.write(f"• 细胞更新: {epidermis.get('cell_turnover', 'N/A')}")
                        if epidermis.get('issues'):
                            st.warning("⚠️ 问题: " + ", ".join(epidermis['issues']))

                        # 真皮层分析
                        st.markdown("**真皮层 (Dermis):**")
                        dermis = layers.get('dermis', {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"• 胶原密度: {dermis.get('collagen_density', 'N/A')}")
                            st.write(f"• 弹性: {dermis.get('elasticity', 'N/A')}")
                        with col2:
                            st.write(f"• 血液循环: {dermis.get('blood_circulation', 'N/A')}")
                            st.write(f"• 炎症: {dermis.get('inflammation', 'N/A')}")
                        if dermis.get('issues'):
                            st.warning("⚠️ 问题: " + ", ".join(dermis['issues']))

                        # 毛囊分析
                        st.markdown("**毛囊 (Follicles):**")
                        follicles = layers.get('follicles', {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"• 健康状态: {follicles.get('health', 'N/A')}")
                            st.write(f"• 堵塞情况: {follicles.get('blockage', 'N/A')}")
                        with col2:
                            st.write(f"• 炎症: {follicles.get('inflammation', 'N/A')}")
                            st.write(f"• 萎缩: {follicles.get('miniaturization', 'N/A')}")

                        # 皮脂腺分析
                        st.markdown("**皮脂腺 (Sebaceous Glands):**")
                        glands = layers.get('sebaceous_glands', {})
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"• 活动性: {glands.get('activity', 'N/A')}")
                            st.write(f"• 分泌水平: {glands.get('secretion_level', 'N/A')}")
                        with col2:
                            st.write(f"• 堵塞: {glands.get('blockage', 'N/A')}")
                            st.write(f"• 炎症: {glands.get('inflammation', 'N/A')}")

                # 显示微观症状
                with st.expander("🔍 **微观症状检测 | Microscopic Symptoms**", expanded=True):
                    if 'micro_symptoms' in detailed:
                        symptoms = detailed['micro_symptoms']
                        stats = detailed.get('statistics', {})

                        # 创建症状统计表
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("红点/红斑", stats.get('red_dots_count', 0))
                        with col2:
                            st.metric("鳞屑/皮屑", stats.get('flakes_count', 0))
                        with col3:
                            st.metric("脓包/丘疹", stats.get('pustules_count', 0))

                        # 详细症状列表
                        if symptoms.get('red_dots'):
                            st.markdown("**🔴 红点/红斑分布:**")
                            for i, dot in enumerate(symptoms['red_dots'][:5], 1):  # 只显示前5个
                                st.write(f"  {i}. {dot.get('type', '红点')} - 强度: {dot.get('intensity', 'N/A')}, 大小: {dot.get('size', 'N/A')}px")

                        if symptoms.get('white_flakes'):
                            st.markdown("**⚪ 鳞屑分布:**")
                            for i, flake in enumerate(symptoms['white_flakes'][:5], 1):
                                st.write(f"  {i}. {flake.get('type', '鳞屑')} - 严重度: {flake.get('severity', 'N/A')}")

                        if symptoms.get('pustules'):
                            st.markdown("**🟡 脓包/丘疹:**")
                            for i, pustule in enumerate(symptoms['pustules'][:5], 1):
                                st.write(f"  {i}. {pustule.get('type', '丘疹')} - 阶段: {pustule.get('stage', 'N/A')}")

                # 显示严重程度评估
                with st.expander("📈 **严重程度评估 | Severity Assessment**", expanded=False):
                    if 'severity_assessment' in detailed:
                        severity = detailed['severity_assessment']

                        # 炎症评估
                        inflammation = severity.get('inflammation', {})
                        st.markdown("**炎症程度:**")
                        st.write(f"• 等级: {inflammation.get('level', 'N/A')}")
                        st.write(f"• 描述: {inflammation.get('description', 'N/A')}")

                        # 干燥评估
                        dryness = severity.get('dryness', {})
                        st.markdown("**干燥程度:**")
                        st.write(f"• 等级: {dryness.get('level', 'N/A')}")
                        st.write(f"• 描述: {dryness.get('description', 'N/A')}")

                        # 油腻评估
                        oiliness = severity.get('oiliness', {})
                        st.markdown("**油腻程度:**")
                        st.write(f"• 等级: {oiliness.get('level', 'N/A')}")
                        st.write(f"• 描述: {oiliness.get('description', 'N/A')}")

                        # 敏感评估
                        sensitivity = severity.get('sensitivity', {})
                        st.markdown("**敏感程度:**")
                        st.write(f"• 等级: {sensitivity.get('level', 'N/A')}")
                        st.write(f"• 描述: {sensitivity.get('description', 'N/A')}")

                # 显示详细发现
                if 'detailed_findings' in detailed and detailed['detailed_findings']:
                    with st.expander("📝 **详细发现 | Detailed Findings**", expanded=False):
                        for finding in detailed['detailed_findings']:
                            st.write(f"• {finding}")

            # 医学诊断（新增）
            if 'diagnosed_conditions' in result and result['diagnosed_conditions']:
                st.markdown("---")
                st.markdown("#### 🩺 Medical Diagnosis | 医学诊断")

                # DEBUG: Show diagnosed_conditions data
                if result.get('debug_mode', False):
                    with st.expander("🔍 DEBUG: diagnosed_conditions 原始数据", expanded=False):
                        for i, cond in enumerate(result['diagnosed_conditions'], 1):
                            st.write(f"**Condition {i}:**")
                            st.write(f"- confidence 值: {cond.get('confidence', 'MISSING')} (类型: {type(cond.get('confidence')).__name__})")
                            st.write(f"- name_cn: {cond.get('name_cn', 'N/A')}")
                            st.json(cond)
                            st.markdown("---")

                for condition in result['diagnosed_conditions']:
                    # 严重程度颜色
                    severity_color = {
                        '轻度': 'info',
                        '早期': 'info',
                        '中度': 'warning',
                        '重度': 'error',
                        '晚期': 'error'
                    }.get(condition['severity'], 'info')

                    # 显示诊断卡片
                    confidence = condition.get('confidence', 0)

                    # DEBUG: 在调试模式下显示confidence提取
                    if result.get('debug_mode', False):
                        import streamlit as st_debug
                        st_debug.write(f"🔍 DEBUG 显示时: condition.get('confidence', 0) = {confidence}, 类型: {type(confidence).__name__}")
                        st_debug.write(f"   原始 condition dict 的 confidence 键: {condition.get('confidence', 'KEY_NOT_FOUND')}")

                    confidence_color = "🟢" if confidence >= 80 else "🟡" if confidence >= 60 else "🔴"

                    with st.expander(f"{condition['icon']} **{condition['name_cn']}** ({condition['name_en']}) - {condition['severity']} {confidence_color}", expanded=True):
                        # 基本信息
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**俗称：** {condition.get('common_name', condition.get('name_cn', 'N/A'))}")
                            if 'icd10_code' in condition:
                                st.markdown(f"**ICD-10编码：** {condition['icd10_code']}")
                        with col2:
                            st.markdown(f"**置信度：** {confidence}% {confidence_color}")
                            if confidence >= 80:
                                st.success("高度可信")
                            elif confidence >= 60:
                                st.warning("中度可信")
                            else:
                                st.error("低度可信")

                        st.markdown("---")

                        # 详细描述
                        st.markdown(f"**📋 医学描述：**")
                        st.info(condition.get('description', '无详细描述'))

                        # 诊断证据（新增）
                        if 'diagnostic_evidence' in condition and condition['diagnostic_evidence']:
                            st.markdown("**🔍 诊断依据：**")
                            st.success(condition['diagnostic_evidence'])

                        # 观察到的症状
                        if 'symptoms' in condition and condition['symptoms']:
                            st.markdown("**👁️ 观察到的症状：**")
                            for symptom in condition['symptoms']:
                                st.write(f"• {symptom}")

                        # 鉴别诊断（新增）
                        if 'differential_diagnosis' in condition and condition['differential_diagnosis']:
                            with st.expander("🔬 鉴别诊断", expanded=False):
                                st.write(condition['differential_diagnosis'])

                        # 严重程度指示器
                        st.markdown("---")
                        if condition['severity'] in ['重度', '晚期']:
                            st.error(f"⚠️ 严重程度：**{condition['severity']}** - 建议尽快就医")
                        elif condition['severity'] == '中度':
                            st.warning(f"⚡ 严重程度：**{condition['severity']}** - 建议咨询医生")
                        else:
                            st.info(f"ℹ️ 严重程度：**{condition['severity']}** - 注意观察")

                # 医学建议
                if 'medical_advice' in result:
                    advice = result['medical_advice']

                    if advice['see_doctor']:
                        if advice['urgency'] == 'urgent':
                            st.error("🚨 **紧急提示：** 检测到严重问题，请立即就医！")
                        elif advice['urgency'] == 'moderate':
                            st.warning("⚠️ **重要提示：** 建议尽快咨询医生")

                    if advice['recommendations']:
                        st.markdown("**💊 专业建议：**")
                        for rec in advice['recommendations']:
                            st.write(f"• {rec}")

            # 检测到的问题
            st.markdown("---")
            st.markdown("#### 🎯 Detected Issues | 检测到的问题")
            concerns = result.get('concerns', [])
            if concerns:
                for concern in concerns:
                    st.warning(concern)
            else:
                st.info("未发现明显问题 | No significant issues detected")

            # 护理建议
            st.markdown("#### 💡 Care Recommendations | 护理建议")
            scalp_type = result.get('scalp_type', 'normal')
            recommendations = get_care_recommendations(scalp_type)
            for rec in recommendations:
                st.info(f"✓ {rec}")
        else:
            st.info("👆 Please upload an image and click analyze | 请先上传照片并点击分析按钮")
    
    # 产品推荐区域
    if 'analyzed' in st.session_state and st.session_state['analyzed']:
        st.markdown("---")
        st.markdown("### 🛒 Recommended Products | 推荐产品")
        
        result = st.session_state['result']
        
        # 加载产品数据
        products_df = load_products('data/products.csv')
        
        if not products_df.empty:
            # 获取推荐产品
            recommended = recommend_products(
                result.get('scalp_type', 'normal'),
                result.get('concerns', []),
                products_df,
                top_n=3
            )

            # 保存推荐历史（如果有analysis_id）
            if 'analysis_id' in result and not recommended.empty:
                try:
                    save_recommendation_history(result['analysis_id'], recommended)
                except Exception as e:
                    print(f"保存推荐历史失败: {e}")
            
            if not recommended.empty:
                cols = st.columns(3)
                for idx, (_, product) in enumerate(recommended.iterrows()):
                    with cols[idx]:
                        # 产品容器
                        with st.container():
                            # 显示产品图片（如果有）
                            if pd.notna(product.get('image')) and product['image']:
                                img_path = f"assets/products/{product['image']}"
                                if os.path.exists(img_path):
                                    st.image(img_path, use_container_width=True)
                                else:
                                    st.image("https://via.placeholder.com/300x200?text=Product+Image", use_container_width=True)
                            else:
                                st.image("https://via.placeholder.com/300x200?text=Product+Image", use_container_width=True)

                            # 产品信息卡片
                            st.markdown(f"### 🏷️ {product['name']}")

                            # 使用列布局显示详细信息
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.markdown(f"**🏢 品牌**")
                                st.write(product['brand'])
                                st.markdown(f"**📦 类型**")
                                st.write(product['type'])
                            with col_info2:
                                st.markdown(f"**👤 适用**")
                                st.write(product['suitable_for'])
                                st.markdown(f"**🎯 针对**")
                                st.write(product['concern'])

                            # 价格突出显示
                            st.markdown(f"""
                            <div style="
                                text-align: center;
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: white;
                                padding: 1rem;
                                border-radius: 10px;
                                margin: 1rem 0;
                                font-size: 1.8rem;
                                font-weight: bold;
                                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                            ">
                                RM {product['price_myr']}
                            </div>
                            """, unsafe_allow_html=True)

                            # 产品描述
                            st.markdown(f"""
                            <div style="
                                background: #f8f9fa;
                                padding: 0.8rem;
                                border-radius: 8px;
                                border-left: 3px solid #667eea;
                                font-size: 0.9rem;
                                color: #555;
                                margin-bottom: 1rem;
                            ">
                                {product['description']}
                            </div>
                            """, unsafe_allow_html=True)

                            # 购买按钮
                            st.link_button(
                                "🛍️ Buy Now | 立即购买",
                                product['link'],
                                use_container_width=True
                            )
            else:
                st.warning("No products found for your scalp type | 未找到适合的产品")
        else:
            st.error("Product database not found | 产品数据库未找到")

with tab2:
    st.markdown("### 📊 分析历史 | Analysis History")

    # 获取当前会话的分析历史
    history = AnalysisHistoryDB.get_user_history(st.session_state['session_id'], limit=20)

    if history:
        st.success(f"找到 {len(history)} 条分析记录")

        # 显示统计信息
        col1, col2, col3 = st.columns(3)

        # 计算平均健康分数
        avg_score = sum(h['health_score'] for h in history) / len(history)
        with col1:
            st.metric("平均健康分数", f"{avg_score:.1f}/100")

        # 最常见的头皮类型
        scalp_types = {}
        for h in history:
            scalp_type = h['scalp_type']
            scalp_types[scalp_type] = scalp_types.get(scalp_type, 0) + 1
        most_common = max(scalp_types.items(), key=lambda x: x[1])[0] if scalp_types else "无"
        with col2:
            st.metric("最常见类型", most_common)

        with col3:
            st.metric("总分析次数", len(history))

        st.markdown("---")

        # 显示历史记录列表
        for i, record in enumerate(history, 1):
            with st.expander(f"📅 {record['created_at']} - {record['scalp_type']}", expanded=(i==1)):
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("**基本信息:**")
                    st.write(f"• 头皮类型: {record['scalp_type']}")
                    st.write(f"• 置信度: {record['confidence']}%")
                    st.write(f"• 健康评分: {record['health_score']}/100")

                with col_b:
                    st.markdown("**检测到的问题:**")
                    if record['concerns']:
                        for concern in record['concerns']:
                            st.write(f"• {concern}")
                    else:
                        st.write("无")

                # 诊断的疾病
                if record['diagnosed_conditions']:
                    st.markdown("**医学诊断:**")
                    for condition in record['diagnosed_conditions']:
                        severity = condition.get('severity', '')
                        name_cn = condition.get('name_cn', '')
                        confidence = condition.get('confidence', 0)
                        st.write(f"• {name_cn} - {severity} (置信度: {confidence}%)")

                # 建议
                if record['recommendations']:
                    st.markdown("**护理建议:**")
                    for rec in record['recommendations']:
                        st.info(f"✓ {rec}")

        # 显示总体统计
        st.markdown("---")
        statistics = AnalysisHistoryDB.get_statistics()
        st.markdown("### 📈 总体统计 | Overall Statistics")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总分析次数", statistics['total_analyses'])
        with col2:
            st.metric("今日分析", statistics['today_analyses'])
        with col3:
            st.metric("平均健康分数", f"{statistics['avg_health_score']:.1f}")
        with col4:
            # 显示头皮类型分布
            if statistics['scalp_distribution']:
                most_type = max(statistics['scalp_distribution'].items(), key=lambda x: x[1])
                st.metric("最多类型", most_type[0])
    else:
        st.info("暂无分析历史记录。上传照片开始您的第一次分析！")

with tab3:
    st.markdown("### ℹ️ About Our AI Technology | 关于我们的AI技术")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        #### **English**
        
        Our AI-powered scalp analysis system uses advanced computer vision and deep learning 
        algorithms to:
        
        - **Detect scalp type**: Oily, dry, normal, or sensitive
        - **Identify issues**: Dandruff, hair loss, inflammation
        - **Provide recommendations**: Personalized care tips and product suggestions
        - **Track progress**: Monitor your scalp health over time
        
        **Technology Stack:**
        - Computer Vision
        - Deep Learning (CNN)
        - Image Processing
        - Recommendation Algorithms
        
        **Accuracy Rate:** 87%+ (based on clinical validation)
        """)
    
    with col_info2:
        st.markdown("""
        #### **中文**
        
        我们的AI头皮分析系统使用先进的计算机视觉和深度学习算法来：
        
        - **检测头皮类型**：油性、干性、正常或敏感
        - **识别问题**：头屑、脱发、炎症
        - **提供建议**：个性化护理建议和产品推荐
        - **跟踪进度**：长期监测头皮健康状况
        
        **技术栈：**
        - 计算机视觉
        - 深度学习（CNN）
        - 图像处理
        - 推荐算法
        
        **准确率：** 87%+（基于临床验证）
        """)
    
    st.markdown("---")
    st.markdown("### 🔒 Privacy & Security | 隐私与安全")
    st.info("""
    - Your images are processed securely and not stored permanently
    - All data is encrypted during transmission
    - We comply with GDPR and Malaysian data protection laws
    
    - 您的图片经过安全处理，不会永久存储
    - 所有数据在传输过程中都经过加密
    - 我们遵守GDPR和马来西亚数据保护法
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>© 2024 Scalp Health AI Analyzer</strong></p>
    <p>Professional Scalp Analysis for Malaysia | 马来西亚专业头皮分析</p>
    <p style="font-size: 12px; margin-top: 1rem;">
        For best results, take photos in good lighting conditions | 
        为获得最佳效果，请在光线充足的条件下拍照
    </p>
</div>
""", unsafe_allow_html=True)
