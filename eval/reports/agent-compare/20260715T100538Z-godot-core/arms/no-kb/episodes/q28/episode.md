# q28 · bug_fix · arm: `no-kb`

**题**：String formatting produces garbled output on a locale edge case. Which formatting routine is the culprit?  ·  **gold**：core/string/print_string.cpp, vformat
**答对**：✗  ·  **答案**：`String::sprintf`
**指标**：tokens=5659 · llm_calls=15 · tool_steps=14 · 耗时=62.12s · 截断=⚠是

---

**👤 用户**：String formatting produces garbled output on a locale edge case. Which formatting routine is the culprit?

> 💭 **思考**：The user is asking about a string formatting routine in Godot's core that produces garbled output on a locale edge case. Let me search for relevant code.

**🔧 `grep_code`**({"pattern": "locale"})

**🔧 `grep_code`**({"pattern": "format"})

> 💭 **思考**：The results are a bit broad. Let me look for more specific string formatting routines that deal with locale. The key file would likely be in the string directory. Let me search for more specific patterns like "sprintf" or "String::format" or number formatting.

**🔧 `grep_code`**({"pattern": "String::format"})

**🔧 `grep_code`**({"pattern": "num_scientific"})

> 💭 **思考**：Let me look at the ustring.cpp file, particularly the String::format and number formatting routines that might involve locale handling.

**🔧 `grep_code`**({"pattern": "num_real"})

**🔧 `grep_code`**({"pattern": "snprintf"})

> 💭 **思考**：Let me look at the ustring.cpp file to find the locale-related formatting routines. The key function is likely `String::num` or `String::num_real` which uses `snprintf` and might be affected by locale settings. Let me look at the actual code.

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/ustring.cpp"})

> 💭 **思考**：The file is large. Let me search for the specific locale-related formatting function. The key issue is usually about number formatting where `snprintf` produces locale-dependent decimal separators. Let me grep for the specific function.

**🔧 `grep_code`**({"pattern": "num_real"})

**🔧 `grep_code`**({"pattern": "setlocale"})

> 💭 **思考**：No `setlocale` in core. Let me look at the ustring.h to understand what `num` functions exist and find the formatting routines. The key locale edge case is typically about `String::num` using `snprintf` which respects locale for decimal separators. Let me read the relevant part of ustring.cpp or ust

**🔧 `read_file`**({"path": "/Users/ks_128/Documents/godot-src/core/string/ustring.h"})

> 💭 **思考**：The header file is truncated. Let me search more specifically for the number formatting function that deals with locale issues. The common culprit in Godot is `String::num()` or `String::num_scientific()`. The locale edge case is about decimal separator (`.` vs `,`) being affected by C locale when u

**🔧 `grep_code`**({"pattern": "num_int64"})

**🔧 `grep_code`**({"pattern": "decimal"})

> 💭 **思考**：Let me look at the specific `String::num` function implementation in ustring.cpp. The locale edge case is typically about `snprintf` producing a comma `,` instead of a period `.` as the decimal separator when the system locale uses commas. Let me search for the actual `String::num` implementation mo

**🔧 `grep_code`**({"pattern": "String String::num"})

**🔧 `grep_code`**({"pattern": "vformat"})

> 💭 **思考**：The user is asking about a String formatting routine that produces garbled output on a locale edge case. Based on the files shown, I need to identify the culprit. The grep results show that `ustring.cpp` matched for what appears to be formatting-related searches. The single match in `ustring.cpp` fo

**🤖 Agent**：`String::sprintf`

**👤 用户**：（用完工具次数，强制作答）

**🤖 Agent**：`String::sprintf`

**📋 工具结果**：
```
matched 19 files:
/Users/ks_128/Documents/godot-src/core/config/project_settings.cpp
/Users/ks_128/Documents/godot-src/core/io/translation_loader_po.cpp
/Users/ks_128/Documents/godot-src/core/io/resource_loader.cpp
/Users/ks_128/Documents/godot-src/core/core_constants.cpp
/Users/ks_128/Documents/godot-src/core/object/object.cpp
/Users/ks_128/Documents/godot-src/core/object/object.h
/Users/ks_128/Documents/godot-src/core/object/property_info.h
/Users/ks_128/Documents/godot-src/core/os/os.cpp
/Users/ks_128/Documents/godot-src/core/os/os.h
/Users/ks_128/Documents/godot-src/core/core_bind.cpp
/Use
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.h
/Users/ks_128/Documents/godot-src/core/crypto/crypto.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface_header_generator.cpp
/Users/ks_128/Do
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
matched 6 files:
/Users/ks_128/Documents/godot-src/core/doc_data.cpp
/Users/ks_128/Documents/godot-src/core/io/json.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_call.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_parser.cpp
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
matched 8 files:
/Users/ks_128/Documents/godot-src/core/math/vector4.cpp
/Users/ks_128/Documents/godot-src/core/math/vector3.cpp
/Users/ks_128/Documents/godot-src/core/math/vector2.cpp
/Users/ks_128/Documents/godot-src/core/math/quaternion.cpp
/Users/ks_128/Documents/godot-src/core/math/plane.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant.cpp
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
matched 3 files:
/Users/ks_128/Documents/godot-src/core/io/logger.cpp
/Users/ks_128/Documents/godot-src/core/core_bind.cpp
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
/**************************************************************************/
/*  ustring.cpp                                                           */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 8 files:
/Users/ks_128/Documents/godot-src/core/math/vector4.cpp
/Users/ks_128/Documents/godot-src/core/math/vector3.cpp
/Users/ks_128/Documents/godot-src/core/math/vector2.cpp
/Users/ks_128/Documents/godot-src/core/math/quaternion.cpp
/Users/ks_128/Documents/godot-src/core/math/plane.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant.cpp
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
(no matches)
```

**📋 工具结果**：
```
/**************************************************************************/
/*  ustring.h                                                             */
/**************************************************************************/
/*                         This file is part of:                          */
/*                             GODOT ENGINE                               */
/*                        https://godotengine.org                         */
/**************************************************************************/
/* Copyright (c) 2014-present Godot Engine contributors (see 
```

**📋 工具结果**：
```
matched 7 files:
/Users/ks_128/Documents/godot-src/core/io/ip_address.cpp
/Users/ks_128/Documents/godot-src/core/io/file_access_pack.cpp
/Users/ks_128/Documents/godot-src/core/debugger/remote_debugger_peer.cpp
/Users/ks_128/Documents/godot-src/core/debugger/remote_debugger.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_call.cpp
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
matched 10 files:
/Users/ks_128/Documents/godot-src/core/version.h
/Users/ks_128/Documents/godot-src/core/math/math_funcs.h
/Users/ks_128/Documents/godot-src/core/math/math_funcs.cpp
/Users/ks_128/Documents/godot-src/core/math/expression.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_call.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_utility.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_parser.cpp
/Users/ks_128/Documents/godot-src/core/variant/variant_utility.h
/Users/ks_128/Documents/godot-src/core/string/ustring.h
/Users/ks_128/Documents/godot-src/core/s
```

**📋 工具结果**：
```
matched 1 files:
/Users/ks_128/Documents/godot-src/core/string/ustring.cpp
```

**📋 工具结果**：
```
matched 20 files:
/Users/ks_128/Documents/godot-src/core/crypto/crypto_resource_format.cpp
/Users/ks_128/Documents/godot-src/core/crypto/crypto_core.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_interface_header_generator.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_library_loader.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension.cpp
/Users/ks_128/Documents/godot-src/core/extension/gdextension_manager.cpp
/Users/ks_128/Documents/godot-src/core/extension/extension_api
```

