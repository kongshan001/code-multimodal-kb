# thinking

用户问"消息队列用哪个类？"，这是在问Godot引擎里的消息队列相关的类。

我需要在Godot core/源码中搜索相关的类名。消息队列在Godot中通常涉及到消息处理、事件队列等机制。

让我先搜索一下相关的类名。常见的可能是MessageQueue、MessageHandler、或者类似的名称。

---

找到了！在core/object/message_queue.h文件中有MessageQueue类的定义。让我看一下这个文件来确认类名。

---

文件开头部分没有显示类定义，让我再看一下后面的内容。

---

看起来这个文件的读取功能只返回了前面的license部分。不过从grep的结果已经明确知道了，Godot中的消息队列类就是MessageQueue，定义在core/object/message_queue.h文件中。

根据问题的要求，我需要用符号名直接作答，不要太长的解释。

---

`MessageQueue`
