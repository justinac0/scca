import sys

from xrd_analysis import XRDanalysis
from xrd_data import XRDdata
import numpy as np

if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) == 4:
        sample = XRDdata(str(arguments[1]), str(arguments[1]))
        XRDanalysis.display_analysis(sample, float(arguments[2]), int(arguments[3]))
        XRDanalysis.plot(sample, 'blue')
    else:
        print("usage: python main.py [xrd_data.path] [wavelength] [normal_multiplier]")
        pass
