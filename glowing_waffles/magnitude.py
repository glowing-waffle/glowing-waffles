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
    """
    
    # NOTE: need to do for all stars and use weighted average
    
    v_measured = 0                          # instrumental magnitude of the variable star 
    c_measured = 0                          # instrumental magnitude of the comparison star
    delta_v = v_measured - c_measured       # differential magnitude
    
    c_published = 0                         # published magnitude of the comparison star
    V = delta_v + c_published               # standardized magnitude
    
    return V
