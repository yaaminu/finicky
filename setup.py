import pathlib2
from setuptools import setup

HERE = pathlib2.Path(__file__).parent

README = (HERE / "Readme.md").read_text()
deps = pathlib2.Path('requirements.txt').read_bytes().split("\n")
dependencies = [dep for dep in deps if len(dep.strip()) > 0]

setup(
    name="Finicky",
    version="0.1.6",
    description="Easy Data Validation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yaaminu/finicky",
    author="Aminu Abdul Manaf",
    author_email="afolanyaaminu@gmai.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=2.7",  # requires f-strings
    packages=["finicky"],
    include_package_data=True,
    install_requires=dependencies,
    entry_points={
        "console_scripts": [
        ]
    },
)
