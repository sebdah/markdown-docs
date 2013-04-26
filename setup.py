""" Setup script for PyPI """
from setuptools import setup


setup(name='markdown-docs',
    version='0.2.0-SNAPSHOT',
    license='Apache License, Version 2.0',
    description='Documentation generator for Markdown projects',
    author='Sebastian Dahlgren',
    author_email='sebastian.dahlgren@gmail.com',
    maintainer='Sebastian Dahlgren',
    maintainer_email='sebastian.dahlgren@gmail.com',
    url='http://sebdah.github.com/markdown-docs/',
    keywords="markdown documentation md mdown",
    platforms=['Any'],
    packages=['markdowndocs'],
    scripts=['scripts/markdown-docs'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask >= 0.9',
        'Jinja2 >= 2.6',
        'Markdown >= 2.3.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
