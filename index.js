function escapeHTML(html) {
  return document.createElement('div')
    .appendChild(document.createTextNode(html))
    .parentNode.innerHTML;
}

var node_appender;

$(function jqueryOnLoadEntry() {
  var messages = document.getElementById("chat-window-messages");
  var sent_prototype = document.getElementById("chat-window-sent-proto");
  var recv_prototype = document.getElementById("chat-window-recv-proto");

  node_appender = makeNodeAppender(messages, sent_prototype, recv_prototype);

  var send_button = document.getElementById("chat-window-send-message");
  var chat_input = document.getElementById("chat-window-input");
  chat_input.addEventListener("keypress", onTestChange);
});

function makeNodeAppender(parent, proto_sent, proto_recv) {
  var _parent = parent;
  var _proto_sent = proto_sent;
  var _proto_recv = proto_recv;

  return {
    'add_sent_message': function add_sent_message(text) {
      var newelement = _proto_sent.cloneNode(true);
      newelement.children[0].innerHTML = escapeHTML(text);
      newelement.removeAttribute('id');
      _parent.appendChild(newelement);
    },
    'add_recv_message': function add_recv_message(text) {
      var newelement = _proto_recv.cloneNode(true);
      newelement.children[0].innerHTML = escapeHTML(text);
      newelement.removeAttribute('id');
      _parent.appendChild(newelement);
    }
  }
}

function onTestChange(event) {
  // console.log("success");
  var key = event.keyCode;

  // If the user has pressed enter
  if (key == 13) {
    var value = $('#chat-window-input').val();
    node_appender.add_sent_message(value);
    $.ajax({
      type: "POST",
      url: 'http://mybey.ankin.info/status',
      data: { 'textmessage': value },

      success: function successCallback(response) {
        response = JSON.parse(response);
        message  = response['message'];
        gif      = response['gif'];

        node_appender.add_recv_message(message);
        $('#animation img').attr('src', 'reaction_gifs/' + gif + '.gif')
          // .load(function newImageLoaded() { console.log('done'); });

        $('#chat-window-input').val('');
      }
    });

    return false;
  }

  else {
    return true;
  }
}
