# Copyright (c) 2013, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data_list = get_data(filters)
	data = []
	for i in data_list:
		row = ({
			"name":i.name,
			"item_of_work":i.item_of_work,
			"uom":i.to_uom,
			"project":i.project,
			"project_structure":i.project_structure,
			"qty":i.qty,
			"actual_qty":i.actual_qty,
			"balance_qty":i.balance_qty,
			"item":i.item,
			"labour":i.labour,
			"mat_qty":    frappe.db.get_value("BOQ Material Detail",{"parent":i.name,"item_code":i.item},["qty"]),
			"mat_rate":   frappe.db.get_value("BOQ Material Detail",{"parent":i.name,"item_code":i.item},["rate"]),
			"mat_amount": frappe.db.get_value("BOQ Material Detail",{"parent":i.name,"item_code":i.item},["amount"]),
			"lab_qty":    frappe.db.get_value("BOQ Labour Detail",{"parent":i.name,"labour":i.labour},["qty"]),
			"lab_rate":   frappe.db.get_value("BOQ Labour Detail",{"parent":i.name,"labour":i.labour},["rate"]),
			"lab_amount": frappe.db.get_value("BOQ Labour Detail",{"parent":i.name,"labour":i.labour},["amount"]),
			"total_other_taxes_and_charges":i.total_other_taxes_and_charges,
			"grand_total":i.grand_total
			})
		data.append(row)

	return columns,data







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
	'fieldtype': 'Link',
	'fieldname': 'project',
	'width': 200,
	'options':'Project',
	},
	{
	'label': _('Project Structure'),
	'fieldtype': 'Data',
	'fieldname': 'project_structure',
	'width': 200,
	},
	{
	'label': _('Item of Work'),
	'fieldtype': 'Link',
	'fieldname': 'item_of_work',
	'width': 200,
	'options':'Item of Work',
	},
	{
	'label': _('Item'),
	'fieldtype': 'Data',
	'fieldname': 'item',
	'width': 200,
	},
	{
	'label': _('UOM'),
	'fieldtype': 'Data',
	'fieldname': 'uom',
	'width': 200,
	},
	{
	'label': _('Material Qty'),
	'fieldtype': 'Float',
	'fieldname': 'mat_qty',
	'width': 200,
	},
	{
	'label': _('Material Rate'),
	'fieldtype': 'Float',
	'fieldname': 'mat_rate',
	'width': 200,
	},
	{
	'label': _('Material Amount'),
	'fieldtype': 'Float',
	'fieldname': 'mat_amount',
	'width': 200,
	},
	{
	'label': _('Labour'),
	'fieldtype': 'Link',
	'fieldname': 'labour',
	'width': 200,
	'options':'Item'
	},
	{
	'label': _('Labour Qty'),
	'fieldtype': 'Float',
	'fieldname': 'lab_qty',
	'width': 200,
	},
	{
	'label': _('Labour Rate'),
	'fieldtype': 'Float',
	'fieldname': 'lab_rate',
	'width': 200,
	},
	{
	'label': _('Labour Amount'),
	'fieldtype': 'Float',
	'fieldname': 'lab_amount',
	'width': 200,
	},
	{
	'label': _('Other Taxes and Charges Rate'),
	'fieldtype': 'Float',
	'fieldname': 'otc_rate',
	'width': 240,
	},
	
	{
	'label': _('Other Taxes and Charges Total'),
	'fieldtype': 'Float',
	'fieldname': 'total_other_taxes_and_charges',
	'width': 240,
	},
	{
	'label': _('Grand Total'),
	'fieldtype': 'Float',
	'fieldname': 'grand_total',
	'width': 240,
	}
	
	
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		    boq.name ,
            boq.item_of_work ,
            boq.project ,
            boq.project_structure ,
            boq.to_uom,
            boq.total_other_taxes_and_charges,
            CASE WHEN boq.has_conversion = 1 THEN boq.amount_after_conversion ELSE boq.grand_total END AS grand_total,
            bl.labour ,
            bl.qty ,
            bl.actual_qty ,
            bl.balance_qty,
            bl.item,
            bl.labour

        FROM
            `tabBOQ` boq LEFT JOIN
            `tabBOQ Ledger` bl ON  bl.boq =  boq.name

        WHERE 
            boq.docstatus = 1 and (bl.ledger_type = "Labour" or bl.ledger_type = "Material")%s

        GROUP BY
            boq.name,bl.labour,bl.item  """ % conditions,filters,as_dict = 1)



def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and boq.project = %(project)s"
	if filters.get("project_structure"):
		conditions +=" and boq.project_structure = %(project_structure)s"
	if filters.get("item_of_work"):
		conditions +=" and boq.item_of_work = %(item_of_work)s"
	if filters.get("from_date"):
		conditions +=" and boq.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions +=" and boq.posting_date <= %(to_date)s"
	return conditions

