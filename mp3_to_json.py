import os
import whisper
import json

model=whisper.load_model("large-v2")

audios=os.listdir("audios")
for audio in audios:   
    number=audio.split("_")[0]
    title=audio.split("_")[1][:-4]
    text=model.transcribe(
        audio=f"audios/{audio}",
        language="hi",
        task="translate",
        word_timestamps=False
    )
print(text["segments"])

chunks=[]
for segment in text["segments"]:
    chunks.append({
        "number": number, "title": title, "start": segment["start"], "end": segment["end"],"text":segment["text"]
    })
chunks_with_metadata={"chunks": chunks, "text":text["text"]}
with open(f"json/{audio[:-4]}.json", "w") as f:
    json.dump(chunks_with_metadata, f)
