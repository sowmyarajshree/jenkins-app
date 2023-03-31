/*
#Parent Filters
1.Project Filter
2.Accounting Period Filter
3.Subcontractor

#Child Filters
1.labourer

#Parent Function
1.trigger_on_labour_hours()
2.validate_muster_roll()
3.filter_project()
4.button_ot_hours()
5.button_labour_attendance_revision()
6.button_labour_progress_entry()
7.filter_subcontractor()
8.null_subcontractor_labour_details()
9.trigger_on_posting_date()

#Child Function
1.calculate_hrs()

*/
frappe.ui.form.on('Labour Attendance', {
    //Labour Attendance Dublicate Issue
    setup: function(frm, doc) {
        //trigger_on_posting_date();
    },
    validate: function(frm, doc) {
        validate_muster_roll();
        labour_attendance_mandatory();
    },
    refresh: function(frm, doc) {
        filter_project();
        button_ot_hours();
        button_labour_attendance_revision();
        button_labour_progress_entry();
        filter_subcontractor();
        trigger_on_posting_date();
        hide_add_button();
        cur_frm.add_custom_button("What is Next?", () => { 
            let msg = "Hey great Job your next step to update the Labour Progress Entry";
            const utterance = new SpeechSynthesisUtterance(msg);
            utterance.rate = 0.7
            utterance.pitch = 1
            utterance.volume = 10
            window.speechSynthesis.speak(utterance);
            console.log("voice")

        })

    },

    attendance_type: function(frm, doc) {
        null_subcontractor_labour_details();
    },

    total_working_hours: function(frm, doc) {
        trigger_on_labour_hours();
    },
    total_ot_hours: function(frm, doc) {
        trigger_on_labour_hours();
    },
    posting_date: function() {
        trigger_on_posting_date();
    }

});

function validate_muster_roll() {
    if (cur_frm.doc.attendance_type === 'Muster Roll') {
        cur_frm.set_value('subcontractor', null)
    }
}

function filter_project() {
    cur_frm.set_query("project", function() {
        return {
            "filters": [
                ["Project", "status", "=", "Open"]
            ]
        };
    })
}

function button_ot_hours() {
    if (cur_frm.doc.status === "Not Started" && cur_frm.doc.docstatus === 1) {
        cur_frm.add_custom_button("Update OT Hours", () => {
            frappe.call({
                method: "construction.construction.doctype.labour_attendance.labour_attendance.update_ot_hours",
                args: {
                    "docname": cur_frm.doc.name
                },
                freeze: true,
                callback: function(r) {
                    if (!r.exc) {
                        frappe.model.sync(r.message);
                        frappe.set_route("Form", r.message.doctype, r.message.name)
                    }
                }
            });
        }, "Create").addClass("btn-primary");
    }
}

function button_labour_attendance_revision() {
    if (cur_frm.doc.status === "Not Started" && cur_frm.doc.docstatus === 1) {
        cur_frm.add_custom_button("Labour Attendance Revision", () => {
            frappe.call({
                method: "construction.construction.doctype.labour_attendance.labour_attendance.update_labour_att_revision",
                args: {
                    "docname": cur_frm.doc.name
                },
                freeze: true,
                callback: function(r) {
                    if (!r.exc) {
                        frappe.model.sync(r.message);
                        frappe.set_route("Form", r.message.doctype, r.message.name);
                    }
                }
            })
        }, "Create")
    }
}

function button_labour_progress_entry() {
    if (cur_frm.doc.status !== "Completed" && cur_frm.doc.docstatus === 1) {
        cur_frm.add_custom_button("Labour Progress Entry", () => {
            frappe.call({
                method: "construction.construction.doctype.labour_attendance.labour_attendance.create_labour_progress_entry",
                args: {
                    "docname": cur_frm.doc.name
                },
                freeze: true,
                callback: function(r) {
                    if (!r.exc) {
                        frappe.model.sync(r.message);
                        frappe.set_route("Form", r.message.doctype, r.message.name)
                    }
                }
            });
        }, "Create").addClass("btn-primary");
    }
}

function filter_subcontractor() {
    if (cur_frm.doc.subcontractor !== undefined || cur_frm.doc.subcontractor !== "") {
        cur_frm.set_query("subcontractor", function() {
            return {
                "filters": [
                    ["Supplier", "nx_is_sub_contractor", "=", 1]
                ]
            };
        });
    }
}

function null_subcontractor_labour_details() {
    cur_frm.set_value("posting_time", moment(frappe.datetime.now_datetime()).format("HH:mm:ss"))
    if (cur_frm.doc.attendance_type === "Muster Role") {
        frm.set_value("labour_details", null);
        frm.set_value("subcontractor", null);
    }
}

function trigger_on_labour_hours() {
    if (cur_frm.doc.attendance_type === 'Subcontractor') {
        cur_frm.set_value('total_hours', cur_frm.doc.total_working_hours + cur_frm.doc.total_ot_hours);
    }
}

function trigger_on_posting_date(frm, doc) {
    frappe.db.get_value('Accounting Period', {
        'start_date': ['<=', cur_frm.doc.posting_date],
        'end_date': ['>=', cur_frm.doc.posting_date]
    }, ['name']).then(doc => cur_frm.set_value('accounting_period', doc.message.name));
}

frappe.ui.form.on('Labour Detail', {
    qty: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.qty > 0) {
            frappe.db.get_single_value('Construction Settings', 'hours').then(hours => {
                frappe.model.set_value(cdt, cdn, 'working_hours', (d.qty * hours));
                frappe.model.set_value(cdt, cdn, 'sum_of_working_hrs', (d.qty * hours));
            });
        }
    },
    labour_details_add: function(frm, cdt, cdn) {
        calculate_hrs();
    },
    labour_details_remove: function(frm, cdt, cdn) {
        calculate_hrs();
    }
});

function calculate_hrs() {
    if (cur_frm.doc.attendance_type === 'Subcontractor') {
        let total_working_hours = 0;
        let total_ot_hours = 0;
        let total_no_persons = 0;
        cur_frm.doc.labour_details.forEach(i => {
            total_working_hours += i.working_hours;
            total_ot_hours += i.ot_hours;
            total_no_persons += i.qty;
        });
        cur_frm.set_value('total_working_hours', total_working_hours);
        cur_frm.set_value('total_ot_hours', total_ot_hours);
        cur_frm.set_value('total_no_of_persons', total_no_persons);
    }
}


function glow_spin(frm) {
    cur_frm.fields_dict.update_labour_work_order.$input_wrapper.find('.btn-default').addClass('btn-primary');
    frappe.utils.play_sound('chat-notification');
}

function hide_add_button(){
    if (cur_frm.doc.attendance_type == 'Subcontractor'){
        if (cur_frm.doc.docstatus == 0) {
            cur_frm.fields_dict.labour_details.$wrapper.find('.grid-add-row').show();
        } else {
            cur_frm.fields_dict.labour_details.$wrapper.find('.grid-add-row').hide();
        }
    }
    else if (cur_frm.doc.attendance_type == 'Muster Roll'){
        if (cur_frm.doc.docstatus == 0) {
            cur_frm.fields_dict.muster_roll_detail.$wrapper.find('.grid-add-row').show();
        } else {
            cur_frm.fields_dict.muster_roll_detail.$wrapper.find('.grid-add-row').hide();
        }
    }
}
//Validation For Labour Attendance Mandatory// 
function labour_attendance_mandatory(){
    if(cur_frm.doc.attendance_type == 'Muster Roll'){
        if(cur_frm.doc.muster_roll_detail == null){
            frappe.throw("Enter Muster Roll Information")
        }
    }
    if(cur_frm.doc.attendance_type == 'Subcontractor'){
        if(cur_frm.doc.labour_details == null){
            frappe.throw('Enter the Labor Information')
        }
    }
}




