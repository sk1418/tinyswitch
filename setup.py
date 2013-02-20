from setuptools import setup, find_packages
import glob
setup(
    name = 'tinyswitch',
    version = '1.1.0',
    packages = find_packages(),
    data_files=[('sample',glob.glob('sample/*.*')),('sample/data',['sample/data/proxies'])],
    include_package_data= True,
    zip_safe=False,
    scripts=['tinyswitch'],
    author='Kai Yuan',
    author_email='kent.yuan@gmail.com',
    platforms=['POSIX'],
    keywords='proxy tinyswitch',
    url='https://github.com/sk1418/tinyswitch',
    description='A command line tool to easily switch system proxy(tinyproxy based)',
    long_description="""
    using tinyproxy as system proxy, tinyswitch takes care of changing upstream proxies.
    Also all applications (firefox, commandline tools..) could just setup localhost as proxy.
    """,
)

