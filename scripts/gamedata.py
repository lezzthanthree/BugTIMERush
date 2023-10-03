from os import path

game_folder = ""

def get_save_data():
    savedata = []
    if path.isfile(path.join(game_folder, "currentlvl")):
        with open(path.join(game_folder, 'currentlvl'), 'rt') as f:
            for line in f:
                savedata.append(line.strip())
        f.close()
    else:
        f = open(path.join(game_folder, 'currentlvl'), "w+")
        f.write('0\n')
        savedata.append(0)
        f.close()

    return savedata

def save(save):
    f = open(path.join(game_folder, 'currentlvl'), "w+")
    for data in save:
        f.write(f"{data}\n")
    f.close()