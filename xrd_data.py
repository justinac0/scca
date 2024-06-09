import csv
from scipy.signal import find_peaks

def load_xrd_csv(filename: str):
        x = []
        y = []

        with open(filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

            for row in reader:
                col_count = 0
                for col in row:
                    stripped_str = col.strip()

                    if col_count == 0:
                        x.append(float(stripped_str))
                    else:
                        y.append(float(stripped_str))

                    col_count = col_count + 1

        return (x, y)


class XRDdata:
    def __init__(self, filename: str, title: str):
        (self.x, self.y) = load_xrd_csv(filename)
        self.peaks = self.get_peaks()
        self.title = title

    def get_peaks(self):
        peaks, _ = find_peaks(self.y, height=10, distance=100)

        x = []
        y = []
        idx = []
        for peak_idx in peaks:
            x.append(self.x[peak_idx])
            y.append(self.y[peak_idx])
            idx.append(peak_idx)

        return (x, y, idx)
