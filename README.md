# 🚗 Automotive Powertrain Production Trend Analysis

> **Automotive Powertrain Transition Trend Analysis System Using S&P Global Light Vehicle Forecast Data**
>>>>>>> 

A comprehensive analytics platform that examines the production trends and market share dynamics of Electric Vehicles (EV), Hybrid Electric Vehicles (HEV), and Internal Combustion Engine (ICE) vehicles. The system is built on global light vehicle production data from 2000 to 2037 provided by S&P Global, enabling in-depth analysis of the ongoing powertrain transition in the automotive industry.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 프로젝트 개요

- **목표**: 자동차 Powertrain 전환 트렌드 분석 및 시각화
- **데이터**: S&P Global Light Vehicle Forecast Excel 데이터
- **기간**: 2000년 ~ 2037년 (38년간)
- **분석 대상**: EV, HEV, ICE Powertrain
- **주요 기능**: Prod. Volume Trend, Market Share Trend, Region별 비교, Pace of Transition 분석
- **플랫폼**: Streamlit 기반 인터랙티브 대시보드 + matplotlib 정적 시각화

## 🎯 주요 분석 결과

### 글로벌 Powertrain 전환 트렌드
- **2023년**: EV 11.71% (10.6M 대), ICE 88.29% (79.9M 대)
- **2037년**: EV 46.7% (47.1M 대), ICE 53.3% (53.8M 대)
- **Pace of Transition**: 15년간 EV Portion 35%p 증가

### Region별 특성
- **Greater China**: EV Pace of Transition 최고
- **Europe**: 정책 기반 빠른 전환
- **Americas**: 점진적 전환
- **Asia Pacific**: 시장 다양성

## 🏗️ 프로젝트 구조

```
snP_trend_analysis/
├── data/                             # S&P Original 데이터
│   └── 20250701_LV_Prod_Extended_Pivot.xlsb
├── src/                              # 분석 코드 모듈
│   ├── load_data.py                  # 데이터 로딩 및 전처리
│   ├── classify_powertrain.py        # Powertrain 분류
│   ├── aggregate_production.py       # Prod. Vol. 집계 및 Market Share 계산
│   └── visualize_trends.py           # 시각화 기능
├── outputs/                          # 분석 결과물
│   ├── production_trends.png         # Prod. Volume Trend 그래프
│   ├── market_share_trends.png       # Market Share Trend 그래프
│   ├── top_regions_ev_share.png      # Top Region EV Portion
│   ├── transition_speed.png          # Pace of Transition 비교
│   └── summary_dashboard.png         # 종합 대시보드
├── streamlit_app.py                  # Streamlit 대시보드 앱
├── run_dashboard.py                  # 대시보드 실행 스크립트
├── main.py                           # 메인 실행 파일
├── requirements.txt                  # Python 패키지 의존성
└── README.md                         # 프로젝트 설명서
```

## 🛠️ 설치 및 실행

### 1. 환경 설정

```bash
# 저장소 클론
git clone https://github.com/your-username/automotive-powertrain-analysis.git
cd automotive-powertrain-analysis

# Python 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터 준비

S&P Global Light Vehicle Forecast 데이터 파일을 `data/` 디렉토리에 배치하세요:
```
data/
└── 20250701_LV_Prod_Extended_Pivot.xlsb
```

### 3. 분석 실행

```bash
# 전체 분석 파이프라인 실행 (정적 이미지 생성)
python main.py

# Streamlit 대시보드 실행
python run_dashboard.py
# 또는
streamlit run streamlit_app.py
```

### 4. 웹 대시보드 접속

브라우저에서 `http://localhost:8501`로 접속하여 인터랙티브 대시보드를 확인하세요.

### 3. 개별 모듈 테스트

```bash
# 데이터 로딩 테스트
cd src
python load_data.py

# Powertrain 분류 테스트
python classify_powertrain.py

# Prod. Vol. 집계 테스트
python aggregate_production.py

# 시각화 테스트
python visualize_trends.py
```

## 📊 분석 기능

### 1. 데이터 처리 (F-01 ~ F-05)
- **F-01**: S&P Excel 파일 로딩
- **F-02**: Year별 Prod. Vol. 컬럼 정리 (2023~2037)
- **F-03**: Powertrain 분류 (EV/HEV/ICE)
- **F-04**: Year별 Prod. Vol. 집계
- **F-05**: Market Share 계산

### 2. 시각화 (F-06 ~ F-09)
- **F-06**: Powertrain별 Prod. Volume Trend (선 그래프)
- **F-07**: Market Share Trend (스택 영역 차트)
- **F-08**: 2030년 EV Portion Top Region (바 차트)
- **F-09**: Region별 Pace of Transition 비교

### 3. 출력 (F-10 ~ F-12)
- **F-10**: 분석 리포트 생성
- **F-11**: 그래프 이미지 저장
- **F-12**: Streamlit 대시보드 (구현 완료)

## 🌐 Streamlit 대시보드

### 주요 기능
- **📈 Prod. Volume Trend**: Powertrain Volume Trend by Year 시각화
- **📊 Market Share Trend**: Powertrain별 Market Share Trend 스택 차트
- **🌍 Analysis by Region**: EV% Heatmap by Regions 및 막대 차트
- **⚡ Pace of Transition**: 2023→EV % in 2037 변화량 분석
- **📋 Data Details**: Powertrain Distribution 및 Original Data Sample

### 인터랙티브 기능
- Year 선택 (다중 선택 가능)
- Region 선택 (다중 선택 가능)
- Select Powertrain Type (EV/HEV/ICE)
- 실시간 데이터 필터링
- Plotly 기반 인터랙티브 차트

## 🔍 Powertrain 분류 기준

| Powertrain | 분류 조건 |
|-----------|----------|
| **EV (전기차)** | `Fuel Type` == "BEV" 또는 `Powertrain Main Category`에 "Battery Electric" 포함 |
| **HEV (하이브리드)** | `Powertrain Main Category`에 "Hybrid", "PHEV", "Mild Hybrid" 포함 |
| **ICE (내연기관)** | `Fuel Type`이 "Gasoline", "Diesel", "CNG" 등이며 EV/HEV가 아닌 경우 |

## 📈 주요 분석 결과

### 1. Pace of Transition 분석
- 2023년 → EV % in 2037 변화량
- Region별 Pace of Transition 비교
- Prod. Vol. Change 추이

### 2. Analysis by Region
- 2030년 기준 EV Portion Top Region
- Region별 Powertrain 선호도
- Pace of Transition 차이 분석

### 3. 시장 전략 인사이트
- 글로벌 Powertrain 전환 트렌드
- Region별 시장 특성
- 미래 생산 계획 수립 지원

## 🎯 활용 방안

### 1. 대학원 포트폴리오
- 데이터 분석 및 시각화 역량 증명
- 자동차 산업 이해도 표현
- Python 프로그래밍 능력 어필

### 2. 업계 실무 활용
- 시장 분석 및 전략 수립
- 경쟁사 분석 지원
- 투자 의사결정 자료

### 3. 연구 및 교육
- 자동차 산업 트렌드 연구
- 데이터 분석 교육 자료
- 시각화 기법 학습

## 🔧 기술 스택

- **Python**: 3.8+
- **데이터 처리**: pandas, numpy
- **시각화**: matplotlib, seaborn
- **대시보드**: streamlit (선택)
- **데이터 소스**: S&P Global Light Vehicle Forecast

## 🚀 주요 기능

### 📊 인터랙티브 대시보드
- **실시간 필터링**: Year, Region, Select Powertrain Type
- **동적 차트**: Plotly 기반 인터랙티브 시각화
- **메트릭 카드**: 핵심 지표 한눈에 확인
- **데이터 테이블**: Data Details 탐색

### 📈 정적 시각화
- **고품질 차트**: matplotlib + seaborn 기반
- **종합 대시보드**: 모든 분석 결과 통합
- **출력 최적화**: 리포트 및 프레젠테이션용

### 🔍 분석 모듈
- **자동 분류**: Powertrain 타입 자동 식별
- **Pace of Transition**: EV 전환 트렌드 정량 분석
- **Region별 비교**: 시장 특성 및 선호도 분석

## 🛡️ 문제 해결

### 자주 발생하는 문제들

#### 1. 파일 로딩 오류
```bash
# 오류: No such file or directory
# 해결: 데이터 파일 경로 확인
ls -la data/20250701_LV_Prod_Extended_Pivot.xlsb
```

#### 2. 패키지 설치 오류
```bash
# pyxlsb 설치 문제
pip install --upgrade pip
pip install pyxlsb
```

#### 3. Streamlit 실행 오류
```bash
# 포트 충돌 시
streamlit run streamlit_app.py --server.port 8502
```

## 📝 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.



