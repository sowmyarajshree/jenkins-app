frappe.listview_settings["Labour Attendance"] = {
    add_fields:["status"],
    get_indicator:function(doc){
        if (doc.status === "Draft"){
            return[__("Draft"),"red",("status,=,Draft")];
        }
        if (doc.status === "Not Started"){
            return[__("Not Started"),"purple",("status,=,Not Started")];
        }
        if (doc.status === "In Progress"){
            return[__("In Progress"),"orange",("status,=,In Progress")];
        }
        if (doc.status === "Completed"){
            return[__("Completed"),"green",("status,=,Completed")];
        }
    },
    refresh:function(doc){
        cur_list.page.fields_dict['project'].get_query =function(doc){
            return{
                filters:[['Project','status','=','Open']]
            }
        }
        cur_list.page.fields_dict['subcontractor'].get_query =function(doc){
            return{
                filters:[['Supplier','nx_is_sub_contractor','=',1]]
            }
        }
    }
};