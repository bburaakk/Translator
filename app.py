import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.video.io.VideoFileClip import VideoFileClip
import whisper
from transformers import MarianMTModel, MarianTokenizer


class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Çeviri Uygulaması")
        self.root.geometry("600x500")

        # Whisper modelini yükle
        self.whisper_model = whisper.load_model("medium")

        # Marian modelini yükle
        self.marian_model_name = "Helsinki-NLP/opus-mt-tc-big-en-tr"
        self.marian_model = MarianMTModel.from_pretrained(self.marian_model_name, use_auth_token=True)
        self.marian_tokenizer = MarianTokenizer.from_pretrained(self.marian_model_name, use_auth_token=True)

        # Arayüz Elemanları
        self.create_widgets()

    def create_widgets(self):
        # Video yükle butonu
        self.load_video_button = tk.Button(self.root, text="Video Yükle", command=self.load_video)
        self.load_video_button.pack(pady=20)

        # Ses dosyasını metne çevirme butonu
        self.transcribe_button = tk.Button(self.root, text="Ses Dosyasını Metne Çevir", command=self.transcribe_audio)
        self.transcribe_button.pack(pady=10)

        # Metni çevirmek için buton
        self.translate_button = tk.Button(self.root, text="Metni Çevir", command=self.translate_text)
        self.translate_button.pack(pady=10)

        # Çeviri sonucu alanı
        self.result_label = tk.Label(self.root, text="Çeviri Sonucu:")
        self.result_label.pack(pady=10)

        self.result_text = tk.Text(self.root, height=10, width=60)
        self.result_text.pack(pady=10)

        # Çevrilmiş metni kaydetme butonu
        self.save_button = tk.Button(self.root, text="Kaydet", command=self.save_translation)
        self.save_button.pack(pady=20)

    def load_video(self):
        # Kullanıcıdan video dosyası seçmesi istenir
        self.video_path = filedialog.askopenfilename(title="Bir video dosyası seçin", filetypes=(
        ("Video Files", "*.mp4;*.avi;*.mov"), ("All Files", "*.*")))
        if self.video_path:
            try:
                # Video dosyasını yükleyip ses çıkarma
                video = VideoFileClip(self.video_path)
                audio_path = "audio.wav"
                video.audio.write_audiofile(audio_path)
                self.audio_path = audio_path
                messagebox.showinfo("Başarılı", f"Ses dosyası başarıyla çıkarıldı: {audio_path}")
            except Exception as e:
                messagebox.showerror("Hata", f"Video işlenirken bir hata oluştu: {e}")

    def transcribe_audio(self):
        if hasattr(self, 'audio_path'):
            # Whisper ile ses dosyasını metne çevirme
            result = self.whisper_model.transcribe(self.audio_path)
            self.transcribed_text = result["text"]

            # Metni dosyaya kaydet
            with open("transcription.txt", "w", encoding="utf-8") as file:
                file.write(self.transcribed_text)

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.transcribed_text)
            messagebox.showinfo("Başarılı",
                                "Ses dosyası başarıyla metne çevrildi ve 'transcription.txt' dosyasına kaydedildi!")
        else:
            messagebox.showwarning("Uyarı", "Lütfen önce bir video yükleyin!")

    def translate_text(self):
        if hasattr(self, 'transcribed_text'):
            # Çevrilecek metni cümlelere ayır
            sentences = self.transcribed_text.split(". ")

            translated_sentences = []
            # Her bir cümleyi çevir
            for sentence in sentences:
                inputs = self.marian_tokenizer(sentence, return_tensors="pt", truncation=True, padding=True,
                                               max_length=512)
                translated = self.marian_model.generate(**inputs)
                translated_text = self.marian_tokenizer.decode(translated[0], skip_special_tokens=True)

                translated_sentences.append(translated_text)

            # Çevrilen metni birleştir ve ekrana yaz
            translated_text = ". ".join(translated_sentences)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, translated_text)

            # Çevrilen metni kaydet
            with open("translated.txt", "w", encoding="utf-8") as file:
                file.write(translated_text.strip())

            messagebox.showinfo("Başarılı", "Metin başarıyla çevrildi ve 'translated.txt' dosyasına kaydedildi!")
        else:
            messagebox.showwarning("Uyarı", "Lütfen önce ses dosyasını metne çevirin!")

    def save_translation(self):
        # Çevrilen metni kaydetmek için dosya kaydetme penceresi
        translated_text = self.result_text.get(1.0, tk.END).strip()
        if translated_text:
            save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            if save_path:
                try:
                    with open(save_path, "w") as file:
                        file.write(translated_text)
                    messagebox.showinfo("Başarılı", "Çeviri başarıyla kaydedildi!")
                except Exception as e:
                    messagebox.showerror("Hata", f"Çeviri kaydedilirken bir hata oluştu: {e}")
        else:
            messagebox.showwarning("Uyarı", "Çevrilecek metin yok!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
