# -*- coding: utf-8 -*-
# Copyright (c) 2020, nxweb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import erpnext
from frappe import _
from frappe import utils
from frappe.model.document import Document
from frappe.utils import ceil, flt, floor

class GateInward(Document):
	def on_submit(self):
		#self.update_po()
		#self.val_not_exist()
		#self.update_status()
		self.update_visitors_vehicle()
		self.validate_po_status()
		#self.val_child()

	def before_submit(self):
		self.update_total()
		self.validate_duplicate_po()
		self.validate_pending_qty()

	def before_save(self):
		self.update_supplier_name()
		self.update_customer_name()
		self.update_courier_date()
		self.update_visitors_details()
		#self.validate_po_jo()
		#self.update_total()

	'''def on_update(self):
		self.val_child()'''

	def validate(self):
		self.validate_pending_qty()
		self.validate_pending_qty_job()
		self.status = self.get_status()
		#self.update_total()
		#self.validate_po_duplicate()
		#self.get_status_on_ack()

	def on_cancel(self):
		self.status = "Cancelled"
		#self.unlink_po()

	def on_update_after_submit(self):
		self.update_received_count()
		self.update_courier_count()
		self.get_status_on_ack()
		self.update_gate_inward_onupdate()

	def before_update_after_submit(self):
		self.update_total()
		#self.update_received_status_joso()
		self.update_bill_count()
		self.update_customer_return_count()
		self.get_status_on_ack()
		self.update_visitors_out_time()
		#self.make_acknowledgement_read_only()


	#validate pending qty
	def validate_pending_qty(self):
		if self.inward_types == "Purchase Order":
			for i in self.gi_po_details:
				if i.pending_qty <= 0:
					frappe.throw("Pending Qty Cannot be Zero or Negative value")
				if i.in_qty > i.pending_qty:
					frappe.throw("In Qty Cannot be greater than Pending Qty")

	#validate pending qty
	def validate_pending_qty_job(self):
		if self.inward_types == "Job Work Order":
			for j in self.gi_job_work_received_service:
				if j.pending_qty <= 0:
					frappe.throw("Pending Qty Cannot be Zero or Negative value")
				if j.in_qty > j.pending_qty:
					frappe.throw("In Qty Cannot be greater than Pending Qty")


	#update status based on docstatus
	def get_status(self):
		if self.docstatus == 0:
			status = "Draft"
		elif self.docstatus == 1:
			status = "Open"
		elif self.docstatus == 2:
			status = "Cancelled"
		return status

	#update status based on acknowledgement and issued_to
	def update_status(self):
		for d in self.gi_bills:
			if d.acknowledgement == "Received" and d.issued_to:
				self.status = "Completed"
		for d in self.gi_courier_details:
			if d.acknowledgement == "Received" and d.issued_to:
				self.status = "Completed"

	#update status based on acknowledgement
	def get_status_on_ack(self):
		for d in self.gi_po_details:
			if self.received_status == 100:
				self.status = "Completed"
			else:
				self.status = "Open"

		for d in self.gi_customer_returns:
			if self.received_status == 100:
				self.status = "Completed"
			else:
				self.status = "Open"
		for d in self.gi_returnables:
			if d.stock_entry_no:
				self.status = "Completed"
			else:
				self.status = "Open"
		for d in self.gi_bills:
			if self.received_status == 100:
				self.status = "Completed"
			else:
				self.status = "Open"
			if self.status == "Completed":
				if self.billed_status == 100:
					self.status = "Billed"
				else:
					self.status = "Completed"
		for d in self.gi_courier_details:
			if self.received_status == 100:
				self.status = "Completed"
			else:
				self.status = "Open"
			if self.status == "Completed":
				if self.billed_status == 100:
					self.status = "Handed Over"
				else:
					self.status = "Completed"
		if self.inward_types == "Visitors Entry":
			if self.vi_out_time:
				self.status = "Completed"
			else:
				self.status = "Open"

		for d in self.gi_customer_provided:
			if self.received_status == 100:
				self.status = "Completed"
			else:
				self.status = "Open"

		for d in self.gi_job_work_received_service:
			if self.received_status == 100:
				self.status = "Completed"
			else:
				self.status = "Open"

		for d in self.gi_supplier_return:
			if self.received_status == 100:
				self.status = "Completed"
			else:
				self.status = "Open"

	#update gate_inward no to purchase order
	def update_po(self):
		for d in self.gi_po_details:
			po_doc = frappe.get_doc("Purchase Order",d.purchase_order)
			if po_doc.name == d.purchase_order:
				for p in po_doc.items:
					po_doc.gate_inward = self.name
					p.gate_inward = self.name
					po_doc.save(ignore_permissions=True)

	#unlink gate_inward no from purchase order
	def unlink_po(self):
		for d in self.gi_po_details:
			po_doc = frappe.get_doc("Purchase Order",d.purchase_order)
			for p in po_doc.items:
				po_doc.gate_inward = None
				po_doc.save(ignore_permissions=True)

	#update received_status in parent
	def update_received_status_joso(self):
		if self.inward_types == "Job Work Order":
			if self.jo_count != 0 and self.so_count == 0:
				self.received_status = self.jo_status
			if self.so_count != 0 and self.jo_count == 0:
				self.received_status = self.so_status
			if self.jo_count != 0 and self.so_count != 0:
				self.received_status = (self.jo_status + self.so_status)/ 2

	#validates Duplicate purchase order in child table
	def val_child(self):
		for d in self.gi_po_details:
			if frappe.db.count("GI PO Details",{"parent":self.name,"purchase_order":d.purchase_order,"document_no":d.document_no}) > 1:
				frappe.throw(_("Duplicate value {0} at row {1}").format(d.purchase_order,d.idx))

	#validate purchase order status and naming_series
	def val_not_exist(self):
		if self.inward_types == "Purchase Order":
			po_name = []
			for d in self.gi_po_details:
				po_list = frappe.get_list("Purchase Order",filters={"status":["in","To Receive and Bill,To Receive"],"naming_series":"PUR-ORD-.YYYY.-"},fields=["name"])
				for p in po_list:
					po_name.append(p.name)
					if d.purchase_order not in po_name:
						frappe.throw("Value not found")
		if self.inward_types == "Job Work Order":
			po_name = []
			for d in self.gi_po_details:
				po_list = frappe.get_list("Purchase Order",filters={"status":["in","To Receive and Bill,To Receive"],"naming_series":"JOB-ORD-.YYYY.-"},fields=["name"])
				for p in po_list:
					po_name.append(p.name)
					if d.purchase_order not in po_name:
						frappe.throw("Value not found")

	#update supplier name in child table
	def update_supplier_name(self):
		if self.supplier_name:
			for d in self.gi_po_details:
				d.supplier = self.supplier_name
			for d in self.gi_returnables:
				d.supplier_name = self.supplier_name
			for d in self.gi_bills:
				d.supplier_name = self.supplier_name
		'''if self.new_supplier_name:
			for d in self.gi_bills:
				d.supplier_name = self.new_supplier_name'''

	#update customer_name in child table
	def update_customer_name(self):
		if self.customer_name:
			for d in self.gi_customer_returns:
				d.customer_name = self.customer_name

	#update courier_date in child table
	def update_courier_date(self):
		for d in self.gi_courier_details:
			d.courier_date = self.posting_date

	#update parent values to child table
	def update_visitors_details(self):
		for d in self.visitors_detail:
			d.vi_address = self.vi_address
			d.vi_mobile_no = self.vi_mobile_no
			d.vi_contact_person = self.vi_contact_person
			d.vi_out_time = self.vi_out_time
			d.vi_company = self.vi_company

	#validate supplier in purchase order
	def validate_po_jo(self):
		if self.inward_types == "Purchase Order" or self.inward_types == "Job Work Order":
			for d in self.gi_po_details:
				if d.purchase_order:
					supplier =frappe.get_value("Purchase Order",{"name":d.purchase_order},["supplier"])
					if supplier != self.supplier_name:
						frappe.throw("Supplier name not found in Purchase Order")
					else:
						pass

	#update first row values to all other rows in child table
	def update_visitors_vehicle(self):
		for d in self.visitors_detail:
			details = frappe.db.get_list("Visitors Detail",filters={"parent": self.name,"idx":1},fields=["vi_vehicle_no","vi_items_taken_in"])
			for i in details:
				d.vi_items_taken_in = i.vi_items_taken_in
				d.vi_vehicle_no = i.vi_vehicle_no


	#updates visitors out time to child table
	def update_visitors_out_time(self):
		if self.vi_out_time:
			for d in self.visitors_detail:
				d.vi_out_time = self.vi_out_time

	#make acknowledgement field read_only
	def make_acknowledgement_read_only(self):
		for d in self.gi_bills:
			if d.acknowledgement == "Received" and d.issued_to != None:
				#acknowledgement = d.acknowledgement
				#user = d.user
				d.acknowledgement.read_only = 1
				d.issued_to.read_only = 1

	#validate purchase order count
	def validate_po_duplicate(self):
		for d in self.gi_po_details:
			val = frappe.db.sql("""select parent from `tabGI PO Details` where supplier = %s and document_no = %s and purchase_order = %s and parent !=%s""", (d.supplier, d.document_no, d.purchase_order, d.parent))
			if val:
				frappe.throw(_("Entry for the purchase order and document is already existed"))

	#calculate total and all other linked document counts
	def update_total(self):
		self.total = 0
		self.jo_count = 0
		self.so_count = 0
		if self.inward_types == "Purchase Order" or self.inward_types == "Job Work Order":
			for d in self.gi_po_details:
				idx_count = frappe.db.count("GI PO Details",{"parent":self.name,"idx": d.idx})
				self.total += idx_count
		if self.inward_types == "Bills":
			for d in self.gi_bills:
				idx_count = frappe.db.count("GI Bills",{"parent":self.name,"idx": d.idx})
				self.total += idx_count
		if self.inward_types == "Couriers":
			for d in self.gi_courier_details:
				idx_count = frappe.db.count("GI Courier Details",{"parent":self.name,"idx": d.idx})
				self.total += idx_count

		if self.inward_types == "Customer Returns":
			for d in self.gi_customer_returns:
				idx_count = frappe.db.count("GI Customer Returns",{"parent":self.name,"idx": d.idx})
				self.total += idx_count

		if self.inward_types == "Customer Provided Item":
			for d in self.gi_customer_provided:
				idx_count = frappe.db.count("GI Customer Provided",{"parent":self.name,"idx": d.idx})
				self.total += idx_count

		if self.inward_types == "Job Work Order":
			for d in self.gi_job_work_received_service:
				idx_count = frappe.db.count("GI Job Work Received Service",{"parent":self.name,"idx": d.idx})
				jo_count = frappe.db.count("GI Job Work Received Service",{"parent":self.name,"idx": d.idx,"purchase_type":"Job Work"})
				so_count = frappe.db.count("GI Job Work Received Service",{"parent":self.name,"idx": d.idx,"purchase_type":"Service Order"})
				self.total += idx_count
				self.jo_count += jo_count
				self.so_count += so_count
		if self.inward_types == "Supplier Return":
			for d in self.gi_supplier_return:
				idx_count = frappe.db.count("GI Supplier Return",{"parent":self.name,"idx": d.idx})
				self.total += idx_count
		if self.inward_types == "Other Deliveries":
			for d in self.other_deliveries:
				idx_count = frappe.db.count("Other Deliveries",{"parent":self.name,"idx": d.idx})
				self.total += idx_count

	#calculate idx_count and per_billed based on issued_to
	def update_bill_count(self):
		self.idx_count = 0
		self.per_billed = 0
		if self.inward_types == "Bills":
			for d in self.gi_bills:
				if d.issued_to != None:
					self.count += 1
				if d.bill_status == "Billed":
					self.per_billed += 1
		if self.inward_types == "Couriers":
			for d in self.gi_courier_details:
				if d.issued_to != None:
					self.count += 1
				if d.courier_status == "Handed Over":
					self.per_billed += 1

	#calculate idx_count based on sales_invoice_no
	def update_customer_return_count(self):
		self.idx_count = 0
		if self.inward_types == "Customer Returns":
			for d in self.gi_customer_returns:
				if d.sales_invoice_no != None:
					self.count += 1

	#validate Purchase Order status
	def validate_po_status(self):
		if self.inward_types == "Purchase Order":
			for d in self.gi_po_details:
				doc = frappe.get_doc("Purchase Order",d.purchase_order)
				if doc.status not in ["To Receive and Bill","To Receive"]:
					frappe.throw(_("Purchase Order status is {0}").format(doc.status))
				else:
					pass
		if self.inward_types == "Job Work Order":
			for j in self.gi_job_work_received_service:
				doc_j = frappe.get_doc("Purchase Order",j.purchase_order)
				if doc_j.status not in ["To Receive and Bill","To Receive"]:
					frappe.throw(_("Purchase Order status is {0}").format(doc_j.status))
				else:
					pass

	#update received_status and gate_inward status
	def update_received_count(self):
		for d in self.gi_bills:
			if self.inward_types == "Bills":
				received_count = frappe.db.sql("""select count(issued_to) as count from `tabGI Bills` where issued_to IS NOT NULL and parent = %s """,self.name,as_dict=1)
				bill_count = frappe.db.sql("""select count(bill_status) as bill_count from `tabGI Bills` where bill_status = "Billed" and parent = %s """,self.name,as_dict=1)
				for i in received_count:
					#frappe.msgprint(_("{0} count").format(i.count))
					received_status = (i.count / self.total) * 100
					frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,self.name))
					if received_status == 100:
						frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,self.name)
					else:
						frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,self.name)
					self.reload()
				if self.status == "Completed":
					for j in bill_count:
						#frappe.msgprint(_("{0} count").format(j.bill_count))
						bill_status = (j.bill_count / self.total) * 100
						frappe.db.sql("""update `tabGate Inward` set billed_status = %s where name = %s """,(bill_status,self.name))
						if bill_status == 100:
							frappe.db.sql("""update `tabGate Inward` set status = "Billed" where name = %s """,self.name)
						else:
							frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,self.name)
						self.reload()

	#update received_status and gate_inward status
	def update_courier_count(self):
		for d in self.gi_courier_details:
			if self.inward_types == "Couriers":
				received_count = frappe.db.sql("""select count(issued_to) as count from `tabGI Courier Details` where issued_to IS NOT NULL and parent = %s """,self.name,as_dict=1)
				bill_count = frappe.db.sql("""select count(courier_status) as bill_count from `tabGI Courier Details` where courier_status = "Handed Over" and parent = %s """,self.name,as_dict=1)
				for i in received_count:
					#frappe.msgprint(_("{0} count").format(i.count))
					received_status = (i.count / self.total) * 100
					frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,self.name))
					if received_status == 100:
						frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,self.name)
					else:
						frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,self.name)
					self.reload()
				if self.status == "Completed":
					for j in bill_count:
						#frappe.msgprint(_("{0} count").format(j.bill_count))
						bill_status = (j.bill_count / self.total) * 100
						frappe.db.sql("""update `tabGate Inward` set billed_status = %s where name = %s """,(bill_status,self.name))
						if bill_status == 100:
							frappe.db.sql("""update `tabGate Inward` set status = "Handed Over" where name = %s """,self.name)
						else:
							frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,self.name)
						self.reload()

	#validate Duplicate purchase order
	def validate_duplicate_po(self):
		'''if self.inward_types == "Purchase Order":
			po_item_count = 0
			for p in self.gi_po_details:
				po_doc = frappe.get_doc("Purchase Order",p.purchase_order)
				for q in po_doc.items:
					po_item_count += frappe.db.count("Purchase Order Item",{"parent":po_doc.name,"item_code":q.item_code})
				if (frappe.db.count("GI PO Details",{"parent":self.name,"purchase_order":p.purchase_order,"item_code":p.item_code}) > 1):
					frappe.throw(_("Duplicate Purchase Order {0}").format(p.purchase_order))'''
		if self.inward_types == "Job Work Order":
			jo_item_count = 0
			for j in self.gi_job_work_received_service:
				jo_doc = frappe.get_doc("Purchase Order",j.purchase_order)
				for k in jo_doc.items:
					jo_item_count += frappe.db.count("Purchase Order Item",{"parent":jo_doc.name,"item_code":k.item_code})
				if (frappe.db.count("GI Job Work Received Service",{"parent":self.name,"purchase_order":j.purchase_order,"item_code":j.item_code}) > 1):
					frappe.throw(_("Duplicate Purchase Order {0}").format(j.purchase_order))

	#update status on update after submit
	def update_gate_inward_onupdate(self):
		if self.inward_types == "Purchase Order":
			for d in self.gi_po_details:
				received_count = frappe.db.sql("""select count(purchase_receipt_ref_no) as count from `tabGI PO Details` where purchase_receipt_ref_no IS NOT NULL and parent = %s """,self.name,as_dict=1)
				for k in received_count:
					received_status = (k.count / self.total) * 100
					frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,self.name))
					if received_status == 100:
						frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,self.name)
					else:
						frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,self.name)
					self.reload()
		if self.inward_types == "Job Work Order":
			total = 0
			received_count = frappe.db.sql("""select count(purchase_receipt_no) as count from `tabGI Job Work Received Service` where purchase_receipt_no IS NOT NULL and purchase_type = "Job Work" and parent = %s """,self.name,as_dict=1)
			so_received_count = frappe.db.sql("""select count(stock_entry_no) as count from `tabGI Job Work Received Service` where stock_entry_no IS NOT NULL and purchase_type = "Service Order" and parent = %s """,self.name,as_dict=1)
			for k in received_count:
				for s in so_received_count:
					if self.jo_count != 0 and self.so_count == 0:
						received_status = (k.count / self.jo_count) * 100
						frappe.db.sql("""update `tabGate Inward` set jo_status = %s where name = %s """,(received_status,self.name))
						frappe.db.sql("""update `tabGate Inward` set received_status = jo_status where name = %s """,(self.name))
					if self.so_count != 0 and self.jo_count == 0:
						so_status = (s.count / self.so_count) * 100
						frappe.db.sql("""update `tabGate Inward` set so_status = %s where name = %s """,(so_status,self.name))
						frappe.db.sql("""update `tabGate Inward` set received_status = so_status where name = %s """,(self.name))
					if self.so_count != 0 and self.jo_count != 0:
						total = self.so_count + self.jo_count
						so_status_1 = ((s.count / self.so_count) * 100)
						jo_status_1 = ((k.count / self.jo_count) * 100)
						frappe.db.sql("""update `tabGate Inward` set so_status = %s where name = %s """,(so_status_1,self.name))
						frappe.db.sql("""update `tabGate Inward` set jo_status = %s where name = %s """,(jo_status_1,self.name))
						frappe.db.sql("""update `tabGate Inward` set received_status = (jo_status+so_status)/2 where name = %s """,(self.name))
					status = frappe.db.sql("""select received_status from `tabGate Inward` where name = %s """,self.name,as_dict=1)
					for i in status:
						if i.received_status == 100:
							frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,self.name)
						else:
							frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,self.name)
						self.reload()



'''@frappe.whitelist()
def update_po_items(docname,scan_barcode):
	if scan_barcode:
		po_doc = frappe.get_doc("Purchase Order",scan_barcode)
		supplier = po_doc.supplier
		po_date = po_doc.transaction_date

		return supplier,po_date'''


#update child table based on Purchase order child table through update button
@frappe.whitelist()
def update_po_items(docname,supplier_name,document_no,document_date,scan_barcode):
	pending_qty = 0
	items = []
	doc = frappe.get_doc("Purchase Order",scan_barcode)
	for d in doc.items:
		pending_qty = (d.qty + ceil(d.qty * 5/100)) - d.received_qty
		items.append({
			"purchase_order":scan_barcode,
			"supplier": doc.supplier,
			"document_no": document_no,
			"document_date":document_date,
			"in_qty": d.qty,
			"pending_qty": pending_qty,
			"item_name": d.item_name,
			"po_date":doc.transaction_date,
			"description":d.description,
			"item_code":d.item_code,
			"uom":d.uom,
			"rate":d.rate,
			"amount":d.amount,
			"warehouse":d.warehouse,
			"cost_center":d.cost_center,
			"nx_item_code":d.nx_item_code,
			"conversion_factor":d.conversion_factor,
			"stock_uom":d.stock_uom,
			"is_subcontracted": doc.is_subcontracted,
			"supplier_warehouse": doc.supplier_warehouse
		})
	return items
