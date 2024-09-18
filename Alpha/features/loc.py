import webbrowser, requests
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder

import geocoder
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_current_location():
    g = geocoder.ip('me')
    if g.ok:
        return g.latlng
    else:
        return None

def find_location_and_distance(place):
    current_location = get_current_location()

    if current_location:
        geolocator = Nominatim(user_agent="location_app")

        location = geolocator.geocode(place)

        if location:
            place_location = (location.latitude, location.longitude)

            place_details = geolocator.reverse(place_location, language='en')
            if place_details and place_details.raw.get('address'):
                address = place_details.raw['address']

                city = address.get('city', '')
                state = address.get('state', '')
                country = address.get('country', '')

                place_description = f"{place} exists in {state}, {country}"

                distance = geodesic(current_location, place_location).kilometers
                response = f"{place_description}. The distance from your current location to {place} is {distance:.2f} km."
                return response
            else:
                return f"Sorry, couldn't find detailed location info for {place}."
        else:
            return f"Sorry, couldn't find the location: {place}."
    else:
        return "Couldn't determine your current location."


def my_location():
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_requests = requests.get(url)
    geo_data = geo_requests.json()
    city = geo_data['city']
    state = geo_data['region']
    country = geo_data['country']

    return city, state, country