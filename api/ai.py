import os
import wave
from django.http import JsonResponse
from google import genai


gemini_api_key = os.getenv('GEMINI_API_KEY')
gemini_model="gemini-2.0-flash-exp"


def text_to_text(request):

    try:
        client = genai.Client(api_key=gemini_api_key)

        response = client.models.generate_content(
            model=gemini_model,
            contents="How old are you, Gemini?"
        )
        
        return JsonResponse({'response': response.text}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

async def text_to_speech(request):
    
    try:
        client = genai.Client(api_key=gemini_api_key)
        config_settings={"generation_config": {"response_modalities": ["AUDIO"]}}

        file_name = 'audio.wav'
        
        with wave.open(file_name, 'wb') as wav:
            wav.setnchannels(1)  # Mono audio
            wav.setsampwidth(2)  # Sample width in bytes
            wav.setframerate(16000)  # 16 kHz sample rate


            print(f"Attempting to connect to WebSocket with model: {gemini_model}")

            async with client.aio.live.connect(model=gemini_model, config=config_settings) as session: 
                print("Connection established to model:", gemini_model)               
               
                message = "Hello? Gemini are you there?"
                print("> ", message, "\n")
                
                await session.send(input=message, end_of_turn=True)

                turn = session.receive()
                async for n,response in enumerate(turn):
                    if response.data is not None:
                        wav.writeframes(response.data)

                        if n==0:
                            print(response.server_content.model_turn.parts[0].inline_data.mime_type)
                        print('.', end='')
        
        print("Audio saved as:", file_name)
        

        return JsonResponse({'audio_file': file_name}, status=200)

        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
