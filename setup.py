from setuptools import setup

setup(
    name='savegame-manager',
    version='1.2.0',
    scripts=['./scripts/savegame.cmd'],
    author='Arjun Srivastava',
    description='Save folder manager for PC games.',
    packages=['src.savegame'],
    install_requires=[
        'setuptools',
        'argparse',
        'psutil>=5.7.0',
        'tkinter'
    ],
    python_requires='>=3.8'
)
