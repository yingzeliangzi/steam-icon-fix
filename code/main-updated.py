import string
import os
import vdf
from steam.client import SteamClient
from urllib.request import urlretrieve

cloudflare_icon_url = "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/"
steam_folder_finder = ['Program Files/Steam','Program Files(x86)/Steam','Steam']
disk_all = []
game_list = []

def get_disklist():
    global disk_all
    for c in string.ascii_uppercase:
        disk = c + ':\\'
        if os.path.isdir(disk):
            disk_all.append(disk)

def get_steam_vdf():
    global steam_vdf
    for i in disk_all:
        for j in steam_folder_finder:
            if os.path.exists(os.path.join(i,j,'steamapps','libraryfolders.vdf')) is True:
                steam_vdf = os.path.join(i,j,'steamapps','libraryfolders.vdf')
                global steam_icon_folder
                steam_icon_folder = os.path.join(i,j,'steam','games')

def get_gamelist():
    global steam_vdf
    global game_list
    vdf_data = vdf.load(open(steam_vdf))
    for i in range(len(vdf_data['libraryfolders'].keys())):
        i_game_list = list(vdf_data['libraryfolders'][str(i)]['apps'].keys())
        game_list.extend(i_game_list)
    #print(game_list)
    

def get_icon():
    client = SteamClient()
    client.anonymous_login()
    assert client.logged_on
    for app_id in game_list:
        app_id = int(app_id)
        game_info = (client.get_product_info(apps=[app_id, ]))['apps'][app_id]['common']
        try:
            game_name = game_info["name_localized"]["english"]
        except KeyError:
            game_name = game_info["name"]
        if game_info["name"] == "Steamworks Common Redistributables":
            continue
        if "clienticon" in list(game_info.keys()):
            if os.path.exists(os.path.join(steam_icon_folder, game_info["clienticon"] + '.ico')):
                print("# %s \t\tICON ALREADY EXISTS, SKIP." % game_name)
                continue
            game_icon_url = cloudflare_icon_url + str(app_id) + "/" + game_info["clienticon"] + '.ico'
            game_icon_filename = os.path.join(steam_icon_folder, game_info["clienticon"] + '.ico')
            urlretrieve(game_icon_url, game_icon_filename)
            if os.path.exists(game_icon_filename):
                print("# %s \t\tICON DOWNLOAD SUCCESSFUL." % game_name)
            else:
                print("# %s \t\tICON DOWNLOAD FAILED." % game_name)
        else:
            print("# %s \t\tDON'T HAVE ICON, SKIP." % game_name)
    return True

if __name__ == '__main__':
    get_disklist()
    get_steam_vdf()
    get_gamelist()
    get_icon()
