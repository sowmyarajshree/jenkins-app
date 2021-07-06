# Copyright (c) 2013, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _

def execute(filters=None):
	data = []
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	get_data(filters,data)
	return columns, data


def get_columns(filters):
	return [{
		'label': _('Sales Plan'),
		'fieldtype': 'Link',
		'fieldname': 'sales_plan',
		'width': 100,
		'options':'Sales Plan',
	},
	{
		'label': _('Item Code'),
		'fieldtype': 'Link',
		'fieldname': 'item_code',
		'width': 100,
		'options':'Item',
	},
	{
		'label': _('Planned Date'),
		'fieldtype': 'Date',
		'fieldname': 'posting_date',
		'width': 100
	},
	{
		'label': _('Planned Frequency'),
		'fieldtype': 'Select',
		'fieldname':'sales_plan_frequency',
		'options': ["Daily","Weekly","Monthly"],
		'width': 100
	},
	{
		'label': _('Planned Qty'),
		'fieldtype': 'Float',
		'fieldname': 'qty',
		'width': 100
	},
	{
		'label': _('Delivered Qty'),
		'fieldtype': 'Float',
		'fieldname': 'delivered_qty',
		'width': 100,
	},
	{
		'label': _('Difference Qty'),
		'fieldtype': 'Float',
		'fieldname': 'difference_qty',
		'width': 100,
	}
	]

def get_data(filters, data):
	get_sales_plan_entries(filters,data)

def get_sales_plan_entries(filters,data):
	conditions = get_conditions(filters)
	sales_plan_ledger_entries = frappe.db.sql("""SELECT spl.name as spl_name ,spl.sales_plan, spl.qty, spl.posting_date, spl.item_code, spl.sales_plan_frequency
								FROM `tabSales Plan Ledger Entry` spl
								WHERE
									spl.docstatus = 1 %s""" % conditions, filters, as_dict=1)

	for d in sales_plan_ledger_entries:
		data.append({
				"sales_plan": d.sales_plan,
				"qty": d.qty,
				"posting_date": d.posting_date,
				"item_code": d.item_code,
				"sales_plan_frequency": d.sales_plan_frequency
		})
		delivered_note = frappe.get_list("Delivery Note",filters={"posting_date": d.posting_date},fields=["name"])
		for dl in delivered_note:
			delivered_qty = frappe.get_value("Delivery Note Item",{"parent": dl.name},["qty"])
			if delivered_qty != None:
				data.append({
					"delivered_qty": delivered_qty,
					"difference_qty": delivered_qty - d.qty
				})
		if filters.get("group_by_item"):
			row =[]
			data.append(row)

def get_conditions(filters):
	conditions = ""
	if filters.get("item_code"):
		conditions +=" and spl.item_code = %(item_code)s"
	if filters.get("sales_plan_frequency"):
		conditions +=" and spl.sales_plan_frequency = %(sales_plan_frequency)s"
	if filters.get("to_date"):
		conditions +=" and spl.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and spl.posting_date >= %(from_date)s"
	if filters.get("group_by_item"):
		conditions +="GROUP BY spl.item_code"

	return conditions
