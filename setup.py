import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="krait",
    version="0.0.1",
    author="alex",
    author_email="junglefire@hotmail.com",
    description="A small python lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/junglefire/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)