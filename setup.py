import setuptools, os

basepath = os.path.dirname(__file__)
basepath += '/' if basepath != '' else ''

with open(basepath + "README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open(basepath + 'requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line)

setuptools.setup(
    name='contemply',
    version='1.0.0',
    packages=setuptools.find_packages(basepath + 'src'),
    package_dir={'': basepath + 'src'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "Environment :: Console"
    ],
    url='https://github.com/smertiens/contemply',
    project_urls={

    },
    keywords='boilerplate skeleton code generator cli interactive',
    license='AGPL-3.0',
    author='Sean Mertiens',
    author_email='sean@atraxi-flow.com',
    description='Contemply turns your boring old templates and project scaffolds into interactive code generators.',
    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=requirements,
    python_requires='>=3.4',

    package_data={
        'contemply': ['samples/*', 'LICENSE'],
    },

    entry_points={
        'console_scripts': [
            'contemply=contemply.contemply_cli:main',
        ]
    }
)
