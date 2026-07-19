# thinking

用户问"引擎主类叫什么？"，这是在问 Godot 引擎的核心类。我需要搜索 Godot 代码库来找到这个主类。

让我用 cmm_search 来搜索相关的符号。

---

这个搜索没有直接返回引擎主类。让我换个方式搜索，搜索 "Engine" 类：

---

好的，找到了 `Engine` 类。看起来是 `core/config/engine/engine.h` 中定义的 `Engine` 类。让我再读取一下文件确认：

---

文件路径不对。让我尝试读取正确的路径：

---

路径还是不对。让我直接从搜索结果看，有几个匹配：
- `core/config/engine.Engine.Engine`
- `core_bind.Engine.Engine`

看起来 `Engine` 就是 Godot 引擎的主类。我应该直接回答用户。

---

`Engine`
