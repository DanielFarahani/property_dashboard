from setuptools import setup, find_packages

setup(name="corelogic_pyclient",
      version="0.1.0",
      description="CoreLogic API Wrapper (craw) for interacting with CoreLogic (Property Data Reports & Analytics)",
      url="https://github.com/danielfarahani/corelogic_pyclient",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='corelogic proptech property',
      author="Daniel Farahani",
      author_email="danfarahani@gmail.com",
      license="MIT",
      packages=find_packages(exclude=["test_*.*"]),
      install_requires=['click']
      include_package_data=True,
      zip_safe=True,
      )