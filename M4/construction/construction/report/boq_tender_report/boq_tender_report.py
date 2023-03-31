# # Copyright (c) 2023, Nxweb and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data
def get_columns(filters):
    return[    
    	{
			"label": "Project",
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width":200
			
		},
		{
			"label": "Project Structure",
			"fieldname": "project_structure",
			"fieldtype": "Link",
			"options": "Project Structure",
			"width":200

			
		},
		{
			"label": "Item Of Work",
			"fieldname": "item_of_work",
			"fieldtype": "Link",
			"options": "Item of Work",
			"width":200

		},
		{
			"label": "Work Status",
			"fieldname": "work_status",
			"fieldtype": "Select",
			"options": ["", "Sheduled", "Not Sheduled", "In Progress", "Completed"],
			"width":200

		},
		{
			"label": "Billing Status",
			"fieldname": "billing_status",
			"fieldtype": "Select",
			"options": ["", "To Quotation", "To Order", "Order", "Not Billable"],
			"width":200

		},
		{
			"label": "Estimate Quantity",
			"fieldname": "estimate_quantity",
			"fieldtype": "Float",
			"width":180

		}        
	        ]

def get_data(filters):
	conditions=get_conditions(filters)
	return frappe.db.sql("""
        SELECT 
            boq.project, boq.project_structure, boq.item_of_work, boq.work_status, boq.billing_status, boq.estimate_quantity
        FROM 
            `tabBOQ` boq
        WHERE 
         boq.docstatus = 1 %s 
        ORDER BY
         boq.project """ % conditions, filters, as_dict=1) 

def get_conditions(filters):
    conditions = ""
    if filters.get("project"):
        conditions += "and boq.project = %(project)s"
    if filters.get("project_structure"):
        conditions += "and boq.project_structure = %(project_structure)s"
    if filters.get("item_of_work"):
        conditions += "and boq.item_of_work = %(item_of_work)s"
    if filters.get("work_status"):
        conditions += "and boq.work_status = %(work_status)s"
    if filters.get("billing_status"):
        conditions += "and boq.billing_status = %(billing_status)s"        
    return conditions
