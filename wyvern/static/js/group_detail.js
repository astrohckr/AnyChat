var connection = new RTCMultiConnection(group);

connection.socketURL = 'http://138.87.178.144:3000/';

connection.session = {
    audio: true,
    video: true,
    data: true
};

connection.sdpConstraints.mandatory = {
    OfferToReceiveAudio: true,
    OfferToReceiveVideo: true
};

connection.onstream = function (event) {
    var video = event.mediaElement;
    var $div = $('<div/>');

    $div.addClass('video');
    $div.addClass('thumbnail');

    $("#videos").append($div);
    $div.append(video);

    video.controls = false;
    video.play();
};

//connection.onmessage = appendDIV;
//connection.filesContainer = document.getElementById('file-container');
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

connection.openOrJoin(group);

//$('#open').onclick = function () {
//    this.disabled = true;
//    connection.open(document.getElementById(group).value);
//};
//$('#join').onclick = function () {
//    this.disabled = true;
//    connection.join(document.getElementById(group).value);
//};

//var SIGNALING_SERVER = 'ws://138.87.178.144:3000/';
//var serverSocket = io(SIGNALING_SERVER);
//
//
//var openSignalingChannel = function (config) {
//    var channel = config.channel || this.channel || group;
//    var sender = Math.round(Math.random() * 9999999999) + 9999999999;
//
//    serverSocket.emit('new-channel', {
//        channel: channel,
//        sender: sender
//    });
//
//    var groupSocket = io(SIGNALING_SERVER + channel);
//
//    groupSocket.channel = channel;
//
//    groupSocket.on('connect', function () {
//        if (config.callback) config.callback(groupSocket);
//    });
//
//    groupSocket.send = function (message) {
//        groupSocket.emit('message', {
//            sender: sender,
//            data: message
//        });
//    };
//
//    groupSocket.on('message', config.onmessage);
//
//    groupSocket.emit('messgae', {
//        sender: 'ryan',
//        data: 'srtxhrthntrjnty'
//    });
//};
//
//var connection = new RTCMultiConnection(group).connect();
//
//
//var start = function () {
////    if (action === 'open') {
////        var sessionDescription = connection.open();
////
////        serverSocket.send(sessionDescription);
////
////    } else {
//        serverSocket.onmessage = function (event) {
//            var sessionDescription = event.data.sessionDescription;
//
//            connection.join(sessionDescription);
//        };
//        connection.connect();
//        connection.join(group);
//    //}
//};
//
//connection.getExternalIceServers = false;
//connection.iceServers = [{
//    "urls": "turn:138.87.178.144:8889",
//    "username": "u",
//    "credential": "p"
//}];
//
//connection.channel = group;
//connection.session = {
//    audio: true, // by default, it is true
//    video: true, // by default, it is true
//    screen: false,
//
//    data: true,
//
//    oneway: false,
//    broadcast: false
//};
//
////connection.transmitRoomOnce = true;
//
//// defaults, in kbps
//connection.bandwidth = {
//    audio: 80,
//    video: 2048
//    //data: 1638400
//};
//
//
//
//connection.onNewSession = function (session) {
//    console.log(session);
//    connection.join(session);
//};
//
//connection.onspeaking = function (e) {
//    // e.streamid, e.userid, e.stream, etc.
//    e.mediaElement.style.border = '1px solid red';
//};
//
//connection.onsilence = function (e) {
//    // e.streamid, e.userid, e.stream, etc.
//    e.mediaElement.style.border = '';
//};
//
//connection.onstream = function (event) {
//    if (event.isScreen) {
//        // screenVideo.src = event.blobURL;
//        addVideo(event.mediaElement);
//    }
//
//    //if (event.isAudio) {
//    //    audioOnlyTag.src = event.blobURL;
//    //}
//
//    if (event.isVideo) {
//        // audioPlusVideo.src = event.blobURL;
//        // videoOnly.src = event.blobURL;
//        addVideo(event.mediaElement);
//    }
//};
//
//connection.onstreamended = function (e) {
//    // e.mediaElement (audio or video element)
//    // e.stream     native MediaStream object
//    // e.streamid   unique identifier of the stream synced from stream sender
//    // e.session {audio: true, video: true}
//    // e.blobURL
//    // e.type     "local" or "remote"
//    // e.extra
//    // e.userid   the person who shared stream with you!
//    e.mediaElement.parentNode.parentNode.removeChild(e.mediaElement.parentNode);
//};
//
//connection.onmessage = function (e) {
//    var server = e.userid === 'server' ? 'server' : '';
//
//    var $message = $('<div class="message' + server.toLowerCase() + '"></div>');
//    var $text = $('<div class="text"></div>');
//    $message.text(e.userid);
//    $text.text(e.data);
//
//    // command: e.extra
//};
//
//start();
