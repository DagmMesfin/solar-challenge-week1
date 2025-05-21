import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import numpy as np
import streamlit as st
import requests
from io import StringIO

def style_dataframe(df):
    """Apply consistent styling to all dataframes"""
    return df.style.background_gradient(cmap='RdYlBu_r')\
        .set_properties(**{
            'font-size': '12pt',
            'font-family': 'Arial',
            'text-align': 'center',
            'padding': '10px',
            'border': '1px solid #ddd'
        })\
        .set_table_styles([
            {'selector': 'th',
             'props': [
                 ('background-color', '#f0f2f6'),
                 ('color', '#262730'),
                 ('font-weight', 'bold'),
                 ('text-align', 'center'),
                 ('padding', '10px'),
                 ('border', '1px solid #ddd')
             ]},
            {'selector': 'td',
             'props': [
                 ('text-align', 'center'),
                 ('padding', '10px'),
                 ('border', '1px solid #ddd')
             ]}
        ])\
        .format(precision=2)

def load_csv_from_url(url):
    """Load CSV data from a URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return pd.read_csv(StringIO(response.text), parse_dates=['Timestamp'])
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading data from URL: {e}")
        return None

@st.cache_data(ttl=3600)
def load_all_data(data_paths):
    """Load and process data for all countries from local files or URLs"""
    dfs = {}
    for country, path in data_paths.items():
        try:
            # Check if the path is a URL
            if path.startswith(('http://', 'https://')):
                df = load_csv_from_url(path)
            else:
                df = pd.read_csv(path, parse_dates=['Timestamp'])
            
            if df is not None:
                if 'Comments' in df.columns:
                    df = df.drop('Comments', axis=1)
                df.set_index('Timestamp', inplace=True)
                df['hour'] = df.index.hour
                dfs[country] = df
            else:
                st.error(f"Failed to load data for {country}")
        except Exception as e:
            st.error(f"Error processing data for {country}: {e}")
    
    return dfs

def create_correlation_matrix(df, columns):
    """Create correlation matrix heatmap"""
    corr = df[columns].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        text=corr.round(3),
        texttemplate='%{text}',
        textfont={"size": 12},
        hoverongaps=False
    ))
    fig.update_layout(
        title="Correlation Matrix",
        height=600,
        xaxis_title="Variables",
        yaxis_title="Variables"
    )
    return fig

def create_scatter_with_trendline(df, x_col, y_col):
    """Create scatter plot with trendline"""
    x = df[x_col].values
    y = df[y_col].values
    mask = ~np.isnan(x) & ~np.isnan(y)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], y[mask])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='markers',
        name='Data Points',
        marker=dict(
            size=8,
            opacity=0.6
        )
    ))
    
    x_trend = np.array([x[mask].min(), x[mask].max()])
    y_trend = slope * x_trend + intercept
    fig.add_trace(go.Scatter(
        x=x_trend,
        y=y_trend,
        mode='lines',
        name=f'Trendline (R² = {r_value**2:.3f})',
        line=dict(color='red', width=2)
    ))
    
    fig.update_layout(
        title=f"{x_col} vs {y_col}",
        xaxis_title=x_col,
        yaxis_title=y_col,
        showlegend=True,
        height=500
    )
    
    return fig, r_value, p_value, slope, intercept

def create_box_plot(comp_df, metric, countries):
    """Create box plot for distribution analysis"""
    fig = go.Figure()
    for country in countries:
        country_data = comp_df[comp_df['Country'] == country][metric]
        fig.add_trace(go.Box(
            y=country_data,
            name=country,
            boxpoints='outliers',
            showlegend=False
        ))
    
    fig.update_layout(
        title=f"Distribution of {metric} by Country",
        yaxis_title=metric,
        height=500
    )
    return fig

def create_time_series_plot(daily_data, metric):
    """Create time series plot"""
    fig = go.Figure()
    for country, data in daily_data.items():
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data,
            name=country,
            mode='lines'
        ))
    
    fig.update_layout(
        title=f"Daily Average {metric} by Country",
        xaxis_title="Date",
        yaxis_title=metric,
        hovermode='x unified'
    )
    return fig

def create_monthly_plot(monthly_data, metric):
    """Create monthly average plot"""
    fig = go.Figure()
    for country, data in monthly_data.items():
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data,
            name=country,
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title=f"Monthly Average {metric} by Country",
        xaxis_title="Date",
        yaxis_title=metric,
        hovermode='x unified'
    )
    return fig

def create_cleaning_impact_plot(before_cleaning, after_cleaning):
    """Create cleaning impact bar plot"""
    comparison_data = pd.DataFrame({
        'Sensor': ['ModA', 'ModB', 'ModA', 'ModB'],
        'Condition': ['Before Cleaning', 'Before Cleaning', 'After Cleaning', 'After Cleaning'],
        'Mean Value': [
            before_cleaning['ModA'],
            before_cleaning['ModB'],
            after_cleaning['ModA'],
            after_cleaning['ModB']
        ]
    })
    
    fig = go.Figure()
    for sensor in ['ModA', 'ModB']:
        sensor_data = comparison_data[comparison_data['Sensor'] == sensor]
        fig.add_trace(go.Bar(
            x=sensor_data['Condition'],
            y=sensor_data['Mean Value'],
            name=sensor,
            text=sensor_data['Mean Value'].round(2),
            textposition='auto',
        ))
    
    fig.update_layout(
        title="Sensor Performance Before and After Cleaning",
        xaxis_title="Cleaning Status",
        yaxis_title="Mean Irradiance (W/m²)",
        barmode='group',
        showlegend=True
    )
    return fig

def create_daytime_averages_plot(daytime_avg, metric):
    """Create daytime averages bar plot"""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(daytime_avg.keys()),
        y=list(daytime_avg.values()),
        text=[f"{v:.2f}" for v in daytime_avg.values()],
        textposition='auto',
    ))
    
    fig.update_layout(
        title=f"Average {metric} by Country",
        xaxis_title="Country",
        yaxis_title=f"Average {metric}",
        showlegend=False
    )
    return fig 