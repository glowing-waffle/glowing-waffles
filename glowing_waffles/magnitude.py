from numpy import size

__all__ = ['aavso']

def aavso(variable_star, comparison_stars):
    """
    Perform AAVSO-style differential photometry calcuation
    on a selected star, and an array of other stars.
    ----------
    variable_star : a np.ndarray
        A numpy array of variable star information.
    comparison_stars : a np.ndarray
        A numpy array of extracted comparison stars. 
        Assumed to not contain variable star.
    Returns
    The AAVSO-style differential photometric value.
    """
    
    v_measured = variable_star.getmagnitude()     # instrumental magnitude of the variable star 
    
    weighted_std_mag = 0                          # start at 0, increment each time
    
    # compare to all comparision stars
    for star_info in comparison_stars:
        c_measured = star_info.getmagnitude()     # instrumental magnitude of the comparison star
        delta_v = v_measured - c_measured         # differential magnitude
        
        # somehow calculate and include a weight ??
        weight = 1
        
        c_published = 0                             # published magnitude of the comparison star
        V = delta_v + c_published                   # standardized magnitude
        weighted_std_mag += V * weight              # weight each magnitude
        
    weighted_std_mag / comparison_stars.size        # averaging weights
    
    return weighted_std_mag
