nick = 'bobbot'
host = 'irc.rizon.net'
channels = ['#perwl', ]
owner = 'yournickname'

# password is the NickServ password, serverpass is the server password
# password = 'example'
# serverpass = 'serverpass'

# These are people who will be able to use admin.py's functions...
admins = [owner, 'bobsapp[vps]', 'bobsapp']
# But admin.py is disabled by default, as follows:
exclude = ['admin']

# If you want to enumerate a list of modules rather than disabling
# some, use "enable = ['example']", which takes precedent over exclude
# 
# enable = []

# Directories to load user modules from
# e.g. /path/to/my/modules
extra = []

# Services to load: maps channel names to white or black lists
external = { 
   '#perwl': ['!'], # allow all
   # '#conservative': [], # allow none
   '*': [] # default whitelist, allow all
}

# EOF

