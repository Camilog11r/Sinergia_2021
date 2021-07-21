import numpy as np
import matplotlib.pyplot as plt

import welly
welly.__version__
from welly import Well

w = Well.from_las("./Well_Logging/SNRG-0001_basic_logs.las",remap={'KB': 'EKB', 'UWI': 'WELL'})
l = w.to_lasio()
l.well['NULL']
w.to_las('./Well_Logging/SNRG-0001_basic_logs.las',null_value=-999)
tracks = ['MD', 'GR', 'RHOZ', 'MD']
w.plot(tracks=tracks)
