# 🌡️ Temperature Tracker

A web-based application built with Streamlit for tracking and visualizing body temperature measurements over time.

## Features

- **Temperature Recording**: Add temperature readings with timestamps
  - Input range: 35.0°C - 42.0°C
  - Automatic current time recording or manual date/time entry
  - Data persistence using CSV storage

- **Statistical Analysis**:
  - Average temperature
  - Minimum temperature
  - Maximum temperature

- **Data Visualization**:
  - Interactive temperature history chart
  - Time-based temperature trends
  - Raw data view option

## Requirements

- Python 3.11 or higher
- Dependencies:
  - streamlit >= 1.41.1
  - pandas >= 2.2.3
  - plotly >= 6.0.0
  - pytz >= 2024.2

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/FeverTracker.git
cd FeverTracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. To add a temperature reading:
   - Enter the temperature value in Celsius
   - Choose between current time or manual date/time entry
   - Click "Add Temperature"

4. View statistics and temperature history in the charts below
   - Toggle "Show raw data" to see the detailed temperature records

## File Structure

- `main.py`: Main application file with Streamlit interface
- `utils.py`: Utility functions for data handling and chart creation
- `style.py`: Custom CSS styling for the web interface
- `temperature_data.csv`: Data storage file for temperature readings

## Features in Detail

### Temperature Input
- Decimal precision to 0.1°C
- Input validation for safe temperature ranges
- Flexible timestamp options

### Data Visualization
- Interactive line chart showing temperature trends
- Hover details for each data point
- Adjustable view range
- Grid lines for better readability

### Statistics Panel
- Real-time calculation of key metrics
- Clear presentation of average, minimum, and maximum temperatures

## Data Storage

Temperature readings are stored in a CSV file (`temperature_data.csv`) with the following format:
- timestamp: Date and time of the reading
- temperature: Temperature value in Celsius

## Styling

The application features a clean, modern interface with:
- Responsive layout
- Custom-styled input fields
- Clear data visualization
- Mobile-friendly design
