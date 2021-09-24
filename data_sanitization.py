import json
import regex  # The original module I use
import re
import time
import operator
from string import punctuation
# TO-DO: THE PUNCTUATION IS NOT ENOUGH TO ELIMINATE ALL OF THE SYMBOLS...
#        DONE BY GOING THROUGH ANOTHER ROUND OF CHECKING FOR EXTENDED UNICODE LIST


class DataSanitization:
    """Clean up the data from the json files"""
    def __init__(self, *streamers):
        self.emotes_list = []
        self.emoji_list = []
        self.comments_list = []
        self.useless_list = []
        self.streamers = streamers
        self.COMMENTS_MIXED_EMOTES_PATTERN = r"(?=(:_?\w+_?:))"
        self.EMOTES_EXTRACTION_PATTERN = r"(:_?\w+_?:)"
        self.EMOJI_UNICODE_LIST = re.compile(
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
            "\U00002701-\U000027BF"  # Dingbats
            "\U000024C2-\U0001F251"  # I have no idea what it contains but I'm too afraid to touch it.
            "]"
        )
        self.CJK_CHARS = re.compile(
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
        self.UNICODE_ARROW = re.compile('[\u2190-\u21FF]')

        self.CYRILLIC_UNICODE_LIST = re.compile(
            "["
            "\u0400-\u04ff"
            "\u0500-\u052f"
            "]")

        self.PUNCTUATION = punctuation
        self.EXTENDED_PUNCTUATION = re.compile(
            "["
            "\u2000-\u206f"
            "]"
        )
        self.counter = 0

    def go_thru_streamers(self):
        for streamer in self.streamers:
            print(f"Making frequency dictionaries for {streamer.title()}...")
            self.load_file_path(name=streamer)
            # Restart...
            self.emotes_list = []
            self.emoji_list = []
            self.comments_list = []
            self.useless_list = []
            self.counter = 0
            time.sleep(10)

    def load_file_path(self, name):
        LIVE_FILE_PATH = f"streamer_comments/{name}/live"
        FILE_SAVE_PATH = f"{name}_elements_freq.json"
        for i in range(0, 30):
            comments_list = self.list_dictionaries_keys(name=name, file_path=LIVE_FILE_PATH, index=i)
            self.live_chat_categorization(comments=comments_list)
        list_o_words = self.words_combiner(self.comments_list)
        words_freq = self.frequency_dict(group=list_o_words)
        emotes_freq = self.frequency_dict(group=self.emotes_list)
        emoji_freq = self.frequency_dict(group=self.emoji_list)
        streamer_comm_freq = {
            "words_freq": words_freq,
            "emotes_freq": emotes_freq,
            "emoji_freq": emoji_freq
        }
        with open(file=FILE_SAVE_PATH, mode="w") as f:
            json.dump(streamer_comm_freq, f)

    def list_dictionaries_keys(self, name, file_path, index):
        """There is a reason why I have to keep each comment a dictionary on its own in the list
        . It is to prevent the duplicate keys problems in dictionary."""
        file_path = file_path + f"/{name}_LC_#{index}.json"
        comments_list = []
        with open(file_path, mode="r") as f:
            live_chat_list = json.load(f)
        for comment in live_chat_list:
            comments_list.append(list(comment.keys())[0])
        return comments_list

    def live_chat_categorization(self, comments: list):
        """Categorize all the comments into 3 groups: COMMENTS_LIST, EMOJI, EMOTES"""
        comments_list = comments
        for comment in comments_list:
            self.counter += 1
            print(self.counter)
            if re.search(self.CJK_CHARS, comment):
                comment = self.extract_and_sub(comment, pattern=self.CJK_CHARS, group_list=self.comments_list, replacement="")
            # Ngl, this is too much for little gain...
            if re.search(self.CYRILLIC_UNICODE_LIST, comment):
                comment = self.extract_and_sub(comment, pattern=self.CYRILLIC_UNICODE_LIST, group_list=self.comments_list, replacement="")
            if re.search(self.COMMENTS_MIXED_EMOTES_PATTERN, comment):
                comment = self.extract_and_sub(comment, pattern=self.EMOTES_EXTRACTION_PATTERN, group_list=self.emotes_list)
            if re.search(self.EMOJI_UNICODE_LIST, comment):
                comment = self.extract_and_sub(comment, pattern=self.EMOJI_UNICODE_LIST, group_list=self.emoji_list)
            if re.search(self.UNICODE_ARROW, comment):
                comment = self.extract_and_sub(comment, pattern=self.UNICODE_ARROW, group_list=self.emoji_list)
            if comment.strip() != "":
                if re.search(self.EXTENDED_PUNCTUATION, comment):
                    comment = self.extract_and_sub(comment, pattern=self.EXTENDED_PUNCTUATION, group_list=self.useless_list, replacement="")
                self.comments_list.append(comment)

    def extract_and_sub(self, comment, pattern, group_list, replacement=" "):
        """Extract the list of matches, then remove them from the comments"""
        matches = re.findall(pattern, comment)
        # The group at the init function
        group_list += matches
        for match in matches:
            comment = re.sub(match, replacement, comment)
        return comment

    def words_combiner(self, sentences: list):
        """This and the freq dict are the only things I get from the analyzer. Even then, in this case, I have to use
        extended punctuation unicode list to eliminate non-conventional punctuations."""
        comment_string = " ".join(sentences)
        formatted_string = ""
        for i in comment_string:
            if i not in punctuation:
                formatted_string += i
        formatted_string = formatted_string.lower()
        list_o_words = formatted_string.split()
        return list_o_words

    def frequency_dict(self, group: list):
        freq_dict = {}
        for element in group:
            freq_dict[element] = freq_dict.get(element, 0) + 1
        freq_dict = dict(sorted(freq_dict.items(), key=operator.itemgetter(1), reverse=True))
        return freq_dict


if __name__ == '__main__':
    clean_up = DataSanitization("amelia", "kiara")
    clean_up.go_thru_streamers()

