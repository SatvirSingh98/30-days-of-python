import os

from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop

from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS


source_path = os.path.join(SAMPLE_INPUTS, 'sample.mp4')
GIF_DIR = os.path.join(SAMPLE_OUTPUTS, 'gifs')

os.makedirs(GIF_DIR, exist_ok=True)

output_path = os.path.join(GIF_DIR, 'sample1.gif')


# it will pixelated gif because of ffmpeg
clip = VideoFileClip(source_path)
fps = clip.fps
sub_clip1 = clip.subclip(t_start=10, t_end=20)
sub_clip1 = sub_clip1.resize(width=500)
sub_clip1.write_gif(output_path, program='ffmpeg', fps=fps)
# ffmpeg will give small size gifs compared to imageio(default)
# but imageio will not give pixelated gif.


# solution:- make mp4 from this subclip and then do the gif part.
# >>> but very large file. <<<
# output_path = os.path.join(GIF_DIR, 'sample2.gif')
# output_path2 = os.path.join(GIF_DIR, 'sample.mp4')
# sub_clip2 = clip.subclip(t_start=10, t_end=20)
# sub_clip2.write_videofile(output_path2)
# sub_clip_path = os.path.join(GIF_DIR, 'sample.mp4')
# sub_clip2.write_gif(output_path, program='ffmpeg', fps=fps)


# creating a cropped clip
width, height = clip.size
sub_clip3 = clip.subclip(t_start=10, t_end=20)
cropped_clip = crop(sub_clip3, width=320, height=320,
                    x_center=width / 2, y_center=height / 2)

output_path = os.path.join(GIF_DIR, 'sample3.gif')
cropped_clip.write_gif(output_path, program='ffmpeg', fps=fps)
