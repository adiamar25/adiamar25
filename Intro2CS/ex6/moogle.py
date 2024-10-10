#################################################################
# FILE : math_print.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex6 2023
# DESCRIPTION: A simple program that makes a search engine...
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################

############################ IMPORTS ############################

import sys
import pickle
import bs4
import collections
import argparse
import requests
import urllib.parse
import copy

########################### FUNCTIONS ###########################


def links_amount_in_file(soup, link_to_find):
    """ A function that gets an html text, and link name, 
    returns how many times it showed there. """
    link_counter = 0
    for p in soup.find_all("p"):
        for link in p.find_all("a"):
            target = link.get("href")
            if target == link_to_find:
                link_counter += 1
    return link_counter


def remove_enter(string):
    """ A  function that gets a string, and cut 
    the "\n" chars, if there are. """
    if "\n" in string:
        string = string[:-1]
    return string


def crawl(base_url, index_file, out_file):
    """ A function that get an url, and file of relative urls, returns
        a pickle file contain a dict of the number of links from every
        site, to all the rest. """
    with open(index_file, 'r') as url_file:
        traffic_dict = {}
        file_lines = url_file.readlines()
        for line in file_lines:
            line = remove_enter(line)
            full_url = urllib.parse.urljoin(base_url, line)
            response = requests.get(full_url)
            html = response.text
            soup = bs4.BeautifulSoup(html, 'html.parser')
            inner_dict = {}
            for line2 in file_lines:
                line2 = remove_enter(line2)
                link_counter = links_amount_in_file(soup, line2)
                if link_counter > 0:
                    inner_dict[line2] = link_counter
            traffic_dict[line] = inner_dict
    with open(out_file, 'wb') as f:
        pickle.dump(traffic_dict, f)


def new_dict(traff_dict):
    """ A function that gets a dict, and 
        trasform all its value to 0. """
    dict = {}
    for key in traff_dict.keys():
        dict[key] = 0
    return dict


def tot_link_amount(page, traff_dict):
    """A function gets a page name and a dict, 
        and returns the sum of the keys in the inner dict
        that reffered by dict[page]. """
    counter = 0
    for key in traff_dict[page].keys():
        counter += traff_dict[page][key]
    return counter


def page_rank(iterations, dict_file, out_file):
    """ gets an iteration number, links dict file and return
        a pickle file contains a ranking dict. """
    r = {str: float}
    iterations = int(iterations)
    with open(dict_file, "rb") as f:
        traffic_dict = pickle.load(f)
    for page in traffic_dict.keys():
        r[page] = 1
    curr_iterations = 0
    while curr_iterations < iterations:
        new_r = new_dict(traffic_dict)
        for key in traffic_dict.keys():
            key_link_amount = tot_link_amount(key, traffic_dict)
            for inner_key in traffic_dict[key].keys():
                new_r[inner_key] += r[key] * \
                    (traffic_dict[key][inner_key] / key_link_amount)
        r = new_r
        curr_iterations += 1
    with open(out_file, 'wb') as f:
        pickle.dump(r, f)


def html_text(base_url, relative_url):
    """ A function that download an html code to python. """
    relative_url = remove_enter(relative_url)
    full_url = urllib.parse.urljoin(base_url, relative_url)
    response = requests.get(full_url)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup


def html_to_text(html_code):
    """ A function that convert a givven html code to text. """
    content = ''
    for p in html_code.find_all("p"):
        content += ' ' + p.text
    return content


def words_dict(base_url, index_file, out_file):
    """ A function that gets a base_url a file contains relative urls, returns
        a dict contain a dict' which maps all the words from all the sites
        to its amount of total apperance in every site. """
    with open(index_file, 'r') as url_file:
        words_dict = {}
        file_lines = url_file.readlines()
        content_list = []
        for line in file_lines:
            line = remove_enter(line)
            soup = html_text(base_url, line)
            content = html_to_text(soup)
            content_list = content.split()
            for word in content_list:
                if word not in words_dict.keys():
                    words_dict[word] = {line: 1}
                else:
                    if line not in words_dict[word].keys():
                        words_dict[word][line] = 1
                    else:
                        words_dict[word][line] += 1
    with open(out_file, 'wb') as f:
        pickle.dump(words_dict, f)


def create_dict_of_lists(list1, list2):
    """ A function that gets to list and unite them to a dict,
        the i index's elemnt from list1 is the key, 
        and from list2 is the value. """
    united_dict = {}
    for i in range(len(list1)):
        for j in range(len(list2)):
            if i == j:
                united_dict[list1[i]] = list2[j]
    return united_dict




def search(query, ranking_dict_file, words_dict_file, max_results):
    """ A function get a query string, a ranking dict file, a words dict file,
        returns the relevant results by some  actions. """
    max_results = int(max_results)
    with open(ranking_dict_file, "rb") as f:
        ranking_dict = pickle.load(f)
    with open(words_dict_file, "rb") as f2:
        real_words_dict = pickle.load(f2)
    query_list = query.split()
    actual_query_list = []
    for word in query_list:
        if word in real_words_dict.keys():
            actual_query_list.append(word)
    apperance_dict = new_dict(ranking_dict)
    for query_word in actual_query_list:
        for site in ranking_dict.keys():
            if site in real_words_dict[query_word].keys():
                apperance_dict[site] += 1
    relevant_sites = []
    for site in apperance_dict.keys():
        if apperance_dict[site] == len(actual_query_list):
            relevant_sites.append(site)
    rel_ranking_dict = {}
    for site in relevant_sites:
        rel_ranking_dict[site] = ranking_dict[site]
    sorted_ranking_list = sorted(rel_ranking_dict.values(), reverse=True)
    i = 0
    final_sites_dict = {}
    for rank in sorted_ranking_list:
        if i < max_results:
            for key in rel_ranking_dict:
                if rel_ranking_dict[key] == rank:
                    final_sites_dict[key] = rank
        i += 1
    total_rank = {}
    for site in final_sites_dict.keys():
        min_reps = real_words_dict[actual_query_list[0]][site]
        for query_word in actual_query_list:
            if real_words_dict[query_word][site] < min_reps:
                min_reps = real_words_dict[query_word][site]
            rel_rank = final_sites_dict[site]
            total_rank[site] = min_reps * rel_rank
    sorted_rank = sorted(total_rank.values(), reverse=True)
    final_results = {}
    for rank in sorted_rank:
        for key in total_rank.keys():
            if total_rank[key] == rank:
                final_results[key] = rank
    page_sorted_list = []
    for key in final_results.keys():
        page_sorted_list.append(key)
    for i in range(len(page_sorted_list)):
        print(page_sorted_list[i], sorted_rank[i])

    '''for rank in sorted_rank:
        for key in total_rank.keys():
            if total_rank[key] == rank:
                print(key, rank)'''


if __name__ == '__main__':

    if sys.argv[1] == "crawl":
        crawl(sys.argv[2], sys.argv[3], sys.argv[4])

    if sys.argv[1] == "page_rank":
        page_rank(sys.argv[2], sys.argv[3], sys.argv[4])

    if sys.argv[1] == "words_dict":
        words_dict(sys.argv[2], sys.argv[3], sys.argv[4])

    if sys.argv[1] == "search":
        search(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
