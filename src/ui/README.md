# 🥣 AI 음식 검사 프로젝트

한식 이미지 분류 및 영양 정보 분석을 위한 AI 기반 웹 어플리케이션 UI

## 📁 프로젝트 구조

```

ui/          # 배포용 Streamlit 앱
├── app.py                     # 메인 웹 애플리케이션
├── model/                     # 학습된 모델 파일
│   ├── food-2025-08-26 03:29:51.110312.keras
│   └── indices-2025-08-26 03:29:51.110312.json
├── module/                    # 핵심 모듈
│   ├── api.py                 # API 연결 및 데이터 처리
│   ├── img.py                 # 이미지 전처리
│   └── predict.py             # 모델 예측
└── requirements.txt           # 의존성 패키지
```

## 🚀 실행 방법

### 1. 환경 설정

```bash
# Python 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows
```

### 2. 의존성 설치

```bash
cd food_nutrition_deploy
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하여 애플리케이션을 사용할 수 있습니다.

## 📋 사용법
1. app.py의 118번 줄부터가 핵심 수행 코드입니다.
```
if st.session_state.current_result is None:
   st.session_state.current_image = uploaded_file
   img_array = get_image_from_uploader(uploaded_file)
   pred = predict(img_array)
   st.session_state.current_image_name = pred['predict'][0]
   st.session_state.current_image_confidence = pred['confidence']
   result = connection_api(pred, [])
   st.session_state.current_result = result
```

2. module의 predict.py는 model에서 keras를 읽어서 예측하게 됩니다.
3. module의 img.py는 입력 이미지를 배열로 변환합니다.
4. module의 api는 향후 LLM의 응답을 받을 코드입니다.

향후 체크한 뒤 남형님이 짜주신 구조에 맞게 변형해서 main에 올리도록 하겠습니다!