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
	'width'      :100,
	"options":"Project"
	},
	{
	'label': _('Status'),
	'fieldtype': 'Select',
	'fieldname': 'status',
	'width': 80,
	"options":["Open","Not Started","In Progress","Completed"]
	},
	{
	'label'      :_('Subcontractor'),
	'fieldtype'  :'Link',
	'fieldname'  :'subcontractor',
	'width'      :100,
	'options' : 'Supplier'
	},
	{
	'label'      :_('Posting Date'),
	'fieldtype'  :'Date',
	'fieldname'  :'posting_date',
	'width'      :100
	},
	{
	'label'      :_('Labourer'),
	'fieldtype'  :'Link',
	'fieldname'  :'labourer',
	'width'      :100,
	"options": "Labourer"
	},
	{
	'label'      :_('No of Person'),
	'fieldtype'  :'Int',
	'fieldname'  :'qty',
	'width'      :70
	},
	{
	'label'      :_('Working Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'working_hours',
	'width'      :70
	},
	{
	'label'      :_('OT Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'ot_hours',
	'width'      :70
	},
	{
	'label'      :_('Revised Out Person'),
	'fieldtype'  :'Float',
	'fieldname'  :'revised_out_person',
	'width'      :70
	},
	{
	'label'      :_('Revised in Person'),
	'fieldtype'  :'Float',
	'fieldname'  :'revised_in_person',
	'width'      :70
	},
	{
	'label'      :_('Revised In Time'),
	'fieldtype'  :'Float',
	'fieldname'  :'revised_in_time',
	'width'      :70
	},
	{
	'label'      :_('Revised Out Time'),
	'fieldtype'  :'Float',
	'fieldname'  :'revised_out_time',
	'width'      :70
	},
	{
	'label'      :_('Sum of Working Hrs'),
	'fieldtype'  :'Float',
	'fieldname'  :'sum_of_working_hrs',
	'width'      :70
	},
	{
	'label'      :_('Total F And F Hrs'),
	'fieldtype'  :'Float',
	'fieldname'  :'f_and_f_hrs',
	'width'      :70
	},
	{
	'label'      :_('Total Rate Work Hrs'),
	'fieldtype'  :'Float',
	'fieldname'  :'rate_work_hrs',
	'width'      :70
	},
	{
	'label'      :_('Worked Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'total_worked_hours',
	'width'      :70
	},
	{
	'label'      :_('Balance Hours'),
	'fieldtype'  :'Float',
	'fieldname'  :'balance_hrs',
	'width'      :70
	}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
		la.project,
		la.status,
		la.subcontractor,
		la.posting_date,
		ld.labourer,
		ld.qty,
		ld.working_hours,
		ld.ot_hours,
		ld.revised_in_time,
		ld.revised_out_time,
		ld.sum_of_working_hrs,
		ld.f_and_f_hrs,
		ld.rate_work_hrs,
		ld.total_worked_hours,
		ld.balance_hrs
		
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

