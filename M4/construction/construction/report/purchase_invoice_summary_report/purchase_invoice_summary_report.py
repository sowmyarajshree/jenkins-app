# Copyright (c) 2023, Nxweb and contributors
# For license information, please see license.txt

# import frappe
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
	     'label': _('Date'),
	     'fieldtype': 'Date',
	     'fieldname': 'transaction_date',
	     'width': 200,
	     'options':'Purchase Order'
	    },
	    {
	    'label': _('Purchase Order'),
	    'fieldtype': 'Link',
	    'fieldname': 'purchase_order',
	    'width': 200,
	    'options':'Purchase Order'
	   },
	   {
	    'label': _('Purchase Receipt'),
	    'fieldtype': 'Link',
	    'fieldname': 'purchase_receipt',
	    'width': 200,
	    'options':'Purchase Receipt'
	   },
	   {
	    'label': _('Purchase Invoice'),
	    'fieldtype': 'Link',
	    'fieldname': 'name',
	    'width': 200,
	    'options':'Purchase Invoice'
	   },
	   {
	    'label': _('Date'),
	    'fieldtype': 'Date',
	    'fieldname': 'posting_date',
	    'width': 200
	   },
	   {
	   'label': _('Supplier Invoice No'),
	   'fieldtype': 'Data',
	   'fieldname': 'bill_no',
	   'width': 200
	   },
	   {
	    'label': _('Project'),
	    'fieldtype': 'Link',
	    'fieldname': 'project',
	    'width': 200,
	    'options':'Project'
	   },
	   {
	    'label': _('Supplier'),
	   'fieldtype': 'Link',
	   'fieldname': 'supplier',
	   'width': 200,
	   "options":"Supplier"
	   },
	   {
	    'label': _('Item Name'),
	   'fieldtype': 'Data',
	   'fieldname': 'item_name',
	   'width': 200

	   },
	   {
	    'label': _('Accepted Quantity'),
	   'fieldtype': 'Float',
	   'fieldname': 'qty',
	   'width': 200

	   },
	   {
	    'label': _('Rate'),
	   'fieldtype': 'Float',
	   'fieldname': 'rate',
	   'width': 200

	   },
	   {
	    'label': _('Amount'),
	   'fieldtype': 'Float',
	   'fieldname': 'amount',
	   'width': 200

	   },
	   {
	    'label': _('Total'),
	   'fieldtype': 'Float',
	   'fieldname': 'total',
	   'width': 200

	   },
	   {
	    'label': _('Purchase Taxes and Charges Template'),
	   'fieldtype': 'Data',
	   'fieldname': 'taxes_and_charges',
	   'width': 200

	   },
	   {
	    'label': _('Grand Total'),
	   'fieldtype': 'Float',
	   'fieldname': 'grand_total',
	   'width': 200
	   }
	   ]

def get_data(filters):
	conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql("""
	SELECT
	    po.transaction_date,
	    pi.purchase_order,
	    pi.purchase_receipt,
	    p.posting_date,
	    p.name,
	    p.supplier,
	    p.bill_no,
	    p.project,
	    pi.item_name,
	    pi.qty,
	    pi.rate,
	    pi.amount,
	    p.total,
	    p.taxes_and_charges,
	    p.grand_total
	    

	    
	FROM
	    `tabPurchase Invoice` p left join `tabPurchase Invoice Item` pi on p.name=pi.parent  left join `tabPurchase Order` po on pi.purchase_order=po.name

    WHERE
        pi.parent = p.name and p.docstatus = 1 %s  """% conditions, filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("supplier"):
		conditions +=" and p.supplier = %(supplier)s"
	if filters.get("from_date"):
		conditions += "and p.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += "and p.posting_date <= %(to_date)s"
	if filters.get("project"):
		conditions += "and p.project_name = %(project)s"
	return conditions
