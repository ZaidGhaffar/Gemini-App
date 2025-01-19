const WEBSOCKET_URL = "ws://localhost:8000/ws"
const micbutton = document.getElementById("mic-button")
let initalized = false

document.getElementById("mic-button").addEventListener('click',async()=>{
    try{
        const stream = await navigator.mediaDevices.getUserMedia({audio:true})
        console.log("mic access has been granted...")
        
    }catch(error){
        console.log("mic has been disconnected🎙️ ")
    }
})


function connect(){
    console.log("Connecting.....")
    const Socket = new WebSocket(WEBSOCKET_URL)  

    Socket.onopen = (event) =>{
        console.log("WebSocket Connected ✅...")
    }

    Socket.onclose = (event) =>{
        console.log("WebSocket DisConnected❌...",event)
    }

    Socket.onerror = (event) =>{
        console.log("Error ❌",event)
    }

    Socket.onmessage = receivemessage
}

function sendVoiceMessage(b64PCM){

    payload = {
        realtime_input: {
            media_chunks: [{
                    mime_type: "audio/pcm",
                    data: b64PCM,
                },
            ],
        },
    }
            Socket.send(JSON.stringify(payload));
            console.log("sent: ", payload);
}


function receivemessage(event){
    const messageData = JSON.parse(event.data);
    const response = new Response(messageData);

    if(response.text){
        displayMessage("GEMINI: " + response.text);
    }
    if(response.audioData){
      injestAudioChuckToPlay(response.audioData);
    }
}



async function initalizedaudiocontext(){
        if (initalized) return;

        audioInputContext = new (window.AudioContext ||
        window.webkitAudioContext)({ sampleRate: 24000 });
        await audioInputContext.audioWorklet.addModule("pcm-processor.js");
        workletNode = new AudioWorkletNode(audioInputContext, "pcm-processor");
        workletNode.connect(audioInputContext.destination);
        initalized = true;
}


