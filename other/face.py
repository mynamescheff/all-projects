def print_text_art():
    num_spaces = [11, 8, 5, 2, 0, 0, 0]
    art_lines = []

    for i in range(4):
        line = ":D" + " " * num_spaces[i] + "<=====8"
        art_lines.append(line)
    
    art_lines.append(":O===8")
    art_lines.append(":O=8")
    art_lines.append(":3")

    for line in art_lines:
        print(line)

if __name__ == "__main__":
    print_text_art()
