from pathlib import Path


OUTPUT_DIR = Path("data/sample_docs")

DOCUMENTS = {
    "01_rag_basics.txt": """
RAG 基础知识

检索增强生成（Retrieval-Augmented Generation，RAG）是一种把信息检索和大语言模型生成结合起来的技术。
典型 RAG 流程包括文档加载、文本切分、向量化、向量存储、查询向量化、相似度检索、上下文构造和答案生成。

RAG 的主要目的不是重新训练大语言模型，而是在推理阶段给模型补充外部知识。
因此，当知识库内容变化时，可以通过重新建立或更新向量索引来更新知识，而不必重新训练模型。

一个基本 RAG 系统通常先把长文档切分成多个 chunk。
每个 chunk 通过 Embedding 模型转换为向量，并存储在向量数据库中。
用户提问时，问题也会被转换为向量，然后根据向量距离检索最相关的文本块。

RAG 的一个核心优势是能够把生成结果与外部知识来源关联起来。
如果系统保留文档名称、页码和文本片段等 metadata，就可以实现答案来源追踪，提高系统的可解释性。
""",

    "02_embeddings.txt": """
Embedding 与语义检索

Embedding 是把文本映射到高维数值向量的过程。
语义相近的文本通常在向量空间中距离更近，因此可以利用向量距离完成语义搜索。

本项目使用 nomic-embed-text 作为本地 Embedding 模型。
该模型通过 Ollama 在本地运行，不需要调用云端 Embedding API。
在当前环境中，nomic-embed-text 生成的向量维度为 768。

向量检索常使用余弦相似度、欧氏距离或内积等方式衡量向量之间的接近程度。
与传统关键词匹配相比，Embedding 检索可以匹配表达方式不同但语义相似的问题和文档。

Embedding 模型与大语言模型承担不同职责。
Embedding 模型主要负责检索，大语言模型主要负责根据检索结果生成自然语言答案。
在 RAG 系统中，两者通常分别部署和调用。
""",

    "03_chromadb.txt": """
ChromaDB 向量数据库

ChromaDB 是面向 Embedding 数据的向量数据库，可用于存储文本向量及其 metadata。
在本项目中，ChromaDB 作为 RAG 系统的向量存储组件。

文档经过切分和向量化以后，每个 chunk 会写入 ChromaDB。
除了向量以外，还可以保存 source、source_file、page、file_sha256 等元数据。
这些 metadata 可以用于来源追踪、过滤检索以及文档版本管理。

本项目使用持久化目录 ./chroma_db 保存本地向量库。
这样程序重新启动以后，不需要每次都重新向量化全部文档。

ChromaDB 可以通过 similarity search 返回与问题最相似的若干文本块。
同时，LangChain 也可以把 Chroma 包装成 retriever，供 RetrievalQA 等 RAG 链调用。
""",

    "04_similarity.txt": """
Similarity 检索

Similarity 检索按照查询向量与文档向量之间的相似程度进行排序。
系统通常选择得分最高的前 K 个文本块作为检索结果，这个参数称为 Top-K。

Top-K 较小时，提供给语言模型的上下文更精简，但可能漏掉有用信息。
Top-K 较大时，召回范围增加，但也可能引入冗余或无关文本。

本项目把 Top-K 从原来固定的 4 改为可配置参数。
评测阶段重点比较 Top-K 等于 3、4、5 时的检索表现。

Similarity 方法的优点是逻辑简单、执行速度快，并且通常能够优先返回最接近问题语义的文本。
它的不足是多个高相似度结果之间可能内容高度重复，从而浪费上下文窗口。
""",

    "05_mmr.txt": """
MMR 多样化检索

最大边际相关性（Maximum Marginal Relevance，MMR）是一种兼顾相关性和结果多样性的检索策略。
MMR 不只是寻找与问题最相似的文本，还会降低多个检索结果之间的内容重复程度。

典型 MMR 流程先从向量库中取出 fetch_k 个候选文本，再从这些候选中选择最终的 k 个结果。
因此 fetch_k 一般大于最终的 Top-K。

lambda_mult 用于控制相关性和多样性之间的权衡。
lambda_mult 越偏向相关性，结果越接近普通相似度检索；越强调多样性，则更倾向于选择彼此不同的文本块。

本项目默认设置 mmr_fetch_k 为 12，mmr_lambda_mult 为 0.5。
最终实验比较 Similarity 和 MMR 在 Top-K 为 3、4、5 时的检索效果。
""",

    "06_chunking.txt": """
文本切分策略

长文档通常不能直接整体作为一个检索单元，因此 RAG 系统需要进行文本切分。
切分后的基本检索单元一般称为 chunk。

本项目使用 RecursiveCharacterTextSplitter 进行文本切分。
默认 chunk_size 为 500，chunk_overlap 为 50。
其中 chunk_size 控制单个文本块的目标长度，chunk_overlap 表示相邻文本块之间保留一定重叠内容。

适当的 overlap 可以降低重要信息恰好被切分边界截断的风险。
但 overlap 太大会生成大量重复内容，增加向量存储和检索冗余。

合理的 chunk 大小需要结合文档类型、Embedding 模型、检索任务和大语言模型上下文长度综合确定。
评测检索策略时，应保持切分参数一致，以确保不同检索方法之间的比较公平。
""",

    "07_ollama.txt": """
Ollama 本地模型部署

Ollama 是一个用于在本地运行大语言模型和 Embedding 模型的工具。
本项目使用 Ollama 替代原始项目中的 Gemini 云端模型，从而避免依赖外部 API Key。

当前回答模型为 Qwen2.5 3B，模型名称是 qwen2.5:3b。
Embedding 模型为 nomic-embed-text。
两个模型都运行在本地 Ollama 服务中。

Ollama 默认本地服务地址为 http://localhost:11434。
LangChain 可以通过 ChatOllama 调用生成模型，也可以通过 OllamaEmbeddings 调用 Embedding 模型。

本地部署的优点包括数据不必上传到外部服务、开发阶段不产生 API 调用费用，并且方便离线演示。
缺点是推理速度和可运行模型规模受本机 CPU、GPU 和内存资源限制。
""",

    "08_fastapi_streamlit.txt": """
FastAPI 与 Streamlit

本项目采用 FastAPI 提供后端问答接口，采用 Streamlit 提供轻量级 Web 前端。
前后端通过 HTTP 请求进行通信。

FastAPI 的查询接口为 POST /api/v1/query。
请求体包含 question 字段，后端调用 RAG 链完成检索和生成，再返回 answer 和 sources。

sources 不再只是文件路径字符串。
改进后的接口会返回文件名、页码和命中的原文 snippet，从而提高答案可追溯性。
对于 TXT 文件，页码可以为空；对于 PDF 文件，可以利用加载器产生的 page metadata 显示页码。

Streamlit 前端会把检索来源显示为可展开区域。
用户可以查看回答，也可以展开来源查看被检索到的原始文本片段。
""",

    "09_incremental_ingestion.txt": """
文件哈希与增量入库

如果每次启动系统都重新向量化全部文档，会造成大量重复计算，并可能让同一文档重复写入向量数据库。
因此本项目加入基于 SHA-256 文件哈希的重复检测和增量入库机制。

系统读取文件二进制内容并计算 SHA-256。
如果当前 Hash 与 manifest 中记录的 Hash 完全一致，则认为文件没有变化，并跳过重新向量化。

如果发现新的文件，系统执行 NEW 流程。
如果同名文件的 Hash 发生变化，则执行 UPDATE 流程，写入新版本向量并删除旧版本向量。

manifest 文件保存在 chroma_db/ingestion_manifest.json。
每个向量块还保存 source_file 和 file_sha256 metadata。

该机制可以避免相同文件被反复向量化，并支持知识库文档的增量更新。
""",

    "10_evaluation.txt": """
RAG 检索评测

本项目使用 Hit@K、MRR 和平均检索延迟评价检索模块。
评测的重点是检索结果是否能够找到正确来源，以及正确来源在结果列表中的排序位置。

Hit@K 表示前 K 个检索结果中是否至少出现一个正确来源。
对全部测试问题求平均后，可以得到整体 Hit@K。

MRR 是 Mean Reciprocal Rank，即平均倒数排名。
如果正确来源排在第 1 位，该问题的 reciprocal rank 为 1；
排在第 2 位时为 1/2；排在第 3 位时为 1/3。
如果前 K 个结果中没有正确来源，则该问题的 reciprocal rank 为 0。

平均检索延迟用于衡量执行一次检索所需要的时间。
为了公平比较 Similarity 和 MMR，实验使用相同的知识库、Embedding 模型和文本切分配置。

最终实验比较 6 组配置：
Similarity 的 Top-K 3、4、5，以及 MMR 的 Top-K 3、4、5。
每组配置使用同一套 50 个问题进行评测。
""",
}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for filename, content in DOCUMENTS.items():
        path = OUTPUT_DIR / filename
        path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"Created: {path}")

    print()
    print(f"Created {len(DOCUMENTS)} evaluation documents.")


if __name__ == "__main__":
    main()