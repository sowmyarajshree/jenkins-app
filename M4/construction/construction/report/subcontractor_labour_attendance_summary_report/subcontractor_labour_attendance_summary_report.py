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
	'label'      :_('Subcontractor'),
	'fieldtype'  :'Link',
	'fieldname'  :'subcontractor',
	'width'      :180,
	'options' : 'Supplier'
	},
	{
	'label'      :_('Posting Date'),
	'fieldtype'  :'Date',
	'fieldname'  :'posting_date',
	'width'      :170
	},
	{
	'label'      :_('No of Person'),
	'fieldtype'  :'Int',
	'fieldname'  :'qty',
	'width'      :160
	},
	{
	'label'      :_('Working Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'working_hours',
	'width'      :160
	},
	{
	'label'      :_('OT Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'ot_hours',
	'width'      :160
	},
	{
	'label'      :_('Worked Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'total_worked_hours',
	'width'      :160
	}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		la.project,
		la.subcontractor,
		la.posting_date,
		ld.qty,
		ld.working_hours,
		ld.ot_hours,
		ld.sum_of_working_hrs,
		ld.total_worked_hours
		
		FROM
			`tabLabour Detail` ld LEFT JOIN `tabLabour Attendance` la on ld.parent = la.name 
		WHERE la.docstatus = 1 %s
		
		ORDER BY
		la.project """ % conditions, filters, as_dict=1)

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
	if filters.get("subcontractor"):
		conditions +=" and la.subcontractor = %(subcontractor)s"
	return conditions

