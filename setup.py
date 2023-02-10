from setuptools import setup

setup(
    name='syscourseutils',
    version='0.1.0',
    py_modules=['single_normal_curve'],
    install_requires=[
        'Click', 'pandas', 'lxml', 'plotly', 'requests', 'html5lib'
    ],
    entry_points={
        'console_scripts': [
            'generatehtml = single_normal_curve:generate_from_configuration',
        ],
    },
)
