import regex

import cld3
from string import punctuation

EMOJI_UNICODE_LIST = regex.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251" 
    "]"
)  # Thanks mgaitan again...

ayo = "Ｇ G"
print(ayo.lower())
test_mixed_string = "alright a:_hic:ayaya🎶🎶:_booooottommm:🎶🎶:_peko::_bottom_left:💩" \
                    "USS Enterprise:bottom_left:aaaaa:_cute_sheep_:"
only_emotes_emoji = ":_hic::_peko::_tea::_bottomleft:😛😛😛😛"
emote_extraction = r"(:_?\w+_?:)"
japanese_characters = "「日本」あいつやっちゃったか？"
emotes_list = regex.findall(emote_extraction, japanese_characters)
emoji_list = regex.findall(EMOJI_UNICODE_LIST, japanese_characters)
print(emoji_list)

COMMENTS_MIXED_EMOTES_PATTERN = r"(?=(:_?\w+_?:))"
if regex.search(COMMENTS_MIXED_EMOTES_PATTERN, only_emotes_emoji):
    print("KEK")

if regex.search(EMOJI_UNICODE_LIST, only_emotes_emoji):
    print("TROLLOPS")


for emote in emotes_list:
    only_emotes_emoji = regex.sub(emote, " ", only_emotes_emoji)
for emoji in emoji_list:
    only_emotes_emoji = regex.sub(emoji, " ", only_emotes_emoji)
print(emotes_list, emoji_list)
print(len(only_emotes_emoji))
print(only_emotes_emoji.split())

random_stuff = "\u2197\u2197\u2197\u2197\u2197"
print(regex.search(EMOJI_UNICODE_LIST, random_stuff))
random_stuff = "\u0400"
CYRILLIC_UNICODE_LIST = regex.compile(
    "["
    "\u0400-\u04ff"
    "\u0500-\u052f"
    "]"
)
slavic_text = "\u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430"
print(regex.findall(CYRILLIC_UNICODE_LIST, slavic_text))
print("\U000027B0")

EXTENDED_PUNCTUATION = regex.compile(
    "["
    "\u2000-\u206f"
    "]"
)
# This thing is going to take forever to regex, so no use.
CJK_CHARS = regex.compile(
    "["
    "\u2e80-\u2eff"  # CJK Radicals Supplement
    "\u2f00-\u2fdf"  # Kangxi Radicals
    "\u3000-\u303f"  # CJK Symbols and Punctuation
    "\u3040-\u309f"  # Hiragana
    "\u30A0-\u30ff"  # Katakana
    "\u31f0-\u31ff"  # Katakana Phonetic Extensions
    "\u3200-\u32ff"  # Enclosed CJK Letters and Months
    "\u3300-\u33ff"  # CJK Compatibility
    "\u3400-\u4dbf"  # CJK Unified Ideographs Extension A
    "\u4e00-\u9fff"  # CJK Unified Ideographs
    "\U00020000-\U0002A6DF"  # CJK Unified Ideographs Extension B
    "\U0002F800-\U0002FA1F"  # CJK Compatibility Ideographs Supplement
    "\u3130-\u318f"  # Hangul Compatibility Jamo
    "\uac00-\ud7af"  # Hangul Syllables
    "]"
)
print("\U00020000")
cjk_chars = "あ "
print(f"\u30a2 {cjk_chars}")
print(regex.match(cjk_chars, cjk_chars))
ayayaya = "I'm a person. I'm not a robot, mah guy."
print(''.join(nani.strip(punctuation) for nani in ayayaya))
print(cld3.get_language("🕳"))
