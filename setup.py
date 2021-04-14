import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "Readme.md").read_text()
deps = pathlib.Path('requirements.txt').read_text().split("\n")
dependencies = [dep for dep in deps if len(dep.strip()) > 0]

setup(
    name="Finicky",
    version="0.1.3",
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
