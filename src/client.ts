import net from 'net';
// import delay from 'delay';
import { message_class, hello_class, error_class, isJsonString, make_message_json} from './utils';
import { canonicalize, canonicalizeEx } from 'json-canonicalize';

const SERVER_HOST = '0.0.0.0';
const SERVER_PORT = 18018;

// socket send and receive information from a peer
const socket = new net.Socket(); 
socket.connect(SERVER_PORT,SERVER_HOST, async () =>{
    console.log('Connectd to server');
    // await delay(3000);
    let hello_message:hello_class = {
        "type": "hello",
        "version": "0.9.0",
        "agent": "Marabu-Core Client 0.9"
    }
    let hello_str:string = canonicalize(hello_message);
    let message1 = 'Hello, server!';
    let message1_json = make_message_json(message1,'data');

    socket.write(`${hello_str}\n`);
    socket.write(`${message1_json}\n`);
    // socket.write(`${message1}\n`);
    // await delay(3000);
    // socket.write('Love Client\n');
})
let buffer = '';
socket.on('data', (data)=>{
    buffer += data;
    const messages = buffer.split('\n');
    if (messages.length>1){
        for (const message of messages.slice(0,-1)){
            if (isJsonString(message)){
                console.log(`Server sent: ${message}`);
                let message_orig = JSON.parse(message);

                // deal with the handshake error
                if (message_orig.type == 'error'){
                    if (message_orig.name == 'INVALID_HANDSHAKE'){
                        socket.emit('close');
                    }
                    if (message_orig.name == 'INVALID_FORMAT'){
                        socket.emit('error',message);
                    }
                }
            }else{
                let error_message:error_class = {
                    "type": "error",
                    "name": "INVALID_FORMAT",
                    "message": "",
                }
                let error_str:string = canonicalize(error_message);
                socket.emit('error', error_str);
            }
        }
    }       
    buffer = messages[messages.length-1];
});

socket.on('error', (error)=>{
    console.log(`Server error: ${error}`);
});

socket.on('close',()=>{
    console.log(`Server disconnected`);
});