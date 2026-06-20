import os
import time
import random
import turtle
import math

# Variables globales de estado en el juego

estado_juego = {
    "nombre": "", "tiempo": 0, "animo": 100, "turno_actual": 1,
    "px": 0.0, "py": 0.0, "angulo": 0, "meta_x": 0, "meta_y": 0,
    "cooldown_eventos": 0, "karma_urbano": 0, "historial_logs": [],
    
    "inicio_x": 0.0, "inicio_y": 0.0, "inicio_tiempo": 0, "inicio_animo": 100, "inicio_angulo": 0
}

historia_flags = {
    "actos_vistos": [], "estados_personaje": [], "mochila": [], 
    "misiones_activas": {}, "aliado_metro": False, "amigo_mimo": False,
    "enemigo_publico": False, "heroe_canino": False, "javi_contacto": False,
    "ganso_aliado": False, "atasco_meta": False, "cruasanes_cantidad": 0,
    "turnos_sombra_parque": 0, "guille_bloqueado": False,
    "ptr_amor": 0, "ptr_guille": 0, "ptr_mama": 0, "ptr_laura": 0, "ptr_pensamiento": 0,
    "encuentros_profundos_vistos": []
}

registro_secretos = {
    "gatos_fijos": 0, "turnos_con_gato_actual": 0, "gato_en_cortejo": False,
    "tipo_gato_actual": None
}

DIRECCIONES_ANGULOS = {"W": 90, "S": 270, "A": 180, "D": 0, "WD": 45, "WA": 135, "SA": 225, "SD": 315}

chats_data = {
    "Amor ❤️ ": {"historial": [], "unread": False, "pending_options": {}},
    "Bro Guille": {"historial": [], "unread": False, "pending_options": {}},
    "Mamá 👵": {"historial": [], "unread": False, "pending_options": {}},
    "Prima Laura ✉️": {"historial": [], "unread": False, "pending_options": {}}
}

tramas = {
    "amor_trama_iniciada": False, "amor_trama_resuelta": False, "amor_fase": 1, 
    "amor_timer_ghosting": 0, "guille_trama_iniciada": False, "guille_trama_resuelta": False,
    "empapado_chat": False, "cojo_chat": False, "insolacion_chat": False
}

# Colores
# Texto
ROJO = '\033[91m'
VERDE = '\033[92m'
AZUL = '\033[94m'
RESET = '\033[0m'

# Fondo
FONDO_ROJO = '\033[41m'
FONDO_VERDE = '\033[42m'
FONDO_AZUL = '\033[44m'

# Funciones útiles 

def clear_terminal(): 
    os.system('cls' if os.name == 'nt' else 'clear')

def escribir_consola_lento(texto, retraso=0.012):
    """Escribe el texto de forma fluida y natural."""
    for letra in texto:
        print(letra, end='', flush=True)
        time.sleep(retraso)
    print()

def registrar_log(texto): 
    estado_juego["historial_logs"].append(f"Turno {estado_juego['turno_actual']}: {texto}")

def cambiar_animo(valor): 
    estado_juego["animo"] = max(0, min(100, estado_juego["animo"] + valor))

def cambiar_tiempo(valor): 
    estado_juego["tiempo"] = max(0, estado_juego["tiempo"] + valor)

def cambiar_karma(valor): 
    estado_juego["karma_urbano"] = max(-20, min(20, estado_juego["karma_urbano"] + valor))

def calcular_rumbo_exacto(x_origen, y_origen, x_destino, y_destino):
    dx = x_destino - x_origen
    dy = y_destino - y_origen
    angulo = math.degrees(math.atan2(dy, dx))
    if angulo < 0: angulo += 360
    sectores = ["D", "WD", "W", "WA", "A", "SA", "S", "SD"]
    idx = int(round((angulo % 360) / 45)) % 8
    return sectores[idx]

def respuesta_inmediata(contacto, texto):
    """Simula el efecto de que el NPC está escribiendo una respuesta en whatsapp"""
    print(f"\n  [{contacto} está escribiendo", end="")
    for _ in range(4):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print("]")
    time.sleep(0.3)
    print(f"  {contacto}: '{texto}'")
    chats_data[contacto]["historial"].append(contacto + ": " + texto)

def basic_reply(contacto, animo_mod, karma_mod):
    chats_data[contacto]["pending_options"] = {}
    cambiar_animo(animo_mod)
    cambiar_karma(karma_mod)

def enviar_mensaje(contacto, texto, opciones=None, typing=False):
    """Pone un mensaje en la bandeja y lo muestra."""
    chats_data[contacto]["historial"].append(contacto + ": " + texto)
    chats_data[contacto]["unread"] = True
    if opciones: chats_data[contacto]["pending_options"] = opciones
    
    clear_terminal()
    print("\n\n" + "  💬 "*10)
    print(f"   {FONDO_VERDE}[WHATSAPP] NUEVO MENSAJE DE: {contacto.upper()}{RESET}")
    print("  " + "─"*30)
    
    if typing:
        print("   [Escribiendo", end="")
        for _ in range(4):
            time.sleep(0.3)
            print(".", end="", flush=True)
        print("\r" + " "*30 + "\r", end="")
        
    print("   🗨️  ", end="")
    escribir_consola_lento(f"\"{texto}\"", 0.015)
    print("  💬 "*10 + "\n")
    
    input("  [PULSA ENTER PARA CONTINUAR]")
    clear_terminal()

# Tramas/subtramas 

def resolver_amor_trama(fase, animo_val=0):
    chats_data["Amor ❤️ "]["pending_options"] = {}
    if fase == 1:
        tramas["amor_fase"] = 1.5; tramas["amor_timer_ghosting"] = 0; cambiar_animo(5)
        respuesta_inmediata("Amor ❤️ ", "Okiss! Luego te paso una foto para que me des el visto bueno.")
    elif fase == 2:
        tramas["amor_fase"] = 2.5; cambiar_animo(10)
        respuesta_inmediata("Amor ❤️ ", "¡Ay que monisss GRACIASS!")
    elif fase == 3:
        tramas["amor_trama_resuelta"] = True; cambiar_animo(animo_val)
        respuesta_inmediata("Amor ❤️ ", "Uff, vale. Menos mal. La he conseguido frenar. VEN YA")

def resolver_guille(aceptado):
    chats_data["Bro Guille"]["pending_options"] = {}
    if aceptado:
        historia_flags["misiones_activas"]["VINILO_GUILLE"] = "ACTIVADA"
        print(f"\n-> ¡Misión secundaria aceptada! Busca el hito {FONDO_AZUL}CIAN{RESET} en el radar GPS.")
        respuesta_inmediata("Bro Guille", "¡Eres un grande chaval! Le digo a mi hermano que te espere allí.")
        q = turtle.Turtle(); q.hideturtle(); q.penup(); q.color("cyan"); q.goto(40, 20); q.dot(12); turtle.update()
    else:
        historia_flags["guille_bloqueado"] = True
        respuesta_inmediata("Bro Guille", "Qué soso eres, tío. Pues nada, paso de ti hoy.")

def activar_mision_tio():
    chats_data["Amor ❤️ "]["pending_options"] = {}
    historia_flags["misiones_activas"]["AYUDA_TIO"] = "ACTIVADA"
    respuesta_inmediata("Amor ❤️ ", "No te preocupes. Le he escrito a tu tío Alberto. Está en la oficina central (30, 50), pásate y te da ropa seca.")


#DATA POOLS

POOL_PENSAMIENTOS = [
    "Mi primo devorará los canapés de jamón si no aligero las zancadas.",
    "El urbanismo de esta zona lo diseñó un mono jugando al Tetris con las aceras.",
    "Si salvo el aniversario me pido la ración de pollo gigante en la cena de gala.",
    "Ojalá haber traído los patines en línea de mi hermano para correr más rápido.",
    "La corbata de gala me está rozando el cuello de mala manera, qué agobio.",
    "Como fracase con la caja, mi madre me va a dar la charla del siglo.",
    "Qué cantidad de peatones cruzando, me entran ganas de empujar esquinas.",
    "Venga, concéntrate: una manzana al frente, otra adelante... sin rodeos.",
    "Rezo para que el abuelo Pepe no intente bailar breakdance en la pista hoy.",
    "El ruido del tráfico me está empezando a dar un dolor de cabeza monumental.",
    "Si consigo un taxi milagroso que vaya en mi dirección me tiro en plancha.",
    "Me duelen las pantorrillas, el asfalto está durísimo con estos zapatos."
]

FICHA_AMOR_EVOLUTIVO = {
    1: {"m": "¿Por qué zona de la ciudad vas? Toda la familia me está preguntando. Manda ubicación."},
    2: {"m": "BRO SÉ QUE LO HAS VISTO."},
    3: {"m": "¡RESPONDE YA! Mi madre tiene el motor del coche encendido. Como salga va a liar un atasco de locos."},
    4: {"m": "Es la última vez que te escribo. Mi madre está abriendo la puerta del garaje. Si no contestas arranca."}
}

POOL_AMOR_PROGRESIVO = [
    {"m": "He conseguido que te sienten a mi lado en la mesa principal, ¡así que ven limpio!", "r1": "'¡Allí estaré oliendo a colonia impecable!'", "f1": lambda: [basic_reply("Amor ❤️ ", 5, 0), respuesta_inmediata("Amor ❤️ ", "Más te vale jaja, te espero.")], "r2": "'La ciudad me está destrozando el traje hoy.'", "f2": lambda: basic_reply("Amor ❤️ ", -2, 0)},
    {"m": "Te he escondido una ración doble de tarta de chocolate en la nevera por si acaso.", "r1": "'¡Eres la mejor persona de la historia!'", "f1": lambda: [basic_reply("Amor ❤️ ", 10, 0), respuesta_inmediata("Amor ❤️ ", "Lo sé 😎. Date prisa.")], "r2": "'Me hará falta para revivir después de correr.'", "f2": lambda: basic_reply("Amor ❤️ ", 5, 0)},
    {"m": "Tus tíos ya han empezado a debatir de política. Sácame de aquí, no aguanto más.", "r1": "'¡Voy corriendo a rescatarte de ese infierno!'", "f1": lambda: basic_reply("Amor ❤️ ", 5, 0), "r2": "'Hazte la dormida con el teléfono en la mano.'", "f2": lambda: [basic_reply("Amor ❤️ ", 2, 0), respuesta_inmediata("Amor ❤️ ", "Es lo que estoy haciendo ahora mismo... ayuda.")]},
    {"m": "Tu madre me está mirando raro porque no suelto el teléfono de la mano.", "r1": "'Dile que me estás guiando como un controlador aéreo.'", "f1": lambda: basic_reply("Amor ❤️ ", 4, 0), "r2": "'Guárdalo cinco minutos, no la hagamos enfadar.'", "f2": lambda: [basic_reply("Amor ❤️ ", -2, 0), respuesta_inmediata("Amor ❤️ ", "Vale, lo guardo. Escríbeme cuando estés cerca.")]},
    {"m": "Amorrr ven yaaa que tengo hambreeee", "r1": "'¡ESTOY CORRIENDO, NO TE COMAS LA MESA!'", "f1": lambda: [basic_reply("Amor ❤️ ", 5, 0), respuesta_inmediata("Amor ❤️ ", "Ay que tonterias dices, date prisa")], "r2": "'Me quedan unos minutos, aguanta un poco.'", "f2": lambda: basic_reply("Amor ❤️ ", -2, 0)}
]

POOL_GUILLE_PROGRESIVO = [
    {"m": "Acuérdate de pedirle el número al viejo de la tienda por si tiene vinilos guapos.", "r1": "'Hecho, si veo algo interesante te pego un toque.'", "f1": lambda: [basic_reply("Bro Guille", 5, 0), respuesta_inmediata("Bro Guille", "¡Dpm! Eres un grande.")], "r2": "'No estoy para vinilos ahora... voy asfixiado.'", "f2": lambda: basic_reply("Bro Guille", -2, 0)},
    {"m": "Si te quedas sin margen de minutos me avisas y paso con la moto a recogerte.", "r1": "'¡Grande! Me guardo el comodín de rescate.'", "f1": lambda: [cambiar_tiempo(5), respuesta_inmediata("Bro Guille", "Guárdalo, a ver si llegas vivo.")], "r2": "'A pie se forjan los héroes, hermano.'", "f2": lambda: basic_reply("Bro Guille", 2, 2)},
    {"m": "¿Estás haciendo speedrun de recados? Ponte W.P.S.I.A.T.W.I.N", "r1": "'Me lo pongo mentalmente, voy a tope.'", "f1": lambda: basic_reply("Bro Guille", 8, 0), "r2": "'Estoy más para la marcha fúnebre ahora mismo.'", "f2": lambda: basic_reply("Bro Guille", -4, 0)},
    {"m": "Si llegas a la tienda y no hay cola, pídele al dueño que te enseñe el vinilo raro de los 80.", "r1": "'¡Lo haré! A ver si hay suerte.'", "f1": lambda: [basic_reply("Bro Guille", 5, 0), respuesta_inmediata("Bro Guille", "¡Eres un crack!")], "r2": "'No me da tiempo a mirar vinilos ahora mismo.'", "f2": lambda: basic_reply("Bro Guille", -2, 0)}
]

POOL_MAMA_PROGRESIVO = [
    {"m": "Hijo, ve con cuidado en los pasos de cebra. Trae la caja sana y sin arañazos.", "r1": "'La protejo con mi vida, mamá.'", "f1": lambda: basic_reply("Mamá 👵", 2, 2), "r2": "'Sí, si, ya voy concentrado.'", "f2": lambda: basic_reply("Mamá 👵", -2, 0)},
    {"m": "No te pares a comer nada de comida basura por la calle, guarda hambre.", "r1": "'Me guardo el apetito para el gran banquete.'", "f1": lambda: [basic_reply("Mamá 👵", 2, 1), respuesta_inmediata("Mamá 👵", "Así me gusta. Hay marisco del bueno.")], "r2": "'Si veo una buena panadería no prometo nada.'", "f2": lambda: basic_reply("Mamá 👵", 3, 0)}
]

POOL_LAURA_PROGRESIVO = [
    {"m": "¡Tío! Los primos de Valencia ya han llegado y están preguntando por ti.", "r1": "'Diles que paciencia, que traigo el regalo VIP.'", "f1": lambda: basic_reply("Prima Laura ✉️", 5, 0), "r2": "'Qué plastas son, decidles que me den diez minutos.'", "f2": lambda: [basic_reply("Prima Laura ✉️", -4, 0), respuesta_inmediata("Prima Laura ✉️", "Jajaja se lo diré tal cual.")]},
    {"m": "La abuela se está poniendo el collar de diamantes caro de herencia.", "r1": "'¡Máxima presión! Aligero la zancada.'", "f1": lambda: cambiar_tiempo(2), "r2": "'Qué nivelazo, que no abran el vino sin mí.'", "f2": lambda: basic_reply("Prima Laura ✉️", 4, 0)}
]

#Historia y eventos del sistema

def mostrar_introduccion(screen):
    clear_terminal()
    screen.bgcolor("#1a1a1a")
    screen.setworldcoordinates(0, 0, 100, 100)
    turtle.tracer(0, 0)
    escritor = turtle.Turtle(); escritor.hideturtle(); escritor.penup(); escritor.color("#f1c40f")
    print("=======================================================================")
    print(f" PRÓLOGO: LA ENCOMIENDA DE {estado_juego['nombre'].upper()}")
    print("=======================================================================\n")
    escribir_consola_lento("Hoy es el 50º aniversario de tus abuelos. Toda la familia ya está reunida en el restaurante.")
    escribir_consola_lento("El regalo principal de la noche, una valiosa y frágil caja de música vintage, te espera en la tienda.")
    escribir_consola_lento("Tus padres han confiado en ti para que la recojas. Un recado sencillo. O eso parecía.")
    escritor.goto(50, 75); escritor.write("=== EL MANDADO DEL ANIVERSARIO ===", align="center", font=("Courier", 14, "bold"))
    escritor.goto(50, 52); escritor.write("Hoy es el 50º aniversario de tus abuelos. La familia espera.", align="center", font=("Arial", 10, "normal"))
    escritor.goto(50, 42); escritor.write("La valiosa caja de música de regalo te espera en la tienda antigua.", align="center", font=("Arial", 10, "normal"))
    turtle.update(); time.sleep(1.5); escritor.clear()
    escribir_consola_lento("\nPero hay un problemilla crítico: el dueño de la tienda de antigüedades echa el cierre PRONTO.")
    escribir_consola_lento(f"Tienes exactamente {estado_juego['tiempo']} minutos. La ciudad es un laberinto infernal en hora punta.")
    print("\n-----------------------------------------------------------------------")
    escritor.color("#e74c3c"); escritor.goto(50, 60); escritor.write(f"TIENES {estado_juego['tiempo']} MINUTOS. NO FALLES A LA FAMILIA.", align="center", font=("Arial", 11, "bold"))
    turtle.update(); time.sleep(1.5); escritor.clear()

def verificar_cambio_de_acto(dist_meta):
    if dist_meta > 65 and "ACTO_I" not in historia_flags["actos_vistos"]:
        historia_flags["actos_vistos"].append("ACTO_I")
        print("\n" + "="*70)
        escribir_consola_lento("[HISTORIA - ACTO I: LA ESCAPADA DEL BARRIO]")
        print("="*70)
        escribir_consola_lento("Cierras la puerta del portal de un golpe sordo. El sol empieza a caer y tiñe las nubes de naranja.")
        escribir_consola_lento("La presión de la familia se palpa en el ambiente. Tienes la dirección anotada en un papel arrugado.")
        escribir_consola_lento("Cruzas la primera gran avenida respirando hondo, confiando en que la ciudad colabore hoy.")
        print("="*70)
        input("\n[PULSA ENTER PARA DAR EL PRIMER PASO]")
        clear_terminal()
    elif 30 <= dist_meta <= 65 and "ACTO_II" not in historia_flags["actos_vistos"]:
        historia_flags["actos_vistos"].append("ACTO_II")
        print("\n" + "="*70)
        escribir_consola_lento("[HISTORIA - ACTO II: EL LABERINTO DE CEMENTO]")
        print("="*70)
        escribir_consola_lento("El enorme horizonte de los edificios de oficinas tapa la luz directa del sol atardeciendo.")
        escribir_consola_lento("El aire de repente huele a humo de tubo de escape y a prisa masiva. Estás en el centro neurálgico.")
        escribir_consola_lento("Miras el reloj de tu muñeca de reojo: la cuenta atrás avanza de forma completamente implacable.")
        print("="*70)
        input("\n[PULSA ENTER PARA CONTINUAR]")
        clear_terminal()
    elif dist_meta < 30 and "ACTO_III" not in historia_flags["actos_vistos"]:
        historia_flags["actos_vistos"].append("ACTO_III")
        print("\n" + "="*70)
        escribir_consola_lento("[HISTORIA - ACTO III: LA RECTA FINAL]")
        print("="*70)
        escribir_consola_lento("Divisas a lo lejos los toldos clásicos de rayas del distrito histórico de los anticuarios.")
        escribir_consola_lento("La meta está al alcance de tus ojos, pero tus piernas pesan toneladas tras tanto asfalto.")
        escribir_consola_lento("Usa todo lo que has aprendido. Ahora o nunca. O eres el héroe de la cena, o el gran proscrito.")
        print("="*70)
        input("\n[PULSA ENTER PARA DAR EL EMPUJÓN FINAL DE LA NOCHE]")
        clear_terminal()

def verificar_notificaciones_automaticas():
    
    if "EMPAPADO" in historia_flags["estados_personaje"] and not tramas["empapado_chat"]:
        tramas["empapado_chat"] = True
        opc = {
            "1": {"texto": "Sí, me estoy empapando y mi traje está arruinado.", "fx": lambda: basic_reply("Mamá 👵", -5, 0)},
            "2": {"texto": "De momento aguanto bien, no te agobies mamá.", "fx": lambda: basic_reply("Mamá 👵", 2, 0)}
        }
        enviar_mensaje("Mamá 👵", "Hijo, dicen en las noticias que hay charcos enormes por el centro comercial, ¿te estás manchando?", opc, typing=True)

    if "COJO" in historia_flags["estados_personaje"] and not tramas["cojo_chat"]:
        tramas["cojo_chat"] = True
        opc = {
            "1": {"texto": "Me he dado un golpe tremendo en la pierna, no puedo correr.", "fx": lambda: basic_reply("Prima Laura ✉️", -5, 0)},
            "2": {"texto": "Guille es un exagerado que ve visiones, estoy perfectamente.", "fx": lambda: basic_reply("Prima Laura ✉️", 2, 0)}
        }
        enviar_mensaje("Prima Laura ✉️", "Tío, ¿por qué andas tan raro por la calle? Guille me ha dicho por Instagram que te vio cojeando en una esquina.", opc, typing=True)

    if "INSOLACION" in historia_flags["estados_personaje"] and not tramas["insolacion_chat"]:
        tramas["insolacion_chat"] = True
        opc = {
            "1": {"texto": "Me da vueltas todo, el sol de las obras me ha matado.", "fx": lambda: basic_reply("Amor ❤️ ", -10, 0)},
            "2": {"texto": "Hace calor pero sobrevivo como un guerrero.", "fx": lambda: basic_reply("Amor ❤️ ", 5, 0)}
        }
        enviar_mensaje("Amor ❤️ ", "Oye mi vida, hace unos 35 grados ahí fuera en el asfalto. ¿Te estás hidratando bien? Me preocupas.", opc, typing=True)

#Mapa turtle

def generar_distritos_ciudad():
    if estado_juego["px"] < 50: estado_juego["meta_x"] = random.randint(85, 97)
    else: estado_juego["meta_x"] = random.randint(3, 15)
    if estado_juego["py"] < 50: estado_juego["meta_y"] = random.randint(85, 97)
    else: estado_juego["meta_y"] = random.randint(3, 15)
        
    park = {"x1": random.randint(25, 45), "y1": random.randint(25, 45)}
    park["x2"], park["y2"] = park["x1"] + 32, park["y1"] + 32
    obras = {"x1": random.randint(20, 55), "y1": random.randint(20, 55)}
    obras["x2"], obras["y2"] = obras["x1"] + 22, obras["y1"] + 22
    return park, obras

def dibujar_manzanas_ciudad(pintor, park, obras):
    for x in range(0, 100, 3):
        for y in range(0, 100, 3):
            cx, cy = x + 1.1, y + 1.1
            color = "#bdc3c7"
            if park["x1"] <= cx <= park["x2"] and park["y1"] <= cy <= park["y2"]: color = "#2ecc71"
            elif obras["x1"] <= cx <= obras["x2"] and obras["y1"] <= cy <= obras["y2"]: color = "#e67e22"
            pintor.penup(); pintor.goto(x, y); pintor.color(color); pintor.begin_fill()
            for _ in range(4): pintor.forward(2.2); pintor.left(90)
            pintor.end_fill()

# Encuentros narrativos

def procesar_encuentro_profundo():
    """Diálogos ramificados. Pausan el mapa."""
    encuentros_posibles = ["PROFESOR", "MANIFESTACION", "MUSICO", "TURISTA"]
    disponibles = [e for e in encuentros_posibles if e not in historia_flags["encuentros_profundos_vistos"]]
    
    if not disponibles: return False
    encuentro = random.choice(disponibles)
    historia_flags["encuentros_profundos_vistos"].append(encuentro)
    
    clear_terminal()
    print("\n" + "★"*65)
    print("                ENCUENTRO URBANO                 ")
    print("★"*65 + "\n")
    
    if encuentro == "PROFESOR":
        escribir_consola_lento("Mientras caminas, chocas hombro con hombro con un hombre mayor.")
        escribir_consola_lento("Se le caen unos pesados libros. Al mirarle, te das cuenta de que es Don Alberto,")
        escribir_consola_lento("tu antiguo profesor de matemáticas, que siempre preguntaba por tus abuelos.")
        print("\nDon Alberto: '¡Pero bueno, si es el nieto de los mayores de la plaza! ¿A dónde vas tan rápido?'")
        print("\n[1] Ayudarle a recoger los libros y charlar con él (Pierdes 4 mins).")
        print("[2] Pedirle disculpas rápidas y salir corriendo (0 mins).")
        ch = input("\nElige (1-2): ").strip()
        
        if ch == "1":
            cambiar_tiempo(-4)
            print("\nTe agachas y le ayudas. Él sonríe cálidamente.")
            escribir_consola_lento("Don Alberto: 'Muchas gracias... oye, ¿y cómo está tu abuelo Pepe de la rodilla?'")
            print("\n[1] 'Está genial, de hecho voy a por su regalo de bodas de oro.'")
            print("[2] 'Profe, me alegro de verle pero tengo una prisa criminal.'")
            ch2 = input("\nElige (1-2): ").strip()
            
            if ch2 == "1":
                escribir_consola_lento("\nDon Alberto: '¡Cincuenta años! Qué maravilla. Mira, corta por los callejones detrás")
                escribir_consola_lento("de la vieja iglesia. No hay coches y llegarás en nada.'")
                historia_flags["misiones_activas"]["CALLEJON_ABUELO"] = "ACTIVADA"
                cambiar_animo(20); cambiar_karma(5)
                print("\n-> Has sido amable. Desbloqueas los Callejones Ocultos (70, 40) y ganas +20% Ánimo.")
            else:
                escribir_consola_lento("\nDon Alberto: 'Vaya... la juventud de hoy, siempre corriendo. Cuídate.'")
                print("\n-> Se aparta ofendido. Ahorras tiempo pero pierdes la recompensa.")
        else:
            print("\nLe dejas con la palabra en la boca. Sientes una punzada en el estómago.")
            cambiar_animo(-20); cambiar_karma(-5)
            print("-> Ahorras tiempo, pero tu conciencia te destroza (-20% Ánimo).")
            
    elif encuentro == "MANIFESTACION":
        escribir_consola_lento("Giras una esquina y te topas con una manifestación masiva bloqueando la avenida.")
        escribir_consola_lento("Están protestando por el cierre del parque local. Los antidisturbios bloquean el paso.")
        print("\n[1] Intentar abrirte paso a la fuerza entre los escudos.")
        print("[2] Hablar con una de las manifestantes del megáfono.")
        ch = input("\nElige (1-2): ").strip()
        
        if ch == "1":
            escribir_consola_lento("\nEmpiezas a dar codazos. Un agente te frena en seco con el escudo de plástico.")
            escribir_consola_lento("Agente: '¡Atrás, chaval! Zona acordonada, no pasa nadie.'")
            print("\n[1] '¡Aparta, tengo que ir a la tienda por mis abuelos!' (Empujar)")
            print("[2] 'Perdone agente, doy la vuelta.' (Retroceder)")
            ch2 = input("\nElige (1-2): ").strip()
            if ch2 == "1":
                escribir_consola_lento("\nEl policía te da un barrido de piernas. Caes al asfalto doliéndote de todo.")
                historia_flags["estados_personaje"].append("COJO"); cambiar_animo(-25); cambiar_karma(-5)
                print("\n-> Cruzas la línea, pero te han reventado. Ganas estado COJO, -25% Ánimo.")
            else:
                cambiar_tiempo(-4)
                print("\n-> Das un rodeo de 4 minutos, pero sales ileso del altercado.")
        else:
            escribir_consola_lento("\nTe acercas a una chica joven con un megáfono y un chaleco verde.")
            escribir_consola_lento("Chica: 'Oye, ¿tú también estás en contra de la tala de los sauces?'")
            print("\n[1] 'A tope. Los árboles son la vida del barrio.'")
            print("[2] 'Me da igual, solo quiero cruzar la calle, déjame pasar.'")
            ch2 = input("\nElige (1-2): ").strip()
            if ch2 == "1":
                escribir_consola_lento("\nChica: '¡Así se habla! Toma, cruza por nuestra carpa médica para atajar.'")
                cambiar_animo(15); cambiar_karma(3)
                print("\n-> Te dan una botella de agua y te dejan atajar (+15% Ánimo).")
            else:
                cambiar_tiempo(-5)
                print("\n-> Te ignoran y tienes que bordear a toda la multitud (Pierdes 5 minutos).")

    elif encuentro == "MUSICO":
        escribir_consola_lento("Llegas a una plaza. Un joven está tocando el violonchelo maravillosamente.")
        print("\n[1] Sentarte a escucharle un rato (Pierdes 3 mins).")
        print("[2] Apretar el paso ignorando la música (0 mins).")
        ch = input("\nElige (1-2): ").strip()
        
        if ch == "1":
            cambiar_tiempo(-3)
            escribir_consola_lento("\nEl músico termina la pieza, te mira y sonríe.")
            escribir_consola_lento("Músico: 'Veo que vas estresado. ¿Tienes alguna petición especial para hoy?'")
            print("\n[1] 'Toca algo muy alegre, necesito energía para llegar.'")
            print("[2] 'Toca algo épico, como de película de héroes.'")
            ch2 = input("\nElige (1-2): ").strip()
            
            escribir_consola_lento("\nEl músico asiente y empieza a tocar magistralmente.")
            if ch2 == "1":
                cambiar_animo(25); cambiar_karma(2)
                print("-> La melodía feliz te llena de vitalidad pura (+25% Ánimo).")
            else:
                cambiar_animo(20); cambiar_karma(2); estados = historia_flags["estados_personaje"]
                if "ESTRESADO" in estados: estados.remove("ESTRESADO")
                print("-> La épica te quita todo el estrés acumulado de golpe (+20% Ánimo).")
        else:
            print("\nEl sonido se desvanece a tu espalda. Ahorras tiempo, pero sigues tenso.")

    elif encuentro == "TURISTA":
        escribir_consola_lento("Un turista con un mapa enorme de papel te corta el paso desesperado.")
        escribir_consola_lento("Turista: 'Excuse me, I need to find the Gothic Quarter, am I close?'")
        print("\n[1] Dedicar tiempo a explicarle en inglés (Pierdes 2 mins).")
        print("[2] 'I don't speak English, sorry' y seguir caminando.")
        ch = input("\nElige (1-2): ").strip()
        if ch == "1":
            cambiar_tiempo(-2)
            print("\nTurista: 'Oh, thank you so much! Here, take this souvenir pin.'")
            cambiar_karma(4); cambiar_animo(10)
            print("-> El buen karma te inunda el pecho (+4 Karma, +10% Ánimo).")
        else:
            cambiar_karma(-4)
            print("\nTurista: 'Oh... okay, hope this doesn't affect Tesco opening times.'")
            print("\n-> El turista se queda refunfuñando. Ganas tiempo, pierdes decencia (-4 Karma).")

    print("\n" + "★"*65)
    input("[PULSA ENTER PARA CONTINUAR TU RUTA]")
    clear_terminal()
    return True

# Eventos de estado y narrativa

def inyectar_narrativa_viva_turno():
    turno = estado_juego["turno_actual"]
    nombre = estado_juego["nombre"]
    estados = historia_flags["estados_personaje"]
    
    # Actualizar estados
    if estado_juego["animo"] <= 40 and "ESTRESADO" not in estados: estados.append("ESTRESADO")
    elif estado_juego["animo"] > 40 and "ESTRESADO" in estados: estados.remove("ESTRESADO")
    if estado_juego["karma_urbano"] >= 8 and "RITMO_ZEN" not in estados: estados.append("RITMO_ZEN")
    elif estado_juego["karma_urbano"] < 8 and "RITMO_ZEN" in estados: estados.remove("RITMO_ZEN")

    # TRAMAS OBLIGATORIAS
    if turno == 3 and not tramas["amor_trama_iniciada"]:
        tramas["amor_trama_iniciada"] = True
        opc = {"1": {"texto": "El vestido azul.", "fx": lambda: resolver_amor_trama(1)}, "2": {"texto": "El traje oscuro.", "fx": lambda: resolver_amor_trama(1)}}
        enviar_mensaje("Amor ❤️ ", "Vida, ¿qué me pongo para la fiesta? ¿El vestido azul o el traje oscuro?", opc, typing=True)

    if tramas["amor_fase"] == 1.5:
        tramas["amor_timer_ghosting"] += 1
        if tramas["amor_timer_ghosting"] >= 2:
            opc = {"1": {"texto": "11/10, espectacular.", "fx": lambda: resolver_amor_trama(2)}, "2": {"texto": "Me encanta.", "fx": lambda: resolver_amor_trama(2)}}
            enviar_mensaje("Amor ❤️ ", f"Mira, me he puesto lo que dijiste. {FONDO_VERDE}[FOTO.jpg]{RESET} ¿Nota del 1 al 10?", opc, typing=True)
            tramas["amor_fase"] = 2


    if "ACTO_II" in historia_flags["actos_vistos"] and tramas["amor_fase"] == 2.5:
        opc = {"1": {"texto": "¡Dile que no salga!", "fx": lambda: resolver_amor_trama(3, 5)}, "2": {"texto": "El tráfico es un caos, asumo el riesgo.", "fx": lambda: resolver_amor_trama(3, -5)}}
        enviar_mensaje("Amor ❤️ ", "Oye, ¿por dónde vas? Mi madre se está alterando y quiere coger el coche para ir a buscarte.", opc, typing=True)
        tramas["amor_fase"] = 3
        tramas["amor_timer_ghosting"] = 0
        
    # El Ghosting es muy malo muy malo
    # Usa las claves de FICHA_AMOR_EVOLUTIVO 
    # Este flujo está diseñado con un contador de turnos (t)
    # Ignorar los mensajes creará un atasco alrededor de la tienda de antigüedades y hará que el paso por los cuadrantes cueste el triple de tiempo.
    # Las respuestas son bastante realistas y están basadas en mi novia en la vida real.
    if tramas["amor_fase"] == 3 and not tramas["amor_trama_resuelta"]:
        if chats_data["Amor ❤️ "]["pending_options"]:
            tramas["amor_timer_ghosting"] += 1
            t = tramas["amor_timer_ghosting"]
            
            
            if t == 2 and 2 in FICHA_AMOR_EVOLUTIVO:
                enviar_mensaje("Amor ❤️ ", FICHA_AMOR_EVOLUTIVO[2]["m"], typing=True)
                cambiar_animo(-5)
                
            
            elif t == 4 and 3 in FICHA_AMOR_EVOLUTIVO:
                enviar_mensaje("Amor ❤️ ", FICHA_AMOR_EVOLUTIVO[3]["m"], typing=True)
                cambiar_animo(-10)
                
            
            elif t >= 6 and not historia_flags["atasco_meta"]:
                historia_flags["atasco_meta"] = True
                chats_data["Amor ❤️ "]["pending_options"] = {} 
                tramas["amor_trama_resuelta"] = True
                
                if 4 in FICHA_AMOR_EVOLUTIVO:
                    enviar_mensaje("Amor ❤️ ", FICHA_AMOR_EVOLUTIVO[4]["m"], typing=True)
                
                print(f"\n🚨 {ROJO}[CONSECUENCIA POR GHOSTING]{RESET}: Has ignorado los mensajes demasiado tiempo.")
                print("Tu suegra ha sacado el coche del garaje presa del pánico y ha colapsado la zona del centro neurálgico.")
                print("¡El paso por los cuadrantes adyacentes a la tienda de antigüedades costará el TRIPLE de tiempo!")
                cambiar_animo(-20)
                
                
                p = turtle.Turtle()
                p.hideturtle()
                p.penup()
                p.color("#e74c3c")
                p.pensize(3.5)
                p.goto(estado_juego["meta_x"] - 12, estado_juego["meta_y"] - 12)
                p.pendown()
                for _ in range(4): 
                    p.forward(24)
                    p.left(90)
                turtle.update()
                
                input("\n[PULSA ENTER PARA VOLVER A LA CALLE]")
                clear_terminal()

    if turno == 7 and not tramas["guille_trama_iniciada"]:
        tramas["guille_trama_iniciada"] = True
        opc = {"1": {"texto": "Hecho bro, me desvío a (40, 20).", "fx": lambda: resolver_guille(True)}, "2": {"texto": "Imposible, voy fatal.", "fx": lambda: resolver_guille(False)}}
        enviar_mensaje("Bro Guille", f"Socio, en {FONDO_AZUL}Disco-Metrópolis (40, 20){RESET} queda el último disco de Humbug. ¡Si te desvías mi hermano te lleva en furgo a la meta!", opc, typing=True)

    #Mensajes aleatorios
    if random.randint(1, 100) <= 50:
        for c, data in random.sample(list(chats_data.items()), len(chats_data)):
            if not data["unread"] and not data["pending_options"]:
                if c == "Bro Guille" and historia_flags["guille_bloqueado"]: continue
                nodo = None
                
                if c == "Amor ❤️ " and tramas["amor_trama_resuelta"] and historia_flags["ptr_amor"] < len(POOL_AMOR_PROGRESIVO):
                    nodo = POOL_AMOR_PROGRESIVO[historia_flags["ptr_amor"]]; historia_flags["ptr_amor"] += 1
                elif c == "Bro Guille" and historia_flags["ptr_guille"] < len(POOL_GUILLE_PROGRESIVO):
                    nodo = POOL_GUILLE_PROGRESIVO[historia_flags["ptr_guille"]]; historia_flags["ptr_guille"] += 1
                elif c == "Mamá 👵" and historia_flags["ptr_mama"] < len(POOL_MAMA_PROGRESIVO):
                    nodo = POOL_MAMA_PROGRESIVO[historia_flags["ptr_mama"]]; historia_flags["ptr_mama"] += 1
                elif c == "Prima Laura ✉️" and historia_flags["ptr_laura"] < len(POOL_LAURA_PROGRESIVO):
                    nodo = POOL_LAURA_PROGRESIVO[historia_flags["ptr_laura"]]; historia_flags["ptr_laura"] += 1
                
                if nodo:
                    opc = {"1": {"texto": nodo["r1"], "fx": nodo["f1"]}, "2": {"texto": nodo["r2"], "fx": nodo["f2"]}}
                    enviar_mensaje(c, nodo["m"], opc, typing=True)
                    break 

    # MONÓLOGOS INTERNOS
    if not any(data["unread"] for data in chats_data.values()):
        if random.randint(1, 100) <= 15:
            print("\n" + "~"*65)
            pool_actual = list(POOL_PENSAMIENTOS)
            if "EMPAPADO" in estados: pool_actual.insert(0, "Siento el asqueroso lodo del charco metido en el zapato.")
            if "INSOLACION" in estados: pool_actual.insert(0, "Me da vueltas la cabeza, el sol de las obras me marea.")
            
            idx = historia_flags["ptr_pensamiento"] % len(pool_actual)
            print(f"[PENSAMIENTO DE {nombre.upper()}]: '{pool_actual[idx]}'")
            historia_flags["ptr_pensamiento"] += 1
            print("~"*65)

# Menú del móvil y apps

def abrir_smartphone():
    while True:
        print("\n┌───────────────────────────────────────────────────────────┐")
        print("│                      📱 MÓVIL                             │")
        print("├───────────────────────────────────────────────────────────┤")
        print("│  [1] 🗺️  Google Maps                                       │")
        print("│  [2] 💬  WhatsApp                                         │")
        print("│  [3] 🎒  Mochila                                          │")
        print("│  [4] 📞  Llamada de Emergencia (Contactos)                │")
        print("│  [5] ❌  Guardar Teléfono en el Bolsillo                  │")
        print("└───────────────────────────────────────────────────────────┘")
        op = input("Selecciona app: ").strip()
        if op == "1": mostrar_radar_gps_terminal()
        elif op == "2": hub_whatsapp()
        elif op == "3": menu_mochila_fisica()
        elif op == "4": menu_contactos_emergencia()
        elif op == "5": break

def mostrar_radar_gps_terminal():
    print("\n┌───────────────────────────────────────────────────────────┐")
    print("│                           GPS                             │")
    print("├───────────────────────────────────────────────────────────┤")
    pois = {"Tienda Destino": (estado_juego["meta_x"], estado_juego["meta_y"]), "Metro Central": (30, 30)}
    if historia_flags["misiones_activas"].get("AYUDA_TIO") == "ACTIVADA": pois["Oficina Tío Alberto"] = (30, 50)
    if historia_flags["misiones_activas"].get("CALLEJON_ABUELO") == "ACTIVADA": pois["Callejones Ocultos"] = (70, 40)
    
    # Imprimir los puntos de interés de la ciudad
    for n, coords in pois.items():
        dist = math.hypot(coords[0] - estado_juego["px"], coords[1] - estado_juego["py"])
        rumbo = calcular_rumbo_exacto(estado_juego["px"], estado_juego["py"], coords[0], coords[1])
        
        
        info_punto = f" • {n} ({int(coords[0])}, {int(coords[1])})"
        
        
        linea_interna = f"{info_punto:<34} : A {round(dist, 1):>4} blq. rumbo [{rumbo:>2}]"
        print(f"│{linea_interna}│")
        
    
    if historia_flags["misiones_activas"].get("VINILO_GUILLE") == "ACTIVADA":
        coords = (40, 20)
        dist = math.hypot(coords[0] - estado_juego["px"], coords[1] - estado_juego["py"])
        rumbo = calcular_rumbo_exacto(estado_juego["px"], estado_juego["py"], coords[0], coords[1])
        
        info_guille = f" • Disco-Metrópolis ({coords[0]}, {coords[1]})"
        linea_guille = f"{info_guille:<34} : A {round(dist, 1):>4} blq. rumbo [{rumbo:>2}]"
        print(f"│{FONDO_AZUL}{linea_guille}{RESET}│")
        
    print("│                                                           │")
    print("│ Brújula: W=Norte, S=Sur, A=Oeste, D=Este                  │")
    print("└───────────────────────────────────────────────────────────┘")
    input("\n[PULSA ENTER PARA VOLVER]")

def hub_whatsapp():
    while True:
        clear_terminal()
        print("\n┌───────────────────────────────────────────────────────────┐")
        print("│                       💬 WHATSAPP                         │")
        print("├───────────────────────────────────────────────────────────┤")
        contactos = ["Amor ❤️ ", "Bro Guille", "Mamá 👵", "Prima Laura ✉️"]
        for i, c in enumerate(contactos, 1):
            badge = "[NUEVO 🔴]" if chats_data[c]["unread"] else ""
            if c == "Bro Guille" and historia_flags["guille_bloqueado"]: badge = "[Bloqueado 🚫]"
            print(f"│  [{i}] {c} {badge}")
        print("│  [5] ⬅️  Volver al menú del teléfono                      │")
        print("└───────────────────────────────────────────────────────────┘")
        ch = input("Abrir chat (1-5): ").strip()
        try:
            if 1 <= int(ch) <= 4: ver_chat_individual(contactos[int(ch) - 1])
            elif int(ch) == 5: break
        except ValueError: pass

def ver_chat_individual(contacto):
    clear_terminal()
    print(f"\n--- 💬 CHAT PRIVADO: {contacto} ---")
    chats_data[contacto]["unread"] = False
    
    if not chats_data[contacto]["historial"]: print("  No hay mensajes recientes.")
    else:
        for msg in chats_data[contacto]["historial"][-6:]: print("  " + msg)
            
    opc = chats_data[contacto].get("pending_options")
    if opc:
        print("\nElige tu respuesta textual:")
        for k, v in opc.items(): print(f"  [{k}] {v['texto']}")
        ch = input("\nEnviar opción numérica: ").strip()
        if ch in opc:
            chats_data[contacto]["historial"].append("Tú: " + opc[ch]["texto"])
            print("\n-> Mensaje entregado con doble check.")
            opc[ch]["fx"]() 
        else:
            print("\nOpción inválida. El mensaje se ha quedado en borrador.")
            chats_data[contacto]["unread"] = True 
    input("\n[PULSA ENTER PARA SALIR DEL CHAT]")

def menu_mochila_fisica():
    print("\n--- 🎒 MOCHILA (INVENTARIO) ---")
    if not historia_flags["mochila"]: print("  Inventario vacío.")
    else:
        for idx, obj in enumerate(historia_flags["mochila"], 1):
            cant = f" ({historia_flags['cruasanes_cantidad']} uds)" if obj == "CRUASANES" else ""
            print(f"  [{idx}] {obj}{cant}")
        print("\n¿Deseas consumir o equipar algo?")
        print("  [1] Comer Cruasán (+30% Ánimo)\n  [2] Beber AGUA_HELADA (Cura Insolación)\n  [3] Cancelar")
        op = input("Elige: ").strip()
        if op == "1" and "CRUASANES" in historia_flags["mochila"]:
            if historia_flags["cruasanes_cantidad"] > 0:
                historia_flags["cruasanes_cantidad"] -= 1; cambiar_animo(30)
                print(f"\nTe comes un cruasán artesanal. Quedan {historia_flags['cruasanes_cantidad']}.")
                if historia_flags["cruasanes_cantidad"] == 0: historia_flags["mochila"].remove("CRUASANES")
        elif op == "2" and "AGUA_HELADA" in historia_flags["mochila"]:
            historia_flags["mochila"].remove("AGUA_HELADA")
            if "INSOLACION" in historia_flags["estados_personaje"]:
                historia_flags["estados_personaje"].remove("INSOLACION")
                print("\nBebes el agua. INSOLACION curada.")
    input("\n[PULSA ENTER PARA VOLVER]")

def menu_contactos_emergencia():
    print("\n--- 📞 AGENDA TELEFÓNICA---")
    if historia_flags["javi_contacto"]: print("  [2] Javi (Motorista Exprés - Coste: 1 min)")
    else: print("  No tienes a nadie registrado.")
    op = input("[1] Colgar | Marcar número: ").strip()
    if op == "2" and historia_flags["javi_contacto"]:
        if "ACTO_III" in historia_flags["actos_vistos"] and estado_juego["tiempo"] <= 12:
            if historia_flags["guille_bloqueado"]:
                print("\nComunica. Guille le ha dicho a Javi que pase de ti por egoísta.")
            else:
                print("\n[EFECTO MARIPOSA]: Javi acude derrapando montado en la scooter.")
                estado_juego["px"], estado_juego["py"] = estado_juego["meta_x"], estado_juego["meta_y"]
                estado_juego["tiempo"] = max(1, estado_juego["tiempo"] - 1)
                print("-> ¡Te subes atrás y te deja en la meta de la TIENDA en 1 minuto!")
        else:
            print("\nJavi: '¡Buenas chaval! Estoy liado en el taller, avisa si la cosa es crítica al final.'")
    input("\n[ENTER PARA VOLVER]")

#Eventos aleatorios

def ejecutar_evento_aleatorio(zona):
    if estado_juego["cooldown_eventos"] > 0: return
    if random.randint(1, 100) > 35: return
    estado_juego["cooldown_eventos"] = 3
    print("\n⚠️ [EVENTO ALEATORIO] ⚠️")
    estados = historia_flags["estados_personaje"]
    
    if zona == "PARQUE":
        ev = random.choice([1, 2])
        if ev == 1:
            print("Un ganso colosal te corta el paso.")
            if registro_secretos["gatos_fijos"] > 0 and registro_secretos["tipo_gato_actual"] == "PROTECTOR":
                print("\n[DEFENSA FELINA]: Tu gato protector bufa y el ave gigante huye.")
                return
            print("[1] Espantarlo a gritos\n[2] Dar un rodeo por el césped (2 min)")
            if "CRUASANES" in historia_flags["mochila"]: print("[3] Lanzarle un valioso cruasán como soborno")
            ch = input("Elige acción: ").strip()
            if ch == "3" and "CRUASANES" in historia_flags["mochila"]:
                historia_flags["cruasanes_cantidad"] -= 1
                if historia_flags["cruasanes_cantidad"] == 0: historia_flags["mochila"].remove("CRUASANES")
                historia_flags["ganso_aliado"] = True
                print("-> El ganso huele la mantequilla y devora el hojaldre. ¡Es tu aliado!")
            elif ch == "2":
                cambiar_tiempo(-2); print("-> Pierdes 2 minutos rodeando el fango.")
            else:
                if random.randint(1, 100) <= 60:
                    estados.append("COJO"); cambiar_animo(-15); cambiar_karma(-2)
                    print("-> ¡Mala decisión! Te mete un picotazo sangrante. Secuela: COJO.")
                else: print("Logras espantarlo agitando los brazos. Pasas libre.")
        elif ev == 2:
            print("Encuentras un perro Golden Retriever llorando con la correa rota.")
            print("[1] Perder 6 inmensos minutos rescatándolo\n[2] Ignorarlo por prisa")
            ch = input("Elige: ").strip()
            if ch == "1":
                cambiar_tiempo(-6); cambiar_animo(15); cambiar_karma(4); historia_flags["heroe_canino"] = True
                print("-> ¡Dueño localizado! El cartero te abraza. Bandera: HEROE_CANINO.")
            else:
                cambiar_animo(-10); cambiar_karma(-3); print("-> Remordimiento en tu pecho.")
                
    elif zona == "OBRAS":
        ev = random.choice([1, 2])
        if ev == 1:
            print("El rudo capataz te frena: una enorme grúa mueve vigas de acero ardiendo.")
            print("[1] Esperar cívicamente bajo un andamio (3 min)\n[2] Colarte saltando las vallas")
            ch = input("Elige vía: ").strip()
            if ch == "1":
                cambiar_tiempo(-3); cambiar_karma(2); historia_flags["mochila"].append("AGUA_HELADA")
                print("-> El capataz te obsequia una botella de AGUA_HELADA.")
            else:
                estados.append("INSOLACION"); cambiar_karma(-2)
                print("-> El esfuerzo físico te da un golpe de calor brutal: INSOLACION.")
        elif ev == 2:
            print("Un enorme charco de cemento fresco bloquea la acera.")
            print("[1] Rodear la manzana por precaución (4 min)\n[2] Intentar saltarlo a la pata coja")
            ch = input("Elige: ").strip()
            if ch == "1":
                cambiar_tiempo(-4); print("-> Pierdes tiempo pero mantienes los zapatos limpios.")
            else:
                if random.randint(1,100) > 50:
                    cambiar_animo(-15); estados.append("EMPAPADO")
                    print("-> ¡Splash! Te hundes en el cemento. Secuela: EMPAPADO.")
                else:
                    print("-> Logras un salto olímpico. Pasas limpio.")
    else: 
        ev = random.choice([1, 2, 3, 4])
        if ev == 1 and not registro_secretos["gato_en_cortejo"]:
            print("Un pequeño gato callejero de profundos ojos brillantes te maúlla.")
            registro_secretos["gato_en_cortejo"] = True
            registro_secretos["turnos_con_gato_actual"] = 1
            registro_secretos["tipo_gato_actual"] = random.choice(["PROTECTOR", "ASUSTADIZO", "GLOTON", "LIDER"])
            cambiar_animo(10)
            print(f"-> Senda natural felina iniciada. Gato de clase: {registro_secretos['tipo_gato_actual']}.")
        elif ev == 2:
            print("Un taxi amarillo pasa zumbando sobre un bache salpicándote de lodo.")
            estados.append("EMPAPADO"); cambiar_animo(-15)
            print("-> ¡Tu maravillosa ropa está manchada irremediablemente! Secuela: EMPAPADO.")
        elif ev == 3:
            print("Un ladrón escurridizo pasa corriendo y choca contra ti, tirándote al suelo.")
            print("[1] Perseguirle para recuperar orgullo (4 min)\n[2] Levantarte y sacudirte")
            ch = input("Elige: ").strip()
            if ch == "1":
                cambiar_tiempo(-4); cambiar_karma(3); cambiar_animo(15)
                print("-> Le alcanzas y le das un buen susto. Recuperas la moral.")
            else:
                cambiar_animo(-10); print("-> El choque te deja el cuerpo cortado y sucio.")
        elif ev == 4:
            print("Unos metros adelante pasas por la fachada de la nueva Panadería Central. El aroma es increíble.")
            print("[1] Entrar a comprar una caja de cruasanes finos (3 min)\n[2] Pasar de largo")
            ch = input("Elige: ").strip()
            if ch == "1":
                cambiar_tiempo(-3)
                if "INSOLACION" in estados and "AGUA_HELADA" not in historia_flags["mochila"] and random.randint(1,100)<=30:
                    cambiar_animo(-30)
                    print("\n-> ¡Desastroso contratiempo físico! Los mareos te hacen tropezar. ¡Los dulces estallan en el suelo!")
                else:
                    if "CRUASANES" not in historia_flags["mochila"]: historia_flags["mochila"].append("CRUASANES")
                    historia_flags["cruasanes_cantidad"] += 4
                    print(f"\n-> Sales cargando con inmenso éxito una caja con {historia_flags['cruasanes_cantidad']} cruasanes.")

    print("\n" + "─"*50)
    input("[PULSA ENTER PARA REANUDAR EL VIAJE]")
    clear_terminal()

def avanzar_cortejo_gatos():
    probabilities = {1: 90, 2: 60, 3: 45, 4: 30}
    turno_gato = registro_secretos["turnos_con_gato_actual"]
    prob_permanecer = probabilities.get(turno_gato, 30)
    if turno_gato == 1 and historia_flags["heroe_canino"]: prob_permanecer -= 20
    if registro_secretos["tipo_gato_actual"] == "LIDER": prob_permanecer += 15 
        
    if random.randint(1, 100) <= prob_permanecer:
        if turno_gato == 4:
            registro_secretos["gatos_fijos"] += 1
            registro_secretos["gato_en_cortejo"] = False
            registro_secretos["turnos_con_gato_actual"] = 0
            print(f"\n🐱 ¡Domesticado! El gato de clase {registro_secretos['tipo_gato_actual']} se une a tu retaguardia.")
        else:
            registro_secretos["turnos_con_gato_actual"] += 1
            print(f"\n🐱 Gato siguiéndote. Nivel de lealtad felina: {registro_secretos['turnos_con_gato_actual']}/4.")
            if registro_secretos["tipo_gato_actual"] == "GLOTON" and "CRUASANES" in historia_flags["mochila"] and historia_flags["cruasanes_cantidad"] > 0:
                if random.randint(1, 100) <= 35:
                    historia_flags["cruasanes_cantidad"] -= 1
                    print("⚠️ ¡ATENCIÓN ROBO! ¡El gato glotón ha metido la pata en la caja y te ha robado un cruasán caliente!")
                    if historia_flags["cruasanes_cantidad"] == 0: historia_flags["mochila"].remove("CRUASANES")
    else:
        registro_secretos["gato_en_cortejo"] = False
        registro_secretos["turnos_con_gato_actual"] = 0
        print("\n🐱 El felino huye asustado por un callejón.")
    input("[PULSA ENTER]")

# Eventos finales y reporte

def imprimir_reporte_final(resultado, motivo):
    clear_terminal()
    
    
    mapeo_hitos = {
        
        "ACTO_I": "Escapaste con éxito de tu barrio natal",
        "ACTO_II": "Te adentraste en el laberinto de cemento central",
        "ACTO_III": "Alcanzaste la recta final del distrito histórico",
        
        "VINILO_GUILLE": "Compraste el vinilo de Guille en la Disco-Metrópolis",
        "AYUDA_TIO": "Te cambiaste de ropa seca con tu tío Alberto",
        "CALLEJON_ABUELO": "Atajaste por los callejones ocultos de la iglesia",
        "POLICIA_VISTO": "Te libraste elegantemente de la patrulla policial",
        
        "PROFESOR": "Te paraste a charlar con tu maestro Don Alberto",
        "MUSICO": "Te detuviste a escuchar al artista del violonchelo",
        "MANIFESTACION": "Lidiaste con la manifestación masiva del parque",
        "TURISTA": "Ayudaste al turista extranjero con tu inglés"
    }

    
    hitos_narrativos = []
    
    
    for act in historia_flags["actos_vistos"]:
        if act in mapeo_hitos:
            hitos_narrativos.append(mapeo_hitos[act])
            
    
    for misiones, estado in historia_flags["misiones_activas"].items():
        if estado == "RESUELTA" and misiones in mapeo_hitos:
            hitos_narrativos.append(mapeo_hitos[misiones])
            
    
    for encuentro in historia_flags["encuentros_profundos_vistos"]:
        if encuentro in mapeo_hitos:
            hitos_narrativos.append(mapeo_hitos[encuentro])

    
    print("\n" + "💬 " * 12)
    escribir_consola_lento(f"   {FONDO_VERDE}🔔 [WHATSAPP] GRUPO: CENA ANIVERSARIO ABUELOS 👵❤️👴{RESET}", 0.004)
    escribir_consola_lento("  " + "─" * 48, 0.004)
    escribir_consola_lento("  Amor ❤️: ¡Por fin entras por la puerta! Estábamos atacados de los nervios.")
    time.sleep(1)
    escribir_consola_lento("  Amor ❤️: Mira la foto que acaba de mandar tu prima de la mesa de gala: [FOTO_CELEBRACION_FAMILIAR.JPG] 📸", 0.004)
    time.sleep(1)
    escribir_consola_lento("")
    escribir_consola_lento("  Amor ❤️: Por cierto, me ha saltado al móvil el informe de tu trayecto compartido de la app. ¿Desde cuándo tienes Strava?")
    time.sleep(1)
    escribir_consola_lento("  Amor ❤️: Vaya locura de aventura urbana te has tenido que comer para llegar:\n", 0.004)
    time.sleep(1)
    
    
    print("  ┌───────────────────────────────────────────────────────────┐")
    
   
    linea_nombre = f"FINAL ENCOMIENDA DE ORO: {estado_juego['nombre'].upper()}"
    escribir_consola_lento(f"  │ {linea_nombre:<57} │", 0.004)
    print("  ├───────────────────────────────────────────────────────────┤")
    
    escribir_consola_lento(f"  │ {'  Parámetros de Configuración Inicial:':<57} │", 0.004)
    
    linea_origen = f"   • Origen: Casa en coordenadas (X: {estado_juego['inicio_x']}, Y: {estado_juego['inicio_y']})"
    escribir_consola_lento(f"  │ {linea_origen:<57} │", 0.004)
    
    linea_rumbo = f"   • Rumbo de Salida: {estado_juego['inicio_angulo']}° | Ánimo Base: {estado_juego['inicio_animo']}%"
    escribir_consola_lento(f"  │ {linea_rumbo:<57} │", 0.004)
    
    linea_reloj_ini = f"   • Reloj Inicial: {estado_juego['inicio_tiempo']} min."
    escribir_consola_lento(f"  │ {linea_reloj_ini:<57} │", 0.004)
    
    escribir_consola_lento(f"  │ {'':<57} │", 0.004)
    escribir_consola_lento(f"  │ {'  Estadísticas Finales del Recorrido:':<57} │", 0.004)
    
    linea_destino = f"   • Coordenadas de Destino: (X: {round(estado_juego['px'], 1)}, Y: {round(estado_juego['py'], 1)})"
    escribir_consola_lento(f"  │ {linea_destino:<57} │", 0.004)
    
    linea_pasos = f"   • Pasos / Turnos totales: {estado_juego['turno_actual']} turnos consumidos."
    escribir_consola_lento(f"  │ {linea_pasos:<57} │", 0.004)
    
    linea_recursos = f"   • Recursos Restantes: Reloj: {estado_juego['tiempo']} min | Ánimo: {estado_juego['animo']}%"
    escribir_consola_lento(f"  │ {linea_recursos:<57} │", 0.004)
    
    linea_karma = f"   • Karma Urbano: {estado_juego['karma_urbano']} pts | Ejército de Gatos: {registro_secretos['gatos_fijos']}."
    escribir_consola_lento(f"  │ {linea_karma:<57} │", 0.004)
    
    escribir_consola_lento(f"  │ {'':<57} │", 0.004)
    
    
    escribir_consola_lento(f"  │ {'   Hitos y Zonas de Interés Visitadas:':<57} │", 0.004)
    if not hitos_narrativos:
        escribir_consola_lento(f"  │ {'   • Ningún hito destacado en esta ruta.':<57} │", 0.004)
    else:
        for hito in hitos_narrativos:
            linea_hito = f"   • {hito[:50]}"
            escribir_consola_lento(f"  │ {linea_hito:<57} │", 0.004)
            
    escribir_consola_lento(f"  │ {'':<57} │", 0.004)
    escribir_consola_lento(f"  │ {'   Causa de Finalización de la Simulación:':<57} │", 0.004)
    
    linea_motivo = f"   • {motivo[:50]}"
    escribir_consola_lento(f"  │ {linea_motivo:<57} │", 0.004)
    
    escribir_consola_lento(f"  │ {'  Resultado Final:':<57} │", 0.004)
    
    linea_resultado = f"   • {resultado[:50]}"
    escribir_consola_lento(f"  │ {linea_resultado:<57} │", 0.004)
    print("  └───────────────────────────────────────────────────────────┘")
    
    print("")
    print("  Amor ❤️: ¡Siéntate ya y vamos a abrir los regalos! 🎁")
    print("  " + "💬 " * 12)
    print("")
    
    print("[EPÍLOGO - LA CENA:]")
    print("="*65)
    if resultado == "¡VICTORIA SECRETA GATUNA!":
        escribir_consola_lento("Llegas exhausto a la tienda y ves la persiana bajada... ¡Pero tu ejército de gatos se alinea en la calle!")
        escribir_consola_lento("El dueño abre la trastienda en pijama, extasiado ante el espectáculo felino.")
        escribir_consola_lento("Te entrega la caja envuelta gratis y llegas a la cena en una procesión triunfal.")
    elif resultado == "¡VICTORIA SECRETA REPOSTERA!":
        escribir_consola_lento("El maestro panadero resulta ser el hermano del anticuario. Impresionado por cómo trasladaste")
        escribir_consola_lento("sus preciados hojaldres intactos, ¡te ofrece el traspaso de la panadería gratis!")
    elif resultado == "¡VICTORIA ESTÁNDAR!":
        escribir_consola_lento("¡Lo lograste! Entras a la tienda de milagro justo antes del cierre patronal y caminas")
        escribir_consola_lento("triunfante hacia el restaurante. Tus abuelos rompen a llorar de pura emoción.")
    elif motivo == "COLAPSO POR ESTRÉS":
        escribir_consola_lento("La hostilidad de la metrópolis quiebra tu mente. Te dejas caer en un banco de madera,")
        escribir_consola_lento("apagas el móvil harto del caos y llamas a un coche para volver a tu cama.")
    else:
        escribir_consola_lento("Ves a lo lejos las luces apagadas. El anticuario ha echado el cierre.")
        escribir_consola_lento("Te presentas en las bodas de oro con las manos vacías y una tarjeta barata.")
    print("="*65 + "\n")
    
    input("[PULSA ENTER PARA FINALIZAR LA EXPEDICIÓN]")

#Bucle principal

def jugar_expedicion():
    clear_terminal()
    print("=========================================================")
    print("          CONFIGURACIÓN DE LA ENCOMIENDA DE ORO      ")
    print("=========================================================\n")
    
    name = input("Introduce el nombre de tu personaje: ").strip()
    estado_juego["nombre"] = name if name else "NietoViajero505"
    
    while True:
        try:
            x_in = input("Coordenada X inicial (0-100) [recomendado: 0]: ").strip()
            y_in = input("Coordenada Y inicial (0-100): ").strip()
            estado_juego["px"] = float(int(x_in)); estado_juego["py"] = float(int(y_in))
            if 0 <= estado_juego["px"] <= 100 and 0 <= estado_juego["py"] <= 100: break
            print("¡Error! Los límites son estrictamente entre 0 y 100.")
        except ValueError: print("Entrada inválida. Escribe números enteros.")
            
    while True:
        print("\nSelecciona el modelo de dificultad:")
        print("[1] Calles Libres (Preset) (60 Minutos, Ánimo 100%)")
        print("[2] Hora Punta (Preset) (45 Minutos, Ánimo 80%)")
        print("[3] Configuración Avanzada")
        op = input("Opción de arranque (1-3): ").strip()
        if op == "1": estado_juego["tiempo"] = 60; estado_juego["animo"] = 100; break
        elif op == "2": estado_juego["tiempo"] = 45; estado_juego["animo"] = 80; break
        elif op == "3":
            while True:
                try:
                    t_custom = int(input("\nTiempo límite (10-100): ").strip())
                    a_custom = int(input("Ánimo inicial (10-100): ").strip())
                    if 10 <= t_custom <= 100 and 10 <= a_custom <= 100:
                        estado_juego["tiempo"] = t_custom; estado_juego["animo"] = a_custom; break
                    print("¡Error! Rango estricto de 10 a 100.")
                except ValueError: print("Entrada inválida.")
            break

    # Un ángulo inicial es obligatorio según las bases del concurso
    # He optado por dar una penalización si el jugador empieza mirando en la dirección incorrecta
    # Ya que la navegación del juego es con los puntos cardinales, esta es la única manera de cumplir con las bases.
    while True:
        print("\n¿Hacia qué dirección estás mirando al salir de tu casa?")
        print("Opciones: D (Este), W (Norte), A (Oeste), S (Sur) o diagonales (WD, WA, SD, SA)")
        dir_inicial = input("Introduce tu dirección de salida: ").strip().upper()
        if dir_inicial in DIRECCIONES_ANGULOS:
            estado_juego["angulo"] = DIRECCIONES_ANGULOS[dir_inicial]
            break
        print("Dirección no reconocida. Selecciona una opción de la brújula urbana.")

    
    estado_juego["inicio_x"] = estado_juego["px"]
    estado_juego["inicio_y"] = estado_juego["py"]
    estado_juego["inicio_tiempo"] = estado_juego["tiempo"]
    estado_juego["inicio_animo"] = estado_juego["animo"]
    estado_juego["inicio_angulo"] = estado_juego["angulo"]

    # Generamos de forma anticipada las coordenadas para evaluar el despiste
    park_distrito, obras_distrito = generar_distritos_ciudad()

    # Si hay despiste, hay penalización
    rumbo_correcto = calcular_rumbo_exacto(estado_juego["px"], estado_juego["py"], estado_juego["meta_x"], estado_juego["meta_y"])
    despiste_detectado = False
    if dir_inicial != rumbo_correcto:
        cambiar_animo(-5)
        cambiar_tiempo(-2)
        despiste_detectado = True

    #Muestra todos los parámetros obligatorios de golpe antes de jugar
    clear_terminal()
    print("=======================================================================")
    print(f"                 INICIO DE LA EXPEDICIÓN: {estado_juego['nombre'].upper()}              ")
    print("=======================================================================\n")
    
    escribir_consola_lento(
        f"«Vale, lo tengo todo listo», dijo {estado_juego['nombre']} mientras se arreglaba el pelo frente al espejo del portal.\n"
        f"«Salgo en dirección {estado_juego['angulo']}° (mirando hacia el rumbo {dir_inicial}) y tengo...\n*mira su reloj con prisa*\n"
        f"exactamente {estado_juego['inicio_tiempo']} minutos para llegar desde mi casa en ({estado_juego['inicio_x']}, {estado_juego['inicio_y']}) "
        f"hasta la tienda de antigüedades, localizada en ({estado_juego['meta_x']}, {estado_juego['meta_y']}).\nMi ánimo mental está al {estado_juego['inicio_animo']}%... ¡Vamos!»"
    )
    
    if despiste_detectado:
        print(f"\n{ROJO}[DESPISTE URBANO]{RESET}: La tienda está realmente hacia el rumbo {rumbo_correcto}, pero saliste caminando hacia el {dir_inicial}.")
        print("Tuviste que dar la vuelta a la manzana al darte cuenta del error. Pierdes 2 minutos de reloj y te estresas (-5% Ánimo).")
        
    print("\n" + "─"*75)
    print("LÍMITES: Coordenadas fijas de 0.0 a 100.0 en los ejes X e Y.")
    print("CONDICIONES DE FIN: Llegar a la meta, sin agotar el tiempo (0 min) o colapsar mentalmente (0% ánimo).")
    print("─"*75)
    
    input("\n[PULSA ENTER PARA AJUSTARTE LAS ZAPATILLAS Y SALIR A LA AVENIDA]")
    clear_terminal()

    # Inicialización de la pantalla gráfica de Turtle
    screen = turtle.Screen()
    mostrar_introduccion(screen)
    
    screen.bgcolor("#2c3e50")
    screen.setworldcoordinates(-5, -5, 105, 105)
    turtle.tracer(0, 0)
    
    dibujar_manzanas_ciudad(turtle.Turtle(), park_distrito, obras_distrito)
    
    
    borde_mapa = turtle.Turtle()
    borde_mapa.hideturtle()
    borde_mapa.speed(0)
    borde_mapa.penup()
    borde_mapa.color("#ff0000")
    borde_mapa.pensize(3)
    borde_mapa.goto(-0.5, -0.5)
    borde_mapa.pendown()
    for _ in range(4):
        borde_mapa.forward(101)
        borde_mapa.left(90)
    
    pintor = turtle.Turtle()
    pintor.hideturtle()
    pintor.penup(); pintor.goto(estado_juego["meta_x"], estado_juego["meta_y"]); pintor.dot(14, "#e74c3c")
    pintor.color("white"); pintor.goto(estado_juego["meta_x"] - 4, estado_juego["meta_y"] - 5)
    pintor.write("TIENDA META", font=("Arial", 8, "bold"))
    
    pintor.penup(); pintor.goto(30, 30); pintor.dot(12, "#3498db")
    pintor.color("white"); pintor.goto(27, 24); pintor.write("METRO CENTRAL", font=("Arial", 8, "bold"))
    turtle.update()
    
    turtle.tracer(1, 5)
    jugador_turtle = turtle.Turtle()
    jugador_turtle.shape("circle"); jugador_turtle.color("#f1c40f"); jugador_turtle.shapesize(0.5); jugador_turtle.pensize(2.5)
    jugador_turtle.penup(); jugador_turtle.goto(estado_juego["px"], estado_juego["py"]); jugador_turtle.pendown()
    
    clear_terminal()
    
    while True:
        dist_meta = math.hypot(estado_juego["px"] - estado_juego["meta_x"], estado_juego["py"] - estado_juego["meta_y"])
        
        # SUCESOS NARRATIVOS GLOBALES
        verificar_cambio_de_acto(dist_meta)
        
        # PROCESADOR DE ENCUENTROS
        if random.randint(1, 100) <= 8:
            if procesar_encuentro_profundo():
                pass # Vuelve a evaluar la UI después del texto
                
        inyectar_narrativa_viva_turno() 
        verificar_notificaciones_automaticas()
        
        # Interfaz aislada
        accion_valida = False
        while not accion_valida:
            mensajes_pendientes = sum(1 for v in chats_data.values() if v["unread"])
            if mensajes_pendientes > 0:
                print("\n" + "="*75)
                print(f" 📱 Tienes {mensajes_pendientes} chat(s) pendiente(s) en WhatsApp. Te recomendamos abrir el móvil.")
                print("="*75)
                
            cx, cy = estado_juego["px"], estado_juego["py"]
            en_parque = park_distrito["x1"] <= cx <= park_distrito["x2"] and park_distrito["y1"] <= cy <= park_distrito["y2"]
            en_obras = obras_distrito["x1"] <= cx <= obras_distrito["x2"] and obras_distrito["y1"] <= cy <= obras_distrito["y2"]
            
            
            reporte_bioma = ""
            if en_parque:
                reporte_bioma += "🌲 Estás transitando el Parque (Efecto: +3 Ánimo al consolidar paso).\n"
                if "INSOLACION" in historia_flags["estados_personaje"]:
                    historia_flags["turnos_sombra_parque"] += 1
                    if historia_flags["turnos_sombra_parque"] >= 2:
                        historia_flags["estados_personaje"].remove("INSOLACION"); historia_flags["turnos_sombra_parque"] = 0
                        reporte_bioma += "☀️ [ALIVIO CLÍNICO]: Curada eficientemente la INSOLACION bajo la sombra.\n"
            elif en_obras:
                if "RITMO_ZEN" not in historia_flags["estados_personaje"]:
                    reporte_bioma += "🚧 Estás ahogándote en la ruidosa Zona de Obras (-5 Ánimo por acústica al consolidar).\n"
                else:
                    reporte_bioma += "🚧 Distrito Obras: Tu RITMO_ZEN te hace inmune al ruido de las perforadoras.\n"
            else:
                reporte_bioma += "🏙️ Estás en el asfalto del distrito comercial general.\n"
                
            if "EMPAPADO" in historia_flags["estados_personaje"]:
                reporte_bioma += "💧 Secuela activa (EMPAPADO): La ropa mojada drena -1% de ánimo extra al consolidar turno.\n"

            print("\n--- REPORTES DE ZONA ---")
            print(reporte_bioma.strip())

            # RESOLUCIÓN HITOS GEOGRÁFICOS DE MISIONES 
            # Uso math.isclose() para permitir un margen de error en la posición del jugador y que no se pierda la misión por un decimal de más o de menos

            if historia_flags["misiones_activas"].get("AYUDA_TIO") == "ACTIVADA":
                if math.isclose(cx, 30, abs_tol=3.0) and math.isclose(cy, 50, abs_tol=3.0):
                    print("\n=== EVENTO DE MISION: LA OFICINA DEL TÍO ALBERTO ===")
                    print("Subes corriendo empapado. Tu querido tío te presta una sudadera limpia de algodón.")
                    historia_flags["estados_personaje"].remove("EMPAPADO"); estado_juego["animo"] = 100
                    historia_flags["misiones_activas"]["AYUDA_TIO"] = "RESUELTA"
                    print("-> Secuela EMPAPADO removida de la ficha. Ánimo al 100%."); input("\n[PULSA ENTER]")

            if historia_flags["misiones_activas"].get("CALLEJON_ABUELO") == "ACTIVADA":
                if math.isclose(cx, 70, abs_tol=3.0) and math.isclose(cy, 40, abs_tol=3.0):
                    print("\n=== SUCESO DE MAPA: LOS CALLEJONES OCULTOS DEL FUNDADOR ===")
                    print("Cortas por un pasaje de adoquines libre de peatones. ¡Avanzas 10 bloques gratis!")
                    estado_juego["px"] += 10
                    jugador_turtle.penup(); jugador_turtle.goto(estado_juego["px"], cy); jugador_turtle.pendown()
                    historia_flags["misiones_activas"]["CALLEJON_ABUELO"] = "RESUELTA"; input("\n[PULSA ENTER]")

            if historia_flags["misiones_activas"].get("VINILO_GUILLE") == "ACTIVADA":
                if math.isclose(cx, 40, abs_tol=2.5) and math.isclose(cy, 20, abs_tol=2.5):
                    print(f"\n{FONDO_AZUL}💿 === EVENTO CRÍTICO: LA DISCO-METRÓPOLIS ==={RESET}")
                    print("Compras raudo la última copia sellada del vinilo de Arctic Monkeys.")
                    historia_flags["mochila"].append("VINILO_HUMBUG"); cambiar_tiempo(-3)
                    dx_m, dy_m = estado_juego["meta_x"] - estado_juego["px"], estado_juego["meta_y"] - estado_juego["py"]
                    dist_m = math.hypot(dx_m, dy_m)
                    estado_juego["px"] += (dx_m / dist_m) * 25; estado_juego["py"] += (dy_m / dist_m) * 25
                    jugador_turtle.penup(); jugador_turtle.goto(estado_juego["px"], estado_juego["py"]); jugador_turtle.pendown()
                    print("-> ¡ÉPICO! ¡La furgoneta del hermano de Guille te adelanta 25 bloques directos!")
                    historia_flags["misiones_activas"]["VINILO_GUILLE"] = "RESUELTA"; historia_flags["javi_contacto"] = True
                    input("\n[PULSA ENTER]")

            if historia_flags["enemigo_publico"] and "ACTO_III" in historia_flags["actos_vistos"] and "POLICIA_VISTO" not in historia_flags["misiones_activas"]:
                historia_flags["misiones_activas"]["POLICIA_VISTO"] = "ACTIVADA"
                print("\n🚨 [EVENTO DE CONTENCIÓN PÚBLICA]: Un coche patrulla frena a tu lado.")
                print("Agente Uniformado: 'Oye chaval, das el perfil del vídeo agrediendo a artistas. Identifícate.'")
                if estado_juego["karma_urbano"] >= 5:
                    print("[EFECTO KARMA POSITIVO]: Los comerciantes te defienden por tus buenas acciones previas.")
                    print("-> El policía te deja marchar sin hacerte perder tiempo.")
                else:
                    print("-> No tienes aliados. Pierdes 5 valiosos minutos dando explicaciones y rellenando actas.")
                    cambiar_tiempo(-5)
                input("\n[PULSA ENTER]")

            lista_est = ", ".join(historia_flags["estados_personaje"]) if historia_flags["estados_personaje"] else "TODO GUAY"
            
            print("\n" + "─" * 75)
            print(f" SALUD FÍSICA: {lista_est} | KARMA URBANO TOTAL: {estado_juego['karma_urbano']} PTS.")
            print("─" * 75)
            print(f" TURNO ACTUAL: {estado_juego['turno_actual']:<4} | TIEMPO: {estado_juego['tiempo']:<3} min | ÁNIMO: {estado_juego['animo']}%")
            print(f" Ubicación GPS: (X: {round(cx,1)}, Y: {round(cy,1)})")
            print("─" * 75)
            
            print("\n[1] Moverse  |  [2] SACAR MOVIL (Menú)")
            accion = input("\nElige acción (1-2): ").strip()
            
            if accion == "2":
                abrir_smartphone()
                clear_terminal()
                continue 
                
            if accion == "1":
                accion_valida = True
            else:
                print("\n¡Comando de consola inválido! Pierdes unos minutos dudando...")
                cambiar_tiempo(-1); estado_juego["turno_actual"] += 1; time.sleep(1.5); clear_terminal()
                break 

        if not accion_valida:
            continue 

        
        print("\nBrújula (W=Norte, S=Sur, A=Oeste, D=Este | Diagonales: WD, WA, SD, SA)")
        cmd_dir = input("Introduce la dirección de tu próximo paso: ").strip().upper()
        if cmd_dir not in DIRECCIONES_ANGULOS:
            print("\n¡Dirección no reconocida! Tropiezas con una farola perdiendo equilibrio. Que vergüenza"); cambiar_animo(-5); time.sleep(1.5); clear_terminal(); continue
            
        print("\nModificador de ritmo: [1] Normal (1 bloq.) | [2] Prisa (3 bloq.) | [3] Sprint (5 bloq.)")
        cmd_vel = input("Elige la velocidad de tus zapatillas: ").strip()
        
        # Captura de forma exacta el recurso Antes" justo aquí, previo a procesar la acción del turno 
        ant_x, ant_y = estado_juego["px"], estado_juego["py"]
        ant_tiempo, ant_animo = estado_juego["tiempo"], estado_juego["animo"]

        distancia = 1
        if cmd_vel == "2": distancia = 3; cambiar_animo(-2)
        elif cmd_vel == "3": 
            if "COJO" in historia_flags["estados_personaje"]:
                print("\n¡Tu severa lesión muscular te impide esprintar! Marcha regular forzada."); distancia = 1; time.sleep(2)
            else:
                distancia = 5; cambiar_animo(-10 if "ESTRESADO" in historia_flags["estados_personaje"] else -6)
            
        if en_parque and distancia > 1: print("\n¡El barro arcilloso del bioma te chupa los zapatos! Paso normal forzado."); distancia = 1; time.sleep(1.5)

        if "INSOLACION" in historia_flags["estados_personaje"] and estado_juego["turno_actual"] % 3 == 0:
            rad = math.radians((DIRECCIONES_ANGULOS[cmd_dir] + 180) % 360)
        else:
            estado_juego["angulo"] = DIRECCIONES_ANGULOS[cmd_dir]
            rad = math.radians(estado_juego["angulo"])
        
        multiplicador_tiempo = 1
        if historia_flags["atasco_meta"] and math.hypot(cx - estado_juego["meta_x"], cy - estado_juego["meta_y"]) <= 12:
            if historia_flags["ganso_aliado"]:
                print("\n¡Tu enorme ganso escolta abre un camino seguro entre el atasco familiar bufando y picoteando!")
                time.sleep(2)
            else:
                print("\n¡Estás atrapado en el núcleo de gravedad del atasco! Moverse aquí consume el TRIPLE de tiempo.")
                multiplicador_tiempo = 3
                time.sleep(2)

        teorica_x = estado_juego["px"] + (distancia * math.cos(rad))
        teorica_y = estado_juego["py"] + (distancia * math.sin(rad))
        
        # NO SE PUEDE SALIR.
        if teorica_x < 0 or teorica_x > 100 or teorica_y < 0 or teorica_y > 100:
            print(f"\n🚧 {ROJO}[COLISIÓN PERIMETRAL]{RESET}: Has intentado salir del mapa. Las vallas urbanas te retienen en el límite. Tienes que ir a la tienda, ¿recuerdas?")

        nueva_x = max(0.0, min(100.0, teorica_x))
        nueva_y = max(0.0, min(100.0, teorica_y))
        
        estado_juego["px"], estado_juego["py"] = nueva_x, nueva_y
        cambiar_tiempo(-1 * multiplicador_tiempo)
        jugador_turtle.goto(estado_juego["px"], estado_juego["py"])
        
        
        nuevo_en_parque = park_distrito["x1"] <= nueva_x <= park_distrito["x2"] and park_distrito["y1"] <= nueva_y <= park_distrito["y2"]
        nuevo_en_obras = obras_distrito["x1"] <= nueva_x <= obras_distrito["x2"] and obras_distrito["y1"] <= nueva_y <= obras_distrito["y2"]
        
        if nuevo_en_parque:
            cambiar_animo(3)
        elif nuevo_en_obras and "RITMO_ZEN" not in historia_flags["estados_personaje"]:
            cambiar_animo(-5)
            
        if "EMPAPADO" in historia_flags["estados_personaje"]:
            cambiar_animo(-1)
        
        if math.isclose(estado_juego["px"], 30, abs_tol=2) and math.isclose(estado_juego["py"], 30, abs_tol=2):
            print("\n🚇 ¡Estás posicionado exactamente frente a las sucias escaleras de la boca del Metro Central!")
            dx_t, dy_t = estado_juego["meta_x"] - estado_juego["px"], estado_juego["meta_y"] - estado_juego["py"]
            dist_obj = math.hypot(dx_t, dy_t)
            avance = min(35.0, dist_obj * 0.6)
            
            viajar = input("¿Deseas invertir tus billetes en coger la línea rápida subterránea? Consume 4 minutos (S/N): ").strip().upper()
            if viajar == "S":
                estado_juego["px"] += (dx_t / dist_obj) * avance; estado_juego["py"] += (dy_t / dist_obj) * avance
                cambiar_tiempo(-4)
                jugador_turtle.penup(); jugador_turtle.goto(estado_juego["px"], estado_juego["py"]); jugador_turtle.pendown()
                print(f"-> ¡El tren express te acerca un total mágico de {round(avance, 1)} bloques a tu meta!"); input("\n[PULSA ENTER]")
                
        ejecutar_evento_aleatorio("PARQUE" if nuevo_en_parque else ("OBRAS" if nuevo_en_obras else "GENERAL"))
        
        if registro_secretos["gatos_fijos"] > 0 and not registro_secretos["gato_en_cortejo"] and random.randint(1, 100) <= 20:
            registro_secretos["gato_en_cortejo"] = True; registro_secretos["turnos_con_gato_actual"] = 1
            registro_secretos["tipo_gato_actual"] = random.choice(["PROTECTOR", "ASUSTADIZO", "GLOTON", "LIDER"])
        if registro_secretos["gato_en_cortejo"]: avanzar_cortejo_gatos()
        
        if estado_juego["cooldown_eventos"] > 0: estado_juego["cooldown_eventos"] -= 1
        registrar_log(f"Marcha completada a {cmd_dir}. Coordenadas: ({round(estado_juego['px'],1)}, {round(estado_juego['py'],1)})")
        
        
        print("\n" + "📝 " * 15)
        print(f"RECURSOS - TURNO {estado_juego['turno_actual']}")
        print(f"   • Acción: Desplazamiento hacia [{cmd_dir}] | Ritmo de calzado: [{cmd_vel}]")
        print(f"   • Ubicación GPS: ({round(ant_x, 1)}, {round(ant_y, 1)}) ➡️ ({round(estado_juego['px'], 1)}, {round(estado_juego['py'], 1)})")
        print(f"   • Tiempo: {ant_tiempo} min ➡️ {estado_juego['tiempo']} min")
        print(f"   • Ánimo: {ant_animo}% ➡️ {estado_juego['animo']}%")
        print("📝 " * 15)
        input("\n[PULSA ENTER PARA CONTINUAR]")

        if dist_meta <= 2.5:
            if registro_secretos["gatos_fijos"] >= 3: imprimir_reporte_final("¡VICTORIA SECRETA GATUNA!", "Asalto masivo de ejército de élite leal felino.")
            elif "CRUASANES" in historia_flags["mochila"] and estado_juego["animo"] >= 85: imprimir_reporte_final("¡VICTORIA SECRETA REPOSTERA!", "Protección táctica de hojaldre completamente intacto.")
            elif historia_flags["enemigo_publico"] and estado_juego["karma_urbano"] >= 5: imprimir_reporte_final("¡VICTORIA ÉPICA VIRAL!", "Héroe redimido en polémica viral de internet global.")
            else: imprimir_reporte_final("¡VICTORIA ESTÁNDAR!", "Entrada victoriosa a tiempo.")
            break
        if estado_juego["animo"] <= 0: imprimir_reporte_final("FRACASO ABSOLUTO DE SALUD MENTAL", "EL COLAPSO LLEGÓ INMINENTE Y BRUTAL POR EL PESO DEL ESTRÉS Y UN FULMINANTE ATAQUE DE PÁNICO URBANO"); break
        if estado_juego["tiempo"] <= 0: imprimir_reporte_final("FRACASO MATEMÁTICO TEMPORAL", "EL INEXORABLE TIEMPO LÍMITE LLEGÓ A CERO ESTRICTO Y DEFINITIVO. LA TIENDA ECHÓ EL CIERRE CON LÁGRIMAS."); break
        
        estado_juego["turno_actual"] += 1
        clear_terminal()

if __name__ == "__main__":
    while True:
        jugar_expedicion()
        if input("\n¿Deseas reiniciar la máquina de simulación global con nuevas variables? Pulsa (S/N): ").strip().upper() != "S": break
        
        turtle.resetscreen()
        estado_juego["turno_actual"], estado_juego["historial_logs"], estado_juego["karma_urbano"] = 1, [], 0
        registro_secretos["gatos_fijos"], registro_secretos["gato_en_cortejo"] = 0, False
        historia_flags["estados_personaje"], historia_flags["mochila"], historia_flags["misiones_activas"], historia_flags["encuentros_profundos_vistos"] = [], [], {}, []
        historia_flags["atasco_meta"], historia_flags["ganso_aliado"] = False, False
        historia_flags["cruasanes_cantidad"], historia_flags["turnos_sombra_parque"], historia_flags["guille_bloqueado"] = 0, 0, False
        tramas["amor_trama_iniciada"], tramas["amor_trama_resuelta"], tramas["amor_fase"], tramas["amor_timer_ghosting"] = False, False, 1, 0
        tramas["guille_trama_iniciada"], tramas["guille_trama_resuelta"], tramas["empapado_chat"], tramas["cojo_chat"], tramas["insolacion_chat"] = False, False, False, False, False
        for data in chats_data.values(): data["historial"], data["unread"], data["pending_options"] = [], False, {}