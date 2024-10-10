

##### 2020 B B Q13  #recursion #backtracking #####

# def decode(codebook: dict[str:str], cipher: str):
#     return _helper(codebook, cipher, [])


# def _helper(codebook: dict[str:str], cipher: str, lst: list, msg = ""):
#     if len(cipher) == 0:
#         lst.append(msg[:-1])
#         return

#     for string in codebook.keys():
#         counter = 0
#         for i in range(len(string)):
#             if len(string) <= len(cipher) and string[i] == cipher[i]:
#                 counter += 1
#         if counter == len(string):
#             msg += codebook[string]
#             msg += " "
#             _helper(codebook, cipher[counter:], lst, msg)
#             msg = msg[:-1]
#             for i in range(len(msg)-1, -1, -1):
#                 if msg[i] == " ":
#                     break
#                 else:
#                     msg = msg[:i]

#     return lst


# cipher = "abcdefghij"
# codebook = {'hij': 'lied', 'ab': 'hide', 'cdef': 'your',
#             'efg': 'secrets', 'abcd': 'old', 'xyz': 'submarine',
#             'efghij': 'spies', 'ghij': 'message', 'abz': 'rocket'}
# print(decode(codebook, cipher))

############################### Done ###############################

##### 2021 B B Q15  #recursion #backtracking #####

# def n_of_sums(n: int, k: int, fun):
#     if n == 0:
#         return 1
#     elif n < 0 or k <= 0:
#         return 0
#     else:
#         call1 = n_of_sums(n-k, fun(k), fun)
#         call2 = n_of_sums(n, fun(k), fun)
#     return call1 + call2


# def fun1(a): return a-1


# n1 = 6
# k1 = 4
# def fun2(b): return b-2


# n2 = 12
# k2 = 12
# def fun3(x): return x//2


# n3 = 11
# k3 = 8
# def fun4(y): return y-3


# n4 = 7
# k4 = 4
# print(n_of_sums(n2, k2, fun2))


# def best_sum(lst: list, n: int):
# # base case
#     if len(lst) == 0:
#         return set()
#     # skip to rest of list
#     if lst[0] > n:
#         return best_sum(lst[1:], n)

#     # recursive call 1
#     take_first_elem = {lst[0]} | (best_sum(lst[1:], n - lst[0]))

#     # recursive call 2
#     skip_first_elem = best_sum(lst[1:], n)
#     if sum(take_first_elem ) > sum(skip_first_elem):
#         return take_first_elem
#     else:
#         return skip_first_elem


# lst = [4, 2, 3, 5]
# n = 13
# print(best_sum([2,3,2,5,2,7,2,8,2], 27))
# print(best_sum(lst, n))


# def rev_lst(lst: list):
#     if not lst:
#         return lst[:]

#     return _helper(lst[:])


# def _helper(copy_list: list):
#     if len(copy_list) == 0:
#         copy_list = []
#         return copy_list

#     return [copy_list[-1]] + _helper(copy_list[:-1])


# lst = ['a', 'b', 3, 5, [1, 2]]
# lst = rev_lst(lst)
# print(rev_lst(lst))


# def ranksearch(lst: list, k: int):
#     if len(lst) == k:
#         return max(lst)

#     lst.remove(max(lst))
#     return ranksearch(lst, k)

# print(ranksearch([3, 2, 7, 9, 1, 4, 0], 4))

# def f3(n:int, x, y):
#     return _helper(n, x, y)


# def _helper(n:int, x, y, lst1: list=[], lst2: list=[]):
#     if len(lst2) == n:
#         lst1.append(lst2[:])
#         return

#     tup = (x, y)
#     for i in range(len(tup)):
#         if tup[i] == x or not lst2 or (tup[i] == y and lst2[-1] != y):
#             lst2.append(tup[i])
#             _helper(n, x, y, lst1, lst2)
#             lst2.pop()

#     return lst1

# print(f3(2, [3, '5'], 'xy'))


# def contain_all_of(items: list, world: list):
#     items = list(set(items))
#     world = list(set(world))
#     if len(items) > len(world):
#         return False
#     return _helper(items, world, 0)


# def _helper(items, world, ind):
#     #print(items[ind])
#     if ind+1 >= len(items) and items[ind] in world:
#         return True

#     if items[ind] not in world:
#         return False

#     return _helper(items, world, ind+1)


# print(contain_all_of([6, 3, 9, 7, 5, 4, 2, 9], [2, 3, 1, 10, 13, 5, 6, 7, 9]))


# def helper(prev2, curr):
#     if curr == 0:
#         return 1

#     if curr == 1:
#         return 2

#     if curr == 2:
#         return 3

#     return (helper(curr) ** 2) / prev2

# def fib(n):
#     return helper(n)

# print(fib(5))

# class TextDoc:

#     def __init__(self):
#         self.__caret = [0, 0]
#         self.__lines = [""]

#     def move_caret(self, row: int, col: int):
#         if row >= len(self.__lines) or len(self.__lines[row]) < col:
#             raise ValueError

#         self.__caret = [row, col]

#         return None

#     def type_in(self, char):
#         curr_line = self.__lines[self.__caret[0]]

#         if char == "\n":
#             self.__lines[self.__caret[0]] = curr_line[:self.__caret[1]] + char
#             self.__lines.insert(self.__caret[0] + 1, curr_line[self.__caret[1]:])
#             self.__caret = [self.__caret[0] + 1, 0]

#         else:
#             self.__lines[self.__caret[0]] = curr_line[:self.__caret[1]] + char + curr_line[self.__caret[1]:]
#             self.__caret[1] += 1

#         return None

#     def get_current_line(self):
#         return self.__lines[self.__caret[0]][:-1]

#     def __str__(self):
#         document = ""

#         for line in self.__lines:
#             document += line

#         return document

# text_doc = TextDoc()
# text_doc.type_in("I")
# text_doc.type_in("L")
# text_doc.move_caret(0, 1)
# text_doc.type_in("\n")
# text_doc.move_caret(1, 1)
# text_doc.type_in("o")
# text_doc.type_in("v")
# text_doc.type_in("e")
# text_doc.type_in("\n")
# text_doc.type_in("U")

# print(text_doc)


# def sum_non_adj(lst):
#     if len(lst) <= 2:
#         return lst[0]

#     return max(lst[0] + sum_non_adj(lst[2:]), sum_non_adj(lst[1:]))

# def guess_pass(pwd: str, text: str):
#     if text == "":
#         return False
#     if pwd == "":
#         return []
#     if len(pwd) > len(text):
#         return False
#     res = _helper(pwd, text, [], 0, 0)
#     if len(res) == len(pwd):
#         return res
#     return False


# def _helper(pwd: str, text: str, lst: list, ind1: int, counter: int):
#     if ind1 >= len(pwd):
#         return

#     if pwd[ind1] in text[counter:]:
#         cur_pos = text[counter:].find(pwd[ind1])
#         lst.append(counter+cur_pos)
#         counter += (cur_pos + 1)
#         ind1 += 1
#         _helper(pwd, text, lst, ind1, counter)
#         return lst


# pwd = "helloworld"
# text = "myhelloworldokay"
# pwd1 = "abc-123"
# text1 = "acb-123"
# print(guess_pass(pwd, text))

# def count_substrs(word):
#     return count_helper1(word, 0)


# def count_helper1(word, start):
#     if start >= len(word):
#         return 0
#     return count_helper2(word, start, start) + count_helper1(word, start + 1)


# def count_helper2(word, start, end):
#     if end >= len(word):
#         return 0
#     result = count_helper2(word, start, end + 1)
#     if word[start] == word[end]:
#         result += 1
#     return result

# print((count_substrs('abcab')))


# def describe_str(st1):
#     c = same_char_helper(st1, 0)
#     if c == len(st1):
#         return st1[0] + str(c)
#     return st1[0] + str(c) + describe_str(st1[c:])


# def same_char_helper(s, k):
#     ch = s[k]
#     count = 0
#     while s[k] == ch:
#         count += 1
#         k += 1
#         if k == len(s):
#             break
#     return count


# print(describe_str("abbcccdeaa"))

# def edit_distance(a, b):
#     return edit_help(a, b, len(a), len(b))


# def edit_help(a, b, m, n):
#     if m == 0:
#         return n
#     if n == 0:
#         return m
#     if a[m-1] == b[n-1]:
#         return edit_help(a, b, m-1, n-1)
#     return 1 + min(edit_help(a, b, m, n-1),
#                    edit_help(a, b, m-1, n),
#                    edit_help(a, b, m-1, n-1))

# print(edit_distance("axbyc", "abc"))


# def find_valley(lst: list):
#     if lst[0] < lst[1]:
#         return 0
#     elif lst[-1] < lst[-2]:
#         return (len(lst)-1)
#     return _helper(lst, 1)


# def _helper(lst: list, ind: int):
#     if lst[ind-1] >= lst[ind] <= lst[ind+1]:
#         return ind

#     return _helper(lst, ind+1)


# print(find_valley([7, 5, 4, 3, 2, 7, 9, 10]))

# def helper(num_x, num_y, num_z, st, lst):
#     if num_x == 0 and num_y == 0 and num_z == 0:
#         lst.append(st)
#         return
#     if num_x > 0:
#         helper(num_x - 1, num_y, num_z, st + "x", lst)
#     if num_y > 0:
#         helper(num_x, num_y - 1, num_z, st + "y", lst)
#     if num_z > 0:
#         helper(num_x, num_y, num_z - 1, st + "z", lst)

#     return lst


# def xyz(num_x, num_y, num_z):
#     if num_x == 0 and num_y == 0 and num_z == 0:
#         return []
#     return helper(num_x, num_y, num_z, "", [])


# print(xyz(2, 0, 1))


# def same_char_helper(s, k):
#     counter = 0
#     char = s[k]
#     while  k < len(s) and s[k] == char:
#         counter += 1
#         k += 1

#     return counter

# def describe_str(st1):
#     if st1 == "":
#         return ""
#     c = same_char_helper(st1, 0)
#     return st1[0] + str(c) + describe_str(st1[c:])

# print(describe_str("aabbbcccccddeea"))


################# Linked Lists #################

# class Node:
#     def __init__(self, data, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + "->" + repr(self.next)


# def split_sorted(head: Node):
#     sorted_list = []
#     cur_head = head

#     while head and head.next:
#         if head.data <= head.next.data:
#             head = head.next
#         else:
#             sorted_list.append(cur_head)
#             cur_head = head.next
#             head.next = None
#             head = cur_head
#     sorted_list.append(cur_head)

#     return sorted_list


# my_head = Node(1, Node(2, Node(3, Node(2, Node(1, Node(10))))))
# print(split_sorted(my_head))


# class Node:
#     def __init__(self, data, next=None):
#         self.data = data
#         self.next = next

# class LinkedList:
#     def __init__(self, head):
#         self.head = head


# def separe(L: LinkedList, pr):
#     cur = L.head
#     T = LinkedList(None)
#     F = LinkedList(None)
#     while cur:
#         if pr(cur.data):
#             if not T.data:
#                 T.data = cur.data
#             else:
#                 T.next = cur


# L = LinkedList(Node(2, Node(12, Node(1, Node(11)))))
# pr = lambda x: x%2 == 0
# print(separe(L, pr))


# class Node:
#     def __init__(self, data, next=None):
#         self.data = data
#         self.next = next

# def find_cycle(head: Node):
#     cur1 = head
#     cur2 = head.next

#     while cur1:
#         while cur2:
#             if cur2.next == cur1:
#                 return True
#             cur2 = cur2.next
#         cur1 = cur1.next
#         cur2 = cur1

#     return False


# my_head = Node(1, Node(2, Node(3, Node(4, Node(5, (Node(2, Node(3, Node(4, Node(5))))))))))
# print(find_cycle(my_head))


# class Node:
#     def __init__(self, data, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + "->" + repr(self.next)


# def split(head: Node, k: int):
#     lst: list = []
#     cur1 = head
#     cur2 = head

#     while head:
#         for i in range(k-1):
#             if cur1:
#                 cur1 = cur1.next
#         if cur1:
#             cur2 = cur1.next
#             cur1.next = None
#             lst.append(head)
#             head = cur2
#             cur1 = cur2
#         else:
#             lst.append(head)
#             head = head.next
#             break

#     return lst


# my_head = Node(5, Node(-3, Node(8, Node(1, Node(5, Node(7, Node(2, Node(4, Node(9)))))))))
# #my_head = Node(1, Node(7, Node(2)))
# k = 2
# print(split(my_head, k))


# class Node:
#     def __init__(self, data, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + "->" + repr(self.next)


# def eq_sums(L1: Node, L2: Node):
#     sum1 = 0
#     sum2 = 0
#     cur1 = L1
#     cur2 = L2

#     while cur1:
#         sum1 += cur1.data
#         cur1 = cur1.next

#     while cur2:
#         sum2 += cur2.data
#         cur2 = cur2.next

#     min_L = L1
#     if sum2 < sum1:
#         min_L = L2

#     cur = min_L
#     while cur.next:
#         cur = cur.next

#     i = 0
#     while i < abs(sum2 - sum1):
#         cur.next = Node(1)
#         cur = cur.next
#         i += 1

#     return min_L


# L1 = Node(5, Node(-3, Node(8, Node(1, Node(5)))))
# L2 = Node(7, Node(1, Node(2, Node(3, Node(6)))))
# print(eq_sums(L1, L2))


# from typing import Optional


# class Node:  # DO NOT CHANGE THIS CLASS!
#     def __init__(self, data: str, rep: int, next_node: Optional["Node"]) -> None:
#         self.data = data
#         self.rep = rep
#         self.next = next_node

#     def __repr__(self):
#         return repr(self.data) + ":" + repr(self.rep) + " -> " + repr(self.next)


# def compress(head: Node):
#     cur = head

#     while cur.next:
#         if cur.data == cur.next.data:
#             cur.rep += cur.next.rep
#             if cur.next.next:
#                 cur.next = cur.next.next
#             else:
#                 cur.next = None
#                 break
#         else:
#             cur = cur.next

#     return head


# head = Node("c", 2, Node("a", 3, Node("a", 1, Node("a", 3, None))))
# print(compress(head))


# class Node:
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + " -> " + repr(self.next)


# class LinkedList:
#     def __init__(self, head):
#         self.head = head

#     def swap(self,prev,cur,next):
#         if prev == None:
#             self.head = next
#         else:
#             prev.next = next
#         cur.next = next.next
#         next.next = cur

#     def sort(self):
#         sorted = False
#         while not sorted:
#             prev, node = None, self.head
#             sorted = True
#             while node != None and node.next != None:
#                 next = node.next
#                 if next.data < node.data:
#                     self.swap(prev, node, next)
#                     sorted = False
#                 else:
#                     prev = node
#                 node = next

# def get_size(self):
#     cur = self.head
#     size = 0
#     while cur:
#         cur = cur.next
#         size += 1
#     return size

# def sort(self, first_half, second_half):

# def cut(self):
#     curr = self.head
#     second_half = None
#     for i in range(self.get_size() // 2):
#         curr = curr.next
#     second_half = curr.next
#     curr.next = None
#     self.sort(self.head, second_half)

# def merge(self, first_half, second_half):
#     if first_half.data > second_half.data:
#         save = first_half
#         first_half = second_half
#         second_half = save
#     while first_half and second_half:

# def sort(self):
#     cur = self.head
#     cur2 = None

#     while cur.next:
#         if cur.data > cur.next.data:
#             save = cur.next
#             cur.next = cur.next.next
#             save.next = cur
#             if cur2:
#                 cur2.next = save
#                 self.head = cur2
#                 cur = self.head
#             else:
#                 self.head = save
#                 cur = self.head
#         else:
#             cur2 = self.head
#             cur = cur.next
#     print(self.head)
#     return None


# my_node = Node(9, Node(-3, Node(4, Node(1, Node(8)))))
# L = LinkedList(my_node)
# print(L.sort())


# class Node:
#     def __init__(self, data, next=None):
#         self.data = data
#         self.next = next


# def find_cycle(head: Node):
#     cur1 = head
#     cur2 = head.next
#     while cur1 and cur2 and cur2.next:
#         if cur1 == cur2:
#             return True
#         cur1 = cur1.next
#         cur2 = cur2.next.next

#     return False


# # last = Node()
# # node = Node(Node(last))
# # last.next = node
# # lst = Node(Node(Node(node)))

# lst = Node(6, Node(5, Node(4)))
# print(find_cycle(lst))

# class Node:
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + " -> " + repr(self.next)


# def split_sorted(head: Node):
#     lst = []
#     cur = head
#     if cur:
#         lst.append(cur)

#     while cur.next:
#         if cur.data > cur.next.data:
#             save = cur.next
#             lst.append(cur.next)
#             cur.next = None
#             cur = save
#         else:
#             cur = cur.next

#     return lst


# head = Node(10, Node(9, Node(8, Node(3, Node(1)))))
# print(split_sorted(head))


# class Node:
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + " -> " + repr(self.next)

# class LinkedList:
#     def __init__(self, head):
#         self.head = head

# def separe(L: LinkedList, pr):
#     cur = L.head
#     T = None
#     F = None
#     t = None
#     f = None

#     while cur:
#         cur2 = cur.next
#         cur.next = None
#         if pr(cur.data):
#             if not T:
#                 t = cur
#                 T = LinkedList(t)
#             else:
#                 t.next = cur
#                 t = t.next
#         else:
#             if not F:
#                 f = cur
#                 F = LinkedList(f)
#             else:
#                 f.next = cur
#                 f = f.next
#         cur = cur2

#     return T, F


# node = Node(2, Node(12, Node(1, Node(11))))
# L = LinkedList(node)
# pr = lambda x: x % 2 == 0
# a, b = separe(L, pr)
# j =1


# class Node:
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + " -> " + repr(self.next)


# def find_max_sum_pair(head: Node):
#     max_pair = None
#     cur1 = head
#     cur2 = head

#     while cur1 and cur2.next:
#         while cur2.next.next:
#             cur2 = cur2.next
#         if not max_pair:
#             max_pair = cur1.data + cur2.next.data
#         else:
#             if cur1.data + cur2.next.data > max_pair:
#                 max_pair = cur1.data + cur2.next.data
#         cur1 = cur1.next
#         cur2.next = None
#         cur2 = cur1

#     return max_pair

# node = Node(7, Node(1, Node(2, Node(4, Node(-3, Node(-2))))))
# print(find_max_sum_pair(node))


# class Node:
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + " -> " + repr(self.next)


# def shift(head, k):
#     cur = head
#     cur2 = head

#     for i in range(k-1):
#         cur = cur.next
#     head = cur.next
#     cur.next = None
#     save = head

#     while save.next:
#         save = save.next
#     save.next = cur2

#     return head


# node = Node(10, Node(20, Node(30, Node(40, Node(50, Node(60))))))
# print(shift(node, 3))


# class Node:
#     def __init__(self, data=None, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + " -> " + repr(self.next)


# def zipper(head1, head2):
#     cur1, cur2 = head1, head2
#     if not cur1:
#         return cur2
#     if not cur2:
#         return cur1
#     new_head = None

#     while cur1 or cur2:
#         if cur1:
#             head1 = cur1.next
#             cur1.next = None
#             if not new_head:
#                 new_head = cur1
#                 save = new_head
#             else:
#                 save.next = cur1
#                 save = save.next
#         if cur2:
#             head2 = cur2.next
#             cur2.next = None
#             save.next = cur2
#         save = save.next
#         cur1, cur2 = head1, head2

#     return new_head

# head1 = Node(1, Node(2, Node(3, Node(4))))
# head2 = Node("A", Node("B", Node("C", Node("D"))))
# print(zipper(head1, head2))


# class MyKeyError(Exception):  # an exception to use with the MultiSet class.
#     pass


# class MultiSet:
#     def __init__(self):
#         self.__multiset = {}

#     def insert(self, item):
#         if item in self.__multiset.keys():
#             self.__multiset[item] += 1
#         else:
#             self.__multiset[item] = 1
#         return None

#     def extend(self, iterable):
#         for item in iterable:
#             if item in self.__multiset.keys():
#                 self.__multiset[item] += 1
#             else:
#                 self.__multiset[item] = 1
#         return None

#     def remove(self, item):
#         if item not in self.__multiset.keys():
#             raise MyKeyError
#         self.__multiset[item] -= 1
#         if self.__multiset[item] == 0:
#             self.__multiset.pop(item)
#         return None

#     def __str__(self):
#         string = "{"
#         for item in self.__multiset.keys():
#             for i in range(self.__multiset[item]):
#                 string += str(item)
#                 if i < len(self.__multiset)-1:
#                     string += ", "
#         final_str = ""
#         for j in range(len(string)):
#             if j < len(string)-2:
#                 final_str += string[j]
#         final_str += "}"

#         return final_str


# my_set = MultiSet()
# my_set.insert(1)
# my_set.extend([2, 3, 4, 5])
# my_set.remove(3)
# my_set.insert("a")
# my_set.insert(6.78)
# print(my_set)


# class EditableString:
#     def __init__(self, some_str):
#         self.__str = some_str
#         self.__last_action = None
#         self.__params = ()


#     def insert_char_at(self, char1, ind):
#         if ind > len(self.__str) or ind < 0:
#             raise IndexError
#         if ind == len(self.__str):
#             self.__str += str(char1)
#         else:
#             first_half = self.__str[:ind]
#             second_helf = self.__str[ind:]
#             self.__str = first_half + str(char1) + second_helf
#         self.__last_action = self.insert_char_at
#         self.__params = (char1, ind)

#         return

#     def delete_char_at_ind(self, ind):
#         if ind >= len(self.__str) or ind < 0:
#             raise IndexError
#         else:
#             self.__str = self.__str[:ind] + self.__str[ind+1:]
#         self.__last_action = self.delete_char_at_ind
#         self.__params = (ind,)

#         return

#     def redo_last_action(self):
#         if not self.__last_action:
#             return None
#         if len(self.__params) == 2:
#             param1 = self.__params[0]
#             param2 = self.__params[1]
#             self.insert_char_at(param1, param2)
#         else:
#             self.delete_char_at_ind(self.__params[0])

#     def __str__(self):
#         return self.__str

# estr = EditableString("HelloWorld")
# estr.insert_char_at("b", 2)
# print(estr)
# estr.redo_last_action()
# print(estr)
# estr.delete_char_at_ind(2)
# print(estr)
# estr.redo_last_action()
# print(estr)
# estr.insert_char_at(5, 6)
# print(estr)
# estr.delete_char_at_ind(9)
# print(estr)
# estr.insert_char_at("YAHH!!!", 4)
# print(estr)


# class Campus:
#     def __init__(self):
#         self.classmates: dict[str, set[str]] = {}

#     def add_classmate(self, st1, st2):
#         if st1 not in self.classmates.keys():
#             self.classmates[st1] = {st2}
#         else:
#             self.classmates[st1].add(st2)

#         if st2 not in self.classmates.keys():
#             self.classmates[st2] = {st1}
#         else:
#             self.classmates[st2].add(st1)

#     def soc_dist(self, st1, st2, n):
#         if st1 == st2:
#             return True

#         if st1 not in self.classmates.keys():
#             return  False

#         is_st2 = False
#         for key in self.classmates.keys():
#             for stud in self.classmates[key]:
#                 if stud == st2:
#                     is_st2 = True
#                     break
#             if is_st2:
#                 break
#         if not is_st2:
#             return False

#         is_st1_passed = False
#         soc_distance = 0
#         for key in self.classmates.keys():
#             if key == st1:
#                 is_st1_passed = True
#             if is_st1_passed:
#                 soc_distance += 1
#                 if st2 in self.classmates[key]:
#                     break

#         if soc_distance == n:
#             return True
#         return False


# teva = Campus()
# teva.add_classmate('a','b')
# teva.add_classmate('a','c')
# teva.add_classmate('d','b')
# teva.add_classmate('d','k')
# print(teva.classmates)
# # {'a': {'c', 'b'}, 'b': {'d', 'a'}, 'c': {'a'}, 'd': {'b', 'k'}, 'k': {'d'}}
# print("a-b",teva.soc_dist('a','b',1))
# # a-b True
# print("a-d",teva.soc_dist('a','d',2))
# # a-d True
# print("a-k",teva.soc_dist('a','k',3))
# # a-k True
# print("a-p",teva.soc_dist('a','p',3))
# # a-p False
# print("s-p",teva.soc_dist('s','p',1))
# # s-p False
# print("a-a",teva.soc_dist('a','a',100))
# # a-a True

# class Node:
#     def __init__(self, data, children = []):
#         self.data, self.children = data, children

# def check_tree(root: Node):
#     lst = _helper(root)
#     if not lst[0] and not lst[1]:
#         return
#     elif not lst[0]:
#         return 1
#     return 0

# def _helper(root: Node, counter: int = 0, lst: list = [True, True]):
#     if not root.children:
#         if counter % 2 != 0:
#             lst[1] = False
#         else:
#             lst[0] = False
#         return

#     for child in root.children:
#         _helper(child, counter+1)

#     return lst


# tree = Node(1, [Node(2, [Node(5, []), Node(6, []), Node(7, [])]), Node(3, [Node(8, [Node(11, [])]), Node(9, [Node(12, [])]), Node(4, [Node(10, [Node(13, [Node(14, [])])])])])])

# tree2 = Node(1, [Node(2), Node(4, [Node(5, [Node(6)])])])
# tree3 = Node(1, [Node(2, [Node(3)]), Node(4, [Node(5, [Node(6, [Node(7)])])])])

# print(check_tree(tree3))


# def mb_fib(n):
#     if n <= 3:
#         return n

#     return _helper(n)


# def _helper(n, counter=0, prev1=3, prev2=2, prev3=1):
#     if counter == n-4:
#         return prev1 * prev2 * prev3

#     return _helper(n, counter+1, prev1*prev2*prev3, prev1, prev2)


# def fib(n):
#     if n <= 3:
#         return n

#     return fib(n-1) * fib(n-2) * fib(n-3)


# print(mb_fib(20) == fib(20))
# from typing import Optional

# def assign(n:int, k: int, hate: set[tuple[int, int]]) -> Optional[list[list[int]]]:
#     table: list = []
#     persons = [i for i in range(1, n+1)]
#     tables = [table[:] for i in range(k)]
#     l =_helper(n, tables, hate)
#     for lst in l:
#         if not lst:
#             return None
#     return l


# def _helper(next_person, tables: list[list], hate):
#     if next_person == 0:
#         return tables

#     for table in tables:
#         for person in table:
#             hate_echother = (next_person, person) in hate or (person, next_person) in hate
#             if not hate_echother:
#                 table.append(next_person)
#                 _helper(next_person-1, tables, hate)
#                 table.pop()

#     return tables

# print(assign(4, 2, {(1,2), (1,3)}))


# def sum_lists(lst1: list[int], lst2: list[int]) -> list[int]:
#     if lst1 == lst2 == [0]:
#         return [0]

#     sum_lst = []
#     longer_lst, shorter_lst = lst1, lst2
#     if len(lst2) > len(lst1):
#         longer_lst, shorter_lst = lst2, lst1
#     margin = len(longer_lst) - len(shorter_lst)

#     i = 0
#     while i < len(longer_lst):
#         if i < margin:
#             sum_lst.append(longer_lst[i])
#         else:
#             sum_lst.append(longer_lst[i]+shorter_lst[i-margin])
#         i += 1

#     for i in range(len(sum_lst)-1, -1, -1):
#         if sum_lst[i] > 9:
#             if i > 0:
#                 sum_lst[i] -= 10
#                 sum_lst[i-1] += 1
#             else:
#                 sum_lst[i] -= 10
#                 sum_lst.insert(0, 1)

#     for num in sum_lst:
#         if num == 0:
#             sum_lst.remove(num)
#         else:
#             break

#     return sum_lst


# lst1 = [8, 8, 8, 8, 8, 1, 3, 3]
# lst2 = [9, 9, 9, 9, 9, 9, 9]
# sum_lst = sum_lists(lst1, lst2)
# str1 = ""
# for num in sum_lst:
#     str1 += str(num)
# print(int(str1)) == (88888133+9999999)


# def find_stain_size(mat: list[list[int]], place: list[int, int]) -> int:
#     y, x = place
#     return {(y + dy, x + dx)
#             for dy in [-1, 0, 1] for dx in [-1, 0, 1]
#             if dx or dy if 0 <= y + dy < len(mat)
#             if 0 <= x + dx < len (mat[0])}

# mat = [[1, 1, 0, 0, 0],
#        [0, 1, 0, 1, 0],
#        [1, 0, 0, 0, 0],
#        [0, 0, 1, 1, 1],
#        [0, 1, 1, 1, 1]]
# place = [3, 3]
# print(find_stain_size(mat, place))


# def pairs_sum1(d: dict):
#     nums_list = [num for num in d.keys() for reps in range(d[num])]
#     nums_list = sorted(nums_list)
#     if len(nums_list)%2 == 0:
#         sum_pair = nums_list[0] + nums_list[-1]
#         new_list = nums_list[1:-1]
#     else:
#         sum_pair = nums_list[-1]
#         new_list = nums_list[:-1]
#     for i in range(len(new_list)//2):
#         if new_list[0+i] + new_list[-1-i] != sum_pair:
#             return False

#     return True


# def pairs_sum2(d: dict):
#     if not d:
#         return True
#     counter = 0
#     sum = 0
#     for key, value in d.items():
#         counter += value
#         sum += key*value
#     pair_sum = sum // counter + 2
#     for key, value in d.items():
#         if key == pair_sum/2:
#             if value%2 == 1:
#                 return False
#         else:
#             if value != d[pair_sum-key]:
#                 return False
#     return True


# d = {0:1, 1:2, 3:1, 7:2, 8:1}
# print(pairs_sum2(d))


# from typing import Optional


# class Node:
#     def __init__(self, data, prev=None, next=None):
#         self.data = data   # will be either '(' or ')'
#         self.prev = prev
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + " -> " + repr(self.next)


# def balanced(head: Node):
#     cur: Optional[Node] = head
#     if not head:
#         return True
#     if cur and not cur.next:
#         return False

#     while cur and cur.next:
#         if cur.data == "(" and cur.next.data == ")":
#             if cur.prev:
#                 # prev1 = cur.prev
#                 cur.prev.next = cur.next.next
#                 if cur.next.next:
#                     cur.next.next.prev = cur.prev
#                 # cur = prev1
#                 cur = head
#             else:
#                 if cur.next:
#                     cur = cur.next.next
#                 else:
#                     cur = None
#             if not cur:
#                 return True
#         else:
#             cur = cur.next

#     return False


# node1 = Node("(")
# node2 = Node("(", node1)
# node3 = Node(")", node2)
# node4 = Node(")", node3)
# node5 = Node("(", node4)
# node6 = Node(")", node5)
# node7 = Node(")", node6)
# node8 = Node(")", node7)
# node1.next = node2
# node2.next = node3
# node3.next = node4
# node4.next = node5
# node5.next = node6
# node6.next = node7
# node7.next = node8
# print(balanced(node1))__init__(self, data, left=None, right=None):


# from functools import *

# class Time:
#     def __init__(self, hours: int, minutes: int):
#         if not 0 <= hours <= 23 or not 0 <= minutes <= 59:
#             raise ValueError
#         self.__hours = hours
#         self.__minutes = minutes
#         self.__time_tup = (hours, minutes)

#     def __str__(self):
#         return f"{self.__hours}:{self.__minutes}"

#     def time_tup_getter(self):
#         return self.__time_tup

#     def __eq__(self, other):
#         return self.__hours == other.__hours and self.__minutes == other.__minutes


# class Schedule:
#     def __init__(self):
#         self.__schedule = []

#     def add_time(self, t: Time):
#         if t not in self.__schedule:
#             self.__schedule.append(t)
#         else:
#             raise Exception("the schedule already has a" +
#                             f"train leaving at time {t.__hours}:{t.__minutes}")

#     def find_train(self, t: Time):
#         best = None
#         low = 0
#         high = len(self.__schedule)
#         while low < high:
#             mid = (low+high) // 2
#             time = self.__schedule[mid]
#             if t > time:
#                 high = mid
#                 continue
#             else:
#                 if not best or time < best:
#                     best = time
#                 low = mid
#         if not best:
#             raise Exception("not train")
#         return best


# time1 = Time(12, 32)
# time2 = Time(20, 43)
# time3 = Time(7, 51)
# time4 = Time(18, 37)
# time5 = Time(8, 9)
# time6 = Time(18, 32)
# time7 = Time(14, 25)
# time8 = Time(16, 42)
# schedule = Schedule()
# schedule.add_time(time1)
# schedule.add_time(time2)
# schedule.add_time(time3)
# schedule.add_time(time4)
# schedule.add_time(time5)
# schedule.add_time(time6)
# schedule.add_time(time7)
# schedule.add_time(time8)
# time = Time(19, 30)
# print(schedule.find_train(time))

# from typing import Optional

# def assign(n: int, k: int, hate: set[tuple[int,int]]) -> Optional[list[list[int]]]:
#     return _helper(n, [[] for i in range(k)], hate)


# def _helper(next_person, tables, hate):
#     if next_person == 0:
#         return tables

#     for table in tables:
#         can_place = True
#         for person in table:
#             is_hate = (person, next_person) in hate or (next_person, person) in hate
#             if is_hate:
#                 can_place = False
#                 break
#         if can_place:
#             table.append(next_person)
#             result = _helper(next_person-1, tables, hate)
#             return result
#     table.pop()

#     return None


# hate = {(1,3), (2,4), (1,2)}
# n = 4
# k = 2
# print(assign(n, k, hate))


# from functools import reduce

# print_message = True
# msg = "the product is:" if print_message else ""
# lst = [3, 2, 0, 0, -5, 6, 0, 8, 9]
# g = lambda x,y: x*y if x!=0 and y!=0 else (x if x!=0 else y)
# print(msg, reduce(g, lst))


# def invert_dictionary(d):
#     return {val:[key for key in d.keys() if d[key] == val] for val in d.values()}


# d = {7:1, 8:2, 9:3, 10:3, 11:2, 12:2}
# print(invert_dictionary(d))


# class Node:
#     def __init__(self, data, next=None):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         return repr(self.data) + " -> " + repr(self.next)


# def find_max_sum_pair(head: Node) -> float:
#     cur1 = head
#     cur2 = head

#     while cur2.next:
#         cur2 = cur2.next

#     max_sum = cur1.data + cur2.data
#     cur1 = cur1.next
#     first_data = cur1.data
#     cur3 = cur1
#     while cur1 is not cur2:
#         if cur1.next == cur2:
#             if (cur1.data * 2) > max_sum:
#                 max_sum = (cur1.data) * 2
#             break
#         while cur3.next is not cur2:
#             cur3 = cur3.next
#         if cur1.data + cur3.data > max_sum:
#             max_sum = cur1.data + cur3.data
#         cur2 = cur3
#         cur1 = cur1.next
#         cur3 = cur1

#     return max_sum


# node = Node(7, Node(1, Node(2, Node(4, Node(-3, Node(-2, Node(-1)))))))
# print(find_max_sum_pair(node))
# print(node)


# def xyz(num_x, num_y, num_z):
#     if num_x == num_y == num_z == 0:
#         return [""]
#     return _helper(num_x, num_y, num_z, "", [])


# def _helper(x: int, y: int, z: int, st: str, lst: list):
#     if len(st) == x+y+z:
#         lst.append(st)
#         return

#     for char in ("x", "y", "z"):
#         if char == "x" and st.count("x") < x or char == "y" and st.count("y") < y \
#             or char == "z" and st.count("z") < z:
#             st += char
#             _helper(x, y, z, st, lst)
#             st = st[:-1]

#     return lst

# print(xyz(1, 1, 1))


# from typing import Optional

# class BinT:
#     def __init__(self, data, left=None, right=None):
#         self.data = data
#         self.left = left
#         self.right = right

# def trim(root: BinT, low: int, high: int) -> Optional[BinT]:
#     if not root:
#         return None

#     root.left = trim(root.left, low, high)
#     root.right = trim(root.right, low, high)
#     if root.data <= low:
#         return root.right
#     if root.data >= high:
#         return root.left

#     return root


# root_2 = BinT(3, BinT(0 ,None, BinT(2, BinT(1), None)), BinT(4))
# print(trim(root_2, low=0, high=4)) == BinT(3, BinT(2, BinT(1), None), None))


# def find_stain_size(mat, place):
#     if (not 0 <= place[0] < len(mat)) or (not 0 <= place[1] < len(mat[0])):
#         return 0
#     if mat[place[0]][place[1]] == 0:
#         return 0

#     counter = 1
#     mat[place[0]][place[1]] = 0
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             counter += find_stain_size(mat, [place[0]+i, place[1]+j])

#     return counter

# mat1 = [[1, 1, 0, 0, 0], [0, 1, 0, 1, 0], [1, 0, 0, 0, 0], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1]]
# print(find_stain_size(mat1, [4,3]))

# def intersect(intervals: list[tuple[float,float]], points: list[float]) -> bool:
#     intervals.sort(key = lambda x:x[1])
#     points.sort()
#     while True:
#         if not points or not intervals:
#             return False
#         p = points.pop()
#         s,e = intervals.pop()
#         if p>e:
#             intervals.append((s,e))
#         elif p<s:
#             points.append(p)
#         else:
#             return True


# intervals = [(1,2), (3,5), (6.5, 7.5)]
# points = [0, 6, 8]
# print(intersect(intervals, points))


# class Tree:
#     def __init__(self, data, branches=[]):
#         self.data = data
#         self.branches = list(branches)


# def monotonic(t: Tree):
#     res = _helper(t, [True])
#     return res[0]


# def _helper(t: Tree, is_monotonic: list):
#     for branch in t.branches:
#         if branch.data < t.data:
#             is_monotonic[0] = False
#         _helper(branch, is_monotonic)

#     return is_monotonic

# def monotonic(t: Tree):
#     is_monotonic = True
#     for branch in t.branches:
#         if branch.data < t.data:
#             is_monotonic = False
#         is_monotonic = monotonic(branch) and is_monotonic
#     return is_monotonic


# def monotonic(t: Tree):
#     for branch in t.branches:
#         if branch.data < t.data or not monotonic(branch):
#             return False
#     return True


# tree2 = Tree(3, [Tree(3,), Tree(6, [Tree(6)])])
# tree3 = Tree(5)
# tree4 = Tree(7, [Tree(7)])
# tree1 = Tree(2, [tree2, tree3, tree4])
# print(monotonic(tree1))


# class Tree:
#     def __init__(self, data, branches=[]):
#         self.data = data
#         self.branches = list(branches)

#     def is_a_leaf(self):
#         return not self.branches


# def plus_it(t: Tree):
#     if t.is_a_leaf():
#         return t.data

#     sum = 0
#     help = 1
#     for branch in t.branches:
#         if t.data == "+":
#             sum += plus_it(branch)
#         else:
#             sum = 0
#             for i in range(plus_it(branch)):
#                 sum += help
#             help = sum

#     return sum


# t2 = Tree("*", [Tree(2), Tree(3)])
# t3 = Tree("+", [Tree(8), Tree(7)])
# t4 = Tree("*", [Tree(5), Tree(7)])
# t1 = Tree("+", [t2, t3, t4])

# print(plus_it(t1))


# class Node:
#     def __init__(self, data, left=None, right=None):
#         self.data = data
#         self.left = left
#         self.right = right


# def is_legal_BST(root: Node) -> bool:
#     res = _helper(root, [True])
#     return res[0]


# def _helper(root: Node, lst: list):
#     if not root or (not root.left and not root.right):
#         return

#     if root.left and root.data < root.left.data:
#         lst[0] = False
#     if root.right and root.data >= root.right.data:
#         lst[0] = False

#     _helper(root.left, lst)
#     _helper(root.right, lst)

#     return lst


# tree7 = Node(9, None, Node(15))
# tree6 = Node(6, Node(5))
# tree5 = Node(8, tree6, tree7)
# tree4 = Node(3, Node(1))
# tree3 = Node(2, Node(2))
# tree2 = Node(2, tree3, tree4)
# tree1 = Node(4, tree2, tree5)

# print(is_legal_BST(tree1))


# class TreeNode:
#     def __init__(self, data, left=None, right=None):
#         self.data = data
#         self.left = left
#         self.right = right


# def kth_smallest(t: TreeNode, k: int):
#     datas = _helper(t, [])
#     datas.sort()
#     return datas[k-1]


# def _helper(t:TreeNode, lst: list):
#     if not t:
#         return

#     lst.append(t.data)
#     _helper(t.left, lst)
#     _helper(t.right, lst)

#     return lst


# root = TreeNode(8)
# root.left = TreeNode(5)
# root.right = TreeNode(14)
# root.left.left = TreeNode(0)
# root.left.right = TreeNode(6)
# root.right.right = TreeNode(27)
# root.right.right.right = TreeNode(300)

# print(kth_smallest(root, 1))
# print(kth_smallest(root, 2))
# print(kth_smallest(root, 3))
# print(kth_smallest(root, 7))

# class Link:
#     empty = ()

#     def __init__(self, data, next=empty):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         if self.next is Link.empty:
#             return "Link({})".format(self.data)
#         else:
#             return "Link({}, {})".format(self.data, self.next)


# def de_comp(n: int, base_lst: Link):
#     return _helper(n, base_lst, 0)


# def _helper(n: int, base_lst: Link, counter: int, new_lst=None, save=None):
#     if counter == n:
#         return new_lst
#     else:
#         if not base_lst.next and base_lst.data + counter != n:
#             raise ArithmeticError

#     if base_lst and base_lst.data + counter <= n:
#         counter += base_lst.data
#         if not new_lst:
#             new_lst = Link(base_lst.data)
#             save = new_lst
#         else:
#             save.next = Link(base_lst.data)
#             save = save.next
#     if base_lst.next:
#         base_lst = base_lst.next

#     return _helper(n, base_lst, counter, new_lst, save)


# twos = Link(32, Link(16, Link(8, Link(4, Link(2, Link(1))))))
# fibos = Link(
#     34, Link(21, Link(13, Link(8, Link(5, Link(3, Link(2, Link(1))))))))
# print(de_comp(100, fibos))


# def xyz(num_x, num_y, num_z):
#     if num_x == num_y == num_z == 0:
#         return [""]
#     return _helper(num_x, num_y, num_z, [], "")


# def _helper(num_x: int, num_y: int, num_z: int, lst: list, st: str):
#     if num_x == num_y == num_z == 0:
#         lst.append(st)
#         return

#     if num_x > 0:
#         _helper(num_x-1, num_y, num_z, lst, st+"x")

#     if num_y > 0:
#         _helper(num_x, num_y-1, num_z, lst, st+"y")

#     if num_z > 0:
#         _helper(num_x, num_y, num_z-1, lst, st+"z")

#     return lst


# print(xyz(2, 1, 1))


# def unify(intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
#     if not intervals:
#         return []
#     intervals.sort()
#     cur = intervals[0]
#     result = []
#     for i in range(1, len(intervals)):
#         if intervals[i][0] < cur[1]:
#             cur = (cur[0], max(cur[1], intervals[i][1]))
#         else:
#             result.append(cur)
#             cur = intervals[i]

#     result.append(cur)
#     return result


# from math import gcd


# def lcm(a, b):  # intentionally fails when gcd(a,b)==0
#     return abs(a // gcd(a, b) * b)


# class Frac:
#     def __init__(self, mone, mehane):
#         self.mone = mone

#         if mehane == 0:
#             raise ZeroDivisionError

#         self.mehane = mehane
#         self._reduce()

#     def _reduce(self):
#         common_d = gcd(self.mone, self.mehane)
#         self.mone = self.mone // common_d
#         self.mehane = self.mehane // common_d

#     def __add__(self, other):
#         least_common_d = lcm(self.mehane, other.mehane)
#         to_mult_self = least_common_d // self.mehane
#         to_mult_other = least_common_d // other.mehane
#         new_mone = (to_mult_self*self.mone + to_mult_other*other.mone)
#         new_mehane = least_common_d
#         return Frac(new_mone, new_mehane)

#     def __sub__(self, other):
#         least_common_d = lcm(self.mehane, other.mehane)
#         to_mult_self = least_common_d // self.mehane
#         to_mult_other = least_common_d // other.mehane
#         new_mone = (self.mone*to_mult_self - other.mone*to_mult_other)
#         new_mehane = least_common_d
#         return Frac(new_mone, new_mehane)

#     def __mul__(self, other):
#         new_mone = self.mone * other.mone
#         new_mehane = self.mehane * other.mehane
#         return Frac(new_mone, new_mehane)

#     def __truediv__(self, other):
#         if other.mone == 0:
#             raise ZeroDivisionError
#         other.mone, other.mehane = other.mehane, other.mone
#         new_frac = self.__mul__(other)
#         return new_frac

#     def __pow__(self, power):
#         if power == 0:
#             return Frac(1, 1)
#         if power == 1:
#             return self
#         if power == -1:
#             return Frac(self.mehane, self.mone)
#         if power > 0:
#             for i in range(power-1):
#                 self.mone *= self.mone
#                 self.mehane *= self.mehane
#         else:
#             self.mone, self.mehane = self.mehane, self.mone
#             for i in range(-power-1):
#                 self.mone *= self.mone
#                 self.mehane *= self.mehane

#         return Frac(self.mone, self.mehane)

#     def __eq__(self, obj):
#         if type(obj) is Frac:
#             self._reduce()
#             obj._reduce()
#             if self.mone == obj.mone and self.mehane == obj.mehane:
#                 return True

#         return False

#     def __ge__(self, other):
#         least_common_d = lcm(self.mehane, other.mehane)
#         new_self_mone = least_common_d // self.mehane
#         new_other_mone = least_common_d // other.mehane
#         if new_self_mone >= new_other_mone:
#             return True
#         return False

#     def __str__(self):
#         if self.mone < 0 and self.mehane < 0:
#             self.mone, self.mehane = abs(self.mone), abs(self.mehane)
#         elif self.mehane < 0:
#             self.mone = -1*self.mone
#             self.mehane = -1*self.mehane
#         if abs(self.mone) <= abs(self.mehane):
#             return f"{self.mone}/{self.mehane}"
#         if self.mone < 0:
#             num = -1*((-1*self.mone) // self.mehane)
#         elif self.mehane < 0:
#             num = (-1*self.mone // (-1*(self.mehane)))
#         else:
#             num = self.mone // self.mehane
#         new_mone = abs(self.mone) % abs(self.mehane)
#         new_mehane = self.mehane
#         return f"{num} {new_mone}/{new_mehane}"


# fr1 = Frac(21, 36)
# fr2 = Frac(13, 5)
# print(fr1)  # 7/12
# print(fr2)  # 2 3/5
# print(Frac(-3, 6))  # -1/2
# print(Frac(3, -6))  # -1/2
# print(Frac(-3, 2))  # -1 1/2
# print(Frac(6, 3))  # 2 0/1
# print(Frac(0, 3))  # 0/1
# print(fr1+fr2)  # 3 11/60
# print(fr1-fr2)  # -2 1/60
# print(fr2-fr1)  # 2 1/60
# print(fr1*fr2)  # 1 31/60
# print(fr2/fr1)  # 4 16/35
# print(fr1**2)  # 144/49 = 
# print(fr2**-1)  # 5/13
# print(Frac(3, 6) == Frac(2, 4))  # True
# print(fr1 == fr2)  # False
# print(fr1 >= fr2)  # False
# print(fr2 >= fr1)  # True



# class Cycle:
#     def __init__(self, data):
#         self.__datas = [data]
#         self.__cur = data
#         self.__cur_ind = 0
        
#     def insert_next(self, data):
#         self.__datas.insert(self.__cur_ind+1, data)
        
#     def rotate(self):
#         if self.__cur == self.__datas[-1]:
#             self.__cur = self.__datas[0]
#             self.__cur_ind = 0
#         else:
#             cur_index = self.__datas.index(self.__cur)
#             self.__cur = self.__datas[cur_index+1]
#             self.__cur_ind = cur_index+1
#         return self.__cur
    
#     def rotate_back(self):
#         if self.__cur == self.__datas[0]:
#             self.__cur == self.__datas[-1]
#             self.__cur_ind = len(self.__datas)-1
#         else:
#             cur_index = self.__datas.index(self.__cur)
#             self.__cur = self.__datas[cur_index-1]
#             self.__cur_ind = cur_index-1
#         return self.__cur
    
#     def delete(self):
#         if len(self.__datas) == 1:
#             raise LookupError
#         elif self.__cur_ind == len(self.__datas)-1:
#             self.__datas = self.__datas[:-1]
#             self.__cur_ind = 0
#         else:
#             self.__datas = self.__datas[:self.__cur_ind] + self.__datas[self.__cur_ind+1:]
#             self.__cur = self.__datas[self.__cur_ind]
            
            
# c = Cycle(3) 
# c.insert_next(2) 
# c.insert_next(1) 
# print(c.rotate())
# print(c.rotate())
# print(c.rotate())
# print(c.rotate())
# c.delete()
# print(c.rotate_back())




# class Baker:
#     def __init__(self, product, ingredients):
#         self.product = product
#         self.ingredients = ingredients
#         self.storage = {}
#         self.shelf = []        
        
#     def purchase(self, parts):
#         for ingred in parts:
#             if not self.ingredients or ingred not in self.storage.keys():
#                 self.storage[ingred] = 1
#             else:
#                 self.storage[ingred] += 1
    
#     def bake(self):
#         for key in self.storage.keys():
#             if key in self.ingredients:
#                 if self.storage[key] < self.ingredients.count(key):
#                     message = f"Not enough ingredients in storage for {self.product}"
#                     raise Exception(message)
#         for ingred in self.ingredients:
#             for key in self.storage.keys():
#                 if ingred == key and self.storage[key] > 0:
#                     self.storage[key] -= 1
#         self.shelf.append(self.product)
                        
#         return True
    
#     def __str__(self):
#         ingred_dict = {}
#         for ingred in self.ingredients:
#             if not ingred_dict or ingred not in ingred_dict.keys():
#                 ingred_dict[ingred] = 1
#             else:
#                 ingred_dict[ingred] += 1
                
#         message = f"Bakes {self.product} - "
#         for key in ingred_dict.keys():
#             message += str(ingred_dict[key]) + " " + key + " " 
            
#         return message
    
    
# dan = Baker('nuts_delight',['nuts','maple','sugar','cider','almonds', 'nuts'])
# dan.purchase(['maple', 'sugar', 'nuts', 'maple', 'cider'])
# #dan.bake()
# dan.purchase(['nuts', 'almonds'])
# gal = Baker('healthy_bounty', ['maple', 'tahini', 'coconut', 'coconut oil', 'dark chocolate'])
# dan.purchase(['tahini', 'tahini', 'coconut', 'coconut oil', 'dark chocolate'])
# dan.bake()
# print(gal)



# class TextDoc:
#     def __init__(self):
#         self.row = 0
#         self.col = 0
#         self.lines = [""]
        
#     def move_caret(self, row, col):
#         if row < 0 or row >= len(self.lines):
#             raise ValueError
#         if col < 0 or col > len(self.lines[row]):
#             raise ValueError
#         self.row = row
#         self.col = col
#         return None
    
#     def type_in(self, char):
#         if char == "\n":
#             self.row += 1
#             self.col = 0
#             self.lines.append("")
#         else:
#             self.lines[self.row] = self.lines[self.row][:self.col] + char + self.lines[self.row][self.col:]
            
#     def get_current_line(self):
#         return self.lines[self.row]
    

# c = TextDoc()
# c.type_in("a")
# print(c.get_current_line())
# c.move_caret(0, 1)
# c.type_in("b")
# c.move_caret(0, 2)
# c.type_in("c")
# c.move_caret(0, 3)
# c.type_in("d")
# c.move_caret(0, 4)
# c.type_in("e")
# c.move_caret(0, 5)
# c.type_in("f")
# c.move_caret(0, 6)
# print(c.get_current_line())
# c.type_in("\n")
# c.type_in("h")
# c.move_caret(1, 1)
# c.type_in("e")
# c.move_caret(1, 2)
# c.type_in("l")
# c.move_caret(1, 3)
# c.type_in("l")
# c.move_caret(1, 4)
# c.type_in("o")
# print(c.get_current_line())

