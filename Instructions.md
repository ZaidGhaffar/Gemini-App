**# This is Why you should choose FastAPI**

1. It's super fast due to its :
   - Starlette -> Fast lightweight & asynchronous Progrmming
   - Pydantic -> Data validation and settings management
2. It's super easy to Learn
3. Integration is very easy with FastAPI
4. It's very easy to deploy
5. It's very easy to use
6. Security

navigation.getUserMedia() -> microphone
microhphone -> float32
float32 bit -> Int16 (16-bit PCM)
Int16 -> Base64
base64 -> payload
payload -> websocket
websocket -> Backend

**# Frontend part**

1. When we call navigator.mediaDevices.getUserMedia() the browser acesss the user microphone & start capturing the user audio in raw binary format. - the microhphone audio data comes as float32 data. - we convert the float32 data into int16 16-bit PCM format. It's like preparing the sound for delivery! - Once in PCM format, Our code converts it into Base64 format. This makes it easier to send over the WebSocket. 🚀 - Finally the Base64 data is wrapped up in payload (a neat package (json format)) and sent over the WebSocket.

**# Understanding **

- the onaudioprocess event is fired/triggered whenever the audio chunk is available.
- Our code converts the floating-point data into 16-bit PCM format
