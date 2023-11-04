import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog
import tkinter.messagebox
import time
from  ds_messenger import DirectMessage
from  ds_messenger import DirectMessenger

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # a list of the Direct messages
        self._posts = {}
        self._posts2 = []
        self.nextid = 0
        self.current_user = None
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    def set_user(self, username, password):
        self.username = username
        self.password = password
        self.ds_client = DirectMessenger(username=username, password=password)
        self.load_data()
        
    def load_data(self):
        allMsgs = self.ds_client.retrieve_all()
        self._posts.clear()
        for m in allMsgs:
            if self._posts.__contains__(m.recipient):
                self._posts[m.recipient].append(m)
            else:
                self._posts[m.recipient] = [m]
        
        x = self.posts_tree.get_children()
        for item in x:
            self.posts_tree.delete(item)
            
        self.nextid = 0
        for u in self._posts.keys():
            self.posts_tree.insert('', self.nextid, self.nextid, text=u)
            self.nextid = self.nextid + 1
        for u in self._posts2:
            if u not in self._posts.keys():
                self.posts_tree.insert('', self.nextid, self.nextid, text=u)
                self.nextid = self.nextid + 1
        
        self.dispaly_user(self.current_user)
        self.root.after(5000, self.load_data)
                        
    def dispaly_user(self, username):
        if username is None:
            return
        
        allMsgs = self._posts[username]
        self.entry_editor.delete('1.0', 'end')
        for m in allMsgs:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(m.timestamp)))
            self.entry_editor.insert('end', m.recipient + " (" + t + ")\n")
            self.entry_editor.insert('end', "    " + m.message + "\n")
            self.entry_editor.insert('end', "\n")
            
    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        username = (list(self._posts.keys()))[index]
        self.current_user = username
        self.dispaly_user(username)
 
    """
    Inserts a single post to the post_tree widget.
    """
    def send_click(self):
        c = self.input_editor.get('1.0', 'end').rstrip()
        if self.current_user is None:
            tkinter.messagebox.showwarning(title='warnning', message='not user selected')
        else:
            self.ds_client.send(c, self.current_user)
            self.input_editor.delete('1.0', 'end')

    """
    Inserts a single post to the post_tree widget.
    """
    def add_click(self):
        username = tkinter.simpledialog.askstring(parent = self.root, title = 'Enter password',prompt='Enter password:',initialvalue = 'user800')
        if username is not None and len(username) > 0:
            self._posts2.append(username)
            if username not in self._posts.keys():
                self._posts[username] = []
                self.posts_tree.insert('', self.nextid, self.nextid, text=username)
                self.nextid = self.nextid + 1
                
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):

        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
 
        post_frame = tk.Frame(master=posts_frame, bg="")
        post_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.posts_tree = ttk.Treeview(post_frame, height=19)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        add_frame = tk.Frame(master=posts_frame, bg="")
        add_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        add_button = tk.Button(master=add_frame, text="Add User", width=20, height=1)
        add_button.configure(command=self.add_click)
        add_button.pack(fill=tk.NONE, side=tk.RIGHT, expand=False, padx=5, pady=5) 
        
        right_frame = tk.Frame(master=self, bg="")
        right_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        
        entry_frame = tk.Frame(master=right_frame, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

        input_frame = tk.Frame(master=right_frame, bg="")
        input_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
 
        self.input_editor = tk.Text(input_frame, height=5)
        self.input_editor.pack(fill=tk.Y, side= tk.TOP, expand=True, padx=5, pady=5)
 
        send_frame = tk.Frame(master=input_frame, bg="")
        send_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        send_button = tk.Button(master=send_frame, text="Send", width=15, height=1)
        send_button.configure(command=self.send_click)
        send_button.pack(fill=tk.NONE, side=tk.RIGHT, expand=False, padx=5, pady=5)        
   
"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""
class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
 
    def set_user(self):
        self.username = None
        self.password = None
        while self.username is None or self.password is None:
            self.username = tkinter.simpledialog.askstring(parent = self.root, title = 'Enter username',prompt='Enter username:',initialvalue = 'user800')
            self.password = tkinter.simpledialog.askstring(parent = self.root, title = 'Enter password',prompt='Enter password:',initialvalue = 'user800')

        self.body.set_user(str(self.username), str(self.password))
  
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):

        self.body = Body(self.root)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
 
if __name__ == "__main__":
 
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Messenger Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    
    app.set_user()
    
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()