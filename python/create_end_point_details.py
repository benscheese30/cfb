# create a script that will create the cfdb_endpoint_details.json file based on the cfbd_api_structure.json file
import json

def endpoint_details():
    # read in local json file
    with open("resources/cfbd_api_structure.json", "r") as f:
        api_structure = json.load(f)

    # extract endpoint names and parameters
    paths = api_structure["paths"]
    endpoint_dict = {}

    # loop through endpoints
    for k in paths:
        print(k)
        path_base = paths[k]["get"]
        # get parameters
        if "parameters" in path_base:
            params = {}
            # get parameter names and data types
            for p in path_base["parameters"]:
                params[p["name"]] = {
                    "type": p["type"],
                    "required": p["required"]
                }
        # add to dictionary
        endpoint_dict[k] = {
            "params": params
        }

    # save/update a new json file to resources directory from a dictionary
    with open("resources/cfbd_endpoint_details.json", "w") as f:
        json.dump(endpoint_dict, f)

if __name__ == "__main__":
    endpoint_details()
