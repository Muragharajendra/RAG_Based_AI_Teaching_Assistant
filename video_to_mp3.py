# Converting video to mp3

import os
import subprocess


files=os.listdir('videos')
print(f"Number of video files: {len(files)}")
a=[]
for file in files:
    try:
        # Expected format: Title_..._Tutorial_<number>_...
        # Example: Basic_Structure_of_an_HTML_Website_Sigma_Web_Development_Course_-_Tutorial_3_720P.mp4
        parts = file.split("_Tutorial_")
        if len(parts) > 1:
            tutorial_number = parts[1].split("_")[0]
            file_name = parts[0]
            
            output_filename = f"audios/{tutorial_number}_{file_name}.mp3"
            print(f"Converting {file} -> {output_filename} (Video #{tutorial_number})")
            subprocess.run(["ffmpeg", "-y", "-i", f"videos/{file}", output_filename])
        else:
            print(f"Skipping file {file}: 'Tutorial' not found in name.")
            
    except Exception as e:
        print(f"Error processing {file}: {e}")

audio_filess=os.listdir("audios")
print(f"Number of audio files: {len(audio_filess)}")


