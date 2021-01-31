# http://go.chriswarrick.com/entry_points

from setuptools import setup

setup(
    name="bbh2sr",
    version="1.0",
    packages=["bbh2sr"],
    entry_points={
        "gui_scripts": [
            "bbh2sr = bbh2sr.__main__:main"
        ]
    },
)