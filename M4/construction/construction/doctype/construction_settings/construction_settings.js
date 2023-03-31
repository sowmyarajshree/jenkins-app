frappe.ui.form.on('Construction Settings', {
	    refresh: function(frm,doc){
	    	cur_frm.set_query('f_and_f_item',function(){
	    		return{
	    			"filters":{'disabled':0}
	    			
	    		}
	    	}),
	    	cur_frm.set_query('rate_work_item',function(){
	    		return{
	    			"filters":{'disabled':0}
	    		}
	    	})

            cur_frm.fields_dict.labour_item.get_query = function(doc) {
			    return{
		            filters:[
			            ['nx_is_labour', '=', '1']
			        
		            ]
			    };
	       }
        }

    
});


frappe.ui.form.on('Construction Settings',{
	generate_acc_period:function(frm,doc){
	frappe.prompt([
			{
        		label:'Start Date',
        		fieldname:'start_date',
        		fieldtype:'Date',
        		reqd:1
        	},
        	{
        		label:'',
        		fieldname:'column_break',
        		fieldtype:"Column Break"
        	},
        	{
        		label:'End Date',
        		fieldname:'end_date',
        		fieldtype:'Date',
        		reqd:1
        	}
	],
	(values)=>{
		let st_date = values.start_date
		let ed_date= values.end_date
		frappe.xcall(
			      'construction.construction.doctype.construction_settings.construction_settings.make_acc_date',
        			{
        				'start':st_date,
        				'end':ed_date,
        				'open_day':cur_frm.doc.account_period_open_day,
        				'period':cur_frm.doc.period
        			})
	})
   }
})