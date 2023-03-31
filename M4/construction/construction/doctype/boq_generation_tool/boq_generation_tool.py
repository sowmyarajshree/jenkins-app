# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class BOQGenerationTool(Document):
	pass

@frappe.whitelist()
def get_boq_entry(project,proj_str):
	if project == "":
		frappe.throw(_("Enter project"))
	
	elif project != None and proj_str != None:
		boq_list = []
		boq_doc_list = frappe.get_list("BOQ",{"project":project,"project_structure":proj_str,"docstatus":1,"is_duplicate":0},["name","item_of_work","project_structure"])
		for i in boq_doc_list:
			boq_list.append({
			   "boq":i.name,
			   "item_of_work":i.item_of_work,
			   "project_structure":i.project_structure
			})
	
	elif proj_str == None:
		boq_list = []
		boq_doc_list = frappe.get_list("BOQ",{"project":project,"docstatus":1},["name","item_of_work","project_structure"])
		for i in boq_doc_list:
			boq_list.append({
			   "boq":i.name,
			   "item_of_work":i.item_of_work,
			   "project_structure":i.project_structure

			})
	return boq_list

@frappe.whitelist()
def create_boq(selected_boq,selected_proj_str):
	boq_list = eval(selected_boq)
	proj_str_list = eval(selected_proj_str)
	for i in boq_list:		
		for j in proj_str_list:
			boq_doc = frappe.get_doc("BOQ",i)
			duplicate_boq = frappe.copy_doc(boq_doc)
			duplicate_boq.created_from = boq_doc.name
			duplicate_boq.is_duplicate = 1
			duplicate_boq.project_structure = j
			duplicate_boq.work_status = "Not Scheduled"   
			duplicate_boq.billing_status = "To Quotation"
			duplicate_boq.task = None
			#duplicate_boq.qty_after_request = 

			duplicate_boq.save(ignore_permissions = True)
			frappe.db.commit()
		frappe.db.set_value("BOQ",i,"is_master",1)
		
	frappe.msgprint("BOQ is Created")

























