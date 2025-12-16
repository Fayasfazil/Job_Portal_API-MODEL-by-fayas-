from setuptools import setup, find_packages

setup(
    name='job_portal_api',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask==2.3.3',
        'SQLAlchemy==2.0.23',
        'PyJWT==2.8.0',
        'psycopg2-binary==2.9.9',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'run-api=src.app:main',
        ],
    },
    description='A Python REST API backend demonstrating authentication and CRUD operations.',
    author='FAYAS AHAMED',
    license='MIT',
)
