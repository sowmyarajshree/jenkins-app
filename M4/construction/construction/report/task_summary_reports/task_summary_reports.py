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
	'width'      :180,
	"options":"Project"
	},
	{
	'label': _('Task'),
	'fieldtype': 'Link',
	'fieldname': 'name',
	'width': 180,
	"options":"Task"
	},
	{
	'label'      :_('Project Structure'),
	'fieldtype'  :'Link',
	'fieldname'  :'nx_project_structure',
	'width'      :340,
	"options":"Project Structure"
	},
	{
	'label'      :_('Item of Work'),
	'fieldtype'  :'Link',
	'fieldname'  :'nx_item_of_work',
	'width'      :340,
	"options":"Item of Work"
	},
	{
	'label'      :_('Status'),
	'fieldtype'  :'Select',
	'fieldname'  :'progress_status',
	'width'      :130,
	"options":["Open","In Progress"]
	}
	
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		t.project ,
		t.nx_project_structure,
		t.nx_item_of_work,
		t.qty,
		t.actual_qty,
		t.balance_qty,
		t.progress_status,
		t.name

		FROM
		`tabTask` t

		WHERE 
		t.docstatus = 0 %s 
		ORDER BY
		t.project """ % conditions, filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and t.project = %(project)s"
	if filters.get("nx_project_structure"):
		conditions +=" and t.nx_project_structure = %(nx_project_structure)s"
	if filters.get("nx_item_of_work"):
		conditions +=" and t.nx_item_of_work = %(nx_item_of_work)s"
	if filters.get("progress_status"):
		conditions +=" and t.progress_status = %(progress_status)s"


	return conditions
