# q26 · code_retrieval · arm: `kb+superpowers`

**题**：HTTP 客户端用哪个类？  ·  **gold**：HTTPClient
**答对**：✓  ·  **答案**：`HTTPClient`（定义在 `io/http_client.h`）。其 TCP 实现为 `HTTPClientTCP`。
**指标**：tokens=1274 · llm_calls=2 · tool_steps=1 · 耗时=10.86s · 截断=否

---

**👤 用户**：HTTP 客户端用哪个类？

**🔧 `cmm_search`**({"query": "HTTP client class"})

**📋 工具结果**：
```
- ~HTTPClient  (Users-ks_128-Documents-godot-src-core.io.http_client.HTTPClient.~HTTPClient)  io/http_client.h
- HTTPClientTCP  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP.HTTPClientTCP)  io/http_client_tcp.cpp
- set_http_proxy  (Users-ks_128-Documents-godot-src-core.io.http_client.HTTPClient.set_http_proxy)  io/http_client.cpp
- _get_http_data  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP._get_http_data)  io/http_client_tcp.cpp
- set_http_proxy  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP.set_http_proxy)  io/ht
```

**🤖 Agent**：`HTTPClient`（定义在 `io/http_client.h`）。其 TCP 实现为 `HTTPClientTCP`。

