"""
产品推荐系统模块
基于头皮类型和问题推荐合适的产品
Updated to use SQLite database instead of CSV
"""
import pandas as pd
import os
import sys

# 添加database支持
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import ProductDB, RecommendationDB

def load_products(csv_path=None):
    """
    加载产品数据库（从SQLite）
    保留csv_path参数以兼容旧代码
    """
    try:
        # 使用SQLite数据库
        products_df = ProductDB.get_all_products(active_only=True)

        if products_df.empty:
            print("No active products found in database")

        return products_df
    except Exception as e:
        print(f"Error loading products from database: {e}")
        return pd.DataFrame()

def recommend_products(scalp_type, concerns, products_df=None, top_n=3):
    """
    根据头皮类型和问题推荐产品

    参数:
        scalp_type: 头皮类型
        concerns: 头皮问题列表
        products_df: 产品数据框（如果为None，自动从数据库加载）
        top_n: 推荐产品数量

    返回:
        推荐产品的DataFrame
    """
    # 如果没有提供产品数据框，从数据库加载
    if products_df is None:
        products_df = load_products()

    if products_df.empty:
        return pd.DataFrame()

    # 映射头皮类型到中文关键词
    type_mapping = {
        "油性头皮 (Oily Scalp)": "油性",
        "干性头皮 (Dry Scalp)": "干性",
        "正常头皮 (Normal Scalp)": "正常",
        "敏感头皮 (Sensitive Scalp)": "敏感"
    }

    search_type = type_mapping.get(scalp_type, "所有")

    # 筛选适合的产品
    if search_type == "所有":
        filtered_products = products_df.copy()
    else:
        filtered_products = products_df[
            (products_df['suitable_for'].str.contains(search_type, na=False)) |
            (products_df['suitable_for'].str.contains('所有', na=False))
        ]

    # 根据concerns进一步筛选
    concern_keywords = []
    for concern in concerns:
        if "油" in concern:
            concern_keywords.append("油")
        if "干" in concern or "缺水" in concern:
            concern_keywords.append("干")
        if "头屑" in concern:
            concern_keywords.append("头屑")
        if "脱发" in concern or "掉发" in concern:
            concern_keywords.append("脱发")
        if "敏感" in concern or "红肿" in concern:
            concern_keywords.append("敏感")
        if "炎症" in concern:
            concern_keywords.append("炎症")
        if "毛囊" in concern:
            concern_keywords.append("毛囊")

    # 评分系统：根据匹配程度给产品打分
    def score_product(product_row):
        score = 0

        # 头皮类型匹配（基础分）
        if search_type in str(product_row['suitable_for']):
            score += 10
        elif '所有' in str(product_row['suitable_for']):
            score += 5

        # 关注问题匹配（每个匹配加分）
        product_concern = str(product_row['concern']).lower()
        for keyword in concern_keywords:
            if keyword in product_concern:
                score += 5

        # 特殊问题优先级
        if "脱发" in concern_keywords and "脱发" in product_concern:
            score += 10  # 脱发问题优先
        if "头屑" in concern_keywords and "头屑" in product_concern:
            score += 8   # 头屑问题次优先

        return score

    # 给所有产品打分
    filtered_products['recommendation_score'] = filtered_products.apply(score_product, axis=1)

    # 按分数排序，分数相同时按价格排序（价格适中优先）
    filtered_products['price_rank'] = abs(filtered_products['price_myr'] - 35)  # 35是中间价位
    filtered_products = filtered_products.sort_values(
        by=['recommendation_score', 'price_rank'],
        ascending=[False, True]
    )

    # 返回top_n个产品
    recommended = filtered_products.head(top_n)

    # 移除临时列
    if 'recommendation_score' in recommended.columns:
        recommended = recommended.drop(['recommendation_score', 'price_rank'], axis=1, errors='ignore')

    return recommended

def save_recommendation_history(analysis_id, recommended_products):
    """
    保存推荐历史到数据库

    参数:
        analysis_id: 分析记录ID
        recommended_products: 推荐的产品DataFrame
    """
    if recommended_products.empty:
        return

    try:
        product_ids = recommended_products['id'].tolist()
        reasons = []

        for _, product in recommended_products.iterrows():
            reason = f"推荐用于{product['suitable_for']}，针对{product['concern']}"
            reasons.append(reason)

        RecommendationDB.save_recommendations(analysis_id, product_ids, reasons)
    except Exception as e:
        print(f"Error saving recommendation history: {e}")

def get_popular_products(limit=5):
    """
    获取热门产品（被推荐次数最多的）

    参数:
        limit: 返回产品数量

    返回:
        热门产品DataFrame
    """
    try:
        return RecommendationDB.get_popular_products(limit)
    except Exception as e:
        print(f"Error getting popular products: {e}")
        return pd.DataFrame()

def search_products_by_keyword(keyword):
    """
    按关键词搜索产品

    参数:
        keyword: 搜索关键词

    返回:
        匹配的产品DataFrame
    """
    try:
        return ProductDB.search_products(keyword)
    except Exception as e:
        print(f"Error searching products: {e}")
        return pd.DataFrame()

def format_product_card(product, show_image=False):
    """
    格式化产品卡片HTML
    保留原有格式以兼容现有代码
    """
    import os
    import pandas as pd

    # 检查是否有图片
    image_html = ""
    if show_image and 'image' in product.index and pd.notna(product['image']) and product['image']:
        img_path = os.path.join('assets/products', product['image'])
        if os.path.exists(img_path):
            image_html = f'<img src="assets/products/{product["image"]}" style="width: 100%; border-radius: 10px; margin-bottom: 15px;">'
        else:
            image_html = '<img src="https://via.placeholder.com/300x200?text=Product+Image" style="width: 100%; border-radius: 10px; margin-bottom: 15px;">'

    # 添加库存状态显示（如果有）
    stock_html = ""
    if 'stock_quantity' in product.index:
        stock = product.get('stock_quantity', 0)
        if stock > 10:
            stock_html = f'<span style="color: #27ae60;">✓ 库存充足</span>'
        elif stock > 0:
            stock_html = f'<span style="color: #f39c12;">⚠ 库存有限 ({stock})</span>'
        else:
            stock_html = f'<span style="color: #e74c3c;">✗ 暂时缺货</span>'

    return f"""
    <div style="
        border: 2px solid #e0e0e0;
        padding: 20px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        height: 100%;
    ">
        {image_html}
        <h3 style="color: #2c3e50; margin-bottom: 10px;">{product['name']}</h3>
        <p style="color: #7f8c8d; font-size: 14px;"><strong>品牌：</strong>{product['brand']}</p>
        <p style="color: #7f8c8d; font-size: 14px;"><strong>类型：</strong>{product['type']}</p>
        <p style="color: #7f8c8d; font-size: 14px;"><strong>适用：</strong>{product['suitable_for']}</p>
        <p style="color: #27ae60; font-size: 14px;"><strong>针对：</strong>{product['concern']}</p>
        <p style="color: #e74c3c; font-size: 24px; font-weight: bold; margin: 15px 0;">RM {product['price_myr']}</p>
        <p style="font-size: 13px; color: #555; line-height: 1.5;">{product.get('description', '')}</p>
        {stock_html}
    </div>
    """

# 测试函数
if __name__ == "__main__":
    print("Testing product recommendation system with SQLite...")

    # 加载产品
    products = load_products()
    print(f"Loaded {len(products)} products from database")

    # 测试推荐
    if not products.empty:
        test_scalp = "油性头皮 (Oily Scalp)"
        test_concerns = ["头屑", "油腻"]

        recommendations = recommend_products(test_scalp, test_concerns, products)
        print(f"\nRecommendations for {test_scalp} with concerns {test_concerns}:")
        for _, product in recommendations.iterrows():
            print(f"  - {product['name']} (RM {product['price_myr']})")