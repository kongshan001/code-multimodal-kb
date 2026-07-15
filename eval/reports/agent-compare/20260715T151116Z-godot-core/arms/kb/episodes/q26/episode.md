# q26 · code_retrieval · arm: `kb`

**题**：HTTP 客户端用哪个类？  ·  **gold**：HTTPClient
**答对**：✓  ·  **答案**：`HTTPClient`（定义在 `io/http_client.h`），底层 TCP 实现为 `HTTPClientTCP`。
**指标**：tokens=1048 · llm_calls=2 · tool_steps=1 · 耗时=15.39s · 截断=否

---

**👤 用户**：HTTP 客户端用哪个类？

> 💭 **思考**：The user is asking which class to use for an HTTP client in Godot.

**🔧 `cmm_search`**({"query": "HTTP client class"})

> 💭 **思考**：The search returned the relevant class. The main class is `HTTPClient`, with `HTTPClientTCP` as the underlying implementation.

**🤖 Agent**：`HTTPClient`（定义在 `io/http_client.h`），底层 TCP 实现为 `HTTPClientTCP`。

**📋 工具结果**：
```
- ~HTTPClient  (Users-ks_128-Documents-godot-src-core.io.http_client.HTTPClient.~HTTPClient)  io/http_client.h
- HTTPClientTCP  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP.HTTPClientTCP)  io/http_client_tcp.cpp
- set_http_proxy  (Users-ks_128-Documents-godot-src-core.io.http_client.HTTPClient.set_http_proxy)  io/http_client.cpp
- _get_http_data  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP._get_http_data)  io/http_client_tcp.cpp
- set_http_proxy  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP.set_http_proxy)  io/ht
```

