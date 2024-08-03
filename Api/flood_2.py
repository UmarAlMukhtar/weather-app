import requests
import pandas as pd

# Initialize the Keras REST API endpoint URL
KERAS_REST_API_URL = "http://35.223.122.225:5000/predict"

# Define the date (constant for all requests)
date1 = '2023-01-01'

# Read the coordinates from the CSV file
df_coordinates = pd.read_csv('coordinates.csv')

# Loop through the coordinates and make API requests
for index, row in df_coordinates.iterrows():
    latp = row['latitude']
    longp = row['longitude']
    
    # Prepare the data payload
    mydata = {'date': date1, 'latp': latp, 'longp': longp}
    
    # Submit the request
    r = requests.post(KERAS_REST_API_URL, json=mydata).json()
    
    # Ensure the request was successful
    if r["success"]:
        print(f"Sample {index + 1}: Success")
        print(r["predictions"])
    else:
        print(f"Sample {index + 1}: Request failed")