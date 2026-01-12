import streamlit as st
import google.generativeai as genai
import json

# ===== PWA ファイル提供 =====
# manifest.json を返す
if st.query_params.get("file") == "manifest":
    manifest = {
        "name": "Gemini Chat",
        "short_name": "GemChat",
        "start_url": ".",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#ffffff",
        "icons": []
    }
    st.write(json.dumps(manifest))
    st.stop()

# sw.js を返す
if st.query_params.get("file") == "sw":
    st.write("""
self.addEventListener("install", e => {
    self.skipWaiting();
});
self.addEventListener("activate", e => {
    clients.claim();
});
""")
    st.stop()

# ===== ページ設定 =====
st.set_page_config(page_title="Gemini Chat", layout="wide")

# ===== PWA 登録 =====
st.markdown("""
<link rel="manifest" href="?file=manifest">
<script>
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("?file=sw");
}
</script>
""", unsafe_allow_html=True)

# ===== サイドバー =====
st.sidebar.title("⚙️ 設定")

model_name = st.sidebar.selectbox(
    "モデルを選択",
    ["gemini-2.0-flash", "gemini-2.0-pro"]
)

system_prompt = st.sidebar.text_area(
    "システムプロンプト（任意）",
    "あなたは優秀なアシスタントです。"
)

if st.sidebar.button("🧹 会話をクリア"):
    st.session_state.messages = []

# ===== Gemini クライアント =====
# ★ 正しい初期化方法（Client() は存在しないためエラーになる）
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel(model_name)

# ===== タイトル =====
st.markdown(
    "<h1 style='text-align: center;'>💬 Gemini Chat UI</h1>",
    unsafe_allow_html=True
)

# ===== チャット履歴 =====
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        st.markdown(
            f"""
            <div style='text-align: right; margin: 10px;'>
                <div style='display: inline-block; max-width: 80%; background-color: #DCF8C6; padding: 10px 15px; border-radius: 10px;'>
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='text-align: left; margin: 10px;'>
                <div style='display: inline-block; max-width: 80%; background-color: #F1F0F0; padding: 10px 15px; border-radius: 10px;'>
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ===== 入力欄 =====
prompt = st.chat_input("メッセージを入力")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    contents = system_prompt + "\n\nユーザー: " + prompt

    # ★ 正しい生成方法
    response = model.generate_content(contents)
    reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()
