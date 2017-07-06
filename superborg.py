import functools
from types import MethodType

def borg(cls):
    """A class decorator for Borg design pattern."""
    cls._state = {}
    cls._new       = cls.__new__
    cls._init      = cls.__init__

    @functools.wraps(cls.__new__)
    def wrapper_new(cls, *args, **kwargs):
        new_inst          = cls._new(cls, *args, **kwargs)
        new_inst.__dict__ = cls._state
        return new_inst

    @functools.wraps(cls.__init__)
    def wrapper_init(self, *args, **kwargs):
        if hasattr(self,"_borg"):
            return
        self._borg = True
        cls._init(self, *args, **kwargs)

    cls.__new__  = MethodType(wrapper_new, cls, type(cls))
    cls.__init__ = wrapper_init

    return cls

def super_borg(cls):
    """A class decorator for the Super Borg design pattern."""
    cls._state = {}
    _new       = cls.__new__
    _init      = cls.__init__

    @functools.wraps(cls.__new__)
    def wrapper_new(cls, *args, **kwargs):
        new_inst          = _new(cls, *args, **kwargs)
        new_inst.__dict__ = cls._state
        return new_inst

    @functools.wraps(cls.__init__)
    def wrapper_init(self, *args, **kwargs):
        if not hasattr(self,"_super_borg"):
            self._super_borg = True
            _init(self, *args, **kwargs)
        if hasattr(self,"__inscribe__") and (args or kwargs):
            self.__inscribe__(*args, **kwargs)

    cls.__new__  = MethodType(wrapper_new, cls, type(cls))
    cls.__init__ = wrapper_init

    return cls

@super_borg
class TestClass(object):
    def __init__(self, val):
        self._list = []

    def __inscribe__(self,val):
        self._list.append(val)

    def __iter__(self):
        return iter(self._list)

a = TestClass(1)
b = TestClass(2)
c = TestClass(3)
d = TestClass()

assert list(TestClass()) == list(d)
assert list(a) == list(d)
print list(a)
