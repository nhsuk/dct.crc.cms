import requests


class PostcodeException(Exception):
    pass


def get_postcode_data(postcode):
    API_URL = "https://api.postcodes.io/postcodes?q="

    data = requests.get(API_URL + requests.utils.quote(postcode, safe=""))
    if data.status_code != 200:
        raise PostcodeException(
            "Postcode request failed %s (%s)" % (data.status_code, data.text)
        )

    try:
        response = data.json()
        result = response.get("result")
        if not result or len(result) == 0:
            raise PostcodeException("Postcode not found")
        return result[0]
    except PostcodeException:
        raise
    except Exception as e:
        raise PostcodeException(
            "Failed to retrieve postcode '%s' - not a valid JSON response '%s' (%s)"
            % (postcode, data.text, e)
        )


def get_postcode_region(postcode):
    try:
        response = get_postcode_data(postcode)
        return response.get("region")
    except Exception as e:
        raise PostcodeException(
            "Failed to retrieve postcode region '%s' (%s)" % (postcode, e)
        )


def get_region(postcode: str):
    base_region = get_postcode_region(postcode=postcode)

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

    region = regions.get(base_region, "region.other")

    return region
