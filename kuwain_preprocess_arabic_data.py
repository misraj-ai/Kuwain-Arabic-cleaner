import html
import logging
import re
import regex
from typing import List
import emoji



URL_REGEXES = [
    r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
    r"@(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$@iS",
    r"http[s]?://[a-zA-Z0-9_\-./~\?=%&]+",
    r"www[a-zA-Z0-9_\-?=%&/.~]+",
    r"[a-zA-Z]+\.com",
    r"(?=http)[^\s]+",
    r"(?=www)[^\s]+",
    r"://",
]
USER_MENTION_REGEX = r"@[\w\d]+"
EMAIL_REGEXES = [r"[\w-]+@([\w-]+\.)+[\w-]+", r"\S+@\S+"]

MULTIPLE_CHAR_PATTERN = re.compile(r"(\D)\1{2,}", re.DOTALL)


REGEX_URL_STEP1 = r"(?=http)[^\s]+"
REGEX_URL_STEP2 = r"(?=www)[^\s]+"
REGEX_URL = r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
REGEX_MENTION = r"@[\w\d]+"
REGEX_EMAIL = r"\S+@\S+"


NUMBER_WITH_FLOATING_POINT = r'[+-]?((\d+(\.\d*)?)|(\.\d+))'
NUMBER_WITH_FLOATING_POINT_STARTS_WITH_NON_DIGIT = r'([+-](\d+(\.\d*)?))'

HYPHEN_PATTERN = r"\u002D\u2010-\u2015_"
ACCEPTED_NON_LETTER_OR_NUMBER =                          r"\[\]!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_`{\|}~—٪’،؟`୍“؛”ۚ»؛\s«–…‘/" + HYPHEN_PATTERN + "·•×÷&!"
ACCEPTED_NON_LETTER_OR_NUMBER_NO_SPACE =                 r"\[\]!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_`{\|}~—٪’،؟`୍“؛”ۚ»؛«–…‘/" + HYPHEN_PATTERN + "·•×÷&!"
ACCEPTED_NON_LETTER_OR_NUMBER_NO_DOT_PLUSE_MINUS_SPACE = r"\[\]!\"#\$%\'\(\)\*,\:;\<=·>?@\[\\\]\^_`{\|}~—٪’،؟`୍“؛”ۚ»؛«–…‘/" + "·•×÷&!"
ACCEPTED_NON_LETTER_OR_NUMBER_NO_Apostrophe_Hyphen_DOT_Underscore_SPACE = r"\[\]!\"#\$%\\(\)\*,\:;\<=·>?@\[\\\]\^`{\|}~٪’،؟`୍“؛”ۚ»؛«…‘/" + "·•×÷&!"

#arabic words
ARABIC_LETTER_PATTERN = r"\u0621-\u063A\u0641-\u064A"  # ء to غ and ف to ي only letters
HARAKA_PATTERN = r"\u064b-\u0652" #harakat and shadda
TATWEEL_PATTERN = r"ـ"

EXTENDED_ARABIC_LETTER_PATTERN = r"\u0600-\u06FF"

#latten words
LATTEN_LETTER_PATTERN = r"A-Za-zÀ-ÖØ-öø-ÿĀ-ſƀ-ƿǝ-ǿ0-9"

#all letters and numbers in all languages
ALL_LETTERS_AND_NUMBERS = r'\w'

#numbers
ARABIC_NUMBER_PATTERN = r"0-9" # 0 to 9
HINDI_NUMBER_PATTERN = r"\u0660-\u0669" #٠ to ٩
ALL_NUMBER_PATTERN = ARABIC_NUMBER_PATTERN + HINDI_NUMBER_PATTERN

EMOJI_PATTERN = "".join(list(sorted(emoji.EMOJI_DATA, key=len, reverse=True)))
"".join(sorted(emoji.EMOJI_DATA, key=len, reverse=True))


_HINDI_NUMS = "٠١٢٣٤٥٦٧٨٩"
_ARABIC_NUMS = "0123456789"
HINDI_TO_ARABIC_MAP = str.maketrans(_HINDI_NUMS, _ARABIC_NUMS)


ARABIC_MAP = {
    'ﺏ': 'ب', 'ﺗ': 'ت', 'ﺷ': 'ش', 'ﻦ': 'ن', 'ﻷ': 'لا', 'ﺴ': 'س', 'ﻧ': 'ن', 'ٲ': 'ا', 'ﻻ': 'لا', 'ﻜ': 'ك',
    'ﺇ': 'ا', 'ﺑ': 'ب', 'ﺎ': 'ا', 'ک': 'ك', 'ﺯ': 'ز', 'ﺌ': 'ئ', 'ﻰ': 'ى', 'ﻣ': 'م', 'ﺕ': 'ت', 'ﺆ': 'ؤ',
    'ﺼ': 'ص', 'ﺏ': 'ب', 'ﻥ': 'ن', 'ﺲ': 'س', 'ﻠ': 'ل', 'ﺻ': 'ص', 'ﺟ': 'ج', 'ﺰ': 'ز', 'ﺃ': 'ا', 'ﺁ': 'ا',
    'ﺘ': 'ت', 'ﺈ': 'ا', 'ﻳ': 'ي', 'ی': 'ى', 'ﺓ': 'ة', 'ﺜ': 'ث', 'ﺒ': 'ب', 'ﻟ': 'ل', 'ﺺ': 'ص', 'ﺧ': 'خ',
    'ﻒ': 'ف', 'ﻚ': 'ك', 'ﺿ': 'ض', 'ﺣ': 'ح', 'ﻔ': 'ف', 'ﻴ': 'ي', 'ﺳ': 'س', 'ﻭ': 'و', 'ﻤ': 'م', 'ﻘ': 'ق',
    'ﻋ': 'ع', 'ﻲ': 'ي', 'ﻵ': 'لا', 'ﻞ': 'ل', 'ﻏ': 'غ', 'ﻱ': 'ي', 'ﻙ': 'ك', 'ﻊ': 'ع', 'ﻪ': 'ه', 'ﺛ': 'ث',
    'ﻨ': 'ن', 'ﺨ': 'خ', 'ۃ': 'ة', 'ﻡ': 'م', 'ﻫ': 'ه', 'ﻩ': 'ه', 'ﺍ': 'ا', 'ﻗ': 'ق', 'ﺬ': 'ذ', 'ﻝ': 'ل',
    'ﻛ': 'ك', 'ﺖ': 'ت', 'ﻈ': 'ظ', 'ﺫ': 'ذ', 'ﺤ': 'ح', 'ﻼ': 'لا', 'ٱ': 'ا', 'ﺪ': 'د',
    'ﺮ': 'ر', 'ﺹ': 'ص','ﺱ': 'س', 'ﻌ': 'ع', 'ﺠ': 'ج', 'ﺄ': 'ا', 'ﺐ': 'ب',
    'ﺩ':'د', 'ﺔ':'ة', 'ﺭ':'ر', 'ﻢ':'م', 'ﻬ':'ه', 'ﻮ':'و', 'ﻓ':'ف', 'ﻓ':'ف',
    '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9', '٠': '0',

    'ﷺ':'صلى الله عليه وسلم', 'ﷻ':'جل جلاله', 'ﷹ':'صلى', 'ﷸ':'وسلم','ﷲ':'الله','ﷳ':'أكبر','ﷴ':'محمد',
    'ﷵ':'صلى الله عليه وسلم', 'ﷶ':'رسول', 'ﷷ':'عليه', '﷽':'بسم الله الرحمن الرحيم',
}
ARABIC_MAP = str.maketrans(ARABIC_MAP)

#script
SCRIPT_TAGS = r'<script.*>[\s\S]*?<\/script>'
#style
STYLE_TAGS = r'<style.*>[\s\S]*?<\/style>'

class KawnPreprocessor:
    """
    A Preprocessor class that cleans and preprocesses text for KAWN LLM.

    Args:

        remove_html_markup(:obj: `bool`, `optional`, defaults to :obj:`True`): Whether to remove html artfacts.

        replace_urls_emails_mentions(:obj:`bool`, `optional`, defaults to :obj:`True`): Whether to remove urls, emails and metions.

        strip_tashkeel(:obj:`bool`, `optional`, defaults to :obj:`False`): remove diacritics (FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SUKUN, SHADDA).

        strip_tatweel(:obj:`bool`, `optional`, defaults to :obj:`True`): remove tatweel '\\u0640'.

        strip_extended_arabic_and_quranic_symbols(:obj:`bool`, `optional`, defaults to :obj:`True`): remove quranic symbols like small alef and kul...

        keep_latten(:obj:`bool`, `optional`, defaults to :obj:`True`): keep word chars from Latin,

        keep_all_non_arabic_letters(:obj:`bool`, `optional`, defaults to :obj:`True`): keep word chars from languages other than arabic and English. this include numbers and word chars (for example Chinese, Japanese, Cyrillic, Greek, and Hebrew... if true this will override `keep_latten` option

        keep_emojis(:obj:`bool`, `optional`, defaults to :obj:`True`): don't remove emojis while preprocessing.

        map_hindi_numbers_to_arabic(:obj:`bool`, `optional`, defaults to :obj:`True`): Replaces hindi numbers with the corresponding Arabic one. ex: "١٩٩٥" --> "1995".

        standarize_non_traditional_ar_chars(:obj:`bool`, `optional`, defaults to :obj:`True`):change conncected arabic chars to its standard form'ﺗ': 'ت'...

        seperate_nums_and_words(:obj:`bool`, `optional`, defaults to :obj:`True`): insert whitespace between words and numbers. ex: مرحبا123 -> مرحبا 123    ex: -23.2+4 -> -23.2 +4

        seperate_nums_from_pucks(:obj:`bool`, `optional`, defaults to :obj:`False`): insert whitespace between numbers and punctuatios.   ex: -23.2+4

        seperate_words_from_pucks(:obj:`bool`, `optional`, defaults to :obj:`False`) : insert whitespace between punctuations and letters or numbers next to them.
        Arabic Example: مرحباً، بكم -> مرحباً ، بكم
        English: can contatin some puncks like `it's` or `pre-process` or `Mr.`  ex: hello Dr. Who this is english text, it's nice to pre-process -> hello Dr. Who this is english text , it's nice to pre-process

        remove_non_digit_repetition(:obj:`bool`, `optional`, defaults to :obj:`True`): replace repetition of more than 2 non-digit character with 2 of this character.

    Returns:

        KawnPreprocessor: A preprocessor instance

    Example:

        kawn_prep = KawnPreprocessor()

        kawn_prep.preprocess("SOME ARABIC TEXT")
    """

    def __init__(
        self,
        remove_html_markup: bool = True,
        replace_urls_emails_mentions: bool = True,
        strip_tashkeel: bool = False,
        strip_tatweel: bool = True,
        strip_extended_arabic_and_quranic_symbols: bool = True,
        keep_latten: bool = True,
        keep_all_non_arabic_letters: bool = True,
        keep_emojis: bool = True,
        map_hindi_numbers_to_arabic: bool = True,
        standarize_non_traditional_ar_chars: bool = True,
        seperate_nums_and_words: bool =True,
        seperate_nums_from_pucks: bool =False,
        seperate_words_from_pucks: bool = False,
        remove_non_digit_repetition: bool = True,

    ):

        #initialize pattern
        to_keep_pattern = ACCEPTED_NON_LETTER_OR_NUMBER

        self.remove_html_markup = remove_html_markup
        self.replace_urls_emails_mentions = replace_urls_emails_mentions
        self.strip_tatweel = strip_tatweel
        self.map_hindi_numbers_to_arabic = map_hindi_numbers_to_arabic
        self.seperate_nums_and_words = seperate_nums_and_words
        self.seperate_nums_from_pucks = seperate_nums_from_pucks
        self.seperate_words_from_pucks = seperate_words_from_pucks
        self.remove_non_digit_repetition = remove_non_digit_repetition
        self.map_hindi_numbers_to_arabic = map_hindi_numbers_to_arabic
        self.standarize_non_traditional_ar_chars = standarize_non_traditional_ar_chars


        if not strip_tashkeel:
          to_keep_pattern += HARAKA_PATTERN


        if not strip_extended_arabic_and_quranic_symbols:
          to_keep_pattern += EXTENDED_ARABIC_LETTER_PATTERN
        else:
          to_keep_pattern += ARABIC_LETTER_PATTERN

        if keep_all_non_arabic_letters:
          to_keep_pattern += ALL_LETTERS_AND_NUMBERS

        if keep_latten and not keep_all_non_arabic_letters:
          to_keep_pattern += LATTEN_LETTER_PATTERN

        if keep_emojis:
          to_keep_pattern += EMOJI_PATTERN

        if map_hindi_numbers_to_arabic: #this means only arabic chars are accepted
          to_keep_pattern += ARABIC_NUMBER_PATTERN
        else:
          ALL_NUMBER_PATTERN


        # rejected chars are:
        self.REJECTED_CHARS_REGEX = r"[^" + to_keep_pattern + r"]"

    def preprocess(self, text: str) -> str:
        """
        Preprocess takes an input text line an applies the same preprocessing used in kawn
                            pretraining, or according to settings

        Args:

            text (:obj:`str`): inout text string

        Returns:

            string: A preprocessed string depending on settings
        """
        text = str(text)
        text = html.unescape(text)


        if self.replace_urls_emails_mentions:
            for reg in URL_REGEXES:
                text = re.sub(reg, "", text)
            for reg in EMAIL_REGEXES:
                text = re.sub(reg, "", text)
            text = re.sub(USER_MENTION_REGEX, "", text)


        if self.remove_html_markup:
            # remove html line breaks
            text = re.sub(SCRIPT_TAGS, "",text)
            # remove html line breaks
            text = re.sub(STYLE_TAGS, "",text)
            # remove html line breaks
            text = re.sub("<br />", " ", text)
            # remove html markup
            text = re.sub("</?[^>]+>", " ", text)


        if self.strip_tatweel:
          text = re.sub(TATWEEL_PATTERN, "", text)

        if self.standarize_non_traditional_ar_chars:
            text = text.translate(ARABIC_MAP)
        else:
          if self.map_hindi_numbers_to_arabic:
              text = text.translate(HINDI_TO_ARABIC_MAP)

        # remove repeated characters >2
        if self.remove_non_digit_repetition:
            text = self._remove_non_digit_repetition(text)

        if self.seperate_nums_and_words:
          text = regex.sub(r"([\p{L}}ًٌٍَُِْ]+)([\p{N}]+)", r"\1 \2", text) #letters connceted to nums
          text = regex.sub(r"([\p{N}]+)([\p{L}}ًٌٍَُِْ]+)", r"\1 \2", text) #nums conncected to letters
          text = regex.sub(r"(?<num1>("+NUMBER_WITH_FLOATING_POINT+"))(?<num2>("+NUMBER_WITH_FLOATING_POINT_STARTS_WITH_NON_DIGIT+"))",  r"\g<num1> \g<num2>", text) #nums conncected to nums

        if self.seperate_nums_from_pucks:
          text = regex.sub(r"(?<punc>["+ACCEPTED_NON_LETTER_OR_NUMBER_NO_DOT_PLUSE_MINUS_SPACE+"]+)(?<num>("+NUMBER_WITH_FLOATING_POINT+"))", r"\g<punc> \g<num>", text) #numbers connceted to punks
          text = regex.sub(r"(?<num>("+NUMBER_WITH_FLOATING_POINT+"))(?<punc>["+ACCEPTED_NON_LETTER_OR_NUMBER_NO_DOT_PLUSE_MINUS_SPACE+"]+)", r"\g<num> \g<punc>", text) #punks connceted to numbers


        if self.seperate_words_from_pucks:
          #arabic words
          text = regex.sub(r"(?<punc>["+ACCEPTED_NON_LETTER_OR_NUMBER_NO_SPACE+"]+)(?<word>["+EXTENDED_ARABIC_LETTER_PATTERN+"]+)", r"\g<punc> \g<word>", text) #numbers connceted to punks
          text = regex.sub(r"(?<word>["+EXTENDED_ARABIC_LETTER_PATTERN+"]+)(?<punc>["+ACCEPTED_NON_LETTER_OR_NUMBER_NO_SPACE+"]+)", r"\g<word> \g<punc>", text) #punks connceted to numbers
          #latin words
          text = regex.sub(r"(?<punc>["+ACCEPTED_NON_LETTER_OR_NUMBER_NO_Apostrophe_Hyphen_DOT_Underscore_SPACE+"]+)(?<word>["+LATTEN_LETTER_PATTERN+"]+)", r"\g<punc> \g<word>", text) #numbers connceted to punks
          text = regex.sub(r"(?<word>["+LATTEN_LETTER_PATTERN+"]+)(?<punc>["+ACCEPTED_NON_LETTER_OR_NUMBER_NO_Apostrophe_Hyphen_DOT_Underscore_SPACE+"]+)", r"\g<word> \g<punc>", text) #punks connceted to numbers

        # remove unwanted characters
        text = re.sub(self.REJECTED_CHARS_REGEX, "", text)
        #this is from emojis
        text = text.replace("\uFE0F", "")

        # remove extra spaces, but keeping new lines and tabs

        text = '\n'.join(['\t'.join([' '.join(sub_sent.split()).strip() for sub_sent in sent.split('\t')]) for sent in text.split('\n') if not self._is_small_sent(sent)])

        return text



    def _remove_non_digit_repetition(self, text: str) -> str:
        """
        :param text:  the input text to remove elongation
        :return: delongated text
        """
        text = MULTIPLE_CHAR_PATTERN.sub(r"\1\1", text)
        return text


    def _is_small_sent(self, sentence: str) -> bool:
        """
        :param sentence:  a sentence
        :return: True if the senentence is less than three chars
        """
        return len(sentence) < 3


