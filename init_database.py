#!/usr/bin/env python
"""
数据库初始化脚本
Run this script to initialize the SQLite database and migrate CSV data
"""
import os
import sys

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.database import setup_database, ProductDB, get_db_connection

def main():
    print("=" * 60)
    print("Scalp Analysis System - Database Initialization")
    print("=" * 60)

    # 设置数据库
    setup_database()

    # 验证数据库
    print("\nVerifying database...")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 检查所有表
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)
        tables = cursor.fetchall()
        print(f"\nTables created: {[table['name'] for table in tables]}")

        # 检查产品数量
        cursor.execute("SELECT COUNT(*) as count FROM products")
        product_count = cursor.fetchone()['count']
        print(f"Product count: {product_count}")

        if product_count > 0:
            # 显示一些产品样例
            print("\nProduct samples:")
            products_df = ProductDB.get_all_products()
            for idx, row in products_df.head(3).iterrows():
                print(f"  - {row['name']} ({row['brand']}) - RM {row['price_myr']}")

    print("\n" + "=" * 60)
    print("Database initialization completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()