---
title: 从零搭建 RAG 系统
category: workflows
tags: [RAG, 教程, 实战, 向量数据库]
related:
  - ../concepts/rag-retrieval.md
  - ../concepts/embedding-vector-db.md
depends_on:
  - ../concepts/rag-retrieval.md
  - ../concepts/llm-basics.md
verification: false
created: 2026-05-07
updated: 2026-05-07
---

<!-- related_to: docs/concepts/rag-retrieval.md, docs/concepts/embedding-vector-db.md -->

# 从零搭建 RAG 系统

> 完整的手把手教程：从准备数据到部署一个可用的 RAG 问答系统。

---

## 完整流程

```
数据准备 → 文档切分 → Embedding → 向量存储 → 检索构建 → LLM 生成 → 部署
```

## 环境准备

```bash
pip install langchain langchain-openai langchain-community chromadb tiktoken openai
```

## 完整代码实现

> ⚠️ 以下代码使用 LangChain v0.3+ API。`RetrievalQA` 在 v0.3 中已进入维护模式，推荐新项目使用 LCEL（LangChain Expression Language）。

```python
import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 1. 加载文档
loader = TextLoader("knowledge_base.txt")
documents = loader.load()

# 2. 文档切分
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)

# 3. 创建 Embedding 并存入向量库
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 4. 创建检索 QA 链
llm = ChatOpenAI(model="gpt-4o", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 5. 提问
response = qa_chain.run("你的问题")
print(response)
```
