import matplotlib.pyplot as plt
from terminaltables import AsciiTable
import math

from xrd_data import XRDdata

TITLE_FONT_SIZE = 30 
AXIS_FONT_SIZE = 24
LEGEND_FONT_SIZE = 24
TICK_FONT_SIZE = 20
BRAGGS_FONT_SIZE = 18

plt.rcParams.update({
    'font.family': 'monospace',
    'xtick.labelsize': TICK_FONT_SIZE,
    'ytick.labelsize': TICK_FONT_SIZE,
})

class XRDanalysis:
    @staticmethod
    def get_miller_indices(n: int):
        for h in range(n + 1):
            for k in range(h + 1):
                for l in range(k + 1):
                    if (h**2 + k**2 + l**2 == n):
                        return (h, k, l)

    @staticmethod
    def get_lattice_constant(d_spacing: float, h: int, k: int, l: int):
        return (d_spacing * math.sqrt(h**2 + k**2 + l**2))

    @staticmethod
    def get_interplanar_spacing(n: int, wavelength: float, theta_deg: float):
        return (n * wavelength) / (2 * XRDanalysis.get_sin_theta(theta_deg))

    @staticmethod
    def get_braggs_angle(two_theta: float):
        return (two_theta / 2)

    @staticmethod
    def get_sin_theta(theta: float):
        return (math.sin(math.radians(theta)))

    @staticmethod
    def compute_composition(I0, I, ma_a, ma_b):
        composition_array = []

        for i in range(len(I0)):
            intensity_ratio = I[i]/I0[i]
            c = intensity_ratio * ma_b / (ma_a - intensity_ratio * (ma_a - ma_b) )
            composition_array.append(c)

        return composition_array

    @staticmethod
    def display_analysis(xrd_data: XRDdata, source_wave_length: float, normal_ratio: int):
        table = []

        table_header = [
            'Peak #',
            '2θ (Deg)',
            'Intensities',
            'd (Å)',
            'sin^2(θ)',
            'ratio',
            'integer',
            'hkl',
            'a (Å)'
        ]

        table.append(table_header)

        d_spacing = []
        sin_2_theta = []
        integers = []
        ratios = []
        miller_indices = []
        lattice_consts = []

        (peaks, intensities, _) = xrd_data.peaks

        for i in range(len(peaks)):
            theta = XRDanalysis.get_braggs_angle(peaks[i])
            d_space = XRDanalysis.get_interplanar_spacing(1, source_wave_length, theta)
            d_spacing.append(d_space)
            sin_2_theta.append(XRDanalysis.get_sin_theta(theta)**2)

        for i in range(len(peaks)): # find miller indices
            ratio = sin_2_theta[i] / min(sin_2_theta)
            integer = int(round(ratio * normal_ratio))
            miller_indices.append(XRDanalysis.get_miller_indices(integer))

            ratios.append(ratio)
            integers.append(integer)
    
            (h, k, l) = miller_indices[i]
            lattice_consts.append(XRDanalysis.get_lattice_constant(d_spacing[i], h, k, l))

            row = [
                str(i + 1),
                str(f'{peaks[i]:.2f}'),
                str(intensities[i]),
                str(f'{d_spacing[i]:.2f}'),
                str(f'{sin_2_theta[i]:.2f}'),
                str(f'{ratios[i]:.2f}'),
                str(f'{integers[i]}'),
                str(miller_indices[i]),
                str(f'{lattice_consts[i]:.2f}')
            ]

            lattice_const_sum = 0
            for value in lattice_consts:
                lattice_const_sum += value

            table.append(row)

        print(xrd_data.title)
        print(AsciiTable(table).table)

        avg_lattice_const = lattice_const_sum / len(lattice_consts)
        print(f'Average Lattice Constant: {avg_lattice_const:.2f} Å\n')

    @staticmethod
    def plot(xrd_data: XRDdata, color: str):
        x = xrd_data.x
        y = xrd_data.y

        plt.style.use('fast')
        plt.figure(figsize=(8,8))
        plt.axis([min(x), max(x), 0, max(y)+25])
        plt.plot(x, y, color)
 
        (x0, y0, idx) = xrd_data.peaks
        for i in idx:
            vstr = str(f'{x[i]:.2f}°')
            vstr_len = len(vstr)
            xoffs = -vstr_len
            #plt.annotate('2θ: ' + vstr + '\n' + 'Intensity: ' + str(y[i]), (x[i] - vstr_len/2, y[i] + 3), fontsize=10)
            plt.annotate(vstr, (x[i] + xoffs, y[i] + 4), fontsize=BRAGGS_FONT_SIZE)
            plt.vlines(x[i], ymin=0, ymax=y[i], lw=2, ls=':', color='black')

        plt.plot(x0, y0, '.', color='black', markersize=12) # plot peaks
        plt.legend(['XRD Data', '2θ Peaks'], loc="upper right", fontsize=LEGEND_FONT_SIZE)

        plt.title(xrd_data.title, fontsize=TITLE_FONT_SIZE, fontweight='bold', loc='left')
        plt.xlabel('2θ (degrees)', fontsize=AXIS_FONT_SIZE)
        plt.ylabel('Intensity (counts)', fontsize=AXIS_FONT_SIZE)

        save_file_path = f"{xrd_data.title}.png" 
        print(f"saving figure: '{save_file_path}'...")

        plt.savefig(save_file_path)
        plt.show()

