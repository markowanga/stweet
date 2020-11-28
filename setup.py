import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("requirements.txt", "r") as fh:
    REQUIRED = fh.readlines()

setuptools.setup(
    name="stweet",
    version="0.1.5",
    author="Marcin Wątroba",
    author_email="markowanga@gmail.com",
    description="Package to scrap tweets",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/markowanga/stweet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=REQUIRED
)
