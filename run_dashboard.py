#!/usr/bin/env python3
"""
Streamlit 대시보드 실행 스크립트
"""

import subprocess
import sys
import os

def main():
    """Streamlit 대시보드를 실행합니다."""
    
    print("🚗 Automotive Powertrain Production Trend")
    print("=" * 50)
    
    # 현재 디렉토리 확인
    current_dir = os.getcwd()
    print(f"현재 디렉토리: {current_dir}")
    
    # 필요한 파일들 확인
    required_files = [
        "streamlit_app.py",
        "data/20250701_LV_Prod_Extended_Pivot.xlsb",
        "src/load_data.py",
        "src/classify_powertrain.py",
        "src/aggregate_production.py",
        "src/visualize_trends.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 다음 파일들이 없습니다:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n프로젝트 구조를 확인해주세요.")
        return
    
    print("✅ 모든 필요한 파일이 확인되었습니다.")
    
    # Streamlit 실행
    try:
        print("\n🌐 Streamlit 대시보드를 Start합니다...")
        print("브라우저에서 http://localhost:8501 을 열어주세요.")
        print("대시보드를 End하려면 Ctrl+C를 누르세요.")
        print("-" * 50)
        
        # Streamlit 실행
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
        
    except KeyboardInterrupt:
        print("\n\n👋 대시보드가 End되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {e}")
        print("Streamlit이 설치되어 있는지 확인해주세요:")
        print("pip install streamlit")

if __name__ == "__main__":
    main() 