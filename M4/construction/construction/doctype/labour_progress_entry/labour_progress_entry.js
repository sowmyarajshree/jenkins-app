/*Setup: Set All Static Filters 
 #Parent Filters
 1.Project Filter
 2.Project Structure Filter
 3.Structure Level Filter
 3.Section Filter
 4.Section Unit Or Section Level Filter
 5.Item Of Work Filter
 6.Task Filter
 7.BOQ Filter
 8.Labour Filter
 9.Labour Attendance Filter
 10.Subcontractor Filter

#childTable1 Filter
1.GRID
2.Dimensional UOM

#childTable2 Filter
1.Laborer Filter
2.Muster Roll Filter
 */


/*
 #Parent Functions
 1.Create Muster Roll Button and Function
 2.Create F And F Button and Function
 3.Create Rate Work Button and Function
 4.Get labourer Button Function
 5.Calculate Total Qty and Validate Total Qty
 6.Calculate Total Working Hours
 7.Calculate Total Steel Qty
 8.Set Accounting period
 9.Set Attendance and Validate Attendance
 10.Update Status and validate Status
 11.Project Trigger Function
 12.Project structure Trigger Function
 13.Structure Level Trigger Function
 13.Level Unit Trigger Functio
 14.Section Trigger Function
 15.Section level Trigger Function
 16.section unit level trigger function
 17.Item Of Work Trigger Function
 18.Labour Type Trigger Function
`19.Posting Date Trigger Function
 20.BOQ Trigger Function
 21.Labour Trigger Function
 22.Setup Functions
 23.Refresh Functions
 23.Validate Functions
 24.validate_has_conversion()
 25.create_grid()
 26.create_task()
 27.for_glow()
 28.get_labour()
 29.level_and_section_filters()
 30.filter_task_in_item_of_work()
 31.apply_labour_filter()
 */


/*
 #Child1 Functions
 1.Calcualte Quantity
 2.Set Quantity UOM
 3.If Conversion Exists make conversion
 4.Add Row Function
 5.Remove Row Fundtion
 6.Length wise calculate qty and set uom
 7.Breadth wise  Calculate qty and set uom
 8.Depth / height wise calculate qty and set uom
 9.Allow to make grid
 
 #Child2 (Working Hours)Functions
 1.set_total_working_hours(frm, cdt, cdn)
 2.set_working_hours(frm, cdt, cdn)

#Child3(BBS Abstart) Functions
 1.validate_get_abstart()
 */




/*Child3 Functions*/

//Parent Filters 
function validate_get_abstart() {
    cur_frm.set_value('bbs_abstract', null);
    cur_frm.doc.bbs_details.uniqBy(i => i.dia_in_mm).forEach(j => {
        var row = cur_frm.add_child("bbs_abstract");
        row.steel_description = j.dia_in_mm;
        if (row.steel_description === "8") {
            row.kg_rm = 0.395 // (8 mm D)^2 /162
        } else if (row.steel_description === "10") {
            row.kg_rm = 0.617 // (10 mm D)^2 /162
        } else if (row.steel_description === "12") {
            row.kg_rm = 0.888 // (12 mm D)^2 /162
        } else if (row.steel_description === "16") {
            row.kg_rm = 1.580 // (16 mm D)^2 /162
        } else if (row.steel_description === "2/0") {
            row.kg_rm = 2.469 // (20 mm D)^2 /162
        } else if (row.steel_description === "25") {
            row.kg_rm = 3.850 // (25 mm D)^2 /162
        } else if (row.steel_description === "32") {
            row.kg_rm = 6.320 // (32 mm D)^2 /162
        }
        cur_frm.doc.total_qty = 0
        cur_frm.doc.total_quantity = 0
        cur_frm.doc.bbs_abstract.forEach(i => {
            i.length = cur_frm.doc.bbs_details.filter(j => j.dia_in_mm === i.steel_description).reduce((sum, q) => {
                return sum + q.total_dia
            }, 0)
            if (i.steel_description === "8") {
                i.weight = 0.395 * i.length // (8 mm D)^2 /162
            } else if (i.steel_description === "10") {
                i.weight = 0.617 * i.length // (10 mm D)^2 /162
            } else if (i.steel_description === "12") {
                i.weight = 0.888 * i.length // (12 mm D)^2 /162
            } else if (i.steel_description === "16") {
                i.weight = 1.580 * i.length // (16 mm D)^2 /162
            } else if (i.steel_description === "20") {
                i.weight = 2.469 * i.length // (20 mm D)^2 /162
            } else if (i.steel_description === "25") {
                i.weight = 3.850 * i.length // (25 mm D)^2 /162
            } else if (i.steel_description === "32") {
                i.weight = 6.320 * i.length // (32 mm D)^2 /162
            }
            cur_frm.doc.total_qty += i.weight
            cur_frm.doc.total_quantity += i.weight
            cur_frm.doc.bbs_abstract.sort((a,b) => Number(a.steel_description) - Number(b.steel_description))
            cur_frm.refresh_field('bbs_abstract');
            cur_frm.refresh_field('total_qty');
            cur_frm.refresh_field('total_quantity');
        });

    });
}

function apply_labour_filter() {
    frappe.db.get_doc('BOQ', cur_frm.doc.boq).then(doc => {
        cur_frm.fields_dict['labour'].get_query = function() {
            console.log('Labour Applied');
            return {
                filters: [
                    ['name', 'in', doc.labour_detail.map(i => i.labour)]
                ]
            };
        };
    });
}

function validate_has_conversion() {
    if (cur_frm.doc.has_conversion === 1) {
        cur_frm.set_value("total_qty", cur_frm.doc.total_quantity / 1000) //1000 kg = 1 tonne     
    } else if (cur_frm.doc.has_conversion === 0) {
        cur_frm.set_value("total_qty", cur_frm.doc.total_quantity) //1000 kg = 1 tonne     
    }
}

function apply_grid_filter() {
    cur_frm.fields_dict.measurement_sheet_detail.grid.get_field("grid").get_query = function() {
        return {
            filters: {
                'project': cur_frm.doc.project_name
            }
        }
    }
}

function apply_grid_filter_bbs_details() {
    cur_frm.fields_dict.bbs_details.grid.get_field("grid").get_query = function() {
        return {
            filters: {
                'project': cur_frm.doc.project_name
            }
        }
    }
}

function apply_dimensional_uom_filter() {
    frappe.db.get_list('UOM Conversion Factor', {
        fields: ['to_uom'],
        filters: {
            category: 'Length'
        },
        pluck: 'to_uom',
        limit: 100
    }).then(records => {
        cur_frm.fields_dict.measurement_sheet_detail.grid.get_field('dimensional_uom').get_query = () => {
            return {
                filters: [
                    ["name", "in", [...records, 'Nos']]
                ]
            };
        };
    });
}

function apply_project_filter() {
    cur_frm.set_query("project_name", function() {
        return {
            "filters": [
                ["Project", "status", "=", "Open"]
            ]
        };
    })
}

function create_grid() {
    //if (cur_frm.doc.has_measurement_sheet === "Yes") {
    cur_frm.add_custom_button("Grid", () => make_multi_grid(), __("Grid"));

    function make_multi_grid() {
        const fields = [{
            label: 'Grid',
            fieldtype: 'Table',
            fieldname: 'items',
            fields: [{
                fieldtype: 'Data',
                fieldname: 'grid_name',
                reqd: 1,
                label: __('Grid Name'),
                in_list_view: 1
            }],
        }]
        var d = new frappe.ui.Dialog({
            title: __('Grid Table'),
            fields: fields,
            primary_action: function() {
                var data = d.get_values("items");
                frappe.call({
                    'method': 'construction.construction.doctype.labour_progress_entry.labour_progress_entry.make_grids',
                    args: {
                        'items': data,
                        'boq_detail': {
                            "project": cur_frm.doc.project_name,
                            "project_structure": cur_frm.doc.project_structure,
                            "item_of_work": cur_frm.doc.item_of_work,
                            "to_uom": cur_frm.doc.uom,
                            "boq": cur_frm.doc.boq
                        }
                    },
                    freeze: true
                });
                d.hide();
            },
            primary_action_label: __('Create')
        });
        d.show();
    }
    //}
}


function create_muster_roll_entry() {
    if (cur_frm.doc.docstatus === 1 && cur_frm.doc.status === "To Prepared and Bill" && cur_frm.doc.labour_type === "Muster Roll") {
        cur_frm.add_custom_button("Muster Roll Entry", () => {
            frappe.call({
                method: "construction.construction.doctype.labour_progress_entry.labour_progress_entry.create_muster_role_entry",
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
        }, "Create");
    }
}

function create_f_and_f_entry() {
    if (cur_frm.doc.docstatus === 1 && cur_frm.doc.status === "To Prepared and Bill" && cur_frm.doc.labour_type === "F and F") {
        cur_frm.add_custom_button("F and F Entry", () => {
            frappe.call({
                method: "construction.construction.doctype.labour_progress_entry.labour_progress_entry.create_f_and_f_entry",
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
        }, "Create");
    }
}

function create_rate_work_entry() {
    if (cur_frm.doc.docstatus === 1 && cur_frm.doc.status === "To Prepared and Bill" && cur_frm.doc.labour_type === "Rate Work") {
        cur_frm.add_custom_button("Rate Work Entry", () => {
            frappe.call({
                method: "construction.construction.doctype.labour_progress_entry.labour_progress_entry.create_rate_work_entry",
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
        }, "Create");
    }
}

function create_task() {
    cur_frm.fields_dict.get_labourer.$input_wrapper.find('.btn-default').addClass('btn-primary');
    if (cur_frm.doc.docstatus === 1) {
        setTimeout(() => {
            cur_frm.remove_custom_button("Task", "Get Items From")
        }, 10)
    }
    cur_frm.refresh_field("measurement_sheet_detail")
    cur_frm.refresh_field("working_details")
}

function apply_item_of_work_filter() {
    cur_frm.set_query("item_of_work", function() {
        return {
            "filters": {
                "project": cur_frm.doc.project_name
            }
        }
    })
}

function subcontractor_filter() {
    cur_frm.set_query("subcontractor", function(doc) {
        return {
            "filters": {
                "nx_is_sub_contractor": 1
            }
        }
    })
}

function apply_project_structure_filter() {
    cur_frm.set_query("project_structure", function(doc) {
        return {
            "filters": {
                "project": cur_frm.doc.project_name
            }
        }
    });
}

function boq_filter() {
    cur_frm.set_query("boq", function(doc) {
        return {
            "filters": {
                "project": cur_frm.doc.project_name,
                "project_structure": cur_frm.doc.project_structure,
                "item_of_work": cur_frm.doc.item_of_work
            }
        }
    })
}

function apply_task_filter() {
    cur_frm.set_query("task_id", function(doc) {
        return {
            "filters": [
                ["Task", "project", "=", cur_frm.doc.project_name]
            ]
        }
    })
}

function maximize_task_field() {
    $(cur_frm.fields_dict.task_id.$wrapper).css('max-width', "100%");
}

function apply_accounting_period() {
    frappe.db.get_value('Accounting Period', {
        'start_date': ['<=', cur_frm.doc.posting_date],
        'end_date': ['>=', cur_frm.doc.posting_date]
    }, ['name']).then(doc => cur_frm.set_value('accounting_period', doc.message.name));
}

function for_glow() {
    if (cur_frm.doc.working_details) {
        let $add_cls = $('<span id ="forbuttons" class="spinner-grow spinner-grow-sm"></span>');
        cur_frm.fields_dict.get_labourer.$input_wrapper.find('.btn-default').addClass('btn-primary');
        //cur_frm.fields_dict.get_labourer.$input_wrapper.find('.btn-default').append($add_cls);
    }
}

function get_labour_details() {
    frappe.utils.play_sound('alert');
    //document.querySelector('#forbuttons').remove();
    const att_field = ["labourer", "muster_roll", "no_of_person", "balance_hours"]
    frappe.call({
        method: "construction.construction.doctype.labour_progress_entry.labour_progress_entry.get_labourer_details",
        args: {
            "project": cur_frm.doc.project_name,
            "posting_date": cur_frm.doc.posting_date,
            "subcontractor": cur_frm.doc.subcontractor || " ",
            "labour_type": cur_frm.doc.labour_type
        },
        freeze: true,
        callback: function(r) {
            if (r.message) {
                cur_frm.clear_table("working_details")
                $.each(r.message, function(i, d) {
                    var f_and_f_tab = cur_frm.add_child("working_details")
                    for (let i in d) {
                        if (d[i] && in_list(att_field, i)) {
                            f_and_f_tab[i] = d[i]
                        }
                    }
                });
            }
            cur_frm.refresh_field("working_details")
        }
    })
    //let $add_cls = $('<span id ="labbuttons" class="spinner-grow spinner-grow-sm"></span>');
    //document.querySelector('#labbuttons').remove();
}

function apply_filter_task_() {
    if (cur_frm.doc.project_structure !== undefined) {
        cur_frm.set_query("task_id", function(doc) {
            return {
                "filters": [
                    ["Task", "project", "=", cur_frm.doc.project_name],
                    ["Task", "nx_project_structure", "=", cur_frm.doc.project_structure]
                ]
            }
        });
    }
    if (cur_frm.doc.project_structure) {
        var level_list = [];
        frappe.db.get_doc('Project Structure', cur_frm.doc.project_structure).then(doc => {
            doc.structure_level_detail.forEach(i => level_list.push(i.structure_level_name))
        })
        cur_frm.fields_dict["structure_level"].get_query = function(doc) {
            return {
                filters: [
                    ["name", "in", level_list]
                ]
            }
        }
    }
}

function level_and_section_filters() {
    if (cur_frm.doc.structure_level) {
        var level_Unit_List = [];
        frappe.db.get_doc("Structure Level", cur_frm.doc.structure_level).then(doc => {
            doc.level_unit_detail.forEach(i => level_Unit_List.push(i.level_unit_name))
        });
        cur_frm.fields_dict["level_unit"].get_query = function(doc) {
            return {
                filters: [
                    ["name", "in", level_Unit_List]
                ]
            };
        };

        var section_list = [];
        frappe.db.get_doc("Structure Level", cur_frm.doc.structure_level).then(doc => {
            doc.section_detail.forEach(i => section_list.push(i.section_name))
        });
        cur_frm.fields_dict["section"].get_query = function() {
            return {
                filters: [
                    ["name", "in", section_list]
                ]
            }
        }
    }
}

function section_unit_filter() {
    if (cur_frm.doc.section) {
        var section_Unit_List = [];
        frappe.db.get_doc("Section", cur_frm.doc.section).then(doc => {
            doc.section_unit_detail.forEach(i => section_Unit_List.push(i.section_unit_name))
        });
        cur_frm.fields_dict["section_unit"].get_query = function() {
            return {
                filters: [
                    ["name", "in", section_Unit_List]
                ]
            }
        }

    }
}

function filter_task_in_item_of_work() {
    if (cur_frm.doc.item_of_work !== undefined) {
        cur_frm.set_query("task_id", function(doc) {
            return {
                "filters": [
                    ["Task", "project", "=", cur_frm.doc.project_name],
                    ["Task", "nx_project_structure", "=", cur_frm.doc.project_structure],
                    ["Task", "nx_item_of_work", "=", cur_frm.doc.item_of_work]
                ]
            }
        });
    }
}

function pri_lab_and_has_sheet_from_boq() {
    frappe.db.get_doc("BOQ", cur_frm.doc.boq).then(doc => {
        let values = {
            'is_primary_labour': '',
            'has_measurement_sheet': ''
        }
        doc.labour_detail.filter(i => {
            if (i.labour === cur_frm.doc.labour) {
                values.is_primary_labour = i.primary_labour;
                values.has_measurement_sheet = i.has_measurement_sheet
            }
        })
        cur_frm.set_value(values)


    })
}

function apply_labourer_filter() {
    cur_frm.fields_dict.working_details.grid.get_field('labourer').get_query = function(doc, cdt, cdn) {
        var d = locals[cdt][cdn];
        return {
            filters: [
                ["Labourer", "name", "in", labourer]
            ]
        };
    }
}

function labourer_detail() {
    frappe.db.get_value("Labour Attendance", {
        "project": cur_frm.doc.project_name,
        "posting_date": cur_frm.doc.posting_date,
        "subcontractor": cur_frm.doc.subcontractor,
        "attendance_type": "Subcontractor"
    }, ["name"]).then(r => {
        let labourer = []
        frappe.db.get_doc("Labour Attendance", r.message.name, filters = null).then(la_doc => {
            console.log(la_doc.name);
            la_doc.labour_details.forEach(i => {
                labourer.push(i.labourer)
            })
        })

        //if(cur_frm.doc.labour){


        //};
    })
}

function apply_labour_filter() {
    if (cur_frm.doc.boq === undefined || cur_frm.doc.boq === '') {
        //frappe.msgprint('Enter BOQ No')
    } else if (cur_frm.doc.boq !== undefined || cur_frm.doc.boq !== '') {
        let labours = []
        frappe.db.get_doc('BOQ', cur_frm.doc.boq).then(doc => {
            doc.labour_detail.forEach(i => labours.push(i.labour))
        })
        console.log(labours)
        cur_frm.fields_dict['labour'].get_query = function(doc) {
            return {
                filters: [
                    // ['nx_labour_applicable_for', '=',"BOQ"],
                    ['name', 'in', labours]
                ]
            }
        }
    };
}

function validate_ledg_balance_qty() {
    frappe.db.get_value("BOQ Ledger", {
        "boq": cur_frm.doc.boq,
        "labour": cur_frm.doc.labour
    }, ["balance_qty"]).then(r => {
        cur_frm.set_value("ledg_balance_qty", r.message.balance_qty);
    })
}

function working_detail_null() {
    if (cur_frm.doc.working_details) {
        cur_frm.set_value("working_details", null);
    }
}

function filter_labour_detail_labour() {
    if (cur_frm.doc.boq === undefined || cur_frm.doc.boq === '') {
        //frappe.msgprint('Enter BOQ No')
    } else if (cur_frm.doc.boq !== undefined || cur_frm.doc.boq !== '') {
        let labours = []
        frappe.db.get_doc('BOQ', cur_frm.doc.boq, filters = null).then(doc => {
            doc.labour_detail.forEach(i => labours.push(i.labour))
        })
        console.log(labours)
        cur_frm.fields_dict['labour'].get_query = function(doc) {
            return {
                filters: [
                    // ['nx_labour_applicable_for', '=',"BOQ"],
                    ['name', 'in', labours]
                ]
            }
        }
    }
}

function get_task_buttton() {
    cur_frm.add_custom_button(__('Task'), function() {
        new frappe.ui.form.MultiSelectDialog({
            doctype: "Task",
            target: cur_frm,
            setters: {
                nx_boq_id: cur_frm.doc.boq,
                project: cur_frm.doc.project_name,
                nx_item_of_work: cur_frm.doc.item_of_work,
                nx_project_structure: cur_frm.doc.project_structure
            },
            get_query() {
                return {
                    filters: {
                        boq_status: ["=", "In Progress" || "Scheduled"]
                    }
                };
            },
            action(selections) {
                for (let b in selections) {
                    frappe.db.get_doc("Task", selections[b]).then(doc => {
                        cur_frm.set_value("task_id", doc.name)
                        cur_frm.set_value("boq", doc.nx_boq_id);
                        cur_frm.set_value("project_name", doc.project)
                        cur_frm.set_value("project_structure", doc.nx_project_structure)
                        cur_frm.set_value("item_of_work", doc.nx_item_of_work)
                        frappe.ui.hide_open_dialog();
                    });
                }
            }
        });
    }, __("Get Items From"));
}
// function sort_dia_in_mm(){
//     if(cur_frm.doc.bbs_details){
//         var d=locals[cdt][cdn];
//         dia_mm=(d.dia_in_mm).sort()
//         if(cur_frm.doc.bbs_abstract){
//             var j=locals[cdt][cdn]
//             frappe.model.set_value(cdt,cdn,"steel_description",dia_mm)
//         }
//     }
// }
frappe.ui.form.on('Labour Progress Entry', {
    get_abstract: function(frm, doc) {
        validate_get_abstart();
        //sort_dia_in_mm();
    },
    labour_type: function(frm, doc) {
        apply_labour_filter();
        working_detail_null();
    },
    boq: function(frm, doc) {
        apply_labour_filter()
    },
    has_conversion: function(frm, doc) {
        validate_has_conversion();
    },
    setup: function(frm, doc) {
        apply_grid_filter();
        apply_dimensional_uom_filter();
        maximize_task_field();
        apply_grid_filter_bbs_details();
    },
    labour: function(frm, doc) {
        if (cur_frm.doc.has_measurement_sheet === "Yes") {
            cur_frm.refresh()

        }

    },
    posting_date: function(frm, doc) {
        apply_accounting_period();
        labourer_detail();
        working_detail_null();
        filter_labour_detail_labour();
    },
    refresh: function(frm, doc) {
        cur_frm.add_custom_button(__('Grid'),
            function() {
                if (cur_frm.doc.project_name === undefined) {

                    frappe.throw("Enter the project")
                }
                new frappe.ui.form.MultiSelectDialog({
                    doctype: "Grid",
                    target: cur_frm,
                    setters: {
                        project: cur_frm.doc.project_name,
                    },

                    add_filters_group: 1,
                    get_query() {
                        return {
                            filters: {
                                docstatus: ["=", 0]
                            }
                        };
                    },
                    action(selections) {
                        cur_frm.set_value("measurement_sheet_detail", [])
                        for (let b in selections) {
                            frappe.db.get_doc("Grid", selections[b]).then(doc => {

                                var child = cur_frm.add_child("measurement_sheet_detail")
                                child.grid = doc.name

                                frappe.ui.hide_open_dialog();
                                cur_frm.refresh_field("measurement_sheet_detail")
                            });
                        }

                        if (cur_frm.doc.measurement_sheet_detail[0].grid === undefined) {
                            cur_frm.get_field("measurement_sheet_detail").grid.grid_rows[0].remove
                        }
                        cur_frm.refresh_field("measurement_sheet_detail")


                    }
                });
                setTimeout(() => {
                    if (cur_dialog && frappe.is_mobile() === false) {
                        if (cur_dialog.title === "Select Grids") {
                            //console.log("test")
                            cur_dialog.$wrapper.find('.modal-dialog').css("max-width", "70%");
                        }
                    }
                }, 900)

            }, __("Get Grid From"));

        if (cur_frm.is_new() === 1 && frappe.get_prev_route()[1] === "Rate Work Entry") {
            let rwe_doc = frappe.model.get_doc("Rate Work Entry", frappe.get_prev_route()[2])
            cur_frm.set_value("project_name", rwe_doc.project)
        };
        if (cur_frm.is_new() === 1 && frappe.get_prev_route()[1] === "Muster Roll Entry") {
            let mre_doc = frappe.model.get_doc("Muster Roll Entry", frappe.get_prev_route()[2])
            cur_frm.set_value("project_name", mre_doc.project)
        }


        apply_project_filter();
        create_grid();
        create_muster_roll_entry();
        create_f_and_f_entry();
        create_rate_work_entry();
        create_task();
        apply_item_of_work_filter();
        subcontractor_filter();
        apply_project_structure_filter();
        boq_filter();
        apply_task_filter();
        apply_accounting_period();
        //get_task_buttton();
        apply_filter_task_();

    },
    has_measurement_sheet: function(frm, doc) {
        for_glow();

    },
    get_labourer: function(frm, doc) {
        get_labour_details();
    },
    project_name: function(frm, doc) {
        apply_task_filter();
        if (cur_frm.doc.project_name === null || cur_frm.doc.project_name === undefined || cur_frm.doc.project_name === ""){
            cur_frm.set_value("project_structure",null)
            cur_frm.set_value("item_of_work",null)
        }
    },
    project_structure: function(frm, doc) {
        apply_filter_task_();

    },

    structure_level: function(frm, doc) {
        level_and_section_filters();
        section_unit_filter();
    },

    item_of_work: function(frm, doc) {
        filter_task_in_item_of_work();
    },
    labour: function(frm, doc) {


        let $add_cls = $('<span id ="forbuttons" class="spinner-grow spinner-grow-sm"></span>');
        cur_frm.fields_dict.get_labourer.$input_wrapper.find('.btn-default').addClass('btn-primary');
        frappe.db.get_value("BOQ Ledger", {
            "boq": cur_frm.doc.boq,
            "labour": cur_frm.doc.labour
        }, ["balance_qty"]).then(r => {
            cur_frm.set_value("ledg_balance_qty", r.message.balance_qty);
        });


        pri_lab_and_has_sheet_from_boq();
        apply_labourer_filter();;
        labourer_detail();
        create_grid();
    },
    subcontractor: function(frm, doc) {

        apply_labour_filter();
        labourer_detail();
    },
    muster_role: function(frm, doc) {
        apply_labour_filter();
    },
    validate: function(frm, doc) {
        validate_ledg_balance_qty();
    },
    hours_lpe: function(frm, doc) {
        cur_frm.set_value("total_lpe_hours", (cur_frm.doc.hours_lpe)) //removed ot_hours
    },
    ot_hours: function(frm, doc) {
        cur_frm.set_value("total_lpe_hours", (cur_frm.doc.hours_lpe)) //removed ot_hours
    },
    steel_reinforcement: function(frm, doc) {
        if (cur_frm.doc.steel_reinforcement === 1) {
            cur_frm.set_value("measurement_sheet_detail", null)
            cur_frm.set_value("total_qty", null)
        }
    }

});
frappe.ui.form.on('Measurement Sheet Detail', {
    no: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.breadth && d.no && d.length_wise && d.depth_height) {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.length_wise * d.breadth * d.depth_height));
        } else if (d.no !== 0) {
            frappe.model.set_value(cdt, cdn, "quantity", d.no);
        }
        if (d.no === 0) {
            frappe.model.set_value(cdt, cdn, "quantity", d.length_wise * d.breadth * d.depth_height);
        }
    },
    length_wise: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.breadth && d.no && d.length_wise && d.depth_height) {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.length_wise * d.breadth * d.depth_height));
        } else if (d.length_wise !== 0) {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.length_wise));
        } else {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.breadth * d.depth_height));
        }
    },
    breadth: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.breadth && d.no && d.length_wise && d.depth_height) {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.length_wise * d.breadth * d.depth_height));
        } else if (d.breadth !== 0) {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.length_wise * d.breadth));
        } else {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.length_wise * d.depth_height));
        }
    },
    depth_height: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        if (d.depth_height !== 0) {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.length_wise * d.breadth * d.depth_height));
        } else if (d.depth_height !== 0 && d.breadth === 0) {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.length_wise * d.depth_height));
        } else if (d.depth_height !== 0 && d.length_wise === 0) {
            frappe.model.set_value(cdt, cdn, "quantity", (d.no * d.breadth * d.depth_height));
        }
    },
    quantity: function(frm, cdt, cdn) {
        cur_frm.doc.total_qty = 0;
        $.each(cur_frm.doc["measurement_sheet_detail"] || [], function(i, item) {
            cur_frm.doc.total_qty += item.quantity;
        });
        refresh_field("total_qty");
    }
});


function conversion_factor(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.dimensional_uom !== 'Nos' && d.length_wise && d.breadth === 0 && d.depth_height === 0) {
        frappe.model.set_value(cdt, cdn, 'quantity', (d.no * d.length_wise));
        frappe.model.set_value(cdt, cdn, 'uom', d.dimensional_uom);
    } else if (d.dimensional_uom !== 'Nos' && d.length_wise && d.breadth && d.depth_height === 0) {
        frappe.model.set_value(cdt, cdn, 'quantity', (d.no * d.length_wise * d.breadth));
        frappe.model.set_value(cdt, cdn, 'uom', ("Square" + " " + d.dimensional_uom));
    } else if (d.dimensional_uom !== 'Nos' && d.length_wise && d.breadth && d.depth_height) {
        frappe.model.set_value(cdt, cdn, 'quantity', (d.no * d.length_wise * d.breadth * d.depth_height));
        frappe.model.set_value(cdt, cdn, 'uom', ("Cubic" + " " + d.dimensional_uom));
    } else {
        frappe.model.set_value(cdt, cdn, 'quantity', (d.no));
        frappe.model.set_value(cdt, cdn, 'uom', 'Nos');
        frappe.model.set_value(cdt, cdn, 'length_wise', 0);
        frappe.model.set_value(cdt, cdn, 'breadth', 0);
        frappe.model.set_value(cdt, cdn, 'depth_height', 0);
    }


}

function qty_conversion(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    frappe.xcall('construction.construction.doctype.boq.boq.type_converter', {
        'value': d.quantity,
        'from_uom': d.uom,
        'to_uom': d.converted_uom,
        'tk_value': d.depth_height,
        'tk_uom': d.dimensional_uom,
        'w_value': d.breadth,
        'w_uom': d.dimensional_uom
    }).then(r => {
        console.log('type_conversion')
        frappe.model.set_value(cdt, cdn, 'converted_qty', r)
    })

}
frappe.ui.form.on('Measurement Sheet Detail', {
    length_wise: function(frm, cdt, cdn) {
        conversion_factor(frm, cdt, cdn);

    },
    breadth: function(frm, cdt, cdn) {
        conversion_factor(frm, cdt, cdn);
    },
    depth_height: function(frm, cdt, cdn) {
        conversion_factor(frm, cdt, cdn);
    },
    no: function(frm, cdt, cdn) {
        conversion_factor(frm, cdt, cdn);
    },
    dimensional_uom: function(frm, cdt, cdn) {
        conversion_factor(frm, cdt, cdn);
    },
    converted_uom: function(frm, cdt, cdn) {
        qty_conversion(frm, cdt, cdn);

    }
});
frappe.ui.form.on('Measurement Sheet Detail', {
    measurement_sheet_detail_remove: function(frm, cdt, cdn) {
        cur_frm.doc.total_qty = 0;
        $.each(cur_frm.doc["measurement_sheet_detail"] || [], function(i, item) {
            cur_frm.doc.total_qty += item.quantity;
        });
        refresh_field("total_qty");
    }
});
frappe.ui.form.on('Working Detail', {
    no_of_person: function(frm, cdt, cdn) {
        set_total_working_hours(frm, cdt, cdn);
    },
    working_hours: function(frm, cdt, cdn) {
        set_total_working_hours(frm, cdt, cdn);
    },
    total_working_hours: function(frm, cdt, cdn) {
        set_working_hours(frm, cdt, cdn);
    },
    working_details_remove: function(frm, cdt, cdn) {
        set_working_hours(frm, cdt, cdn);
    }

});

function set_total_working_hours(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "total_working_hours", (d.no_of_person * d.working_hours))
}

function set_working_hours(frm, cdt, cdn) {
    cur_frm.doc.lpe_total_hours = 0
    cur_frm.doc.working_details.forEach(i => {
        cur_frm.doc.lpe_total_hours += i.total_working_hours
    })
    cur_frm.refresh_field("lpe_total_hours")
}
//calculation for Steel Reinforcement//
frappe.ui.form.on("BBS Details", {
    nos: function(frm, cdt, cdn) {
        conversion_type_meter(frm, cdt, cdn);
    },
    cutting_length: function(frm, cdt, cdn) {
        conversion_type_meter(frm, cdt, cdn);
    },
    member: function(frm, cdt, cdn) {
        conversion_type_meter(frm, cdt, cdn);
    },
    conversion_type: function(frm, cdt, cdn) {
        conversion_feet_and_meter(frm, cdt, cdn);
    },
    bbs_details_add: function(frm, cdt, cdn) {
        conversion_type(frm, cdt, cdn);
    }
});

function conversion_type_meter(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.conversion_type === "Meter") {
        frappe.model.set_value(cdt, cdn, "total_dia", d.member * d.nos * d.cutting_length)
    } else {
        frappe.model.set_value(cdt, cdn, "total_dia", (d.member * d.nos * d.cutting_length) / 3.28)
    }
}

function conversion_feet_and_meter(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    if (d.conversion_type === "Feet") {
        frappe.model.set_value(cdt, cdn, "total_dia", d.total_dia / 3.28) // 1 m = 3.28 feet
        frappe.model.set_value(cdt, cdn, "total_length_uom", "feet")
        frappe.model.set_value(cdt, cdn, "cutting_length_uom", "feet")
    } else if (d.conversion_type === "Meter") {
        frappe.model.set_value(cdt, cdn, "total_dia", d.member * d.nos * d.cutting_length)
        frappe.model.set_value(cdt, cdn, "total_length_uom", "Meter")
        frappe.model.set_value(cdt, cdn, "cutting_length_uom", "Meter")
    }
}

function conversion_type(frm, cdt, cdn) {
    if (cur_frm.doc.conversion_type) {
        var d = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "conversion_type", cur_frm.doc.conversion_type)
    }
}
