import numpy as np
from photutils import centroid_com
import ipywidgets as ipw
from astropy.stats import sigma_clipped_stats
from astropy.table import Table
import matplotlib.pyplot as plt
from glowing_waffles.visualization import seeing_plot

__all__ = ['set_keybindings', 'box', 'make_show_event']

out = ipw.Output()
out2 = ipw.Output()
out3 = ipw.Output()


def set_keybindings(image_widget):
    """
    Set image widget keyboard bindings. The bindings are:

    + Pan by click-and-drag or with arrow keys.
    + Zoom by scrolling or using the ``+``/``-`` keys.
    + Adjust contrast by Ctrl-left click and drag; reset with
      shift-right-click.

    Any existing key bindings are removed.

    Parameters
    ----------

    image_widget : astrowidgets.ImageWidget
        Image widget on which to set the key bindings.
    """
    bind_map = image_widget._viewer.get_bindmap()
    # Displays the event map...
    # bind_map.eventmap
    bind_map.clear_event_map()
    bind_map.map_event(None, (), 'ms_left', 'pan')
    bind_map.map_event(None, (), 'pa_pan', 'zoom')

    # bind_map.map_event(None, (), 'ms_left', 'cursor')
    # contrast with right mouse
    bind_map.map_event(None, (), 'ms_right', 'contrast')

    # shift-right mouse to reset contrast
    bind_map.map_event(None, ('shift',), 'ms_right', 'contrast_restore')
    bind_map.map_event(None, ('ctrl',), 'ms_left', 'cursor')

    # Bind +/- to zoom in/out
    bind_map.map_event(None, (), 'kp_+', 'zoom_in')
    bind_map.map_event(None, (), 'kp_=', 'zoom_in')
    bind_map.map_event(None, (), 'kp_-', 'zoom_out')
    bind_map.map_event(None, (), 'kp__', 'zoom_out')

    # Bind arrow keys to panning
    # There is NOT a typo below. I want the keys to move the image in the
    # direction of the arrow
    bind_map.map_event(None, (), 'kp_left', 'pan_right')
    bind_map.map_event(None, (), 'kp_right', 'pan_left')
    bind_map.map_event(None, (), 'kp_up', 'pan_down')
    bind_map.map_event(None, (), 'kp_down', 'pan_up')


def find_center(image, center_guess, cutout_size=30, max_iters=10):
    """
    Find the centroid of a star from an initial guess of its position. Originally
    written to find star from a mouse click.

    Parameters
    ----------

    image : numpy array or CCDData
        Image containing the star.

    center_guess : array or tuple
        The position, in pixels, of the initial guess for the position of
        the star. The coordinates should be horizontal first, then vertical,
        i.e. opposite the usual Python convention for a numpy array.

    cutout_size : int, optional
        The default width of the cutout to use for finding the star.

    max_iters : int, optional
        Maximum number of iterations to go through in finding the center.
    """
    pad = cutout_size // 2
    x, y = center_guess

    # Keep track of iterations
    cnt = 0

    # Grab the cutout...
    sub_data = image[y - pad:y + pad, x - pad:x + pad]  # - med

    # ...do stats on it...
    _, sub_med, _ = sigma_clipped_stats(sub_data)
    # sub_med = 0

    # ...and centroid.
    x_cm, y_cm = centroid_com(sub_data - sub_med)

    # Translate centroid back to original image (maybe use Cutout2D instead)
    cen = np.array([x_cm + x - pad, y_cm + y - pad])

    # ceno is the "original" center guess, set it to something nonsensical here
    ceno = np.array([-100, -100])

    while (cnt <= max_iters and
           (np.abs(np.array([x_cm, y_cm]) - pad).max() > 3
            or np.abs(cen - ceno).max() > 0.1)):

        # Update x, y positions for subsetting
        x = int(np.floor(x_cm)) + x - pad
        y = int(np.floor(y_cm)) + y - pad
        sub_data = image[y - pad:y + pad, x - pad:x + pad]  # - med
        _, sub_med, _ = sigma_clipped_stats(sub_data)
        # sub_med = 0
        mask = (sub_data - sub_med) < 0
        x_cm, y_cm = centroid_com(sub_data - sub_med, mask=mask)
        ceno = cen
        cen = np.array([x_cm + x - pad, y_cm + y - pad])
        if not np.all(~np.isnan(cen)):
            raise RuntimeError('Centroid finding failed, '
                               'previous was {}, current is {}'.format(ceno, cen))
        cnt += 1

    return cen


def make_show_event(iw):
    def show_event(viewer, event, datax, datay):

        i = iw._viewer.get_image()
        data = i.get_data()

        # Location of click in original image
        x = int(np.floor(event.data_x))
        y = int(np.floor(event.data_y))

        cen = find_center(data, (x, y), cutout_size=30)

        # ADD MARKER WHERE CLICKED
        iw.add_markers(Table(data=[[cen[0]], [cen[1]]], names=['x', 'y']))
        # print(foo, moo)

        # CONSTRUCT RADIAL PROFILE OF PATCH AROUND STAR
        yd, xd = np.indices((sub_data.shape))
        r = np.sqrt((xd - foo)**2 + (yd - moo)**2)
        r_exact = r.copy()
        r = r.astype(np.int)
        tbin = np.bincount(r.ravel(), sub_data.ravel())
        rbin = np.bincount(r.ravel(), r_exact.ravel())
        nr = np.bincount(r.ravel())
        radialprofile = tbin / nr
        ravg = rbin / nr
        adjust_max = radialprofile.max() - sub_med
        scaled_profile = (radialprofile - sub_med) / adjust_max
        scaled_exact_counts = (sub_data - sub_med) / adjust_max

        # DISPLAY THE SCALED PROFILE
        out.clear_output(wait=True)
        with out:
            # print(dir(event))
            # print(event.data_x, event.data_y)
            plt.clf()
            # sub_med += med
            seeing_plot(r_exact, scaled_exact_counts, ravg, scaled_profile, 5,
                        'Some Image Name', file_name='some_name', gap=6, annulus_width=13)
            plt.show()

        # CALCULATE AND DISPLAY NET COUNTS INSIDE RADIUS
        out2.clear_output(wait=True)
        with out2:
            tbin2 = np.bincount(r.ravel(), (sub_data - sub_med).ravel())
            counts = np.cumsum(tbin2)
            mag_diff = -2.5 * np.log10(counts / counts.max())
            plt.plot(range(len(radialprofile)), counts)
            plt.xlim(0, 20)
            #plt.ylim(0.2, 0)
            plt.grid()
            sub_blot = sub_data.copy()
            sub_blot[10:30, 10:30] = np.nan
            sub_std = np.nanstd(sub_blot)
            plt.title('Net counts in aperture std {:.2f} med {:.2f}'.format(
                sub_std, sub_med))
            sub_pois = (sub_data - sub_med)
            e_sky = np.sqrt(sub_med)
            rn = 10
            sub_noise_sq = np.sqrt(sub_pois ** 2 + sub_std ** 2) ** 2
            nbin = np.sqrt(np.bincount(r.ravel(), (sub_noise_sq).ravel()))
            plt.xlabel('Aperture radius')
            plt.show()

        # CALCULATE And DISPLAY SNR AS A FUNCTION OF RADIUS
        out3.clear_output(wait=True)
        with out3:
            poisson = np.sqrt(np.cumsum(tbin2))
            error = np.sqrt(poisson ** 2 + np.cumsum(nr)
                            * (e_sky ** 2 + rn ** 2))
            snr = np.cumsum(tbin2) / error
            snr_max = snr[:20].max()
            plt.plot(range(len(radialprofile)), snr)
            plt.title('Signal to noise ratio {}'.format(snr.max()))
            plt.xlim(0, 20)
            # plt.ylim(0, 2)
            plt.xlabel('Aperture radius')
            plt.grid()
            plt.show()
    return show_event


def box(imagewidget):
    big_box = ipw.HBox()
    layout = ipw.Layout(width='20ch')
    hb = ipw.HBox()
    ap_t = ipw.IntText(description='Aperture', value=5, layout=layout)
    in_t = ipw.IntText(description='Inner annulus', value=10, layout=layout)
    out_t = ipw.IntText(description='Outer annulus', value=20, layout=layout)
    hb.children = [ap_t, in_t, out_t]

    lil_box = ipw.VBox()
    lil_box.children = [out, out2, out3]
    big_box.children = [imagewidget, lil_box]
    big_box.layout.width = '100%'
    # Line below puts space between the image and the plots so the plots
    # don't jump around as the image value changes.
    big_box.layout.justify_content = 'space-between'

    return big_box
