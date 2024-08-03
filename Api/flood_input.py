# USAGE
# python3 flood_input.py

# import the necessary packages
import requests

# initialize the Keras REST API endpoint URL along with the input
KERAS_REST_API_URL = "http://35.223.122.225:5000/predict"
#Get data from form ans assign to below 3 variables
date1='2023-01-01'
latp=9.847858051091798
longp=76.68516864855208


#don't edit below codes
mydata = {'date': date1,'latp':latp,'longp':longp}
# submit the request
r = requests.post(KERAS_REST_API_URL,json=mydata ).json()

# ensure the request was sucessful
if r["success"]:
        print("Success")
        print(r["predictions"])

# otherwise, the request failed
else:
        print("Request failed")