__all__ = ['aavso']

def aavso(ccd_image, sources, variable_star):
    """
    Perform AAVSO-style differential photometry, with a few options for estimating
    the local background from an annulus around the aperture.
    ----------
    ccd_image : `~ccdproc.CCDData`, a np.ndarray
        Image on which to perform aperture photometry.
    sources : `~astropy.table.Table`
        Table of extracted sources. Assumed to be the output of
        `~photutils.daofind()` source extraction function. Assumed to not contain variable star.
    variable_star:_______ information for the variable start
        _____
    Returns
    The AAVSO-style differential photometric value.
    ???
    """
    
    # step 1 -Check your images 
    # step 2 - Identify the stars -> psf plot? NOTE: done in source_detection.py
    # step 3 - Set the aperture NOTE: done in photometry.py
    # step 4 - Choose the check and comparison stars to use 
    # step 5 - Measure the magnitude -> Δv = v_measured - c_measured (differential magnitude)
    #                               -> V = Δv + C_published           (standardized magnitude)
    #       - compare one–by–one the variable star with each comparison star # NOTE: how do I get the star that we want?
    #       -  return the results as a weighted average of all these values
    # step 6 - Determine the uncertainty 
    #       - σ = ( (Σ(x_i- x)2)/ (N-1) )1/2
    #       S/N = N_ADU×G / ( (N_ADU×G) + npix×( (N_ADU,sky×G)+N_dark+(N_r.n.)2) )1/2
