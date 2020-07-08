# -*- coding: utf-8 -*-
"""
This script will create travel-time lookup tables for QuakeMigrate.

For more details, please see the manual and read the docs.

"""

from pyproj import Proj

from QMigrate.io import read_stations, read_vmodel
from QMigrate.lut import compute, LUT, read_nlloc

# --- i/o paths ---
lut_file = "/path/to/save/lut_file"
station_file = "/path/to/station_file"
vmodel_file = "/path/to/vmodel_file"

# --- Read in the stations and velocity model files ---
stations = read_stations(station_file)
vmod = read_vmodel(vmodel_file)

# --- Define projections ---
# Values used are for the Borneo example available on GitHub.
cproj = Proj(proj="longlat", ellps="WGS84", datum="WGS84", no_defs=True)
gproj = Proj(proj="lcc", lon_0=116.75, lat_0=6.25, lat_1=4.0, lat_2=7.5,
             datum="WGS84", ellps="WGS84", units="m", no_defs=True)

# --- Create new LUT ---
# Values used are for the Borneo example available on GitHub.
lut = LUT(ll_corner=[116.075, 5.573, -1750],
          ur_corner=[117.426, 6.925, 27750],
          cell_size=[500., 500., 500.],
          grid_proj=gproj, coord_proj=cproj)

# --- Homogeneous LUT generation ---
compute(lut, stations, method="homogeneous", vp=5000., vs=3000., log=True)

# --- skfmm LUT generation ---
compute(lut, stations, method="1dfmm", vmod=vmod, log=True)

# --- NLLoc sweep LUT generation ---
compute(lut, stations, method="1dsweep", vmod=vmod, block_model=True, log=True)

# --- Read NLLoc lookup tables ---
lut = read_nlloc("/path/to/nlloc_files", stations, log=True)

# --- Save LUT ---
lut.save(lut_file)
