"""
Created on the 2nd of October, 2017

[11/10] This is an effective replacement to GapiExtend.py, in
conjunction with k.py. This contains the container objects
that are used in other places in GAPI.

As of now, only MLS is in use. Queue WILL be used at a later point,
but LinkedMLS will not. It only existed to allow for stacks to have
functions attached to them, but the structure has been reworked so that
detections.py no longer needs a LinkedMLS (everything related to detectors
goes by the stack names of MLS objects now anyways).
"""

from collections import deque
from threading import Thread
from time import clock

class Queue:
    queue = deque
    def __init__(self):
        self.queue = deque()

    def enqueue(self, func, isLong=False, **kwargs):
        self.queue.append((func, isLong, kwargs))

    def dequeue(self): # [0]: func, [1]: isLong, [2]: kwargs
        data = self.queue.popleft()
        lamb = lambda: data[0](**data[2])
        if data[1]:
            Thread(target=lamb).start()
            return False
        lamb();
        return True

    def dequeue_for_time(self, time):
        start = clock()
        while start + time > clock():
            try:
                self.dequeue()
            except IndexError:
                return True
        return False

class MLS:
    """
    Multi-Levelled Stack
    That's not an accurate description of what this class actually is,
    but the name is being held for historical reasons.
    """
    stacks = dict
    order = list
    enforceType = type
    def __init__(self, stacks):
        self.stacks = dict()
        self.order = list(stacks)
        for stack in stacks:
            self.stacks[stack] = list()

    def __repr__(self):
        string = ""
        for item, ref, i in self:
            string += "{}, {}, {}\n".format(item, ref, i)
        return string[0:len(string)-2]

    def __iter__(self): # [0]: item, [1]: stack, [2]: index
        for ref in self.order:
            for i in range(len(self.stacks[ref])):
                if self.stacks[ref] != None:
                    yield self.stacks[ref][i], ref, i

    def __len__(self):
        return sum((len(x) for x in self.stacks.values()))

    def move_object(self, obj, newStack):
        ... # NOT DONE

    def find_object(self, obj):
        for item, ref, i in self:
            if item is obj:
                return ref, i

    def remove_object(self, obj):
        ref, i = self.find_object(obj)
        self.stacks[ref][i] = None

    def append_object(self, obj, stack):
        self.stacks[stack].append(obj)

    def add_object(self, obj, stack):
        for i in range(len(self.stacks[stack])):
            if self.stacks[stack][i] == None:
                self.stacks[stack][i] = obj
                return
        self.append_object

    def insert_object(self, obj, stack, pos):
        self.stacks[stack].insert(pos, obj)

class LinkedMLS(MLS):
    link = dict
    def __init__(self, stacks, stackFuncs):
        super().__init__(stacks)
        self.link = dict()
        for ref, func in zip(self.order, stackFuncs):
            self.link[ref] = func

    def __iter__(self):
        generator = super().__iter__()
        for item, ref, i in generator:
            yield item, ref, i, self.link[ref] # [0]: item, [1]: ref, [2]: index, [3]: func




            
