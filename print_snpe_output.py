import argparse
import numpy as np
import os


parser = argparse.ArgumentParser()
parser.add_argument('indir', type=str,
        help='Path to directory containing numpy files to process')
args = parser.parse_args()

for fil in os.listdir(args.indir):
    result = np.fromfile(os.path.join(args.indir, fil), dtype=np.float32)
    print(fil, result)
