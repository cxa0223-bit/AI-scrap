# 部署指南 | Deployment Guide

## 📋 目录
- [Streamlit Cloud 部署（推荐）](#streamlit-cloud)
- [Docker 部署](#docker)
- [Railway 部署](#railway)
- [Google Cloud Run 部署](#google-cloud-run)
- [其他选项](#其他选项)

---

## 🌟 Streamlit Cloud（推荐 - 免费）

### 优势：
- ✅ **完全免费**
- ✅ 专为Streamlit优化
- ✅ 自动从GitHub部署
- ✅ 简单易用，无需DevOps知识
- ✅ 自动HTTPS
- ✅ 适合中小型应用

### 步骤：

1. **将代码推送到GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/scalp-analyzer.git
git push -u origin main
```

2. **登录Streamlit Cloud**
   - 访问: https://streamlit.io/cloud
   - 使用GitHub账号登录

3. **创建新应用**
   - 点击 "New app"
   - 选择你的GitHub仓库
   - 主文件路径: `app.py`
   - 点击 "Deploy"

4. **等待部署完成**
   - 通常需要3-5分钟
   - 会自动安装依赖并启动

### 限制：
- 1GB内存
- 1个CPU核心
- 适合演示和测试

---

## 🐳 Docker 部署

### 本地测试：

```bash
# 构建镜像
docker build -t scalp-analyzer .

# 运行容器
docker run -p 8501:8501 scalp-analyzer
```

### 部署到服务器：

```bash
# 1. 在服务器上拉取代码
git clone https://github.com/你的用户名/scalp-analyzer.git
cd scalp-analyzer

# 2. 构建并运行
docker-compose up -d
```

### docker-compose.yml 示例：

```yaml
version: '3.8'
services:
  scalp-analyzer:
    build: .
    ports:
      - "8501:8501"
    restart: always
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
```

---

## 🚂 Railway（推荐 - 有免费额度）

### 优势：
- ✅ 每月$5免费额度
- ✅ 支持Docker和自动检测
- ✅ 自动HTTPS和域名
- ✅ 简单的环境变量管理
- ✅ 适合生产环境

### 步骤：

1. **访问 Railway**
   - https://railway.app
   - 使用GitHub登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 授权并选择你的仓库

3. **配置**
   - Railway会自动检测Dockerfile
   - 等待自动部署

4. **获取URL**
   - 在Settings中生成域名
   - 或绑定自定义域名

### 成本估算：
- 免费额度: $5/月
- 超出后: ~$0.000463/GB-秒

---

## ☁️ Google Cloud Run

### 优势：
- ✅ 按使用付费
- ✅ 自动扩缩容
- ✅ 适合流量波动大的应用
- ✅ 每月200万请求免费

### 步骤：

1. **安装 Google Cloud SDK**
```bash
# Windows
choco install gcloudsdk

# Mac
brew install --cask google-cloud-sdk
```

2. **登录并设置项目**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

3. **构建并部署**
```bash
# 启用Cloud Run API
gcloud services enable run.googleapis.com

# 构建容器
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/scalp-analyzer

# 部署
gcloud run deploy scalp-analyzer \
  --image gcr.io/YOUR_PROJECT_ID/scalp-analyzer \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1
```

### 成本估算：
- 前200万请求免费
- 之后: ~$0.40/百万请求

---

## 🎯 其他选项

### 1. **Hugging Face Spaces**
- **优势**: 免费、AI/ML友好
- **步骤**:
  1. 创建Space选择Streamlit
  2. 推送代码
- **网址**: https://huggingface.co/spaces

### 2. **Render**
- **优势**: 免费套餐、自动HTTPS
- **限制**: 15分钟无活动会休眠
- **网址**: https://render.com

### 3. **Fly.io**
- **优势**: 全球CDN、每月免费额度
- **网址**: https://fly.io

### 4. **AWS ECS/EC2**
- **优势**: 完全控制、可扩展
- **劣势**: 需要DevOps知识、成本较高

### 5. **Azure Container Instances**
- **优势**: 简单易用
- **成本**: ~$30-50/月

---

## 🎯 推荐决策树

```
是否需要完全免费？
├─ 是 → Streamlit Cloud 或 Hugging Face Spaces
└─ 否
   ├─ 需要更多资源和稳定性？
   │  ├─ 是 → Railway 或 Google Cloud Run
   │  └─ 否 → Render (有休眠限制)
   └─ 需要完全控制？
      └─ 是 → Docker + VPS (DigitalOcean/Vultr)
```

---

## 💡 最佳推荐（针对马来西亚市场）

### 1️⃣ **开发/演示阶段**: Streamlit Cloud
- 完全免费
- 快速部署
- 适合展示给客户

### 2️⃣ **小规模生产**: Railway
- 性价比高
- 有免费额度
- 稳定可靠

### 3️⃣ **大规模生产**: Google Cloud Run (Asia-Southeast1)
- 新加坡节点，延迟低
- 自动扩缩容
- 按需付费

---

## 🔧 部署前检查清单

- [ ] requirements.txt 已更新
- [ ] .streamlit/config.toml 已配置
- [ ] 产品图片已上传到 assets/products/
- [ ] data/products.csv 已包含所有产品
- [ ] 测试所有功能正常运行
- [ ] 设置环境变量（如有API密钥）

---

## 🆘 常见问题

### Q: 图片无法显示？
A: 确保 `assets/products/` 目录和图片都已推送到Git仓库

### Q: 内存不足？
A: 升级到付费套餐或优化图片大小

### Q: 部署后速度慢？
A: 选择离马来西亚更近的服务器区域（如新加坡）

### Q: 如何绑定自定义域名？
A: 各平台都支持，在设置中添加CNAME记录

---

## 📞 获取帮助

如有部署问题，请参考各平台文档：
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Railway: https://docs.railway.app
- Google Cloud: https://cloud.google.com/run/docs

---

**祝部署顺利！Good luck with your deployment! 🚀**
