#################################################################
# FILE : ex6.py
# WRITER : Avigail zuckerman , avig1237 , 211441381
# EXERCISE : intro2cs1 ex6 2023
# DESCRIPTION: A simple program that creating moogle
# STUDENTS I DISCUSSED THE EXERCISE WITH: Meital Man, Shir Meir.
# WEB PAGES I USED: https://reshetech.co.il/python-tutorials/reading-and-writing-files-in-python
#################################################################
9 import bs4
10 import requests
11 import urllib.parse
12 import pickle
13 import copy
14 import sys
15
16
17 def creat_index_list(INDEX_FILE):
18 """
19
20 :param INDEX_FILE: the file with all the names of the pages
21 :return: list of the name
22 """
23 with open(INDEX_FILE) as all_names:
24 names = [i.rstrip('\n')for i in all_names.readlines()]
25
26 return names
27
28
29
30 def crawl(BASE_URL, INDEX_FILE, OUT_FILE):
31 """
32
33 :param BASE_URL: The basic link to the site
34 :param INDEX_FILE: The name of the page on the website
35 :param OUT_FILE:The name of the file to which we will export the dictionary
36 :return: Downloading the pages from the Internet and discovering the links between them
37 """
38 all_index = creat_index_list(INDEX_FILE)
39 big_dict = {}
40 for i in all_index:
41 small_dict = {}
42 full_url = urllib.parse.urljoin(BASE_URL, i)
43 response = requests.get(full_url)
44 html = response.text
45 for q in all_index:
46 sum = 0
47 soup = bs4.BeautifulSoup(html, "html.parser")
48 for p in soup.find_all("p"):
49 for link in p.find_all("a"):
50 target = link.get("href")
51 if target == q:
52 sum += 1
53 if sum > 0:
54 small_dict[q] = sum
55 big_dict[i] = small_dict
56 with open(OUT_FILE, 'wb') as f: #Export the dictionary to a pickle file
57 pickle.dump(big_dict, f)
58 #return big_dict
59
3
60
61 def dicts(DICT_FILE):
62 """
63
64 :param DICT_FILE: The link dictionary from the previous function
65 :return:Two dictionaries from which we will compile the main dictionary
66 """
67 with open(DICT_FILE, "rb") as f:
68 dicts = pickle.load(f)
69 r = {}
70 new_r = {}
71 for q in dicts:
72 r[q] = 1 #A dictionary with the initial values
73 new_r[q] = 0 #The base dictionary for calculations
74 return r,new_r
75
76
77 def sum_links(DICT_FILE,page):
78 with open(DICT_FILE, "rb") as f:
79 all_pages = pickle.load(f)
80 sumi = 0
81 for i in all_pages[page].values():
82 sumi += i
83 return sumi
84
85
86
87 def page_rank(ITERATIONS, DICT_FILE, OUT_FILE):
88 """
89
90 :param ITERATIONS:The number of times we will repeat the function
91 :param DICT_FILE: The link dictionary from the previous function
92 :param OUT_FILE:The name of the file to which we will export the dictionary
93 :return:Ranking web pages by importance
94 """
95 with open(DICT_FILE, "rb") as f:
96 all_pages = pickle.load(f)
97 iter = int(ITERATIONS)
98
99 dict_file = dicts(DICT_FILE)
100 end_dict = dict_file[0]
101
102 for i in range(iter):
103 mid_dict = copy.deepcopy(dicts(DICT_FILE)[1])
104 for r in mid_dict:
105 num = 0
106 for key_1, val_1 in all_pages.items(): # Calculation of the total number of links on the page
107 if(r in val_1):
108 summ = sum_links(DICT_FILE, key_1)
109 pre_val = end_dict[key_1]
110 float(all_pages[key_1][r])
111 if summ == 0:
112 mid_dict[r]=0
113 else:
114 rank = pre_val * val_1[r] / summ # Calculation of page value
115 num += rank
116 mid_dict[r] += num # Placement in the calculation dictionary
117 end_dict = mid_dict # Placement in the dictionary of values
118 with open(OUT_FILE, 'wb') as f: # Export the dictionary to a pickle file
119 pickle.dump(end_dict, f)
120
121
122
123
124
125 def words_dict(BASE_URL,INDEX_FILE,OUT_FILE):
126 """
127
4
128 :param BASE_URL: The basic link to the site
129 :param INDEX_FILE: The name of the page on the website
130 :param OUT_FILE:The name of the file to which we will export the dictionary
131 :return: A dictionary sorted by words and the number of times they appear on each page
132 """
133 index_file = creat_index_list(INDEX_FILE)
134 big_dict = {}
135 for i in index_file:
136 small_dict = {}
137 small_dict[i] = 1
138 big_url = urllib.parse.urljoin(BASE_URL, i) #Create a full URL
139 response = requests.get(big_url)
140 html = response.text
141 soup = bs4.BeautifulSoup(html, "html.parser") #Finding all the relevant texts on the page
142 for p in soup.find_all("p"):
143 content = p.text
144 chapter = content.split()
145 for q in chapter:
146 if q in big_dict and i in big_dict[q]: #Checking if the word is in the dictionary and if so, has it appeared147 big_dict[q][i] =copy.deepcopy(big_dict[q][i]+1)
148 elif q in big_dict:
149 big_dict[q][i] = 1
150 else:
151 big_dict[q] = copy.deepcopy(small_dict)
152 with open(OUT_FILE, 'wb') as f: ##Export the dictionary to a pickle file
153 pickle.dump(big_dict, f)
154 #print(big_dict["scar"])
155 #print(words_dict("https://www.cs.huji.ac.il/w~intro2cs1/ex6/wiki/", "small_index (2).txt" , "words_dict_res"))
156
157
158
159 def first_check(QUERY, WORDS_DICT_FILE):
160 """
161
162 :param QUERY: The requested words to search in the dictionary
163 :param WORDS_DICT_FILE: dictionary that maps words to pages
164 :return: A list of dictionaries containing the number of times the requested word appears on each page
165 """
166 with open(WORDS_DICT_FILE, "rb") as f:
167 word_dict = pickle.load(f)
168 pages = []
169 for i in QUERY.split():
170 if i in word_dict:
171 pages.append(word_dict[f"{i}"])
172 else:
173 continue
174 #print(pages)
175 return pages
176
177
178
179 def sec_check(QUERY, WORDS_DICT_FILE):
180 """
181
182 :param QUERY: The requested words to search in the dictionary
183 :param WORDS_DICT_FILE: dictionary that maps words to pages
184 :return: A dictionary that assigns a page to the minimum inventions of the words sought in it
185 """
186 # with open(WORDS_DICT_FILE, "rb") as f:
187 # word_dict = pickle.load(f)
188 res_pages = {}
189 pages = first_check(QUERY,WORDS_DICT_FILE)
190 # A list of dictionaries containing the number of times the requested word appears on each page
191 for i in pages[0]: # Checking if all the requested words are on the page
192 bool = True
193 lst = []
194 for q in pages:
195 if i not in q:
5
196 bool = False
197 break
198 else:
199 lst.append(q[i])
200
201 if bool == True:
202 res_pages[i] = min(lst) # Placing the values obtained in the dictionary
203 return res_pages
204
205
206
207
208 def search(QUERY, RANKING_DICT_FILE, WORDS_DICT_FILE, MAX_RESULTS):
209 """
210
211 :param QUERY: The requested words to search in the dictionary
212 :param RANKING_DICT_FILE: The rating dictionary
213 :param WORDS_DICT_FILE: dictionary that maps words to pages
214 :param MAX_RESULTS: The amount of results requested
215 :return: Number of top search results requested
216 """
217 with open(RANKING_DICT_FILE, "rb") as f:
218 rankig_file = pickle.load(f)
219 maxi = int(MAX_RESULTS)
220
221 res_page = sec_check(QUERY, WORDS_DICT_FILE) #dictionary that assigns a page to the minimum inventions of the words sough222 sort_ranks = {}
223 all_nums = []
224 all_ranks = []
225 final_ranks = {}
226 names = []
227 for i in res_page:
228 if i in rankig_file:
229 #sort_ranks[rankig_file[i]]=i
230 all_nums.append(rankig_file[i])
231 sort_ranks[i]=rankig_file[i]
232 all_nums.sort(reverse=True)
233 for w in all_nums[:maxi]:
234 for key, val in rankig_file.items():
235 if val == w:
236 rank = w * res_page[key] #Calculation of the weighted score of the search result
237 final_ranks[key]=rank
238 all_ranks.append(rank)
239 break
240 #final_ranks[rankig_file[w]]=rank
241 all_ranks.sort(reverse=True)
242 for q in all_ranks:
243 for key_1, val_1 in final_ranks.items():
244 if val_1==q:
245 print(key_1, q)
246 break
247 #del final_ranks[q]
248 #print(search("broom wand cape", "page_rank_res.pickle","words_dict_res","4"))
249
250
251 if __name__ == '__main__':
252 if sys.argv[1] == 'crawl':
253 crawl(sys.argv[2],sys.argv[3],sys.argv[4])
254 if sys.argv[1] == 'page_rank':
255 page_rank(sys.argv[2],sys.argv[3],sys.argv[4])
256 if sys.argv[1] == 'words_dict':
257 words_dict(sys.argv[2],sys.argv[3],sys.argv[4])
258 if sys.argv[1] == 'search':
259 search(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
260
261 #
262 # print(crawl("https://www.cs.huji.ac.il/w~intro2cs1/ex6/wiki/","names.txt","out_file.pickle"))
263 # print(page_rank(100, "out_file.pickle", "page_rank_res.pickle"))
6
264 # print(words_dict("https://www.cs.huji.ac.il/w~intro2cs1/ex6/wiki/", "small_index (2).txt" , "words_dict_res"))
265 # print(search("broom wand cape", "page_rank_res.pickle","words_dict_res","4"))