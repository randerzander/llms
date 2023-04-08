def add_ordered_identifier(dict_list, identifier_key):
    # Enumerate through the list to get both the index and the dictionary
    for index, dictionary in enumerate(dict_list):
        # Add the ordered identifier (index) as a new key-value pair to the dictionary
        # We add 1 to the index to make it 1-based (e.g., 1, 2, 3) instead of 0-based (e.g., 0, 1, 2)
        dictionary[identifier_key] = str(index + 1)
    return dict_list
 
def clean(response):
  return response.split("ACTION:")[1].strip()
