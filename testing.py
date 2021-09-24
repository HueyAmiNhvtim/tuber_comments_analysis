import json

path = f"amelia_elements_freq.json"
with open(file=path) as f:
    woawoawoawoa = json.load(f)
words_freq = woawoawoawoa["words_freq"]
emotes_freq = woawoawoawoa["emotes_freq"]
emoji_freq = woawoawoawoa["emoji_freq"]

print(len(list(words_freq.keys())))
print(len(list(emotes_freq.keys())))
print(len(list(emoji_freq.keys())))