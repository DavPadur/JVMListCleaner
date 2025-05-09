import csv
import os
import json
import pandas as pd
from simple_salesforce import Salesforce

class JVMDb:
    file_path = None
    file = None
    reader = None
    id_db = {}       # email -> id
    owner_db = {}    # email -> owner name
    new_ids = {}
    new_owners = []
    
    root = None
    db_file_path = None
    db_file_path_var = None
    db_file_label = None
    db_file_label_var = None

    def __init__(self, use_salesforce=False, secrets_path=os.path.expanduser("~/.sf_secrets.json"), file_path=None):
        if use_salesforce:
            self.load_from_salesforce(secrets_path)
        else:
            self.load_from_csv(file_path or 'C:\\Users\\David\\Documents\\JVMListCleaner\\salesforce_test_data.csv')

    def load_from_csv(self, file_path):
        self.file_path = file_path
        self.file = open(self.file_path, "r", newline="", encoding='utf-8')
        self.reader = list(csv.DictReader(self.file))
        for row in self.reader:
            self.id_db[row['email']] = row['id']
            self.owner_db[row['email']] = row['owner name']

    def load_from_salesforce(self, secrets_path):
        # Authenticate
        with open(secrets_path, 'r') as f:
            creds = json.load(f)
        sf = Salesforce(
            username=creds['username'],
            password=creds['password'],
            security_token=creds['security_token'],
            domain=creds['domain']
        )

        queries = [
            ("Contact", "Email"),
            ("Contact", "Alt_Email__c"),
            ("Contact", "X2nd_Alt_Email__c"),
            ("Lead", "Email", "AND IsConverted = FALSE"),
            ("Lead", "Alt_Email__c", "AND IsConverted = FALSE"),
            ("Lead", "X2nd_Alt_Email__c", "AND IsConverted = FALSE"),
        ]

        all_results = []

        for entry in queries:
            object_name, email_field = entry[0], entry[1]
            extra = entry[2] if len(entry) > 2 else ""
            id_field = "X18_Digit_Lead_ID__c" if object_name == "Lead" else "X18_Digit_Contact_ID__c"
            if object_name == "Lead":
                query = (
                    f"SELECT {id_field}, OwnerId, {email_field}, MobilePhone, FirstName, LastName "
                    f"FROM {object_name} WHERE {email_field} LIKE '%@%' AND IsConverted = FALSE"
                )
            else:
                query = (
                    f"SELECT {id_field}, OwnerId, {email_field}, MobilePhone, FirstName, LastName "
                    f"FROM {object_name} WHERE {email_field} LIKE '%@%'"
                )
            result = sf.query_all(query)
            records = result['records']
            df = pd.DataFrame(records).drop(columns='attributes')
            df = df.rename(columns={email_field: 'Email', id_field: 'ID', 'OwnerId': 'Owner'})
            all_results.append(df)

        # Combine into one DataFrame and update id/owner dbs
        combined = pd.concat(all_results, ignore_index=True).drop_duplicates(subset=["Email"])
        for _, row in combined.iterrows():
            if pd.notna(row['Email']):
                self.id_db[row['Email']] = row['ID']
                self.owner_db[row['Email']] = row['Owner']

    def get_id(self, email):
        return self.id_db.get(email, '')

    def get_owner(self, email):
        return self.owner_db.get(email, '')

    def print_db(self, type):
        if type == 'id':
            for x in self.id_db: print(f'{x} : {self.id_db[x]}')
        if type == 'owner':
            for x in self.owner_db: print(f'{x} : {self.owner_db[x]}')
