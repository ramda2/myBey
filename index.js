
function makehtmlstring(message, from) {
    return '<div class="from-' + from + '"><p>' + message + '</p></div><div class="clear"></div>';
};


$( document ).ready(function () {
	
});


function onTestChange() {
    var key = window.event.keyCode;

    // If the user has pressed enter
    if (key == 13) {
        $('#chat').append(makehtmlstring($('#theinput').val(), "me"));
        $.ajax({
		  type: "POST",
		  url: 'http://127.0.0.1:5000/status',
		  data: {'textmessage': $('#theinput').val() },
		  
		  success: function(response){
			response = JSON.parse(response);		  	
		  	message = response['message']
		  	gif = response['gif']
		  	$('#chat').append(makehtmlstring(message, "them"));
		  	$('#animation img').attr('src', gif+'.gif').load(function(){ console.log('done');});
		  	$('#theinput').val('');

		  }
		});
        return false;
    }
    else {
        return true;
    }
}