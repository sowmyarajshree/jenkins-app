frappe.custom_reports["Test report"] = {
	"filters": [
		{
      "fieldname":"company",
			"label": __("Company"),
      "options":"Company",
      "fieldtype": "MultiSelectList",
			 refresh: function(txt) {
				if (!frappe.custom_report.filters) return;

				let company = frappe.custom_report.get_filter_value('company');
				if (!company) return;

				return frappe.db.get_link_option(company, txt);
		}

	]
};

		
