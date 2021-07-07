from BotAmino import BotAmino
import urllib
import os
from amino.lib.util.exceptions import ChatInvitesDisabled
from google_trans_new import google_translator
from BotAmino import *
import random
from random import uniform, choice, randint
import time
import json
import websocket
import threading
import contextlib
import sys
import json

client = BotAmino()

@client.command("test") #Allows the user to test if the bot is online (!test)
def test(data):
    data.subClient.send_message(data.chatId, f"Hello {data.author}! If you're reading this; It means that I'm online")

@client.command("Plaster") #Words of encouragement (!Plaster)
def Plaster(data):
    data.subClient.send_message(data.chatId, "I present to you a plaster, I've added some extra magic onto it so that it heals more than Physical pain, it helps heal heart pain and sadness too!! Swissy said that you need it so I've made this so you can feel better!!! 9/10 Swissy's reccomend it")
    
@client.command("follow") #Follows the user who sent the message (!follow)
def follow(data):
    data.subClient.send_message(data.chatId, f"Hey! {data.author}, I've just followed you!")
    data.subClient.follow_user(data.authorId)

@client.command("unfollow") #Unfollows the User who sent the message (!unfollow)
def unfollow(data):
    data.subClient.send_message(data.chatId, f"Oh, {data.author}, I've just unfollowed you... Is it something I've said?")
    data.subClient.unfollow_user(data.authorId)

@client.command("ramen") #Allows for free ramen to be given (!ramen)
def ramen(data):
    data.subClient.send_message(data.chatId, f"Here you go {data.author}!! Some Ramen for you 🍜🍜🍜")

@client.command("help") #Sends tutorial to user + mini introduction to bot
def help(data):
    data.subClient.send_message(data.chatId, f"Hello, I am the official Chatbot account for MAMAMOO Amino. You can call me Kevin!, If you need help in how to interact with me, look at this post! https://aminoapps.com/c/mamamoo/page/blog/the-mmmabot-tutorial-18-05-2021/r07W_QG7teu04aqGZe8oM4J4nw4KMlW6106")

@client.command("radish") #Offers radish milkies (!radish)
def radish(data):
    data.subClient.send_message(data.chatId, f"GaGa~ Here's your Milkies {data.author}~ Since you wanna act like a baby about this. *Hands out radishes*")

@client.command("huggies") #Bestowes upon the user big huggies
def huggies(data):
    data.subClient.send_message(data.chatId, f"Hey {data.author}! Open Wide!!! *HUGGIEEEESSSSSS*, They're called huggies because they're proven to be much more uwu than a normal hug.")

@client.command("name") #Changes the name on the Profile (!name x)
def name(data):
    data.subClient.subclient.edit_profile(nickname=data.message)
    data.subClient.send_message(chatId=data.chatId,message=f"name changed to {data.message}")
    
@client.on_member_join_chat() #When a Member Joins the Chat, Kevin will welcome them
def say_hello(data):
    data.subClient.send_message(data.chatId, f"welcome to the Chat {data.author}, I hope you enjoy your stay!")

@client.command("spawn") #Joins all Groupchats
def spawn (data):
    data.subClient.join_all_chat()
    data.subClient.send_message(data.chatId, f"All chatrooms have been Joined {data.author}.")

@client.command("unspawn") #Leaves All Groupchats
def unspawn (data):
    data.subClient.leave_all_chats()
    data.subClient.send_message(data.chatId, f"All chatrooms have been Left {data.author}.")

@client.command("bg") #Gets the bg of a groupchat (!bg)
def bg(data):
    image = data.subClient.get_chat_thread(data.chatId).backgroundImage
    if image is not None:
      filename = image.split("/")[-1]
      urllib.request.urlretrieve(image, filename)
      with open(filename, 'rb') as fp:
        data.subClient.send_message(chatId=data.chatId, file=fp, fileType="image")

@client.on_member_leave_chat(["chatId"]) # Greet's the member upon their Departure
def say_goodbye(data):
    data.subClient.send_message(data.chatId, "See you later MooMoo, Until Next Time!")

@client.command() #Translate's replied text into english via Embedded Google Translate (!tr)
def tr(args):
  data = args.subClient.subclient.get_message_info(chatId = args.chatId, messageId = args.messageId)
  reply_message = data.json['extensions']
  if reply_message:
    reply_message = data.json['extensions']['replyMessage']['content']
    reply_messageId = data.json['extensions']['replyMessage']['messageId']
    translator = google_translator() 
    detect_result = translator.detect(reply_message)[1]
    translate_text = translator.translate(reply_message)
    reply = "[IC]"+str(translate_text)+"\n\n[c]Translated Text from "+str(detect_result)
    print(reply)
    args.subClient.send_message(chatId=data.chatId,message=reply,replyTo=reply_messageId)


@client.command("icon") #Remotely change the Profile Icon (!icon, Reply on message ATTRIBUTE ERROR)
def icon(data):
    info = data.subClient.get_message_info(chatId = data.chatId, messageId = data.messageId)
    reply_message = info.json['extensions']
    if reply_message:
        image = info.json['extensions']['replyMessage']['mediaValue']
        for i in range(1,5):
            data.subClient.subclient.edit_profile(icon=image)
    data.subClient.send_message(data.chatId, message="Done")
            
@client.command("luv") #Love Probability (!luv x y)
def luv(data):
        msg = data.message + " null null "
        msg = msg.split(" ")
        msg[2] = msg[1]
        msg[1] = msg[0]
        try:
            data.subClient.send_message(data.chatId, message=f"the probability of love between {msg[1]} and {msg[2]} is {random.randint(0,100)}%")
        except:
            pass

@client.command("reboot")
def reboot(args):
    args.subClient.send_message(args.chatId, "Restarting Bot")
    os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])

@client.event("on_chat_invite")
def on_chat_invite(data):
    try:
        commuId = data.json["ndcId"]
        subClient = client.get_community(commuId)
    except Exception:
        return

    args = Parameters(data, subClient)

    subClient.join_chatroom(chatId=args.chatId)
    subClient.send_message(args.chatId, f"Hello!\n[B]I am a bot, if you have any question ask a staff member!\nHow can I help you?\n(you can do {subClient.prefix}help if you need help)")

client.activity = True
client.launch(True)
print("ready")