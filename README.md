# Project Veda 🤖🛡️

**Project Veda**는 건프라(건담 프라모델) 입문자와 빌더들을 위한 AI 시각 보조 및 전술 정보 브리핑 시스템입니다. 사용자가 건프라 이미지를 업로드하면 기체를 식별하고, 전술 데이터 및 상세 브리핑을 제공합니다. AI 엔지니어를 지망하는 사람이 건프라 매니아인 배우자를 위해 만들었습니다.

## ✨ 주요 기능

- **이미지 업로드 및 스캔**: 드래그앤드롭 또는 클릭으로 건프라 이미지 업로드 (`jpg`, `png`, `jpeg` 지원)
- **전술 데이터 브리핑**:
  - **식별 코드**: 기체명 및 예상 등급 (MG, HG, RG 등) 식별
  - **전술 데이터**: 기체의 소속, 대표 파일럿, 핵심 특징 요약
  - **상세 브리핑**: 애니메이션 내 활약상 및 기체 설정 제공
- **VLM 기반 분석**: Google Gemini (Flash) API를 연동하여 이미지 분석 수행

## 📂 주요 파일 구성

- **`api/index.py`**: Flask 메인 애플리케이션. 이미지 업로드 처리 및 Gemini API 연동
- **`templates/index.html`**: 군사 HUD 컨셉의 다크 테마 UI
- **`static/style.css`**: 프리미엄 다크 테마 스타일시트
- **`static/script.js`**: 이미지 업로드, 분석 요청, 결과 렌더링 로직
- **`vercel.json`**: Vercel 서버리스 배포 설정
- **`check.py`**: API 키 및 Gemini 모델 동작 확인 유틸리티

---

## 🚀 배포 (Vercel)

1. [Vercel Dashboard](https://vercel.com)에서 이 레포지토리를 import
2. **Environment Variables** 설정:
   ```
   GOOGLE_API_KEY = 본인의_Gemini_API_키
   ```
3. Deploy 버튼 클릭

---

## 🛠️ 로컬 실행

```bash
git clone <repository-url>
cd project_veda
pip install -r requirements.txt
```

`.env` 파일 생성:

```env
GOOGLE_API_KEY="본인의_API_키_입력"
```

앱 실행:

```bash
python api/index.py
# → http://localhost:5000
```

---

## 🔮 향후 개발 계획

현재의 범용 VLM API 의존도를 낮추고 빠르고 정확한 건프라 특화 인식을 위해, **추후 자체적인 컴퓨터 비전(CV) 인식 엔진을 개발하여 탑재할 예정**입니다. 이를 통해 파츠, 등급, 세부 기체명 등 건프라 판별의 정확도와 속도를 비약적으로 높일 계획입니다.
