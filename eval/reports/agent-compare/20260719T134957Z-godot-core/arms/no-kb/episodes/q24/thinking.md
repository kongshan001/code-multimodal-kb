# thinking

用户在问 Godot 4.7 core/ 中加密解密用的是哪个类。我需要在源码中搜索加密相关的类。

在 Godot 中，加密解密相关的类通常是：
- CryptoKey - 用于非对称加密
- X509Certificate - 证书
- Crypto - 通用加密类

让我搜索一下相关的类名。

---

找到了！在 core/crypto/crypto.h 和 core/crypto/crypto.cpp 中应该有 Crypto 类的定义。让我读一下头文件确认。

---

路径可能不对，让我用完整路径试试。

---

好的，我能读取文件了。虽然开头是版权注释，但从路径匹配来看，这个 Crypto 类是存在的。让我再看看文件内容，确认类名。

---

`Crypto`
