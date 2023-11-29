from elevenlabs import Voice, VoiceSettings, voices, generate, play, set_api_key, stream

set_api_key("e5fb5e7333aea826329755e9f1459ab6")

def stream_audio(text):
    audio = generate(
        text=text,
        voice=Voice(
            voice_id="XrExE9yKIg1WjnnlVkGX",
            settings=VoiceSettings(stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=False)
        ),
        model='eleven_multilingual_v2',
        stream=True
    )

    # Stream the audio directly 
    stream(audio)

if __name__ == "__main__":
    text = "안녕하세요? 저는 교수라고 합니다."
    stream_audio(text)
