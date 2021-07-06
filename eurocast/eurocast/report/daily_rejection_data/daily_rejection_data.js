frappe.query_reports["Daily Rejection Data"] = {
      "filters": [
           {
              "fieldname":"from_date",
              "label":("From Date"),
              "fieldtype":"Date",
              "default":get_today(),
             "reqd":1
          },
           {
              "fieldname":"to_date",
              "label":("To Date"),
              "fieldtype":"Date",
              "default":get_today(),
             "reqd":1
          }
]
}
