function Framework(mode){
	Framework.mode = mode;
	Framework.Lesson_location = "";
	Framework.PageVisitedStatus = new Array();
	Framework.completion = "incomplete";
	Framework.currentIndex = 0;
	Framework.protocol = window.location.href.indexOf("https") != -1 ? "https" : "http";
	Framework.ccAvailable = false;
	Framework.format = "old";
	Framework.lastPage = '';
	this.includeFiles(mode);
	//this.initUI();	
}

Framework.prototype.includeFiles = function(mode){
	doLMSInitialize();	
}
