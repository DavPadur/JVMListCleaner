import csv
import re
import tkinter as tk
from jvmlist import JVMList
# from jvmlist import JVMDb


def verify(jl):
    updated_rows = []
    # db = JVMDb()
    jl.overwrite_status_box(f'Attempting to clean file: {jl.get_file_name()}')
    
    with open(jl.input_file_path.get(), "r", newline="", encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        headers = list(reader[0].keys())
        jl.append_status_box(f'... File read successfully')

        required_columns = ["Errors", "ContactId", "Owner Name", "OwnerId", "BDO Owner", "Contact Owner", "Company Name",
                            "AccountId", "RecordTypeId", "Type", "Lead Source", "Marketing List Date", "Marketing List Type"]
        
        for col in required_columns:
            if col not in headers:
                headers.append(col)

        header_order = ["Email", "Phone", "Street Address", "City", "State", "Zip Code", "County",
                        "Listing Price", "Loan Amount", "Credit Amount", "First Name", "Last Name", "Errors", 
                        "ContactId", "Owner Name", "OwnerId", "BDO Owner", "Contact Owner", "Company Name", "AccountId",
                        "RecordTypeId", "Type", "Lead Source", "Marketing List Date", "Marketing List Type"]

        updated_headers = {
            "Email": "Email",
            "Phone": "Phone",
            "Street Address": "Marketing Address Street",
            "City": "Marketing Address City",
            "State": "Marketing Address State",
            "Zip Code": "Marketing Address Zip",
            "County": "Marketing Address County",
            "Listing Price": "Listing Price",
            "Loan Amount": "Loan Amount",
            "Credit Amount": "Credit Amount",
            "First Name": "FirstName",
            "Last Name": "LastName",
            "Errors": "Errors",
            "ContactId": "ContactId",
            "Owner Name": "Owner Name",
            "OwnerId": "OwnerId",
            "BDO Owner": "BDO Owner",
            "Contact Owner": "Contact Owner",
            "Company Name": "Company Name",
            "AccountId": "AccountId",
            "RecordTypeId": "RecordTypeId",
            "Type": "Type",
            "Lead Source": "Lead Source",
            "Marketing List Date": "Marketing List Date",
            "Marketing List Type": "Marketing List Type",
        }
        jl.append_status_box(f'... Headers mapped')
       
        for row in reader:
            updated_row = {updated_headers.get(col, col): row.get(col, "").strip() for col in header_order}
            row_be_good = True  
            error_msg = "" 

            for header, column in jl.field_dict.items():
                if column not in headers:
                    continue
                if not row[column]:
                    continue

                value = row[column].strip()
                updated_value = value  
                error = None

                if header == "First Name":
                    updated_value, error = proper_name(value, 'first_name')
                elif header == "Last Name":
                    updated_value, error = proper_name(value, 'last_name')
                elif header == "Email":
                    updated_value, error = valid_email(value)
                    # if not error:
                    #     print(db.get_id(value))
                    #     print(db.get_owner(value))
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
                    updated_value, error = proper_name(value, 'county')
                elif header == "Listing Price":
                    updated_value, error = format_dollars(value, 'listing_price')#re.sub("[^0-9]", "", value)
                elif header == "Loan Amount":
                    updated_value, error = format_dollars(value, 'loan_amount')#re.sub("[^0-9]", "", value)
                elif header == "Credit Amount":
                    updated_value, error = format_dollars(value, 'credit_amount')#re.sub("[^0-9]", "", value)

                if error:
                    error_msg += error + ', '
                    row_be_good = False
                    jl.append_status_box(f'... Error on line: {jl.successful_rows + jl.error_rows}:{header}')

                updated_row[updated_headers[header]] = updated_value

            updated_row["Errors"] = error_msg.strip(", ") if not row_be_good else ""
            # updated_row["ContactId"] = '' #to do
            # updated_row["Owner Name"] = '' #to do
            # updated_row["OwnerId"] = '' #to do
            # updated_row["BDO Owner"] = '' #to do
            # updated_row["Contact Owner"] = '' #to do
            updated_row["Company Name"] = 'JVM Partner'
            updated_row["RecordTypeId"] = '0121N000000qrYwQAI'
            updated_row["AccountId"] = '0013l00002X71zdAAB'
            updated_row["Type"] = 'Realtor'
            updated_row["Lead Source"] = 'MLS'
            updated_row["Marketing List Type"] = jl.list_type_value.get()
            updated_row["Marketing List Date"] = jl.list_date_value
        
            updated_rows.append(updated_row)

            if row_be_good:
                jl.successful_rows += 1
               #print(f"Row {jl.successful_rows + jl.error_rows} read successfully")
            else:
                jl.error_rows += 1
                print(f"Row {jl.successful_rows + jl.error_rows} failed formatting: {error_msg}")
                print(f"Invalid Row: {row}")

    final_rows = [{updated_headers[col]: row.get(updated_headers[col], "") for col in header_order} for row in updated_rows]

    output_file = jl.input_file_path.get().replace(".csv", "_output.csv")
    with open(output_file, "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[updated_headers[col] for col in header_order])
        writer.writeheader()
        writer.writerows(final_rows)

    jl.row_count_str.set(jl.read_rows)
    jl.successful_rows_str.set(jl.successful_rows)
    jl.error_count_str.set(jl.error_rows)

    print(f"File saved in: {output_file}")
    print(f"Rows read: {jl.read_rows}, Successful rows: {jl.successful_rows}, Errors: {jl.error_rows}")

def proper_name(name, type):
    error = ''
    out = " ".join(word.capitalize() for word in name.split())  
    out = re.sub(r"(?<!\w)(mc)(\w)", lambda m: m.group(1).capitalize() + m.group(2).capitalize(), out, flags=re.IGNORECASE)
    out = re.sub(r"(?<!\w)(o')(\w)", lambda m: m.group(1).capitalize() + m.group(2).capitalize(), out, flags=re.IGNORECASE)
    out = re.sub(r"-(\w)", lambda m: '-' + m.group(1).capitalize(), out, flags=re.IGNORECASE)

    if re.search(r"[\(\)]", out): 
        error += 'Removed (' + re.findall(r"\((.*?)\)", out)[0] + ') from ' + type 
        out = re.sub(r"\(.*?\)", "", out) 

    if type in {'first_name', 'last_name'}:
        for word in name.lower().split():
            if word in {'the', 'team', 'group', 'true'}:
                error += 'Invalid '+ type
                break

    if type == 'first_name' and len(re.sub(r"[^a-zA-Z]", "", name)) <= 2:
        error += 'Verify ' + type

    if type == 'last_name':
        out = re.sub(r"\s(iii|ii|iv|jr|sr)", '', out, flags=re.IGNORECASE) # remove suffix
        out = re.sub(r"[,\.]", '', out)# remove dumb punctuation
    return out, error

def valid_email(email):
    error = ''
    if not email:
        error += 'Missing email'
    elif ';' in email or not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        error += 'Invalid email'
    return email, error

def valid_phone(phone):
    error = None
    phone = re.sub("[^0-9]", "", phone) 
    if len(phone) < 10 or len(phone) > 11:
        error = 'Invalid phone'
    return phone, error

def format_street(address):
    out =" ".join(word.capitalize() for word in address.split()) # capitalizes each word
    out = re.sub(r"(?<!\w)(mc)(\w)", lambda m: m.group(1).capitalize() + m.group(2).capitalize(), out, flags=re.IGNORECASE)# capitalizes McXxxx
    out = re.sub(r"(?<!\w)(o')(\w)", lambda m: m.group(1).capitalize() + m.group(2).capitalize(), out, flags=re.IGNORECASE)# capitalizes O'Xxxx
    out = re.sub(r"(?<!\w)(#)([^\s]+)", lambda m: m.group(1).capitalize() + m.group(2).upper(), out, flags=re.IGNORECASE)# capitalizes #A33
    out = re.sub(r"(\s[ns][ew]\b)", lambda m: m.group(1).upper(), out, flags=re.IGNORECASE)# capitalizes NE,NW,SE,SW
    return out

def format_state(state):
    error = None
    if state.upper() in state_abbreviations.values():
        return state.upper(), error
    updated_value = state_abbreviations.get(state.title(), "")
    if not updated_value:
        error = 'Invalid state'
    return updated_value, error

def format_zip(zip):
    return re.sub(r"\D", "", zip)[:5]

def format_dollars(dollars, type):
    error = None
    out = None
    dollars = int(re.sub(r"[^0-9]", "", dollars))
    if not dollars:
        error = 'Missing ' + type
        return dollars, error
    out = f"${dollars:,}"
    return out, error




state_abbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "American Samoa": "AS",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District Of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Guam": "GU",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Trust Territories": "TT",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Virgin Islands": "VI",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}