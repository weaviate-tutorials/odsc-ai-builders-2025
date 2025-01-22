# File: ./helpers.py

from enum import Enum
from typing import List, Literal, Optional
import subprocess
import json
from collections import Counter
import weaviate
from weaviate import WeaviateClient
from weaviate.collections import Collection
from weaviate.classes.query import Filter
import os


class CollectionName(str, Enum):
    """Enum for Weaviate collection names."""

    SUPPORTCHAT = "SupportChat"


def connect_to_weaviate() -> WeaviateClient:
    client = weaviate.connect_to_local(
        port=8080,  # For Kubernetes, use 80
        headers={
            "X-ANTHROPIC-API-KEY": os.environ["ANTHROPIC_API_KEY"],
            "X-OPENAI-API-KEY": os.environ["OPENAI_API_KEY"],
            "X-COHERE-API-KEY": os.environ["COHERE_API_KEY"],
        },
    )
    return client


def get_collection_names() -> List[str]:
    client = connect_to_weaviate()
    collections = client.collections.list_all(simple=True)
    return collections.keys()


def get_top_companies(collection: Collection, top_n: int, get_counts: bool = True, recalculate_stats = True, save_outputs = True) -> List[tuple[str, int]]:

    if os.path.exists("top_companies.json") and not recalculate_stats:
        with open("top_companies.json") as f:
            top_companies = json.load(f)
    else:
        response = collection.query.fetch_objects(limit=200)
        companies = [str(c.properties["company_author"]) for c in response.objects if c.properties["company_author"] != ""]
        top_companies = Counter(companies).most_common(15)

    if save_outputs:
        with open("top_companies.json", "w") as f:
            json.dump(top_companies, f)

    top_companies = top_companies[:top_n]

    actual_company_counts = dict()

    if get_counts:
        for company, _ in top_companies:
            count = collection.aggregate.over_all(
                filters=Filter.by_property("company_author").equal(company),
                total_count=True,
            )
            actual_company_counts[company] = count.total_count
    else:
        actual_company_counts = top_companies

    return actual_company_counts


def weaviate_query(
    collection: Collection,
    query: str,
    company_filter: str,
    limit: int,
    search_type: Literal["Hybrid", "Vector", "Keyword"],
    rag_query: Optional[str] = None,
):
    if company_filter and company_filter != "Any":
        company_filter_obj = Filter.by_property("company_author").equal(company_filter)
    else:
        company_filter_obj = None

    if search_type == "Hybrid":
        alpha = 0.5
    elif search_type == "Vector":
        alpha = 1
    elif search_type == "Keyword":
        alpha = 0

    if rag_query:
        search_response = collection.generate.hybrid(
            query=query,
            target_vector="text_with_metadata",
            filters=company_filter_obj,
            alpha=alpha,
            limit=limit,
            grouped_task=rag_query
        )
    else:
        search_response = collection.query.hybrid(
            query=query,
            target_vector="text_with_metadata",
            filters=company_filter_obj,
            alpha=alpha,
            limit=limit,
        )
    return search_response


def get_pprof_results() -> str:
    return subprocess.run(
        ["go", "tool", "pprof", "-top", "http://localhost:6060/debug/pprof/heap"],
        capture_output=True,
        text=True,
        timeout=10,
    )


STREAMLIT_STYLING = """
<style>
    .stHeader {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
"""
