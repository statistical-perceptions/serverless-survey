from setuptools import setup

setup(
    name='serverlesssurvey',
    version='0.1.0',
    packages=['ssbuilder'],
    install_requires=[
        'Click', 'pandas', 'lxml', 'plotly', 'requests', 'html5lib'
    ],

    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ssgeneratehtml = ssbuilder:generate_from_configuration',
        ],
    },
)
