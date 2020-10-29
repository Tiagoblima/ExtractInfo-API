import json
import os
import random

import fitz
import spacy
from numpy import mean
from sumy.summarizers.text_rank import TextRankSummarizer

from util import PATH_TO_MODEL
from util.summarization import summarize_batch


class DocInfo:
    """
    The class wraps the information about the text
    """

    def __init__(self, text, summary, annotations):
        self.text = text
        self.summary = summary
        self.annots = annotations


class ExtractInfo:
    """
    Class extract main information from a pdf file.
    The information includes: extractive summarization and NER.
    """

    def __init__(self, path_to_pdfs,
                 text_summarizer=None,
                 spacy_model=None):

        """
         Class extract main information from a pdf file.
         The information includes: extractive summarization and NER.
        :param path_to_pdfs: It must be the dir containing the pdfs files
        :param text_summarizer: A compatible text summarizer, if not defined TextRank will be used
        :param spacy_model: a spacy model to find the NER annotation, if None the default will be loaded from disk
        """
        self.texts = []
        self.origin_dir = path_to_pdfs
        self.docs = []
        if text_summarizer:
            self.summarizer = text_summarizer
        else:
            self.summarizer = TextRankSummarizer
        if spacy_model:
            self.spacy_model = spacy.load(spacy_model)
        else:
            self.spacy_model = spacy.load(PATH_TO_MODEL)
        self.summaries = []
        self.annots = []
        self.load_pdfs()

    def load_pdfs(self):
        """
         Load all documents as pyMufPDF documents
        :return: the documents as pyMufPDF documents
        """
        for pdfs in os.listdir(self.origin_dir):
            self.docs.append(fitz.Document(os.path.join(self.origin_dir, pdfs)))
        return self.docs

    def get_texts(self):
        """
        Retrieve the text from the pdfs documents
        :return: a list of pdf documents
        """
        for doc in self.docs:
            text_doc = []
            for page in doc.pages():
                text_doc.append(page.getText())
            self.texts.append('\n'.join(text_doc))
        return self.texts

    def get_summary(self, sent_count=None):
        """
        Summarize all the text from the pdfs using the summarizer defined in the __init__ method
        :param sent_count: The number of sentence which must be retrieved if it's None,
                            it will get a random number between 1 and 3 and multiplied by
                            the mean of text lengths
        :return: all text summaries
        """
        if sent_count is None:
            lens = [len(text) for text in self.texts]
            sent_count = int(mean(lens) * (random.choice(range(1, 4)) / 10))

        self.summaries = list(summarize_batch(self.texts, sent_count, self.summarizer))
        return self.summaries

    def save_annotations(self):
        """
         Makes NER annotation in the
        :return: all annotation in the JSONL format.
        """

        docs = self.spacy_model.pipe(self.texts)
        self.annots = []
        try:
            os.remove('Resources/annotations.jsonl')
        except OSError:
            pass
        annotation_file = open('Resources/annotations.jsonl', 'a', encoding='utf-8')
        for doc in docs:
            annotation = {"text": doc.text, "labels": []}
            for ent in doc.ents:
                annotation["labels"].append([ent.start, ent.end, ent.label_])
            self.annots.append(annotation)

            json.dump(annotation, annotation_file)
            annotation_file.write('\n')
        return self.annots

    def run_pipe(self):
        """
        Run the pipe extracting all the information from the pdfs
        :return:
        """
        self.get_texts()
        self.get_summary()
        self.save_annotations()

        for i in range(len(self.texts)):
            yield DocInfo(self.texts[i], self.summaries[i], self.annots[i])
