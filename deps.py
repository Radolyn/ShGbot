import os
import sys

def run_python_tool(command):
    os.system(
        'cd \"' + os.path.dirname(sys.executable) + '\" && ' + os.path.basename(sys.executable) + ' -m ' + command)

run_python_tool('pip install --upgrade pip')

run_python_tool('pip install requests discord youtube-dl --user')
run_python_tool('pip install -U discord.py[voice]')
run_python_tool('pip install --upgrade youtube-dl')
#run_python_tool('ffmpeg -i input.mp4 output.avi')

print('Bot ready to work.')  
