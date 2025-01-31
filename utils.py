import pandas as pd
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from typing import Tuple
import datetime as dt

# ISO format with timezone for consistent datetime handling
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"

def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv('temperature_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'], format=DATETIME_FORMAT)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['timestamp', 'temperature'])

def save_data(df: pd.DataFrame) -> None:
    # Ensure timestamps are formatted consistently and sorted
    df_copy = df.copy()
    df_copy = df_copy.sort_values('timestamp', ascending=True)
    df_copy['timestamp'] = df_copy['timestamp'].dt.strftime(DATETIME_FORMAT)
    df_copy.to_csv('temperature_data.csv', index=False)

def add_temperature(temp: float, timestamp: datetime, df: pd.DataFrame) -> pd.DataFrame:
    new_data = pd.DataFrame({
        'timestamp': [timestamp],
        'temperature': [temp]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)
    return df

def get_statistics(df: pd.DataFrame) -> Tuple[float, float, float]:
    if len(df) == 0:
        return 0.0, 0.0, 0.0
    
    avg_temp = df['temperature'].mean()
    min_temp = df['temperature'].min()
    max_temp = df['temperature'].max()
    return round(avg_temp, 1), round(min_temp, 1), round(max_temp, 1)

def create_temperature_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    
    if len(df) > 0:
        # Convert UTC timestamps to local time for display
        df_local = df.copy()
        df_local['timestamp'] = df_local['timestamp'].dt.tz_convert(dt.datetime.now().astimezone().tzinfo)
        
        fig.add_trace(go.Scatter(
            x=df_local['timestamp'],
            y=df['temperature'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#3498db', width=2),
            marker=dict(size=8, color='#2980b9')
        ))

        fig.update_layout(
            title='Temperature Over Time',
            xaxis_title='Time',
            yaxis_title='Temperature (°C)',
            hovermode='x unified',
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
        )

        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f0f0f0',
        )

        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#f0f0f0',
            range=[min(35, df['temperature'].min() - 0.5),
                  max(42, df['temperature'].max() + 0.5)]
        )

    return fig
