# Copyright (c) 2023, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns=get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	return[
	{
		'fieldname':'project',
		'label':_('Project'),
		'fieldtype':'Link',
		'width':150,
		'options':'Project'
	},
	{
		'fieldname':'labour_type',
		'label':_('Labour Type'),
		'fieldtype':'Select',
		'width':150,
		'options':['Muster Roll']
	},
	{
		'fieldname':'muster_roll',
		'label':_('Muster Roll'),
		'fieldtype':'Link',
		'width':150,
		'options':'Muster Roll'
	},
	{
		'fieldname':'posting_date',
		'label':_('Posting Date'),
		'fieldtype':'Date',
		'width':150,
	},
	{
		'fieldname':'total_hrs',
		'label':_('Total Hours From LPE'),
		'fieldtype':'Float',
		'width':180,
	},
	{
		'fieldname':'amount',
		'label':_('Total Amount From LA'),
		'fieldtype':'Float',
		'width':180,
	},
	{
		'fieldname':'total_lpe_hours',
		'label':_('Total Amount'),
		'fieldtype':'Float',
		'width':150,
	},
	{
		'fieldname':'tax_percentage',
		'label':_('Tax Percentage'),
		'fieldtype':'Float',
		'width':150,
	},
	{
		'fieldname':'tax_amount',
		'label':_('Tax Amount'),
		'fieldtype':'Float',
		'width':150,
	},
	{
		'fieldname':'grand_total',
		'label':_('Grand Total'),
		'fieldtype':'Float',
		'width':150,
	},
	{
		'fieldname':'rounded_total',
		'label':_('Rounded Total'),
		'fieldtype':'Float',
		'width':150,
	},
	]

def get_data(filters):
	conditions=get_conditions(filters)
	return frappe.db.sql(""" 
		SELECT 
        	mre.project,
			mre.labour_type,
			mre.muster_roll,
			mre.posting_date,
			lp.total_hrs,
			faf.amount,
			mre.total_lpe_hours,
			mre.tax_percentage,
			mre.tax_amount,
			mre.grand_total,
			mre.rounded_total
		FROM 
			`tabMuster Roll Entry` mre
			LEFT JOIN `tabLabour Progress Detail` lp on lp.parent=mre.name
			LEFT JOIN `tabF and F Item` faf on faf.parent=mre.name
			WHERE mre.docstatus=1 %s

		ORDER BY
		mre.project;
		 """ % conditions, filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and mre.project = %(project)s"
	if filters.get("to_date"):
		conditions +=" and mre.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and mre.posting_date >= %(from_date)s"
	#if filters.get("status"):
		#conditions +=" and mre.status = %(status)s"
	if filters.get("muster_roll"):
		conditions +=" and mre.muster_roll = %(muster_roll)s"
	return conditions