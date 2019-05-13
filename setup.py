import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='py-expressway',
      version='0.0.1',
      author='Jason Neurohr',
      author_email='jason@jasonneurohr.com',
      description='A package for interacting with the Cisco Expressway REST API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/jasonneurohr/py-expressway',
      license='Apache 2.0',
      packages=setuptools.find_packages(),
      classifiers=[
            "License :: OSI Approved :: Apache Software License"
      ])