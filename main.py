"""
Automotive Powertrain Production Trend 메인 실행 파일
전체 분석 파이프라인을 실행하고 결과를 생성합니다.
"""


import sys
import os
import logging
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.load_data import load_excel_data, extract_year_columns, get_data_info
from src.classify_powertrain import classify_powertrain, get_powertrain_distribution, validate_powertrain_classification
from src.aggregate_production import (aggregate_production_by_year, calculate_market_share,
                                     get_transition_analysis, get_regional_analysis,
                                     get_top_regions_by_ev_share)
from src.visualize_trends import (plot_production_trends, plot_market_share_trends,
                                plot_top_regions_ev_share, plot_transition_speed_comparison,
                                create_summary_dashboard)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_full_analysis():
    """전체 분석 파이프라인을 실행합니다."""
    
    start_time = datetime.now()
    logger.info("=== Automotive Powertrain Production Trend 시작 ===")
    
    try:
        # 1. 데이터 로딩
        logger.info("1단계: 데이터 로딩")
        file_path = "data/20250701_LV_Prod_Extended_Pivot.xlsb"
        df = load_excel_data(file_path)
        
        # 데이터 정보 출력
        info = get_data_info(df)
        logger.info(f"데이터 크기: {info['shape']}")
        logger.info(f"컬럼 수: {len(info['columns'])}")
        
        # 2. Year 컬럼 추출
        logger.info("2단계: Year 컬럼 추출")
        df, year_cols = extract_year_columns(df)
        logger.info(f"분석 Year: {year_cols[0]} ~ {year_cols[-1]} ({len(year_cols)}년)")
        
        # 3. 파워트레인 분류
        logger.info("3단계: 파워트레인 분류")
        df = classify_powertrain(df)
        
        # 분류 결과 확인
        distribution = get_powertrain_distribution(df)
        logger.info(f"파워트레인 분포: {distribution}")
        
        # 분류 검증
        validation = validate_powertrain_classification(df)
        logger.info(f"분류 검증 완료: EV {len(validation['ev_samples'])}개, HEV {len(validation['hev_samples'])}개, ICE {len(validation['ice_samples'])}개")
        
        # 4. 생산량 집계
        logger.info("4단계: 생산량 집계")
        agg_df = aggregate_production_by_year(df, year_cols)
        logger.info(f"집계 완료: {agg_df.shape}")
        
        # 5. 점유율 계산
        logger.info("5단계: 점유율 계산")
        share_df = calculate_market_share(agg_df, year_cols)
        logger.info("점유율 계산 완료")
        
        # 6. Pace of Transition 분석
        logger.info("6단계: Pace of Transition 분석")
        transition = get_transition_analysis(share_df, year_cols)
        logger.info(f"Pace of Transition: {transition['share_change']:.2f}%p ({transition['start_year']}→{transition['end_year']})")
        
        # 7. Analysis by Region
        logger.info("7단계: Analysis by Region")
        regional_results = get_regional_analysis(df, year_cols)
        logger.info(f"Analysis by Region 완료: {len(regional_results)}개 지역")
        
        # 8. 상위 지역 선정
        logger.info("8단계: 상위 지역 선정")
        top_regions = get_top_regions_by_ev_share(regional_results)
        logger.info(f"상위 지역 선정 완료: {len(top_regions)}개 지역")
        
        # 9. 출력 디렉토리 생성
        logger.info("9단계: 출력 디렉토리 생성")
        os.makedirs("outputs", exist_ok=True)
        
        # 10. 시각화 생성
        logger.info("10단계: 시각화 생성")
        
        # Prod. Volume Trend
        plot_production_trends(agg_df, year_cols, "outputs/production_trends.png")
        
        # Market Share Trend
        plot_market_share_trends(share_df, year_cols, "outputs/market_share_trends.png")
        
        # 상위 지역 EV 비중
        if len(top_regions) > 0:
            plot_top_regions_ev_share(top_regions, save_path="outputs/top_regions_ev_share.png")
        
        # Pace of Transition 비교
        if regional_results:
            plot_transition_speed_comparison(regional_results, save_path="outputs/transition_speed.png")
        
        # 종합 대시보드
        create_summary_dashboard(share_df, year_cols, top_regions, transition, 
                               "outputs/summary_dashboard.png")
        
        # 11. 결과 요약
        logger.info("11단계: 결과 요약")
        print("\n" + "="*60)
        print("📊 Automotive Powertrain Production Trend 결과")
        print("="*60)
        
        print(f"\n📈 Pace of Transition 분석 ({transition['start_year']} → {transition['end_year']})")
        print(f"   • 시작 EV 비중: {transition['start_ev_share']:.1f}%")
        print(f"   • 종료 EV 비중: {transition['end_ev_share']:.1f}%")
        print(f"   • 변화량: {transition['share_change']:.1f}%p")
        print(f"   • 생산량 변화: {transition['production_change']/1e6:.1f}M 대")
        
        if len(top_regions) > 0:
            print(f"\n🏆 2030년 EV 비중 상위 지역")
            for i, (_, row) in enumerate(top_regions.head(5).iterrows(), 1):
                print(f"   {i}. {row['region']}: {row['ev_share']:.1f}%")
        
        print(f"\n📁 생성된 파일:")
        print(f"   • outputs/production_trends.png")
        print(f"   • outputs/market_share_trends.png")
        print(f"   • outputs/top_regions_ev_share.png")
        print(f"   • outputs/transition_speed.png")
        print(f"   • outputs/summary_dashboard.png")
        
        # 실행 시간 계산
        end_time = datetime.now()
        execution_time = end_time - start_time
        logger.info(f"분석 완료! 실행 시간: {execution_time}")
        
        return {
            'success': True,
            'execution_time': execution_time,
            'data_shape': info['shape'],
            'year_range': f"{year_cols[0]}~{year_cols[-1]}",
            'powertrain_distribution': distribution,
            'transition_analysis': transition,
            'top_regions_count': len(top_regions)
        }
        
    except Exception as e:
        logger.error(f"분석 중 오류 발생: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """메인 실행 함수"""
    print("🚗 Automotive Powertrain Production Trend")
    print("="*50)
    
    result = run_full_analysis()
    
    if result['success']:
        print(f"\n✅ 분석이 성공적으로 완료되었습니다!")
        print(f"⏱️  실행 시간: {result['execution_time']}")
    else:
        print(f"\n❌ 분석 중 오류가 발생했습니다: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main() 