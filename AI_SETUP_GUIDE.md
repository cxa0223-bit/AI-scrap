# AI Services Setup Guide for Scalp Analyzer
# 头皮分析AI服务设置指南

## 🚀 Quick Start | 快速开始

### Step 1: Install AI Libraries | 安装AI库

```bash
# For Claude (Anthropic)
pip install anthropic

# For OpenAI GPT-4 Vision
pip install openai

# Or install both
pip install anthropic openai
```

### Step 2: Get API Keys | 获取API密钥

#### Claude (Anthropic)
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-api03-`)

#### OpenAI GPT-4 Vision
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Create a new secret key
5. Copy the key (starts with `sk-`)

### Step 3: Configure in App | 在应用中配置

1. Open the Scalp Analyzer app
2. Navigate to **AI Settings** page (🤖 AI Settings)
3. Enable "AI-Enhanced Analysis"
4. Select your preferred AI service
5. Enter your API key
6. Save settings

## 💰 Pricing | 价格

### Claude (Anthropic)
- **Claude 3 Opus**: ~$0.015 per image
- **Claude 3 Sonnet**: ~$0.003 per image
- Best for detailed medical analysis

### OpenAI GPT-4 Vision
- **GPT-4 Vision**: ~$0.01-0.02 per image
- Good for general analysis
- Faster response time

### Local Analysis (Free)
- Rule-based analysis
- No API required
- Good for basic detection

## 🔧 Advanced Configuration | 高级配置

### Environment Variables | 环境变量

For permanent configuration, set environment variables:

```bash
# Windows CMD
set ANTHROPIC_API_KEY=your_claude_api_key
set OPENAI_API_KEY=your_openai_api_key

# Windows PowerShell
$env:ANTHROPIC_API_KEY="your_claude_api_key"
$env:OPENAI_API_KEY="your_openai_api_key"

# Linux/Mac
export ANTHROPIC_API_KEY="your_claude_api_key"
export OPENAI_API_KEY="your_openai_api_key"
```

### Docker Configuration

Add to your `docker-compose.yml`:

```yaml
environment:
  - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
  - OPENAI_API_KEY=${OPENAI_API_KEY}
```

## 📊 Feature Comparison | 功能对比

| Feature | Claude | GPT-4 Vision | Local |
|---------|--------|--------------|-------|
| Accuracy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Speed | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Medical Knowledge | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Disease Detection | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cost | 💵💵 | 💵💵 | Free |
| Language Support | CN/EN | CN/EN | CN/EN |

## 🎯 Best Practices | 最佳实践

1. **Combine Results**: Enable "Combine with Local Analysis" for best accuracy
2. **High-Quality Images**: Upload clear, well-lit scalp photos
3. **Multiple Angles**: Take photos from different angles
4. **Monitor Usage**: Track API usage to control costs
5. **Backup Analysis**: Keep local analysis as fallback

## 🛠️ Troubleshooting | 故障排除

### Common Issues | 常见问题

1. **"API key not valid"**
   - Check if key is correctly copied
   - Ensure no extra spaces
   - Verify key is active

2. **"Rate limit exceeded"**
   - Wait a few minutes
   - Consider upgrading API plan
   - Use local analysis temporarily

3. **"Module not found"**
   - Install required library: `pip install anthropic` or `pip install openai`

4. **"Connection error"**
   - Check internet connection
   - Verify API service status
   - Try again later

## 📚 API Documentation | API文档

- [Claude API Docs](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [OpenAI Vision Docs](https://platform.openai.com/docs/guides/vision)

## 🤝 Support | 支持

For issues or questions:
1. Check this guide
2. Visit the [GitHub Issues](https://github.com/cxa0223-bit/AI-scrap/issues)
3. Contact support through the app

## 📈 Usage Examples | 使用示例

### Example 1: Medical-Grade Analysis
- Service: Claude
- Settings: Enable AI + Combine Results
- Best for: Serious conditions, medical consultation prep

### Example 2: Quick Check
- Service: GPT-4 Vision
- Settings: AI only
- Best for: Daily monitoring, quick assessments

### Example 3: Offline Mode
- Service: Local Analysis
- Settings: Disable AI
- Best for: No internet, privacy concerns, basic checks

---

*Last Updated: November 2024*
*Version: 2.0*