import sys, os
from algorithm import download_images, clip_images, calculate_vi

def main() -> int:
    """Main function"""

    url: str = "https://api.spectator.earth/imagery/"
    API_KEY: str = os.getenv('API_KEY')

    # check if API_KEY is present in the environment variables, else raise an Exception
    if API_KEY == None:
        print('API_KEY not present in Environment Variables.')
        raise EnvironmentError("API_KEY not present in Environment Variables.")
        # return 1

    coordinates: list[tuple[float, float]] = [
        (78.029715, 20.583639),
        (78.044536, 20.584024),
        (78.043671, 20.571318),
        (78.031456, 20.572034)
    ]

    image_present: bool = download_images.check_images_with_coordinates(url, API_KEY, coordinates)

    # print(image_present)

    if image_present:
        results: list = download_images.get_image_results_with_coordinates(url, API_KEY, coordinates)

        selected_result: dict = download_images.select_image(results, 0)

        # downloading 4th band
        band4_name: str = 'B04.jp2'
        band4_name: str = download_images.download_band_image(selected_result, 3, API_KEY)

        # downloading 8th band
        band8_name: str = 'B08.jp2'
        band8_name: str = download_images.download_band_image(selected_result, 7, API_KEY)

        print("BOTH THE IMAGES DOWNLOADED")

        # NOTE: Converting jp2 to tif format for clipping
        band4_converted: str = 'B04.tif'
        band4_converted: str = clip_images.convert_jp2_2_tif(band4_name)

        band8_converted: str = 'B08.tif'
        band8_converted: str = clip_images.convert_jp2_2_tif(band8_name)

        print("BOTH IMAGES CONVERTED FROM JP2 TO TIF")

        band4_clipped: str = 'clipped_B04.tif'
        band4_clipped: str = clip_images.clip_image(band4_converted, coordinates)

        band8_clipped: str = 'clipped_B08.tif'
        band8_clipped: str = clip_images.clip_image(band8_converted, coordinates)

        print("BOTH IMAGE CLIPPED")

        calculate_vi.calculate_ndvi(band4_clipped, band8_clipped)

        print("CALCULATED NDVI")

    return 0

if __name__ == "__main__":
    sys.exit(main())