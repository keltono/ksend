from setuptools import setup

setup(
    name='app',
    version='0.2',
    py_modules=['app'],
    data_files=[('templates', ['templates/index.html','templates/success.html'])],
   # package_data={'': ['./templates/*']},
    # include_package_data=True,
    entry_points={
        'console_scripts': ['ksend = app:run']
    },
)
