from __future__ import print_function, division

import numpy as np

from astroquery.vizier import Vizier

from astropy.coordinates import SkyCoord
from astropy.table import Table
import astropy.units as units

from itertools import izip

from ccdproc import CCDData

def scale_and_downsample(data, downsample=4, min_percent=20, max_percent=99.5):

    scaled_data = scale_image(data, min_percent=min_percent, max_percent=max_percent)

    if downsample > 1:
        scaled_data = block_reduce(scaled_data, block_size=(downsample, downsample))
    return scaled_data

def in_frame(frame_wcs, coordinates):
    """
    Description:Check which of a set of coordinates are in the footprint of
    the WCS of an image
    Preconditions:
    Postconditions:
    """
    x, y = frame_wcs.all_world2pix(coordinates.ra, coordinates.dec, 0)
    in_x = (x >= 0) & (x <= frame_wcs._naxis1)
    in_y = (y >= 0) & (y <= frame_wcs._naxis2)
    return in_x & in_y

def catalog_search(frame_wcs, shape, desired_catalog, raheader, decheader, rad = 0.5):
    """
    Description: This function takes coordinate data from an image and a 
    catalog name and returns the positions of those stars.
    Preconditions:frame_wcs is a WCS object, shape is tuple, list or array of
    numerical values, desired_catalog is a string and radius is a numerical 
    value.
    Postconditions:
    """
    rad = rad*units.deg
    #Find the center of the frame
    center_coord = frame_wcs.all_pix2world([[shape[1]/2, shape[0]/2]], 0)
    center = SkyCoord(center_coord, frame='icrs', unit='deg')
    
    #Get catalog via cone search
    Vizier.ROW_LIMIT = -1   #Set row_limit to have no limit
    cat = Vizier.query_region(center, radius=rad, catalog=desired_catalog)
    cat = cat[0] #Vizier always returns list even if there is only one element. Grab that element.
    cat_coords = SkyCoord(ra=cat[raheader], dec=cat[decheader])
    in_fov = in_frame(frame_wcs, cat_coords)
    x, y = frame_wcs.all_world2pix(cat_coords.ra, cat_coords.dec, 0)
    return (cat[in_fov], x[in_fov], y[in_fov])