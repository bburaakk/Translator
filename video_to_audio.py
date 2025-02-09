from moviepy.video.io.VideoFileClip import VideoFileClip

video = VideoFileClip("video.mp4")
video.audio.write_audiofile("audio.wav")
