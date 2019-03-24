from setuptools import find_packages
from setuptools import setup
import os


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '1.0a13.dev0'
shortdesc = 'Web application stub'
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'CHANGES.rst',
    'LICENSE.rst'
]])


setup(
    name='cone.app',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='node pyramid cone web',
    author='Robert Niederreiter',
    author_email='dev@bluedynamics.com',
    url=u'https://github.com/bluedynamics/cone.app',
    license='Simplified BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['cone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Chameleon',
        'node',
        'node.ext.ugm',
        'pyramid>1.4.999',
        'pyramid_zcml',
        'pyramid_chameleon',
        'bdajax>1.9.999',
        'cone.tile',
        'yafowil',
        'yafowil.webob',
        'yafowil.bootstrap',
        'repoze.workflow',
    ],
    extras_require=dict(
        lxml=[
            'lxml'
        ],
        yaml=[
            'yafowil.yaml'
        ],
        test=[
            'lxml',
            'yafowil.yaml',
            'zope.testrunner'
        ],
        docs=[
            'Sphinx',
            'sphinx_bootstrap_theme',
            'repoze.sphinx.autointerface'
        ],
    ),
    tests_require=[
        'lxml',
        'yafowil.yaml',
        'zope.testrunner'
    ],
    test_suite='cone.app.tests.test_app.test_suite',
    entry_points="""\
    [paste.app_factory]
    main = cone.app:main
    [paste.filter_app_factory]
    remote_addr = cone.app:make_remote_addr_middleware
    """
)
