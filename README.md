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
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- Dependencies are managed via `pyproject.toml`:
  - streamlit >= 1.41.1
  - pandas >= 2.2.3
  - plotly >= 6.0.0
  - pytz >= 2024.2

## Installation

### Prerequisites
First, install `uv` if you haven't already:
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Project Setup
1. Clone this repository:
```bash
git clone https://github.com/yourusername/FeverTracker.git
cd FeverTracker
```

2. Set up configuration:
```bash
# Copy the template configuration file
cp config.json.template config.json

# Edit config.json with your MongoDB connection details
# Update the uri, database_name, and collection_name as needed
```

3. Initialize the project (this will install all dependencies):
```bash
make init
```

## Usage

### Quick Start
```bash
make run
```

### Available Make Commands
Run `make help` to see all available commands:

- `make run` - Install dependencies and start the application
- `make install` - Install dependencies using uv
- `make test` - Run application tests to verify everything works
- `make dev` - Install development dependencies
- `make clean` - Clean up temporary files and caches
- `make update` - Update all dependencies to latest versions
- `make info` - Show project and environment information
- `make status` - Show current environment status
- `make reset` - Reset the environment (clean + fresh install)

### Manual Usage
If you prefer not to use the Makefile:

1. Install dependencies:
```bash
uv sync
```

2. Start the application:
```bash
uv run streamlit run main.py
```

3. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

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
- `pyproject.toml`: Project configuration and dependencies
- `uv.lock`: Lock file with exact dependency versions
- `Makefile`: Automation scripts for common development tasks
- `test_app.py`: Test script to verify application functionality
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

## Configuration

The application uses a `config.json` file to store MongoDB connection details. This file is not tracked in version control for security reasons.

### Configuration File Format
```json
{
  "mongodb": {
    "uri": "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority",
    "database_name": "fever_tracker_db",
    "collection_name": "temperatures"
  }
}
```

### Environment Variable Override
You can also set the MongoDB URI using the `MONGODB_URI` environment variable, which will override the value in the configuration file:
```bash
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
```

## Data Storage

Temperature readings are stored in MongoDB with the following document structure:
- timestamp: Date and time of the reading
- temperature: Temperature value in Celsius
- medication: Optional medication information

Legacy CSV support is maintained for migration purposes.

## Styling

The application features a clean, modern interface with:
- Responsive layout
- Custom-styled input fields
- Clear data visualization
- Mobile-friendly design
