import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Textile Analytics - Full Filters", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("textile_company_data_10000.csv")
    
    # Clean data
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
    numeric_cols = [
        'Profit', 'Loss', 'Total Sale', 'Total Manufacturing', 'Remaining Products',
        'Total No of Workers', 'Salary of Workers', 'Raw Material Cost', 'Production Cost'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Derived metrics
    df['Net Profit'] = df.get('Profit', 0) - df.get('Loss', 0)
    df['Profit Margin'] = (df['Net Profit'] / df['Total Sale'].replace(0, np.nan)) * 100
    df['Profit Margin'] = df['Profit Margin'].fillna(0)
    df['Profit per Worker'] = df['Net Profit'] / df['Total No of Workers'].replace(0, 1)
    
    return df

df = load_data()

# Main title
st.title("Textile Performance Analytics Dashboard")

# ========================================
# FULL SEPARATE FILTERS (no heading)
# ========================================

# Row 1: Dropdowns
filter_row1 = st.columns(4)

with filter_row1[0]:
    year_options = ["All"] + sorted(df['Year'].unique().tolist())
    selected_year = st.selectbox("📅 Year:", year_options)

with filter_row1[1]:
    product_options = ["All"] + sorted(df['Product Name'].unique().tolist())
    selected_product = st.selectbox("🧵 Product:", product_options)

with filter_row1[2]:
    min_sales = st.slider("💰 Min Sales:", 0, 200000, 0)

with filter_row1[3]:
    min_workers_dropdown = st.selectbox(
        "👥 Workers Range:",
        ["All", "100-150", "150-200", "200-250", "250+"]
    )

# Row 2: More filters
filter_row2 = st.columns(3)

with filter_row2[0]:
    sort_metric = st.selectbox("🏆 Top 10 Sort:", ['Net Profit', 'Total Sale', 'Profit Margin'])

with filter_row2[1]:
    min_profit = st.slider("💵 Min Profit:", 0, 100000, 0)

with filter_row2[2]:
    min_margin = st.slider("📈 Min Margin %:", -100.0, 50.0, -100.0)

st.markdown("---")

# ========================================
# Apply ALL filters with workers dropdown logic
# ========================================

# Start from full df then apply filters step by step
base_filter = df.copy()

# Year condition only if not "All"
if selected_year != "All":
    base_filter = base_filter[base_filter['Year'] == selected_year]

# Sales / profit / margin
base_filter = base_filter[
    (base_filter['Total Sale'] >= min_sales) &
    (base_filter['Net Profit'] >= min_profit) &
    (base_filter['Profit Margin'] >= min_margin)
].copy()

# Product condition only if not "All"
if selected_product != "All":
    base_filter = base_filter[base_filter['Product Name'] == selected_product]

# Workers dropdown filter
if min_workers_dropdown != "All":
    if min_workers_dropdown == "100-150":
        filtered_df = base_filter[
            (base_filter['Total No of Workers'] >= 100) &
            (base_filter['Total No of Workers'] <= 150)
        ]
    elif min_workers_dropdown == "150-200":
        filtered_df = base_filter[
            (base_filter['Total No of Workers'] >= 150) &
            (base_filter['Total No of Workers'] <= 200)
        ]
    elif min_workers_dropdown == "200-250":
        filtered_df = base_filter[
            (base_filter['Total No of Workers'] >= 200) &
            (base_filter['Total No of Workers'] <= 250)
        ]
    elif min_workers_dropdown == "250+":
        filtered_df = base_filter[base_filter['Total No of Workers'] >= 250]
else:
    filtered_df = base_filter

# ========================================
# TAB STRUCTURE
# ========================================
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔥 Advanced Analytics", "💰 Operations Dashboard"])

# ========================================
# TAB 1: OVERVIEW
# ========================================
with tab1:
    st.markdown("### 📊 Key Performance Indicators")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)
    kpi_col1.metric("Records", f"{len(filtered_df):,}")
    kpi_col2.metric("💰 Total Sales", f"${filtered_df['Total Sale'].sum():,.0f}")
    kpi_col3.metric("💵 Net Profit", f"${filtered_df['Net Profit'].sum():,.0f}")
    kpi_col4.metric("📈 Avg Margin", f"{filtered_df['Profit Margin'].mean():.1f}%")
    kpi_col5.metric("👥 Avg Workers", f"{filtered_df['Total No of Workers'].mean():.0f}")
    kpi_col6.metric("📅 Year", "All" if selected_year == "All" else selected_year)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sales_data = filtered_df.groupby('Product Name')['Total Sale'].mean().round(0).reset_index()
        fig1 = px.bar(
            sales_data, x='Product Name', y='Total Sale',
            title="Average Total Sale by Product",
            color='Total Sale', color_continuous_scale='Blues'
        )
        fig1.update_traces(texttemplate='%{y:,.0f}', textposition='auto')
        fig1.update_layout(height=400, showlegend=False, xaxis_tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        profit_data = filtered_df.groupby('Year')['Net Profit'].mean().round(0).reset_index()
        fig2 = px.bar(
            profit_data, x='Year', y='Net Profit',
            title="Average Net Profit by Year",
            color='Net Profit', color_continuous_scale='Blues'
        )
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    
    st.markdown("### 🏆 Top 10 Performers")
    if len(filtered_df) > 0:
        top_data = filtered_df.nlargest(10, sort_metric)[['Product Name', sort_metric]].copy()
        top_data.columns = ['Product Name', 'Metric Value']
        top_data['Metric Value'] = top_data['Metric Value'].round(0)
        
        fig_top = px.bar(
            top_data, x='Metric Value', y='Product Name', orientation='h',
            title=f"Top 10 by {sort_metric}",
            color='Metric Value', color_continuous_scale='Blues'
        )
        fig_top.update_traces(texttemplate='%{x:,.0f}', textposition='auto')
        fig_top.update_layout(height=400)
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.warning("No data matches current filters")

# ========================================
# TAB 2: ADVANCED ANALYTICS
# ========================================
with tab2:
    st.markdown("### 🔥 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Product × Year Heatmap")
        heatmap_data = filtered_df.groupby(['Product Name', 'Year'])['Net Profit'].mean().reset_index()
        if len(heatmap_data) > 0:
            fig_heatmap = px.density_heatmap(
                heatmap_data, x='Year', y='Product Name', z='Net Profit',
                title="Net Profit Heatmap",
                color_continuous_scale='RdYlGn'
            )
            fig_heatmap.update_layout(height=450)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.warning("No data for heatmap")
    
    with col2:
        st.markdown("#### Year-over-Year Growth")
        growth = filtered_df.groupby('Year').agg({
            'Total Sale': 'mean',
            'Net Profit': 'mean'
        }).round(0).reset_index()
        
        if len(growth) > 0:
            fig_growth = go.Figure()
            fig_growth.add_trace(go.Scatter(
                x=growth['Year'], y=growth['Total Sale'],
                mode='lines+markers', name='Avg Sales',
                line=dict(color='blue', width=4), marker=dict(size=10)
            ))
            fig_growth.add_trace(go.Scatter(
                x=growth['Year'], y=growth['Net Profit'],
                mode='lines+markers', name='Avg Profit',
                line=dict(color='green', width=4), marker=dict(size=10)
            ))
            fig_growth.update_layout(
                title="YoY Growth Trends",
                height=450, xaxis_title="Year", yaxis_title="Amount ($)"
            )
            st.plotly_chart(fig_growth, use_container_width=True)
        else:
            st.warning("No data for growth chart")

# ========================================
# TAB 3: OPERATIONS DASHBOARD
# ========================================
with tab3:
    st.markdown("### 💰 Operations Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Production Cost Share")
        cost_pie_data = filtered_df.groupby('Product Name')['Production Cost'].sum().reset_index()
        if len(cost_pie_data) > 0:
            fig_pie = px.pie(
                cost_pie_data, values='Production Cost', names='Product Name',
                title="Production Cost by Product",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(
                texttemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}',
                textposition='inside'
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No data for pie chart")
    
    with col2:
        st.markdown("#### Cost Structure Breakdown")
        cost_cols = ['Raw Material Cost', 'Production Cost', 'Salary of Workers']
        cost_breakdown = filtered_df[cost_cols].mean().round(0).reset_index()
        cost_breakdown.columns = ['Cost Type', 'Amount']
        fig_cost = px.pie(
            cost_breakdown, values='Amount', names='Cost Type',
            title="Average Cost Breakdown",
            color_discrete_sequence=['gold', 'lightcoral', 'lightblue']
        )
        fig_cost.update_traces(textinfo='label+percent+value', textfont_size=12)
        fig_cost.update_layout(height=400)
        st.plotly_chart(fig_cost, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("#### 👥 Worker Efficiency")
    filtered_df['Profit per Worker'] = (
        filtered_df['Net Profit'] / filtered_df['Total No of Workers'].replace(0, 1)
    )
    fig_worker = px.box(
        filtered_df, x='Product Name', y='Profit per Worker',
        title="Profit per Worker by Product",
        color='Product Name', color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_worker.update_layout(height=400, xaxis_tickangle=45)
    st.plotly_chart(fig_worker, use_container_width=True)

# ========================================
# GLOBAL FOOTER
# ========================================
st.markdown("---")
st.markdown("### 📋 Dataset Summary")

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
summary_col1.metric("Filtered Records", f"{len(filtered_df):,}")
summary_col2.metric("Selected Year", "All" if selected_year == "All" else selected_year)
summary_col3.metric("Selected Product", selected_product)
summary_col4.metric("Min Sales Filter", f"${min_sales:,}")

with st.expander("🔍 Raw Data Preview (Top 50)", expanded=False):
    preview_cols = [
        'Year', 'Product Name', 'Total Sale', 'Net Profit', 'Profit Margin',
        'Total No of Workers', 'Raw Material Cost', 'Production Cost'
    ]
    st.dataframe(filtered_df[preview_cols].head(50).round(2), use_container_width=True)

st.markdown("---")
st.caption("✅ FULL FILTERS with 'All' for Year & Product + live-reactive dashboard.")
