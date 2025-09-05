# Automotive Powertrain Production Trend Analysis

> **Automotive Powertrain Trend Analysis System using S&P Global Light Vehicle Forecast**

A comprehensive analytics platform that analyzes the production trends and market share shifts of Electric Vehicles (EV), Hybrid Electric Vehicles (HEV), and Internal Combustion Engine (ICE) vehicles, based on global automotive production data from 2000 to 2037

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Project Overview

- **Objective**: Analysis and Visualization of Automotive Powertrain Transition Trends
- **Data**: S&P Global Light Vehicle Forecast Excel Data
- **Period**: 2000 ~ 2037 (38yrs)
- **Analysis Range**: EV, HEV, ICE Powertrain
- **Main Function**: Production volume trend, Market share change, Comparison by Region, Trend shifting speed
- **Platform**: Streamlit based interactive dashboard + matplotlib Visualization


## Project Structure

```
snP_trend_analysis/
├── data/                             # S&P Original Data
│   └── 20250701_LV_Prod_Extended_Pivot.xlsb
├── src/                              # Analysis Code Module
│   ├── load_data.py                  # Data Loading, pre-process
│   ├── classify_powertrain.py        # Powertrain Classification
│   ├── aggregate_production.py       # Aggregation of prod. & share calc.
│   └── visualize_trends.py           # Visualization Function
├── outputs/                          # Analyze Output
│   ├── production_trends.png         # Prod. Vol. Trend Graph
│   ├── market_share_trends.png       # Market Share Trend Graph
│   ├── top_regions_ev_share.png      # EV Share on TOP regions
│   ├── transition_speed.png          # Transition Speed Comparison
│   └── summary_dashboard.png         # Summary Dashboard
├── streamlit_app.py                  # Streamlit Dashboard App
├── run_dashboard.py                  # Run Script for Dashboard
├── main.py                           # Main exe. file
├── requirements.txt                  # Python package dependancy
└── README.md                         # Project Description
```

## Installation and Open

### 1. Settings

```bash
# Clone the repository
git clone https://github.com/your-username/automotive-powertrain-analysis.git
cd automotive-powertrain-analysis

# Create Python virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Data Preparation

Place S&P Global Light Vehicle Forecast data file in  `data/`directory:
```
data/
└── 20250701_LV_Prod_Extended_Pivot.xlsb
```

### 3. Perform Analysis

```bash
# Run the entire analysis pipeline (generate static images)
python main.py

# Run Streamlit dashboard
python run_dashboard.py
# or
streamlit run streamlit_app.py
```

### 4. Access to Web Dashboard

Open interactive dashboard by accessing  `http://localhost:8501`in your browser.

### 3. Individual Module Test

```bash
# Test data loading
cd src
python load_data.py

# Test powertrain classification
python classify_powertrain.py

# Test production volume aggregation
python aggregate_production.py

# Test visualization
python visualize_trends.py
```

## Analysis Function

### 1. Data Function (F-01 ~ F-05)
- **F-01**: Load S&P Excel File
- **F-02**: Regional Prod. Vol. by Column (2023~2037)
- **F-03**: Powertrain Classification (EV/HEV/ICE)
- **F-04**: Prod. vol. by year summary
- **F-05**: Market Share Calculation

### 2. Visualization (F-06 ~ F-09)
- **F-06**: Prod. Vol. Trend by Powertrain (Line Graph)
- **F-07**: Market Share Change (Stack Range Chart)
- **F-08**: 2030 EV Portion in TOP regions (Bar Chart)
- **F-09**: Regional Transition Speed Comparison

### 3. Output (F-10 ~ F-12)
- **F-10**: Analysis Report Creation
- **F-11**: Save Graph Image
- **F-12**: Streamlit Dashboard

## Streamlit Dashboard

### Main Features
- **Production Volume Trend**:Yearly powertrain production volume visualization
- **Market Share Trend**: Stacked chart of powertrain market share
- **Analysis by Region**: EV% heatmap and bar chart by region
- **Pace of Transition**: Change in EV% from 2023 → 2037
- **Data Details**: Powertrain distribution and original data sample

### Interactive Features
- Multi-year selection
- Multi-region selection
- Powertrain type selection (EV/HEV/ICE)
- Real-time data filtering
- Interactive charts using Plotly

## Powertrain Classification Criteria

| Powertrain | Classification Criteria |
|-----------|----------|
| **EV** | `Fuel Type` == "BEV" or `Powertrain Main Category`contains "Battery Electric" |
| **HEV** | `Powertrain Main Category` contains "Hybrid", "PHEV", "Mild Hybrid" |
| **ICE** | `Fuel Type`"Gasoline", "Diesel", "CNG",etc. and not classified as EV/HEV |

## Key Analysis Results

### 1. Pace of Transition
- Change in EV % from 2023 to 2037
- Regional comparison of pace of transition
- Production volume change trend

### 2. Analysis by Region
- EV portion top regions in 2030
- Regional powertrain preferences
- Comparative pace of transition analysis

### 3. Strategic Market Insights
- Global powertrain transition trends
- Regional market characteristics
- Support for future production planning

## Applications

### 1. Personal Portfolio
- Demonstrate data analysis & visualization skills
- Showcase understanding of the automotive industry
- Highlight Python programming capability

### 2. Industry Use
- Market analysis & strategy development
- Competitive analysis support
- Input for investment decision-making

### 3. Research & Education
- Automotive industry trend research
- Data analysis teaching material
- Visualization technique learning

## Tech Stack

- **Python**: 3.8+
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Dashboard**: streamlit (Optional)
- **Data Source**: S&P Global Light Vehicle Forecast

## Core Features

### Interactive Dashboard
- **Real-time Filtering**: Year, region, powertrain type
- **Dynamic Charts**: Interactive visualization with Plotly
- **Metric Cards**: Key indicators at a glance
- **Data Tables**: Explore detailed datasets

### Static Visualization
- **High-quality charts**: matplotlib + seaborn based
- **Comprehensive Dashboard**: Integrated analysis results
- **Optimized Output**: For reports and presentations

### Analysis Modules
- **Automatic classification**: Identify powertrain types
- **Pace of Transition**: Quantitative EV transition analysis
- **Regional comparison**: Market characteristics & preferences

## Troubleshooting

### Common Issues

#### 1. File Loading Error
```bash
# Error: No such file or directory
# Solution: Check data file path
ls -la data/20250701_LV_Prod_Extended_Pivot.xlsb
```

#### 2. Package Installation Error
```bash
# pyxlsb installation issue
pip install --upgrade pip
pip install pyxlsb
```

#### 3. Streamlit Execution Error
```bash
# If port conflict occurs
streamlit run streamlit_app.py --server.port 8502
```

## License

___This project is intended for educational and research purposes.___
