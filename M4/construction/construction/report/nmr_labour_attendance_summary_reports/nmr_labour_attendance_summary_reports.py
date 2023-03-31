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
	'label':_('Project'),
	'fieldtype':'Link',
	'fieldname':'project',
	'width':150,
	'options':'Project'
	},
	{
	'label':_('ID'),
	'fieldtype':'Link',
	'fieldname':'name',
	'width':200,
	'options':'Labour Attendance'
	},
	{
	'label':_('Attendance Type'),
	'fieldtype':'Select',
	'fieldname':'attendance_type',
	'width':130,
	'options' :["Muster Roll"]
	},
	{
	'label':_('Muster Roll'),
	'fieldtype':'Link',
	'fieldname':'muster_roll',
	'width':160,
	'options':'Muster Roll'
	},
	{
	'label':_('Posting Date'),
	'fieldtype':'Date',
	'fieldname':'posting_date',
	'width':140
	},
	{
	'label':_('Accounting Period'),
	'fieldtype':'Link',
	'fieldname':'accounting_period',
	'width':200,
	'options':'Accounting Period'
	},
	{
	'label':_('Total No of Persons'),
	'fieldtype':'Int',
	'fieldname':'total_no_of_persons',
	'width':160
	},
	{
	'label':_('Total OT Hours'),
	'fieldtype':'Float',
	'fieldname':'total_ot_hours',
	'width':140
	},
	{
	'label':_('Total Working Hours'),
	'fieldtype':'Float',
	'fieldname':'total_working_hours',
	'width':160
	}
	]


def get_data(filters):
	conditions=get_conditions(filters)
	return frappe.db.sql(""" 
		SELECT
		la.project,
		la.name,
		la.attendance_type,
		GROUP_CONCAT(mr.muster_roll)AS muster_roll,
		la.posting_date,
		la.accounting_period,
		la.total_no_of_persons,
		la.total_ot_hours,
		la.total_working_hours

		FROM 
		`tabLabour Attendance` la INNER JOIN `tabMuster Roll Detail` mr on mr.parent=la.name
		WHERE la.docstatus=1 and la.attendance_type="Muster Roll" %s

		GROUP BY la.name

		ORDER BY
		la.project
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
