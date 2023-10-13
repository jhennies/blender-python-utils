import runpy
from setuptools import setup, find_packages

version = runpy.run_path("blender_python_utils/__version__.py")["__version__"]

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
            "split_segmentation = blender_python_utils.split_segmentation:main"
        ]
    },
    install_requires=[
        'numpy',
        'h5py',
        'scipy'
    ]
)
