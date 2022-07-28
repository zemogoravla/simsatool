
def save_txt(filename, txt):
    with open(filename, "w") as text_file:
        text_file.write(txt)

def save_txt_list(filename, txt_list):
    with open(filename, "w") as text_file:
        for item in txt_list:
            text_file.write(item)
            text_file.write('\n')
        
        text_file.write('\n')