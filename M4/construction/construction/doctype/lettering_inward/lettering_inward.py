# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LetteringInward(Document):
	def before_insert(self):
		self.workflow_status_copy()
	
	def validate(self):
		self.workflow_status_copy_for_approval()

	def workflow_status_copy(self):
		self.status = "Draft"

	def workflow_status_copy_for_approval(self):
		if self.workflow_state == "Approved":
			self.status = "Approved"

