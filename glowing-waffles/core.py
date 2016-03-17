from __future__ import print_function, division, absolute_import


# IMPORTS ARE MISSING AND WILL NEED TO BE ADDED.

def photutils_stellar_photometry(ccd_image, coords, aperture_radius,
                                 who_knows):
    """
    Perform aperture photometry on an image, with a few options for estimating
    the local background from an annulus around the aperture.
    """

    # NOTE: THIS MAY NEED TO BE BROKEN UP INTO SMALLER FUNCTIONS.

    # Create aperture and annulus objects from the coordinates.

    # Perform aperture photometry at all of the coordinates.

    # Perform photometry on the annulus and...
    # ...get the list of pixels in the annulus.

    # Filter the list based on argument provided to reject outliers.

    # Get value of the "typical" background pixel. User should have options for
    # doing this, I suppose, though the default should be the median.

    # Subtract the background from the aperture flux.

    # Return a table that includes at least:
    #   + ra, dec of center
    #   + x, y of center
    #   + flux
    #   + sky background per pixel
    #   + aperture radius used
    #   + annulus radius used
    #   + flux error
    pass
