from setuptools import setup, find_packages

setup(
    name="dowser",
    version="0.1.0",
    author="Daniel De Lucca Fonseca",
    author_email="daniel@delucca.dev",
    description="Dowser simplifies profiling and modeling the memory usage of Python programs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/delucca/dowser",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "dowser=dowser.cli:cli",
        ],
    },
)
