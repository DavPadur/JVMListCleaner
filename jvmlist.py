import io
import csv
import tkinter as tk
from datetime import datetime

class JVMList:
    input_file_path = None
    fields =[]
    field_dict = {}
    dropdown_options = []
    output_options = []
    read_rows = 0
    successful_rows = 0
    error_rows = 0
    overwrite_input_file = False

    # tkinter
    root = None
    row_count = None
    row_count_str = None
    success_count = None
    successful_rows_str = None
    error_count = None
    error_count_str = None
    status_box = None
    list_date_value = None
    list_type_value = None
    list_date_value_default = datetime.today().strftime('%m/%d/%y')
    list_type_options = ['SPCP', 'FTHB', 'Homerun', 'Stale', 'Ratebreak']

    def get_file_name(self):
        if self.input_file_path:
            return self.input_file_path.get().split('/')[-1]
        return None

    def overwrite_status_box(self, text):
        self.status_box.config(state=tk.NORMAL)
        self.status_box.delete("1.0", tk.END)
        self.status_box.insert(tk.INSERT, text)
        self.status_box.see(tk.INSERT)
        self.status_box.config(state=tk.DISABLED)
    
    def append_status_box(self, text):
        self.status_box.config(state=tk.NORMAL)
        self.status_box.insert(tk.CURRENT, '\n'+ text)
        self.status_box.see(tk.END)
        self.status_box.config(state=tk.DISABLED)


# class JVMDb:
#     file_path = None
#     file = None
#     reader = None
#     id_db = {} # email is the key to return the id
#     owner_db = {} # email is the key to return the owner
#     new_ids = {}
#     new_owners = [] 

#     def __init__(self):
#         self.file_path = '../../test/test_email_db.csv'
#         self.file = open(self.file_path, "r", newline="", encoding='utf-8')
#         self.reader = list(csv.DictReader(self.file))
#         for row in self.reader:
#             self.id_db[row['email']] = row['id']
#             self.owner_db[row['email']] = row['owner name']

#     def get_id(self, email):
#         try:
#             return self.id_db[email]
#         except:
#             return ''
    
#     def get_owner(self, email):
#         try:
#             return self.owner_db[email]
#         except:
#             return ''
    
#     def print_db(self, type):
#         if type == 'id':
#             for x in self.id_db: print(f'{x} : {self.id_db[x]}')
#         if type == 'owner': 
#             for x in self.owner_db: print(f'{x} : {self.owner_db[x]}')

