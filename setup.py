from setuptools import setup, find_packages

setup(
    name='PKULogin',
    version='0.1.0',
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
