'''class Backson:
    __cache = None

    def __init__(self, val):
        self.__val = val
        self.__friend = Backson.__cache
        Backson.__cache = None

        if self.__friend is None:
            self.__friend = self
            Backson.__cache = self

    def __str__(self): return self.__val + self.__friend.__val
    
print(Backson("a"), Backson("b"), Backson("c"), Backson("d"))'''


'''def brute_search(word, text, num):
    
    counter = 0
    i = 0
    jump = len(word)
    
    while i <= (len(text)-jump):
        
        if text[i:i+jump] != word:
            i += 1
        else:
            counter += 1
            jump = len(word)
            i += jump
            
    return counter >= num


word = "xyz"
text = "xxyzxzyz"
print(brute_search(word, text, 1))'''


'''def find_range(dict_list):
    
    sorted_set = set()
    
    for dict in dict_list:
        for key in dict.keys():
            sorted_set.add(key)
            
    sorted_list = sorted(list(sorted_set))
    
    new_dict = {}
    for item in sorted_list:
        values_list = []
        for dict in dict_list:
            for key in dict.keys():
                if key == item:
                    values_list.append(dict[key])
        min_max_list = []
        min_max_list.append(min(values_list))
        min_max_list.append(max(values_list))
        new_dict[item] = min_max_list
        
    return new_dict, sorted_list
    
    
dict_list = [{'glop': 4, 'is': 7, 'best': 10}, {'glop': 2, 'best': 6}, 
             {'glop': 1, 'is': 2}, {'dippy': 2}]
print(find_range(dict_list))'''


'''def combination_lock(*args: int):
    def func(*func_args):
        is_same = True

        for arg in args:
            if arg != func_args[0]:
                is_same = False

        return func

    return func


f = combination_lock(1, 2, 3, 4)
is_same = f(1)(2)(3)(4)
print(is_same)
is_same2 = f(1)(1)(10)(4)'''


# def func(original_function):

#     def wrapper():
#         print("the wrraper has been here first")
#         return original_function()

#     return wrapper


# @func
# def foo():
#     print("and then, the original function came")

# foo()

'''class Person:
    
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
        self.__vac_num = 0
        self.__spouse = None
        
    def get_vac_num(self):
        return self.__vac_num
        
    def set_vac_num(self, new_num):
        self.__vac_num = new_num
        return None
        
    def get_age(self):
        return self.__age
        
    def get_name(self):
        return self.__name
        
    def marry(self, spouse):
        if ((spouse == None) or 
            (spouse.__spouse != self and spouse.__spouse != None) 
            or (self.__spouse != spouse and self.__spouse != None)):
            raise Exception
        else:
            self.__spouse = spouse
            spouse.__spouse = self
            
    def get_spouse(self):
        return self.__spouse
        
        
class VaccinationCenter:
    
    vaccine_total = 50

    def __init__(self, min_age):
        self.__min_age = min_age
        
    def set_age_limit(self, min_age):
        self.__min_age = min_age
        return None
        
    def give_vaccine(self, person):
        if self.is_eligible(person):
            person.set_vac_num(person.get_vac_num()+1) 
            VaccinationCenter.vaccine_total -= 1
            return True
        return False
    
    def is_eligible(self, person):
        if VaccinationCenter.vaccine_total > 0:
            if ((person.get_age() >= self.__min_age) 
                or (person.get_vac_num() > 0)):
                return True
            elif person.get_spouse() != None:
                if  person.get_spouse().get_vac_num() > 0:
                    return True
        return False
    
if __name__ == '__main__':
    
    v1 = VaccinationCenter(25)
    p1 = Person("Omer", 20)
    p2 = Person("Nitzan", 27)
    p3 = Person("Tamar", 23)
    print(v1.is_eligible(p1))
    p1.marry(p2)
    print(v1.is_eligible(p1))
    v1.give_vaccine(p2)
    print(v1.is_eligible(p1))
    v1.give_vaccine(p1)
    print(p1.get_vac_num())
    p2.marry(p1)
    p2.marry(p3)'''


# class Node:
#     def __init__(self, data, left=None, right=None):
#         self.data = data
#         self.left = left
#         self.right = right


# def find_path(root, k):
#     if not root:
#         return
#     return _helper(root, k)


# def _helper(root, k, lst = []):
#     lst.append(root.data)

#     if not root.left and not root.right:
#         if sum(lst) == k:
#             return lst
#         else:
#             return

#     if root.left:
#         new_list = _helper(root.left, k, lst[:])
#         if (new_list):
#             return new_list

#     if root.right:
#         new_list = _helper(root.right, k, lst[:])
#         if (new_list):
#             return new_list


# left = Node(2,  Node(8), Node(0, Node(9)))
# right = Node(-7, Node(5, Node(0), Node(9)), Node(4, None, Node(-3)))
# tree = Node(1, left, right)
# root = tree

# print(find_path(Node(6), 6))


'''def find_path(root, k):
    if not root:
        return
    if not root.right and not root.left:
        if root.data != k:
            return
        return [k]
    lst = []
    _helper(root, k, lst)
    
    
def _helper(root, k, lst):
    
    if not root.left and not root.right:
        if sum(lst) == k:
            return lst
        else:
            return
        
    if root.left:
        lst.append(root.left.data)
        _helper(root.left, k, lst)
    
    else:
        lst.append(root.right.data)
        _helper(root.right, k, lst)'''


'''def find_ingre(final_item, recipes, lst=[]):
    basic = True
    for recipe in recipes:
        if final_item in recipe[-1]:
            basic = False
            for ingred in recipe[0]:
                find_ingre(ingred, recipes, lst)
    if basic:
        lst.append(final_item)
    return lst


def get_ingredients(final_item, recipes):
    return set(find_ingre(final_item, recipes))


recipes = {(("water", "flour", "salt"), ("messy counter", )),
           (("frozen dough", "water"), ("dough", )),
           (("dough", "garlic"), ("garlic bread", "dirty oven")),
           (("garlic bread", "cheese"), ("sandwich", )),
           (("envelope", "paper", "stamp"), ("letter", ))}

final_item = "sandwich"

print(get_ingredients(final_item, recipes))'''


'''def find_max_prefix_sum(lst):
    
    return _helper(lst, 0, 0, 0, 0) + 1
    
    
def _helper(lst, ind, maximum, counter, i):
    
    if ind == len(lst):
        return i
    
    counter += lst[ind]
    if maximum < counter:
        i = ind 
        maximum  = counter
    return _helper(lst, ind+1, maximum, counter, i)
    

lst1 = [1, -5, 9, -12, 3, 3, 3, 2]
lst2 = [1, -5, 9, 7]
print(find_max_prefix_sum(lst1))'''


'''import string

LETTERCONVERSION = ord('a')

def letter_to_index(let):
    return ord(let) - LETTERCONVERSION
    
def index_to_letter(num):
    return chr(ord('a') + num)
    
def create_vigenere_square():
    square = list()
    alphabet_list = list(string.ascii_lowercase)
    for i in range(len(alphabet_list)):
        square.append(alphabet_list[i:] + alphabet_list[:i])
    return square
vs = create_vigenere_square()
# lst.index(element) returns the index of the given element in the list lst.
# For example, ['a', 'b', 'c'].index('c') returns the integer 2.
#### DO NOT CHANGE ANYTHING ABOVE THIS LINE! ####

def encrypt(msg, key):
    
    encrypt_msg = ""
    for i in range(len(msg)):
        if i >= len(key):
            j = ((i+1) % len(key)) - 1
        else:
            j = i
        rel_char = key[j]
        to_add = vs[letter_to_index(rel_char)][letter_to_index(msg[i])]
        encrypt_msg += to_add
        
    return encrypt_msg


def decrypt(msg, key):
    
    decrypt_msg = ""
    for i in range(len(msg)):
        if i >= len(key):
            j = ((i+1) % len(key)) - 1
        else:
            j = i
        rel_char = key[j]
        rel_ind = 0
        for ind in range(len(vs)):
            if vs[letter_to_index(rel_char)][ind] == msg[i]:
                rel_ind = ind
                break
        decrypt_msg += index_to_letter(rel_ind)
        
    return decrypt_msg
    
    
msg = "cell"
key = "beg"
dec = "dirm"

print(encrypt(msg, key))
print(decrypt(dec, key))'''


'''lst1 = [(5, 2), 0, "-7", 4, 8]
lst2 = [1, 2, 3, 4, 5]

try:
    for item in lst1:
        try:
            print((lst2[lst1.index(item)+1] // item), end = " ")
        except(TypeError): print("a", end = " ")
        except(ZeroDivisionError): print("b", end = " ")
        except(IndexError): print("c", end = " ")

except: print("e", end = " ")
finally: print("f", end = " ")'''


'''class Node:
    def __init__(self, data, left=None, right=None):
        self.data, self.left, self.right = data, left, right
### The code above was provided.

def is_legal_BST(root):
    if root is None:
        return True
    return _helper(root, True)
    
    
def _helper(root, is_tree):

    if not root.left and not root.right:
        return is_tree 
    
    if root.left:
        if root.left.data > root.data:
            is_tree = False
            
    if root.right:
        if root.right.data <= root.data:
            is_tree = False
    
    return _helper(root.left, is_tree) and _helper(root.right, is_tree)
    

BT = Node(9, Node(7, Node(5), Node(10)), Node(12, Node(8), Node(17)))
print(is_legal_BST(BT))'''


'''class cycle:
    
    def __init__(self, data):
        self.__data = data
        self.__my_cycle = [self.__data]
        self.__next = None
        self.__prev = None
        
    def insert_next(self, data):
        self.__next = data
        data_pos = self.__my_cycle.index(self.__data)
        self.__my_cycle.insert(data_pos+1, data)
        print(self.__my_cycle)
        
    def rotate(self):
        self.__prev = self.__data
        self.__data = self.__next
        next_ind = self.__my_cycle.index(self.__next)
        if next_ind == len(self.__my_cycle) - 1:
            self.__next = self.__my_cycle[0]
        else:
            self.__next = self.__my_cycle[next_ind+1]
        return self.__data
        
    def rotate_back(self):
        self.__next = self.__data
        self.__data = self.__prev
        prev_ind = self.__my_cycle.index(self.__prev)
        if prev_ind == 0:
            self.__prev = self.__my_cycle[-1]
        else:
            self.__prev = self.__my_cycle[prev_ind-1]
        return self.__data
        
    def delete(self):
        if not self.__next and not self.__prev:
            raise LookupError
        else:
            self.__my_cycle.remove(self.__data)
            self.__data = self.__next
            next_ind = self.__my_cycle.index(self.__next)
            if next_ind == len(self.__my_cycle) - 1:
                self.__next = self.__my_cycle[0]
            else:
                self.__next = self.__my_cycle[next_ind+1]
        print("my cycle: ", self.__my_cycle)
            
            
c = cycle(3)
c.insert_next(2)
c.insert_next(1)
print(c.rotate())
print(c.rotate())
print(c.rotate())
print(c.rotate())
c.delete()
print(c.rotate_back())'''


'''from typing import List


def min_time(num_workers: int, tasks: List[float]):
    return _helper([0]*num_workers, tasks, 0)


def _helper(worker_time, tasks, ind):
    if ind >= len(tasks):
        return max(worker_time)
    
    best = None
    for worker in range(len(worker_time)):
        worker_time[worker] += tasks[ind]
        if best == None or worker_time[worker] < best:
            val = _helper(worker_time, tasks, ind+1)
            if best == None or val < best:
                best = val
        worker_time[worker] -= tasks[ind]
    return best


num_workers = 4
tasks = [4, 2, 2.5, 2, 3, 5]
print(min_time(num_workers, tasks))'''


# class Node:
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next

# def linked_filter(f, lnk):

# if lnk is None:
#     return lnk

# filtered_next = linked_filter(f, lnk.next)

# if f(lnk.data):
#     return Node(lnk.data, filtered_next)
# else :
#     return filtered_next


'''new_lkd = None
    head = new_lkd
    while lnk:
        if f(lnk.data):
            new_node =  Node(lnk.data)
            if not new_lkd:
                new_lkd = new_node
                head = new_lkd
            else:
                new_lkd.next = new_node
                new_lkd = new_lkd.next
        lnk = lnk.next
    return head
    
    
f = lambda x: (x+1) % 2
lnk = Node(2, Node(3, Node(4, Node(5, Node(6)))))
excpected = Node(2, Node(4, Node(6)))
print(linked_filter(f, lnk))'''


# def f3(n, x, y):

#     if n == 0:
#         return [[]]

#     elif n == 1:
#         return [[x], [y]]

#     call = f3(n-1, x, y)
#     return [[x] + i for i in call] + [[y] + j for j in call if j[0] == x]


# f3(3, 'a', (2,))
# result1 = [ ['a', 'a', 'a'],
#             ['a', 'a', (2,)],
#             ['a', (2,), 'a'],
#             [(2,), 'a', 'a'],
#             [(2,), 'a', (2,)] ]

# print(f3(2, [3,'5'], 'xy'))
# result2 = [[[3, '5'], [3, '5']],
#            [[3, '5'], 'xy'],
#            ['xy', [3, '5']]]

# print(f3(1, [3], '9'))
# result3 = [[[3]], ['9']]


'''class Node:
    
    def __init__(self, data, next=None):
        self.data, self.next = data, next
    
    
def find_max_sum_pair(head):   
    
    max_sum = 0
    cur = head
    cur_sum = 0
    lst = []
    while cur:
        lst.append(cur.data)
        cur = cur.next
    for i in range(len(lst)):
        cur_sum += (lst[i]+lst[-i-1])
        if cur_sum > max_sum:
            max_sum = cur_sum
        cur_sum = 0
    
    return max_sum

    
lkd = Node(7, Node(1, Node(2, Node(4, Node(-3, Node(-2, Node(-1)))))))
print(find_max_sum_pair(lkd))'''


'''def xyz(num_x, num_y, num_z):
    
    result = []
    helper(num_x, num_y, num_z, result, "")
    return result

def helper(x, y, z, result, initial_str):
    
    if x == 0 and y == 0 and z == 0:
        result.append(initial_str)
        return
    
    if x > 0:
        helper(x-1, y, z, result, initial_str+"x")
    if y > 0:
        helper(x, y-1, z, result, initial_str+"y")
    if z > 0:
        helper(x, y, z-1, result, initial_str+"z")
        
        
print(xyz(2,0,1))'''


'''from typing import List, Tuple

def intersect(intervals: List[Tuple[float,float]], points: List[float])-> bool:
        intervals.sort(key = lambda x: x[1])
        points.sort()
        while True:
            if not points or not intervals:
                return False
            p = points.pop()
            s,e = intervals.pop()
            if p > e:
                intervals.append((s, e))
            elif p < s:
                points.append(p)
            else:
                return True
        
    
    
print(intersect([(1, 2), (3, 4)], [7, 3.5]))
print(intersect([(1, 2), (3, 4)], [1]))
print(intersect([(3.5, 4.5), (-1, 2), (3, 4)], [2.5, 5.5]))'''


'''class Campus:
    
    def __init__(self):
        self.dict = {}
        
    def add_classmates(self, st1, st2):
        if st1 in self.dict.keys():
            self.dict[st1].add(st2)
        else:
            self.dict[st1] = {st2}
        if st2 in self.dict.keys():
            self.dict[st2].add(st1)
        else:
            self.dict[st2] = {st1} 
            
    def soc_dist(self, st1, st2, n):
        if st1 == st2:
            return True
            
        elif st1 not in self.dict.keys() or st2 not in self.dict.keys():
            return False
            
        else:
            counter = 1
            keys_lst = list(self.dict.keys())
            vals_lst = list(self.dict.values())
            for i in range(len(keys_lst)):
                if keys_lst[i] == st1:
                    print(i)
                    ind = i
                    
            for j in range(ind, len(vals_lst)):
                if self.dict[st1] != vals_lst[j]:
                    print(vals_lst[i])
                    print(self.dict[st1])
                    counter += 1
                    print(vals_lst[i])
                else:
                    break
            print("counter:", counter)
            if counter == n:
                return True
            
        return False
                        
            
teva = Campus()
teva.add_classmates('a', 'b')
teva.add_classmates('a', 'c')
teva.add_classmates('d', 'b')
teva.add_classmates('d', 'k')
print(teva.dict)
print("a-b", teva.soc_dist('a', 'b', 1))'''


'''def gen_str(k):
    
    _helper(k, "")
    
    
def _helper(k, st):

    if len(st) >= k:
        print(st)
        return
        
    for i in range(2):
        if not st or not (int(st[-1]) == i == 1):
            st += str(i)
            _helper(k, st)
        st = st[:-1]


gen_str(3)'''


'''
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
        
        
def shift(head, k):
    cur = head
    
    for i in range(k - 1):
        cur = cur.next
    new_node = cur.next
    cur.next = None
    new_head = new_node
    while new_node.next:
        new_node = new_node.next
    new_node.next = head
    
    return new_head
    
    
    
lkd = Node(10, Node(20, Node(30, Node(40, Node(50, Node(60))))))
print(shift(lkd, 3))'''


'''from functools import reduce


def appear_at_least(words_list, k):
    
    new_dict = reduce(is_word_in_dict, words_list, {})
    words_over_k = filter(lambda x: new_dict[x] >= k, new_dict.keys())
    return set(words_over_k)
    
    # equals to: >>>
    
    # new_dict = reduce(is_word_in_dict, words_list, {})
    # words_over_k = filter(lambda x: x[1] >= k, new_dict.items())
    # words_alone = map(lambda x: x[0], words_over_k)
    # return set(words_alone)
    
    
def is_word_in_dict(dct: dict, word):
    
    if word in dct.keys():
        dct[word] += 1
        
    else:
        dct[word] = 1
        
    return dct
    
    
print(appear_at_least(["a", "b", "c", "a", "b", "b", "d"],2))'''


'''
class EditableString:
    
    def __init__(self, st):
        
        self.__st = str(st)
        self.last_action = None
        self.__args = tuple()

        
    def insert_char_at(self, char1, ind):
        
        if ind == len(self.__st):
            self.__st += str(char1)
            
        elif 0 <= ind <= len(self.__st):
            self.__st = self.__st[:ind] + str(char1) + self.__st[ind:]
            
        else:
            raise IndexError
        
        self.__last_action = self.insert_char_at
        self.__args = (char1, ind)
        
    
            
    def delete_char_at(self, ind):
        
        if 0 <= ind <= (len(self.__st) - 1):
            self.__st = self.__st[:ind] + self.__st[ind+1:]
            
        else:
            raise IndexError
        
        self.__last_action = self.delete_char_at 
        self.__args = (ind, )
            
    def redo_last_action(self):
        
        self.__last_action(*self.__args)
            
    
    def __str__(self):
        
        return self.__st
        
        
estr = EditableString("hello")
estr.insert_char_at("b", 2)
print(estr)
estr.delete_char_at(2)
print(estr)
print(estr.last_action)
estr.redo_last_action()
print(estr)
estr.insert_char_at("l", 2)
print(estr)
estr.redo_last_action()
print(estr)'''


'''def sum_non(lst):
    
    if len(lst) == 0:
        return 0
    
    elif len(lst) == 1: 
        return lst[0]
    
    return max(lst[0] + sum_non(lst[2:]), sum_non(lst [1:]))




#print(sum_non([1, 2, 3, 4]))
print(sum_non([2, 21, 8, 2, 5, 3]))'''


'''class Node:
    
    def __init__(self, data, next=None):
        self.data, self.next = data, next

    def __repr__(self):
        return repr(self.data) + "->" + repr(self.next)
   
        
def split(head, k):
    
    lst = []   
     
    while head:
        temp_lkd = head
        i = 0
        
        while i < (k-1) and head.next != None:
            head = head.next
            i += 1
        saved_head = head.next
        head.next = None
        lst.append(temp_lkd)
        head = saved_head
    
    return lst 
        
        
lst = Node(5, Node(-3, Node(8, Node (1, Node(5)))))
new_lst = split(lst, 2)
print(new_lst)'''


'''class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
        
        
class LinkedList:
    
    def __init__(self, head):
        self.__head = head
        self.__tail = None


    def is_repetative(self, lst):
        head = self.__head
        i = 0
        while head:
            if head.data != lst[i%len(lst)]:
                return False
            head = head.next
            i += 1
            
        if i % len(lst):
            return False 
        
        return True
    
    
    
lkd = Node("a", Node("b", Node("a", Node("b", Node("a", Node("b"))))))
my_list = LinkedList(lkd)
print(my_list.is_repetative(["a", "b"]))
print(my_list.is_repetative(["a", "b", "a"]))
print(my_list.is_repetative(["a", "b", "a", "b"]))
print(my_list.is_repetative(["c"]))'''


'''def has_loop(list_of_links):
    for link in list_of_links:
        cur=link
        for i in range(len(list_of_links)):
            cur = cur.next
            if not cur:
                break
        else:
            return True
    return False'''


'''def max_sum(lst1, lst2, lst3, lim):
    
    max_sum = 0
    for i in range(len(lst1)):
        for j in range(len(lst2)):
            for k in  range(len(lst3)):
                temp_sum = lst1[i] + lst2[j] + lst3[k]
                if max_sum < temp_sum <= lim:
                    max_sum = temp_sum
    return max_sum
            
    

liz1 = [9, 8, 7]
liz2 = [2, 5, 1]
liz3 = [6]
liz4 = [6, 2]
liz5 = [0]

print(max_sum(liz1, liz2, liz3, 30)) #exprcted: 20
print(max_sum(liz1, liz2, liz3, 20))  # excpected: 20
print(max_sum(liz3, liz4, liz5, 13))   # excpected: 12
print(max_sum(liz3, liz4, liz5, 7))     # excpected: 0'''


"""from math import gcd
#intentionally fails when gcd(a,b)==0
def lcm(a, b): return abs(a // gcd(a, b) * b)

class Frac:
    
    def __init__(self, mone, mehane):
        
        self.mone = mone
        if mehane == 0:
            raise ZeroDivisionError
        self.mehane = mehane
        self._reduce()

    def _reduce(self):
        
        rel_gcd = gcd(self.mone, self.mehane)
        self.mone = self.mone // rel_gcd
        self.mehane = self.mehane // rel_gcd
        
    def __add__(self, other):
        
        common_d = lcm(self.mehane, other.mehane)
        other_mone = (common_d // other.mehane) * other.mone
        self_mone = (common_d // self.mehane) * self.mone
        return Frac(self_mone+other_mone, common_d)
        
    def __sub__(self, other):
        
        common_d = lcm(self.mehane, other.mehane)
        other_mone = (common_d // other.mehane) * other.mone
        self_mone = (common_d // self.mehane) * self.mone
        return Frac(self_mone-other_mone, common_d)
        
    def __mul__(self, other):
        
        return Frac(self.mone*other.mone, self.mehane*other.mehane)
        
    def __truediv__(self, other):
        
        if other.mone == 0:
            raise ZeroDivisionError
        
        else:
            return Frac(self.mone*other.mehane, self.mehane*other.mone)
            
    def __pow__(self, power):
        
        if self.mone == 0 and power == 0:
            return Frac(1, 1)
            
        if self.mone == 0 and self.mehane != 0:
            raise ZeroDivisionError
         
        new_mone = self.mone
        new_mehane = self.mehane
        for i in range(power):
            new_mone = new_mone * new_mone
            new_mehane = new_mehane * new_mehane
        return Frac(new_mone, new_mehane)
        
    def __eq__(self, obj):
        
        if type(obj) == Frac:
            if obj.mone == self.mone and obj.mehane == self.mehane:
                return True
            
            if (obj.mone / self.mone) == (obj.mehane // self.mehane):
                return True
                
        return False
        
    def __ge__(self, other):
        
        if (self.mone / self.mehane) >= (other.mone / other.mehane):
            return True
            
        return False
        
    def __str__(self):
        
        mone_div_mehane = self.mone // self.mehane
        if mone_div_mehane != 1 or mone_div_mehane != 0:
            new_mone = str(mone_div_mehane) + " " + str(self.mone-(mone_div_mehane*self.mehane))
            return (new_mone + "/" + str(self.mehane))
        return (str(self.mone) + "/" + str(self.mehane))
        
fr1 = Frac(21, 36)
fr2 = Frac(13, 5)
print(fr1)
print(fr2)
print(Frac(-3, 6))
print(Frac(3, -6))
print(Frac(-3, 2))
print(Frac(6, 3))
print(Frac(0, 3))
print(fr1+fr2)
print(fr1-fr2)
print(fr2-fr1)
print(fr1*fr2)
print(fr2/fr1)
print(fr1**2)
print(Frac(3, 6)==Frac(2, 4))
print(fr1==fr2)
print(fr1>=fr2)       
print(fr2>=fr1)     """


'''class Tree:
    
    def __init__(self, data, branches=[]):
        
        self.data = data
        self.branches = list(branches)
        
    def is_a_leaf(self):
        
        return not self.branches
        
        
def plus_it(t):
    
    if t.data == '+':
        return sum([plus_it(x) for x in t.branches])
    
    elif t.data == '*':
        res = 1
        
        for k in t.branches:
            exp, res = res, 0
            for i in range(plus_it(k)):
                res = res + exp
        return res
    
    else:
        return t.data

    


t1 = Tree('*', [Tree(2), Tree(3)])
t2 = Tree('+',[Tree(8), Tree(7)])
t3 = Tree('*',[Tree(5), Tree(7)])
t4 = Tree('+',[t1, t2, t3])
print(plus_it(t4))'''


'''class BinaryTreeNode:
    
    def __init__(self, left = None, right = None, data = None):
        
        self.left = left
        self.right = right
        self.data = data

    
def set_val(root, path, data):
    
    cur = root
    for node in path:
        if node == "L":
            if not cur.left:
                cur.left = BinaryTreeNode()
            cur = cur.left
        if node == "R":
            if not cur.right:
                cur.right = BinaryTreeNode()
            cur = cur.right
    cur.data = data
            
        
        
x = BinaryTreeNode()
set_val(x, ["L","R"] ,4)
print(x.left.right.data)'''


'''def set_power(s, n):

    if n==0: 
        return [[]]
    
    v = set_power(s, n-1)
    ans = []
    for t in v:
        for x in s:
            ans.append(t + [x])
    return ans
    


            
print(set_power([7, 8], 3))'''


'''def high_low(n):
    if len(str(n)) == 1:
        return True
    
    elif str(n)[0] < str(n)[1]:
        return False
    
    else:
        return high_low(int(str(n)[1:]))
    

print(high_low(432521))'''


'''def add_sparse_matrix(A, B, dim):
    ans = []
    
    for i in range(dim[0]):
        ans.append([0]*dim[1])
        
    for i, j in A.keys():
        ans[i][j] = A[(i, j)]
        
    for k, m in B.keys():
        ans[k][m] += B[(k, m)]
        
    return ans



dim = (3, 4)
A = {(0,2):2, (1,0):3, (2,1):4}
B = {(0,0):5, (0,2):6, (1,1):4, (2,1):5, (2,3):7}
print(add_sparse_matrix(A, B, dim))


def two_diags(mat):
    if len(mat) == 1:
        return mat[0][0]
    
    diag1, diag2 = 0, 0
    for r in range(len(mat)):
        diag1 += mat[r][r]
        diag2 += mat[r][len(mat)-1-r]
        
    return diag1, diag2
    

A2 = [[0,0,2,0],
      [3,0,0,0],
      [0,4,0,0],
      [1,0,3,0]]

B2 = [[5,0,6,0],
      [0,4,0,0],
      [0,5,0,7],
      [0,3,0,4]]

print(two_diags(A2))
print(two_diags(B2))'''


'''class Lnk:
    empty = ()
    
    def __init__(self, data, next = empty):
        self.data = data
        self.next = next
        
    def __repr__(self):
        if self.next is Lnk.empty:
            return "Lnk({})".format(self.data)
        else:
            return "Lnk({}, {})".format(self.data, self.next)
            
            
def place_between(inter, lnk_lst):
    
    new_lkd = None
    
    while lnk_lst:
        save_new = new_lkd
        
        if lnk_lst.next != Lnk.empty and lnk_lst.data == lnk_lst.next.data:
            cur_lkd = Lnk(lnk_lst.data)
            cur_lkd.next = Lnk(inter)
        
        else:
            cur_lkd = Lnk(lnk_lst.data)
          
        if not save_new:
            save_new = cur_lkd
        else:
            while save_new.next:
                save_new = save_new.next
            save_new.next = cur_lkd
            
        if not new_lkd:
            new_lkd = save_new
        
        lnk_lst = lnk_lst.next
        
    return new_lkd
        
    
    
my_lnk = Lnk(8, Lnk(7, Lnk(7, Lnk(5, Lnk(6, Lnk(6, Lnk(4)))))))
inter = 10
#print(place_between(inter, my_lnk))
print(place_between(-7, Lnk(3, Lnk(3))))
print(place_between(3, Lnk(3, Lnk(3))))
print(place_between(-7, Lnk(-7, Lnk(3, Lnk(3)))))
print(place_between(11, Lnk(7, Lnk(7,Lnk(6,Lnk(6,Lnk(11)))))))
print(place_between(10, Lnk(9, Lnk(9, Lnk(9)))))
ling = Lnk(11, Lnk(21))
print(place_between(5, ling))'''


'''class Tree:
    def __init__(self, data, branches=[]):
        self.data = data
        self.branches = list(branches)
        
    def is_a_leaf(self):
        return not self.branches
    
    def __repr__(self):
        if self.branches:
            return 'Tree({0}, {1})'.format(self.data, repr(self.branches))
        else:
            return 'Tree({0})'.format(repr(self.data))
        
        
        
def ops_on(oper , vals):
    if oper == '+':
        return sum(vals)
    elif oper == '*':
        return mult(vals)
    
def mult(vals):
    res = 1
    for x in vals:
        res *= x
    return res

def ops_to_leaves(iTree: Tree):
    if iTree.data in ('*', '+'):
        operands = []
        
        for br in iTree.branches:
            operands.append(ops_to_leaves(br))
        iTree.branches = [Tree(iTree.data)] + iTree.branches
        iTree.data = ops_on(iTree.data, operands)
    return iTree.data
            

iTree= Tree('*',[Tree('+',[Tree(5),Tree(6)]), Tree('+',[Tree(3),Tree(4)])])
print(ops_to_leaves(iTree))'''


'''class Lnk:
    empty = ()

    def __init__(self, data, next=empty):
        self.data = data
        self.next = next

    def __repr__(self):
        if self.next is Lnk.empty:
            return "Lnk({})".format(self.data)
        else:
            return "Lnk({}, {})".format(self.data, self.next)


def single_rep(lg: Lnk):
    counter = 0
    head = lg
    prev = None

    while head.next:
        if prev != head.data != head.next.data:
            cur_next = head.next
            head.next = Lnk(head.data, cur_next)
            prev = head.data
            counter += 1
            head = head.next.next
        else:
            prev = head.data
            head = head.next
    if prev != head.data:
        head.next = Lnk(head.data)
        counter += 1
    return counter


tr3 = Lnk(8, Lnk(4, Lnk(4, Lnk(5, Lnk(7, Lnk(7, Lnk(2)))))))
print(single_rep(tr3))
print(tr3)'''


'''def no_twins(n: int, x: int, y: int) -> list:
    if n == 0:
        return [[]]
    return _helper(n, x, y, [], [])


def _helper(n: int, x: int, y: int, lst1: list, lst2: list):

    if len(lst2) == n:
        lst1.append(lst2[:])
        return

    for num in (x, y):
        if len(lst2) == 0 or num == x or lst2[-1] != y:
            lst2.append(num)
            _helper(n, x, y, lst1, lst2)
        if lst2:
            lst2.pop()

    return lst1


print(sorted(no_twins(4, 5, 3)))'''


'''def f(x, m):
    
    for i in range(len(x)):
        if i == len(x)-1:
            return m + x[i]
        else:
            return f(x[1:], x[i]+m)
        
        
assert f([11, 12, 1, 2, 9], 0) == 35
assert f([5, 1, 12, 13, 1], 0) == 32'''


'''class Time:
    def __init__(self, hours, minutes):
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            self.__hours = hours
            self.__minutes = minutes
        else:
            raise ValueError
            
    def __str__(self):
        return str(self.__hours) + ":" + str(self.__minutes)
        
    
    


class Schedule:
    def __init__(self):
        self.__drive_schedule = []
        
    def add_time(self, t: Time):
        times_hours_list = []
        times_minutes_list = []
        for time in self.__drive_schedule:
            times_hours_list.append(time.__hour)
            times_minutes_list.append(time.__minute)
            if t.__hours in times_hours_list and t.__minutes in times_minutes_list:
                string_t = str(t.__hours) + ":" + str(t.__minutes)
                raise Exception(f"The schedule already has a train leaving at time {string_t}")
            else:
                self.__drive_schedule.append(t)
            
    def get_schedule(self):
        return self.__drive_schedule
            
    def find_train(self, t: Time):
        min_hour = t.__hour
        min_minute == t.__minute
        wanted_time = None
        for time in self.__drive_schedule:
            if t.__hour < time.__hour > min_time:
                min_hour = time.__hour
                if t.__minute < time.__minute < min_minute:
                    min_minute = time.__minute
                    wanted_time = time

        return wanted_time
                
    
time1 = Time(16, 23)
time2 = Time(22, 46)
time3 = Time(22, 46)
new_schedule = Schedule()
new_schedule.add_time(time1)
new_schedule.add_time(time2)
new_schedule.add_time(time3)
x = new_schedule.get_schedule()
for time in x:
    print(time)'''


'''
def sum_lists(list_1, list_2):
    sum_list = []
    len_diff = len(list_1) - len(list_2)
    if len_diff >= 0:
        
        for num in list_1[:len_diff]:
            sum_list.append(num)
            
        for i in range(len(list_1[len_diff:])):
            for j in range(len(list_2)):
                if i == j:
                    if list_1[i+len_diff] + list_2[j] > 9:
                        sum_list[j] += 1
                        sum_list.append(list_1[i+len_diff]+list_2[j]-10)
                    else:
                        sum_list.append(list_1[i+len_diff] + list_2[j])
    else:
        len_diff = abs(len_diff)
        
        for num in list_2[:len_diff]:
            sum_list.append(num)
            
        for k in range(len(list_2[len_diff:])):
            for m in range(len(list_1)):
                if k == m:
                    if list_2[k+len_diff] + list_1[m] > 9:
                        sum_list[m] += 1
                        sum_list.append(list_1[m]+list_2[k+len_diff]-10)
                    else:
                        sum_list.append(list_1[m]+list_2[k+len_diff])
                    
    return sum_list
    
    
    
list_2 = [2, 9, 6, 0, 8, 7]
list_1 = [9, 4, 5, 9, 5]
print(sum_lists(list_1, list_2))'''


def fib1(n):

    if n == 1:
        return 1

    if n == 2:
        return 2

    if n == 3:
        return 3

    return fib1(n-3) * fib1(n-2) * fib1(n-1)


def fib2(n):
    
    if n == 1:
        return 1
        
    if n == 2:
        return 2

    if n == 3:
        return 3
    
    if n == 4:
        return 6
    
    num1 = fib2(n-3)
    num2, num3 = _helper(num1)
    res = num1 * num2 * num3
    return res
    
    
def _helper(num1):
    
    num2 = num1 * num1
    num3 = num2 * num2
    return num2, num3

print(fib1(8))
print(fib2(8))