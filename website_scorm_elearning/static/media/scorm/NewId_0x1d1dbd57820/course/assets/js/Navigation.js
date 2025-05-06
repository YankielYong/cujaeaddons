var Navigation = {
	ccLanguage: '',
	icons: {
		doc: 'doc-new.svg',
		pdf: 'pdf-new.svg',
		ppt: 'ppt-new.svg',
		xls: 'xls-new.svg',
		zip: 'zip-new.svg'
	},
	loadPages:function(currentIndex){
		Navigation.lessonLbl = "Lesson";
		clearInterval(Navigation.interval);
		var currentPageObj = Framework.courseArray[currentIndex];
		Framework.currentIndex = currentIndex;
		$('.inner-status-inprogress').removeClass('inner-status-inprogress');
		$('#'+Framework.currentIndex).parent().addClass('inner-status-inprogress');
		$('#'+Framework.currentIndex)[0].scrollIntoView();
		Navigation.tracks = [];
		 
		if(currentPageObj.type == 'video') {
			var videos = currentPageObj.videos[0];
			var lang;
			var index;
			var enObj;
			if(videos.subtitles.length > 0) {
				videos.subtitles = Utils.sortByKeyAscByName(videos.subtitles, 'label');
				for(i=0;i<videos.subtitles.length;i++) {
					if(videos.subtitles[i].lang == 'en') {
						enObj = videos.subtitles[i];
						index = i;
						break;
					} 
				}
				videos.subtitles.splice(index,1);
				videos.subtitles.unshift(enObj);

				for(i=0;i<videos.subtitles.length;i++) {
					lang += `<option value="${videos.subtitles[i].lang}">${videos.subtitles[i].label}</option>`;
					Navigation.tracks.push({
						src:videos.subtitles[i].url,
						kind:'captions',
						srclang:videos.subtitles[i].lang,
						label:videos.subtitles[i].label
					});
				}
	
				$('.js-select').html('<div aria-controls="listbox1" aria-expanded="false" aria-haspopup="listbox" aria-labelledby="combo1-label" id="combo1" class="combo-input" role="combobox" tabindex="0" aria-activedescendant="">Select a Transcript Language</div> <div class="combo-menu" role="listbox" id="listbox1" aria-labelledby="combo1-label" tabindex="-1"> </div>');
	
				const selectEls = document.querySelectorAll('.js-select');
				selectEls.forEach((el) => {
					new Select(el, videos.subtitles);
				});
			} else {
				$('.transcriptbtn').hide();
			}
			
			$('#lesson-video').html('<video-js id="videoPlayer" class="video-js vjs-default-skin vjs-big-play-centered" controls preload="auto">');

			//console.log(tracks);
			if(Navigation.player){
				Navigation.player.dispose();
				$('#lesson-video').html('<video-js id="videoPlayer" class="video-js vjs-default-skin vjs-big-play-centered" controls preload="auto">');
			}
			
			Navigation.player = new videojs('videoPlayer', {
				//fluid: true, 
				tracks: Navigation.tracks,
				poster: videos.thumbnail_url,
				playbackRates: [0.7, 1.0, 1.5, 2.0],
				fill: true,
				responsive: true,
				html5: {
					nativeTextTracks: false
				},
			});
			Navigation.player.src({src: videos.url, type: 'application/x-mpegURL'});
			if(videos.subtitles.length == 0) {
				Navigation.audioSync(Framework.currentIndex, '');
			}
			Navigation.player.on("ended",function() {
				Navigation.lessonCompletion();
			});
			$('.vjs-big-play-button').focus();
		} else {
			clearInterval(Navigation.interval);
			if(currentPageObj.attachments.length > 0) {
				var cyuxml = currentPageObj.attachments[0];
				var cyu = `cyu.html?xml=${cyuxml.url}`;
				var htmlContent = '<iframe allowFullScreen allowTransparency="true" frameborder="0" id="'+ currentPageObj.id +'" mozallowfullscreen src="'+ cyu + '" title="Check Your Understanding" type="text/html" webkitAllowFullScreen width="100%" height="100%"></iframe>';
				View.updateElements("lesson-video",htmlContent);
			}
			
		}
		
		
		if(currentPageObj.type == 'html') {
			Navigation.lessonCompletion();	
		}
		
		Navigation.updateProgressBar();
		$('#pageno').html(Navigation.lessonLbl + " " + (parseInt(Framework.currentIndex) + 1)+" of "+ Framework.courseArray.length);
			
		//Navigation.getTeamsShareUrl();
		if(currentIndex == 0){
			$('#back').addClass('disable').removeClass('enable');
		}else{
			$('#back').removeClass('disable').addClass('enable');
		} 
		
		if(Framework.courseArray.length-1 == Framework.currentIndex){
			Framework.lastPage = true;
			$('#next').addClass('disable').removeClass('enable');
		}else{
			Framework.lastPage = false;
			$('#next').removeClass('disable').addClass('enable');
		}
		Navigation.sendStatus();
		
	},

	transcript: function(){		
		var src;
		for(i=0;i < Navigation.tracks.length;i++) {						
			if(Navigation.tracks[i].srclang == Framework.language) {
				src = Navigation.tracks[i].src;
				break;
			}
		}
		
		$.get(src, function(vttString) {			
			
			var parser = new WebVTT.Parser(window, WebVTT.StringDecoder()),
			cues = [],
			regions = [];
			parser.oncue = function(cue) {
				cues.push(cue);
			};
			parser.onregion = function(region) {
				regions.push(region);
			}
			parser.parse(vttString);
			parser.flush();
			
			var ccText = "";
			for(i=0;i<cues.length;i++){
				ccText += '<span start ="' + cues[i].startTime + '" tabindex="' + (9+i+1) + '" id="cc'+i+'" class="ccspan">' + cues[i].text + '</span>&nbsp;';
			}			
			$('#transcriptText').html(ccText);
			$('.ccspan').click(function(){
				Navigation.seekPlayer($(this).attr('start'));
			});
			
			$('.ccspan').keypress(function(event) {
				if(event.keyCode == 13){
					$(document.activeElement).click();	
				}
			});
			Navigation.audioSync(Framework.currentIndex, cues);
		});

		
	},
	audioSync: function (currentIndex, json) {
		clearInterval(Navigation.interval);
		Navigation.interval = setInterval(function() {
			var currentTime = parseFloat(Navigation.player.currentTime());			
			Navigation.highlightScript(currentTime, json);
		}, 100);
		
	},

	highlightScript: function(currentTime, json) {
		
		if(currentTime > 50 && !$('#'+Framework.currentIndex).hasClass('completed')) {
			Navigation.lessonCompletion();
		}
		for(var j=0; j<json.length; j++) {
			if(parseFloat(json[j].startTime) < parseFloat(currentTime) && parseFloat(json[j].endTime) > parseFloat(currentTime)){
				$('.ccspan').css('background', 'transparent');
				$('#cc'+j).css('background', '#FFF500');
				$('#cc'+j)[0].scrollIntoView();				
			}
		}
	},	
	
	lessonCompletion: function() {
		
		$('#'+Framework.currentIndex).parent().addClass('inner-status-done');
		$('#'+Framework.currentIndex).addClass('completed');
		$('#'+Framework.currentIndex).prev().removeClass('fa-play').removeClass('fa-file-alt').addClass('fa-solid fa-check');
		Framework.courseArray[Framework.currentIndex].PageVisitedStatus = 1;
		Navigation.sendStatus();
	},

	seekPlayer: function(start) {
		Navigation.player.currentTime(start);
	},

	updateProgressBar: function() {
		var percentageText = ((Utils.getCountFromObject(Framework.courseArray, 'PageVisitedStatus', 1))/Framework.courseArray.length)*100;
		$("#progressContainer").circularloader({
			progressPercent: percentageText 
		});
	},

	getCourseInfo: function(progressObj) {
		Framework.progress = progressObj;
		Navigation.loadStructure();
	},

	loadStructure : function(){
		structure = structure.data;
		Framework.courseArray = new Array();
		Framework.language = "en";	
		var icon;
		var lessonNumber;
		var lessonText;
		var coursemap = '<div class="accordion-item"><h2 class="accordion-header" id="headingOne1"><a href="#" class="accordion-button" data-bs-toggle="collapse" data-bs-target="#collapseOne1" aria-expanded="true" aria-controls="collapseOne1"><p class="accordion-no">01</p>Introduction<span class="other-title"></span></a></h2><div id="collapseOne1" class="accordion-collapse collapse show" aria-labelledby="headingOne1" data-bs-parent="#accordion"><div class="accordion-body">';

		document.title = structure.courses.name;
		$('.page-title h1').html(structure.courses.name);	
		Framework.courseName = structure.courses.name;
		//Framework.courseId = structure.courses.id;
		var sections = structure.courses.sections;
		//Framework.courseArray = structure.courses.course_lessons;
		var documents = structure.courses.documents;

		var coursemap = '';
		var lessonCount = 1;
		var videoCount = 1;
		$.each(sections, function (index, section) {
			var lessons = section.course_lessons;
			coursemap += `<div class="accordion-item"><h2 class="accordion-header" id="headingOne${index}"><a href="#" class="accordion-button" data-bs-toggle="collapse" data-bs-target="#collapseOne${index}" aria-expanded="true" aria-controls="collapseOne${index}"><p class="accordion-no">${index+1}</p>${section.title}<span class="other-title">~lesson~ videos</span></a></h2><div id="collapseOne${index}" class="accordion-collapse collapse show" aria-labelledby="headingOne${index}" data-bs-parent="#accordion"><div class="accordion-body">`;
			
			var totalVideoLesson = 0;
			$.each(lessons, function (i, currentPage) {
				Framework.courseArray.push(currentPage);
				var duration = "";
				if(currentPage.name.toLowerCase().indexOf('module') > -1) {
					currentPage.name = currentPage.name.split(':')[1];
				}
				//currentPage.type = 'video';				
				var lessonNumber = videoCount < 10 ? `0${videoCount}` : videoCount;
				if(currentPage.videos.length > 0) {
					icon = 'fa-play';
					lessonText = `Lesson ${lessonNumber}:`;
					currentPage.type = 'video';
					duration = currentPage.videos[0].duration.split(':');
					duration = `${duration[0]} Minutes ${duration[1]} Seconds`;
					videoCount++;
					totalVideoLesson++;
				} else {	
					icon = 'fa-file-alt';
					lessonText = '';
					currentPage.type = 'cyu';
				}
				//var icon = currentPage.videos.length > 0 ? 'fa-play' : 'fa-file-alt';
				coursemap += `<div class="accordion-lesson-list"><i class="lesson fa fas ${icon}"></i><a href="#" id=${lessonCount-1} class="text-black lesson"> ${lessonText} ${currentPage.name}</a><p>${duration}</p></div>`;
				lessonCount++;
			});
			coursemap = coursemap.replace('~lesson~', totalVideoLesson);
			coursemap += '</div></div></div>';
		});
		
		View.updateElements("accordion",coursemap);
		$(".lesson").click(function(){
			Navigation.loadPages($(this).attr('id'));
		});
		var downloads = '';
		var extension;
		$.each(documents, function (i, docs) {
			extension = docs.url.split('.').pop();
			if(extension.charAt(extension.length - 1) == 'x') {
				extension = extension.substr(0, extension.length - 1);
			}
			downloads += `<div class="cm-list"><div class="cm-top download-main"><div class="cm-left download-left"><span><img src="./assets/images/course/icons/${Navigation.icons[extension]}" alt=""></span><div class="uder-download-left"><h6>${docs.name}</h6><p>${docs.description}</p></div></div><div class="cm-right"><a href="${docs.url}" class="launch-btn" target="_blank"><img src="./assets/images/course/icons/Download.svg" alt=""> Download</a></div></div></div>`;
		});
		$('.downloadlist').html(downloads);
		//$('#0').click();
		Navigation.navigation(Framework.progress);
		
	},
	navigation:function(options){
		
		if(options.Lesson_location != "" && options.Lesson_location != null && options.Lesson_location != "undefined"){
			Framework.currentIndex = options.Lesson_location;
			Framework.PageVisitedStatus = options.PageVisitedStatus.split(",")
			$.each( Framework.courseArray, function( index, obj ) {
				let value = Framework.PageVisitedStatus[index];
				
				if(value == undefined || value == null || value == 'undefined') { value= 0; }
 				obj.PageVisitedStatus = value;
				 console.log(value);
			});
			Navigation.markCompletion();
			$("#bookmark").modal("show");
			$('#bookmark_ok').focus();
		}else{
			$('#0').click();
		}
	},

	markCompletion:function(){
		for(i=0;i<Framework.courseArray.length;i++) {
			if(Framework.courseArray[i].PageVisitedStatus == 1) {
				$('#'+i).parent().addClass('inner-status-done');
				$('#'+i).addClass('completed');
				$('#'+i).prev().removeClass('fa-play').removeClass('fa-file-alt').addClass('fa-solid fa-check');
			}
		}
	},
	
	sendStatus:function(){
		Navigation.updateProgressBar();
		var cnt = 0;
		var progress = '';
		for(i=0;i<Framework.courseArray.length;i++){
			progress += Framework.courseArray[i].PageVisitedStatus + ',';
			if(Framework.courseArray[i].PageVisitedStatus == 1){
				cnt++;
			}
		}
		var score = Math.ceil((cnt/Framework.courseArray.length)*100);
		if(cnt ==Framework.courseArray.length){
			Framework.completion = "completed";
		}
		
		if(Framework.mode == "scorm"){
			doLMSSetValue(Framework.completion,Framework.currentIndex, progress,score );
		}else if(Framework.mode == "scorm13"){
		
		}else if(Framework.mode == "tincan"){
			Tincan.putData(Framework.currentIndex,progress);
		}else if(Framework.mode == "teams"){
			Teams.putData(Framework.currentIndex, progress, Framework.completion, score);
		}else{
			Web.set(Framework.currentIndex,progress);
		}
	},
	
	exit:function(){
		if(Framework.mode == "scorm"){
			doLMSFinish();
		}else if(Framework.mode == "scorm13"){
		
		}else if(Framework.mode == "tincan"){
			Tincan.putData();
		}else if(Framework.mode == "teams"){
			Teams.putData(Framework.currentIndex, progress, Framework.completion, score);
		}else{
			Web.set(Framework.currentIndex,progress);
		}
	}

}