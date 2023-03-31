# Copyright (c) 2021, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class ProjectPlaning(Document):
	def validate(self):
		self.validate_project()


	def validate_project(self):
		if self.project == None:
			frappe.throw(_("Project cannot be Empty"))

@frappe.whitelist()
def get_boq_entry(project,proj_str,item_of_work):
	boq = []
	if (project == ""):
		frappe.throw(_("Project Cannot be Empty"))
	if (project != None and item_of_work == "" and proj_str == ""):
		boq_li = frappe.get_list("BOQ",{"project":project,"work_status":"Not Scheduled","docstatus":1},["name"])
		if len(boq_li) == 0:
			frappe.throw(_("BOQ is not created against for given project" ))
		for b in boq_li:
			boq.append({
				"boq":b.name
			 })
	elif (project != None and proj_str != "" and item_of_work != ""):
		boq_li = frappe.get_list("BOQ",{"project":project,"work_status":"Not Scheduled","project_structure":proj_str,"item_of_work":item_of_work,"docstatus":1},["name"])
		if len(boq_li) == 0:
			frappe.throw(_("BOQ is not created against for given project structure and Item of work"))
		for b in boq_li:
			boq.append({
				"boq":b.name
			})
	elif (project != None and proj_str != "" and item_of_work == ""):
		boq_li = frappe.get_list("BOQ",{"project":project,"project_structure":proj_str,"work_status":"Not Scheduled","docstatus":1},["name"])
		if len(boq_li) == 0:
			frappe.throw(_("BOQ is not created against for given project and project structure"))
		for b in boq_li:
			boq.append({
				"boq":b.name
				})
	elif (project != None and proj_str == "" and item_of_work != ""):
		boq_li = frappe.get_list("BOQ",{"project":project,"item_of_work":item_of_work,"work_status":"Not Scheduled","docstatus":1},["name"])
		if len(boq_li) == 0:
			frappe.throw(_("BOQ is not created against for given project and item_of_work"))
		for b in boq_li:
			boq.append({
				"boq":b.name
				})
	return boq

@frappe.whitelist()
def create_task(items):
	item1 = eval(items)
	for i in item1:
		boq_doc = frappe.get_doc("BOQ",i)
		task_doc = frappe.new_doc("Task")
		task_doc.update({
			"subject":boq_doc.project,
			"project":boq_doc.project,
			"nx_project_structure":boq_doc.project_structure,
			"nx_boq_id":boq_doc.name,
			"nx_item_of_work":boq_doc.item_of_work,
			"nx_qty":boq_doc.estimate_quantity,
			"nx_primary_labour_qty":boq_doc.primary_labour_qty
			})
		task_doc.save(ignore_permissions = True)
		frappe.msgprint(_("Task is Created {0}").format(task_doc.name))
	


















