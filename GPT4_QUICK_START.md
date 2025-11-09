# GPT-4 快速启动指南

## ✅ GPT-4 已完全集成！

你的头皮分析系统**默认使用 GPT-4**，无需额外配置。

---

## 🚀 快速开始

### 方法 1: 使用环境变量（推荐）

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-your-openai-api-key-here"
streamlit run app.py
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-your-openai-api-key-here
streamlit run app.py
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
streamlit run app.py
```

### 方法 2: 在界面中输入

1. 运行应用: `streamlit run app.py`
2. 上传头皮图片
3. **AI 增强分析已默认勾选** ✅
4. **GPT-4 已默认选中** ✅
5. 输入你的 OpenAI API 密钥
6. 点击"开始AI分析"

---

## 🤖 支持的 GPT-4 模型

系统会**自动尝试**以下模型（按优先级）:

### GPT-5 系列（未来支持）🚀
- `gpt-5` - 基础版
- `gpt-5-preview` - 预览版
- `gpt-5-turbo` - Turbo版

### GPT-4.5 系列（如果存在）
- `gpt-4.5`
- `gpt-4.5-turbo`

### GPT-4 系列（当前可用）⭐
- **`gpt-4o`** - GPT-4 Omni，最新最强
- **`gpt-4o-mini`** - 经济实惠，大多数用户可用
- `gpt-4-turbo` - 高性能
- `gpt-4-vision-preview` - 稳定版本

系统会从最新的模型开始尝试，自动回退到可用的模型。

---

## 💰 成本估算

### GPT-4o (最新)
- 输入: ~$2.50 / 1M tokens
- 输出: ~$10.00 / 1M tokens
- **每次分析**: $0.01 - $0.03
- **100次分析**: $1.00 - $3.00
- **1000次分析**: $10.00 - $30.00

### GPT-4o-mini (经济)
- 输入: ~$0.15 / 1M tokens
- 输出: ~$0.60 / 1M tokens
- **每次分析**: $0.002 - $0.01
- **100次分析**: $0.20 - $1.00
- **1000次分析**: $2.00 - $10.00

---

## 🎯 当前默认配置

```python
# 系统默认设置
默认AI服务: GPT-4 (OpenAI)
默认启用AI: ✅ 是
自动模型选择: ✅ 是
自动环境变量: ✅ 是
图像增强: ✅ 是
```

---

## 📊 GPT-4 vs Claude 对比

| 特性 | GPT-4 (OpenAI) | Claude (Anthropic) |
|------|----------------|-------------------|
| **视觉分析** | ⭐⭐⭐⭐⭐ 最强 | ⭐⭐⭐⭐ 很强 |
| **医学诊断** | ⭐⭐⭐⭐⭐ 专业 | ⭐⭐⭐⭐⭐ 专业 |
| **响应速度** | ⭐⭐⭐⭐⭐ 快 | ⭐⭐⭐⭐ 中等 |
| **成本** | $0.01-0.03/张 | $0.001-0.005/张 |
| **模型更新** | 频繁（GPT-5即将到来）| 稳定 |
| **推荐用途** | 最精准的诊断 | 经济实惠的分析 |

---

## 🔧 功能特性

### 图像增强（GPT-4独有）
系统会自动对上传的图像进行优化:
- ✅ 智能尺寸调整（最大1920px）
- ✅ 锐化处理（增强细节）
- ✅ 对比度优化（识别炎症）
- ✅ 色彩增强（区分肤色）

### 智能模型选择
系统会自动:
1. 尝试最新的 GPT-5（当可用时）
2. 回退到 GPT-4o（最强大）
3. 如果不可用，使用 GPT-4o-mini（经济）
4. 最后尝试 GPT-4-turbo / GPT-4-vision

### 详细诊断报告
GPT-4 提供:
- 🔬 头皮分区分析（前额、头顶、颞部、枕部）
- 📊 健康评分细分（头皮/毛发/炎症/卫生）
- 🩺 8种疾病智能识别（带ICD-10编码）
- 💡 专业治疗建议（分级推荐）
- 🔍 建议的进一步检查
- ⚠️ 就医紧急程度评估

---

## 🐛 故障排查

### 问题 1: "API密钥错误"

**检查**:
1. API密钥格式正确 (以 `sk-` 开头)
2. 访问 https://platform.openai.com/api-keys 验证密钥
3. 检查账户余额: https://platform.openai.com/usage

### 问题 2: "模型不可用"

**原因**: 免费账户可能无法访问 GPT-4

**解决**:
1. 升级到付费账户
2. 系统会自动回退到 GPT-4o-mini
3. 或者切换到 Claude (更经济)

### 问题 3: "配额用完"

**解决**:
1. 检查账户余额
2. 充值账户
3. 等待配额重置
4. 临时切换到 Claude

---

## 📝 配置示例

### Streamlit Cloud 部署

在 Streamlit Cloud App Settings → Secrets:
```toml
OPENAI_API_KEY = "sk-your-key-here"
```

### 本地 .env 文件

创建 `.env` 文件:
```env
OPENAI_API_KEY=sk-your-key-here
```

---

## 🎊 开始使用

1. **获取 API 密钥**: https://platform.openai.com/api-keys
2. **设置环境变量** 或在界面中输入
3. **运行应用**: `streamlit run app.py`
4. **上传图片** - AI分析已默认启用
5. **查看专业诊断报告**！

---

## 💡 提示

- **首次使用**: 建议使用 GPT-4o-mini（更便宜）
- **重要诊断**: 使用 GPT-4o（最准确）
- **批量分析**: 考虑使用 Claude（成本更低）
- **测试功能**: 使用本地分析（免费）

---

**系统状态**: ✅ GPT-4 已完全集成
**默认AI**: GPT-4 (OpenAI)
**自动环境变量**: 已启用
**更新日期**: 2025-11-09
