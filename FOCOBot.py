from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import asyncio
import nest_asyncio

nest_asyncio.apply()

# Función para mostrar las opciones de selección
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Obtener enlace al GIEP", callback_data='1')],
        [InlineKeyboardButton("Si estoy de vacaciones, ¿cuándo entrego mis tareas?", callback_data='2')],
        [InlineKeyboardButton("¿Cuándo se publican los nuevos e-books?", callback_data='3')],
        [InlineKeyboardButton("¿En qué parte del telegram se encuentran los e-books?", callback_data='4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Selecciona una pregunta usando el menú:', reply_markup=reply_markup)

# Función que maneja las respuestas del usuario
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    # Responder según la opción seleccionada
    if query.data == '1':
        await query.edit_message_text(text="Enlace al GIEP: https://www.giep-platform.pafar.com.ve")
    elif query.data == '2':
        await query.edit_message_text(text="Las personas que se encuentran de vacaciones tienen una semana para entregar sus actividades, después de integrarse de manera física a Movilnet.")
    elif query.data == '3':
        await query.edit_message_text(text="Los nuevos e-books se publican cada 2 semanas después de la entrega, es decir, 15 días o 10 días hábiles.")
    elif query.data == '4':
        await query.edit_message_text(text="En los grupos de Telegram y en los correos corporativos (@movilnet.com.ve).")

# Función que muestra el menú si es el primer mensaje
async def show_menu_on_first_message(update: Update, context):
    # Al recibir cualquier mensaje, muestra el menú como si fuera el comando /start
    await start(update, context)

# Configuración del bot
async def main():
    application = Application.builder().token("7047103350:AAFyzHfZcG0DVxq515V77Vrnd1AeroG5adE").build()

    # Comando /start para mostrar las preguntas
    application.add_handler(CommandHandler("start", start))

    # Manejo de respuestas por botones
    application.add_handler(CallbackQueryHandler(button))

    # Mostrar automáticamente el menú al recibir el primer mensaje del usuario
    application.add_handler(MessageHandler(filters.ALL, show_menu_on_first_message))

    # Ejecutar el bot usando run_polling
    await application.run_polling()

if __name__ == '__main__':
    # Usar asyncio.run solo si el loop no está corriendo
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        print("El event loop ya está corriendo.")
        asyncio.ensure_future(main())  # Usar ensure_future si ya hay un loop corriendo
    else:
        asyncio.run(main())
