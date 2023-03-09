import tkinter as tk
from tkinter import filedialog
from main import DromParser

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Создаем элементы управления
        self.pages_label = tk.Label(self, text="Введите количество страниц:")
        self.pages_entry = tk.Entry(self)
        self.filename_label = tk.Label(self, text="Введите название файла:")
        self.filename_entry = tk.Entry(self)
        self.choose_file_button = tk.Button(self, text="Выбрать файл", command=self.choose_file)
        self.run_button = tk.Button(self, text="Запустить парсер", command=self.run_parser)
        self.quit_button = tk.Button(self, text="Выйти", command=self.master.destroy)

        # Размещаем элементы управления на форме
        self.pages_label.pack()
        self.pages_entry.pack()
        self.filename_label.pack()
        self.filename_entry.pack()
        self.choose_file_button.pack()
        self.run_button.pack()
        self.quit_button.pack()

    def choose_file(self):
        # Открываем диалог выбора файла и сохраняем выбранный путь в поле ввода имени файла
        filename = filedialog.asksaveasfilename(initialdir="/", title="Выберите файл", filetypes=(("CSV files", "*.csv"),))
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, filename)

    def run_parser(self):
        # Создаем экземпляр парсера и запускаем его с заданными параметрами
        n_pages = int(self.pages_entry.get())
        filename = self.filename_entry.get()
        parser = DromParser(n_pages=n_pages)
        parser.parse_all_pages()
        parser.save_to_csv(filename)
        tk.messagebox.showinfo("Парсинг окончен", "Данные успешно сохранены в файле {}".format(filename))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
