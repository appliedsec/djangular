try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='djangular',
    version='0.2.7',
    description="A reusable app that provides better app integration with AngularJS.",
    long_description="""
A reusable app that provides better app integration with AngularJS.  Djangular
allows you to create AngularJS content per app, instead of creating a single
massive AngularJS application inside of Django.  This allows you to selectively
use apps per site, as well as create a consistent structure across all of your
Django apps.

This is intended to be a Django version of the Angular-Seed project
(https://github.com/angular/angular-seed).  The current mindset is to limit the
amount of changes introduced by Djangular.
""",
    keywords='djangular django angular angularjs',
    license='Apache',
    packages=['djangular'],
    include_package_data=True,
    author='Brian Montgomery',
    author_email='brianm@appliedsec.com',
    url='http://github.com/appliedsec/djangular',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    )
