from setuptools import setup
import os

moduleDirectory = os.path.dirname(os.path.realpath(__file__))
exec(open(moduleDirectory + "/rockfinder/__version__.py").read())


def readme():
    with open(moduleDirectory + '/README.md') as f:
        return f.read()


setup(name='rockfinder',
      version=__version__,
      description="CL-util to check the Minor Planet Centre's MPChecker for moving objects at a given sky location and epoch. Returns either the name of the closest object, or a non-match.",
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
      ],
      keywords=['terminal', 'astronomy', 'tool'],
      url='https://github.com/thespacedoctor/rockfinder',
      download_url='https://github.com/thespacedoctor/rockfinder/archive/v%(__version__)s.zip' % locals(
      ),
      author='David Young',
      author_email='davidrobertyoung@gmail.com',
      license='MIT',
      packages=['rockfinder'],
      include_package_data=True,
      install_requires=[
          'pyyaml',
          'requests',
          'fundamentals'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      # entry_points={
      #     'console_scripts': ['rockfinder=rockfinder.cl_utils:main'],
      # },
      zip_safe=False)
