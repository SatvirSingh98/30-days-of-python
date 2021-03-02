import os
from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS
from moviepy.editor import (VideoFileClip, AudioFileClip, CompositeVideoClip,
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
intro_text = intro_text.set_position('center')

intro_music = background_audio_clip.subclip(t_start=0, t_end=intro_duration)
intro_text = intro_text.set_audio(intro_music)

intro_video_dir = os.path.join(overlay_text_dir, 'intro-video.mp4')
intro_text.write_videofile(intro_video_dir)


# overlaying text on the original video
w, h = video_clip.size
watermark_text = TextClip(txt='CFE', fontsize=30, align='East',
                          color='white', size=(w, 30))
watermark_text = watermark_text.set_fps(video_clip.fps)
watermark_text = watermark_text.set_duration(video_clip.duration)
watermark_text = watermark_text.set_position('bottom')

# ordering of clip is important in CompositeVideoClip
cvc = CompositeVideoClip([video_clip, watermark_text], size=video_clip.size)
cvc = cvc.set_duration(video_clip.duration)
cvc = cvc.set_fps(video_clip.fps)


# if above does not work:
# cvc = CompositeVideoClip([watermark_text], size=video_clip.size)
# cvc = cvc.set_duration(video_clip.duration)
# cvc = cvc.set_fps(video_clip.fps)
# overlay_clip = CompositeVideoClip([video_clip, cvc], size=video_clip.size)
# overlay_clip = overlay_clip.set_duration(video_clip.duration)
# overlay_clip = overlay_clip.set_fps(video_clip.fps)
# final_clip = concatenate_videoclips([intro_text, overlay_clip])

final_clip = concatenate_videoclips([intro_text, cvc])
final_clip.write_videofile(final_video_dir)
