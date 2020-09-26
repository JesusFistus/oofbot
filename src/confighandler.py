configfilelocation = 'C:/Users/Yanni/Documents/GitHub/oofbot/src/data/Bot.cfg'


def configdict():
    contentdict = {}
    with open(configfilelocation, 'r') as file:
        file.seek(0, 0)
        for line in file:
            try:
                key = line.split('=')[0].strip(' ')
                value = line.split('=')[1].strip(' ').strip('\n')
                contentdict[key] = value
            except:
                print(f'ERROR: There was a problem while reading from configfile at {configfilelocation}')
    return contentdict


cfgdict = configdict()


def get(key):
    try:
        value = cfgdict[key]
        if ',' in value:  # einzelne values dürfen keine ',' enthalten
            return value.split(',')
        return value
    except KeyError:
        print(f'"{key}" could not be found in configfile')


def update():
    global cfgdict
    cfgdict = configdict()
