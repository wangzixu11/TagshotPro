# TagshotPro
智能批量图片标签与重命名工具。 基于 Python/CustomTkinter 构建的跨平台桌面应用，通过结构化标签和实时预览，将图片归档命名效率提升 80%。支持内置压缩。

### 🔗下载与使用
(https://pan.baidu.com/s/1T4arErKy7hcqfQe8xQAFcg?pwd=1010 )

### ✨项目简介

Tagshot Pro V2 是一款专为高效工作流设计的跨平台桌面应用。它解决了在工程、设计或资料归档过程中，手动为大量图片文件命名耗时长、易出错的问题。

通过一个直观的暗色主题界面，您可以快速浏览图片、应用预设的结构化标签，并实时预览最终文件名。这款工具将繁琐的命名过程转化为快速、自动化的“点选”流程。

### 🚀核心特性

#### 🏷️ 标签驱动的重命名

结构化标签库： 预设三大标签分类（例如：外部视角、内部视角、细节特写），用户只需点击即可将标签添加到文件名中，确保命名规范化和一致性。

统一前缀管理： 轻松添加和修改项目编号或日期等通用前缀，所有图片文件名自动更新。

实时预览： 在列表视图中，文件的新名称与原名称并排显示，确保“所见即所得”，避免命名错误。

#### 🔄优化工作流

图片自动流转： 应用标签或完成操作后，程序自动跳转到列表中的下一张图片，极大地提升了连续处理图片的效率。

拖放支持： 快速将图片文件夹或文件拖入应用，立即开始工作。

跨平台兼容： 基于 Python 和 customtkinter 构建，完美支持 Windows, macOS 和 Linux 系统。

#### ⚙️实用工具箱

内置图片压缩： 在重命名的同时，提供可选的图片压缩功能，可自定义质量和最大尺寸，优化存储空间。

错误处理与日志： 提供清晰的错误报告和操作状态信息，确保重命名过程可靠。

现代化 UI： 采用专业的暗色主题和清晰的三栏布局，提供舒适高效的用户体验。

#### 技术栈

核心语言: Python

GUI 框架: customtkinter (现代化 UI)

图像处理: Pillow (PIL)

文件系统操作: os, shutil

---

程序依赖以下主要的 Python 库：

1.  **`customtkinter`**: 用于创建现代、美观的桌面 GUI 界面。
2.  **`Pillow` (PIL)**: Python 图像库，用于处理图片（例如打开、重命名和压缩）。

以下是完整的安装和运行步骤：

### 🛠️ 步骤一：安装 Python (如果尚未安装)

如果您的电脑上还没有安装 Python，请先安装它。

1.  访问 [Python 官方网站](https://www.python.org/downloads/)。
2.  下载并运行最新的稳定版本（建议使用 Python 3.9 或更高版本）。
3.  **安装时，请确保勾选** `Add python.exe to PATH` **（或类似选项）**。这使得您可以在命令行（CMD/终端）中直接运行 Python 命令。

### 🛠️ 步骤二：安装所需的 Python 库

安装库是运行您的程序最关键的一步。您需要使用 Python 的包管理器 `pip` 来安装 `customtkinter` 和 `Pillow`。

1.  **打开命令行/终端：**

      * **Windows:** 按下 `Win` 键 + `R`，输入 `cmd`，然后按回车。
      * **macOS/Linux:** 打开 **终端 (Terminal)** 应用程序。

2.  **执行安装命令：**
    运行以下命令来安装所有必需的库：

    ```bash
    pip install customtkinter Pillow
    ```

      * `pip install customtkinter`: 安装 GUI 框架。
      * `pip install Pillow`: 安装图片处理库 (PIL)。

3.  **确认安装成功：**
    如果命令执行成功，您将看到类似 `Successfully installed customtkinter-x.x.x Pillow-x.x.x` 的消息。

### 🛠️ 步骤三：运行 Tagshot Pro V2

现在，您的系统已经准备好运行程序了。

1.  **定位文件：**

      * 找到您保存 `TagshotProV2.py` 文件的文件夹。

2.  **在命令行中导航到该文件夹：**

      * 回到您在步骤二中打开的命令行/终端。
      * 使用 `cd` (Change Directory) 命令进入您的文件所在目录。

    **示例：** 如果您的文件在桌面上名为 `TagshotPro` 的文件夹中，您可能需要输入类似如下的命令：

    ```bash
    cd C:\Users\YourUser\Desktop\TagshotPro
    ```

    (请将路径替换为您实际的文件夹路径)

3.  **执行程序：**
    在命令行中，输入以下命令来运行您的 Python 脚本：

    ```bash
    python TagshotProV2.py
    ```

程序窗口应该会立即弹出。如果程序顺利运行，说明您安装的所有依赖都已正确配置。

-----

### ⚠️ 疑难解答

如果在运行过程中遇到任何问题，请检查以下几点：

| 问题 | 错误信息示例 | 解决方法 |
| :--- | :--- | :--- |
| **找不到命令** | `python is not recognized as an internal or external command` | **确保**在安装 Python 时勾选了 `Add python.exe to PATH`，或手动将其添加到系统环境变量中。 |
| **缺少库** | `ModuleNotFoundError: No module named 'customtkinter'` | 回到步骤二，重新运行 `pip install customtkinter Pillow` 命令，确保您的命令行使用的 Python 环境是正确的。 |
| **权限问题** | `Permission denied: 'TagshotProV2.py'` | 尝试使用 `python3 TagshotProV2.py`，或确保您的用户账户有权执行该文件。 |

---

# 更新日志

#### V2.1 
- 增加了编辑标签功能，现在标签支持用户自定义。适配更多应用场景。
- 更新了图片选取编辑功能，现在可以通过四个点选择需要添加高斯模糊的区域。
- 修复了PNG图片无法压缩的问题，现在上传图片的时候，会先检测是否有除了jpg以外的格式，如果有则询问是否先转换为jpg格式。
- 修复了进入模糊编辑后预览图片尺寸不正确的问题。
