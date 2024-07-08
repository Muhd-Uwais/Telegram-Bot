import logging
import json
from telegram import Update
from telegram.ext import *
from espCommand import EspCommands

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

owner = 5308782919  # uwais

esp = EspCommands()


def read_data_from_file():
    try:
        with open('authorized.json', 'r') as file:
            data = json.load(file)
            data = {key: str(value) for key, value in data.items()}
    except FileNotFoundError:
        data = {}
    return data


def read_data_from_not_allowed():
    try:
        with open('unauthorized.json', 'r') as file:
            data = json.load(file)
            data = {key: str(value) for key, value in data.items()}
    except FileNotFoundError:
        data = {}
    return data


def write_data_to_file(data):
    with open('authorized.json', 'w') as file:
        json.dump(data, file, indent=4)


def write_data_to_not_allowed(un_id):
    with open('unauthorized.json', 'w') as file:
        json.dump(un_id, file, indent=4)


COMMANDS = {
    "/start": "Start the bot and get a greeting message.",
    "/help": "Get a list of available commands and their descriptions.",
    "/light": "To turn on and off light with their name "
              "(/light <lightname> on/off)"
              "you can see the light names in /help. "}

user_id = read_data_from_file()
not_allowed_id = read_data_from_not_allowed()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if update.message.from_user.last_name:
        username = update.message.from_user.first_name + " " + update.message.from_user.last_name
    else:
        username = update.message.from_user.first_name
    if str(chat_id) in user_id.values():
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Welcome! You are allowed to use this bot.")
        available_commands = "\n".join([f"{command} - {description}" for command, description in COMMANDS.items()])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi! I'm your bot.\nAvailable commands:"
                                                                              f"\n{available_commands}")
    else:
        not_allowed_id[username] = str(chat_id)
        write_data_to_not_allowed(not_allowed_id)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Sorry, you are not allowed to use this bot.")


async def help0(update: Update, context: CallbackContext):
    # help0 means help, the reason for using help0 is help is built-in function..
    message = """Hi there! I'm Nova, your friendly AI assistant for smart home control. 

I'm here to make your life a little easier by helping you manage your home environment with simple commands. ✨

◉ Here's what I can do:

◈Light Control:
  ○ Turn on/off the lights you can type "/light <lightname> on/off" and in that send the light's name and state 
      (/light Hlight on/off).
  ○  The names of light :  "blight" for bathu room's light
                         ● "hlight" for hall light
                         ● "slight" for sitting room light
                         ● "ulight" for uwais room light
                         ● "alight" for achu room light
                         ● "mlight" for master(umma/vappa) room light  
◈Fan Control:
  ○ Feeling warm? Get some cool air flowing with "/fan_on".
  ○ Want some peace and quiet? Use "/fan_off" to relax in tranquility.

◆ It's as easy as that! ◆ 
Just remember these commands, and I'll take care of the rest.

◆ "/start" to start ◆

◈Ready to experience the convenience of smart home automation? Let's get started!"""

    message = message.replace('\xa0', ' ').strip()
    chat_id = update.effective_chat.id
    if update.message.from_user.last_name:
        username = update.message.from_user.first_name + " " + update.message.from_user.last_name
    else:
        username = update.message.from_user.first_name
    if str(chat_id) in user_id.values():
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        not_allowed_id[username] = str(chat_id)
        write_data_to_not_allowed(not_allowed_id)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Sorry, you are not allowed to use this bot.")


async def light(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.message.from_user.last_name:
        username = update.message.from_user.first_name + " " + update.message.from_user.last_name
    else:
        username = update.message.from_user.first_name
    text = update.message.text.lower().split()  # Get lowercase words
    if str(chat_id) in user_id.values():
        if len(text) >= 2:
            # Extract light name and desired state
            light_name = text[1]
            state = text[2]

            if state == "on":
                reply = esp.send_command("on")
                await context.bot.send_message(chat_id=chat_id, text=f"{light_name.title()} {reply}")
            elif state == "off":
                reply = esp.send_command("off")
                await context.bot.send_message(chat_id=chat_id, text=f"{light_name.title()} {reply}")
            else:
                await context.bot.send_message(chat_id=chat_id, text="Invalid light state. Use 'on' or 'off'.")
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           text="Invalid command format. Use '/light <light_name> on/off'.")
    else:
        not_allowed_id[username] = str(chat_id)
        write_data_to_not_allowed(not_allowed_id)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Sorry, you are not allowed to use this bot.")


async def list_all_users(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.message.from_user.last_name:
        username = str(update.message.from_user.first_name + " " + update.message.from_user.last_name)
    else:
        username = update.message.from_user.first_name
    if str(chat_id) in user_id.values():
        if chat_id == owner:
            users_list = "\n".join([f"{name} ({chat_id})" for chat_id, name in user_id.items()])
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Allowed users:\n{users_list}")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Sorry, this function is only allowed to owner")

    else:
        not_allowed_id[username] = str(chat_id)
        write_data_to_not_allowed(not_allowed_id)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Sorry, you are not allowed to use this bot")


async def list_not_users(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.message.from_user.last_name:
        username = update.message.from_user.first_name + " " + update.message.from_user.last_name
    else:
        username = update.message.from_user.first_name
    if str(chat_id) in user_id.values():
        if chat_id == owner:
            not_allowed = read_data_from_not_allowed()
            users_list = "\n".join([f"{name} ({chat_id})" for chat_id, name in not_allowed.items()])
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Not allowed users:\n{users_list}")
        else:
            await update.message.reply_text("Sorry, this function is only allowed for owner")
    else:
        not_allowed_id[username] = str(chat_id)
        write_data_to_not_allowed(not_allowed_id)
        await update.message.reply_text("Sorry, you are not allowed to use this bot")


async def add_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.message.from_user.last_name:
        username = update.message.from_user.first_name + " " + update.message.from_user.last_name
    else:
        username = update.message.from_user.first_name
    if str(chat_id) in user_id.values():
        if chat_id == owner:
            users_list = "\n".join([f"{name} ({chat_id})" for chat_id, name in not_allowed_id.items()])
            if len(users_list) == 0:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="There is no UnAuthorized users")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=f"UnAuthorized users:\n{users_list}")

            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Type like this : /adduser <name> <value>")
            args = context.args
            username = args[0]
            if len(args) < 2:
                if username == "dlt_all":
                    write_data_to_not_allowed({})
                    await update.message.reply_text("All elements in the unauthorized has been deleted")
                else:
                    await update.message.reply_text("Type like this : /adduser <name> <value>")
                    return
            else:
                username = args[0]
                value = ' '.join(args[1:])
                user_id[username] = value
                write_data_to_file(user_id)
                await update.message.reply_text(f"Successfully Added {username}")
        else:
            await update.message.reply_text("Sorry, this function only allowed to owner")
    else:
        not_allowed_id[username] = str(chat_id)
        write_data_to_not_allowed(not_allowed_id)
        await update.message.reply_text("Sorry, you are not allowed to use this bot")


async def remove_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.message.from_user.last_name:
        username = update.message.from_user.first_name + " " + update.message.from_user.last_name
    else:
        username = update.message.from_user.first_name
    if str(chat_id) in user_id.values():
        if chat_id == owner:
            users_list = "\n".join([f"{name} ({chat_id})" for chat_id, name in user_id.items()])
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Allowed users:\n{users_list}")
            args = context.args
            if len(args) < 1:
                await update.message.reply_text("Type like this : /remove_user <name>")
                return
            name = args[0]
            if name in user_id:
                del user_id[name]
                write_data_to_file(user_id)
                await update.message.reply_text(f"Removed user {name}")
            else:
                await update.message.reply_text(f"User {name} not found")
        else:
            await update.message.reply_text("Sorry, this function is only allowed to owner")
    else:
        not_allowed_id[username] = str(chat_id)
        write_data_to_not_allowed(not_allowed_id)
        await update.message.reply_text("Sorry, you are not allowed to use this bot")


async def message_handler(update: Update, context: CallbackContext) -> None:
    # Check if the message starts with "/"
    command_entered = update.message.text.split()[0].lower()

    # Suggest similar commands if an incorrect command was entered
    suggested_commands = [cmd for cmd in COMMANDS.keys() if cmd.lower().startswith(command_entered)]
    if not suggested_commands:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"No command '{command_entered}' found. Did you mean one of these?"
                                            f"\n{', '.join(COMMANDS.keys())}")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"No command '{command_entered}' found."
                                            f" Did you mean '{suggested_commands[0]}'?")


if __name__ == '__main__':
    TOKEN = ""
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help0))
    application.add_handler(CommandHandler('light', light))
    application.add_handler(CommandHandler('list_all_users', list_all_users))
    application.add_handler(CommandHandler('list_not_users', list_not_users))
    application.add_handler(CommandHandler('adduser', add_user))
    application.add_handler(CommandHandler('remove_user', remove_user))
    application.add_handler(MessageHandler(filters.Text(), message_handler))

    application.run_polling()
