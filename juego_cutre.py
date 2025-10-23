import random
import json
import os
from datetime import datetime

# =============================================================================
# VARIABLES GLOBALES
# =============================================================================

# Variables del jugador
xp = 0
puntos_de_stats = 0
lvl = 1
vida = 0
max_vida = 0
ataque = 0
defensa = 0
velocidad = 0
esquive = 0
inteligencia = 0
destreza = 0
suerte = 0
mana = 0
max_mana = 0
dinero_jugador = 500


# Variables del enemigo
vida_enemigo = 0
max_vida_enemigo = 0
ataque_enemigo = 0
defensa_enemigo = 0
velocidad_enemigo = 0
inteligencia_enemigo = 0
suerte_enemigo = 0
xp_del_enemigo = 0
enemigo_encontrado = ""
dinero = 0
enemigo_quemado = False
enemigo_congelado = False
materiales_crafteo = {}
recetas_disponibles = {}

# Variables del juego
turnos = 0
inv = []
arma_equipada = []
armadura_equipada = []
objetos_en_tienda = []
arma_activa = False
armadura_activa = False
estas_en_combate = False
turnos_en_combate = 0
turnos_quemadura = 0
daño_quemadura = 0
turnos_congelacion = 0
eleccion_de_camino = ""

# Variables de efectos de estado
enemigo_quemado = False
turnos_quemadura = 0
daño_quemadura = 0
enemigo_congelado = False
turnos_congelacion = 0
buffs_activos = {}

# Variables para stats de armas/armaduras
ataque_arma = 0
max_vida_arma = 0
defensa_arma = 0
max_mana_arma = 0
vida_arma = 0
destreza_arma = 0
suerte_arma = 0
inteligencia_arma = 0
velocidad_arma = 0
esquive_arma = 0

# =============================================================================
# DATOS DEL JUEGO - OBJETOS, HECHIZOS Y CONJUNTOS
# =============================================================================

# Listas de objetos por rareza
objeto_comun = [
    "espada de madera",
    "arco de madera", "baculo de madera", "dagas de madera",
    "armadura de cuero reforzado", "armadura de cuero ligero",
    "túnicas de aprendiz", "armadura de cuero negro"
]

objeto_raro = [
    "espada avanzada",
    "arco avanzado", "baculo avanzado", "dagas avanzadas",
    "armadura de cuero tachonado", "armadura de cuero élfico",
    "túnicas de seda encantada", "armadura de sombras menores"
]

objeto_epico = [
    "espada de hierro",
    "arco de hierro", "baculo de hierro", "dagas de hierro",
    "armadura de mallas de hierro", "armadura de escamas dragón",
    "túnicas de hilos de mithril", "armadura de escamas sombría"
]

objeto_legendario = [
    "excalibur imitacion", "espada de fuego", "espada de ventisca",
    "arco de los elfos", "baculo de un mago experto", "dagas de la noche",
    "dagas de la luna", "guadaña de los muertos", "guadaña del vacio",
    "arco de apolo imitacion", "baculo de merlin imitacion",
    "armadura de placas encantadas", "armadura de hojas ancestrales",
    "túnicas de tejido estelar", "armadura de la noche eterna"
]

objeto_mitico = [
    "baculo de merlin", "baculo del rey de los magos", "excalibur",
    "arco del rey de los elfos", "guadaña del vacio cosmico",
    "guadaña del rey de los muertos", "espada infernal de fuego eterno",
    "espada de ventisca eterna", "dagas de la noche eterna",
    "dagas de la luna llena", "arco de apolo", "armadura del rey arturo",
    "armadura solar divina", "túnicas del archimago supremo",
    "armadura del vacío absoluto"
]

# Valores de objetos
valores_objetos = {
    # Común
    "pocion de vida pequeña": 75, "pocion de mana pequeña": 75,
    "espada de madera": 220, "arco de madera": 220, "baculo de madera": 220,
    "dagas de madera": 220, "armadura de cuero reforzado": 200,
    "armadura de cuero ligero": 240, "túnicas de aprendiz": 200,
    "armadura de cuero negro": 260,

    # Raro
    "pocion de vida mediana": 225, "pocion de mana mediana": 225,
    "espada avanzada": 1100, "arco avanzado": 1100, "baculo avanzado": 1100,
    "dagas avanzadas": 1050, "armadura de cuero tachonado": 950,
    "armadura de cuero élfico": 1000, "túnicas de seda encantada": 1000,
    "armadura de sombras menores": 1050,

    # Épico
    "pocion de vida grande": 450, "pocion de mana grande": 450,
    "espada de hierro": 4500, "arco de hierro": 4500, "baculo de hierro": 4500,
    "dagas de hierro": 4300, "armadura de mallas de hierro": 4200,
    "armadura de escamas dragón": 4800, "túnicas de hilos de mithril": 4400,
    "armadura de escamas sombría": 4700,

    # Legendario
    "excalibur imitacion": 8000, "espada de fuego": 7500, "espada de ventisca": 7500,
    "arco de los elfos": 7800, "baculo de un mago experto": 8000,
    "dagas de la noche": 7200, "dagas de la luna": 7300, "guadaña de los muertos": 7000,
    "guadaña del vacio": 7600, "arco de apolo imitacion": 7800,
    "baculo de merlin imitacion": 7900, "armadura de placas encantadas": 8200,
    "armadura de hojas ancestrales": 8300, "túnicas de tejido estelar": 8200,
    "armadura de la noche eterna": 8600,

    # Mítico
    "baculo de merlin": 14000, "baculo del rey de los magos": 16500,
    "excalibur": 16000, "arco del rey de los elfos": 15500,
    "guadaña del vacio cosmico": 15000, "guadaña del rey de los muertos": 17000,
    "espada infernal de fuego eterno": 15800, "espada de ventisca eterna": 15800,
    "dagas de la noche eterna": 14800, "dagas de la luna llena": 15200,
    "arco de apolo": 16200, "armadura del rey arturo": 17500,
    "armadura solar divina": 16800, "túnicas del archimago supremo": 17000,
    "armadura del vacío absoluto": 18500
}

# Sistema de hechizos
hechizos_disponibles = {
    "bola de fuego": {
        "costo": 15, "daño_base": 25, "tipo": "daño",
        "descripcion": "Lanza una bola de fuego que causa daño mágico"
    },
    "rayo de hielo": {
        "costo": 20, "daño_base": 30, "tipo": "daño_congelacion",
        "descripcion": "Rayo helado que daña y puede congelar al enemigo"
    },
    "curación menor": {
        "costo": 12, "curacion": 40, "tipo": "curacion",
        "descripcion": "Restaura puntos de vida"
    },
    "curación mayor": {
        "costo": 25, "curacion": 80, "tipo": "curacion",
        "descripcion": "Restaura gran cantidad de puntos de vida"
    },
    "bendición de fuerza": {
        "costo": 18, "buff_stat": "ataque", "buff_valor": 10,
        "duracion": 3, "tipo": "buff",
        "descripcion": "Aumenta el ataque por 3 turnos"
    },
    "escudo mágico": {
        "costo": 20, "buff_stat": "defensa", "buff_valor": 15,
        "duracion": 4, "tipo": "buff",
        "descripcion": "Aumenta la defensa por 4 turnos"
    },
    "velocidad felina": {
        "costo": 15, "buff_stat": "velocidad", "buff_valor": 12,
        "duracion": 3, "tipo": "buff",
        "descripcion": "Aumenta la velocidad por 3 turnos"
    },
    "tormenta arcana": {
        "costo": 35, "daño_base": 50, "tipo": "daño_area",
        "descripcion": "Hechizo devastador de alto costo"
    }
}

# Conjuntos de armas y armaduras
conjuntos_armas_armaduras = {
    # GUERRERO
    ("espada de madera", "armadura de cuero reforzado"): {
        "nombre": "Aprendiz de Espada", "bonificacion": {"defensa": 3},
        "descripcion": "+3 Defensa, 15% chance de bloqueo"
    },
    ("espada avanzada", "armadura de cuero tachonado"): {
        "nombre": "Espadachín Veterano", "bonificacion": {"ataque": 5},
        "descripcion": "+5 Ataque, 20% chance de contraataque"
    },
    ("excalibur", "armadura del rey arturo"): {
        "nombre": "Portador de Excalibur", "bonificacion": {"ataque": 25},
        "descripcion": "+25 Ataque, 50% chance de Luz Sagrada"
    },

    # ARQUERO
    ("arco de madera", "armadura de cuero ligero"): {
        "nombre": "Cazador Novato", "bonificacion": {"velocidad": 5},
        "descripcion": "+5 Velocidad, 10% chance de disparo certero"
    },
    ("arco de apolo", "armadura solar divina"): {
        "nombre": "Avatar de Apolo", "bonificacion": {"destreza": 30},
        "descripcion": "+30 Destreza, 40% chance de Eclipse Solar"
    },

    # MAGO
    ("baculo de madera", "túnicas de aprendiz"): {
        "nombre": "Estudiante de Magia", "bonificacion": {"inteligencia": 10},
        "descripcion": "+10 Inteligencia, 15% chance de Chispa Mágica"
    },
    ("baculo de merlin", "túnicas del archimago supremo"): {
        "nombre": "Sucesor de Merlín", "bonificacion": {"inteligencia": 40},
        "descripcion": "+40 Inteligencia, 50% chance de Magia Definitiva"
    },

    # ASESINO
    ("dagas de madera", "armadura de cuero negro"): {
        "nombre": "Ladrón de Callejón", "bonificacion": {"velocidad": 6},
        "descripcion": "+6 Velocidad, 15% chance de Golpe Furtivo"
    },
    ("dagas de la noche eterna", "armadura del vacío absoluto"): {
        "nombre": "Sombra Viviente", "bonificacion": {"velocidad": 35},
        "descripcion": "+35 Velocidad, 45% chance de Dominio Sombra"
    }
}

# Habilidades especiales de armas
habilidades_armas = {
    # Legendarias
    "excalibur imitacion": {"nombre": "golpe_critico", "chance": 15, "efecto": "critico_1_5"},
    "espada de fuego": {"nombre": "quemar", "chance": 20, "efecto": "quemadura_5_3"},
    "espada de ventisca": {"nombre": "congelar", "chance": 20, "efecto": "congelacion_2"},
    "arco de los elfos": {"nombre": "disparo_doble", "chance": 25, "efecto": "doble_ataque"},
    "dagas de la noche": {"nombre": "ataque_furtivo", "chance": 20, "efecto": "ignora_defensa"},

    # Míticas
    "excalibur": {"nombre": "corte_divino", "chance": 25, "efecto": "ignora_defensa_critico"},
    "arco de apolo": {"nombre": "rayo_solar", "chance": 25, "efecto": "dano_fijo_50"},
    "baculo de merlin": {"nombre": "hechizo_devastador", "chance": 20, "efecto": "critico_2_0"},
    "dagas de la noche eterna": {"nombre": "ataque_sombra", "chance": 35, "efecto": "critico_1_8"}
}
# =============================================================================
# DROPS ENEMIGOS Y SUS POSIBILIDADES
# =============================================================================

# Sistema de materiales de crafteo
materiales_comunes = {
    "hierro refinado": "Material común para forjar armas básicas",
    "cuero resistente": "Material común para crear armaduras ligeras", 
    "gema arcana": "Material común que potencia objetos mágicos",
    "madera élfica": "Material común de alta calidad para armas",
    "metal encantado": "Material común con propiedades mágicas"
}

materiales_especiales = {
    "nucleo de golem": "Núcleo ardiente extraído de un Golem derrotado",
    "colmillo de orco": "Colmillo afilado de un Orco veterano",
    "esencia sombría": "Energía oscura concentrada de las sombras",
    "cristal de mana": "Cristal puro que almacena energía mágica"
}

# Probabilidades de drop por enemigo (sobre 10000)
drops_enemigos = {
    "Slime": {
        "hierro refinado": 2000,
        "cuero resistente": 1500,
        "gema arcana": 500
    },
    "Goblin": {
        "hierro refinado": 2500,
        "cuero resistente": 2000,
        "gema arcana": 800,
        "madera élfica": 1200,
        "colmillo de orco": 50  # Raro
    },
    "Orco": {
        "hierro refinado": 3000,
        "metal encantado": 2000,
        "madera élfica": 1500,
        "colmillo de orco": 300,  # Material especial más común
        "cristal de mana": 100
    },
    "Golem": {
        "metal encantado": 3500,
        "hierro refinado": 2500,
        "nucleo de golem": 800,  # Su material especial
        "cristal de mana": 400,
        "gema arcana": 1000
    }
}

# Recetas de crafteo para armas míticas
recetas_crafteo = {
    # SOLO OBJETOS MÍTICOS (los más poderosos)
    "espada infernal de fuego eterno": {
        "nucleo de golem": 2,
        "metal encantado": 5,
        "hierro refinado": 8,
        "cristal de mana": 3
    },
    "espada de ventisca eterna": {
        "cristal de mana": 4,
        "metal encantado": 6,
        "hierro refinado": 7,
        "gema arcana": 3
    },
    "arco de apolo": {
        "madera élfica": 10,
        "cristal de mana": 5,
        "gema arcana": 4,
        "metal encantado": 3
    },
    "baculo de merlin": {
        "cristal de mana": 8,
        "gema arcana": 6,
        "esencia sombría": 2,
        "metal encantado": 4
    },
    "dagas de la noche eterna": {
        "esencia sombría": 3,
        "metal encantado": 4,
        "hierro refinado": 6,
        "colmillo de orco": 2
    },
    "guadaña del vacio cosmico": {
        "esencia sombría": 5,
        "nucleo de golem": 1,
        "cristal de mana": 4,
        "metal encantado": 6
    },
    "excalibur": {
        "cristal de mana": 10,
        "metal encantado": 8,
        "hierro refinado": 12,
        "gema arcana": 5,
        "nucleo de golem": 1
    },
    "armadura del vacío absoluto": {
        "esencia sombría": 8,
        "metal encantado": 10,
        "cuero resistente": 15,
        "cristal de mana": 4
    },
    "túnicas del archimago supremo": {
        "cristal de mana": 12,
        "gema arcana": 10,
        "cuero resistente": 8,
        "esencia sombría": 3
    },
    "armadura solar divina": {
        "cristal de mana": 8,
        "metal encantado": 12,
        "cuero resistente": 10,
        "nucleo de golem": 2
    },
    
    # RECETAS ÉPICAS COMO PASO INTERMEDIO
    "espada de hierro mejorada": {
        "hierro refinado": 5,
        "metal encantado": 2,
        "gema arcana": 1
    },
    "arco de hierro mejorado": {
        "madera élfica": 6,
        "hierro refinado": 3,
        "gema arcana": 2
    },
    "baculo de hierro mejorado": {
        "cristal de mana": 4,
        "metal encantado": 3,
        "gema arcana": 2
    }
}


recetas_crafteo_restringidas = {
    # SOLO OBJETOS MÍTICOS (los más poderosos)
    "espada infernal de fuego eterno": {
        "nucleo de golem": 2,
        "metal encantado": 5,
        "hierro refinado": 8,
        "cristal de mana": 3
    },
    "espada de ventisca eterna": {
        "cristal de mana": 4,
        "metal encantado": 6,
        "hierro refinado": 7,
        "gema arcana": 3
    },
    "arco de apolo": {
        "madera élfica": 10,
        "cristal de mana": 5,
        "gema arcana": 4,
        "metal encantado": 3
    },
    "baculo de merlin": {
        "cristal de mana": 8,
        "gema arcana": 6,
        "esencia sombría": 2,
        "metal encantado": 4
    },
    "dagas de la noche eterna": {
        "esencia sombría": 3,
        "metal encantado": 4,
        "hierro refinado": 6,
        "colmillo de orco": 2
    },
    "guadaña del vacio cosmico": {
        "esencia sombría": 5,
        "nucleo de golem": 1,
        "cristal de mana": 4,
        "metal encantado": 6
    },
    "excalibur": {
        "cristal de mana": 10,
        "metal encantado": 8,
        "hierro refinado": 12,
        "gema arcana": 5,
        "nucleo de golem": 1
    },
    "armadura del vacío absoluto": {
        "esencia sombría": 8,
        "metal encantado": 10,
        "cuero resistente": 15,
        "cristal de mana": 4
    },
    "túnicas del archimago supremo": {
        "cristal de mana": 12,
        "gema arcana": 10,
        "cuero resistente": 8,
        "esencia sombría": 3
    },
    "armadura solar divina": {
        "cristal de mana": 8,
        "metal encantado": 12,
        "cuero resistente": 10,
        "nucleo de golem": 2
    }
}
    
    
# =============================================================================
# FUNCIONES AUXILIARES Y UTILIDADES
# =============================================================================

def validar_entrada_numerica(prompt, min_val=None, max_val=None):
    """Valida entrada numérica con límites opcionales"""
    while True:
        try:
            valor = int(input(prompt))
            if min_val is not None and valor < min_val:
                print(f"Valor debe ser al menos {min_val}")
                continue
            if max_val is not None and valor > max_val:
                print(f"Valor debe ser como máximo {max_val}")
                continue
            return valor
        except ValueError:
            print("Por favor, ingresa un número válido.")


def calcular_probabilidad_critico():
    """Calcula la probabilidad de crítico basada en destreza"""
    probabilidad_base = 5  # 5% base
    bonus_destreza = destreza // 10  # Cada 10 de destreza = +1% crítico
    return min(50, probabilidad_base + bonus_destreza)  # Máximo 50%


def aplicar_critico(daño_base):
    """Aplica daño crítico si se cumple la probabilidad"""
    probabilidad = calcular_probabilidad_critico()
    if random.randint(1, 100) <= probabilidad:
        daño_critico = int(daño_base * 1.5)
        return daño_critico, True
    return daño_base, False


def calcular_probabilidad_esquive(velocidad_atacante, velocidad_defensor, esquive_base=0):
    """Calcula probabilidad de esquive limitada entre 5% y 80%"""
    diferencia_velocidad = max(0, velocidad_defensor - velocidad_atacante) // 5
    probabilidad = 5 + diferencia_velocidad + esquive_base
    return min(80, max(5, probabilidad))


def obtener_clase_actual():
    """Detecta la clase del jugador basándose en sus stats"""
    if inteligencia >= 40:
        return "Mago"
    elif velocidad >= 25 and esquive >= 15:
        return "Asesino"
    elif destreza >= 35:
        return "Arquero"
    elif max_vida >= 110 or (ataque >= 35 and defensa >= 25):
        return "Guerrero"
    else:
        return "Aventurero"


# =============================================================================
# SISTEMA DE ESTADÍSTICAS Y EQUIPAMIENTO
# =============================================================================

def obtener_stats_objeto(nombre_objeto):
    """Obtiene las estadísticas de un objeto específico"""
    global ataque_arma, max_vida_arma, defensa_arma, max_mana_arma, vida_arma
    global destreza_arma, suerte_arma, inteligencia_arma, velocidad_arma, esquive_arma

    # Resetear stats
    ataque_arma = max_vida_arma = defensa_arma = max_mana_arma = 0
    destreza_arma = suerte_arma = vida_arma = inteligencia_arma = 0
    velocidad_arma = esquive_arma = 0

    nombre = nombre_objeto.lower()

    # ARMAS BÁSICAS
    if nombre == "espada de madera":
        ataque_arma = 8
        defensa_arma = 2
    elif nombre == "arco de madera":
        destreza_arma = 10
        velocidad_arma = 3
    elif nombre == "baculo de madera":
        inteligencia_arma = 12
        max_mana_arma = 15
    elif nombre == "dagas de madera":
        ataque_arma = 6
        velocidad_arma = 5
        suerte_arma = 2

    # ARMAS AVANZADAS
    elif nombre == "espada avanzada":
        ataque_arma = 15
        defensa_arma = 5
        max_vida_arma = 5
    elif nombre == "arco avanzado":
        destreza_arma = 18
        velocidad_arma = 5
        esquive_arma = 3
    elif nombre == "baculo avanzado":
        inteligencia_arma = 20
        max_mana_arma = 25
        velocidad_arma = 3
    elif nombre == "dagas avanzadas":
        ataque_arma = 12
        velocidad_arma = 8
        suerte_arma = 4
        esquive_arma = 2

    # ARMAS DE HIERRO
    elif nombre == "espada de hierro":
        ataque_arma = 25
        defensa_arma = 8
        max_vida_arma = 15
        velocidad_arma = 3
    elif nombre == "arco de hierro":
        destreza_arma = 28
        velocidad_arma = 8
        esquive_arma = 5
        max_vida_arma = 10
    elif nombre == "baculo de hierro":
        inteligencia_arma = 30
        max_mana_arma = 40
        velocidad_arma = 5
        max_vida_arma = 5
    elif nombre == "dagas de hierro":
        ataque_arma = 20
        velocidad_arma = 12
        suerte_arma = 6
        esquive_arma = 4
        max_vida_arma = 5

    # ARMAS LEGENDARIAS
    elif nombre == "excalibur imitacion":
        ataque_arma = 40
        defensa_arma = 15
        max_vida_arma = 25
        velocidad_arma = 5
    elif nombre == "espada de fuego":
        ataque_arma = 35
        defensa_arma = 10
        max_vida_arma = 20
    elif nombre == "espada de ventisca":
        ataque_arma = 35
        defensa_arma = 10
        max_vida_arma = 20
    elif nombre == "arco de los elfos":
        destreza_arma = 35
        velocidad_arma = 15
        esquive_arma = 8
        max_vida_arma = 15
    elif nombre == "baculo de un mago experto":
        inteligencia_arma = 45
        max_mana_arma = 60
        velocidad_arma = 8
        max_vida_arma = 10
    elif nombre == "dagas de la noche":
        ataque_arma = 30
        velocidad_arma = 18
        suerte_arma = 10
        esquive_arma = 6
    elif nombre == "dagas de la luna":
        ataque_arma = 28
        velocidad_arma = 15
        suerte_arma = 12
        esquive_arma = 8
        max_vida_arma = 10
    elif nombre == "guadaña de los muertos":
        ataque_arma = 32
        defensa_arma = 12
        max_vida_arma = 20
        suerte_arma = 5
    elif nombre == "guadaña del vacio":
        ataque_arma = 30
        esquive_arma = 10
        suerte_arma = 15
        velocidad_arma = 8
    elif nombre == "arco de apolo imitacion":
        destreza_arma = 38
        velocidad_arma = 12
        esquive_arma = 6
        max_vida_arma = 18
    elif nombre == "baculo de merlin imitacion":
        inteligencia_arma = 42
        max_mana_arma = 55
        velocidad_arma = 6
        max_vida_arma = 12

    # ARMAS MÍTICAS
    elif nombre == "baculo de merlin":
        inteligencia_arma = 70
        max_mana_arma = 100
        velocidad_arma = 15
        max_vida_arma = 30
    elif nombre == "baculo del rey de los magos":
        inteligencia_arma = 85
        max_mana_arma = 150
        velocidad_arma = 20
        max_vida_arma = 40
    elif nombre == "excalibur":
        ataque_arma = 60
        defensa_arma = 25
        max_vida_arma = 50
        velocidad_arma = 12
        suerte_arma = 5
    elif nombre == "arco del rey de los elfos":
        destreza_arma = 50
        velocidad_arma = 25
        esquive_arma = 15
        max_vida_arma = 35
    elif nombre == "guadaña del vacio cosmico":
        ataque_arma = 45
        esquive_arma = 20
        suerte_arma = 25
        velocidad_arma = 15
        max_vida_arma = 20
    elif nombre == "guadaña del rey de los muertos":
        ataque_arma = 50
        defensa_arma = 30
        max_vida_arma = 60
        velocidad_arma = 10
    elif nombre == "espada infernal de fuego eterno":
        ataque_arma = 55
        defensa_arma = 15
        max_vida_arma = 40
        velocidad_arma = 8
    elif nombre == "espada de ventisca eterna":
        ataque_arma = 55
        defensa_arma = 15
        max_vida_arma = 40
        velocidad_arma = 8
    elif nombre == "dagas de la noche eterna":
        ataque_arma = 45
        velocidad_arma = 30
        esquive_arma = 20
        suerte_arma = 12
    elif nombre == "dagas de la luna llena":
        ataque_arma = 42
        velocidad_arma = 25
        esquive_arma = 25
        suerte_arma = 18
        max_vida_arma = 25
    elif nombre == "arco de apolo":
        destreza_arma = 65
        velocidad_arma = 20
        esquive_arma = 12
        max_vida_arma = 45
        suerte_arma = 8

    # ARMADURAS GUERRERO
    elif nombre == "armadura de cuero reforzado":
        ataque_arma = 2
        max_vida_arma = 5
        defensa_arma = 8
    elif nombre == "armadura de cuero tachonado":
        ataque_arma = 4
        max_vida_arma = 15
        defensa_arma = 12
        velocidad_arma = 2
    elif nombre == "armadura de mallas de hierro":
        ataque_arma = 6
        max_vida_arma = 25
        defensa_arma = 18
        velocidad_arma = 3
        suerte_arma = 2
    elif nombre == "armadura de placas encantadas":
        ataque_arma = 10
        max_vida_arma = 40
        defensa_arma = 25
        velocidad_arma = 5
        suerte_arma = 4
    elif nombre == "armadura del rey arturo":
        ataque_arma = 20
        max_vida_arma = 70
        defensa_arma = 40
        velocidad_arma = 10
        suerte_arma = 8
        esquive_arma = 5

    # ARMADURAS ARQUERO
    elif nombre == "armadura de cuero ligero":
        max_vida_arma = 8
        defensa_arma = 4
        velocidad_arma = 6
        esquive_arma = 3
    elif nombre == "armadura de cuero élfico":
        max_vida_arma = 18
        defensa_arma = 8
        velocidad_arma = 10
        esquive_arma = 6
        destreza_arma = 3
    elif nombre == "armadura de escamas dragón":
        max_vida_arma = 30
        defensa_arma = 12
        velocidad_arma = 15
        esquive_arma = 10
        destreza_arma = 8
    elif nombre == "armadura de hojas ancestrales":
        max_vida_arma = 45
        defensa_arma = 18
        velocidad_arma = 20
        esquive_arma = 15
        destreza_arma = 12
        suerte_arma = 5
    elif nombre == "armadura solar divina":
        max_vida_arma = 65
        defensa_arma = 25
        velocidad_arma = 30
        esquive_arma = 25
        destreza_arma = 20
        suerte_arma = 10

    # ARMADURAS MAGO
    elif nombre == "túnicas de aprendiz":
        max_vida_arma = 10
        defensa_arma = 3
        max_mana_arma = 15
        inteligencia_arma = 8
    elif nombre == "túnicas de seda encantada":
        max_vida_arma = 20
        defensa_arma = 6
        max_mana_arma = 25
        inteligencia_arma = 15
        velocidad_arma = 3
    elif nombre == "túnicas de hilos de mithril":
        max_vida_arma = 35
        defensa_arma = 10
        max_mana_arma = 40
        inteligencia_arma = 25
        velocidad_arma = 5
        suerte_arma = 3
    elif nombre == "túnicas de tejido estelar":
        max_vida_arma = 50
        defensa_arma = 15
        max_mana_arma = 60
        inteligencia_arma = 35
        velocidad_arma = 8
        suerte_arma = 6
    elif nombre == "túnicas del archimago supremo":
        max_vida_arma = 80
        defensa_arma = 25
        max_mana_arma = 100
        inteligencia_arma = 55
        velocidad_arma = 15
        suerte_arma = 12

    # ARMADURAS ASESINO
    elif nombre == "armadura de cuero negro":
        max_vida_arma = 6
        defensa_arma = 2
        velocidad_arma = 8
        esquive_arma = 5
        suerte_arma = 3
    elif nombre == "armadura de sombras menores":
        max_vida_arma = 16
        defensa_arma = 5
        velocidad_arma = 12
        esquive_arma = 8
        suerte_arma = 6
    elif nombre == "armadura de escamas sombría":
        max_vida_arma = 28
        defensa_arma = 8
        velocidad_arma = 18
        esquive_arma = 12
        suerte_arma = 10
        destreza_arma = 5
    elif nombre == "armadura de la noche eterna":
        max_vida_arma = 42
        defensa_arma = 12
        velocidad_arma = 25
        esquive_arma = 18
        suerte_arma = 15
        destreza_arma = 8
    elif nombre == "armadura del vacío absoluto":
        max_vida_arma = 65
        defensa_arma = 20
        velocidad_arma = 40
        esquive_arma = 30
        suerte_arma = 25
        destreza_arma = 15


def mostrar_estadisticas():
    """Muestra las estadísticas completas del jugador y enemigo"""
    print(f"\n=== TUS ESTADÍSTICAS ===")
    print(f"Vida: {vida}/{max_vida}")
    print(f"Maná: {mana}/{max_mana}")
    print(f"Ataque: {ataque}")
    print(f"Defensa: {defensa}")
    print(f"Velocidad: {velocidad}")
    print(f"Destreza: {destreza} (Crítico: {calcular_probabilidad_critico()}%)")
    print(f"Esquive: {esquive}")
    print(f"Inteligencia: {inteligencia}")
    print(f"Suerte: {suerte}")
    print(f"Nivel: {lvl} | XP: {xp}")
    print(f"Puntos de stats: {puntos_de_stats}")
    print(f"Dinero: {dinero_jugador}")

    if estas_en_combate:
        print(f"\n=== ESTADÍSTICAS DEL ENEMIGO ===")
        print(f"Vida: {vida_enemigo}/{max_vida_enemigo}")
        print(f"Ataque: {ataque_enemigo}")
        print(f"Defensa: {defensa_enemigo}")
        print(f"Velocidad: {velocidad_enemigo}")
        print(f"Inteligencia: {inteligencia_enemigo}")
        print(f"Suerte: {suerte_enemigo}")


def distribuir_puntos_de_stats():
    """Sistema para distribuir puntos de estadísticas"""
    global puntos_de_stats, max_vida, ataque, defensa, velocidad, esquive
    global inteligencia, destreza, suerte, vida, max_mana, mana

    while puntos_de_stats > 0:
        print(f"\nTienes {puntos_de_stats} puntos de stats disponibles.")
        print("Estadísticas disponibles:")
        print("1. max_vida - 2. ataque - 3. defensa - 4. velocidad")
        print("5. esquive - 6. inteligencia - 7. destreza - 8. suerte - 9. max_mana")

        stat = input("¿A qué atributo quieres asignar puntos? (nombre o 'salir'): ").lower()

        if stat == "salir":
            print("Has decidido no distribuir más puntos de stats.")
            break

        if stat not in ["max_vida", "ataque", "defensa", "velocidad", "esquive",
                        "inteligencia", "destreza", "suerte", "max_mana"]:
            print("Atributo no reconocido. Por favor, elige uno válido.")
            continue

        cantidad_de_stats = validar_entrada_numerica("¿Cuántos puntos quieres asignar?: ", 1, puntos_de_stats)

        # Aplicar los puntos
        if stat == "max_vida":
            max_vida += cantidad_de_stats
            vida += cantidad_de_stats
        elif stat == "ataque":
            ataque += cantidad_de_stats
        elif stat == "destreza":
            destreza += cantidad_de_stats
        elif stat == "defensa":
            defensa += cantidad_de_stats
        elif stat == "velocidad":
            velocidad += cantidad_de_stats
        elif stat == "esquive":
            esquive += cantidad_de_stats
        elif stat == "inteligencia":
            inteligencia += cantidad_de_stats
        elif stat == "suerte":
            suerte += cantidad_de_stats
        elif stat == "max_mana":
            max_mana += cantidad_de_stats
            mana += cantidad_de_stats

        puntos_de_stats -= cantidad_de_stats
        print(f"Has asignado {cantidad_de_stats} puntos a {stat}.")


# =============================================================================
# SISTEMA DE CONJUNTOS Y EQUIPAMIENTO
# =============================================================================

def verificar_conjunto_activo():
    """Verifica si hay un conjunto de equipamiento activo"""
    if not arma_equipada or not armadura_equipada:
        return None

    arma = arma_equipada[0].lower()
    armadura = armadura_equipada[0].lower()

    for (arma_conjunto, armadura_conjunto), datos in conjuntos_armas_armaduras.items():
        if arma == arma_conjunto and armadura == armadura_conjunto:
            return datos
    return None


def aplicar_bonificacion_conjunto(conjunto_datos):
    """Aplica las bonificaciones de un conjunto"""
    global ataque, defensa, velocidad, inteligencia, destreza

    bonificacion = conjunto_datos["bonificacion"]
    for stat, valor in bonificacion.items():
        if stat == "ataque":
            ataque += valor
        elif stat == "defensa":
            defensa += valor
        elif stat == "velocidad":
            velocidad += valor
        elif stat == "inteligencia":
            inteligencia += valor
        elif stat == "destreza":
            destreza += valor


def remover_bonificacion_conjunto(conjunto_datos):
    """Remueve las bonificaciones de un conjunto"""
    global ataque, defensa, velocidad, inteligencia, destreza

    bonificacion = conjunto_datos["bonificacion"]
    for stat, valor in bonificacion.items():
        if stat == "ataque":
            ataque -= valor
        elif stat == "defensa":
            defensa -= valor
        elif stat == "velocidad":
            velocidad -= valor
        elif stat == "inteligencia":
            inteligencia -= valor
        elif stat == "destreza":
            destreza -= valor

def inicializar_estados_equipamiento():
    global arma_activa, armadura_activa
    
    # Si la lista tiene elementos (len > 0), entonces está activa
    arma_activa = len(arma_equipada) > 0
    armadura_activa = len(armadura_equipada) > 0
    
def equipar_arma(nombre_objeto):
    """Equipa un arma y aplica sus stats"""
    global ataque, defensa, destreza, max_vida, velocidad, esquive
    global inteligencia, suerte, max_mana, vida, mana, arma_activa, inv

    if arma_activa:
        print("Ya tienes equipada un arma, desequípatela primero para cambiarla")
        return

    arma_activa = True
    obtener_stats_objeto(nombre_objeto)
    ataque += ataque_arma
    defensa += defensa_arma
    destreza += destreza_arma
    max_vida += max_vida_arma
    velocidad += velocidad_arma
    esquive += esquive_arma
    inteligencia += inteligencia_arma
    suerte += suerte_arma
    max_mana += max_mana_arma
    vida += max_vida_arma
    mana += max_mana_arma
    if mana > max_mana:
        mana = max_mana

    arma_equipada.append(nombre_objeto)
    inv.remove(nombre_objeto)
    print(f"Has equipado: {nombre_objeto}")

    conjunto_activo = verificar_conjunto_activo()
    if conjunto_activo:
        aplicar_bonificacion_conjunto(conjunto_activo)
        print(f"¡Conjunto activado: {conjunto_activo['nombre']}!")
        print(f"Bonificación: {conjunto_activo['descripcion']}")


def equipar_armadura(nombre_objeto):
    """Equipa una armadura y aplica sus stats"""
    global ataque, defensa, destreza, max_vida, velocidad, esquive
    global inteligencia, suerte, max_mana, vida, mana, armadura_activa, inv

    if armadura_activa:
        print("Ya tienes una armadura puesta, quítate la que tienes puesta primero")
        return

    armadura_activa = True
    obtener_stats_objeto(nombre_objeto)
    ataque += ataque_arma
    defensa += defensa_arma
    destreza += destreza_arma
    max_vida += max_vida_arma
    velocidad += velocidad_arma
    esquive += esquive_arma
    inteligencia += inteligencia_arma
    suerte += suerte_arma
    max_mana += max_mana_arma
    vida += max_vida_arma
    mana += max_mana_arma
    if mana > max_mana:
        mana = max_mana

    armadura_equipada.append(nombre_objeto)
    inv.remove(nombre_objeto)
    print(f"Has equipado: {nombre_objeto}")

    conjunto = verificar_conjunto_activo()
    if conjunto:
        aplicar_bonificacion_conjunto(conjunto)
        print(f"¡Conjunto completado: {conjunto['nombre']}!")
        print(f"Bonificación: {conjunto['descripcion']}")


def desequipar_arma(nombre_objeto):
    """Desequipa un arma y remueve sus stats"""
    global ataque, defensa, destreza, max_vida, velocidad, esquive
    global inteligencia, suerte, max_mana, vida, mana, arma_activa, inv

    if not arma_activa:
        print("No tienes ningún arma equipada")
        return

    conjunto_previo = verificar_conjunto_activo()
    if conjunto_previo:
        remover_bonificacion_conjunto(conjunto_previo)

    arma_activa = False
    obtener_stats_objeto(nombre_objeto)
    ataque -= ataque_arma
    defensa -= defensa_arma
    destreza -= destreza_arma
    max_vida -= max_vida_arma
    velocidad -= velocidad_arma
    esquive -= esquive_arma
    inteligencia -= inteligencia_arma
    suerte -= suerte_arma
    max_mana -= max_mana_arma

    if vida > max_vida:
        vida = max_vida
    if mana > max_mana:
        mana = max_mana

    arma_equipada.remove(nombre_objeto)
    inv.append(nombre_objeto)
    print(f"Has desequipado: {nombre_objeto}")


def desequipar_armadura(nombre_objeto):
    """Desequipa una armadura y remueve sus stats"""
    global ataque, defensa, destreza, max_vida, velocidad, esquive
    global inteligencia, suerte, max_mana, vida, mana, armadura_activa, inv

    if not armadura_activa:
        print("No tienes ninguna armadura puesta")
        return

    conjunto_previo = verificar_conjunto_activo()
    if conjunto_previo:
        remover_bonificacion_conjunto(conjunto_previo)

    armadura_activa = False
    obtener_stats_objeto(nombre_objeto)
    ataque -= ataque_arma
    defensa -= defensa_arma
    destreza -= destreza_arma
    max_vida -= max_vida_arma
    velocidad -= velocidad_arma
    esquive -= esquive_arma
    inteligencia -= inteligencia_arma
    suerte -= suerte_arma
    max_mana -= max_mana_arma

    if vida > max_vida:
        vida = max_vida
    if mana > max_mana:
        mana = max_mana

    armadura_equipada.remove(nombre_objeto)
    inv.append(nombre_objeto)
    print(f"Has desequipado: {nombre_objeto}")


# =============================================================================
# SISTEMA DE INVENTARIO
# =============================================================================

def inventario():
    """Sistema de inventario mejorado"""
    global inv, vida, mana, max_vida, max_mana

    if not inv and not arma_equipada and not armadura_equipada:
        print("Tu inventario está vacío y no tienes equipamiento.")
        return

    if inv:
        print("Objetos en tu inventario:")
        for i, objeto in enumerate(inv, 1):
            print(f"{i}. {objeto}")
    else:
        print("Tu inventario está vacío.")

    if arma_equipada or armadura_equipada:
        print("\nEquipamiento actual:")
        if arma_equipada:
            print(f"Arma: {arma_equipada[0]}")
        if armadura_equipada:
            print(f"Armadura: {armadura_equipada[0]}")

    accion_inventario = input(
        "\n¿Qué quieres hacer? (usar objeto / equipar objeto / desequipar objeto / ver detalles objeto / salir del inventario): ").lower()

    if accion_inventario == "usar objeto":
        usar_objeto_inventario()
    elif accion_inventario == "equipar objeto":
        equipar_objeto_inventario()
    elif accion_inventario == "desequipar objeto":
        desequipar_objeto_inventario()
    elif accion_inventario == "ver detalles objeto":
        ver_detalles_objeto()
    elif accion_inventario == "salir del inventario":
        return
    else:
        print("Acción no reconocida.")
        inventario()


def usar_objeto_inventario():
    """Sistema para usar objetos consumibles"""
    global vida, mana, max_vida, max_mana, inv

    if not inv:
        print("No tienes objetos en el inventario.")
        return

    objeto_a_usar = input("¿Qué objeto quieres usar? ").lower()

    if objeto_a_usar not in inv:
        print("No tienes ese objeto en el inventario.")
        return

    if objeto_a_usar == "pocion de vida pequeña":
        vida += 20
        inv.remove(objeto_a_usar)
        if vida > max_vida:
            vida = max_vida
        print(f"Has usado {objeto_a_usar}. Tu vida ha aumentado a {vida}.")
    elif objeto_a_usar == "pocion de mana pequeña":
        mana += 20
        inv.remove(objeto_a_usar)
        if mana > max_mana:
            mana = max_mana
        print(f"Has usado {objeto_a_usar}. Tu mana ha aumentado a {mana}.")
    elif objeto_a_usar == "pocion de vida mediana":
        vida += 50
        inv.remove(objeto_a_usar)
        if vida > max_vida:
            vida = max_vida
        print(f"Has usado {objeto_a_usar}. Tu vida ha aumentado a {vida}.")
    elif objeto_a_usar == "pocion de mana mediana":
        mana += 50
        inv.remove(objeto_a_usar)
        if mana > max_mana:
            mana = max_mana
        print(f"Has usado {objeto_a_usar}. Tu mana ha aumentado a {mana}.")
    elif objeto_a_usar == "pocion de vida grande":
        vida += 100
        inv.remove(objeto_a_usar)
        if vida > max_vida:
            vida = max_vida
        print(f"Has usado {objeto_a_usar}. Tu vida ha aumentado a {vida}.")
    elif objeto_a_usar == "pocion de mana grande":
        mana += 100
        inv.remove(objeto_a_usar)
        if mana > max_mana:
            mana = max_mana
        print(f"Has usado {objeto_a_usar}. Tu mana ha aumentado a {mana}.")
    else:
        print("Este objeto no se puede usar.")


def equipar_objeto_inventario():
    """Sistema para equipar objetos"""
    if not inv:
        print("No tienes objetos en el inventario para equipar.")
        return

    objeto_a_equipar = input("¿Qué objeto quieres equipar? ").lower()
    if objeto_a_equipar not in inv:
        print("No tienes ese objeto en el inventario.")
        return

    # Determinar si es arma o armadura
    armas_palabras = ["espada", "arco", "baculo", "dagas", "guadaña"]
    armaduras_palabras = ["armadura", "túnicas"]

    es_arma = any(palabra in objeto_a_equipar for palabra in armas_palabras)
    es_armadura = any(palabra in objeto_a_equipar for palabra in armaduras_palabras)

    if es_arma:
        equipar_arma(objeto_a_equipar)
    elif es_armadura:
        equipar_armadura(objeto_a_equipar)
    else:
        print("No se puede equipar este objeto.")


def desequipar_objeto_inventario():
    """Sistema para desequipar objetos"""
    if not arma_equipada and not armadura_equipada:
        print("No tienes objetos equipados.")
        return

    objeto_desequipar = input("¿Qué objeto quieres desequipar? ").lower()

    if arma_equipada and objeto_desequipar in [arma.lower() for arma in arma_equipada]:
        desequipar_arma(arma_equipada[0])
    elif armadura_equipada and objeto_desequipar in [armadura.lower() for armadura in armadura_equipada]:
        desequipar_armadura(armadura_equipada[0])
    else:
        print("No tienes ese objeto equipado.")


def ver_detalles_objeto():
    """Muestra detalles completos de un objeto"""
    todos_objetos = inv + arma_equipada + armadura_equipada
    if not todos_objetos:
        print("No tienes objetos para examinar.")
        return

    objeto_ver = input("¿Qué objeto quieres examinar? ").lower()

    # Buscar objeto (case insensitive)
    objeto_encontrado = None
    for obj in todos_objetos:
        if obj.lower() == objeto_ver:
            objeto_encontrado = obj
            break

    if not objeto_encontrado:
        print("No tienes ese objeto.")
        return

    # Obtener y mostrar stats del objeto
    obtener_stats_objeto(objeto_encontrado)
    print(f"\n=== DETALLES DE {objeto_encontrado.upper()} ===")

    stats_mostrados = []
    if ataque_arma > 0:
        stats_mostrados.append(f"Ataque: +{ataque_arma}")
    if defensa_arma > 0:
        stats_mostrados.append(f"Defensa: +{defensa_arma}")
    if max_vida_arma > 0:
        stats_mostrados.append(f"Vida Máxima: +{max_vida_arma}")
    if velocidad_arma > 0:
        stats_mostrados.append(f"Velocidad: +{velocidad_arma}")
    if inteligencia_arma > 0:
        stats_mostrados.append(f"Inteligencia: +{inteligencia_arma}")
    if destreza_arma > 0:
        stats_mostrados.append(f"Destreza: +{destreza_arma}")
    if suerte_arma > 0:
        stats_mostrados.append(f"Suerte: +{suerte_arma}")
    if esquive_arma > 0:
        stats_mostrados.append(f"Esquive: +{esquive_arma}")
    if max_mana_arma > 0:
        stats_mostrados.append(f"Mana Máxima: +{max_mana_arma}")

    if stats_mostrados:
        for stat in stats_mostrados:
            print(stat)
    else:
        print("Este objeto no proporciona bonificaciones de stats.")

    # Mostrar valor del objeto
    if objeto_encontrado in valores_objetos:
        print(f"Valor: {valores_objetos[objeto_encontrado]} monedas")

    # Mostrar habilidad especial si la tiene
    if objeto_encontrado.lower() in habilidades_armas:
        habilidad = habilidades_armas[objeto_encontrado.lower()]
        print(f"\n🌟 HABILIDAD ESPECIAL:")
        print(f"   {habilidad['nombre'].replace('_', ' ').title()}")
        print(f"   Probabilidad: {habilidad['chance']}%")

    # Mostrar si forma parte de un conjunto
    for (arma_conj, armadura_conj), datos in conjuntos_armas_armaduras.items():
        if objeto_ver == arma_conj or objeto_ver == armadura_conj:
            print(f"\nCONJUNTO: {datos['nombre']}")
            otra_pieza = armadura_conj if objeto_ver == arma_conj else arma_conj
            print(f"   Se completa con: {otra_pieza}")
            print(f"   Bonificación: {datos['descripcion']}")

            # Verificar si tiene la otra pieza
            tiene_otra_pieza = False
            for obj in todos_objetos:
                if obj.lower() == otra_pieza:
                    tiene_otra_pieza = True
                    break

            if tiene_otra_pieza:
                print(f"   ¡TIENES LA OTRA PIEZA DEL CONJUNTO!")
            else:
                print(f"   Te falta la otra pieza del conjunto")

    print("=" * 40)


# =============================================================================
# SISTEMA DE GUARDADO Y CARGA
# =============================================================================

def mostrar_slots_guardado():
    """Muestra el estado de los 3 slots de guardado"""
    print("\n" + "=" * 50)
    print("📁 SLOTS DE GUARDADO DISPONIBLES")
    print("=" * 50)

    for i in range(1, 4):
        archivo_slot = f'partida_slot{i}.json'
        if os.path.exists(archivo_slot):
            try:
                with open(archivo_slot, 'r', encoding='utf-8') as f:
                    datos = json.load(f)

                nivel = datos.get('nivel', 1)
                nombre = datos.get('nombre', 'Aventurero')
                clase = datos.get('clase', 'Desconocida')
                turnos_guardados = datos.get('turnos', 0)

                timestamp = os.path.getmtime(archivo_slot)
                fecha = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")

                print(f"🟢 SLOT {i}: {nombre} - {clase} Nivel {nivel}")
                print(f"    Turnos: {turnos_guardados} | Guardado: {fecha}")

            except Exception:
                print(f"🟡 SLOT {i}: Archivo corrupto o ilegible")
        else:
            print(f"🔴 SLOT {i}: Vacío")

    print("=" * 50)


def guardar_partida():
    """Guarda el progreso del jugador en un slot específico"""
    global lvl, xp, vida, max_vida, mana, max_mana, ataque, defensa, velocidad
    global destreza, esquive, inteligencia, suerte, inv, dinero_jugador
    global arma_equipada, armadura_equipada, turnos, puntos_de_stats

    print("\n🎮 GUARDAR PARTIDA")
    mostrar_slots_guardado()

    slot = validar_entrada_numerica("\n¿En qué slot quieres guardar? (1, 2, 3) o (0 para cancelar): ", 0, 3)
    if slot == 0:
        print("Guardado cancelado.")
        return False

    archivo_slot = f'partida_slot{slot}.json'

    # Verificar si el slot ya tiene una partida guardada
    if os.path.exists(archivo_slot):
        try:
            with open(archivo_slot, 'r', encoding='utf-8') as f:
                datos_existentes = json.load(f)

            nombre_existente = datos_existentes.get('nombre', 'Aventurero')
            clase_existente = datos_existentes.get('clase', 'Desconocida')
            nivel_existente = datos_existentes.get('nivel', 1)

            print(f"\n⚠️  ADVERTENCIA: El Slot {slot} ya contiene una partida:")
            print(f"   {nombre_existente} - {clase_existente} Nivel {nivel_existente}")

            confirmacion = input("¿Quieres SOBREESCRIBIR esta partida? (si/no): ").lower()
            if confirmacion != "si":
                print("Guardado cancelado.")
                return False
        except Exception:
            pass

    nombre_jugador = input("Ingresa tu nombre para identificar esta partida: ").strip()
    if not nombre_jugador:
        nombre_jugador = "Aventurero"

    datos = {
        'nombre': nombre_jugador,
        'clase': obtener_clase_actual(),
        'nivel': lvl,
        'xp': xp,
        'vida': vida,
        'max_vida': max_vida,
        'mana': mana,
        'max_mana': max_mana,
        'ataque': ataque,
        'defensa': defensa,
        'velocidad': velocidad,
        'destreza': destreza,
        'esquive': esquive,
        'inteligencia': inteligencia,
        'suerte': suerte,
        'inventario': inv,
        'dinero': dinero_jugador,
        'arma_equipada': arma_equipada,
        'armadura_equipada': armadura_equipada,
        'turnos': turnos,
        'puntos_de_stats': puntos_de_stats,
        'fecha_guardado': datetime.now().isoformat()
    }

    try:
        with open(archivo_slot, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print(f"✅ Partida guardada exitosamente en el Slot {slot}.")
        return True
    except Exception as e:
        print(f"❌ Error al guardar la partida: {e}")
        return False


def cargar_partida():
    """Carga el progreso del jugador desde un slot específico"""
    global lvl, xp, vida, max_vida, mana, max_mana, ataque, defensa, velocidad
    global destreza, esquive, inteligencia, suerte, inv, dinero_jugador
    global arma_equipada, armadura_equipada, turnos, puntos_de_stats
    global arma_activa, armadura_activa

    print("\n📂 CARGAR PARTIDA")
    mostrar_slots_guardado()

    slots_disponibles = []
    for i in range(1, 4):
        if os.path.exists(f'partida_slot{i}.json'):
            slots_disponibles.append(i)

    if not slots_disponibles:
        print("\n❌ No hay partidas guardadas.")
        return False

    print(f"\nSlots disponibles para cargar: {', '.join(map(str, slots_disponibles))}")

    while True:
        slot = validar_entrada_numerica("¿Qué slot quieres cargar? (0 para cancelar): ", 0, 3)
        if slot == 0:
            print("Carga cancelada.")
            return False
        elif slot in slots_disponibles:
            break
        else:
            print(f"Slot {slot} no está disponible.")

    archivo_slot = f'partida_slot{slot}.json'

    try:
        with open(archivo_slot, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        # Cargar todas las variables con valores por defecto
        lvl = datos.get('nivel', 1)
        xp = datos.get('xp', 0)
        vida = datos.get('vida', 100)
        max_vida = datos.get('max_vida', 100)
        mana = datos.get('mana', 0)
        max_mana = datos.get('max_mana', 0)
        ataque = datos.get('ataque', 20)
        defensa = datos.get('defensa', 10)
        velocidad = datos.get('velocidad', 15)
        destreza = datos.get('destreza', 10)
        esquive = datos.get('esquive', 5)
        inteligencia = datos.get('inteligencia', 10)
        suerte = datos.get('suerte', 1)
        inv = datos.get('inventario', [])
        dinero_jugador = datos.get('dinero', 0)
        arma_equipada = datos.get('arma_equipada', [])
        armadura_equipada = datos.get('armadura_equipada', [])
        turnos = datos.get('turnos', 0)
        puntos_de_stats = datos.get('puntos_de_stats', 0)

        # Actualizar estados de equipamiento
        
        inicializar_estados_equipamiento()

        nombre = datos.get('nombre', 'Aventurero')
        clase = datos.get('clase', 'Aventurero')

        print(f"✅ Partida cargada exitosamente del Slot {slot}.")
        print(f"🎮 Bienvenido de vuelta, {nombre} ({clase})!")
        print(f"📊 Nivel {lvl} | {vida}/{max_vida} HP | {mana}/{max_mana} MP")
        print(f"💰 Dinero: {dinero_jugador} | Turnos: {turnos}")

        return True

    except FileNotFoundError:
        print(f"❌ No se encontró el archivo del Slot {slot}.")
        return False
    except json.JSONDecodeError:
        print(f"❌ El archivo del Slot {slot} está corrupto.")
        return False
    except Exception as e:
        print(f"❌ Error al cargar la partida: {e}")
        return False


def eliminar_partida():
    """Función para eliminar partidas guardadas"""
    print("\n🗑️ ELIMINAR PARTIDA")
    mostrar_slots_guardado()

    slots_disponibles = []
    for i in range(1, 4):
        if os.path.exists(f'partida_slot{i}.json'):
            slots_disponibles.append(i)

    if not slots_disponibles:
        print("\n❌ No hay partidas para eliminar.")
        return

    print(f"\nSlots disponibles para eliminar: {', '.join(map(str, slots_disponibles))}")

    slot = validar_entrada_numerica("¿Qué slot quieres eliminar? (0 para cancelar): ", 0, 3)
    if slot == 0:
        print("Operación cancelada.")
        return
    elif slot not in slots_disponibles:
        print(f"Slot {slot} no tiene partida guardada.")
        return

    archivo_slot = f'partida_slot{slot}.json'
    try:
        with open(archivo_slot, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        nombre = datos.get('nombre', 'Aventurero')
        clase = datos.get('clase', 'Desconocida')
        nivel = datos.get('nivel', 1)

        print(f"\n⚠️  Vas a eliminar permanentemente:")
        print(f"   Slot {slot}: {nombre} - {clase} Nivel {nivel}")

        confirmacion = input("¿Estás SEGURO? Esta acción no se puede deshacer (si/no): ").lower()
        if confirmacion == "si":
            os.remove(archivo_slot)
            print(f"✅ Partida del Slot {slot} eliminada exitosamente.")
        else:
            print("Eliminación cancelada.")

    except Exception as e:
        print(f"❌ Error al eliminar la partida: {e}")


# =============================================================================
# SISTEMA DE HECHIZOS Y BUFFS
# =============================================================================

def gestionar_buffs():
    """Reduce la duración de los buffs activos y elimina los que expiraron"""
    global buffs_activos, ataque, defensa, velocidad

    buffs_a_eliminar = []
    for buff_nombre, buff_data in buffs_activos.items():
        buff_data['duracion'] -= 1
        if buff_data['duracion'] <= 0:
            stat = buff_data['stat']
            valor = buff_data['valor']

            if stat == "ataque":
                ataque -= valor
            elif stat == "defensa":
                defensa -= valor
            elif stat == "velocidad":
                velocidad -= valor

            buffs_a_eliminar.append(buff_nombre)
            print(f"El buff {buff_nombre} ha expirado.")

    for buff in buffs_a_eliminar:
        del buffs_activos[buff]


def lanzar_hechizo():
    """Sistema de hechizos corregido - NO consume turno de ataque completo"""
    global mana, vida, max_vida, vida_enemigo, ataque, defensa, velocidad, buffs_activos
    global enemigo_congelado, turnos_congelacion, enemigo_quemado, turnos_quemadura, daño_quemadura

    if inteligencia < 20:
        print("No tienes suficiente inteligencia para lanzar hechizos.")
        return False

    print("\n=== HECHIZOS DISPONIBLES ===")
    for nombre, datos in hechizos_disponibles.items():
        disponible = "✓" if mana >= datos['costo'] else "✗"
        print(f"{disponible} {nombre.title()}: {datos['descripcion']} (Costo: {datos['costo']} mana)")

    hechizo = input("\n¿Qué hechizo quieres lanzar? (o 'cancelar'): ").lower()

    if hechizo == 'cancelar':
        return False

    if hechizo not in hechizos_disponibles:
        print("Hechizo no reconocido.")
        return False

    datos_hechizo = hechizos_disponibles[hechizo]

    if mana < datos_hechizo['costo']:
        print(f"No tienes suficiente maná. Necesitas {datos_hechizo['costo']} pero tienes {mana}")
        return False

    # Consumir maná
    mana -= datos_hechizo['costo']

    # HECHIZOS DE DAÑO NORMAL
    if datos_hechizo['tipo'] == 'daño':
        daño_base = datos_hechizo['daño_base'] + (inteligencia // 5)
        daño_final = max(1, daño_base - defensa_enemigo)
        daño_final, fue_critico = aplicar_critico(daño_final)

        vida_enemigo -= daño_final
        print(f"¡{hechizo.title()}! Causas {daño_final} de daño mágico.")
        if fue_critico:
            print("¡Crítico mágico!")
        
        print(f"Maná restante: {mana}/{max_mana}")
        return True

    # HECHIZOS DE DAÑO CON CONGELACIÓN
    elif datos_hechizo['tipo'] == 'daño_congelacion':
        daño_base = datos_hechizo['daño_base'] + (inteligencia // 5)
        daño_final = max(1, daño_base - defensa_enemigo)
        daño_final, fue_critico = aplicar_critico(daño_final)

        vida_enemigo -= daño_final
        print(f"¡{hechizo.title()}! Causas {daño_final} de daño helado.")
        
        if fue_critico:
            print("¡Crítico mágico!")

        # Verificar congelación independientemente del crítico
        if not enemigo_congelado and random.randint(1, 100) <= 30:
            enemigo_congelado = True
            turnos_congelacion = 2
            print("¡El enemigo ha sido congelado por 2 turnos!")
        
        print(f"Maná restante: {mana}/{max_mana}")
        return True

    # HECHIZOS DE CURACIÓN
    elif datos_hechizo['tipo'] == 'curacion':
        curacion = datos_hechizo['curacion'] + (inteligencia // 10)
        vida_anterior = vida
        vida = min(max_vida, vida + curacion)
        curacion_real = vida - vida_anterior
        print(f"¡{hechizo.title()}! Te curas {curacion_real} puntos de vida.")
        
        print(f"Maná restante: {mana}/{max_mana}")
        return True

    # HECHIZOS DE BUFF
    elif datos_hechizo['tipo'] == 'buff':
        buff_stat = datos_hechizo['buff_stat']
        buff_valor = datos_hechizo['buff_valor']
        duracion = datos_hechizo['duracion']

        if hechizo in buffs_activos:
            print("Ya tienes este buff activo.")
            mana += datos_hechizo['costo']  # Devolver el maná
            return False

        # Aplicar buff
        buffs_activos[hechizo] = {
            'stat': buff_stat,
            'valor': buff_valor,
            'duracion': duracion
        }

        if buff_stat == "ataque":
            ataque += buff_valor
        elif buff_stat == "defensa":
            defensa += buff_valor
        elif buff_stat == "velocidad":
            velocidad += buff_valor

        print(f"¡{hechizo.title()}! {buff_stat.title()} aumentado en {buff_valor} por {duracion} turnos.")
        print(f"Maná restante: {mana}/{max_mana}")
        return True
    
    # HECHIZOS DE ÁREA/DEVASTADORES
    elif datos_hechizo['tipo'] == 'daño_area':
        daño_base = datos_hechizo['daño_base'] + (inteligencia // 3)
        daño_final = max(1, daño_base - defensa_enemigo)
        daño_final, fue_critico = aplicar_critico(daño_final)

        vida_enemigo -= daño_final
        print(f"¡{hechizo.title()}! ¡Tormenta devastadora de {daño_final} de daño!")
        
        if fue_critico:
            print("¡Crítico mágico devastador!")
        
        print(f"Maná restante: {mana}/{max_mana}")
        return True

    return False


# =============================================================================
# SISTEMA DE COMBATE Y EFECTOS
# =============================================================================

def aplicar_efectos_estado():
    """Aplica los efectos de estado al inicio del turno del enemigo - CORREGIDO"""
    global vida_enemigo, enemigo_quemado, turnos_quemadura, daño_quemadura
    global enemigo_congelado, turnos_congelacion

    # Aplicar daño por quemadura
    if enemigo_quemado:
        vida_enemigo -= daño_quemadura
        print(f"El enemigo recibe {daño_quemadura} puntos de daño por quemadura.")
        turnos_quemadura -= 1

        if turnos_quemadura <= 0:
            enemigo_quemado = False
            daño_quemadura = 0
            print("La quemadura del enemigo ha terminado.")

    # Manejar congelación
    if enemigo_congelado:
        print("El enemigo está congelado y no puede moverse.")
        turnos_congelacion -= 1
        
        if turnos_congelacion <= 0:
            enemigo_congelado = False
            print("El enemigo ya no está congelado.")

def reset_efectos_combate():
    """Limpia todos los efectos de combate al finalizar - FUNCIÓN CORREGIDA"""
    global buffs_activos, enemigo_quemado, turnos_quemadura, daño_quemadura
    global enemigo_congelado, turnos_congelacion, ataque, defensa, velocidad

    # Remover efectos de buffs activos del jugador ANTES de limpiar el diccionario
    for buff_nombre, buff_data in buffs_activos.items():
        stat = buff_data['stat']
        valor = buff_data['valor']
        
        if stat == "ataque":
            ataque -= valor
        elif stat == "defensa":
            defensa -= valor
        elif stat == "velocidad":
            velocidad -= valor
    
    # Ahora sí limpiar el diccionario
    buffs_activos.clear()
    
    # Limpiar efectos de estado del enemigo
    enemigo_quemado = False
    turnos_quemadura = 0
    daño_quemadura = 0
    enemigo_congelado = False
    turnos_congelacion = 0


def activar_habilidad_arma(nombre_arma, daño_base):
    """Activa la habilidad especial del arma si se cumple el porcentaje de chance"""
    global enemigo_quemado, turnos_quemadura, daño_quemadura, enemigo_congelado, turnos_congelacion

    if nombre_arma not in habilidades_armas:
        return daño_base, "", {}

    habilidad = habilidades_armas[nombre_arma]

    if random.randint(1, 100) > habilidad["chance"]:
        return daño_base, "", {}

    efecto = habilidad["efecto"]
    nombre_habilidad = habilidad['nombre'].replace('_', ' ').title()
    mensaje = f"¡{nombre_habilidad}!"
    efectos_estado = {}

    if efecto == "critico_1_5":
        daño_modificado = int(daño_base * 1.5)
        mensaje_completo = f"{mensaje} Daño crítico x1.5"
    elif efecto == "critico_2_0":
        daño_modificado = int(daño_base * 2.0)
        mensaje_completo = f"{mensaje} Hechizo devastador x2.0"
    elif efecto == "critico_1_8":
        daño_modificado = int(daño_base * 1.8)
        mensaje_completo = f"{mensaje} Ataque sombra x1.8"
    elif efecto == "ignora_defensa":
        daño_modificado = daño_base + defensa_enemigo
        mensaje_completo = f"{mensaje} Ignora toda la defensa enemiga"
    elif efecto == "ignora_defensa_critico":
        daño_modificado = int((daño_base + defensa_enemigo) * 1.5)
        mensaje_completo = f"{mensaje} Corte divino: ignora defensa y daño crítico x1.5"
    elif efecto == "dano_fijo_50":
        daño_modificado = daño_base + 50
        mensaje_completo = f"{mensaje} +50 daño solar"
    elif efecto == "doble_ataque":
        daño_extra = max(1, daño_base - defensa_enemigo)
        daño_modificado = daño_base + daño_extra
        mensaje_completo = f"{mensaje} Disparo doble: {daño_base} + {daño_extra} daño"
    elif efecto == "quemadura_5_3":
        daño_modificado = daño_base
        if not enemigo_quemado:
            efectos_estado = {
                'quemadura': True,
                'turnos_quemadura': 3,
                'daño_quemadura': 5
            }
            mensaje_completo = f"{mensaje} El enemigo está en llamas (5 daño x 3 turnos)"
        else:
            mensaje_completo = f"{mensaje} (El enemigo ya está quemándose)"
    elif efecto == "congelacion_2":
        daño_modificado = daño_base
        if not enemigo_congelado:
            efectos_estado = {
                'congelacion': True,
                'turnos_congelacion': 2
            }
            mensaje_completo = f"{mensaje} El enemigo está congelado (2 turnos sin atacar)"
        else:
            mensaje_completo = f"{mensaje} (El enemigo ya está congelado)"
    else:
        daño_modificado = daño_base
        mensaje_completo = f"{mensaje} (Efecto desconocido: {efecto})"

    return daño_modificado, mensaje_completo, efectos_estado


def aplicar_efectos_estado_arma(efectos):
    """Aplica los efectos de estado generados por las habilidades de armas"""
    global enemigo_quemado, turnos_quemadura, daño_quemadura, enemigo_congelado, turnos_congelacion

    if 'quemadura' in efectos and efectos['quemadura']:
        enemigo_quemado = True
        turnos_quemadura = efectos['turnos_quemadura']
        daño_quemadura = efectos['daño_quemadura']

    if 'congelacion' in efectos and efectos['congelacion']:
        enemigo_congelado = True
        turnos_congelacion = efectos['turnos_congelacion']


def accion_ataque_yo():
    """Función de ataque del jugador mejorada"""
    global vida_enemigo, arma_equipada, ataque, defensa_enemigo

    daño_base = max(1, ataque - defensa_enemigo)

    # Verificar esquive del enemigo
    probabilidad_esquive = calcular_probabilidad_esquive(velocidad, velocidad_enemigo)
    if random.randint(1, 100) <= probabilidad_esquive:
        print("El enemigo ha esquivado tu ataque.")
        return

    # Aplicar crítico basado en destreza
    daño_con_critico, fue_critico = aplicar_critico(daño_base)

    # Activar habilidad de arma si está equipada
    mensaje_habilidad = ""
    efectos_estado = {}

    if arma_equipada:
        nombre_arma = arma_equipada[0].lower()
        daño_final, mensaje_habilidad, efectos_estado = activar_habilidad_arma(nombre_arma, daño_con_critico)

        if efectos_estado:
            aplicar_efectos_estado_arma(efectos_estado)
    else:
        daño_final = daño_con_critico

    # Aplicar daño
    vida_enemigo -= daño_final
    print(f"Atacas y le infliges {daño_final} puntos de daño al enemigo.")

    # Mostrar si fue crítico
    if fue_critico and not mensaje_habilidad:
        print("¡Golpe crítico!")

    # Mostrar mensaje de habilidad si se activó
    if mensaje_habilidad:
        print(mensaje_habilidad)

    # Verificar si el enemigo fue derrotado
    if vida_enemigo <= 0:
        vida_enemigo = 0
        print(f"Vida del enemigo: {vida_enemigo}")
        accion_derrotar_enemigo()
    else:
        print(f"Vida del enemigo: {vida_enemigo}")


def accion_ataque_enemigo():
    """Función de ataque del enemigo mejorada"""
    global vida, ataque_enemigo, defensa, enemigo_congelado

    # Verificar si el enemigo está congelado
    if enemigo_congelado:
        print("El enemigo está congelado y no puede atacar.")
        return

    # Calcular probabilidad de esquive del jugador
    probabilidad_esquive_jugador = calcular_probabilidad_esquive(velocidad_enemigo, velocidad, esquive)
    if random.randint(1, 100) <= probabilidad_esquive_jugador:
        print("Has esquivado el ataque del enemigo.")
        return

    daño_recibido = max(1, ataque_enemigo - defensa)

    print(f"El enemigo te ataca y te inflige {daño_recibido} puntos de daño.")
    vida -= daño_recibido
    print(f"Tu vida: {vida}")

    if vida <= 0:
        vida = 0
        print("Has sido derrotado. Fin del juego.")
        exit()


def accion_de_combate():
    """Sistema de combate principal con orden correcto de hechizos"""
    global vida_enemigo, turnos_en_combate, estas_en_combate
    turnos_en_combate = 1

    while vida_enemigo > 0 and vida > 0:
        print(f"\n=== TURNO DE COMBATE {turnos_en_combate} ===")

        # Aplicar efectos de estado al inicio del turno
        aplicar_efectos_estado()

        # Gestionar buffs del jugador
        gestionar_buffs()

        # Verificar si el enemigo murió por efectos de estado
        if vida_enemigo <= 0:
            vida_enemigo = 0
            print("El enemigo ha sido derrotado por efectos de estado.")
            accion_derrotar_enemigo()
            return

        # Mostrar información del combate
        print(f"Tu vida: {vida}/{max_vida} | Maná: {mana}/{max_mana}")
        print(f"Vida del enemigo: {vida_enemigo}/{max_vida_enemigo}")

        # Mostrar buffs activos
        if buffs_activos:
            print("Buffs activos:")
            for buff_nombre, buff_data in buffs_activos.items():
                print(f"  - {buff_nombre.title()}: +{buff_data['valor']} {buff_data['stat']} ({buff_data['duracion']} turnos)")

        accion = input("\n¿Qué quieres hacer? (atacar / hechizo / inventario / ver stats / huir / pausa): ").lower()

        if accion == "atacar":
            # Orden de ataque basado en velocidad
            if velocidad >= velocidad_enemigo:
                accion_ataque_yo()
                if vida_enemigo > 0:
                    accion_ataque_enemigo()
            else:
                accion_ataque_enemigo()
                if vida > 0:
                    accion_ataque_yo()

        elif accion == "hechizo":
            # CORREGIDO: Verificar orden de velocidad para hechizos también
            if velocidad >= velocidad_enemigo:
                # Jugador es más rápido, lanza hechizo primero
                if lanzar_hechizo():
                    if vida_enemigo <= 0:
                        accion_derrotar_enemigo()
                        return
                    # Enemigo ataca después si está vivo
                    accion_ataque_enemigo()
                else:
                    continue  # Hechizo cancelado, no consume turno
            else:
                # Enemigo es más rápido, ataca primero
                accion_ataque_enemigo()
                if vida > 0:
                    # Jugador lanza hechizo después si está vivo
                    if lanzar_hechizo():
                        if vida_enemigo <= 0:
                            accion_derrotar_enemigo()
                            return
                    else:
                        continue  # Hechizo cancelado

        elif accion == "huir":
            print("Has huido del combate.")
            estas_en_combate = False
            reset_efectos_combate()  # Limpiar efectos al huir
            eleccion_de_camino_def()
            return

        elif accion == "inventario":
            inventario()
            continue  # No consume turno

        elif accion == "ver stats":
            mostrar_estadisticas()
            distribuir = input("¿Deseas distribuir puntos de stats? (si/no): ").lower()
            if distribuir == "si" and puntos_de_stats > 0:
                distribuir_puntos_de_stats()
            continue  # No consume turno

        elif accion == "pausa":
            menu_pausa()
            continue  # No consume turno

        else:
            print("Acción no reconocida.")
            continue

        turnos_en_combate += 1


# =============================================================================
# SISTEMA DE ENEMIGOS
# =============================================================================

def accion_derrotar_enemigo():
    """Función mejorada para cuando derrotas un enemigo"""
    global xp, lvl, puntos_de_stats, enemigo_encontrado, xp_del_enemigo, estas_en_combate, dinero, dinero_jugador, turnos_congelacion, turnos_quemadura
    print(f"¡Has derrotado al {enemigo_encontrado}!, sigues avanzando por el camino.")
    xp += xp_del_enemigo
    dinero_jugador += dinero
    estas_en_combate = False
    reset_efectos_combate()
    obtener_drops_enemigo(enemigo_encontrado)
    # Sistema de level up mejorado
    nivel_anterior = lvl
    while xp >= lvl * lvl + 9 * lvl:
        xp -= (lvl * lvl + 9 * lvl)
        lvl += 1
        puntos_de_stats += 10

    if lvl > nivel_anterior:
        print(f"¡Felicidades! Has subido al nivel {lvl}!")
        print(f"Te falta {(lvl * lvl + 9 * lvl) - xp} de XP para el próximo nivel.")
        print(f"Tienes {puntos_de_stats} puntos de stats para distribuir.")

    print(f"Has ganado {dinero} de dinero. Dinero total: {dinero_jugador}")
    estas_en_combate = False
    eleccion_de_camino_def()


def enemigo_debil():
    """Genera un enemigo débil"""
    global max_vida_enemigo, vida_enemigo, ataque_enemigo, defensa_enemigo, velocidad_enemigo
    global dinero, inteligencia_enemigo, xp_del_enemigo, enemigo_encontrado, estas_en_combate, turnos, suerte_enemigo
    estas_en_combate = True
    enemigo_encontrado = "Slime"
    xp_del_enemigo = 10
    dinero = 100
    turnos += 1
    iniciar_nuevo_combate(enemigo_encontrado)

    max_vida_enemigo = random.randint(50, 60)
    vida_enemigo = max_vida_enemigo
    ataque_enemigo = random.randint(10, 15)
    defensa_enemigo = random.randint(5, 10)
    velocidad_enemigo = random.randint(7, 10)
    inteligencia_enemigo = random.randint(1, 5)
    suerte_enemigo = random.randint(0, 2)

    print(f"Has encontrado un {enemigo_encontrado} (Turno {turnos}), ¡Prepárate para luchar!")
    if turnos > 5:
        multiplicador = 1 + (turnos * 0.1)
        max_vida_enemigo = int(max_vida_enemigo * multiplicador)
        vida_enemigo = max_vida_enemigo
        ataque_enemigo = int(ataque_enemigo * multiplicador)
        defensa_enemigo = int(defensa_enemigo * multiplicador)
        velocidad_enemigo = int(velocidad_enemigo * multiplicador)
        inteligencia_enemigo = int(inteligencia_enemigo * multiplicador)
        print("El enemigo parece más fuerte debido al tiempo transcurrido en la cueva...")

    accion_de_combate()


def enemigo():
    """Genera un enemigo normal"""
    global max_vida_enemigo, ataque_enemigo, defensa_enemigo, velocidad_enemigo, vida_enemigo
    global dinero, inteligencia_enemigo, xp_del_enemigo, enemigo_encontrado, estas_en_combate, turnos, suerte_enemigo
    if turnos < 5:
        num_camino()
    estas_en_combate = True
    enemigo_encontrado = "Goblin"
    dinero = 250
    xp_del_enemigo = 40
    turnos += 1
    iniciar_nuevo_combate(enemigo_encontrado)

    max_vida_enemigo = random.randint(80, 100)
    vida_enemigo = max_vida_enemigo
    ataque_enemigo = random.randint(18, 28)
    defensa_enemigo = random.randint(12, 20)
    velocidad_enemigo = random.randint(15, 20)
    inteligencia_enemigo = random.randint(8, 15)
    suerte_enemigo = random.randint(2, 4)

    print(f"Has encontrado un {enemigo_encontrado} (Turno {turnos}), ¡Prepárate para luchar!")
    if turnos > 5:
        multiplicador = 1 + (turnos * 0.1)
        max_vida_enemigo = int(max_vida_enemigo * multiplicador)
        vida_enemigo = max_vida_enemigo
        ataque_enemigo = int(ataque_enemigo * multiplicador)
        defensa_enemigo = int(defensa_enemigo * multiplicador)
        velocidad_enemigo = int(velocidad_enemigo * multiplicador)
        inteligencia_enemigo = int(inteligencia_enemigo * multiplicador)
        print("El enemigo parece más fuerte debido al tiempo transcurrido en la cueva...")

    accion_de_combate()


def enemigo_fuerte():
    """Genera un enemigo fuerte"""
    global max_vida_enemigo, ataque_enemigo, vida_enemigo, defensa_enemigo, velocidad_enemigo
    global inteligencia_enemigo, dinero, xp_del_enemigo, enemigo_encontrado, estas_en_combate, turnos, suerte_enemigo
    estas_en_combate = True
    enemigo_encontrado = "Orco"
    dinero = 750
    xp_del_enemigo = 100
    turnos += 1
    iniciar_nuevo_combate(enemigo_encontrado)

    max_vida_enemigo = random.randint(110, 140)
    vida_enemigo = max_vida_enemigo
    ataque_enemigo = random.randint(30, 40)
    defensa_enemigo = random.randint(18, 35)
    velocidad_enemigo = random.randint(15, 30)
    inteligencia_enemigo = random.randint(12, 20)
    suerte_enemigo = random.randint(4, 6)

    print(f"Has encontrado un {enemigo_encontrado} (Turno {turnos}), ¡Prepárate para luchar!")
    if turnos > 5:
        multiplicador = 1 + (turnos * 0.1)
        max_vida_enemigo = int(max_vida_enemigo * multiplicador)
        vida_enemigo = max_vida_enemigo
        ataque_enemigo = int(ataque_enemigo * multiplicador)
        defensa_enemigo = int(defensa_enemigo * multiplicador)
        velocidad_enemigo = int(velocidad_enemigo * multiplicador)
        inteligencia_enemigo = int(inteligencia_enemigo * multiplicador)
        print("El enemigo parece más fuerte debido al tiempo transcurrido en la cueva...")

    accion_de_combate()


def enemigo_Golem():
    """Genera un Golem"""
    global max_vida_enemigo, ataque_enemigo, vida_enemigo, defensa_enemigo, velocidad_enemigo
    global inteligencia_enemigo, dinero, xp_del_enemigo, enemigo_encontrado, estas_en_combate, turnos, suerte_enemigo
    estas_en_combate = True
    enemigo_encontrado = "Golem"
    dinero = 1250
    xp_del_enemigo = 300
    turnos += 1
    iniciar_nuevo_combate(enemigo_encontrado)

    max_vida_enemigo = random.randint(160, 180)
    vida_enemigo = max_vida_enemigo
    ataque_enemigo = random.randint(40, 50)
    defensa_enemigo = random.randint(60, 75)
    velocidad_enemigo = random.randint(13, 15)
    inteligencia_enemigo = random.randint(10, 16)
    suerte_enemigo = random.randint(4, 5)

    print(f"Has encontrado un {enemigo_encontrado} (Turno {turnos}), ¡Prepárate para luchar!")
    if turnos > 5:
        multiplicador = 1 + (turnos * 0.1)
        max_vida_enemigo = int(max_vida_enemigo * multiplicador)
        vida_enemigo = max_vida_enemigo
        ataque_enemigo = int(ataque_enemigo * multiplicador)
        defensa_enemigo = int(defensa_enemigo * multiplicador)
        velocidad_enemigo = int(velocidad_enemigo * multiplicador)
        inteligencia_enemigo = int(inteligencia_enemigo * multiplicador)
        print("El enemigo parece más fuerte debido al tiempo transcurrido en la cueva...")

    accion_de_combate()

def iniciar_nuevo_combate(nombre_enemigo):
    """Limpia efectos de combates anteriores al iniciar uno nuevo"""
    global enemigo_quemado, turnos_quemadura, daño_quemadura, enemigo_congelado, turnos_congelacion
    
    # Limpiar efectos de estado del enemigo anterior
    enemigo_quemado = False
    turnos_quemadura = 0
    daño_quemadura = 0
    enemigo_congelado = False
    turnos_congelacion = 0
    
    print(f"¡Nuevo combate iniciado contra {nombre_enemigo}!")
    
# =============================================================================
# SISTEMA DE EXPLORACIÓN Y TESOROS
# =============================================================================

def obtener_objetos_disponibles():
    """Devuelve los objetos disponibles según los turnos transcurridos"""
    objetos_disponibles = []
    objetos_disponibles.extend(objeto_comun)

    if turnos >= 3:
        objetos_disponibles.extend(objeto_raro)
    if turnos >= 8:
        objetos_disponibles.extend(objeto_epico)
    if turnos >= 15:
        objetos_disponibles.extend(objeto_legendario)
    if turnos >= 25:
        objetos_disponibles.extend(objeto_mitico)

    return objetos_disponibles


def generar_rareza_comun():
    """Genera objetos de tesoros comunes"""
    global turnos, inv
    rareza = random.randint(1, 10000)

    if turnos < 3:
        objeto_generado = random.choice(objeto_comun)
        print(f"Has encontrado un objeto común: {objeto_generado}")
    elif turnos < 8:
        if rareza <= 7000:
            objeto_generado = random.choice(objeto_comun)
            print(f"Has encontrado un objeto común: {objeto_generado}")
        else:
            objeto_generado = random.choice(objeto_raro)
            print(f"Has encontrado un objeto raro: {objeto_generado}")
    elif turnos < 15:
        if rareza <= 5000:
            objeto_generado = random.choice(objeto_comun)
            print(f"Has encontrado un objeto común: {objeto_generado}")
        elif rareza <= 7500:
            objeto_generado = random.choice(objeto_raro)
            print(f"Has encontrado un objeto raro: {objeto_generado}")
        else:
            objeto_generado = random.choice(objeto_epico)
            print(f"Has encontrado un objeto épico: {objeto_generado}")
    elif turnos < 25:
        if rareza <= 5000:
            objeto_generado = random.choice(objeto_comun)
            print(f"Has encontrado un objeto común: {objeto_generado}")
        elif rareza <= 7500:
            objeto_generado = random.choice(objeto_raro)
            print(f"Has encontrado un objeto raro: {objeto_generado}")
        elif rareza <= 9000:
            objeto_generado = random.choice(objeto_epico)
            print(f"Has encontrado un objeto épico: {objeto_generado}")
        elif rareza <= 9700:
            objeto_generado = random.choice(objeto_legendario)
            print(f"Has encontrado un objeto legendario: {objeto_generado}")
        else:
            objeto_generado = random.choice(objeto_mitico)
            print(f"Has encontrado un objeto mítico: {objeto_generado}")

    inv.append(objeto_generado)
    eleccion_de_camino_def()


def generar_rareza_dorado():
    """Genera objetos de tesoros dorados (mejor probabilidad)"""
    global turnos, inv
    rareza = random.randint(1, 10000)

    if turnos < 3:
        if rareza <= 5000:
            objeto_generado = random.choice(objeto_comun)
            print(f"Has encontrado un objeto común: {objeto_generado}")
        else:
            objeto_generado = random.choice(objeto_raro) if objeto_raro else random.choice(objeto_comun)
            print(f"Has encontrado un objeto raro: {objeto_generado}")
    elif turnos < 8:
        if rareza <= 3000:
            objeto_generado = random.choice(objeto_comun)
            print(f"Has encontrado un objeto común: {objeto_generado}")
        elif rareza <= 6000:
            objeto_generado = random.choice(objeto_raro)
            print(f"Has encontrado un objeto raro: {objeto_generado}")
        else:
            objeto_generado = random.choice(objeto_epico)
            print(f"Has encontrado un objeto épico: {objeto_generado}")
    elif turnos < 15:
        if rareza <= 2000:
            objeto_generado = random.choice(objeto_comun)
            print(f"Has encontrado un objeto común: {objeto_generado}")
        elif rareza <= 4500:
            objeto_generado = random.choice(objeto_raro)
            print(f"Has encontrado un objeto raro: {objeto_generado}")
        elif rareza <= 7500:
            objeto_generado = random.choice(objeto_epico)
            print(f"Has encontrado un objeto épico: {objeto_generado}")
        else:
            objeto_generado = random.choice(objeto_legendario)
            print(f"Has encontrado un objeto legendario: {objeto_generado}")
    else:
        if rareza <= 2000:
            objeto_generado = random.choice(objeto_comun)
            print(f"Has encontrado un objeto común: {objeto_generado}")
        elif rareza <= 4500:
            objeto_generado = random.choice(objeto_raro)
            print(f"Has encontrado un objeto raro: {objeto_generado}")
        elif rareza <= 7500:
            objeto_generado = random.choice(objeto_epico)
            print(f"Has encontrado un objeto épico: {objeto_generado}")
        elif rareza <= 9000:
            objeto_generado = random.choice(objeto_legendario)
            print(f"Has encontrado un objeto legendario: {objeto_generado}")
        else:
            objeto_generado = random.choice(objeto_mitico)
            print(f"Has encontrado un objeto mítico: {objeto_generado}")

    inv.append(objeto_generado)
    eleccion_de_camino_def()
    
def generar_pociones_inicio():
    """Genera pociones para los primeros turnos"""
    global inv
    pociones_disponibles = [
        "pocion de vida pequeña",
        "pocion de mana pequeña"
    ]
    
    # Generar 1-2 pociones
    cantidad = random.randint(1, 2)
    for _ in range(cantidad):
        pocion = random.choice(pociones_disponibles)
        inv.append(pocion)
        print(f"Has encontrado: {pocion}")
    
    eleccion_de_camino_def()
    
def num_camino():
    """Función modificada con restricciones de progresión por turnos"""
    global turnos
    camino = random.randint(1, 10000)
    
    # RESTRICCIONES POR TURNOS - Solo enemigos débiles al inicio
    if turnos < 6:
        # Turnos 1-5: Solo enemigos débiles, tesoros y pociones
        if camino <= 6500:
            enemigo_debil()
        elif camino <= 8000:
            print("¡Se encontró con un tesoro! ¡Felicidades!")
            turnos += 1
            generar_rareza_comun()
        elif camino <= 9500:
            print("Encontraste algunas pociones abandonadas.")
            turnos += 1
            generar_pociones_inicio()
        else:
            print("¡Se encontró con un tesoro dorado! ¡Qué suerte!")
            turnos += 1
            generar_rareza_dorado()
    
    # TURNOS 6-11: Enemigos normales desbloqueados
    elif turnos < 12:
        if camino <= 3000:
            enemigo_debil()
        elif camino <= 5500:
            enemigo()  # Goblin desbloqueado
        elif camino <= 7000:
            print("¡Se encontró con un tesoro! ¡Felicidades!")
            turnos += 1
            generar_rareza_comun()
        elif camino <= 8000:
            print("Se encontró con la tienda")
            tienda()
        elif camino <= 9000:
            print("¡Se encontró con un tesoro dorado! ¡Qué suerte!")
            turnos += 1
            generar_rareza_dorado()
        else:
            herreria()
    
    # TURNOS 12-17: Enemigos fuertes desbloqueados
    elif turnos < 18:
        if camino <= 2500:
            enemigo_debil()
        elif camino <= 4500:
            enemigo()
        elif camino <= 6000:
            enemigo_fuerte()  # Orco desbloqueado
        elif camino <= 7500:
            print("¡Se encontró con un tesoro! ¡Felicidades!")
            turnos += 1
            generar_rareza_comun()
        elif camino <= 8500:
            print("Se encontró con la tienda")
            tienda()
        elif camino <= 9200:
            print("¡Se encontró con un tesoro dorado! ¡Qué suerte!")
            turnos += 1
            generar_rareza_dorado()
        else:
            herreria()
    
    # TURNOS 18+: Todos los enemigos desbloqueados
    else:
        if camino <= 2000:
            enemigo_debil()
        elif camino <= 4000:
            enemigo()
        elif camino <= 5500:
            enemigo_fuerte()
        elif camino <= 6800:
            enemigo_Golem()  # Golem desbloqueado
        elif camino <= 7800:
            print("¡Se encontró con un tesoro! ¡Felicidades!")
            turnos += 1
            generar_rareza_comun()
        elif camino <= 8600:
            print("Se encontró con la tienda")
            tienda()
        elif camino <= 9100:
            print("¡Se encontró con un tesoro dorado! ¡Qué suerte!")
            turnos += 1
            generar_rareza_dorado()
        else:
            herreria()


def eleccion_de_camino_def():
    """Función para elegir el camino a seguir"""
    global eleccion_de_camino
    
    while True:
        print(f"\nTurnos transcurridos: {turnos}")
        eleccion_de_camino = input("¿Hacia dónde quieres ir? (izquierda / derecha / derecho / pausa): ").lower()

        if eleccion_de_camino in ["izquierda", "derecha", "derecho"]:
            num_camino()
            break
        elif eleccion_de_camino == "pausa":
            menu_pausa()
            # Continúa el loop para preguntar de nuevo
        else:
            print("Elección no reconocida. Por favor elige: izquierda, derecha, derecho o pausa")
            # Continúa el loop automáticamente


# =============================================================================
# SISTEMA DE TIENDA
# =============================================================================

def tienda():
    """Función de tienda con restricción de aparición por turnos"""
    global objetos_en_tienda, turnos
    
    # RESTRICCIÓN: Tienda no disponible hasta turno 6
    if turnos < 6:
        print("Encuentras los restos de una tienda abandonada, pero no hay nada útil aquí.")
        print("Parece que necesitas adentrarte más en la cueva...")
        eleccion_de_camino_def()
        return
    
    objetos_en_tienda = []
    turnos += 1
    print(f"Turnos transcurridos: {turnos}")
    rerol_tienda()
    volver_a_tienda()


def rerol_tienda():
    """Genera objetos para la tienda según el progreso"""
    global objetos_en_tienda, turnos
    objetos_en_tienda = []

    for i in range(5):
        rareza_tienda = random.randint(1, 10000)

        if turnos < 3:
            objeto_generado = random.choice(objeto_comun)
        elif turnos < 8:
            if rareza_tienda <= 6000:
                objeto_generado = random.choice(objeto_comun)
            else:
                objeto_generado = random.choice(objeto_raro)
        elif turnos < 15:
            if rareza_tienda <= 4000:
                objeto_generado = random.choice(objeto_comun)
            elif rareza_tienda <= 7000:
                objeto_generado = random.choice(objeto_raro)
            else:
                objeto_generado = random.choice(objeto_epico)
        elif turnos < 25:
            if rareza_tienda <= 3000:
                objeto_generado = random.choice(objeto_comun)
            elif rareza_tienda <= 5500:
                objeto_generado = random.choice(objeto_raro)
            elif rareza_tienda <= 8000:
                objeto_generado = random.choice(objeto_epico)
            else:
                objeto_generado = random.choice(objeto_legendario)
        else:
            if rareza_tienda <= 2000:
                objeto_generado = random.choice(objeto_comun)
            elif rareza_tienda <= 4000:
                objeto_generado = random.choice(objeto_raro)
            elif rareza_tienda <= 6500:
                objeto_generado = random.choice(objeto_epico)
            elif rareza_tienda <= 8500:
                objeto_generado = random.choice(objeto_legendario)
            else:
                objeto_generado = random.choice(objeto_mitico)

        precio = valores_objetos.get(objeto_generado, 100)
        print(f"Objeto en tienda: {objeto_generado} - Precio: {precio}")
        objetos_en_tienda.append(objeto_generado)


def volver_a_tienda():
    """Menú principal de la tienda"""
    accion_tienda = input("¿Qué desea hacer? (comprar objeto / vender objeto / seguir camino): ").lower()

    if accion_tienda == "comprar objeto":
        accion_comprar_tienda()
    elif accion_tienda == "vender objeto":
        accion_vender_tienda()
    elif accion_tienda == "seguir camino":
        num_camino()
    else:
        print("Opción no válida.")
        volver_a_tienda()


def accion_comprar_tienda():
    """Sistema de compra en la tienda"""
    global valores_objetos, inv, dinero_jugador, objetos_en_tienda

    if not objetos_en_tienda:
        print("No hay objetos disponibles en la tienda.")
        volver_a_tienda()
        return

    print("\nObjetos disponibles para comprar:")
    for i, objeto in enumerate(objetos_en_tienda, 1):
        precio = valores_objetos.get(objeto, 100)
        print(f"{i}. {objeto} - Precio: {precio}")

    while True:
        accion_de_compra = input("¿Qué objeto desea comprar? (nombre del objeto o 'salir'): ").lower()
        if accion_de_compra == "salir":
            volver_a_tienda()
            return

        if accion_de_compra in objetos_en_tienda:
            precio = valores_objetos.get(accion_de_compra, 100)
            if dinero_jugador >= precio:
                if avisar_conjunto_al_comprar(accion_de_compra):
                    confirmacion = input(f"¿Estás seguro de comprar {accion_de_compra} por {precio}? (si/no): ").lower()
                    if confirmacion == "si":
                        dinero_jugador -= precio
                        inv.append(accion_de_compra)
                        objetos_en_tienda.remove(accion_de_compra)
                        print(f"Has comprado {accion_de_compra}. Tu dinero restante es: {dinero_jugador}")
                        volver_a_tienda()
                        return
            else:
                print(f"No tienes suficiente dinero. Te faltan {precio - dinero_jugador}")
        else:
            print("Objeto no disponible en la tienda.")


def accion_vender_tienda():
    """Sistema de venta RESTRINGIDO - Solo épico para arriba"""
    global dinero_jugador, arma_equipada, armadura_equipada, inv, valores_objetos

    # Filtrar solo objetos épicos, legendarios y míticos
    objetos_vendibles = []
    todos_objetos = inv + arma_equipada + armadura_equipada
    
    for objeto in todos_objetos:
        if (objeto in objeto_epico or 
            objeto in objeto_legendario or 
            objeto in objeto_mitico):
            objetos_vendibles.append(objeto)
    
    if not objetos_vendibles:
        print("La tienda solo acepta objetos de calidad ÉPICA o superior.")
        print("No tienes objetos de suficiente calidad para vender.")
        volver_a_tienda()
        return

    print("\nTus objetos VENDIBLES (Épico+) en la tienda:")
    for objeto in objetos_vendibles:
        precio_venta = calcular_precio_venta(objeto)
        estado = " (EQUIPADO)" if objeto in arma_equipada or objeto in armadura_equipada else ""
        
        # Mostrar rareza del objeto
        if objeto in objeto_epico:
            rareza = "ÉPICO"
        elif objeto in objeto_legendario:
            rareza = "LEGENDARIO"
        elif objeto in objeto_mitico:
            rareza = "MÍTICO"
        
        print(f"- {objeto}{estado} [{rareza}] - Precio de venta: {precio_venta}")

    accion_vender = input("¿Qué objeto desea vender? ('salir' para volver): ").lower()

    if accion_vender == 'salir':
        volver_a_tienda()
        return

    if accion_vender in objetos_vendibles:
        precio_venta = calcular_precio_venta(accion_vender)

        # Remover objeto de donde esté
        if accion_vender in inv:
            inv.remove(accion_vender)
        elif accion_vender in arma_equipada:
            desequipar_arma(accion_vender)
        elif accion_vender in armadura_equipada:
            desequipar_armadura(accion_vender)

        dinero_jugador += precio_venta
        print(f"Se vendió exitosamente {accion_vender}. Tu dinero es: {dinero_jugador}")
        accion_vender_tienda()
    else:
        if accion_vender in todos_objetos:
            print("La tienda no acepta objetos de calidad inferior a ÉPICO.")
        else:
            print("No tienes ese objeto.")
        accion_vender_tienda()


def calcular_precio_venta(objeto):
    """Calcula el precio de venta basado en la rareza del objeto"""
    precio_base = valores_objetos.get(objeto, 100)

    if objeto in objeto_comun:
        return int(precio_base * 0.30)
    elif objeto in objeto_raro:
        return int(precio_base * 0.30)
    elif objeto in objeto_epico:
        return int(precio_base * 0.35)
    elif objeto in objeto_legendario:
        return int(precio_base * 0.35)
    elif objeto in objeto_mitico:
        return int(precio_base * 0.40)



def avisar_conjunto_al_comprar(objeto_a_comprar):
    """Avisa si el objeto completará un conjunto"""
    for (arma_conj, armadura_conj), datos in conjuntos_armas_armaduras.items():
        if objeto_a_comprar == arma_conj or objeto_a_comprar == armadura_conj:
            otra_pieza = armadura_conj if objeto_a_comprar == arma_conj else arma_conj

            todos_objetos = inv + arma_equipada + armadura_equipada
            if otra_pieza in todos_objetos:
                print(f"¡AVISO DE CONJUNTO!")
                print(f"Si compras '{objeto_a_comprar}' completarás el conjunto:")
                print(f"{datos['nombre']}")
                print(f"Bonificación: {datos['descripcion']}")
                confirmacion_conjunto = input("¿Aún quieres comprarlo? (si/no): ").lower()
                return confirmacion_conjunto == "si"
    return True


# =============================================================================
# SISTEMA DE HERRERIA Y SISTEMA DE DROPS
# =============================================================================


def menu_herreria():
    """Menú principal de la herrería"""
    print(f"\n🔥 ¿Qué deseas hacer en la herrería?")
    print("1. Ver recetas disponibles")
    print("2. Craftear objeto")
    print("3. Ver mis materiales")
    print("4. Salir de la herrería")
    
    opcion = validar_entrada_numerica("Elige una opción (1-4): ", 1, 4)
    
    if opcion == 1:
        ver_recetas_disponibles()
    elif opcion == 2:
        craftear_objeto()
    elif opcion == 3:
        ver_materiales_crafteo()
    elif opcion == 4:
        print("El herrero se despide cordialmente.")
        eleccion_de_camino_def()
        
        
def herreria():
    """Sistema de herrería con restricción de aparición por turnos"""
    global turnos
    
    # RESTRICCIÓN: Herrería no disponible hasta turno 8
    if turnos < 8:
        print("Encuentras una forja antigua y fría. No hay herrero aquí todavía.")
        print("Quizás si exploras más profundo encuentres al maestro herrero...")
        eleccion_de_camino_def()
        return
    
    turnos += 1
    print(f"¡Bienvenido a la Herrería Ancestral! ")
    print(f"Turnos transcurridos: {turnos}")
    print("El herrero te saluda con una sonrisa y te muestra sus servicios.")
    
    menu_herreria()

def ver_materiales_crafteo():
    """Muestra todos los materiales de crafteo del jugador"""
    print(f"\n📦 TUS MATERIALES DE CRAFTEO:")
    
    if not materiales_crafteo:
        print("No tienes materiales de crafteo.")
        menu_herreria()
        return
    
    print("\n--- MATERIALES COMUNES ---")
    for material, cantidad in materiales_crafteo.items():
        if material in materiales_comunes:
            print(f"  {material}: {cantidad} - {materiales_comunes[material]}")
    
    print("\n--- MATERIALES ESPECIALES ---")
    for material, cantidad in materiales_crafteo.items():
        if material in materiales_especiales:
            print(f"  {material}: {cantidad} - {materiales_especiales[material]}")
    
    input("\nPresiona Enter para continuar...")
    menu_herreria()




def ver_recetas_disponibles():
    """Muestra todas las recetas y qué materiales tienes/necesitas"""
    print(f"\n📋 RECETAS DISPONIBLES:")
    
    for objeto, receta in recetas_crafteo.items():
        print(f"\n🔸 {objeto.upper()}")
        puede_craftear = True
        
        for material, cantidad_necesaria in receta.items():
            cantidad_actual = materiales_crafteo.get(material, 0)
            
            if cantidad_actual >= cantidad_necesaria:
                estado = "✅"
            else:
                estado = "❌"
                puede_craftear = False
            
            print(f"   {estado} {material}: {cantidad_actual}/{cantidad_necesaria}")
        
        if puede_craftear:
            print("   🎉 ¡PUEDES CRAFTEARLO!")
        else:
            print("   ⏳ Necesitas más materiales")
    
    input("\nPresiona Enter para continuar...")
    menu_herreria()

def craftear_objeto():
    """Sistema para craftear SOLO objetos épicos y superiores"""
    global materiales_crafteo, inv
    
    objetos_crafteables = []
    
    print(f"\n🔥 OBJETOS ÉPICOS+ QUE PUEDES CRAFTEAR:")
    
    # Verificar qué objetos se pueden craftear
    for objeto, receta in recetas_crafteo_restringidas.items():
        puede_craftear = True
        for material, cantidad_necesaria in receta.items():
            if materiales_crafteo.get(material, 0) < cantidad_necesaria:
                puede_craftear = False
                break
        
        if puede_craftear:
            objetos_crafteables.append(objeto)
            print(f"🎯 {objeto}")
    
    if not objetos_crafteables:
        print("❌ No tienes suficientes materiales para craftear objetos épicos.")
        print("Los objetos comunes y raros no se pueden craftear aquí.")
        menu_herreria()
        return
    
    objeto_elegido = input(f"\n¿Qué objeto quieres craftear? ('salir' para volver): ").lower()
    
    if objeto_elegido == 'salir':
        menu_herreria()
        return
    
    if objeto_elegido in objetos_crafteables:
        # Mostrar resumen del crafteo
        print(f"\n🔥 CRAFTEANDO: {objeto_elegido.upper()}")
        print("Materiales que se consumirán:")
        
        receta = recetas_crafteo_restringidas[objeto_elegido]
        for material, cantidad in receta.items():
            print(f"  - {material}: {cantidad}")
        
        confirmacion = input("\n¿Confirmas el crafteo? (si/no): ").lower()
        
        if confirmacion == "si":
            # Consumir materiales
            for material, cantidad in receta.items():
                materiales_crafteo[material] -= cantidad
                if materiales_crafteo[material] <= 0:
                    del materiales_crafteo[material]
            
            # Dar el objeto
            inv.append(objeto_elegido)
            
            print(f"\n🎉 ¡CRAFTEO EXITOSO! 🎉")
            print(f"Has crafteado: {objeto_elegido}")
            print(f"El objeto ha sido añadido a tu inventario.")
            print("El herrero sonríe orgulloso de su trabajo épico.")
            menu_herreria()
        else:
            print("Crafteo cancelado.")
            menu_herreria()
    else:
        print("Objeto no disponible para craftear o no es de calidad épica+.")
        craftear_objeto()


def obtener_drops_enemigo(nombre_enemigo):
    """Versión mejorada que otorga materiales de crafteo al derrotar enemigos"""
    global materiales_crafteo
    
    if nombre_enemigo not in drops_enemigos:
        print(f"No se encontraron materiales del {nombre_enemigo}.")
        return
    
    drops_obtenidos = []
    drops_especiales = []
    
    for material, probabilidad in drops_enemigos[nombre_enemigo].items():
        if random.randint(1, 10000) <= probabilidad:
            if material in materiales_crafteo:
                materiales_crafteo[material] += 1
            else:
                materiales_crafteo[material] = 1
            
            drops_obtenidos.append(material)
            
            # Verificar si es material especial
            if material in materiales_especiales:
                drops_especiales.append(material)
    
    if drops_obtenidos:
        print(f"\n✨ MATERIALES OBTENIDOS DEL {nombre_enemigo.upper()}:")
        for material in drops_obtenidos:
            cantidad_actual = materiales_crafteo[material]
            print(f"   + {material} (Total: {cantidad_actual})")
            
        # Mensaje especial para materiales raros
        if drops_especiales:
            print(f"\n🌟 ¡MATERIAL ESPECIAL OBTENIDO! 🌟")
            for material in drops_especiales:
                print(f"   ⭐ {material}")
                print(f"   📝 {materiales_especiales[material]}")

def verificar_objetos_crafteable():
    """Función para verificar que todos los objetos crafteables existen en las listas"""
    objetos_inexistentes = []
    
    for objeto in recetas_crafteo.keys():
        encontrado = False
        todas_las_listas = objeto_comun + objeto_raro + objeto_epico + objeto_legendario + objeto_mitico
        
        if objeto in todas_las_listas:
            encontrado = True
        
        if not encontrado:
            objetos_inexistentes.append(objeto)
    
    if objetos_inexistentes:
        print("⚠️ OBJETOS CRAFTEABLES NO ENCONTRADOS EN LISTAS:")
        for obj in objetos_inexistentes:
            print(f"   - {obj}")
    else:
        print("✅ Todos los objetos crafteables existen en las listas de objetos.")
        
        
def debug_materiales():
    """Función de debug para agregar materiales manualmente (solo para pruebas)"""
    global materiales_crafteo
    
    print("🔧 MODO DEBUG - AGREGANDO MATERIALES DE PRUEBA")
    
    # Agregar algunos materiales para pruebas
    test_materials = {
        "hierro refinado": 10,
        "cuero resistente": 8,
        "gema arcana": 5,
        "metal encantado": 3,
        "cristal de mana": 2,
        "nucleo de golem": 1
    }
    
    for material, cantidad in test_materials.items():
        materiales_crafteo[material] = cantidad
    
    print("Materiales de prueba agregados:")
    for material, cantidad in test_materials.items():
        print(f"   + {material}: {cantidad}")



# =============================================================================
# SISTEMA DE MENÚS Y NAVEGACIÓN
# =============================================================================

def menu_pausa():
    """Menú de pausa durante la aventura"""
    while True:
        print("\n⏸️ MENÚ DE PAUSA")
        print("1. 💾 Guardar partida")
        print("2. 📊 Ver estadísticas")
        print("3. 🎒 Inventario")
        print("4. 🔧 Distribuir puntos de stats")
        print("5. ▶️ Continuar aventura")
        print("6. 🚪 Salir del juego")

        opcion = validar_entrada_numerica("Elige una opción (1-6): ", 1, 6)

        if opcion == 1:
            guardar_partida()
        elif opcion == 2:
            mostrar_estadisticas()
        elif opcion == 3:
            inventario()
        elif opcion == 4:
            if puntos_de_stats > 0:
                distribuir_puntos_de_stats()
            else:
                print("No tienes puntos de stats para distribuir.")
        elif opcion == 5:
            return
        elif opcion == 6:
            confirmar = input("¿Quieres guardar antes de salir? (si/no): ").lower()
            if confirmar == "si":
                if guardar_partida():
                    print("¡Gracias por jugar! Progreso guardado.")
                else:
                    print("Error al guardar, pero gracias por jugar.")
            else:
                print("¡Gracias por jugar!")
            exit()


# =============================================================================
# FUNCIÓN PRINCIPAL Y SELECCIÓN DE CLASE
# =============================================================================

def main():
    """Función principal del juego completamente corregida"""
    global max_vida, vida, ataque, defensa, velocidad, esquive, inteligencia, destreza, suerte, max_mana, mana, turnos
    global arma_activa, armadura_activa, dinero_jugador, inv

    print("=" * 60)
    print("🗡️  BIENVENIDO AL RPG MEJORADO - VERSIÓN CORREGIDA  🗡️")
    print("=" * 60)
    arma_equipada = []
    armadura_equipada = []
    inicializar_estados_equipamiento()
    while True:
        print("\n🎮 MENÚ PRINCIPAL")
        print("1. 🆕 Nueva partida")
        print("2. 📂 Cargar partida")
        print("3. 🗑️ Eliminar partida")
        print("4. 🚪 Salir del juego")

        inicio = validar_entrada_numerica("\nElige una opción (1-4): ", 1, 4)

        if inicio == 4:
            print("¡Hasta la próxima aventura!")
            return
        elif inicio == 2:
            if cargar_partida():
                print("\n🎯 Continuando aventura...")
                eleccion_de_camino_def()
                return
        elif inicio == 3:
            eliminar_partida()
            continue
        elif inicio == 1:
            break

    # Comenzar nueva partida
    print("\n🆕 Comenzando una nueva aventura...")
    nombre = input("¿Cuál es tu nombre, valiente aventurero? ").strip().capitalize()
    if not nombre:
        nombre = "Aventurero"

    print(f"\nBienvenido {nombre}! Eres un aventurero en un mundo lleno de peligrosos monstruos y tesoros legendarios.")
    print("Tu misión es sobrevivir en la misteriosa cueva y encontrar los tesoros más poderosos.")
    print("✨ Sistema mejorado con combate avanzado, hechizos, conjuntos de equipamiento y guardado múltiple.")

    print("\nElige tu clase:")
    print("1. Guerrero - Fuerte y resistente (Alta vida y ataque)")
    print("2. Mago - Poderoso en magia (Alta inteligencia y maná)")
    print("3. Arquero - Ágil y preciso (Alta destreza y velocidad)")
    print("4. Asesino - Rápido y letal (Alta velocidad y críticos)")

    seleccion_de_clase = validar_entrada_numerica("Elige tu clase (1-4): ", 1, 4)

    if seleccion_de_clase == 1:
        print("\n⚔️ Has elegido la clase GUERRERO ⚔️")
        print("Eres fuerte y valiente, resistente en combate pero no muy ágil.")
        max_vida = 115
        vida = max_vida
        ataque = 40
        defensa = 30
        velocidad = 15
        esquive = 5
        inteligencia = 5
        destreza = 30
        suerte = 1
        max_mana = 15
        mana = max_mana
        print("Empiezas con una espada de madera")
        inv.append("espada de madera")

    elif seleccion_de_clase == 2:
        print("\n🔮 Has elegido la clase MAGO 🔮")
        print("Eres inteligente y poderoso en magia, pero físicamente frágil.")
        max_vida = 75
        vida = max_vida
        ataque = 20
        defensa = 15
        velocidad = 15
        esquive = 5
        inteligencia = 45
        destreza = 20
        suerte = 1
        max_mana = 100
        mana = max_mana
        print("Empiezas con un báculo de madera")
        print("¡Puedes lanzar hechizos poderosos usando tu maná!")
        inv.append("baculo de madera")

    elif seleccion_de_clase == 3:
        print("\n🏹 Has elegido la clase ARQUERO 🏹")
        print("Eres ágil y preciso, excelente a distancia pero no muy resistente.")
        max_vida = 85
        vida = max_vida
        ataque = 35
        defensa = 20
        velocidad = 30
        esquive = 20
        inteligencia = 15
        destreza = 40
        suerte = 1
        max_mana = 30
        mana = max_mana
        print("Empiezas con un arco de madera")
        inv.append("arco de madera")

    elif seleccion_de_clase == 4:
        print("\n🗡️ Has elegido la clase ASESINO 🗡️")
        print("Eres sigiloso y letal, rápido y con alta probabilidad de críticos.")
        max_vida = 70
        vida = max_vida
        ataque = 40
        defensa = 15
        velocidad = 30
        esquive = 10
        inteligencia = 20
        destreza = 20
        suerte = 1
        max_mana = 15
        mana = max_mana
        print("Empiezas con unas dagas de madera")
        inv.append("dagas de madera")

    print(f"\n=== TUS ESTADÍSTICAS INICIALES ===")
    print(f"Vida: {vida}/{max_vida}")
    print(f"Maná: {mana}/{max_mana}")
    print(f"Ataque: {ataque}")
    print(f"Defensa: {defensa}")
    print(f"Velocidad: {velocidad}")
    print(f"Destreza: {destreza} (Crítico: {calcular_probabilidad_critico()}%)")
    print(f"Esquive: {esquive}")
    print(f"Inteligencia: {inteligencia}")
    print(f"Suerte: {suerte}")
    print(f"Dinero inicial: {dinero_jugador}")

    print(f"\n🏰 Historia: {nombre} es un aventurero valiente que viajaba por un bosque oscuro")
    print("buscando oportunidades para cazar monstruos y conseguir riquezas para su familia.")
    print("De repente, encuentras una cueva misteriosa. A pesar del mal presentimiento,")
    print("decides entrar pensando en tus seres queridos y en darles una vida mejor.")

    print("\n🕯️ Al entrar en la cueva oscura, prendes una antorcha para ver mejor.")
    print("Después de caminar un rato, el camino se divide en 3 direcciones...")

    guardar = input("\n¿Quieres guardar tu progreso antes de comenzar? (si/no): ").lower()
    if guardar == "si":
        guardar_partida()

    eleccion_de_camino_def()


# =============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Juego interrumpido por el usuario!")
        print("¡Gracias por jugar!")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        print("Por favor, reporta este error si persiste.")


