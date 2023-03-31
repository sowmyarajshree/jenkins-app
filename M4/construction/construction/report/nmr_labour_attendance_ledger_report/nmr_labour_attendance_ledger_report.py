# Copyright (c) 2023, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import formatdate
from frappe import _


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns=get_columns(filters)
	data =get_data(filters)
	return columns, data

def get_columns(filters):
	return[
	{
	'label':_('Project'),
	'fieldtype':'Link',
	'fieldname':'project',
	'width':150,
	'options':'Project'
	},
	{
	'label':_('Posting Date'),
	'fieldtype':'Date',
	'fieldname':'posting_date',
	'width':140
	},
	{
	'label':_('Muster Roll'),
	'fieldtype':'Link',
	'fieldname':'muster_roll',
	'width':160,
	'options':'Muster Roll'
	},
	{
	'label':_('Wages'),
	'fieldtype':'Float',
	'fieldname':'wages',
	'width':120
	},
	{
	'label':_('Working Hours'),
	'fieldtype':'Float',
	'fieldname':'working_hours',
	'width':150
	},
	{
	'label':_('OT Hours'),
	'fieldtype':'Float',
	'fieldname':'ot_hours',
	'width':120
	},
	{
	'label':_('Revised In Time'),
	'fieldtype':'Float',
	'fieldname':'revised_in_time',
	'width':160
	},
	{
	'label':_('Revised Out Time'),
	'fieldtype':'Float',
	'fieldname':'revised_out_time',
	'width':160
	},
	{
	'label':_('Total Working Hours'),
	'fieldtype':'Float',
	'fieldname':'total_working_hours',
	'width':160
	},
	{
	'label':_('Total Worked Hours'),
	'fieldtype':'Float',
	'fieldname':'total_worked_hours',
	'width':160
	},
	{
	'label':_('Balance Hours'),
	'fieldtype':'Float',
	'fieldname':'balance_hours',
	'width':150
	},
	{
	'label':_('Status'),
	'fieldtype':'Select',
	'fieldname':'status',
	'width':160,
	'options':['Not Started','In Progress','Completed']
	},
	]

def get_data(filters):
	conditions=get_conditions(filters)
	return frappe.db.sql(""" 
		SELECT
		la.project,
		la.posting_date,
		mr.muster_roll,
		mr.wages,
		mr.working_hours,
		mr.ot_hours,
		mr.revised_in_time,
		mr.revised_out_time,
		mr.total_working_hours,
		mr.total_worked_hours,
		mr.balance_hours,
		la.status


		FROM 
		`tabLabour Attendance` la INNER JOIN `tabMuster Roll Detail` mr on mr.parent=la.name
		WHERE la.docstatus=1 and la.attendance_type="Muster Roll" %s


		ORDER BY
		la.project,
		la.posting_date
		 """ % conditions, filters, as_dict=1)



def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and la.project = %(project)s"
	if filters.get("to_date"):
		conditions +=" and la.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and la.posting_date >= %(from_date)s"
	if filters.get("status"):
		conditions +=" and la.status = %(status)s"
	if filters.get("muster_roll"):
		conditions +=" and mr.muster_roll = %(muster_roll)s"
	return conditions
