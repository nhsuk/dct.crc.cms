import requests


def get_postcode_region(postcode):
    API_URL = "http://api.postcodes.io/postcodes?q="

    data = requests.get(API_URL + postcode)

    try:
        return data.json().get("result")[0].get("region")
    except: # noqa
        raise Exception(data.json().get("error"))


def get_region(postcode: str):
    baseRegion = get_postcode_region(postcode=postcode)

    regions = {
        "East Midlands": "region.east_midlands",
        "East of England": "region.east_of_england",
        "London": "region.london",
        "North East": "region.north_east",
        "North West": "region.north_west",
        "South East": "region.south_east",
        "South West": "region.south_west",
        "West Midlands": "region.west_midlands",
        "Yorkshire and The Humber": "region.yorkshire_and_humber",
    }

    region = regions.get(baseRegion, "region.other")

    return region
