from setuptools import setup, find_packages
from os import path
import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py2uml',
    version=versioneer.get_version(),
    description='Create UML diagrams using mermaid syntax.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mmngreco/py2uml',
    author='mmngreco',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=[],
    entry_points={'console_scripts': ['py2uml = py2uml.core:cli']}
)
