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
	'label'      :_('ID'),
	'fieldtype'  :'Link',
	'fieldname'  :'name',
	'width'      :170,
	'options':'Muster Roll Entry'
	},
	{
		'fieldname':'project',
		'label':_('Project'),
		'fieldtype':'Link',
		'width':150,
		'options':'Project'
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
		'fieldname':'labour_attendance',
		'label':_('Labour Attendance'),
		'fieldtype':'Link',
		'width':180,
		'options':'Labour Attendance'
	},
	{
		'fieldname':'date',
		'label':_('LA Date'),
		'fieldtype':'Date',
		'width':130,
	},
	{
		'fieldname':'total_person',
		'label':_('LA Total Person'),
		'fieldtype':'Float',
		'width':130,
	},
	{
		'fieldname':'hours_worked',
		'label':_('Hours Worked'),
		'fieldtype':'Float',
		'width':130,
	},
	{
		'fieldname':'rate',
		'label':_('Rate'),
		'fieldtype':'Float',
		'width':130,
	},
	{
		'fieldname':'amount',
		'label':_('LA Amount'),
		'fieldtype':'Float',
		'width':130,
	},
	{
		'fieldname':'total_amount',
		'label':_('Total Amount'),
		'fieldtype':'Float',
		'width':130,
	},
	{
		'fieldname':'total_hours',
		'label':_('Total Hours'),
		'fieldtype':'Float',
		'width':130,
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
	{
		'fieldname':'work_efficiency',
		'label':_('Work Efficiency'),
		'fieldtype':'Percent',
		'width':130,
	},
	{
		'fieldname':'status',
		'label':_('Status'),
		'fieldtype':'Select',
		'width':130,
		'options':['To Bill','Completed']
	},
	]

def get_data(filters):
	conditions=get_conditions(filters)
	return frappe.db.sql(""" 
		SELECT
			mre.name,
        	mre.project,
			mre.muster_roll,
			mre.posting_date,
			faf.labour_attendance,
			faf.date,
			faf.total_person,
			faf.hours_worked,
			faf.rate,
			faf.amount,
			mre.total_amount,
			mre.total_hours,
			mre.tax_percentage,
			mre.tax_amount,
			mre.grand_total,
			mre.rounded_total,
			mre.work_efficiency,
			mre.status
		FROM 
			`tabMuster Roll Entry` mre
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
	if filters.get("status"):
		conditions +=" and mre.status = %(status)s"
	if filters.get("muster_roll"):
		conditions +=" and mre.muster_roll = %(muster_roll)s"
	return conditions
