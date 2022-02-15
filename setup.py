from setuptools import setup

setup(
    name='savegame-manager',
    version='1.0',
    scripts=['./scripts/myscript'],
    author='Me',
    description='This runs my script which is great.',
    packages=['lib.myscript'],
    install_requires=[
        'setuptools',
        'argparse',
        'psutil>=5.7.0'

    ],
    python_requires='>=3.8'
)