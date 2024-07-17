import os
import gradio as gr
import edge_tts
import asyncio
import random
import time

async def tts(text, voice, speed, output_file):
    if speed > 0:
        rate_str = f"+{speed}%"
    elif speed < 0:
        rate_str = f"{speed}%"
    else:
        rate_str = "0%"

    communicate = edge_tts.Communicate(text, voice, rate=rate_str)
    await communicate.save(output_file)

def infer_tts_audio(tts_voice, tts_text, tts_speed):
    folder_tts = "output"
    os.makedirs(folder_tts, exist_ok=True)
    out_path = os.path.join(folder_tts, f"tts_{random.randint(10000, 99999)}.mp3")

    speed_value = int(tts_speed.rstrip('%'))
    start_time = time.time()
    asyncio.run(tts(tts_text, tts_voice, speed_value, out_path))
    end_time = time.time()

    return out_path

voices = asyncio.run(edge_tts.list_voices())
voice_options = sorted([v['ShortName'] for v in voices])

speed_options = ["-100%", "-90%", "-80%", "-70%", "-60%", "-50%", "-40%", "-30%", "-20%", "-10%", "+10%", "+20%", "+30%", "+40%", "+50%", "+60%", "+70%", "+80%", "+90%", "+100%"]

def get_gui():
    with gr.Blocks() as app:
        gr.Markdown("<center><strong><font size='7'>Multilingual TTS</font></strong></center>")
        gr.Markdown("This demo uses edge-tts to convert text to speech in multiple languages.")

        with gr.Row():
            with gr.Column(scale=1):
                tts_text = gr.Textbox(value="", placeholder="Write the text here...", label="Text", lines=3)
            with gr.Column(scale=1):
                tts_voice = gr.Dropdown(label="Voice", choices=voice_options, value=voice_options[0])
                tts_speed = gr.Dropdown(label="Speed", choices=speed_options, value="+10%")

        tts_button = gr.Button("Convert to Speech")
        tts_output = gr.Audio(label="Generated Speech")

        tts_button.click(
            fn=infer_tts_audio,
            inputs=[tts_voice, tts_text, tts_speed],
            outputs=[tts_output]
        )

    return app

if __name__ == "__main__":
    app = get_gui()
    port = int(os.environ.get("PORT", 7860))
    app.queue()
    app.launch(server_name="0.0.0.0", server_port=port)  # Removed share=True
