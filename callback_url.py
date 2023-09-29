import os

if os.path.exists("/content/koboldcpp/nohup.out"):
    with open("/content/koboldcpp/nohup.out", "r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "Your quick Tunnel has been created!" in line and i+1 < len(lines):
                retrieved_link = lines[i+1].split("|")[1].strip()
                print("\nKobold API Link:", retrieved_link, "\n")
                break