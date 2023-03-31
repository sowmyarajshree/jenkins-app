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
	   'label': _('Labour Progress Entry'),
	   'fieldtype': 'Link',
	   'fieldname': 'name',
	   'width': 200,
	   'options':'Labour Progress Entry',
	   },
	   {
	   'label': _('Project'),
	   'fieldtype': 'Link',
	   'fieldname': 'project_name',
	   'width': 200,
	   'options':'Project',
	   },
	   {
	   'label': _('Project Structure'),
	   'fieldtype': 'Link',
	   'fieldname': 'project_structure',
	   'width': 200,
	   'options':'Project Structure',
	   },
	   {
	   'label': _('Item of Work'),
	   'fieldtype': 'Data',
	   'fieldname': 'item_of_work',
	   'width': 200,
	   },
	  {
	   'label': _('Status'),
	   'fieldtype': 'Data',
	   'fieldname': 'status',
	   'width': 200,
	   }
	   ]


def get_data(filters):
	conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql(""" SELECT 
		                         lpe.name,
		                         lpe.project_name,
		                         lpe.project_structure,
		                         lpe.labour_type,
		                         lpe.item_of_work,
		                         lpe.status

		                     FROM 
		                         `tabLabour Progress Entry` lpe

		                     WHERE  
		                         lpe.docstatus = 1 and lpe.status = "To Prepared and Bill" %s """ %  conditions,filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("project_name"):
		conditions +=" and lpe.project_name = %(project_name)s"
		
	return conditions
















