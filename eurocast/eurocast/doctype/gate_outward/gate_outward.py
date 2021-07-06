# -*- coding: utf-8 -*-
# Copyright (c) 2020, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import utils
import erpnext
from frappe import _
from frappe.model.document import Document

class GateOutward(Document):
	def on_submit(self):
		self.update_stock_entry()
		self.update_sales_invoice()
		self.update_stock_entry_so()
		self.validate_duplicate_entries()
		self.update_gate_out_forotherdeliveries()

	def validate(self):
		self.validate_dc_no_others()

	def before_submit(self):
		self.update_purchase_order_no()
		self.update_courier_status()

	'''def before_save(self):
		self.update_purchase_order_no()'''

	def on_cancel(self):
		self.unlink_stock_entry()
		self.unlink_sales_invoice()
		self.cancel_stock_entry()

	def before_update_after_submit(self):
		self.update_courier_status()

	#updates gate_outward number to stock_entry
	def update_stock_entry(self):
		if self.gate_outward_type == "Purchase Order" or self.gate_outward_type == "Job Order":
			for d in self.go_purchase_order_details:
				if d.document_no:
					doc = frappe.get_doc("Stock Entry",d.document_no)
					doc.nx_gate_outward = self.name
					doc.stock_entry_status = "Closed"
					doc.save(ignore_permissions=True)

	#unlink gate_outward number from stock_entry
	def unlink_stock_entry(self):
		if self.gate_outward_type == "Purchase Order" or self.gate_outward_type == "Job Order":
			for d in self.go_purchase_order_details:
				if d.document_no:
					doc = frappe.get_doc("Stock Entry",d.document_no)
					doc.nx_gate_outward = None
					doc.stock_entry_status = "Open"
					doc.save(ignore_permissions=True)

	#update gate_outward number to sales_invoice
	def update_sales_invoice(self):
		if self.gate_outward_type == "Invoices":
			for d in self.go_invoices:
				if d.invoice_no:
					doc = frappe.get_doc("Sales Invoice",d.invoice_no)
					doc.gate_outward = self.name
					doc.sales_invoice_status = "Closed"
					doc.save(ignore_permissions=True)

	#unlink gate_outward number from sales_invoice
	def unlink_sales_invoice(self):
		if self.gate_outward_type == "Invoices":
			for d in self.go_invoices:
				if d.invoice_no:
					doc = frappe.get_doc("Sales Invoice",d.invoice_no)
					doc.gate_outward = None
					doc.sales_invoice_status = "Open"
					doc.save(ignore_permissions=True)

	#update purchase_order number in stock_entry
	def update_purchase_order_no(self):
		for d in self.go_purchase_order_details:
			if self.gate_outward_type == "Purchase Order":
				if d.document_no:
					doc = frappe.get_doc("Stock Entry",d.document_no)
					d.purchase_order = doc.nx_sub_purchase_order
					po = frappe.get_doc("Purchase Order",doc.nx_sub_purchase_order)
					d.po_date = po.transaction_date
			if self.gate_outward_type == "Job Order":
				if d.document_no:
					doc_s = frappe.get_doc("Stock Entry",d.document_no)
					d.purchase_order = doc_s.purchase_order
					po_s = frappe.get_doc("Purchase Order",doc_s.purchase_order)
					d.po_date = po_s.transaction_date

	#update courier_status in GateOutward
	def update_courier_status(self):
		if self.gate_outward_type == "Couriers":
			for d in self.go_courier_details:
				if d.courier_issued_time != None and d.courier_tracking_no != None:
					d.courier_status = "Completed"
				else:
					d.courier_status = "Open"

	#update gate_outward number to stock_entry
	def update_stock_entry_so(self):
		if self.gate_outward_type == "Job Order":
			for d in self.go_send_service:
				doc = frappe.get_doc("Stock Entry",d.stock_entry_no)
				if doc.stock_entry_type == "Send to Service":
					if doc.nx_supplier == d.supplier_name:
						doc.nx_gate_outward = self.name
						doc.save(ignore_permissions=True)
				if doc.stock_entry_type == "Send to Subcontractor":
					if doc.supplier == d.supplier_name:
						doc.nx_gate_outward = self.name
						doc.save(ignore_permissions=True)

	#unlink gate_outward number from stock_entry
	def cancel_stock_entry(self):
		if self.gate_outward_type == "Job Order":
			for d in self.go_send_service:
				doc = frappe.get_doc("Stock Entry",d.stock_entry_no)
				if doc.stock_entry_type == "Send to Service":
					if doc.nx_supplier == d.supplier_name:
						doc.nx_gate_outward = None
						doc.save(ignore_permissions=True)
				if doc.stock_entry_type == "Send to Subcontractor":
					if doc.supplier == d.supplier_name:
						doc.nx_gate_outward = None
						doc.save(ignore_permissions=True)

	#validates Duplicate stock Entry
	def validate_duplicate_entries(self):
		for d in self.go_send_service:
			if frappe.db.count("GO Send Service",{"parent":self.name,"stock_entry_no":d.stock_entry_no}) > 1:
				frappe.throw(_("Duplicate value {0} at row {1}").format(d.stock_entry_no,d.idx))


	#update gate outward name to stock entry
	def update_gate_out_forotherdeliveries(self):
		if self.gate_outward_type == "Other Deliveries":
			for d in self.go_other_deliveries:
				if d.dc_no != None:
					doc = frappe.get_doc("Stock Entry",d.dc_no)
					doc.nx_gate_outward = self.name
					doc.save(ignore_permissions=True)

	#validate gate outward name in link field
	def validate_dc_no_others(self):
		if self.gate_outward_type == "Other Deliveries":
			for d in self.go_other_deliveries:
				doc = frappe.get_doc("Stock Entry",d.dc_no)
				if doc.nx_gate_outward != None:
					frappe.throw("Gate Outward is already mapped in selected DC")


#update purchase_order item table in update button
@frappe.whitelist()
def update_items_service(purchase_order):
	po = frappe.get_doc("Purchase Order",purchase_order)
	items = []
	for q in po.items:
		stock_uom = frappe.get_value("Item",{"item_code":q.item_code},["stock_uom"])
		item_group = frappe.get_value("Item",{"item_code":q.item_code},["item_group"])
		uom = frappe.get_value("UOM Conversion Detail",{"parent":q.item_code},["uom"])
		conversion_factor = frappe.get_value("UOM Conversion Detail",{"parent":q.item_code},["conversion_factor"])
		items.append({
			"qty": q.qty,
			"item_code": q.item_code,
			"stock_uom": stock_uom,
			"uom": uom,
			"conversion_factor": conversion_factor,
			"transfer_qty":q.qty,
			"item_group": item_group,
			"item_name": q.item_name
		})
	return items
