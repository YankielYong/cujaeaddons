$(document).ready(function(){

	function progresswrap() {
        var progressPath = document.querySelector('.progress-wrap path');
        var pathLength = progressPath.getTotalLength();
        progressPath.style.transition = progressPath.style.WebkitTransition = 'none';
        progressPath.style.strokeDasharray = pathLength + ' ' + pathLength;
        progressPath.style.strokeDashoffset = pathLength;
        progressPath.getBoundingClientRect();
        progressPath.style.transition = progressPath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';
        var updateProgress = function() {
            var scroll = $(window).scrollTop();
            var height = $(document).height() - $(window).height();
            var progress = pathLength - (scroll * pathLength / height);
            progressPath.style.strokeDashoffset = progress;
        }
        updateProgress();
        $(window).scroll(updateProgress);
        var offset = 50;
        var duration = 550;
        jQuery(window).on('scroll', function() {
            if (jQuery(this).scrollTop() > offset) {
                jQuery('.progress-wrap').addClass('active-progress');
            } else {
                jQuery('.progress-wrap').removeClass('active-progress');
            }
        });
        jQuery('.progress-wrap').on('click', function(event) {
            event.preventDefault();
            jQuery('html, body').animate({ scrollTop: 0 }, duration);
            return false;
        })
    }
    progresswrap();

    // lv-toggle-button
    if ($('.lv-toggle-button').length) { 
       $('.lv-toggle-button').click(function(){
            $('.lv-main').toggleClass('sidebar-close');
            $(this).toggleClass('lv-toggle-colose')
        }); 
    } 

    // lv-tabs
    if ($('.lv-tabs').length) { 
        $('.lv-tabs-list li a').on('click', function() {
            var dashboard_menu_type = $(this).attr('data-bind');
            $('.lv-tabs-data-list').hide();
            $('.lv-tabs-list li a').removeClass('lv-tabs-list-active');
            $('#' + dashboard_menu_type).show();
            $(this).addClass('lv-tabs-list-active');
        });
    }

    // mobile-hunger
    if ($('.mobile-hunger').length) { 
		$('.mobile-hunger').keypress(function(event) {			
			if(event.keyCode == 13 || event.keyCode == 32){
				$('.mobile-hunger').click();
			}
		});
        $('.mobile-hunger').click(function(){
			$('.header-icon').toggleClass('mobile-show');
			if($('.header-icon').hasClass('mobile-show')) {
				$(this).attr('aria-label', 'Close Mobile View Panel');
				$(this).attr('aria-expanded','true');
			} else {
				$(this).attr('aria-label', 'Open Mobile View Panel');
				$(this).attr('aria-expanded','false');
			}
			
            
         }); 
    }
 
    $('.feedback-close').click(function(){
        $('.lq-1').hide();
        $('.lq-2').show();
     }); 

    // checkWidth
    function checkWidth() {

        if ($(window).width() < 991) {
            $('.lv-main').addClass('sidebar-close');
            $('.lv-toggle-button').addClass('lv-toggle-colose');
        } else {
            $('.lv-main').removeClass('sidebar-close');
            $('.lv-toggle-button').removeClass('lv-toggle-colose');
        }
    }
    checkWidth();

    // changes src
    function changessrc() {
        if ($(window).width() < 1199) { 
            $('.brand-logo .logo a img').attr("src", "assets/images/logo-icon.png");
        } else { 
            $('.brand-logo .logo a img').attr("src", "assets/images/logo.png");
        }
    }
    changessrc();
    
    var skillPers = document.querySelectorAll(".skill-per");
    skillPers.forEach(function (skillPer) {
        var per = parseFloat(skillPer.getAttribute("per"));
        skillPer.style.width = per + "%";

        var animatedValue = 0;
        var startTime = null;

        function animate(timestamp) {
            if (!startTime) startTime = timestamp;
            var progress = timestamp - startTime;
            var stepPercentage = progress / 1000; // Dividing by duration in milliseconds (1000ms = 1s)

            if (stepPercentage < 1) {
                animatedValue = per * stepPercentage;
                skillPer.setAttribute("per", Math.floor(animatedValue) + "%");
                requestAnimationFrame(animate);
            } else {
                animatedValue = per;
                skillPer.setAttribute("per", Math.floor(animatedValue) + "%");
            }
        }

        requestAnimationFrame(animate);
    });

	$("#language-select").change(function() {
		Framework.language = $('select[name=language-select]').val();
		console.log(Framework.language);
		Navigation.transcript(Framework.videoId);
	});
	
	
    /*------------------------------------------------------------------------------------------------------- 
       ### When document is Scrollig, do ###
    -------------------------------------------------------------------------------------------------------*/
    $(window).on('scroll', function() { 
    });

    /*------------------------------------------------------------------------------------------------------- 
       ### When document is loaded, do ###
    -------------------------------------------------------------------------------------------------------*/ 
    $(window).on('load', function() { 
    });

    /*------------------------------------------------------------------------------------------------------- 
       ### When document is loaded, do ###
    -------------------------------------------------------------------------------------------------------*/ 
    $(window).resize(function(){
        checkWidth();         
        changessrc();         
    });
	$('#downloadLink').tipsy({gravity: 'n'});
	$('#share, #dripfeed-button, #dripfeed-button').tipsy({gravity: 'e'});

	var mode = Utils.urlQueryString("type",document.location.search);
	
	if(mode == null){
		mode = "wbt";
	}
	new Framework(mode);
	Framework.courseId = courseId;
	
	$(window).bind('beforeunload', function () {
		Navigation.exit();
		 window.opener.hide();
	});
	
	$(document).keypress(function(event) {
		if(event.keyCode == 13){
			$(document.activeElement).click();	
		}
	});

	function changeButtonTabOrder(start, tabIndex){
		for(i=start;i<interfacesButtons.length;i++){
			$('#'+interfacesButtons[i]).attr('tabIndex', ++tabIndex);
		}
	}

	$('#downloadLink').click(function(){
		$("#downloads").modal("show");
		$('.launch-btn')[0].focus();
	});
	$('.download-close').click(function(){
		$("#downloads").modal("hide");
		$('.course-downloads').focus();
	});
	$('#coursemapbtn').click(function(){
		$('#transcriptContainer, #searchContainer').hide();
		$('.mainbuttons').removeClass('active');

		var totalPages = $('.link').length;
		if(!$(this).hasClass('active')){
			$(this).addClass('active');
			$('.link').each(function(i) { 
				$(this).attr("tabIndex",(2+i));
			});
			changeButtonTabOrder(1, totalPages+1);
		}
		if($(window).width() < 981) {
			$('#coursemapContainer').toggle();
		}else {
			$('#coursemapContainer').show();
		}
	});

	$('#transcriptbtn').click(function(){
		
		$('#coursemapContainer, #searchContainer').hide();
		$('.mainbuttons').removeClass('active');

		$("#transcriptContainer, #transcript").show();
		if(!$(this).hasClass('active')){
			$(this).addClass('active');
		} 
	});
	
	$('#search_btn').click(function(){
		$('#coursemapContainer, #transcriptContainer').hide();
		$('.mainbuttons').removeClass('active');
		$('#searchContainer').show();
		$(this).addClass('active');		
	});

	$('#share').click(function(){	
		const lesson = Framework.courseArray[Framework.currentIndex].displayText;
		$('#lessonInfo').html(`${lesson} from Course ${Framework.courseName}.`);
		$('.copylink-textbox').val(Framework.shareLessonUrl);
		$('#toEmail').val('');
		$('#sharemessage').val('')
		$('.teams-share-button').html('Share in Teams');
		$('.share-success').hide();
		$("#share-lesson").modal("show");
		$("#toEmail").focus();
		/*$('#disabler').show();
		$('#share-container').show();*/
	});

	$('#back').click(function(){	
		if(!$(this).hasClass('disable')){
			if(Framework.currentIndex > 0){
				Framework.currentIndex--;
				$('#'+Framework.currentIndex).click();
			}
		}
	});
	
	$('#next').click(function(){
		if(!$(this).hasClass('disable')){
			if(Framework.courseArray.length > Framework.currentIndex-1){
				Framework.currentIndex++;
				$('#'+Framework.currentIndex).click();			
			}
		}
	});
	
	$('#Search_txt').focus(function() {
		$(this).val("");
	});
	
	$("#Search_txt").keyup(function(event) {
		if($(this).val() !='') {
			$('#lessons, #transcript').hide();
			$('.lv-tabs-list li a').removeClass('lv-tabs-list-active');
			$('#search').show();
			var cnt = 0;
			var searchText = $('#Search_txt').val().toLowerCase();
			var lessonNumber, icon, currentPage, tempText;
			$('#search').html("");
			$('#coursemapContainer').hide();

			for(i=0;i<Framework.courseArray.length;i++) {
				currentPage = Framework.courseArray[i];
				tempText = currentPage.name.toLowerCase();
				if(tempText.indexOf(searchText) != -1){
					cnt++;
					lessonNumber = i+1;
					lessonNumber = i < 9 ? `0${lessonNumber}` : lessonNumber;
					icon = currentPage.type == 'video' ? 'fa-play' : 'fa-file-alt';
				
					if(currentPage.name.toLowerCase().indexOf('module') > -1) {
						currentPage.name = currentPage.name.split(':')[1];
					}
					$('#search').append(`<div role="list" class="accordion-lesson-list"><i class="fa fas ${icon}"></i><a tabIndex="0" role="listitem" href="#" id=${i} class="text-black search-lesson search-lesson-${i}" role="">Lesson ${lessonNumber}: ${currentPage.name}</a><p></p></div>`);
					$('#search').addClass('lv-tabs-data-active');
					
					$('.search-lesson').click(function(){
						$('#search').hide();	
						$('#lessons').show();
						Navigation.loadPages($(this).attr('id'));
						
					});
				}
			}
			//changeButtonTabOrder(3, 3+cnt+1);
			$('#search').attr("role","alert");
			$('#search').attr("aria-label","Search Result for " + $("#Search_txt").val());
			//$('.search-lesson-0').focus();
			if(cnt == 0){
				$('#searchLinkHolder').html("<span class='noresult'>No result found.</span>");
			}
		}
	});
	$('#searchClose').click(function(){
		$('#searchContainer').slideToggle();
	});
	
	$('#bookmark_ok').click(function(){
		$('#'+Framework.currentIndex).click();
		$('#disabler').hide();
		$('#bookmark_container').hide();
	});
	$('#bookmark_cancel').click(function(){
		$('#disabler').hide();
		$('#bookmark_container').hide();
		Framework.currentIndex = 0;
		$('#'+Framework.currentIndex).click();
	});

	$('#container_close').click(function() {
		$('#playerContainer').animate({"width":"99%"}, "slow");
		$('#otherContent').animate({"right":"-500px"}, "slow", function() {
			$( "#container_show" ).show( "slow", function() {});
		});
	});

	$('#container_show').click(function() {
		$(this).hide( "slow", function() {});
		$('#playerContainer').animate({"width":"75%"}, "slow");
		$('#otherContent').animate({"right":"0px"}, "slow");
	});
	
	$('#cc_btn').click(function(){
		if($("#transcript").is(":visible")){
			$("#transcript").hide();
			$("#player").css('width', '99%');
		}else{
			$("#player").css('width', '80%');
			$("#transcript").show();
		}
	});
	
	$("#switch").click(function(){
		if($('#switch').is(':checked')){
			$("#transcriptContainer").hide();
			$("#player").css('width', '96%');
		}else{
			$("#transcriptContainer").show();
			$("#player").css('width', '75%');
		}
	});
	
	$('#closeBtn').click(function(){
		top.close();
	});
});

function updateCCLanguage(lang) {
	Framework.language = lang;
	Navigation.transcript();
}

function setScore(arg) {
	Navigation.lessonCompletion();
}


