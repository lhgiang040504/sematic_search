# from threading import Lock
# from typing import List

# from transformers import MarianMTModel, MarianTokenizer

# model_name = "Helsinki-NLP/opus-mt-vi-en"
# translate_model = None
# translate_tokenizer = None
# model_lock = Lock()

# def load_translation_model():
#     global translate_model, translate_tokenizer
#     if translate_model is None or translate_tokenizer is None:
#         with model_lock:
#             if translate_model is None or translate_tokenizer is None:
#                 translate_tokenizer = MarianTokenizer.from_pretrained(model_name)
#                 translate_model = MarianMTModel.from_pretrained(model_name)
#     return translate_model, translate_tokenizer

# from threading import Lock
# from typing import List

# from transformers import MarianMTModel, MarianTokenizer

# model_name = "Helsinki-NLP/opus-mt-vi-en"
# translate_model = None
# translate_tokenizer = None
# model_lock = Lock()

# def load_translation_model():
#     global translate_model, translate_tokenizer
#     if translate_model is None or translate_tokenizer is None:
#         with model_lock:
#             if translate_model is None or translate_tokenizer is None:
#                 translate_tokenizer = MarianTokenizer.from_pretrained(model_name)
#                 translate_model = MarianMTModel.from_pretrained(model_name)
#     return translate_model, translate_tokenizer

# def translate_vi_to_en(text: str) -> str:
#     translate_model, translate_tokenizer = load_translation_model()
#     batch = translate_tokenizer([text], return_tensors="pt", padding=True)
#     gen = translate_model.generate(**batch)
#     translated = translate_tokenizer.batch_decode(gen, skip_special_tokens=True)
#     return translated[0]

# if __name__ == "__main__":
#     vi_text = "Tôi yêu lập trình và trí tuệ nhân tạo."
#     en_text = translate_vi_to_en(vi_text)
#     print(f"VI: {vi_text}")
#     print(f"EN: {en_text}")

from threading import Lock
from typing import List

from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-vi-en"
translate_model = None
translate_tokenizer = None
model_lock = Lock()

def load_translation_model():
    global translate_model, translate_tokenizer
    if translate_model is None or translate_tokenizer is None:
        with model_lock:
            if translate_model is None or translate_tokenizer is None:
                translate_tokenizer = MarianTokenizer.from_pretrained(model_name)
                translate_model = MarianMTModel.from_pretrained(model_name)
    return translate_model, translate_tokenizer

def translate_vi_to_en(text: str) -> str:
    translate_model, translate_tokenizer = load_translation_model()
    batch = translate_tokenizer([text], return_tensors="pt", padding=True)
    gen = translate_model.generate(**batch)
    translated = translate_tokenizer.batch_decode(gen, skip_special_tokens=True)
    return translated[0]

if __name__ == "__main__":
    vi_text = "Tôi yêu lập trình và trí tuệ nhân tạo."
    en_text = translate_vi_to_en(vi_text)
    print(f"VI: {vi_text}")
    print(f"EN: {en_text}")