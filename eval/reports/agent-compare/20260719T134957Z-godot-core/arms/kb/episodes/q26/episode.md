# q26 · code_retrieval · arm: `kb`

- **题**：HTTP 客户端用哪个类？
- **gold**：HTTPClient
- **答对**：✓
- **答案**：`HTTPClient`
- **指标**：tokens=1974 · llm_calls=2 · tool_steps=1 · 耗时=10.41s · 截断=否

---

**👤 用户**：HTTP 客户端用哪个类？

> 💭 **思考**：用户在问 HTTP 客户端用哪个类。这是一个关于 Godot 4.7 core/ 代码库的问题。我需要搜索相关的 HTTP 客户端类。

让我使用语义搜索工具来查找 HTTP 客户端相关的类。

**🔧 `cmm_search`**({"query": "HTTP client"})

> 💭 **思考**：搜索结果显示有几个 HTTP 客户端相关的类：

1. `HTTPClient` - 这是主要的 HTTP 客户端类
2. `HTTPClientTCP` - 这是 TCP 实现的 HTTP 客户端

从类名来看，`HTTPClient` 应该是用户要找的主要 HTTP 客户端类。根据收敛纪律，我已经找到了相关的符号，应该直接用符号名作答。

**🤖 Agent**：`HTTPClient`

**📋 工具结果**：
```
- ~HTTPClient  (Users-ks_128-Documents-godot-src-core.io.http_client.HTTPClient.~HTTPClient)  io/http_client.h
- HTTPClientTCP  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP.HTTPClientTCP)  io/http_client_tcp.cpp
- set_http_proxy  (Users-ks_128-Documents-godot-src-core.io.http_client.HTTPClient.set_http_proxy)  io/http_client.cpp
- _get_http_data  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP._get_http_data)  io/http_client_tcp.cpp
- set_http_proxy  (Users-ks_128-Documents-godot-src-core.io.http_client_tcp.HTTPClientTCP.set_http_proxy)  io/ht
```

