
# 🚇 UrbanMobility Transit Analytics

## Project Overview
UrbanMobility Transit Analytics is a data analytics project focused on understanding public transport ridership, route performance, and journey delays. The project uses Python for data preparation and analysis and Power BI for interactive visualization.

## 🎯 Objectives
- Analyze passenger ridership trends.
- Identify high-demand bus routes.
- Examine journey delays and delay patterns.
- Compare route performance across different hours.
- Provide data-driven recommendations for transport planning.

## 🛠️ Tools and Technologies
- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- NetworkX
- Power BI
- CSV datasets
- Jupyter Notebook

## 📂 Project Structure
```text
UrbanMobility-Transit-Analytics/
├── data/
│   ├── da_bus_routes.csv
│   ├── da_journey_times.csv
│   └── da_ridership_data.csv
├── outputs/
│   ├── cleaned_da_bus_routes.csv
│   ├── cleaned_da_journey_times.csv
│   ├── cleaned_da_ridership_data.csv
│   ├── delay_heatmap.png
|   |--recomendation.route.py
│   └── route_network.png
├── data_cleaning.py
├── eda.py
├── route_analysis.py
└── cynaris project 1.pbix
```

## 📊 Analysis Performed
- Data cleaning and preparation
- Exploratory data analysis (EDA)
- Ridership trend analysis
- Route and journey-time analysis
- Delay pattern visualization
- Route network analysis
- Power BI dashboard development

## 💡 Recommendations
1. Increase bus frequency during peak-demand hours.
2. Investigate recurring delays on congested routes.
3. Improve schedules using hourly ridership patterns.
4. Monitor route performance regularly using refreshed data.

## 📈 Dashboard
The Power BI dashboard is designed to present key performance indicators, ridership trends, delay analysis, high-demand routes, and route-hour performance.

To view the dashboard, download the `.pbix` file from this repository and open it using Power BI Desktop.

## ▶️ How to Run
1. Clone or download this repository.
2. Install Python and the required libraries.
3. Place the datasets in the `data/` folder.
4. Run the Python analysis scripts.
5. Open the Power BI `.pbix` file in Power BI Desktop.

Install common libraries with:

```bash
pip install pandas numpy matplotlib seaborn networkx
```

## 👨‍💻 Project Information
- **Project:** UrbanMobility Transit Analytics
- **Role:** Data Analyst Intern
- **Domain:** Public Transport Analytics
- **Location:** Bengaluru, India

## ⚠️ Note
This project supports transport planning through data analysis. Recommendations should be validated against actual operational conditions before implementation.
