import csv

from jvmlist import JVMList


def map(jl):

    if not jl.input_file_path.get():
        print("No file selected for mapping.")
        return

    try:
        with open(jl.input_file_path.get(), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader) 

            jl.read_rows = 0

            for row in reader:
                if any(row):  # Only count non-empty rows
                    jl.read_rows += 1

    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    jl.row_count_str.set(jl.read_rows)


    # Populate dropdown_options with headers from the CSV
    for dropdown in jl.dropdown_options:
        dropdown['values'] = headers
        dropdown.set('')
        

    # Keywords for each dropdown field
    dropdown_keywords = {
        0: ["first name", "firstname"],         
        1: ["last name", "lastname"],    
        2: ["email", "e-mail"],     
        3: ["phone", "mobile"],        
        4: ["address", "street"],   
        5: ["city"],                  
        6: ["state"],                  
        7: ["zip", "code", "postal"],                    
        8: ["county"],
        9: ["listing price", "price", "list price"],
        10: ["loan amount", "loan"],
        11: ["credit amount", "credit"]
    }

    # Iterate through headers and assign best matches to dropdowns
    for idx, keywords in dropdown_keywords.items():
        for header in headers:
            h = header.lower()

            # Check for keywords
            if all(keyword in h for keyword in keywords): # for ANDed keywords
                jl.dropdown_options[idx].set(header) 
                jl.field_dict[jl.fields[idx]] = header
                break
            elif any(keyword in h for keyword in keywords): # for ORed keywords
                jl.dropdown_options[idx].set(header) 
                jl.field_dict[jl.fields[idx]] = header
                break
    
    # Find type from filename jl.input_file_path
    file_name_split = jl.input_file_path.get().split('/')[-1].lower().split(' ')

    jl.list_type_value.set('')
    for k in jl.list_type_options:
        if k.lower() in file_name_split:
            jl.list_type_value.set(k)
            break

    jl.row_count_str.set(jl.read_rows)
        

            
