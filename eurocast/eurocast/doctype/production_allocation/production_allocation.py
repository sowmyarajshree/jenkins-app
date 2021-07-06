# -*- coding: utf-8 -*-
# Copyright (c) 2020, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ProductionAllocation(Document):

#validate duplicate production allocation based on item, serial_no and workstation
	def validate_duplicate_record(self):
			res = frappe.db.sql("""select name from `tabProduction Allocation` where workstation = %s and serial_no = %s
				and item = %s and docstatus = 1 and nx_is_disabled = 0""",
				(self.workstation, self.serial_no, self.item))
			if res:
				frappe.throw(_("Entry for the same item, serial no, workstation and  for {0} is already existed").format(self.workstation))





	def validate(self):
		self.validate_duplicate_record()
