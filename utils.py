import pandas as pd
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
from typing import Tuple
import datetime as dt
import os
import json
from pymongo import MongoClient
from pymongo.collection import Collection

# ISO format with timezone for consistent datetime handling
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"

def load_config() -> dict:
    """Load configuration from config.json file."""
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        st.error("Configuration file 'config.json' not found. Please create it with MongoDB connection details.")
        raise
    except json.JSONDecodeError as e:
        st.error(f"Error parsing configuration file: {str(e)}")
        raise
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        raise

def get_mongodb_collection() -> Collection:
    """Get MongoDB collection for temperature data."""
    try:
        config = load_config()
        mongodb_config = config['mongodb']
        
        # Allow environment variable to override config file
        mongodb_uri = os.getenv('MONGODB_URI', mongodb_config['uri'])
        database_name = mongodb_config['database_name']
        collection_name = mongodb_config['collection_name']
        
        client = MongoClient(mongodb_uri)
        db = client[database_name]
        collection = db[collection_name]
        return collection
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

def migrate_csv_to_mongodb() -> None:
    """One-time migration of CSV data to MongoDB."""
    try:
        # Load existing CSV data
        df = pd.read_csv('temperature_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'], format=DATETIME_FORMAT)
        if 'medication' not in df.columns:
            df['medication'] = ''
        
        # Get MongoDB collection
        collection = get_mongodb_collection()
        
        # Convert DataFrame to list of documents
        documents = []
        for _, row in df.iterrows():
            doc = {
                'timestamp': row['timestamp'].to_pydatetime(),
                'temperature': float(row['temperature']),
                'medication': str(row['medication']) if pd.notna(row['medication']) else ''
            }
            documents.append(doc)
        
        # Insert documents into MongoDB
        if documents:
            collection.insert_many(documents)
            st.success(f"Successfully migrated {len(documents)} temperature readings to MongoDB!")
        else:
            st.info("No data found in CSV file to migrate.")
            
    except FileNotFoundError:
        st.info("No CSV file found to migrate.")
    except Exception as e:
        st.error(f"Error during migration: {str(e)}")

def load_data() -> pd.DataFrame:
    """Load temperature data from MongoDB."""
    try:
        collection = get_mongodb_collection()
        
        # Retrieve all documents from MongoDB
        documents = list(collection.find().sort('timestamp', 1))
        
        if not documents:
            return pd.DataFrame(columns=['timestamp', 'temperature', 'medication'])
        
        # Convert documents to DataFrame
        data = []
        for doc in documents:
            data.append({
                'timestamp': doc['timestamp'],
                'temperature': doc['temperature'],
                'medication': doc.get('medication', '')
            })
        
        df = pd.DataFrame(data)
        
        # Ensure timestamp is timezone-aware
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data from MongoDB: {str(e)}")
        return pd.DataFrame(columns=['timestamp', 'temperature', 'medication'])

def add_temperature(temp: float, timestamp: datetime, medication: str) -> None:
    """Add a new temperature reading to MongoDB."""
    try:
        collection = get_mongodb_collection()
        
        # Create document
        document = {
            'timestamp': timestamp,
            'temperature': round(temp, 1),
            'medication': medication if medication else ''
        }
        
        # Insert document
        collection.insert_one(document)
        
    except Exception as e:
        st.error(f"Error adding temperature to MongoDB: {str(e)}")
        raise

def get_statistics(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate temperature statistics."""
    if len(df) == 0:
        return 0.0, 0.0, 0.0
    
    avg_temp = df['temperature'].mean()
    min_temp = df['temperature'].min()
    max_temp = df['temperature'].max()
    return round(avg_temp, 1), round(min_temp, 1), round(max_temp, 1)

def create_temperature_chart(df: pd.DataFrame) -> go.Figure:
    """Create a temperature chart from the DataFrame."""
    fig = go.Figure()
    
    if len(df) > 0:
        # Convert UTC timestamps to local time for display
        df_local = df.copy()
        df_local['timestamp'] = df_local['timestamp'].dt.tz_convert(dt.datetime.now().astimezone().tzinfo)
        
        # Create hover text with medication info
        hover_text = []
        for _, row in df_local.iterrows():
            text = f"Temperature: {row['temperature']}°C"
            if pd.notna(row['medication']) and row['medication']:
                text += f"<br>Medication: {row['medication']}"
            hover_text.append(text)

        # Create marker colors based on medication
        marker_colors = ['#ff0000' if pd.notna(med) and med else '#2980b9' for med in df['medication']]

        fig.add_trace(go.Scatter(
            x=df_local['timestamp'],
            y=df['temperature'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#3498db', width=2),
            marker=dict(size=8, color=marker_colors),
            hovertext=hover_text,
            hoverinfo='text'
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
