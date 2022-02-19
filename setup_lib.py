import os, pygame, json

def set_settings(json_file):
    settings_dict = {}
    settings_dict["src_path"] =  os.path.dirname(os.path.realpath(__file__))
    settings_dict["window_size"] = (1600,900)
    with open(json_file,"r+") as f:
        json.dump(settings_dict, f, indent=4)


def get_settings(json_file):
    settings_dict = {}
    with open(json_file, "r") as f:
        settings = json.load(f)
        for k, v in settings.items():
            settings_dict[k] = v
    return settings_dict
            

def load_images(src_dir):
    directory = os.path.join(src_dir, "images")
    img_files_list = []
    image_dict = {}
    for file in os.listdir(directory):
        img_files_list.append(os.path.join(directory, file))
    for img in img_files_list:
        img_without_ext = os.path.splitext(img)
        img_name = (img_without_ext[0].split(os.path.sep))[-1]
        image_dict[img_name] = pygame.image.load(img)
    return image_dict
