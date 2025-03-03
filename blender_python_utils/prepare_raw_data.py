
import os
import logging
import numpy as np


def load_data(filepath, key='data'):

    ext = os.path.splitext(filepath)[1]

    if ext == '.h5':

        from h5py import File
        with File(filepath, mode='r') as f:
            return f[key][:]

    if ext == '.n5':

        from z5py import File
        with File(filepath, mode='r') as f:
            return f[key][:]

    raise ValueError(f'Invalid file extension: {ext}')


def save_volume(volume, filepath):
    np.savez(filepath, volume)


def prepare_raw_data(
        input_filepath,
        out_filepath,
        input_key='data',
        pixel_spacing=(0.01, 0.01, 0.01),
        sigma=None,
        verbose=False,
):

    logging.info(f'input_filepath = {input_filepath}')
    logging.info(f'out_filepath = {out_filepath}')

    data = load_data(input_filepath, input_key)

    out_dirpath = os.path.split(out_filepath)[0]
    if out_dirpath and not os.path.exists(out_dirpath):
        os.mkdir(out_dirpath)

    if sigma is not None:
        from blender_python_utils.prepare_one_segmentation import smooth
        data = smooth(data, sigma, pixel_spacing)

    save_volume(data, out_filepath)


def main():

    # ----------------------------------------------------
    import argparse

    parser = argparse.ArgumentParser(
        description='Prepare raw data to be imported into Blender',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('input_filepath', type=str,
                        help='h5 container containing a segmentation')
    parser.add_argument('out_filepath', type=str,
                        help='Output file where the results will be written to')
    parser.add_argument('-key', '--input_key', type=str, default='data',
                        help='Dataset key within the input file')
    parser.add_argument('-ps', '--pixel_spacing', type=float, nargs=3, default=(0.01, 0.01, 0.01),
                        metavar=('z', 'y', 'x'),
                        help='Pixel spacing in micrometers; default=(0.01, 0.01, 0.01)')
    parser.add_argument('--sigma', type=float, default=None,
                        help='Gaussian sigma applied to the segmentation; default=None')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    input_filepath = args.input_filepath
    out_filepath = args.out_filepath
    input_key = args.input_key
    pixel_spacing = args.pixel_spacing
    sigma = args.sigma
    verbose = args.verbose

    from blender_python_utils.log_settings import set_logging

    set_logging(verbose=verbose)

    prepare_raw_data(
        input_filepath,
        out_filepath,
        input_key=input_key,
        pixel_spacing=pixel_spacing,
        sigma=sigma,
        verbose=verbose
    )


if __name__ == '__main__':
    main()
