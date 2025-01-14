"""
SCHATSI004:

####004.001: Read Ranking

######## 004.001.001: Register every term

- register every existing term in the text
- Bigrams: Register every useful phrase with two words, e.g. 'Artifical Intelligence', 'Data Science',...
- Trigrams: Register every useful phrase with three words, e.g. 'Internet of things',...

For this tasks use filter to delete unuseful terms, like filling words (of, the, otherwise,...), or bigrams and
trigrams, which don't make any sense, for example 'on the road', 'of algorithm', 'Use of the'...

There has to be a filter for characters like '.', ',', ';', '-', '?', '!'..., so that these characters won't be
part of a word.

INPUT: string which contains the whole text from a paper
OUTPUT: a list which all terms, filtered for unuseful terms and unuseful phrases


######## 004.001.002: Ranking

INPUT: list with all terms from 004.001.001 AND Meta data table from SCHATSI003.002 (Data Cleansing)
OUTPUT: A File called "SCHATSI_terms.csv", which contains all entries for every paper in the following style

Filename (as Foreign key)   | Author    | Year  | Title     | Total Count   | Term      | Term Count
-----------------------------------------------------------------------------------------------------
example.pdf                 | Mr. M     | 1999  | Blabla    |  20345        | Pointer   | 15
example.pdf                 | Mr. M     | 1999  | Blabla    |  20345        | Stack     | 2
example.pdf                 | Mr. M     | 1999  | Blabla    |  20345        | Array     | 71
...                             ...         ...     ...         ...             ...         ...
Miller.pdf                  | Mr. X     | 2010  | MyLife    |  10000        | Pointer   | 33
Miller.pdf                  | Mr. X     | 2010  | MyLife    |  10000        | Beer      | 2
Miller.pdf                  | Mr. X     | 2010  | MyLife    |  10000        | Family member   | 45
...                             ...         ...     ...         ...             ...         ...

NOTE: The first 5 coloums are from SCHATSI_datacleansing.csv (1-4) and from SCHATSI_included.csv (5)

- For every Paper there has to be a routine for every element in the list of terms from 004.001.001, so that
the frequency of a term is counted and a line is written in the file "SCHATSI_terms.csv"
"""

import pandas as pd


def terms(text):
    word = ""
    entry = ""
    term_list = []
    i = 0

    special_chars = [' ', '\n', '\t', '.', ',', '?', '!', '%', '&', '/', '(', ')', '[', ']', '{', '}', '=', '§', '$',
                     '€', ":", ";", "|", "@", "+", "-", "*", "~", "#", "'", "_", ">", "<", "`", "´", "\"", "\'", "/"]

    # append characters to a word, until a space or a spacial char is detected -> end of the term
    while i < len(text)-1:
        if text[i] not in special_chars:
            word = word + text[i]
            i = i + 1
        elif text[i] in special_chars and word != "":
            i = i + 1
            break
        else:
            i = i + 1

        # When a word is found: the word is written into an entry and the entry is appended to a term list
        # After that the word is reseted
        # and a new word will be searched
        if word != "" and text[i] in special_chars:
            entry = word
            word = ""
            term_list.append(entry)
            entry = ""
    return term_list


def bigrams(term_list):
    bigram = []
    bigram_list = []

    # taking two terms, write them into a list called bigram and write this into bigram_list; iterate over term_list
    for i in range(0, len(term_list)-1):
        bigram.append(term_list[i])
        bigram.append(term_list[i+1])
        bigram_list.append(bigram)
        bigram = []
    return bigram_list


def trigrams(term_list):
    trigram = []
    trigram_list = []

    # taking 3 terms, write them into a list called trigram, write it into trigram_list; iterate over term_list til end
    for i in range(0, len(term_list)-2):
        trigram.append(term_list[i])
        trigram.append(term_list[i+1])
        trigram.append(term_list[i+2])
        trigram_list.append(trigram)
        trigram = []
    return trigram_list


def term_filtering(term_list, stopwords):
    # remove duplicates and filter for unuseful words
    term_list_filtered = []
    term_count_filtered = []

    # if element is not already in list and is not a stopword -> write the term into a filtered list
    for element in term_list:
        if element not in term_list_filtered and element not in stopwords:
            term_list_filtered.append(element)
    # every time a term in the list is found increase the counter +1, in the end the total number is found
    for element in term_list_filtered:
        counter = 0
        for term in term_list:
            if element == term:
                counter = counter + 1
        term_count_filtered.append(counter)

    # returning the list with the filtered single-word expressions and a list with the total number of each word
    return term_list_filtered, term_count_filtered


def bigram_filtering(bigram_list, stopwords):
    bigram_list_filtered = []
    bigram_count_filtered = []

    # filter for duplicates
    for element in bigram_list:
        if element in bigram_list_filtered:
            continue
        elif element[0] in stopwords or element[1] in stopwords:
            # filter for unuseful expression like "of the", "water is", "the road"...
            continue
        else:
            bigram_list_filtered.append(element)

    # count the total number of each term
    for element in bigram_list_filtered:
        counter = 0
        for bigram in bigram_list:
            if element == bigram:
                counter = counter + 1
        bigram_count_filtered.append(counter)

    # returning the list with the filtered bigram expressions and a list with the total number of each expression
    return bigram_list_filtered, bigram_count_filtered


def trigram_filtering(trigram_list, stopwords):
    trigram_list_filtered = []
    trigram_count_filtered = []
    # filter for duplicates
    for element in trigram_list:
        if element in trigram_list_filtered:
            continue
        elif element[0] not in stopwords and element[1] in stopwords and element[2] not in stopwords:
            # filter for unuseful expressions like: "in the end", "trust is the",....
            trigram_list_filtered.append(element)
        else:
            continue

    # count total number of each trigram expression
    for element in trigram_list_filtered:
        counter = 0
        for trigram in trigram_list:
            if element == trigram:
                counter = counter + 1
        trigram_count_filtered.append(counter)

    # returning the list with the filtered trigram expressions and a list with the total number of each word
    return trigram_list_filtered, trigram_count_filtered


def ranking(functional_terms_input, terms_input):
    # local path

    # docker path
    # functional_terms_input = pandas.read_csv('/data/input/SCHATSI_functional_terms.csv', sep=';')
    # terms_input = pandas.read_csv('/data/output/SCHATSI_terms.csv', sep=';')

    # a list with all functional terms, which will be used later for the ranking
    # func = []
    # for index, row in functional_terms_input.iterrows():
    #     func.append(row['term'])

    # # finding all entries with a functional word as a term in "SCHATSI_terms.csv"
    # # And write them in the Pandas Dataframe "terms_df"
    # terms = []
    # for element in func:
    #     query_search = 'term == \"' + element + "\""
    #     term_found = terms_input.query(query_search)
    #     terms.append(term_found.values.tolist())
    #     pass
    # terms_df = pd.DataFrame(terms, columns=terms_input.columns)
    terms_df = functional_terms_input.join(terms_input.set_index('term'), on='term', how='inner')

    # preparation for building global sum of filtered words from "SCHATSI_terms.csv", for every file in the csv-file
    term_filenames_column = terms_input['filename']
    term_filenames = term_filenames_column.drop_duplicates()
    filename_list = []
    for index, value in term_filenames.items():
        filename_list.append(value)

    # global sum of FILTERED WORDS from SCHATSI_terms.csv
    global_sum = []
    # sum of FOUND FUNCTIONAL TERMS in SCHATSI_terms.csv
    sum_found_func_terms = []
    for element in filename_list:
        global_sum.append([element, 0])
        sum_found_func_terms.append([element, 0])
    global_sum_df = pd.DataFrame(global_sum, columns=['filename', 'sum_terms'])
    sum_found_func_terms_df = pd.DataFrame(sum_found_func_terms, columns=['filename', 'sum_functional_terms'])

    # fill Dataframe for global sum of filtered words for every file in "SCHATSI_terms.csv"
    for index, row in terms_input.iterrows():
        add = row['term count']
        global_sum_df.loc[global_sum_df.filename == row['filename'], 'sum_terms'] += add

    # fill dataframe for sum of functional words from "SCHATSI_functional_terms.csv" for every file in "SCHATSI_terms"
    for index, row in terms_df.iterrows():
        add = row['term count']
        sum_found_func_terms_df.loc[sum_found_func_terms_df.filename == row['filename'], 'sum_functional_terms'] += add

    # calculate the results by dividing the sum of functional terms by the global sum for each file
    merged_df = sum_found_func_terms_df.merge(global_sum_df, how='inner', on='filename')

    merged_df = merged_df.reindex(columns=['filename', 'sum_functional_terms', 'sum_terms', 'result'])
    merged_df['result'] = merged_df['sum_functional_terms'].div(merged_df['sum_terms'])

    # order them from the highest score to the smallest
    merged_df = merged_df.sort_values('result', ascending=False)

    # Drop out the Columns with the Sum of functional terms and the global sum of terms
    # merged_df.drop(['sum_functional_terms', 'sum_terms'], axis=1)
    return merged_df
