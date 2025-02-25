
import logging
import os.path
import numpy as np


def smooth(volume, sigma, pixel_spacing=None):

    import numpy as np

    if sigma == 0:
        return volume

    sigma = np.array([sigma] * 3)
    if pixel_spacing is not None:
        min_px_spacing = min(pixel_spacing)
        sigma /= (np.array(pixel_spacing) / min_px_spacing)
        logging.debug(f'sigma = {sigma}')

    from scipy.ndimage import gaussian_filter
    volume = gaussian_filter(volume, sigma, mode='constant', cval=0)

    return volume


def binarize(volume):

    volume[volume > 0] = 255
    return volume.astype('uint8')


def save_mesh(filepath, verts, faces, normals, values):
    np.savez_compressed(filepath, verts=verts, faces=faces, normals=normals, values=values)


def prepare_one_segmentation(
        input_filepath,
        out_filepath,
        input_key='data',
        pixel_spacing=(0.01, 0.01, 0.01),
        sigma=1.2,
        verbose=False,
):
    logging.info(f'input_filepath = {input_filepath}')
    logging.info(f'out_filepath = {out_filepath}')

    from blender_python_utils.split_segmentation import load_segmentation

    segmentation = load_segmentation(input_filepath, key=input_key)

    out_dirpath = os.path.split(out_filepath)[0]
    if not os.path.exists(out_dirpath):
        os.mkdir(out_dirpath)

    # Binarize and smooth
    segmentation = binarize(segmentation)
    segmentation = smooth(segmentation, sigma, pixel_spacing)

    # Make a mesh
    from skimage.measure import marching_cubes
    thresh = 64
    verts, faces, normals, values = marching_cubes(segmentation, thresh)

    save_mesh(out_filepath, verts, faces, normals, values)

    # from split_segmentation import save_object
    # save_object(segmentation, out_filepath)


def main():

    # ----------------------------------------------------
    import argparse

    parser = argparse.ArgumentParser(
        description='Split a segmentation into individual objects that can be imported into Blender',
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
    parser.add_argument('--sigma', type=float, default=1.2,
                        help='Gaussian sigma applied to the segmentation; default=1.2')
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

    prepare_one_segmentation(
        input_filepath,
        out_filepath,
        input_key=input_key,
        pixel_spacing=pixel_spacing,
        sigma=sigma,
        verbose=verbose
    )


if __name__ == '__main__':
    main()
