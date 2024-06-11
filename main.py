import click

from xrd_analysis import XRDanalysis
from xrd_data import XRDdata
import numpy as np

@click.command()
@click.version_option("0.1.0", prog_name="scca")
@click.argument("file", type=str)
@click.argument("wavelength", type=float)
@click.argument("multiplier", type=int)
def do_analysis(file, wavelength, multiplier):
    sample = XRDdata(file, file)
    XRDanalysis.display_analysis(sample, wavelength, multiplier)
    XRDanalysis.plot(sample, 'blue')

if __name__ == '__main__':
    do_analysis()
