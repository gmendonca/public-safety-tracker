import requests
import json
import sys
import xml.etree.ElementTree
import webbrowser

pickup_location_1 = "35 W 33rd St, Chicago, IL 60616"
pickup_location_2 = "3241 S Federal St, Chicago, IL 60616"

class PublicSafety():
    def __init__(self, name):
        self.home = "199 E 33rd Blvd, Chicago, IL 60616"
        with open("properties.json") as f:
            self.properties = json.loads(f.read())
        self.name = name
        self.home_latitude, self.home_longtidue = self.get_location(self.home)
        #self.current_latiude, self.current_longtidue = self.get_location(self.home)
        self.current_location = self.home

    def get_location(self, address):
        base_url = "http://geocoder.cit.api.here.com/6.2/geocode.xml"
        pad_app_id = "?app_id="+self.properties['app-id']
        pad_app_code = "&app_code="+self.properties['app-code']
        pad_gen = "&gen=9"
        pad_searchtext = "&searchtext="+address
        url = base_url + pad_app_id + pad_app_code + pad_gen + pad_searchtext
        response = (requests.get(url)).content
        e = xml.etree.ElementTree.fromstring(response)
        position = e.findall("./Response/View/Result/Location/DisplayPosition")
        for child in position:
            latitude = child.find('Latitude').text
            longitude = child.find('Longitude').text
        return (latitude, longitude)

    def car_location(self):
        latitude, longitude = self.get_location(self.current_location)
        return (latitude, longitude)

    def obtain_route(self):
        base_url = "http://route.cit.api.here.com/routing/7.2/calculateroute.json"
        pad_app_id = "?app_id="+self.properties['app-id']
        pad_app_code = "&app_code="+self.properties['app-code']
        curr_lat, curr_long = self.get_location(self.current_location)
        pad_waypoint0 = "&waypoint0=geo!"+curr_lat+","+curr_long
        dest_lat, dest_long = self.get_location(pickup_location_2)
        pad_waypoint1 = "&waypoint1=geo!"+dest_lat+","+dest_long
        mode = "&mode=fastest;car;"
        url = base_url + pad_app_id + pad_app_code + pad_waypoint0 + pad_waypoint1 + mode
        response = (requests.get(url))
        base_url1 = "http://image.maps.cit.api.here.com/mia/1.6/routing"
        poix0 = "&poix0="+curr_lat+","+curr_long+";00a3f2;00a3f2;11;."
        poix1 = "&poix1="+dest_lat+","+dest_long+";white;white;11;."
        markings = "&lc=1652B4&lw=6&t=0&ppi=320&w=400&h=600"
        url1 = base_url1 + pad_app_id + pad_app_code + pad_waypoint0 + pad_waypoint1 + poix0 + poix1+ markings
        webbrowser.open(url1)
        return response.json()
