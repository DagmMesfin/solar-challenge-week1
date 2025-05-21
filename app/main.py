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
    create_box_plot,
    create_time_series_plot,
    create_monthly_plot,
    create_cleaning_impact_plot,
    create_daytime_averages_plot,
    create_density_scatter,
    create_means_comparison,
    create_kde_plot
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
    "Benin": "https://drive.usercontent.google.com/download?id=1pTXeDbozO16Dz-46U6nVOVEDcdOIl8l1&export=download",
    "Sierra Leone": "https://drive.usercontent.google.com/download?id=1PTCdPIgw7_a8A_5qac6tkUZ1hTDAmj1C&export=download",
    "Togo": "https://drive.usercontent.google.com/download?id=17LwF0MUUTQwPNXfgZePi-peIOwv0tGhu&export=download"
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
            default=["GHI", "DHI"]
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
        
        # Create KDE plot
        fig = create_kde_plot(df_filtered, col_x, col_y)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display summary statistics
        st.subheader("Summary Statistics")
        stats_df = df_filtered[[col_x, col_y]].agg(['mean', 'std', 'min', 'max']).round(2)
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