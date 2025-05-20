import tkinter as tk
import csv
import os
import json
import subprocess
from tkinter import filedialog 
from tkinter import ttk
from map import map
from verify import verify
from jvmlist import JVMList
from jvmdb import JVMDb
from simple_salesforce import SalesforceLogin, Salesforce

jl = JVMList()
db = JVMDb()

with open("sf_secrets.json", "r") as file:
    creds = json.load(file)

# Access just the username
username = creds["username"]
password = creds["password"]
security_token = creds["security_token"]
domain = creds["domain"]

sf = Salesforce(
    username=username, password=password, security_token=security_token, instance_url="https://brave-impala-i69fxm-dev-ed.trailblaze.my.salesforce.com"
)

instance_url="https://brave-impala-i69fxm-dev-ed.trailblaze.my.salesforce.com"
print("Instance URL:", instance_url)

# now you can connect directly:
#sf = Salesforce(instance_url=instance_url, session_id=session_id)
#print(sf.query("SELECT Id, Name FROM Account LIMIT 5"))

# Using system() method to execute shell commands

# this logs you in. it only needs to run once per terminal session
subprocess.Popen('SF Org Login Web', shell=True)

# Runs the queries of Contact
subprocess.run(["powershell.exe", "-Command", "sf data export bulk --query \"SELECT X18_Digit_Contact_ID__c, OwnerId, Email, MobilePhone, FirstName, LastName FROM Contact WHERE Email LIKE '%@%'\" -o myOrg --output-file='csv1.csv' --wait 1"], shell=True)
subprocess.run(["powershell.exe", "-Command", "sf data export bulk --query \"SELECT X18_Digit_Contact_ID__c, OwnerId, Alt_Email__c, MobilePhone, FirstName, LastName FROM Contact WHERE Alt_Email__c LIKE '%@%'\" -o myOrg --output-file='csv2.csv' --wait 1"], shell=True)
subprocess.run(["powershell.exe", "-Command", "sf data export bulk --query \"SELECT X18_Digit_Contact_ID__c, OwnerId, X2nd_Alt_Email__c, MobilePhone, FirstName, LastName FROM Contact WHERE X2nd_Alt_Email__c LIKE '%@%'\" -o myOrg --output-file='csv3.csv' --wait 1"], shell=True)

# Runs the queries of Lead
subprocess.run(["powershell.exe", "-Command", "sf data export bulk --query \"SELECT X18_Digit_Lead_ID__c, OwnerId, Email, MobilePhone, FirstName, LastName FROM Lead WHERE Email LIKE '%@%' AND IsConverted = FALSE\" -o myOrg --output-file='csv4.csv' --wait 1"], shell=True)
subprocess.run(["powershell.exe", "-Command", "sf data export bulk --query \"SELECT X18_Digit_Lead_ID__c, OwnerId, Alt_Email__c, MobilePhone, FirstName, LastName FROM Lead WHERE Alt_Email__c LIKE '%@%' AND IsConverted = FALSE\" -o myOrg --output-file='csv5.csv' --wait 1"], shell=True)
subprocess.run(["powershell.exe", "-Command", "sf data export bulk --query \"SELECT X18_Digit_Lead_ID__c, OwnerId, X2nd_Alt_Email__c, MobilePhone, FirstName, LastName FROM Lead WHERE X2nd_Alt_Email__c LIKE '%@%' AND IsConverted = FALSE\" -o myOrg --output-file='csv6.csv' --wait 1"], shell=True)

#then use python magic to combine all of the csvs into one.
#this doesn't need to happen here, but i put it all here just for debugging pruposees

#python magic
def combine_csvs(output_path="combined_output.csv"):
    csv_files = [f"csv{i}.csv" for i in range(1, 7)]
    header_written = False

    with open(output_path, "w", newline='', encoding='utf-8') as outfile:
        writer = None

        for file in csv_files:
            if os.path.exists(file):
                with open(file, "r", newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    try:
                        header = next(reader)
                    except StopIteration:
                        print(f"Skipping empty file: {file}")
                        continue

                    if not header_written:
                        writer = csv.writer(outfile)
                        writer.writerow(header)
                        header_written = True

                    for row in reader:
                        writer.writerow(row)
            else:
                print(f"File not found: {file}")

    print(f"Combined CSV saved to {output_path}")

def select_files():
    file_names = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])
    jl.read_rows = 0
    jl.successful_rows = 0
    jl.error_rows = 0
    
    if file_names:
        input_file_path_var.set(file_names[0])
        jl.input_file_path = file_names[0]
        file_name_short = ", ".join([os.path.basename(file) for file in file_names])
        input_file_label_var.set(file_name_short)
        jl.input_file_path = input_file_path_var  

        jl.row_count_str.set(jl.read_rows)
        jl.successful_rows_str.set(jl.successful_rows)
        jl.error_count_str.set(jl.error_rows)
        map_button.config(state=tk.NORMAL)
        verify_button.config(state=tk.NORMAL)
    else:
        input_file_path_var.set("") 
        input_file_label_var.set("No files selected")
        map_button.config(state=tk.DISABLED)
        verify_button.config(state=tk.DISABLED)


def db_select():
    file_names = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])
    
    if file_names:
        db_file_path_var.set(file_names[0])
        db.file_path = file_names[0]
        file_name_short = ", ".join([os.path.basename(file) for file in file_names])
        db_file_label_var.set(file_name_short)
        db.file_path = db_file_path_var
        db_map_button.config(state=tk.NORMAL)
        db_clean_button.config(state=tk.NORMAL)
    else:
        input_file_path_var.set("") 
        input_file_label_var.set("No Database")
        db_map_button.config(state=tk.DISABLED)
        db_clean_button.config(state=tk.DISABLED)

def file_db():
    pass

def edit_db():
    pass
    
def view_db():
    pass

def update_field_dict(event):
    for idx, dropdown in enumerate(jl.dropdown_options):
        header = dropdown.get()
        if header: 
            jl.field_dict[jl.fields[idx]] = header


# Initialize root window
jl.root = tk.Tk()
jl.root.geometry("600x650")
jl.root.title("JVM List Cleaner")
jl.root.iconbitmap("res/icon.ico")

# File Uploads Section
input_file_title = tk.Label(jl.root, text="Input File Select", font=('Arial', 14))
input_file_title.pack(anchor="w", padx=20, pady=5)

input_select_title = tk.Label(jl.root, text="Choose File: ", font=('Arial', 12))
input_select_title.pack(anchor="w", padx=20, pady=5)

input_file_path = tk.StringVar()
input_file_path_var = input_file_path
input_file_label_var = tk.StringVar()
input_file_label_var.set("No files selected")

input_select_button = tk.Button(jl.root, text="Select File", command=select_files)
input_select_button.pack(anchor="w", padx=40, pady=2)

input_file_label = tk.Label(jl.root, textvariable=input_file_label_var, font=('Arial', 10), anchor="w", wraplength=1000)
input_file_label.pack(anchor="w", padx=40, pady=5)

# Map Button
map_button = tk.Button(jl.root, text='Map', state=tk.DISABLED, command=lambda: map(jl))
map_button.pack(anchor="w", padx=20, pady=10)

# Verify Button
verify_button = tk.Button(jl.root, text='Clean File', state=tk.DISABLED, command=lambda: verify(jl, db))
verify_button.place(x=250, y=475)

# List Info
list_info_title = tk.Label(jl.root, text="List Info", font=('Arial', 14))
list_info_title.pack(anchor="w", padx=25, pady=20)

list_date_title = tk.Label(jl.root, text="List Date: ", font=('Arial', 12))
list_date_title.pack(anchor="w", padx=25, pady=10)

jl.list_date_value = jl.list_date_value_default
list_date_input = tk.Text(jl.root, height=1, width=11)
list_date_input.insert('1.0', jl.list_date_value)
list_date_input.place(x=110, y=263)

list_type_title = tk.Label(jl.root, text="List Type: ", font=('Arial', 12))
list_type_title.pack(anchor="w", padx=25, pady=10)

jl.list_type_value = tk.StringVar()
list_type_input = ttk.Combobox(jl.root, textvariable=jl.list_type_value, values=jl.list_type_options, width=11) 
list_type_input.place(x=110, y=305)

# Errors Section
error_title = tk.Label(jl.root, text="Errors", font=('Arial', 14))
error_title.pack(anchor="w", padx=25, pady=10)

row_title = tk.Label(jl.root, text="Rows Read: ", font=('Arial', 12))
row_title.pack(anchor="w", padx=25, pady=10)

jl.row_count_str = tk.IntVar(value=jl.read_rows)
jl.row_count = tk.Label(jl.root, textvariable=jl.row_count_str, font=('Arial', 12))
jl.row_count.place(x=125, y=395)

success_title = tk.Label(jl.root, text="Successes: ", font=('Arial', 12))
success_title.pack(anchor="w", padx=25, pady=10)

jl.successful_rows_str = tk.IntVar(value=jl.successful_rows)
jl.success_count = tk.Label(jl.root, textvariable=jl.successful_rows_str, font=('Arial', 12))
jl.success_count.place(x=125, y=438)

error_title = tk.Label(jl.root, text="Errors: ", font=('Arial', 12))
error_title.pack(anchor="w", padx=25, pady=10)

jl.error_count_str = tk.IntVar(value=jl.error_rows)
jl.error_count = tk.Label(jl.root, textvariable=jl.error_count_str, font=('Arial', 12))
jl.error_count.place(x=125, y=481)

jl.status_box = tk.Text(jl.root, width=45, height=5.5)
jl.status_box.config(state=tk.DISABLED)
jl.status_box.place(x=25, y=530)

# Buttons for the Database Functions

db_title = tk.Label(db.root, text="Database Functions", font=('Arial', 14))
db_title.place(x=390, y=490)

db_select_button = tk.Button(jl.root, text="Database", command=db_select) #auto upload database, from the one previously downloaded
db_select_button.place(x=400, y=525)

db_file_path = tk.StringVar()
db_file_path_var = db_file_path
db_file_label_var = tk.StringVar()
db_file_label_var.set("No Database")

db_file_label = tk.Label(db.root, textvariable=db_file_label_var, font=('Arial', 10), anchor="w", wraplength=1000)
db_file_label.place(x=475, y=525)

db_map_button = tk.Button(db.root, text='DB Map', state=tk.DISABLED, command=lambda: map(jl))
db_map_button.place(x=400, y=565)

db_clean_button = tk.Button(db.root, text="DB Update", command=edit_db)
db_clean_button.place(x=465, y=565)

combine_button = tk.Button(db.root, text="Combine CSVs", command=lambda: combine_csvs("combined_output.csv"))
combine_button.place(x=400, y=600)

# Dropdown Menus Section
dropdown_title = tk.Label(db.root, text="Input File Mapping", font=('Arial', 14))
dropdown_title.place(x=250, y=5)
dropdown_frame = tk.Frame(db.root)
dropdown_frame.place(x=250, y=55)

jl.fields = [
    "First Name", "Last Name", "Email", "Phone", "Street Address", "City", "State", "Zip Code", "County", "Listing Price", "Loan Amount", "Credit Amount"
]

jl.field_dict = {}  # field type : csv header
                              
jl.dropdown_options = []

jl.output_options = []

# Create labels and dropdown menus
for idx, field in enumerate(jl.fields):
    label = tk.Label(dropdown_frame, text=field, font=('Arial', 12))
    label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

    dropdown = ttk.Combobox(dropdown_frame, width=20) 
    dropdown.grid(row=idx, column=1, padx=10, pady=5)
    jl.dropdown_options.append(dropdown)

    dropdown.bind("<<ComboboxSelected>>", update_field_dict)

jl.root.mainloop()
