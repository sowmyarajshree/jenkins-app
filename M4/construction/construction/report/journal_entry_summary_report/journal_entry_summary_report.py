import frappe
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
	"options":"Project"
	},
	{
	'label': _('Entry Type'),
	'fieldtype': 'Select',
	'fieldname': 'voucher_type',
	'width': 150,
	"options":["Journal Entry"]
	},
	{
	'label'      :_('Name'),
	'fieldtype'  :'Data',
	'fieldname'  :'name',
	'width'      :150
	},
	{
	'label'      :_('Posting Date'),
	'fieldtype'  :'Date',
	'fieldname'  :'posting_date',
	'width'      :150
	},
	{
	'label'      :_('Credit'),
	'fieldtype'  :'Currency',
	'fieldname'  :'credit_in_account_currency',
	'width'      :150,
	"options": "account_currency"
	},
	{
	'label'      :_('Debit'),
	'fieldtype'  :'Currency',
	'fieldname'  :'debit_in_account_currency',
	'width'      :150,
	"options": "account_currency"
	},
	{
	'label'      :_('Cost Center'),
	'fieldtype'  :'Link',
	'fieldname'  :'cost_center',
	'width'      :150,
	"options": "Cost Center"
	},
	{
	'label'      :_('Account'),
	'fieldtype'  :'Link',
	'fieldname'  :'account',
	'width'      :150,
	"options": "Account"
	}
	
	]

def get_data(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		SELECT
			jea.project,
			je.voucher_type,
			je.name,
			je.posting_date,
			jea.account,
			jea.credit,
			jea.debit,
			jea.cost_center

		FROM
			`tabJournal Entry Account` jea left join
			`tabJournal Entry` je on jea.parent = je.name 

		WHERE
			je.docstatus = 1 %s
		ORDER BY
		jea.project """ % conditions, filters, as_dict=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions +=" and jea.project = %(project)s"
	if filters.get("to_date"):
		conditions +=" and posting_date <= %(to_date)s"
	if filters.get("from_date"):
		conditions +=" and posting_date >= %(from_date)s"
	return conditions

