# Copyright (c) 2013, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
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
	'label': _('Item of Work'),
	'fieldtype': 'Link',
	'fieldname': 'item_of_work',
	'width': 200,
	'options':'Item of Work',
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
	'label': _('Labour'),
	'fieldtype': 'Link',
	'fieldname': 'labour',
	'width': 200,
	'options':'Item'
	},
	{
	'label': _('Estimated Qty'),
	'fieldtype': 'Float',
	'fieldname': 'qty',
	'width': 200,
	},
	{
	'label': _('Actual Qty'),
	'fieldtype': 'Float',
	'fieldname': 'actual_qty',
	'width': 200,
	},
	{
	'label': _('Balance Qty'),
	'fieldtype': 'Float',
	'fieldname': 'balance_qty',
	'width': 200,
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
            bl.labour ,
            bl.qty ,
            bl.actual_qty ,
            bl.balance_qty
        FROM
            `tabBOQ` boq LEFT JOIN
            `tabBOQ Labour Detail` bd ON bd.parent = boq.name LEFT JOIN
            `tabBOQ Ledger` bl ON  bl.boq =  boq.name
        WHERE 
            boq.docstatus = 1 and bl.ledger_type = "Labour" %s
        GROUP BY
            boq.name,bl.labour  """ % conditions,filters,as_dict = 1)



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

































