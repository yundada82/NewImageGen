import streamlit as st
from openai import OpenAI

st.title("🎨 AI 이미지 스타일 선택기")
st.write("텍스트와 스타일을 선택하면 AI가 이미지를 생성합니다.")

# ℹ️ 사용 방법 안내
st.markdown("## ℹ️ 사용 방법")
st.markdown("""
- 왼쪽 사이드바에 OpenAI API 키를 입력하세요.  
- 원하는 이미지 설명(프롬프트)을 선택하거나 직접 입력하세요.  
- 스타일을 선택한 후 [이미지 생성하기] 버튼을 누르면 결과가 출력됩니다.
""")

# 🔐 API 키 입력
st.sidebar.title("🔑 설정")
openai_api_key = st.sidebar.text_input("OpenAI API 키 입력", type="password")
if not openai_api_key:
    st.sidebar.warning("OpenAI API 키를 입력하세요.")
    st.stop()

# 🔌 OpenAI 클라이언트 생성
client = OpenAI(api_key=openai_api_key)

# ✏️ 프롬프트 선택 및 직접 입력
default_prompts = [
    "A cute dog",
    "A futuristic cityscape at night",
    "A bowl of ramen with chopsticks",
    "A fantasy forest with glowing plants"
]
selected_prompt = st.selectbox("📝 프롬프트를 선택하세요", default_prompts)
custom_prompt = st.text_input("또는 직접 프롬프트를 입력하세요 (선택 사항)", value="")

# 실제 사용할 프롬프트 결정
prompt_text = custom_prompt.strip() if custom_prompt else selected_prompt

# 🎨 스타일 선택
style = st.radio("🎨 스타일을 선택하세요", ["실사", "일러스트", "만화"])

# 스타일 매핑
style_map = {
    "실사": "in photorealistic style",
    "일러스트": "in illustration style",
    "만화": "in cartoon style"
}

# 최종 프롬프트 구성
final_prompt = f"{prompt_text}, {style_map[style]}"

# ▶️ 버튼 클릭 시 이미지 생성
if st.button("이미지 생성하기"):
    with st.spinner("이미지를 생성 중입니다..."):
        try:
            response = client.images.generate(
                prompt=final_prompt,
                model="dall-e-3",
                n=1,
                size="1024x1024"  # 기본 정사각형 크기 사용
            )
            image_url = response.data[0].url
            st.image(image_url, caption=f"{style} 스타일 이미지", use_column_width=True)
        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
