# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
import re
import pandas as pd
import pyttsx3
from frappe import _
from frappe.model.document import Document
from datetime import date
from datetime import datetime
from dateutil import parser
import gtts
import playsound
from construction.construction.journal_entry import handle_validation_error
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

class FandFEntry(Document):
	def validate(self):
		self.update_status()
		self.calculate_work_efficiency()
		self.validate_f_and_f_entry_datas()
		self.f_and_f_total_amount()
		self.labour_progres_entry_missing_validation()
		self.lpe_child_amount_update()
		self.lpe_validation()
		self.rate_amt_validation()
		self.validate_posting_date()

	def before_submit(self):
		self.lpe_status_update()
		self.update_labour_rate_in_boq_ledger()
		self.update_labour_rate_in_lpe()

	def before_cancel(self):
		self.update_labour_rate_in_boq_ledger_on_cancel()
		self.update_status_on_cancel()
		self.update_labour_rate_in_lpe_on_cancel()

	def before_insert(self):
		self.lpe_validation()


	def update_tot_amt_to_item_price(self):
		fandf_item=frappe.get_value("Construction Settings","construction_settings",'f_and_f_item')
		item_name=frappe.get_value("Item Price",{"item_code":fandf_item},["name"])
		frappe.set_value("Item Price",item_name,"price_list_rate",self.total_amount)

	#rate and amt can't be zero
	def rate_amt_validation(self):
		for i in self.items:
			if(i.rate==0 or i.amount==0):
				#engine = pyttsx3.init()
				#engine.say("hi M4")
				#engine.runAndWait()

				frappe.msgprint("Rate and Amount Can't be Zero")
				#voice_in = "Rate and Amount Can't be Zero"
				#conv_voice_in = gtts.gTTS(voice_in,lang="en")
				#conv_voice_in.save("m4voice.mp3")
				#playsound.playsound("m4voice")
				
				

	#status update
	def update_status(self):
		self.total_hours_lpe = 0
		for i in self.labour_progress_details:
			self.total_hours_lpe += i.total_hrs
		if self.docstatus == 0:
			self.status = "Draft"
		if self.docstatus == 1:
			self.status = "To Bill"

	#labour progress entry name, status update
	def lpe_status_update(self):
		for l in self.labour_progress_details:
			frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"status","To Bill")
			frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_doctype","F and F Entry")
			frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_name",self.name)

	#labour progress entry name, status on cancel
	def update_status_on_cancel(self):
		if self.docstatus == 2:
			self.status = "Cancelled"
			for l in self.labour_progress_details:
				frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"status","To Prepared and Bill")
				frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_doctype",None)
				frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_name",None)

	#labour progress validation
	def lpe_validation(self):
		for l in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
			if ((lpe_doc.status == "To Bill") or (lpe_doc.status == "Completed") or (lpe_doc.labour_type != self.labour_type)):
				frappe.throw(_("Labour Progress Entry chose is not applicable in row {0}").format(l.idx))

	def validate_posting_date(self):
		for i in self.labour_progress_details:
			lab_dates=datetime.strptime(i.dates,"%Y-%m-%d")
			post_date=datetime.strptime(self.posting_date,"%Y-%m-%d")
			if post_date < lab_dates:
				frappe.throw("You Given Posting date not match in Labour progress entry dates")


	#labour attendance status update
	def f_and_f_total_amount(self):
		self.total_amount = 0
		self.total_hours = 0
		for i in self.items:
			self.total_amount += i.amount
			self.total_hours += i.hours_worked
			i.date = frappe.get_value("Labour Attendance",{"name":i.labour_attendance},["posting_date"])

	def lpe_child_amount_update(self)  :
		for i in self.items:
			if i.is_machine == 0:
				per_hour = 0
				for l in self.labour_progress_details:
					if (getdate(i.date) == getdate(l.dates)) and (i.labourer == l.labourer):
						per_hour = i.rate/8
						l.amount = l.total_hrs * per_hour
			else:
				per_hour = 0
				for l in self.labour_progress_details:
					if (getdate(i.date) == getdate(l.dates)) and (i.labourer == l.labourer):
						per_hour = i.rate
						l.amount = l.total_hrs * per_hour


	def validate_f_and_f_entry_datas(self):
		for l in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
			if (lpe_doc.subcontractor != self.subcontractor and lpe_doc.project != self.project):
				frappe.throw(_("Subcontractor or Project is not relatable in Labour Progress Entry"))


	def update_labour_rate_in_lpe(self):
		for i in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",i.labour_progress_entry)
			for w in lpe_doc.working_details:
				if w.labourer == i.labourer:
					frappe.db.set_value("Working Detail",w.name,"labour_bill_rate",i.amount)
					labour_bill_rate = frappe.get_value("Labour Progress Entry",{"name":lpe_doc.name},["labour_rate"])
					frappe.db.set_value("Labour Progress Entry",lpe_doc.name,"labour_rate",(labour_bill_rate + i.amount))

	def update_labour_rate_in_lpe_on_cancel(self):
		for i in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",i.labour_progress_entry)
			for w in lpe_doc.working_details:
				frappe.db.set_value("Working Detail",w.name,"labour_bill_rate",0)
			frappe.db.set_value("Labour Progress Entry",lpe_doc.name,"labour_rate",0)
	
	#update labour rate
	def update_labour_rate_in_boq_ledger(self):
		for l in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",{"name":l.labour_progress_entry},["name"])
			boq_ledg_value = frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["name"])
			boq_ledg_doc = frappe.get_doc("BOQ Ledger",boq_ledg_value)
			frappe.set_value("BOQ Ledger",boq_ledg_doc.name,"actual_amount",frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"]) + l.amount)
			frappe.set_value("BOQ Ledger",boq_ledg_doc.name,"actual_rate",(frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"])/boq_ledg_doc.actual_qty))

	#update labour rate on cancel
	def update_labour_rate_in_boq_ledger_on_cancel(self):
		for l in self.labour_progress_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",{"name":l.labour_progress_entry},["name"])
			boq_ledg_value = frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["name"])
			boq_ledg_doc = frappe.get_doc("BOQ Ledger",boq_ledg_value)
			frappe.set_value("BOQ Ledger",boq_ledg_doc.name,"actual_amount",frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"]) - l.amount)
			frappe.set_value("BOQ Ledger",boq_ledg_doc.name,"actual_rate",(frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"])/boq_ledg_doc.actual_qty))

	def labour_progres_entry_missing_validation(self):
		tot_lpe = []
		for i in self.labour_progress_details:
			lpe_count = frappe.get_list("Working Detail",{"parent":i.labour_progress_entry},["name"],ignore_permissions = True)
			for j in lpe_count:
				if j.name not in tot_lpe:
					tot_lpe.append(j.name)

		lpe_details = []
		for l in self.labour_progress_details:
			if l.working_details_name not in lpe_details:
				lpe_details.append(l.working_details_name)
		entry_diff = frozenset(tot_lpe).symmetric_difference(frozenset(lpe_details))

		if entry_diff:
			frappe.throw(_("In the list one the Labour Progress Entry is Missing"))

	
	def calculate_work_efficiency(self):
		self.work_efficiency = round((self.total_hours_lpe / self.total_hours)*100)


@frappe.whitelist()
def fetch_labour_work_order_price(labourer,lwo):
	lwo_rate = frappe.get_value("Labourer Rate Detail",{"parent":lwo,"labour_item":labourer},["rate"])
	return lwo_rate

@frappe.whitelist()
def create_purchase_invoice(docname):
	fandf_doc = frappe.get_doc("F and F Entry",docname)
	pur_inv_doc = frappe.new_doc("Purchase Invoice")
	cons_sett_doc = frappe.get_doc("Construction Settings")
	stock_uom = frappe.get_value("Item",{"name":cons_sett_doc.f_and_f_item},["stock_uom"])
	customer = frappe.get_value("Project",{"name":fandf_doc.project},["customer"])
	pur_inv_doc.update({
		"supplier":fandf_doc.subcontractor,	
		"project_name":fandf_doc.project,
		"project":fandf_doc.project,
		"supplier_warehouse":cons_sett_doc.warehouse,
		"customer":customer,
		"naming_series":"PINV-FFB-.#####"
		})

	pur_inv_doc.append("items",{
			"item_code":cons_sett_doc.f_and_f_item,
			"item_name":fandf_doc.project +"-"+ fandf_doc.name,
			"nx_reference_name":fandf_doc.name,
			"nx_reference_doctype": fandf_doc.doctype,
			"uom":stock_uom,
			"qty":1,
			"rate":fandf_doc.total_amount,
			"amount":fandf_doc.total_amount,
			"labour_type":"F and F"
		})
	pur_inv_doc.save(ignore_permissions=True)
	return pur_inv_doc

@frappe.whitelist()
def get_labour_attendance(lab_att,project,labour_type,posting_date,subcontractor):
	attendance = []

	att_list = list(set(frappe.db.get_list('Labour Attendance',{'posting_date': ['in', eval(lab_att)] ,"subcontractor":subcontractor,"project":project,"docstatus":1} ,['name'],as_list =1)))

	att_list = re.sub('[(),]','',str(att_list)).replace(' ',',')
	for d in eval(att_list):
		lab_att_doc = frappe.get_doc("Labour Attendance",d)
		for i in lab_att_doc.labour_details:
			if i.f_and_f_hrs != 0:
				attendance.append({
						"date":lab_att_doc.posting_date,
			    		"labour_attendance":lab_att_doc.name,
			    		"total_person":i.qty,
			    		"hours_worked":i.f_and_f_hrs,
			    		"labourer":i.labourer
			    		
	    	})    	
	return attendance

@frappe.whitelist()
def update_lwo_rate(labourer,date,labour_work_order):
	lwo_value = frappe.get_value("Labour Work Order",{"name":labour_work_order,"from_date":["<=",date],"to_date":[">=",date],"status":"Active"},["name"])
	lwo_rate = frappe.get_value("Labourer Rate Detail",{"parent":lwo_value,"labour_item":labourer},["rate"])
	if lwo_rate:
		return lwo_rate
	else:
		frappe.throw(_("Rate for this Labourer in this date is Available"))






