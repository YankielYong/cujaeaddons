var Answer;
var correct;
var incorrect;
var optionArray = new Array();
var questionObj = new Object();
var attempt = 0;
var xmlObj;
var flag;

function loadXML(filePath, callback, options){
				
	$.get(filePath,function(data){
		callback(data, options);
	});
}
		
$(document).ready(function(){
	
	var filePath = Utils.urlQueryString('xml');//Get query string
	loadXML(filePath,parseXML,'');
	
	$('.question-submit-btn').click(function(){
	
		if(!$(this).hasClass('inactive')){
			attempt++;
			if(questionObj.cyu_type == "mcq"){
			
				var selected_value = parseInt($('input[name="options"]:checked').val());
				console.log($('input[name="radio"]:checked').val());
				console.log(questionObj.Answer);
				flag = selected_value == questionObj.Answer ? 1 : 0; 
				
			}else{
				var selectedValues = [];
				var correctValues = [];
				 $(':checkbox:checked').each(function(i){
					selectedValues[i] = $(this).val();
				 });
				correctValues = (questionObj.Answer).split(",");
				 flag = $(selectedValues).not(correctValues).length == 0 && $(correctValues).not(selectedValues).length == 0 ? 1 : 0;
			}
			
			var message = flag == 1 ? questionObj.correct : questionObj.incorrect;
			
			if(flag == 1){
				$('.question-alt span').html(message);
				$('.finalfeedback').css('display','flex');
				$(this).hide();
				showAnswer();
				attempt > 1 ? parent.setScore(.5) : parent.setScore(1);
			}else{
				if(attempt > 1){					
					$(this).hide();
					$('.question-alt span').html(message);
					$('.finalfeedback').css('display','flex');
					showAnswer();
					parent.setScore(0);
					
				}else{
					$(".modal").modal("show");
					$('.feedback-close').focus();
				}				 
			}
		}
	});
	$('.Next').click(function(){
		parent.$('#next').click();
	});
	
});

function showAnswer(){
	$('.tick').show();
	$('input[name="radio"]').attr("disabled",true);
	$('.Next').focus();
	if(parent.Framework.lastPage) {
		$('.Next').hide();
	}
	
}
function parseXML(xml){
	xmlObj = xml;
	questionObj.cyu_type = $(xml).find("assessment").attr('questionType').toLowerCase();
	
	questionObj.question = $(xml).find("question").text();
	questionObj.correct	= $(xml).find("correct").text();
	questionObj.incorrect = $(xml).find("incorrect").text();

	$('.question-options').attr('aria-labelledby', questionObj.question);
	
	$('.question-title').html(questionObj.question);
	questionObj.Answer = parseInt($(xml).find("assessment").attr('Answer'));
		
	$(xml).find("options").each(function(index){
		optionArray[index] = $(this).text();
		tick = parseInt(index + 1) == questionObj.Answer ? "<div class='tick'><img src='assets/images/tick.png' alt='Correct Answer Tick Mark'/></div>" : '';
		//$(".question-options").append(`<div class="question-options-list">${tick}<div class="question-radio"><input id="radio-${(index+1)}" name="radio" type="radio" value=${(index+1)}><label for="radio-${(index+1)}" class="radio-label"></label><div class="line"></div></div><div class="question-items"><div class="question-no">${(index+1)}</div><div class="question-name">${$(this).text()}</div></div></div>`);
		$(".question-options").append(`<div class="question-options-list">${tick}<div class="question-radio"><input id="radio-${(index+1)}" name="options" type="radio" value=${(index+1)} aria-label="${$(this).text()}"><label for="radio-${(index+1)}" class="radio-label"></label><div class="line"></div></div><div class="question-items"><div class="question-no">${(index+1)}</div><div class="question-name">${$(this).text()}</div></div></div>`);
	});
	questionObj.options = optionArray;
	$('#radio-1').focus();
}