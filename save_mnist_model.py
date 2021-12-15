import argparse
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import datasets, layers, models


parser = argparse.ArgumentParser()
parser.add_argument('outdir', type=str,
        help='Directory to save to')
args = parser.parse_args()


if not os.path.isdir(args.outdir):
    os.makedirs(args.outdir)

# Set up MNIST model
in_size=(28, 28, 1)
model = models.Sequential()
model.add(layers.Conv2D(32, (5, 5), activation='relu', input_shape=in_size))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (5, 5), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(10, activation='softmax'))

# Get MNIST test data
_, (test_data, _) = datasets.mnist.load_data()
test_data = test_data.reshape((10000,) + in_size)
test_data = test_data / 255.0

# Save the model to .pb file
pbdir = os.path.join(args.outdir, 'pb')
tf.saved_model.save(model, pbdir)

# Save a test input as a raw numpy array. This is the required input format
# for the SNPE command-line tools.
raw_dir = os.path.join(args.outdir, 'raw')
if not os.path.isdir(raw_dir):
    os.makedirs(raw_dir)

raw_input_file = os.path.join(raw_dir, 'input.raw')
test_data[0].astype(np.float32).tofile(raw_input_file)

# Save the path to the raw input file to another file. This, again, is the
# required input format for the SNPE command-line tools.
raw_input_list_file = os.path.join(raw_dir, 'raw_input_list.txt')
with open(raw_input_list_file, 'w') as outfile:
    outfile.write(raw_input_file)

# Generate additional command-line arguments needed for executing SNPE
# command-line tools
insize_str = ','.join([str(x) for x in (1,) + in_size])
cmdstr = "-d {} {}".format(model.input.name, insize_str)
output = model.output
outstr = output.name.split('/')[0]
cmdstr += " --out_node {}".format(outstr)

dlc_file = os.path.join(args.outdir, 'model.dlc')
net_run_outdir = os.path.join(args.outdir, 'out')

print('------------------------------------------------')
print('Generate a DLC file using the following command:')
print('   snpe-tensorflow-to-dlc {} -i {} -o {}'.format(cmdstr, pbdir, dlc_file))
print('')
print('Run the DLC file using the following command:')
print('   snpe-net-run --container {} --input_list {} --output_dir {}'.format(
    dlc_file, raw_input_list_file, net_run_outdir))
