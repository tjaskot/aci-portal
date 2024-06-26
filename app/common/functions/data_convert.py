import json

inserts_data = {
    "01": "!",
    "02": "equ pn$desc to 1",
    "03": "equ pn$group to 2",
    "04": "equ pn$cpn to 3",
    "05": "equ pn$serial to 4",
    "06": "equ pn$code to 5",
    "07": "equ pn$ser.pfx to 5",
    "08": "equ pn$xnet to 6",
    "09": "equ pn$short.desc to 7",
    "10": "equ pn$family to 8",
    "11": "equ pn$style to 9",
    "12": "equ pn$bclist to 10",
    "13": "equ pn$disable to 11",
    "14": "equ pn$ctgry to 12",
    "16": "equ pn$sn.type to 13"
}


# Function to transform inserts data
def transform_inserts(data):
    transformed = {}
    for key, value in data.items():
        if value.startswith("equ"):
            parts = value.split()
            # Swapping '$' and '.' to '_'
            variable = parts[1].replace('$', '_').replace('.', '_')
            position = int(parts[3])
            transformed[position] = variable
    return transformed


def data_convert(qm_data):
    # Mapping QM data to their corresponding transformed insert variable names
    json_data = {
        "file": "xpn",
        "record": qm_data["xpn"]
    }

    transformed_inserts = transform_inserts(inserts_data)

    for position, variable in transformed_inserts.items():
        # Format the position as a two-digit string key
        value = qm_data[f"{position:02d}"]
        # Split the value into a list if it contains the delimiter 'ÿ'
        if 'ÿ' in value:
            value = value.split('ÿ')
        json_data[variable] = value

    # Convert to JSON
    json_output = json.dumps(json_data, indent=4, sort_keys=True)

    # Output the JSON data
    print(json_output)

    # Optionally, save to a file
    # with open('output.json', 'w') as json_file:
    #     json_file.write(json_output)

    return json_output
