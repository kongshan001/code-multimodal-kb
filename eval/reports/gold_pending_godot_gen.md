# gold_pending · target=godot_gen（人审后：保留 11 条 clean）
# 审核说明：拒了 Vector→数学向量(误导)、Node/Color 歧义同名、method/class 重复变体(留 class)。

## candidate
- query: 在 Godot 中，用来表示和操作 RGBA 色彩通道的数学数据类型是什么？
- gold: ["Color"]
- source: Color [function] math/color.h

## candidate
- query: 在 Variant 的 Variant::Type 枚举中，表示颜色类型的枚举成员是什么？
- gold: ["COLOR"]
- source: COLOR [enum_member] variant/variant.h

## candidate
- query: 在 Godot 的场景树中，所有可被实例化并参与组织的对象的最基础构建块是什么？
- gold: ["Node"]
- source: Node [class] io/resource.h

## candidate
- query: 在 Godot 中，用来表示场景树节点层级路径或属性路径的专用数据类型是什么？
- gold: ["NodePath"]
- source: NodePath [method] string/node_path.cpp

## candidate
- query: 在 Godot 中，所有可以被序列化保存到磁盘并在节点间共享复用的数据基类是哪个？
- gold: ["Resource"]
- source: Resource [class] io/resource.h

## candidate
- query: 在 Godot 引擎中，负责为资源生成、存储和查询全局唯一标识符（UID）的类是哪个？
- gold: ["ResourceUID"]
- source: ResourceUID [class] io/resource_uid.h

## candidate
- query: 在二进制资源格式的底层读写中，用于存储单个资源核心信息的结构体叫什么？
- gold: ["ResourceData"]
- source: ResourceData [struct] io/resource_format_binary.h

## candidate
- query: 在 Godot 中，哪个单例类负责统一管理所有键盘、鼠标及手柄的输入事件与动作状态查询？
- gold: ["Input"]
- source: Input [class] input/input.h

## candidate
- query: 在 Godot 中，哪个单例类负责管理所有动作与输入事件的映射关系？
- gold: ["InputMap"]
- source: InputMap [class] input/input_map.h

## candidate
- query: 在 Godot 引擎中，所有输入事件（如键盘按键、鼠标点击或手柄操作）的基类是哪个？
- gold: ["InputEvent"]
- source: InputEvent [class] input/input_event.h

## candidate
- query: 在 Godot 的底层音频处理中，用于表示单个音频采样数据（通常包含左右声道）的结构体是什么？
- gold: ["AudioFrame"]
- source: AudioFrame [method] math/audio_frame.h
