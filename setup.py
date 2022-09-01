from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erpnext_pk/__init__.py
from erpnext_pk import __version__ as version

setup(
	name="erpnext_pk",
	version=version,
	description="ERPNext Pakistan Regional Customization",
	author="ParaLogic",
	author_email="info@paralogic.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
