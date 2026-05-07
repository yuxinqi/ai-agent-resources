---
title: Google Gemini API 使用指南
category: platforms
tags: [Google, Gemini, API, Vertex AI]
related:
  - platform-comparison.md
depends_on:
  - ../concepts/llm-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/platforms/platform-comparison.md -->

# Google Gemini API 使用指南

> Google Gemini 是 Google 推出的多模态大模型系列，以超长上下文（1M+ token）和深度 Google 生态集成为特色。

---

## 一、平台概览

| 项目 | 内容 |
|------|------|
| 官网 | https://ai.google.dev |
| API 入口 | Google AI Studio / Vertex AI |
| 代表模型 | Gemini 2.5 Pro, Gemini 2.5 Flash |
| 上下文窗口 | 最高 1M+ tokens |
| 多模态 | ✅ 文本、图像、音频、视频输入 |
| 免费额度 | 有（每分钟 60 次请求，有限制） |
| ⚠️ 状态 | ⏳ 待验真 |

## 二、注册与 API 密钥申请

### 2.1 Google AI Studio（个人开发者）

1. 访问 [Google AI Studio](https://aistudio.google.com)
2. 使用 Google 账号登录
3. 点击 **Get API Key** → 创建 API 密钥
4. 复制密钥并安全保存

### 2.2 Vertex AI（企业用户）

1. 访问 [Google Cloud Console](https://console.cloud.google.com)
2. 创建或选择一个项目
3. 启用 **Vertex AI API**
4. 配置服务账号和 IAM 权限
5. 使用服务账号密钥或 ADC（Application Default Credentials）认证

## 三、Python 快速入门

### Google AI Studio 方式

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-2.5-pro")
response = model.generate_content("介绍一下 Gemini 2.5 的核心特性")
print(response.text)
```

### Vertex AI 方式

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="your-project-id", location="us-central1")
model = GenerativeModel("gemini-2.5-pro")
response = model.generate_content("介绍一下 Gemini 2.5 的核心特性")
print(response.text)
```

## 四、核心能力

### 4.1 超长上下文

Gemini 2.5 Pro 支持高达 **1M+ tokens** 的上下文窗口，可处理：
- 整本技术书籍（如《AI 指数报告》全文）
- 超长对话历史
- 大规模代码仓库

### 4.2 多模态输入

支持同时输入文本、图像、音频、视频进行推理：

```python
import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.5-pro")
response = model.generate_content([
    "描述这张图片中的内容",
    genai.upload_file("photo.jpg")
])
print(response.text)
```

### 4.3 工具调用 / Function Calling

```python
model = genai.GenerativeModel("gemini-2.5-pro")
tools = [ ... ]  # 定义工具函数
model.tools = tools
response = model.generate_content("查询今天的天气")
```

### 4.4 搜索增强（Google Search Grounding）

Gemini 可以结合 Google 搜索获取实时信息：

```python
response = model.generate_content(
    "今天比特币价格是多少？",
    tools="google_search_retrieval"  # 启用搜索增强
)
```

## 五、定价参考

> ⚠️ 以下价格信息待验真。请以[官方定价页面](https://ai.google.dev/pricing)为准。

| 模型 | 输入（每百万 token） | 输出（每百万 token） |
|------|---------------------|---------------------|
| Gemini 2.5 Pro | ~$1.25 - $2.50 | ~$5.00 - $10.00 |
| Gemini 2.5 Flash | ~$0.15 - $0.50 | ~$0.60 - $2.00 |

**免费额度**：AI Studio 提供每分钟 60 次请求的免费额度，有每日上限。

## 六、注意事项

1. **区域限制**：部分功能在特定地区不可用，请查看[支持区域列表](https://ai.google.dev/gemini-api/docs/available-regions)
2. **内容政策**：遵循 Google [可接受使用政策](https://ai.google.dev/gemini-api/docs/safety-settings)
3. **数据隐私**：AI Studio 的免费层可能使用数据进行模型改进，Vertex AI 提供更严格的隐私控制
4. **限流**：免费层有 Rate Limit，生产环境建议使用 Vertex AI
5. **SDK 安装**：`pip install google-generativeai`（AI Studio）或 `pip install vertexai`（Vertex AI）

## 七、相关资源

- [API 平台综合对比](platform-comparison.md)
