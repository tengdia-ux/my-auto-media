import streamlit as st
import trafilatura
import openai

st.set_page_config(page_title="全球内容本地化助手", page_icon="🌐")

with st.sidebar:
    st.title("⚙️ 配置中心")
    api_key = st.text_input("输入 DeepSeek API Key:", type="password")
    target_platform = st.selectbox("目标平台", ["小红书 (爆款图文)", "抖音 (短视频脚本)", "微信公众号 (深度文)", "微博 (即时新闻)"])

st.title("🚀 国外内容一键本地化")

url = st.text_input("粘贴国外网页链接 (URL):", placeholder="https://www.theverge.com/...")

if st.button("开始生成"):
    if not api_key:
        st.warning("请先在左侧输入 API Key")
    elif not url:
        st.warning("请输入链接")
    else:
        try:
            with st.spinner("🔍 正在抓取并分析原文..."):
                # 使用新的抓取工具 trafilatura
                downloaded = trafilatura.fetch_url(url)
                content = trafilatura.extract(downloaded)
                
                if not content:
                    st.error("无法抓取该网页内容，请尝试其他链接。")
                    st.stop()

            with st.spinner("✍️ AI 正在创作本地化内容..."):
                client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                
                system_prompt = f"你是一个专业的社交媒体专家，擅长将国外内容转化为适用于{target_platform}的内容。你会消除翻译腔，使用地道的中国社交媒体流行语。"
                user_prompt = f"原文内容：\n{content[:4000]}\n\n任务：进行本地化创作，要求有吸引力的标题、正文和标签。"

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ]
                )
                result = response.choices[0].message.content

            st.success("✅ 生成成功！")
            st.markdown(result)
            
        except Exception as e:
            st.error(f"处理失败。错误详情: {e}")
