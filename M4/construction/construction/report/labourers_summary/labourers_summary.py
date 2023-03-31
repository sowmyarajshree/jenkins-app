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
	   'label': _('Subcontractor'),
	   'fieldtype': 'Link',
	   'fieldname': 'subcontractor',
	   'width': 200,
	   'options':'Supplier',
	   },
	   {
	   'label': _('Labourer'),
	   'fieldtype': 'Link',
	   'fieldname': 'labourer',
	   'width': 200,
	   'options':'Labourer',
	   },	   
	   {
	   'label': _('Posting Date'),
	   'fieldtype': 'Date',
	   'fieldname': 'posting_date',
	   'width': 200,
	   },
	   {
	   'label': _('No of Person'),
	   'fieldtype': 'Float',
	   'fieldname': 'qty',
	   'width': 200,
	   },
	   {
	   'label': _('Revised Persons'),
	   'fieldtype': 'Float',
	   'fieldname': 'revised_persons',
	   'width': 200,
	   },
	   {
	   'label': _('Sum of Working Hours'),
	   'fieldtype': 'Float',
	   'fieldname': 'sum_of_working_hrs',
	   'width': 200,
	   },
	   {
	   'label': _('OT Hours'),
	   'fieldtype': 'Float',
	   'fieldname': 'ot_hours',
	   'width': 200,
	   },
	   {
	   'label': _('Total Worked Hours'),
	   'fieldtype': 'Float',
	   'fieldname': 'total_worked_hours',
	   'width': 200,
	   },
	   
	   ]


def get_data(filters):
	conditions = get_conditions(filters)
	data =[]
	return frappe.db.sql("""
	SELECT
	    la.subcontractor,
	    la.posting_date,
	    lad.labourer,
	    lad.qty,
	    lad.revised_persons,
	    lad.sum_of_working_hrs,
	    lad.ot_hours,
	    lad.total_worked_hours
	    
	FROM
	    `tabLabour Attendance` la, `tabLabour Details` lad

    WHERE
        lad.parent = la.name and la.docstatus = 1 %s and order by la.subcontractor ASC """ % conditions, filters, as_dict=1)


def get_conditions(filters):
	conditions = ""
	if filters.get("subcontractor"):
		conditions +=" and la.subcontractor = %(subcontractor)s"
	return conditions



