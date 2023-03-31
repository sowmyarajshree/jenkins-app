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
	'width'      :200,
	'options':'Labour OT Entry'
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
	'label'      :_('Subcontractor'),
	'fieldtype'  :'Link',
	'fieldname'  :'subcontractor',
	'width'      :130,
	'options'    :'Supplier'
	},
	{
	'label'      :_('Total No Of Person'),
	'fieldtype'  :'Float',
	'fieldname'  :'total_no_of_person',
	'width'      :130
	},
	{
	'label'      :_('Total OT Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'total_ot_hours',
	'width'      :120
	},
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		lot.name,
		lot.project,
		lot.posting_date,
		lot.subcontractor,
		lot.total_no_of_person,
		lot.total_ot_hours
		FROM
			`tabLabour OT Entry` lot
		WHERE lot.docstatus = 1 and lot.attendance_type="Subcontractor" %s

		ORDER BY
		lot.project,
		lot.posting_date
		""" % conditions, filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and lot.project = %(project)s"
	if filters.get("subcontractor"):
		conditions +=" and lot.subcontractor = %(subcontractor)s"
	if filters.get("to_date"):
		conditions +=" and lot.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and lot.posting_date >= %(from_date)s"
	# if filters.get("status"):
	# 	conditions +=" and f.status = %(status)s"
	return conditions