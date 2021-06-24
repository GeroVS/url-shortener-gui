from __future__ import with_statement

import contextlib
from urllib import request

try:
    from urllib.parse import urlencode

except ImportError:
    from urllib import urlencode

try:
    from urllib.request import urlopen

except ImportError:
    from urllib import urlopen


from tkinter import *
import clipboard

class Window():
    #shorten url without an preferred alias
    def make_tiny(self, url) -> str:
        request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))  
        print(request_url)  
        with contextlib.closing(urlopen(request_url)) as response:                      
            return response.read().decode('utf-8 ')
    #shorten url with alias
    def make_tiny_alias(self, url, alias) -> str:
        request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url,'alias':alias}))  
        print(request_url)  
        with contextlib.closing(urlopen(request_url)) as response:                      
            return response.read().decode('utf-8 ')
    #initialize the gui
    def __init__(self) -> None:
        self.window = Tk()
    #define window parameters
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        self.window.title("URL tiny Shortener")
        self.window.grid_columnconfigure(1, weight=1)
    #variable for checkbox    
        is_checked = IntVar()
    #define label
        label = Label(self.window, text="Url:", font=("Helvetica", "13"))
        label.grid(row=0, column=1)
    #define url input
        url_input = Entry(self.window, font=("Helvetica", "13"))
        url_input.grid(row=1, column=1, pady=6)
    #define url output
        str_url = StringVar(self.window)
        shortened_url = Label(self.window, textvariable=str_url,  font=("Helvetica", "13"), fg="#fff", bg="#1abc9c")
        shortened_url.grid(row=4, column=1, pady=6)
    #define alias input
        alias_input = Entry(self.window, font=("Helvetica", "13"), state="disabled")
        alias_input.grid(row=2, column=1, pady=6)

    #activate or deactivate alias input
        def checked() -> None:
            if is_checked.get():
                alias_input.configure(state="normal")
            else:
                alias_input.configure(state="disabled")

    #checkbox definition
        chk = Checkbutton(state='active', text="Use Alias:", onvalue=1, offvalue=0, variable=is_checked, command=(lambda : checked()))
        chk.grid(row=2, column=0, pady=6)
        
    #function to invoke either of the two shorteners
        def tiny() -> None:
            url = url_input.get()
            if is_checked.get():
                alias = alias_input.get()
                try:
                    result = self.make_tiny_alias(url,alias)
                    str_url.set(result)
                    url_input.delete(0, END)
                except:
                    str_url.set("Unavailable alias")
            else:
                try:
                    result = self.make_tiny(url)
                    str_url.set(result)
                    url_input.delete(0, END)
                except:
                    str_url.set("Enter url, please")

            
            
    #button definition
        btn = Button(self.window, text="Short Url", padx=8, pady=4, font=("Helvetica", "14"), bg="#2ecc71", fg="#fff", activebackground="#16a085", command=(lambda : tiny()))
        btn.grid(row=3, column=1, pady=6)
    #copy to clipboard function
        def copy_short_url() -> None:
            try:
                clipboard.copy(str_url.get())
            except:
                pass
    #define copy to clipboard button
        cpy_btn = Button(self.window, text="Copy URL", padx=8, pady=4, font=("Helvetica", "14"), bg="#34495e", fg="#fff", activebackground="#16a085", command=(lambda : copy_short_url()))
        cpy_btn.grid(row=3, column=0, pady=6)

#Show the window
    def show(self) -> None:
        self.window.mainloop()

def main():
        window = Window()
        window.show()

if __name__ == "__main__":
    main()