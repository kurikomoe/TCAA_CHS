[![SyncParatranz](https://github.com/kurikomoe/TCAA_CHS/actions/workflows/sync_paratranz.yml/badge.svg)](https://github.com/kurikomoe/TCAA_CHS/actions/workflows/sync_paratranz.yml)

## 运行图

<center><bold>让我们说中文！</bold></center>

![运行图](docs/title.png)

![中文测试](docs/first_scene.png)

![教程](./docs/tutorial.png)



## 计划

程序媛一只，不会翻译，希望能找到人。

文本目前在 https://paratranz.cn/projects/12747 上进行汉化协作。可以自行提交加入申请。

汉化组工作群：862399169 (QQ)，需要翻译，校对，修图（大概）。



## 进度


### 文本汉化

- [x] 找出所有的 m_text
  - [x] 主界面文本在 level0 中，剩下大部分在 resource 中。
  - [x] 导出到 paratranz 脚本
  - [x] paratranz 导入游戏脚本
- [x] 找出所有的人物介绍 （CharacterLibrary-level0-599.json）
  - [x] 导出到 paratranz 脚本
  - [x] paratranz 导入游戏脚本
- [x] 咒语描述文本（SpellLibrary-level0-602.json）
  - [x] 导出到 paratranz 脚本
  - [x] paratranz 导入游戏脚本。
- [x] 物品描述文本（ItemLibrary-level0-603.json）
  - [x] 导出到 paratranz 脚本
  - [x] paratranz 导入游戏脚本。
- [x] Default(en) 的剧本文件
  - [x] 导出到 paratranz 脚本
  - [x] paratranz 导入游戏脚本。
- [x] Case 内部文本，例如教程等
  - [x] 这部分文本内嵌在 yarn script 中。位于 `Case 1-sharedassets0.assets-154.json` 这种文件内部的 compiledYarnProgram 字节码内。经过看 yarnspinner 源代码可知，这部分脚本通过虚拟机执行，通过观察发现，这些其实是 protobuf 编译后的二进制，<del>因此可以使用 `protoscope` 直接编辑文本。</del>
      切换到 yarn-spinner 2.2.1 版本，可以直接利用 yarn.proto 定义文件解析 protobuf，获得对应的 inst 虚拟机指令。
      通过分析 RunCommand 指令过滤出所有内嵌文本 instruction，之后对这些文本进行提取汉化。
  - [x] 汉化方法：导出文本后
    - [x] <del>直接 hook 对应的显示函数，替换文本</del> 不行，发现要 hook 的地方还挺多的（>2)
    - [x] <del>利用 protoscope 重新编译后导入到资源文件中 (见 samples 文件夹)</del>
    - [x] 利用 自己写的脚本 重新编译后导入到资源文件中 (见 samples 文件夹)
- [ ] 其他待定


### 图片汉化（目前不涉及）

- [ ] 如果修的图少： UABEA 直接导入 png

- [ ] 如果修的图多：导出后修正 resS 文件再批量导入。




### 字库替换（完成）

>  这部分只能手动用 UABEA 操作的样子。

目前所有字体都替换成了同一个字体，需要有汉化组美工来推荐字体映射。原始字体放在 assets 文件夹。



需要修正的文件：

- SDC
  - m_Name
  - m_GameObject
    - m_FileID
    - m_PathID
  - m_Script
    - m_FileID
    - m_PathID
  - material
    - m_FileID
    - m_PathID
  - m_SourceFontFile 这个感觉不改也行，应该不是动态生成的，这部分可能只是个 editor 看的
  - m_FaceInfo
    - m_FamilyName
    - m_StyleName
  - m_AtlasTextures:
    - Array
      - m_FileId
      - m_PathID

- Material
  - m_Name
  - m_Shader
    - m_FileID
    - m_PathID
- Atlas
  - m_Name
  - 合理利用导出和 edit resS 文件

注意，TMPro 的 Monobehaviour 重导入可能会出错（表现为导入后 edit data 后显示序列化出错），此时重新导入直到 edit data 正常为止。
