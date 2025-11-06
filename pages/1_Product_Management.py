"""
产品管理后台 - Product Management Admin
"""
import streamlit as st
import pandas as pd
from PIL import Image
import os
import shutil

# 页面配置
st.set_page_config(
    page_title="产品管理后台 | Product Management",
    page_icon="🛠️",
    layout="wide"
)

# 自定义CSS
st.markdown("""
<style>
    .admin-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .product-card {
        border: 2px solid #e0e0e0;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("""
<div class="admin-header">
    <h1>🛠️ 产品管理后台</h1>
    <h3>Product Management Admin Panel</h3>
</div>
""", unsafe_allow_html=True)

# 数据文件路径
CSV_PATH = 'data/products.csv'
IMAGE_DIR = 'assets/products'

# 确保目录存在
os.makedirs(IMAGE_DIR, exist_ok=True)

# 加载产品数据
@st.cache_data
def load_products():
    try:
        df = pd.read_csv(CSV_PATH)
        return df
    except Exception as e:
        st.error(f"加载产品数据失败: {e}")
        return pd.DataFrame()

def save_products(df):
    """保存产品数据到CSV"""
    try:
        df.to_csv(CSV_PATH, index=False)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"保存失败: {e}")
        return False

def save_uploaded_image(uploaded_file, product_id):
    """保存上传的图片"""
    if uploaded_file is not None:
        # 获取文件扩展名
        ext = uploaded_file.name.split('.')[-1]
        filename = f"product_{product_id}.{ext}"
        filepath = os.path.join(IMAGE_DIR, filename)

        # 保存文件
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return filename
    return None

# 主界面
tabs = st.tabs(["📋 产品列表", "➕ 添加产品", "✏️ 编辑产品", "🗑️ 删除产品"])

# Tab 1: 产品列表
with tabs[0]:
    st.markdown("### 📋 当前产品列表 | Current Products")

    products_df = load_products()

    if not products_df.empty:
        st.info(f"共有 {len(products_df)} 个产品")

        # 显示产品
        for idx, product in products_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])

                with col1:
                    # 显示产品图片
                    if pd.notna(product.get('image')) and product['image']:
                        img_path = os.path.join(IMAGE_DIR, product['image'])
                        if os.path.exists(img_path):
                            st.image(img_path, width=150)
                        else:
                            st.image("https://via.placeholder.com/150x150?text=No+Image", width=150)
                    else:
                        st.image("https://via.placeholder.com/150x150?text=No+Image", width=150)

                with col2:
                    st.markdown(f"**ID:** {product['id']} | **产品:** {product['name']}")
                    st.markdown(f"**品牌:** {product['brand']} | **类型:** {product['type']}")
                    st.markdown(f"**适用:** {product['suitable_for']} | **针对:** {product['concern']}")
                    st.markdown(f"**价格:** RM {product['price_myr']}")
                    st.markdown(f"**描述:** {product['description']}")

                with col3:
                    st.markdown(f"**图片:**")
                    if pd.notna(product.get('image')) and product['image']:
                        st.success("✅ 已上传")
                    else:
                        st.warning("⚠️ 未上传")

                st.markdown("---")
    else:
        st.warning("暂无产品数据")

# Tab 2: 添加产品
with tabs[1]:
    st.markdown("### ➕ 添加新产品 | Add New Product")

    products_df = load_products()
    next_id = products_df['id'].max() + 1 if not products_df.empty else 1

    with st.form("add_product_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 基本信息 | Basic Info")
            new_name = st.text_input("产品名称 | Product Name *", placeholder="例如: Anti-Dandruff Shampoo")
            new_brand = st.text_input("品牌 | Brand *", placeholder="例如: Head & Shoulders")
            new_type = st.selectbox("产品类型 | Type *",
                                    ["洗发水", "护发素", "护发精华", "头皮护理", "生发水"])
            new_suitable = st.selectbox("适用头皮 | Suitable For *",
                                       ["油性头皮", "干性头皮", "正常头皮", "敏感头皮", "所有类型", "染发发质", "细软发质"])
            new_concern = st.text_input("针对问题 | Concern *",
                                       placeholder="例如: 头屑/油腻")

        with col2:
            st.markdown("#### 价格与链接 | Price & Link")
            new_price = st.number_input("价格 (RM) | Price *", min_value=0.0, step=0.1, format="%.2f")
            new_link = st.text_input("购买链接 | Purchase Link *",
                                    placeholder="https://shopee.com.my/...")
            new_description = st.text_area("产品描述 | Description *",
                                          placeholder="描述产品特点...")

            st.markdown("#### 产品图片 | Product Image")
            new_image = st.file_uploader("上传产品图片 | Upload Image",
                                        type=['jpg', 'jpeg', 'png'],
                                        help="支持JPG、PNG格式")

            if new_image:
                st.image(new_image, caption="预览", width=200)

        submitted = st.form_submit_button("✅ 添加产品 | Add Product", type="primary", use_container_width=True)

        if submitted:
            if new_name and new_brand and new_price > 0:
                # 保存图片
                image_filename = ""
                if new_image:
                    image_filename = save_uploaded_image(new_image, next_id)

                # 创建新产品
                new_product = {
                    'id': next_id,
                    'name': new_name,
                    'brand': new_brand,
                    'type': new_type,
                    'suitable_for': new_suitable,
                    'concern': new_concern,
                    'price_myr': new_price,
                    'link': new_link,
                    'description': new_description,
                    'image': image_filename
                }

                # 添加到DataFrame
                products_df = pd.concat([products_df, pd.DataFrame([new_product])], ignore_index=True)

                # 保存
                if save_products(products_df):
                    st.success(f"✅ 产品添加成功！ID: {next_id}")
                    st.balloons()
                    st.rerun()
            else:
                st.error("⚠️ 请填写所有必填项（标*）")

# Tab 3: 编辑产品
with tabs[2]:
    st.markdown("### ✏️ 编辑产品 | Edit Product")

    products_df = load_products()

    if not products_df.empty:
        # 选择要编辑的产品
        product_options = products_df.apply(
            lambda x: f"ID {x['id']}: {x['name']} ({x['brand']})", axis=1
        ).tolist()

        selected_product = st.selectbox("选择要编辑的产品 | Select Product", product_options)
        selected_id = int(selected_product.split(":")[0].replace("ID ", ""))

        # 获取产品数据
        product = products_df[products_df['id'] == selected_id].iloc[0]

        with st.form("edit_product_form"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 基本信息 | Basic Info")
                edit_name = st.text_input("产品名称", value=product['name'])
                edit_brand = st.text_input("品牌", value=product['brand'])
                edit_type = st.selectbox("产品类型",
                                        ["洗发水", "护发素", "护发精华", "头皮护理", "生发水"],
                                        index=["洗发水", "护发素", "护发精华", "头皮护理", "生发水"].index(product['type']) if product['type'] in ["洗发水", "护发素", "护发精华", "头皮护理", "生发水"] else 0)
                edit_suitable = st.selectbox("适用头皮",
                                           ["油性头皮", "干性头皮", "正常头皮", "敏感头皮", "所有类型", "染发发质", "细软发质"],
                                           index=["油性头皮", "干性头皮", "正常头皮", "敏感头皮", "所有类型", "染发发质", "细软发质"].index(product['suitable_for']) if product['suitable_for'] in ["油性头皮", "干性头皮", "正常头皮", "敏感头皮", "所有类型", "染发发质", "细软发质"] else 0)
                edit_concern = st.text_input("针对问题", value=product['concern'])

            with col2:
                st.markdown("#### 价格与链接 | Price & Link")
                edit_price = st.number_input("价格 (RM)", min_value=0.0, value=float(product['price_myr']), step=0.1, format="%.2f")
                edit_link = st.text_input("购买链接", value=product['link'])
                edit_description = st.text_area("产品描述", value=product['description'])

                st.markdown("#### 产品图片 | Product Image")

                # 显示当前图片
                if pd.notna(product.get('image')) and product['image']:
                    img_path = os.path.join(IMAGE_DIR, product['image'])
                    if os.path.exists(img_path):
                        st.image(img_path, caption="当前图片", width=200)

                edit_image = st.file_uploader("上传新图片（留空保持不变）",
                                            type=['jpg', 'jpeg', 'png'],
                                            key="edit_image")

                if edit_image:
                    st.image(edit_image, caption="新图片预览", width=200)

            submitted = st.form_submit_button("💾 保存修改 | Save Changes", type="primary", use_container_width=True)

            if submitted:
                # 更新图片
                image_filename = product.get('image', '')
                if edit_image:
                    image_filename = save_uploaded_image(edit_image, selected_id)

                # 更新产品信息
                products_df.loc[products_df['id'] == selected_id, 'name'] = edit_name
                products_df.loc[products_df['id'] == selected_id, 'brand'] = edit_brand
                products_df.loc[products_df['id'] == selected_id, 'type'] = edit_type
                products_df.loc[products_df['id'] == selected_id, 'suitable_for'] = edit_suitable
                products_df.loc[products_df['id'] == selected_id, 'concern'] = edit_concern
                products_df.loc[products_df['id'] == selected_id, 'price_myr'] = edit_price
                products_df.loc[products_df['id'] == selected_id, 'link'] = edit_link
                products_df.loc[products_df['id'] == selected_id, 'description'] = edit_description
                products_df.loc[products_df['id'] == selected_id, 'image'] = image_filename

                if save_products(products_df):
                    st.success("✅ 产品更新成功！")
                    st.rerun()
    else:
        st.warning("暂无产品可编辑")

# Tab 4: 删除产品
with tabs[3]:
    st.markdown("### 🗑️ 删除产品 | Delete Product")

    products_df = load_products()

    if not products_df.empty:
        st.warning("⚠️ 删除操作不可恢复，请谨慎操作！")

        # 选择要删除的产品
        product_options = products_df.apply(
            lambda x: f"ID {x['id']}: {x['name']} ({x['brand']})", axis=1
        ).tolist()

        selected_product = st.selectbox("选择要删除的产品 | Select Product to Delete", product_options, key="delete_select")
        selected_id = int(selected_product.split(":")[0].replace("ID ", ""))

        # 显示产品信息
        product = products_df[products_df['id'] == selected_id].iloc[0]

        col1, col2 = st.columns([1, 2])
        with col1:
            if pd.notna(product.get('image')) and product['image']:
                img_path = os.path.join(IMAGE_DIR, product['image'])
                if os.path.exists(img_path):
                    st.image(img_path, width=200)

        with col2:
            st.markdown(f"**产品名称:** {product['name']}")
            st.markdown(f"**品牌:** {product['brand']}")
            st.markdown(f"**类型:** {product['type']}")
            st.markdown(f"**价格:** RM {product['price_myr']}")

        st.markdown("---")

        # 确认删除
        confirm = st.checkbox("我确认要删除这个产品 | I confirm to delete this product")

        if st.button("🗑️ 删除产品 | Delete Product", type="primary", disabled=not confirm, use_container_width=True):
            # 删除图片文件
            if pd.notna(product.get('image')) and product['image']:
                img_path = os.path.join(IMAGE_DIR, product['image'])
                if os.path.exists(img_path):
                    os.remove(img_path)

            # 删除产品
            products_df = products_df[products_df['id'] != selected_id]

            if save_products(products_df):
                st.success("✅ 产品已删除！")
                st.rerun()
    else:
        st.warning("暂无产品可删除")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p><strong>🛠️ 产品管理后台</strong></p>
    <p style="font-size: 12px;">Product Management Admin Panel | Scalp Analyzer</p>
</div>
""", unsafe_allow_html=True)
