from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import asyncio
import nest_asyncio

# Apply nest_asyncio to avoid issues with event loops in certain environments.
nest_asyncio.apply()

# Function: start
# Summary:
#   Sends a menu with options as inline buttons when the user interacts with the bot.
# Parameters:
#   update (Update): Contains information about the incoming update (such as the message and user).
#   context: Contains information and data related to the conversation, like bot details.
# Remarks:
#   Displays four options for the user to choose from and replies with a menu using InlineKeyboardMarkup.
async def start(update: Update, context):
    # Check if the menu has already been sent to the user
    user_data = context.user_data
    if user_data.get('menu_active', False):
        return  # Do nothing if the menu is already active

    # Mark the menu as active for this user
    user_data['menu_active'] = True

    keyboard = [
        [InlineKeyboardButton("Obtener enlace al GIEP", callback_data='1')],
        [InlineKeyboardButton("Si estoy de vacaciones, ¿cuándo entrego mis tareas?", callback_data='2')],
        [InlineKeyboardButton("¿Cuándo se publican los nuevos e-books?", callback_data='3')],
        [InlineKeyboardButton("¿En qué parte del telegram se encuentran los e-books?", callback_data='4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Selecciona una pregunta usando el menú:', reply_markup=reply_markup)


async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    # Dictionary to map callback data to questions with bold text
    questions = {
        '1': "<b>Has seleccionado: Obtener enlace al GIEP</b>",
        '2': "<b>Has seleccionado: Si estoy de vacaciones, ¿cuándo entrego mis tareas?</b>",
        '3': "<b>Has seleccionado: ¿Cuándo se publican los nuevos e-books?</b>",
        '4': "<b>Has seleccionado: ¿En qué parte del telegram se encuentran los e-books?</b>"
    }

    # Dictionary to map callback data to answers
    answers = {
        '1': "Enlace al GIEP: https://www.giep-platform.pafar.com.ve",
        '2': "Las personas que se encuentran de vacaciones tienen una semana para entregar sus actividades, después de integrarse de manera física a Movilnet.",
        '3': "Los nuevos e-books se publican cada 2 semanas después de la entrega, es decir, 15 días o 10 días hábiles.",
        '4': "En los grupos de Telegram y en los correos corporativos (@movilnet.com.ve)."
    }

    # Get the question and answer based on the selected option
    question_selected = questions.get(query.data, "Opción no válida")
    answer = answers.get(query.data, "No hay respuesta para esta opción")

    # Send both the question and answer in the same message using HTML
    await query.edit_message_text(text=f"{question_selected}\n{answer}", parse_mode="HTML")

    # Mostrar el menú de nuevo tras responder
    keyboard = [
        [InlineKeyboardButton("Obtener enlace al GIEP", callback_data='1')],
        [InlineKeyboardButton("Si estoy de vacaciones, ¿cuándo entrego mis tareas?", callback_data='2')],
        [InlineKeyboardButton("¿Cuándo se publican los nuevos e-books?", callback_data='3')],
        [InlineKeyboardButton("¿En qué parte del telegram se encuentran los e-books?", callback_data='4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Restablece la bandera para permitir que el menú vuelva a aparecer después de responder
    context.user_data['menu_active'] = True

    # Enviar el menú de nuevo
    await query.message.reply_text('Selecciona otra pregunta usando el menú:', reply_markup=reply_markup)


# Function: show_menu_on_first_message
# Summary:
#   Automatically shows the menu when the user sends any message to the bot.
# Parameters:
#   update (Update): Contains details about the user's incoming message.
#   context: Provides context about the conversation or interaction.
# Remarks:
#   This function acts like an auto-trigger to show the menu, simulating the /start command.
async def show_menu_on_first_message(update: Update, context):
    # Call start function if the menu is not already active
    await start(update, context)


# Function: main
# Summary:
#   Configures and runs the Telegram bot using polling.
# Remarks:
#   The bot is set up with handlers for the /start command, button presses from the menu,
#   and a fallback to show the menu when any message is received. It uses long polling to keep
#   the bot responsive.
async def main():
    application = Application.builder().token("7047103350:AAFyzHfZcG0DVxq515V77Vrnd1AeroG5adE").build()

    # Handle the /start command to show the menu
    application.add_handler(CommandHandler("start", start))

    # Handle button clicks in the menu
    application.add_handler(CallbackQueryHandler(button))

    # Automatically show the menu when the user sends a message
    application.add_handler(MessageHandler(filters.ALL, show_menu_on_first_message))

    # Start the bot using long polling
    await application.run_polling()


# Entry point: Runs the bot using asyncio, ensuring that the event loop is properly handled.
if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    # If the event loop is already running, ensure future tasks are added to the loop
    if loop and loop.is_running():
        print("The event loop is already running.")
        asyncio.ensure_future(main())  # Use ensure_future if an event loop exists
    else:
        # If no event loop exists, run the main function with asyncio
        asyncio.run(main())
