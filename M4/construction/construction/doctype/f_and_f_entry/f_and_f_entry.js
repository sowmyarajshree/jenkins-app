/* 
#Parent Filter
1.parent_lwo_filter()
2.lwo_filter()
3.lpe_filter()
4.subcontractor_filter()
5.project_filter()

#Parent Function
1.lwo_read_only()
2.remove_lpe_gif_buttons()
3.lpe_button()
4.button_purchase_invoice()
5.get_lwo(subcontractor, labour_type, is_primary_labour)
6.get_item_button()
7.update_rate_button_fun()
8. glow(frm)
9.dates()
10.labourer()
11.labour_progress_entries()
12. glow_spin(frm)

#Child Table Function F and F Item
1.tot_hrs_calculation()

#Child Table Function Labour Progress Details
1.rate_amt()
2.amt_validation()
3.update_lwo_rate()
4.tot_amt_tot_hrs()
5.child_lwo_filter()
*/

//Parent Filter
function project_filter() {
    cur_frm.set_query("project", function() {
        return {
            "filters": [
                ["Project", "status", "=", "Open"]
            ]
        };
    });
}

function subcontractor_filter() {
    cur_frm.set_query("subcontractor", function() {
        return {
            "filters": {
                "nx_is_sub_contractor": 1
            }
        };
    });
}

function lpe_filter() {
    cur_frm.fields_dict["labour_progress_details"].grid.get_field("labour_progress_entry").get_query = function() {
        return {
            filters: [
                ["Labour Progress Entry", "status", "=", "To Prepared and Bill"],
                ["Labour Progress Entry", "docstatus", "=", 1],
                ["Labour Progress Entry", "labour_type", "=", "F and F"],
                ["Labour Progress Entry", "project_name", "=", cur_frm.doc.project]
            ]
        };
    };
}

function child_lwo_filter() {
    cur_frm.fields_dict["items"].grid.get_field("labour_work_order").get_query = function() {
        return {
            filters: [
                ["Labour Work Order", "project", "=", cur_frm.doc.project],
                ["Labour Work Order", "status", "=", "Active"],
                ["Labour Work Order", "labour_type", "=", "F and F"],

            ]
        };
    };
}

function parent_lwo_filter() {
    cur_frm.set_query("labour_work_order", function(doc) {
        return {
            filters: [
                ["Labour Work Order", "project", "=", cur_frm.doc.project],
                ["Labour Work Order", "status", "=", "Active"],
                ["Labour Work Order", "labour_type", "=", cur_frm.doc.labour_type],
                ["Labour Work Order", "subcontractor", "=", cur_frm.doc.subcontractor]
            ]
        };

    });
}


//Parent Function
function lwo_read_only() {
    if (cur_frm.labour_work_order !== "") {
        cur_frm.fields_dict["items"].grid.update_docfield_property('labour_work_order', 'read_only', 1);

    }
}

function remove_lpe_gif_buttons() {
    if (cur_frm.doc.docstatus === 1) {
        setTimeout(() => {
            cur_frm.remove_custom_button("Labour Progress Entry", "Get Items From");


        }, 10);
    }
}


function lpe_button() {
    if (cur_frm.doc.docstatus !== 1) {
        cur_frm.add_custom_button(__('Labour Progress Entry'),
            function() {
                if (cur_frm.doc.project === undefined) {
                    get_item_glow();
                    frappe.throw("Enter the Project");
                }
                if (cur_frm.doc.subcontractor === undefined) {
                    get_item_glow();
                    frappe.throw("Enter the Subcontractor")
                }
                new frappe.ui.form.MultiSelectDialog({
                    doctype: "Labour Progress Entry",
                    target: cur_frm,
                    setters: {
                        project_name: cur_frm.doc.project,
                        item_of_work: cur_frm.doc.item_of_work,
                        project_structure: cur_frm.doc.project_structure,
                        subcontractor: cur_frm.doc.subcontractor,
                        posting_date: null

                    },
                    add_filters_group: 1,
                    get_query() {
                        return {
                            filters: {
                                docstatus: ["=", 1],
                                status: ["=", "To Prepared and Bill"],
                                labour_type: ["=", "F and F"]
                                //has_measurement_sheet: ["=","Yes"]

                            }
                        };
                    },
                    action(selections) {
                        cur_frm.set_value("labour_progress_details", [])
                        for (let b in selections) {
                            cur_frm.doc.total_hours_lpe = 0;
                            frappe.db.get_doc("Labour Progress Entry", selections[b]).then(doc => {
                                for (let i of doc.working_details) {
                                    cur_frm.set_value("subcontractor", doc.subcontractor)

                                    var child = cur_frm.add_child("labour_progress_details")
                                    child.total_hrs = i.total_working_hours
                                    child.labour_progress_entry = doc.name
                                    child.dates = doc.posting_date
                                    child.item_code = i.labourer
                                    child.is_primary_labour = doc.is_primary_labour
                                    child.project = doc.project
                                    child.project_structure = doc.project_structure
                                    child.hours = i.working_hours
                                    child.no_of_person = i.no_of_person
                                    child.labourer = i.labourer
                                    child.working_details_name = i.name
                                    child.total_quantity = doc.total_qty
                                    child.item_of_work = doc.item_of_work

                                }
                                // Sort child table by dates
                                cur_frm.doc.labour_progress_details = cur_frm.doc.labour_progress_details
                                    .sort((a,b) => (moment(a.dates, "YYYY-MM-DD")-moment(b.dates, "YYYY-MM-DD")));
                                cur_frm.refresh_field('labour_progress_details');
                                console.log("Labour progress details sorted successfully")
                                frappe.ui.hide_open_dialog();
                                get_lwo(subcontractor, labour_type, is_primary_labour)

                            });
                        }
                        cur_frm.refresh_field("labour_progress_details");
                        cur_frm.set_value("items",[]);
                        cur_frm.set_value("total_amount",0);




                    }
                });

                setTimeout(() => {
                    if (cur_dialog && frappe.is_mobile() === false) {
                        if (cur_dialog.title === "Select Labour Progress Entries") {
                            console.log("test")
                            cur_dialog.$wrapper.find('.modal-dialog').css("max-width", "80%");
                        }
                    }
                }, 900)

            }, __("Get From"))

    }

}


function button_purchase_invoice() {
    if (cur_frm.doc.docstatus === 1 && cur_frm.doc.status === "To Bill") {
        cur_frm.add_custom_button("Purchase Invoice", () => {
            frappe.call({
                method: "construction.construction.doctype.f_and_f_entry.f_and_f_entry.create_purchase_invoice",
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
            });
        });
    }
}


function get_lwo(subcontractor, labour_type, is_primary_labour) {
    if (cur_frm.doc.labour_work_order === undefined) {


        frappe.db.get_value("Labour Work Order", {
            "subcontractor": subcontractor,
            "labour_type": labour_type
        }, ["name"]).then(r => {

            cur_frm.set_value('labour_work_order', r.message.name);
            cur_frm.set_value('subcontractor', subcontractor);
            cur_frm.set_value('labour_type', labour_type);
            console.log(r);
        });
    }
}

function get_item_button() {
    if (cur_frm.doc.docstatus !== 1) {
        const att_field = ["labour_attendance", "labourer", "hours_worked", "rate", "amount", "date", "total_person", "labour_work_order"]
        frappe.call({
            method: "construction.construction.doctype.f_and_f_entry.f_and_f_entry.get_labour_attendance",
            args: {
                "lab_att": dates(),
                "project": cur_frm.doc.project,
                "labour_type": cur_frm.doc.labour_type,
                "posting_date": cur_frm.doc.posting_date,
                "subcontractor": cur_frm.doc.subcontractor
            },
            freeze: true,
            callback: function(r) {
                if (r.message) {
                    cur_frm.clear_table("items")
                    $.each(r.message, function(i, d) {
                        var f_and_f_tab = cur_frm.add_child("items")
                        for (let i in d) {
                            if (d[i] && in_list(att_field, i)) {
                                f_and_f_tab[i] = d[i]
                            }
                        }
                    });
                    cur_frm.doc.total_hours = 0
                    cur_frm.doc.items.forEach(i => {
                        cur_frm.doc.total_hours += i.hours_worked
                    })
                    cur_frm.refresh_field("total_hours")
                }
                cur_frm.doc.labour_progress_details = cur_frm.doc.labour_progress_details.sort((a,b) => (moment(a.dates, "YYYY-MM-DD")-moment(b.dates, "YYYY-MM-DD")))
                cur_frm.refresh_field("items")

            }
        })
    }
}

function update_rate_button_fun() {
    if (cur_frm.doc.docstatus !== 1) {
        cur_frm.doc.total_amount = 0;
        cur_frm.doc.items.forEach(i => {
            frappe.xcall("construction.construction.doctype.f_and_f_entry.f_and_f_entry.fetch_labour_work_order_price", {
                "lwo": cur_frm.doc.labour_work_order,
                "labourer": i.labourer,
                "status": "Active"
            }).then(r => {
                if (i.is_machine === 0) {
                    i.rate = r;
                    i.amount = (r / 8) * i.hours_worked;
                    cur_frm.doc.total_amount += i.amount

                    cur_frm.refresh_field('items');
                    cur_frm.refresh_field('total_amount')
                }

            });

        });
    }
}

function glow(frm) {

    cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default').addClass('btn-primary');
    let $add_cls = $('<span class="spinner-grow spinner-grow-sm"></span>');
    cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default').append($add_cls)
    frappe.utils.play_sound('chat-notification');

}

function dates() {
    let dates = []
    cur_frm.doc.labour_progress_details.forEach(i => dates.push(i.dates))
    return dates
}


function labourer() {
    let labourer = []
    cur_frm.doc.items.forEach(i => labourer.push(i.labourer))
    return labourer
}

function labour_progress_entries() {
    let lp_entries = []
    cur_frm.doc.f_and_f_details_update.forEach(i => lp_entries.push(i.labour_attendance))
    return lp_entries
}

function glow_spin(frm) {
    if (cur_frm.doc.total_hours_lpe !== null) {
        cur_frm.fields_dict.get_items.$input_wrapper.find('.btn-default').addClass('btn-primary');
        frappe.utils.play_sound('chat-notification');


    }

}



//#Child Function  Labour Progress Details
function tot_hrs_calculation(frm, cdt, cdn) {
    cur_frm.doc.total_hours_lpe = 0;
    cur_frm.doc.labour_progress_details.forEach(i => {
        cur_frm.doc.total_hours_lpe += i.total_hrs;
    });
    cur_frm.refresh_field("total_hours_lpe");

}

//#Child Function F and F item
function rate_amt(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.is_machine === 1) {
        frappe.xcall("construction.construction.doctype.f_and_f_entry.f_and_f_entry.fetch_labour_work_order_price", {
            "lwo": cur_frm.doc.labour_work_order,
            "labourer": d.labourer,
            "status": "Active"
        }).then(r => {
            d.rate = r
            d.amount = r * d.hours_worked
            cur_frm.refresh_field('items');
        })
    } else {
        frappe.xcall("construction.construction.doctype.f_and_f_entry.f_and_f_entry.fetch_labour_work_order_price", {
            "lwo": cur_frm.doc.labour_work_order,
            "labourer": d.labourer,
            "status": "Active"
        }).then(r => {
            d.rate = r
            d.amount = r / 8 * d.hours_worked
            cur_frm.refresh_field('items');
        })
    }
}

function amt_validation(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.is_machine === 0) {
        frappe.model.set_value(cdt, cdn, "amount", ((d.rate / 8) * d.hours_worked))
    } else {
        frappe.model.set_value(cdt, cdn, "amount", (d.rate * d.hours_worked))

    }
}

function update_lwo_rate() {
    var d = locals[cdt][cdn];
    frappe.call({
        method: "construction.construction.doctype.f_and_f_entry.f_and_f_entry.update_lwo_rate",
        args: {
            "labourer": d.labourer,
            "date": d.date,
            "labour_work_order": d.labour_work_order,
            "project": cur_frm.doc.project || ''
        },
        freeze: true,
        callback: function(r) {
            if (r.message) {
                frappe.speak(r.message)
                frappe.model.set_value(cdt, cdn, "rate", r.message);
            }
            refresh_field('rate');
        }
    });

}

function tot_amt_tot_hrs(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    cur_frm.doc.total_amount = 0
    cur_frm.doc.total_hours = 0
    cur_frm.doc.items.forEach(i => {
        cur_frm.doc.total_amount += i.amount
        cur_frm.doc.total_hours += i.hours_worked
    })
    cur_frm.refresh_field("total_amount")
    cur_frm.refresh_field("total_hours")


}

function set_accounting_period() {
    frappe.db.get_value('Accounting Period', {
        'start_date': ['<=', cur_frm.doc.posting_date],
        'end_date': ['>=', cur_frm.doc.posting_date]
    }, ['name']).then(doc => cur_frm.set_value('accounting_period', doc.message.name));
}

function get_item_glow(frm) {
    cur_frm.fields_dict.get_items.$input_wrapper.find('.dropdown-item').addClass('btn btn-primary');
    frappe.utils.play_sound('alert');
}

frappe.ui.form.on('F and F Entry', {
    setup: function(frm, doc) {
        set_accounting_period();
        subcontractor_filter();
    },
    labour_work_order: function(frm, doc) {
        lwo_read_only();
    },
    refresh: function(frm, doc) {
        cur_frm.refresh_field("labour_progress_details");
        cur_frm.refresh_field("f_and_f_details");
        project_filter();
        remove_lpe_gif_buttons();
        subcontractor_filter();
        set_accounting_period();
        lpe_button();
        button_purchase_invoice();
        lpe_filter();
        child_lwo_filter();
        parent_lwo_filter();

    },
    posting_date: function(frm, doc) {
        set_accounting_period();
    },
    project: function(frm, doc) {
        parent_lwo_filter();
    },
    get_items: function(frm, doc) {
        
        get_item_button();

    },
    update_rate: function(frm, doc) {
        update_rate_button_fun();
        let msg = "Hey your rate is updated successfully";
        const utterance = new SpeechSynthesisUtterance(msg);
        utterance.rate = 1
        utterance.pitch = 1
        utterance.volume = 10
        speechSynthesis.speak(utterance);
        console.log("voice")
    }
});


frappe.ui.form.on('Labour Progress Detail', {
    labour_progress_details_remove: function(frm, cdt, cdn) {
        tot_hrs_calculation(frm, cdt, cdn);
    }
});




frappe.ui.form.on('F and F Item', {
    is_machine: function(frm, cdt, cdn) {
        rate_amt(frm, cdt, cdn);
        amt_validation(frm, cdt, cdn);

    },
    rate: function(frm, cdt, cdn) {
        amt_validation(frm, cdt, cdn);
    },
    hours_worked: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "amount", ((d.rate / 8) * d.hours_worked))
    },
    amount: function(frm, cdt, cdn) {
        cur_frm.doc.total_amount = 0
        cur_frm.doc.items.forEach(i => {
            cur_frm.doc.total_amount += i.amount
        })
        cur_frm.refresh_field("total_amount")
    },
    items_remove: function(frm, cdt, cdn) {
        tot_amt_tot_hrs(frm, cdt, cdn);
    },
    labour_work_order: function(frm, cdt, cdn) {
        update_lwo_rate();
    }
});

//input-with-feedback form-control bold
function get_item_glow(frm) {
    cur_frm.fields_dict.get_items.$input_wrapper.find('.dropdown-item').addClass('btn btn-primary');
    frappe.utils.play_sound('alert');


}