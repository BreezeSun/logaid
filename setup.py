from setuptools import setup, find_packages
setup(
      name='logaid',  # 包的名称
      version='1.2.3',  # 包的版本号
      author='BreezeSun',  # 作者姓名
      description='A log aid for you.',
      packages=find_packages(),
      long_description=open('README.md','r',encoding='utf-8').read(),
      long_description_content_type="text/markdown",
      license="MIT"
)

