/*
#Parent Trigger
1.refresh
2.get_attendance_details
3.labour_attendance


#Child Trigger OT Labour Detail
1.no_of_person
2.ot_hours

#Parent Function
1.project_filter
2.labour_attendace
3.remove_add_row()

#button function
1.get_attendance_details
#Child Function 
1.validate_labour_hours(frm,cdt,cdn)

*/
function subcontractor_filter() {
    cur_frm.set_query("subcontractor", function(doc) {
        return {
            "filters": {
                "nx_is_sub_contractor": 1
            }
        }
    })
}

function validate_labour_hours(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (cur_frm.doc.attendance_type == "Subcontractor") {
        frappe.model.set_value(cdt, cdn, "total_ot_hours", (d.no_of_person * d.ot_hours));
    } else if (cur_frm.doc.attendance_type == "Muster Roll") {
        frappe.model.set_value(cdt, cdn, "total_ot_hours", d.ot_hours);
    }
}

function project_filter() {
    cur_frm.set_query("project", function() {
        return {
            "filters": [
                ["Project", "status", "=", "Open"]
            ]
        };
    });
}

function labour_attendace() {
    cur_frm.set_query("labour_attendance", function() {
        return {
            filters: [
                ["Labour Attendance", "project", "=", cur_frm.doc.project]
            ]
        }
    });
}

function get_labour_attendance_details() {
    const set_fields = ["muster_roll", "labourer", "no_of_person", "ot_hours", "total_ot_hours"];
    frappe.call({
        method: "construction.construction.doctype.labour_ot_entry.labour_ot_entry.update_ot_details",
        args: {
            "labour_attendance": cur_frm.doc.labour_attendance,
        },
        freeze: true,
        callback: function(r) {
            if (r.message) {
                cur_frm.set_value("ot_details", []);
                $.each(r.message, function(i, d) {
                    var ot_detail = cur_frm.add_child('ot_details');
                    for (let key in d) {
                        if (d[key] && in_list(set_fields, key)) {
                            ot_detail[key] = d[key];
                        }
                    }
                });
                cur_frm.refresh_field('ot_details');
            }
        }
    });
}

function remove_add_row() {
    if (cur_frm.doc.attendance_type !== "Subcontractor") {
        cur_frm.get_field("ot_details").grid.wrapper.find(".grid-add-row").remove();
        cur_frm.refresh_field('ot_details');
    }

}

function labourer_filter() {
    if (cur_frm.doc.attendance_type === "Subcontractor") {
        let labourer = []
        frappe.db.get_doc("Labour Attendance", cur_frm.doc.labour_attendance).then(lab_att => {
            lab_att.labour_details.forEach(i => {
                labourer.push(i.labourer)
            })
        })
        cur_frm.fields_dict.ot_details.grid.get_field('labourer').get_query = function() {
            return {
                filters: [
                    ['Labourer', 'name', 'in', labourer]
                ]
            }
        }
    }
}

function ot_total_hours_calculation(frm, cdt, cdn) {
    let total_ot_hours = 0;
    cur_frm.doc.ot_details.forEach(i => {
        total_ot_hours += i.total_ot_hours;
    });
    cur_frm.set_value('total_ot_hours', total_ot_hours);
}




frappe.ui.form.on('Labour OT Entry', {
    refresh: function(frm, doc) {
        project_filter();
        labour_attendace();
        labourer_filter();
        subcontractor_filter();
    },
    //Muster Roll Modification.
    get_attendance_details: function(frm, doc) {
        get_labour_attendance_details();
        labourer_filter();

    },
    labour_attendance: function(frm, doc) {
        cur_frm.set_value("ot_details", null);
    }
});




//Muster Roll Modification
frappe.ui.form.on('OT Labour Detail', {
    no_of_person: function(frm, cdt, cdn) {
        validate_labour_hours(frm, cdt, cdn);
    },
    ot_hours: function(frm, cdt, cdn) {
        validate_labour_hours(frm, cdt, cdn);
    },
    total_ot_hours: function(frm, cdt, cdn) {
        ot_total_hours_calculation(frm, cdt, cdn)
    },
    ot_details_remove: function(frm, cdt, cdn) {
        ot_total_hours_calculation(frm, cdt, cdn)
    }

});