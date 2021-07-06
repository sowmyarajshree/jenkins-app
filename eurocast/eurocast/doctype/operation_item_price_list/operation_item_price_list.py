# -*- coding: utf-8 -*-
# Copyright (c) 2020, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class OperationItemPriceList(Document):

	def validate(self):
		self.validate_duplicate_record()


	def validate_duplicate_record(self):
			res = frappe.db.sql("""select name from `tabOperation Item Price List` where item = %s and operation = %s and supplier = %s and price_list = %s""",
				(self.item, self.operation, self.supplier, self.price_list))
			if res:
				frappe.throw("Entry for the Item price for the operation and supplier is already existed")

