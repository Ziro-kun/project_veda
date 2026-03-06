import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# app.py가 있는 폴더의 위치 찾기
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 키가 없으면 경고를 띄웁니다.
if not api_key:
    st.error("⚠️ .env 파일을 찾을 수 없거나 API 키가 없습니다. 확인해주세요!")
    st.stop()

# 2. 제미나이 모델 연결 (가성비 좋은 Flash 모델 사용)
genai.configure(api_key=api_key)
try:
    # 1순위: 최신 플래시 모델
    model = genai.GenerativeModel('gemini-flash-latest')
except:
    # 2순위: 그게 없으면 프로 비전 (구관이 명관)
    model = genai.GenerativeModel('gemini-pro-vision')

# AI에게 명령
def analyze_gundam(image):
    prompt = """
    당신은 '프로젝트 베다'의 전술 오퍼레이터입니다. 
    입력된 건담(프라모델) 이미지를 분석하여 입문자를 위한 정보를 한국어로 브리핑하세요.
    
    [출력 양식]
    ### 1. 식별 코드
    - **기체명:** (정확한 기체명)
    - **예상 등급:** (MG, HG, RG 등. 확실하지 않으면 '식별 불가'로 표기)

    ### 2. 전술 데이터
    - **소속:** (지구연방군, 지온공국, 솔레스탈 비잉 등)
    - **파일럿:** (대표 파일럿 이름)
    - **특징:** (입문자가 흥미를 가질만한 특징 1줄 요약)

    ### 3. 상세 브리핑
    (해당 기체의 설정이나 애니메이션 속 활약상을 3줄 이내로 요약해서 설명)
    """
    
    response = model.generate_content([prompt, image])
    return response.text

# 화면 구성 (UI)
st.set_page_config(page_title="Project Veda", page_icon="🤖")

st.title("Project Veda 🤖")
st.caption("G-Intelligence: Tactical Information System")

st.markdown("---")

# 파일 업로더
uploaded_file = st.file_uploader("전술 데이터를 스캔할 이미지를 업로드하세요.", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Image Scanned.', use_container_width=True)

    if st.button("데이터 분석 개시 (Analyze)"):
        with st.spinner('베다 시스템이 데이터베이스와 링크 중입니다...'):
            try:
                # 위에서 만든 함수 실행
                result = analyze_gundam(image)
                
                # 결과 출력
                st.success("분석 완료.")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"시스템 오류 발생: {e}")