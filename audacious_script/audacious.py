# audacious now playing for weechat
# nashgul <m.alcocer1978@gmail.com>
# version 0.1

# white => "00", black => "01", darkblue => "02", darkgreen => "03", lightred => "04", darkred => "05", magenta => "06", orange => "07", yellow => "08", lightgreen => "09", cyan => "10", lightcyan => "11", lightblue => "12", lightmagenta => "13", gray => "14", lightgray => "15"

import weechat
import subprocess

weechat.register("audacious_np", "nashgul", "0.01", "GPL2", "now playing for audacious (usage: /audacious)", "", "")

name = 'audacious'
description = 'show now playing for audacious'
hook = weechat.hook_command(name, description, '', '', '', 'now_playing', '')

def get_info_array():
    info_list = (['audtool current-song',
        'audtool current-song-length',
        'audtool current-song-output-length',
        'audtool current-song-bitrate-kbps',
        'audtool current-song-filename'])
    results = []
    for x in info_list:
        temporal = subprocess.Popen(x, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        b = temporal.stdout.read().splitlines()
        results.append(b[0])
    return results

def now_playing(datos, channel, args):
    colors = {
            'white' : '00', 'black' : '01', 'darkblue' : '02', 'darkgreen' : '03',
            'lightred' : '04', 'darkred' : '05', 'magenta' : '06', 'orange' : '07',
            'yellow' : '08', 'lightgreen' : '09', 'cyan' : '10', 'lightcyan' : '11',
            'lightblue' : '12', 'lightmagenta' : '13', 'gray' : '14', 'lightgray' : '15'
            }
    
    info_array = get_info_array()

    message_color = "%s" % colors['darkblue']
    message = u'\x03' + message_color + 'esta reproduciendo' + u'\x0f'
    song_color = "%s" % colors['lightred']
    song = u'\x03' + song_color + info_array[0] + u'\x0f'
    song_filename_color = "%s" % colors['lightred']
    song_filename = u'\x03' + song_filename_color + info_array[4] + u'\x0f'
    brackets_color = "%s" % colors['yellow']
    bracket_1 = u'\x03' + brackets_color + '[' + u'\x0f' 
    bracket_2 = u'\x03' + brackets_color + ']' + u'\x0f'
    hyphen_color = "%s" % colors['yellow']
    hyphen = u'\x03' + hyphen_color + '-' + u'\x0f'
    at_color = "%s" % colors['yellow']
    at_sym = u'\x03' + at_color + '@' + u'\x0f'
    output_length_color = "%s" % colors['lightblue']
    output_length = u'\x03' + output_length_color + info_array[2] + u'\x0f'
    length_color = "%s" % colors['lightblue']
    length = u'\x03' + length_color + info_array[1] + u'\x0f'
    bitrate_color = "%s" % colors['lightmagenta']
    bitrate = u'\x03' + bitrate_color + info_array[3] + ' kbps' + u'\x0f'

    if length == '0:00':
        string = "%s %s %s %s %s" %(bracket_1, output_length, at_sym, bitrate, bracket_2)
    else:
        string = "%s %s %s %s %s %s %s" %(bracket_1, output_length, hyphen, length, at_sym, bitrate, bracket_2)
    source = ''
    if song_filename.lower().startswith('http'):
        source = song_filename 
    output_string = "%s: %s %s %s" %(message, source, song, string)
    weechat.command(channel, "/me %s" % (output_string))
    return weechat.WEECHAT_RC_OK

