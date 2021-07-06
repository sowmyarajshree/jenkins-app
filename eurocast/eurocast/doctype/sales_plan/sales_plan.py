 # -*- coding: utf-8 -*-
# Copyright (c) 2020, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import getdate, cstr, add_days, date_diff, getdate, ceil,formatdate, add_months,date_diff,now_datetime
from itertools import count
import datetime
import calendar
from datetime import timedelta
from erpnext.support.doctype.issue.issue import get_holidays
from frappe.model.document import Document

class SalesPlan(Document):
	def on_submit(self):
		self.create_sales_plan_ledger()

	def validate(self):
		self.status = self.get_status()
		self.validate_strt_end_date()

	def before_cancel(self):
		self.cancel_sales_plan_ledger()

#update status based on docstatus
	def get_status(self):
		if self.docstatus == 0:
			status = "Draft"
		elif self.docstatus == 1:
			status = "Submitted"
		elif self.docstatus == 2:
			status = "Cancelled"
		return status

#create sales plan ledger entry
	def create_sales_plan_ledger(self):
		for d in self.sales_plan_detail:
			doc = frappe.new_doc("Sales Plan Ledger Entry")
			doc.update({
						"sales_plan": self.name,
						"item_code": d.item_code,
						"qty": d.frequency_planned_qty,
						"posting_date": d.date,
						"sales_plan_frequency": self.sales_plan_frequency,
						"docstatus": 1,
						"status":"Submitted",
						"customer": self.customer,
						"month": self.month,
						"year": self.year,
						"scheduled_qty": self.per_day_qty,
						"item_name": self.item_name
			})
			doc.save(ignore_permissions=True)

#cancel sales plan ledger on cancel
	def cancel_sales_plan_ledger(self):
		ledger_list = frappe.get_list("Sales Plan Ledger Entry",filters={"sales_plan":self.name},fields=["name"])
		for d in ledger_list:
			doc = frappe.get_doc("Sales Plan Ledger Entry",d.name)
			doc.docstatus = 2
			doc.save(ignore_permissions=True)
			frappe.delete_doc("Sales Plan Ledger Entry",doc.name)

#validate start and end dates based on month and frequency
	def validate_strt_end_date(self):
		if self.sales_plan_frequency == "Daily":
			month_start_date = self.start_date
			month_end_date = self.end_date
			month_s = getdate(month_start_date).month
			month_e = getdate(month_end_date).month
			if self.month == "Jan":
				month = 1
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "Feb":
				month = 2
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "Mar":
				month = 3
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "Apr":
				month = 4
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "May":
				month = 5
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "June":
				month = 6
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "July":
				month = 7
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "Aug":
				month = 8
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "Sep":
				month = 9
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "Oct":
				month = 10
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "Nov":
				month = 11
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")
			if self.month == "Dec":
				month = 12
				if month_s == month and month_e == month:
					pass
				else:
					frappe.throw("Please select dates within given month")

#update items and date as list in child table
@frappe.whitelist()
def update_items(docname,item_code,start_date,end_date,per_day_qty):
	days_list = []
	items = []
	times = date_diff(end_date,start_date) + 1
	for d in range(times):
		if d == 0:
			items.append({
						"item_code": item_code,
						"frequency_planned_qty": per_day_qty,
						"date": start_date
			})
		if d > 0:
			date = add_days(start_date,d)
			items.append({
						"item_code": item_code,
						"frequency_planned_qty": per_day_qty,
						"date": date
			})

	return items



#update items in child table based on the holidays
@frappe.whitelist()
def update_holidays(docname,item_code,start_date,end_date,per_day_qty,holiday_list):
	#holidays = frappe.db.get_list("Holiday",filters={"parent":holiday_list},fields=["holiday_date"])
	month_start_date = getdate(start_date).month
	holidays = frappe.db.sql("""select parent,holiday_date from `tabHoliday` where parent = %(parent)s and month(holiday_date) = %(month)s """,
				{"parent":holiday_list,"month": month_start_date},as_dict=1)
	holiday_list = []
	for h in holidays:
		holiday_date = formatdate(h.holiday_date,"yyyy-MM-dd")
		holiday_list.append(holiday_date)

	days_list = []
	items = []
	times = date_diff(end_date,start_date) + 1

	for d in range(times):
		date = add_days(start_date,d)
		days_list.append(date)

	days_set = set(days_list)
	holidays_set = set(holiday_list)
	list_of_sets = days_set.difference(holidays_set)
	list = sorted(list_of_sets)

	for l in list:
		items.append({
						"item_code": item_code,
						"frequency_planned_qty": per_day_qty,
						"date": l
		})

	return items


#update dates based on month field values
@frappe.whitelist()
def update_dates(docname,month,year):
	now_year = now_datetime().year
	if month == "Jan":
		month_no = 1
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		end_date_n = datetime.date(now_year, int(month_no), days)
		start_date = getdate(start_date_n)
		end_date = getdate(end_date_n)
	if month == "Feb":
		month_no = 2
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "Mar":
		month_no = 3
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "Apr":
		month_no = 4
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "May":
		month_no = 5
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "June":
		month_no = 6
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "July":
		month_no = 7
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "Aug":
		month_no = 8
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "Sep":
		month_no = 9
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "Oct":
		month_no = 10
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "Nov":
		month_no = 11
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)
	if month == "Dec":
		month_no = 12
		days = calendar.monthrange(now_year,month_no)[1]
		start_date_n = datetime.date(now_year, int(month_no), 1)
		start_date = getdate(start_date_n)
		end_date_n = datetime.date(now_year, int(month_no), days)
		end_date = getdate(end_date_n)


	return start_date, end_date
