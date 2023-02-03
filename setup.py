from setuptools import setup
  
setup(
    name='my_package',
    version='0.1',
    description='Newboy app',
    author='newsboy',
    author_email='newsboy@example.com',
    packages=['my_package'],
    install_requires=[
        'numpy',
        'pandas',
        'praw',
        'flask',
        'cohere',
    ],
)