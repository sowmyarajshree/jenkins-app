from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


@frappe.whitelist()
def validate_material_labour(self,method):
	if self.nx_item_type == "Labour":
		self.is_stock_item = 0
	if self.nx_item_type == "Material":
		self.is_stock_item = 1

