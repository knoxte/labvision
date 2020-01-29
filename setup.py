import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='labvision',
    version='0.1',
    license='MIT',
    packages=setuptools.find_packages(),
)

