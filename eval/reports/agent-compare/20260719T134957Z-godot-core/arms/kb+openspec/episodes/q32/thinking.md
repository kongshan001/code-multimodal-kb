# thinking

用户在问 Godot core 代码库中使用侵入式链表（链表指针内嵌进节点自身，不额外分配节点）的链表类叫什么。

我需要在 Godot core/ 中搜索相关的类。通常这种侵入式链表在 C++ 中会有特定的命名模式，比如 "IntrusiveList"、"LinkedList" 或者类似的名字。

让我搜索一下。

---

搜索结果显示有两个类：
1. `List` 在 templates/list.h
2. `SelfList` 在 templates/self_list.h

根据问题描述（链表指针内嵌进节点自身，侵入式，不额外分配节点），这应该是 `SelfList`。让我确认一下。

---

文件路径不对。让我尝试搜索 SelfList 的详细信息。

---

好的，从搜索结果来看，`SelfList` 确实有 `next` 和 `prev` 指针，这符合侵入式链表的特征。根据问题描述，这就是用户在找的类。

用户问的是"链表指针内嵌进节点自身（侵入式，不额外分配节点）的链表类叫什么"，答案应该是 `SelfList`。

---

`SelfList`
