import net from 'net';
import delay from 'delay';
import { message_class, hello_class, error_class, isJsonString, make_message_json} from './utils';
import { canonicalize, canonicalizeEx } from 'json-canonicalize';
import * as fs from 'fs';

const PORT = 18018;
const HOST = '0.0.0.0';

const bootstrapPeers: string[] = [
    "45.63.84.226:18018",
    "45.63.89.228.1:18018",
    "144.202.122.8:18018"
];

let discoveredPeers: string[] = bootstrapPeers;

// Save the list of discovered peers to a local file
function saveDiscoveredPeers() {
    fs.writeFileSync("discovered_peers.json", JSON.stringify(discoveredPeers));
}

// Load the list of discovered peers from a local file
function loadDiscoveredPeers() {
    if (fs.existsSync("discovered_peers.json")) {
        discoveredPeers = JSON.parse(fs.readFileSync("discovered_peers.json").toString());
    }
}

// Add a new peer to the list of discovered peers
function addPeer(peer: string) {
    discoveredPeers.push(peer);
    saveDiscoveredPeers();
}

// Remove a peer from the list of discovered peers
function removePeer(peer: string) {
    const index = discoveredPeers.indexOf(peer);
    if (index !== -1) {
        discoveredPeers.splice(index, 1);
        saveDiscoveredPeers();
    }
}

const server = net.createServer((socket)=>{
    const address = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log(`[LOG] Client connected : ${address}`);
    
    loadDiscoveredPeers();

    // predefine json strings
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
                        let message_obj = JSON.parse(message);
                        if (message_obj.type != 'hello'){
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
                    console.log(`[LOG] Client ${address} sent: ${message}`);
                    let message_obj = JSON.parse(message);
                    if (message_obj.type == 'peers'){
                        addPeer(`${message_obj.peers[1]}`);
                        console.log(`[LOG] Add peer ${message_obj.peers[1]}`);
                    }

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

    
