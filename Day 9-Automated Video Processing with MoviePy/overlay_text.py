import os
from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS
from moviepy.editor import (VideoFileClip, AudioFileClip,
                            TextClip, concatenate_videoclips)


source_video_path = os.path.join(SAMPLE_INPUTS, 'sample.mp4')
source_audio_path = os.path.join(SAMPLE_INPUTS, 'audio.mp3')
overlay_text_dir = os.path.join(SAMPLE_OUTPUTS, 'overlay_text')

os.makedirs(overlay_text_dir, exist_ok=True)

final_audio_dir = os.path.join(overlay_text_dir, 'overlay-audio.mp3')
final_video_dir = os.path.join(overlay_text_dir, 'overlay-video.mp4')


video_clip = VideoFileClip(source_video_path)


# another audio file to clip
background_audio_clip = AudioFileClip(source_audio_path)

# creating text clip
text = '''
This clip shows how to open terminal.
'''
intro_duration = 5
intro_text = TextClip(txt=text, color='white', fontsize=70,
                      size=video_clip.size)
intro_text = intro_text.set_fps(video_clip.fps)
intro_text = intro_text.set_duration(intro_duration)
intro_text = intro_text.set_pos('center')

intro_video_dir = os.path.join(overlay_text_dir, 'intro-video.mp4')
intro_text.write_videofile(intro_video_dir)

final_clip = concatenate_videoclips([intro_text, video_clip])
final_clip.write_videofile(final_video_dir)
