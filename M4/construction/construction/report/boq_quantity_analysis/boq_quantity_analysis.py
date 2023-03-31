# Copyright (c) 2013, Nxweb and contributors
# For license information, please see license.txt
import frappe
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data_list = get_data(filters)
	data = []
	for i in data_list:
		row = ({
			 "name":i.name,
	         "project":i.project,
	         "project_structure":i.project_structure,
	         "item_of_work":i.item_of_work,
	         "estimate_quantity":i.estimate_quantity,
	         "excess_quantity":i.excess_quantity,
	         "est_total_qty":i.est_total_qty,
	         "percent": (i.excess_quantity/i.estimate_quantity) * 100
			})
		data.append(row)
	return columns, data



def get_columns(filters):
	return[
	   {
	   'label': _('Project'),
	   'fieldtype': 'Data',
	   'fieldname': 'project',
	   'width': 300,
	   },
	   {
	   'label': _('Project Structure'),
	   'fieldtype': 'Data',
	   'fieldname': 'project_structure',
	   'width': 300,
	   },
	   {
	   'label': _('Item Of Work'),
	   'fieldtype': 'Data',
	   'fieldname': 'item_of_work',
	   'width': 300,
	   },
	   {
	   'label': _('Percentage'),
	   'fieldtype': 'Percent',
	   'fieldname': 'percent',
	   'width': 300,
	   }

	   ]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(""" with temp as 



	 (SELECT boq.name as name,
	         boq.project as project,
	         boq.project_structure as project_structure,
	         boq.item_of_work as item_of_work,
	         boq.estimate_quantity as estimate_quantity,
	         boq.excess_quantity as excess_quantity,
	         boq.est_total_qty as est_total_qty

	  FROM `tabBOQ` boq 

	  WHERE  boq.docstatus = 1) 


	            SELECT 
	                  name,
	                  project,
	                  project_structure,
	                  item_of_work,
	                  estimate_quantity,
	                  excess_quantity,
	                  est_total_qty   
	            FROM 
	                  temp
	                   %s """ %  conditions,filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and boq.project = %(project)s"
	if filters.get("project_structure"):
		conditions +=" and boq.project_structure = %(project_structure)s"
	if filters.get("item_of_work"):
		conditions +=" and boq.item_of_work = %(item_of_work)s"	
	return conditions
