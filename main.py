import streamlit as st
from datetime import datetime
import pytz
from utils import load_data, add_temperature, get_statistics, create_temperature_chart
from style import apply_custom_style

def main():
    st.set_page_config(
        page_title="Temperature Tracker",
        page_icon="🌡️",
        layout="wide"
    )

    apply_custom_style()

    st.title("🌡️ Temperature Tracker")
    st.markdown("Track your body temperature over time")

    # Initialize session state for timestamp
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = datetime.now().date()
    if 'selected_time' not in st.session_state:
        st.session_state.selected_time = datetime.now().time()

    # Load existing data
    df = load_data()

    # Input section
    st.subheader("Add New Temperature Reading")

    col1, col2 = st.columns([2, 1])

    with col1:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=35.0,
            max_value=42.0,
            value=37.0,
            step=0.1,
            format="%.1f"
        )

    with col2:
        use_current_time = st.checkbox("Use current time", value=True)

    if not use_current_time:
        selected_date = st.date_input("Date", st.session_state.selected_date)
        selected_time = st.time_input("Time", st.session_state.selected_time)

        # Update session state only when input changes
        if selected_date != st.session_state.selected_date:
            st.session_state.selected_date = selected_date
        if selected_time != st.session_state.selected_time:
            st.session_state.selected_time = selected_time

        # Convert local time to UTC
        local_dt = datetime.combine(st.session_state.selected_date, st.session_state.selected_time)
        timestamp = local_dt.astimezone(pytz.UTC)
    else:
        timestamp = datetime.now(pytz.UTC)

    if st.button("Add Temperature"):
        df = add_temperature(temperature, timestamp, df)
        st.success("Temperature reading added successfully!")
        st.rerun()

    # Statistics section
    st.subheader("Statistics")
    avg_temp, min_temp, max_temp = get_statistics(df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average", f"{avg_temp}°C")
    with col2:
        st.metric("Minimum", f"{min_temp}°C")
    with col3:
        st.metric("Maximum", f"{max_temp}°C")

    # Chart section
    st.subheader("Temperature History")
    if len(df) > 0:
        fig = create_temperature_chart(df)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No temperature readings yet. Add your first reading above!")

    # Display raw data
    if st.checkbox("Show raw data"):
        # Convert UTC to local time for display
        df_display = df.copy()
        df_display['timestamp'] = df_display['timestamp'].dt.tz_convert(datetime.now().astimezone().tzinfo)
        st.dataframe(df_display.sort_values('timestamp', ascending=False))

if __name__ == "__main__":
    main()
