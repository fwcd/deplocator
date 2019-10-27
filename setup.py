import setuptools

setuptools.setup(
    name='deplocator',
    version='0.1',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'deplocator=deplocator.__main__:main'
        ]
    }
)
