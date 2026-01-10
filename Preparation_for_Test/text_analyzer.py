import os
import re
import json


class Text_Analyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""
        self.words = {}
        self.words_count = 0
        self.sentences = []
        self. sentences_count = 0
        self.paragraphs = 0
        self.most_common_word = ""
        self.longest_sentence = ""
        self.longest_sentence_words = 0
        self. avarage_word_lenght = 0
        self. exclusions = ["и", "на", "в", "с", "за", "от", "да", "е", "не", "по", "до", "се", "като"]

    def read_file(self):
        print(f"\nReading {self.file_path}(... )")
        with open(self. file_path, "r", encoding="utf-8") as file:
            self.text = file.read()
        print("Process completed successfully!")

    def count_paragraphs(self):
        print(f"\nCounting paragraphs(... )")
        paragraphs = [p for p in self.text.split("\n\n") if p.strip()]
        self.paragraphs = len(paragraphs)
        print("Process completed successfully!")

    def count_sentences(self):
        print(f"\nCounting sentences(... )")
        text_cleaned = re.sub(r'\s+', ' ', self. text.strip())
        
        sentences = re.split(r'[.!?]+', text_cleaned)
        
        self.sentences = [s.strip() for s in sentences if s.strip()]
        self.sentences_count = len(self.sentences)
        
        print(f"  → Found {self.sentences_count} sentences")
        print("Process completed successfully!")

    def count_words(self):
        print(f"\nCounting words(... )")
        
        for sentence in self.sentences:
            words = sentence.split()
            
            if len(words) > self.longest_sentence_words:
                self.longest_sentence_words = len(words)
                self.longest_sentence = sentence

            for word in words:
                clean_word = re.sub(r'[^\w\s]', '', word).lower()
                if clean_word: 
                    self.words_count += 1
                    
                    if clean_word not in self.exclusions:
                        self.words[clean_word] = self. words. get(clean_word, 0) + 1
                    
                    self.avarage_word_lenght += len(clean_word)
        
        if self.words:
            self.most_common_word = max(self.words, key=self.words.get)
        
        if self.words_count > 0:
            self.avarage_word_lenght /= self.words_count
        
        print("Process completed successfully!")

    def unique_words_percentage(self):
        print(f"\nCalculating unique words percentage(...)")
        unique_count = sum(1 for count in self.words.values() if count == 1)
        
        if self.words_count > 0:
            unique_percentage = (unique_count / self.words_count) * 100
        else: 
            unique_percentage = 0
        
        print("Process completed successfully!")
        return unique_percentage

    def analyze(self):
        self.read_file()
        self.count_paragraphs()
        self.count_sentences()
        self.count_words()
        unique_percentage = self.unique_words_percentage()

        print('\n' + '='*50)
        print("               TEXT ANALYSIS RESULTS")
        print("="*50)
        print(f"Total words: {self.words_count}")
        print(f"Total sentences: {self.sentences_count}")
        print(f"Total paragraphs: {self.paragraphs}")
        
        if self.most_common_word:
            print(f"\nMost common word: '{self.most_common_word}' ({self.words[self.most_common_word]} times)")
        
        print(f"Average word length: {self. avarage_word_lenght} characters")
        print(f"Unique words percentage:  {unique_percentage:.2f}%")
        
        if self.longest_sentence:
            print(f"\nLongest sentence:")
            print(f'  "{self.longest_sentence}"')
            print(f"  ({self. longest_sentence_words} words)")
        
        print("="*50)


    def export_to_json(self, json_file_path):
        print(f"\nExporting the text file details to {json_file_path}") 

        json_data = {
            "file_path": self.file_path,

            "statistics": {
                "total words": self.words_count,
                "total_sentences": self.sentences_count,
                "total_paragraphs": self.paragraphs,
                "avarage_word_lenght": round(self.avarage_word_lenght, 2)
            },
            
            "most_common_word":{
                "word": self.most_common_word,
                "count": len(self.most_common_word)
            },

            "longest_sentence": {
                "text": self.longest_sentence,
                "word_count": self.longest_sentence_words
            },

            "word_frequency": self.words
        }

        with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)

        print("Process completed successfully!")


def main():
    file_path = r"C:\Users\TheCiRa7\Desktop\VSE\Vuvedenie_V_Skriptovite_Ezici\Preparation_for_Test\test.txt"

    if not os.path.isfile(file_path):
        print(f"Error: '{file_path}' is not a valid file!")
        return
    
    analyzer = Text_Analyzer(file_path)
    analyzer.analyze()
    analyzer.export_to_json("text_analysis.json")


if __name__ == "__main__":
    main()