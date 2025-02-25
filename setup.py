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
            "split_segmentation = blender_python_utils.split_segmentation:main",
            "prepare_one_segmentation = blender_python_utils.prepare_one_segmentation:main",
            "prepare_raw_data = blender_python_utils.prepare_raw_data:main"
        ]
    },
    install_requires=[
        'numpy',
        'h5py',
        'scipy'
    ]
)
