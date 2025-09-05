# 🚗 Automotive Powertrain Production Trend Analysis

<<<<<<< HEAD
> **S&P Global Light Vehicle Forecast 데이터를 활용한 자동차 Powertrain 전환 트렌드 분석 시스템**
=======
> **Automotive Powertrain Transition Trend Analysis System Using S&P Global Light Vehicle Forecast Data**
>>>>>>> 935bb8f728bc7070b84bdd2f32007875d96bd175

A comprehensive analytics platform that examines the production trends and market share dynamics of Electric Vehicles (EV), Hybrid Electric Vehicles (HEV), and Internal Combustion Engine (ICE) vehicles. The system is built on global light vehicle production data from 2000 to 2037 provided by S&P Global, enabling in-depth analysis of the ongoing powertrain transition in the automotive industry.

📋 Project Overview

Goal: Analyze and visualize automotive powertrain transition trends

Data: S&P Global Light Vehicle Forecast Excel data

Period: 2000–2037 (38 years)

Scope of Analysis: EV, HEV, ICE powertrains

Key Features: Production Volume Trend, Market Share Trend, Regional Comparison, Pace of Transition analysis

Platform: Streamlit-based interactive dashboard + static visualization using matplotlib

🎯 Key Findings
Global Powertrain Transition Trend

2023: EV 11.71% (10.6M units), ICE 88.29% (79.9M units)

2037: EV 46.7% (47.1M units), ICE 53.3% (53.8M units)

Pace of Transition: EV share increases by 35 percentage points over 15 years

Regional Characteristics

Greater China: Highest pace of EV transition

Europe: Policy-driven rapid transition

Americas: Gradual transition

Asia Pacific: Market diversity

🏗️ Project Structure
snP_trend_analysis/
├── data/                             # Original S&P data
│   └── 20250701_LV_Prod_Extended_Pivot.xlsb
├── src/                              # Analysis code modules
│   ├── load_data.py                  # Data loading and preprocessing
│   ├── classify_powertrain.py        # Powertrain classification
│   ├── aggregate_production.py       # Production volume aggregation & market share calculation
│   └── visualize_trends.py           # Visualization functions
├── outputs/                          # Analysis outputs
│   ├── production_trends.png         # Production Volume Trend graph
│   ├── market_share_trends.png       # Market Share Trend graph
│   ├── top_regions_ev_share.png      # Top Region EV Portion
│   ├── transition_speed.png          # Pace of Transition comparison
│   └── summary_dashboard.png         # Summary dashboard
├── streamlit_app.py                  # Streamlit dashboard app
├── run_dashboard.py                  # Dashboard execution script
├── main.py                           # Main execution file
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation

🛠️ Installation & Execution
1. Environment Setup
# Clone the repository
git clone https://github.com/your-username/automotive-powertrain-analysis.git
cd automotive-powertrain-analysis

# Create Python virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

2. Data Preparation

Place the S&P Global Light Vehicle Forecast data file in the data/ directory:

data/
└── 20250701_LV_Prod_Extended_Pivot.xlsb

3. Run Analysis
# Run the entire analysis pipeline (generate static images)
python main.py

# Run Streamlit dashboard
python run_dashboard.py
# or
streamlit run streamlit_app.py

4. Access Web Dashboard

Open a browser and go to http://localhost:8501 to access the interactive dashboard.

5. Test Individual Modules
# Test data loading
cd src
python load_data.py

# Test powertrain classification
python classify_powertrain.py

# Test production volume aggregation
python aggregate_production.py

# Test visualization
python visualize_trends.py

📊 Analysis Functions
1. Data Processing (F-01 ~ F-05)

F-01: Load S&P Excel file

F-02: Organize yearly production volume columns (2023–2037)

F-03: Classify powertrains (EV/HEV/ICE)

F-04: Aggregate yearly production volumes

F-05: Calculate market share

2. Visualization (F-06 ~ F-09)

F-06: Powertrain Production Volume Trend (line graph)

F-07: Market Share Trend (stacked area chart)

F-08: 2030 EV Portion Top Regions (bar chart)

F-09: Regional Pace of Transition comparison

3. Output (F-10 ~ F-12)

F-10: Generate analysis report

F-11: Save graphs as images

F-12: Streamlit dashboard (implemented)

🌐 Streamlit Dashboard
Main Features

📈 Production Volume Trend: Yearly powertrain production volume visualization

📊 Market Share Trend: Stacked chart of powertrain market share

🌍 Analysis by Region: EV% heatmap and bar chart by region

⚡ Pace of Transition: Change in EV% from 2023 → 2037

📋 Data Details: Powertrain distribution and original data sample

Interactive Features

Multi-year selection

Multi-region selection

Powertrain type selection (EV/HEV/ICE)

Real-time data filtering

Interactive charts using Plotly

🔍 Powertrain Classification Criteria
Powertrain	Classification Criteria
EV (Electric Vehicle)	Fuel Type == "BEV" or Powertrain Main Category contains "Battery Electric"
HEV (Hybrid)	Powertrain Main Category contains "Hybrid", "PHEV", "Mild Hybrid"
ICE (Internal Combustion Engine)	Fuel Type is "Gasoline", "Diesel", "CNG", etc. and not classified as EV/HEV
📈 Key Analysis Results
1. Pace of Transition

Change in EV % from 2023 to 2037

Regional comparison of pace of transition

Production volume change trend

2. Analysis by Region

EV portion top regions in 2030

Regional powertrain preferences

Comparative pace of transition analysis

3. Strategic Market Insights

Global powertrain transition trends

Regional market characteristics

Support for future production planning

🎯 Applications
1. Graduate School Portfolio

Demonstrates data analysis & visualization skills

Showcases understanding of the automotive industry

Highlights Python programming capability

2. Industry Use

Market analysis & strategy development

Competitive analysis support

Input for investment decision-making

3. Research & Education

Automotive industry trend research

Data analysis teaching material

Visualization technique learning

🔧 Tech Stack

Python: 3.8+

Data Processing: pandas, numpy

Visualization: matplotlib, seaborn

Dashboard: streamlit

Data Source: S&P Global Light Vehicle Forecast

🚀 Core Features
📊 Interactive Dashboard

Real-time filtering: Year, Region, Powertrain type

Dynamic charts: Interactive visualization with Plotly

Metric cards: Key indicators at a glance

Data tables: Explore detailed datasets

📈 Static Visualization

High-quality charts: matplotlib + seaborn based

Comprehensive dashboard: Integrated analysis results

Optimized outputs: For reports and presentations

🔍 Analysis Modules

Automatic classification: Identify powertrain types

Pace of Transition: Quantitative EV transition analysis

Regional comparison: Market characteristics & preferences

🛡️ Troubleshooting
Common Issues
1. File Loading Error
# Error: No such file or directory
# Solution: Check data file path
ls -la data/20250701_LV_Prod_Extended_Pivot.xlsb

2. Package Installation Error
# pyxlsb installation issue
pip install --upgrade pip
pip install pyxlsb

3. Streamlit Execution Error
# If port conflict occurs
streamlit run streamlit_app.py --server.port 8502

📝 License

This project is intended for educational and research purposes.

