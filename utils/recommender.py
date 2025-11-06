"""
产品推荐系统模块
基于头皮类型和问题推荐合适的产品
"""
import pandas as pd

def load_products(csv_path='data/products.csv'):
    """加载产品数据库"""
    try:
        products_df = pd.read_csv(csv_path)
        return products_df
    except FileNotFoundError:
        print(f"找不到产品数据文件: {csv_path}")
        return pd.DataFrame()

def recommend_products(scalp_type, concerns, products_df, top_n=3):
    """
    根据头皮类型和问题推荐产品
    
    参数:
        scalp_type: 头皮类型
        concerns: 头皮问题列表
        products_df: 产品数据框
        top_n: 推荐产品数量
    
    返回:
        推荐产品的DataFrame
    """
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
    
    # 如果有具体问题，优先推荐针对性产品
    if concern_keywords:
        priority_products = filtered_products[
            filtered_products['concern'].apply(
                lambda x: any(keyword in str(x) for keyword in concern_keywords)
            )
        ]
        
        if len(priority_products) >= top_n:
            return priority_products.head(top_n)
        else:
            # 如果针对性产品不够，补充其他适合的产品
            remaining = filtered_products[
                ~filtered_products['id'].isin(priority_products['id'])
            ]
            combined = pd.concat([priority_products, remaining])
            return combined.head(top_n)
    
    return filtered_products.head(top_n)

def format_product_card(product, show_image=False):
    """
    格式化产品卡片HTML
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
        <p style="font-size: 13px; color: #555; line-height: 1.5;">{product['description']}</p>
    </div>
    """
