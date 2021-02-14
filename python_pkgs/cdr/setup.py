import setuptools


setuptools.setup(
    name="cdr",
    version="0.0.1",
    author="Adam Parkin",
    author_email="pzelnip@gmail.com",
    description="Script for opening projects in VS Code",
    long_description="Script for opening projects in VS Code",
    url="https://github.com/pzelnip/dotfiles/python_pkgs/cdr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"cdr": "cdr"},
    entry_points={
        "console_scripts": [
            "cdr=cdr.cdr:main"
        ],
    },
    python_requires=">=3.5",
)
