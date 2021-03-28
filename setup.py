from setuptools import setup, find_packages


install_requires = [
    'asyncpg==0.22.0',
    'uvloop==0.15.2',
    'nyoibo==0.2.0'
]

test_require = [
    'pytest==5.4.3',
    'pytest-cov==2.10.0',
]

with open('README.md') as f:
    readme = f.read()


setup(
    name='kinton-orm',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    author='Julián Cortés',
    author_email='julian.cortes77@pm.me',
    description='async python orm',
    long_description=readme,
    keywords='async orm postgres database',
    url='https://github.com/pity7736/kinton-orm',
    tests_require=test_require,
    python_requires='>=3.7'
)
