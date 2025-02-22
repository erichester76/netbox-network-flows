from setuptools import setup, find_packages

setup(
    name='traffic_flows',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'netbox>=4.1.0',
    ],
)