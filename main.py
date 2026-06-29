import streamlit as st
from utils import generate_script

st.title("🎬集美Promote生成器📖")

with st.sidebar:
    # 选择模型提供商
    model_provider = st.selectbox(
        "选择模型提供商",
        ["DeepSeek", "Moonshot AI (Kimi)", "OpenAI", "智谱 AI (GLM)", "通义千问", "自定义"],
        index=0  # 默认选择 DeepSeek
    )

    # 根据选择设置默认参数
    provider_config = {
        "DeepSeek": {
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
            "key_url": "https://platform.deepseek.com/api_keys",
            "key_label": "DeepSeek"
        },
        "Moonshot AI (Kimi)": {
            "base_url": "https://api.moonshot.cn/v1",
            "model": "moonshot-v1-32k",
            "key_url": "https://platform.moonshot.cn/console/api-keys",
            "key_label": "Moonshot AI"
        },
        "OpenAI": {
            "base_url": None,
            "model": "gpt-3.5-turbo",
            "key_url": "https://platform.openai.com/account/api-keys",
            "key_label": "OpenAI"
        },
        "智谱 AI (GLM)": {
            "base_url": "https://open.bigmodel.cn/api/paas/v4",
            "model": "glm-4",
            "key_url": "https://open.bigmodel.cn/usercenter/apikeys",
            "key_label": "智谱 AI"
        },
        "通义千问": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model": "qwen-plus",
            "key_url": "https://dashscope.console.aliyun.com/apiKey",
            "key_label": "通义千问"
        },
        "自定义": {
            "base_url": "",
            "model": "",
            "key_url": "",
            "key_label": ""
        }
    }

    config = provider_config[model_provider]

    # 自定义模式下显示更多输入框
    if model_provider == "自定义":
        base_url = st.text_input("API Base URL：", placeholder="https://api.example.com/v1")
        model_name = st.text_input("模型名称：", placeholder="如：gpt-3.5-turbo")
    else:
        base_url = config["base_url"]
        model_name = config["model"]
        st.caption(f"默认模型：{model_name}")

    # 关键：显示当前实际使用的 API 地址，防止缓存导致发错服务器
    st.info(f"当前调用地址：{base_url}")

    # 如果当前选的是 Kimi，提醒用户余额不足，建议切换
    if model_provider == "Moonshot AI (Kimi)":
        st.warning("⚠️ Kimi 当前余额不足，请在下拉菜单切换为 DeepSeek，或使用其他提供商。")

    api_key = st.text_input(f"请输入{config['key_label']} API密钥：", type="password")

    # 拦截：如果用的是 Kimi 的 Key，直接报错
    if api_key and api_key.startswith("ak-"):
        st.error("❌ 检测到这是 Kimi (Moonshot) 的 API Key，余额已不足。请换成 DeepSeek 的 Key (sk- 开头)，或在上方下拉菜单切换到其他提供商。")
        st.stop()

    if config["key_url"]:
        st.markdown(f"[获取{config['key_label']} API密钥]({config['key_url']})")

subject = st.text_input("💡 请输入视频的主题")
video_length = st.number_input("⏱️ 请输入视频的大致时长（单位：分钟）", min_value=0.1, step=0.1)
creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
submit = st.button("生成脚本")

if submit and not api_key:
    st.info("请输入你的 API 密钥")
    st.stop()
if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("视频长度需要大于或等于0.1")
    st.stop()
if submit and model_provider == "自定义" and (not base_url or not model_name):
    st.info("自定义模式下需要填写 API Base URL 和模型名称")
    st.stop()
if submit:
    with st.status("正在生成脚本，请稍等...") as status:
        status.write("1️⃣ 正在生成标题...")
        search_result, title, script = generate_script(
            subject,
            video_length,
            creativity,
            api_key,
            base_url=base_url,
            model_name=model_name
        )
        status.write("2️⃣ 标题已生成，正在生成脚本...")
        status.update(label="脚本生成完成！", state="complete")
    st.success("视频脚本已生成！")
    st.subheader("🔥 标题：")
    st.write(title)
    st.subheader("📝 视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果 👀"):
        st.info(search_result)