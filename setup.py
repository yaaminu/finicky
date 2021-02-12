import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="Yaval",
    version="0.0.3",
    description="Easy Data Validation",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yaaminu/yaval",
    author="Aminu Abdul Manaf",
    author_email="afolanyaaminu@gmai.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.6",  # requires f-strings
    packages=["yaval"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
        ]
    },
)
