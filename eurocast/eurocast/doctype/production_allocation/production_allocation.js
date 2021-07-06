// Copyright (c) 2020, nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Production Allocation', {
	operation: function(frm,doc) {
		frm.set_query("workstation", function(doc){
	        return {
	                "filters": {
	                    "operation": frm.doc.operation
	            }
	        };
    	});
	}
});
