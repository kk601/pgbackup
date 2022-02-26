from setuptools import setup, find_packages

with open('README.md', encoding='UTF-8') as f:
    readname = f.read()

setup(
    name='pgbackup',
    version='1.1.0',
    description='Backup database to local file or to aws S3',
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