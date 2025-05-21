import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import numpy as np
from datetime import datetime, timedelta
from utils import (
    style_dataframe,
    load_all_data,
    create_correlation_matrix,
    create_scatter_with_trendline,
    create_box_plot,
    create_time_series_plot,
    create_monthly_plot,
    create_cleaning_impact_plot,
    create_daytime_averages_plot
)

# Page config
st.set_page_config(
    page_title="Solar Data Discovery Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
st.sidebar.title("🔍 Dashboard Filters")
section = st.sidebar.radio("Section", ["Country Analysis", "Cross-Country Comparison"])

# --- Load data (Supporting both local and online CSVs) ---
data_paths = {
    "Benin": "https://my.microsoftpersonalcontent.com/personal/fdd48cc5c7ca68e6/_layouts/15/download.aspx?UniqueId=90a6e3f9-c245-46f0-8966-2ec4db7471f8&Translate=false&tempauth=v1e.eyJzaXRlaWQiOiJkNWNkMzA4MC1kZTVmLTQ3ZDUtYTI2Ni1mMzIyYTk1ZGI0MWQiLCJhcHBpZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDA0ODE3MTBhNCIsImF1ZCI6IjAwMDAwMDAzLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMC9teS5taWNyb3NvZnRwZXJzb25hbGNvbnRlbnQuY29tQDkxODgwNDBkLTZjNjctNGM1Yi1iMTEyLTM2YTMwNGI2NmRhZCIsImV4cCI6IjE3NDc4MjcyNjMifQ.I2FN3aiZ1DgTKxt7TnSmSBoSLVSKm-cuU7AnMWyqEbfpcVBUY4kyXxVxW2Ez21orcD_qp_rdVVIU5mlikGEUcMBKAqy4Q_O6ilucJE6eqyP6o2GVGCwndQBWtD8sn2r8JXgnMcBC4s2VG3EjcSwCfpZVYXUkvQRlSe_s1Izc395e4b_eJsU1gRHecc125RFMTRE6njG8HTLlGFW-g_N5dUoIzxiK5Nx_Lk8iPqW_Ewj-onc0uDrU8Srv2YJRJEhNh5zC54WbUkG5FTMsvpsUwNY2FW2Lx8HqFe_hxKZV6AjuVdrc_KY1cdvZMWvxK3mE0Vyk-PN0HBRrlNbdYM_8n1l7ioFFadujxzPR8CDSvF5HprCgd7SBt34vJZVfCayPtoEB9pLP6iyQVLJR5N4yqivOlabWJKe7PyreeO_xQzU.9LG9RVcqUaDUAEu3gwgVOp30gv3DEbOV97o_YpdqJ4I&ApiVersion=2.0&AVOverride=1",
    "Sierra Leone": "https://my.microsoftpersonalcontent.com/personal/fdd48cc5c7ca68e6/_layouts/15/download.aspx?UniqueId=f833aabe-7967-4c41-a56b-c3ca5b4f4d09&Translate=false&tempauth=v1e.eyJzaXRlaWQiOiJkNWNkMzA4MC1kZTVmLTQ3ZDUtYTI2Ni1mMzIyYTk1ZGI0MWQiLCJhcHBpZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDA0ODE3MTBhNCIsImF1ZCI6IjAwMDAwMDAzLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMC9teS5taWNyb3NvZnRwZXJzb25hbGNvbnRlbnQuY29tQDkxODgwNDBkLTZjNjctNGM1Yi1iMTEyLTM2YTMwNGI2NmRhZCIsImV4cCI6IjE3NDc4Mjc2MTUifQ.YQIu3D6EKRMu_Bm8eyhODKor7v4cZD8K9kOl2mKV94FzkJE9nHeC7VlPbvemE-JygRfR-CcRrPVMY7lzAnWvRznadV7Sg95OTVWPK1tnWIEY2rmcVKLhG1hj8ATAuWHd_B12gqEh1IiUnld4b3b6hDw0VYYwmvWAupO-gWLxiiqFnhVMDjwGz5LpeTAfsh06I4RSHji-jcAv4__cF-djOVruku1KHc1-nDCgYMwJ4nTN7CTa6cEJ9_UpnR1Li0JYt5Ac1koMQj0wx2NZ1CjANvRK2XUm9eXbyf6Lb-qvzCYbwj5UNbFDM4tjh_49oVu0arjH8606fX2b8-I1o5NIo49CIxrIYukgSrA6C-Xdk1biLfUNKP4y_9joENxWMblNojiOssuEukTYZaC1RQF_4HyDsgttqACaiwfEtKmMbD0.uuwFHfhbXQ__RJo4tf9oswTGw8huqDddQuYwqmZzjic&ApiVersion=2.0&AVOverride=1",
    "Togo": "https://my.microsoftpersonalcontent.com/personal/fdd48cc5c7ca68e6/_layouts/15/download.aspx?UniqueId=b0e52d80-5c9b-4b18-820d-676a67c948d5&Translate=false&tempauth=v1e.eyJzaXRlaWQiOiJkNWNkMzA4MC1kZTVmLTQ3ZDUtYTI2Ni1mMzIyYTk1ZGI0MWQiLCJhcHBpZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDA0ODE3MTBhNCIsImF1ZCI6IjAwMDAwMDAzLTAwMDAtMGZmMS1jZTAwLTAwMDAwMDAwMDAwMC9teS5taWNyb3NvZnRwZXJzb25hbGNvbnRlbnQuY29tQDkxODgwNDBkLTZjNjctNGM1Yi1iMTEyLTM2YTMwNGI2NmRhZCIsImV4cCI6IjE3NDc4Mjc2NzYifQ.NPKkYlDdT7RjLln7c_PDqvUKYUhJIXGm8yLufZkgN4tcvXdKiUe3JSF5br3gdKmiU3e2R0B7gAliNcjsXMUTWdatTpvxs4kTqveTwudtatGrOiP6DImDiTcp3eFxW5CTnfPxnm8Ui-gRABpuC8vwr4KsZu3HW55ZY6OiqthasTi_h0vE0hXp50bM1fzsksX0C1ikT_w_0v4Eo3vYFcbycIbipnqLZVsvUbUgwXdEzxCtlaQIcQ95ydv7ldozpRplqvePGPxGMobeXgE_GdybDMJP1ANmtAuqdL18_FDps8zymBrWUZyJcjstgJ0oG7DWnvRMEFVN8wBn0kmaBy62Dh45HukJdgsTn-9dZb2jLMdFHzT0adRkjVQ-AlGfR3XNrWVgPh3yAGL2SohK_ybJ1CQBCfKczjZ5-mWJOSZdTAQ.neD7r511BoNln76BFuh1M8ANHC8R1pjk6T2a5DqUUcY&ApiVersion=2.0&AVOverride=1"
}

# For local development, you can use local paths:
# data_paths = {
#     "Benin": "data/benin_clean.csv",
#     "Sierra Leone": "data/sierraleone_clean.csv",
#     "Togo": "data/togo_clean.csv"
# }

# Load all data at once
dfs = load_all_data(data_paths)

# --- Country-specific analysis ---
if section == "Country Analysis":
    country = st.sidebar.selectbox("Select Country", list(data_paths.keys()))
    df = dfs[country]
    
    # Date range selector
    min_date = df.index.min()
    max_date = df.index.max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )
    
    # Filter data based on date range
    mask = (df.index.date >= date_range[0]) & (df.index.date <= date_range[1])
    df_filtered = df[mask]
    
    analysis_type = st.sidebar.radio("Select Analysis Type", [
        "Overview", "Time Series", "Cleaning Impact", "Correlation", "Advanced Analysis"])

    if analysis_type == "Overview":
        st.title(f"🌞 Solar Overview — {country}")
        
        # Key metrics in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg GHI (W/m²)", f"{df_filtered['GHI'].mean():.2f}")
        with col2:
            st.metric("Avg DNI (W/m²)", f"{df_filtered['DNI'].mean():.2f}")
        with col3:
            st.metric("Avg DHI (W/m²)", f"{df_filtered['DHI'].mean():.2f}")

        # Interactive time series plots
        st.subheader("Interactive Time Series")
        metrics = st.multiselect(
            "Select metrics to display",
            ["GHI", "DNI", "DHI", "Tamb", "RH"],
            default=["GHI", "DNI", "DHI"]
        )
        
        if metrics:
            fig = go.Figure()
            for metric in metrics:
                fig.add_trace(go.Scatter(
                    x=df_filtered.index,
                    y=df_filtered[metric],
                    name=metric,
                    mode='lines'
                ))
            fig.update_layout(
                title="Solar Metrics Over Time",
                xaxis_title="Date",
                yaxis_title="Value",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Daily patterns
        st.subheader("Daily Patterns")
        selected_metric = st.selectbox("Select metric for daily pattern", metrics)
        
        df_filtered['Hour'] = df_filtered.index.hour
        daily_pattern = df_filtered.groupby('Hour')[selected_metric].agg(['mean', 'std']).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_pattern['Hour'],
            y=daily_pattern['mean'],
            name='Mean',
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=daily_pattern['Hour'],
            y=daily_pattern['mean'] + daily_pattern['std'],
            name='Upper Bound',
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=daily_pattern['Hour'],
            y=daily_pattern['mean'] - daily_pattern['std'],
            name='Lower Bound',
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(0,100,80,0.2)',
            showlegend=False
        ))
        fig.update_layout(
            title=f"Daily Pattern of {selected_metric}",
            xaxis_title="Hour of Day",
            yaxis_title=selected_metric,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

    elif analysis_type == "Time Series":
        st.title(f"📈 Time Series Analysis — {country}")
        
        # Interactive time series with range slider
        metric = st.selectbox("Select Metric", ["GHI", "DNI", "DHI", "Tamb", "RH"])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_filtered.index,
            y=df_filtered[metric],
            mode='lines',
            name=metric
        ))
        fig.update_layout(
            title=f"{metric} Over Time",
            xaxis_title="Date",
            yaxis_title=metric,
            hovermode='x unified',
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
       

    elif analysis_type == "Cleaning Impact":
        st.title(f"🧽 Cleaning Impact on Sensors — {country}")
        if 'Cleaning' in df_filtered.columns:
            # Calculate mean values before and after cleaning
            cleaning_dates = df_filtered[df_filtered['Cleaning'] == 1].index
            
            if len(cleaning_dates) > 0:
                # Calculate overall means for each sensor
                before_cleaning = df_filtered[df_filtered['Cleaning'] == 0][['ModA', 'ModB']].mean()
                after_cleaning = df_filtered[df_filtered['Cleaning'] == 1][['ModA', 'ModB']].mean()
                
                # Create and display the cleaning impact plot
                fig = create_cleaning_impact_plot(before_cleaning, after_cleaning)
                st.plotly_chart(fig, use_container_width=True)
                
                # Display the values in a table
                st.subheader("Mean Values")
                summary_df = pd.DataFrame({
                    'Sensor': ['ModA', 'ModB'],
                    'Before Cleaning': [before_cleaning['ModA'], before_cleaning['ModB']],
                    'After Cleaning': [after_cleaning['ModA'], after_cleaning['ModB']],
                    'Improvement (%)': [
                        ((after_cleaning['ModA'] - before_cleaning['ModA']) / before_cleaning['ModA'] * 100),
                        ((after_cleaning['ModB'] - before_cleaning['ModB']) / before_cleaning['ModB'] * 100)
                    ]
                }).round(2)
                
                st.dataframe(style_dataframe(summary_df))
            else:
                st.warning("No cleaning events found in the selected date range.")
        else:
            st.warning("Cleaning flag not available in dataset.")

    elif analysis_type == "Correlation":
        st.title(f"📊 Correlation Analysis — {country}")
        
        # Define specific columns for correlation
        corr_columns = ["GHI", "DNI", "DHI", "TModA", "TModB"]
        
        # Create and display correlation matrix
        fig = create_correlation_matrix(df_filtered, corr_columns)
        st.plotly_chart(fig, use_container_width=True)
        
        # Pairwise correlation analysis
        st.subheader("Pairwise Correlation Analysis")
        col_x = st.selectbox("X-axis", corr_columns)
        col_y = st.selectbox("Y-axis", [col for col in corr_columns if col != col_x], 
                           index=1 if col_x != corr_columns[1] else 0)
        
        # Create scatter plot with trendline
        fig, r_value, p_value, slope, intercept = create_scatter_with_trendline(df_filtered, col_x, col_y)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display correlation statistics
        st.subheader("Correlation Statistics")
        stats_df = pd.DataFrame({
            'Metric': ['Correlation Coefficient', 'R-squared', 'P-value', 'Slope', 'Intercept'],
            'Value': [
                f"{r_value:.3f}",
                f"{r_value**2:.3f}",
                f"{p_value:.3e}",
                f"{slope:.3f}",
                f"{intercept:.3f}"
            ]
        })
        st.dataframe(style_dataframe(stats_df))

    elif analysis_type == "Advanced Analysis":
        st.title(f"🔬 Advanced Analysis — {country}")
        
        # Anomaly detection
        st.subheader("Anomaly Detection")
        metric = st.selectbox("Select metric", ["GHI", "DNI", "DHI"])
        
        # Time-based patterns
        st.subheader("Time-based Patterns")
        df_filtered['Hour'] = df_filtered.index.hour
        df_filtered['Day'] = df_filtered.index.day_name()
        df_filtered['Month'] = df_filtered.index.month_name()
        
        time_pattern = st.selectbox(
            "Select time pattern",
            ["Hourly", "Daily", "Monthly"]
        )
        
        if time_pattern == "Hourly":
            pattern_data = df_filtered.groupby('Hour')[metric].mean()
            x_axis = pattern_data.index
        elif time_pattern == "Daily":
            pattern_data = df_filtered.groupby('Day')[metric].mean()
            x_axis = pattern_data.index
        else:
            pattern_data = df_filtered.groupby('Month')[metric].mean()
            x_axis = pattern_data.index
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_axis,
            y=pattern_data,
            text=pattern_data.round(2),
            textposition='auto',
        ))
        fig.update_layout(
            title=f"{time_pattern} Pattern of {metric}",
            xaxis_title=time_pattern,
            yaxis_title=metric
        )
        st.plotly_chart(fig, use_container_width=True)

# --- Cross-country comparison ---
elif section == "Cross-Country Comparison":
    st.title("🌍 Cross-Country Comparison")
    
    # Date range selector for comparison
    min_date = min(df.index.min() for df in dfs.values())
    max_date = max(df.index.max() for df in dfs.values())
    date_range = st.sidebar.date_input(
        "Select Date Range for Comparison",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )
    
    # Filter data based on date range
    dfs_filtered = {
        country: df[(df.index.date >= date_range[0]) & (df.index.date <= date_range[1])]
        for country, df in dfs.items()
    }
    
    # Metric selection
    metric = st.selectbox("Select Metric to Compare", ["GHI", "DNI", "DHI"])
    
    # Create tabs for different comparison views
    tab1, tab2, tab3 = st.tabs(["Distribution", "Time Series", "Daytime Averages"])
    
    with tab1:
        st.subheader("Distribution Analysis")
        
        # Filter for daytime data (6-18)
        daytime_dfs = {
            country: df[(df['hour'] >= 6) & (df['hour'] <= 18)]
            for country, df in dfs_filtered.items()
        }
        
        # Create comparison dataframe
        comp_df = pd.concat([
            daytime_dfs[c][metric].rename(c) for c in data_paths
        ], axis=1).melt(var_name="Country", value_name=metric)
        
        # Create and display box plot
        fig = create_box_plot(comp_df, metric, data_paths.keys())
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        summary_stats = comp_df.groupby("Country")[metric].agg([
            ('Mean', 'mean'),
            ('Median', 'median'),
            ('Std Dev', 'std'),
            ('Min', 'min'),
            ('Max', 'max')
        ]).round(2)
        
        st.dataframe(style_dataframe(summary_stats))
    
    with tab2:
        st.subheader("Time Series Comparison")
        
        # Resample data to daily for better performance
        daily_data = {
            country: df[metric].resample('D').mean()
            for country, df in dfs_filtered.items()
        }
        
        # Create and display daily time series plot
        fig = create_time_series_plot(daily_data, metric)
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly averages for trend analysis
        monthly_data = {
            country: df[metric].resample('M').mean()
            for country, df in dfs_filtered.items()
        }
        
        # Create and display monthly plot
        fig = create_monthly_plot(monthly_data, metric)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Daytime Averages (6:00 - 18:00)")
        
        # Calculate daytime averages
        daytime_avg = {}
        for country, df in dfs_filtered.items():
            daytime_mask = (df['hour'] >= 6) & (df['hour'] <= 18)
            daytime_avg[country] = df[daytime_mask][metric].mean()
        
        # Create and display daytime averages plot
        fig = create_daytime_averages_plot(daytime_avg, metric)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display the values in a table
        daytime_df = pd.DataFrame({
            'Country': list(daytime_avg.keys()),
            f'Average {metric}': list(daytime_avg.values())
        }).round(2)
        
        st.dataframe(style_dataframe(daytime_df))