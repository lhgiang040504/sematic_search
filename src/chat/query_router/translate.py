from threading import Lock
from typing import Optional
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect
from dotenv import dotenv_values

# Load config (nếu sau này bạn muốn chọn model qua .env)
config = dotenv_values(".env")
translate_model_name = config.get("TRANSLATE_MODEL", "facebook/nllb-200-distilled-600M")

# Global model & lock
tokenizer = None
model = None
model_lock = Lock()

# Lang map
lang_map = {
    'vi': 'vi',
    'en': 'en',
    # Add more if needed
}

def load_translation_model():
    global tokenizer, model
    if model is None or tokenizer is None:
        with model_lock:
            print("Loading translation model...")
            tokenizer_local = AutoTokenizer.from_pretrained(translate_model_name)
            model_local = AutoModelForSeq2SeqLM.from_pretrained(translate_model_name)
            tokenizer = tokenizer_local
            model = model_local
    return tokenizer, model

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'unknown'

def translate_to_english(text: str) -> str:
    tokenizer_local, model_local = load_translation_model()

    detected_lang = detect_language(text)
    print(f"Detected language: {detected_lang}")

    if detected_lang == 'en':
        return text

    if detected_lang not in lang_map:
        print("Unsupported language, fallback to original text.")
        return text

    src_lang = lang_map[detected_lang]
    tgt_lang = lang_map['en']

    tokenizer_local.src_lang = src_lang
    encoded = tokenizer_local(text, return_tensors="pt")

    generated_tokens = model_local.generate(
        **encoded,
        forced_bos_token_id=tokenizer_local.lang_code_to_id[tgt_lang]
    )

    translated_text = tokenizer_local.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated_text

if __name__ == "__main__":
    print("----- Testing translation -----")
    test_text_vi = "Làm thế nào để cài đặt Python trên máy tính của tôi?"
    translated = translate_to_english(test_text_vi)
    print(f"Original: {test_text_vi}")
    print(f"Translated: {translated}")
