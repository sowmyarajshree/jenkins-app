# -*- coding: utf-8 -*-
# Copyright (c) 2021, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ClientBill(Document):
	def validate(self):
		self.set_status()
		self.running_abstract()

	def before_submit(self):
		self.previous_client_bill_qty()
		self.update_client_bill_status()
	def before_cancel(self):
		self.cancel_previous_client_bill_qty()

	def set_status(self):
		if self.docstatus == 0:
			self.nx_status = "Draft"
		if self.docstatus == 1:
			self.nx_status = "Completed"
# Running abstract sum all customer entry
	def running_abstract(self):
		list = frappe.db.sql("""select sum(nx_running_abstract) as running_abstract from `tabClient Bill` where project = %s and customer_name = %s and docstatus = '1' """,(self.project,self.customer_name),as_dict=1)
		if list[0].running_abstract != None:
			doc = frappe.get_last_doc("Client Bill",{"project":self.project,"customer_name":self.customer_name,'docstatus':1})
			self.nx_running_abstract = doc.nx_running_abstract + 1
		else:
			self.nx_running_abstract = 1
		if  self.total_lpe_qty != self.total_client_bill_qty:
			frappe.throw(_("Value Changed In Client Bill LPE Table Update a Values To Click 'Get Item To Bill' Button"))

# Update Previous Client Bill Qty In Boq and Labour Progrss Entry
	def previous_client_bill_qty(self):
		'''for i in self.client_bill_detail:
			doc= frappe.get_doc("BOQ",i.boq)
			frappe.db.set_value("BOQ",doc.name,"previous_client_bill_qty",doc.previous_client_bill_qty + i.qty)'''
		for j in self.client_bill_lpe_detail:
			doc = frappe.get_doc("Labour Progress Entry",j.lpe_no)
			frappe.db.set_value("Labour Progress Entry",doc.name,"previous_client_bill_qty",doc.previous_client_bill_qty + j.qty)

# cancle Previous Client Bill Qty In Boq and Labour Progrss Entry
	def cancel_previous_client_bill_qty(self):
		'''for i in self.client_bill_detail:
			doc= frappe.get_doc("BOQ",i.boq)
			frappe.db.set_value("BOQ",doc.name,"previous_client_bill_qty",doc.previous_client_bill_qty - i.qty)'''
		for j in self.client_bill_lpe_detail:
			qty = frappe.db.get_value("Labour Progress Entry",{"name":j.lpe_no},["previous_client_bill_qty"])
			total_qty = frappe.db.get_value("Labour Progress Entry",{"name":j.lpe_no},["total_qty"])
			frappe.db.set_value("Labour Progress Entry",j.lpe_no,"previous_client_bill_qty",(qty - j.qty))
			if total_qty > qty - j.qty:
				frappe.db.set_value("Labour Progress Entry",j.lpe_no,"client_bill_status","In Progress")

# update status
	def update_client_bill_status(self):
		for j in self.client_bill_lpe_detail:
			qty = frappe.db.get_value("Labour Progress Entry",{"name":j.lpe_no},["previous_client_bill_qty"])
			total_qty = frappe.db.get_value("Labour Progress Entry",{"name":j.lpe_no},["total_qty"])
			if qty > total_qty:
				frappe.throw(_("Client Bill LPE Qty Not Greater Then LabourProgressEntry Qty {0} at row {1}".format(total_qty,j.idx)))
			if total_qty > qty:
				frappe.db.set_value("Labour Progress Entry",j.lpe_no,"client_bill_status","In Progress")
			elif total_qty == qty:
				frappe.db.set_value("Labour Progress Entry",j.lpe_no,"client_bill_status","Completed")
#Client bill table qty_validation
	def validate_client_bill_detail(self):
		for k in self.client_bill_detail:
			sum_of_qty =frappe.db.sql('''select  sum(lp.qty) as qty  from `tabClient Bill LPE Detail` lp where lp.parent = %s and lp.item_of_work = %s group by lp.item_of_work''',(k.parent,k.item_of_work),as_dict=1 )[0]['qty']
			if  sum_of_qty != k.qty:
				frappe.throw(_("Value Changed In Client Bill LPE Table Update a Values To Click 'Get Item To Bill' Button"))
