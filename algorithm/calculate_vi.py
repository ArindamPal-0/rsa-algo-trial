"""
# calculate_vi

### functions:
- calculate_ndvi
"""
import rasterio
import numpy as np
import imageio

def calculate_ndvi(band4_imagename: str, band8_imagename: str) -> None:
    bands: list[str] = [band4_imagename, band8_imagename]
    full_image: list = [
        rasterio.open('clipped_B04.tif', 'r', driver='GTiff').read(),
        rasterio.open('clipped_B08.tif', 'r', driver='GTiff').read()
    ]

    raster_img_f4: list = [image.astype('f4') for image in full_image]

    ndvi_clipped = np.divide(np.subtract(raster_img_f4[0], raster_img_f4[1]), np.add(raster_img_f4[0], raster_img_f4[1]))

    ndvi_array = np.squeeze(ndvi_clipped)

    # saving it into an image file
    # TODO: Change this image saving technique
    imageio.imwrite('ndvi_image.png', ndvi_array)
