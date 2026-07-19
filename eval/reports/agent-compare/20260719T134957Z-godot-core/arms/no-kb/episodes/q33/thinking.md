# thinking

用户在问 Godot core 里的内存池类，用于按页批量分配固定大小对象，避免频繁 new/delete。这是一个关于内存管理的问题。

我需要在 Godot core/ 源码里搜索相关的内存池类。这种类通常会包含 "pool"、"allocator"、"page" 等关键词。

让我先搜索包含 "pool" 的类。

---

搜索到了一些包含 "Pool" 的文件。让我看看 `pooled_list.h` 这个文件，因为它很可能是用户要找的内存池类。

---

好的，我找到了 `pooled_list.h` 文件。这个文件应该包含一个内存池类。让我看看这个文件中的类定义。这个文件很长，我需要再读更多内容来找到类定义。

但也许还有其他更专门的内存池类。让我也搜索一下 "page" 相关的类。

---

文件内容太长，我需要搜索更具体的模式。让我搜索包含 "template" 和 "pool" 的类定义，或者直接搜索 "class Pool" 来找到确切的类名。

---

让我直接搜索 "PoolList" 来确认这个类名。

---

奇怪，没有搜索到 PoolList。让我再尝试一些其他的搜索模式来找到内存池相关的类。也许应该搜索 "allocator" 或者 "memory pool"。

---

让我搜索一下 "page allocator" 或者其他相关的内存池术语。也许我应该查看 templates 目录下的其他文件。

---

太好了！找到了 `paged_allocator.h` 文件，这很可能就是用户要找的内存池类。让我看看这个文件的内容。

---

我看到了 paged_allocator.h 文件的开头。让我搜索这个文件中的类定义来找到确切的类名。

---

好的，找到了 `PagedAllocator` 类在 paged_allocator.h 文件中。这应该就是用户要找的内存池类。让我再确认一下这个类的定义。

---

`PagedAllocator`
