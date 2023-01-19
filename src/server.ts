import net from 'net';
import delay from 'delay';
import { message_class, hello_class, error_class, isJsonString, make_message_json} from './utils';
import { canonicalize, canonicalizeEx } from 'json-canonicalize';

const PORT = 18018;
const HOST = '0.0.0.0';
let client_list = ['144.202.122.8','45.63.84.226','45.63.89.228'];

const server = net.createServer((socket)=>{
    const address = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log(`Client connected : ${address}`);
    
    // predefine lots of json strings
    let hello_message:hello_class = {
        "type": "hello",
        "version": "0.9.0",
        "agent": "Marabu-Core Client 0.9"
    }
    let hello_str:string = canonicalize(hello_message);
    let getpeers_message:any = { "type": "getpeers" };
    let getpeers_str:string = canonicalize(getpeers_message);

    // initialize 
    let buffer = ''
    let init_mark = true;
    socket.on('data', async (data)=>{
        buffer += data;
        const messages = buffer.split('\n');
        if (messages.length>1){
            for (const message of messages.slice(0,-1)){
                if (isJsonString(message)){
                    if (init_mark){
                        let message_orig = JSON.parse(message);
                        if (message_orig.type != 'hello'){
                            let error_message:error_class = {
                                "type": "error",
                                "name": "INVALID_HANDSHAKE",
                                "message": "",
                            }
                            let error_str:string = canonicalize(error_message);
                            socket.emit('error', error_str);
                            socket.write(`${error_str}\n`);
                        }else{
                            socket.write(`${hello_str}\n`);
                            socket.write(`${getpeers_str}\n`);
                        }
                    }
                    init_mark = false;
                    console.log(`Client ${address} sent: ${message}`);
                    // socket.write(`Recieved. ${message}`);
                }else{
                    // console.log(`Client ${address} sent: INVALID_FORMAT`)
                    let error_message:error_class = {
                        "type": "error",
                        "name": "INVALID_FORMAT",
                        "message": "",
                    }
                    let error_str:string = canonicalize(error_message);
                    socket.emit('error', error_str);
                    socket.write(`${error_str}\n`);
                }
            }
        }       
        buffer = messages[messages.length-1];
        
        // await delay(3000); //create delay
        // socket.write(`Hello, Cllient! Love, Server.`);
    });
    socket.on('error',(error)=>{
        console.log(`Client ${address} error: ${error}`);
    });
    socket.on('close',()=>{
        console.log(`Client ${address} disconnected`);
    });
});


server.listen(PORT, HOST, () =>{
    console.log(`Server listening on ${HOST}:${PORT}`);
});

    
