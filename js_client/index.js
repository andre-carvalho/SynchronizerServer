var general = {
    namespace:'/occurrences',
    socket: undefined,
    getCenterMap:function(){
        return {point: {lat:23.33,lng:-3.55}};
    },
    token:'',
    login() {
        credentials = JSON.stringify({'email':'afacarvalho@yahoo.com.br','password':'!@12qwaszX'});
        $.post({
            url : "http://127.0.0.1:5000/login",
            data : credentials,
            headers: {
                'Content-Type':'application/json'
            },
            dataType: 'json',
            beforeSend : function(){
                console.log('Enviando....');
            }
        })
        .done(function(msg){
            console.log(msg);
            general.token=msg.auth_token;
        })
        .fail(function(jqXHR, textStatus, msg){
            console.log(msg);
        });
    },
    connect: function(){
        // Connect to the Socket.IO server.
        // The connection URL has the following format:
        //     http[s]://<domain>:<port>[/<namespace>]
        //var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
        if(!general.token) {
            console.log('You should login before connect to websocket.');
            return false;
        }
        // send the token on connection
        this.socket = io("http://192.168.1.121:8001"+this.namespace, {
            query: {
              token: general.token,
            },
          });
          
        this.socket.connect();
        
        // Event handler for new connections.
        // The callback function is invoked when a connection with the
        // server is established.
        this.socket.on('connected', function() {
            // send center map to server.
            general.socket.emit('userposition', general.getCenterMap());
        });
        // Event handler for server sent data.
        // The callback function is invoked whenever the server emits data
        // to the client. The data is then displayed in the "Received"
        // section of the page.
        this.socket.on('nearpoints', function(msg) {
            // receive points that is inside the buffer along to center map.
            $('#log').append('<br>' + $('<div/>').text('Received msg:' + msg.data + ': ' + msg.points).html());
        });
    }
};

$(document).ready(function() {

    $('form#connect').submit(function(event) {
        general.connect();
        return false;
    });

    $('form#emit').submit(function(event) {
        general.socket.emit('userposition',  general.getCenterMap());
        return false;
    });

    $('form#broadcast').submit(function(event) {
        // when one client push a new point to the server.
        general.socket.emit('pointsbroadcast', {data: 'new_point', points: [general.getCenterMap()]});
        return false;
    });
    
    $('form#disconnect').submit(function(event) {
        general.socket.emit('disconnect');
        return false;
    });

    $('#login').click(function(event) {
        general.login();
        return false;
    });

    $('#isReady').html("OK, i'm ready!");

    // Interval function that tests message latency by sending a "ping"
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    // var ping_pong_times = [];
    // var start_time;
    // window.setInterval(function() {
    //     start_time = (new Date).getTime();
    //     general.socket.emit('ping');
    // }, 5000);
    // // Handler for the "pong" message. When the pong is received, the
    // // time from the ping is stored, and the average of the last 30
    // // samples is average and displayed.
    // general.socket.on('pong', function() {
    //     var latency = (new Date).getTime() - start_time;
    //     ping_pong_times.push(latency);
    //     ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
    //     var sum = 0;
    //     for (var i = 0; i < ping_pong_times.length; i++)
    //         sum += ping_pong_times[i];
    //     $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
    // });
    
});