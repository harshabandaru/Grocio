"""
Grocio: Twilio app for maintaining lists between friends
        like groceries
Help:
1. Adding items into your list
add <list name> <item1> <item2>
2. List items in your list
list <list name>
3. Delete items in your list using indexes in the list
remove <list name> <index_item1> <index_item2>

Also persists data in file between server restarts

@Author: Sriharsha Bandaru
"""
# /usr/bin/env python
from flask import Flask, request
import pickle
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Map can hold multiple lists
list_map = {}

# Retrieve data on server restart
def retrieve_data():
    global list_map
    try:
        with open('.serverdata', 'rb') as f:
                list_map = pickle.load(f)
    except:
        print('No file')

# Persist the data onto a file for server restarts
def persist_data():
    global list_map
    with open('.serverdata', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(list_map, f, pickle.HIGHEST_PROTOCOL)

@app.route("/sms", methods=['GET', 'POST'])
def process_sms():
    global list_map
    """Process incoming messages"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Get the request tokens
    tokens =  str(body).strip().split()

    # Start our response
    resp = MessagingResponse()
    print(tokens)

    # Process request for help
    if body.lower() == 'help me':
        usage_str = "1. Adding items into your list\n" +\
                    "add <list name> <item1> <item2> ...\n\n" +\
                    "2. List items in your list\n" +\
                    "list <list name>\n\n" + \
                    "3. Delete items in your list using indexes in the list\n" + \
                    "remove <list name> <index_item1> <index_item2> ...\n\n" +\
                    "Have fun :)"
        resp.message(usage_str)
        return str(resp)

    # Process put for item
    if tokens[0].lower() == 'add':
        list_name = tokens[1].lower()
        list_items = []

        # Get the list if it exists
        if list_name in list_map:
            list_items = list_map[list_name]

        list_items = list_items + tokens[2:]

        # Put the list back in dictionary
        list_map[list_name] = list_items
        persist_data()
        resp.message("Added items in list " + list_name)

    # Process list items
    if tokens[0].lower() == 'list':
        try:
            list_name = tokens[1].lower()
            list_items = []

            # Get the list if it exists
            if list_name in list_map:
                list_items = list_map[list_name]

            response_list_str = ""
            index = 1
            # Give a response with indexed items
            for item in list_items:
                response_list_str = response_list_str +\
                                    str(index) + ". " + item + " "
                index = index + 1
            resp.message(response_list_str)
        except:
            resp.message("Error: Please check your request")

    # Process delete for items
    if tokens[0].lower() == 'remove':
        list_name = tokens[1].lower()
        list_items = []

        # Get the list if it exists
        if list_name in list_map:
            list_items = list_map[list_name]

        try:
            # Get the indices to delete
            del_indexes = [int(x) - 1 for x in tokens[2:]]
            temp_list = []
            cur_index = 0
            for item in list_items:
                # put the item in temp list if not in del_index
                if cur_index not in del_indexes:
                    temp_list.append(item)
                cur_index = cur_index + 1
            list_items = temp_list

            # Put the list back in dictionary
            list_map[list_name] = list_items
            persist_data()
            resp.message("Deleted items in list " + list_name)
        except:
            resp.message("Indexes not valid")

    #print(list_items)
    print(str(resp))


    # Add a message


    return str(resp)

if __name__ == "__main__":
    retrieve_data()
    app.run(debug=True)