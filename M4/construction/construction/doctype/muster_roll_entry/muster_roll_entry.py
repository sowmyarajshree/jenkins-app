# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
import re
from frappe import _
from frappe.model.document import Document
from datetime import date
from dateutil import parser
from datetime import datetime
from frappe.utils import (
    DATE_FORMAT,
    add_days,
    add_to_date,
    cint,
    comma_and,
    date_diff,
    flt,
    getdate,
)
    

class MusterRollEntry(Document):
	def before_insert(self):
		self.lpe_validation()
		self.duplicate_validate_doc0()
		#self.validate_muster_roll_duplicate()
		
	def validate(self):
		self.lpe_validation()
		self.update_status()
		self.get_percentage_from_hours()
		self.total_hour_calculations()
		self.amt_calculation()
		self.tds_for_muster_roll()
		self.rounding_total_for_muster_roll()
		self.lpe_child_amount_update()
		self.validate_posting_date()
		self.calculate_work_efficiency()
		self.duplicate_validate_doc1()
		

	def before_submit(self):
		self.update_labour_rate()
		self.update_labour_rate_in_lpe()
		self.lpe_status_update()

	def before_cancel(self):
		self.update_labour_rate_on_cancel()
		self.update_labour_rate_in_lpe_on_cancel()
		self.update_status_on_cancel()
		

	def update_status(self):
		if self.docstatus == 0:
			self.status = "Draft"
		if self.docstatus == 1:
			self.status = "To Bill"

	# def validate_muster_roll_duplicate(self):
	# 	if(frappe.db.exists("Muster Roll Entry",{"accounting_period":self.accounting_period,"docstatus":0,"project":self.project,"muster_roll":self.muster_roll},["name"])):
	# 		frappe.throw(("This Muster Roll Entry Already Entered"))
	# 	elif(frappe.db.exists("Muster Roll Entry",{"accounting_period":self.accounting_period,"docstatus":1,"project":self.project,"muster_roll":self.muster_roll},["name"])):
	# 		frappe.throw(("This Muster Roll Entry Already Entered"))

	def duplicate_validate_doc1(self):
		if(self.labour_type =='Muster Roll'):
			existing_doc=frappe.get_list("Muster Roll Entry",filters={"accounting_period":self.accounting_period,"docstatus":1,"project":self.project,"muster_roll":self.muster_roll})
			if(existing_doc):
				frappe.throw("This Muster Roll Entry Already Entered")
	def duplicate_validate_doc0(self):
		if(self.labour_type =='Muster Roll'):
			existing_doc=frappe.get_list("Muster Roll Entry",filters={"accounting_period":self.accounting_period,"docstatus":0,"project":self.project,"muster_roll":self.muster_roll})
			if(existing_doc):
				frappe.throw("This Muster Roll Entry Already Entered")

	def tds_for_muster_roll(self):
		if self.tax_percentage >= 1:
			self.tax_amount = self.total_amount * (self.tax_percentage/100)
			self.grand_total = self.total_amount - self.tax_amount
		else:
			self.grand_total = self.total_amount
	def rounding_total_for_muster_roll(self):
		if self.rounding_adjustment == 0:
			self.rounded_total = self.grand_total
		elif self.rounding_adjustment != 0:
			self.rounded_total = self.grand_total + self.rounding_adjustment
	
    #child table amount calculate for total_amount
	def amt_calculation(self):
		self.total_amount=0
		for i in self.f_and_f_details_update:
			self.total_amount+=i.amount

	
	def update_status_on_cancel(self):
		if self.docstatus == 2:
			self.status = "Cancelled"
			for l in self.labour_progress_details:
				frappe.set_value("Labour Progress Entry",l.labour_progress_entry,"status","To Prepared and Bill")
				frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_doctype",None)
				frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_name",None)


	def lpe_status_update(self):
		for l in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
			labour_bill_rate = []
			for w in lpe_doc.working_details:
				if w.labour_bill_rate != 0:
					labour_bill_rate.append(w.idx)
			if len(lpe_doc.working_details) == len(labour_bill_rate):
				frappe.db.set_value("Labour Progress Entry",lpe_doc.name,"status","To Bill")

	def lpe_validation(self):
		for l in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
			if (lpe_doc.labour_type != self.labour_type) and (lpe_doc.status != "To Prepared and Bill"):
				frappe.throw(_("Labour Progress Entry chose is not applicable in row {0}").format(l.idx))

    #update labour rate
	def update_labour_rate(self):
		for l in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",{"name":l.labour_progress_entry},["name"])
			boq_ledg_value = frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["name"])
			boq_ledg_doc = frappe.get_doc("BOQ Ledger",boq_ledg_value)
			frappe.set_value("BOQ Ledger",boq_ledg_doc.name,"actual_amount",frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"]) + l.amount)
			if boq_ledg_doc.actual_qty != 0:
				frappe.set_value("BOQ Ledger",boq_ledg_doc.name,"actual_rate",(frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"])/boq_ledg_doc.actual_qty))

    #update labour rate on cancel
	def update_labour_rate_on_cancel(self):
		for l in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",{"name":l.labour_progress_entry},["name"])
			boq_ledg_value = frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["name"])
			boq_ledg_doc = frappe.get_doc("BOQ Ledger",boq_ledg_value)
			frappe.set_value("BOQ Ledger",boq_ledg_doc.name,"actual_amount",frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"]) - l.amount)
			if boq_ledg_doc.actual_qty != 0:
				frappe.set_value("BOQ Ledger",boq_ledg_doc.name,"actual_rate",(frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"])/boq_ledg_doc.actual_qty))

#percentage calculation from lpe total hours
	def get_percentage_from_hours(self):
		for i in self.labour_progress_details:			
			lpe_total_hrs = frappe.db.sql(''' SELECT sum(lpe_total_hours) as tot_hours_lpe 
				                              FROM `tabLabour Progress Entry` 
				                              WHERE posting_date = %s and 
				                              status = "To Prepared and Bill" and 
				                              docstatus = 1 and labour_type = "Muster Roll" and project_name = %s
				                              group by posting_date ''',(i.dates,self.project),as_dict=1)
			for j in lpe_total_hrs:
				i.percentage = (i.total_hrs/j.tot_hours_lpe) * 100
				for l in self.f_and_f_details_update:
					if i.dates == l.date:
						i.amount = (i.percentage * l.amount) / 100 

	def calculate_work_efficiency(self):
		self.work_efficiency = round((self.total_lpe_hours / self.total_hours)*100)

	def total_hour_calculations(self):
		for i in self.f_and_f_details_update:
			i.total_hours = frappe.get_value("Labour Attendance",{"name":i.labour_attendance},["total_worked_hrs"])
			i.ffd_mrd_date = frappe.get_value("Labour Attendance",{"name":i.labour_attendance},["posting_date"])

	def validate_posting_date(self):
		for i in self.labour_progress_details:
			lab_dates=datetime.strptime(i.dates,"%Y-%m-%d")
			post_date=datetime.strptime(self.posting_date,"%Y-%m-%d")
			if post_date < lab_dates:
				frappe.throw("You Given Posting date not match in Labour progress entry dates")
		

	# amount edit
	def lpe_child_amount_update(self):
		for l in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
			for w in lpe_doc.working_details:
				if self.muster_roll == w.muster_roll:
					l.total_hrs = w.total_working_hours
					wages = frappe.get_value("Muster Roll",{"name":self.muster_roll},["wages"])
					per_hour_wages = wages/8
					l.amount = per_hour_wages * l.total_hrs


	def update_labour_rate_in_lpe(self):
		for i in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",i.labour_progress_entry)
			for w in lpe_doc.working_details:			
				if w.muster_roll == self.muster_roll:
					frappe.db.set_value("Working Detail",w.name,"labour_bill_rate",i.amount)									
					labour_bill_rate = frappe.get_value("Labour Progress Entry",{"name":lpe_doc.name},["labour_rate"])
					frappe.db.set_value("Labour Progress Entry",lpe_doc.name,"labour_rate",(labour_bill_rate + i.amount))

	def update_labour_rate_in_lpe_on_cancel(self):
		labour_bill_rate = 0
		for i in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",i.labour_progress_entry)
			labour_bill_rate += i.amount
			for w in lpe_doc.working_details:
				if w.muster_roll == self.muster_roll:
					frappe.db.set_value("Working Detail",w.name,"labour_bill_rate",0)
					labour_bill_rate = frappe.get_value("Labour Progress Entry",{"name":lpe_doc.name},["labour_rate"])
					frappe.db.set_value("Labour Progress Entry",lpe_doc.name,"labour_rate",(labour_bill_rate - i.amount))

@frappe.whitelist()
def create_journal_entry(docname):
	muster_doc = frappe.get_doc("Muster Roll Entry",docname)
	journal_doc = frappe.new_doc("Journal Entry")
	journal_doc.append("accounts",{
		"account":"Cash - SSC",
		"credit_in_account_currency":muster_doc.rounded_total,
		"nx_muster_roll_entry":docname,
		"project":muster_doc.project
		})
	journal_doc.append("accounts",{
		"account":"TDS Account - SSC",
		"credit_in_account_currency":muster_doc.tax_amount,
		"nx_muster_roll_entry":docname,
		"project":muster_doc.project
		})
	journal_doc.append("accounts",{
		"account":"NMR Wages - SSC",
		"debit_in_account_currency":muster_doc.rounded_total+muster_doc.tax_amount,
		"nx_muster_roll_entry":docname,
		"project":muster_doc.project
		})
	return journal_doc

@frappe.whitelist()
def get_labour_attendance(dates,muster_roll,project):
    attendance = []
    att_list = list(set(frappe.db.get_list('Labour Attendance',{'posting_date': ['in', eval(dates)] ,"attendance_type":"Muster Roll","project":project,"docstatus": 1} ,['name'],as_list =1)))
    att_list = re.sub('[(),]','',str(att_list)).replace(' ',',')
    for d in eval(att_list):
        lab_att_doc = frappe.get_doc("Labour Attendance",d)
        cons_sett_doc = frappe.get_doc("Construction Settings")
        for i in lab_att_doc.muster_roll_detail:
        	if muster_roll == i.muster_roll:
	        	per_hour_wages = i.wages/cons_sett_doc.hours
		        attendance.append({
		            "date":lab_att_doc.posting_date,
		    		"labour_attendance":lab_att_doc.name,
		    		"total_person":"1",
		    		"rate":per_hour_wages,
		    		"hours_worked":i.total_worked_hours,
		    		"amount":(per_hour_wages * i.total_working_hours)
		        })
    return attendance




