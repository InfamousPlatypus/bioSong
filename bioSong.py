import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import urllib
import urllib.request
import json
import os

xc_API = "http://www.xeno-canto.org/api/2/recordings?query="
Large_Font = ("Verdana", 12)


def set_dir():
    path = filedialog.askdirectory(initialdir="/", title="Select A Directory")
    os.chdir(path)
    return(path)


def error_popup(err_type, err_msg):
    messagebox.showerror(err_type, err_msg)


def question_popup(title, question, action):
    answer = messagebox.askyesno(title, question)
    if answer == "yes":
        action = action()
        return action


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


class bioSong(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="icon.ico")
        tk.Tk.wm_title(self, "bioSong")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Set Directory", command=set_dir)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        xc_menu = tk.Menu(menubar, tearoff=0)
        xc_menu.add_command(
            label="Search", command=lambda: self.show_frame(SearchPage))
        menubar.add_cascade(label="Xeno-Canto", menu=xc_menu)

        datamenu = tk.Menu(menubar, tearoff=0)
        datamenu.add_command(label="Convert to MP3", command=set_dir)
        datamenu.add_command(label="Resample", command=set_dir)
        datamenu.add_command(label="STFT", command=set_dir)
        menubar.add_cascade(label="Data Manipulation", menu=datamenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        for f in (StartPage, SearchPage):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        page_name = SearchPage.__name__
        self.frames[page_name] = frame

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()

    def get_page(self, page_name):
        return self.frames[page_name]
# -----------------------------------------------------------
#


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="start page", font=Large_Font)
        label.pack()
# -----------------------------------------------------------


class SearchPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        input_frame = ttk.Frame(self)
        input_frame.pack(fill='both')
        tab_control = ttk.Notebook(input_frame)
        normal_search = ttk.Frame(tab_control)
        advanced_search = ttk.Frame(tab_control)
        download = ttk.Frame(tab_control)
        tab_control.pack(expand=1, fill="both")


        # Search tab -----------------------------------------
        tab_control.add(normal_search, text="Search")
        label = ttk.Label(
            normal_search, text="Xeno-Canto Search", font=Large_Font)

        self.species_label = ttk.Label(normal_search, text="Species:")
        self.species_input = ttk.Entry(normal_search)

        self.country_label = ttk.Label(normal_search, text="Country:")
        self.country_input = ttk.Entry(normal_search)

        self.search_btn = ttk.Button(normal_search, text="Search", command=lambda: self.chk_search_input(
        self.species_input.get(), self.country_input.get()))

        label.grid(row=0, column=0, columnspan=2,
                   sticky="nsew", padx=20, pady=10)
        self.species_label.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        self.species_input.grid(row=0, column=3, sticky="w")
        self.country_label.grid(row=0, column=4, sticky="e", padx=10, pady=10)
        self.country_input.grid(row=0, column=5, sticky="w")
        self.search_btn.grid(row=0, column=6, sticky="w", padx=10, pady=10)

        # Advanced Search tab -----------------------------------------
        tab_control.add(advanced_search, text="Advanced Search")


        # Download tab -----------------------------------------
        tab_control.add(download, text="Download")

        self.download_all_btn = ttk.Button(download, text="Download All", command=lambda: self.xc_download_all_recs(temp))
        self.download_selected_btn = ttk.Button(download, text="Download Selected", command=lambda: self.xc_download_selected_recs(temp))

        self.download_all_btn.grid(row=0, column=0, sticky="e", padx=20, pady=10)
        self.download_selected_btn.grid(row=0, column=1, sticky="w", padx=20, pady=10)



        results_frame = ttk.Frame(self, relief="groove", borderwidth = 1)
        results_frame.pack(fill='both', expand=True)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        self.results_label = ttk.Label(results_frame, text="Results: ")
        self.search_results = ttk.Treeview(results_frame)
        self.search_results['columns'] = (
            "length", "country", "location", "type", "cat")
        self.search_results.heading("#0", text='Species', anchor='w', command=lambda: self.sortby(
            self.search_results, "#0", False))
        self.search_results.column("#0", anchor="w", width=200)
        self.search_results.heading("length", text='Length (s)', anchor='w', command=lambda: self.sortby(
            self.search_results, "length", False))
        self.search_results.column('length', anchor='w', width=100)
        self.search_results.heading('country', text='Country', anchor='w', command=lambda: self.sortby(
            self.search_results, "country", False))
        self.search_results.column('country', anchor='w', width=125)
        self.search_results.heading('location', text='Location', anchor='w', command=lambda: self.sortby(
            self.search_results, "location", False))
        self.search_results.column('location', anchor='w', width=125)
        self.search_results.heading('type', text='Type', anchor='w', command=lambda: self.sortby(
            self.search_results, "type", False))
        self.search_results.column('type', anchor='w', width=100)
        self.search_results.heading('cat', text='Cat.nr', anchor='w', command=lambda: self.sortby(
            self.search_results, "cat", False))
        self.search_results.column('cat', anchor='w', width=150)
        treeYScroll = ttk.Scrollbar(results_frame, orient="vertical")
        treeYScroll.configure(command=self.search_results.yview)
        self.search_results.configure(yscrollcommand=treeYScroll.set)

        self.search_results.rowconfigure(0, weight=1)
        self.search_results.columnconfigure(0, weight=1)

        # Creat search results view
        self.results_label.grid(row=0, column=0, sticky="w", pady=2)
        self.search_results.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        treeYScroll.grid(row=1, column=0, sticky="nse", pady=6, padx=7)

        self.status_label = ttk.Label(self, text="", border=1)
        self.status_label.pack(side="bottom", fill='x')

    num_recs = None
    temp = None
    # Checks if user has actually input something
    def chk_search_input(self, species, country):
        species = species.strip()
        country = country.strip()
        if species == "" and country == "":
            error_popup("Warning", "Please input a species and or a country.")
        else:
            if len(species) != 0 and len(country) != 0 and hasNumbers(species + country) == False:
                if " " in species:
                    self.status_label.config(
                        text="Retrieving Search Results...")
                    self.species_input.delete(0, 'end')
                    self.country_input.delete(0, 'end')
                    self.update_idletasks()
                    self.xc_if_both(species, country)
                else:
                    self.species_input.delete(0, 'end')
                    self.country_input.delete(0, 'end')
                    error_popup(
                        "Warning", "Please use valid search criteria.\nExample species format: Genus species\nNumbers are not allowed")
            else:
                if species == "" and len(country) != 0 and hasNumbers(country) == False:
                    self.status_label.config(
                        text="Retrieving Search Results...")
                    self.country_input.delete(0, 'end')
                    self.update_idletasks()
                    self.xc_if_country(country)
                else:
                    if " " in species and hasNumbers(species) == False:
                        self.status_label.config(
                            text="Retrieving Search Results...")
                        self.species_input.delete(0, 'end')
                        self.update_idletasks()
                        self.xc_if_species(species)
                    else:
                        self.species_input.delete(0, 'end')
                        self.country_input.delete(0, 'end')
                        error_popup(
                            "Warning", "Please use valid search criteria.\nExample species format: Genus species\nNumbers are not allowed")

    # sets up xc api link if country and call xc_get_data
    def xc_if_country(self, usr_input):
        country = usr_input.replace(" ", "&")
        link = xc_API + "cnt:" + country
        country = ""
        self.xc_get_json(link, country, False)

    # sets up xc api link if species and call xc_get_data
    def xc_if_species(self, usr_input):
        genus, species = usr_input.split(" ")
        link = xc_API + genus + "%20" + species
        country = ""
        self.xc_get_json(link, country, False)

    # sets up xc api link if species and call xc_get_data
    def xc_if_both(self, species, country):
        genus, species = species.split(" ")
        link = xc_API + genus + "%20" + species
        self.xc_get_json(link, country, True)

    # gets the json file
    def xc_get_json(self, link, country, both):
        global temp
        temp = urllib.request.urlopen(link)
        status = temp.getcode()
        if status == 200:
            temp = json.load(temp)
            if temp["numRecordings"] == "0":
                self.species_input.delete(0, 'end')
                self.country_input.delete(0, 'end')
                error_popup(
                    "Error", "There seems to have been an error with your request.\nNo recordings found.")
            else:
                self.populate_search_results(temp, country, both)
        else:
            self.species_input.delete(0, 'end')
            self.country_input.delete(0, 'end')
            error_popup("Error", "Code: " + status +
                        "There seems to have been an error with your request.")

    # Populates the list view for user
    def populate_search_results(self, temp, country, both):
        global num_recs
        for row in self.search_results.get_children():
            self.search_results.delete(row)
        if both == True:
            count = 0
            for r in temp["recordings"]:
                co = r["cnt"]
                if co.lower() == country.lower():
                    en = r["en"]
                    ge = r["gen"]
                    sp = r["sp"]
                    le = r["time"]
                    co = r["cnt"]
                    lo = r["loc"]
                    ty = r["type"]
                    nr = r["id"]
                    self.search_results.insert(
                        "", "end", text=ge + " " + sp + " - " + en, values=(le, co, lo, ty, "XC" + nr))
                    count += 1
            num_recs = str(count)
            num_spec = temp["numSpecies"]
            self.status_label.config(
                text="Search Results:  " + num_recs + " recordings from " + num_spec + " species found.")
        else:
            num_recs = temp["numRecordings"]
            num_spec = temp["numSpecies"]
            self.status_label.config(
                text="Search Results:  " + num_recs + " recordings from " + num_spec + " species found.")
            for r in temp["recordings"]:
                en = r["en"]
                ge = r["gen"]
                sp = r["sp"]
                le = r["time"]
                co = r["cnt"]
                lo = r["loc"]
                ty = r["type"]
                nr = r["id"]
                self.search_results.insert(
                    "", "end", text=ge + " " + sp + " - " + en, values=(le, co, lo, ty, "XC" + nr))

    # Sort search data
    def sortby(self, tree, col, descending):
        """Sort tree contents when a column is clicked on."""
        # grab values to sort
        data = [(tree.set(child, col), child)
                for child in tree.get_children('')]

        # reorder data
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

        # switch the heading so that it will sort in the opposite direction
        tree.heading(col,
                     command=lambda col=col: self.sortby(tree, col, int(not descending)))

    def xc_download_all_recs(self, temp):
        path = set_dir()
        self.status_label.config(text="Downloading...")
        self.update_idletasks()
        self.popup = tk.Toplevel()
        self.popup.geometry("300x200")
        tk.Label(self.popup, text="Downloading recording: ").pack(pady = 5)
        curr_dl = tk.Label(self.popup, text="")
        curr_dl.pack() 
        tk.Label(self.popup, text=" of " + num_recs).pack()    
        progress = 0
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            self.popup, variable=progress_var, maximum=100)
        progress_bar.pack(fill="x", anchor="w", expand="yes", pady = 5, padx = 5)
        self.cancel_btn = ttk.Button(self.popup, text="Cancel", command=lambda: self.stop()) 
        self.cancel_btn.pack(pady = 10)     
        self.popup.pack_slaves()
        progress_step = float(100.0/len(temp["recordings"]))
        global downloading
        downloading = True
        if downloading == True:
            count = 0
            for p in temp["recordings"]:
                recording_url = "https:" + p["file"]
                download_file = "XC" + p["id"] + " - " + p["en"] + \
                    " - " + p["gen"] + " " + p["sp"] + ".mp3"
                full_filename = os.path.join(path, download_file)
                urllib.request.urlretrieve(recording_url, full_filename)
                self.popup.update()
                curr_dl.configure(text = count)
                progress += progress_step
                progress_var.set(progress)
                count +=1
            self.status_label.config(text="")

    def xc_download_selected_recs(self, temp):
        path = set_dir()
        self.status_label.config(text="Downloading...")
        self.update_idletasks()
        self.popup = tk.Toplevel()
        self.popup.geometry("300x200")
        tk.Label(self.popup, text="Downloading recording: ").pack(pady = 5)
        curr_dl = tk.Label(self.popup, text="")
        curr_dl.pack() 
        tk.Label(self.popup, text=" of " + num_recs).pack()    
        progress = 0
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            self.popup, variable=progress_var, maximum=100)
        progress_bar.pack(fill="x", anchor="w", expand="yes", pady = 5, padx = 5)
        self.cancel_btn = ttk.Button(self.popup, text="Cancel", command=lambda: self.stop()) 
        self.cancel_btn.pack(pady = 10)     
        self.popup.pack_slaves()
        progress_step = float(100.0/len(temp["recordings"]))
        global downloading
        downloading = True
        selected_items = self.search_results.selection()
        for selected_item in selected_items:
            cat_nr = selected_item["cat"]
            for p in temp["recordings"]:
                if cat_nr == p["id"]:
                    recording_url = "https:" + p["file"]
                    download_file = "XC" + p["id"] + " - " + p["en"] + \
                        " - " + p["gen"] + " " + p["sp"] + ".mp3"
                    full_filename = os.path.join(path, download_file)
                    urllib.request.urlretrieve(recording_url, full_filename)
                    self.popup.update()
                    curr_dl.configure(text = count)
                    progress += progress_step
                    progress_var.set(progress)
                    count +=1
        self.status_label.config(text="")

    def stop(self):
        global downloading
        downloading = False
        self.status_label.config(text="")
        self.update_idletasks()
        self.popup.destroy()


# -----------------------------------------------------------


app = bioSong()
app.geometry("950x500")
app.mainloop()
