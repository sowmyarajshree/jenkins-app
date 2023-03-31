# Copyright (c) 2023, Nxweb and contributors
# For license information, please see license.txt

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
	'label'      :_('ID'),
	'fieldtype'  :'Link',
	'fieldname'  :'name',
	'width'      :170,
	'options':'Labour Attendance Revision'
	},
	{
	'label'      :_('Project'),
	'fieldtype'  :'Link',
	'fieldname'  :'project',
	'width'      :150,
	'options':'Project'
	},
	{
	'label'      :_('Posting Date'),
	'fieldtype'  :'Date',
	'fieldname'  :'posting_date',
	'width'      :120
	},
	{
	'label':'Subcontractor',
	'fieldtype':'Link',
	'fieldname':'subcontractor',
	'width'	   :150,
	'options' :"Supplier"
	},
	{
	'label'      :_('Revised Type'),
	'fieldtype'  :'Select',
	'fieldname'  :'revised_type',
	'width'      :130,
	'options':['Labour In','Labour Out']
	},
	{
	'label'      :_('Labourer'),
	'fieldtype'  :'Link',
	'fieldname'  :'labourer',
	'width'      :130,
	'options'    :'Labourer'
	},
	{
	'label'      :_('No Of Person'),
	'fieldtype'  :'Float',
	'fieldname'  :'no_of_person',
	'width'      :130
	},
	{
	'label'      :_('Revised Timing'),
	'fieldtype'  :'Select',
	'fieldname'  :'revised_timing',
	'width'      :130,
	'options':['Half Day','Full Day','Custom Hours']
	},
	{
	'label'      :_('Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'hours',
	'width'      :120
	},
	{
	'label'      :_('Total Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'total_hours',
	'width'      :120
	},
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		lar.name,
		lar.project,
		lar.posting_date,
		lar.subcontractor,
		lar.revised_type,
		rs.labourer,
		rs.no_of_person,
		rs.revised_timing,
		rs.hours,
		rs.total_hours


		FROM
			`tabLabour Attendance Revision` lar LEFT JOIN
			`tabLabour Attendance Revision Item Sub` rs on rs.parent=lar.name
		WHERE lar.docstatus = 1 and lar.attendance_type="Subcontractor" %s


		ORDER BY
		lar.project,
		lar.posting_date
		""" % conditions, filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and lar.project = %(project)s"
	if filters.get("to_date"):
		conditions +=" and lar.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and lar.posting_date >= %(from_date)s"
	if filters.get("subcontractor"):
		conditions +=" and lar.subcontractor = %(subcontractor)s"
	if filters.get("revised_type"):
		conditions +=" and lar.revised_type = %(revised_type)s"
	return conditions
