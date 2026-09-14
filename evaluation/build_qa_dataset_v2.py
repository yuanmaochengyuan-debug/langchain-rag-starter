import json
from pathlib import Path


INPUT_PATH = Path("evaluation/qa_dataset.json")
OUTPUT_PATH = Path("evaluation/qa_dataset_v2.json")


# 经过整套语料统一审核后，补充“同样能够直接回答问题”的相关文档。
EXTRA_RELEVANT = {
    4: [
        "07_ollama.txt",
        "13_embedding_dimension.txt",
        "23_ollama_privacy.txt",
        "rag_test.txt",
    ],
    5: [
        "15_chroma_persistence.txt",
        "rag_test.txt",
    ],
    6: [
        "12_rag_metadata.txt",
    ],
    7: [
        "17_topk_tradeoff.txt",
    ],
    8: [
        "18_similarity_redundancy.txt",
        "21_chunk_overlap.txt",
    ],
    9: [
        "18_similarity_redundancy.txt",
    ],
    10: [
        "19_mmr_fetchk.txt",
    ],
    12: [
        "21_chunk_overlap.txt",
    ],
    13: [
        "23_ollama_privacy.txt",
    ],
    16: [
        "26_streamlit_ui.txt",
    ],
    17: [
        "27_sha256.txt",
        "28_manifest.txt",
    ],
    18: [
        "28_manifest.txt",
    ],
    19: [
        "29_hit_at_k.txt",
    ],
    23: [
        "03_chromadb.txt",
        "16_vector_metadata_filter.txt",
    ],
    24: [
        "08_fastapi_streamlit.txt",
    ],
    25: [
        "02_embeddings.txt",
    ],
    27: [
        "02_embeddings.txt",
    ],
    28: [
        "02_embeddings.txt",
    ],
    29: [
        "03_chromadb.txt",
    ],
    31: [
        "12_rag_metadata.txt",
    ],
    32: [
        "09_incremental_ingestion.txt",
    ],
    33: [
        "04_similarity.txt",
    ],
    35: [
        "04_similarity.txt",
        "21_chunk_overlap.txt",
    ],
    36: [
        "05_mmr.txt",
    ],
    37: [
        "05_mmr.txt",
    ],
    38: [
        "05_mmr.txt",
    ],
    39: [
        "05_mmr.txt",
    ],
    40: [
        "05_mmr.txt",
    ],
    41: [
        "06_chunking.txt",
    ],
    42: [
        "06_chunking.txt",
    ],
    43: [
        "06_chunking.txt",
    ],
    44: [
        "06_chunking.txt",
    ],
    45: [
        "07_ollama.txt",
    ],
    46: [
        "07_ollama.txt",
    ],
    47: [
        "07_ollama.txt",
    ],
    48: [
        "10_evaluation.txt",
    ],
    49: [
        "08_fastapi_streamlit.txt",
    ],
}


def main():
    with INPUT_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    for item in dataset:
        sources = [item["gold_source"]]
        sources.extend(EXTRA_RELEVANT.get(item["id"], []))

        # 去重但保持顺序
        item["gold_sources"] = list(dict.fromkeys(sources))

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            dataset,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Created: {OUTPUT_PATH}")
    print(f"Questions: {len(dataset)}")
    print("Q4:", dataset[3]["gold_sources"])
    print("Q8:", dataset[7]["gold_sources"])


if __name__ == "__main__":
    main()