import socket
from discord_webhook import DiscordWebhook, DiscordEmbed
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 55673
WH_URL="<URL_HERE>"

IMPERIAL_UNITS=True

SONDES_DICT=[]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

def webhook_gen(sonde_info):

    ID = str(sonde_info['callsign']).split('-')[1]
    if IMPERIAL_UNITS:
        units = " ft"
        alt = str(format((float(sonde_info['altitude']) * 3.28084), '.2f'))
    else:
        units = " m"
        alt = str(sonde_info['altitude'])

    webhook = DiscordWebhook(url=WH_URL)
    embed = DiscordEmbed(title="Sonde Launch Detected!", description='https://sondehub.org/' + ID, color='00FFFF', inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/T7goLBv.png')
    embed.add_embed_field(name="Callsign: ", value=str(sonde_info['callsign']))
    embed.add_embed_field(name="Frequency: ", value=str(sonde_info['freq']), inline=False)
    embed.add_embed_field(name="Lat/Lon: ", value=str(sonde_info['latitude']) + ', ' + str(sonde_info['longitude']))
    embed.add_embed_field(name="Altitude: ", value=alt + units)
    embed.set_footer(text='Radiosonde_auto_rx Discord Webhook Script by trevor229')

    webhook.add_embed(embed)

    response = webhook.execute()


while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    parsed_data = json.loads(data)
    if parsed_data['type'] == "PAYLOAD_SUMMARY":
        if parsed_data['callsign'] in SONDES_DICT:
            print("sonde already in dict!")
        else:
            webhook_gen(parsed_data)
            # Very last thing to do after processing and sending embed is add sonde callsign to dict
            SONDES_DICT.append(parsed_data['callsign'])
    else:
        print("Unknown UDP message type!")