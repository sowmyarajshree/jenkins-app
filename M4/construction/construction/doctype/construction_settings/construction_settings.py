# -*- coding: utf-8 -*-
# Copyright (c) 2021, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from datetime import timedelta
import pandas as pd

class ConstructionSettings(Document):
	pass




@frappe.whitelist()
#auto creation of accounting period based on weekly,month and yearly  
def make_acc_date(start,end,open_day,period):
	if period == "Weekly":
		week_name='W'+'-'+open_day[0:3]
		period_range=pd.date_range(start,end,freq=week_name)
		for i in period_range:
			# if i.date().strftime("%A")==open_day:
				generate_date=frappe.new_doc("Accounting Period")
				generate_date.update({
					"start_date":i, # start date 
					"end_date":i+timedelta(days=6), # (start date + after 6 days)
					"period_name":(i+timedelta(days=6)).strftime("%U-Week %Y"),  # (start date + after 6 days) by end_date get the week name
					"company":"Sri Sasthaa Constructions"
					})
				doc_type=['Payroll Entry','Sales Invoice','Purchase Invoice','Journal Entry','Bank clearance','Asset','Stock Entry','Payment Entry']
				for i in doc_type:
					generate_date.append('closed_documents',{
						"document_type":i,
						"closed":0
						})
					generate_date.save(ignore_permissions=True)
		frappe.msgprint(_("Accounting Period created"))
	if period == "Monthly":
		acc_period_date=pd.date_range(start,end,freq='MS')
		for i in acc_period_date:
				ed_date=i+timedelta(days=32) 
				generate_date=frappe.new_doc("Accounting Period")
				generate_date.update({
					"start_date":i,
					"end_date":ed_date.replace(day=1) - timedelta(days=1),
					"period_name":(ed_date.replace(day=1) - timedelta(days=1)).strftime("%B-%Y"),
					"company":"Sri Sasthaa Constructions"
					})
				doc_type=['Payroll Entry','Sales Invoice','Purchase Invoice','Journal Entry','Bank Clearance','Asset','Stock Entry','Payment Entry']
				for i in doc_type:
					generate_date.append('closed_documents',{
						"document_type":i,
						"closed":0
						})
					generate_date.save(ignore_permissions=True)
		frappe.msgprint(_("Accounting Period created"))





