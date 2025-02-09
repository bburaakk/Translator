from transformers import MarianMTModel, MarianTokenizer

# Modelin ismi
model_name = "Helsinki-NLP/opus-mt-tc-big-en-tr"

# Model ve tokenizer'ı yükle
model = MarianMTModel.from_pretrained(model_name, use_auth_token=True)
tokenizer = MarianTokenizer.from_pretrained(model_name, use_auth_token=True)

# 'transcription.txt' dosyasından metni oku
with open("transcription.txt", "r") as file:
    text = file.read()

# Metni cümlelere ayır (Türkçe ve İngilizce cümle sınırları farklı olabilir)
sentences = text.split(". ")

# Çevrilen metni saklamak için bir liste
translated_sentences = []

# Her bir cümleyi çevir
for sentence in sentences:
    # Cümleyi tokenize et
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Çeviriyi yap
    translated = model.generate(**inputs)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

    translated_sentences.append(translated_text)

# Çevrilen tüm cümleleri birleştir
translated_text = ". ".join(translated_sentences)

# Çevrilen metni 'translated.txt' dosyasına yaz
with open("translated.txt", "w") as file:
    file.write(translated_text.strip())

print("Çeviri tamamlandı ve 'translated.txt' dosyasına yazıldı.")
