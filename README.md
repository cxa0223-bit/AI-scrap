# 🔬 Scalp Health AI Analyzer - Malaysia Edition
# 头皮健康AI分析系统 - 马来西亚版

## 📖 Project Overview | 项目概述

A professional AI-powered web application for scalp health analysis, specifically designed for the Malaysian market. Upload scalp images to receive instant AI analysis and personalized product recommendations.

专为马来西亚市场设计的专业AI头皮健康分析网页应用。上传头皮照片即可获得即时AI分析和个性化产品推荐。

## ✨ Features | 功能特点

- 🤖 **AI-Powered Analysis** | AI驱动分析
  - Automatic scalp type detection (oily, dry, normal, sensitive)
  - 自动检测头皮类型（油性、干性、正常、敏感）
  
- 🎯 **Problem Detection** | 问题检测
  - Identifies dandruff, hair loss, inflammation, and more
  - 识别头屑、脱发、炎症等问题
  
- 💡 **Personalized Recommendations** | 个性化推荐
  - Care tips based on your scalp condition
  - 基于头皮状况的护理建议
  
- 🛒 **Product Suggestions** | 产品推荐
  - Curated products available in Malaysia (Shopee, Lazada)
  - 精选马来西亚可购买的产品（Shopee、Lazada）
  
- 🌏 **Bilingual Interface** | 双语界面
  - English & Chinese support
  - 支持英文和中文

## 🚀 Quick Start | 快速开始

### Prerequisites | 前置要求

- Python 3.8 or higher | Python 3.8或更高版本
- pip package manager | pip包管理器

### Installation | 安装步骤

1. **Clone or download this project** | 克隆或下载此项目
```bash
git clone <your-repo-url>
cd scalp-analyzer-project
```

2. **Create virtual environment (recommended)** | 创建虚拟环境（推荐）
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies** | 安装依赖
```bash
pip install -r requirements.txt
```

4. **Run the application** | 运行应用
```bash
streamlit run app.py
```

5. **Open in browser** | 在浏览器打开
```
The app will automatically open at: http://localhost:8501
应用会自动在浏览器打开：http://localhost:8501
```

## 📁 Project Structure | 项目结构

```
scalp-analyzer-project/
├── app.py                      # Main application | 主应用程序
├── requirements.txt            # Python dependencies | Python依赖
├── README.md                   # Documentation | 说明文档
├── data/
│   └── products.csv           # Product database | 产品数据库
├── utils/
│   ├── ai_analyzer.py         # AI analysis module | AI分析模块
│   └── recommender.py         # Recommendation system | 推荐系统
├── models/                     # AI models (future) | AI模型（未来）
└── assets/                     # Images, logos | 图片、Logo
```

## 🛠️ Customization | 自定义

### Adding New Products | 添加新产品

Edit `data/products.csv` to add your own products:
编辑 `data/products.csv` 添加你自己的产品：

```csv
id,name,brand,type,suitable_for,concern,price_myr,link,description
16,Your Product,Brand,Type,Scalp Type,Concern,99.00,https://...,Description
```

### Updating AI Model | 更新AI模型

To integrate your own trained model:
集成你自己训练的模型：

1. Place model file in `models/` directory
2. Update `utils/ai_analyzer.py` to load your model
3. Modify the `analyze_scalp_image()` function

## 🌐 Deployment | 部署

### Option 1: Streamlit Cloud (Free) | 选项1：Streamlit Cloud（免费）

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Option 2: Railway.app

1. Push code to GitHub
2. Visit [railway.app](https://railway.app)
3. Create new project from GitHub repo
4. Deploy automatically

### Option 3: Custom VPS

1. Set up Ubuntu/Debian server
2. Install dependencies
3. Use Nginx as reverse proxy
4. Run with systemd service

## 💰 Cost Estimation | 成本估算

### Free Tier | 免费方案
- **Streamlit Cloud**: Free for public apps
- **Railway.app**: $5 credit/month free
- **Total**: RM 0/month

### Paid Tier | 付费方案
- **Streamlit Cloud**: ~RM 80/month
- **Railway.app**: ~RM 20-40/month
- **Custom VPS**: ~RM 50-100/month
- **Domain**: RM 50-100/year

## 🔐 Security & Privacy | 安全与隐私

- Images are processed in-memory only
- No permanent storage of user photos
- All data transmission is encrypted
- Compliant with Malaysian data protection laws

- 图片仅在内存中处理
- 不永久存储用户照片
- 所有数据传输都已加密
- 符合马来西亚数据保护法

## 📊 Technology Stack | 技术栈

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: TensorFlow, OpenCV, scikit-learn
- **Data**: Pandas, NumPy
- **Deployment**: Streamlit Cloud / Railway / VPS

## 🤝 Contributing | 贡献

Contributions are welcome! Please feel free to submit a Pull Request.
欢迎贡献！请随时提交Pull Request。

## 📝 License | 许可证

This project is licensed under the MIT License.
本项目采用MIT许可证。

## 📧 Contact | 联系方式

- Email: support@scalpanalyzer.my
- WhatsApp: +60 12-345 6789

## 🙏 Acknowledgments | 致谢

- Thanks to all open-source contributors
- Special thanks to the Streamlit community
- Inspired by skincare analysis projects on GitHub

---

**Made with ❤️ for Malaysia | 为马来西亚用心打造**
