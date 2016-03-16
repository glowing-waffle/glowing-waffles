

from ccdproc import CCDData
from astropy.stats import sigma_clipped_stats
from photutils import daofind



def source_detection(data):
	    
	mean, median, std = sigma_clipped_stats(data, sigma=3.0, iters=5)    
	return daofind(data - median, fwhm=3.0, threshold=5.*std)
	