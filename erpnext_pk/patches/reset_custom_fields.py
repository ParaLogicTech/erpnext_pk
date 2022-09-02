from erpnext_pk.install import make_custom_fields, apply_property_setters


def execute():
	make_custom_fields()
	apply_property_setters()
