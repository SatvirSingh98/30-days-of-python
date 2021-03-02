# Here we will mix two audio into the video file

import os
from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
# from moviepy.audio.fx.volumex import volumex


source_video_path = os.path.join(SAMPLE_INPUTS, 'sample.mp4')
source_audio_path = os.path.join(SAMPLE_INPUTS, 'audio.mp3')
mixed_audio_dir = os.path.join(SAMPLE_OUTPUTS, 'mixed_audio')

os.makedirs(mixed_audio_dir, exist_ok=True)
og_audio_dir = os.path.join(mixed_audio_dir, 'og.mp3')
final_audio_dir = os.path.join(mixed_audio_dir, 'final-audio.mp3')
final_video_dir = os.path.join(mixed_audio_dir, 'final-video.mp4')


video_clip = VideoFileClip(source_video_path)
original_audio = video_clip.audio
# extracting the original audio
original_audio.write_audiofile(og_audio_dir)


# another audio file to clip
background_audio_clip = AudioFileClip(source_audio_path)
# making subclip of this of same length of video clip
bg_music = background_audio_clip.subclip(t_start=0, t_end=video_clip.duration)

# now we want the background music to be low
bg_music = bg_music.volumex(0.10)  # 10% of it's audio
# or bg_music = bg_music.fx(vfx.volumex, 0.10)

final_audio = CompositeAudioClip([original_audio, bg_music])
final_audio.write_audiofile(final_audio_dir, fps=original_audio.fps)

final_clip = video_clip.set_audio(final_audio)
final_clip.write_videofile(final_video_dir)


# if error in audio file:
# new_audio = AudioFileClip(final_audio_path)
# final_clip = video_clip.set_audio(new_audio)


# if above not work (it is for mp4)
# final_clip.write_videofile(final_video_dir, codec='libx264',
#                            audio_codec='aac')
