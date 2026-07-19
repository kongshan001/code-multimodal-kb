# q37 · code_retrieval · arm: `no-kb`

- **题**：Godot core 里定长环形缓冲区（先进先出、写满覆盖最旧）的容器类叫什么？
- **gold**：RingBuffer
- **答对**：✓
- **答案**：`RingBuffer`
- **指标**：tokens=18336 · llm_calls=10 · tool_steps=9 · 耗时=18.83s · 截断=否

---

**👤 用户**：Godot core 里定长环形缓冲区（先进先出、写满覆盖最旧）的容器类叫什么？

> 💭 **思考**：用户在问 Godot core 源码中定长环形缓冲区（FIFO、写满时覆盖最旧元素）的容器类名称。我需要在 Godot core/ 源码里搜索相关实现。

环形缓冲区的可能关键词：
- "ring"
- "circular"
- "buffer"
- "fifo"
- "queue"
- "fixed size"
- "circular buffer"

让我先搜索 "ring" 相关：

**🔧 `grep_code`**({"pattern": "ring"})

> 💭 **思考**：没有明显结果。让我搜索 "circular"：

**🔧 `grep_code`**({"pattern": "circular"})

> 💭 **思考**："buffer" 可能是个好关键词：

**🔧 `grep_code`**({"pattern": "buffer"})

> 💭 **思考**：让我换个角度，查找 "fifo"：

**🔧 `grep_code`**({"pattern": "fifo"})

> 💭 **思考**：让我在核心模板库里搜索可能叫 "CircularBuffer" 或类似名称的类：

**🔧 `grep_code`**({"pattern": "CircularBuffer"})

> 💭 **思考**：让我搜索更通用的 "RingBuffer"：

**🔧 `grep_code`**({"pattern": "RingBuffer"})

> 💭 **思考**：找到了！有 `/Users/ks_128/Documents/godot-src/core/templates/ring_buffer.h` 这个文件。让我查看这个文件：

**🔧 `read_file`**({"path": "core/templates/ring_buffer.h"})

> 💭 **思考**：路径可能需要完整路径。让我尝试：

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/templates/ring_buffer.h"})

> 💭 **思考**：好的，找到 `ring_buffer.h` 文件了。文件名就是 `ring_buffer.h`，所以类名应该是 `RingBuffer`。让我看一下开头部分确认类名：

**🔧 `grep_code`**({"pattern": "class RingBuffer"})

> 💭 **思考**：确认了是 `RingBuffer` 类。让我直接用这个类名作答，不重复查询。

**🤖 Agent**：`RingBuffer`

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/hashing_context.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/hashing_context.h
/Users/ks_128/Documents/godot-src/core/crypto/aes_context.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto.cpp
/Users/ks_128/
```

**📋 工具结果**：
```
matched 6 files:
/Users/ks_128/Documents/godot-src/core/core_globals.h
/Users/ks_128/Documents/godot-src/core/input/input.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_format_binary.cpp
/Users/ks_128/Documents/godot-src/core/io/json.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_deep_duplicate.h
/Users/ks_128/Documents/godot-src/core/core_bind.cpp
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.h
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_special_compat_hashes.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension.h
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/input/inp
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
matched 8 files:
/Users/ks_128/Documents/godot-src/core/io/packet_peer_udp.cpp
/Users/ks_128/Documents/godot-src/core/io/packet_peer.h
/Users/ks_128/Documents/godot-src/core/io/stream_peer_gzip.h
/Users/ks_128/Documents/godot-src/core/io/packet_peer_udp.h
/Users/ks_128/Documents/godot-src/core/io/stream_peer_gzip.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_parser.cpp
/Users/ks_128/Documents/godot-src/core/templates/ring_buffer.h
/Users/ks_128/Documents/godot-src/core/string/string_buffer.h
```

**📋 工具结果**：
```
(read error: [Errno 2] No such file or directory: 'core/templates/ring_buffer.h')
```

**📋 工具结果**：
```
/**************************************************************************/
/*  ring_buffer.h                                                         */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/templates/ring_buffer.h
```

