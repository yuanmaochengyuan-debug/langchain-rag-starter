import json
from pathlib import Path


OUTPUT_PATH = Path("evaluation/qa_dataset.json")


QA_DATASET = [
    {
        "id": 1,
        "question": "RAG 的主要作用是什么？",
        "gold_source": "01_rag_basics.txt",
    },
    {
        "id": 2,
        "question": "为什么更新 RAG 知识库通常不需要重新训练大语言模型？",
        "gold_source": "01_rag_basics.txt",
    },

    {
        "id": 3,
        "question": "Embedding 在 RAG 系统中主要负责什么？",
        "gold_source": "02_embeddings.txt",
    },
    {
        "id": 4,
        "question": "当前项目使用的本地文本向量模型是什么？",
        "gold_source": "02_embeddings.txt",
    },

    {
        "id": 5,
        "question": "本项目使用哪个数据库存储文本向量？",
        "gold_source": "03_chromadb.txt",
    },
    {
        "id": 6,
        "question": "ChromaDB 除了向量以外还可以保存哪些信息？",
        "gold_source": "03_chromadb.txt",
    },

    {
        "id": 7,
        "question": "Similarity Search 中的 Top-K 表示什么？",
        "gold_source": "04_similarity.txt",
    },
    {
        "id": 8,
        "question": "普通相似度检索可能存在哪种结果冗余问题？",
        "gold_source": "04_similarity.txt",
    },

    {
        "id": 9,
        "question": "MMR 检索相比普通相似度检索增加了什么考虑？",
        "gold_source": "05_mmr.txt",
    },
    {
        "id": 10,
        "question": "MMR 为什么通常需要先获取 fetch_k 个候选文本？",
        "gold_source": "05_mmr.txt",
    },

    {
        "id": 11,
        "question": "本项目使用什么工具切分长文档？",
        "gold_source": "06_chunking.txt",
    },
    {
        "id": 12,
        "question": "文本切分时保留 overlap 有什么作用？",
        "gold_source": "06_chunking.txt",
    },

    {
        "id": 13,
        "question": "本项目使用 Ollama 的主要目的是什么？",
        "gold_source": "07_ollama.txt",
    },
    {
        "id": 14,
        "question": "Ollama 默认的本地服务地址是什么？",
        "gold_source": "07_ollama.txt",
    },

    {
        "id": 15,
        "question": "系统的后端接口框架和前端框架分别是什么？",
        "gold_source": "08_fastapi_streamlit.txt",
    },
    {
        "id": 16,
        "question": "改进后的 sources 会返回哪些来源信息？",
        "gold_source": "08_fastapi_streamlit.txt",
    },

    {
        "id": 17,
        "question": "系统如何判断一个文件是否已经入库且没有发生变化？",
        "gold_source": "09_incremental_ingestion.txt",
    },
    {
        "id": 18,
        "question": "文件内容发生变化后增量入库会执行什么流程？",
        "gold_source": "09_incremental_ingestion.txt",
    },

    {
        "id": 19,
        "question": "Hit@K 主要评价检索系统的什么能力？",
        "gold_source": "10_evaluation.txt",
    },
    {
        "id": 20,
        "question": "MRR 和 Hit@K 的关注重点有什么区别？",
        "gold_source": "10_evaluation.txt",
    },

    {
        "id": 21,
        "question": "RAG 为什么能够降低大语言模型产生幻觉的风险？",
        "gold_source": "11_rag_hallucination.txt",
    },
    {
        "id": 22,
        "question": "如果检索阶段返回了错误文档，生成结果可能出现什么问题？",
        "gold_source": "11_rag_hallucination.txt",
    },

    {
        "id": 23,
        "question": "向量数据库中的 metadata 可以用于哪些功能？",
        "gold_source": "12_rag_metadata.txt",
    },
    {
        "id": 24,
        "question": "PDF 文档的页码信息通常存放在哪里？",
        "gold_source": "12_rag_metadata.txt",
    },

    {
        "id": 25,
        "question": "当前 nomic-embed-text 输出的向量维度是多少？",
        "gold_source": "13_embedding_dimension.txt",
    },
    {
        "id": 26,
        "question": "为什么更换 Embedding 模型后通常需要重新构建向量库？",
        "gold_source": "13_embedding_dimension.txt",
    },

    {
        "id": 27,
        "question": "语义检索相比关键词检索有什么优势？",
        "gold_source": "14_semantic_vs_keyword.txt",
    },
    {
        "id": 28,
        "question": "表达方式不同但意思相近的问题为什么仍可能被检索出来？",
        "gold_source": "14_semantic_vs_keyword.txt",
    },

    {
        "id": 29,
        "question": "ChromaDB 持久化存储有什么作用？",
        "gold_source": "15_chroma_persistence.txt",
    },
    {
        "id": 30,
        "question": "为什么 chroma_db 目录不适合提交到 GitHub？",
        "gold_source": "15_chroma_persistence.txt",
    },

    {
        "id": 31,
        "question": "向量数据库的 metadata filter 可以实现什么功能？",
        "gold_source": "16_vector_metadata_filter.txt",
    },
    {
        "id": 32,
        "question": "增量更新时系统如何定位需要删除的旧版本向量？",
        "gold_source": "16_vector_metadata_filter.txt",
    },

    {
        "id": 33,
        "question": "Top-K 设置得过小可能导致什么问题？",
        "gold_source": "17_topk_tradeoff.txt",
    },
    {
        "id": 34,
        "question": "为什么不存在对所有数据集都最优的固定 Top-K？",
        "gold_source": "17_topk_tradeoff.txt",
    },

    {
        "id": 35,
        "question": "Similarity Search 为什么可能返回多个内容高度重复的 chunk？",
        "gold_source": "18_similarity_redundancy.txt",
    },
    {
        "id": 36,
        "question": "MMR 能缓解普通相似度检索中的什么问题？",
        "gold_source": "18_similarity_redundancy.txt",
    },

    {
        "id": 37,
        "question": "MMR 中 fetch_k 和最终 k 的关系通常是什么？",
        "gold_source": "19_mmr_fetchk.txt",
    },
    {
        "id": 38,
        "question": "本项目的默认 mmr_fetch_k 设置为多少？",
        "gold_source": "19_mmr_fetchk.txt",
    },

    {
        "id": 39,
        "question": "MMR 中 lambda_mult 用来控制什么？",
        "gold_source": "20_mmr_lambda.txt",
    },
    {
        "id": 40,
        "question": "本项目默认的 lambda_mult 是多少？",
        "gold_source": "20_mmr_lambda.txt",
    },

    {
        "id": 41,
        "question": "本项目的 chunk_overlap 设置为多少？",
        "gold_source": "21_chunk_overlap.txt",
    },
    {
        "id": 42,
        "question": "chunk_overlap 设置过大会带来什么问题？",
        "gold_source": "21_chunk_overlap.txt",
    },

    {
        "id": 43,
        "question": "本项目默认的 chunk_size 是多少？",
        "gold_source": "22_chunk_size.txt",
    },
    {
        "id": 44,
        "question": "为什么比较检索算法时应该保持 chunk_size 不变？",
        "gold_source": "22_chunk_size.txt",
    },

    {
        "id": 45,
        "question": "使用本地 Ollama 对知识库数据隐私有什么好处？",
        "gold_source": "23_ollama_privacy.txt",
    },
    {
        "id": 46,
        "question": "当前项目中哪些模型通过 Ollama 在本地运行？",
        "gold_source": "23_ollama_privacy.txt",
    },

    {
        "id": 47,
        "question": "Qwen2.5 3B 在这个 RAG 系统中承担什么职责？",
        "gold_source": "24_qwen_role.txt",
    },
    {
        "id": 48,
        "question": "Hit@K 和 MRR 主要评测生成模型还是检索器？",
        "gold_source": "24_qwen_role.txt",
    },

    {
        "id": 49,
        "question": "系统的问答 API 路径是什么？",
        "gold_source": "25_fastapi_endpoint.txt",
    },
    {
        "id": 50,
        "question": "FastAPI 的 Swagger 页面在开发中可以用来做什么？",
        "gold_source": "25_fastapi_endpoint.txt",
    },
]


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            QA_DATASET,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Created: {OUTPUT_PATH}")
    print(f"Questions: {len(QA_DATASET)}")


if __name__ == "__main__":
    main()