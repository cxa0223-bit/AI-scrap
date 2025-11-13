"""
用户认证系统 - User Authentication System
支持注册、登录、会话管理
"""
import sqlite3
import hashlib
import secrets
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple


class UserAuthManager:
    """用户认证管理器"""

    def __init__(self, db_path: str = "data/scalp_analyzer.db"):
        """初始化认证管理器"""
        self.db_path = db_path
        self._init_user_tables()

    def _init_user_tables(self):
        """初始化用户相关数据表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT,
                phone TEXT,
                age INTEGER,
                gender TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                is_premium INTEGER DEFAULT 0,
                analysis_count INTEGER DEFAULT 0
            )
        ''')

        # 会话表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # 密码重置令牌表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                used INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        conn.commit()
        conn.close()

    def _hash_password(self, password: str, salt: str) -> str:
        """使用SHA-256和盐值哈希密码"""
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def _generate_salt(self) -> str:
        """生成随机盐值"""
        return secrets.token_hex(16)

    def _generate_user_id(self) -> str:
        """生成唯一用户ID"""
        return f"user_{secrets.token_hex(8)}_{int(datetime.now().timestamp())}"

    def _validate_email(self, email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_password(self, password: str) -> Tuple[bool, str]:
        """
        验证密码强度
        返回: (是否有效, 错误消息)
        """
        if len(password) < 6:
            return False, "密码至少需要6个字符"
        if len(password) > 128:
            return False, "密码不能超过128个字符"
        # 可以添加更多规则
        return True, ""

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = "",
        phone: str = "",
        age: int = None,
        gender: str = ""
    ) -> Tuple[bool, str, Optional[str]]:
        """
        注册新用户

        返回: (成功, 消息, 用户ID)
        """
        # 验证邮箱
        if not self._validate_email(email):
            return False, "邮箱格式无效", None

        # 验证密码
        valid, msg = self._validate_password(password)
        if not valid:
            return False, msg, None

        # 验证用户名
        if len(username) < 3:
            return False, "用户名至少需要3个字符", None
        if len(username) > 50:
            return False, "用户名不能超过50个字符", None

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 检查用户名是否已存在
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                return False, "用户名已被使用", None

            # 检查邮箱是否已存在
            cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                conn.close()
                return False, "邮箱已被注册", None

            # 生成用户ID和盐值
            user_id = self._generate_user_id()
            salt = self._generate_salt()
            password_hash = self._hash_password(password, salt)

            # 插入用户
            cursor.execute('''
                INSERT INTO users (
                    user_id, username, email, password_hash, salt,
                    full_name, phone, age, gender
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, email, password_hash, salt,
                  full_name, phone, age, gender))

            conn.commit()
            conn.close()

            return True, "注册成功！", user_id

        except sqlite3.IntegrityError as e:
            return False, f"数据库错误: {str(e)}", None
        except Exception as e:
            return False, f"注册失败: {str(e)}", None

    def login_user(self, username_or_email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        用户登录

        返回: (成功, 消息, 用户信息)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 查找用户（支持用户名或邮箱登录）
            cursor.execute('''
                SELECT user_id, username, email, password_hash, salt, full_name,
                       is_active, is_premium, analysis_count
                FROM users
                WHERE (username = ? OR email = ?) AND is_active = 1
            ''', (username_or_email, username_or_email))

            user = cursor.fetchone()

            if not user:
                conn.close()
                return False, "用户名或密码错误", None

            # 验证密码
            user_id, username, email, password_hash, salt, full_name, is_active, is_premium, analysis_count = user
            input_hash = self._hash_password(password, salt)

            if input_hash != password_hash:
                conn.close()
                return False, "用户名或密码错误", None

            # 更新最后登录时间
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?
            ''', (user_id,))
            conn.commit()
            conn.close()

            # 返回用户信息
            user_info = {
                'user_id': user_id,
                'username': username,
                'email': email,
                'full_name': full_name,
                'is_premium': bool(is_premium),
                'analysis_count': analysis_count
            }

            return True, "登录成功！", user_info

        except Exception as e:
            return False, f"登录失败: {str(e)}", None

    def create_session(self, user_id: str, duration_days: int = 30) -> Optional[str]:
        """
        创建用户会话

        返回: session_id
        """
        try:
            session_id = f"sess_{secrets.token_hex(16)}"
            expires_at = datetime.now() + timedelta(days=duration_days)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO user_sessions (session_id, user_id, expires_at)
                VALUES (?, ?, ?)
            ''', (session_id, user_id, expires_at))

            conn.commit()
            conn.close()

            return session_id

        except Exception as e:
            try:
                print(f"Create session failed: {e}")
            except (OSError, ValueError):
                pass
            return None

    def validate_session(self, session_id: str) -> Tuple[bool, Optional[Dict]]:
        """
        验证会话是否有效

        返回: (是否有效, 用户信息)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT s.user_id, u.username, u.email, u.full_name,
                       u.is_premium, u.analysis_count, s.expires_at
                FROM user_sessions s
                JOIN users u ON s.user_id = u.user_id
                WHERE s.session_id = ? AND s.is_active = 1
            ''', (session_id,))

            result = cursor.fetchone()
            conn.close()

            if not result:
                return False, None

            user_id, username, email, full_name, is_premium, analysis_count, expires_at = result

            # 检查是否过期
            expires_dt = datetime.fromisoformat(expires_at)
            if datetime.now() > expires_dt:
                return False, None

            user_info = {
                'user_id': user_id,
                'username': username,
                'email': email,
                'full_name': full_name,
                'is_premium': bool(is_premium),
                'analysis_count': analysis_count
            }

            return True, user_info

        except Exception as e:
            try:
                print(f"Validate session failed: {e}")
            except (OSError, ValueError):
                pass
            return False, None

    def logout_user(self, session_id: str) -> bool:
        """注销用户（使会话失效）"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE user_sessions SET is_active = 0 WHERE session_id = ?
            ''', (session_id,))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            try:
                print(f"Logout failed: {e}")
            except (OSError, ValueError):
                pass
            return False

    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """获取用户信息"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT user_id, username, email, full_name, phone, age, gender,
                       created_at, last_login, is_premium, analysis_count
                FROM users WHERE user_id = ?
            ''', (user_id,))

            result = cursor.fetchone()
            conn.close()

            if not result:
                return None

            return {
                'user_id': result[0],
                'username': result[1],
                'email': result[2],
                'full_name': result[3],
                'phone': result[4],
                'age': result[5],
                'gender': result[6],
                'created_at': result[7],
                'last_login': result[8],
                'is_premium': bool(result[9]),
                'analysis_count': result[10]
            }

        except Exception as e:
            try:
                print(f"Get user info failed: {e}")
            except (OSError, ValueError):
                pass
            return None

    def increment_analysis_count(self, user_id: str):
        """增加用户分析次数"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE users SET analysis_count = analysis_count + 1 WHERE user_id = ?
            ''', (user_id,))

            conn.commit()
            conn.close()

        except Exception as e:
            try:
                print(f"Update analysis count failed: {e}")
            except (OSError, ValueError):
                pass


# 便捷函数
def init_user_system(db_path: str = "data/scalp_analyzer.db"):
    """初始化用户系统"""
    return UserAuthManager(db_path)
