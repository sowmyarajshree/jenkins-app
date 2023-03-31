# Copyright (c) 2021, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.document import Document

class BOQLedger(Document):
	def validate(self):
		self.validate_ledger()

	def on_update(self):
		self.update_work_and_worked_qty_in_boq()

	def validate_ledger(self): #qty,amount,balance qty
		self.amount = self.rate *  self.qty
		self.balance_qty = self.qty - self.actual_qty
		if(self.actual_qty > self.qty):
			frappe.throw('Total Qty Cannot Be Greater Than Balance Qty')

	def update_work_and_worked_qty_in_boq(self):
		if(self.ledger_type == 'Labour'):
			boq = frappe.get_doc('BOQ',self.boq)
			
			if(self.actual_qty >= 0):
				sum_of_worked_qty = frappe.db.sql(''' select sum(actual_qty) from `tabBOQ Ledger` where boq = %s and ledger_type = "Labour" and has_measurement_sheet = "Yes" ''', self.boq)[0][0]
				
				if sum_of_worked_qty != None:
					frappe.db.set_value('BOQ',self.boq,'sum_of_total_worked_qty',sum_of_worked_qty)
				
				if(frappe.db.get_value('BOQ',{'name':self.boq},['sum_of_total_work_qty'])) == (frappe.db.get_value('BOQ',{'name':self.boq},['sum_of_total_worked_qty'])):
					frappe.db.set_value('BOQ',self.boq,'work_status','Completed')
				elif(frappe.db.get_value('BOQ',{'name':self.boq},['sum_of_total_worked_qty'])) > 0 and (frappe.db.get_value('BOQ',{'name':self.boq},['task']) != None ):
					frappe.db.set_value('BOQ',self.boq,'work_status','In Progress')
				elif (boq.task != None):
					frappe.db.set_value('BOQ',self.boq,'work_status','Scheduled')
				
				#to update the working_progress when lpe is cancelled and set to zero 
				if sum_of_worked_qty != None:			
					sum_of_worked_qty_for_zero = frappe.db.sql(''' select sum(actual_qty) from `tabBOQ Ledger` where boq = %s and ledger_type = "Labour" and has_measurement_sheet = "Yes"''', self.boq)[0][0]
					frappe.db.set_value("BOQ",self.boq,"working_progress",round((sum_of_worked_qty_for_zero/boq.sum_of_total_work_qty) * 100))
							