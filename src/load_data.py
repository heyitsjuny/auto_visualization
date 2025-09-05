"""
데이터 로딩 및 전처리 모듈
S&P Light Vehicle Forecast 데이터를 로드하고 기본 전처리를 수행합니다.
"""

import pandas as pd
import re
from typing import Tuple, List
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_excel_data(file_path: str) -> pd.DataFrame:
    """
    S&P Light Vehicle Forecast Excel 파일을 로드합니다.
    
    Args:
        file_path (str): Excel 파일 경로
        
    Returns:
        pd.DataFrame: 로드된 데이터프레임
    """
    try:
        logger.info(f"데이터 로딩 시작: {file_path}")
        
        # 파일 확장자에 따라 적절한 엔진과 시트 선택
        if file_path.endswith('.xlsb'):
            # .xlsb 파일의 경우 'LV Prod Extended' 시트 로드
            df = pd.read_excel(file_path, sheet_name='LV Prod Extended', engine='pyxlsb')
        else:
            df = pd.read_excel(file_path, engine='openpyxl')
            
        logger.info(f"데이터 로딩 완료: {df.shape[0]}행, {df.shape[1]}열")
        return df
    except Exception as e:
        logger.error(f"데이터 로딩 실패: {e}")
        raise


def extract_year_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    연도별 생산량 컬럼을 추출하고 정리합니다.
    
    Args:
        df (pd.DataFrame): 원본 데이터프레임
        
    Returns:
        Tuple[pd.DataFrame, List[str]]: 정리된 데이터프레임과 연도 컬럼 리스트
    """
    # 연도 컬럼 패턴 찾기 (CY 2023 ~ CY 2037)
    year_pattern = r'CY\s*(\d{4})'
    year_columns = []
    
    for col in df.columns:
        match = re.search(year_pattern, str(col))
        if match:
            year = match.group(1)
            year_columns.append((col, year))
    
    # 연도 컬럼명 변경
    for old_col, year in year_columns:
        df = df.rename(columns={old_col: year})
    
    year_cols = [year for _, year in year_columns]
    year_cols.sort()
    
    logger.info(f"연도 컬럼 추출 완료: {len(year_cols)}개 ({year_cols[0]}~{year_cols[-1]})")
    
    return df, year_cols


def get_data_info(df: pd.DataFrame) -> dict:
    """
    데이터 기본 정보를 반환합니다.
    
    Args:
        df (pd.DataFrame): 데이터프레임
        
    Returns:
        dict: 데이터 정보 딕셔너리
    """
    info = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'null_counts': df.isnull().sum().to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum()
    }
    
    logger.info(f"데이터 정보: {df.shape[0]}행, {df.shape[1]}열")
    return info


def main():
    """데이터 로딩 테스트 함수"""
    file_path = "../data/20250701_LV_Prod_Extended_Pivot.xlsb"
    
    try:
        # 데이터 로딩
        df = load_excel_data(file_path)
        
        # 연도 컬럼 추출
        df, year_cols = extract_year_columns(df)
        
        # 데이터 정보 출력
        info = get_data_info(df)
        print(f"연도 컬럼: {year_cols}")
        print(f"컬럼 수: {len(df.columns)}")
        
        return df, year_cols
        
    except Exception as e:
        logger.error(f"데이터 로딩 테스트 실패: {e}")
        return None, None


if __name__ == "__main__":
    main() 