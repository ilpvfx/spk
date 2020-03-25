from setuptools import setup, find_packages

import spfs

setup(
    name="spfs",
    version="0.18.5",
    packages=find_packages(),
    package_data={"spfs": ["*.sh"]},
    entry_points={"console_scripts": ["spfs=spfs.cli:main"]},
    zip_safe=True,
)
