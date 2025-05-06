var View = {
	
	updateElements:function(container, innerElements){
		$('#'+container).html(innerElements);
	},
	updateInterfaceText: function(textObj) {
		console.log(textObj)
		if(textObj.length > 0) {
			for(i=0; i<textObj.length; i++) {
				var attr = textObj[i].type;
				if(attr === 'lable') {
					$('.' + textObj[i].element).html(textObj[i].value);
				} else {
					$('.' + textObj[i].element).attr(attr, textObj[i].value);
				}
			}
		}
	}
}