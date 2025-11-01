import setuptools


setuptools.setup(
    name="newticket",
    version="1.0.0",
    author="Adam Parkin",
    author_email="pzelnip@gmail.com",
    description="Script for creating a new task in VS Code based on a JIRA reference",
    long_description="Script for creating a new task in VS Code based on a JIRA reference",
    url="https://github.com/pzelnip/dotfiles/python_pkgs/newticket",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires="requests python-slugify cryptocode keyring".split(),
    package_dir={"newticket": "newticket"},
    entry_points={
        "console_scripts": ["newticket=newticket.newticket:main"],
    },
    python_requires=">=3.5",
)
