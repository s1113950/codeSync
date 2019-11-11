from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='csync',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Syncs code to machines on code changes',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Steven Robertson',
      url='https://github.com/s1113950/csync.git',
      packages=find_packages(exclude=["tests"]),
      install_requires=[
          "configparser==3.5.0",
          "watchdog==0.8.3"
      ],
      entry_points={
          'console_scripts': ['csync=csync.watcher:main']
      },
      package_data={
      },
      include_package_data=True,
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Developers',
                   'Operating System :: POSIX',
                   'Operating System :: MacOS :: MacOS X',
                   'Programming Language :: Python :: 3'])
