import net from 'net';
import delay from 'delay';

const SERVER_HOST = '0.0.0.0';
const SERVER_PORT = 18018;

// socket send and receive information from a peer
const socket = new net.Socket(); 
socket.connect(SERVER_PORT,SERVER_HOST, async () =>{
    console.log('Connectd to server');
    await delay(3000);
    socket.write('Hello, server!\n Love ');
    await delay(3000);
    socket.write('Client\n');
})

socket.on('data', (data)=>{
    console.log(`Server sent: ${data}`);
});

socket.on('error', (error)=>{
    console.log(`Server error: ${error}`);
});

socket.on('close',()=>{
    console.log(`Server disconnected`);
});