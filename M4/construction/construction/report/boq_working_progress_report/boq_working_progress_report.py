# Copyright (c) 2013, Nxweb and contributors
# For license information, please see license.txt
import frappe
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data



def get_columns(filters):
	return[
	   {
	   'label': _('Project'),
	   'fieldtype': 'Data',
	   'fieldname': 'project',
	   'width': 230,
	   },
	   {
	   'label': _('Project Structure'),
	   'fieldtype': 'Data',
	   'fieldname': 'project_structure',
	   'width': 230,
	   },
	   {
	   'label': _('Item Of Work'),
	   'fieldtype': 'Data',
	   'fieldname': 'item_of_work',
	   'width': 230,
	   },
	   {
	   'label': _('Work Status'),
	   'fieldtype': 'Data',
	   'fieldname': 'work_status',
	   'width': 230,
	   },
	    {
	   'label': _('Working Percentage'),
	   'fieldtype': 'Percent',
	   'fieldname': 'working_progress',
	   'width': 230,
	   }

	   ]

def get_data(filters):
	conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql(""" SELECT boq.name,boq.project,boq.project_structure,boq.item_of_work,boq.work_status,boq.billing_status,boq.working_progress,boq.billing_progress

		                     FROM `tabBOQ` boq 

		                     WHERE  boq.docstatus = 1 %s """ %  conditions,filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and boq.project = %(project)s"
	if filters.get("project_structure"):
		conditions +=" and boq.project_structure = %(project_structure)s"
	if filters.get("item_of_work"):
		conditions +=" and boq.item_of_work = %(item_of_work)s"
	if filters.get("work_status"):
		conditions +=" and boq.work_status = %(work_status)s"
	
	
	
	
	return conditions
