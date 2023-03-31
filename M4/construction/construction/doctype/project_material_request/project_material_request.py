# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class ProjectMaterialRequest(Document):
	def before_submit(self):
		self.auto_creation_of_material_request_purchase()
		self.auto_creation_of_material_request_transfer()
		self.validate_material_request_type()
		self.auto_creation_of_material_request_both_pur()
		self.auto_creation_of_material_request_both_trans()

	def before_cancel(self):
		self.delete_stock_entry_if_draft()

	def validate(self):
		pass
		#self.set_purpose_type()

#purpose_type to copy in all rows
	def set_purpose_type(self):
		if self.purpose_type == "Purchase":
			for i in self.material_request_details:
				i.material_request_type = "Purchase"
				if i.material_request_type != "Purchase":
					frappe.throw(_("Material request type must be Purchase"))
				else:
					pass

		if self.purpose_type == "Transfer":
			for i in self.material_request_details:
				i.material_request_type = "Transfer"
				if i.material_request_type != "Transfer":
					frappe.throw(_("Material request type must be Transfer"))
				else:
					pass

#purpose_type as mandatory
	def validate_material_request_type(self):
		if self.purpose_type == None:
			frappe.throw(_("Purchase Type is Mandatory"))
		for i in self.material_request_details:
			if (i.material_request_type != "Transfer") and (i.material_request_type != "Purchase"):
				frappe.throw("Material Request Type is Mandatory")

#auto creation of material request if purpose_type is Purchase on submit 
	def auto_creation_of_material_request_purchase(self):
		if self.purpose_type == "Purchase":
			material_req_doc = frappe.new_doc("Material Request")
			for i in self.material_request_details:
				if i.material_request_type == "Purchase":
					material_req_doc.update({
						"transaction_date":self.date,
						"material_request_type":"Purchase",
						"project":self.project,
						"schedule_date":self.date,
						"nx_project_material_request":self.name
						})
					material_req_doc.append("items",{
						"item_code":i.item_code,
						"qty":i.qty,
						"description":i.description,
						"warehouse":self.warehouse
				})
			material_req_doc.save()
			frappe.msgprint(_("Material request is created {0}").format(material_req_doc.name))

#auto creation of material request if purpose_type is Transfer on submit 
	def auto_creation_of_material_request_transfer(self):
		if self.purpose_type == "Transfer":
			material_req_doc = frappe.new_doc("Material Request")
			for i in self.material_request_details:
				if i.material_request_type == "Transfer":
					material_req_doc.update({
						"material_request_type":"Material Transfer",
						"project":self.project,
						"schedule_date":self.date,
						"nx_project_material_request":self.name
						})
					material_req_doc.append("items",{
						"item_code":i.item_code,
						"qty":i.qty,
						"description":i.description,
						"warehouse":self.warehouse
				})
			material_req_doc.save()
			frappe.msgprint(_("Material request is created {0}").format(material_req_doc.name))

#auto creation of material request if purpose_type is Purchase/Transfer on submit 
	def auto_creation_of_material_request_both_pur(self):
		if self.purpose_type == "Purchase/Transfer":
			material_req_doc = frappe.new_doc("Material Request")
			for i in self.material_request_details:
				if i.material_request_type == "Purchase":
					material_req_doc.update({
						"material_request_type":"Purchase",
						"project":self.project,
						"schedule_date":self.date,
						"nx_project_material_request":self.name
						})
					material_req_doc.append("items",{
						"item_code":i.item_code,
						"qty":i.qty,
						"description":i.description,
						"warehouse":self.warehouse
				})
			material_req_doc.save()
			frappe.msgprint(_("Material request is created {0}").format(material_req_doc.name))

#auto creation of material request if purpose_type is Purchase/Transfer on submit 
	def auto_creation_of_material_request_both_trans(self):
		if self.purpose_type == "Purchase/Transfer":
			material_req_doc = frappe.new_doc("Material Request")
			for i in self.material_request_details:
				if i.material_request_type == "Transfer":
					material_req_doc.update({
						"material_request_type":"Material Transfer",
						"project":self.project,
						"schedule_date":self.date,
						"nx_project_material_request":self.name
						})
					material_req_doc.append("items",{
						"item_code":i.item_code,
						"qty":i.qty,
						"description":i.description,
						"warehouse":self.warehouse
				})
			material_req_doc.save()
			frappe.msgprint(_("Material request is created {0}").format(material_req_doc.name))

#delete the stock_entry if it is in Draft
	def delete_stock_entry_if_draft(self):
		stock_name = frappe.get_list("Material Request",{"nx_project_material_request":self.name},["name"])
		for i in stock_name:
			mat_req_doc = frappe.get_doc("Material Request",i.name)
			if mat_req_doc.docstatus == 0:
				frappe.delete_doc("Material Request",mat_req_doc.name)























		
