text = "This : is a sample text. It contains some information."

# Find the index of the first full stop
index_of_full_stop = text.find('.')

# Check if a full stop was found and print accordingly
if index_of_full_stop != -1:
    text_up_to_full_stop = text[:index_of_full_stop + 1]  # Include the full stop
    print(text_up_to_full_stop)
else:
    print("No full stop found in the text.")
