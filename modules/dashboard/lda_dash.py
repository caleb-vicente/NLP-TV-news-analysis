# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 11:44:45 2020

@author: cvicentm
"""

#------------------------------------------------------
#GET DDBB update channels into database
#------------------------------------------------------
from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
dic_subtitles = dict(dbAdapter.selectAll())
dbAdapter.close()
print("finalizada consulta")

import modules.variables as v
channels = v.CHANNELS

channel_column = [(subtitle, channel) for subtitle in list(dic_subtitles.keys()) 
                    for channel in channels if subtitle.find(channel)!=-1 ]


from modules.sql import dBAdapter
dbAdapter= dBAdapter.Database()
dbAdapter.open()
for ch in channel_column:
    dbAdapter.update_channel(ch[0],ch[1])   
dbAdapter.close()
print("finalizada consulta")