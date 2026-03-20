# Textile Performance Analytics

A comprehensive data analytics and visualization project designed to evaluate the financial performance, operational efficiency, and sales trends of a textile manufacturing company.

This repository contains both exploratory data analysis (EDA) using Jupyter Notebooks for static reporting, as well as a dynamic, interactive Streamlit dashboard for real-time data manipulation.


## 📊 Dashboard Preview
![Overview](https://github.com/user-attachments/assets/063b15be-3bbd-444d-a6d2-c9e36e2dd7e9)
![Overview 2](https://github.com/user-attachments/assets/0183f744-912d-4778-bd2c-2f6a0152c1e6)
![Analytics Dashboard](https://github.com/user-attachments/assets/39a3a6f3-18a9-4c6e-ba55-626a153d64c8)
![Operation Dashboard](https://github.com/user-attachments/assets/b4e02a1d-0e60-4767-aceb-e845639f1623)


## 🚀 Key Features
### Interactive Streamlit Dashboard (app.py):

-Dynamic filtering capabilities by Year and Product Name.

-Custom slider for Minimum Sales to filter high/low-performing records.

-Real-time calculation of derived metrics: Net Profit, Profit Margin (%), and Profit per Worker.

-Interactive visualizations using Plotly Express (e.g., Boxplots for Worker Efficiency).



### Static Exploratory Data Analysis (textile_python_project.ipynb):

-Robust data wrangling, missing value checks, and data type casting.

-Calculation of core business metrics including Net Profit (Profit - Loss) and Profit Margins.

-Insightful static visualizations, including:

-Average Total Sale by Product (Bar Chart)

-Net Profit Trends by Year (Bar Chart)

-Profit Margin Distributions (Boxplot)



### Performance Insights:

-Identifies top-performing product lines (e.g., Shirts and Kurtas dominate volume).

-Evaluates year-over-year revenue generation and operational bottlenecks.



## 📁 Repository Structure
app.py : The main entry point for the Streamlit web application. Contains the front-end layout, caching logic for data loading, dynamic filters, and Plotly-based interactive components.

textile_python_project.ipynb : The Jupyter Notebook containing the initial data exploration, statistical summaries, and static graph generation using Plotly and Pandas.

textile_company_data_10000.csv : The raw dataset consisting of 10,000 records. Key features include Year, Product Name, Profit, Loss, Total Sale, Total Manufacturing, Total No of Workers, Salary, and Raw Material/Production Costs.



## ⚙️ Installation & Setup
To run this project locally, ensure you have Python 3.8+ installed, then follow these steps:

### Clone the repository:

-git clone https://github.com/Keerti-Subramanya/Textile-Performance-Analysis.git
-cd textile-analytics

### Install the required dependencies:
-pip install pandas numpy streamlit plotly jupyter

### Run the Jupyter Notebook (for static analysis):
-jupyter notebook textile_python_project.ipynb

### Launch the Streamlit Dashboard:
-streamlit run app.py


## 🛠️ Tech Stack
Language: Python 3.x

Data Manipulation: Pandas, NumPy, SciPy

Data Visualization: Plotly (Express & Graph Objects), Matplotlib, Seaborn

Web Framework: Streamlit
