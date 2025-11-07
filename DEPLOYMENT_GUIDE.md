# 部署指南 | Deployment Guide

## 🚀 Streamlit Cloud 部署

### 步骤 1: 推送到 GitHub

```bash
git add .
git commit -m "Update: Add Claude AI integration with Haiku model"
git push origin main
```

### 步骤 2: 配置 Streamlit Cloud

1. **访问** https://share.streamlit.io/
2. **登录** 使用GitHub账户
3. **新建应用** 点击 "New app"
4. **选择仓库**
   - Repository: `your-username/scalp-analyzer-project`
   - Branch: `main`
   - Main file path: `app.py`

### 步骤 3: 配置 Secrets

在 Streamlit Cloud 的 App Settings → Secrets 中添加:

```toml
# .streamlit/secrets.toml
ANTHROPIC_API_KEY = "your-claude-api-key-here"
```

⚠️ **重要**: 不要将真实的API密钥提交到GitHub！

### 步骤 4: 部署

点击 "Deploy" 按钮，等待应用部署完成（约2-5分钟）

---

## 🔐 环境变量配置

### 方法 1: Streamlit Cloud Secrets（推荐）

在 Streamlit Cloud dashboard:
- Settings → Secrets
- 添加 `ANTHROPIC_API_KEY`

### 方法 2: 本地环境变量

#### Windows:
```batch
set ANTHROPIC_API_KEY=your-key-here
streamlit run app.py
```

#### Linux/Mac:
```bash
export ANTHROPIC_API_KEY=your-key-here
streamlit run app.py
```

### 方法 3: .env 文件（本地开发）

创建 `.env` 文件:
```
ANTHROPIC_API_KEY=your-key-here
```

然后在代码中加载:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 📦 依赖项

确保 `requirements.txt` 包含所有依赖:

```
streamlit>=1.39.0
anthropic>=0.7.0
pillow>=11.0.0
opencv-python-headless>=4.10.0
numpy>=2.0.0
pandas>=2.2.0
matplotlib>=3.9.0
scikit-learn>=1.5.0
scipy>=1.11.0
```

---

## 🔧 配置文件

### .streamlit/config.toml

```toml
[server]
headless = true
port = 8501
enableCORS = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

---

## 🌐 自定义域名（可选）

### Streamlit Cloud

1. 进入 App Settings
2. 点击 "General"
3. 添加自定义域名
4. 按照说明配置DNS

### 其他平台部署

#### Railway:
```bash
railway login
railway init
railway up
```

#### Heroku:
```bash
heroku create your-app-name
git push heroku main
```

#### Docker:
```bash
docker build -t scalp-analyzer .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=your-key scalp-analyzer
```

---

## ⚙️ 使用的模型

**当前模型**: `claude-3-haiku-20240307`

**原因**:
- 免费/入门账户可用
- 快速响应
- 成本低廉
- 图像分析能力优秀

**升级模型** (需要付费账户):
- `claude-3-5-sonnet-20241022` - 更强大
- `claude-3-opus-20240229` - 最强大（但已弃用）

修改模型在 `utils/ai_services.py`:
```python
model="claude-3-haiku-20240307"  # 修改这里
```

---

## 🐛 常见问题

### 问题 1: 模型不可用错误

**错误**: `Error code: 404 - model not found`

**原因**: 账户无权访问该模型

**解决**:
1. 检查账户类型
2. 使用 `claude-3-haiku-20240307`
3. 运行 `python test_available_models.py` 查看可用模型

### 问题 2: Streamlit Cloud 部署失败

**检查**:
1. requirements.txt 正确
2. Python 版本兼容 (3.8-3.11推荐)
3. 没有硬编码路径
4. Secrets 已配置

### 问题 3: API 密钥错误

**检查**:
1. Secrets 拼写正确
2. 密钥格式正确 (sk-ant-api03-...)
3. 密钥有效且有余额

---

## 📊 成本估算

### Claude API 定价 (Haiku模型)

- **输入**: ~$0.25 / 1M tokens
- **输出**: ~$1.25 / 1M tokens

### 每次分析成本

- 平均每张图片: **$0.001 - $0.005**
- 100次分析: **$0.10 - $0.50**
- 1000次分析: **$1.00 - $5.00**

### Streamlit Cloud

- **Community Plan**: 免费
  - 1个公开应用
  - 1GB 内存
  - 无限访问

- **Starter Plan**: $20/月
  - 3个私有应用
  - 更多资源

---

## 🔒 安全最佳实践

1. **永远不要**提交API密钥到GitHub
2. **使用** Streamlit Secrets 或环境变量
3. **启用** .gitignore 排除敏感文件
4. **定期** 轮换API密钥
5. **监控** API使用量和成本
6. **限制** API密钥权限（如果可能）

---

## 📝 部署检查清单

- [ ] 清理所有硬编码的API密钥
- [ ] 更新 .gitignore
- [ ] 测试本地运行正常
- [ ] 提交并推送到GitHub
- [ ] 在Streamlit Cloud创建应用
- [ ] 配置 Secrets
- [ ] 测试线上部署
- [ ] 验证AI功能工作
- [ ] 设置自定义域名（可选）
- [ ] 配置监控和日志（可选）

---

## 🎯 推荐部署流程

### 开发环境
```bash
# 1. 克隆仓库
git clone your-repo-url
cd scalp-analyzer-project

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
set ANTHROPIC_API_KEY=your-key

# 4. 运行应用
streamlit run app.py
```

### 生产环境
1. 推送到 GitHub
2. 在 Streamlit Cloud 部署
3. 配置 Secrets
4. 启用HTTPS（自动）
5. 监控运行状态

---

## 📞 技术支持

- **Streamlit文档**: https://docs.streamlit.io/
- **Anthropic文档**: https://docs.anthropic.com/
- **GitHub Issues**: 项目的 Issues 页面

---

**最后更新**: 2025-11-07
**维护者**: Claude Code
