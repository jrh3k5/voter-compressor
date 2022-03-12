import csv

class Address:
    def __init__(self, precinct, house_number, pre_direction, street_name, street_type, unit_type, unit_num, city, state, zip_code, combined_address):
        self.precinct = precinct
        self.house_number = house_number
        self.pre_direction = pre_direction
        self.street_name = street_name
        self.street_type = street_type
        self.unit_type = unit_type
        self.unit_num = unit_num
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.combined_address = combined_address
        self.voters = {}

class VoterFamily:
    def __init__(self):
        self.first_names = []

def compress_csv(input_file_path, output_file_path):
    input_rows = []
    output_rows = []

    addresses = {}

    with open(input_file_path) as input_handle:
        input_csv = csv.reader(input_handle)

        for row in input_csv:
            input_rows.append(row)

    header_row = input_rows.pop(0)
    column_mappings = build_column_mappings(header_row)
    output_rows.append(header_row)
    for input_row in input_rows:
        address = build_address(input_row, column_mappings)
        address_key = build_address_key(address)

        if address_key not in addresses:
            addresses[address_key] = address
        else:
            address = addresses[address_key]

        last_name = input_row[column_mappings["last name"]]
        first_name = input_row[column_mappings["first name"]]

        voter_family = None
        if last_name in address.voters:
            voter_family = address.voters[last_name]
        else:
            voter_family = VoterFamily()
            address.voters[last_name] = voter_family

        voter_family.first_names.append(first_name)

    with open(output_file_path, 'w') as output_handle:
        output_csv = csv.writer(output_handle)

        output_csv.writerow(header_row)

        address_keys = addresses.keys()
        # Sort by the addres key for consistency, determinant order of output
        address_keys.sort()

        precinct_idx = column_mappings["precinct"]
        house_num_idx = column_mappings["hs num"]
        pre_direction_idx = column_mappings["pre direction"]
        street_name_idx = column_mappings["street name"]
        street_type_idx = column_mappings["street type"]
        unit_type_idx = column_mappings["unit type"]
        unit_num_idx = column_mappings["unit num"]
        city_idx = column_mappings["city (ra)"]
        state_idx = column_mappings["state (ra)"]
        zip_code_idx = column_mappings["zip (ra)"]
        new_first_idx = column_mappings["new first"]

        for address_key in address_keys:
            # Less two columns because the first and last name columns are being dropped
            output_row = [""] * len(header_row)

            address = addresses[address_key]

            last_names = address.voters.keys()
            # Sort, again, for determinant output
            last_names.sort()

            combined_family_names = []

            for last_name in last_names:
                unique_first_names = list(set(address.voters[last_name].first_names))
                # Sort the first names - again, for consistency of output
                unique_first_names.sort()
                first_name_count = len(unique_first_names)
                if first_name_count == 1:
                    combined_family_names.append(unique_first_names[0] + " " + last_name)
                elif first_name_count == 2:
                    combined_family_names.append(unique_first_names[0] + " AND " + unique_first_names[1] + " " + last_name)
                else:
                    combined_first_name = ""
                    for first_name_idx, first_name in enumerate(unique_first_names):
                        if first_name_idx == 0:
                            combined_first_name = first_name
                        elif first_name_idx != first_name_count - 1:
                            combined_first_name = combined_first_name + ", " + first_name
                        else:
                            combined_first_name = combined_first_name + ", AND " + first_name
                    combined_family_names.append(combined_first_name + " " + last_name)

            family_count = len(combined_family_names)
            new_first = ""
            if family_count == 1:
                new_first = combined_family_names[0]
            elif family_count == 2:
                new_first = combined_family_names[0] + " AND " + combined_family_names[1]
            else:
                for family_idx, combined_family in enumerate(combined_family_names):
                    if family_idx == 0:
                        new_first = combined_family
                    elif family_idx < family_count - 1:
                        new_first = new_first + ", " + combined_family
                    else:
                        new_first = new_first + " AND " + combined_family

            output_row[precinct_idx] = address.precinct
            output_row[pre_direction_idx] = address.pre_direction
            output_row[house_num_idx] = address.house_number
            output_row[street_name_idx] = address.street_name
            output_row[street_type_idx] = address.street_type
            output_row[unit_type_idx] = address.unit_type
            output_row[unit_num_idx] = address.unit_num
            output_row[city_idx] = address.city
            output_row[state_idx] = address.state
            output_row[zip_code_idx] = address.zip_code
            output_row[new_first_idx] = new_first
            # Cheat and assume that the final column is the combined address
            output_row[len(output_row) - 1] = address.combined_address

            output_csv.writerow(output_row)


def build_column_mappings(header_row):
    column_mappings = {}
    for index, col in enumerate(header_row):
        column_mappings[col.lower()] = index
    return column_mappings

def build_address(row, column_mappings):
    precinct = row[column_mappings["precinct"]]
    house_number = row[column_mappings["hs num"]]
    pre_direction = row[column_mappings["pre direction"]]
    street_name = row[column_mappings["street name"]]
    street_type = row[column_mappings["street type"]]
    unit_type = row[column_mappings["unit type"]]
    unit_num = row[column_mappings["unit num"]]
    city = row[column_mappings["city (ra)"]]
    state = row[column_mappings["state (ra)"]]
    zip_code = row[column_mappings["zip (ra)"]]

    # Cheat and assume that the final column is the combined address
    combined_address = row[len(row) - 1]
    return Address(precinct, house_number, pre_direction, street_name, street_type, unit_type, unit_num, city, state, zip_code, combined_address)

def build_address_key(address):
    return ("precinct:" + address.precinct +
    ":zip_code:" + address.zip_code + 
    ":state:" + address.state + 
    ":city:" + address.city +
    ":street_type:" + address.street_type + 
    ":street_name:" + address.street_name + 
    ":house_number:" + address.house_number + 
    ":pre_direction:" + address.pre_direction + 
    ":unit_type:" + address.unit_type + 
    ":unit_num:" + address.unit_num)







