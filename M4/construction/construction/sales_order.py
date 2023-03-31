from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


def boq_status_changes_not_sche(self,method):
	for i in self.items:
		soi_qty = frappe.db.sql('''SELECT sum(qty) as qty FROM `tabSales Order Item` WHERE item_code = %s and docstatus = 1 ''',(i.item_code))[0][0]
		bill_qty = frappe.get_value("BOQ",{"name":i.item_code},["bill_qty"])

		if (soi_qty != None) and (soi_qty + i.qty) == bill_qty:
			frappe.db.set_value("BOQ",i.item_code,"billing_status","Ordered")
		elif  (soi_qty != None) and (soi_qty + i.qty) != bill_qty:
			frappe.db.set_value("BOQ",i.item_code,"billing_status","To Order")
		elif  (soi_qty != None) and (soi_qty + i.qty) > bill_qty:
			frappe.throw(_("Total Bill Qty is exceeded, Available Balance qty for the Order is {0}").format(bill_qty - soi_qty))
			frappe.throw(_("soi_qty {0}, bill_qty {1}").format((i.qty + soi_qty),bill_qty))

		elif (soi_qty == None):
			frappe.db.set_value("BOQ",i.item_code,"billing_status","Ordered")
		

def boq_status_changes_on_cancel(self,method):
	for i in self.items:
		frappe.db.set_value("BOQ",i.item_code,"billing_status","To Order")
		
def validate_customer(self,method):
	for i in self.items:
		i.nx_balance_to_bill = i.nx_total_boq_qty - i.nx_previous_billed_qty
		if i.prevdoc_docname != None:
			quot_doc = frappe.get_doc("Quotation",i.prevdoc_docname)
			if quot_doc.customer_name != self.customer:
				frappe.throw(_("Customer name is not same as in Quotation, it should be {0}").format(quot_doc.customer_name))

def validate_delivery_date(self,method):
	if self.delivery_date < self.transaction_date:
		frappe.throw(_("Delivery Date can't set before the posting date"))