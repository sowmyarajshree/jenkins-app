#Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import re
import frappe
from frappe.model.document import Document
from frappe import _

class CashRequisitionEntry(Document):
	def validate(self):
		self.calculate_total_amount()
	def before_submit(self):
		self.validate_qty()
		self.update_paid_amount()
	def before_cancel(self):
		self.update_paid_amount_on_cancel()



	def validate_qty(self):
		for d in self.cash_requisition_details:
			if (d.approved_amount <= 0):
				frappe.throw(_('Approved Amount Cannot Be Zero at row {0}').format(d.idx))
			'''else:
				if(d.approved_amount > d.request_amount):
					frappe.throw(_('Approved Amount Cannot Be Greater then Request amount at row {0}').format(d.idx))'''


	def calculate_total_amount(self):
		

		amount = 0 
		approved_labour_bill_amount = 0
		for d in self.cash_requisition_details:
			amount += d.request_amount
			approved_labour_bill_amount += d.approved_amount
			#if(d.payment_request_type == 'Purchase Invoice' and not(d.description)):
				#d.description = re.sub("[\[\]']","",str([item.description for item in frappe.get_doc("Purchase Invoice",d.document_name).items]))

		self.total_labour_bill_amount = amount
		self.approved_labour_bill_amount = approved_labour_bill_amount
		if (self.total_requested_amount == 0):
			frappe.throw('Total Requested Amount cannot be zero')

		self.total_requested_amount = self.total_requested_advance + self.total_labour_bill_amount
		self.total_approved_amount = self.approved_labour_bill_amount + self.total_approved_advance








	def update_paid_amount(self):
		for i in self.cash_requisition_details:
			
			if(i.payment_request_type == 'Purchase Invoice' or i.payment_request_type ==  'Expense Claim'):
				adv_amt = frappe.db.get_value(i.payment_request_type,{"name":i.document_name},['nx_advance_paid'])
				frappe.db.set_value(i.payment_request_type,i.document_name,'nx_advance_paid',(adv_amt+i.approved_amount))
			elif(i.payment_request_type != 'Purchase Invoice'):
				adv_amt = frappe.db.get_value(i.payment_request_type,{"name":i.document_name},['advance_paid'])
				frappe.db.set_value(i.payment_request_type,i.document_name,'advance_paid',(adv_amt+i.approved_amount))



	def update_paid_amount_on_cancel(self):
		for i in self.cash_requisition_details:
			
			if(i.payment_request_type == 'Purchase Invoice' or i.payment_request_type == 'Expense Claim'):
				adv_amt = frappe.db.get_value(i.payment_request_type,{"name":i.document_name},['nx_advance_paid'])
				frappe.db.set_value(i.payment_request_type,i.document_name,'nx_advance_paid',(adv_amt-i.approved_amount))
			elif(i.payment_request_type != 'Purchase Invoice'):
				adv_amt = frappe.db.get_value(i.payment_request_type,{"name":i.document_name},['advance_paid'])
				frappe.db.set_value(i.payment_request_type,i.document_name,'advance_paid',(adv_amt-i.approved_amount))

			
@frappe.whitelist()
def get_subcontractor_details(project,from_date,to_date):
	subcont_detail = []
	lpe_rate = frappe.db.sql(''' SELECT sum(labour_rate) as tot_labour_rate, subcontractor FROM `tabLabour Progress Entry` WHERE project_name = %s  and docstatus = 1 and  posting_date between %s AND %s GROUP BY  subcontractor''',(project,from_date,to_date))[0][0]
	lpe_subcontractor = frappe.db.sql(''' SELECT sum(labour_rate) as tot_labour_rate, subcontractor FROM `tabLabour Progress Entry` WHERE project_name = %s  and docstatus = 1 and  posting_date between %s AND %s GROUP BY  subcontractor''',(project,from_date,to_date))[0][1]
	subcont_detail.append({
			"subcontractor":lpe_subcontractor,
			"amount":lpe_rate
		})
	return subcont_detail



@frappe.whitelist()
def getBillList(billTypeList,filters):
	billList = []
	pyFilter = eval(filters)
	for d in eval(billTypeList):
		if d == 'Muster Role Entry':
			temp = [i.update({'doctype': d}) for i in frappe.db.get_list(d,{'project':pyFilter["project"],'status':'To Bill'},["name","posting_date","total_amount","advance_paid","muster_role"])]
			billList.append(temp)
		elif(d == 'F and F Entry' or d == 'Rate Work Entry'):
			temp = [i.update({'doctype': d}) for i in frappe.db.get_list(d,{'project':pyFilter["project"],'status':'To Bill','posting_date':["between",[pyFilter['startDate'],pyFilter['endDate']]]},["name","posting_date","total_amount","advance_paid","subcontractor"])]
			billList.append(temp)
		elif(d == 'Purchase Invoice'):
			temp = [i.update({'doctype': d}) for i in frappe.db.get_list(d,{'project_name':pyFilter["project"],'status': ["in",['Overdue','Unpaid']],'company':pyFilter["company"],'posting_date':["between",[pyFilter['startDate'],pyFilter['endDate']]]},["name","posting_date","rounded_total","nx_advance_paid","supplier"])]
			billList.append(temp)	
	return billList

@frappe.whitelist()
def update_closing_balance(accountHead,acc_period):
	closingCreditDebit = frappe.db.sql("""select sum(credit),sum(debit) from `tabGL Entry` where account = %s and posting_date <= %s group by account """,(accountHead,frappe.db.get_value('Accounting Period',acc_period,"end_date")),as_dict=1)
	return closingCreditDebit