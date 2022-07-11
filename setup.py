import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def read_file(file):
   with open(file) as f:
        return f.read()

version = read_file("VERSION")

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

requirements = read_requirements("requirements.txt")

setuptools.setup(
    name='mwi_tools',
    version=version,
    author='Basile ROCHUT',
    author_email='basile@marine-weather.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hokuleadev/mwi_tools',
    license='MIT license',
    packages=setuptools.find_packages(exclude=["test"]),
    install_requires=requirements,
)