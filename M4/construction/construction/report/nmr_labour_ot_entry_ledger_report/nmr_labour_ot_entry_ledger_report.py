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
	'width'      :130
	},
	{
	'label':'Muster Roll',
	'fieldtype':'Link',
	'fieldname':'muster_roll',
	'width'	   :160,
	'options' :"Muster Roll"
	},
	{
	'label'      :_('No of Person'),
	'fieldtype'  :'Float',
	'fieldname'  :'no_of_person',
	'width'      :130
	},
	{
	'label'      :_('OT Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'ot_hours',
	'width'      :130
	},
	{
	'label'      :_('Total OT Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'total_ot_hours',
	'width'      :130
	},
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		lot.project,
		lot.posting_date,
		ld.muster_roll,
		ld.no_of_person,
		ld.ot_hours,
		ld.total_ot_hours
		FROM
			`tabLabour OT Entry` lot LEFT JOIN 
			`tabOT Labour Detail` ld on ld.parent=lot.name
		WHERE lot.docstatus = 1 and lot.attendance_type="Muster Roll" %s

		ORDER BY
		lot.project,
		lot.posting_date,
		ld.muster_roll
		""" % conditions, filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and lot.project = %(project)s"
	if filters.get("muster_roll"):
		conditions +=" and ld.muster_roll = %(muster_roll)s"
	if filters.get("to_date"):
		conditions +=" and lot.posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and lot.posting_date >= %(from_date)s"
	return conditions
