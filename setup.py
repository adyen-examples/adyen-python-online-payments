from setuptools import setup, find_packages

# Application set up information

with open("README.md", "r") as fh:
    long_description = fh.read()


requires = [
    'flask',
    'Adyen'
]

setup(
    name='Adyen checkout',
    version='1.0',
    packages=find_packages(),
    url='',
    license='MIT',
    author='adyen',
    author_email='',
    description='Sample Adyen Python Flask Integration',
    long_description=long_description,
    install_requires=requires
)
