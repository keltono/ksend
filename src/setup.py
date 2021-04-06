from setuptools import setup

setup(
    name='ksend',
    version='0.1',
    py_modules=['ksend'],
    entry_points={
        'console_scripts': ['ksend = ksend:run']
    },
)
