///35bcf66075576af96bd5c56a72f29e93ad8e1eb7c4f78dbe8022227d53f11df8

function socketsLive(){

    var APIkey='2f7fe3ca42c5552cac7a6725da53c657e7fb6814c73cf7ffcf7da0da17ad5863';
    var socket  = new WebSocket('wss://wss.apifootball.com/livescore?Widgetkey='+APIkey+'&timezone=+01:00');
    
      console.log('Connecting...');	
      socket.onopen = function(e) {
          alert('Connected');
          console.log('Connected');
          console.log('Waiting data...');
      }		  
      socket.onmessage = function(e) {
          alert( e.data );
          if (e.data) {
              var data = JSON.parse(e.data);
          } 
          else {
              console.log('No new data!');
          }
      }
      socket.onclose = function(){
          socket = null;
          setTimeout(socketsLive, 5000);
      }
  
  }
  socketsLive();