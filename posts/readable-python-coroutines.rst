.. slug: readable-python-coroutines
.. link: 
.. tags: 
.. title: Readable Python coroutines
.. date: 2013/11/10 14:28:51
.. description: 

Quick exercise: write a piece of code that, each time you pass it a word (a
string), tells you if you've passed it that word before. If you're reading a
post with a title like this, it shouldn't take you more than a few minutes. For
bonus points, have an option to ignore case, so it counts 'parrot' and 'Parrot' 
as the same word.

What did you go for? A function with a global variable (yuck!)? A class with a
method? A closure?

How about a coroutine? Here's what that would look like:

.. code:: python

    def have_seen(case_sensitive=False):
        seen = set()
        
        res = None
        while True:
            word = (yield res)
            if not case_sensitive:
                word = word.lower()
            
            res = (word in seen)
            seen.add(word)

And here's how you would use it::

    >>> hs = have_seen()
    >>> next(hs)  # prime it
    >>> hs.send('Hello')
    False
    >>> hs.send('World')
    False
    >>> hs.send('hello')
    True

Coroutines in Python are based on the generator machinery - see the ``yield``
keyword in there? `PEP 342 <http://www.python.org/dev/peps/pep-0342/>`_,
"Coroutines via Enhanced Generators", added the necessary features to Python
2.5, but it's not a very well known part of the language. And it's not hard to
see why - the code above isn't as clear as it should be:

- Emitting and receiving a value happen in the same yield expression. So rather
  than yielding the response at the bottom of the loop, we have to store it in a
  variable and jump back to the top of the loop.
- The coroutine has to emit a value before it can receive one, even though
  there's nothing it really wants to emit. That's why we set ``res = None``
  before the loop, and why the caller has to prime it by calling ``next(hs)``
  before using it. It's easy to write a decorator that calls ``next`` for you,
  but that doesn't make the code inside the coroutine any clearer.

So the standard Python syntax is rather awkward. But we can make it clearer by
using a bit of wrapper code.
The trick is separating sending a value from receiving one:

.. code:: python

    from coromagic import coroutine, receive

    @coroutine
    def have_seen2(case_sensitive=False):
        seen = set()
        
        while True:
            word = (yield receive)
            if not case_sensitive:
                word = word.lower()
            
            yield (word in seen)
            seen.add(word)

We no longer need the `res` variable. Instead, we alternate between two uses of
yield: a receiving yield, where we send the wrapper a token to indicate that
we're ready for a new value, and a sending yield, where we don't expect to get a
value back. The caller can use this in exactly the same way as the original
coroutine, except that the wrapper primes it automatically, so there's no need
to call ``next(hs)``.

The wrapper expects a receiving yield first, and at most one sending yield after
each receiving yield. If a receiving yield is followed by another receiving
yield, without a sending yield inbetween, ``None`` is returned to the caller,
just like a function without a return statement.

Handling exceptions
-------------------

If either of our coroutines above raises an exception, we can't keep using that
coroutine::

    >>> hs.send(12)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "coro_ideas.py", line 8, in have_seen
        word = word.lower()
    AttributeError: 'int' object has no attribute 'lower'
    >>> hs.send('hi')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    StopIteration

I've got a solution of sorts for that, although it still feels a bit awkward.
The coroutine can request a context manager to catch exceptions:

.. code:: python

    from coromagic import get_exception_context

    @coroutine
    def have_seen3(case_sensitive=False):
        exception_context = (yield get_exception_context)
        seen = set()
        
        while True:
            with exception_context:
                word = (yield receive)
                if not case_sensitive:
                    word = word.lower()
                
                yield (word in seen)
                seen.add(word)

The context manager co-ordinates with the wrapper to suppress the exception inside the coroutine, but raise it to the caller::

    >>> hs3 = have_seen3()
    >>> hs3.send(12)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "./coromagic.py", line 28, in send
        raise self.last_exc
      File "./coro_ideas.py", line 47, in have_seen3
        word = word.lower()
    AttributeError: 'int' object has no attribute 'lower'
    >>> hs3.send('hi')
    False

Now the error doesn't stop us processing valid input afterwards.

Who cares about coroutines?
---------------------------

I find them interesting on their own. But this isn't just academic -
there are cases where coroutines can be the clearest way to write something.

The ``have_seen`` example could easily be written with a class or a closure.
Coroutines come into their own for making state machines. With a class or a
closure, the state has to be stored in a variable, and you need a lookup table
to decide how to behave in each state. A coroutine can store the state as the
point where its code is executing.

It's hard to come up with an example of this that's both realistic and
short, but here's my attempt. We're writing a plugin for a chat
application, which lets any chatter say "password foo", silencing everyone until
someone guesses "foo". The application just passes us each message, and expects
a True/False response saying whether it should be broadcast.

.. code:: python

   @coroutine
   def password_game():
       while True:
           # Normal chatting
           while True:
               msg = (yield receive)
               if msg.startswith("password "):
                   password = msg[9:]
                   yield False
                   break
               yield True  # Broadcast
           
           # Waiting for someone to guess the password
           while (yield receive) != password:
               yield False # Don't send messages
           yield True   # Show everyone the password once it has been guessed

In IPython, we have some coroutines for input processing. For instance, the
transformer to strip prompts from pasted code processes the first two lines in a
prompt-detection state. Then it moves into a prompt-stripping state if it
detected a prompt, or a no-op state if it didn't.

The pattern of sending and receiving is also reminiscent of writing a thread
with input and output queues, and waiting for values on those queues. But
threads are messy: you have to deal with synchronisation and shut them
down safely. Calling a cororoutine is as deterministic as calling a function:
it runs, returns a value, and the calling code carries on. Of course, that means
that coroutines themselves don't run in parallel. But you can use them to build
clever things like `tulip <http://code.google.com/p/tulip/>`_, which will become
the ``asyncio`` module in Python 3.4. Tulip can suspend one coroutine and run
others while it waits for data, and then resume it when the data it needs is
ready.

The best resource on coroutines in Python is `this excellent course <http://dabeaz.com/coroutines/>`_ by David Beazley.

Coromagic source code
---------------------

This is the module used in the examples above.

.. listing:: coromagic.py python
