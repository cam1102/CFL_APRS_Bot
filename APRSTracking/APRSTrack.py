from re import A
import serial
import datetime
import aprslib
from aprslib.base91 import from_decimal
import csv
import what3words
import time
import requests
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ['SLACK_BOT_TOKEN']
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

def SlackPost(post,team_channel):

    try:
        response = client.chat_postMessage(channel= team_channel, text = post)
        #assert response["message"]["text"] == post
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
    pass

SlackPost("APRS Tracking Started...", '#alpha_bot')
SlackPost("APRS Tracking Started...", '#bravo_bot')
SlackPost("APRS Tracking Started...", '#charlie_bot')
SlackPost("APRS Tracking Started...", '#delta_bot')
SlackPost("APRS Tracking Started...", '#echo_bot')


csv_alpha = ('CFL_APRS_ALPHA' + str(datetime.datetime.now()))
csv_bravo = ('CFL_APRS_BRAVO' + str(datetime.datetime.now()))
csv_charlie = ('CFL_APRS_CHARLIE' + str(datetime.datetime.now()))
csv_delta = ('CFL_APRS_DELTA' + str(datetime.datetime.now()))
csv_echo = ('CFL_APRS_ECHO' + str(datetime.datetime.now()))
field_names = ["Time","Callsign","Team","Latitiude","Longitude","Altitude (m)","Speed (mph)","Heading (deg)","Link"]


with open(os.path.join('alpha_log', csv_alpha), 'w') as a:
    writer = csv.writer(a)
    writer.writerow(field_names)
    a.close()

with open(os.path.join('bravo_log', csv_bravo), 'w') as b:
    writer = csv.writer(b)
    writer.writerow(field_names)
    b.close()

with open(os.path.join('charlie_log', csv_charlie), 'w') as c:
    writer = csv.writer(c)
    writer.writerow(field_names)
    c.close()

with open(os.path.join('delta_log', csv_delta), 'w') as d:
    writer = csv.writer(d)
    writer.writerow(field_names)
    d.close()

with open(os.path.join('echo_log', csv_echo), 'w') as e:
    writer = csv.writer(e)
    writer.writerow(field_names)
    e.close()


ser2 = serial.Serial('/dev/tty.usbmodem14401', 9600, timeout=1) #open kenwood serial port
print("Connecting to Radio...")

geocoder = what3words.Geocoder("DGOT5E5N")


Callsigns = {'Alpha': 'KE8PTU-11', 'Bravo': 'KF6RFX-12', 'Charlie': 'KE8PTV-11', 'Delta': 'KF6RFX-14', 'Echo': 'KF6RFX-15'}

print('Waiting for Signal...')
AlphaCount = 0
BravoCount = 0

try:
    while 1: #infinite loop unless broken
        if ser2.in_waiting > 0: #If APRS signal is received
            print('Signal Recieved!')
 #Decode the message if possible
            line = ser2.readline().decode('utf-8').rstrip()
            decode = aprslib.parse(line) #Parse APRS Packet
            print(datetime.datetime.now())
            try:
                print(decode["from"])
                now = time.time()
                for team in Callsigns:
                    if decode['from'] == Callsigns[team]:
                        print('From: ', team) #Print Sender
                        #print('Comment:', decode['comment']) #Print Comments
                        lat2 = str(decode['latitude']) #Parse GPS Coords of Sender into string
                        lon2 = str(decode['longitude'])
                        lat2 = lat2[0:10] #truncate GPS Coords for sending
                        lon2 = lon2[0:10]
                        alt2 = str(decode['altitude'])

                        res = geocoder.convert_to_3wa(what3words.Coordinates(lat2, lon2))
                        print(team + ': ' + Callsigns[team])
                        print(res['words'])
                        print(res['map'])
                        print( '('+ str(lat2) + ', ' + str(lon2) + ', ' + str(alt2) + ')' )
                        print('Target Traveling at ' , str(decode['speed']) , ' MPH with a Heading of ' , str(decode['course']) , ' degrees.' )

                        data = (str(datetime.datetime.now()) + ", " + team + ", " + Callsigns[team] + ", " + str(lat2) + ", " + str(lon2) + ", " + alt2 + ", " + str(decode['speed']) + ", " + str(decode['course']) + ", " + res['map'] + "\n")

                        if team == 'Alpha':
                            AlphaState = 'ALPHA------------------------ \n @team_alpha_f21 - Your Balloon is at ' + res['words'] + ', ' + '('+ str(decode['latitude']) + ', ' + str(decode['longitude']) + ', ' + alt2 + ') \n Target Traveling at ' + str(decode['speed']) + ' MPH with a Heading of ' + str(decode['course']) + ' degrees. \n See Map Here: ' + str(res['map'])
                            with open(os.path.join('alpha_log', csv_alpha), 'a') as a:          
                                a.write(data)
                                a.close()
                            if AlphaCount == 2:
                                SlackPost(AlphaState, '#alpha_bot')
                                AlphaCount = 0
                            else: 
                                AlphaCount = AlphaCount + 1   

                        if team == 'Bravo':
                            BravoState = 'BRAVO------------------------ \n @team_bravo_f21 - Your Balloon is at ' + res['words'] + ', ' + '('+ str(decode['latitude']) + ', ' + str(decode['longitude']) + ', ' + alt2 + ') \n Target Traveling at ' + str(decode['speed']) + ' MPH with a Heading of ' + str(decode['course']) + ' degrees. \n See Map Here: ' + str(res['map'])
                            with open(os.path.join('bravo_log', csv_bravo), 'a') as b:          
                                b.write(data)
                                b.close()
                            if BravoCount == 2:
                                SlackPost(BravoState, '#bravo_bot')
                                BravoCount = 0
                            else:
                                print (BravoCount)    
                                BravoCount = BravoCount + 1 

                        if team == 'Charlie':
                            CharlieState = 'CHARLIE------------------------ \n @team_charlie_f21 - Your Balloon is at ' + res['words'] + ', ' + '('+ str(decode['latitude']) + ', ' + str(decode['longitude']) + ', ' + alt2 + ') \n Target Traveling at ' + str(decode['speed']) + ' MPH with a Heading of ' + str(decode['course']) + ' degrees. \n See Map Here: ' + str(res['map'])
                            with open(os.path.join('charlie_log', csv_charlie), 'a') as c:          
                                c.write(data)
                                c.close()
                            SlackPost(CharlieState, '#charlie_bot')
 
                        if team == 'Delta':
                            DeltaState = 'DELTA------------------------ \n @team_delta_f21 - Your Balloon is at ' + res['words'] + ', ' + '('+ str(decode['latitude']) + ', ' + str(decode['longitude']) + ', ' + alt2 + ') \n Target Traveling at ' + str(decode['speed']) + ' MPH with a Heading of ' + str(decode['course']) + ' degrees. \n See Map Here: ' + str(res['map'])
                            with open(os.path.join('delta_log', csv_delta), 'a') as d:          
                                d.write(data)
                                d.close()
                            SlackPost(DeltaState, '#delta_bot')

                        if team == 'Echo':
                            EchoState = 'ECHO------------------------ \n @team_echo_f21 - Your Balloon is at ' + res['words'] + ', ' + '('+ str(decode['latitude']) + ', ' + str(decode['longitude']) + ', ' + alt2 + ') \n Target Traveling at ' + str(decode['speed']) + ' MPH with a Heading of ' + str(decode['course']) + ' degrees. \n See Map Here: ' + str(res['map'])
                            with open(os.path.join('echo_log', csv_echo), 'a') as e:          
                                e.write(data)
                                e.close()
                            SlackPost(EchoState, '#echo_bot')




            except:
                 print("Parsing Failed")

except KeyboardInterrupt:
    SlackPost("Tracking Ended... File Here:", '#alpha_bot')
    SlackPost("Tracking Ended... File Here:", '#bravo_bot')
    SlackPost("Tracking Ended... File Here:", '#charlie_bot')
    SlackPost("Tracking Ended... File Here:", '#delta_bot')
    SlackPost("Tracking Ended... File Here:", '#echo_bot')
    filepath_alpha= ("/Users/cameronb/Documents/:Univeristy_of_Michigan /Fall_2021/CubeSat Design/repos/team-delta/APRSTracking/alpha_log/" + csv_alpha)
    filepath_bravo= ("/Users/cameronb/Documents/:Univeristy_of_Michigan /Fall_2021/CubeSat Design/repos/team-delta/APRSTracking/bravo_log/" + csv_bravo)
    filepath_charlie= ("/Users/cameronb/Documents/:Univeristy_of_Michigan /Fall_2021/CubeSat Design/repos/team-delta/APRSTracking/charlie_log/" + csv_charlie)
    filepath_delta= ("/Users/cameronb/Documents/:Univeristy_of_Michigan /Fall_2021/CubeSat Design/repos/team-delta/APRSTracking/delta_log/" + csv_delta)
    filepath_echo= ("/Users/cameronb/Documents/:Univeristy_of_Michigan /Fall_2021/CubeSat Design/repos/team-delta/APRSTracking/echo_log/" + csv_echo)

    response = client.files_upload(channels='#alpha_bot', file=filepath_alpha)
    response = client.files_upload(channels='#bravo_bot', file=filepath_bravo)
    response = client.files_upload(channels='#charlie_bot', file=filepath_charlie)
    response = client.files_upload(channels='#delta_bot', file=filepath_delta)
    response = client.files_upload(channels='#echo_bot', file=filepath_echo)
    
