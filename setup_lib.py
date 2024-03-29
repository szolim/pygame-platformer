import os, pygame, json

def set_settings(json_file):
    """Save all the general settings to a json file"""
    settings_dict = {}
    settings_dict["src_path"] = os.path.dirname(os.path.realpath(__file__))
    settings_dict["window_size"] = (1600, 900)
    with open(json_file, "r+") as f:
        json.dump(settings_dict, f, indent=4)


def get_settings(json_file):
    """load all the needed settings from a json file as a dictionary"""
    settings_dict = {}
    with open(json_file, "r") as f:
        settings = json.load(f)
        for k, v in settings.items():
            settings_dict[k] = v
    return settings_dict


def load_images(src_dir, images_dir=None):
    """Create a dictionary of assets(images_dir) where key is name of
    .png file wihtout extension, and value is a pygame.surface loaded from that file"""
    if images_dir != None:
        directory = os.path.join(src_dir, "images{}{}".format(os.sep, images_dir))
        img_files_list = []
        image_dict = {}
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                img_files_list.append(os.path.join(directory, file))
        for img in img_files_list:
            img_without_ext = os.path.splitext(img)
            img_name = (img_without_ext[0].split(os.path.sep))[-1]
            image_dict[img_name] = pygame.image.load(img)
            image_dict[img_name].set_colorkey((0,0,0))
    
    else: 
        directory = os.path.join(src_dir, "images")
        img_files_list = []
        image_dict = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                img_files_list.append(os.path.join(root, file))
        for img in img_files_list:
            img_without_ext = os.path.splitext(img)
            img_name = (img_without_ext[0].split(os.path.sep))[-1]
            image_dict[img_name] = pygame.image.load(img)
            image_dict[img_name].set_colorkey((0,0,0))
    return image_dict
