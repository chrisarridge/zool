import setuptools

setuptools.setup(
    name = 'Zool',
    version = '1.0',
	package_dir = {'': 'source'},
    packages = ['zool'],
    author = 'Chris Arridge',
    author_email = 'c.arridge@lancaster.ac.uk',
    description = 'Plot layout toolkit',
	url = 'https://github.com/chrisarridge/zool',
	install_requires = ['numpy', 'matplotlib', 'kiwisolver']
)
