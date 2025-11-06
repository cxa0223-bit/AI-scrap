"""
SQLite数据库模型和管理
Database models and management
"""
import os
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
import pandas as pd
from contextlib import contextmanager

# 数据库文件路径
DB_PATH = "data/scalp_analyzer.db"

@contextmanager
def get_db_connection():
    """获取数据库连接的上下文管理器"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 返回字典式的行
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """初始化数据库表结构"""
    os.makedirs("data", exist_ok=True)

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 产品表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            type TEXT NOT NULL,
            suitable_for TEXT NOT NULL,
            concern TEXT NOT NULL,
            price_myr REAL NOT NULL,
            link TEXT,
            description TEXT,
            image TEXT,
            stock_quantity INTEGER DEFAULT 100,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 分析历史表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            session_id TEXT NOT NULL,
            scalp_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            health_score INTEGER NOT NULL,
            concerns TEXT,  -- JSON字符串
            diagnosed_conditions TEXT,  -- JSON字符串
            recommendations TEXT,  -- JSON字符串
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 用户表（基础版，未来扩展）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            nickname TEXT,
            email TEXT,
            phone TEXT,
            analysis_count INTEGER DEFAULT 0,
            last_analysis_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 产品推荐记录表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            rank INTEGER NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (analysis_id) REFERENCES analysis_history(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)

        # 创建索引以提高查询性能
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_suitable ON products(suitable_for)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_concern ON products(concern)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_active ON products(is_active)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analysis_session ON analysis_history(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analysis_created ON analysis_history(created_at)")

        conn.commit()
        print("Database tables initialized successfully")

# 产品相关操作
class ProductDB:
    @staticmethod
    def get_all_products(active_only=True) -> pd.DataFrame:
        """获取所有产品"""
        with get_db_connection() as conn:
            query = "SELECT * FROM products"
            if active_only:
                query += " WHERE is_active = 1"
            query += " ORDER BY id"
            return pd.read_sql_query(query, conn)

    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Dict]:
        """根据ID获取产品"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    @staticmethod
    def add_product(product_data: Dict) -> int:
        """添加新产品"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            columns = ['name', 'brand', 'type', 'suitable_for', 'concern',
                      'price_myr', 'link', 'description', 'image']
            values = [product_data.get(col, '') for col in columns]

            placeholders = ','.join(['?' for _ in columns])
            columns_str = ','.join(columns)

            cursor.execute(
                f"INSERT INTO products ({columns_str}) VALUES ({placeholders})",
                values
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update_product(product_id: int, product_data: Dict) -> bool:
        """更新产品信息"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 构建更新语句
            update_fields = []
            values = []
            for key, value in product_data.items():
                if key != 'id':  # 跳过ID字段
                    update_fields.append(f"{key} = ?")
                    values.append(value)

            # 添加更新时间
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(product_id)

            query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete_product(product_id: int, soft_delete=True) -> bool:
        """删除产品（软删除或硬删除）"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            if soft_delete:
                cursor.execute(
                    "UPDATE products SET is_active = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (product_id,)
                )
            else:
                cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def search_products(keyword: str) -> pd.DataFrame:
        """搜索产品"""
        with get_db_connection() as conn:
            query = """
            SELECT * FROM products
            WHERE is_active = 1
            AND (
                name LIKE ? OR
                brand LIKE ? OR
                type LIKE ? OR
                description LIKE ? OR
                concern LIKE ?
            )
            ORDER BY name
            """
            keyword_pattern = f"%{keyword}%"
            params = [keyword_pattern] * 5
            return pd.read_sql_query(query, conn, params=params)

# 分析历史相关操作
class AnalysisHistoryDB:
    @staticmethod
    def save_analysis(analysis_data: Dict) -> int:
        """保存分析结果"""
        import json

        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 将列表和字典转换为JSON字符串
            concerns_json = json.dumps(analysis_data.get('concerns', []), ensure_ascii=False)
            conditions_json = json.dumps(analysis_data.get('diagnosed_conditions', []), ensure_ascii=False)
            recommendations_json = json.dumps(analysis_data.get('recommendations', []), ensure_ascii=False)

            cursor.execute("""
            INSERT INTO analysis_history
            (session_id, scalp_type, confidence, health_score, concerns,
             diagnosed_conditions, recommendations, image_path, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis_data.get('session_id', ''),
                analysis_data.get('scalp_type', ''),
                analysis_data.get('confidence', 0),
                analysis_data.get('health_score', 0),
                concerns_json,
                conditions_json,
                recommendations_json,
                analysis_data.get('image_path', ''),
                analysis_data.get('user_id', '')
            ))

            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_user_history(session_id: str, limit: int = 10) -> List[Dict]:
        """获取用户的分析历史"""
        import json

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM analysis_history
            WHERE session_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """, (session_id, limit))

            history = []
            for row in cursor.fetchall():
                record = dict(row)
                # 解析JSON字符串
                record['concerns'] = json.loads(record.get('concerns', '[]'))
                record['diagnosed_conditions'] = json.loads(record.get('diagnosed_conditions', '[]'))
                record['recommendations'] = json.loads(record.get('recommendations', '[]'))
                history.append(record)

            return history

    @staticmethod
    def get_statistics() -> Dict:
        """获取统计数据"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 总分析次数
            cursor.execute("SELECT COUNT(*) as total FROM analysis_history")
            total_analyses = cursor.fetchone()['total']

            # 今日分析次数
            cursor.execute("""
            SELECT COUNT(*) as today FROM analysis_history
            WHERE DATE(created_at) = DATE('now')
            """)
            today_analyses = cursor.fetchone()['today']

            # 各头皮类型分布
            cursor.execute("""
            SELECT scalp_type, COUNT(*) as count
            FROM analysis_history
            GROUP BY scalp_type
            """)
            scalp_distribution = {row['scalp_type']: row['count'] for row in cursor.fetchall()}

            # 平均健康评分
            cursor.execute("SELECT AVG(health_score) as avg_score FROM analysis_history")
            avg_health_score = cursor.fetchone()['avg_score'] or 0

            return {
                'total_analyses': total_analyses,
                'today_analyses': today_analyses,
                'scalp_distribution': scalp_distribution,
                'avg_health_score': round(avg_health_score, 1)
            }

# 推荐记录相关操作
class RecommendationDB:
    @staticmethod
    def save_recommendations(analysis_id: int, product_ids: List[int], reasons: List[str] = None):
        """保存推荐记录"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            for rank, product_id in enumerate(product_ids, 1):
                reason = reasons[rank-1] if reasons and len(reasons) >= rank else "基于AI分析推荐"
                cursor.execute("""
                INSERT INTO recommendation_history
                (analysis_id, product_id, rank, reason)
                VALUES (?, ?, ?, ?)
                """, (analysis_id, product_id, rank, reason))

            conn.commit()

    @staticmethod
    def get_popular_products(limit: int = 10) -> pd.DataFrame:
        """获取最受欢迎的产品（推荐最多的）"""
        with get_db_connection() as conn:
            query = """
            SELECT p.*, COUNT(r.id) as recommendation_count
            FROM products p
            LEFT JOIN recommendation_history r ON p.id = r.product_id
            WHERE p.is_active = 1
            GROUP BY p.id
            ORDER BY recommendation_count DESC
            LIMIT ?
            """
            return pd.read_sql_query(query, conn, params=(limit,))

# 数据迁移函数
def migrate_from_csv():
    """从CSV文件迁移数据到SQLite"""
    import os

    csv_path = "data/products.csv"

    if not os.path.exists(csv_path):
        print("CSV file not found, skipping migration")
        return False

    try:
        # 读取CSV数据
        df = pd.read_csv(csv_path)

        with get_db_connection() as conn:
            # 先清空产品表（如果需要）
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM products")
            if cursor.fetchone()['count'] > 0:
                print("Database already has product data, skipping migration")
                return False

            # 迁移数据到SQLite
            for _, row in df.iterrows():
                product_data = {
                    'name': row.get('name', ''),
                    'brand': row.get('brand', ''),
                    'type': row.get('type', ''),
                    'suitable_for': row.get('suitable_for', ''),
                    'concern': row.get('concern', ''),
                    'price_myr': float(row.get('price_myr', 0)),
                    'link': row.get('link', ''),
                    'description': row.get('description', ''),
                    'image': row.get('image', '')
                }
                ProductDB.add_product(product_data)

            print(f"Successfully migrated {len(df)} products to SQLite database")
            return True

    except Exception as e:
        print(f"Data migration failed: {e}")
        return False

# 初始化函数
def setup_database():
    """设置数据库（初始化并迁移数据）"""
    # 初始化数据库结构
    init_database()

    # 从CSV迁移数据
    migrate_from_csv()

    # 显示统计信息
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM products WHERE is_active = 1")
        product_count = cursor.fetchone()['count']
        print(f"Database has {product_count} active products")

if __name__ == "__main__":
    # 测试数据库设置
    setup_database()