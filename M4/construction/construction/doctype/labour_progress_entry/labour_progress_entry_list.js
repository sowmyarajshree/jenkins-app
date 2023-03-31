frappe.listview_settings["Labour Progress Entry"] = {
    add_fields:["status"],
    get_indicator:function(doc){
        if (doc.status === "To Prepared and Bill"){
            return[__("To Prepared and Bill"),"purple",("status,=,To Prepared and Bill")];
        }
        if (doc.status === "To Bill"){
            return[__("To Bill"),"orange",("status,=,To Bill")];
        }
        if (doc.status === "Completed"){
            return[__("Completed"),"green",("status,=,Completed")];
        }
    },
    refresh:function(doc){
    cur_list.page.fields_dict['subcontractor'].get_query =function(doc){
            return{
                filters:[['Supplier','nx_is_sub_contractor','=',1]]
            }
        } 
    cur_list.page.fields_dict['project_name'].get_query =function(doc){
            return{
                filters:[['Project','status','=','Open']]
            }
        } 
    cur_list.page.fields_dict['project_structure'].get_query = function(doc){
            return{
                filters:[
                     ['Project Structure','project','=',cur_list.page.fields_dict.project_name.value]
                ]
            }
         }

   cur_list.page.fields_dict["item_of_work"].get_query = function(doc){
        return{
            filters:[
                    ["Item of Work","project","=",cur_list.page.fields_dict.project_name.value]
                ]
            }
       }

    cur_list.page.fields_dict["task_id"].get_query = function(doc) {
        return {
            filters: [
                ["Task", "project", "=", cur_list.page.fields_dict.project_name.value]
                ]
            }
       }
    }

};