from setuptools import setup, find_packages

with open('README.md', encoding='UTF-8') as f:
    readname = f.read()

setup(
    name='pgbackup',
    version='0.1.0',
    description='database backups locally or to azure storeage',
    author='kk601',
    author_email='kubakurowski106@gmail.com',
    install_requires=['boto3'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points = {
        'console_scripts':[
            'pgbackup=pgbackup.cli:main'
        ]
    }
)