# Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from datetime import date
from datetime import datetime

class RateWorkEntry(Document):
	def before_insert(self):
		self.lpe_validation()

	def validate(self):
		self.update_status()
		self.rate_work_calculation()
		self.rate_amt_validation()
		self.lwo_validation()
		self.lpe_validation()
		self.validate_posting_date()
		
	
	def before_submit(self):
		self.lpe_status_update()
		self.labour_rate_update()
		
	def before_cancel(self):
		self.lpe_status_on_cancel()
		self.labour_rate_update_on_cancel()

	
	#update total amount to item price
	def update_tot_amt_to_item_price(self):
		rate_wk_item=frappe.get_value("Construction Settings","construction_settings","rate_work_item")
		item_name=frappe.get_value("Item Price",{"item_code":rate_wk_item},["name"])
		frappe.set_value("Item Price",item_name,"price_list_rate",self.total_amount)

    #Rate and Amt Can't be zero		
	def rate_amt_validation(self):
		for i in self.labour_progress_work_details:
			if i.rate==0 or i.amount==0:
				frappe.throw("Rate and Amount can't be Zero")

	def validate_posting_date(self):
		for i in self.labour_progress_work_details:
			lab_dates=datetime.strptime(str(i.dates),"%Y-%m-%d")
			post_date=datetime.strptime(self.posting_date,"%Y-%m-%d")
			if post_date < lab_dates:
				frappe.throw("You Given Posting Date not matched in Labour Progress Entry Date Field")
		

    # fixed calculation in rate work 
	def rate_work_calculation(self):
		if self.has_lwo == "Yes":
			self.total_amount=0
			lwo_doc = frappe.get_doc("Labour Work Order",self.labour_work_order)	
			for i in self.labour_progress_work_details:
				for l in lwo_doc.labour_rate_details:
					if l.labour_item == i.labour_work:
						i.rate = l.rate
						i.amount=i.qty * i.rate
						self.total_amount += i.amount
		else:
			self.total_amount=0
			for i in self.labour_progress_work_details:
				i.amount=i.qty * i.rate
				self.total_amount += i.amount
		if self.total_amount == 0:
			frappe.throw(_("Total Amount Cannot be Zero"))


	def update_status(self):
		if self.docstatus == 0:
			self.status = "Draft"
		if self.docstatus == 1:
			self.status = "To Bill"

	def lwo_validation(self):
		if self.has_lwo == "Yes":
			labour_type = frappe.get_value("Labour Work Order",{"name":self.labour_work_order},["labour_type"])
			if self.labour_type != labour_type:
				frappe.throw(_("Labour Work Order {0} Not Belongs to Rate Work".format(self.labour_work_order)))

	def lpe_status_update(self):
		for l in self.labour_progress_work_details:
			frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"status","To Bill")
			frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_doctype","Rate Work Entry")
			frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_name",self.name)

	def lpe_status_on_cancel(self):
		if self.docstatus == 2:
				self.status = "Cancelled"
		for l in self.labour_progress_work_details:
			frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"status","To Prepared and Bill")
			frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_doctype",None)
			frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"reference_name",None)

	def lpe_validation(self):
		for l in self.labour_progress_work_details:
			lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
			if (lpe_doc.status == "To Bill") or (lpe_doc.status == "Completed") or (lpe_doc.labour_type != self.labour_type):
				frappe.throw(_("Labour Progress Entry chose is not applicable in row {0}").format(l.idx))

	def labour_rate_update(self):
		if self.has_lwo == "Yes":
			for l in self.labour_progress_work_details:
				lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
				frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"labour_rate",((frappe.get_value("Labour Progress Entry",{"name":l.labour_progress_entry},["labour_rate"])) + lpe_doc.total_qty * l.rate))
				ledg_name = frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["name"])
				ledg_doc = frappe.get_doc("BOQ Ledger",ledg_name)		
				frappe.db.set_value("BOQ Ledger",ledg_doc.name,"actual_amount",frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"]) + (lpe_doc.total_qty * l.rate))
				frappe.set_value("BOQ Ledger",ledg_doc.name,"actual_rate",(frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"])/ledg_doc.actual_qty))
		if self.has_lwo == "No":
			for l in self.labour_progress_work_details:
				lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
				frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"labour_rate",((frappe.get_value("Labour Progress Entry",{"name":l.labour_progress_entry},["labour_rate"])) + lpe_doc.total_qty * l.rate))
				ledg_name = frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["name"])
				ledg_doc = frappe.get_doc("BOQ Ledger",ledg_name)		
				frappe.db.set_value("BOQ Ledger",ledg_doc.name,"actual_amount",frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"]) + (lpe_doc.total_qty * l.rate))
				frappe.set_value("BOQ Ledger",ledg_doc.name,"actual_rate",(frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"])/ledg_doc.actual_qty))
		
	def labour_rate_update_on_cancel(self):
		if self.has_lwo == "Yes":
			for l in self.labour_progress_work_details:
				lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
				frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"labour_rate",((frappe.get_value("Labour Progress Entry",{"name":l.labour_progress_entry},["labour_rate"])) - lpe_doc.total_qty * l.rate))
				ledg_name = frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["name"])
				ledg_doc = frappe.get_doc("BOQ Ledger",ledg_name)		
				frappe.db.set_value("BOQ Ledger",ledg_doc.name,"actual_amount",frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"]) - (lpe_doc.total_qty * l.rate))
				frappe.set_value("BOQ Ledger",ledg_doc.name,"actual_rate",(frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"])/ledg_doc.actual_qty))
		if self.has_lwo == "No":
			for l in self.labour_progress_work_details:
				lpe_doc = frappe.get_doc("Labour Progress Entry",l.labour_progress_entry)
				frappe.db.set_value("Labour Progress Entry",l.labour_progress_entry,"labour_rate",((frappe.get_value("Labour Progress Entry",{"name":l.labour_progress_entry},["labour_rate"])) - lpe_doc.total_qty * l.rate))
				ledg_name = frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["name"])
				ledg_doc = frappe.get_doc("BOQ Ledger",ledg_name)		
				frappe.db.set_value("BOQ Ledger",ledg_doc.name,"actual_amount",frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"]) - (lpe_doc.total_qty * l.rate))
				frappe.set_value("BOQ Ledger",ledg_doc.name,"actual_rate",(frappe.get_value("BOQ Ledger",{"boq":lpe_doc.boq,"labour":lpe_doc.labour},["actual_amount"])/ledg_doc.actual_qty))

@frappe.whitelist()
def create_purchase_invoice(docname):
	 rate_work_doc = frappe.get_doc("Rate Work Entry",docname)
	 pur_inv_doc = frappe.new_doc("Purchase Invoice")
	 cons_sett_doc = frappe.get_doc("Construction Settings")
	 stock_uom = frappe.get_value("Item",{"name":cons_sett_doc.rate_work_item},["stock_uom"])
	 pur_inv_doc.update({
	 	    "supplier":rate_work_doc.subcontractor,	 	    
	 	    "project_name":rate_work_doc.project,
	 	    "project":rate_work_doc.project,
	 	    "supplier_warehouse":cons_sett_doc.warehouse,
	 	    "naming_series": "PINV-RWB-.#####"
	 })
	 pur_inv_doc.append("items",{
	 		"item_code":cons_sett_doc.rate_work_item,
	 		"item_name":rate_work_doc.name,
	 		"nx_reference_name":rate_work_doc.name,
	 		"nx_reference_doctype": rate_work_doc.doctype,	
	 		"uom":stock_uom,
	 		"qty":1,
	 		"rate":rate_work_doc.total_amount,
	 		"amount":rate_work_doc.total_amount,
	 		"labour_type":"Rate Work"
	 	})
	 pur_inv_doc.save(ignore_permissions=True)
	 return pur_inv_doc

@frappe.whitelist()
def get_lwo_rate(lwo_doc,labour_work):
	lwo_rate = frappe.get_value("Labour Rate Detail",{"parent":lwo_doc,"labour_item":labour_work},["rate"])
	return lwo_rate

@frappe.whitelist()
def fetch_labour_work_order_price(labourer,lwo):
	lwo_rate = frappe.get_value("Labour Rate Detail",{"parent":lwo,"labour_item":labourer},["rate"])
	return lwo_rate






