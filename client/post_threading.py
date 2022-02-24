from threading import Thread

class PostThread(Thread):
    """Object that manages the threaded execution for given functions"""
    
    def __init__(self, func):
        """Creates the thread object with the method to be called"""
        Thread.__init__(self,)
        self.func, self.daemon = func, True
    
    def execute(self, *args, **kwargs):
        """1. Store the method call' arguments, starts the thread
           2. Returns the thread object to the caller"""
        self.args, self.kwargs = args, kwargs
        self.start()
        return self

    def kill(self):
        if self.isAlive():
            self._Thread__stop()
            
class Post:
    """Object that provides threaded calls for parent object' methods"""
    def __init__(self, parent):
        self.parent = parent
    
    def __getattr__(self, attr):
        """1. Finds the method asked for in parent object
           2. Encapsulates this method in PostThread' object
           3. Returns the pointer to the execution function"""
        try:
            func = getattr(self.parent, attr)
            post_thread = PostThread(func)
            return post_thread.execute 
        except:
            raise Exception(f"ERROR: Post call on {str(self.parent)}: method {attr} not found")
