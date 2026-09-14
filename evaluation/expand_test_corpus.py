from pathlib import Path


OUTPUT_DIR = Path("data/sample_docs")

DOCUMENTS = {
    "11_rag_hallucination.txt": """
RAG 与幻觉控制

大语言模型可能生成知识库中不存在的信息，这种现象通常称为幻觉。
RAG 通过向模型提供检索到的外部上下文，可以降低回答完全依赖模型内部参数知识的程度。

一个可靠的 RAG Prompt 通常要求模型优先依据检索上下文回答。
如果上下文中没有足够信息，系统应明确说明无法根据当前知识库回答，而不是自行编造答案。

降低幻觉不能只依赖 Prompt。
如果检索阶段返回了错误文档，即使生成模型严格遵守上下文，也可能得到错误答案。
因此检索质量是 RAG 系统可靠性的基础。
""",

    "12_rag_metadata.txt": """
RAG Metadata

向量数据库中的每个文本块除了正文和向量以外，还可以保存 metadata。
常见 metadata 包括文件名、页码、文档类型、文件哈希和时间戳。

本项目保存 source_file 和 file_sha256。
PDF 加载器还可以提供 page 信息。

metadata 不参与文本生成本身，但可以用于结果过滤、文档版本管理和来源追踪。
当系统需要展示答案依据时，可以把文件名、页码和命中文本片段返回给用户。
""",

    "13_embedding_dimension.txt": """
Embedding 向量维度

不同 Embedding 模型会生成不同维度的向量。
向量维度由模型结构决定，不能随意修改。

当前项目使用 nomic-embed-text。
在本地测试中，该模型返回 768 维文本向量。

同一个向量集合中的文档和查询必须使用相同的 Embedding 模型。
如果更换 Embedding 模型，通常需要重新向量化原有知识库，否则向量空间不一致，检索结果没有意义。
""",

    "14_semantic_vs_keyword.txt": """
语义检索与关键词检索

关键词检索依赖问题和文档中是否出现相同或相近的词语。
语义检索则利用 Embedding 表示文本含义。

例如用户搜索“如何避免文档重复导入”，文档可能写的是“使用文件哈希实现增量入库”。
两句话关键词并不完全一致，但语义检索仍可能找到正确内容。

语义检索适合自然语言问答，但也可能在专有名词、编号和精确字符串场景中不如关键词匹配稳定。
""",

    "15_chroma_persistence.txt": """
Chroma 持久化存储

本项目将 ChromaDB 数据保存在 ./chroma_db 目录。
持久化意味着程序退出以后，已经生成的向量不会因为进程结束而消失。

重新启动 FastAPI 后端时，系统可以直接重新连接已有向量库。
因此正常问答不需要每次启动都重新运行全部文档的 Embedding。

chroma_db 属于运行时数据，因此项目通过 .gitignore 避免将本地向量数据库提交到 GitHub。
""",

    "16_vector_metadata_filter.txt": """
向量数据库过滤

除了按照语义相似度搜索，向量数据库还可以结合 metadata 进行过滤。
例如可以限制只搜索某个文件、某类文档或某个版本。

本项目在增量更新中利用 file_sha256 metadata 标记每个 chunk 属于哪个文件版本。
当同一个文件发生变化时，可以根据旧 Hash 删除旧版本对应的向量块。

这种设计比根据文本内容逐条判断旧向量更加可靠。
""",

    "17_topk_tradeoff.txt": """
Top-K 的权衡

Top-K 决定一次检索最终返回多少个候选文本块。

较小的 K 可以减少上下文长度和噪声，同时降低大模型处理的文本量。
但 K 太小可能导致真正有用的证据没有被召回。

较大的 K 通常能够提高召回机会，但也会引入更多不相关文本和重复内容。
因此不存在对所有数据集都最优的固定 K。

本项目选择 K 等于 3、4、5 进行对比实验，并通过 Hit@K、MRR 和延迟共同判断配置。
""",

    "18_similarity_redundancy.txt": """
Similarity 检索的重复问题

普通 Similarity Search 会独立按照查询与每个文本块之间的相似度进行排序。
它并不会显式考虑多个结果之间是否互相重复。

如果一篇长文档被切成多个高度相似的相邻 chunk，这些 chunk 可能同时占据前几名。
这样虽然每个结果与问题都相关，但提供给语言模型的信息多样性不足。

MMR 的主要动机之一就是缓解这种重复结果问题。
""",

    "19_mmr_fetchk.txt": """
MMR 中的 fetch_k

MMR 通常不会直接从整个向量库逐条选择最终结果。
系统先按照相似度获得一批候选，这个候选数量通常由 fetch_k 控制。

之后 MMR 再从候选集合中选择最终的 Top-K 结果。
所以 fetch_k 应当不小于最终的 k。

本项目默认 fetch_k 为 12，而最终 Top-K 在 3、4、5 之间变化。
这样 MMR 有足够的候选文本用于进行相关性与多样性权衡。
""",

    "20_mmr_lambda.txt": """
MMR 中的 lambda_mult

MMR 使用 lambda_mult 控制查询相关性与结果多样性的权衡。

较大的相关性权重会让 MMR 更接近普通 Similarity Search。
较强调多样性时，算法会更主动避免选择彼此高度相似的文本。

本项目默认 lambda_mult 为 0.5。
该设置表示实验阶段同时关注结果与查询的相关程度以及多个结果之间的信息多样性。
""",

    "21_chunk_overlap.txt": """
Chunk Overlap

文本切分时，相邻 chunk 可以保留部分重复内容，这个参数称为 chunk_overlap。

本项目的 chunk_overlap 为 50。
其目的在于避免一个完整语义刚好跨越两个文本块边界时，被完全拆开。

Overlap 太小可能造成上下文割裂。
Overlap 太大则会增加重复向量数量，并可能加剧 Similarity 检索返回相邻重复文本的问题。
""",

    "22_chunk_size.txt": """
Chunk Size

本项目默认 chunk_size 为 500。
它决定文本切分时单个 chunk 的目标长度。

Chunk 太大会让一个向量同时包含过多主题，影响检索定位精度。
Chunk 太小则会失去上下文信息，并增加向量数量。

进行检索策略对比时，应固定 chunk_size 和 chunk_overlap。
否则无法判断性能变化究竟来自检索算法还是文本切分参数。
""",

    "23_ollama_privacy.txt": """
本地模型与数据隐私

本地 Ollama 部署的一个优势是知识库内容可以在本机完成 Embedding 和大模型推理。
开发者无需为了每次问答把文档内容发送到外部模型 API。

当前项目的 Qwen2.5 3B 与 nomic-embed-text 都通过本地 Ollama 服务运行。

本地运行并不自动意味着整个系统满足所有安全要求，但它能够减少开发阶段对第三方模型服务的依赖。
""",

    "24_qwen_role.txt": """
Qwen 在 RAG 中的职责

本项目使用 qwen2.5:3b 作为生成模型。

Qwen 不负责从 ChromaDB 中搜索文档。
检索器首先取得相关文本块，然后 LangChain 把检索上下文与用户问题一起传递给 Qwen。

因此 RAG 可以把检索模块与生成模块分开评测。
Hit@K 和 MRR 主要衡量 Retriever，而最终回答质量还会受到大语言模型能力和 Prompt 的影响。
""",

    "25_fastapi_endpoint.txt": """
FastAPI Query Endpoint

系统的问答 API 路径为 POST /api/v1/query。
客户端在 JSON 请求体中提交 question。

后端建立 RAG Chain，执行检索和答案生成。
返回结构包含 answer 和 sources。

FastAPI 还会自动生成 Swagger API 文档。
开发阶段可以访问 /docs 页面，通过 Try it out 功能直接测试接口。
""",

    "26_streamlit_ui.txt": """
Streamlit 前端

Streamlit 用于快速构建本项目的 Web 问答界面。

用户在输入框中输入问题，前端使用 HTTP POST 请求调用 FastAPI。
收到响应后，页面展示 answer。

改进后的前端还会显示 Sources。
每个来源可以作为展开区域，其中展示文件名、页码和 snippet，使用户能够查看回答依据。
""",

    "27_sha256.txt": """
SHA-256 文件指纹

SHA-256 可以把文件内容映射为固定长度的哈希值。
即使文件只发生很小的修改，生成的 Hash 通常也会改变。

本项目读取文件二进制数据计算 SHA-256。
Hash 用于判断一个文件是否与上一次入库时完全相同。

如果 Hash 没有变化，系统执行 SKIP。
这样可以避免同一文件被重复 Embedding 和重复写入 ChromaDB。
""",

    "28_manifest.txt": """
增量入库 Manifest

系统把已经处理过的文件及其 SHA-256 保存到 ingestion_manifest.json。

该文件位于 chroma_db 目录下。
运行 ingest.py 时，程序先加载 manifest，再计算当前文件的 Hash。

如果文件名和 Hash 与记录一致，则文件未变化。
如果同名文件的 Hash 不同，则进入 UPDATE 流程。
如果 manifest 中没有该文件，则进入 NEW 流程。
""",

    "29_hit_at_k.txt": """
Hit@K 指标

Hit@K 用于判断检索器是否在前 K 个结果中找到了至少一个正确答案来源。

例如一个问题的正确来源是 05_mmr.txt。
如果 Top-3 检索结果中包含该文件，则该问题的 Hit@3 等于 1。
如果没有出现，则等于 0。

对所有问题的 Hit 值求平均，就得到数据集整体 Hit@K。
该指标关注是否召回正确来源，但不关心它具体排在第几名。
""",

    "30_mrr.txt": """
MRR 指标

MRR 的全称是 Mean Reciprocal Rank，即平均倒数排名。

对于一个问题，首先寻找第一个正确来源在检索结果中的位置。
如果排第 1，reciprocal rank 为 1。
排第 2 为 0.5。
排第 4 为 0.25。

如果 Top-K 内没有正确来源，则记为 0。

MRR 比 Hit@K 更关注正确结果是否排在靠前位置，因此适合评价检索排序质量。
""",
}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for filename, content in DOCUMENTS.items():
        path = OUTPUT_DIR / filename
        path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"Created: {path}")

    print()
    print(f"Created {len(DOCUMENTS)} additional documents.")


if __name__ == "__main__":
    main()