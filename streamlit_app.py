"""
Automotive Powertrain Production Trend
Interactive Web Application using Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import os
import sys

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 분석 모듈들 import
from src.load_data import load_excel_data, extract_year_columns
from src.classify_powertrain import classify_powertrain, get_powertrain_distribution
from src.aggregate_production import (
    aggregate_production_by_year, 
    calculate_market_share,
    get_regional_analysis,
    get_transition_analysis,
    get_top_regions_by_ev_share
)

# 페이지 설정
st.set_page_config(
    page_title="Automotive Powertrain Production Trend",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data():
    """Data Loading and Pre-Processing (Apply Caching)"""
    try:
        # 데이터 로딩 - 절대 경로 사용
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data", "20250701_LV_Prod_Extended_Pivot.xlsb")
        
        # 파일 존재 확인
        if not os.path.exists(file_path):
            st.error(f"Cannot find data file: {file_path}")
            return None
            
        df = load_excel_data(file_path)
        
        # Year 컬럼 추출
        df, year_cols = extract_year_columns(df)
        
        # Powertrain 분류
        df = classify_powertrain(df)
        
        # Prod. Vol. 집계
        production_data = aggregate_production_by_year(df, year_cols)
        
        # Market Share 계산
        market_share_data = calculate_market_share(production_data, year_cols)
        
        # Analysis by Region
        regional_data = get_regional_analysis(df, year_cols)
        
        # Pace of Transition 분석
        transition_data = get_transition_analysis(market_share_data, year_cols)
        
        # Top Region 분석
        top_regions = get_top_regions_by_ev_share(regional_data, target_year='2030')
        
        return {
            'df': df,
            'year_cols': year_cols,
            'production_data': production_data,
            'market_share_data': market_share_data,
            'regional_data': regional_data,
            'transition_data': transition_data,
            'top_regions': top_regions
        }
    except Exception as e:
        st.error(f"Error has occurred while loading data: {str(e)}")
        return None

def main():
    """Main Application"""
    
    # 헤더
    st.markdown('<h1 class="main-header">🚗 Automotive Powertrain Production Trend</h1>', unsafe_allow_html=True)
    
    # 데이터 로딩
    with st.spinner("Loading and Analyzing Data..."):
        data = load_and_process_data()
    
    if data is None:
        st.error("Cannot load data. Please check the file directory.")
        return
    
    # 사이드바 설정
    st.sidebar.markdown('<h3 class="sidebar-header">📊 Analysis Setting</h3>', unsafe_allow_html=True)
    
    # Year 선택
    selected_years = st.sidebar.multiselect(
        "Select Year",
        options=data['year_cols'],
        default=['2023', '2025', '2030', '2035', '2037']
    )
    
    # Region 선택
    regions = ['Greater China', 'Europe', 'Americas', 'Asia Pacific']
    selected_regions = st.sidebar.multiselect(
        "Select Region",
        options=regions,
        default=regions
    )
    
    # 실제 존재하는 Powertrain 타입 확인
    available_powertrains = data['production_data']['powertrain_type'].unique().tolist()
    
    # Powertrain 선택
    selected_powertrains = st.sidebar.multiselect(
        "Select Powertrain Type",
        options=available_powertrains,
        default=available_powertrains
    )
    
    # 메인 대시보드
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="No. of Data",
            value=f"{data['df'].shape[0]:,}",
            help="No. of Vehicle Models"
        )
    
    with col2:
        ev_count = data['df']['powertrain_type'].value_counts().get('EV', 0)
        st.metric(
            label="No. of EV Model",
            value=f"{ev_count:,}",
            help="No. of EV Model"
        )
    
    with col3:
        # 2023 Total Vol 계산 (Year가 컬럼이므로)
        total_production_2023 = data['production_data']['2023'].sum() if '2023' in data['production_data'].columns else 0
        st.metric(
            label="2023 Total Vol",
            value=f"{total_production_2023:,.0f}M",
            help="2023 Exp. Total Vol (M)"
        )
    
    with col4:
        # EV % in 2037 계산
        ev_share_2037 = 0
        if '2037_share' in data['market_share_data'].columns:
            ev_row = data['market_share_data'][data['market_share_data']['powertrain_type'] == 'EV']
            if len(ev_row) > 0:
                ev_share_2037 = ev_row['2037_share'].iloc[0]
        
        st.metric(
            label="EV % in 2037",
            value=f"{ev_share_2037:.1f}%",
            help="Exp. EV % in 2037"
        )
    
    # 탭 구성
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Prod. Volume Trend", 
        "📊 Market Share Trend", 
        "🌍 Analysis by Region", 
        "⚡ Pace of Transition", 
        "📋 Data Details"
    ])
    
    with tab1:
        st.subheader("Powertrain Volume Trend by Year")
        
        # 데이터 구조 변환: Year를 인덱스로, Powertrain을 컬럼으로
        production_df = data['production_data'].set_index('powertrain_type')
        production_df = production_df[selected_years].T  # 전치하여 Year를 인덱스로
        
        # 존재하는 Powertrain만 필터링
        available_powertrains = [pt for pt in selected_powertrains if pt in production_df.columns]
        filtered_production = production_df[available_powertrains]
        
        # Plotly로 Prod. Volume Trend 그래프
        fig = go.Figure()
        
        for powertrain in available_powertrains:
            fig.add_trace(go.Scatter(
                x=filtered_production.index,
                y=filtered_production[powertrain],
                mode='lines+markers',
                name=powertrain,
                line=dict(width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="Powertrain Volume Trend by Year",
            xaxis_title="Year",
            yaxis_title="Prod. Vol. (M)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Prod. Vol. Data 테이블
        st.subheader("Prod. Vol. Data")
        st.dataframe(filtered_production.round(2))
    
    with tab2:
        st.subheader("Powertrain Market Share Trend")
        
        # Market Share 데이터 구조 변환
        share_df = data['market_share_data'].set_index('powertrain_type')
        share_columns = [f'{year}_share' for year in selected_years if f'{year}_share' in share_df.columns]
        
        if share_columns:
            share_df = share_df[share_columns].T  # 전치하여 Year를 인덱스로
            # 컬럼명을 Year로 변경
            share_df.columns = [col.replace('_share', '') for col in share_df.columns]
            
            # 선택된 Powertrain만 필터링
            available_powertrains = [pt for pt in selected_powertrains if pt in share_df.columns]
            filtered_share = share_df[available_powertrains]
            
            # 스택 영역 차트
            fig = go.Figure()
            
            for powertrain in available_powertrains:
                fig.add_trace(go.Scatter(
                    x=filtered_share.index,
                    y=filtered_share[powertrain],
                    mode='lines',
                    fill='tonexty',
                    name=powertrain,
                    stackgroup='one'
                ))
            
            fig.update_layout(
                title="Year별 Powertrain Market Share Trend",
                xaxis_title="Year",
                yaxis_title="Market Share (%)",
                hovermode='x unified',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Market Share 데이터 테이블
            st.subheader("Market Share data")
            st.dataframe(filtered_share.round(2))
        else:
            st.warning("Cannot find Market Share data.")
    
    with tab3:
        st.subheader("EV % by Regions")
        
        # Region별 데이터 처리
        if data['regional_data']:
            # Region별 EV Portion 데이터 수집
            regional_ev_data = {}
            for region, region_df in data['regional_data'].items():
                if region in selected_regions:
                    ev_row = region_df[region_df['powertrain_type'] == 'EV']
                    if len(ev_row) > 0:
                        ev_shares = {}
                        for year in selected_years:
                            share_col = f'{year}_share'
                            if share_col in ev_row.columns:
                                ev_shares[year] = ev_row[share_col].iloc[0]
                        regional_ev_data[region] = ev_shares
            
            if regional_ev_data:
                # 데이터프레임으로 변환
                regional_df = pd.DataFrame(regional_ev_data).T
                
                # 히트맵
                fig = px.imshow(
                    regional_df,
                    aspect='auto',
                    title="EV% Heatmap by Regions",
                    labels=dict(x="Year", y="Region", color="EV Portion (%)"),
                    color_continuous_scale='RdYlBu_r'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Region별 막대 차트
                fig2 = go.Figure()
                
                for region in regional_df.index:
                    fig2.add_trace(go.Bar(
                        x=regional_df.columns,
                        y=regional_df.loc[region],
                        name=region
                    ))
                
                fig2.update_layout(
                    title="EV Portion Trend by Regions",
                    xaxis_title="Year",
                    yaxis_title="EV Portion (%)",
                    barmode='group',
                    height=500
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("Cannot find Regional EV Data.")
        else:
            st.warning("Dataname Analysis by Region does not exist.")
    
    with tab4:
        st.subheader("EV Pace of Transition Analysis")
        
        # Pace of Transition 데이터 처리
        transition_data = data['transition_data']
        
        if transition_data:
            # Pace of Transition 요약 정보 표시
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Start EV Portion",
                    value=f"{transition_data.get('start_ev_share', 0):.1f}%",
                    help=f"{transition_data.get('start_year', '2023')} EV Portion"
                )
            
            with col2:
                st.metric(
                    label="End EV Portion",
                    value=f"{transition_data.get('end_ev_share', 0):.1f}%",
                    help=f"{transition_data.get('end_year', '2037')} EV Portion"
                )
            
            with col3:
                st.metric(
                    label="Portion Change",
                    value=f"{transition_data.get('share_change', 0):.1f}%p",
                    help="EV Portion Change"
                )
            
            with col4:
                st.metric(
                    label="Prod. Vol. Change",
                    value=f"{transition_data.get('production_change', 0)/1e6:.1f}M",
                    help="EV Prod. Vol. Change (M)"
                )
            
            # Pace of Transition 시각화 (단일 값이므로 막대 차트 대신 정보 표시)
            st.subheader("Pace of Transition details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Summary-Global EV Transition")
                transition_info = f"""
                **Period**: {transition_data.get('start_year', '2023')} → {transition_data.get('end_year', '2037')}
                
                **Start EV Portion**: {transition_data.get('start_ev_share', 0):.1f}%
                **End EV Portion**: {transition_data.get('end_ev_share', 0):.1f}%
                **Portion Change**: {transition_data.get('share_change', 0):.1f}%p
                
                **Start EV Prod. Vol.**: {transition_data.get('start_ev_production', 0)/1e6:.1f}M 대
                **End EV Prod. Vol.**: {transition_data.get('end_ev_production', 0)/1e6:.1f}M 대
                **Prod. Vol. Change**: {transition_data.get('production_change', 0)/1e6:.1f}M 대
                """
                st.markdown(transition_info)
            
            with col2:
                st.subheader("2030 EV Portion Top Region")
                if not data['top_regions'].empty:
                    st.dataframe(data['top_regions'])
                else:
                    st.warning("Top Region Data does not exist.")
        else:
            st.warning("Pace of Transition Analysis Data does not exist.")
    
    with tab5:
        st.subheader("Data Details Analysis")
        
        # 데이터 요약
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Powertrain Distribution")
            powertrain_dist = data['df']['powertrain_type'].value_counts()
            fig = px.pie(
                values=powertrain_dist.values,
                names=powertrain_dist.index,
                title="Powertrain Classification Result"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Total Vol. by Year")
            # 숫자 컬럼만 선택하여 합계 계산
            numeric_cols = data['production_data'].select_dtypes(include=[np.number]).columns
            total_production = data['production_data'][numeric_cols].sum(axis=0)
            
            fig = px.line(
                x=total_production.index,
                y=total_production.values,
                title="Total Prod. Volume Trend by Year",
                labels={'x': 'Year', 'y': 'Total Prod. Vol. (M)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Original Data Sample
        st.subheader("Original Data Sample (Top 100 Lines)")
        sample_cols = ['S: Fuel Type', 'S: Powertrain Main Category', 'powertrain_type'] + selected_years[:5]
        st.dataframe(data['df'][sample_cols].head(100))
    
    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚗 Automotive Powertrain Production Trend</p>
        <p>Data Source: S&P Light Vehicle Forecast | Analysis Period: 2000-2037</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 