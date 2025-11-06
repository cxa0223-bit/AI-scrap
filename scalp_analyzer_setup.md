# 头皮分析系统 - 完整搭建指南

## 项目结构
```
scalp-analyzer/
├── app.py                    # 主应用文件
├── requirements.txt          # 依赖包
├── models/                   # AI模型文件
│   └── scalp_model.h5
├── data/
│   └── products.csv          # 产品数据库
├── utils/
│   ├── image_processor.py    # 图像处理
│   ├── ai_analyzer.py        # AI分析
│   └── recommender.py        # 推荐系统
└── assets/
    └── logo.png
```

## 第一步：环境安装

### 安装Python（如果还没有）
访问 https://www.python.org/downloads/ 下载Python 3.9+

### 创建项目文件夹
```bash
mkdir scalp-analyzer
cd scalp-analyzer
```

### 创建虚拟环境
```bash
python -m venv venv

# Windows激活
venv\Scripts\activate

# Mac/Linux激活
source venv/bin/activate
```

### 安装依赖包
```bash
pip install streamlit
pip install tensorflow
pip install opencv-python
pip install pillow
pip install pandas
pip install numpy
pip install scikit-learn
```

## 第二步：创建产品数据库

创建 `data/products.csv`：
```csv
id,name,brand,type,suitable_for,concern,price_myr,link,description
1,控油清爽洗发水,潘婷,洗发水,油性头皮,油腻/脱发,28.90,https://shopee.com.my/xxx,深层清洁配方
2,滋润修护洗发水,海飞丝,洗发水,干性头皮,干燥/头屑,32.50,https://shopee.com.my/xxx,保湿滋养配方
3,舒缓敏感洗发水,多芬,洗发水,敏感头皮,瘙痒/红肿,35.00,https://shopee.com.my/xxx,温和无刺激
4,防脱发精华液,霸王,护发精华,所有类型,脱发,89.90,https://shopee.com.my/xxx,强韧发根
5,头皮护理精油,THE BODY SHOP,头皮护理,干性头皮,干燥,68.00,https://shopee.com.my/xxx,天然植物配方
```

## 第三步：创建主应用 app.py

```python
import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np

# 页面配置
st.set_page_config(
    page_title="头皮健康分析系统",
    page_icon="💆",
    layout="wide"
)

# 标题
st.title("🔬 头皮健康AI分析系统")
st.markdown("### 上传您的头皮照片，获取专业分析和产品推荐")

# 侧边栏
with st.sidebar:
    st.header("📋 使用说明")
    st.write("1. 上传头皮检测仪拍摄的照片")
    st.write("2. 等待AI分析（约5-10秒）")
    st.write("3. 查看分析结果和推荐产品")
    st.write("4. 点击链接购买推荐产品")
    
    st.markdown("---")
    st.info("📍 服务地区：马来西亚")

# 主界面
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 上传照片")
    uploaded_file = st.file_uploader(
        "选择头皮照片", 
        type=['jpg', 'jpeg', 'png'],
        help="支持JPG、PNG格式"
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="您上传的照片", use_container_width=True)
        
        # 分析按钮
        if st.button("🔍 开始AI分析", type="primary"):
            with st.spinner("正在分析您的头皮状况..."):
                # 这里调用AI模型（暂时用模拟数据）
                import time
                time.sleep(2)
                
                # 存储分析结果到session
                st.session_state['analyzed'] = True
                st.session_state['scalp_type'] = "油性头皮"
                st.session_state['concerns'] = ["油脂分泌过多", "轻微脱发"]
                st.session_state['confidence'] = 87.5

with col2:
    st.subheader("📊 分析结果")
    
    if 'analyzed' in st.session_state and st.session_state['analyzed']:
        # 显示分析结果
        st.success("✅ 分析完成！")
        
        # 头皮类型
        st.metric(
            label="头皮类型", 
            value=st.session_state['scalp_type'],
            delta=f"置信度: {st.session_state['confidence']}%"
        )
        
        # 主要问题
        st.markdown("**🎯 检测到的问题：**")
        for concern in st.session_state['concerns']:
            st.warning(f"⚠️ {concern}")
        
        # 健康建议
        st.markdown("**💡 护理建议：**")
        st.info("""
        - 建议每2-3天洗一次头发
        - 使用控油洗发产品
        - 避免用过热的水洗头
        - 保持规律作息，减少压力
        """)
    else:
        st.info("👆 请先上传照片并点击分析按钮")

# 产品推荐区域
if 'analyzed' in st.session_state and st.session_state['analyzed']:
    st.markdown("---")
    st.subheader("🛒 为您推荐的产品")
    
    # 读取产品数据库
    try:
        products_df = pd.read_csv('data/products.csv')
        
        # 根据头皮类型筛选产品（简化版）
        recommended_products = products_df[
            products_df['suitable_for'].str.contains('油性', na=False)
        ].head(3)
        
        # 显示产品卡片
        cols = st.columns(3)
        for idx, (_, product) in enumerate(recommended_products.iterrows()):
            with cols[idx]:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; height: 100%;">
                    <h4>{product['name']}</h4>
                    <p><strong>品牌：</strong>{product['brand']}</p>
                    <p><strong>类型：</strong>{product['type']}</p>
                    <p><strong>适用：</strong>{product['suitable_for']}</p>
                    <p style="color: #e74c3c; font-size: 20px; font-weight: bold;">RM {product['price_myr']}</p>
                    <p style="font-size: 14px; color: #666;">{product['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button(
                    "🛍️ 立即购买", 
                    product['link'],
                    use_container_width=True
                )
    except FileNotFoundError:
        st.error("产品数据库文件未找到，请先创建 data/products.csv")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>© 2024 头皮健康分析系统 | 马来西亚专业版</p>
    <p>如有疑问，请联系客服：support@example.com</p>
</div>
""", unsafe_allow_html=True)
```

## 第四步：本地测试运行

```bash
# 确保在项目文件夹内
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

## 第五步：添加真实AI模型（简化版）

创建 `utils/ai_analyzer.py`：

```python
import cv2
import numpy as np
from PIL import Image

def analyze_scalp_image(image):
    """
    简化版头皮分析
    真实项目中应该使用训练好的深度学习模型
    """
    # 转换为numpy数组
    img_array = np.array(image)
    
    # 计算图像的平均亮度和颜色分布
    avg_brightness = np.mean(img_array)
    
    # 简单规则判断（实际应使用AI模型）
    if avg_brightness > 150:
        scalp_type = "油性头皮"
        concerns = ["油脂分泌过多", "可能堵塞毛孔"]
    elif avg_brightness < 100:
        scalp_type = "干性头皮"
        concerns = ["头皮干燥", "可能有头屑"]
    else:
        scalp_type = "正常头皮"
        concerns = ["整体健康", "继续保持"]
    
    confidence = np.random.uniform(80, 95)  # 模拟置信度
    
    return {
        'scalp_type': scalp_type,
        'concerns': concerns,
        'confidence': round(confidence, 1)
    }
```

## 下一步：部署到云端

### 推荐部署平台（马来西亚友好）：

1. **Streamlit Cloud**（免费，最简单）
   - 链接GitHub仓库自动部署
   - 访问：https://share.streamlit.io

2. **Railway.app**（免费额度充足）
   - 支持从GitHub部署
   - 速度快，适合东南亚

3. **Render.com**（免费层）
   - 稳定可靠
   - 东南亚访问速度好

### 部署步骤（以Streamlit Cloud为例）：

1. 将代码上传到GitHub
2. 访问 share.streamlit.io
3. 连接GitHub仓库
4. 点击Deploy
5. 获得公开链接（如：https://your-app.streamlit.app）

## 成本估算（马来西亚）

- 域名：RM 50-100/年（可选）
- Streamlit Cloud：免费
- 如需升级：约RM 80/月
- 总计：初期可以 **RM 0** 开始！

## 马来西亚本地化建议

1. **语言支持**：添加英文/马来文界面切换
2. **支付对接**：集成Shopee/Lazada链接
3. **货币显示**：使用RM（马来西亚林吉特）
4. **产品库**：选择在马来西亚容易购买的品牌
5. **客服支持**：考虑对接WhatsApp Business

## 需要的产品数据

建议收集以下马来西亚常见品牌：
- 潘婷 (Pantene)
- 海飞丝 (Head & Shoulders)
- 多芬 (Dove)
- 霸王 (Ba Wang)
- 清扬 (Clear)
- THE BODY SHOP
- Guardian自有品牌
- Watsons自有品牌
