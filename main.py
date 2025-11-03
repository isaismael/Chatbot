import os
import telebot
from dotenv import load_dotenv
from database import crear_tabla, agregar_turno, obtener_turnos, cancelar_turno

# Cargar variables del entorno
load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')
if not BOT_TOKEN:
    raise ValueError("No se encontró el token del bot")

bot = telebot.TeleBot(BOT_TOKEN)

# Crear base de datos si no existe
crear_tabla()

# --- Comandos ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 ¡Hola! Soy el asistente de turnos.\n\n"
                          "Podés usar los siguientes comandos:\n"
                          "/especialidades - Ver especialidades\n"
                          "/ver_turnos - Ver tus turnos\n"
                          "/cancelar - Cancelar un turno")


# --- Mostrar especialidades ---
@bot.message_handler(commands=['especialidades'])
def mostrar_especialidades(message):
    especialidades = ["Clínica médica", "Pediatría", "Dermatología", "Cardiología", "Traumatología"]
    texto = "🏥 *Especialidades disponibles:*\n\n"
    for esp in especialidades:
        texto += f"🔹 {esp}\n"
    texto += "\nEscribí la especialidad que querés para continuar."
    bot.send_message(message.chat.id, texto, parse_mode="Markdown")
    bot.register_next_step_handler(message, elegir_especialidad)


def elegir_especialidad(message):
    especialidad = message.text
    # En un caso real, podrías filtrar por médicos disponibles
    bot.send_message(message.chat.id, f"Elegiste *{especialidad}*.\n\nPor favor, ingresá el nombre del médico:", parse_mode="Markdown")
    bot.register_next_step_handler(message, lambda msg: elegir_medico(msg, especialidad))


def elegir_medico(message, especialidad):
    medico = message.text
    bot.send_message(message.chat.id, "📅 Ingresá la *fecha del turno* (formato: DD/MM/AAAA):", parse_mode="Markdown")
    bot.register_next_step_handler(message, lambda msg: elegir_fecha(msg, especialidad, medico))


def elegir_fecha(message, especialidad, medico):
    fecha = message.text
    bot.send_message(message.chat.id, "🕐 Ingresá la *hora del turno* (formato: HH:MM):", parse_mode="Markdown")
    bot.register_next_step_handler(message, lambda msg: confirmar_turno(msg, especialidad, medico, fecha))


def confirmar_turno(message, especialidad, medico, fecha):
    hora = message.text
    paciente = message.from_user.first_name

    agregar_turno(paciente, especialidad, medico, fecha, hora)
    bot.send_message(message.chat.id, f"✅ Turno confirmado para *{paciente}*\n\n"
                                      f"👨‍⚕️ Médico: {medico}\n"
                                      f"🏥 Especialidad: {especialidad}\n"
                                      f"📅 Fecha: {fecha}\n"
                                      f"🕐 Hora: {hora}", parse_mode="Markdown")


# --- Ver turnos ---
@bot.message_handler(commands=['ver_turnos'])
def ver_turnos(message):
    turnos = obtener_turnos()
    if not turnos:
        bot.send_message(message.chat.id, "No hay turnos registrados.")
        return

    texto = "📋 *Turnos registrados:*\n\n"
    for t in turnos:
        texto += f"🆔 {t[0]} | {t[1]} - {t[2]} ({t[3]})\n📅 {t[4]} {t[5]} | Estado: {t[6]}\n\n"
    bot.send_message(message.chat.id, texto, parse_mode="Markdown")


# --- Cancelar turno ---
@bot.message_handler(commands=['cancelar'])
def cancelar(message):
    bot.send_message(message.chat.id, "🔢 Ingresá el *ID del turno* que querés cancelar:")
    bot.register_next_step_handler(message, confirmar_cancelacion)


def confirmar_cancelacion(message):
    try:
        id_turno = int(message.text)
        cancelar_turno(id_turno)
        bot.send_message(message.chat.id, f"❌ Turno {id_turno} cancelado correctamente.")
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ El ID ingresado no es válido.")


# --- Eco (fallback) ---
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Usá /help para ver los comandos disponibles 🙂")


# --- Iniciar bot ---
print("ChatBot de gestión de turnos iniciado...")
bot.infinity_polling()
