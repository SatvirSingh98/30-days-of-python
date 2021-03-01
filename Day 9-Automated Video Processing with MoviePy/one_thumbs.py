import os

from moviepy.editor import VideoFileClip
from PIL import Image

from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS


source_path = os.path.join(SAMPLE_INPUTS, 'sample.mp4')
thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, 'thumbnails')
thumbnail_per_frame_dir = os.path.join(SAMPLE_OUTPUTS, 'thumbnails_per_frame')


os.makedirs(thumbnail_dir, exist_ok=True)
os.makedirs(thumbnail_per_frame_dir, exist_ok=True)


clip = VideoFileClip(source_path)
print(clip.reader.fps)  # number of frames per second = 30.0
print(clip.reader.nframes)  # total number of frames = 906
print(clip.duration)  # seconds = 30.17

fps = clip.reader.fps
nframes = clip.reader.nframes
sec = nframes / (fps * 1.0)  # 1.0 is multiplied to prevent round-off error
# or sec = clip.duration

# now we have to create image for every frame
duration = int(clip.duration)  # or clip.reader.duration


# thumbnail for frame per second
for i in range(duration):
    frame = clip.get_frame(i)
    # print(frame, '\n') numpy array of pixels at particular second of clip
    img_path = os.path.join(thumbnail_dir, f"{i}.jpg")
    # print(f'frame at {i+1} seconds at {new_img_path}')
    img = Image.fromarray(frame)
    img.save(img_path)


# thumbnail for each frame
for i, per_frame in enumerate(clip.iter_frames()):
    img_per_frame_path = os.path.join(thumbnail_per_frame_dir, f"{i}.jpg")
    img_per_frame = Image.fromarray(per_frame)
    img_per_frame.save(img_per_frame_path)
