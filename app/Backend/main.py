from src.Audio_Handler import AudioHandler
import asyncio
import sys


class GeminiApp:
    def __init__(self):
        self.handler = AudioHandler()
    
    async def main(self):
        try:
            await self.handler.Run()
        except Exception as e:
            print("Error in main Function 🥪   :   ",e)
        finally:
            self.handler.Close()
    
if __name__ == "__main__":
    app = GeminiApp()
    asyncio.run(app.main())


