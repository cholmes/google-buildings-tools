from setuptools import setup, find_packages

setup(
    name='google-buildings-cli',
    version='0.1',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'google-buildings-cli=google_buildings_cli:main',
        ],
    },
)

