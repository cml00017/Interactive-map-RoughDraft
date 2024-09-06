import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set State ranges for zoom feature
STATE_BOUNDS = {
    "Alabama": {"lat_range": [30.1, 35.0], "lon_range": [-88.5, -84.9]},
    "Arizona": {"lat_range": [31.3, 37.0], "lon_range": [-114.8, -109.0]},
    "Arkansas": {"lat_range": [33.0, 36.5], "lon_range": [-94.6, -89.6]},
    "California": {"lat_range": [32.5, 42.0], "lon_range": [-124.5, -114.1]},
    "Colorado": {"lat_range": [36.9, 41.0], "lon_range": [-109.1, -102.0]},
    "Connecticut": {"lat_range": [40.9, 42.1], "lon_range": [-73.7, -71.8]},
    "Delaware": {"lat_range": [38.5, 39.8], "lon_range": [-75.8, -75.0]},
    "Florida": {"lat_range": [24.4, 31.0], "lon_range": [-87.6, -80.0]},
    "Georgia": {"lat_range": [30.4, 35.0], "lon_range": [-85.6, -80.8]},
    "Idaho": {"lat_range": [42.0, 49.0], "lon_range": [-117.2, -111.0]},
    "Illinois": {"lat_range": [36.9, 42.5], "lon_range": [-91.5, -87.5]},
    "Indiana": {"lat_range": [37.8, 41.8], "lon_range": [-88.1, -84.8]},
    "Iowa": {"lat_range": [40.4, 43.5], "lon_range": [-96.6, -90.1]},
    "Kansas": {"lat_range": [36.9, 40.0], "lon_range": [-102.1, -94.6]},
    "Kentucky": {"lat_range": [36.5, 39.1], "lon_range": [-89.6, -81.9]},
    "Louisiana": {"lat_range": [28.9, 33.0], "lon_range": [-94.0, -88.8]},
    "Maine": {"lat_range": [43.0, 47.5], "lon_range": [-71.1, -66.9]},
    "Maryland": {"lat_range": [37.9, 39.7], "lon_range": [-79.5, -75.0]},
    "Massachusetts": {"lat_range": [41.2, 42.9], "lon_range": [-73.5, -69.9]},
    "Michigan": {"lat_range": [41.7, 48.3], "lon_range": [-90.4, -82.4]},
    "Minnesota": {"lat_range": [43.5, 49.4], "lon_range": [-97.2, -89.5]},
    "Mississippi": {"lat_range": [30.2, 35.0], "lon_range": [-91.6, -88.0]},
    "Missouri": {"lat_range": [35.9, 40.6], "lon_range": [-95.8, -89.1]},
    "Montana": {"lat_range": [44.4, 49.0], "lon_range": [-116.1, -104.0]},
    "Nebraska": {"lat_range": [39.8, 43.0], "lon_range": [-104.1, -95.3]},
    "Nevada": {"lat_range": [35.0, 42.0], "lon_range": [-120.0, -114.0]},
    "New Hampshire": {"lat_range": [42.7, 45.3], "lon_range": [-72.6, -70.7]},
    "New Jersey": {"lat_range": [38.9, 41.4], "lon_range": [-75.6, -73.9]},
    "New Mexico": {"lat_range": [31.3, 37.0], "lon_range": [-109.0, -103.0]},
    "New York": {"lat_range": [40.5, 45.1], "lon_range": [-79.8, -71.9]},
    "North Carolina": {"lat_range": [33.8, 36.6], "lon_range": [-84.3, -75.5]},
    "North Dakota": {"lat_range": [45.9, 49.0], "lon_range": [-104.1, -96.6]},
    "Ohio": {"lat_range": [38.4, 41.9], "lon_range": [-84.8, -80.5]},
    "Oklahoma": {"lat_range": [33.6, 37.0], "lon_range": [-103.0, -94.4]},
    "Oregon": {"lat_range": [41.9, 46.3], "lon_range": [-124.6, -116.5]},
    "Pennsylvania": {"lat_range": [39.7, 42.3], "lon_range": [-80.5, -74.7]},
    "Rhode Island": {"lat_range": [41.1, 42.0], "lon_range": [-71.9, -71.1]},
    "South Carolina": {"lat_range": [32.0, 35.2], "lon_range": [-83.4, -78.5]},
    "South Dakota": {"lat_range": [42.4, 45.9], "lon_range": [-104.1, -96.4]},
    "Tennessee": {"lat_range": [34.9, 36.7], "lon_range": [-90.4, -81.6]},
    "Texas": {"lat_range": [25.8, 36.5], "lon_range": [-106.6, -93.5]},
    "Utah": {"lat_range": [36.9, 42.0], "lon_range": [-114.1, -109.0]},
    "Vermont": {"lat_range": [42.7, 45.0], "lon_range": [-73.5, -71.5]},
    "Virginia": {"lat_range": [36.5, 39.5], "lon_range": [-83.7, -75.2]},
    "Washington": {"lat_range": [45.5, 49.0], "lon_range": [-124.8, -116.9]},
    "West Virginia": {"lat_range": [37.2, 40.6], "lon_range": [-82.7, -77.7]},
    "Wisconsin": {"lat_range": [42.5, 47.1], "lon_range": [-92.9, -86.2]},
    "Wyoming": {"lat_range": [40.9, 45.0], "lon_range": [-111.0, -104.0]}
}

STATE_ABBREVIATIONS = {
    "Alabama": "AL", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
    "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY",
    "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}


def data_load(data):
    return pd.read_csv(data)


def main():
    df = data_load('USPopulations.csv')

    # Rename columns for easier referencing
    df.rename(columns={
        "LONG": "lon",
        "LAT": "lat",
        "2022_POPULATION": "population",
        "CITY": "city",
        "STATE": "state_name"
    }, inplace=True)

    df['state_abbreviation'] = df['state_name'].map(STATE_ABBREVIATIONS)

    st.title("Population Map Visualization")

    # Dropdown menu for selecting multiple states or the entire US
    state_options = ["United States"] + df['state_name'].unique().tolist()
    selected_states = st.multiselect("Select United States or States", state_options, default=["United States"])

    if "United States" in selected_states and len(selected_states) == 1:
        # Group by state and sum population
        state_data = df.groupby('state_abbreviation', as_index=False)['population'].sum()

        # Create a state-level choropleth map
        fig = px.choropleth(
            state_data,
            locations='state_abbreviation',
            locationmode='USA-states',
            color='population',
            hover_name='state_abbreviation',
            hover_data=['population'],
            scope='usa',
            color_continuous_scale="Bluered",  # Blue to Red color scale
            labels={'population': 'Population'},
            title="State-level Population For Contiguous United States"
        )

        # Update layout to increase map size
        fig.update_layout(
            width=1200,  # Set the width of the map
            height=700,  # Set the height of the map
        )

        # Display the map
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("State Population Data")
        st.dataframe(state_data)

    else:
        # Filter the data to only the selected states
        city_data = df[df['state_name'].isin(selected_states)]
        city_data['city'].replace({' town': '', ' city': ''}, regex=True, inplace=True)
        city_data['log_population'] = np.log10(city_data['population'])

        min_population, max_population = st.slider("Select Population Range",
            min_value=int(city_data['population'].min()),
            max_value=int(city_data['population'].max()),
            value=(int(city_data['population'].min()), int(city_data['population'].max()))
        )
        city_data = city_data[(city_data['population'] >= min_population) & (city_data['population'] <= max_population)]

        # Adjust bounds for multiple states
        lat_range = [min(city_data['lat']), max(city_data['lat'])]
        lon_range = [min(city_data['lon']), max(city_data['lon'])]

        # Create a city-level scatter plot map
        fig = px.scatter_geo(
            city_data,
            lat='lat',
            lon='lon',
            hover_name='city',
            hover_data=['state_name', 'population'],
            size='population',
            size_max=25,
            color='log_population',
            color_continuous_scale="Bluered",  # Blue to Red color scale
            scope='usa',
            title=f"City-level Population in {', '.join(selected_states)}"
        )
        fig.update_geos(
            fitbounds="locations",  # Fit to the bounds of the selected states
            projection_scale=8,  # Adjust the zoom level
            lataxis_range=lat_range,  # Zoom to the latitude range of selected states
            lonaxis_range=lon_range  # Zoom to the longitude range of selected states
        )

        # Update layout to increase map size
        fig.update_layout(
            width=1200,  # Set the width of the map
            height=700,  # Set the height of the map
        )

        # Display the city-level map
        st.plotly_chart(fig, use_container_width=True)
        st.subheader(f"City Population Data for {', '.join(selected_states)}")
        st.dataframe(city_data[['city', 'state_name', 'population']])


if __name__ == "__main__":
    main()


