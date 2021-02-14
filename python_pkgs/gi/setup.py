import setuptools


setuptools.setup(
    name="gi",
    version="0.0.1",
    author="Adam Parkin",
    author_email="pzelnip@gmail.com",
    description="Script for correcting git typos",
    long_description="Script for correcting git typos",
    url="https://github.com/pzelnip/dotfiles/python_pkgs/gi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"gi": "gi"},
    entry_points={
        "console_scripts": [
            "gi=gi.gi:main"
        ],
    },
    python_requires=">=3.5",
)
