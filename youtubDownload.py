import yt_dlp

video_url = "https://www.youtube.com/watch?v=N_aXNgq-2Ms" 

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # 1080p video + en iyi ses
    'outtmpl': 'indirilen_video.%(ext)s'  # Özel dosya adı
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("İndirme tamamlandı!")
