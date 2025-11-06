"""
产品管理后台 - Product Management Admin
Updated to use SQLite database instead of CSV
"""
import streamlit as st
import pandas as pd
from PIL import Image
import os
import sys
import shutil

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))

from database import ProductDB, init_database, get_db_connection

# 初始化数据库（如果需要）
init_database()

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
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("""
<div class="admin-header">
    <h1>🛠️ 产品管理后台</h1>
    <h3>Product Management Admin Panel</h3>
    <p>基于SQLite数据库的产品管理系统</p>
</div>
""", unsafe_allow_html=True)

# 图片目录
IMAGE_DIR = 'assets/products'
os.makedirs(IMAGE_DIR, exist_ok=True)

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

# 显示统计信息
def show_stats():
    """显示统计信息"""
    col1, col2, col3, col4 = st.columns(4)

    products_df = ProductDB.get_all_products(active_only=False)
    active_products = ProductDB.get_all_products(active_only=True)

    with col1:
        st.markdown("""
        <div class="stats-card">
            <h2>{}</h2>
            <p>总产品数</p>
        </div>
        """.format(len(products_df)), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stats-card" style="background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);">
            <h2>{}</h2>
            <p>活跃产品</p>
        </div>
        """.format(len(active_products)), unsafe_allow_html=True)

    with col3:
        avg_price = active_products['price_myr'].mean() if not active_products.empty else 0
        st.markdown("""
        <div class="stats-card" style="background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);">
            <h2>RM {:.2f}</h2>
            <p>平均价格</p>
        </div>
        """.format(avg_price), unsafe_allow_html=True)

    with col4:
        # 计算有图片的产品数
        with_images = len(active_products[active_products['image'].notna() & (active_products['image'] != '')])
        st.markdown("""
        <div class="stats-card" style="background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);">
            <h2>{}</h2>
            <p>有图片产品</p>
        </div>
        """.format(with_images), unsafe_allow_html=True)

# 显示统计
show_stats()

# 主界面
tabs = st.tabs(["📋 产品列表", "➕ 添加产品", "✏️ 编辑产品", "🗑️ 删除产品", "🔍 搜索产品"])

# Tab 1: 产品列表
with tabs[0]:
    st.markdown("### 📋 当前产品列表 | Current Products")

    # 选项
    col1, col2 = st.columns([2, 1])
    with col1:
        show_inactive = st.checkbox("显示已停用产品", value=False)
    with col2:
        if st.button("🔄 刷新数据", use_container_width=True):
            st.rerun()

    products_df = ProductDB.get_all_products(active_only=not show_inactive)

    if not products_df.empty:
        st.info(f"共有 {len(products_df)} 个{'活跃' if not show_inactive else ''}产品")

        # 显示产品
        for idx, product in products_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 3, 1, 1])

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

                    # 显示状态
                    if product.get('is_active', True):
                        st.success("✅ 活跃")
                    else:
                        st.error("❌ 已停用")

                with col3:
                    # 库存信息
                    stock = product.get('stock_quantity', 100)
                    if stock > 10:
                        st.success(f"库存: {stock}")
                    elif stock > 0:
                        st.warning(f"库存: {stock}")
                    else:
                        st.error("缺货")

                with col4:
                    # 图片状态
                    if pd.notna(product.get('image')) and product['image']:
                        st.success("✅ 有图片")
                    else:
                        st.warning("⚠️ 无图片")

                st.markdown("---")
    else:
        st.warning("暂无产品数据")

# Tab 2: 添加产品
with tabs[1]:
    st.markdown("### ➕ 添加新产品 | Add New Product")

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
            st.markdown("#### 价格与库存 | Price & Stock")
            new_price = st.number_input("价格 (RM) | Price *", min_value=0.0, step=0.1, format="%.2f")
            new_stock = st.number_input("库存数量 | Stock Quantity", min_value=0, value=100)
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
                # 先添加产品到数据库
                product_data = {
                    'name': new_name,
                    'brand': new_brand,
                    'type': new_type,
                    'suitable_for': new_suitable,
                    'concern': new_concern,
                    'price_myr': new_price,
                    'link': new_link,
                    'description': new_description,
                    'image': '',
                    'stock_quantity': new_stock
                }

                # 添加到数据库
                new_id = ProductDB.add_product(product_data)

                # 保存图片
                if new_image and new_id:
                    image_filename = save_uploaded_image(new_image, new_id)
                    # 更新图片路径
                    ProductDB.update_product(new_id, {'image': image_filename})

                st.success(f"✅ 产品添加成功！ID: {new_id}")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ 请填写所有必填项（标*）")

# Tab 3: 编辑产品
with tabs[2]:
    st.markdown("### ✏️ 编辑产品 | Edit Product")

    products_df = ProductDB.get_all_products(active_only=False)

    if not products_df.empty:
        # 选择要编辑的产品
        product_options = products_df.apply(
            lambda x: f"ID {x['id']}: {x['name']} ({x['brand']})", axis=1
        ).tolist()

        selected_product = st.selectbox("选择要编辑的产品 | Select Product", product_options)
        selected_id = int(selected_product.split(":")[0].replace("ID ", ""))

        # 获取产品数据
        product = ProductDB.get_product_by_id(selected_id)

        if product:
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
                    edit_active = st.checkbox("产品活跃", value=product.get('is_active', True))

                with col2:
                    st.markdown("#### 价格与库存 | Price & Stock")
                    edit_price = st.number_input("价格 (RM)", min_value=0.0, value=float(product['price_myr']), step=0.1, format="%.2f")
                    edit_stock = st.number_input("库存数量", min_value=0, value=product.get('stock_quantity', 100))
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
                    # 准备更新数据
                    update_data = {
                        'name': edit_name,
                        'brand': edit_brand,
                        'type': edit_type,
                        'suitable_for': edit_suitable,
                        'concern': edit_concern,
                        'price_myr': edit_price,
                        'link': edit_link,
                        'description': edit_description,
                        'stock_quantity': edit_stock,
                        'is_active': edit_active
                    }

                    # 处理图片更新
                    if edit_image:
                        image_filename = save_uploaded_image(edit_image, selected_id)
                        update_data['image'] = image_filename

                    # 更新数据库
                    if ProductDB.update_product(selected_id, update_data):
                        st.success("✅ 产品更新成功！")
                        st.rerun()
                    else:
                        st.error("❌ 更新失败")
    else:
        st.warning("暂无产品可编辑")

# Tab 4: 删除产品
with tabs[3]:
    st.markdown("### 🗑️ 删除产品 | Delete Product")

    products_df = ProductDB.get_all_products(active_only=False)

    if not products_df.empty:
        st.warning("⚠️ 删除操作不可恢复，请谨慎操作！")

        # 删除方式选择
        delete_mode = st.radio("删除方式", ["软删除（标记为停用）", "硬删除（永久删除）"])

        # 选择要删除的产品
        product_options = products_df.apply(
            lambda x: f"ID {x['id']}: {x['name']} ({x['brand']})", axis=1
        ).tolist()

        selected_product = st.selectbox("选择要删除的产品 | Select Product to Delete", product_options, key="delete_select")
        selected_id = int(selected_product.split(":")[0].replace("ID ", ""))

        # 获取产品信息
        product = ProductDB.get_product_by_id(selected_id)

        if product:
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
                st.markdown(f"**库存:** {product.get('stock_quantity', 0)}")

                if product.get('is_active', True):
                    st.success("当前状态: ✅ 活跃")
                else:
                    st.error("当前状态: ❌ 已停用")

            st.markdown("---")

            # 确认删除
            confirm = st.checkbox(f"我确认要{'停用' if delete_mode == '软删除（标记为停用）' else '永久删除'}这个产品")

            if st.button("🗑️ 删除产品 | Delete Product", type="primary", disabled=not confirm, use_container_width=True):
                soft_delete = (delete_mode == "软删除（标记为停用）")

                # 如果是硬删除，删除图片文件
                if not soft_delete and pd.notna(product.get('image')) and product['image']:
                    img_path = os.path.join(IMAGE_DIR, product['image'])
                    if os.path.exists(img_path):
                        try:
                            os.remove(img_path)
                        except Exception as e:
                            st.warning(f"图片删除失败: {e}")

                # 删除产品
                if ProductDB.delete_product(selected_id, soft_delete=soft_delete):
                    if soft_delete:
                        st.success("✅ 产品已停用！")
                    else:
                        st.success("✅ 产品已永久删除！")
                    st.rerun()
                else:
                    st.error("❌ 删除失败")
    else:
        st.warning("暂无产品可删除")

# Tab 5: 搜索产品
with tabs[4]:
    st.markdown("### 🔍 搜索产品 | Search Products")

    search_keyword = st.text_input("输入搜索关键词（产品名、品牌、类型、描述等）", placeholder="例如: 洗发水")

    if st.button("🔍 搜索", type="primary", use_container_width=True) or search_keyword:
        if search_keyword:
            results = ProductDB.search_products(search_keyword)

            if not results.empty:
                st.success(f"找到 {len(results)} 个相关产品")

                for idx, product in results.iterrows():
                    with st.container():
                        col1, col2, col3 = st.columns([1, 3, 1])

                        with col1:
                            if pd.notna(product.get('image')) and product['image']:
                                img_path = os.path.join(IMAGE_DIR, product['image'])
                                if os.path.exists(img_path):
                                    st.image(img_path, width=100)

                        with col2:
                            st.markdown(f"**{product['name']}** ({product['brand']})")
                            st.markdown(f"类型: {product['type']} | 价格: RM {product['price_myr']}")
                            st.markdown(f"描述: {product['description']}")

                        with col3:
                            st.markdown(f"库存: {product.get('stock_quantity', 0)}")
                            if product.get('is_active', True):
                                st.success("✅ 活跃")
                            else:
                                st.error("❌ 停用")

                        st.markdown("---")
            else:
                st.warning(f"未找到包含 '{search_keyword}' 的产品")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p><strong>🛠️ 产品管理后台</strong></p>
    <p style="font-size: 12px;">SQLite Database Powered | Product Management Admin Panel</p>
</div>
""", unsafe_allow_html=True)