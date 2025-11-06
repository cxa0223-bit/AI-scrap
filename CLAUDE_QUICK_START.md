# 🚀 Claude AI 快速使用指南

## ✅ 安装状态
- **Anthropic库**: ✅ 已安装成功
- **API密钥**: ✅ 已配置完成
- **连接测试**: ✅ 通过

## 📝 使用步骤

### 方法1：通过UI配置（推荐）

1. **打开应用**: http://localhost:8501

2. **进入AI设置页面**:
   - 点击左侧边栏的 "🤖 AI Settings"

3. **配置Claude**:
   - ✅ 勾选 "Enable AI-Enhanced Analysis"
   - 选择 "Claude (Anthropic)"
   - 在API密钥栏粘贴您的Claude API密钥
   - （密钥格式：sk-ant-api03-...）
   - ✅ 勾选 "Combine with Local Analysis"（获得最佳准确度）
   - 选择语言：Chinese (中文)

4. **保存设置**:
   - 点击 "💾 Save Settings"

5. **开始使用**:
   - 返回主页
   - 上传头皮照片
   - 点击 "🚀 Start AI Analysis"
   - Claude会提供专业的医学分析！

### 方法2：自动加载（已配置）

运行 `set_claude_key.bat` 文件，然后启动应用：
```bash
set_claude_key.bat
python -m streamlit run app.py
```

## 🎯 Claude分析特点

| 功能 | 说明 |
|------|------|
| **医学知识** | 专业的皮肤科知识库 |
| **疾病识别** | 准确识别各种头皮疾病 |
| **中文支持** | 完美支持中文诊断报告 |
| **详细建议** | 提供治疗和护理建议 |

## 💰 费用说明

- **价格**: 约 $0.01-0.03 每次分析
- **模型**: Claude 3 Opus（最准确）
- **建议**: 先用免费的本地分析筛选，有问题再用Claude深度分析

## 🔍 分析结果示例

使用Claude后，您将获得：

1. **专业诊断**：
   - 具体疾病名称（中英文）
   - 严重程度评估
   - 置信度百分比

2. **症状描述**：
   - 详细的症状列表
   - 医学术语解释

3. **治疗建议**：
   - 药物推荐
   - 生活方式调整
   - 是否需要就医

## ⚠️ 注意事项

1. **隐私保护**: 图片会发送到Claude服务器分析，注意隐私
2. **网络要求**: 需要稳定的网络连接
3. **API限制**: 注意API调用频率限制
4. **医疗声明**: AI分析仅供参考，严重问题请就医

## 🛠️ 故障排除

如果遇到问题：

1. **"API key not valid"**:
   - 检查密钥是否正确复制
   - 确认没有多余空格

2. **"Connection error"**:
   - 检查网络连接
   - 尝试重新保存设置

3. **分析失败**:
   - 确保图片清晰
   - 尝试使用本地分析模式

## 📞 联系支持

- GitHub Issues: https://github.com/cxa0223-bit/AI-scrap/issues
- 应用内反馈：AI Settings页面

---

**现在就开始使用Claude进行专业的头皮健康分析吧！** 🎉