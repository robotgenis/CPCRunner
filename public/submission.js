$(document).ready(function($) {
    $("#submitForm").submit(function(){
		$("#submitLoading").css({"display":"block"});
	});
	$("#submitLoading").css({"display":"none"});
});
