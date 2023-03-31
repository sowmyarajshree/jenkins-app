from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


def update_bill_qty_in_boq(self,method):
	pass
	'''for d in self.items:
		pcb_qty = frappe.db.get_value('BOQ',{'name':d.item_code},['previous_client_bill_qty']) or 0
		boq_qty =  frappe.db.get_value('BOQ',{'name':d.item_code},['est_total_qty']) or 0
		frappe.db.set_value('BOQ',d.item_code,'billing_progress', round(((pcb_qty+d.qty)/boq_qty) *100))
		frappe.db.set_value('BOQ',d.item_code,'previous_client_bill_qty',(pcb_qty+d.qty))'''

def update_bill_qty_in_boq_on_cancel(self,method):
	pass
	'''for d in self.items:
		pcb_qty = frappe.db.get_value('BOQ',{'name':d.item_code},['previous_client_bill_qty']) or 0
		boq_qty =  frappe.db.get_value('BOQ',{'name':d.item_code},['est_total_qty']) or 0
		frappe.db.set_value('BOQ',d.item_code,'billing_progress', round(((pcb_qty-d.qty)/boq_qty) *100))
		frappe.db.set_value('BOQ',d.item_code,'previous_client_bill_qty',(pcb_qty-d.qty))'''


