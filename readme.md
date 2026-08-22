# 视频脚本生成器

一个基于 Streamlit 和 LangChain 的中文视频脚本生成工具。输入视频主题、预期时长和创造力参数后，应用会调用大语言模型生成标题，并参考中文维基百科检索结果生成结构化脚本。

## 功能特点

- 支持 DeepSeek、Moonshot AI（Kimi）、OpenAI、智谱 AI（GLM）和通义千问。
- 支持填写自定义的 OpenAI 兼容 API 地址与模型名称。
- 分两步生成视频标题和视频脚本。
- 自动检索中文维基百科，为脚本补充参考信息。
- 可调节视频时长和生成内容的创造力。
- 维基百科检索失败时会自动降级，仍可继续生成脚本。

## 界面参数

| 参数 | 说明 |
| --- | --- |
| 模型提供商 | 选择要调用的模型服务，默认使用 DeepSeek |
| API 密钥 | 对应模型服务商提供的 API Key，仅用于本次请求 |
| 视频主题 | 希望生成脚本的主题 |
| 视频时长 | 期望的视频时长，单位为分钟，最小值为 0.1 |
| 创造力 | 对应模型的 `temperature`，数值越低越严谨，越高越多样 |

## 支持的模型

| 提供商 | 默认模型 | 默认 API 地址 |
| --- | --- | --- |
| DeepSeek | `deepseek-chat` | `https://api.deepseek.com/v1` |
| Moonshot AI（Kimi） | `moonshot-v1-32k` | `https://api.moonshot.cn/v1` |
| OpenAI | `gpt-3.5-turbo` | 使用 OpenAI SDK 默认地址 |
| 智谱 AI（GLM） | `glm-4` | `https://open.bigmodel.cn/api/paas/v4` |
| 通义千问 | `qwen-plus` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 自定义 | 自行填写 | 自行填写 OpenAI 兼容接口地址 |

模型名称、接口可用性和计费规则可能随服务商调整，请以各服务商控制台为准。

## 技术栈

- Python
- Streamlit
- LangChain
- `langchain-openai`
- Wikipedia API

## 项目结构

```text
video_generator/
├── main.py           # Streamlit 页面、参数校验和结果展示
├── utils.py          # 提示词、模型调用和维基百科检索
├── requirements.txt  # Python 依赖及锁定版本
├── .gitignore        # Git 忽略规则
└── readme.md          # 项目说明
```

## 快速开始

### 1. 进入项目目录

```bash
cd /Users/leecy/Documents/米奇妙妙屋/视频脚本生成器/video_generator
```

### 2. 创建并激活虚拟环境

推荐使用 Python 3.10 或更高版本。

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell：

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. 安装依赖

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. 启动应用

```bash
python -m streamlit run main.py
```

启动后，浏览器通常会自动打开：

```text
http://localhost:8501
```

## 使用方法

1. 在左侧栏选择模型提供商。
2. 输入该提供商的 API 密钥。
3. 输入视频主题和预计时长。
4. 调整创造力参数。
5. 点击“生成脚本”。
6. 查看生成的标题、脚本及维基百科参考结果。

选择“自定义”时，还需要填写：

- API Base URL，例如 `https://api.example.com/v1`
- 模型名称，例如 `your-model-name`

自定义服务必须兼容 OpenAI Chat Completions 调用方式。

## 生成流程

```text
视频主题
   ↓
大模型生成标题
   ↓
检索中文维基百科
   ↓
标题 + 视频时长 + 检索结果
   ↓
大模型生成【开头、中间、结尾】结构的视频脚本
```

## API 密钥与隐私

- 当前代码从 Streamlit 侧边栏读取 API 密钥，不会自动读取项目中的 `.env` 文件。
- `.env` 已被 Git 忽略，请勿提交 API Key、访问令牌或其他敏感信息。
- API 密钥会被发送给所选模型服务商，用于完成模型请求。
- 视频主题会发送给模型服务商，并用于查询维基百科；请勿输入不应外传的敏感内容。
- 如果密钥曾被提交到 Git 或公开分享，请立即到对应服务商控制台撤销并重新生成。

## 常见问题

### 提示“请输入你的 API 密钥”

需要在左侧栏填写与当前模型提供商匹配的有效 API Key。

### 自定义模型无法调用

请确认：

- API Base URL 完整且通常以 `/v1` 结尾。
- 模型名称与服务商文档完全一致。
- 服务支持 OpenAI 兼容的 Chat Completions 接口。
- API Key 有效且账户余额充足。

### 生成过程超时

单次模型调用的超时时间为 60 秒。可以稍后重试、切换模型服务商，或检查网络和服务状态。

### 维基百科搜索失败

程序会显示“维基百科搜索失败”，随后跳过参考资料并直接根据主题生成脚本，不会因此终止整个流程。

### Kimi 密钥被拦截

当前界面对以 `ak-` 开头的 Kimi 密钥设置了余额提示和拦截逻辑。若账户已经恢复可用，需要先调整 `main.py` 中的对应判断。

## 当前限制

- 生成结果只显示在页面中，暂未提供一键导出功能。
- 视频时长仅作为提示词约束，实际脚本长度由模型决定。
- 每次生成包含两次模型请求，可能产生相应的 API 费用。
- 模型输出和维基百科内容可能存在错误，正式使用前应人工核对。

## 开发说明

页面入口位于 `main.py`，核心生成逻辑位于 `utils.py`：

- `main.py`：模型选择、参数输入、校验、进度状态和结果展示。
- `utils.py`：构建提示词、初始化 `ChatOpenAI`、生成标题、检索维基百科并生成脚本。

修改代码后可重新运行：

```bash
python -m streamlit run main.py
```

Streamlit 会监听文件变化并自动刷新页面。
