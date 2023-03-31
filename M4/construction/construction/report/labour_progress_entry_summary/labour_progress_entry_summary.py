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
	# frappe.msgprint("{0}".format(data))
	return columns, data

def get_columns(filters):
	return[
	 
	   {
	   'label': _('Project'),
	   'fieldtype': 'Link',
	   'fieldname':'project_name',
	   'width': 200,
	   'options':'Project',
	   },
	   {
	   'label' : _('Project Structure'),
	   'fieldtype' : 'Link',
	   'field_name' : 'project_structure',
	   'width' : 200,
	   'options' : 'Project Structure'
	   },
	   {
	   'label' : _('Item of Work'),
	   'fieldtype' : 'Link',
	   'field_name' : 'item_of_work',
	   'width' : 200,
	   'options' : 'Item of Work'
	   },
	   {
	   'label' : _('UOM'),
	   'fieldtype' : 'Link',
	   'field_name' : 'uom',
	   'width' : 200,
	   'options' : 'UOM'
	   },
	   {
	   'label' : _('Subcontractor'),
	   'fieldtype' : 'Link',
	   'field_name' : 'subcontractor',
	   'width' : 200,
	   'options' : 'Supplier'
	   },
	   {
	   'label' : _('Labour Type'),
	   'fieldtype' : 'Select',
	   'field_name' : 'labour_type',
	   'width' : 200,
	   'options' : ["F and F","Rate Work","Muster Roll"]
	   },
	   {
	   'label' : _('Qty'),
	   'fieldtype' : 'Float',
	   'field_name' : 'qty',
	   'width' : 200
	   },
	   {
	   'label' : _('Length'),
	   'fieldtype' : 'Float',
	   'field_name' : 'length',
	   'width' : 200
	   },
	   {
	   'label' : _('Breadth'),
	   'fieldtype' : 'Float',
	   'field_name' : 'breadth',
	   'width' : 200
	   },
	   {
	   'label' : _('Depth'),
	   'fieldtype' : 'Float',
	   'field_name' : 'depth',
	   'width' : 200
	   },
	   {
	   'label' : _('Quantity'),
	   'fieldtype' : 'Float',
	   'field_name' : 'quantity',
	   'width' : 200
	   },
	   
	   ]


def get_data(filters):
	conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql("""
	SELECT
	    lpe.name, lpe.project_name, lpe.project_structure, lpe.subcontractor, lpe.item_of_work, lpe.labour_type, lpe.uom,
	    lped.length, lped.breadth, lped.depth_height, lped.quantity,lpe.total_qty as qty
	FROM
	    `tabLabour Progress Entry` lpe LEFT JOIN
	    `tabMeasurement Sheet Detail` lped ON lpe.name = lped.parent
    WHERE
        lpe.docstatus = 1 %s """ % conditions, filters, as_dict=1)






def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions +=" and lpe.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions +=" and lpe.posting_date <= %(to_date)s"
	if filters.get("project_name"):
		conditions +=" and lpe.project_name = %(project_name)s"
	if filters.get("labour_type"):
		conditions +=" and lpe.labour_type = %(labour_type)s"
	if filters.get("item_of_work"):
		conditions +=" and lpe.item_of_work = %(item_of_work)s"
	return conditions
