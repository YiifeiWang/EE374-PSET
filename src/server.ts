import net from 'net';
import delay from 'delay';
import { message_class, isJsonString, make_message_json} from './utils';


const PORT = 18018;
const HOST = '0.0.0.0';


const server = net.createServer((socket)=>{
    const address = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log(`Client connected : ${address}`);
    let buffer = ''
    socket.on('data', async (data)=>{
        buffer += data;
        const messages = buffer.split('\n');
        if (messages.length>1){
            for (const message of messages.slice(0,-1)){
                if (isJsonString(message)){
                    console.log(`Client ${address} sent: ${message}`);
                }else{
                    console.log(`INVALID_FORMAT`)
                    socket.write(`INVALID_FORMAT`);
                }
            }
        }       
        buffer = messages[messages.length-1];
        
        // await delay(3000); //create delay
        socket.write(`Hello, Cllient! Love, Server.`);
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