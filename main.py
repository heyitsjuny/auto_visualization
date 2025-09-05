"""
Automotive Powertrain Production Trend Main Exe. File
Execute entire analysis pipeline and create result.
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
    """Executing entire analysis pipeline."""
    
    start_time = datetime.now()
    logger.info("=== Automotive Powertrain Production Trend Start ===")
    
    try:
        # 1. 데이터 로딩
        logger.info("Step 1: Loading Data")
        file_path = "data/20250701_LV_Prod_Extended_Pivot.xlsb"
        df = load_excel_data(file_path)
        
        # 데이터 정보 출력
        info = get_data_info(df)
        logger.info(f"Data Size: {info['shape']}")
        logger.info(f"No. of Columns: {len(info['columns'])}")
        
        # 2. Year 컬럼 추출
        logger.info("Step 2: Extracting Year Column")
        df, year_cols = extract_year_columns(df)
        logger.info(f"Analysis Year: {year_cols[0]} ~ {year_cols[-1]} ({len(year_cols)}년)")
        
        # 3. Powertrain 분류
        logger.info("Step 3: Powertrain Classification")
        df = classify_powertrain(df)
        
        # Classification Result 확인
        distribution = get_powertrain_distribution(df)
        logger.info(f"Powertrain Distribution: {distribution}")
        
        # 분류 검증
        validation = validate_powertrain_classification(df)
        logger.info(f"Validation Complete: EV {len(validation['ev_samples'])}, HEV {len(validation['hev_samples'])}개, ICE {len(validation['ice_samples'])}개")
        
        # 4. Prod. Vol. 집계
        logger.info("Step 4: Aggregate Prod. Vol.")
        agg_df = aggregate_production_by_year(df, year_cols)
        logger.info(f"Aggregation Complete: {agg_df.shape}")
        
        # 5. Market Share 계산
        logger.info("Step 5: Market Share Calculation")
        share_df = calculate_market_share(agg_df, year_cols)
        logger.info("Market Share Calculation Complete")
        
        # 6. Pace of Transition 분석
        logger.info("Step 6: Pace of Transition Analysis")
        transition = get_transition_analysis(share_df, year_cols)
        logger.info(f"Pace of Transition: {transition['share_change']:.2f}%p ({transition['start_year']}→{transition['end_year']})")
        
        # 7. Analysis by Region
        logger.info("Step 7: Analysis by Region")
        regional_results = get_regional_analysis(df, year_cols)
        logger.info(f"Analysis by Region Complete: {len(regional_results)}개 Region")
        
        # 8. Top Region 선정
        logger.info("Step 8: Top Region Selection")
        top_regions = get_top_regions_by_ev_share(regional_results)
        logger.info(f"Top Region Selection Complete: {len(top_regions)}개 Region")
        
        # 9. 출력 디렉토리 생성
        logger.info("Step 9: Output Directory Creation")
        os.makedirs("outputs", exist_ok=True)
        
        # 10. 시각화 생성
        logger.info("Step 10: Visualization Creation")
        
        # Prod. Volume Trend
        plot_production_trends(agg_df, year_cols, "outputs/production_trends.png")
        
        # Market Share Trend
        plot_market_share_trends(share_df, year_cols, "outputs/market_share_trends.png")
        
        # Top Region EV Portion
        if len(top_regions) > 0:
            plot_top_regions_ev_share(top_regions, save_path="outputs/top_regions_ev_share.png")
        
        # Pace of Transition 비교
        if regional_results:
            plot_transition_speed_comparison(regional_results, save_path="outputs/transition_speed.png")
        
        # 종합 대시보드
        create_summary_dashboard(share_df, year_cols, top_regions, transition, 
                               "outputs/summary_dashboard.png")
        
        # 11. 결과 요약
        logger.info("11단계: Summary")
        print("\n" + "="*60)
        print("📊 Automotive Powertrain Production Trend Summary")
        print("="*60)
        
        print(f"\n📈 Pace of Transition Analysis ({transition['start_year']} → {transition['end_year']})")
        print(f"   • Start EV Portion: {transition['start_ev_share']:.1f}%")
        print(f"   • End EV Portion: {transition['end_ev_share']:.1f}%")
        print(f"   • Change : {transition['share_change']:.1f}%p")
        print(f"   • Prod. Vol. Change: {transition['production_change']/1e6:.1f}M ")
        
        if len(top_regions) > 0:
            print(f"\n🏆 2030 EV Portion Top Region")
            for i, (_, row) in enumerate(top_regions.head(5).iterrows(), 1):
                print(f"   {i}. {row['region']}: {row['ev_share']:.1f}%")
        
        print(f"\n📁 files created:")
        print(f"   • outputs/production_trends.png")
        print(f"   • outputs/market_share_trends.png")
        print(f"   • outputs/top_regions_ev_share.png")
        print(f"   • outputs/transition_speed.png")
        print(f"   • outputs/summary_dashboard.png")
        
        # 실행 시간 계산
        end_time = datetime.now()
        execution_time = end_time - start_time
        logger.info(f"Analysis Complete! Execution time: {execution_time}")
        
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
        logger.error(f"Error has occurred during analysis: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """Main Function Execution"""
    print("🚗 Automotive Powertrain Production Trend")
    print("="*50)
    
    result = run_full_analysis()
    
    if result['success']:
        print(f"\n✅ Analysis Successfully Complete!")
        print(f"⏱️  Execution Time: {result['execution_time']}")
    else:
        print(f"\n❌ Error has Occurred during Analysis: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main() 