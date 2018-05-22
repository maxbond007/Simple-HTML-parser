# -*- coding: utf-8 -*-
# -*- version: Python 3.6.3 -*-
"""
Created on Thu Apr 19 2018

@author: Maxim Bondarenko
"""

import os
import sys
import logging
import argparse
import urllib.request
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logging.info("Program started")


def createParser():
    """
    This function create parser by 'argparse' module

    Returns:
        expected parameter in the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', nargs='?',
                        default='https://www.phonexia.com/en/')
    return parser


def parser():
    """
    This function load of the webpage HTML and parse HTML script after that
    preprocess, separate and transfer of each line as a new sentence

    Returns:
        the set of sentences where each line as a new sentence

    Raises:
        Exception: Wrong URL!
    """
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    try:
        # loading of the webpage HTML
        webpage = urllib.request.urlopen(namespace.url)
    except Exception:
        logging.warning(u'Wrong URL')
        return "Wrong URL!"

    list_html = webpage.read()
    htmlStr = list_html.decode("utf8")
    soup = BeautifulSoup(htmlStr, "lxml")  # Parsing of the HTML script

    for script in soup("script"):
        script.extract()  # remove tag("script") from the soup

    dirty_text = soup.get_text()
    lines = (line.strip() for line in dirty_text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def main():
    """
    Writing result to the file
    """
    filename = 'text_from_html.txt'
    filepath = input(u'Please, enter an address of a directory ' +
                     u'to save the output data or \npress enter ' +
                     u'to save it in the current working directory' +
                     u'\nNew directory: ')

    fullpath = os.path.join(filepath, filename)
    my_file = open(fullpath, 'w', encoding='utf-8')
    my_file.write(parser())

    my_file.close()
    logging.info(u'The result is in a file called text_from_html.txt')


if __name__ == "__main__":
    main()
    