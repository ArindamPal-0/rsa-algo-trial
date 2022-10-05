"""
# download_images.py

This module implements the functionality to check and download satellite images given coordinates.

## functions:
- get_image_with_coordinates
- check_images_with_coordinates
- select_image
- download_band_image
"""

from shapely import geometry
import requests

from pprint import pprint

# TODO: add pydantic validation to the function params

def get_image_results_with_coordinates(url: str, api_key: str, coordinates: list[tuple[int, int]], date_from: str = '2022-02-10', cc_less_than: str = '20.00') -> list:
    # creating `shapely.geometry.Polygon` from the given coordinates
    coordinatesPolygon: geometry.Polygon = geometry.Polygon(coordinates)

    params = {
        'api_key': api_key,
        'geometry': coordinatesPolygon,
        'cc_less_than': cc_less_than,
        'date_from': date_from
    }

    response = requests.get(url, params=params)
    data = response.json()


    if response.status_code != 200:
        if 'results' not in data:
            pprint(data, indent=2)
            print('ERROR in response from api.')
            raise Exception("ERROR in response from api")
        
        pprint(data, indent=2)
        print('Some Error Occured')
        raise Exception('Some Error Occured')

    results: list = data['results']

    return results

def check_images_with_coordinates(url: str, api_key: str, coordinates: list[tuple[int, int]], date_from: str = '2022-02-10', cc_less_than: str = '20.00') -> bool:
    """
    # check_images_with_coordinates

    Checks if any satellite image of the given coordinates is present via the api.

    ### @params
    - url
        - type: str
        - desc: api url
        - eg: `https://api.spectator.earth/imagery/`
    - coordinates 
        - type: list[tuple[int, int]]
        - desc: it is list of tuples containing longitude and latitude, i.e. `[(lon, lat), ...]`
        - eg: `[
            (78.029715, 20.583639),
            (78.044536, 20.584024),
            (78.043671, 20.571318),
            (78.031456, 20.572034)
        ]`

    ### @return
    - image_present
        - type: bool
        - desc: tells if any result is obtained, true if yes otherwise false

    """

    results: list = get_image_results_with_coordinates(url, api_key, coordinates, date_from, cc_less_than)

    # print(len(results))

    image_present: bool = len(results) > 0

    return image_present

def select_image(results: list, index: int) -> dict:
    return results[index]

def download_band_image(selected_result: dict, band_index: int, api_key: str) -> None:
    # get download url
    download_url: str = selected_result['download_url']
    print(download_url)

    # request for available band images
    apikey_param = {'api_key': api_key}
    selected_result_response = requests.get(download_url, params=apikey_param)
    selected_result_data = selected_result_response.json()


    # TODO: Check if the said band exists

    # select the appropriate band image
    band_image = selected_result_data[band_index]

    # print image description
    print(f"name: {band_image['name']}")
    print(f"path: {band_image['path']}")
    print(f"size: {band_image['size']}")

    # get the image url
    band_url = f"{download_url}{band_image['path']}"
    print(band_url)

    # download the image content
    apikey_param = {'api_key': api_key}
    band_response = requests.get(band_url, params=apikey_param)
    band_image_data = band_response.content

    # check if download successful
    if len(band_image_data) != band_image['size']:
        raise Exception("Download failed!")

    # save the image to file appropriately named
    with open(band_image['name'], 'wb') as file:
        file.write(band_image_data)