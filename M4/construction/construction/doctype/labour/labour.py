# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe import _

class Labour(Document):
	def validate(self):
		self.validte_uom_conversion()

	def validte_uom_conversion(self):
		if ((self.uom_conversion_factor == None) or (self.uom_conversion_factor == 0)):
			frappe.throw("Uom Conversion Factor cannot be Zero")