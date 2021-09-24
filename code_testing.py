import regex
# TO-DO: TEST THE EMOJI REGEX PATTERN.


# FIRST STAGE CATEGORIZATION:
EMOTES_SPAM_PATTERN = r"^(:_?\w+_?:)+$"  # First conditional
EMOJI_SPAM_PATTERN = regex.compile(
    "^["
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
    "]+$")  # Thanks mgaitan... SECOND ELIF

# That also includes comments mixed with both EMOJIS AND EMOTES... THIRD ELIF
COMMENTS_MIXED_EMOTES_PATTERN = r"(?=(:_?\w+_?:))"
# This will be the elif after the above pattern fails to detect emote... FOURTH ELIF
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


test_string = "The quick brown fox jumps over the lazy dog 💩💩:_hic:"
test_list = test_string.split(" ")
test_string_emoji = "💩💩"

# 2ND STAGE CATEGORIZATION:
emote_extraction = r"(:_?\w+_?:)"

test_mixed_string = "alright a:_hic:ayaya🎶🎶:_booooottommm:🎶🎶:_peko::_bottom_left:💩USS Enterprise:bottom_left:aaaaa:_cute_sheep_:"
# ONLY EMOJI AND EMOTES TESTING.......
test_emoji_emotes = "🎶🎶💩🎶🎶💩:_hic::_bottomleft::_bigS:🎶💩"
# ONLY EMOTES:
only_emotes = ":_hic::_peko::_peko::_peko:"
ayy = regex.findall(emote_extraction, test_mixed_string)
lmao = regex.findall(EMOJI_UNICODE_LIST, test_mixed_string)
gura = regex.findall(emote_extraction, test_emoji_emotes)
ame = regex.findall(EMOJI_UNICODE_LIST, test_emoji_emotes)
peko = regex.findall(emote_extraction, only_emotes)
print(ayy, lmao)
print(gura, ame)
print(peko )

#print(test_list)
#print(list(test_mixed_string))


# EMOJI TESTING...........
test_emoji = "USS Enterprise USS Yorktown USS Hornet 🎶🎶💩"
emoji_list = regex.findall(EMOJI_UNICODE_LIST, test_emoji)
print(emoji_list)


