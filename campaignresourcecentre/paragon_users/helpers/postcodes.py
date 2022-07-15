import requests


def get_postcode_region(postcode):

    API_URL = "https://api.postcodes.io/postcodes?q="

    data = requests.get(API_URL + requests.utils.quote(postcode, safe=""))
    if data.status_code != 200:
        raise Exception(
            "Postcode request failed %s (%s)" % (data.status_code, data.text)
        )

    try:
        response = data.json()
    except Exception as e:
        raise Exception(
            "Failed to retrieve postcode '%s' - not a valid JSON response '%s' (%s)"
            % (postcode, data.text, e)
        )

    try:
        return response.get("result")[0].get("region")
    except Exception as e:  # noqa
        raise Exception(
            "Failed to retrieve postcode region '%s' (%s)" % (postcode, data.text)
        )


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
