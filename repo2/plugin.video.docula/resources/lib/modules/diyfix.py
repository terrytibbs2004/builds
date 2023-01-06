# -*- coding: utf-8 -*-

# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)

import urllib, sys, re, os, unicodedata
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs

try:
    # Python 3
    from urllib.request import urlopen, Request
except ImportError:
    # Python 2
    from urllib2 import urlopen, Request

try:
    # Python 3
    from html.parser import HTMLParser
except ImportError:
    # Python 2
    from HTMLParser import HTMLParser

from resources.lib.modules.common import *

params = get_params()
mode = None

addon_id     = xbmcaddon.Addon().getAddonInfo('id') 
artAddon     = 'script.j1.artwork'

selfAddon = xbmcaddon.Addon(id=addon_id)
plugin_handle = int(sys.argv[1])
dialog = xbmcgui.Dialog()
mysettings = xbmcaddon.Addon(id = 'plugin.video.docula')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')

try:
    datapath= xbmcvfs.translatePath(selfAddon.getAddonInfo('profile'))
except:
    datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))

try:
    fanart = xbmcvfs.translatePath(os.path.join(home, 'fanart.jpg'))
    icon = xbmcvfs.translatePath(os.path.join(home, 'icon.png'))
except:
    fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
    icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

mediapath = 'http://j1wizard.net/media/'

BASE  = "plugin://plugin.video.youtube/playlist/"
cBASE = "plugin://plugin.video.youtube/channel/"
uBASE = "plugin://plugin.video.youtube/user/"

#=========================================================================================================

YOUTUBE_CHANNEL_ID_4001 = "PLmVg1E9ug_5FPbIZpzIT1X0P8pB0vBZey" #Appliance Repair Videos
YOUTUBE_CHANNEL_ID_4002 = "PL9B1EF76E0E47B661"                 #Refrigerator Repair
YOUTUBE_CHANNEL_ID_4003 = "PLcw0jYjduh9NbZSi17ssOgdRF3JxkbO4d" #GE Appliance Repair
YOUTUBE_CHANNEL_ID_4004 = "PLzMQZSxC-ydsJxsbJSYWQ-65gK6Sh9Lgj" #Dryer, Dishwasher, And More
YOUTUBE_CHANNEL_ID_4005 = "PLw-xTfzVdUvdmAYEXvux55DdcoOZeI7-u" #Domestic Appliance Repair
YOUTUBE_CHANNEL_ID_4006 = "PLnPe5qHhMYYIXyVj8J3bqk1NgUWAtH-VJ" #Maytag Appliance Repair
YOUTUBE_CHANNEL_ID_4007 = "PL3EB33F2356EAFCD4"                 #More Refrigerator Repair
YOUTUBE_CHANNEL_ID_4008 = "PL9460A1B80DCFAA37"                 #Refrigerator, Icemaker, Repair
YOUTUBE_CHANNEL_ID_4009 = "PLEI370zA5QD8asMbeNZovHe9NhJD8L4vR" #Samsung Refrigerator Repair
YOUTUBE_CHANNEL_ID_4010 = "PL1XIJVXWDpWlSmARqp6XVt_MRTX4dZi13" #Appliance Repair 101
YOUTUBE_CHANNEL_ID_4011 =	"PL503FB42FF1C27877"                 #Appliance - Refrigerators 101
YOUTUBE_CHANNEL_ID_4012 = "PLnPe5qHhMYYIAatxUKCMn0UgEuLcIxB97" #Frigidaire Appliance Repair
YOUTUBE_CHANNEL_ID_4013 = "PLjEkHwf0clGyaZFJ7JEvHCIRWa0EM1cel" #Appliance Troubleshoot And Repair
YOUTUBE_CHANNEL_ID_4014 = "PL9us_8L8rYRcnpZqHrotx1vcClbbcg_v1" #Appliance Repair Two
YOUTUBE_CHANNEL_ID_4015 = "PL3F459A4232ECBA0A"                 #Repairs - Appliances
YOUTUBE_CHANNEL_ID_4016 = "PLnPe5qHhMYYIzxeSE2QWUGI1N-B5-lOq_" #Bosch Appliance And More
YOUTUBE_CHANNEL_ID_4017 = "PLTbuM2OJ19bP4Nv-L1VoodGQwbKHAdMQH" #Home Appliance Repairs
YOUTUBE_CHANNEL_ID_4018 = "PLmVg1E9ug_5GPlmrakB0lTSp8T6A6Go7h" #Easy Miele Appliance Repair
YOUTUBE_CHANNEL_ID_4019 = "PLnPe5qHhMYYKoVOb2xl2o0XPGOKS2grgW" #Miele Appliance Repair
YOUTUBE_CHANNEL_ID_4020 = "PL759B71082A02775B"                 #More Appliance Repair
YOUTUBE_CHANNEL_ID_4021 = "PLgrHnXFgPD2X7jxXmWTR9ezddezbfClz_" #Bill Newberry Appliance Repair
YOUTUBE_CHANNEL_ID_4022 = "PLE69028BF10BB54DB"                 #Kenmore - Whirlpool Repair
YOUTUBE_CHANNEL_ID_4023 = "PL0yxKzTTHvzxRAd3J66FvTKEsPyii63QS" #GE Appliance Repair
YOUTUBE_CHANNEL_ID_4024 = "PL5xArxxmQoF1nE599-QfGPmoIC154CROT" #GE Side By Side Frigerator
YOUTUBE_CHANNEL_ID_4025 = "PL1KbCKGqZdQILcfNeFFfQocZHEg5LFJJV" #Popular GE Dishwasher Videos
YOUTUBE_CHANNEL_ID_4026 = "PL1KbCKGqZdQJ9F7p96NnyjD51P8tWTlgD" #Popular GE Clothes Dryer Video
YOUTUBE_CHANNEL_ID_4027 = "PL1KbCKGqZdQLtauY902uVmE8HglQXS3Fd" #Popular GE Stove Repair Video
YOUTUBE_CHANNEL_ID_4028 = "PL1KbCKGqZdQK5-MsETF4QQhOot-8V2-H9" #Popular GE Icemaker Video
YOUTUBE_CHANNEL_ID_4029 = "PL1KbCKGqZdQL54gUo01XIqm6S6X12xnqG" #Popular GE Microwave Repair Video
YOUTUBE_CHANNEL_ID_4030 = "PLQjiaVNP5TCKO-KGqhe7fGhqrJw_zyvZc" #Popular GE Clothes Washer Videos
YOUTUBE_CHANNEL_ID_4031 = "PL7zNVN3dbpmscAp5zYzP3F1slM_GjUM-E" #Popular Hotpoint And Kenmore Video
YOUTUBE_CHANNEL_ID_4032 = "PLbvOduRAsH208jqTaL5241Xpfg4T2G-sK" #Popular Maytag Clothes Washer Videos
YOUTUBE_CHANNEL_ID_4033 = "PLZ4jKPxStiUxERcDK6xDbIGbcEEtz2e3L" #Window Air Conditioner And Appliance
YOUTUBE_CHANNEL_ID_4034 = "PL6B12D4E23544521C"                 #How To Repair Air Conditioners
YOUTUBE_CHANNEL_ID_4035 = "" #
YOUTUBE_CHANNEL_ID_4036 = "" #
YOUTUBE_CHANNEL_ID_4037 = "" #
YOUTUBE_CHANNEL_ID_4038 = "" #
YOUTUBE_CHANNEL_ID_4039 = "" #
YOUTUBE_CHANNEL_ID_4040 = "" #
YOUTUBE_CHANNEL_ID_4041 = "" #
YOUTUBE_CHANNEL_ID_4042 = "" #
YOUTUBE_CHANNEL_ID_4043 = "" #
YOUTUBE_CHANNEL_ID_4044 = "" #
YOUTUBE_CHANNEL_ID_4045 = "" #
YOUTUBE_CHANNEL_ID_4046 = "" #
YOUTUBE_CHANNEL_ID_4047 = "" #
YOUTUBE_CHANNEL_ID_4048 = "" #
YOUTUBE_CHANNEL_ID_4049 = "" #
YOUTUBE_CHANNEL_ID_4050 = "PLtlovSIm2kUqZe7LUTKU1Dy3t8fa0yWeI" #Small Appliance And Tool Repair
YOUTUBE_CHANNEL_ID_4051 = "PLTbuM2OJ19bP4Nv-L1VoodGQwbKHAdMQH" #Home Appliance Repair And Service
YOUTUBE_CHANNEL_ID_4052 = "PLLeIKkAbXalPN8Taomp3CNVwYpOUYIBSr" #Appliance Repair: Keurig And More
YOUTUBE_CHANNEL_ID_4053 = "PLbZR-5Tc92erEgy86yB_XmtmHTTRl4V6_" #Coffee Pot Repair
YOUTUBE_CHANNEL_ID_4054 = "PL-nScDq_S2WPg3w8nIAI54XoAL4bVUTKU" #Kitchenaid Mixer Repairs
YOUTUBE_CHANNEL_ID_4055 = "PLkQ2BYmMy3eDuplKeeirQhI2eqXib0ko4" #Delonghi Coffee Maker And More
YOUTUBE_CHANNEL_ID_4056 = "PLvhpPFnSTdRz-RcJ4U-nKX3XWUNpD_XQH" #Old Radio Repair And More
YOUTUBE_CHANNEL_ID_4057 = "PLZeS6GNK1mI1auobpVtHuGUsixO0_twt1" #Singer Sewing Machine Repair
YOUTUBE_CHANNEL_ID_4058 = "PLu4FNfRM4yJpngrrxeZuYR3a2e5FA9UZi" #Husqvarna Sewing Machine Repair
YOUTUBE_CHANNEL_ID_4059 = "PLuMSfWJ9GYpO9L-mEVlwNAVSN7esQ1PO6" #Sewing Machine Repair
YOUTUBE_CHANNEL_ID_4060 = "PLgyc6eruU9hfMufC7a7dSmUKFYuZHv6PC" #More Sewing Machine Repair
YOUTUBE_CHANNEL_ID_4061 = "PLkEygncLQDWMAfGWH3UdUaigzfvRaACmQ" #Mixer and Blender Repair
YOUTUBE_CHANNEL_ID_4062 = "PLNsgjHb-ieskX4NVw8WE7S6V5pwBm33rK" #Dremel Tool Repair And Tips
YOUTUBE_CHANNEL_ID_4063 = "PLrBxzx9A1ipNGdEQlCWjRgssFHC9WfStA" #Kitchen Blender Repair
YOUTUBE_CHANNEL_ID_4064 = "PLrBxzx9A1ipMHT9p3TrGTBZ2JdcxZbutl" #Small Appliance Repair
YOUTUBE_CHANNEL_ID_4065 = "PLJEhES5WbXW3RQq1iSb70fIUZO07zirVA" #Microwave Oven Repair
YOUTUBE_CHANNEL_ID_4066 = "PLiENBcs2au1bq9BELfkbr7RW0YoDEkNJp" #Hoover Vacuum Cleaner Repair
YOUTUBE_CHANNEL_ID_4067 = "PLxJnOsa4Pi_EXjn5eBLYpBcO4iAAuZvGv" #Vacuum Cleaner Repair
YOUTUBE_CHANNEL_ID_4068 = "PLiENBcs2au1ZrNeyYrmpRQIftgsx1Pgji" #Electrolux vacuum cleaner repair
YOUTUBE_CHANNEL_ID_4069 = "PLMPlcXf6u73l4V7t7uZRn9-W-F39roU_u" #Repairs: Vacuum Cleaners
YOUTUBE_CHANNEL_ID_4070 = "PLM4HYsHL_dExfF3-iM6zNdWmSx1Wui-h_" #Shop Vac Repairs
YOUTUBE_CHANNEL_ID_4071 = "PLt4-8weTYtVtKcIu_cil5IpJx9VYC5_ue" #Popular Bissell And Vacuum Video
YOUTUBE_CHANNEL_ID_4072 = "" #
YOUTUBE_CHANNEL_ID_4073 = "" #
YOUTUBE_CHANNEL_ID_4074 = "" #
YOUTUBE_CHANNEL_ID_4075 = "" #
YOUTUBE_CHANNEL_ID_4076 = "" #
YOUTUBE_CHANNEL_ID_4077 = "" #
YOUTUBE_CHANNEL_ID_4078 = "" #
YOUTUBE_CHANNEL_ID_4079 = "" #
YOUTUBE_CHANNEL_ID_4080 = "" #
YOUTUBE_CHANNEL_ID_4081 = "" #
YOUTUBE_CHANNEL_ID_4082 = "" #
YOUTUBE_CHANNEL_ID_4083 = "" #
YOUTUBE_CHANNEL_ID_4084 = "" #
YOUTUBE_CHANNEL_ID_4085 = "" #
YOUTUBE_CHANNEL_ID_4086 = "" #
YOUTUBE_CHANNEL_ID_4087 = "" #
YOUTUBE_CHANNEL_ID_4088 = "" #
YOUTUBE_CHANNEL_ID_4089 = "" #
YOUTUBE_CHANNEL_ID_4090 = "" #
YOUTUBE_CHANNEL_ID_4091 = "" #
YOUTUBE_CHANNEL_ID_4092 = "" #
YOUTUBE_CHANNEL_ID_4093 = "" #
YOUTUBE_CHANNEL_ID_4094 = "" #
YOUTUBE_CHANNEL_ID_4095 = "" #
YOUTUBE_CHANNEL_ID_4096 = "" #
YOUTUBE_CHANNEL_ID_4097 = "" #
YOUTUBE_CHANNEL_ID_4098 = "" #
YOUTUBE_CHANNEL_ID_4099 = "" #
YOUTUBE_CHANNEL_ID_4100 = "PLEBoj5Njb1CaFDd5T9OnfMkS8wxQMUuAM" #Small Engine Repair
YOUTUBE_CHANNEL_ID_4101 = "PL2CD9761691C69800"                 #Lawnmower Repair
YOUTUBE_CHANNEL_ID_4102 = "PLu4nZ1fK5Id9GCKz0-9ejoExGf-FesYoI" #Repairs: Lawnmowers
YOUTUBE_CHANNEL_ID_4103 = "PLzUFIbYcndzVKJbzNEJh8IC4HEoQE5erf" #Weed Eater, Trimmers Repair
YOUTUBE_CHANNEL_ID_4104 = "PLBIWLmjTh7sOPYnEEgi-iYN7VyrqX4GnK" #Briggs And Stratton And Lawn Mower
YOUTUBE_CHANNEL_ID_4105 = "PLFOzJmuVe9k5REC_Mx9A3Zw-PhngjL-QJ" #String Trimmer And Leaf Blower Video
YOUTUBE_CHANNEL_ID_4106 = "PL9BSohcCwpQ2j7mkJLwk2dbAF4FOmb_S3" #Stihl MS170: Chainsaws
YOUTUBE_CHANNEL_ID_4107 = "PLgVFOrH4DEBkH7ibiq2Oh6Cj7ROkXOO5e" #Popular Chainsaw Videos
YOUTUBE_CHANNEL_ID_4108 = "PLCvUtm_axBnK24Wzh9LUqWxI7Ow7ZrqIb" #Poulain Pro Repair Video
YOUTUBE_CHANNEL_ID_4109 = "PL0KnfkfKaEfIATs-bQtEVd1jpClrhy1KO" #Craftsman Riding Mower Repair
YOUTUBE_CHANNEL_ID_4110 = "PLOTZjij4iVfR8Ha59mncOef3T7XzxXUjZ" #Lawn Mower Repair Video
YOUTUBE_CHANNEL_ID_4111 = "PLydO3Ru3iDiX7mM6NCTKowOV6l1c_6QqC" #Troy-Built Bronco Tractor Video
YOUTUBE_CHANNEL_ID_4112 = "PLgpTYBXbHpmJHZCgC8krmFwmRwS-y8YHv" #Riding Mower Repairs
YOUTUBE_CHANNEL_ID_4113 = "PL_hTA0Mj43i5abH46wJSG8D44_VHhS2UZ" #John Deere Riding Mower Repair
YOUTUBE_CHANNEL_ID_4114 = "PLbIE4lmhouwP56Dn8MSBUo8mfzJ-IYPk8" #John Deere Repairs: Riding Mower
YOUTUBE_CHANNEL_ID_4115 = "PLsYoN2fs0wwfgxccGfpiZA2bMQuFCv5aD" #Husqvarna Riding Mower Repair
YOUTUBE_CHANNEL_ID_4116 = "PLT0dlXJWEiMzOe2FuwMOO-l-qHrr_8h3w" #Murray Mower Repair Video
YOUTUBE_CHANNEL_ID_4117 = "PLhORnVQxJe0VP3W2dESQirBL0cWLUDO0s" #Carburetor Repair Video Series
YOUTUBE_CHANNEL_ID_4118 = "PL-XtZs_KE6F51PDKwGNMUz5tH0tdMDLIG" #Lawn Mowers And MTD Products
YOUTUBE_CHANNEL_ID_4119 = "PLPDSbcALwm4L_O-PBw2tM38BZziem14ol" #2-Cycle Engine Repair
YOUTUBE_CHANNEL_ID_4120 = "PL5y1VWhO4UKuHCj71HmDe3S8QFSage3jx" #Carburetor Repair Videos
YOUTUBE_CHANNEL_ID_4121 = "" #
YOUTUBE_CHANNEL_ID_4122 = "" #
YOUTUBE_CHANNEL_ID_4123 = "" #
YOUTUBE_CHANNEL_ID_4124 = "" #
YOUTUBE_CHANNEL_ID_4125 = "" #
YOUTUBE_CHANNEL_ID_4126 = "" #
YOUTUBE_CHANNEL_ID_4127 = "" #
YOUTUBE_CHANNEL_ID_4128 = "" #
YOUTUBE_CHANNEL_ID_4129 = "" #
YOUTUBE_CHANNEL_ID_4130 = "" #
YOUTUBE_CHANNEL_ID_4131 = "" #
YOUTUBE_CHANNEL_ID_4132 = "" #
YOUTUBE_CHANNEL_ID_4133 = "" #
YOUTUBE_CHANNEL_ID_4134 = "" #
YOUTUBE_CHANNEL_ID_4135 = "" #
YOUTUBE_CHANNEL_ID_4136 = "" #
YOUTUBE_CHANNEL_ID_4137 = "" #
YOUTUBE_CHANNEL_ID_4138 = "" #
YOUTUBE_CHANNEL_ID_4139 = "" #
YOUTUBE_CHANNEL_ID_4140 = "" #
YOUTUBE_CHANNEL_ID_4141 = "" #
YOUTUBE_CHANNEL_ID_4142 = "" #
YOUTUBE_CHANNEL_ID_4143 = "" #
YOUTUBE_CHANNEL_ID_4144 = "" #
YOUTUBE_CHANNEL_ID_4145 = "" #
YOUTUBE_CHANNEL_ID_4146 = "" #
YOUTUBE_CHANNEL_ID_4147 = "" #
YOUTUBE_CHANNEL_ID_4148 = "" #
YOUTUBE_CHANNEL_ID_4149 = "" #
YOUTUBE_CHANNEL_ID_4150 = "PLkJADc1qDrr_0MRi-qB9a5w2iyaBS-Ivb" #Plumbing Repairs
YOUTUBE_CHANNEL_ID_4151 = "PLVGwtfOyi0COduZcfixs13nnyScp7tEU7" #Fixing Things Around The Home
YOUTUBE_CHANNEL_ID_4152 = "PL0TSumYgsK5F0iwsiTXbrAjmWYOF_obql" #DIY Home Maintenance
YOUTUBE_CHANNEL_ID_4153 = "PLZoCMm1i4ry-JC_9IEl1xovSjR1qsjMiV" #Fan Electric Motor Repair
YOUTUBE_CHANNEL_ID_4154 = "PLsa3B6Lob01H4J6K5qhee9QPxo_F75dUg" #Home Repair: Plumbing
YOUTUBE_CHANNEL_ID_4155 = "PL8uD2CXuYLTQjDpAR6d0-baP-QmTLdLAn" #Home Repair And Bathtubs Video
YOUTUBE_CHANNEL_ID_4156 = "PL5bPtkUTaUWuohojSlEAlsaQvPJk26ADn" #Mobile Home Repairs
YOUTUBE_CHANNEL_ID_4157 = "PLDisarMwyE4P-t2c9wsERfzpWOwhirX_B" #HVAC Training Video
YOUTUBE_CHANNEL_ID_4158 = "PLjiXAEI9BqTvLCr2-8w16ajWRcyoPfcWU" #Electrical Wiring Video
YOUTUBE_CHANNEL_ID_4159 = "PLz-Df2AZyvO-JjsrvaVdGRWE0sfkyOiPL" #How To Test AC Compressors
YOUTUBE_CHANNEL_ID_4160 = "PLpkhBF0FjkwRO007KoPZ52vY6qSFYqQH3" #Home Improvement And Repair
YOUTUBE_CHANNEL_ID_4161 = "PLRBC-f3KkyJforJMV_iKoXDMP8pHZIZTq" #Popular Mosaic And Countertop
YOUTUBE_CHANNEL_ID_4162 = "PLIcIEnzVQfkOOQcMnEfofhfRBFerCGvOf" #Electricity: Troubleshooting
YOUTUBE_CHANNEL_ID_4163 = "PLNWirpSjKfeJ6FTbicWY72LbXKYloxrgV" #Popular Stainless Steel And Sink
YOUTUBE_CHANNEL_ID_4164 = "PLjH21j_HF8YR4q5AL1IXDB7_xybyQ5GDL" #Home Additions, Renovations, And More
YOUTUBE_CHANNEL_ID_4165 = "PL52iiVOj3SM0p5nXILN70T1Pvv3PpLVHS" #Home Repair: Kitchen Cabinets
YOUTUBE_CHANNEL_ID_4166 = "PLW7HO4dAq9_sS4ldcVXyMD19m7E6Q2TMR" #Handyman: Home Howto Video
YOUTUBE_CHANNEL_ID_4167 = "PLmfJCnMhFQoN9eYhBJixoNe1pYkzQ1cbs" #Plumbing - Boiler Basics
YOUTUBE_CHANNEL_ID_4168 = "PLIkVdxQ4ylV6771cnEgHy072PXjtpB8Y6" #Window Washing And Screen Repair
YOUTUBE_CHANNEL_ID_4169 = "PLw5qGtB6zcsMuVJlYCI867QB4DRh0r-1-" #Repairs: Drywall Tips
YOUTUBE_CHANNEL_ID_4170 = "PLZVeULHsgFZg5bmAdxIJgQi_7wzE95ITU" #Mechanical: Fan And HVAC Videos
YOUTUBE_CHANNEL_ID_4171 = "PL0qZzRONiQBJWCDwwzc8weGjUAzkhugI3" #Popular Sink And Drain Videos
YOUTUBE_CHANNEL_ID_4172 = "PLqjSJ7tZBxenjRkx2_40qqy7XMmuOcF3j" #Repairs: Epoxy Flooring Videos
YOUTUBE_CHANNEL_ID_4173 = "PL0BG7YlzszC1Uz5rhqcRJ2XhNg2emgohP" #Repairs: Veneering Video
YOUTUBE_CHANNEL_ID_4174 = "PL5Vuddj4r0Fm2i_xqIe8f93nXVDcRDsn_" #Carpet Cleaning Video
YOUTUBE_CHANNEL_ID_4175 = "" #
YOUTUBE_CHANNEL_ID_4176 = "" #
YOUTUBE_CHANNEL_ID_4177 = "" #
YOUTUBE_CHANNEL_ID_4178 = "" #
YOUTUBE_CHANNEL_ID_4179 = "" #
YOUTUBE_CHANNEL_ID_4180 = "" #
YOUTUBE_CHANNEL_ID_4181 = "" #
YOUTUBE_CHANNEL_ID_4182 = "" #
YOUTUBE_CHANNEL_ID_4183 = "" #
YOUTUBE_CHANNEL_ID_4184 = "" #
YOUTUBE_CHANNEL_ID_4185 = "" #
YOUTUBE_CHANNEL_ID_4186 = "" #
YOUTUBE_CHANNEL_ID_4187 = "" #
YOUTUBE_CHANNEL_ID_4188 = "" #
YOUTUBE_CHANNEL_ID_4189 = "" #
YOUTUBE_CHANNEL_ID_4190 = "" #
YOUTUBE_CHANNEL_ID_4191 = "" #
YOUTUBE_CHANNEL_ID_4192 = "" #
YOUTUBE_CHANNEL_ID_4193 = "" #
YOUTUBE_CHANNEL_ID_4194 = "" #
YOUTUBE_CHANNEL_ID_4195 = "" #
YOUTUBE_CHANNEL_ID_4196 = "" #
YOUTUBE_CHANNEL_ID_4197 = "" #
YOUTUBE_CHANNEL_ID_4198 = "" #
YOUTUBE_CHANNEL_ID_4199 = "" #
YOUTUBE_CHANNEL_ID_4200 = "PLdYrEEm7Js49Mj4sUD4hZpfNN8HIQSpON" #Walter Reeves - Southern Gardening
YOUTUBE_CHANNEL_ID_4201 = "PLZ2SMqWIyysSbT34vtBYkQ6hV0xsOCzl-" #Martha Stewart Gardening Tips
YOUTUBE_CHANNEL_ID_4202 = "PLgI3-4_ax8H83audNVQBaSmn2xW9nrGrd" #Black Gumbo Southern Gardening
YOUTUBE_CHANNEL_ID_4203 = "PLMqSgLFcy5-QPWWakDkwfRUb5eog68NkD" #Gardening With Cody - Codys Lab
YOUTUBE_CHANNEL_ID_4204 = "PL1eicvxnN9grZ9T_Qu0jurUlnu4NqDkZ5" #A - Z Of Gardening Episodes
YOUTUBE_CHANNEL_ID_4205 = "PL4DWqGQoaC_Zg9g7Vp0vRTKtkCafGHGSZ" #Gardeners World Popular Videos
YOUTUBE_CHANNEL_ID_4206 = "PL-Oo0RZFhcPFK8UaM_nD61rPTA4jWqoP2" #Gardening And Kitchen Garden
YOUTUBE_CHANNEL_ID_4207 = "PLI54BTV1KZwRFSyhvx4IcOTr8sbyI6BO3" #Container Gardening Videos
YOUTUBE_CHANNEL_ID_4208 = "PL-Oo0RZFhcPHn1JArgvEzu2BgrqzJNwqg" #Gardening And Raised Bed Gardening
YOUTUBE_CHANNEL_ID_4209 = "PL-Oo0RZFhcPHyEDAkzcpxVoKtqqii-gKA" #Popular Videos - Gardening
YOUTUBE_CHANNEL_ID_4210 = "PLme-1fWBofIzk1kmBXYAZdARpeE-Ad_Im" #How To Build A Greenhouse
YOUTUBE_CHANNEL_ID_4211 = "PLToGke_2f_Zc5muUMfmvYlcDv9I4aqXre" #Greenhouse Gardening
YOUTUBE_CHANNEL_ID_4212 = "PLme-1fWBofIxNWDU5k8q26i-rt8pHOu9e" #DIY Indoor Greenhouse
YOUTUBE_CHANNEL_ID_4213 = "PLEBd5qJNfRYiRhAbMuWcCTj0tWqw_zClB" #Greenhouse Academy Episodes
YOUTUBE_CHANNEL_ID_4214 = "PLn7DW_xovIDmtIvbqRskcDOFz5HihJ2uT" #Greenhouse Automation
YOUTUBE_CHANNEL_ID_4215 = "" #
YOUTUBE_CHANNEL_ID_4216 = "" #
YOUTUBE_CHANNEL_ID_4217 = "" #
YOUTUBE_CHANNEL_ID_4218 = "" #
YOUTUBE_CHANNEL_ID_4219 = "" #
YOUTUBE_CHANNEL_ID_4220 = "" #
YOUTUBE_CHANNEL_ID_4221 = "" #
YOUTUBE_CHANNEL_ID_4222 = "" #
YOUTUBE_CHANNEL_ID_4223 = "" #
YOUTUBE_CHANNEL_ID_4224 = "" #
YOUTUBE_CHANNEL_ID_4225 = "" #
YOUTUBE_CHANNEL_ID_4226 = "" #
YOUTUBE_CHANNEL_ID_4227 = "" #
YOUTUBE_CHANNEL_ID_4228 = "" #
YOUTUBE_CHANNEL_ID_4229 = "" #
YOUTUBE_CHANNEL_ID_4230 = "" #
YOUTUBE_CHANNEL_ID_4231 = "" #
YOUTUBE_CHANNEL_ID_4232 = "" #
YOUTUBE_CHANNEL_ID_4233 = "" #
YOUTUBE_CHANNEL_ID_4234 = "" #
YOUTUBE_CHANNEL_ID_4235 = "" #
YOUTUBE_CHANNEL_ID_4236 = "" #
YOUTUBE_CHANNEL_ID_4237 = "" #
YOUTUBE_CHANNEL_ID_4238 = "" #
YOUTUBE_CHANNEL_ID_4239 = "" #
YOUTUBE_CHANNEL_ID_4240 = "" #
YOUTUBE_CHANNEL_ID_4241 = "" #
YOUTUBE_CHANNEL_ID_4242 = "" #
YOUTUBE_CHANNEL_ID_4243 = "" #
YOUTUBE_CHANNEL_ID_4244 = "" #
YOUTUBE_CHANNEL_ID_4245 = "" #
YOUTUBE_CHANNEL_ID_4246 = "" #
YOUTUBE_CHANNEL_ID_4247 = "" #
YOUTUBE_CHANNEL_ID_4248 = "" #
YOUTUBE_CHANNEL_ID_4249 = "" #
YOUTUBE_CHANNEL_ID_4250 = "PLWMk5uyu_r4yRsdKgWtB7pKqATdRSzvxV" #Popular Electronics And TV Video
YOUTUBE_CHANNEL_ID_4251 = "PLNk11UwAe2jdKj8RQ5_XxYEbXqZaW-3og" #Fix It: Computer Repairs
YOUTUBE_CHANNEL_ID_4252 = "PLlHYXngG1dcOVLV2l8hfJOEuK_8cwx--L" #IT Knowledge Base: Computer
YOUTUBE_CHANNEL_ID_4253 = "PLXH0-u8bUsluROGGaADQ8u070WrPt1JWC" #Electronics: How To Make
YOUTUBE_CHANNEL_ID_4254 = "PLbt5yGBXEvI1MnRy4Lt8TTNGgE_epJ_-q" #Solar, Batteries, Inverters, Ect
YOUTUBE_CHANNEL_ID_4255 = "PL4k9rZJhVcJF_lvuTAPPH57PBNyV9qQZM" #Power Bank Battery And Solar
YOUTUBE_CHANNEL_ID_4256 = "PLbRsB6WOs7FvOedxshdfNMgbW1QaT2GBe" #Electronics: Tablet Repair
YOUTUBE_CHANNEL_ID_4257 = "PLaF2JrJEd5VRkahbnunOezLqI6lbzHvqb" #Electronics Repair School
YOUTUBE_CHANNEL_ID_4258 = "PLB8F7DF0E2DE523AD"                 #Kitchen Table Electronics Repair
YOUTUBE_CHANNEL_ID_4259 = "PLbieLTSjLNFihpdQgqJPSPIoy6AHWqHs3" #How To Fix Electronics: TVs And More
YOUTUBE_CHANNEL_ID_4260 = "PLO37BzxQcqmyuF_VzI1KoliOBWJ8gD4L_" #Electronics Repair Videos
YOUTUBE_CHANNEL_ID_4261 = "PLk7y689ZbjjNTaGNMnycoAwqDdSaXtZmu" #Windows 10/8/7 Problems And Fixes
YOUTUBE_CHANNEL_ID_4262 = "PLopY6Rpyvor-fPOcqQj6vvBcPjR7I43cC" #Computer Tips And Tricks 2019
YOUTUBE_CHANNEL_ID_4263 = "PLo-ZP0EsY6w2DfoSXgeO8X_NdIGqrwMdG" #LCD, LED TV Repair Training
YOUTUBE_CHANNEL_ID_4264 = "PLMbs_EucXuhKVbeMAFZ05vFbKzkdU5myY" #Electronics: TV Repair
YOUTUBE_CHANNEL_ID_4265 = "PL0sLWmrl8QhytCk1kckaMMO5u2Am8UXXG" #Vizio TV Repairs and Tips
YOUTUBE_CHANNEL_ID_4266 = "PLB94A18896AB0C27F"                 #Easy Most Common TV Repairs
YOUTUBE_CHANNEL_ID_4267 = "PLIzXby9EnurGuLl3F6DYIEJqseJNN9zAd" #Android TV Box Repair
YOUTUBE_CHANNEL_ID_4268 = "PLhpcdAXI9iPOqbWZPitlkkCKUex5qAqG1" #Android TV Box: MXQ Repair
YOUTUBE_CHANNEL_ID_4269 = "PL-Ar8N0xRszo96OQMFMb3fzHnqeHTWimq" #Android: TV Box Repair
YOUTUBE_CHANNEL_ID_4270 = "PLy7sFv96r0et5gW0PHLH71KM3V17tNkFW" #Android Box Fix
YOUTUBE_CHANNEL_ID_4271 = "PL4yOmK4BlraQYa9wES2ANM5AgcUOfQQ56" #Repairing Electronics
YOUTUBE_CHANNEL_ID_4272 = "PL762ECFD2F81607C1"                 #Xbox Repair Manual
YOUTUBE_CHANNEL_ID_4273 = "PL1B85A61A6B28510F"                 #Xbox 360 Repair Video
YOUTUBE_CHANNEL_ID_4274 = "" #
YOUTUBE_CHANNEL_ID_4275 = "" #
YOUTUBE_CHANNEL_ID_4276 = "" #
YOUTUBE_CHANNEL_ID_4277 = "" #
YOUTUBE_CHANNEL_ID_4278 = "" #
YOUTUBE_CHANNEL_ID_4279 = "" #
YOUTUBE_CHANNEL_ID_4280 = "" #
YOUTUBE_CHANNEL_ID_4281 = "" #
YOUTUBE_CHANNEL_ID_4282 = "" #
YOUTUBE_CHANNEL_ID_4283 = "" #
YOUTUBE_CHANNEL_ID_4284 = "" #
YOUTUBE_CHANNEL_ID_4285 = "" #
YOUTUBE_CHANNEL_ID_4286 = "" #
YOUTUBE_CHANNEL_ID_4287 = "" #
YOUTUBE_CHANNEL_ID_4288 = "" #
YOUTUBE_CHANNEL_ID_4289 = "" #
YOUTUBE_CHANNEL_ID_4290 = "" #
YOUTUBE_CHANNEL_ID_4291 = "" #
YOUTUBE_CHANNEL_ID_4292 = "" #
YOUTUBE_CHANNEL_ID_4293 = "" #
YOUTUBE_CHANNEL_ID_4294 = "" #
YOUTUBE_CHANNEL_ID_4295 = "" #
YOUTUBE_CHANNEL_ID_4296 = "" #
YOUTUBE_CHANNEL_ID_4297 = "" #
YOUTUBE_CHANNEL_ID_4298 = "" #
YOUTUBE_CHANNEL_ID_4299 = "" #
YOUTUBE_CHANNEL_ID_4300 = "PLicoQ907WfsCPwWI49ekidkJhDImPQWnQ" #Automotive Troubleshoot And Repair
YOUTUBE_CHANNEL_ID_4301 = "PLCw3n037qEdfmBvdwhji8pgJb1QZM36TN" #Automobile Detailing Video
YOUTUBE_CHANNEL_ID_4302 = "PLeEvvHvFl8uzuJothYujoXlUtcj_ynjic" #Ford Repair Videos By Astral Auto
YOUTUBE_CHANNEL_ID_4303 = "PLY9mgCQatPBxbLKu8KegOq9Lo8QUGJSQi" #Useful Car Repair Tips
YOUTUBE_CHANNEL_ID_4304 = "PL5__U-kYrFIg5OEfvtnw0Cp1u8pqe1DMN" #Automotive Full Course
YOUTUBE_CHANNEL_ID_4305 = "PLQM_1cDn2dhTWAWma_ECx-Usiq8kgpPnX" #Car Repair Videos
YOUTUBE_CHANNEL_ID_4306 = "PLj62kp2F8euJ-0X5S3JkYIW9YDZGASWm7" #Popular Auto Repair And Maintenance
YOUTUBE_CHANNEL_ID_4307 = "PLa1nGolaBjZm01CU3QsuXJSGY1IHOaw_S" #Automobile Repair Videos
YOUTUBE_CHANNEL_ID_4308 = "PLtRKk64pu2wpGsswJ3qpXOPf_ZLUe3OYU" #Precision Auto Dent Repair
YOUTUBE_CHANNEL_ID_4309 = "PL5IiNkEirUmKXNeOnAU6b8jHH_rUz0D2e" #Popular Videos: Fuel Injection And Repair
YOUTUBE_CHANNEL_ID_4310 = "PLhlgwO1W75jtC6RCq9IzbfQL1LQ84NFUy" #DIY General Auto Repair Videos
YOUTUBE_CHANNEL_ID_4311 = "PL6jUeULIkvBmgC9wz1oRSbh1wkwX2TUBr" #DIY Car Repair Videos
YOUTUBE_CHANNEL_ID_4312 = "PLytBWlNJVEIWVHNA55mwsqV03VOrNZ41r" #Workshop Auto Repair Manual
YOUTUBE_CHANNEL_ID_4313 = "PLPcvsD3EO8wh-X1v6hh-YeIccA_A1B_s4" #Car Under Chassis Repair
YOUTUBE_CHANNEL_ID_4314 = "PLIvoMh3chOJ-IxzVcvJVQVhyOKdlObUdy" #Auto Restoration And Preservation
YOUTUBE_CHANNEL_ID_4315 = "PLWep5LzT0sxk10n9fThNMID2tdfVRg-yC" #VW Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4316 = "PLeEvvHvFl8uy1CIJtmj6QXQyNidAUTbh6" #Chevy Repair Videos By Astral Auto
YOUTUBE_CHANNEL_ID_4317 = "PLWep5LzT0sxnGypBzmtCr5_BSMmb5ZgvB" #Hyundai Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4318 = "PLWep5LzT0sxmGaE_D-PugagtaTjGevAG9" #BMW 3 E36 Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4319 = "PLeEvvHvFl8uwAi_GZBfUyUKrANoZsq7g0" #Cadillac Repair Video By Astral Auto
YOUTUBE_CHANNEL_ID_4320 = "PLZkZmTslnhkKfImDjGBNF4sKYl28B5wBZ" #Mercedes Auto Repairs
YOUTUBE_CHANNEL_ID_4321 = "PLgQEtJpBHB2Xm64j6bS-qD1zMfH7UMh7Z" #Pontiac Grand Am GT Auto Repair
YOUTUBE_CHANNEL_ID_4322 = "PLWep5LzT0sxn5tAU9gHJS3pRFgtwnDsVo" #Audi Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4323 = "PLY9mgCQatPByG5gbKTDXdUTKpcOqOHCi5" #Car Battery Restore And Maintenance
YOUTUBE_CHANNEL_ID_4324 = "PLY9mgCQatPBxOCYelfyo23kiYIlyoPSjg" #How To Analyze Car Problems
YOUTUBE_CHANNEL_ID_4325 = "PLoPyuXRd3PNgPEk1Rqkwvt6xe-rgLlJJW" #Repair Auto Electrical Shorts
YOUTUBE_CHANNEL_ID_4326 = "PLeEvvHvFl8uxKUbDyWySnl7808GkHqJz9" #Toyota Repair Video By Astral Auto
YOUTUBE_CHANNEL_ID_4327 = "PLeEvvHvFl8uygKKm9v4DNO6LTuazCtzRG" #Chrysler Repair Video By Astral Auto
YOUTUBE_CHANNEL_ID_4328 = "PLeEvvHvFl8uxODbmDe9jQ2b7WCB8eNjgr" #Honda Repair Videos By Astral Auto
YOUTUBE_CHANNEL_ID_4329 = "PLeEvvHvFl8uy6VF2NxMDjScOszGgyUPX7" #Nissan Repair Videos By Astral Auto
YOUTUBE_CHANNEL_ID_4330 = "PLeEvvHvFl8uyWoIin6zxVTTCU3MObNGiM" #BMW Repair Videos By Astral Auto
YOUTUBE_CHANNEL_ID_4331 = "PLeEvvHvFl8uxYGkNGlsmQWfJyBptObNjE" #Kia Repair Videos By Astral Auto
YOUTUBE_CHANNEL_ID_4332 = "PLeEvvHvFl8uyLfUP95H1qA8AdjqtdjtFP" #Jeep Repair Videos By Astral Auto
YOUTUBE_CHANNEL_ID_4333 = "PLeEvvHvFl8uzA1YwOme16ogQK5kgeabdZ" #Dodge Repair Videos By Astral Auto
YOUTUBE_CHANNEL_ID_4334 = "PLqJG4ZyPIF6MgWID9RAvyzkdLQF1lnrmt" #BMW 3 Series (E46) Repair Videos
YOUTUBE_CHANNEL_ID_4335 = "PLuyRKAcXjUiFJkDyysk3Rnc2SH9gCjdG1" #BMW E46 3-Series Repair Videos
YOUTUBE_CHANNEL_ID_4336 = "PLWep5LzT0sxns3AqYnqRcpPvavO7ZyACz" #Fiat Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4337 = "PLWep5LzT0sxky9jB9WYo8WXYuzAzlsHEv" #Volvo Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4338 = "PLWep5LzT0sxnkEog3fo5JASk1nLWhZZV3" #Nissan Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4339 = "PLWep5LzT0sxkzGFDibj8Js-D_BlOzV5Do" #BMW Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4340 = "PLWep5LzT0sxn9o1yA5vdSAmSlj45uLf11" #Toyota Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4341 = "PLWep5LzT0sxl8ih7DIhLfdUfvnLlZTcBM" #Mercedes-Benz Car Repair Tutorial
YOUTUBE_CHANNEL_ID_4342 = "PLLrqujg3_D00VnZ7ex3yKWA_y1gTCNI_f" #Jeep Repair Videos
YOUTUBE_CHANNEL_ID_4343 = "PLv4wHe3V4Rqkr2O1rCJYOTt3dQqPM150z" #How To Repair Car Headliner
YOUTUBE_CHANNEL_ID_4344 = "PLAoWgZnFWzsHkEX_8UmE3ASD6stnRJTt7" #Volvo Car Repair Videos
YOUTUBE_CHANNEL_ID_4345 = "PLjVSLU9wgBvvJsnoOlZbegHrjbTgddD84" #Toyota Camry 2009 Repair Videos
YOUTUBE_CHANNEL_ID_4346 = "PLmofIXcQVz067Yadd8oUlLG9yFX7hVM-d" #PT Cruiser Repair Videos
YOUTUBE_CHANNEL_ID_4347 = "" #
YOUTUBE_CHANNEL_ID_4348 = "" #
YOUTUBE_CHANNEL_ID_4349 = "" #
YOUTUBE_CHANNEL_ID_4360 = "PLB1zH01p3No-BvzflClsLb_qd05UYQnRU" #Musical Instrument Repair: Guitars
YOUTUBE_CHANNEL_ID_4361 = "PLSFLd5frIPrXCAWhseyUP1mYGSATROZr2" #Stratacaster And Telecaster Guitar
YOUTUBE_CHANNEL_ID_4362 = "PLQcWgafHVn2CWsILYWma2ECejlmyVYjDJ" #Amp Repairs Electrics
YOUTUBE_CHANNEL_ID_4363 = "PL1PqqIj0rGhPT-ajqLNrV21MfkpusKOY4" #Stew-Mac Guitar Repair
YOUTUBE_CHANNEL_ID_4364 = "PL833B580B4C1BE556"                 #Guitar Repair Videos
YOUTUBE_CHANNEL_ID_4365 = "PLDf_edljRHgZmo6HbxiupZJhjM4JSLR3u" #Guitar Finish Repairs
YOUTUBE_CHANNEL_ID_4366 = "PLXVAjY43wv_2U7u1YVs7-ZDFZwRG9UPz9" #More Guitar Repairs
YOUTUBE_CHANNEL_ID_4367 = "PLTsGAg_fo_Krr68u4rl98DNis4X6un38u" #Guitar Amp Repair Video
YOUTUBE_CHANNEL_ID_4368 = "PLZdMD1HYcbhlE6QI511Icu1dRC3bAMh6B" #More Guitar Amp Repair
YOUTUBE_CHANNEL_ID_4369 = "PLVB1Qcr3Vb7fzShE6lpc_07Rh71v9mFve" #Amp Repair And Troubleshooting
YOUTUBE_CHANNEL_ID_4370 = "PLYPNuwvDCq5P1HGaiGFG_X5GqlOWnRtfb" #Tube Amp Repair Videos
YOUTUBE_CHANNEL_ID_4371 = "PLK_zQ6_j4TF0g6isHiGyDoLcl-yloMhbu" #Guitar Tube Amplifier Repair
YOUTUBE_CHANNEL_ID_4372 = "PLt6_M1LxfJZswUU1DABQsVcdczJqgK7tg" #Amp Repair Videos
YOUTUBE_CHANNEL_ID_4373 = "PLqQGTv50yTPCgQhXzZRStkyxugopiCEgc" #Speaker Repair Videos
YOUTUBE_CHANNEL_ID_4374 = "PL9dUgqJngZPsVEkRXs1SfIsYQu4wT1rc7" #Guitar Amps And Repair
YOUTUBE_CHANNEL_ID_4375 = "PLOGMllrXXzJOJeLA1E2rnd3wZRsWukOo3" #Drum Repair Stuff
YOUTUBE_CHANNEL_ID_4376 = "PL652Zqf_WkoRs672pwPll30X1SFxHv46T" #Drum Repair And Build
YOUTUBE_CHANNEL_ID_4377 = "PL2pZVB9czfbDp_u5C0w0DwRlBbkKcNhtw" #Drum Repair Videos
YOUTUBE_CHANNEL_ID_4378 = "PLirut8Pk0R2tLTO_ftOcO7gDJ3WjLF-TG" #Saxophone Repair Videos
YOUTUBE_CHANNEL_ID_4379 = "PLbHaTWK4lthLdybVPteFqEYt-z9FAhne4" #Musical Instrument Repair
YOUTUBE_CHANNEL_ID_4380 = "PLwRnNUXb3nCEwzj9T4qaNnvjG-G9AENtw" #Musical Instrument: Flute Repair
YOUTUBE_CHANNEL_ID_4381 = "PLs7o13HrLfKve_wibE-pSiDa-qqrChHpL" #Musical Instrument: Clarinet Repair
YOUTUBE_CHANNEL_ID_4382 = "PL7Gj9-WGYrmpWX1k3ejKOBnNJPUVdSzpb" #Band Instrument Repair
YOUTUBE_CHANNEL_ID_4383 = "PLIP4IrJ-yGZGi_r4S_1StugRitq48Oa9N" #Musical Instrument: Trumpet Repair
YOUTUBE_CHANNEL_ID_4384 = "" #
YOUTUBE_CHANNEL_ID_4385 = "" #
YOUTUBE_CHANNEL_ID_4386 = "" #
YOUTUBE_CHANNEL_ID_4387 = "" #
YOUTUBE_CHANNEL_ID_4388 = "" #
YOUTUBE_CHANNEL_ID_4389 = "" #
YOUTUBE_CHANNEL_ID_4390 = "" #
YOUTUBE_CHANNEL_ID_4391 = "" #
YOUTUBE_CHANNEL_ID_4392 = "" #
YOUTUBE_CHANNEL_ID_4393 = "" #
YOUTUBE_CHANNEL_ID_4394 = "" #
YOUTUBE_CHANNEL_ID_4395 = "" #
YOUTUBE_CHANNEL_ID_4396 = "" #
YOUTUBE_CHANNEL_ID_4397 = "" #
YOUTUBE_CHANNEL_ID_4398 = "" #
YOUTUBE_CHANNEL_ID_4399 = "" #
YOUTUBE_CHANNEL_ID_4400 = "" #
YOUTUBE_CHANNEL_ID_4401 = "" #
YOUTUBE_CHANNEL_ID_4402 = "" #
YOUTUBE_CHANNEL_ID_4403 = "" #
YOUTUBE_CHANNEL_ID_4404 = "" #
YOUTUBE_CHANNEL_ID_4405 = "" #
YOUTUBE_CHANNEL_ID_4406 = "" #
YOUTUBE_CHANNEL_ID_4407 = "" #
YOUTUBE_CHANNEL_ID_4408 = "" #
YOUTUBE_CHANNEL_ID_4409 = "" #
YOUTUBE_CHANNEL_ID_4410 = "" #
YOUTUBE_CHANNEL_ID_4400 = "" #
YOUTUBE_CHANNEL_ID_4401 = "" #
YOUTUBE_CHANNEL_ID_4402 = "" #
YOUTUBE_CHANNEL_ID_4403 = "" #
YOUTUBE_CHANNEL_ID_4404 = "" #
YOUTUBE_CHANNEL_ID_4405 = "" #
YOUTUBE_CHANNEL_ID_4406 = "" #
YOUTUBE_CHANNEL_ID_4407 = "" #
YOUTUBE_CHANNEL_ID_4408 = "" #
YOUTUBE_CHANNEL_ID_4409 = "" #
YOUTUBE_CHANNEL_ID_4410 = "" #
YOUTUBE_CHANNEL_ID_4410 = "" #
YOUTUBE_CHANNEL_ID_4411 = "PLjZWz2vV4K5KhoyDpJ7UUh2VxXQWLiViU" #Pets: Cats And Dogs Video
YOUTUBE_CHANNEL_ID_4412 = "PLdHGnBlTh0xF9lBSfJaekbudtYUYX3jcl" #Pets: Ask A Pet Vet
YOUTUBE_CHANNEL_ID_4413 = "PL_PlO6WnLPmcsp3uFuKJLLezsX40t-eTZ" #Pets: Dog Behavior
YOUTUBE_CHANNEL_ID_4414 = "PL61GiCCEEiP9T3Oh-XWlk9Z5kHomFhjaN" #Pets: Video And Info Mix
YOUTUBE_CHANNEL_ID_4415 = "PLKWwEJm36m7q9uc02VaAFs_BGYRbED-nF" #Pets: Guinea Pigs
YOUTUBE_CHANNEL_ID_4416 = "PLeM0g-KmHardqezcKd5EpWruuv-VAuUcx" #Pets Dog Care Video
YOUTUBE_CHANNEL_ID_4417 = "PLCzXTsIyQSO1sJPeS0qIJtc9vjYhmdNoq" #Pets: Dog Care
YOUTUBE_CHANNEL_ID_4418 = "PL0609051E495BD014"                 #Pets: Dog Training
YOUTUBE_CHANNEL_ID_4419 = "PL2onuJ8dkqmUVo2NeAvGpZxQwrD7IUkM_" #Pets: Puppy Training
YOUTUBE_CHANNEL_ID_4420 = "PLnnWiXUypldM_lxri74kBuh6gtlkoSKbA" #Pets: Parrots And Cockatiels
YOUTUBE_CHANNEL_ID_4421 = "PL3kAlm400HwTN7isyXk6og0mpn-l1rj8Z" #Pets: Cat Fun, Info, And More
YOUTUBE_CHANNEL_ID_4422 = "PLBe5QTZXE7qE7F8XvDHpxEwDkYn8Zz-3a" #Pets: Cat Info And Care
YOUTUBE_CHANNEL_ID_4423 = "PL910D6FDB89672E90"                 #Pets: Pets: Kitten Care
YOUTUBE_CHANNEL_ID_4424 = "PLyNij-VrzAUAW3KgqQJg3c7HcRJrOoOeq" #Pets: Cat Breeds
YOUTUBE_CHANNEL_ID_4425 = "PLLALQuK1NDrjnjAFAcbvUg4tmT_jxnjTU" #How To Care For Pet Rabbits
YOUTUBE_CHANNEL_ID_4426 = "PLLALQuK1NDrjv-0JHcOS-1ECjzXrSadW0" #How To Take Care Of Aquariums
YOUTUBE_CHANNEL_ID_4427 = "PLTVpsxamkX9BqZ-3nrR6HVGfWAya9GNDY" #Pets: Bird And Fish Care
YOUTUBE_CHANNEL_ID_4428 = "PLKYzeCvCW6M3vBi4kCsz3bgeQCh06Eo8Y" #Pets: Fish Care
YOUTUBE_CHANNEL_ID_4429 = "PLK6p5h-NYEHSuOm7iFcxw5Q2H11-1SaMM" #Pets: Goldfish Care
YOUTUBE_CHANNEL_ID_4430 = "PLWu6M5u0Vbc7tvAydNaxb8yW9DrJJdMYP" #Pets: Cockatiel Care
YOUTUBE_CHANNEL_ID_4431 = "PLZGqvW_9B1FpG_ePs1tF5eB0qveOrZ-IE" #Pet Dogs: Poodle Care
YOUTUBE_CHANNEL_ID_4432 = "PLNhWjG4VxAmhvoEkUfFsv6LKhLqXcGn-P" #Pets: Turtle Care 101
YOUTUBE_CHANNEL_ID_4433 = "PL044B75EC96839EA4"                 #Pet Cats: Persian Care
YOUTUBE_CHANNEL_ID_4434 = "PLUTUyiYi2YPsD1yjow-TEB0pWahLVpok-" #Pets: Fish Care And Bettas
YOUTUBE_CHANNEL_ID_4435 = "PLy4qQ9gZEUShaEsuoK-xqNVzsDytBo-EZ" #Turtle Care: DOs And DONTs
YOUTUBE_CHANNEL_ID_4436 = "PLFhP5ULP471H9dLHi24ZvO5Uf8wy2V41K" #Pets: DIY Saltwater Tank
YOUTUBE_CHANNEL_ID_4437 = "PL5LFn18nrLF_5wb5_uhlVdABUJcaNCx0Z" #Natural Horse Hoof Care 
YOUTUBE_CHANNEL_ID_4438 = "PLSX7fm7VayRWNtBPF3ikijNvL6hbU2EKH" #Pets: Taking Care Of Horses
YOUTUBE_CHANNEL_ID_4439 = "PLLMYgJzwNMbvTWf-hXJf1VI9ishjoQP2Q" #Pets: Elles Reptiles
YOUTUBE_CHANNEL_ID_4440 = "PLIjDGjgIbotxFdQiKxvG_o8RFBho0eWWS" #Pets: Dog Training
YOUTUBE_CHANNEL_ID_4441 = "PL7Qt42ozIdJlP84imourlcEjToiw7t8bQ" #Pets: Concrete Dog Kennels
YOUTUBE_CHANNEL_ID_4442 = "PLljN9yxHua4wiludSNha1ofNyZwnZPk2h" #Pets: Exotics Lair Library
YOUTUBE_CHANNEL_ID_4443 = "PLit00rNoUxibFOihyNAes_R1fxL3KD3wo" #Pets: Dog Grooming
YOUTUBE_CHANNEL_ID_4444 = "PLkweNOC3mBJjcWk64cQ51x46wGRCGEutg" #Pets: Exotic Lair
YOUTUBE_CHANNEL_ID_4445 = "PLKbH9esyd2GweIPVWcy4_yGJtXwf3k3s6" #Pets: Pet Care Mix
YOUTUBE_CHANNEL_ID_4446 = "PLa6zRh4N6NoZqGnijXfQYCY0hQHyZlQxb" #Pets: Lizards And Frogs
YOUTUBE_CHANNEL_ID_4447 = "PL_j3xzBytgjyAfkP1cK9bTJtg-4Djl4K5" #Pets: Docs And Shorts
YOUTUBE_CHANNEL_ID_4448 = "PLjxFELVZJB2U5iLNIbJGb2hSDwsk_q5e2" #Hairless Cats And Dogs
YOUTUBE_CHANNEL_ID_4449 = "PLT7OmSiCi1CT1AH7OwBeC3rN6l7yYEotb" #Pets: Cat Care
YOUTUBE_CHANNEL_ID_4450 = "PLDhmYgld1im4S4QVvWfGWHCME7SmlpZ6i" #Pets: Cat Documentary
	
##@route(mode='appliance')
def Appliance():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Appliance Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4001+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Refrigerator Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4002+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]GE Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4003+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Dryer, Dishwasher, And More[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4004+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Domestic Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4005+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Maytag Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4006+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]More Refrigerator Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4007+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Refrigerator, Icemaker, Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4008+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Samsung Refrigerator Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4009+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Appliance Repair 101[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4010+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Appliance - Refrigerators 101[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4011+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Frigidaire Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4012+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Appliance Troubleshoot And Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4013+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Appliance Repair Two[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4014+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Repairs - Appliances[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4015+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Bosch Appliance And More[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4016+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Home Appliance Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4017+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Easy Miele Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4018+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Miele Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4019+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]More Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4020+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Bill Newberry Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4021+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Kenmore - Whirlpool Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4022+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]GE Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4023+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]GE Side By Side Frigerator[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4024+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular GE Dishwasher Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4025+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular GE Clothes Dryer Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4026+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular GE Stove Repair Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4027+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular GE Icemaker Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4028+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular GE Microwave Repair Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4029+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular GE Clothes Washer Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4030+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Hotpoint And Kenmore Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4031+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Maytag Clothes Washer Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4032+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Window Air Conditioner And Appliance[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4033+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]How To Repair Air Conditioners[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4034+"/", folder=True,
		icon=mediapath+"diy_appliance.png", fanart=fanart)
		
	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'diyfix.png', fanart)

##@route(mode='gadgets')
def Gadgets():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Small Appliance And Tool Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4050+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Home Appliance Repair And Service[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4051+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Appliance Repair: Keurig And More[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4052+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Coffee Pot Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4053+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Kitchenaid Mixer Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4054+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Delonghi Coffee Maker And More[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4055+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Old Radio Repair And More[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4056+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Singer Sewing Machine Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4057+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Husqvarna Sewing Machine Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4058+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Sewing Machine Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4059+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]More Sewing Machine Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4060+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Mixer and Blender Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4061+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Dremel Tool Repair And Tips[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4062+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Kitchen Blender Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4063+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Small Appliance Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4064+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Microwave Oven Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4065+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Hoover Vacuum Cleaner Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4066+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Vacuum Cleaner Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4067+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Electrolux vacuum cleaner repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4068+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Repairs: Vacuum Cleaners[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4069+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Shop Vac Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4070+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Bissell And Vacuum Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4071+"/", folder=True,
		icon=mediapath+"diy_gadgets.png", fanart=fanart)

	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'diyfix.png', fanart)

#@route(mode='diy_musical')
def DIY_Musical():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Musical Instrument Repair: Guitars[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4360+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Stratacaster And Telecaster Guitar[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4361+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Amp Repairs Electrics[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4362+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Stew-Mac Guitar Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4363+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Guitar Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4364+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Guitar Finish Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4365+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]More Guitar Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4366+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Guitar Amp Repair Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4367+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]More Guitar Amp Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4368+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Amp Repair And Troubleshooting[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4369+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Tube Amp Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4370+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Guitar Tube Amplifier Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4371+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Amp Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4372+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Speaker Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4373+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Guitar Amps And Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4374+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Drum Repair Stuff[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4375+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Drum Repair And Build[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4376+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Drum Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4377+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Saxophone Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4378+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Musical Instrument Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4379+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Musical Instrument: Flute Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4380+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Musical Instrument: Clarinet Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4381+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Band Instrument Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4382+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Musical Instrument: Trumpet Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4383+"/", folder=True,
		icon=mediapath+"diy_musical.png", fanart=fanart)

	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'diyfix.png', fanart)

#@route(mode='home')
def Home():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Plumbing Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4150+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Fixing Things Around The Home[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4151+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]DIY Home Maintenance[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4152+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Fan Electric Motor Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4153+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Home Repair: Plumbing[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4154+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Home Repair And Bathtubs Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4155+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Mobile Home Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4156+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]HVAC Training Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4157+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Electrical Wiring Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4158+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]How To Test AC Compressors[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4159+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Home Improvement And Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4160+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Mosaic And Countertop[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4161+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Electricity: Troubleshooting[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4162+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Stainless Steel And Sink[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4163+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Home Additions, Renovations, And More[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4164+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Home Repair: Kitchen Cabinets[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4165+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Handyman: Home Howto Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4166+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Plumbing - Boiler Basics[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4167+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Window Washing And Screen Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4168+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Repairs: Drywall Tips[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4169+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Mechanical: Fan And HVAC Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4170+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Sink And Drain Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4171+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Repairs: Epoxy Flooring Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4172+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Repairs: Veneering Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4173+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Carpet Cleaning Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4174+"/", folder=True,
		icon=mediapath+"diy_home.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'diyfix.png', fanart)

#@route(mode='electronics')
def Electronics():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Electronics And TV Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4250+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Fix It: Computer Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4251+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]IT Knowledge Base: Computer[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4252+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Electronics: How To Make[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4253+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Solar, Batteries, Inverters, Ect[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4254+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Power Bank Battery And Solar[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4255+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Electronics: Tablet Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4256+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Electronics Repair School[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4257+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Kitchen Table Electronics Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4258+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]How To Fix Electronics: TVs And More[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4259+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Electronics Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4260+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Windows 10/8/7 Problems And Fixes[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4261+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Computer Tips And Tricks 2019[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4262+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]LCD, LED TV Repair Training[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4263+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Electronics: TV Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4264+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Vizio TV Repairs and Tips[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4265+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Easy Most Common TV Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4266+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Android TV Box Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4267+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Android TV Box: MXQ Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4268+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Android: TV Box Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4269+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Android Box Fix[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4270+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Repairing Electronics[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4271+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Xbox Repair Manual[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4272+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Xbox 360 Repair Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4273+"/", folder=True,
		icon=mediapath+"diy_electronics.png", fanart=fanart)

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'diyfix.png', fanart)

#@route(mode='lawn')
def Lawn():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Small Engine Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4100+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Lawnmower Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4101+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Repairs: Lawnmowers[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4102+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Weed Eater, Trimmers Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4103+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Briggs And Stratton And Lawn Mower[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4104+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]String Trimmer And Leaf Blower Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4105+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Stihl MS170: Chainsaws[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4106+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Popular Chainsaw Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4107+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Poulain Pro Repair Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4108+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Craftsman Riding Mower Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4109+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Lawn Mower Repair Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4110+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Troy-Built Bronco Tractor Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4111+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Riding Mower Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4112+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]John Deere Riding Mower Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4113+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]John Deere Repairs: Riding Mower[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4114+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Husqvarna Riding Mower Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4115+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Murray Mower Repair Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4116+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Carburetor Repair Video Series[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4117+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Lawn Mowers And MTD Products[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4118+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]2-Cycle Engine Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4119+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Carburetor Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4120+"/", folder=True,
		icon=mediapath+"diy_lawn.png", fanart=fanart)
		
	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'diyfix.png', fanart)

#@route(mode='garden')
def Garden():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Walter Reeves - Southern Gardening[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4200+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Martha Stewart Gardening Tips[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4201+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Black Gumbo Southern Gardening[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4202+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Gardening With Cody - Codys Lab[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4203+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]A - Z Of Gardening Episodes[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4204+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Gardeners World Popular Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4205+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Gardening And Kitchen Garden[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4206+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Container Gardening Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4207+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Gardening And Raised Bed Gardening[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4208+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Popular Videos - Gardening[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4209+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]How To Build A Greenhouse[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4210+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Greenhouse Gardening[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4211+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]DIY Indoor Greenhouse[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4212+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Greenhouse Academy Episodes[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4213+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Greenhouse Automation[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4214+"/", folder=True,
		icon=mediapath+"diy_garden.png", fanart=fanart)
		
	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'diyfix.png', fanart)

#@route(mode='pets')
def Pets():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Cats And Dogs Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4411+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Ask A Pet Vet[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4412+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Dog Behavior[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4413+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Video And Info Mix[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4414+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Guinea Pigs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4415+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets Dog Care Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4416+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Dog Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4417+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Dog Training[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4418+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Puppy Training[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4419+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Parrots And Cockatiels[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4420+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Cat Fun, Info, And More[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4421+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Cat Info And Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4422+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Kitten Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4423+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Cat Breeds[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4424+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]How To Care For Pet Rabbits[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4425+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]How To Take Care Of Aquariums[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4426+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Bird And Fish Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4427+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Fish Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4428+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Goldfish Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4429+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Pets: Cockatiel Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4430+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Pet Dogs: Poodle Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4431+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Pets: Turtle Care 101[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4432+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Pet Cats: Persian Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4433+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Pets: Fish Care And Bettas[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4434+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Turtle Care: DOs And DONTs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4435+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Pets: DIY Saltwater Tank[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4436+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Natural Horse Hoof Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4437+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Taking Care Of Horses[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4438+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Elles Reptiles[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4439+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Dog Training[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4440+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Pets: Concrete Dog Kennels[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4441+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Pets: Exotics Lair Library[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4442+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Pets: Dog Grooming[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4443+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)		
		
	Add_Dir(
		name="[COLOR white][B]Pets: Exotic Lair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4444+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Pets: Pet Care Mix[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4445+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Pets: Lizards And Frogs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4446+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Universe Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4447+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Hairless Cats And Dogs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4448+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Cat Care[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4449+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Pets: Cat Documentary[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4450+"/", folder=True,
		icon=mediapath+"diy_pets.png", fanart=fanart)
		
	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'diyfix.png', fanart)

#@route(mode='auto')
def Auto():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)

	Add_Dir(
		name="[COLOR white][B]Automotive Troubleshoot And Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4300+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
	
	Add_Dir(
		name="[COLOR white][B]Automobile Detailing Video[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4301+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Ford Repair Videos By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4302+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Useful Car Repair Tips[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4303+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Automotive Full Course[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4304+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Car Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4305+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Auto Repair And Maintenance[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4306+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Automobile Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4307+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Precision Auto Dent Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4308+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Popular Videos: Fuel Injection And Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4309+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]DIY General Auto Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4310+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
	
	Add_Dir(
		name="[COLOR white][B]DIY Car Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4311+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Workshop Auto Repair Manual[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4312+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Car Under Chassis Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4313+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Auto Restoration And Preservation[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4314+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]VW Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4315+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Chevy Repair Videos By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4316+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Hyundai Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4317+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]BMW 3 E36 Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4318+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Cadillac Repair Video By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4319+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Mercedes Auto Repairs[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4320+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
	
	Add_Dir(
		name="[COLOR white][B]Pontiac Grand Am GT Auto Repair[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4321+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Audi Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4322+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Car Battery Restore And Maintenance[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4323+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]How To Analyze Car Problems[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4324+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Repair Auto Electrical Shorts[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4325+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Toyota Repair Video By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4326+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Chrysler Repair Video By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4327+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Honda Repair Videos By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4328+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Nissan Repair Videos By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4329+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]BMW Repair Videos By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4330+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
	
	Add_Dir(
		name="[COLOR white][B]Kia Repair Videos By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4331+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Jeep Repair Videos By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4332+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Dodge Repair Videos By Astral Auto[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4333+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]BMW 3 Series (E46) Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4334+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]BMW E46 3-Series Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4335+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Fiat Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4336+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Volvo Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4337+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Nissan Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4338+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]BMW Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4339+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Toyota Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4340+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
	
	Add_Dir(
		name="[COLOR white][B]Mercedes-Benz Car Repair Tutorial[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4341+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)
		
	Add_Dir(
		name="[COLOR white][B]Jeep Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4342+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]How To Repair Car Headliner[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4343+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Volvo Car Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4344+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Toyota Camry 2009 Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4345+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]Toyota Camry 2009 Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4346+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	Add_Dir(
		name="[COLOR white][B]PT Cruiser Repair Videos[/B][/COLOR]", url=BASE+YOUTUBE_CHANNEL_ID_4327+"/", folder=True,
		icon=mediapath+"diy_auto.png", fanart=fanart)

	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'diyfix.png', fanart)

#xbmcplugin.endOfDirectory(plugin_handle)
