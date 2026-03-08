import os
from io import BytesIO
from flask import Flask, request, jsonify, render_template
from PIL import Image
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

PROMPT = """
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


def pil_to_bytes(image: Image.Image) -> bytes:
    buf = BytesIO()
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # 퀄리티를 최적화하여 Vercel 메모리 초과/타임아웃 방지
    image.thumbnail((1024, 1024))
    image.save(buf, format='JPEG', quality=85)
    return buf.getvalue()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': '이미지 파일이 없습니다.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다.'}), 400

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return jsonify({'error': 'API 키가 설정되지 않았습니다. 환경 변수를 확인해주세요.'}), 503

    try:
        image = Image.open(file.stream)
        img_bytes = pil_to_bytes(image)
        
        # JPEG로 강제 변환하므로 mime type은 항상 image/jpeg
        mime = 'image/jpeg'

        # v1beta → v1 강제 지정 (유료 키 환경에서 v1beta 404 방지)
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(api_version='v1')
        )
        image_part = types.Part.from_bytes(data=img_bytes, mime_type=mime)

        # gemini-1.5-flash: 범용 무료 티어에서 가장 안정적으로 지원
        MODELS = ['gemini-1.5-flash', 'gemini-1.5-flash-8b', 'gemini-1.5-pro']
        response = None
        last_err = None
        for model_name in MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[PROMPT, image_part],
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
                    )
                )
                break
            except Exception as e:
                last_err = e
                continue
        if response is None:
            raise last_err
        return jsonify({'result': response.text})

    except Exception as e:
        return jsonify({'error': f'분석 중 오류 발생: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
