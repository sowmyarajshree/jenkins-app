frappe.listview_settings["BOQ"] = {
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

  
},


	add_fields:["work_status","billing_status"],
	get_indicator:function(doc){
		if (doc.billing_status === "Ordered"  && doc.work_status === "Completed") {
			return[__("Ordered | Completed"),"green","status","=","Ordered | Completed"]
		}

		else if (( doc.billing_status === "Ordered" &&  doc.work_status === "Not Scheduled")) {
			return[__("Ordered | Not Scheduled"),"red","status","=","Ordered | Not Scheduled"]
		}
		else if (( doc.billing_status === "Ordered" &&  doc.work_status === "Scheduled")) {
			return[__("Ordered | Scheduled"),"orange","status","=","Ordered | Scheduled"]
		}


		else if (( doc.billing_status === "To Order" &&  doc.work_status === "Completed")) {
			return[__("To Order | Completed"),"green","status","=","Ordered | Completed"]
		}
		else if (( doc.billing_status === "To Order" &&  doc.work_status === "In Progress")) {
			return[__("To Order | In Progress"),"yellow","status","=","To Order | In Progress"]
		}
		else if (( doc.billing_status === "To Order" &&  doc.work_status === "Scheduled")) {
			return[__("To Order | Scheduled"),"orange","status","=","To Order | Scheduled"]
		}
		else if (( doc.billing_status === "To Order" &&  doc.work_status === "Not Scheduled")) {
			return[__("To Order | Not Scheduled"),"red","status","=","To Order | Not Scheduled"]
		}


		else if (( doc.billing_status === "To Quotation" &&  doc.work_status === "Completed")) {
			return[__("To Quotation | Completed"),"green","status","=","To Quotation | Completed"]
		}
		else if (( doc.billing_status === "To Quotation" &&  doc.work_status === "In Progress")) {
			return[__("To Quotation | In Progress"),"yellow","status","=","To Quotation | In Progress"]
		}
		else if (( doc.billing_status === "To Quotation" &&  doc.work_status === "Scheduled")) {
			return[__("To Quotation | Scheduled"),"orange","status","=","To Quotation | Scheduled"]
		}
		else if (( doc.billing_status === "To Quotation" &&  doc.work_status === "Not Scheduled")) {
			return[__("To Quotation | Not Scheduled"),"red","status","=","To Quotation | Not Scheduled"]
		}

		else if ((doc.billing_status === "Ordered") || (doc.work_status === "In Progress")){
			return[__("Ordered | In Progress"),"yellow","status","=","Ordered | In Progress"]
		}



		else if (( doc.billing_status === "Not Billable" &&  doc.work_status === "Completed")) {
			return[__("Completed"),"green","status","=","Completed"]
		}
		else if (( doc.billing_status === "Not Billable" &&  doc.work_status === "In Progress")) {
			return[__("In Progress"),"yellow","status","=","In Progress"]
		}
		else if (( doc.billing_status === "Not Billable" &&  doc.work_status === "Scheduled")) {
			return[__("Scheduled"),"orange","status","=","Scheduled"]
		}
		else if (( doc.billing_status === "Not Billable" &&  doc.work_status === "Not Scheduled")) {
			return[__("Not Scheduled"),"red","status","=","Not Scheduled"]
		}

		else if ((doc.billing_status === "Not Billable") || (doc.work_status === "In Progress")){
			return[__("In Progress"),"yellow","status","=","In Progress"]
		}
	}
}
