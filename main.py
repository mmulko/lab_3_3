from flask import Flask, render_template, request
import requests
import folium
from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    key = request.form.get("domain")
    start_coords = (46.2276, 2.2137)
    folium_map = folium.Map(location=start_coords, zoom_start=3)
    f_json = get_json(name, key)
    num = len(f_json['users'])
    for user in range(num - 1):
        if len(list(f_json['users'][user]["location"])) < 1:
            continue
        else:
            f_name = f_json['users'][user]["screen_name"]
            f_loc = f_json['users'][user]["location"]
            geolocator = Nominatim(user_agent="mmulko")
            try:
                time.sleep(1)
                location = geolocator.geocode(f_loc)
                if location is None:
                    cord = "None"
                else:
                    cord = [location.latitude, location.longitude]
            except GeocoderTimedOut:
                cord = "None"
            if cord == "None":
                continue
            else:
                folium_map.add_child(folium.Marker(location=cord, popup=f_name,
                                                   icon=folium.Icon(
                                                       icon='user')))
    return folium_map._repr_html_()


def get_json(key, name):
    base_url = "https://api.twitter.com/"
    access_token = key
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    search_params = {
        'screen_name': name
    }
    search_url = '{}1.1/friends/list.json'.format(base_url)
    response = requests.get(search_url, headers=search_headers,
                            params=search_params)
    json_response = response.json()
    return json_response


if __name__ == "__main__":
    app.run(debug=True)
