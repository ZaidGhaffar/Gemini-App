import pyaudio
import asyncio
from google import genai
from asyncio import TaskGroup
from dotenv import load_dotenv
load_dotenv()

# Initialize the PyAudio system
FORMAT = pyaudio.paInt16
CHANNELS = 1 
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNKS = 1024
MODEL = "models/gemini-2.0-flash-exp"

class AudioHandler:
    def __init__(self):
        self.ai_speaking = False
        self.client = genai.Client(http_options={"api_version": "v1alpha"})
        self.Congfig = {"generation_config": {"response_modalities": ["AUDIO"]}}
        self.queue_in_audio = asyncio.Queue()
        self.queue_out_audio = asyncio.Queue()
        self.pya = pyaudio.PyAudio()
        
    async def ListenAudio(self):
        """Listens audio from the microphone and put them in queue"""
        device_info = self.pya.get_default_input_device_info()
        input_stream = self.pya.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=device_info["index"],
            frames_per_buffer=CHUNKS,
        )
        try:
            print("Listening...")
            while True:
                if not self.ai_speaking:
                    data = await asyncio.to_thread(
                        input_stream.read,CHUNKS, exception_on_overflow=False
                    )
                    await self.queue_in_audio.put(data)
                else:
                    await asyncio.sleep(0.1)
        except Exception as e:
            print("Error in ListenAudio Function 🥪   :   ",e)
        finally:
            input_stream.stop_stream()
            input_stream.close()
    
    
    async def SendAudio(self,session):
        """Continuesly takes audio from the queue & Send it to the Gemini models"""
        try:
            while True:
                audio_data = await self.queue_in_audio.get()
                if audio_data is None:
                    break
                await session.send(input={"data":audio_data,"mime_type": "audio/pcm"},end_of_turn=True)
        except Exception as e:
            print("Error in SendAudio Function 🥪   :   ",e)
    
    async def RecieveAudio(self,session):
        """Continuesly takes audio from the Gemini model & put them into queue for playing that"""
        try:
            while True:
                turns = session.receive()
                async for response in turns:
                    data = response.data
                    if data:
                        await self.queue_out_audio.put(data)
                    text = response.text
                    if text:
                        print(f"Assistant:            {text}")
        except Exception as e:
            print("Error in RecieveAudio Function 🥪   :   ",e)
    
    
    async def PlayAudio(self):
        """Plays the audio from the queue"""
        output_stream = self.pya.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RECEIVE_SAMPLE_RATE,
            output=True,
        )
        try:
            while True:
                data = await self.queue_out_audio.get()
                if not self.ai_speaking:
                    self.ai_speaking = True
                    print("AI Speaking...")
                await asyncio.to_thread(output_stream.write,data)
                if self.queue_out_audio.empty():
                    self.ai_speaking = False  # AI has finished speaking
                    print("You can speak now.")
        except Exception as e:
            print("Error in ListenAudio Function 🥪   :   ",e)
            
    async def Run(self):
        """Initalize the AI Session & start all the asynchronous tasks"""
        try:
            async with (    
                self.client.aio.live.connect(model=MODEL, config=self.Congfig) as session,
                TaskGroup() as tg,
            ):
                tg.create_task(self.ListenAudio())
                tg.create_task(self.SendAudio(session))
                tg.create_task(self.RecieveAudio(session))
                tg.create_task(self.PlayAudio())
                
                # Keep the main coroutine alive
                await asyncio.Event().wait()              
        except Exception as e:
            print("Error in ListenAudio Function 🥪   :   ",e)
            
    def Close(self):
        """Closes the audio stream"""
        self.pya.terminate()

if __name__ == "__main__":
    pass

