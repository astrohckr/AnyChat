function AnyChatConnection(connection, connectCallback) {
  var channelId = connection.channel;

  var socket = WS4Redis({
    uri: socketUri,//subscribe-broadcast&
    receive_message: onmessage,
    connected: onopen,
    heartbeat_msg: heartbeat
  });

  var heartbeat_msg = "--heartbeat--";//{"eventName": "--heartbeat--"};
  var heartbeat_interval = null;
  var missed_heartbeats = 0;


  // server message event
  function onmessage(e) {
    var data = JSON.parse(e.data);

    //// ignore heartbeat messages
    //if (data.eventName === heartbeat_msg.eventName) {
    //  // reset the counter for missed heartbeats
    //  missed_heartbeats = 0;
    //  return;
    //}

    if (data.eventName === connection.socketMessageEvent) {
      onMessagesCallback(data.data);
    }

    if (data.eventName === 'presence') {
      data = data.data;
      if (data.userid === connection.userid) return;
      connection.onUserStatusChanged({
        userid: data.userid,
        status: data.isOnline === true ? 'online' : 'offline',
        extra: connection.peers[data.userid] ? connection.peers[data.userid].extra : {}
      });
    }
  }

  socket.onerror = function () {
    console.error('Socket connection is failed.');
  };

  socket.onclose = function () {
    console.warn('Socket connection is closed.');
  };

  function onopen() {
    // if connection.enableLogs
    console.info('socket.io connection is opened.');
    if (connectCallback) connectCallback(socket);

    socket.emit('presence', {
      userid: connection.userid,
      isOnline: true
    });


    //// keep track of heartbeats, close socket if timed out
    //if (heartbeat_interval === null) {
    //  missed_heartbeats = 0;
    //
    //  heartbeat_interval = setInterval(function () {
    //    missed_heartbeats++;
    //
    //    // timeout after 3 missed heartbeats
    //    if (missed_heartbeats >= 3) {
    //      clearInterval(heartbeat_interval);
    //      heartbeat_interval = null;
    //      console.warn("Closing connection. Too many missed heartbeats.");
    //      socket.close();
    //
    //      return;
    //    }
    //
    //    socket.send(JSON.stringify(heartbeat_msg));
    //  }, 5000);
    //}
  };

  socket.emit = function (eventName, data, callback) {
    socket.send_message(JSON.stringify({
      eventName: eventName,
      data: data
    }));

    if (callback) { // this shouldn't be called, it is used in openOrJoin
      console.warn('Callback exists');
      callback();
    }
  };

  var mPeer = connection.multiPeersHandler;

  function onMessagesCallback(message) {
    if (message.remoteUserId != connection.userid) return;

    if (connection.enableLogs) {
      console.debug(message.sender, message.message);
    }

    if (connection.peers[message.sender] && connection.peers[message.sender].extra != message.extra) {
      connection.peers[message.sender].extra = message.extra;
      connection.onExtraDataUpdated({
        userid: message.sender,
        extra: message.extra
      });
    }

    if (message.message.streamSyncNeeded && connection.peers[message.sender]) {
      var stream = connection.streamEvents[message.message.streamid];
      if (!stream || !stream.stream) {
        return;
      }

      var action = message.message.action;

      if (action === 'ended') {
        connection.onstreamended(stream);
        return;
      }

      var type = message.message.type != 'both' ? message.message.type : null;
      stream.stream[action](type);
      return;
    }

    if (message.message === 'connectWithAllParticipants') {
      if (connection.broadcasters.indexOf(message.sender) === -1) {
        connection.broadcasters.push(message.sender);
      }

      mPeer.onNegotiationNeeded({
        allParticipants: connection.peers.getAllParticipants(message.sender)
      }, message.sender);
      return;
    }

    if (message.message === 'removeFromBroadcastersList') {
      if (connection.broadcasters.indexOf(message.sender) !== -1) {
        delete connection.broadcasters[connection.broadcasters.indexOf(message.sender)];
        connection.broadcasters = removeNullEntries(connection.broadcasters);
      }
      return;
    }

    if (message.message === 'dropPeerConnection') {
      if (connection.peers[message.sender]) {
        connection.peers[message.sender].peer.close();
        connection.peers[message.sender].peer = null;
        delete connection.peers[message.sender];
      }
      return;
    }

    if (message.message.allParticipants) {
      if (message.message.allParticipants.indexOf(message.sender) === -1) {
        message.message.allParticipants.push(message.sender);
      }

      message.message.allParticipants.forEach(function (participant) {
        mPeer[!connection.peers[participant] ? 'createNewPeer' : 'renegotiatePeer'](participant, {
          localPeerSdpConstraints: {
            OfferToReceiveAudio: connection.sdpConstraints.mandatory.OfferToReceiveAudio,
            OfferToReceiveVideo: connection.sdpConstraints.mandatory.OfferToReceiveVideo
          },
          remotePeerSdpConstraints: {
            OfferToReceiveAudio: connection.session.oneway ? !!connection.session.audio : connection.sdpConstraints.mandatory.OfferToReceiveAudio,
            OfferToReceiveVideo: connection.session.oneway ? !!connection.session.video || !!connection.session.screen : connection.sdpConstraints.mandatory.OfferToReceiveVideo
          },
          isOneWay: !!connection.session.oneway || connection.direction === 'one-way',
          isDataOnly: isData(connection.session)
        });
      });
      return;
    }

    if (message.message.newParticipant) {
      if (message.message.newParticipant == connection.userid) return;
      if (!!connection.peers[message.message.newParticipant]) return;

      mPeer.createNewPeer(message.message.newParticipant, message.message.userPreferences || {
            localPeerSdpConstraints: {
              OfferToReceiveAudio: connection.sdpConstraints.mandatory.OfferToReceiveAudio,
              OfferToReceiveVideo: connection.sdpConstraints.mandatory.OfferToReceiveVideo
            },
            remotePeerSdpConstraints: {
              OfferToReceiveAudio: connection.session.oneway ? !!connection.session.audio : connection.sdpConstraints.mandatory.OfferToReceiveAudio,
              OfferToReceiveVideo: connection.session.oneway ? !!connection.session.video || !!connection.session.screen : connection.sdpConstraints.mandatory.OfferToReceiveVideo
            },
            isOneWay: !!connection.session.oneway || connection.direction === 'one-way',
            isDataOnly: isData(connection.session)
          });
      return;
    }

    if (message.message.readyForOffer) {
      connection.addNewBroadcaster(message.sender);
    }

    if (message.message.newParticipationRequest) {
      if (connection.peers[message.sender]) {
        if (connection.peers[message.sender].peer) {
          connection.peers[message.sender].peer.close();
          connection.peers[message.sender].peer = null;
        }
        delete connection.peers[message.sender];
      }

      var userPreferences = {
        extra: message.extra || {},
        localPeerSdpConstraints: message.message.remotePeerSdpConstraints || {
          OfferToReceiveAudio: connection.sdpConstraints.mandatory.OfferToReceiveAudio,
          OfferToReceiveVideo: connection.sdpConstraints.mandatory.OfferToReceiveVideo
        },
        remotePeerSdpConstraints: message.message.localPeerSdpConstraints || {
          OfferToReceiveAudio: connection.session.oneway ? !!connection.session.audio : connection.sdpConstraints.mandatory.OfferToReceiveAudio,
          OfferToReceiveVideo: connection.session.oneway ? !!connection.session.video || !!connection.session.screen : connection.sdpConstraints.mandatory.OfferToReceiveVideo
        },
        isOneWay: typeof message.message.isOneWay !== 'undefined' ? message.message.isOneWay : !!connection.session.oneway || connection.direction === 'one-way',
        isDataOnly: typeof message.message.isDataOnly !== 'undefined' ? message.message.isDataOnly : isData(connection.session),
        dontGetRemoteStream: typeof message.message.isOneWay !== 'undefined' ? message.message.isOneWay : !!connection.session.oneway || connection.direction === 'one-way',
        dontAttachLocalStream: !!message.message.dontGetRemoteStream,
        connectionDescription: message,
        successCallback: function () {
          // if its oneway----- todo: THIS SEEMS NOT IMPORTANT.
          if (typeof message.message.isOneWay !== 'undefined' ? message.message.isOneWay : !!connection.session.oneway || connection.direction === 'one-way') {
            connection.addNewBroadcaster(message.sender, userPreferences);
          }

          if (!!connection.session.oneway || connection.direction === 'one-way' || isData(connection.session)) {
            connection.addNewBroadcaster(message.sender, userPreferences);
          }
        }
      };

      connection.onNewParticipant(message.sender, userPreferences);
      return;
    }

    if (message.message.shiftedModerationControl) {
      connection.onShiftedModerationControl(message.sender, message.message.broadcasters);
      return;
    }

    if (message.message.changedUUID) {
      if (connection.peers[message.message.oldUUID]) {
        connection.peers[message.message.newUUID] = connection.peers[message.message.oldUUID];
        delete connection.peers[message.message.oldUUID];
      }
    }

    if (message.message.userLeft) {
      mPeer.onUserLeft(message.sender);

      if (!!message.message.autoCloseEntireSession) {
        connection.leave();
      }

      return;
    }

    mPeer.addNegotiatedMessage(message.message, message.sender);
  }

  window.addEventListener('beforeunload', function () {
    socket.emit('presence', {
      userid: connection.userid,
      isOnline: false
    });
  }, false);

  return socket;
}