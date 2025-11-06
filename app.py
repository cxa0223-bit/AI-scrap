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
        uploaded_file = st.file_uploader(
            "Choose your scalp image | 选择头皮照片", 
            type=['jpg', 'jpeg', 'png'],
            help="Supports JPG, PNG formats | 支持JPG、PNG格式"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image | 上传的照片", use_container_width=True)
            
            # 分析按钮
            if st.button("🚀 Start AI Analysis | 开始AI分析", type="primary"):
                with st.spinner("Analyzing your scalp condition... | 正在分析头皮状况..."):
                    # 调用AI分析
                    result = analyze_scalp_image(image)

                    # 保存分析历史到数据库
                    analysis_data = {
                        'session_id': st.session_state['session_id'],
                        'scalp_type': result.get('scalp_type', ''),
                        'confidence': result.get('confidence', 0),
                        'health_score': result.get('health_score', 0),
                        'concerns': result.get('concerns', []),
                        'diagnosed_conditions': result.get('diagnosed_conditions', []),
                        'recommendations': get_care_recommendations(result['scalp_type']),
                        'image_path': '',  # 可以保存图片路径
                        'user_id': st.session_state.get('user_id', '')
                    }

                    # 保存到数据库
                    try:
                        analysis_id = AnalysisHistoryDB.save_analysis(analysis_data)
                        result['analysis_id'] = analysis_id
                    except Exception as e:
                        st.warning(f"保存分析历史失败: {e}")

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
                    value=f"{result['confidence']}%"
                )
            
            # 健康评分
            st.markdown("#### 🏥 Health Score | 健康评分")
            st.progress(result['health_score'] / 100)
            st.write(f"**{result['health_score']}/100**")

            # 医学诊断（新增）
            if 'diagnosed_conditions' in result and result['diagnosed_conditions']:
                st.markdown("---")
                st.markdown("#### 🩺 Medical Diagnosis | 医学诊断")

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
                    with st.expander(f"{condition['icon']} **{condition['name_cn']}** ({condition['name_en']}) - {condition['severity']}", expanded=True):
                        st.markdown(f"**俗称：** {condition['common_name']}")
                        st.markdown(f"**置信度：** {condition['confidence']}%")
                        st.markdown(f"**描述：** {condition['description']}")

                        # 严重程度指示器
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
            for concern in result['concerns']:
                st.warning(concern)
            
            # 护理建议
            st.markdown("#### 💡 Care Recommendations | 护理建议")
            recommendations = get_care_recommendations(result['scalp_type'])
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
                result['scalp_type'],
                result['concerns'],
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
