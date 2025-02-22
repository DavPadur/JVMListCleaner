import csv
import re
import tkinter as tk
from jvmlist import JVMList

# general proper function def verify(file_path, field_dict, jl):
def verify(jl):
    updated_rows = [] # initialized list all

    with open(jl.input_file_path.get(), "r", newline="", encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        headers = list(reader[0].keys())
        
        if "Errors" not in headers:
            headers.append("Errors")
        
        for row in reader:
            updated_row = row.copy()
            row_be_good = True  # Assume row is valid until proven otherwise
            error_msg = ""

            for header, column in jl.field_dict.items():
                if column not in headers: continue
                if not row[column]: continue

                value = row[column].strip()
                updated_value = value # just in case it's perfect
                error = None
                if header == "First Name":
                    updated_value, error = proper_name(value, 'fname')
                elif header == "Last Name":
                    updated_value, error = proper_name(value, 'lname')
                elif header == "Email":
                    updated_value = valid_email(value)
                elif header == "Phone":
                    updated_value, error = valid_phone(value)
                elif header == "Street Address":
                    updated_value = format_street(value)
                elif header == "City":
                    updated_value, error = proper_name(value, 'city')
                elif header == "State":
                    updated_value, error = format_state(value)
                elif header == "Zip Code":
                    updated_value = format_zip(value)
                elif header == "County":
                    updated_value, error = proper_name(value)

                if error:
                    error_msg += error + ', '
                    row_be_good = False
                updated_row[column] = updated_value

            updated_row["Errors"] = error_msg.strip(", ") if not row_be_good else ""
        
            updated_rows.append(updated_row)

            # Track the number of successesful and error rows
            if row_be_good:
                jl.successful_rows += 1
            else:
                jl.error_rows += 1
                print(f"Row {jl.read_rows} failed formatting: {error_msg}") # Temporary fstring printout until implementation of errors.py 
                print(f"Invalid Row: {row}")

    input_file_path_str = jl.input_file_path.get()
    output_file = input_file_path_str.replace(".csv", "_output.csv")
    with open(output_file, "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(updated_rows)
        
    jl.row_count_str.set(jl.read_rows)
    jl.successful_rows_str.set(jl.successful_rows)
    jl.error_count_str.set(jl.error_rows)
    print(f"File saved in: {output_file}")
    print(f"Rows read: {jl.read_rows}, Successful rows: {jl.successful_rows}, Errors: {jl.error_rows}") # temp until we print out in errors.py

    jl.row_count_str.set(jl.read_rows)
    jl.successful_rows_str.set(jl.successful_rows)
    jl.error_count_str.set(jl.error_rows)
    print(f"File saved in: {output_file}")
    print(f"Rows read: {jl.read_rows}, Successful rows: {jl.successful_rows}, Errors: {jl.error_rows}") # temp until we print out in errors.py



def proper_name(name, type):
    error = None
    out =" ".join(word.capitalize() for word in name.split()) # capitalizes each word
    out = re.sub(r"(?<!\w)(mc)(\w)", lambda m: m.group(1).capitalize() + m.group(2).capitalize(), out, flags=re.IGNORECASE)# capitalizes McXxxx
    out = re.sub(r"(?<!\w)(')(\w)", lambda m: m.group(1).capitalize() + m.group(2).capitalize(), out, flags=re.IGNORECASE)# capitalizes O'Xxxx
    if type == 'fname' and re.fullmatch(r"[a-zA-Z]\.[a-zA-Z]\.", name):
        out = name.upper()
    if type in { 'fname', 'lname' } and name.lower():
        for s in name.lower().split():
            if s in { 'the', 'team', 'group', 'true'}:
                error = 'Invalid '+ type
                break
    return out, error

def valid_email(email):
    return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)) 

def valid_phone(phone):
    error = None
    phone = re.sub("[^0-9]", "", phone) 
    if re.search(r'[^0-9]', phone) or len(phone) < 10 or len(phone) > 11:
        error = 'Invalid phone'
    return phone, error

def format_street(address):
    out =" ".join(word.capitalize() for word in address.split()) # capitalizes each word
    out = re.sub(r"(?<!\w)(mc)(\w)", lambda m: m.group(1).capitalize() + m.group(2).capitalize(), out, flags=re.IGNORECASE)# capitalizes McXxxx
    out = re.sub(r"(?<!\w)(o')(\w)", lambda m: m.group(1).capitalize() + m.group(2).capitalize(), out, flags=re.IGNORECASE)# capitalizes O'Xxxx
    out = re.sub(r"(?<!\w)(#)(\w)", lambda m: m.group(1).capitalize() + m.group(2).upper(), out, flags=re.IGNORECASE)# capitalizes #A33
    out = re.sub(r"(\s[ns][ew]\b)", lambda m: m.group(1).upper(), out, flags=re.IGNORECASE)# capitalizes NE,NW,SE,SW
    return out

def format_state(state):
    error = None
    if state.upper() in state_abbreviations.values():
        return state.upper(), error
    
    updated_value = state_abbreviations.get(state.title(), "")
    if updated_value == "":
        error = 'Invalid state', 
    
    return state, error

def format_zip(zip):
    zip = re.sub(r"\D", "", zip)  
    return zip[:5]


state_abbreviations = {
    "Alabama" : "AL",
    "Alaska" : "AK",
    "Arizona" : "AZ",
    "Arkansas" : "AR",
    "American Samoa" : "AS",
    "California" : "CA",
    "Colorado" : "CO",
    "Connecticut" : "CT",
    "Delaware" : "DE",
    "District of Columbia" : "DC",
    "Florida" : "FL",
    "Georgia" : "GA",
    "Guam" : "GU",
    "Hawaii" : "HI",
    "Idaho" : "ID",
    "Illinois" : "IL",
    "Indiana" : "IN",
    "Iowa" : "IA",
    "Kansas" : "KS",
    "Kentucky" : "KY",
    "Louisiana" : "LA",
    "Maine" : "ME",
    "Maryland" : "MD",
    "Massachusetts" : "MA",
    "Michigan" : "MI",
    "Minnesota" : "MN",
    "Mississippi" : "MS",
    "Missouri" : "MO",
    "Montana" : "MT",
    "Nebraska" : "NE",
    "Nevada" : "NV",
    "New Hampshire" : "NH",
    "Kentucky" : "KY",
    "Louisiana" : "LA",
    "Maine" : "ME",
    "Maryland" : "MD",
    "Massachusetts" : "MA",
    "Michigan" : "MI",
    "Ohio" : "OH",
    "Oklahoma" : "OK",
    "Oregon" : "OR",
    "Pennsylvania" : "PA",
    "Puerto Rico" : "PR",
    "Rhode Island" : "RI",
    "South Carolina" : "SC",
    "South Dakota" : "SD",
    "Tennessee" : "TN",
    "Texas" : "TX",
    "Trust Territories" : "TT",
    "Utah" : "UT",
    "Vermont" : "VT",
    "Virginia" : "VA",
    "Virgin Islands" : "VI",
    "Washington" : "WA",
    "West Virginia" : "WV",
    "Wisconsin" : "WI",
    "Wyoming" : "WY"
}
