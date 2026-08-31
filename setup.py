from setuptools import setup, find_packages
description = """LogAid is a Python library designed to make logging enjoyable.

Have you ever felt too lazy to configure a proper logger and just defaulted to using print()? I know I have. But logging is crucial for any application and really simplifies debugging. With LogAid, you’ve got no excuse not to log from the start—it’s as easy as from logaid import logger.

This library aims to ease the pain of Python logging by offering a range of helpful features that address the common pitfalls of standard loggers. Logging in your app should be second nature, and LogAid strives to make that process both easy and powerful.
"""

setup(
      name='logaid',
      version='1.5.3',
      author='BreezeSun',
      description=description,
      packages=find_packages(),
      package_data={"logaid": ["py.typed", "__init__.pyi"]},
      include_package_data=True,
      long_description=open('README.md','r',encoding='utf-8').read(),
      long_description_content_type="text/markdown",
      license="MIT"
)

