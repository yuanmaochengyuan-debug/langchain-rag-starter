import csv
import json
import time
from pathlib import Path

from app.core.config import settings
from app.services.rag_chain import build_retriever


DATASET_PATH = Path("evaluation/qa_dataset_v2.json")
RESULTS_PATH = Path("evaluation/results_v2.csv")
DETAILS_PATH = Path("evaluation/query_details_v2.csv")

CONFIGS = [
    ("similarity", 3),
    ("similarity", 4),
    ("similarity", 5),
    ("mmr", 3),
    ("mmr", 4),
    ("mmr", 5),
]


def get_source_name(document) -> str:
    """Get source filename from document metadata."""
    source_file = document.metadata.get("source_file")

    if source_file:
        return Path(source_file).name

    source = document.metadata.get("source", "unknown")
    return Path(source).name


def get_gold_sources(item) -> list[str]:
    """Support both old single-source and new multi-source labels."""
    gold_sources = item.get("gold_sources")

    if gold_sources:
        return gold_sources

    return [item["gold_source"]]


def get_first_relevant_rank(
    retrieved_sources: list[str],
    gold_sources: list[str],
):
    """Return rank of first relevant document, or None."""
    gold_set = set(gold_sources)

    for rank, source in enumerate(retrieved_sources, start=1):
        if source in gold_set:
            return rank

    return None


def evaluate_config(dataset, retrieval_type, top_k):
    settings.retrieval_type = retrieval_type
    settings.top_k = top_k

    retriever = build_retriever()

    hits = []
    reciprocal_ranks = []
    latencies_ms = []
    details = []

    print()
    print("=" * 60)
    print(f"Running: {retrieval_type.upper()} | Top-K={top_k}")
    print("=" * 60)

    for index, item in enumerate(dataset, start=1):
        question = item["question"]
        gold_sources = get_gold_sources(item)

        start_time = time.perf_counter()

        documents = retriever.invoke(question)

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        retrieved_sources = [
            get_source_name(document)
            for document in documents
        ]

        rank = get_first_relevant_rank(
            retrieved_sources,
            gold_sources,
        )

        hit = int(rank is not None)

        if rank is None:
            rr = 0.0
            matched_source = ""
        else:
            rr = 1.0 / rank
            matched_source = retrieved_sources[rank - 1]

        hits.append(hit)
        reciprocal_ranks.append(rr)
        latencies_ms.append(latency_ms)

        details.append(
            {
                "id": item["id"],
                "retrieval_type": retrieval_type,
                "top_k": top_k,
                "question": question,
                "gold_sources": " | ".join(gold_sources),
                "retrieved_sources": " | ".join(
                    retrieved_sources
                ),
                "matched_source": matched_source,
                "first_relevant_rank": (
                    rank if rank is not None else ""
                ),
                "hit": hit,
                "reciprocal_rank": round(rr, 4),
                "latency_ms": round(latency_ms, 2),
            }
        )

        status = "HIT" if hit else "MISS"

        print(
            f"[{index:02d}/50] "
            f"{status} "
            f"RR={rr:.3f} "
            f"{latency_ms:.1f} ms"
        )

    hit_at_k = sum(hits) / len(hits)

    mrr = (
        sum(reciprocal_ranks)
        / len(reciprocal_ranks)
    )

    avg_latency_ms = (
        sum(latencies_ms)
        / len(latencies_ms)
    )

    sorted_latencies = sorted(latencies_ms)

    p95_index = max(
        0,
        int(len(sorted_latencies) * 0.95) - 1,
    )

    p95_latency_ms = sorted_latencies[p95_index]

    summary = {
        "retrieval_type": retrieval_type,
        "top_k": top_k,
        "questions": len(dataset),
        "hit_at_k": round(hit_at_k, 4),
        "mrr": round(mrr, 4),
        "avg_latency_ms": round(avg_latency_ms, 2),
        "p95_latency_ms": round(p95_latency_ms, 2),
    }

    print()
    print(
        f"Hit@{top_k}: {hit_at_k:.4f} | "
        f"MRR: {mrr:.4f} | "
        f"Avg latency: {avg_latency_ms:.2f} ms"
    )

    return summary, details


def save_summary(results):
    with RESULTS_PATH.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "retrieval_type",
                "top_k",
                "questions",
                "hit_at_k",
                "mrr",
                "avg_latency_ms",
                "p95_latency_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(results)


def save_details(details):
    with DETAILS_PATH.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "retrieval_type",
                "top_k",
                "question",
                "gold_sources",
                "retrieved_sources",
                "matched_source",
                "first_relevant_rank",
                "hit",
                "reciprocal_rank",
                "latency_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(details)


def main():
    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    print(f"Loaded {len(dataset)} QA pairs.")

    all_results = []
    all_details = []

    for retrieval_type, top_k in CONFIGS:
        summary, details = evaluate_config(
            dataset,
            retrieval_type,
            top_k,
        )

        all_results.append(summary)
        all_details.extend(details)

    save_summary(all_results)
    save_details(all_details)

    print()
    print("=" * 60)
    print("FINAL RESULTS V2")
    print("=" * 60)

    for result in all_results:
        print(
            f"{result['retrieval_type']:10s} "
            f"K={result['top_k']} | "
            f"Hit@K={result['hit_at_k']:.4f} | "
            f"MRR={result['mrr']:.4f} | "
            f"Avg={result['avg_latency_ms']:.2f} ms"
        )

    print()
    print(f"Summary saved to: {RESULTS_PATH}")
    print(f"Details saved to: {DETAILS_PATH}")


if __name__ == "__main__":
    main()