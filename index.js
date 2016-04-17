function setInputGreyed() {
	$('');

}

function makehtmlstring(message, from) {
    return '<div class="from-' + from + '"><p>' + message + '</p></div><div class="clear"></div>';
};


$( document ).ready(function () {
	$('#').click(function () {
		setInputGreyed();
		var textToSend = $('#theinput').val();

	});

	$('#chat').append($(makehtmlstring("i am a", "me")));
});
