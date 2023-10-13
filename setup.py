# import runpy
from setuptools import setup  #, find_packages

# version = runpy.run_path("blender_python_utils/__version__.py")["__version__"]
version = '0.0.1'

setup(
    name="blender_python_utils",
    packages=['blender_python_utils'],  #find_packages(exclude=["test"]),
    version=version,
    author="Julian Hennies",
    url="https://github.com/jhennies/blender-python-utils",
    license="GPLv3",
    entry_points={
        "console_scripts": [
            # "mobie.add_image = mobie.image_data:main"
            "segmentation_to_objects = blender_python_utils.segmentation:segmentation_to_objects"
        ]
    },
    install_requires=[
        'numpy',
        'h5py'
    ]
)
