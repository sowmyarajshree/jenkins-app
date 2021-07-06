from __future__ import unicode_literals
import frappe
import datetime
from datetime import timedelta
from frappe import _
from frappe import utils
from frappe.utils import ceil
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document



#update sales_invoice name and status in gate_inward on_submit
@frappe.whitelist()
def update_gate_inward(self,method):
    if self.is_return == 1:
        if self.gate_inward:
            doc = frappe.get_doc("Gate Inward",self.gate_inward)
            for d in doc.gi_customer_returns:
                d.sales_invoice_no = self.name
                doc.save(ignore_permissions=True)
                received_count = frappe.db.sql("""select count(sales_invoice_no) as count from `tabGI Customer Returns` where sales_invoice_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
                for k in received_count:
                    received_status = (k.count / doc.total) * 100
                    frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
                    if received_status == 100:
                        frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
                    else:
                        frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
                    doc.reload()

#unlink sales_invoice name and change gate_inward status on_cancel
@frappe.whitelist()
def cancel_gate_inward_link(self,method):
    if self.is_return == 1:
        if self.gate_inward:
            doc = frappe.get_doc("Gate Inward",self.gate_inward)
            for d in doc.gi_customer_returns:
                d.sales_invoice_no = None
                doc.save(ignore_permissions=True)
                received_count = frappe.db.sql("""select count(sales_invoice_no) as count from `tabGI Customer Returns` where sales_invoice_no IS NOT NULL and parent = %s """,doc.name,as_dict=1)
                for k in received_count:
                    received_status = (k.count / doc.total) * 100
                    frappe.db.sql("""update `tabGate Inward` set received_status = %s where name = %s """,(received_status,doc.name))
                    if received_status == 100:
                        frappe.db.sql("""update `tabGate Inward` set status = "Completed" where name = %s """,doc.name)
                    else:
                        frappe.db.sql("""update `tabGate Inward` set status = "Open" where name = %s """,doc.name)
                    doc.reload()


#creates stock_entry on_submit
@frappe.whitelist()
def create_stock_entry(self,method):
    if self.is_return == 0:
        doc = frappe.new_doc("Stock Entry")
        doc.stock_entry_type = "Material Transfer"
        #doc.from_warehouse = "Main Store - ECE"
        doc.to_warehouse = self.customer_warehouse
        doc.sales_invoice = self.name
        for d in self.items:
            if d.bin_name != None:
                doc.append("items",{
                        "s_warehouse": "Safety Stock Store - ECE",
                        "t_warehouse": self.customer_warehouse,
                        "item_code": d.bin_name,
                        "item_name": d.bin_item_name,
                        "item_group": d.item_group,
                        "description": d.bin_item_name,
                        "qty": d.total_no_of_bins,
                        "uom": d.uom,
                        "stock_uom":d.stock_uom,
                        "conversion_factor": d.conversion_factor,
                        "transfer_qty": d.total_no_of_bins,
                        "nx_rate": d.rate,
                        "basic_rate": d.rate,
                        "basic_amount": d.amount,
                        "amount": d.amount,
                        "expense_account":d.expense_account,
                        "cost_center": d.cost_center,
                        "actual_qty": d.actual_qty,
                        "allow_zero_valuation_rate": 1
                })
                #doc.docstatus = 1
                doc.save(ignore_permissions=True)
        stock_doc_list = frappe.get_list("Stock Entry",filters={"sales_invoice":self.name,"docstatus":0},fields=["name"])
        for s in stock_doc_list:
            if s.name != None:
                s_doc = frappe.get_doc("Stock Entry",s.name)
                s_doc.docstatus = 1
                s_doc.save(ignore_permissions=True)




#unlink stock_entry on_cancel
@frappe.whitelist()
def unlink_stock_entry(self,method):
    stock_entry_list = frappe.get_list("Stock Entry",filters={"sales_invoice":self.name},fields=["name"])
    for s in stock_entry_list:
        doc = frappe.get_doc("Stock Entry",s.name)
        doc.sales_invoice = None
        doc.docstatus = 2
        doc.save(ignore_permissions=True)
        #frappe.delete_doc("Stock Entry",doc.name)


#updates customer and posting_date from parent to child table
@frappe.whitelist()
def update_cus_date(self,method):
    for d in self.items:
        d.customer = self.customer
        d.posting_date = self.posting_date



#calculates total_no_of_bins in child table
@frappe.whitelist()
def calculate_bin_qty(self,method):
    for d in self.items:
        if d.bin_qty != 0:
            d.total_no_of_bins = ceil(d.qty/d.bin_qty)
