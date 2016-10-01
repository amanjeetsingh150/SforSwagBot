from bs4 import BeautifulSoup
import urllib2
import time
import requests
import telepot
import unirest
Zomatokey='---------ENTER ZOMATO KEY-------------------------'
latitude=0.0
longitude=0.0
WELCOME='Welcome to the s for swag. This bot is used to find lyrics of songs and to know about resturants and their menu around you. For lyrics just type Lyrics <songname>-<artist> in this format and to know restaurants around you send your location.For the menu of restaurants type Menu <restaurantname>.\nFor random quotes type Send quotes...ENJOY\nMade by Amanjeet Singh'
def sendMenu(msg):
    print 'Message of menu wanted ',msg
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    command=msg['text']
    print str(latitude)
    command=command.split(' ',1)[1]
    print command
    command=command.title()
    baseurl1='https://developers.zomato.com/api/v2.1/geocode?lat=%f&lon=%f' %(latitude,longitude)
    header= {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "-------ZOMATO KEY------------------------"}
    response= requests.get(baseurl1,headers=header)
    p=response.json()
    bot.sendMessage(chat_id,"This is the link of the menu: ")
    for x in range(len(p['nearby_restaurants'])):
        print p['nearby_restaurants'][x]['restaurant']['menu_url']
        if p['nearby_restaurants'][x]['restaurant']['name'] == command:
            print p['nearby_restaurants'][x]['restaurant']['menu_url']
            bot.sendMessage(chat_id,p['nearby_restaurants'][x]['restaurant']['menu_url'])
    print baseurl1
    return
def sendnear(msg):
    print 'MESSAGE OF LOCATION ',msg
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    lat=msg['location']['latitude']
    lon=msg['location']['longitude']
    global latitude
    latitude=lat
    global longitude
    longitude=lon
    baseurl='https://developers.zomato.com/api/v2.1/geocode?lat=%f&lon=%f' %(lat,lon)
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "--------------ZOMATO KEY----------------------"}
    response = requests.get(baseurl, headers=header)
    print baseurl
    print str(lat)
    g=response.json()
    bot.sendMessage(chat_id,'These are the list of restaurants and cafes near your :\n')
    for x in range(len(g['nearby_restaurants'])):
        print g['nearby_restaurants'][x]['restaurant']['name']
        bot.sendMessage(chat_id,g['nearby_restaurants'][x]['restaurant']['name'])        
    print g['nearby_restaurants'][0]['restaurant']['name']
    return
    
def find(artist,song,id):
    try:
        atozfile=urllib2.urlopen('http://www.azlyrics.com/lyrics/%s/%s.html' %(artist,song))
        atozhtml=atozfile.read()
        atozfile.close()
        soup=BeautifulSoup(atozhtml,'html.parser')
        a=soup.find_all('div')
        print 'yeeeeee j%s' %a[22].text
        if a[22].text is not None:
            bot.sendMessage(id,a[22].text)
        if a[22].text=='':
            print 'nhi haiii'
            bot.sendMessage(id,'Not Found')
        return 
    except Exception as e:
        return e
def sendQuote(msg):
    print 'Message of menu wanted ',msg
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    command=msg['text']    
    response = unirest.post("https://andruxnet-random-famous-quotes.p.mashape.com/?cat=famous",
    headers={
    "X-Mashape-Key": "-----------------XMASHAPE KEY----------------------------------",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
    }
    )
    print response.body
    t=response.body
    bot.sendMessage(chat_id,t['quote'])
    return
def handle(msg):
    print 'Message ye h ',msg
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type)
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    print ('USER'+username)
    if (content_type) == 'location':
        print 'HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        sendnear(msg)
    if (content_type) == 'text':
        print 'finalllllllllly'
        command=msg['text']
        if command == '/start':
            bot.sendMessage(chat_id,WELCOME)
        if command.split(' ', 1)[0]=='Lyrics':
            sendLyrics(msg)
        if command.split(' ',1)[0]=='Menu':
            sendMenu(msg)
        if command.split(' ',1)[0]=='Send':
            sendQuote(msg)
    return

def sendLyrics(msg):
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    command=msg['text']
    command=command.split(' ',1)[1]
    p=command.index('-')
    songname=command[:p]
    songname=songname.replace(" ","")
    songname=songname.lower()
    artist=command[p+1:]
    artist=artist.replace(" ","")
    artist=artist.lower()
    print songname
    find(artist,songname,chat_id)
    return

bot=telepot.Bot('------------------------BOT KEY---------------------------------')
bot.getMe()
bot.message_loop(handle)
print('Listening.....')
while 1:
    time.sleep(5)

        
            
        
