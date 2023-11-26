from elevenlabs import Voice, VoiceSettings, voices, generate, play, set_api_key, stream

set_api_key("35be9ae7619739902f7f27cc97b282dc")

def stream_audio(text):
    audio = generate(
        text=text,
        voice="Matilda",
        model='eleven_multilingual_v2',
        stream=True
    )

    # Stream the audio directly 
    stream(audio)

if __name__ == "__main__":
    text = "안녕하세요"
    stream_audio(text)
