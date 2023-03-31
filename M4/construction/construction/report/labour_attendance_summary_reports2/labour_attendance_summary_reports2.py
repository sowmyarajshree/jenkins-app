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
    if filters.get('attendance_type') == "Subcontractor":
        return[
                    {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width":250},
                    {"label": "Attendance Type", "fieldname": "attendance_type", "fieldtype": "Data", "width":130},
                    {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width":150},                    
                    {"label": "Subcontractor", "fieldname": "subcontractor", "fieldtype": "Data", "width":150},
                    {"label": "Labourer", "fieldname": "labourer", "fieldtype": "Link", "options": "Labourer", "width":150},
                    {"label": "No of Persons", "fieldname": "qty", "fieldtype": "Float", "width":100},
                    {"label": "Sum of Working Hours", "fieldname": "sum_of_working_hrs", "fieldtype": "Float", "width":150}
                ]
    elif filters.get('attendance_type') == "Muster Roll":
        return[    
                    {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width":250},
                    {"label": "Attendance Type", "fieldname": "attendance_type", "fieldtype": "Data", "width":250},
                    {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width":200},                    
                    {"label": "Muster Roll", "fieldname": "muster_roll", "fieldtype": "Link", "options": "Muster Roll", "width":200},
                    {"label": "Total Working Hours", "fieldname": "total_working_hours", "fieldtype": "Float", "width":200} 
                ] 
    else:          
        return[    
                    {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width":200},
                    {"label": "Attendance Type", "fieldname": "attendance_type", "fieldtype": "Data", "width":130},
                    {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width":100},                    
                    {"label": "Subcontractor", "fieldname": "subcontractor", "fieldtype": "Data", "width":150},
                    {"label": "Labourer", "fieldname": "labourer", "fieldtype": "Link", "options": "Labourer", "width":120},
                    {"label": "No of Persons", "fieldname": "qty", "fieldtype": "Float", "width":100},
                    {"label": "Sum of Working Hours", "fieldname": "sum_of_working_hrs", "fieldtype": "Float", "width":100},
                    {"label": "Muster Roll", "fieldname": "muster_roll", "fieldtype": "Link", "options": "Muster Roll", "width":130},
                    {"label": "Total Working Hours", "fieldname": "total_working_hours", "fieldtype": "Float", "width":130}
	            ]

def get_data(filters):
	conditions=get_conditions(filters)
	return frappe.db.sql("""
        SELECT 
            labour_attendance.project, labour_attendance.attendance_type, labour_attendance.posting_date, labour_attendance.subcontractor,
            labour_details.labourer, labour_details.qty, labour_details.working_hours as hour, labour_details.sum_of_working_hrs,
            muster_roll_detail.muster_roll, muster_roll_detail.working_hours, muster_roll_detail.total_working_hours
        FROM 
            `tabLabour Attendance` labour_attendance
        LEFT JOIN 
            `tabLabour Detail` labour_details ON labour_attendance.name = labour_details.parent
        LEFT JOIN 
            `tabMuster Roll Detail` muster_roll_detail ON labour_attendance.name = muster_roll_detail.parent
        WHERE 
         labour_attendance.docstatus = 1 %s """ % conditions, filters, as_dict=1)

def get_conditions(filters):
    conditions = ""
    if filters.get("project"):
        conditions += "and labour_attendance.project = %(project)s"
    if filters.get("attendance_type"):
        conditions += "and labour_attendance.attendance_type = %(attendance_type)s"
    if filters.get("from_date"):
        conditions += "and labour_attendance.posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += "and labour_attendance.posting_date <= %(to_date)s"
    if filters.get("subcontractor"):
        conditions += "and labour_attendance.subcontractor = %(subcontractor)s"
    if filters.get("muster_roll"):
        conditions += "and muster_roll_detail.muster_roll = %(muster_roll)s" 
                   
    return conditions

