"""代码侧首基线 gold 集（task 2.4 精神：gold 来自真实代码结构，零 LLM）。

target = 已 index 的 graphify 包（775 函数 / 4979 边）。每条 (query → gold 短名集合)。
gold 短名取自 cmm get_architecture 实测存在的真实符号（hotspots/clusters/file_tree）。
本集为**小-N 首基线**（非 RepoBench/SWE-Lancer 全量规模，后者留作 scale-up）。
"""
from __future__ import annotations

PROJECT = "Users-ks_128-.local-share-uv-tools-graphifyy-lib-python3.13-site-packages-graphify"

# (query, gold 短名集合)。混了精确名查询与概念查询，以区分 cmm 检索特征。
GOLD: list[tuple[str, set[str]]] = [
    ("id construction", {"_make_id"}),
    ("build graph from json", {"build_from_json"}),
    ("graph file size cap", {"check_graph_file_size_cap"}),
    ("security", {"check_graph_file_size_cap"}),  # 概念查询
    ("classify file", {"classify_file"}),
    ("xlsx to markdown", {"xlsx_to_markdown"}),
    ("google workspace", {"convert_google_workspace_file"}),
    ("call llm", {"_call_llm"}),
    ("backend api key", {"_get_backend_api_key"}),
    ("fetch arxiv", {"_fetch_arxiv"}),
    ("transcribe audio", {"transcribe"}),
    ("score nodes", {"_score_nodes"}),
    ("query graph text", {"_query_graph_text"}),
    ("rebuild code", {"_rebuild_code"}),
    ("suggest questions", {"suggest_questions"}),
    ("cross community surprises", {"_cross_community_surprises"}),
    ("derive sections from communities", {"derive_sections_from_communities"}),
    ("write callflow html", {"write_callflow_html"}),
    ("pick text", {"pick_text"}),
    ("load graph", {"load_graph"}),
    ("deduplicate entities", {"deduplicate_entities"}),
]
