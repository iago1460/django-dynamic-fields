import os

from setuptools import find_packages, setup

import django_dynamic_fields

setup(
    author='Iago Veloso Abalo',
    name='django-dynamic-fields',
    version=django_dynamic_fields.__version__,
    description='',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/iago1460/django-dynamic-fields',
    install_requires=[
        'django-hstore>=1.3',
    ],
    zip_safe=False,
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
