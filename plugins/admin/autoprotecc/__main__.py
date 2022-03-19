import os
import requests
from bs4 import BeautifulSoup
import asyncio
from userge.utils import take_screen_shot
from userge import userge, Message, config, filters

from PIL import Image
import imagehash
from pymongo import MongoClient
mongocl = MongoClient("mongodb+srv://bhavya32:bhavya32@cluster0.zv4sy.mongodb.net/cluster0?retryWrites=true&w=majority")
dbhashall=mongocl['hashes']["dbhashall"]
dbhashimp=mongocl['hashes']["dbhashimp"]
dbhashnew=mongocl['hashes']["dbhashnew"]
grpstatus=mongocl['grps']["grpstatus"]
grpstatuslcl=[]
#grpstatus = {"-1001532927333":{"ap":0,"ar":1,"name":"AFG"},"-1001596986612":{"ap":0,"ar":1,"name":"Anime"},"-606367897":{"ap":1,"ar":2,"name":"test"},"-1001629575273":{"ap":1,"ar":2,"name":"reverse"}}
for x in grpstatus.find():
  grpstatuslcl.append(x)
def checkgrpstatus(gid):
    for x in grpstatuslcl:
      if x["grpid"]==gid:
        return x
    return {"ap":0, "ar":0}
def updategrpstatus(gid, key, val):
    query={"grpid":gid}
    cs=checkgrpstatus(gid)
    cs[key]=val
    grpstatus.update_one(query, {"$set": cs}, True)
    for x in grpstatuslcl:
      if x["grpid"]==gid:
       x[key]= val
        
def find_between_r( main, first, last ):
    try:
        start = main.rindex( first ) + len( first )
        end = main.rindex( last, start )
        return main[start:end]
    except ValueError:
        return ""
async def grslcl(location):
          multipart = {"encoded_image": (location, open(location, "rb")),"image_content": ""}
          google_rs_response = requests.post("http://www.google.com/searchbyimage/upload", files=multipart, allow_redirects=False)
          the_location = google_rs_response.headers.get("Location")
          #os.remove(location)
          headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"}
          response = requests.get(the_location, headers=headers)
          soup = BeautifulSoup(response.text, "html.parser")
          try:
                prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
          except IndexError:
                return
          prs_anchor_element = prs_div.find("a")
          prs_text = prs_anchor_element.text
          return prs_text
@userge.on_filters(filters.outgoing & filters.text)
async def txtcmd(message: Message):
  global grpstatus
  if (message.outgoing) and (message.text==".grpstatus"):
   await message.reply(str(grpstatuslcl))
  if (message.outgoing) and (".ap " in message.text):
   #grpstatus[str(message.chat.id)]["ap"] = int(message.text.split(" ")[1])
   updategrpstatus(message.chat.id, "ap", int(message.text.split(" ")[1]))
   await message.delete()
  if (message.outgoing) and (".ar " in message.text):
   #grpstatus[str(message.chat.id)]["ar"] = int(message.text.split(" ")[1])
   updategrpstatus(message.chat.id, "ar", int(message.text.split(" ")[1]))
   await message.delete()
   
   
@userge.on_cmd("p", about="revdbsearch")
async def dbrev_search_img(message: Message):
    dis_loc = ''
    if message.reply_to_message:
        message_ = message.reply_to_message
        if message_.photo:
            dis = await message.client.download_media(
                message=message_,
                file_name=config.Dynamic.DOWN_PATH
            )
            dis_loc = os.path.join(config.Dynamic.DOWN_PATH, os.path.basename(dis))
        if dis_loc:
            hash = str(imagehash.average_hash(Image.open(dis_loc)))
            c2db = dbhashall.find_one({hash:{'$exists': 1}})
            if c2db:
             await message.edit("Name - " + c2db[hash])
            else:
             await message.edit("Image not present in DB.")
        else:
            await message.edit("Image couldnt be downloaded.")
            return
            
@userge.on_cmd("pp", about="revdbsearch_new")
async def dbrev_search_img_new(message: Message):
    dis_loc = ''
    if message.reply_to_message:
        message_ = message.reply_to_message
        if message_.photo:
            dis = await message.client.download_media(
                message=message_,
                file_name=config.Dynamic.DOWN_PATH
            )
            dis_loc = os.path.join(config.Dynamic.DOWN_PATH, os.path.basename(dis))
        if dis_loc:
            hash = str(imagehash.average_hash(Image.open(dis_loc)))
            c2db = dbhashnew.find_one({"hash":hash})
            if c2db:
             await message.edit("Name - " + c2db["Name"])
            else:
             await message.edit("Image not present in DB.")
        else:
            await message.edit("Image couldnt be downloaded.")
            return            
@userge.on_filters(filters.photo)
async def echo(message):
# try: 
  if(message.chat.id==-671342927) and ("Add them to your harem by sending /protecc character name" in message.caption):
     location=await message.client.download_media(message)
     hash = str(imagehash.average_hash(Image.open(location)))
     c2db = dbhashall.find_one({hash:{'$exists': 1}})
     if c2db: 
      await asyncio.sleep(2)
      await message.reply(c2db[hash].split(" ")[0])
  elif (message.from_user.id in {1964681186,1733263647,1051235839}) and ("Add them to your harem by sending /protecc character name" in message.caption): 
        location=await message.client.download_media(message)
        hash = str(imagehash.average_hash(Image.open(location)))
        c1db = dbhashimp.find_one({hash:{'$exists': 1}})
        c2db = dbhashnew.find_one({"hash":hash})
        if c1db:
        #if hash in hashes:
        # if(grpstatus[str(message.chat.id)]["ap"]==1):
         if(checkgrpstatus(message.chat.id)["ap"]==1):
          await asyncio.sleep(1)
          message_ = await message.reply("/protecc " + c1db[hash].split(" ")[0])
          await asyncio.sleep(1)
          await message_.delete()
          await asyncio.sleep(2)
          await message.reply("brb ffffff")
         elif(checkgrpstatus(message.chat.id)["ap"]==0):
          await message.client.send_message("me", c1db[hash])
        elif c2db:
        #elif hash in hashall:
         if(checkgrpstatus(message.chat.id)["ar"]==2):
          await asyncio.sleep(2)
          message_ = await message.reply("/protecc " + c2db[name].split(" ")[0])
          #await asyncio.sleep(1)
          await message_.delete()
         elif(checkgrpstatus(message.chat.id)["ar"]==1):
          await message.client.send_message(-1001629575273,"`/protecc "+c2db[name].split(" ")[0]+"`",parse_mode="markdown")
        else:
         if(checkgrpstatus(message.chat.id)["ar"]==1):
          grs=await grslcl(location)
          grp=message.chat.id
          if(message.chat.id==-1001532927333):
           grp="AFG"
          elif(message.chat.id==-1001596986612):
           grp="Anime"
          elif(message.chat.id==-606367897):
           grp="test grp"
          await message.client.send_message(-1001629575273,"GRS - `/protecc "+grs+"`" + " - " + str(grp),parse_mode="markdown")
         if(checkgrpstatus(message.chat.id)["ar"]==2):
          grs=await grslcl(location)
          await asyncio.sleep(1)
          await message.reply("/protecc " + grs)
  if (message.chat.id==-606367897) and ("OwO! Check out this" in message.caption):
     location=await message.client.download_media(message=message)
     hash = str(imagehash.average_hash(Image.open(location)))
     charname=find_between_r(message.caption, ". ", " (W")
     if not dbhashimp.find_one({hash:{'$exists': 1}}):
      dbhashimp.insert_one({hash:charname})
      await message.reply(hash + " - " + charname + " - IMP")
     else:
      await message.reply("Character Already Present in IMP")
     #if not hash in hashes:
     #  hashes[hash] = charname
     #  with open('hashes.txt', 'wb') as f:
     #    cPickle.dump(hashes, f)
     #else:
     # if not hash in hashall:
     #   hashall[hash] = charname
  if (message.chat.id==-1001629575273) and ("OwO! Check out this" in message.caption):
     location=await message.client.download_media(message=message)
     hash = str(imagehash.average_hash(Image.open(location)))
     #charname=find_between_r(message.caption, ". ", " (W")
     charname=" ".join(message.caption.split("\n")[3].split(" ")[1:-3])
     parsedanime = message.caption.split("\n")[2]
     if not dbhashnew.find_one({"hash":hash}):
      #dbhashall.insert_one({hash:charname})
      dbhashnew.insert_one({"Name":charname, "Anime": parsedanime, "hash":hash})
      await message.reply(hash + " - " + charname)
     else:
      await message.reply("Character Already Present")
