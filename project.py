import streamlit as st
import requests
import googlemaps
import numpy as np
from datetime import datetime
from IPython.display import IFrame, display
from googlemaps.exceptions import ApiError

# Function to create sections
def section_context():
    st.title("Improving Transportation: Understanding Commuter Decision-Making")
    st.header("Context (heading 1)")
    st.write("I’m a consultant hired by the council that aims to improve transportation and understand the decision-making of the population when it comes to commute. So the")

def section_data_collection():
    st.header("Data Collection and Data Cleaning (heading 1)")

    ## Survey (heading 2)
    st.subheader("Survey")
    st.write("Number of respondents: 84")
    
    ## Demographic Information (age, income, occupation, residential area)
    st.subheader("Demographic Information")
    st.write("- Age\n- Income\n- Occupation\n- Residential area")

    ## Transportation Information: commute duration and frequency
    st.subheader("Transportation Information")
    st.write("Commute duration and frequency")

    ## Transportation Mode Questions (Primary and Secondary mode of transportation, rental car use)
    st.subheader("Transportation Mode Questions")
    st.write("- Primary mode of transportation\n- Secondary mode of transportation\n- Rental car use")

    ## Environmental Awareness and Behavior (Environmental Concern, factors considered in transportation, Willingness to Switch and to try new methods of transportation
    st.subheader("Environmental Awareness and Behavior")
    st.write("- Environmental Concern\n- Factors considered in transportation\n- Willingness to Switch\n- Willingness to try new methods of transportation")

    ## Weather Impact (how weather affects the mode of transportation, change of transportation based on weather
    st.subheader("Weather Impact")
    st.write("- How weather affects the mode of transportation\n- Change of transportation based on weather")

    ## Data cleaning (heading 2)
    st.subheader("Data cleaning")
    st.write("Convert categorical answers into numerical (E.g How frequently do you use public transportation, income interval turned into middle income)")

def section_eda():
    st.header("EDA and Statistical analysis (heading 1)")

    ## Correlation matrix to explore relationship between variables with Pearson coefficient
    st.subheader("Correlation matrix")
    correlation_matrix = data.corr()
    st.write(correlation_matrix)

    ## Visualizations to explore relationships between different variables
    st.subheader("Visualizations")
    # You can add visualizations here using st.pyplot or other Streamlit visualization features.

    ## Trends and factors into -> ANOVA, we look for p-value of 5% since we propose recommendations to seek for transportation improvements
    st.subheader("Trends and factors into -> ANOVA")
    st.write("We look for p-value of 5% since we propose recommendations to seek for transportation improvements.")
    # Perform ANOVA and interpret results based on your analysis.

def section_main_insights():
    st.header("Main insights (heading 1)")
    # Add your main insights here based on the analyses conducted.


# Utility functions
def get_api_key(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

def calculate_co2_emissions(start_lat, start_lng, end_lat, end_lng, mode):
    # Haversine formula to calculate the distance between two points on the earth
    R = 6371  # radius of the Earth in kilometers
    dLat = np.radians(end_lat - start_lat)
    dLon = np.radians(end_lng - start_lng)
    a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(np.radians(start_lat)) * np.cos(np.radians(end_lat)) * np.sin(dLon / 2) * np.sin(dLon / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c

    # CO2 emissions per passenger kilometer (in grams)
    if mode == 'driving':
        co2_emission = 160
    elif mode == 'transit':  # assuming transit means bus
        co2_emission = 70
    elif mode in ['walking', 'bicycling']:
        co2_emission = 0  # negligible emissions

    # Total CO2 emissions for the journey (in grams)
    total_co2_emission = distance * co2_emission

    return total_co2_emission

def get_weather_info(lat, lon, api_key):
    # OpenWeatherMap API endpoint for current weather
    endpoint = "https://api.openweathermap.org/data/2.5/weather"

    # Parameters for the API request
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',  # Use metric units for temperature
    }

    # Make the API request
    response = requests.get(endpoint, params=params)
    weather_data = response.json()

    # Check if 'main' key is present in weather_data
    if 'main' in weather_data:
        # Extract relevant weather information
        weather_info = {
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity'],
        }

        return weather_info
    else:
        print(f"Error: Could not retrieve weather information for coordinates ({lat}, {lon}).")
        return None

def ask_transportation_preference():
    print("\nSelect your preferred mode of transportation:")
    print("1. Driving")
    print("2. Transit (public transportation route)")
    print("3. Walking")
    print("4. Cycling")

    choice = input("Enter the number corresponding to your choice: ")

    transportation_modes = {
        '1': 'driving',
        '2': 'transit',
        '3': 'walking',
        '4': 'bicycling'
    }

    return transportation_modes.get(choice, 'driving')

def display_map(map_url):
    display(IFrame(src=map_url, width=800, height=600))

# Function for the route planning section
# Function for the route planning section
def section_route_planning(gmaps):
    st.header("Route Planning for Traveling 🌎")

    start_point = st.text_input("Enter starting point:")
    destination = st.text_input("Enter destination:")

    # Your route planning logic goes here

    if st.button("Plan Route"):
        # Get user input for starting point and destination
        try:
            start_point_geocode = gmaps.geocode(start_point)
            start_point_location = start_point_geocode[0]['geometry']['location']
            start_location = {'lat': start_point_location['lat'], 'lng': start_point_location['lng']}
        except (IndexError, KeyError, ApiError) as e:
            st.error(f"Error: Could not retrieve location information for starting point {start_point}.")
            return

        # Get user input for destination
        try:
            destination_geocode = gmaps.geocode(destination)
            destination_location = destination_geocode[0]['geometry']['location']
            end_location = {'lat': destination_location['lat'], 'lng': destination_location['lng']}
        except (IndexError, KeyError, ApiError) as e:
            st.error(f"Error: Could not retrieve location information for destination {destination}.")
            return

        # Other inputs and processing...

        # Get air quality information
        # Replace with your API keys
        openweathermap_api_key = get_api_key("openweathermap_secrets.txt")
        air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={start_location['lat']}&lon={start_location['lng']}&appid={openweathermap_api_key}"
        air_quality_response = requests.get(air_quality_url)
        air_quality_data = air_quality_response.json()
        if 'list' in air_quality_data:
            air_quality_index = air_quality_data['list'][0]['main']['aqi']
            air_quality_meaning = {
                1: 'Good 🟢',
                2: 'Fair 🟡',
                3: 'Moderate 🟠',
                4: 'Poor 🟤',
                5: 'Very Poor 🔴'
            }
            st.write("\nFind below the current meteorological conditions before choosing your method of transportation ")
            st.write(f"\nThe Air Quality Index: {air_quality_index} ({air_quality_meaning.get(air_quality_index, 'Unknown')})")

        # Get weather information
        weather_info = get_weather_info(start_location['lat'], start_location['lng'], openweathermap_api_key)

        # Display weather conditions
        if weather_info:
            st.write('\nWeather Conditions:')
            st.write(f"Temperature: {weather_info['temperature']}°C")
            st.write(f"Description: {weather_info['description']}")
            st.write(f"Humidity: {weather_info['humidity']}%")

        # Ask for transportation mode using a dropdown
        transportation_mode = st.selectbox("Select your preferred mode of transportation:", ["Driving", "Transit", "Walking", "Cycling"])

        # Map transportation mode to corresponding mode for calculations
        mode_mapping = {
            "Driving": "driving",
            "Transit": "transit",
            "Walking": "walking",
            "Cycling": "bicycling"
        }

        selected_mode = mode_mapping.get(transportation_mode, "driving")

        # Calculate CO2 emissions based on the chosen transportation mode
        total_co2_emission = calculate_co2_emissions(
            start_location['lat'], start_location['lng'], end_location['lat'], end_location['lng'], mode=selected_mode
        )

        st.write(f"\nCO2 Emission: {total_co2_emission} g")

        R = 6371  # radius of the Earth in kilometers
        dLat = np.radians(end_location['lat'] - start_location['lat'])
        dLon = np.radians(end_location['lng'] - start_location['lng'])
        a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(np.radians(start_location['lat'])) * np.cos(
            np.radians(end_location['lat'])) * np.sin(dLon / 2) * np.sin(dLon / 2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c

        # Check air quality, distance, and weather conditions
        if (
            air_quality_index in [1, 2, 3]
            and distance < 10
            and ('clouds' in weather_info['description'].lower() or 'clear sky' in weather_info['description'].lower())
        ):
            st.write("\nGiven the good weather conditions and short distance, would you consider changing your mode of transport to biking or walking?")
            reconsider_choice = st.selectbox("(Yes/No):", ["Yes", "No"]).lower()

            if reconsider_choice == 'yes':
                # Ask for transportation mode using a dropdown
                transportation_mode = st.selectbox("Select your preferred mode of transportation:", ["Driving", "Transit", "Walking", "Cycling"])

                # Map transportation mode to corresponding mode for calculations
                selected_mode = mode_mapping.get(transportation_mode, "driving")

                # Recalculate CO2 emissions based on the newly chosen transportation mode
                total_co2_emission = calculate_co2_emissions(
                    start_location['lat'], start_location['lng'], end_location['lat'], end_location['lng'], mode=selected_mode
                )
                st.write(f"\nCO2 Emission: {total_co2_emission} g")

        # Ask the user if they want to proceed with the route
        proceed = st.text_input("\nDo you want to proceed with the route and get the itinerary? (Yes/No):").lower()

        # If the user chooses to proceed, open the map in the default web browser
        if proceed == 'yes':
            map_url = f"https://www.google.com/maps/dir/?api=1&origin={start_point}&destination={destination}&travelmode={selected_mode}"
            display_map(map_url)

# Sidebar navigation
sections = {
    "Context": section_context,
    "Data Collection": section_data_collection,
    "EDA and Analysis": section_eda,
    "Main Insights": section_main_insights,
    "Route Planning": section_route_planning,  # New section for route planning
}

# Display the selected section based on the button clicked
selected_section = st.sidebar.radio("Select Section", list(sections.keys()))
sections[selected_section](gmaps)  # Pass the gmaps object to the selected section function


# Sidebar navigation
sections = {
    "Context": section_context,
    "Data Collection": section_data_collection,
    "EDA and Analysis": section_eda,
    "Main Insights": section_main_insights,
    "Route Planning": section_route_planning,  # New section for route planning
}

# Google Maps API key
google_maps_api_key = get_api_key("google_maps_secrets.txt")
gmaps = googlemaps.Client(key=google_maps_api_key)

# Display the selected section based on the button clicked
selected_section = st.sidebar.radio("Select Section", list(sections.keys()))
sections[selected_section](gmaps)  # Pass the gmaps object to the selected section function
