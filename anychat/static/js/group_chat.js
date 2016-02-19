(function () {
  var connection = new window.RTCMultiConnection();

  connection.setCustomSocketHandler(AnyChatConnection);

  connection.userid = window.localStorage.getItem('user_id');
  connection.socketMessageEvent = 'anychat-message';
//document.getElementById('room-id').value = connection.token();

  connection.session = {
    audio: true,
    video: true
    //data: true
  };

  connection.sdpConstraints.mandatory = {
    OfferToReceiveAudio: true,
    OfferToReceiveVideo: true
  };


  var $videosContainer = $("#videos");
  connection.onstream = function (event) {
    var video = event.mediaElement;
    var $div = $('<div/>');

    $div.addClass('video');
    $div.addClass('thumbnail');

    $videosContainer.append($div);
    $div.append(video);

    video.controls = false;
    video.play();
  };

  connection.onopen = function () {
    //document.getElementById('share-file').disabled = false;
    //document.getElementById('input-text-chat').disabled = false;
  };


  var socket = connection.getSocket();
  $('#text-box').keypress(function (e) {
    if (e.which == 13 && !e.shiftKey) {
      var $text = $('#text-box');
      var message = {
        userId: 'Ryan',
        text: $text.get(0).value
      };

      connection.send(message); // send to everyone
      connection.onmessage({data: message}); // add it to own chat

      $text.val(''); // clear text
    }
  });

  connection.onmessage = function (event) {
    var message = event.data;

    // split message data into multiple divs
    // lines = foo.value.split(/\r\n|\r|\n/);

    var $chat = $('#messages');
    var $message = $('<div/>');
    var $user = $('<div/>');
    var $text = $('<div/>');

    $chat.append($message);
    $message.append($user);
    $message.append($text);

    if (message.userId === 'server') $message.addClass('server');
    $message.addClass('message');
    $user.addClass('user');
    $text.addClass('text');

    $user.text(message.userId);
    $text.text(message.text);
    // command:  message.extra
  };

  // assume all groups are created (open creates a group, join joins a group)
  connection.join(group);

})();