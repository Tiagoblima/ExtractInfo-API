# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Start running the tika service
import os

from preprocessing.pipes import ExtractInfo
from util import PATH_TO_PDF, PATH_TO_TEXT


def main():
    try:
        for i, filename in enumerate(os.listdir(PATH_TO_PDF)):
            os.rename(os.path.join(PATH_TO_PDF, filename), os.path.join(PATH_TO_PDF, "pdf_" + str(i)))
    except OSError:
        pass

    ex_info = ExtractInfo(PATH_TO_PDF)
    docs = ex_info.run_pipe()
    for i, doc in enumerate(docs):
        with open(os.path.join(PATH_TO_TEXT, "text_" + str(i) + '.txt'), 'w', encoding='utf-8') as f:
            f.write(doc.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
