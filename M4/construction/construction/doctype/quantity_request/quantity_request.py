# -*- coding: utf-8 -*-
# Copyright (c) 2021, Nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, add_days, nowdate
from frappe import _
from construction.construction.doctype.boq.boq import type_converter

class QuantityRequest(Document):
	def validate(self):
		self.validate_qty()
	def before_submit(self):
		self.update_task_est_qty()
		self.status_update_after_completed()
		self.update_excess_qty_in_boq()
		self.uom_conversion_after_excess_qty_added()

	def before_cancel(self):
		self.update_task_est_qty_on_cancel()
		self.update_excess_qty_in_boq_while_cancel()
		self.uom_conversion_after_excess_qty_added_on_cancel()

	
	def validate_qty(self):
		if self.qty <= 0:
			frappe.throw(_("Qty cannot be Zero or Negative Number"))


	def update_task_est_qty(self):
		boq_doc = frappe.get_doc("BOQ",self.boq)
		if boq_doc.task != None:
			task_doc = frappe.get_doc("Task",boq_doc.task)
			task_doc.nx_qty = boq_doc.est_total_qty
			task_doc.save(ignore_permissions = True)

	def update_task_est_qty_on_cancel(self):
		boq_doc = frappe.get_doc("BOQ",self.boq)
		if boq_doc.task != None:
			task_doc = frappe.get_doc("Task",boq_doc.task)
			task_doc.nx_qty = boq_doc.est_total_qty
			task_doc.save(ignore_permissions = True)



	def status_update_after_completed(self):
		if self.boq != None:
			boq_doc = frappe.get_doc("BOQ",self.boq)
			if boq_doc.work_status == "Completed":
				frappe.db.set_value("BOQ",self.boq,"work_status","Scheduled")


	#update excess qty while quantity request submit
	def update_excess_qty_in_boq(self):
		boq_doc = frappe.get_doc('BOQ', self.boq)
		boq_doc.excess_quantity += self.qty
		boq_doc.est_total_qty = (boq_doc.estimate_quantity * boq_doc.quantity) + boq_doc.excess_quantity
		if boq_doc.has_conversion == 0:
			boq_doc.sum_of_total_work_qty = sum((d.qty_as_stock * boq_doc.est_total_qty) for d in boq_doc.labour_detail if d.has_measurement_sheet == "Yes")
		boq_doc.bill_qty = boq_doc.est_total_qty
		boq_doc.qty_after_request = boq_doc.bill_qty - boq_doc.billed_qty
		boq_doc.save(ignore_permissions = True)

	#update excess qty while quantity request cancel
	def update_excess_qty_in_boq_while_cancel(self):
		boq_doc = frappe.get_doc('BOQ', self.boq)
		boq_doc.excess_quantity -= self.qty
		boq_doc.est_total_qty = (boq_doc.estimate_quantity * boq_doc.quantity) + boq_doc.excess_quantity
		if boq_doc.has_conversion == 0:
			boq_doc.sum_of_total_work_qty = sum((d.qty_as_stock * boq_doc.est_total_qty) for d in boq_doc.labour_detail if d.has_measurement_sheet == "Yes")
		boq_doc.bill_qty = boq_doc.est_total_qty
		boq_doc.qty_after_request = boq_doc.bill_qty - boq_doc.billed_qty
		boq_doc.save(ignore_permissions = True)

	def uom_conversion_after_excess_qty_added(self):
		if self.uom != None:
			boq_doc = frappe.get_doc("BOQ",self.boq)
			if boq_doc.has_conversion == 1:
				value = type_converter((boq_doc.est_total_qty),boq_doc.from_uom,boq_doc.to_uom,boq_doc.thickness,boq_doc.thickness_uom,boq_doc.width,boq_doc.width_uom)
				boq_doc.converted_qty = value
				boq_doc.sum_of_total_work_qty = sum((d.qty_as_stock * boq_doc.converted_qty) for d in boq_doc.labour_detail if d.has_measurement_sheet == "Yes")
				boq_doc.save(ignore_permissions = True)

	def uom_conversion_after_excess_qty_added_on_cancel(self):
		if self.uom != None:
			boq_doc = frappe.get_doc("BOQ",self.boq)
			if boq_doc.has_conversion == 1:
				value = type_converter((boq_doc.est_total_qty),boq_doc.from_uom,boq_doc.to_uom,boq_doc.thickness,boq_doc.thickness_uom,boq_doc.width,boq_doc.width_uom)
				boq_doc.converted_qty = value
				boq_doc.sum_of_total_work_qty = sum((d.qty_as_stock * boq_doc.converted_qty) for d in boq_doc.labour_detail if d.has_measurement_sheet == "Yes")
				boq_doc.save(ignore_permissions = True)	