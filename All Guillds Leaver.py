import requests, threading, os, time

c = 0

def pick(lenn):
    alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
    text = ''
    for _ in range(0, lenn):
        text += alpha

def headers(token):
    return {
        "authority": "discord.com",
        "method": "POST",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "Authorization": token,
        "content-length": "0",
        "cookie": f"__cfuid={pick(43)}; __dcfduid={pick(32)}; locale=en-US",
        "origin": "https://discord.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.600 Chrome/91.0.4472.106 Electron/13.1.4 Safari/537.36",
        "x-context-properties": "eyJsb2NhdGlvbiI6Ikludml0ZSBCdXR0b24gRW1iZWQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijg3OTc4MjM4MDAxMTk0NjAyNCIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI4ODExMDg4MDc5NjE0MTk3OTYiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjAsImxvY2F0aW9uX21lc3NhZ2VfaWQiOiI4ODExOTkzOTI5MTExNTkzNTcifQ==",
        "x-debug-options": "bugReporterEnabled",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJjYW5hcnkiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC42MDAiLCJvc192ZXJzaW9uIjoiMTAuMC4yMjAwMCIsIm9zX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoic2siLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5NTM1MywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }

def get_guilds(token):
    guilds = requests.get(f"https://discord.com/api/v9/users/@me/guilds", headers=headers(token))
    return guilds.json()

def leave(token):
    global c
    try:
        while True:
            guilds = get_guilds(token)
            if not "You are being rate limited." in str(guilds):
                break
            time.sleep(5)
        if guilds != []:
            print(guilds)
        else:
            print("There are no servers")
        for guild in guilds:
            guild_id = guild["id"]
            req = requests.delete("https://discord.com/api/v9/users/@me/guilds/" + guild_id, headers=headers(token))
            if req.status_code == 204:
                guild_name = guild["name"]
                print(f"Leaved! - {token} GuildID: {guild_id}, GuildNAME: {guild_name}")
            else:
                print(req.json())
            c+=1
    except Exception as e:
        print(e)
        c+=1
    
for token in open("tokens.txt", "r").read().split("\n"):
    try:
        token = token.split(":")[2]
    except:
        pass
    threading.Thread(target=leave, args=(token,)).start()
while True:
    if c == len(open("tokens.txt", "r").read().split("\n")):
        break
os.system("pause")
