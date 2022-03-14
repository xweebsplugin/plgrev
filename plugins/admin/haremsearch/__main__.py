import json
import time
import asyncio
queryid=0
ressarrl=[]
pagearr=[]
from userge import userge, Message, config, filters
@userge.on_cmd("hws", about="harem search waifu")
async def revhws(message: Message):
  global cancontinue
  global ressarrl
  global queryid
  if(message.outgoing) and (".hs" in message.text):
    
    charname=message.text.replace(".hs ", "")
    await message.edit("Searching - " + charname)
    print(charname)
    currpage=0
    
    
    while(True):
     start = time.time()
     query=str(message.chat.id) + "." + str(message.from_user.id) + "." + str(currpage)
     res = await message.client.get_inline_bot_results("Collect_yours_waifus_bot", str(query))
     end = time.time()
     resarr=res["results"]
     if(len(resarr)==0):
      print("end of harem reached")
      break
     for oneres in resarr:
      parsednames = oneres.send_message.message.lower().split("\n")[3].split(" ")
      #print(parsednames)
      if charname in parsednames:
       print("found on pg" + str(currpage))
       await message.client.send_inline_bot_result(message.chat.id, res.query_id, oneres.id)
       end = time.time()
       print(end-start)
       break;
     else:
      print("char not found on pg" + str(currpage))
      currpage+=1
      
      print(end - start)
      continue
     break
    
@userge.on_cmd("hs", about="hharem search husbando")
async def revhs(message: Message):
  global cancontinue
  global ressarrl
  global queryid
  if(message.outgoing) and (".hs" in message.text):
    
    charname=message.text.replace(".hs ", "")
    await message.edit("Searching - " + charname)
    print(charname)
    currpage=0
    
    
    while(True):
     start = time.time()
     query=str(message.chat.id) + "." + str(message.from_user.id) + "." + str(currpage)
     res = await message.client.get_inline_bot_results("Collect_your_husbando_bot", str(query))
     end = time.time()
     resarr=res["results"]
     if(len(resarr)==0):
      print("end of harem reached")
      break
     for oneres in resarr:
      parsednames = oneres.send_message.message.lower().split("\n")[3].split(" ")
      #print(parsednames)
      if charname in parsednames:
       print("found on pg" + str(currpage))
       await message.client.send_inline_bot_result(message.chat.id, res.query_id, oneres.id)
       end = time.time()
       print(end-start)
       break;
     else:
      print("char not found on pg" + str(currpage))
      currpage+=1
      
      print(end - start)
      continue
     break
