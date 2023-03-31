from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


@frappe.whitelist()
def billed_qty_update_in_boq(self,method):
	for i in self.items:
		boq_doc = frappe.get_doc("BOQ",i.nx_boq)
		boq_doc.billed_qty += i.qty
		boq_doc.qty_after_request = boq_doc.bill_qty - boq_doc.billed_qty
		if boq_doc.billed_qty > boq_doc.bill_qty:
			frappe.throw(_("Bill Qty Cannot be Exceeded"))
		boq_doc.save(ignore_permissions = True)


@frappe.whitelist()
def billed_qty_update_in_boq_on_cancel(self,method):
	for i in self.items:
		boq_doc = frappe.get_doc("BOQ",i.nx_boq)
		boq_doc.billed_qty -= i.qty
		boq_doc.qty_after_request = boq_doc.bill_qty - boq_doc.billed_qty
		boq_doc.save(ignore_permissions = True)


@frappe.whitelist()
def validate_customer_in_project(self,method):
	if self.party_name != frappe.get_value("Project",{"name":self.project},["customer"]):
		frappe.throw(_("Customer in the given Project is {0}").format(frappe.get_value("Project",{"name":self.project},["customer"])))

def boq_status_changes_so_on_cancel(self,method):
	for i in self.items:
		frappe.db.set_value("BOQ",i.nx_boq,"billing_status","To Quotation")

def quotation_qty_after_qty_request(self):
	for i in self.items:
		tot_qty = frappe.db.sql('''SELECT sum(qty) FROM `tabQuotation Item` WHERE nx_boq = %s ''',(i.nx_boq))[0][0]
		boq_doc = frappe.get_doc("BOQ",i.nx_boq)
		#if i.nx_boq == tot_qty.parent
		frappe.db.set
		boq_doc.bill_qty - tot_qty		