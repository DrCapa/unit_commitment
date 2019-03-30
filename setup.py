from setuptools import setup, find_packages

setup(
    name='unit_commitment',
    version='1.0',
    url='https://github.com/DrCapa/unit_commitment',
    author='Rico Hoffmann',
    author_email='rico.hoffmann@libero.it',
    description='README',
    packages=find_packages(),
    install_requires=['pandas >= 0.23.4', 'pyomo >= 5.5.0',
                      'numpy >= 1.15.2', 'matplotlib >= 3.0.2',
                      'xlsxwriter >= 1.0.7']
)
