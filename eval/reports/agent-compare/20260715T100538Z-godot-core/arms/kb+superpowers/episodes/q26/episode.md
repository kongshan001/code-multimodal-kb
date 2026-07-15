# q26 · code_retrieval · arm: `kb+superpowers`

**题**：HTTP 客户端用哪个类？  ·  **gold**：HTTPClient
**答对**：✓  ·  **答案**：`HTTPClient`（低层，位于 `core/io/http_client.h`）。

如果要做高级 HTTP 请求（节点级别），通常用 `HTTPRequest` 节点；底层直接控制连接则用 `HTTPClient`（其 TCP 实现
**指标**：tokens=381 · llm_calls=2 · tool_steps=1 · 耗时=15.14s · 截断=否

---

**👤 用户**：HTTP 客户端用哪个类？

> 💭 **思考**：用户问 HTTP 客户端用哪个类。让我搜索一下。

**🔧 `cmm_search`**({"query": "HTTP client class"})

> 💭 **思考**：Got it. The answer is clear.

**🤖 Agent**：`HTTPClient`（低层，位于 `core/io/http_client.h`）。

如果要做高级 HTTP 请求（节点级别），通常用 `HTTPRequest` 节点；底层直接控制连接则用 `HTTPClient`（其 TCP 实现为 `HTTPClientTCP`）。

**📋 工具结果**：
```
- ~HTTPClient  (Users-ks_128-Documents-godot-src-core.io.http_client.HTTPClient.~HTTPClient)  io/http_client.h
- HTTPClientTCP  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP.HTTPClientTCP)  io/http_client_tcp.cpp
- set_http_proxy  (Users-ks_128-Documents-godot-src-core.io.http_client.HTTPClient.set_http_proxy)  io/http_client.cpp
- _get_http_data  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP._get_http_data)  io/http_client_tcp.cpp
- set_http_proxy  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP.set_http_proxy)  io/ht
```

