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
	'width'      :140,
	'options':'F and F Entry'
	},
	{
	'label'      :_('Project'),
	'fieldtype'  :'Link',
	'fieldname'  :'project',
	'width'      :140,
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
	'label'      :_('Labour Attendance'),
	'fieldtype'  :'Link',
	'fieldname'  :'labour_attendance',
	'width'      :140,
	'options'    :'Labour Attendance'
	},
	{
	'label'      :_('LA Date'),
	'fieldtype'  :'Date',
	'fieldname'  :'date',
	'width'      :120
	},
	{
	'label'      :_('Labourer'),
	'fieldtype'  :'Link',
	'fieldname'  :'labourer',
	'width'      :140,
	'options':'Labourer'
	},
	{
	'label'      :_('Total Person'),
	'fieldtype'  :'Float',
	'fieldname'  :'total_person',
	'width'      :120
	},
	{
	'label'      :_('Hours Worked'),
	'fieldtype'  :'Float',
	'fieldname'  :'hours_worked',
	'width'      :120
	},
	{
	'label'      :_('Rate'),
	'fieldtype'  :'Float',
	'fieldname'  :'rate',
	'width'      :120
	},
	{
	'label'      :_('Amount'),
	'fieldtype'  :'Float',
	'fieldname'  :'amount',
	'width'      :120
	},
	{
    "fieldname":"status",
	"label": _("Status"),
	"fieldtype": "Select",
	"width": 150,
	"options":[" ","To Bill","Completed"]
	},
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		f.name,
		f.project,
		f.subcontractor,
		f.posting_date,
		fi.labour_attendance,
		fi.date,
		fi.labourer,
		fi.total_person,
		fi.hours_worked,
		fi.rate,
		fi.amount,
		f.status
		FROM
			`tabF and F Entry` f LEFT JOIN
			`tabF and F Item` fi on fi.parent=f.name 
		WHERE f.docstatus = 1 %s

		-- GROUP BY
		-- f.name

		ORDER BY
		f.project
		""" % conditions, filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and f.project = %(project)s"
	if filters.get("subcontractor"):
		conditions +=" and f.subcontractor = %(subcontractor)s"
	if filters.get("to_date"):
		conditions +=" and f.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and f.posting_date >= %(from_date)s"
	if filters.get("status"):
		conditions +=" and f.status = %(status)s"
	return conditions