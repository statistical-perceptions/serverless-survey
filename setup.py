from setuptools import setup

setup(
    name='serverlesssurvey',
    version='0.3.4',
    packages=['ssbuilder'],
    install_requires=[
        'Click', 'pandas', 'lxml', 'plotly', 'requests', 'html5lib',
        'markdown'
    ],

    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ssgeneratehtml = ssbuilder:generate_from_configuration',
            'sslengthcheck = ssbuilder:check_query_length',
            'ssmergedir = ssbuilder:merge_dir_csvs'
        ],
    },
)
