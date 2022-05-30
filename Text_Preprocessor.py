import os, re, string

# Natural Language Processing Libraries
try: import nltk
except: os.system("pip3 install nltk")
# nltk.download("stopwords")
# nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
wnl = WordNetLemmatizer()

from textblob import TextBlob


def multiple_replace(conversions : dict, text : str):
    """Multiple Replacements using REGEX
        ================================
    """
    regex = re.compile("(%s)" % "|".join(map(re.escape, conversions.keys())))
    return regex.sub(lambda mo: conversions[mo.string[mo.start():mo.end()]], text)




class Text_Processor:
    """Text Processor
        =============
        Provides Functions which can perform text preprocessing steps to make the data Model-ready
    """
    
    stop_words_dict = dict.fromkeys(stopwords.words("english"), 1)




    def __init__(self) -> None:
        pass




    def To_Long_Form(text : str):
        """Short forms to Long forms conversion
            ============
        """

        text = text.lower()
        
        conversions_1 = {
            r"shan't" : "shall not", r"can't" : "can not", r"ain't" : "are not", r"won't" : "will not", r"n't" : " not",
            r"'re" : " are", r"'s" : " is", r"'d" : " would", r"'ll" : " will", r"'ve" : " have",
            r"'m" : " am", r"'cause" : "because", r"o'clock" : "of the clock", r"ma'am" : "madam",
        }
        
        conversions_2 = { r"'y" : " you", r"y'd" : " you would", r"y'" : " you " }
    
        text = multiple_replace(conversions_1, text)
        text = multiple_replace(conversions_2, text)
        text = re.sub(' i ', ' I ', ' ' + text + ' ')
        text = re.sub('\s+', ' ', text).strip()

        return text




    def POS_Lemmatize(text : str):
        """Lemmatization
            ============
            (with appropriate pos tags)
        """

        def pos_tagger(nltk_tag : str):
            POS_Types = { 'J' :  wordnet.ADJ, 'V' :  wordnet.VERB, 'N' :  wordnet.NOUN, 'R' :  wordnet.ADV }
            for PType in POS_Types:
                if nltk_tag.startswith(PType):
                    return POS_Types[PType]
            return None

        pos_tagged = nltk.pos_tag(word_tokenize(text))

        # print(pos_tagged, '\n', '-'*100)
        wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
        # print(wordnet_tagged, '\n', '-'*100)

        lemmatized_sentence = []
        for word, tag in wordnet_tagged:
            if tag is None: lemmatized_sentence.append(word)
            else: lemmatized_sentence.append(wnl.lemmatize(word, tag))

        lemmatized_sentence = " ".join(lemmatized_sentence)

        return lemmatized_sentence




    def CTL_Text(text : str, Numbers : bool = False, Cap_Alphas : bool = False, Small_Alphas : bool = False,
            Punctuations : bool = False, HashTags_Mentions_Urls_Emails : bool = False,
            Multi_Space : bool = True, New_Lines : bool = False, StopWords : bool = False, Lemmatize : bool = True) -> str:
        """Clean -> Tokenize -> Lemmatize Text
            =======

            Set Attributes to True which should be Cleaned or should be Performed
        """

        try:
            if not isinstance(text, str): text = str(text)
            text = text.lower().strip()


            # Remove #HashTags, @Mentions, URLs, etc
            def remove_HashTags_Mentions_Urls(text : str):
                Removals = ['http\S+\s*', 'RT|cc', '#\S+', '\S*@\S+', 'www\S+']
                text = re.sub('|'.join(Removals), "", text, flags = re.MULTILINE)
                return re.sub(r"\@\w+|\#", "", text)
            
            if not HashTags_Mentions_Urls_Emails:
                text = remove_HashTags_Mentions_Urls(text)



            # Remove Special Unicode Characters, Punctuations
            richText = []
            for char in text:
                if char != ' ' and not any(ord(char) in rang for rang in (range(48, 58), range(65, 91), range(97, 123),)):
                    continue
                    # print(f"CHAR : {char}, Unicode Value : {ord(char)}, {[ord(char) in rang for rang in (range(48, 58), range(65, 91), range(97, 123),)]}")
                    # exit(0)
                richText.append(char)
            
            text = ''.join(richText)

            # Remove Punctuations
            # if not Punctuations:
            #     text = text.translate(str.maketrans(dict.fromkeys(string.punctuation.replace("'", ''), " ")))
                
            
            # Finds >=3 same consecutive chars and converts them to 2 same consecutive chars Eg. goooooood -> good (ooooooo -> oo)
            text = re.sub(r'((\w)\2{2,})', r'\2\2', text)   
            

            # Conversion of Chat Abbreviations
            Chat_Abbreviations = {
                " gud " : " good ",
                " luv " : " love ",
                " u "   : " you ",
            }
            text = multiple_replace(Chat_Abbreviations, text)


            # Spelling Corrections
            text = str(TextBlob(text).correct())
            # textBlob.ngrams(2)
            
            
            # Short Forms to Long Forms
            text = ' '.join(re.sub("\s*'\s*", "'", text).strip().split())
            text = Text_Processor.To_Long_Form(text)
            text = re.sub("'", " ", text)


            # Remove Cts WhiteSpaces
            text = re.sub("\s+", " ", text).strip()


            # Remove Stop words
            if not StopWords:
                text = " ".join([word for word in word_tokenize(text) if not Text_Processor.stop_words_dict.get(word, 0)])


            # Lemmatizer
            if Lemmatize: text = Text_Processor.POS_Lemmatize(text)


            # Remove Cts WhiteSpaces
            text = re.sub("\s+", " ", text).strip()

            return text if text else "NA"
        
        except Exception as e:
            print(e)
            return text