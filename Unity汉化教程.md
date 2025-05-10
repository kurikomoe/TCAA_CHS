[WIP： 正在写](https://github.com/nesrak1/UABEA)

---------------------



# 目录

- [Text 文本篇](docs/Tutorials/TMPro.md)
- [TMPro 字库篇]()
- [Video 视频篇]()
- [Images 图片篇]()



# Unity  基本知识速记

以本游戏为例，这里记录了一些 Unity 中常见的知识点（所有用到的工具会在附录表格中记录，并提供地址）

**版本** Unity 的跨版本兼容性是一坨，基本上游戏都要锁定某个版本的 Unity 进行开发。一般来说可以直接查看游戏可执行文件或者 dll 中的版本号拿到 Unity 版本。本游戏是 2022.3.46 版本，可以看到 Unity 官网上该版本是 24/09/XX 发布（还挺新的）

**后端** Unity 游戏分为 Mono 和 il2cpp 两种。其中 il2cpp 就是直接将  C# 代码翻译成 C++ 后变成 C++ 程序。同时在 `global-metadata.dat` 中存储了各种类的字段等信息用于反射等操作（大概），这个游戏就是使用 il2cpp 的。
关于 `global-metadata.dat` 可以参见：[IL2CPP Reverse Engineering Part 2: Structural Overview & Finding the Metadata](https://il2cppdumper.com/reverse/structural-overview-and-finding-the-metadata)

**unityplayer.dll** Unity 引擎的主要代码，C++ 写的，有时候可能通过 Unity 官方服务器拿到符号表。相应的工具有：TODO，但是本游戏似乎拿不到。反正执行各种 downloader 都会报 404 not found，不知道是梯子问题还是真的没有。

**Hook** Unity 游戏根据 Mono 或者 il2cpp 有两种 Hook 方式。同时也有两大主流 Hook 框架：Bepinex，MelonLoader。TODO

**XUnity.AutoTranslator (下称 XAT)** 好东西，但是本游戏用不了。简单看了一下 XAT 的代码，其提供的替换 TextMeshPro 字库图的方法是：

1. 调用 Unity.AssetBundle.dll 的 LoadFromFile 之类的函数从文件系统中加载一个 UnityFS 文件
2. 之后 Unity 自动解包这个文件，再调用 Unity.TMPro.dll 的相关操作去创建一个 FontAsset
3. 之后将这个 Font 强制丢给给游戏内部的 TMPro 类，实现 Font 替换。

对于本游戏，问题是由于单个 data.unity3d 打包了所有的资源文件，因此 il2cpp 裁剪掉了没用的 Unity.AssetBundle.dll，导致我们没有函数可以加载封包。同时我们也不太可能直接调用一个 C# 版的 dll 手动加载（感觉利用 coreclr 相关函数手动创建 clr，再加载 dll 也可以试试？）。

**资源文件替换** 资源文件的替换有点麻烦，目前已知的对于封包内文件，只有 UABEA 提供了资源文件替换功能。
利用 Hook 等方式重定向加载资源文件的方法可以参见 XAT 中 ResourceRedirector 相关的做法（不过前提感觉都是游戏没有阉割了 AssetBundle.dll）

**字库** Unity 游戏已经开始逐渐转向使用 TextMeshPro 插件(?) 制作字库了，与 Unreal 不同，TextMeshPro 真的就是字库图（aka 根据提供的字符 + TTF 字体文件来生成对应的高精度图片，之后显示文字是把图片贴上去）。因此大部分时候 Unity 游戏很容易出现缺字的问题，需要重建字库。

**il2cpp**: il2cpp 这个比较复杂，可能需要单独讲解，这里列一些我看过的资料：

- [[原创] 什么？IL2CPP APP 分析这一篇就够啦！](http://blog.androidcrack.com/index.php/archives/55/)[备份](https://archive.is/ESyiH)，这个是栗子事后（写文章的今天）才找到的资料。
- [IL2CPP 代码裁剪与生成全流程剖析](https://www.lfzxb.top/il2cpp-all-in-one/)，[备份](https://archive.ph/uwxvl)
- [IL2CppDumper 笔记](https://qiankanglai.me/2022/04/23/il2cppdumper-notes/index.html)， [备份](https://archive.md/7Pbof)

**UABEA**： 由`nesrak1`开发的 Unity Assert 解包打包工具（据我所知可能是唯一一个能处理打包操作的）目前有两个版本，一个是旧版：[UABEA](https://github.com/nesrak1/UABEA)，一个是还在开发中的 next 版：[UABEANext](https://github.com/nesrak1/UABEANext/tree/master)。两者最大的不同是，目前只有 `UABEA` 支持从 `data.unity3d` 中导入/删除原始封包（比如 sharedassets0.reS 之类的，`UABEANext` 目前没看到有这个功能），至于为什么需要删除封包，我们在汉化流程中细谈。



# 汉化流程记录

>  这里的汉化流程记录按照的是门类来说明，而非汉化工作的进行流程。

## 解包：

正经来说，汉化 Unity 游戏可以依靠 hook 的形式动态汉化，也可以依靠修改封包的形式实现汉化。由于这个游戏裁剪了重要的 assetbundle 相关的 api，因此反正都需要重新打包字库相关的文件，不如直接用重封包的形式汉化算了。

### 代码

> 解包样本见[传送门](https://github.com/kurikomoe/TCAA_CHS/blob/main/third/il2cppdumper-TCAA.7z)，注意，不含游戏的的 dll，对应文件请自行购买游戏获得。

游戏采用 `il2cpp` 编译，需要使用 `il2cppdumper` 进行解密，由于游戏使用的是 Version 31 API，因此需要使用 pre-release 的最新版 [il2cppdumper](https://github.com/Perfare/Il2CppDumper/releases/tag/v6.7.46) 进行解密操作，或者自行根据 main 分支的代码进行编译，这里放一个编译好的 [binary](https://github.com/kurikomoe/TCAA_CHS/blob/main/third/il2cppdumper-TCAA.7z)（commit id 4741d46ba9cd6159c5d853eb9d6fc48b4bfa2b1a)，里面有游戏版本的 dump 数据。

解密中需要的两个密钥 `CodegenRegistration` 和 `metadataRegistration`，对应的两个解密参数地址分别为：10c39dd8 和 10cdccb8 （仅对当前游戏版本有效）。

这里有多种方法可以拿到密钥：

第一个是 Unknown 上面这个方法：[传送门](https://www.unknowncheats.me/forum/general-programming-and-reversing/355005-il2cppdumper-tutorial-finding-coderegistration-metadataregistration.html)。当然这个方法也太 TM 麻烦了，虽然很好用，但是依靠  IDA 生成 sig 的做法还是有点太复杂了。我们换一个。

第二个方法来自于：[传送门](https://tomorrowisnew.com/posts/Finding-CodeRegistration-and-MetadataRegistration/) （[备份](https://archive.is/TcQQ9)）。本质上还是因为解密函数的调用逻辑不变，因此可以依靠 `global-metadata.dat` 文件读取为基准，手工向上找到对应的关键函数。栗子最开始就是采用这种方法拿到的密钥。

第三种方法：使用最新的 AssetRipper 打开资源文件，记得命令窗口中也会告诉你正确的解密密钥（记得是这样子的）

第四种方法：你也可以直接使用 main 分支源码编译的 il2cppdumper，这个版本自带了密钥寻找方法，可以发现找到的密钥是相同的（一开始手工找到了不知道应该填 RVA 还是 offset 还是 VA，总是解密失败，之后想着编译一下 main 分支的版本试了一下，发现最新版竟然自带了解密功能。）。

> 所以说，密钥需要填写的是 IDA 上面的 VA 地址。

通过 `il2cppdumper` 解包后，我们主要关注这几个文件：`DummyDll/Assembly-CSharp.dll`，`dump.cs`，`script.json`，`stringliteral.json`，`ida_with_struct_py3.py`

| 文件                         | 说明                                                         | 用途                                        |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------- |
| DummyDll/Assembly-CSharp.dll | 游戏的主要代码（但是不含代码）部分，由于 il2cpp 已经将程序的 C# 代码转换成了 native code，因此 `il2cppdumper` 生成的正如其名`dummydll`，只包含基本的代码组织结构，不包含内部实现。但是我们可以根据对应的 RVA 地址在 ida 中看对应的 native 汇编代码。dll 可以通过 [dnspy[ex]](https://github.com/dnSpyEx/dnSpy) 之类的 .net 反汇编工具看。 | 看看作者怎么写的游戏。抓一些 hook 点。      |
| dump.cs                      | 上面 dll 的代码格式                                          |                                             |
| script.json                  | 所有函数的 RVA 等信息                                        |                                             |
| stringliteral.json           | 所有的字符串信息，注意，这些字符串是 C#/Unity 字符串，因此会被放置在 `global-metadata.dat` 中存储，在 dll 中找不到。 | 用于抓一些 SB 作者硬编码在 dll 中的字符串。 |
| ida_with_struct_py3.py       | 用于将上述信息导入到 ida 中，ida 中选择运行脚本启动即可（注意磁盘空间，导入大概能按小时计算，存储可能会占用 GiB 级别） |                                             |



### 解包打包操作

#### 解包

UABEA/AssetRipper 都能支持解包资源文件，载入 `data.unity3d` 文件后可以看到各种资源文件。其中由于 il2cpp 的缘故，直接使用两个工具去看资源文件的话，大部分的 MonoBehaviour 文件都会存在问题。

由于旧版的 UABEA 年久失修，其自带的的 `cpp2il` 相关工具无法对应使用了 `api version 31` 的本游戏，因此这里又一个小技巧：

> 将 il2cppdumpper 生成的 dummydll 文件夹改名为 Managed，放置在 `Attorney of the Arcane_Data` 文件夹下，假装自己是一个 mono 游戏而非 il2cpp 游戏，再在 UABEA 的菜单中选择 `Enable/Disable cpp2il` 关闭内置的  cpp2il 工具支持。此时就能完美解包/打包游戏了。

#### 封包：

封包可以使用 UABEA / UABEANext 进行回填。基本上就是修改其导出的 json 文件，之后选择导入即可，具体操作截图见 [Appendix](#Appendix)，在这里不赘述了。



### 汉化所需资源说明

> 这部分按照重要性顺序说明，字库 -> 文本 -> 图片 -> 音乐

#### 字库

游戏原始使用了如下这个字体：

|      |      |
| ---- | ---- |
|      |      |
|      |      |
|      |      |

#### 文本

游戏主要台词文本使用的是 [YarnSpinner]([Start Here | Yarn Spinner](https://docs.yarnspinner.dev/))  工具，一个开源的 Game Diaglogue 工具。汉化的话有两种方法，一个是直接修改对应的台词文本（解包出来是 De）

游戏内部的各种按钮文本内嵌在各个 MonoBehaviour 的 m_text 里面，翻译的时候直接修改 MonoBehaviour 即可。



#### 图片

没什么好说的，直接 UABEA 解包即可。

#### 音乐

音乐在 Streaming Assets 里面，使用的是 bank 格式，可以直接使用对应的解包工具解包：TODO



### TIPS

如果 UABEA 识别不出来 il2cpp 游戏的 MonoBehavior，那么直接菜单中关闭 il2cpp，之后把 il2cppdumper 生成的 dummydll 改名 managed 丢到 _Data 目录下就可以了。

Texture 文件可以直接用 Plugins 里面的 edit texture 改的

如果引用了 reS 文件，这个文件是简单二进制密排，直接把自己生成的 TextMeshPro 数据 concat 上去，修正 offset 即可。



# Appendix

## 适用于本游戏的打包操作流程说明

TODO
