import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib import pyplot as plt
import pandas as pd
from tkinter import ttk
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MLApplication():
    def __init__(self, master):
        self.master = master
        self.master.title('Machine Learning Application')
        self.master.config(bg='#FBC049')
        self.master.geometry("1200x800")
        self.dataset_path = ''
        self.data = None
        self.cleaned_data = None
        self.features = []
        self.algorithm = ''


        #Create UI Elements

        self.heading = tk.Label(self.master, text='Machine Learning Application', font=('Comic Sans MS',35,'bold'),bg='#FBC049',fg='#003248')
        self.heading.place(x=500, y=20)


        self.label_select_dataset = tk.Label(self.master, text='Select Dataset :', font=('Comic Sans MS',20,'bold'), bg='#FBC049',fg='#003248')
        self.label_select_dataset.place(x=200,y=150)

        self.btn_browse = tk.Button(self.master, text='Browse', bg='#003248', fg='#FBC049',font=('Comic Sans MS',15,'bold'), command=self.browse_dataset)
        self.btn_browse.place(x=450, y=150)


        self.label_dataset_info = tk.Label(self.master, text='Selected Dataset : ',font=('Comic Sans MS',18,'bold'), bg='#FBC049',fg='#003248')
        self.label_dataset_info.place(x=200, y=250)

        self.tree_frame = tk.Frame(self.master)
        self.tree_frame.place(x=200, y=300, width=1100, height=300)

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(side="left", fill="both", expand=True)

        yscrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        yscrollbar.pack(side="right", fill="y")

        xscrollbar = ttk.Scrollbar(self.master, orient="horizontal", command=self.tree.xview)
        xscrollbar.place(x=200, y=605, width=1100)

        self.tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        self.btn_clean = tk.Button(self.master, text='Clean', bg='#003248', fg='#FBC049',font=('Comic Sans MS',15,'bold'), command=self.clean_data)
        self.btn_clean.place(x=200, y=650)

        self.btn_select_features = tk.Button(self.master, text='Select Features', bg='#003248', fg='#FBC049', font=('Comic Sans MS',15,'bold'), command=self.select_features)
        self.btn_select_features.place(x=400, y=650)

        self.selected_features_label = tk.Label(self.master, text='Selected Features: ', font=('Comic Sans MS', 18, 'bold'), bg='#FBC049', fg='#003248')
        self.selected_features_label.place(x=200, y=200)

        self.btn_chart_type = tk.Button(self.master, text='Select Chart', bg='#003248', fg='#FBC049', font=('Comic Sans MS',15,'bold'), command=self.choose_chart)
        self.btn_chart_type.place(x=600, y=650)

    
    def browse_dataset(self):
        self.dataset_path = filedialog.askopenfilename()
        self.label_dataset_info.config(text=f'Selected dataset: {self.dataset_path}')
        self.data = pd.read_csv(self.dataset_path, encoding='latin-1')

        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
        for index, row in self.data.iterrows():
            self.tree.insert("", tk.END, text=index, values=list(row))

    
    def clean_data(self):
        self.cleaned_data = self.data.dropna()
        self.tree.delete(*self.tree.get_children())
        for index, row in self.cleaned_data.iterrows():
            self.tree.insert("", tk.END, text=index, values=list(row))

    def select_features(self):
        select_features_window = tk.Toplevel(self.master)
        select_features_window.geometry("400x400")
        select_features_window.title('Select Features')
        
        checkboxes_frame = tk.Frame(select_features_window)
        checkboxes_frame.pack(pady=20)
        
        feature_checkboxes = {}
        for feature in self.data.columns:
            feature_checkboxes[feature] = tk.BooleanVar()  # Create a BooleanVar for each feature checkbox
            feature_checkboxes[feature].set(False)  # Initialize all checkboxes as unchecked
            checkbox = tk.Checkbutton(checkboxes_frame, text=feature, variable=feature_checkboxes[feature])
            checkbox.pack()
        
        def save_selected_features():
            self.features = [feature for feature in feature_checkboxes.keys() if feature_checkboxes[feature].get()]
            select_features_window.destroy()
            self.update_selected_features_label()  # Call the function to update the label text
            
        ok_button = tk.Button(select_features_window, text='OK', command=save_selected_features)
        ok_button.pack(pady=20)
        
    def update_selected_features_label(self):
        self.selected_features_label.config(text=f'Selected Features: {", ".join(self.features)}')

    
    def choose_chart(self):
        chart_window = tk.Toplevel(self.master)
        chart_window.geometry("400x200")
        chart_window.title('Choose Chart Type')

        chart_type_var = tk.StringVar()
        chart_type_var.set("Scatter Plot")  # Default selection
        chart_types = ["Scatter Plot", "Histogram", "Bar Plot"]

        chart_label = tk.Label(chart_window, text="Select Chart Type:", font=('Comic Sans MS', 12))
        chart_label.pack(pady=10)

        chart_combobox = ttk.Combobox(chart_window, textvariable=chart_type_var, values=chart_types)
        chart_combobox.pack(pady=10)

        chart_button = tk.Button(chart_window, text="Generate Chart", command=lambda: self.generate_chart(chart_type_var.get()))
        chart_button.pack(pady=10)

    def generate_chart(self, chart_type):
        chart_window = tk.Toplevel(self.master)
        chart_window.title(f'{chart_type} Chart')

        if chart_type == "Scatter Plot":
            if self.cleaned_data is not None:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.scatter(self.cleaned_data['x'], self.cleaned_data['y'])
                ax.set_xlabel('X-axis')
                ax.set_ylabel('Y-axis')
                ax.set_title('Scatter Plot')

                canvas = FigureCanvasTkAgg(fig, master=chart_window)
                canvas.get_tk_widget().pack()
                canvas.draw()

            else:
                messagebox.showerror("Data Not Available", "Please load or clean the dataset before generating a scatter plot.")
        elif chart_type == "Histogram":
            if self.cleaned_data is not None:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.hist(self.cleaned_data['value'], bins=10)
                ax.set_xlabel('Value')
                ax.set_ylabel('Frequency')
                ax.set_title('Histogram')

                canvas = FigureCanvasTkAgg(fig, master=chart_window)
                canvas.get_tk_widget().pack()
                canvas.draw()
            else:
                messagebox.showerror("Data Not Available", "Please load or clean the dataset before generating a histogram.")
        elif chart_type == "Bar Plot":
            if self.cleaned_data is not None:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.barplot(x='category', y='value', data=self.cleaned_data)
                ax.set_xlabel('Category')
                ax.set_ylabel('Value')
                ax.set_title('Bar Plot')

                canvas = FigureCanvasTkAgg(fig, master=chart_window)
                canvas.get_tk_widget().pack()
                canvas.draw()
            else:
                messagebox.showerror("Data Not Available", "Please load or clean the dataset before generating a bar plot.")
        else:
            messagebox.showerror("Invalid Chart Type", "Please choose a valid chart type.")
    def start(self):
        self.master.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = MLApplication(root)
    app.start()
