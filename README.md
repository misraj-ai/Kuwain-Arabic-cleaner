# KawnPreprocessor 🧹📚

A comprehensive Arabic text preprocessing class designed to clean and normalize Arabic text for downstream tasks like training large language models (LLMs), machine translation, and NLP applications. This preprocessor supports fine-grained configuration to adapt to a wide variety of data sources, especially noisy web-scraped or user-generated text.

---

## Features

✅ Removes URLs, emails, and user mentions and HTML tags and markup.
✅ Standardizes non-traditional Arabic characters.
✅ Maps Hindi numbers to Arabic numerals.
✅ Normalize non-traditional Arabic character variants  
✅ Fully configurable via initialization
✅ Optionally preserves or removes:
- Diacritics (Tashkeel)
- Tatweel
- Emojis
- Latin or all non-Arabic characters
- Quranic and extended Arabic symbols
✅ Adds spacing between:
- Numbers and words
- Numbers and punctuations
- Words and punctuations
✅ Reduces character repetition.


---

## Installation

Install dependencies using pip:
```bash
pip install emoji regex
```

Clone or copy the script into your project:
```bash
git clone https://github.com/misraj-ai/Kuwain-Arabic-cleaner
```
## Parameters

| Parameter                             | Type    | Default | Description |
|--------------------------------------|---------|---------|-------------|
| `remove_html_markup`                | `bool` | `True`  | Removes HTML tags and style/script blocks|
| `replace_urls_emails_mentions`      | `bool`  | `True`  | Removes URLs, emails, and @mentions|
| `strip_tashkeel`                    | `bool`  | `False`  | Removes diacritics (Harakat)|
| `strip_tatweel`                     | `bool`  | `False` | Removes Arabic Tatweel character |
| `strip_extended_arabic_and_quranic_symbols` | `bool`  | `True` | Removes Quranic symbols (e.g., small alef) |
| `keep_latten`                | `bool`  | `True` | Retains Latin characters|
| `keep_all_non_arabic_letters`        | `bool`  | `True`  | Retains all non-Arabic characters including numbers from other scripts, override `keep_latten` option |
| `remove_emoji`                      | `bool`  | `False` | Keeps emojis in text |
| `map_hindi_numbers_to_arabic`              | `bool`  | `False` | Removes Arabic and English punctuation marks |
| `standarize_non_traditional_ar_chars` | `bool` | `True` | Maps non-standard Arabic characters to standard equivalents |
| `seperate_nums_and_words` | `bool` | `True` | Adds spaces between numbers and words|
|`seperate_nums_from_pucks` | `bool` | `False` | Adds spaces between numbers and punctuations|
|`seperate_words_from_pucks` | `bool` | `False` | Adds spaces between words and punctuations|
|`remove_non_digit_repetition` | `bool` | `True` | Replaces repeated non-digit characters with 2 repetitions|


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
#output: السلام عليكم ورحمة الله وبركاته !! زر موقعنا رقم 1 :
```
