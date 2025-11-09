# GPT-4 集成使用指南
# GPT-4 Integration Guide

## ✅ 已完成的改进

### 1. **启用 OpenAI 依赖**
- ✓ 在 `requirements.txt` 中启用 `openai>=1.40.0`
- ✓ 库已成功安装并可用

### 2. **升级到最新 GPT-4o 模型**
- ✓ 从旧的 `gpt-4-vision-preview` 升级到 `gpt-4o`
- ✓ GPT-4o 是 OpenAI 最新的多模态模型，具有更强的视觉分析能力

### 3. **增强分析 Prompt**
- ✓ 使用与 Claude 相同的详细医学分析 prompt
- ✓ 包含 8 项必检项目、9 种疾病诊断、严格的健康评分标准
- ✓ 要求返回结构化的 JSON 格式结果

### 4. **添加用户界面选项**
- ✓ 在 app.py 中添加 AI 服务选择功能
- ✓ 支持在 GPT-4 和 Claude 之间切换
- ✓ 独立的 API 密钥配置

## 🚀 如何使用 GPT-4 分析

### 步骤 1: 获取 OpenAI API 密钥

1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 登录或注册账号
3. 点击 "Create new secret key"
4. 复制生成的 API 密钥（格式: `sk-...`）

### 步骤 2: 启动应用

```bash
streamlit run app.py
```

### 步骤 3: 配置 GPT-4

1. 上传头皮图像
2. 勾选 **"🚀 使用AI增强分析"**
3. 选择 **"GPT-4 (OpenAI)"**
4. 在 "OpenAI API密钥" 输入框中粘贴您的 API 密钥
5. 点击 **"🚀 Start AI Analysis"**

### 步骤 4: 查看分析结果

GPT-4o 将提供：
- 头皮类型识别（油性/干性/正常/混合/敏感）
- 健康评分（0-100分，严格评分）
- 疾病诊断（包括中英文名称、严重程度、置信度）
- 详细症状描述
- 专业护理建议
- 是否需要就医的建议

## 📊 GPT-4 vs Claude 对比

| 特性 | GPT-4o | Claude 3 Haiku |
|------|--------|----------------|
| **模型** | gpt-4o | claude-3-haiku-20240307 |
| **视觉能力** | ⭐⭐⭐⭐⭐ 极强 | ⭐⭐⭐⭐ 强 |
| **分析速度** | 5-10秒 | 3-8秒 |
| **医学专业性** | ⭐⭐⭐⭐ 强 | ⭐⭐⭐⭐⭐ 极强 |
| **成本** | 较高 | 较低 |
| **推荐场景** | 视觉分析、图像细节 | 医学诊断、文本分析 |

## 💡 使用建议

### 选择 GPT-4o 的场景：
- ✅ 需要强大的视觉分析能力
- ✅ 图像质量高，需要识别细微特征
- ✅ 需要英文分析报告
- ✅ 对响应速度要求不是特别严格

### 选择 Claude 的场景：
- ✅ 需要专业的医学术语和诊断
- ✅ 对成本敏感
- ✅ 需要快速响应
- ✅ 主要用于中文分析

### 最佳实践：
- 💡 两个模型都试试，对比分析结果
- 💡 重要诊断可以使用两个模型交叉验证
- 💡 定期检查 API 使用额度

## 🔧 技术细节

### 模型配置

**GPT-4o (utils/ai_services.py:402)**
```python
model="gpt-4o"
max_tokens=3000
temperature=0  # 确定性输出，适合医学诊断
detail="high"  # 高分辨率图像分析
```

**Prompt 结构**
- 专业医生角色设定
- 18 项详细分析要求
- 9 种常见头皮疾病检测
- 严格的健康评分标准
- 结构化 JSON 输出格式

### API 密钥管理

- ✓ 密钥存储在 `st.session_state` 中（会话级）
- ✓ 不会保存到文件或数据库
- ✓ 支持运行时切换不同的 API 密钥

## ⚠️ 注意事项

### API 成本
- GPT-4o 的视觉 API 调用成本较高
- 建议在 OpenAI 控制台设置使用限额
- 监控 API 使用情况：[OpenAI Usage](https://platform.openai.com/usage)

### API 限制
- GPT-4o 有速率限制（RPM/TPM）
- 如遇到 429 错误，请稍后重试
- 确保账户有足够的余额

### 隐私
- 图像会发送到 OpenAI 服务器进行分析
- OpenAI 承诺不会使用 API 数据训练模型
- 敏感图像请谨慎使用

## 🐛 故障排除

### 问题 1: "OpenAI API error: Authentication failed"
**解决方案：**
- 检查 API 密钥是否正确
- 确认密钥未过期
- 验证账户是否激活

### 问题 2: "Rate limit exceeded"
**解决方案：**
- 等待 1-2 分钟后重试
- 升级 OpenAI 账户层级
- 使用 Claude 作为备选

### 问题 3: "Insufficient quota"
**解决方案：**
- 充值 OpenAI 账户
- 检查账户余额
- 切换到 Claude 服务

### 问题 4: 分析结果不准确
**解决方案：**
- 确保图像清晰、光线充足
- 尝试重新拍摄头皮照片
- 使用 Claude 进行交叉验证

## 📝 更新日志

### 2024-11-08
- ✅ 集成 GPT-4o 模型
- ✅ 增强医学分析 prompt
- ✅ 添加 UI 选择界面
- ✅ 创建测试脚本
- ✅ 编写使用文档

## 🔗 相关链接

- [OpenAI API 文档](https://platform.openai.com/docs/guides/vision)
- [GPT-4o 模型介绍](https://openai.com/index/gpt-4o/)
- [API 定价](https://openai.com/api/pricing/)
- [Anthropic Claude](https://www.anthropic.com/claude)

## 💬 反馈与支持

如有问题或建议，请通过以下方式联系：
- Email: support@scalpanalyzer.my
- GitHub Issues: [项目地址]

---

**祝您使用愉快！Happy analyzing! 🎉**
