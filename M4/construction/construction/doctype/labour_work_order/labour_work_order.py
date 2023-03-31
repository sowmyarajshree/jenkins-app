# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class LabourWorkOrder(Document):
	def validate(self):
		self.status_update()
		self.validate_labour_item()

	def status_update(self):
		if self.docstatus == 0:
			self.status = "Active"

	def validate_labour_item(self):
		labour=[]
		for i in self.labour_rate_details:
			if i.labour_item not in labour:
				labour.append(i.labour_item)
			elif i.labour_item in labour:
					frappe.throw("Given Labour Name Already Exit")


@frappe.whitelist()
def set_close():
	frappe.db.sql(
	   """UPDATE `tabLabour Work Order` SET status='Expired'
	WHERE to_date < CURDATE()""")
	frappe.db.commit()

@frappe.whitelist()
def get_labour_list(project_name,labour_type,subcontractor):
	labour_list = frappe.db.get_list('Labour Progress Entry',{'project_name':project_name,'subcontractor':subcontractor,"docstatus":1},['labour'])
	return  list({d['labour'] for d in labour_list if d['labour']})


