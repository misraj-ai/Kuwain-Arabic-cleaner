# KawnPreprocessor 🧹📚

A comprehensive Arabic text preprocessing class designed to clean and normalize Arabic text for downstream tasks like training large language models (LLMs), machine translation, and NLP applications. This preprocessor supports fine-grained configuration to adapt to a wide variety of data sources, especially noisy web-scraped or user-generated text.

---

## Features

✅ Normalize Arabic characters  
✅ Remove punctuation (optional)  
✅ Retain or remove emojis  
✅ Remove Tashkeel (diacritics), Tatweel (ـ), Quranic symbols  
✅ Remove English text or digits (optional)  
✅ Remove HTML/markup tags  
✅ Normalize non-traditional Arabic character variants  
✅ Fully configurable via initialization

---

## Installation

This is a standalone Python module with no external dependencies except the standard `re` library.

Clone or copy the script into your project:
```bash
git clone https://github.com/misraj-ai/Kuwain-Arabic-cleaner
```
## Parameters

| Parameter                             | Type    | Default | Description |
|--------------------------------------|---------|---------|-------------|
| `remove_diacritics` / `remove_tashkeel` | `bool` | `True`  | Removes Arabic diacritics (Tashkeel) |
| `remove_tatweel`                     | `bool`  | `True`  | Removes Tatweel (ـ) elongation |
| `remove_quranic_symbols`            | `bool`  | `True`  | Removes Quranic symbols (e.g., ۞, ۩) |
| `remove_non_arabic_words`           | `bool`  | `False` | Removes English words and non-Arabic tokens |
| `remove_english_digits`             | `bool`  | `False` | Removes English digits (0–9) |
| `remove_html_markup`                | `bool`  | `False` | Strips HTML/XML tags like `<div>` or `<b>` |
| `keep_emoji`                        | `bool`  | `True`  | Keeps emojis in the text |
| `remove_emoji`                      | `bool`  | `False` | Explicitly removes emojis (overrides `keep_emoji`) |
| `remove_punctuations`              | `bool`  | `False` | Removes Arabic and English punctuation marks |
| `standarize_non_traditional_ar_chars` | `bool` | `True`  | Normalizes variants like “ى” to “ي”, “أ/إ/آ” to “ا”, etc. |


usage
```python
from kuwain_preprocess_arabic_data import KawnPreprocessor

preprocessor = KawnPreprocessor(
    remove_html_markup = True,
    replace_urls_emails_mentions = True,
    strip_tashkeel = True,
    strip_tatweel = True,
    strip_extended_arabic_and_quranic_symbols  = True,
    keep_latten  = True,
    keep_all_non_arabic_letters =  True,
    keep_emojis =  False,
    map_hindi_numbers_to_arabic = True,
    standarize_non_traditional_ar_chars = True,
    seperate_nums_and_words =True,
    seperate_nums_from_pucks =False,
    seperate_words_from_pucks = True,
    remove_non_digit_repetition = True,
)
text = "السَّلامُ عَلَيْكُمْ      ورحمةُ اللهِ وبركاتُهُ!!! 😊😊 زُرْ مَوْقِعَنَا رقم1: www.example.com"
clean_text = preprocessor.preprocess(text)
print(cleaned_text)
```
