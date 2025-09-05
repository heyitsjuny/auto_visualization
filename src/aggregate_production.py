"""
생산량 집계 및 점유율 계산 모듈
파워트레인별 연도별 생산량을 집계하고 점유율을 계산합니다.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def aggregate_production_by_year(df: pd.DataFrame, year_columns: List[str]) -> pd.DataFrame:
    """
    파워트레인별 연도별 생산량을 집계합니다.
    
    Args:
        df (pd.DataFrame): 분류된 데이터프레임
        year_columns (List[str]): 연도 컬럼 리스트
        
    Returns:
        pd.DataFrame: 집계된 생산량 데이터프레임
    """
    # 파워트레인별로 그룹화하여 연도별 생산량 합계 계산
    agg_data = []
    
    for powertrain_type in ['EV', 'HEV', 'ICE']:
        powertrain_df = df[df['powertrain_type'] == powertrain_type]
        
        if len(powertrain_df) > 0:
            year_totals = {}
            for year in year_columns:
                if year in powertrain_df.columns:
                    total = powertrain_df[year].sum()
                    year_totals[year] = total
            
            year_totals['powertrain_type'] = powertrain_type
            agg_data.append(year_totals)
    
    # 데이터프레임으로 변환
    agg_df = pd.DataFrame(agg_data)
    
    # 연도 컬럼을 숫자로 변환하여 정렬
    for year in year_columns:
        if year in agg_df.columns:
            agg_df[year] = pd.to_numeric(agg_df[year], errors='coerce')
    
    logger.info(f"생산량 집계 완료: {len(agg_df)} 파워트레인 타입")
    return agg_df


def calculate_market_share(agg_df: pd.DataFrame, year_columns: List[str]) -> pd.DataFrame:
    """
    연도별 파워트레인 점유율을 계산합니다.
    
    Args:
        agg_df (pd.DataFrame): 집계된 생산량 데이터프레임
        year_columns (List[str]): 연도 컬럼 리스트
        
    Returns:
        pd.DataFrame: 점유율이 추가된 데이터프레임
    """
    # 점유율 계산을 위한 복사본 생성
    share_df = agg_df.copy()
    
    for year in year_columns:
        if year in share_df.columns:
            # 해당 연도의 총 생산량 계산
            total_production = share_df[year].sum()
            
            if total_production > 0:
                # 점유율 계산 (퍼센트)
                share_df[f'{year}_share'] = (share_df[year] / total_production) * 100
            else:
                share_df[f'{year}_share'] = 0
    
    logger.info("점유율 계산 완료")
    return share_df


def get_regional_analysis(df: pd.DataFrame, year_columns: List[str], 
                         region_column: str = 'S: Region') -> Dict[str, pd.DataFrame]:
    """
    지역별 파워트레인 분석을 수행합니다.
    
    Args:
        df (pd.DataFrame): 원본 데이터프레임
        year_columns (List[str]): 연도 컬럼 리스트
        region_column (str): 지역 컬럼명
        
    Returns:
        Dict[str, pd.DataFrame]: 지역별 분석 결과
    """
    if region_column not in df.columns:
        logger.warning(f"지역 컬럼 '{region_column}'을 찾을 수 없습니다.")
        return {}
    
    regional_results = {}
    
    # 지역별로 그룹화하여 분석
    for region in df[region_column].unique():
        if pd.isna(region):
            continue
            
        region_df = df[df[region_column] == region]
        
        # 지역별 파워트레인 집계
        region_agg = aggregate_production_by_year(region_df, year_columns)
        region_share = calculate_market_share(region_agg, year_columns)
        
        regional_results[region] = region_share
    
    logger.info(f"지역별 분석 완료: {len(regional_results)}개 지역")
    return regional_results


def get_transition_analysis(agg_df: pd.DataFrame, year_columns: List[str], 
                           start_year: str = '2023', end_year: str = '2037') -> Dict[str, float]:
    """
    전환 속도 분석을 수행합니다 (특정 기간의 EV 비중 변화).
    
    Args:
        agg_df (pd.DataFrame): 집계된 데이터프레임
        year_columns (List[str]): 연도 컬럼 리스트
        start_year (str): 시작 연도
        end_year (str): 종료 연도
        
    Returns:
        Dict[str, float]: 전환 속도 분석 결과
    """
    if start_year not in year_columns or end_year not in year_columns:
        logger.error(f"분석 연도가 유효하지 않습니다: {start_year}, {end_year}")
        return {}
    
    # EV 데이터 추출
    ev_data = agg_df[agg_df['powertrain_type'] == 'EV']
    
    if len(ev_data) == 0:
        logger.warning("EV 데이터를 찾을 수 없습니다.")
        return {}
    
    ev_row = ev_data.iloc[0]
    
    # 시작 연도와 종료 연도의 EV 생산량
    start_production = ev_row[start_year]
    end_production = ev_row[end_year]
    
    # 전체 생산량에서의 EV 비중
    total_start = agg_df[start_year].sum()
    total_end = agg_df[end_year].sum()
    
    start_share = (start_production / total_start * 100) if total_start > 0 else 0
    end_share = (end_production / total_end * 100) if total_end > 0 else 0
    
    # 변화량 계산
    share_change = end_share - start_share
    production_change = end_production - start_production
    
    transition_analysis = {
        'start_year': start_year,
        'end_year': end_year,
        'start_ev_share': start_share,
        'end_ev_share': end_share,
        'share_change': share_change,
        'start_ev_production': start_production,
        'end_ev_production': end_production,
        'production_change': production_change
    }
    
    logger.info(f"전환 속도 분석 완료: {start_year}→{end_year}, EV 비중 변화: {share_change:.2f}%p")
    return transition_analysis


def get_top_regions_by_ev_share(regional_results: Dict[str, pd.DataFrame], 
                               target_year: str = '2030', top_n: int = 5) -> pd.DataFrame:
    """
    특정 연도 기준 EV 비중 상위 지역을 반환합니다.
    
    Args:
        regional_results (Dict[str, pd.DataFrame]): 지역별 분석 결과
        target_year (str): 기준 연도
        top_n (int): 상위 개수
        
    Returns:
        pd.DataFrame: 상위 지역 데이터프레임
    """
    top_regions = []
    
    for region, region_df in regional_results.items():
        ev_data = region_df[region_df['powertrain_type'] == 'EV']
        
        if len(ev_data) > 0 and f'{target_year}_share' in ev_data.columns:
            ev_share = ev_data.iloc[0][f'{target_year}_share']
            ev_production = ev_data.iloc[0][target_year]
            
            top_regions.append({
                'region': region,
                'ev_share': ev_share,
                'ev_production': ev_production
            })
    
    # EV 비중 기준으로 정렬
    top_df = pd.DataFrame(top_regions)
    if len(top_df) > 0:
        top_df = top_df.sort_values('ev_share', ascending=False).head(top_n)
    
    logger.info(f"EV 비중 상위 {len(top_df)}개 지역 선정 완료")
    return top_df


def main():
    """생산량 집계 테스트 함수"""
    from load_data import load_excel_data, extract_year_columns
    from classify_powertrain import classify_powertrain
    
    try:
        # 데이터 로딩 및 분류
        file_path = "../data/20250701_LV_Prod_Extended_Pivot.xlsb"
        df = load_excel_data(file_path)
        df, year_cols = extract_year_columns(df)
        df = classify_powertrain(df)
        
        # 생산량 집계
        agg_df = aggregate_production_by_year(df, year_cols)
        print(f"집계 결과: {agg_df.shape}")
        
        # 점유율 계산
        share_df = calculate_market_share(agg_df, year_cols)
        print(f"점유율 계산 완료: {share_df.shape}")
        
        # 전환 속도 분석
        transition = get_transition_analysis(share_df, year_cols)
        print(f"전환 속도: {transition}")
        
        return share_df
        
    except Exception as e:
        logger.error(f"생산량 집계 테스트 실패: {e}")
        return None


if __name__ == "__main__":
    main() 