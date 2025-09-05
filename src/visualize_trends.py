"""
시각화 모듈
Powertrain 생산 트렌드와 Market Share Trend를 다양한 차트로 시각화합니다.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_plot_style():
    """시각화 스타일을 설정합니다."""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12


def plot_production_trends(agg_df: pd.DataFrame, year_columns: List[str], 
                          save_path: Optional[str] = None) -> plt.Figure:
    """
    Powertrain별 Prod. Volume Trend를 선 그래프로 시각화합니다.
    
    Args:
        agg_df (pd.DataFrame): 집계된 Prod. Vol. Data프레임
        year_columns (List[str]): Year 컬럼 리스트
        save_path (Optional[str]): 저장 경로
        
    Returns:
        plt.Figure: 생성된 그래프
    """
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = {'EV': '#2E8B57', 'HEV': '#FF6B35', 'ICE': '#4682B4'}
    
    for _, row in agg_df.iterrows():
        powertrain_type = row['powertrain_type']
        production_values = [row[year] for year in year_columns if year in row.index]
        
        ax.plot(year_columns[:len(production_values)], production_values, 
                marker='o', linewidth=3, markersize=8, 
                label=powertrain_type, color=colors.get(powertrain_type, '#333333'))
    
    ax.set_title('Global Automotive Powertrain Production Trends (2023-2037)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Production Volume (Units)', fontsize=14)
    ax.legend(fontsize=12, frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3)
    
    # Y축을 백만 단위로 표시
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Prod. Volume Trend 그래프 저장: {save_path}")
    
    return fig


def plot_market_share_trends(share_df: pd.DataFrame, year_columns: List[str], 
                            save_path: Optional[str] = None) -> plt.Figure:
    """
    Powertrain Market Share Trend를 스택 영역 차트로 시각화합니다.
    
    Args:
        share_df (pd.DataFrame): Market Share 데이터프레임
        year_columns (List[str]): Year 컬럼 리스트
        save_path (Optional[str]): 저장 경로
        
    Returns:
        plt.Figure: 생성된 그래프
    """
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = {'EV': '#2E8B57', 'HEV': '#FF6B35', 'ICE': '#4682B4'}
    
    # 스택 영역 차트 데이터 준비
    share_data = {}
    for _, row in share_df.iterrows():
        powertrain_type = row['powertrain_type']
        share_values = [row[f'{year}_share'] for year in year_columns if f'{year}_share' in row.index]
        share_data[powertrain_type] = share_values
    
    # 스택 영역 차트 생성
    ax.stackplot(year_columns[:len(next(iter(share_data.values())))], 
                 share_data.values(), 
                 labels=share_data.keys(),
                 colors=[colors.get(pt, '#333333') for pt in share_data.keys()],
                 alpha=0.8)
    
    ax.set_title('Global Automotive Powertrain Market Share Trends (2023-2037)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Market Share (%)', fontsize=14)
    ax.legend(fontsize=12, frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3)
    
    # Y축 범위 설정
    ax.set_ylim(0, 100)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Market Share Trend 그래프 저장: {save_path}")
    
    return fig


def plot_top_regions_ev_share(top_regions_df: pd.DataFrame, target_year: str = '2030',
                             save_path: Optional[str] = None) -> plt.Figure:
    """
    EV Portion Top Region을 바 차트로 시각화합니다.
    
    Args:
        top_regions_df (pd.DataFrame): Top Region 데이터프레임
        target_year (str): 기준 Year
        save_path (Optional[str]): 저장 경로
        
    Returns:
        plt.Figure: 생성된 그래프
    """
    setup_plot_style()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 바 차트 생성
    bars = ax.bar(range(len(top_regions_df)), top_regions_df['ev_share'], 
                  color='#2E8B57', alpha=0.8, edgecolor='black', linewidth=1)
    
    # Region명을 X축 라벨로 설정
    ax.set_xticks(range(len(top_regions_df)))
    ax.set_xticklabels(top_regions_df['region'], rotation=45, ha='right')
    
    # 바 위에 값 표시
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax.set_title(f'Top Regions by EV Market Share ({target_year})', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Region', fontsize=14)
    ax.set_ylabel('EV Market Share (%)', fontsize=14)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Top Region EV Portion 그래프 저장: {save_path}")
    
    return fig


def plot_transition_speed_comparison(regional_results: Dict[str, pd.DataFrame], 
                                   start_year: str = '2023', end_year: str = '2037',
                                   save_path: Optional[str] = None) -> plt.Figure:
    """
    Region별 Pace of Transition를 비교하는 바 차트를 생성합니다.
    
    Args:
        regional_results (Dict[str, pd.DataFrame]): Analysis by Region 결과
        start_year (str): Start Year
        end_year (str): End Year
        save_path (Optional[str]): 저장 경로
        
    Returns:
        plt.Figure: 생성된 그래프
    """
    setup_plot_style()
    
    # Pace of Transition 계산
    transition_data = []
    for region, region_df in regional_results.items():
        ev_data = region_df[region_df['powertrain_type'] == 'EV']
        
        if len(ev_data) > 0:
            start_share = ev_data.iloc[0].get(f'{start_year}_share', 0)
            end_share = ev_data.iloc[0].get(f'{end_year}_share', 0)
            share_change = end_share - start_share
            
            transition_data.append({
                'region': region,
                'share_change': share_change,
                'start_share': start_share,
                'end_share': end_share
            })
    
    # 변화량 기준으로 정렬
    transition_df = pd.DataFrame(transition_data)
    transition_df = transition_df.sort_values('share_change', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 바 차트 생성
    colors = ['#2E8B57' if x >= 0 else '#DC143C' for x in transition_df['share_change']]
    bars = ax.bar(range(len(transition_df)), transition_df['share_change'], 
                  color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    # Region명을 X축 라벨로 설정
    ax.set_xticks(range(len(transition_df)))
    ax.set_xticklabels(transition_df['region'], rotation=45, ha='right')
    
    # 바 위에 값 표시
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + (0.5 if height >= 0 else -1),
                f'{height:.1f}%p', ha='center', va='bottom' if height >= 0 else 'top', 
                fontweight='bold')
    
    ax.set_title(f'EV Market Share Change by Region ({start_year} → {end_year})', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Region', fontsize=14)
    ax.set_ylabel('EV Share Change (Percentage Points)', fontsize=14)
    ax.grid(True, alpha=0.3, axis='y')
    
    # 0선 추가
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Pace of Transition 비교 그래프 저장: {save_path}")
    
    return fig


def create_summary_dashboard(share_df: pd.DataFrame, year_columns: List[str],
                           top_regions_df: pd.DataFrame, transition_analysis: Dict,
                           save_path: Optional[str] = None) -> plt.Figure:
    """
    종합 대시보드를 생성합니다.
    
    Args:
        share_df (pd.DataFrame): Market Share 데이터프레임
        year_columns (List[str]): Year 컬럼 리스트
        top_regions_df (pd.DataFrame): Top Region 데이터프레임
        transition_analysis (Dict): Pace of Transition 분석 결과
        save_path (Optional[str]): 저장 경로
        
    Returns:
        plt.Figure: 생성된 대시보드
    """
    setup_plot_style()
    
    fig = plt.figure(figsize=(20, 16))
    
    # 서브플롯 생성
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Market Share Trend (상단 전체)
    ax1 = fig.add_subplot(gs[0, :])
    colors = {'EV': '#2E8B57', 'HEV': '#FF6B35', 'ICE': '#4682B4'}
    
    share_data = {}
    for _, row in share_df.iterrows():
        powertrain_type = row['powertrain_type']
        share_values = [row[f'{year}_share'] for year in year_columns if f'{year}_share' in row.index]
        share_data[powertrain_type] = share_values
    
    ax1.stackplot(year_columns[:len(next(iter(share_data.values())))], 
                  share_data.values(), 
                  labels=share_data.keys(),
                  colors=[colors.get(pt, '#333333') for pt in share_data.keys()],
                  alpha=0.8)
    
    ax1.set_title('Global Powertrain Market Share Evolution', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Market Share (%)', fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 100)
    
    # 2. Top Region EV Portion (좌하단)
    ax2 = fig.add_subplot(gs[1, 0])
    bars = ax2.bar(range(len(top_regions_df)), top_regions_df['ev_share'], 
                   color='#2E8B57', alpha=0.8)
    ax2.set_xticks(range(len(top_regions_df)))
    ax2.set_xticklabels(top_regions_df['region'], rotation=45, ha='right')
    ax2.set_title('Top Regions by EV Share (2030)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('EV Share (%)', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Pace of Transition 요약 (우하단)
    ax3 = fig.add_subplot(gs[1, 1])
    transition_text = f"""
    EV Transition Analysis ({transition_analysis.get('start_year', '2023')} → {transition_analysis.get('end_year', '2037')})
    
    Start EV Share: {transition_analysis.get('start_ev_share', 0):.1f}%
    End EV Share: {transition_analysis.get('end_ev_share', 0):.1f}%
    Change: {transition_analysis.get('share_change', 0):.1f} percentage points
    
    Production Change: {transition_analysis.get('production_change', 0)/1e6:.1f}M units
    """
    
    ax3.text(0.1, 0.5, transition_text, transform=ax3.transAxes, fontsize=12,
             verticalalignment='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
    ax3.set_title('Global EV Transition Summary', fontsize=14, fontweight='bold')
    ax3.axis('off')
    
    # 4. Year별 Prod. Volume Trend (하단 전체)
    ax4 = fig.add_subplot(gs[2, :])
    for _, row in share_df.iterrows():
        powertrain_type = row['powertrain_type']
        production_values = [row[year] for year in year_columns if year in row.index]
        ax4.plot(year_columns[:len(production_values)], production_values, 
                marker='o', linewidth=2, markersize=6, 
                label=powertrain_type, color=colors.get(powertrain_type, '#333333'))
    
    ax4.set_title('Production Volume Trends', fontsize=16, fontweight='bold')
    ax4.set_xlabel('Year', fontsize=12)
    ax4.set_ylabel('Production Volume (Units)', fontsize=12)
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    plt.suptitle('Automotive Powertrain Analysis Dashboard', fontsize=18, fontweight='bold', y=0.98)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"종합 대시보드 저장: {save_path}")
    
    return fig


def main():
    """시각화 테스트 함수"""
    from load_data import load_excel_data, extract_year_columns
    from classify_powertrain import classify_powertrain
    from aggregate_production import (aggregate_production_by_year, calculate_market_share,
                                    get_transition_analysis, get_regional_analysis,
                                    get_top_regions_by_ev_share)
    
    try:
        # 데이터 로딩 및 처리
        file_path = "../data/20250701_LV_Prod_Extended_Pivot.xlsb"
        df = load_excel_data(file_path)
        df, year_cols = extract_year_columns(df)
        df = classify_powertrain(df)
        
        # Prod. Vol. 집계 및 Market Share 계산
        agg_df = aggregate_production_by_year(df, year_cols)
        share_df = calculate_market_share(agg_df, year_cols)
        
        # Analysis by Region
        regional_results = get_regional_analysis(df, year_cols)
        top_regions = get_top_regions_by_ev_share(regional_results)
        transition = get_transition_analysis(share_df, year_cols)
        
        # 출력 디렉토리 생성
        os.makedirs("../outputs", exist_ok=True)
        
        # 시각화 생성
        plot_production_trends(agg_df, year_cols, "../outputs/production_trends.png")
        plot_market_share_trends(share_df, year_cols, "../outputs/market_share_trends.png")
        
        if len(top_regions) > 0:
            plot_top_regions_ev_share(top_regions, save_path="../outputs/top_regions_ev_share.png")
        
        if regional_results:
            plot_transition_speed_comparison(regional_results, save_path="../outputs/transition_speed.png")
        
        create_summary_dashboard(share_df, year_cols, top_regions, transition, 
                               "../outputs/summary_dashboard.png")
        
        logger.info("모든 시각화 완료")
        
    except Exception as e:
        logger.error(f"시각화 테스트 실패: {e}")


if __name__ == "__main__":
    main() 