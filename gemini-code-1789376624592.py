import streamlit as st
import pandas as pd
import plotly.express as px
import traceback

# 페이지 기본 설정
st.set_page_config(
    page_title="Data Explorer Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # 메인 타이틀
    st.title("📊 Data Explorer Pro")
    st.markdown("Streamlit Cloud 배포용으로 제작된 완벽한 CSV 데이터 분석 앱입니다. 왼쪽 사이드바에서 데이터를 업로드하세요.")

    # 사이드바 설정
    st.sidebar.header("1. 데이터 설정")
    uploaded_file = st.sidebar.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

    # 파일이 업로드되었을 때의 로직
    if uploaded_file is not None:
        try:
            # 데이터 로딩 스피너
            with st.spinner("데이터를 불러오고 분석하는 중입니다..."):
                df = pd.read_csv(uploaded_file)

            # 빈 데이터프레임 예외 처리
            if df.empty:
                st.warning("⚠️ 업로드된 파일에 데이터가 없습니다. 다른 파일을 업로드해주세요.")
                return

            st.sidebar.success("✅ 데이터 로드 성공!")

            # 탭을 사용하여 UI를 깔끔하게 분리
            tab1, tab2, tab3 = st.tabs(["데이터 미리보기", "요약 통계", "데이터 시각화"])

            # [탭 1] 데이터 미리보기
            with tab1:
                st.subheader("데이터셋 미리보기")
                st.info(f"총 데이터 크기: {df.shape[0]:,} 행, {df.shape[1]:,} 열")
                st.dataframe(df.head(100), use_container_width=True)
                st.caption("※ 성능을 위해 상위 100행만 미리보기로 제공됩니다.")

            # [탭 2] 요약 통계
            with tab2:
                st.subheader("데이터 기본 통계량")
                try:
                    st.dataframe(df.describe(include='all'), use_container_width=True)
                except Exception as stat_error:
                    st.error("통계량을 계산하는 중 문제가 발생했습니다.")
                    st.code(str(stat_error))

            # [탭 3] 동적 데이터 시각화
            with tab3:
                st.subheader("맞춤형 데이터 시각화")
                st.markdown("X축과 Y축을 선택하여 데이터를 시각화해 보세요.")
                
                # 열 이름 리스트 추출
                columns = df.columns.tolist()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    x_axis = st.selectbox("X축 선택", options=columns, index=0)
                with col2:
                    y_axis = st.selectbox("Y축 선택", options=columns, index=len(columns)-1 if len(columns) > 1 else 0)
                with col3:
                    chart_type = st.selectbox("차트 종류", options=["Scatter (산점도)", "Bar (막대)", "Line (선)"])

                st.markdown("---")
                
                # 차트 렌더링 및 예외 처리
                try:
                    with st.spinner("차트를 그리는 중..."):
                        if chart_type == "Scatter (산점도)":
                            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
                        elif chart_type == "Bar (막대)":
                            fig = px.bar(df, x=x_axis, y=y_axis, title=f"{x_axis}별 {y_axis} 합계/분포")
                        elif chart_type == "Line (선)":
                            fig = px.line(df, x=x_axis, y=y_axis, title=f"{x_axis}에 따른 {y_axis} 변화")
                            
                        # 시각화 출력
                        st.plotly_chart(fig, use_container_width=True)
                        
                except Exception as plot_error:
                    st.error("❌ 차트를 생성하는 중 오류가 발생했습니다. 선택한 열의 데이터 타입(문자열/숫자)이 해당 시각화에 적합한지 확인해주세요.")
                    with st.expander("에러 상세 정보 보기"):
                        st.code(str(plot_error))

        # CSV 파싱 에러 처리
        except pd.errors.EmptyDataError:
            st.error("❌ 오류: 업로드된 CSV 파일이 완전히 비어있습니다.")
        except pd.errors.ParserError:
            st.error("❌ 오류: CSV 파일을 읽어들이는 데 실패했습니다. 파일 형식이 손상되었거나 올바르지 않습니다.")
        # 기타 예상치 못한 에러 처리
        except Exception as e:
            st.error("❌ 알 수 없는 심각한 오류가 발생했습니다.")
            with st.expander("개발자용 에러 로그"):
                st.code(traceback.format_exc())
                
    # 파일이 업로드되지 않은 초기 화면
    else:
        st.info("👈 분석을 시작하려면 왼쪽 메뉴에서 CSV 파일을 업로드해 주세요.")
        
        # 데모용 안내 메시지
        st.markdown("""
        ### 이 앱에서 제공하는 기능:
        1. **데이터 자동 파싱**: CSV 파일을 읽고 데이터프레임으로 변환합니다.
        2. **자동 통계 요약**: 수치형 및 범주형 데이터의 기초 통계량을 제공합니다.
        3. **동적 시각화**: Plotly를 활용하여 사용자가 직접 X/Y축을 지정해 인터랙티브 차트를 그릴 수 있습니다.
        4. **완벽한 예외 처리**: 깨진 파일, 빈 데이터, 잘못된 차트 매핑 등에 대한 에러를 방어합니다.
        """)

if __name__ == "__main__":
    main()