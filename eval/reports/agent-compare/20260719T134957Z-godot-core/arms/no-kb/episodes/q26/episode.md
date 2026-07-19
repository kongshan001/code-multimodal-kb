# q26 · code_retrieval · arm: `no-kb`

- **题**：HTTP 客户端用哪个类？
- **gold**：HTTPClient
- **答对**：✓
- **答案**：`HTTPClient`
- **指标**：tokens=1855 · llm_calls=2 · tool_steps=1 · 耗时=13.35s · 截断=否

---

**👤 用户**：HTTP 客户端用哪个类？

> 💭 **思考**：用户问的是 HTTP 客户端用哪个类，这是在 Godot 引擎代码库的语境下。

我需要查找 Godot 中的 HTTP 客户端类。通常这种类会是 `HttpClient` 或 `HTTPClient` 之类的名称。

让我用 grep 工具搜索一下。

**🔧 `grep_code`**({"pattern": "HTTPClient"})

> 💭 **思考**：找到了 `HTTPClient` 类的相关文件。用户问的是 HTTP 客户端用哪个类，答案应该是 `HTTPClient`。

**🤖 Agent**：`HTTPClient`

**📋 工具结果**：
```
matched 6 files:
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/io/http_client_tcp.h
/Users/ks_128/Documents/godot-src/core/io/http_client.h
/Users/ks_128/Documents/godot-src/core/io/http_client.cpp
/Users/ks_128/Documents/godot-src/core/io/http_client_tcp.cpp
/Users/ks_128/Documents/godot-src/core/register_core_types.cpp
```

