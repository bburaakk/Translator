import whisper

# Whisper modelini yükleyelim (daha iyi doğruluk için medium modeli)
model = whisper.load_model("medium")

# Ses dosyasını metne çevir
result = model.transcribe("audio.wav")

# Tanınan metni ekrana yazdır
print("\nWhisper ile Tanınan Metin:\n", result["text"])

# Metni bir dosyaya kaydet
with open("transcription.txt", "w", encoding="utf-8") as file:
    file.write(result["text"])

print("\nMetin 'transcription.txt' dosyasına kaydedildi!")
