from functools import wraps

# Tokens
receive = object()
get_exception_context = object()

class CoroutineWrapper(object):
    last_exc = None
    
    def __init__(self, generator):
        self.gen = generator
        
        ready = next(self.gen)
        if ready is get_exception_context:
            ready = self.gen.send(ExceptionContext(self))
        assert ready == receive
    
    def send(self, arg):
        self.last_exc = None
        
        res = self.gen.send(arg)
        if res is receive:
            res = None
        else:
            assert next(self.gen) is receive
        
        if self.last_exc is not None:
            raise self.last_exc
        
        return res

def coroutine(genfunc):
    """Decorator for a generator function to wrap it as a coroutine."""
    @wraps(genfunc)
    def wrapped(*args, **kwargs):
        return CoroutineWrapper(genfunc(*args, **kwargs))
    
    return wrapped

class ExceptionContext(object):
    def __init__(self, corowrapper):
        self.corowrapper = corowrapper
    
    def __enter__(self):
        pass
    
    def __exit__(self, type, value, tb):
        if type is None:
            return
        if type is GeneratorExit:
            return False
        
        # Pass other exceptions to the wrapper, and silence them for now
        self.corowrapper.last_exc = value
        return True
            
