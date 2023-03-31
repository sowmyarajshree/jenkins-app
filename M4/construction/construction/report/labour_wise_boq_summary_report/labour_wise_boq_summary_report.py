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
			"work_status":i.work_status,
			"billing_status":i.billing_status,
			"total_labour_cost":i.total_labour_cost,
			"total_material_cost":i.total_material_cost,
			"total_other_taxes_and_charges":i.total_other_taxes_and_charges,
			"grand_total":i.grand_total,
			"est_total_qty":i.est_total_qty,
			"rounded_total":i.rounded_total,
			"labour":i.labour
			})
		iow_value = frappe.db.get_value("Item of Work",{"name":i.item_of_work},["name"])
		iow_doc = frappe.get_doc("Item of Work",iow_value)
		row.update({
			"item_of_work":iow_doc.item_of_work
			})

		pro_str_value = frappe.db.get_value("Project Structure",{"name":i.project_structure},["name"])
		pro_str_doc = frappe.get_doc("Project Structure",pro_str_value)
		row.update({
			"project_structure":pro_str_doc.project_structure
			})

		
		if i.labour:
			lab_det = frappe.db.get_list("BOQ Labour Detail",{"parent":i.name,"labour":i.labour},["labour","qty","rate","amount"])
			row.update({
			   # "labour":lab_det[0].labour,
				"lab_qty":lab_det[0].qty,
				"lab_rate":lab_det[0].rate,
				"lab_amount":lab_det[0].amount,				
				})
		
		data.append(row)
	return columns, data

def get_columns(filters):
	return[
	 {
	   'label': _('BOQ'),
	   'fieldtype': 'Link',
	   'fieldname': 'name',
	   'width': 200,
	   'options':'BOQ',
	   },
	   {
	   'label': _('Project'),
	   'fieldtype': 'Data',
	   'fieldname': 'project',
	   'width': 200,
	   'options':'Project',
	   },
	   {
	   'label': _('Project Structure'),
	   'fieldtype': 'Data',
	   'fieldname': 'project_structure',
	   'width': 200,
	   'options':'Project Structure',
	   },
	   {
	   'label': _('Item Of Work'),
	   'fieldtype': 'Data',
	   'fieldname': 'item_of_work',
	   'width': 200,
	   'options':'Item of Work',
	   },
	   {
	   'label': _('Work Status'),
	   'fieldtype': 'Data',
	   'fieldname': 'work_status',
	   'width': 200,
	   },
	   {
	   'label': _('Billing Status'),
	   'fieldtype': 'Data',
	   'fieldname': 'billing_status',
	   'width': 200,
	   },
	   {
	   'label': _('Total Labour Cost'),
	   'fieldtype': 'Float',
	   'fieldname': 'total_labour_cost',
	   'width': 200	   
	   },
	   {
	   'label': _('Total Material Cost'),
	   'fieldtype': 'Float',
	   'fieldname': 'total_material_cost',
	   'width': 200
	   },
	    {
	   'label': _('Grand Total'),
	   'fieldtype': 'Float',
	   'fieldname': 'grand_total',
	   'width': 200,
	   },
	   {
	   'label': _('Total Other Taxes and Charges'),
	   'fieldtype': 'Float',
	   'fieldname': 'total_other_taxes_and_charges',
	   'width': 200
	   },
	   {
	   'label': _('Total Quantity'),
	   'fieldtype': 'Float',
	   'fieldname': 'est_total_qty',
	   'width': 200
	   },
	   {
	   'label': _('Rounded Total'),
	   'fieldtype': 'Float',
	   'fieldname': 'rounded_total',
	   'width': 200
	   },
	   {
	   'label': _('Labour'),
	   'fieldtype': 'Data',
	   'fieldname': 'labour',
	   'width': 200
	   },
	   {
	   'label': _('Labour Qty'),
	   'fieldtype': 'Data',
	   'fieldname': 'lab_qty',
	   'width': 200
	   },
	   {
	   'label': _('Labour Rate'),
	   'fieldtype': 'Data',
	   'fieldname': 'lab_rate',
	   'width': 200
	   },
	   {
	   'label': _('Labour Amount'),
	   'fieldtype': 'Data',
	   'fieldname': 'lab_amount',
	   'width': 200
	   }
	   
	   

	   ]


def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql(""" SELECT 
		                           boq.name,boq.project,boq.project_structure,
		                           boq.item_of_work,boq.work_status,boq.billing_status,
		                           boq.total_labour_cost,boq.total_material_cost,boq.total_other_taxes_and_charges,
		                           boq.grand_total,boq.est_total_qty,boq.rounded_total,bl.labour



		                     FROM `tabBOQ` boq LEFT JOIN
                                  `tabBOQ Ledger` bl ON  bl.boq =  boq.name

                             WHERE 
                                  boq.docstatus = 1 and bl.ledger_type = "Labour"

                             GROUP BY
                                  boq.name,bl.labour %s """ %  conditions,filters, as_dict=1)


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
	if filters.get("billing_status"):
		conditions +=" and boq.billing_status = %(billing_status)s"
	
	
	
	
	return conditions















