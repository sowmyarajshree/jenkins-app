frappe.listview_settings["Quantity Request"] = {
	refresh: function(frm) {
   cur_list.page.fields_dict['project'].get_query =function(doc){
            return{
                filters:[['Project','status','=','Open']]
            }
        } 
   cur_list.page.fields_dict['project_structure'].get_query = function(doc){
            return{
                filters:[
                     ['Project Structure','project','=',cur_list.page.fields_dict.project.value]
                ]
            }
         }

   cur_list.page.fields_dict["item_of_work"].get_query = function(doc){
        return{
            filters:[
                    ["Item of Work","project","=",cur_list.page.fields_dict.project.value]
                ]
        }

  }

  
}
}