// Copyright (c) 2022, Nxweb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Labour Attendance Tool', {
	refresh: function(frm,doc) {
		//cur_frm.$wrapper.find('.btn-sm').remove()
	    cur_frm.add_custom_button("Create Labour Attendance",() => {
		    //cur_frm.save()
            frappe.call({
                method: 'construction.construction.doctype.labour_attendance_tool.labour_attendance_tool.create_labour_attendance',
                args: {
    	        "project":cur_frm.doc.project,
                "muster_roll_details": cur_frm.doc.muster_roll
                }
            });
        }),
        cur_frm.set_query("project",function(){
            return{
                filters:[["Project","status","=","Open"]]
            }
        })
	}
});
