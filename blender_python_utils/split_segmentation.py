
import logging
import os


def load_segmentation(filepath, key='data'):
    from h5py import File
    with File(filepath, mode='r') as f:
        return f[key][:]


def find_objects(segmentation):
    from scipy import ndimage
    return ndimage.find_objects(segmentation)


def binarize(volume, label):
    volume = volume.copy()
    volume[volume != label] = 0
    volume[volume > 0] = 1
    return volume.astype('float32')


def smooth(volume, sigma, pixel_spacing=None):

    import numpy as np

    if sigma == 0:
        return volume

    volume = volume.copy()

    sigma = np.array([sigma] * 3)
    if pixel_spacing is not None:
        min_px_spacing = min(pixel_spacing)
        sigma /= (np.array(pixel_spacing) / min_px_spacing)
        logging.debug(f'sigma = {sigma}')

    # For the smoothing we need to pad the volumes a bit!
    halo = np.array(np.ceil(sigma)).astype(int)

    in_vol = np.zeros((np.array(volume.shape) + 2 * halo).astype(int))
    in_vol[halo[0]:-halo[0], halo[1]:-halo[1], halo[2]:-halo[2]] = volume

    from scipy.ndimage import gaussian_filter
    volume = gaussian_filter(in_vol, sigma, mode='constant', cval=0)

    return volume, halo


def save_as_npy(volume, filepath):
    import numpy as np
    np.save(filepath, volume)


def save_as_h5(volume, filepath):
    from h5py import File
    with File(filepath, mode='w') as f:
        f.create_dataset('data', data=volume, compression='gzip')


def save_object(volume, filepath):

    filetype = os.path.splitext(filepath)[1]
    if filetype == '.npy':
        save_as_npy(volume, filepath)
    elif filetype == '.h5':
        save_as_h5(volume, filepath)
    else:
        raise ValueError(f'Invalid filetype: {filetype}')


def extract_object(
        segmentation, object_info, idx, out_folder,
        pixel_spacing=(0.01, 0.01, 0.01),
        sigma=1.2,
        save_as='npy'
):
    import numpy as np

    # Extract the volume
    object_volume = segmentation[object_info]

    # The label is one larger than the object id
    label = idx + 1
    logging.debug(f'label = {label}')

    # The object must be in the volume!
    assert label in np.unique(object_volume)

    # Get the object location
    position_px = np.array([object_info[0].start, object_info[1].start, object_info[2].start])

    # Binarize and smooth the object
    # Due to the smoothing the bounding volume becomes larger and the position has to be updated
    object_volume = binarize(object_volume, label)
    object_volume, halo = smooth(object_volume, sigma, pixel_spacing=pixel_spacing)
    position_px -= halo

    # Save the object
    save_object(object_volume, os.path.join(out_folder, 'obj_{:06d}.{}'.format(label, save_as)))

    # Transform the location of the object to micrometers
    position_um = position_px * np.array(pixel_spacing)

    return position_um.tolist()


def save_positions(positions, out_folder):
    import json
    with open(os.path.join(out_folder, 'pos.json'), 'w') as f:
        json.dump(positions, f, indent=2)


def split_segmentation(
        input_filepath,
        out_folder,
        input_key='data',
        pixel_spacing=(0.01, 0.01, 0.01),
        sigma=1.2,
        save_as='npy'
):

    logging.info(f'input_filepath = {input_filepath}')
    logging.info(f'out_folder = {out_folder}')

    segmentation = load_segmentation(input_filepath, key=input_key)

    object_infos = find_objects(segmentation)

    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    positions = {
        idx: extract_object(
            segmentation, object_info, idx, out_folder,
            pixel_spacing=pixel_spacing, sigma=sigma, save_as=save_as
        )
        for idx, object_info in enumerate(object_infos) if object_info is not None
    }

    save_positions(positions, out_folder)


def main():

    # ----------------------------------------------------
    import argparse

    parser = argparse.ArgumentParser(
        description='Split a segmentation into individual objects that can be imported into Blender',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('input_filepath', type=str,
                        help='h5 container containing a segmentation')
    parser.add_argument('out_folder', type=str,
                        help='Output folder where the results will be written to')
    parser.add_argument('-key', '--input_key', type=str, default='data',
                        help='Dataset key within the input file')
    parser.add_argument('-ps', '--pixel_spacing', type=float, nargs=3, default=(0.01, 0.01, 0.01),
                        metavar=('z', 'y', 'x'),
                        help='Pixel spacing in micrometers; default=(0.01, 0.01, 0.01)')
    parser.add_argument('--sigma', type=float, default=1.2,
                        help='Gaussian sigma applied to each extracted object; default=1.2')
    parser.add_argument('--save_as', type=str, default='npy',
                        help='Filetype for saving the object volumes: ["npy", "h5"]; default="npy"')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    input_filepath = args.input_filepath
    out_folder = args.out_folder
    input_key = args.input_key
    pixel_spacing = args.pixel_spacing
    sigma = args.sigma
    save_as = args.save_as
    verbose = args.verbose

    from .log_settings import set_logging

    set_logging(verbose=verbose)

    split_segmentation(
        input_filepath,
        out_folder,
        input_key=input_key,
        pixel_spacing=pixel_spacing,
        sigma=sigma,
        save_as=save_as
    )


if __name__ == '__main__':
    main()
