import os

from moviepy.editor import ImageSequenceClip, ImageClip
# from PIL import Image

from conf import SAMPLE_OUTPUTS


thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, 'thumbnails')
thumbnail_per_frame_dir = os.path.join(SAMPLE_OUTPUTS, 'thumbnails_per_frame')
thumbnail_per_desired_frames_dir = os.path.join(SAMPLE_OUTPUTS,
                                                'thumbnails_per_desired_frames'
                                                )
thumbnail_per_half_sec_dir = os.path.join(SAMPLE_OUTPUTS,
                                          'thumbnails_per_half_sec')


output_video1 = os.path.join(SAMPLE_OUTPUTS, 'thumbnail_1.mp4')
output_video2 = os.path.join(SAMPLE_OUTPUTS, 'thumbnail_2.mp4')


# directly it will give defected video because filepaths are not in order.
# img_dir = os.listdir(thumbnail_dir)
# filepaths = [os.path.join(thumbnail_dir, fname)
#              for fname in img_dir if fname.endswith('.jpg')]
# or
# filepaths = []
# for fname in img_dir:
#     if fname.endswith(".jpg"):
#         path = os.path.join(thumbnail_dir, fname)
#         filepaths.append(path)

# clip = ImageSequenceClip(filepaths, fps=1)
# clip.write_videofile(output_video)  # without audio


directory = {}

# can do for other collections of imgs.
for root, dirs, files in os.walk(thumbnail_per_frame_dir):
    for fname in files:
        if fname.endswith(".jpg"):
            filepath = os.path.join(root, fname)
            try:
                key = int(fname.replace('.jpg', ''))
            except Exception as e:
                print(e)
                key = None

            if key is not None:
                directory[key] = filepath

new_paths = []
for k in sorted(directory.keys()):
    new_filepath = directory[k]
    new_paths.append(new_filepath)

clip1 = ImageSequenceClip(new_paths, fps=30)
clip1.write_videofile(output_video1)  # without audio


# can also convert each filepath into its own frame
my_clips = []
for path in new_paths:
    frame = ImageClip(path)
    # print(frame.img) numpy array
    my_clips.append(frame.img)

clip2 = ImageSequenceClip(my_clips, fps=30)
clip2.write_videofile(output_video2)  # without audio
