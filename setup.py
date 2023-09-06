from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(name='linspector',
      version='0.29.0',
      description='Linspector is a infrastructure and system monitoring daemon and toolchain.',
      url='https://github.com/linspector/linspector',
      author='Johannes Findeisen',
      author_email='you@hanez.org',
      license='MIT',
      packages=['linspector'],
      keywords=['linux', 'system', 'monitoring'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: System Administrators',
          'Natural Language :: English'
      ],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
