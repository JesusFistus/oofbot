import config_handler as config
from student_management import student_setup

commands = {
    'help': help,
    'setup': student_setup
}

# TODO: Eingetragene Zuweisungen auslesen lassen und bei bedarf ändern können

PREFIX = config.get('PREFIX')


async def check_command(message):
    if message.content.startswith(PREFIX):
        command = message.content.split(' ')[0][1:]
        try:
            await commands[command](message)
        except KeyError:
            await message.author.send(f'{command} ist kein gültiger Befehl, '
                                      f'tippe {PREFIX}help für eine liste an verfügbaren Befehlen.')