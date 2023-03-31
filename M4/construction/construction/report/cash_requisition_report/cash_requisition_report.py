# # Copyright (c) 2023, Nxweb and contributors
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
            "label": "Project",
            "fieldname": "project",
            "fieldtype": "Link",
            "options": "Project",
            "width":250
            
        },
        {
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width":250

            
        },
        {
            "label": "Request Date",
            "fieldname": "request_date",
            "fieldtype": "Date",
            "width":200

        },
        {
            "label": "Accounting Period",
            "fieldname": "accounting_period",
            "fieldtype": "Link",
            "options": "Accounting Period",
            "width":250
        },    
        {
            "label": "Workflow State",
            "fieldname": "workflow_state",
            "fieldtype": "Link",
            "options": "Workflow State",
            "width":200
        }            
            ]

def get_data(filters):
    conditions=get_conditions(filters)
    return frappe.db.sql("""
        SELECT 
            cash_requisition.project, cash_requisition.company, cash_requisition.request_date, cash_requisition.accounting_period, cash_requisition.workflow_state
        FROM 
            `tabCash Requisition Entry` cash_requisition
        WHERE 
        cash_requisition.docstatus != 2 %s 
        ORDER BY
         cash_requisition.project """ % conditions, filters, as_dict=1) 


def get_conditions(filters):
    conditions = ""
    if filters.get("project"):
        conditions += "and cash_requisition.project = %(project)s"
    if filters.get("company"):
        conditions += "and cash_requisition.company = %(company)s"
    if filters.get("from_date"):
        conditions += "and cash_requisition.request_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += "and cash_requisition.request_date <= %(to_date)s"    
    if filters.get("accounting_period"):
        conditions += "and cash_requisition.accounting_period = %(accounting_period)s"    
    if filters.get("workflow_state"):
        conditions += "and cash_requisition.workflow_state = %(workflow_state)s"            
    return conditions
