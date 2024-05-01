from setuptools import setup, find_packages

setup(
    name="seismic",
    version="0.1.0",
    author="Daniel De Lucca Fonseca",
    author_email="daniel@delucca.dev",
    description="Tools to simplify the execution of seismic experiments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/delucca/seismic-attributes-memory-profile",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.10",
)
