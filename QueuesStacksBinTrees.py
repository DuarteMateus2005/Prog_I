#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:18:03 2024

@author: duartemateus
"""

from random import randint
from abc import ABC, abstractmethod

class Stack(ABC):
  """ API para o tipo Stack """

  @abstractmethod
  def isEmpty(self):
    """returns true iff the stack is empty"""
    pass

  @abstractmethod
  def push(self, item):
    """pushes an item onto the top of the stack"""
    pass

  @abstractmethod
  def peek(self):
    """requires: not isEmpty()
       returns the top item of the stack"""
    pass

  @abstractmethod
  def pop(self):
    """requires: not isEmpty()
       removes the top item on the stack"""
    pass

#####################################################################  

class ListMutStack(Stack):
  """ mutable implementation of Stack API using lists"""

  def __init__(self):
    """ returns an empty stack """
    self._items = list()

  def isEmpty(self):
    return len(self) == 0

  def peek(self):
    return self._items[-1]

  def pop(self):
    self._items.pop()

  def push(self, item):
    self._items.append(item)

  def __len__(self):
    """returns number of elements in stack"""
    return len(self._items)

  def __str__(self):
    """returns a string representation of the stack's state"""
    return str(self._items)[:-1] + '['

#####################################################################

class ListImutStack(Stack):
  """ immutable implementation of Stack API using lists"""

  def __init__(self):
    """ returns an empty stack """
    self._items = list()

  def isEmpty(self):
    return len(self) == 0

  def peek(self):
    return self._items[-1]

  def pop(self):
    st = ListImutStack()
    st._items = self._items[:]
    st._items.pop()
    return st

  def push(self, item):
    st = ListImutStack()
    st._items = self._items[:]
    st._items.append(item)
    return st

  def __len__(self):
    """returns number of elements in stack"""
    return len(self._items)

  def __str__(self):
    """returns a string representation of the stack's state"""
    return str(self._items)[:-1] + '['
  
#####################################################################

class Queue(ABC):
  """ API para o tipo Queue """

  @abstractmethod
  def isEmpty(self):
    """returns true iff queue is empty"""
    pass

  @abstractmethod
  def enqueue(self, item):
    """inserts item at queue's end"""
    pass

  @abstractmethod
  def front(self):
    """requires: not isEmpty()
       returns the item at queue's beginning"""
    pass

  @abstractmethod
  def dequeue(self):
    """requires: not isEmpty()
       removes the item at queue's beginning"""
    pass

#####################################################################

class CircularArrayQueue(Queue):
  """ representing a queue with a circular array """

  def __init__(self, capacity=6):
    self._queue = [None]*capacity
    self._begin = 0
    self._end = 0
    self._size = 0

  def isEmpty(self):
    return self._size == 0

  def enqueue(self, item):
    if self._size == len(self._queue): # queue is full, double array size
      self._reallocate()
    self._queue[self._end] = item
    self._end = self._inc(self._end)
    self._size += 1

  def front(self):
    return self._queue[self._begin]

  def dequeue(self):
    self._queue[self._begin] = None
    self._begin = self._inc(self._begin)
    self._size -= 1

  def _inc(self, n):
    """ increment by 1, using modular arithmetic """
    return (n+1)%len(self._queue)

  def _reallocate(self):
    newQueue = [None] * (2*self._size)
    j = self._begin
    for i in range(self._size):
      newQueue[i] = self._queue[j]
      j = self._inc(j)
    self._begin = 0
    self._end   = self._size
    self._queue = newQueue

  def __len__(self):
    return self._size

  def __str__(self):
    result = []
    j = self._begin
    for i in range(self._size):
      result.append(self._queue[j])
      j = self._inc(j)
    return '<'+str(result)[1:-1]+'<'

#####################################################################

class TestMutStack(ListMutStack):
  """ subclasse de ListMutStack, esta classe inclui igualdade e clonagem, 
      para efeitos de teste """
  def __eq__(self, st):
    """ verifica se self == st """
    st1, st2 = self.copy(), st.copy()
    while not st1.isEmpty() and not st2.isEmpty():
      if st1.peek() != st2.peek():
        return False
      st1.pop()
      st2.pop()
    return st1.isEmpty() and st2.isEmpty()

  def copy(self):
    """ cria uma cópia de self, ie, um novo objecto com o mesmo estado """
    st = TestMutStack()
    st._items = self._items[:]
    return st

def rndStack(maxSize=32, maxElem=1000):
  """ gera uma stack para teste, com conteúdo aleatório """
  size = randint(0, maxSize)
  st = TestMutStack()
  for x in [randint(-maxElem, maxElem) for _ in range(size)]:
    st.push(x)
  return st

#####################################################################

class Deque(ABC):
  """ API para o tipo Deque """

  @abstractmethod
  def isEmpty(self):
    """returns true iff deque is empty"""
    pass

  @abstractmethod
  def first(self):
    """requires: not isEmpty()
       returns deque's first element"""
    pass

  @abstractmethod
  def last(self):
    """requires: not isEmpty()
       returns deque's last element"""
    pass

  @abstractmethod
  def addFirst(self, item):
    """adds item at deque's front"""
    pass

  @abstractmethod
  def addLast(self, item):
    """adds item at deque's back"""
    pass

  @abstractmethod
  def delFirst(self):
    """requires: not isEmpty()
       removes deque's first element"""
    pass

  @abstractmethod
  def delLast(self):
    """requires: not isEmpty()
       removes deque's last element"""
    pass

#####################################################################  

class ListDeque(Deque):
  def __init__(self):
    self._items = []

  def isEmpty(self):
    return self._items == []

  def first(self):
    return self._items[0]

  def last(self):
    return self._items[-1]

  def addFirst(self, item):
    self._items.insert(0, item)

  def addLast(self, item):
    self._items.append(item)

  def delFirst(self):
    self._items.pop(0)

  def delLast(self):
    self._items.pop()

  def __str__(self):
    return ']'+str(self._items)[1:-1]+'['  

#####################################################################  

class DLLDeque(Deque):
  class Node:
    """internal helper class, represents a node object"""
    def __init__(self, item, prev, next):
      self.data = item
      self.prev = prev
      self.next = next

  def __init__(self):
    self._head = None
    self._tail = None

  def isEmpty(self):
    return self._head is None

  def first(self):
    return self._head.data

  def last(self):
    return self._tail.data

  def addFirst(self, item):
    self._head = DLLDeque.Node(item, None, self._head)
    if self._tail is None:    # se deque é vazia
      self._tail = self._head
    else:
      self._head.next.prev = self._head   

  def addLast(self, item):
    self._tail = DLLDeque.Node(item, self._tail, None)
    if self._head is None:
      self._head = self._tail
    else:
      self._tail.prev.next = self._tail

  def delFirst(self):
    if self._head == self._tail:  # se deque tem um só elemento
      self._head = self._tail = None
    else:
      self._head = self._head.next
      self._head.prev = None

  def delLast(self):
    if self._head == self._tail:
      self._head = self._tail = None
    else:
      self._tail = self._tail.prev
      self._tail.next = None

  def __str__(self):
    result, node = [], self._head
    while node is not None:
      result.append(node.data)
      node = node.next
    return ']'+str(result)[1:-1]+'['
  
#####################################################################  


from abc import ABC, abstractmethod
from random import sample, seed

class BinTree(ABC):
  """ API para o tipo Árvore Binária """

  @abstractmethod
  def left(self):
    """returns the left subtree"""
    pass

  @abstractmethod
  def right(self):
    """returns the right subtree"""
    pass

  @abstractmethod
  def data(self):
    """returns the data at root"""
    pass

#####################################################################  
  
class MutBinTree(BinTree):
  """ implementação mutável de uma árvore binária """
  
  def __init__(self, data, left=None, right=None):
    self._data  = data
    self._left  = left 
    self._right = right

  @property
  def left(self):
    return self._left

  @left.setter
  def left(self, value):
    self._left = value

  @property
  def right(self):
    return self._right

  @right.setter
  def right(self, value):
    self._right = value

  @property
  def data(self):
    return self._data

  @data.setter
  def data(self, value):
    self._data = value
    
#####################################################################  
    
class LinkedBinTree(BinTree):
  """ implementação imutável de uma árvore binária """

  def __init__(self, data, left=None, right=None):
    self._data  = data
    self._left  = left 
    self._right = right

  @property
  def left(self):
    return self._left

  @property
  def right(self):
    return self._right

  @property
  def data(self):
    return self._data

  def __iter__(self):
    return LinkedBinTree.TreeIterator(self)

#####################################################################  

  class TreeIterator:
    """ classe interna responsável pelos iteradores """
    def __init__(self, tree):
      self._stack = ListMutStack()
      self._stack.push(tree)

    def __iter__(self):
      return self

    def __next__(self):
      if self._stack.isEmpty():
        raise StopIteration
      node = self._stack.peek()
      self._stack.pop()
      if node.right:
        self._stack.push(node.right)
      if node.left:
        self._stack.push(node.left)
      return node.data
    
#####################################################################      
    
class BST(MutBinTree):
  """ Implementação de uma árvore binária de pesquisa (BST)
      Os elementos a guardar têm de ser comparáveis, ie, 
      implementar o dunder __lt__.
      A invariante da classe determina que os objetos devem sempre
      representar uma BST """
      
  def __init__(self, data=None, left=None, right=None):
    self._data  = data
    self._left  = left 
    self._right = right

  def search(self, val):
    if self.data == val:
      return True
    if val < self._data:
      return self.left.search(val)
    else:
      return self.right.search(val)

  def insert(self, val):
    if self.data is None:
      self._data = val
    if val < self.data:
      if self.left is None:
        self._left = BST(val)
      else:
        self._left.insert(val)
    elif val > self.data:
      if self.right is None:
        self._right = BST(val)
      else:
        self._right.insert(val)

  def delete(self, val):
    if val < self.data and self.left:  # search value while left/right exists
      self._left = self.left.delete(val)
    elif val > self.data and self.right:
      self._right = self.right.delete(val)
    elif val == self.data:   # found value
      if self.left is None:  # only has right subtree
        return self.right
      if self.right is None: # only has left subtree
        return self.left
      # ok, the node has two children
      # let's find the next value (ie, the smallest from the right subtree)
      # place it here, and delete its old node
      min_node = self.right
      while min_node.left:   # go as left as possible
        min_node = min_node.left 
      self._data = min_node.data                     # place it here
      self._right = self.right.delete(min_node.data) # delete its old node
    return self
  
#################
  
def rndTree(size, rndSeed=None, xs=None, doOnce=True):
  """ gera recursivamente uma árvore binária aleatória """
  if size == 0:
    return None
  if doOnce:
    seed(rndSeed) # para reprodutibilidade
    xs = sample(range(5*size), size)
    doOnce = False

  size_left  = randint(0,size//2)
  size_right = size - size_left - 1
  return LinkedBinTree(xs[0], 
                       rndTree(size_left,  rndSeed, xs[1:size_left+1], doOnce), 
                       rndTree(size_right, rndSeed, xs[size_left+1: ], doOnce))  

def rndBST(size, rndSeed=None):
  """ gera uma BST aleatória com valores 0 a n-1 """
  seed(rndSeed) # para reprodutibilidade
  xs = sample(range(size), size)
  t = BST()  
  for x in xs:
    t.insert(x)
  return t

#################

def size(t):
  if t is None:
    return 0
  return 1 + size(t.left) + size(t.right)

def height(tree):
  if tree is None:
    return 0
  return 1 + max(height(tree.left), height(tree.right))

def occurrences(tree, item):
  if tree is None:
    return 0
  return (occurrences(tree.left,  item) +
          occurrences(tree.right, item) +
          (1 if tree.data == item else 0))

def preOrder(t, visit):
  if t:
    visit(t)
    preOrder(t.left,  visit)
    preOrder(t.right, visit)
    
def inOrder(t, visit):
  if t:
    inOrder(t.left,  visit)
    visit(t)
    inOrder(t.right, visit)

def postOrder(t, visit):
  if t:
    postOrder(t.left,  visit)
    postOrder(t.right, visit)
    visit(t)

def breathOrder(t, visit):
  q = CircularArrayQueue()
  q.enqueue(t)

  while not q.isEmpty():
    node = q.front()
    visit(node)
    q.dequeue()
    if node.left:
      q.enqueue(node.left)
    if node.right:
      q.enqueue(node.right)    

#################

#from graphviz import Digraph # https://graphviz.readthedocs.io

#def showTree(tree, styleEmpty='invis'):
#  adaptado de https://h1ros.github.io/posts/introduction-to-graphviz-in-jupyter-notebook/ 
#  styleGraph = {'nodesep':'.25', 'ranksep':'.2'}
#  styleNode  = {'shape':'circle', 'width':'.3', 'fontsize':'10', 'fixedsize':'True'}
#  styleEdge  = {'arrowsize':'.6'} 
#  def make(tree, nullIdx, styleEmpty, dot=None):
#    if dot is None:
#      dot = Digraph(graph_attr=styleGraph, node_attr=styleNode, edge_attr=styleEdge)
#      dot.node(str(tree), str(tree.data))

#    if tree.left:
#      dot.node(str(tree.left), str(tree.left.data))
#      dot.edge(str(tree), str(tree.left))
#      dot = make(tree.left, nullIdx, styleEmpty, dot)
#    else: # imprimir sub-árvores vazias invisiveis, para melhorar o aspeto final da árvore
#      dot.node(str(tree.left)+str(nullIdx[0]), '', {'style':styleEmpty, 'width':'.1'})
#      dot.edge(str(tree), str(tree.left)+str(nullIdx[0]), color='transparent' if styleEmpty=='invis' else 'blue', minlen='1')
#      nullIdx[0]+=1

#    if tree.right:
#      dot.node(str(tree.right), str(tree.right.data))
#      dot.edge(str(tree), str(tree.right))
#      dot = make(tree.right, nullIdx, styleEmpty, dot)
#    else: 
#      dot.node(str(tree.right)+str(nullIdx[0]), '', {'style':styleEmpty, 'width':'.1'})
#      dot.edge(str(tree), str(tree.right)+str(nullIdx[0]), color='transparent' if styleEmpty=='invis' else 'blue', minlen='1')
#      nullIdx[0]+=1

#    return dot
  
#  dot = make(tree, [0], styleEmpty)
#  #display(dot) # comentar se não estiver nos notebooks
#  return dot

###########################

def sameStructure(t1, t2):
  if not t1 or not t2:       # if either is empty
    return not t1 and not t2 #  returns True iff both are empty  
  return sameStructure(t1.left, t2.left) and sameStructure(t1.right, t2.right)

def equals(t1, t2):
  if not t1 or not t2:       # if either is empty
    return not t1 and not t2 #  returns True iff both are empty
  return (t1.data == t2.data and 
          sameStructure(t1.left, t2.left) and 
          sameStructure(t1.right, t2.right))

def copy(t):
  if t is None:
    return None
  copyLeft  = copy(t.left)
  copyRight = copy(t.right)
  return LinkedBinTree(t.data, copyLeft, copyRight)

def mirror(t):
  if t is None:
    return None
  return LinkedBinTree(t.data, mirror(t.right), mirror(t.left))

def isBalanced(t):
  if t is None:
    return True
  h1, h2 = height(t.left), height(t.right)
  return abs(h1-h2) <= 1 and isBalanced(t.left) and isBalanced(t.right)

def isBST(t):
  if t is None:
    return True
  if (t.left and t.left.data > t.data) or (t.right and t.right.data < t.data):
    return False
  return isBST(t.left) and isBST(t.right)

space  = '    '
branch = '│   '
first  = '├── '
last   = '└── '

def printTree(t, prefix='', isLast=True):
  print(prefix, end='')
  if isLast:
    print(last, end='')
    prefix += space
  else:
    print(first, end='')
    prefix += branch
  print(t.data)
  if t.left:
    printTree(t.left, prefix, False)
  if t.right:
    printTree(t.right, prefix, True)

def fromList(xs, i=0):
  """ build tree from list description (use None for unoccupied positions) """
  if i>=len(xs) or xs[i] is None:
    return None
  return LinkedBinTree(xs[i], 
                       fromList(xs, 2*i+1),
                       fromList(xs, 2*i+2))

def lastIdx(t, idx=0, maxIdx=None):
  if t is None:
    return -1
  if maxIdx is None:
    maxIdx = [0]
    
  maxIdx[0] = max(maxIdx[0], idx)
  if t.left:
    lastIdx(t.left,  2*idx+1, maxIdx)
  if t.right:
    lastIdx(t.right, 2*idx+2, maxIdx)
  return maxIdx[0]

def toList(t, i=0, result=None):
  if result is None:
    result = [None] * (lastIdx(t)+1)
  if t is None or i >= len(result):
    return []
  
  result[i] = t.data
  toList(t.left,  2*i+1, result)
  toList(t.right, 2*i+2, result)
  return result

#####################################################################  
import random


valores = random.shuffle([i for i in range(1,n+1)])
arv = MutBinTree()
def rndCompleteTree(n):
    if valores == []:
        return arv
    else 
    












  