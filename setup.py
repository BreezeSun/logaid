from setuptools import setup, find_packages
setup(
      name='logaid',
      version='1.5.2',
      author='BreezeSun',
      description='A log aid for you.',
      packages=find_packages(),
      package_data={"logaid": ["py.typed", "__init__.pyi"]},
      include_package_data=True,
      long_description=open('README.md','r',encoding='utf-8').read(),
      long_description_content_type="text/markdown",
      license="MIT"
)

