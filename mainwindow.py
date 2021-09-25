from tkinter import *
from tkinter.ttk import Treeview
from controller import Controller
from configuration import CyberleninkaConfiguration
from webbrowser import open


class Widget:
    def __init__(self):
        self.__controller = Controller()
        self.__configuration = CyberleninkaConfiguration()
        self.__window = Tk()
        self.__window.wm_minsize(640, 480)

        self.__parameters_frame = None

        self.__label_max_page = None
        self.__var_max_page = None
        self.__inputbox_max_page = None

        self.__var_filter = None
        self.__drop_filters_button = None

        self.__checkbox_vak = None
        self.__label_vak = None

        self.__checkbox_rsci = None
        self.__label_rsci = None

        self.__checkbox_scopus = None
        self.__label_scopus = None

        self.__table_frame = None
        self.__table_result = None
        self.__columns_num = 8
        self.__table_entries = []

        self.__inputbox_keywords = None
        self.__var_keywords = None
        self.__start_button = None
        self.__label_status = None
        self.__var_status = None

        self.__menu = None

    def __drop_filters_button_clicked(self):
        self.__var_filter.set(0)

    def __update_table(self, results):
        self.__table_frame.delete(*self.__table_frame.get_children())
        for i in range(len(results)):
            self.__table_frame.insert('', 'end',
                                      values=(i+1, results[i].title, results[i].link, results[i].authors,
                                              results[i].year, '\u2713' if results[i].rsci else '',
                                              '\u2713' if results[i].vak else '',
                                              '\u2713' if results[i].scopus else ''))

    def __start_button_clicked(self):
        self.__var_status.set('Searching...')
        self.__window.update()
        self.__configuration.keywords = self.__var_keywords.get()
        self.__configuration.max_page = self.__var_max_page.get()
        self.__configuration.filter_var = self.__var_filter.get()
        results = self.__controller.start(self.__configuration)
        self.__var_status.set('Done!')
        self.__update_table(results)

    def __configuration_parameter_frame(self):
        self.__parameters_frame = Frame(self.__window)

        self.__label_max_page = Label(self.__parameters_frame, text='Number of pages')
        self.__label_max_page.grid(column=0, row=0)
        self.__inputbox_max_page = Entry(self.__parameters_frame, width=10)
        self.__var_max_page = IntVar()
        self.__var_max_page.set(self.__configuration.max_page)
        self.__inputbox_max_page.config(textvariable=self.__var_max_page)
        self.__inputbox_max_page.grid(column=0, row=1)

        self.__var_filter = IntVar()
        self.__var_filter.set(self.__configuration.filter_var)

        self.__label_rsci = Label(self.__parameters_frame, text='RSCI')
        self.__label_rsci.grid(column=1, row=0)
        self.__checkbox_rsci = Radiobutton(self.__parameters_frame, variable=self.__var_filter,
                                           value=self.__configuration.RSCI_VAR)
        self.__checkbox_rsci.grid(column=1, row=1)

        self.__label_vak = Label(self.__parameters_frame, text='ВАК')
        self.__label_vak.grid(column=2, row=0)
        self.__checkbox_vak = Radiobutton(self.__parameters_frame, variable=self.__var_filter,
                                          value=self.__configuration.VAK_VAR)
        self.__checkbox_vak.grid(column=2, row=1)

        self.__label_scopus = Label(self.__parameters_frame, text='Scopus')
        self.__label_scopus.grid(column=3, row=0)
        self.__checkbox_scopus = Radiobutton(self.__parameters_frame, variable=self.__var_filter,
                                             value=self.__configuration.SCOPUS_VAR)
        self.__checkbox_scopus.grid(column=3, row=1)

        self.__drop_filters_button = Button(self.__parameters_frame, text='Drop filters',
                                            command=self.__drop_filters_button_clicked)
        self.__drop_filters_button.grid(column=1, row=2, sticky='nesw')

        self.__inputbox_keywords = Entry(self.__parameters_frame, width=100)

        self.__var_keywords = StringVar()
        self.__var_keywords.set(self.__configuration.keywords)
        self.__inputbox_keywords.config(textvariable=self.__var_keywords)
        self.__inputbox_keywords.grid(column=4, row=0)

        self.__start_button = Button(self.__parameters_frame, text='Search', command=self.__start_button_clicked)
        self.__start_button.grid(column=4, row=1, sticky='nesw')

        self.__var_status = StringVar()

        self.__label_status = Label(self.__parameters_frame, textvariable=self.__var_status)
        self.__label_status.grid(column=4, row=2)

        self.__parameters_frame.pack(side=BOTTOM)

    def __open(self):
        item = self.__table_frame.focus()
        open(self.__table_frame.item(item)['values'][2])

    def __popup_menu(self, event):
        self.__table_frame.identify_row(event.y)
        self.__menu.post(event.x_root, event.y_root)

    def __configuration_table_frame(self):
        columns = ('', 'Title', 'Link', 'Authors', 'Year', 'RSCI', 'ВАК', 'Scopus')

        self.__table_frame = Treeview(self.__window, columns=columns, show='headings')

        self.__table_frame.heading(0, text=columns[0])
        self.__table_frame.column(0, width=50)

        for column_index in range(1, len(columns) - 4):
            self.__table_frame.heading(column_index, text=columns[column_index])
            self.__table_frame.column(column_index, width=300)

        self.__table_frame.heading(4, text=columns[4])
        self.__table_frame.column(4, width=100, anchor=CENTER)

        self.__table_frame.heading(5, text=columns[5])
        self.__table_frame.column(5, width=50, anchor=CENTER)

        self.__table_frame.heading(6, text=columns[6])
        self.__table_frame.column(6, width=50, anchor=CENTER)

        self.__table_frame.heading(7, text=columns[7])
        self.__table_frame.column(7, width=50, anchor=CENTER)

        self.__menu = Menu(self.__table_frame, tearoff=0)
        self.__menu.add_command(command=self.__open, label='Open link')
        self.__table_frame.bind('<Button-2>', self.__popup_menu)

        self.__table_frame.pack(side=TOP, fill=BOTH, expand=True)

    def start(self):
        self.__configuration_parameter_frame()
        self.__configuration_table_frame()
        self.__window.mainloop()


if __name__ == '__main__':
    widget = Widget()
    widget.start()
