function escapeHTML(html) {
  return document.createElement('div')
    .appendChild(document.createTextNode(html))
    .parentNode.innerHTML;
}

$(function jqueryOnLoadEntry() {
  var messages = document.getElementById("chat-window-messages");
  var sent_prototype = document.getElementById("chat-window-sent-proto");
  var recv_prototype = document.getElementById("chat-window-recv-proto");
  var newelement = sent_prototype.cloneNode(true)
  newelement.children[0].innerHTML = escapeHTML("yes");
  newelement.removeAttribute('id');
  messages.appendChild(newelement);
  newelement = recv_prototype.cloneNode(true);
  newelement.removeAttribute('id');
  messages.appendChild(newelement);

  var send_button = document.getElementById("chat-window-send-message");
  send_button.addEventListener("keypress", onTestChange);
});


function onTestChange() {
  var key = window.event.keyCode;

  // If the user has pressed enter
  if (key == 13) {
    $('#chat').append(makehtmlstring($('#theinput').val(), "me"));
    $.ajax({
      type: "POST",
      url: 'http://mybey.ankin.info/status',
      data: {'textmessage': $('#theinput').val() },
      
      success: function(response){
        response = JSON.parse(response);        
        message = response['message']
        gif = response['gif']
        $('#chat').append(makehtmlstring(message, "them"));
        $('#animation img').attr('src', 'reaction_gifs/' + gif+'.gif').load(function(){ console.log('done');});
        $('#theinput').val('');
      }
    });
    return false;
  }
  else {
    return true;
  }
}
