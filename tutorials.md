WIP： 正在写

---------------------

### Unity  基本知识速记

以本游戏为例，这里记录了一些 Unity 中常见的知识点（所有用到的工具会在附录表格中记录，并提供地址）

**版本** Unity 的跨版本兼容性是一坨，基本上游戏都要锁定某个版本的 Unity 进行开发。一般来说可以直接查看游戏可执行文件或者 dll 中的版本号拿到 Unity 版本。本游戏是 2022.3.46 版本，可以看到 Unity 官网上该版本是 24/09/XX 发布（还挺新的）

**后端** Unity 游戏分为 Mono 和 il2cpp 两种。其中 il2cpp 就是直接将  C# 代码翻译成 C++ 后变成 C++ 程序。同时在 `global-metadata.dat` 中存储了各种类的字段等信息用于反射等操作（大概），这个游戏就是使用 il2cpp 的。
关于 `global-metadata.dat` 可以参见：https://il2cppdumper.com/reverse/structural-overview-and-finding-the-metadata

**unityplayer.dll** Unity 引擎的主要代码，C++ 写的，有时候可能通过 Unity 官方服务器拿到符号表。相应的工具有：TODO，但是本游戏似乎拿不到。反正执行各种 downloader 都会报 404 not found，不知道是梯子问题还是真的没有。

**Hook** Unity 程序根据 Mono 或者 il2cpp 有两种 Hook 方式。同时也有两大主流 Hook 框架：Bepinex，MelonLoader

**XUnity.AutoTranslator (下称 XAT)** 好东西，但是本游戏用不了。简单看了一下 XAT 的代码，其提供的替换 TextMeshPro 字库图的方法是：

1. 调用 Unity.AssetBundle.dll 的 LoadFromFile 之类的函数从文件系统中加载一个 UnityFS 文件
2. 之后 Unity 自动解包这个文件，再调用 Unity.TMPro.dll 的相关操作去创建一个 FontAsset
3. 之后将这个 Font 强制丢给给游戏内部的 TMPro 类，实现 Font 替换。

对于本游戏，问题是由于单个 data.unity3d 打包了所有的资源文件，因此 il2cpp 裁剪掉了没用的 Unity.AssetBundle.dll，导致我们没有函数可以加载封包。同时我们也不太可能直接调用一个 C# 版的 dll 手动加载（感觉利用 coreclr 相关函数手动创建 clr，再加载 dll 也可以试试？）。

**资源文件替换** 资源文件的替换有点麻烦，目前已知的对于封包内文件，只有 UABEA 提供了资源文件替换功能。
利用 Hook 等方式重定向加载资源文件的方法可以参见 XAT 中 ResourceRedirector 相关的做法（不过前提感觉都是游戏没有阉割了 AssetBundle.dll）

**字库** Unity 游戏已经开始逐渐转向使用 TextMeshPro 插件(?) 制作字库了，与 Unreal 不同，TextMeshPro 真的就是字库图（aka 根据提供的字符 + TTF 字体文件来生成对应的高精度图片，之后显示文字是把图片贴上去）。因此大部分时候 Unity 游戏很容易出现缺字的问题，需要重建字库。



### 汉化流程记录

#### 解包：

##### 代码

游戏采用 il2cpp 编译，使用 il2cppdumper 进行解密，由于游戏使用的是 Version 31 API，因此需要使用 pre-release 的最新版 il2cppdumper 进行解密操作。

解密中需要的两个密钥 TODO，对应的两个解密参数地址分别为：TODO

这里有多种方法可以拿到密钥，第一个是 Unknown 上面这个方法：TODO

我更推荐使用这个方法自行寻找密钥：TODO

当然，你也可以直接使用最新版的 AssetRipper，这个版本自带了密钥寻找方法，可以发现找到的密钥是相同的。

或者直接用 GitHub repo 中的源码编译出来的 il2cppdumper 解包也能拿到密钥（也就是说 master 分支其实比 pre-release 还新）：

> 这里有一个坑，密钥需要填写的是 IDA 上面基于 0x

##### 资源

UABEA/AssetRipper 都能支持解包资源文件，载入 `data.unity3d` 文件后可以看到各种资源文件。其中由于 il2cpp 的缘故，直接使用两个工具去看资源文件的话，大部分的 MonoBehaviour 文件都会存在问题。



#### 封包：

封包可以使用 UABEA 进行回填。



#### 文本

游戏主要台词文本使用的是 [YarnSpinner]([Start Here | Yarn Spinner](https://docs.yarnspinner.dev/))  工具，一个开源的 Game Diaglogue 工具。汉化的话有两种方法，一个是直接修改对应的台词文本（解包出来是 De）

游戏内部的各种按钮文本内嵌在各个 MonoBehaviour 的 m_text 里面，翻译的时候直接修改 MonoBehaviour 即可。

#### 字库

游戏原始使用了如下这个字体：

|      |      |
| ---- | ---- |
|      |      |
|      |      |
|      |      |



#### 图片

没什么好说的，直接 UABEA 解包即可。

#### 音乐

音乐在 Streaming Assets 里面，使用的是 bank 格式，可以直接使用对应的解包工具解包：TODO



### TIPS

如果 UABEA 识别不出来 il2cpp 游戏的 MonoBehavior，那么直接菜单中关闭 il2cpp，之后把 il2cppdumper 生成的 dummydll 改名 managed 丢到 _Data 目录下就可以了。

Texture 文件可以直接用 Plugins 里面的 edit texture 改的

如果引用了 reS 文件，这个文件是简单二进制密排，直接把自己生成的 TextMeshPro 数据 concat 上去，修正 offset 即可。

