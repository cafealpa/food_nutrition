import streamlit as st
import time
import random
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

def analyze_food_image(image):
    """음식 이미지를 분석하고 영양 정보를 반환하는 함수"""
    time.sleep(3)  # 실제 AI 분석을 시뮬레이션
    
    # 예시 음식 데이터베이스
    food_samples = [
        {
            'name': '김치찌개',
            'nutrition': {
                '칼로리': 180,
                '탄수화물': 15,
                '단백질': 12,
                '지방': 8,
                '나트륨': 1200,
                '식이섬유': 4
            },
            'confidence': 0.92
        },
        {
            'name': '비빔밥',
            'nutrition': {
                '칼로리': 520,
                '탄수화물': 75,
                '단백질': 18,
                '지방': 15,
                '나트륨': 800,
                '식이섬유': 8
            },
            'confidence': 0.88
        },
        {
            'name': '불고기',
            'nutrition': {
                '칼로리': 290,
                '탄수화물': 8,
                '단백질': 26,
                '지방': 18,
                '나트륨': 650,
                '식이섬유': 1
            },
            'confidence': 0.95
        }
    ]
    
    # 랜덤하게 음식 선택 (실제로는 AI 모델이 분석)
    selected_food = random.choice(food_samples)
    
    return selected_food

def create_nutrition_chart(nutrition_data):
    """영양성분을 차트로 시각화"""
    # 막대 차트 생성
    fig = go.Figure()
    
    nutrients = list(nutrition_data.keys())
    values = list(nutrition_data.values())
    
    # 색상 매핑
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
    
    fig.add_trace(go.Bar(
        x=nutrients,
        y=values,
        marker_color=colors[:len(nutrients)],
        text=values,
        textposition='auto',
    ))
    
    fig.update_layout(
        title='영양성분 분석 결과',
        xaxis_title='영양소',
        yaxis_title='함량',
        showlegend=False,
        height=400
    )
    
    return fig

def create_nutrition_pie_chart(nutrition_data):
    """주요 영양소 비율을 파이 차트로 시각화"""
    # 탄수화물, 단백질, 지방만 추출
    macros = {
        '탄수화물': nutrition_data.get('탄수화물', 0),
        '단백질': nutrition_data.get('단백질', 0),
        '지방': nutrition_data.get('지방', 0)
    }
    
    fig = px.pie(
        values=list(macros.values()),
        names=list(macros.keys()),
        title="주요 영양소 비율",
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="음식 영양 분석기",
        page_icon="🍽️",
        layout="wide"
    )
    
    # 자동 스크롤을 위한 CSS와 JavaScript 추가
    st.markdown("""
    <style>
    .scroll-target {
        scroll-margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🍽️ 음식 영양 분석기")
    st.markdown("---")
    
    # 세션 스테이트 초기화
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    
    # 다시 하기 버튼 (결과가 있을 때만 표시)
    if st.session_state.analysis_complete:
        if st.button("🔄 다시 분석하기", type="secondary"):
            st.session_state.analysis_complete = False
            st.session_state.analysis_result = None
            st.session_state.uploaded_image = None
            st.rerun()
    
    # 분석이 완료되지 않았을 때만 업로드 영역 표시
    if not st.session_state.analysis_complete:
        # 이미지 업로드 영역
        st.header("📷 음식 이미지 업로드")
        uploaded_file = st.file_uploader(
            "음식 사진을 업로드하세요",
            type=['png', 'jpg', 'jpeg'],
            help="PNG, JPG, JPEG 형식의 이미지 파일을 업로드하세요",
            key="food_uploader"
        )
        
        if uploaded_file is not None:
            # 업로드된 이미지 저장
            st.session_state.uploaded_image = Image.open(uploaded_file)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(st.session_state.uploaded_image, caption="업로드된 음식 사진", use_container_width=True)
            
            # 분석 버튼
            if st.button("🔍 영양 분석 시작", type="primary"):
                # 프로그레스바와 로딩 메시지를 먼저 표시
                st.markdown('<div class="scroll-target" id="progress-section"></div>', unsafe_allow_html=True)
                st.header("⏳ 분석 진행 중...")
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 프로그레스 진행 중임을 사용자에게 알림
                st.empty()  # 화면 업데이트를 위한 빈 공간
                
                # 진행률 시뮬레이션
                for i in range(101):
                    progress_bar.progress(i)
                    if i < 25:
                        status_text.text('🔍 이미지 전처리 중...')
                    elif i < 50:
                        status_text.text('🤖 AI 음식 인식 중...')
                    elif i < 75:
                        status_text.text('📊 영양성분 분석 중...')
                    else:
                        status_text.text('📈 결과 생성 중...')
                    time.sleep(0.03)
                
                # 분석 실행
                analysis_result = analyze_food_image(st.session_state.uploaded_image)
                st.session_state.analysis_result = analysis_result
                st.session_state.analysis_complete = True
                
                st.rerun()
        else:
            st.info("👆 음식 사진을 업로드하여 영양 분석을 시작하세요!")
    
    # 분석 결과 표시
    if st.session_state.analysis_complete and st.session_state.analysis_result:
        # 업로드된 이미지 다시 표시
        if st.session_state.uploaded_image:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(st.session_state.uploaded_image, caption="분석된 음식 사진", use_container_width=True)
        
        st.markdown('<div class="scroll-target" id="results-section"></div>', unsafe_allow_html=True)
        st.header("📊 분석 결과")
        
        # 결과가 표시됨을 강조
        st.balloons()  # 분석 완료를 축하하는 애니메이션
        
        analysis_result = st.session_state.analysis_result
        
        # 음식명과 신뢰도
        col1, col2 = st.columns(2)
        with col1:
            st.metric("인식된 음식", analysis_result['name'])
        with col2:
            st.metric("인식 정확도", f"{analysis_result['confidence']*100:.1f}%")
        
        st.markdown("---")
        
        # 영양성분 정보
        st.subheader("🥗 영양성분 정보")
        
        nutrition = analysis_result['nutrition']
        
        # 영양성분 메트릭 카드
        cols = st.columns(3)
        nutrients_list = list(nutrition.items())
        
        for i, (nutrient, value) in enumerate(nutrients_list):
            with cols[i % 3]:
                unit = "kcal" if nutrient == "칼로리" else "g" if nutrient != "나트륨" else "mg"
                st.metric(nutrient, f"{value}{unit}")
        
        # 차트 표시
        col1, col2 = st.columns(2)
        
        with col1:
            # 영양성분 막대 차트
            chart = create_nutrition_chart(nutrition)
            st.plotly_chart(chart, use_container_width=True)
        
        with col2:
            # 주요 영양소 비율 파이 차트
            pie_chart = create_nutrition_pie_chart(nutrition)
            st.plotly_chart(pie_chart, use_container_width=True)
        
        # 영양 정보 텍스트
        st.subheader("📝 상세 영양 정보")
        
        st.write(f"""
        **{analysis_result['name']}**의 영양성분 분석 결과입니다.
        
        - **칼로리**: {nutrition['칼로리']}kcal
        - **탄수화물**: {nutrition['탄수화물']}g
        - **단백질**: {nutrition['단백질']}g  
        - **지방**: {nutrition['지방']}g
        - **나트륨**: {nutrition['나트륨']}mg
        - **식이섬유**: {nutrition['식이섬유']}g
        
        이 음식은 균형잡힌 영양소를 제공하며, 건강한 식단의 일부로 섭취하실 수 있습니다.
        """)
        
        st.success("✅ 영양 분석이 완료되었습니다!")
        
        # 다시 하기 버튼을 결과 하단에도 추가
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 새로운 음식 분석하기", type="primary"):
                st.session_state.analysis_complete = False
                st.session_state.analysis_result = None
                st.session_state.uploaded_image = None
                st.rerun()

if __name__ == "__main__":
    main()


# aihubshell -mode d -datasetkey 79 -aihubapikey 'E4306A0F-2AA6-4B70-8D13-B08E98CA588A'