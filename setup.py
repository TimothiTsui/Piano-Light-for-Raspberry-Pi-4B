from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="pyanoled",
    version="1.2.0",
    author="Ethan Lu",
    author_email="fang.lu@gmail.com",
    description="Python Piano LED Visualizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ethanlu/pyanoled",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>3.6',
    packages=find_packages(),
    package_data={'pyanoled': ['conf/*.conf']},
    install_requires=[
        "cython",
        "argparse",
        "mido",
        "numpy",
        "Pillow",
        "psutil",
        "pyhocon",
        "python-rtmidi",
        "RPi.GPIO",
        "rpi-ws281x",
        "spidev",
        "webcolors",
        "wheel"
    ],
    entry_points={
        'console_scripts': [
            'pyanoled = pyanoled.__main__:main'
        ]
    }
)
