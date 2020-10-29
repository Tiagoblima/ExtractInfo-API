import os

import tika
from tika import parser

tika.initVM()

headers = {
    "X-Tika-OCRLanguage": "por"
}


def load_pdfs(path_dir=None):
    """
    Load the pdfs in a director using tika
    :param path_dir:
    :return:
    """

    if path_dir is None:
        path_dir = os.curdir
    pdfs = []

    for filename in os.listdir(path_dir):
        results = parser.from_file(os.path.join(path_dir, filename), headers=headers)

        pdfs.append(results['content'].strip())
    return pdfs
