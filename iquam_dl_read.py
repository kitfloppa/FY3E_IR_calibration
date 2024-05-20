#!/usr/bin/env python3

"""
Created on Tue Oct 13 12:26:53 2020

@author: haifeng zhang; haifeng.zhang@noaa.gov

This script is to download and read iQuam NetCDF format files,
and then plot the spatial distribution of the monthly SST field.

Usage:
iquam_dl_read_v2.py [options]

Options:
--ftp_folder=<ftp_folder>   ftp folder to check for iQuam files
                            [Default: ftp://ftp.star.nesdis.noaa.gov/pub/sod/sst/iquam/v2.10/]
--input_file=<filename>     iQuam file to be downloaded
                            [Default: 202009-STAR-L2i_GHRSST-SST-iQuam-V2.10-v01.0-fv00.0.nc]
--output_path=<path>        Where to save iQuam files and results of analysis, default is the directory where the script
                            is run from. [Default: .]
--plot_all=<True, False>    Controls if all files in the output folder are plotted, or just the downloaded file
                            [Default: True]
--skip_dl=<True, False>     Skip downloading any file, essentially turns the script into a plotting scipt
                            [Default: False]
"""

# modules needed to download a file;
try:
    import wget
except ImportError as err:
    print('Unable to import wget.')

import os
import sys
from glob import glob
# ------------------------------------------------

# modules needed to read and plot iQuam NetCDF file;
import numpy as np

try:
    import matplotlib.pyplot as plt
    from matplotlib import rc
except ImportError as err:
    print('Unable to import matplotlib.')
    raise

try:
    from netCDF4 import Dataset
except ImportError as err:
    print('Unable to import netCDF4.')
    raise

try:
    from mpl_toolkits.basemap import Basemap
except ImportError as err:
    print('Unable to import Basemap. See install instructions at https://matplotlib.org/basemap/users/installing.html')
    raise

# modules for the main file (runtime argument handling)
from docopt import docopt

rc('mathtext', default='regular')


def download(url: str, out_path: str):
    """
    Download file from <url>

    :param url: URL to file
    :param out_path: path to save the file to
    """
    fn = os.path.basename(url)  # get the name of the file from the url
    path_with_filename = os.path.join(out_path, fn)  # build the path where the file is saved
    if not os.path.isfile(path_with_filename):  # check whether the specified path is an existing regular file or not.
        print('Downloading {} ...'.format(fn))
        wget.download(url, out_path)
        print('\n Download Finished')
    else:
        print('{} already present ... skipping'.format(fn))


def read_and_plot_iquam(path_iquam_data):
    """
    Read variables from a file/files in a folder, and plots the spatial distribution of the monthly SST field;
    :param path_iquam_data: path in which the function looks for iquam file/files, and where output is saved.

    if path_iquam_data is a file it will plot the spatial distribution of this file and save the reslt in the same
    folder as file. If path_iquam_data is a folder the function will plot the spatial distribution of the monthly
    SST field for all .nc files in the folder and save the results into this folder.
    """

    # If a folder is passed get all the nc files in the folder, if a file is passed just process the file.
    if os.path.isdir(path_iquam_data):
        glob_path = os.path.join(path_iquam_data, '*.nc')
        path_iquam_files = glob(glob_path)
        out_path = path_iquam_data  # also set the output path to save the image to
    elif os.path.isfile(path_iquam_data):
        path_iquam_files = glob(path_iquam_data)
        out_path = os.path.dirname(path_iquam_data)  # also set the output path to save the image to
    else:
        print("Path passed to path_iquam_data is neither a directory or a file, exiting!")
        return

    ''' loop to read all the files '''
    for iquam_path in path_iquam_files:
        with Dataset(iquam_path) as data:
            # read variables;
            yyyy = data.variables['year'][0]
            month = data.variables['month'][0]
            lon = data.variables['lon'][:]
            lat = data.variables['lat'][:]
            sst = data.variables['sst'][:] - 273.15  # convert from K to degC;

        ''' scatter plot of the SSTs on a worldmap'''

        # set up projection and limits (lowerleft/upperright corner lat/lon)
        m1 = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')

        # plot coordinates from lats and lons
        x, y = m1(lon, lat)

        # generate the scatter plot;
        m1.scatter(x, y, s=1, marker='.', c=sst, cmap='jet')
        m1.drawcoastlines(linewidth=.3)
        m1.fillcontinents()
        m1.drawmapboundary()

        # draw parallels and meridians.
        # four boolean values to determine where the labels will be shown:left, right, top, and bottom.
        m1.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])  # label parallels on left
        m1.drawmeridians(np.arange(-180, 180, 60), labels=[0, 0, 0, 1])  # meridians on bottom

        # show colorbar and set colorbar limit to [0, 35] degC;
        cbar = m1.colorbar()
        cbar.set_label('SST (degC)')
        plt.clim(0, 35)

        # save figure - SST plot in each month;
        output_fn = os.path.join(
            out_path, 'Spatial_distribution_of_iQuam_SST_in_{:4d}.{:02d}.png'.format(yyyy, month)
        )
        plt.savefig(output_fn, dpi=1200)


if __name__ == '__main__':

    # get the arguments from docopt, if none are passed it will get the defaults
    arguments = docopt(__doc__)

    # read the arguments from the docopt dict
    file_name = arguments['--input_file']  # which file to download
    url_folder = arguments['--ftp_folder']  # obtain the url of the ftp folder:
    output_path = arguments['--output_path']  # files are downloaded to this folder and analysed pictures are saved here
    plot_all = arguments['--plot_all']  # plot all *.nc files in output_path or plot only the file passed to the script

    print("Using the arguments:")
    print(arguments)
    print("\n")

    # combine ftp folder and file to create an url for a file
    url_file = os.path.join(url_folder, file_name)

    # download the file into the local folder
    if arguments['--skip_dl'] != "True":  # skip dl if requested
        if 'wget' in sys.modules:
            download(url_file, output_path)
        else:
            msg='''
                Tried to download files after import wget failed. 
                Either install wget or download the files manually and skip downloading by setting the --skip_dl flag. Exiting! 
                '''        
            sys.exit(msg)

    # plot the Iquam files, either just the provided file, or all files in the local folder
    if plot_all == 'True':
        read_and_plot_iquam(output_path)
    else:
        # add filename to output path so that only this file is used for plotting
        output_path = os.path.join(output_path, file_name)
        read_and_plot_iquam(output_path)
