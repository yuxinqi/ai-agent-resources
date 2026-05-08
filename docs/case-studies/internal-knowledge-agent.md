---
id: case-internal-knowledge
title: 内部知识 Agent 案例
type: case-study
level: intermediate
status: draft
evidence_level: L3
practical_rating: A
last_reviewed: "2026-05-08"
valid_until: "2026-08-08"
related:
  - concept-rag
  - concept-memory
  - playbook-rag-agent
  - pattern-router
depends_on:
  - concept-rag
  - concept-agent
tags:
  - case-study
  - knowledge-base
  - internal-tool
  - rag
  - production
---

# 内部知识 Agent 案例

## 背景

某 2000 人科技公司，内部文档分散在 Confluence、飞书文档、GitLab Wiki 等多个平台。新员工入职后需要 2-3 周才能熟悉制度流程，每天有 200+ 内部咨询消息。目标：构建一个内部知识 Agent，让员工可以自然语言查询公司制度和流程。

## 系统架构

```
员工提问
    │
    ▼
Query 改写 + 意图识别
    │
    ├── 制度查询 → RAG Pipeline (制度文档库)
    ├── 技术文档 → RAG Pipeline (技术文档库)
    ├── 人员查询 → API 查询 (HR 系统)
    └── 闲聊 → 直接 LLM
    │
    ▼
结果聚合 + 来源标注
    │
    ▼
输出回答 + 相关文档链接
```

## 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| LLM | GPT-4o-mini | 性价比高，中文好 |
| Embedding | text-embedding-3-large | 中文检索质量好 |
| 向量数据库 | Milvus | 开源，支持大规模 |
| 文档同步 | 自建爬虫 | 多平台统一接入 |
| 框架 | LangChain + LangGraph | 成熟生态 |
| 部署 | 内网 Docker | 数据安全 |

## 实现细节

### 文档同步 Pipeline

```python
# 多平台文档同步
class DocSyncPipeline:
    """定期从各平台同步文档到知识库"""

    def sync_confluence(self):
        """同步 Confluence 页面"""
        pages = confluence_api.get_all_pages(space="HR")
        for page in pages:
            chunks = processor.chunk_text(page.body, source=f"confluence:{page.id}")
            vector_store.add_chunks(chunks)

    def sync_feishu(self):
        """同步飞书文档"""
        docs = feishu_api.list_docs(folder="公司制度")
        for doc in docs:
            content = feishu_api.get_doc_content(doc.id)
            chunks = processor.chunk_text(content, source=f"feishu:{doc.id}")
            vector_store.add_chunks(chunks)

    def sync_gitlab(self):
        """同步 GitLab Wiki"""
        wikis = gitlab_api.list_wikis()
        for wiki in wikis:
            chunks = processor.chunk_text(wiki.content, source=f"gitlab:{wiki.slug}")
            vector_store.add_chunks(chunks)

# 每天凌晨同步一次
# 增量同步：只处理更新的文档
```

### 权限控制

```python
class PermissionAwareRAG:
    """基于用户权限过滤检索结果"""

    def search(self, query: str, user_id: str, top_k: int = 5):
        user_permissions = self.get_user_permissions(user_id)

        # 检索更多结果，然后按权限过滤
        results = self.vector_store.search(query, top_k=top_k * 3)

        filtered = []
        for chunk, score in results:
            doc_permission = self.get_doc_permission(chunk.source)
            if self.has_access(user_permissions, doc_permission):
                filtered.append((chunk, score))
            if len(filtered) >= top_k:
                break

        return filtered
```

### 查询增强

```python
# Query 改写：解决口语化问题
# "年假怎么算" → "公司年假政策 入职年限 年假天数计算方式"

# 意图路由：不同意图走不同 Pipeline
INTENT_ROUTER = {
    "policy": "制度查询，走 RAG",
    "tech_doc": "技术文档查询，走 RAG",
    "people": "人员信息查询，走 HR API",
    "process": "流程查询，走 RAG + 流程图",
    "chat": "闲聊，直接 LLM"
}
```

## 结果

| 指标 | 上线前 | 上线后 | 变化 |
|------|--------|--------|------|
| 内部咨询响应时间 | 2 小时 | 10 秒 | -99% |
| 新员工熟悉时间 | 2-3 周 | 3-5 天 | -75% |
| 重复咨询量 | 200+/天 | 50/天 | -75% |
| 知识查找成功率 | 60% | 88% | +47% |
| 员工满意度 | 2.8/5 | 4.2/5 | +50% |

## 踩过的坑

### 坑 1：文档版本混乱

**问题**：同一制度有多个版本（旧版在 Confluence，新版在飞书），Agent 有时引用旧版。

**解法**：
- 文档元数据中加入版本号和生效日期
- 检索时优先返回最新版本
- 定期清理过期文档

### 坑 2：权限泄露

**问题**：普通员工搜到了仅管理层可见的薪酬制度。

**原因**：初始版本没有做权限过滤，所有文档对所有人可见。

**解法**：实现 PermissionAwareRAG，检索时按用户权限过滤。这是**安全刚需**，不可省略。

### 坑 3：回答不忠实

**问题**：Agent 回答了知识库中没有的信息，编造了不存在的制度。

**解法**：
- System Prompt 强制"只基于检索到的上下文回答"
- 低置信度时返回"未找到相关信息"而非编造
- 每个回答附带来源链接，方便用户验证

### 坑 4：文档同步延迟

**问题**：制度更新后，Agent 仍在回答旧版内容。

**解法**：改为增量同步 + 制度变更时触发即时更新。在回答中标注"此信息更新于 YYYY-MM-DD"。

## 经验教训

1. **数据质量决定上限**：文档规范、版本清晰、标签完善比算法优化更重要
2. **权限控制是刚需**：内部知识通常有权限分级，必须在检索层实现
3. **来源可溯是关键**：用户需要点击链接验证信息，否则不敢信任 Agent
4. **"不知道"比"编造"好**：宁可回答"未找到"也不要编造
5. **文档同步是持续工作**：知识库需要持续维护，否则快速退化

## 成本分析

| 项目 | 月成本 |
|------|--------|
| LLM API (GPT-4o-mini) | ¥2,800 |
| 向量数据库 (Milvus) | ¥1,200 |
| 文档同步服务 | ¥600 |
| 部署 (内网 2 台) | ¥1,600 |
| **总计** | **¥6,200** |
| 节省 HR 咨询时间 | ¥35,000/月 |
| **ROI** | **5.6x** |
