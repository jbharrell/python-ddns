from setuptools import setup, find_packages

setup_params = {
        'entry_points': {
            'console_scripts': ['ddns=ddns:main'],
        },
        'zip_safe': False,
    }



setup(
    packages = find_packages(), 
    py_modules=['ddns'], 
    install_requires=['pyyaml','requests','pycurl',], 
    **setup_params
)

