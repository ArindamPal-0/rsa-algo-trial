"""
# clip_images

### functions:
- convert_jp2_2_tif
- clip_image
"""

from email.mime import image
import rasterio
from rasterio import warp, mask
from shapely import geometry
# from pprint import pprint


def convert_jp2_2_tif(image_name: str) -> str:
    """
        Convert image from jp2 to tif format and returns the converted image name.
    """
    dst_crs = 'EPSG:4326'
    with rasterio.open(image_name) as image:
        # pprint([*image.bounds])
        transform, width, height = warp.calculate_default_transform(image.crs, dst_crs, 
            image.width, image.height, *image.bounds)

        # props = properties or key value pairs
        kwargs = image.meta.copy()
        # pprint(kwargs, indent=2)

        # kwargs.update({'crs': dst_crs, 'transform': transform, 'width': width, 'height': height})
        kwargs['crs'] = dst_crs
        kwargs['transform'] = transform
        kwargs['width'] = width
        kwargs['height'] = height

        # pprint(kwargs, indent=2)

        # dst_filename = 'B04.tif'
        dst_filename: str = '.'.join(image_name.split('.')[:-1]) + '.tif'
        print(dst_filename)

        with rasterio.open(dst_filename, 'w', **kwargs) as dst:

            for j in range(1, image.count + 1):
                warp.reproject(
                    source=rasterio.band(image, j),
                    destination=rasterio.band(dst, j),
                    src_transform=image.transform,
                    src_crs=image.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=warp.Resampling.nearest
                )

        return dst_filename

def clip_image(image_name: str, coordinates: list[tuple[float, float]]) -> str:
    """
        Clipping the satellite image according to required coordinates and returns clipped image name.
    """
    coordinatesPolygon: geometry.Polygon = geometry.Polygon(coordinates)
    shapes = [geometry.mapping(coordinatesPolygon)]

    with rasterio.open(image_name) as src:
        clipped_image, clipped_image_transform = mask.mask(src, shapes, crop=True)

        clipped_image_meta = src.meta
        clipped_image_meta.update({
            'driver': 'GTiff',
            'height': clipped_image.shape[1],
            'width': clipped_image.shape[2],
            'transform': clipped_image_transform
        })

        dst_image: str = 'clipped_' + image_name
        with rasterio.open(dst_image, 'w', **clipped_image_meta) as dst:
            dst.write(clipped_image)

        return dst_image