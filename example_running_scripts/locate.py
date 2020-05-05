# -*- coding: utf-8 -*-
"""
This script will run the locate stage of QuakeMigrate.

For more details, please see the manual and read the docs.

"""

from QMigrate.io import Archive, stations
from QMigrate.lut import LUT
from QMigrate.signal import QuakeScan
from QMigrate.signal.onset import STALTAOnset
from QMigrate.signal.pick import GaussianPicker

# --- i/o paths ---
archive_path = "/path/to/archived/data"
lut_file = "/path/to/lut"
station_file = "/path/to/station_file"
run_path = "/path/to/output"
run_name = "name_of_run"

# --- Set time period over which to run locate ---
starttime = "2018-001T00:00:00.0"
endtime = "2018-002T00:00:00.0"

# --- Read in station file ---
stations = stations(station_file)

# --- Create new Archive and set path structure ---
archive = Archive(stations=stations, archive_path=archive_path)
archive.path_structure(archive_format="YEAR/JD/STATION")
# For custom structures...
# archive.format = "custom/archive_{year}_{month}_structure"

# --- Resample data with mismatched sampling rates ---
# archive.resample = True
# archive.upfactor = 2

# --- Load the LUT ---
lut = LUT(lut_file=lut_file)

# --- Decimate the lookup table ---
# lut = lut.decimate([1, 1, 1])

# --- Create new Onset ---
onset = STALTAOnset(position="centred")
onset.p_bp_filter = [2, 9.9, 2]
onset.s_bp_filter = [2, 9.9, 2]
onset.p_onset_win = [0.2, 1.5]
onset.s_onset_win = [0.2, 1.5]

# --- Create new PhasePicker ---
# For a complete list of parameters and guidance on how to choose them, please
# see the manual and read the docs.
gausspicker_onset = STALTAOnset(position="centred")
gausspicker_onset.p_bp_filter = [2, 9.9, 2]
gausspicker_onset.s_bp_filter = [2, 9.9, 2]
gausspicker_onset.p_onset_win = [0.2, 1.5]
gausspicker_onset.s_onset_win = [0.2, 1.5]

picker = GaussianPicker(onset=gausspicker_onset, marginal_window=1)
picker.plot_picks = True

# --- Create new QuakeScan ---
scan = QuakeScan(archive, lut, onset=onset, picker=picker, run_path=run_path,
                 run_name=run_name, log=True)

# --- Set locate parameters ---
# For a complete list of parameters and guidance on how to choose them, please
# see the manual and read the docs.
scan.marginal_window = 1
scan.sampling_rate = 20
scan.threads = 12

# --- Toggle plotting options ---
scan.plot_event_video = False
scan.plot_event_summary = True

# --- Toggle writing of waveforms ---
scan.write_cut_waveforms = True

# --- Run locate ---
# Between two timestamps
scan.locate(start_time=starttime, end_time=endtime)
# From a triggered events file.
# scan.locate(fname="filename_of_triggered_events")
