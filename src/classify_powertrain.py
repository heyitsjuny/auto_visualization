"""
파워트레인 분류 모듈
S&P 데이터의 Fuel Type과 Powertrain Category를 기반으로 EV/HEV/ICE를 분류합니다.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def classify_powertrain(df: pd.DataFrame) -> pd.DataFrame:
    """
    파워트레인을 EV/HEV/ICE로 분류합니다.
    
    Args:
        df (pd.DataFrame): 원본 데이터프레임
        
    Returns:
        pd.DataFrame: 파워트레인 분류가 추가된 데이터프레임
    """
    # 파워트레인 분류 컬럼 초기화
    df['powertrain_type'] = 'ICE'  # 기본값은 ICE
    
    # EV 분류 (전기차)
    ev_conditions = (
        (df['S: Fuel Type'].str.contains('BEV', case=False, na=False)) |
        (df['S: Powertrain Main Category'].str.contains('Battery Electric', case=False, na=False)) |
        (df['S: Fuel Type'].str.contains('Electric', case=False, na=False))
    )
    df.loc[ev_conditions, 'powertrain_type'] = 'EV'
    
    # HEV 분류 (하이브리드)
    hev_conditions = (
        (df['S: Powertrain Main Category'].str.contains('Hybrid', case=False, na=False)) |
        (df['S: Powertrain Main Category'].str.contains('PHEV', case=False, na=False)) |
        (df['S: Powertrain Main Category'].str.contains('Mild Hybrid', case=False, na=False)) |
        (df['S: Fuel Type'].str.contains('PHEV', case=False, na=False)) |
        (df['S: Fuel Type'].str.contains('HEV', case=False, na=False))
    )
    # HEV는 EV가 아닌 경우에만 적용
    df.loc[hev_conditions & (df['powertrain_type'] != 'EV'), 'powertrain_type'] = 'HEV'
    
    # ICE는 기본값이므로 별도 처리 불필요
    
    logger.info("파워트레인 분류 완료")
    return df


def get_powertrain_distribution(df: pd.DataFrame) -> Dict[str, int]:
    """
    파워트레인 분포를 계산합니다.
    
    Args:
        df (pd.DataFrame): 분류된 데이터프레임
        
    Returns:
        Dict[str, int]: 파워트레인별 개수
    """
    distribution = df['powertrain_type'].value_counts().to_dict()
    
    logger.info(f"파워트레인 분포: {distribution}")
    return distribution


def validate_powertrain_classification(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    파워트레인 분류 결과를 검증합니다.
    
    Args:
        df (pd.DataFrame): 분류된 데이터프레임
        
    Returns:
        Dict[str, List[str]]: 검증 결과
    """
    validation_results = {
        'ev_samples': [],
        'hev_samples': [],
        'ice_samples': [],
        'unclassified': []
    }
    
    # 각 파워트레인 타입별 샘플 추출
    for powertrain_type in ['EV', 'HEV', 'ICE']:
        sample_df = df[df['powertrain_type'] == powertrain_type].head(3)
        for _, row in sample_df.iterrows():
            sample_info = {
                        'fuel_type': row.get('S: Fuel Type', 'N/A'),
        'powertrain_category': row.get('S: Powertrain Main Category', 'N/A'),
                'classified_as': row['powertrain_type']
            }
            validation_results[f'{powertrain_type.lower()}_samples'].append(sample_info)
    
    # 분류되지 않은 데이터 확인
    unclassified = df[df['powertrain_type'].isna()]
    if len(unclassified) > 0:
        validation_results['unclassified'] = unclassified[['S: Fuel Type', 'S: Powertrain Main Category']].head(5).to_dict('records')
    
    logger.info("파워트레인 분류 검증 완료")
    return validation_results


def get_powertrain_columns() -> List[str]:
    """
    파워트레인 분류에 사용되는 컬럼들을 반환합니다.
    
    Returns:
        List[str]: 파워트레인 관련 컬럼 리스트
    """
    return [
        'S: Fuel Type',
        'S: Powertrain Main Category',
        'EP: Plug-In',
        'EP: Battery Capacity',
        'EP: System Power'
    ]


def main():
    """파워트레인 분류 테스트 함수"""
    from load_data import load_excel_data, extract_year_columns
    
    try:
        # 데이터 로딩
        file_path = "../data/20250701_LV_Prod_Extended_Pivot.xlsb"
        df = load_excel_data(file_path)
        df, year_cols = extract_year_columns(df)
        
        # 파워트레인 분류
        df = classify_powertrain(df)
        
        # 분포 확인
        distribution = get_powertrain_distribution(df)
        print(f"파워트레인 분포: {distribution}")
        
        # 검증
        validation = validate_powertrain_classification(df)
        print(f"검증 결과: {len(validation['ev_samples'])} EV, {len(validation['hev_samples'])} HEV, {len(validation['ice_samples'])} ICE 샘플")
        
        return df
        
    except Exception as e:
        logger.error(f"파워트레인 분류 테스트 실패: {e}")
        return None


if __name__ == "__main__":
    main() 