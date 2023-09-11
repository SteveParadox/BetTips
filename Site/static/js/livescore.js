///35bcf66075576af96bd5c56a72f29e93ad8e1eb7c4f78dbe8022227d53f11df8

function socketsLive(){

    var APIkey='2f7fe3ca42c5552cac7a6725da53c657e7fb6814c73cf7ffcf7da0da17ad5863';
    var socket  = new WebSocket('wss://wss.apifootball.com/livescore?Widgetkey='+APIkey+'&timezone=+01:00');
    
      console.log('Connecting...');	
      socket.onopen = function(e) {
          ///alert('Connected');
          console.log('Connected');
          console.log('Waiting data...');
      }		  
      socket.onmessage = function(e) {
          ///alert( e.data );
          if (e.data) {
              var jsonData = JSON.parse(e.data);
                console.log(jsonData);
              var scoreData = ''; // Initialize an empty string to store the data

              // Iterate through the jsonData array
              for (var i = 0; i < jsonData.length; i++) {
                  var match = jsonData[i];
                  var matchInfo = match.match_hometeam_name + ' ' + match.match_hometeam_score + ' vs ' +
                                  match.match_awayteam_score + ' ' + match.match_awayteam_name + ' ' +
                                  match.league_name;
      
                  // Append the match information to the scoreData string
                  scoreData += matchInfo + '<br>';
              }

                console.log(scoreData)
              document.getElementById('data-container').innerHTML = scoreData;
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