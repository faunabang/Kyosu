from elevenlabs import Voice, VoiceSettings, voices, generate, play, set_api_key, stream

set_api_key("35be9ae7619739902f7f27cc97b282dc")

audio = generate(
    text="안녕? 나는 제돌이라고 해.",
    voice=Voice(
        voice_id='XrExE9yKIg1WjnnlVkGX',
        settings=None
        # settings=VoiceSettings(stability=1.0, similarity_boost=1.0, style=0.0, use_speaker_boost=True)
    ),
    model="eleven_multilingual_v2"
)

play(audio)