from __future__ import unicode_literals
import frappe, json
from frappe import msgprint, _
from frappe.model.document import Document
from frappe import utils


#function to update delivery trip no to stock entry doctype
@frappe.whitelist()
def update_stock_entry(self,method):
    for d in self.supplier_stops:
        if d.dc_no:
            doc = frappe.get_doc("Stock Entry",d.dc_no)
            doc.delivery_trip_no = self.name
            doc.save(ignore_permissions=True)


#this function removes the delivery trip no on_cancel
@frappe.whitelist()
def unlink_stock_entry(self,method):
    for d in self.supplier_stops:
        if d.dc_no:
            doc = frappe.get_doc("Stock Entry",d.dc_no)
            doc.delivery_trip_no = None
            doc.save(ignore_permissions=True)


#function to update delivery trip no to sales invoice doctype
@frappe.whitelist()
def update_sv_st(self,method):
    for d in self.delivery_stops:
        if d.invoice_no:
            doc = frappe.get_doc("Sales Invoice",d.invoice_no)
            doc.delivery_trip_no = self.name
            doc.save(ignore_permissions=True)
    if self.is_dc == 1:
        for i in self.customer_stop:
            if i.dc_no:
                docs = frappe.get_doc("Stock Entry",i.dc_no)
                docs.delivery_trip_no = self.name
                docs.save(ignore_permissions=True)


#this function removes the delivery trip no on_cancel
@frappe.whitelist()
def unlink_sv_st(self,method):
    for d in self.delivery_stops:
        if d.invoice_no:
            doc = frappe.get_doc("Sales Invoice",d.invoice_no)
            doc.delivery_trip_no = None
            doc.save(ignore_permissions=True)
        if d.dc_no:
            docs = frappe.get_doc("Stock Entry",d.dc_no)
            docs.delivery_trip_no = None
            docs.save(ignore_permissions=True)

#function to get address name from address child table that is Dynamic link
@frappe.whitelist()
def update_address(name):
    '''for d in self.supplier_stops:
        address = frappe.get_value("Address",{"address_title":d.supplier},["name"])
        d.address = address'''
    link = frappe.get_value("Dynamic Link",{"link_name":name,"link_doctype":"Supplier"},["parent"])
    return link


#function to get address name from address child table that is Dynamic link
@frappe.whitelist()
def update_cus_address(name):
    link = frappe.get_value("Dynamic Link",{"link_name":name,"link_doctype":"Customer"},["parent"])
    return link


#function to update delivery_status
@frappe.whitelist()
def update_delivery_status(self,method):
    if self.ending_km != None and self.in_time != None:
        self.delivery_status = "Closed"
    else:
        self.delivery_status = "Open"
