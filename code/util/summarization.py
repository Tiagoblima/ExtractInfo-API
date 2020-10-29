from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk

nltk.download('punkt')
nltk.download('stopwords')

language = 'portuguese'

stemmer = Stemmer(language)


def summarize(raw_text, sentence_count, model):
    """
    The function summarizes a text string
    :param raw_text: a text string
    :param sentence_count: The number of sentences in the final summarization
    :param model: a compatible model used to summarize
    :return: the summarized
    """

    parser = PlaintextParser.from_string(raw_text, Tokenizer(language))
    summarizer = model(stemmer)
    summarizer.stop_words = get_stop_words(language)

    summary = []
    for sentence in summarizer(parser.document, sentence_count):
        summary.append(str(sentence) + '\n')

    return ''.join(summary)


def summarize_batch(raw_text_list, sentence_count, model):
    """
    Summarizer a batch of documents
    :param raw_text_list: a list of document strings
   :param sentence_count: The number of sentences in the final summarization
    :param model: a compatible model used to summarize
    :return: all the text summarized.
    """

    for raw_text in raw_text_list:
        summary = summarize(raw_text, sentence_count, model)
        yield ''.join(summary)
