# Copyright (c) 2023, Nxweb and contributors
# For license information, please see license.txt

# import frappe
#from frappe.model.document import Document

#class PaymentRequisitionEntry(Document):
#	pass

#Copyright (c) 2022, Nxweb and contributors
# For license information, please see license.txt

import re
import frappe
from frappe.model.document import Document
from frappe import _

class PaymentRequisitionEntry(Document):
	def validate(self):
		self.calculate_total_amount()
	def before_submit(self):
		self.validate_qty()
		self.update_paid_amount()
	def before_cancel(self):
		self.update_paid_amount_on_cancel()



	def validate_qty(self):
		for d in self.labour_bill_detail:
			if (d.approved_amount <= 0):
				frappe.throw(_('Approved Amount Cannot Be Zero at row {0}').format(d.idx))
			'''else:
				if(d.approved_amount > d.request_amount):
					frappe.throw(_('Approved Amount Cannot Be Greater then Request amount at row {0}').format(d.idx))'''


	def calculate_total_amount(self):
		

		amount = 0 
		approved_labour_bill_amount = 0
		for d in self.labour_bill_detail:
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
		for i in self.labour_bill_detail: #changed
			
			if(i.payment_request_type == 'Purchase Invoice' or i.payment_request_type ==  'Expense Claim'):
				adv_amt = frappe.db.get_value(i.payment_request_type,{"name":i.document_name},['nx_advance_paid'])
				frappe.db.set_value(i.payment_request_type,i.document_name,'nx_advance_paid',(adv_amt+i.approved_amount))
			elif(i.payment_request_type != 'Purchase Invoice'):
				adv_amt = frappe.db.get_value(i.payment_request_type,{"name":i.document_name},['advance_paid'])
				frappe.db.set_value(i.payment_request_type,i.document_name,'advance_paid',(adv_amt+i.approved_amount))



	def update_paid_amount_on_cancel(self):
		for i in self.labour_bill_detail: #changed
			
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
def getBillList(filters):
	pyFilter = eval(filters)
	billList = []
	if pyFilter['expense_claim'] == 0:
		mre = [i.update({'doctype': 'Muster Roll Entry'}) for i in frappe.db.get_list('Muster Roll Entry',{'project':pyFilter["project"],'status':'To Bill'},["name","posting_date","total_amount","advance_paid","muster_roll"])]
		billList.append(mre)
		pi = [i.update({'doctype': 'Purchase Invoice'}) for i in frappe.db.get_list('Purchase Invoice',{'project_name':pyFilter["project"],'status': ["in",['Overdue','Unpaid']],'company':pyFilter["company"],'posting_date':["between",[pyFilter['startDate'],pyFilter['endDate']]]},["name","posting_date","rounded_total","nx_advance_paid","supplier"])]
		billList.append(pi)	
		onHoldBill = [i.update({'doctype': 'Labour Bill Detail'})
		 for i in frappe.db.get_list('Labour Bill Detail',{'project':pyFilter["project"],'status': "On Hold"},["party_type","document_name","party","muster_roll","f_and_f_entry","rate_work_entry","advance_paid","project","status","payment_request_type","request_amount","description"])
		   ]
		billList.append(onHoldBill)
	return billList			

@frappe.whitelist()
def update_closing_balance(accountHead,acc_period):
	closingCreditDebit = frappe.db.sql("""select sum(credit),sum(debit) from `tabGL Entry` where account = %s and posting_date <= %s group by account """,(accountHead,frappe.db.get_value('Accounting Period',acc_period,"end_date")),as_dict=1)
	balance = closingCreditDebit[0]['sum(debit)'] - closingCreditDebit[0]['sum(credit)']
	return balance

@frappe.whitelist()
def supplier_advance(supplier,project):
	h=frappe.db.sql("""select p.project,p.project_name,p.supplier,sum(p.outstanding_amount) as amount from `tabPurchase Invoice` p left join `tabSupplier` s on s.name = p.supplier where s.supplier_group like "Labour Subcontractor%%" and p.outstanding_amount > 0 and p.supplier=%s and p.project_name =%s group by p.supplier,p.project_name """,(supplier,project),as_dict=1)
	return h


@frappe.whitelist()
def make_journalEntry(doc_name):
	pre_doc = frappe.get_doc("Payment Requisition Entry",doc_name)
	for row in pre_doc.labour_bill_detail:
		if(row.payment_request_type == "Muster Roll Entry" and row.status == "Approved"):
			print(row)
			mre_doc = frappe.get_doc("Muster Roll Entry",row.document_name)
			journal_doc = frappe.new_doc("Journal Entry")
			journal_doc.update({
				"company":pre_doc.company,
				"posting_date":pre_doc.request_date,
				"user_remark":row.description
				})
			if(mre_doc.tax_amount != 0):
				print("have tax",mre_doc.name)
				journal_doc.append("accounts",{
					"account":"Cash - SSC",
					"credit_in_account_currency":mre_doc.rounded_total,
					"nx_muster_roll_entry":mre_doc.name,
					"project":mre_doc.project
					})
				journal_doc.append("accounts",{
		        	"account":"TDS Account - SSC",
		        	"credit_in_account_currency":mre_doc.tax_amount,
		        	"nx_muster_roll_entry":mre_doc.name,
		        	"project":mre_doc.project
		        	})
				journal_doc.append("accounts",{
					"account":"NMR Wages - SSC",
					"debit_in_account_currency":mre_doc.rounded_total + mre_doc.tax_amount,
					"nx_muster_roll_entry":mre_doc.name,
					"project":mre_doc.project
					})
				journal_doc.save(ignore_permissions = True)
			else:
				print("does not have tax",mre_doc.name)
				journal_doc.append("accounts",{
					"account":"Cash - SSC",
					"credit_in_account_currency":mre_doc.rounded_total,
					"nx_muster_roll_entry":mre_doc.name,
					"project":mre_doc.project
					})
				journal_doc.append("accounts",{
					"account":"NMR Wages - SSC",
					"debit_in_account_currency":mre_doc.rounded_total,
					"nx_muster_roll_entry":mre_doc.name,
					"project":mre_doc.project
					})
				journal_doc.save(ignore_permissions = True)



@frappe.whitelist()
def getExpenseClaimList(filters):
	pyFilter = eval(filters)
	billList = []
	print(billList,pyFilter)
	if pyFilter['expense_claim'] == 1:
		ec = [i.update({'doctype': 'Expense Claim'}) for i in frappe.db.get_list('Expense Claim',{'project':pyFilter["project"],'status': ["in",['Overdue','Unpaid']],'company':pyFilter["company"],'posting_date':["between",[pyFilter['startDate'],pyFilter['endDate']]]},["name","posting_date","total_sanctioned_amount","employee"])]
		print(ec)
		billList.append(ec)
	return billList
