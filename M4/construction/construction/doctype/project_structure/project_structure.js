// Copyright (c) 2021, Nxweb and contributors
// For license information, please see license.txt
frappe.ui.form.on('Project Structure', {
    refresh: function(frm) {

        cur_frm.set_query("project", function() {
            return {
                "filters": [
                    ["Project", "status", "=", "Open"]
                ]
            }
        })


        if (cur_frm.is_new() === 1 && frappe.get_prev_route()[1] === "BOQ") {
            let boq_doc = frappe.model.get_doc("BOQ", frappe.get_prev_route()[2])
            cur_frm.set_value("project", boq_doc.project)
        }
        if (cur_frm.is_new() ===1 && frappe.get_prev_route()[1] === "Labour Progress Entry") {
            let lpe_doc = frappe.model.get_doc("Labour Progress Entry", frappe.get_prev_route()[2])
            cur_frm.set_value("project", lpe_doc.project_name)
        }
        if (cur_frm.is_new() === 1 && frappe.get_prev_route()[1] === "Rate Work Entry") {
            let rwe_doc = frappe.model.get_doc("Rate Work Entry", frappe.get_prev_route()[2])
            cur_frm.set_value("project", rwe_doc.project)
        }
    },

    // Filters for Project Structure
    // is_master: function(frm,doc) { // In Future Enhancement
    // let pro_str = []
    //  frappe.db.get_doc("Project",cur_frm.doc.project).then(doc =>{
    //             doc.project_structure_detail.forEach(i => {
    //                 pro_str.push(i.project_structure)
    //             })
    //         })

    //  cur_frm.fields_dict.project_structure_list.grid.get_field('project_structure').get_query = function(doc,cdt,cdn){
    //         return{
    //             filters:[
    //                ["Project Structure","name","not in",cur_frm.doc.name],
    //                ["Project Structure","name","in",pro_str]
    //             ]
    //         };

    //   };
    //  }

});