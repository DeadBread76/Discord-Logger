import os
import json
import random
import datetime
import discord
import asyncio
import string
import requests
import unicodedata

client = discord.Client()
with open('token.json', 'r') as handle:
    config = json.load(handle)

token = config["token"]

logs = ".\\Logs\\"
if os.path.isdir(logs):
    pass
else:
    os.mkdir(logs)


valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255
def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    for r in replace:
        filename = filename.replace(r,'_')
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    return cleaned_filename[:char_limit]

@client.event
async def on_ready():
    now = datetime.datetime.now()
    await client.change_presence(status=discord.Status.offline)
    usern = client.user.name+"#"+client.user.discriminator
    userlogs = logs+usern+"\\"
    if os.path.isdir(userlogs):
        pass
    else:
        os.mkdir(userlogs)
    with open (userlogs+"userinfo.txt", "w+", errors='ignore') as handle:
        handle.write('====================================\n')
        handle.write('Token: '+str(client.http.token)+'\n')
        handle.write('Email: '+str(client.email)+'\n')
        handle.write('Username: '+str(client.user.name)+'#'+str(client.user.discriminator)+'\n')
        handle.write('User ID: '+str(client.user.id)+'\n')
        handle.write('Created on: '+str(client.user.created_at)+'\n')
        handle.write('Avatar URL: '+str(client.user.avatar_url)+'\n')
        handle.write('====================================\n')
        servercount = 0
        for server in client.servers:
            servercount += 1
        handle.write('Member of '+str(servercount)+' servers:'+'\n')
        for server in client.servers:
            handle.write('\n')
            handle.write('Name: '+server.name+'\n')
            handle.write('ID: '+server.id+'\n')
            if server.owner.id == client.user.id:
                serverowner = True
            else:
                serverowner = False
            for channel in server.channels:
                myperms = channel.permissions_for(server.get_member(client.user.id))
                if myperms.administrator:
                    admin = True
                    break
                else:
                    admin = False
                    break
            membercount = 0
            for member in server.members:
                membercount += 1
            handle.write('Member Count: ' + str(membercount)+'\n')
            handle.write('Owner: '+str(serverowner)+'\n')
            handle.write('Admin: '+str(admin)+'\n')
        handle.write('====================================\n')


@client.event
async def on_message(message):
    await client.wait_until_ready()
    now = datetime.datetime.now()
    try:
        print ("("+now.strftime("%d/%m/%Y %H:%M:%S")+") ["+str(message.author)+"]: "+message.content)
    except:
        pass
    usern = client.user.name+"#"+client.user.discriminator
    userlogs = logs+usern+"\\"
    attachments = message.attachments
    if 'https://discord.gg/' in message.content:
        code = message.content.split("https://discord.gg/",1)[1][:7].rstrip()
        invite = 'https://discord.gg/'+code
        with open (userlogs+"invites.txt", "a+", errors='ignore') as handle:
            handle.write(invite+"\n")
    if message.channel.is_private:
        dmpath = userlogs+"DMs\\"
        if os.path.isdir(dmpath):
            pass
        else:
            os.mkdir(dmpath)
        if attachments:
            for attachment in attachments:
                r = requests.get(attachment["url"])
                if os.path.isdir(dmpath+"Files\\"):
                    pass
                else:
                    os.mkdir(dmpath+"Files\\")
                with open(dmpath+"Files\\"+attachment["filename"], 'wb')as handle:
                    handle.write(r.content)
        with open (dmpath+client.user.name+" DMs.txt", "a+", errors='ignore') as handle:
            handle.write("("+now.strftime("%d/%m/%Y %H:%M:%S")+") ["+str(message.author)+"]: "+message.content+"\n"+"\n")
    else:
        serverpath = userlogs+clean_filename(str(message.server.name))+"\\"
        chanpath = serverpath+clean_filename(str(message.channel.name))+"\\"
        if os.path.isdir(serverpath):
            pass
        else:
            os.mkdir(serverpath)
        if os.path.isdir(chanpath):
            pass
        else:
            os.mkdir(chanpath)
        if attachments:
            for attachment in attachments:
                r = requests.get(attachment["url"])
                if os.path.isdir(chanpath+"Files\\"):
                    pass
                else:
                    os.mkdir(chanpath+"Files\\")
                with open(chanpath+"Files\\"+attachment["filename"], 'wb')as handle:
                    handle.write(r.content)
        with open (chanpath+clean_filename(str(message.channel.name))+".txt", "a+", errors='ignore') as handle:
            handle.write("("+now.strftime("%d/%m/%Y %H:%M:%S")+") ["+str(message.author)+"]: "+message.content+"\n"+"\n")

if config["type"] == "bot":
    try:
        client.run(token)
    except Exception:
        print ("Invalid Token.")
        input ()
elif config["type"] == "user":
    try:
        client.run(token,bot=False)
    except Exception:
        print ("Invalid Token.")
        input ()
