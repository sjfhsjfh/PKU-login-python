from setuptools import setup, find_packages

version = '0.1.1'

setup(
    name='PKULogin',
    version=version,
    description='PKU Login python module',
    author='sjfhsjfh',
    author_email='sjfhsjfh@qq.com',
    url='https://github.com/sjfhsjfh/PKU-login-python',
    install_requires=[
        'requests',
    ],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
