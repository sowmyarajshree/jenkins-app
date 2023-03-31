import frappe
from frappe import _
from frappe.model.document import Document
from datetime import date
from datetime import timedelta
import pandas as pd



@frappe.whitelist()
def validate_for_account_period():
	frappe.db.sql('''update `tabClosed Document` set closed=1 where name in (select i.name from `tabClosed Document` as i left join `tabAccounting Period` as j on i.parent=j.name where j.end_date < CURDATE())''');
	frappe.db.commit()



	