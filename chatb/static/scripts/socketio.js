document.addEventListener('DOMContentLoaded', () => {
    // creating a variable to connect to socketio server
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Set default room
    let room = "Lounge"
    joinRoom("Lounge");

    // Displays incoming messages
    socket.on('message', data => {
        if(data.username === undefined){
            // console.log(data.msg);
            const section = document.createElement('section');
            section.innerHTML = `<p class="message"><em> ${data.msg} </em></p>`;
            document.querySelector('.chat-area').append(section);
        }else{
            const section = document.createElement('section');
            section.innerHTML = `<p class="user-info"><span class="username">${data.username}</span><span class="time"> | ${data.time} </span> </p>
                                 <p class="message"> ${data.msg} </p>`;
            document.querySelector('.chat-area').append(section);   
        }
    });

    // To get the text entered by user in the input
    document.querySelector('.send-msg').onclick = () => {
        socket.send({ 'username':username, 'msg':document.querySelector('.user-msg').value, 'room':room });
        // Clear the input area
        document.getElementById("user-msg-area").innerHTML = "";
    }

    // Room selection
    document.querySelectorAll(".select-room").forEach(li => {
        li.onclick = () =>{
            let newRoom = li.innerHTML;
            if (newRoom == room){
                msg = `You are already in ${room}`;
                const section = document.createElement('section');
                section.innerHTML = `<p class="message"><em> ${msg} </em></p>`;
                document.querySelector('.chat-area').append(section);
            }else{
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    // Leave room
    function leaveRoom(room){
        socket.emit('leave', {'username':username, 'room':room});
    }

    // Join Room
    function joinRoom(room){
        socket.emit('join', {'username':username, 'room':room});
        // Clear the message display area
        document.getElementById("chat-area-display").innerHTML = "";
    }

})