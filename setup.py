from setuptools import setup

setup(name='strictdom',
    version='0.3',
    description='strictly typed wrapper around Knio\'s Dominate',
    long_description='strictly typed wrapper around Knio\'s Dominate, a Python library for creating and manipulating HTML documents',
    url='https://github.com/tawesoft/strictdom',
    author='Ben Golightly',
    author_email='golightly.ben@googlemail.com',
    maintainer='Tawesoft Ltd',
    maintainer_email='opensource@tawesoft.co.uk',
    license='Creative Commons Attribution 4.0 International License and W3C Document License',
    packages=['strictdom'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=True)
