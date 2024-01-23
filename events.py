class ObjectWithEvents(object):
    callbacks = None

    def on(self, event_name, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if event_name not in self.callbacks:
            self.callbacks[event_name] = [callback]
        else:
            self.callbacks[event_name].append(callback)

    def trigger(self, event_name):
        if self.callbacks is not None and event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(self)

class MyClass(ObjectWithEvents):
    def __init__(self, contents):
        self.contents = contents

    def __str__(self):
        return "MyClass containing " + repr(self.contents)

def echo(value): # because "print" isn't a function...
    print value

o = MyClass("hello world")
o.on("example_event", echo)
o.on("example_event", echo)
o.trigger("example_event") # prints "MyClass containing \"Hello World\"" twice