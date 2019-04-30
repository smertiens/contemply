import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='contemply',
    version='1.0.0',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/smertiens/contemply',
    project_urls={

    },
    keywords='boilerplate skeleton code generator cli interactive',
    license='AGPL-3.0',
    author='Sean Mertiens',
    author_email='sean@atraxi-flow.com',
    description='A code generator that creates boilerplate files from templates',
    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=[],
    python_requires='>=3.4',

    entry_points={
        'console_scripts': [
            'contemply=contemply.contemply:main',
        ]
    }
)
