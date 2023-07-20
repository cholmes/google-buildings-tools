from setuptools import setup, find_packages

setup(
    name='google-buildings-cli',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'duckdb',
        'pandas',
        'geopandas',
        'shapely',
        'openlocationcode',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'gob-tools=google_buildings_cli:cli'
        ]
    },

)
