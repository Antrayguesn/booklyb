from setuptools import setup, find_packages

setup(
    name="booklyb_api",
    version="0.0.1",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aigyre Consult",
    author_email="nicolas.antraygues@gmail.com",
    url="https://github.com/antrayguesn/SearchPlace",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "requests",
        "numpy"
    ],
    python_requires=">=3.6",
)
