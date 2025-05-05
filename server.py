# Modificar esto en la parte superior de server.py, donde se configura CORS
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
# Intentar importar flask_compress, pero no fallar si no está disponible
try:
    from flask_compress import Compress
    COMPRESS_AVAILABLE = True
except ImportError:
    COMPRESS_AVAILABLE = False
    print("ADVERTENCIA: flask_compress no está instalado. La compresión está desactivada.")

app = Flask(__name__)
# Configurar CORS para permitir todas las solicitudes desde cualquier origen
# Esto es útil para desarrollo, pero considera restringirlo en producción
CORS(app, resources={r"/*": {"origins": "*"}})

# Alternativamente, para ser más específico:
# CORS(app, resources={r"/*": {"origins": ["https://zodiaco-02nu.onrender.com", "http://localhost:*"]}})
from datetime import datetime, timezone, timedelta
import sys
import os
import requests
import math
import csv
from pathlib import Path
from functools import lru_cache

try:
    from skyfield.api import load, wgs84
    import numpy as np
    SKYFIELD_AVAILABLE = True
    print("Skyfield disponible para cálculos astronómicos precisos")
except ImportError:
    SKYFIELD_AVAILABLE = False
    print("ADVERTENCIA: Skyfield no está instalado. Se usarán cálculos aproximados.")

app = Flask(__name__)
# Configurar CORS
CORS(app)

# Variables globales para recursos precargados
eph = None
ts = None
time_zone_df = None

# API Key para geocodificación
API_KEY = "e19afa2a9d6643ea9550aab89eefce0b"  # Para demo, en producción usar variables de entorno

# Constantes para cálculos astrológicos
PLANET_DATA = {
    'SOL': {'numero': 1},
    'LUNA': {'numero': 6},
    'MERCURIO': {'numero': 4},
    'VENUS': {'numero': 3},
    'MARTE': {'numero': 5},
    'JÚPITER': {'numero': 2},
    'SATURNO': {'numero': 7}
}

PLANET_ORDER = {
    'seco': ['SOL', 'MARTE', 'JÚPITER', 'SATURNO', 'LUNA', 'MERCURIO', 'VENUS'],
    'humedo': ['LUNA', 'MERCURIO', 'VENUS', 'SOL', 'MARTE', 'JÚPITER', 'SATURNO']
}

FAGAN_ALLEN_AYANAMSA = 24.25  # Valor exacto del Ayanamsa Fagan-Allen en 2025 (24° 15')

# Clasificación de planetas por secta - Actualizada para considerar a Mercurio como maléfico
PLANETA_SECTA = {
    'seco': {  # Carta diurna
        'benefico_secta': 'JÚPITER',     # Benéfico de secta a favor (diurno)
        'malefico_contrario': 'MARTE',   # Maléfico contrario a secta (diurno)
        'benefico_contrario': 'VENUS',   # Benéfico contrario a secta (diurno)
        'malefico_mercurio': 'MERCURIO'  # Mercurio como maléfico (diurno)
    },
    'humedo': {  # Carta nocturna
        'benefico_secta': 'VENUS',       # Benéfico de secta a favor (nocturno)
        'malefico_contrario': 'MARTE',   # Maléfico contrario a secta (nocturno)
        'benefico_contrario': 'JÚPITER', # Benéfico contrario a secta (nocturno)
        'malefico_mercurio': 'MERCURIO'  # Mercurio como maléfico (nocturno)
    }
}

DURACION_POR_NIVEL = {
    'virgo': 4, 'libra': 3, 'escorpio': 5, 'ofiuco': 7, 'sagitario': 2,
    'capricornio': 1, 'acuario': 6, 'piscis': 2, 'aries': 5, 'tauro': 3,
    'geminis': 4, 'cancer': 6, 'leo': 1
}

SIGNOS = {
    'virgo': {'planeta': 'MERCURIO', 'años': 4},
    'libra': {'planeta': 'VENUS', 'años': 3},
    'escorpio': {'planeta': 'MARTE', 'años': 5},
    'ofiuco': {'planeta': 'SATURNO', 'años': 7},
    'sagitario': {'planeta': 'JÚPITER', 'años': 2},
    'capricornio': {'planeta': 'SOL', 'años': 1},
    'acuario': {'planeta': 'LUNA', 'años': 6},
    'piscis': {'planeta': 'JÚPITER', 'años': 2},
    'aries': {'planeta': 'MARTE', 'años': 5},
    'tauro': {'planeta': 'VENUS', 'años': 3},
    'geminis': {'planeta': 'MERCURIO', 'años': 4},
    'cancer': {'planeta': 'LUNA', 'años': 6},
    'leo': {'planeta': 'SOL', 'años': 1}
}

DURACIONES = {
    'AÑO': 364,
    'MES': 28,
    'SEMANA': 7,
    'DIA': 1
}

DIMENSIONS = {
    'centerX': 300,
    'centerY': 300,
    'radius': 280,  # Aumentado para maximizar el tamaño de la rueda
    'middleRadius': 190,  # Radio para la carta externa
    'innerRadius': 110,  # Radio para la carta interna
    'glyphRadius': 265
}

SIGNS = [
    {'name': 'ARIES', 'start': 354, 'length': 36, 'symbol': '♈', 'color': '#FFE5E5'},
    {'name': 'TAURUS', 'start': 30, 'length': 30, 'symbol': '♉', 'color': '#E5FFE5'},
    {'name': 'GEMINI', 'start': 60, 'length': 30, 'symbol': '♊', 'color': '#FFFFE5'},
    {'name': 'CANCER', 'start': 90, 'length': 30, 'symbol': '♋', 'color': '#E5FFFF'},
    {'name': 'LEO', 'start': 120, 'length': 30, 'symbol': '♌', 'color': '#FFE5E5'},
    {'name': 'VIRGO', 'start': 150, 'length': 36, 'symbol': '♍', 'color': '#E5FFE5'},
    {'name': 'LIBRA', 'start': 186, 'length': 24, 'symbol': '♎', 'color': '#FFFFE5'},
    {'name': 'SCORPIO', 'start': 210, 'length': 30, 'symbol': '♏', 'color': '#E5FFFF'},
    {'name': 'OPHIUCHUS', 'start': 240, 'length': 12, 'symbol': '⛎', 'color': '#FFFFE5'},
    {'name': 'SAGITTARIUS', 'start': 252, 'length': 18, 'symbol': '♐', 'color': '#FFE5E5'},
    {'name': 'CAPRICORN', 'start': 270, 'length': 36, 'symbol': '♑', 'color': '#E5FFE5'},
    {'name': 'AQUARIUS', 'start': 306, 'length': 18, 'symbol': '♒', 'color': '#FFFFE5'},
    {'name': 'PEGASUS', 'start': 324, 'length': 6, 'symbol': '∩', 'color': '#E5FFFF'},
    {'name': 'PISCES', 'start': 330, 'length': 24, 'symbol': '♓', 'color': '#E5FFFF'}
]

ASPECTS = {
    'CONJUNCTION': {'angle': 0, 'orb': 2, 'color': '#000080', 'name': 'Armónico Relevante'},
    'SEXTILE': {'angle': 60, 'orb': 2, 'color': '#000080', 'name': 'Armónico Relevante'},
    'SQUARE': {'angle': 90, 'orb': 2, 'color': '#FF0000', 'name': 'Inarmónico Relevante'},
    'TRINE': {'angle': 120, 'orb': 2, 'color': '#000080', 'name': 'Armónico Relevante'},
    'OPPOSITION': {'angle': 180, 'orb': 2, 'color': '#000080', 'name': 'Armónico Relevante'}
}

COLORS = {
    'RED': '#FF0000',
    'GREEN': '#00FF00',
    'BLUE': '#0000FF',
    'YELLOW': '#FFFF00'
}

# Nuevas constantes para dignidades planetarias según izarren.top
DIGNIDADES = {
    'SOL': {
        'domicilio': ['ESCORPIO', 'GÉMINIS', 'PEGASO'], 
        'exaltacion': ['LEO', 'ARIES', 'CAPRICORNIO', 'VIRGO'], 
        'caida': ['CÁNCER', 'PISCIS', 'LIBRA', 'ACUARIO', 'OFIUCO'], 
        'exilio': ['TAURO', 'SAGITARIO']  # TAURO está en exilio para el SOL
    },
    'LUNA': {
        'domicilio': ['TAURO', 'SAGITARIO'], 
        'exaltacion': ['CÁNCER', 'PISCIS', 'LIBRA', 'ACUARIO', 'OFIUCO'], 
        'caida': ['LEO', 'ARIES', 'CAPRICORNIO', 'VIRGO'], 
        'exilio': ['ESCORPIO', 'GÉMINIS', 'PEGASO']
    },
    'MERCURIO': {
        'domicilio': ['LEO', 'ARIES', 'ESCORPIO', 'PEGASO'], 
        'exaltacion': ['GÉMINIS', 'CAPRICORNIO', 'VIRGO'], 
        'caida': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO'], 
        'exilio': ['CÁNCER', 'PISCIS', 'SAGITARIO']
    },
    'VENUS': {
        'domicilio': ['CÁNCER', 'PISCIS', 'SAGITARIO'], 
        'exaltacion': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO'], 
        'caida': ['GÉMINIS', 'CAPRICORNIO', 'VIRGO'], 
        'exilio': ['LEO', 'ARIES', 'ESCORPIO', 'PEGASO']
    },
    'MARTE': {
        'domicilio': ['GÉMINIS', 'CAPRICORNIO', 'VIRGO'], 
        'exaltacion': ['LEO', 'ARIES', 'ESCORPIO', 'PEGASO'], 
        'caida': ['CÁNCER', 'PISCIS', 'SAGITARIO'], 
        'exilio': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO']
    },
    'JÚPITER': {  # Con acento
        'domicilio': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO'], 
        'exaltacion': ['CÁNCER', 'PISCIS', 'SAGITARIO'], 
        'caida': ['LEO', 'ARIES', 'ESCORPIO', 'PEGASO'], 
        'exilio': ['GÉMINIS', 'CAPRICORNIO', 'VIRGO']
    },
    'SATURNO': {
        'domicilio': ['LEO', 'ARIES', 'LIBRA', 'ACUARIO'], 
        'exaltacion': ['OFIUCO', 'GÉMINIS'], 
        'caida': ['TAURO', 'ESCORPIO', 'PEGASO'], 
        'exilio': ['CÁNCER', 'PISCIS', 'CAPRICORNIO', 'VIRGO']
    },
    'URANO': {
        'domicilio': ['LEO', 'ARIES', 'ESCORPIO', 'PEGASO'], 
        'exaltacion': ['GÉMINIS', 'CAPRICORNIO', 'VIRGO'], 
        'caida': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO'],  # TAURO está en caída para URANO
        'exilio': ['CÁNCER', 'PISCIS', 'SAGITARIO']
    },
    'NEPTUNO': {
        'domicilio': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO'], 
        'exaltacion': ['CÁNCER', 'PISCIS', 'SAGITARIO'], 
        'caida': ['LEO', 'ARIES', 'ESCORPIO', 'PEGASO'], 
        'exilio': ['GÉMINIS', 'CAPRICORNIO', 'VIRGO']
    },
    'PLUTÓN': {  # Con acento
        'domicilio': ['GÉMINIS', 'CAPRICORNIO', 'VIRGO'], 
        'exaltacion': ['LEO', 'ARIES', 'ESCORPIO', 'PEGASO'], 
        'caida': ['CÁNCER', 'PISCIS', 'SAGITARIO'], 
        'exilio': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO']
    }
}

# Datos para cálculo de picos y presagios - Actualizados para considerar a Mercurio como maléfico
PICO_CONDICIONES = {
    'MAYOR': {
        'dignidad': ['domicilio', 'exaltacion'],
        'aspectos_requeridos': ['CONJUNCTION'],
        'planetas_requeridos': ['JÚPITER', 'VENUS', 'LUNA'],  # Planetas benéficos
        'planetas_maleficos': ['MARTE', 'MERCURIO'],  # Planetas maléficos
        'min_fuerza': 8
    },
    'MODERADO': {
        'dignidad': ['domicilio', 'exaltacion', 'peregrino'],
        'aspectos_requeridos': ['TRINE'],
        'planetas_requeridos': ['JÚPITER', 'VENUS', 'LUNA'],
        'planetas_maleficos': ['MARTE', 'MERCURIO'],
        'min_fuerza': 5
    },
    'MENOR': {
        'dignidad': ['domicilio', 'exaltacion', 'peregrino'],
        'aspectos_requeridos': ['SEXTILE'],
        'planetas_requeridos': ['JÚPITER', 'VENUS', 'LUNA'],
        'planetas_maleficos': ['MARTE', 'MERCURIO'],
        'min_fuerza': 3
    }
}

# Datos para liberación de enlace y presagios - Actualizados para incluir a Mercurio como maléfico
LIBERACION_ENLACE = {
    'SOL': {'libera': ['MARTE', 'MERCURIO'], 'condicion': 'CONJUNCTION'},
    'LUNA': {'libera': ['VENUS', 'JÚPITER'], 'condicion': 'CONJUNCTION'},
    'MERCURIO': {'libera': ['SOL', 'MARTE'], 'condicion': 'CONJUNCTION'},
    'VENUS': {'libera': ['LUNA', 'JÚPITER'], 'condicion': 'CONJUNCTION'}
}

PRESAGIO_CONDICIONES = {
    'BUENO': {
        'planetas': ['JÚPITER', 'VENUS', 'LUNA'],
        'aspectos': ['CONJUNCTION', 'TRINE', 'SEXTILE'],
        'signos_favorables': {
            'JÚPITER': ['SAGITTARIUS', 'PISCES', 'CANCER'],
            'VENUS': ['TAURUS', 'LIBRA', 'PISCES'],
            'SOL': ['LEO', 'ARIES']
        }
    },
    'MALO': {
        'planetas': ['MARTE', 'MERCURIO'],  # Actualizado para incluir a Mercurio como maléfico
        'aspectos': ['SQUARE', 'OPPOSITION', 'QUINCUNX'],
        'signos_desfavorables': {
            'MARTE': ['TAURUS', 'LIBRA', 'AQUARIUS', 'OPHIUCHUS'],
            'MERCURIO': ['CANCER', 'PISCES', 'SAGITTARIUS']  # Añadidos signos desfavorables para Mercurio
        }
    }
}

# Datos para cálculo de enlace y disolución de enlace
ENLACE_PLANETARIO = {
    'SOL': {'fortaleza': 10, 'neutraliza': ['MARTE', 'MERCURIO'], 'debilita': ['LUNA']},  # Actualizado
    'LUNA': {'fortaleza': 8, 'neutraliza': ['VENUS', 'JÚPITER'], 'debilita': ['SOL']},
    'MERCURIO': {'fortaleza': 7, 'neutraliza': ['VENUS'], 'debilita': ['JÚPITER']},
    'VENUS': {'fortaleza': 6, 'neutraliza': ['MERCURIO'], 'debilita': ['MARTE']},
    'MARTE': {'fortaleza': 9, 'neutraliza': ['LUNA'], 'debilita': ['VENUS', 'JÚPITER']},
    'JÚPITER': {'fortaleza': 5, 'neutraliza': ['SOL'], 'debilita': ['MARTE', 'MERCURIO']},
    'SATURNO': {'fortaleza': 4, 'neutraliza': [], 'debilita': []}  # Actualizado
}

# Puntos de referencia para cálculos astrológicos
PUNTOS_REFERENCIA = {
    'ASCENDENTE': {
        'factor_mes': 2,
        'factor_dia': 3,
        'fuerza_modificador': 2,
        'descripcion': 'Punto de la carta que representa el inicio de la primera casa.'
    },
    'PARTE_FORTUNA': {
        'factor_mes': 3,
        'factor_dia': 5,
        'fuerza_modificador': 1,
        'descripcion': 'Punto calculado en base a las posiciones del Sol, la Luna y el Ascendente.'
    },
    'PARTE_ESPIRITU': {
        'factor_mes': 5,
        'factor_dia': 7,
        'fuerza_modificador': 0,
        'descripcion': 'Punto inverso a la Parte de Fortuna, representa la conciencia y el espíritu.'
    }
}

# Función auxiliar para calcular correctamente la distancia en el zodíaco
def distancia_zodiaco(punto_inicio, punto_fin):
    """
    Calcula la distancia entre dos puntos en el zodíaco, siguiendo el sentido natural
    del zodíaco (sentido antihorario).
    """
    return (punto_fin - punto_inicio + 360) % 360

# Precarga de recursos
def preload_resources():
    global eph, ts, time_zone_df
    
    print("Precargando recursos...")
    
    # Cargar efemérides desde GitHub
    try:
        # Cargar desde archivo local
        eph_path = Path('de421.bsp')
        if not eph_path.exists():
            # Intentar cargar desde la carpeta docs
            eph_path = Path('docs') / 'de421.bsp'
        
        print(f"Cargando efemérides desde: {eph_path}")
        eph = load(str(eph_path))
    except Exception as e:
        print(f"Error cargando efemérides: {e}")
        # Intento alternativo
        try:
            print("Intentando cargar efemérides alternativas...")
            eph = load('de440s.bsp')
        except Exception as e2:
            print(f"Error en carga alternativa: {e2}")
            sys.exit(1)  # Salir si no se pueden cargar las efemérides
    
    ts = load.timescale()
    
    # Cargar zona horaria desde CSV
    try:
        time_zone_df = []
        with open('time_zone.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if len(row) >= 6:  # asegurarse de que hay suficientes columnas
                    time_zone_df.append({
                        'timezone': row[0],
                        'country_code': row[1],
                        'abbreviation': row[2],
                        'timestamp': int(row[3]) if row[3].isdigit() else 0,
                        'utc_offset': float(row[4]) if row[4].replace('.', '', 1).isdigit() else 0,
                        'dst': int(row[5]) if row[5].isdigit() else 0
                    })
        print(f"Cargado archivo de zonas horarias: {len(time_zone_df)} entradas")
    except Exception as e:
        print(f"Error cargando zonas horarias: {e}")
        time_zone_df = []
    
    print("Recursos precargados correctamente")

# Cachear obtención de datos de ciudad
@lru_cache(maxsize=100)
def obtener_datos_ciudad(ciudad, fecha=None, hora=None):
    url = f"https://api.geoapify.com/v1/geocode/search?text={ciudad}&apiKey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)  # Timeout para evitar demoras
        if response.status_code == 200:
            datos = response.json()
            if datos.get("features"):
                opciones = [{
                    "nombre": resultado["properties"]["formatted"],
                    "lat": resultado["properties"]["lat"],
                    "lon": resultado["properties"]["lon"],
                    "pais": resultado["properties"].get("country", "")
                }
                for resultado in datos["features"]]
                return opciones
            return {"error": "Ciudad no encontrada"}
        return {"error": f"Error en la consulta: {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "Timeout en la consulta"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

def obtener_zona_horaria(coordenadas, fecha):
    """
    Obtiene la zona horaria usando el archivo time_zone.csv y ajusta para horario de verano/invierno
    basado en las coordenadas y la fecha, considerando hemisferio norte/sur
    """
    try:
        lat = coordenadas["lat"]
        lon = coordenadas["lon"]
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        
        # Determinar hemisferio (norte o sur)
        hemisferio = "norte" if lat >= 0 else "sur"
        
        # Verificar si la fecha está en horario de verano
        # Esta función necesita ser más precisa para fechas históricas
        is_dst = determinar_horario_verano(fecha_obj, hemisferio, coordenadas)
        
        # Buscar en el CSV por aproximación de longitud
        estimated_offset = round(lon / 15)
        
        # Ajustar para países específicos con información conocida
        pais = coordenadas.get("pais", "").lower()
        abbr = "UTC"
        tz_name = "UTC"
        offset = estimated_offset  # valor por defecto
        
        if "spain" in pais or "españa" in pais:
            tz_name = "Europe/Madrid"
            abbr = "CET"
            abbr_dst = "CEST"
            offset = 1
            if is_dst:
                offset = 2
                abbr = abbr_dst
        elif "argentina" in pais:
            tz_name = "America/Argentina/Buenos_Aires"
            abbr = "ART"
            offset = -3
            # Argentina no usa DST actualmente
        elif "mexico" in pais or "méxico" in pais:
            tz_name = "America/Mexico_City"
            abbr = "CST"
            abbr_dst = "CDT"
            offset = -6
            if is_dst:
                offset = -5
                abbr = abbr_dst
        else:
            # Buscar en el CSV la zona más cercana a la longitud estimada
            closest_zone = None
            min_diff = float('inf')
            
            if time_zone_df:
                for zone in time_zone_df:
                    # Los offsets en el CSV están en segundos, convertir a horas
                    csv_offset = zone['utc_offset'] / 3600
                    diff = abs(csv_offset - estimated_offset)
                    
                    if diff < min_diff:
                        min_diff = diff
                        closest_zone = zone
                
                if closest_zone:
                    offset = closest_zone['utc_offset'] / 3600
                    abbr = closest_zone['abbreviation']
                    tz_name = closest_zone['timezone']
                    
                    # Ajustar por DST si corresponde
                    if is_dst and closest_zone['dst'] == 1:
                        offset += 1
            else:
                # Si no hay datos en el CSV, usar la estimación por longitud
                offset = estimated_offset
                abbr = f"GMT{offset:+d}"
                tz_name = f"Estimated/GMT{offset:+d}"
        
        print(f"Zona horaria determinada: {tz_name}, offset: {offset}, DST: {is_dst}")
        
        return {
            "name": tz_name,
            "offset": offset,
            "abbreviation_STD": abbr,
            "abbreviation_DST": abbr,
            "is_dst": is_dst,
            "hemisphere": hemisferio
        }
    
    except Exception as e:
        print(f"Error obteniendo zona horaria: {str(e)}")
        # Si hay un error, devolver un mensaje claro
        print("Error en obtención de zona horaria, usando estimación basada en longitud")
        
        try:
            # Estimar zona horaria basada en longitud
            lon = coordenadas["lon"]
            estimated_offset = round(lon / 15)  # 15 grados = 1 hora
            
            # Para ciudades conocidas, usar valores predeterminados
            pais = coordenadas.get("pais", "").lower()
            
            if "spain" in pais or "españa" in pais:
                estimated_offset = 1
            elif "argentina" in pais:
                estimated_offset = -3
            elif "mexico" in pais or "méxico" in pais:
                estimated_offset = -6
            elif "united states" in pais or "estados unidos" in pais:
                # Aproximación basada en longitud para EEUU
                if lon < -100:
                    estimated_offset = -8  # Pacífico
                elif lon < -90:
                    estimated_offset = -7  # Montaña
                elif lon < -75:
                    estimated_offset = -6  # Central
                else:
                    estimated_offset = -5  # Este
            
            return {
                "name": f"GMT{estimated_offset:+d}",
                "offset": estimated_offset,
                "abbreviation_STD": f"GMT{estimated_offset:+d}",
                "abbreviation_DST": f"GMT{estimated_offset:+d}",
                "is_dst": False,
                "hemisphere": "norte" if coordenadas["lat"] >= 0 else "sur",
                "lon": lon  # Añadir longitud para referencia
            }
        except Exception as inner_e:
            print(f"Error en estimación de zona horaria: {str(inner_e)}")
            # Valor por defecto UTC si todo falla
            return {
                "name": "UTC",
                "offset": 0,
                "abbreviation_STD": "UTC",
                "abbreviation_DST": "UTC",
                "is_dst": False,
                "hemisphere": "norte",
                "estimated": True
            }

def determinar_horario_verano(fecha, hemisferio, coordenadas):
    """
    Determina si una fecha está en horario de verano (DST)
    Basado en reglas históricas y específicas por país
    """
    año = fecha.year
    mes = fecha.month
    dia = fecha.day
    
    # Obtener país
    pais = coordenadas.get("pais", "").lower()
    
    # Reglas específicas para España
    if "spain" in pais or "españa" in pais:
        # España antes de 1974: no había DST
        if año < 1974:
            return False
        elif año >= 1974 and año <= 1975:
            # En 1974-1975, DST fue del 13 de abril al 6 de octubre
            if (mes > 4 and mes < 10) or (mes == 4 and dia >= 13) or (mes == 10 and dia <= 6):
                return True
            return False
        elif año >= 1976 and año <= 1996:
            # Reglas más genéricas para 1976-1996
            # Primavera a otoño, aproximadamente marzo/abril a septiembre/octubre
            if mes > 3 and mes < 10:
                return True
            return False
        else:
            # Desde 1997: Regla actual de la UE - último domingo de marzo a último domingo de octubre
            if mes > 3 and mes < 10:
                return True
            # Marzo: último domingo
            elif mes == 3 and dia >= 25:  # Aproximación al último domingo
                return True
            # Octubre: último domingo
            elif mes == 10 and dia <= 25:  # Aproximación al último domingo
                return True
            return False
    
    # Reglas para otros países
    # Hemisferio Norte (Europa, América del Norte, Asia)
    elif hemisferio == "norte":
        # La mayoría de los países del hemisferio norte siguen este patrón
        # Horario de verano: finales de marzo a finales de octubre
        if año < 1970:
            # Antes de 1970 era menos común el DST
            return False
        
        if mes > 3 and mes < 10:
            return True
        elif mes == 3 and dia >= 25:  # Aproximación al último domingo de marzo
            return True
        elif mes == 10 and dia <= 25:  # Aproximación al último domingo de octubre
            return True
        return False
    
    # Hemisferio Sur (Australia, Nueva Zelanda, Sudamérica)
    else:
        # Muchos países del hemisferio sur no utilizan DST
        # Algunos que sí lo utilizan: Australia, Nueva Zelanda, Chile, Paraguay
        
        # Lista de países conocidos del hemisferio sur con DST
        south_dst_countries = ["australia", "new zealand", "nueva zelanda", "chile", "paraguay"]
        
        # Si no está en la lista, asumimos que no usa DST
        pais_usa_dst = any(country in pais for country in south_dst_countries)
        if not pais_usa_dst:
            return False
            
        # Horario de verano: finales de octubre a finales de marzo
        if mes < 3 or mes > 10:
            return True
        elif mes == 3 and dia <= 25:  # Aproximación al último domingo de marzo
            return True
        elif mes == 10 and dia >= 25:  # Aproximación al último domingo de octubre
            return True
        return False

def convertir_a_utc(fecha, hora, timezone_info):
    """
    Convierte fecha y hora local a UTC considerando zona horaria y DST
    Para cálculos astrológicos correctos, debemos asegurarnos de que la hora UTC sea precisa
    """
    try:
        # Combinar fecha y hora en un objeto datetime
        fecha_hora_str = f"{fecha} {hora}"
        dt_local = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
        
        # Obtener offset en horas desde la API de zona horaria
        # Si estamos en DST, la API ya incluye ese offset
        offset_hours = timezone_info["offset"]
        
        print(f"Offset de zona horaria: {offset_hours} horas")
        print(f"Hora local ingresada: {dt_local}")
        
        # Crear un timezone con el offset
        tz = timezone(timedelta(hours=offset_hours))
        
        # Aplicar timezone al datetime
        dt_local_with_tz = dt_local.replace(tzinfo=tz)
        
        # Convertir a UTC
        dt_utc = dt_local_with_tz.astimezone(timezone.utc)
        
        print(f"Hora convertida a UTC: {dt_utc}")
        return dt_utc
    except Exception as e:
        print(f"Error en conversión a UTC: {str(e)}")
        # Si falla, usar la hora proporcionada con offset manual aproximado
        dt_local = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        
        # Intentar estimar offset basado en longitud si no tenemos zona horaria
        if "lon" in timezone_info:
            lon = timezone_info["lon"]
            est_offset = round(lon / 15)  # 15 grados = 1 hora
            est_tz = timezone(timedelta(hours=est_offset))
            dt_with_tz = dt_local.replace(tzinfo=est_tz)
            return dt_with_tz.astimezone(timezone.utc)
        
        # Fallback: asumir UTC
        return dt_local.replace(tzinfo=timezone.utc)

def calculate_positions_with_skyfield(utc_datetime, lat=None, lon=None):
    """Calculates planetary positions using Skyfield for greater precision, including retrograde status"""
    try:
        if not SKYFIELD_AVAILABLE:
            raise Exception("Skyfield is not available")
        
        print(f"Calculating positions for UTC: {utc_datetime}")
        t = ts.from_datetime(utc_datetime)
        
        # Calculate positions for a day before and after to determine motion direction
        t_before = ts.from_datetime(utc_datetime - timedelta(days=1))
        t_after = ts.from_datetime(utc_datetime + timedelta(days=1))
        
        earth = eph['earth']
        
        positions = []
        bodies = {
            'SOL': eph['sun'],
            'LUNA': eph['moon'],
            'MERCURIO': eph['mercury'],
            'VENUS': eph['venus'],
            'MARTE': eph['mars'],
            'JÚPITER': eph['jupiter barycenter'],
            'SATURNO': eph['saturn barycenter'],
            'URANO': eph['uranus barycenter'],
            'NEPTUNO': eph['neptune barycenter'],
            'PLUTÓN': eph['pluto barycenter']
        }
        
        for body_name, body in bodies.items():
            # Calculate current position
            pos = earth.at(t).observe(body).apparent()
            lat_ecl, lon_ecl, dist = pos.ecliptic_latlon(epoch='date')
            longitude = float(lon_ecl.degrees) % 360
            
            # Calculate position one day before
            pos_before = earth.at(t_before).observe(body).apparent()
            lat_before, lon_before, dist_before = pos_before.ecliptic_latlon(epoch='date')
            longitude_before = float(lon_before.degrees) % 360
            
            # Calculate position one day after
            pos_after = earth.at(t_after).observe(body).apparent()
            lat_after, lon_after, dist_after = pos_after.ecliptic_latlon(epoch='date')
            longitude_after = float(lon_after.degrees) % 360
            
            # Calculate daily motion rates, handling the 0/360 degree boundary
            daily_motion_before = (longitude - longitude_before) % 360
            if daily_motion_before > 180:
                daily_motion_before = daily_motion_before - 360
                
            daily_motion_after = (longitude_after - longitude) % 360
            if daily_motion_after > 180:
                daily_motion_after = daily_motion_after - 360
            
            # Determine retrograde status
            motion_status = "direct"  # Default: direct motion
            
            # The Sun and Moon are never retrograde from Earth's perspective
            if body_name not in ['SOL', 'LUNA']:
                # Check for retrograde motion (negative daily motion)
                if daily_motion_before < 0 and daily_motion_after < 0:
                    motion_status = "retrograde"
                # Check for stationary retrograde (changing from direct to retrograde)
                elif daily_motion_before >= 0 and daily_motion_after < 0:
                    motion_status = "stationary_retrograde"
                # Check for stationary direct (changing from retrograde to direct)
                elif daily_motion_before < 0 and daily_motion_after >= 0:
                    motion_status = "stationary_direct"
                
                # Check for very slow motion (almost stationary)
                if abs(daily_motion_before) < 0.1 or abs(daily_motion_after) < 0.1:
                    if motion_status == "retrograde":
                        motion_status = "stationary_retrograde"
                    elif motion_status == "direct":
                        motion_status = "stationary_direct"
            
            # Calculate dignity based on position
            dignidad = calcular_dignidad_planetaria(body_name, longitude)
            
            positions.append({
                "name": body_name,
                "longitude": longitude,
                "sign": get_sign(longitude),
                "dignidad": dignidad,
                "motion_status": motion_status,
                "daily_motion": (daily_motion_before + daily_motion_after) / 2  # Average daily motion
            })
        
        if lat is not None and lon is not None:
            asc, mc = calculate_asc_mc(t, lat, lon)
            
            positions.append({
                "name": "ASC",
                "longitude": float(asc),
                "sign": get_sign(asc),
                "motion_status": "direct"  # ASC is always direct
            })
            
            positions.append({
                "name": "MC",
                "longitude": float(mc),
                "sign": get_sign(mc),
                "motion_status": "direct"  # MC is always direct
            })
            
            # Add descendant (opposite to ascendant)
            desc = (asc + 180) % 360
            positions.append({
                "name": "DSC",
                "longitude": float(desc),
                "sign": get_sign(desc),
                "motion_status": "direct"  # DSC is always direct
            })
            
            # Add Imum Coeli (IC) (opposite to MC)
            ic = (mc + 180) % 360
            positions.append({
                "name": "IC",
                "longitude": float(ic),
                "sign": get_sign(ic),
                "motion_status": "direct"  # IC is always direct
            })
            
            # Calculate and add Part of Fortune and Part of Spirit
            sol_planet = next((p for p in positions if p["name"] == "SOL"), None)
            luna_planet = next((p for p in positions if p["name"] == "LUNA"), None)
            
            if sol_planet and luna_planet:
                # Determine if it's a dry or humid birth
                is_dry = is_dry_birth(sol_planet["longitude"], asc)
                
                # Correct calculation of Part of Fortune based on chart nature
                if is_dry:  # Dry chart (diurnal)
                    # For diurnal charts: Part of Fortune = ASC + dist(Sun→Moon)
                    dist_sol_a_luna = distancia_zodiaco(sol_planet["longitude"], luna_planet["longitude"])
                    parte_fortuna = (asc + dist_sol_a_luna) % 360
                else:  # Humid chart (nocturnal)
                    # For nocturnal charts: Part of Fortune = ASC + dist(Moon→Sun)
                    dist_luna_a_sol = distancia_zodiaco(luna_planet["longitude"], sol_planet["longitude"])
                    parte_fortuna = (asc + dist_luna_a_sol) % 360
                
                # Correct calculation of Part of Spirit (logical inverse of Part of Fortune)
                if is_dry:  # Dry chart (diurnal)
                    # For diurnal charts: Part of Spirit = ASC + dist(Moon→Sun)
                    dist_luna_a_sol = distancia_zodiaco(luna_planet["longitude"], sol_planet["longitude"])
                    parte_espiritu = (asc + dist_luna_a_sol) % 360
                else:  # Humid chart (nocturnal)
                    # For nocturnal charts: Part of Spirit = ASC + dist(Sun→Moon)
                    dist_sol_a_luna = distancia_zodiaco(sol_planet["longitude"], luna_planet["longitude"])
                    parte_espiritu = (asc + dist_sol_a_luna) % 360
                
                # Add to positions
                positions.append({
                    "name": "PARTE_FORTUNA",
                    "longitude": float(parte_fortuna),
                    "sign": get_sign(parte_fortuna),
                    "motion_status": "direct"  # Parts are always direct
                })
                
                positions.append({
                    "name": "PARTE_ESPIRITU",
                    "longitude": float(parte_espiritu),
                    "sign": get_sign(parte_espiritu),
                    "motion_status": "direct"  # Parts are always direct
                })
        
        return positions
    except Exception as e:
        print(f"Error calculating positions with Skyfield: {str(e)}")
        return calculate_positions_with_approximation(utc_datetime, lat, lon)
        
def calculate_positions_with_utc(utc_datetime, lat=None, lon=None):
    """
    Calcula posiciones planetarias con un datetime UTC
    Asegura que el tiempo se ajusta correctamente según la zona horaria
    """
    try:
        # Usar el datetime UTC directamente
        print(f"Calculando posiciones para UTC: {utc_datetime}")
        t = ts.from_datetime(utc_datetime)
        earth = eph['earth']
        
        positions = []
        bodies = {
            'SOL': eph['sun'],
            'LUNA': eph['moon'],
            'MERCURIO': eph['mercury'],
            'VENUS': eph['venus'],
            'MARTE': eph['mars'],
            'JÚPITER': eph['jupiter barycenter'],
            'SATURNO': eph['saturn barycenter'],
            'URANO': eph['uranus barycenter'],
            'NEPTUNO': eph['neptune barycenter'],
            'PLUTÓN': eph['pluto barycenter']
        }
        
        for body_name, body in bodies.items():
            pos = earth.at(t).observe(body).apparent()
            lat_ecl, lon_ecl, dist = pos.ecliptic_latlon(epoch='date')
            
            longitude = float(lon_ecl.degrees) % 360
            
            # Calcular dignidad planetaria basado en la posición
            dignidad = calcular_dignidad_planetaria(body_name, longitude)
            
            positions.append({
                "name": body_name,
                "longitude": longitude,
                "sign": get_sign(longitude),
                "dignidad": dignidad
            })
        
        if lat is not None and lon is not None:
            asc, mc = calculate_asc_mc(t, lat, lon)
            
            positions.append({
                "name": "ASC",
                "longitude": float(asc),
                "sign": get_sign(asc)
            })
            
            positions.append({
                "name": "MC",
                "longitude": float(mc),
                "sign": get_sign(mc)
            })
        
        return positions
    except Exception as e:
        print(f"Error calculando posiciones: {str(e)}")
        # No lanzar excepción, simplemente retornar un error formateado
        print("Usando método alternativo de cálculo")
        try:
            return calculate_positions(
                utc_datetime.strftime("%d/%m/%Y"),
                utc_datetime.strftime("%H:%M"),
                lat,
                lon
            )
        except Exception as inner_e:
            print(f"Error en método alternativo: {str(inner_e)}")
            return []

def calculate_positions(date_str, time_str, lat=None, lon=None):
    try:
        if '-' in date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            date_str = date_obj.strftime("%d/%m/%Y")
            
        local_dt = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
        spain_tz = timezone(timedelta(hours=1))
        local_dt = local_dt.replace(tzinfo=spain_tz)
        utc_dt = local_dt.astimezone(timezone.utc)
        
        t = ts.from_datetime(utc_dt)
        earth = eph['earth']
        
        positions = []
        bodies = {
            'SOL': eph['sun'],
            'LUNA': eph['moon'],
            'MERCURIO': eph['mercury'],
            'VENUS': eph['venus'],
            'MARTE': eph['mars'],
            'JÚPITER': eph['jupiter barycenter'],
            'SATURNO': eph['saturn barycenter'],
            'URANO': eph['uranus barycenter'],
            'NEPTUNO': eph['neptune barycenter'],
            'PLUTÓN': eph['pluto barycenter']
        }
        
        for body_name, body in bodies.items():
            pos = earth.at(t).observe(body).apparent()
            lat_ecl, lon_ecl, dist = pos.ecliptic_latlon(epoch='date')
            
            longitude = float(lon_ecl.degrees) % 360
            
            # Añadir dignidad planetaria
            dignidad = calcular_dignidad_planetaria(body_name, longitude)
            
            positions.append({
                "name": body_name,
                "longitude": longitude,
                "sign": get_sign(longitude),
                "dignidad": dignidad
            })
        
        if lat is not None and lon is not None:
            asc, mc = calculate_asc_mc(t, lat, lon)
            
            positions.append({
                "name": "ASC",
                "longitude": float(asc),
                "sign": get_sign(asc)
            })
            
            positions.append({
                "name": "MC",
                "longitude": float(mc),
                "sign": get_sign(mc)
            })
        
        return positions
    except Exception as e:
        print(f"Error calculando posiciones: {str(e)}")
        return []

def calculate_positions_with_approximation(utc_datetime, lat=None, lon=None):
    """Alternative method to calculate planetary positions without Skyfield, including retrograde status"""
    try:
        print("Using approximate method for planetary calculations")
        
        # Date and time in compatible format
        date_str = utc_datetime.strftime("%Y-%m-%d")
        time_str = utc_datetime.strftime("%H:%M")
        
        # Base for approximate calculations based on J2000 epoch
        j2000 = datetime(2000, 1, 1, 12, 0).replace(tzinfo=timezone.utc)
        days_since_j2000 = (utc_datetime - j2000).total_seconds() / 86400
        
        # Approximate planetary mean positions (degrees/day since J2000)
        # These values are approximate and only for demonstration use
        planet_rates = {
            'SOL': 0.9856,              # 1 revolution per year
            'LUNA': 13.1764,            # 1 revolution per ~27.3 days
            'MERCURIO': 4.0923,         # 1 revolution per ~88 days
            'VENUS': 1.6021,            # 1 revolution per ~225 days
            'MARTE': 0.5240,            # 1 revolution per ~687 days
            'JÚPITER': 0.0830,          # 1 revolution per ~12 years
            'SATURNO': 0.0334,          # 1 revolution per ~29 years
            'URANO': 0.0117,            # 1 revolution per ~84 years
            'NEPTUNO': 0.006,           # 1 revolution per ~165 years
            'PLUTÓN': 0.004             # 1 revolution per ~248 years
        }
        
        # Approximate parameters for retrograde cycles (simplified)
        retrograde_params = {
            'MERCURIO': {'period': 116, 'duration': 24, 'offset': 36},  # Mercury: ~3 times per year for ~24 days
            'VENUS': {'period': 584, 'duration': 42, 'offset': 50},     # Venus: ~every 19 months for ~42 days
            'MARTE': {'period': 780, 'duration': 80, 'offset': 100},    # Mars: ~every 26 months for ~80 days
            'JÚPITER': {'period': 399, 'duration': 120, 'offset': 33},  # Jupiter: ~once per year for ~120 days
            'SATURNO': {'period': 378, 'duration': 140, 'offset': 73},  # Saturn: ~once per year for ~140 days
            'URANO': {'period': 370, 'duration': 155, 'offset': 80},    # Uranus: ~once per year for ~155 days
            'NEPTUNO': {'period': 367, 'duration': 160, 'offset': 40},  # Neptune: ~once per year for ~160 days
            'PLUTÓN': {'period': 366, 'duration': 175, 'offset': 18}    # Pluto: ~once per year for ~175 days
        }
        
        # Base positions at J2000 (approximate)
        planet_base = {
            'SOL': 280.0,
            'LUNA': 218.3,
            'MERCURIO': 90.0,
            'VENUS': 160.0,
            'MARTE': 200.0,
            'JÚPITER': 270.0,
            'SATURNO': 330.0,
            'URANO': 30.0,
            'NEPTUNO': 330.0,
            'PLUTÓN': 230.0
        }
        
        # Calculate approximate current positions
        positions = []
        for planet, rate in planet_rates.items():
            base_pos = planet_base[planet]
            current_pos = (base_pos + rate * days_since_j2000) % 360
            
            # Calculate planetary dignity
            dignidad = calcular_dignidad_planetaria(planet, current_pos)
            
            # Determine retrograde status (only for planets, not Sun or Moon)
            motion_status = "direct"  # Default
            daily_motion = rate
            
            if planet not in ['SOL', 'LUNA'] and planet in retrograde_params:
                params = retrograde_params[planet]
                # Calculate day within retrograde cycle
                cycle_day = (days_since_j2000 + params['offset']) % params['period']
                
                # Check if planet is in retrograde phase
                if cycle_day < params['duration']:
                    motion_status = "retrograde"
                    daily_motion = -rate * 0.3  # Approximate retrograde motion as slower
                
                # Check if planet is stationary (near the start or end of retrograde period)
                stationary_window = 2  # Days before/after retrograde where planet appears stationary
                if cycle_day < stationary_window:
                    motion_status = "stationary_retrograde"
                    daily_motion = 0.01  # Almost stopped
                elif params['duration'] - stationary_window < cycle_day < params['duration']:
                    motion_status = "stationary_direct"
                    daily_motion = 0.01  # Almost stopped
            
            positions.append({
                "name": planet,
                "longitude": current_pos,
                "sign": get_sign(current_pos),
                "dignidad": dignidad,
                "motion_status": motion_status,
                "daily_motion": daily_motion
            })
        
        # If we have coordinates, calculate cardinal points of the chart
        if lat is not None and lon is not None:
            asc, mc = calculate_asc_mc(utc_datetime, lat, lon)
            
            positions.append({
                "name": "ASC",
                "longitude": float(asc),
                "sign": get_sign(asc),
                "motion_status": "direct"  # ASC is always direct
            })
            
            positions.append({
                "name": "MC",
                "longitude": float(mc),
                "sign": get_sign(mc),
                "motion_status": "direct"  # MC is always direct
            })
            
            # Add descendant (opposite to ascendant)
            desc = (asc + 180) % 360
            positions.append({
                "name": "DSC",
                "longitude": float(desc),
                "sign": get_sign(desc),
                "motion_status": "direct"  # DSC is always direct
            })
            
            # Add Imum Coeli (IC) (opposite to MC)
            ic = (mc + 180) % 360
            positions.append({
                "name": "IC",
                "longitude": float(ic),
                "sign": get_sign(ic),
                "motion_status": "direct"  # IC is always direct
            })
            
            # Calculate and add Part of Fortune and Part of Spirit
            sol_planet = next((p for p in positions if p["name"] == "SOL"), None)
            luna_planet = next((p for p in positions if p["name"] == "LUNA"), None)
            
            if sol_planet and luna_planet:
                # Determine if it's a dry or humid birth
                is_dry = is_dry_birth(sol_planet["longitude"], asc)
                
                # Correct calculation of Part of Fortune based on chart nature
                if is_dry:  # Dry chart (diurnal)
                    # For diurnal charts: Part of Fortune = ASC + dist(Sun→Moon)
                    dist_sol_a_luna = distancia_zodiaco(sol_planet["longitude"], luna_planet["longitude"])
                    parte_fortuna = (asc + dist_sol_a_luna) % 360
                else:  # Humid chart (nocturnal)
                    # For nocturnal charts: Part of Fortune = ASC + dist(Moon→Sun)
                    dist_luna_a_sol = distancia_zodiaco(luna_planet["longitude"], sol_planet["longitude"])
                    parte_fortuna = (asc + dist_luna_a_sol) % 360
                
                # Correct calculation of Part of Spirit (logical inverse of Part of Fortune)
                if is_dry:  # Dry chart (diurnal)
                    # For diurnal charts: Part of Spirit = ASC + dist(Moon→Sun)
                    dist_luna_a_sol = distancia_zodiaco(luna_planet["longitude"], sol_planet["longitude"])
                    parte_espiritu = (asc + dist_luna_a_sol) % 360
                else:  # Humid chart (nocturnal)
                    # For nocturnal charts: Part of Spirit = ASC + dist(Sun→Moon)
                    dist_sol_a_luna = distancia_zodiaco(sol_planet["longitude"], luna_planet["longitude"])
                    parte_espiritu = (asc + dist_sol_a_luna) % 360
                
                # Add to positions
                positions.append({
                    "name": "PARTE_FORTUNA",
                    "longitude": float(parte_fortuna),
                    "sign": get_sign(parte_fortuna),
                    "motion_status": "direct"  # Parts are always direct
                })
                
                positions.append({
                    "name": "PARTE_ESPIRITU",
                    "longitude": float(parte_espiritu),
                    "sign": get_sign(parte_espiritu),
                    "motion_status": "direct"  # Parts are always direct
                })
        
        return positions
    
    except Exception as e:
        print(f"Error in calculate_positions_with_approximation: {str(e)}")
        # If all else fails, return simulated data
        return mockCalculatePositions(True)
        
def calculate_asc_mc(t, lat, lon):
    try:
        gst = t.gast
        lst = (gst * 15 + lon) % 360
        mc = lst % 360
        
        lat_rad = np.radians(lat)
        ra_rad = np.radians(lst)
        eps_rad = np.radians(23.4367)
        
        tan_asc = np.cos(ra_rad) / (np.sin(ra_rad) * np.cos(eps_rad) + np.tan(lat_rad) * np.sin(eps_rad))
        asc = np.degrees(np.arctan(-tan_asc))
        
        if 0 <= lst <= 180:
            if np.cos(ra_rad) > 0:
                asc = (asc + 180) % 360
        else:
            if np.cos(ra_rad) < 0:
                asc = (asc + 180) % 360
                
        asc = asc % 360
        
        dist_mc_asc = (asc - mc) % 360
        if dist_mc_asc > 180:
            asc = (asc + 180) % 360
        
        return asc, mc
    except Exception as e:
        print(f"Error en calculate_asc_mc: {str(e)}")
        # Valores por defecto en caso de error
        return 0, 0

def get_sign(longitude):
    longitude = float(longitude) % 360
    signs = [
        ("ARIES", 354.00, 36.00),
        ("TAURO", 30.00, 30.00),
        ("GÉMINIS", 60.00, 30.00),
        ("CÁNCER", 90.00, 30.00),
        ("LEO", 120.00, 30.00),
        ("VIRGO", 150.00, 36.00),
        ("LIBRA", 186.00, 24.00),
        ("ESCORPIO", 210.00, 30.00),
        ("OFIUCO", 240.00, 12.00),
        ("SAGITARIO", 252.00, 18.00),
        ("CAPRICORNIO", 270.00, 36.00),
        ("ACUARIO", 306.00, 18.00),
        ("PEGASO", 324.00, 6.00),
        ("PISCIS", 330.00, 24.00)
    ]
    
    for name, start, length in signs:
        end = start + length
        if start <= longitude < end:
            return name
        elif start > 354.00 and (longitude >= start or longitude < (end % 360)):
            # Caso especial para Aries que cruza 0°
            return name
    
    return "ARIES"  # Valor por defecto

def calcular_dignidad_planetaria(planeta, longitud):
    """
    Calcula la dignidad planetaria basada en la posición
    Retorna: domicilio, exaltación, caída, exilio o peregrine
    """
    signo = get_sign(longitud)
    
    if planeta in DIGNIDADES:
        # Verificar domicilio
        if signo in DIGNIDADES[planeta]['domicilio']:
            return "domicilio"
        # Verificar exaltación
        elif signo in DIGNIDADES[planeta]['exaltacion']:
            return "exaltacion"
        # Verificar caída
        elif signo in DIGNIDADES[planeta]['caida']:
            return "caida"
        # Verificar exilio
        elif signo in DIGNIDADES[planeta]['exilio']:
            return "exilio"
    
    # Si no está en ninguna dignidad especial
    return ""

# Simulación de datos planetarios para fines de demostración
def mockCalculatePositions(is_natal=True, asc_sign=None, asc_longitude=None):
    """
    Función que provee posiciones planetarias simuladas basadas en los datos 
    del archivo original Aplicación de Carta Astral Doble.tsx
    """
    base_positions = [
        {"name": "SOL", "longitude": 120 if is_natal else 150, "sign": "LEO" if is_natal else "VIRGO"},
        {"name": "LUNA", "longitude": 186 if is_natal else 210, "sign": "LIBRA" if is_natal else "SCORPIO"},
        {"name": "MERCURIO", "longitude": 135 if is_natal else 145, "sign": "LEO" if is_natal else "VIRGO"},
        {"name": "VENUS", "longitude": 90 if is_natal else 100, "sign": "CANCER" if is_natal else "CANCER"},
        {"name": "MARTE", "longitude": 210 if is_natal else 240, "sign": "SCORPIO" if is_natal else "OPHIUCHUS"},
        {"name": "JÚPITER", "longitude": 270 if is_natal else 290, "sign": "CAPRICORN" if is_natal else "CAPRICORN"},
        {"name": "SATURNO", "longitude": 330 if is_natal else 350, "sign": "PISCES" if is_natal else "PISCES"},
        {"name": "URANO", "longitude": 30 if is_natal else 32, "sign": "TAURUS" if is_natal else "TAURUS"},
        {"name": "NEPTUNO", "longitude": 354 if is_natal else 355, "sign": "ARIES" if is_natal else "ARIES"},
        {"name": "PLUTÓN", "longitude": 252 if is_natal else 254, "sign": "SAGITTARIUS" if is_natal else "SAGITTARIUS"},
        {"name": "ASC", "longitude": 0 if is_natal else 10, "sign": "ARIES" if is_natal else "ARIES"},
        {"name": "MC", "longitude": 270 if is_natal else 280, "sign": "CAPRICORN" if is_natal else "CAPRICORN"}
    ]
    
    # Añadir dignidades simuladas
    for planet in base_positions:
        if planet["name"] in DIGNIDADES:
            planet["dignidad"] = calcular_dignidad_planetaria(planet["name"], planet["longitude"])
    
    # Si no es natal, añadir una variación aleatoria a las posiciones
    if not is_natal:
        import random
        for planet in base_positions:
            # Esta variación mantiene la lógica del archivo original
            planet["longitude"] = (planet["longitude"] + random.uniform(-10, 10)) % 360
            planet["sign"] = get_sign(planet["longitude"])
            if planet["name"] in DIGNIDADES:
                planet["dignidad"] = calcular_dignidad_planetaria(planet["name"], planet["longitude"])
    
    # Añadir Parte de Fortuna y Parte del Espíritu simuladas
    asc = next((p for p in base_positions if p["name"] == "ASC"), None)
    sol = next((p for p in base_positions if p["name"] == "SOL"), None)
    luna = next((p for p in base_positions if p["name"] == "LUNA"), None)
    
    if asc and sol and luna:
        is_dry = is_dry_birth(sol["longitude"], asc["longitude"])
        
        # Cálculo correcto de Parte de Fortuna según la naturaleza de la carta
        if is_dry:  # Carta seca (diurna)
            # Para carta diurna: Parte de Fortuna = ASC + dist(Sol→Luna)
            dist_sol_a_luna = distancia_zodiaco(sol["longitude"], luna["longitude"])
            parte_fortuna = (asc["longitude"] + dist_sol_a_luna) % 360
        else:  # Carta húmeda (nocturna)
            # Para carta nocturna: Parte de Fortuna = ASC + dist(Luna→Sol)
            dist_luna_a_sol = distancia_zodiaco(luna["longitude"], sol["longitude"])
            parte_fortuna = (asc["longitude"] + dist_luna_a_sol) % 360
        
        # Cálculo correcto de Parte del Espíritu (inverso lógico de la Parte de Fortuna)
        if is_dry:  # Carta seca (diurna)
            # Para carta diurna: Parte del Espíritu = ASC + dist(Luna→Sol)
            dist_luna_a_sol = distancia_zodiaco(luna["longitude"], sol["longitude"])
            parte_espiritu = (asc["longitude"] + dist_luna_a_sol) % 360
        else:  # Carta húmeda (nocturna)
            # Para carta nocturna: Parte del Espíritu = ASC + dist(Sol→Luna)
            dist_sol_a_luna = distancia_zodiaco(sol["longitude"], luna["longitude"])
            parte_espiritu = (asc["longitude"] + dist_sol_a_luna) % 360
        
        base_positions.append({
            "name": "PARTE_FORTUNA",
            "longitude": parte_fortuna,
            "sign": get_sign(parte_fortuna)
        })
        
        base_positions.append({
            "name": "PARTE_ESPIRITU",
            "longitude": parte_espiritu,
            "sign": get_sign(parte_espiritu)
        })
    
    return base_positions

def calculate_aspects(planets1, planets2=None):
    """Calcula los aspectos entre planetas."""
    if planets2 is None:
        planets2 = planets1
    
    aspects = []
    traditional_planets = ["SOL", "LUNA", "MERCURIO", "VENUS", "MARTE", "JÚPITER", "SATURNO"]
    
    # Filtrar planetas tradicionales
    valid_planets1 = [p for p in planets1 if p["name"] in traditional_planets]
    valid_planets2 = [p for p in planets2 if p["name"] in traditional_planets]
    
    for i, planet1 in enumerate(valid_planets1):
        # Si estamos calculando aspectos en la misma carta, evitar duplicados
        start_j = i + 1 if planets1 == planets2 else 0
        
        for j in range(start_j, len(valid_planets2)):
            planet2 = valid_planets2[j]
            
            # Evitar comparar un planeta consigo mismo
            if planet1 == planet2:
                continue
            
            # Calcular la diferencia angular
            diff = abs(planet1["longitude"] - planet2["longitude"])
            if diff > 180:
                diff = 360 - diff
            
            # Buscar aspectos
            for aspect_type, aspect_data in ASPECTS.items():
                if abs(diff - aspect_data["angle"]) <= aspect_data["orb"]:
                    # Calcular la fuerza del aspecto basado en dignidades
                    fuerza_aspecto = calcular_fuerza_aspecto(planet1, planet2, aspect_type)
                    
                    aspects.append({
                        "planet1": planet1["name"],
                        "planet2": planet2["name"],
                        "type": aspect_type,
                        "angle": diff,
                        "color": aspect_data["color"],
                        "isInterChart": planets1 is not planets2,
                        "fuerza": fuerza_aspecto
                    })
                    break
    
    return aspects

def calcular_fuerza_aspecto(planet1, planet2, aspect_type):
    """
    Calcula la fuerza de un aspecto basado en las dignidades planetarias
    y el tipo de aspecto
    """
    # Valor base por tipo de aspecto
    valor_base = {
        'CONJUNCTION': 5,
        'SEXTILE': 3,
        'SQUARE': -2,
        'TRINE': 4,
        'OPPOSITION': -3,
        'QUINCUNX': -2
    }.get(aspect_type, 0)
    
    # Modificadores por dignidad
    modificadores = {
        'domicilio': 1.5,
        'exaltacion': 2,
        'peregrino': 0,
        'caida': -2,
        'exilio': -1.5
    }
    
    # Aplicar modificadores por dignidad de cada planeta
    mod1 = modificadores.get(planet1.get('dignidad', 'peregrino'), 0)
    mod2 = modificadores.get(planet2.get('dignidad', 'peregrino'), 0)
    
    # Fuerza total
    fuerza = valor_base + mod1 + mod2
    
    return fuerza

def is_dry_birth(sun_longitude, asc_longitude):
    """Determina si un nacimiento es seco o húmedo basado en la posición del Sol."""
    # Es seco cuando el Sol está entre las casas 6 y 11 (inclusive)
    diff = (sun_longitude - asc_longitude) % 360
    house = (diff / 30) + 1
    
    # Es seco si el Sol está en las casas 6 a 11
    return 6 <= house <= 11

def calcular_partes_arabes(positions):
    """Calcula la Parte de Fortuna y Parte del Espíritu a partir de las posiciones planetarias"""
    asc = next((p for p in positions if p["name"] == "ASC"), None)
    sol = next((p for p in positions if p["name"] == "SOL"), None)
    luna = next((p for p in positions if p["name"] == "LUNA"), None)
    
    if not asc or not sol or not luna:
        return None, None
    
    # Determinar si es seco o húmedo según la posición del Sol
    is_dry = is_dry_birth(sol["longitude"], asc["longitude"])
    
    # Cálculo correcto según nacimiento seco o húmedo
    if is_dry:  # Carta seca (diurna)
        # Para carta diurna: Parte de Fortuna = ASC + dist(Sol→Luna)
        dist_sol_a_luna = distancia_zodiaco(sol["longitude"], luna["longitude"])
        parte_fortuna = (asc["longitude"] + dist_sol_a_luna) % 360
        
        # Para carta diurna: Parte del Espíritu = ASC + dist(Luna→Sol)
        dist_luna_a_sol = distancia_zodiaco(luna["longitude"], sol["longitude"])
        parte_espiritu = (asc["longitude"] + dist_luna_a_sol) % 360
    else:  # Carta húmeda (nocturna)
        # Para carta nocturna: Parte de Fortuna = ASC + dist(Luna→Sol)
        dist_luna_a_sol = distancia_zodiaco(luna["longitude"], sol["longitude"])
        parte_fortuna = (asc["longitude"] + dist_luna_a_sol) % 360
        
        # Para carta nocturna: Parte del Espíritu = ASC + dist(Sol→Luna)
        dist_sol_a_luna = distancia_zodiaco(sol["longitude"], luna["longitude"])
        parte_espiritu = (asc["longitude"] + dist_sol_a_luna) % 360
    
    return parte_fortuna, parte_espiritu

# Funciones para Fardarias
def calculate_duration(planet, level):
    """Calcula la duración de un periodo de Fardaria."""
    number = PLANET_DATA[planet]['numero']
    if level == 1:
        return number * DURACIONES['AÑO']
    elif level == 2:
        return number * DURACIONES['MES']
    elif level == 3:
        return number * DURACIONES['SEMANA']
    elif level == 4:
        return number * DURACIONES['DIA']
    return 0

def get_rotated_planets(start_planet, planet_order):
    """Obtiene la secuencia de planetas rotada a partir del planeta inicial."""
    index = planet_order.index(start_planet)
    return planet_order[index:] + planet_order[:index]

def calculate_date(birth_date, day_offset):
    """Calcula una fecha a partir de una fecha base y un desplazamiento en días."""
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    
    date = birth_date + timedelta(days=int(day_offset))
    return date

def calculate_sub_periods(main_planet, level, start_day, end_day, birth_date, planet_order):
    """Calcula subperiodos de Fardarias."""
    if level > 4:
        return []
    
    periods = []
    current_day = start_day
    rotated_planets = get_rotated_planets(main_planet, planet_order)
    
    # Mapa de estimación de signo basado en mes
    month_sign_map = {
        1: "CAPRICORN", 2: "AQUARIUS", 3: "PISCES", 
        4: "ARIES", 5: "TAURUS", 6: "GEMINI",
        7: "CANCER", 8: "LEO", 9: "VIRGO", 
        10: "LIBRA", 11: "SCORPIO", 12: "OPHIUCHUS", 13: "SAGITTARIUS"
    }
    
    # Mapa de regentes zodiacales
    regente_map = {
        "ARIES": "MARTE",
        "TAURUS": "VENUS",
        "GEMINI": "MERCURIO",
        "CANCER": "LUNA",
        "LEO": "SOL",
        "VIRGO": "MERCURIO",
        "LIBRA": "VENUS",
        "SCORPIO": "MARTE",
        "SAGITTARIUS": "JÚPITER",
        "CAPRICORN": "SOL",
        "AQUARIUS": "LUNA",
        "PISCES": "JÚPITER",
        "OPHIUCHUS": "SATURNO"
    }
    
    for planet in rotated_planets:
        duration = calculate_duration(planet, level)
        actual_duration = min(duration, end_day - current_day)
        
        if actual_duration > 0:
            start_date = calculate_date(birth_date, current_day)
            end_date = calculate_date(birth_date, current_day + actual_duration)
            
            # Estimar el signo basado en el mes de inicio
            signo = month_sign_map.get(start_date.month, "ARIES")
            regente = regente_map.get(signo, "")
            
            period = {
                'planet': planet,
                'level': level,
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'startDay': current_day,
                'durationDays': actual_duration,
                'sign': signo,
                'regente': regente
            }
            
            period['subPeriods'] = calculate_sub_periods(
                planet,
                level + 1,
                current_day,
                current_day + actual_duration,
                birth_date,
                planet_order
            )
            
            periods.append(period)
            current_day += actual_duration
    
    return periods

def calculate_fardaria_periods(birth_date, is_dry, start_year=None, end_year=None):
    """Calcula los periodos de Fardarias para una fecha de nacimiento con filtrado opcional de años."""
    planet_order = PLANET_ORDER['seco'] if is_dry else PLANET_ORDER['humedo']
    all_periods = []
    current_day = 0
    total_years = 0
    max_years = 84  # Limitar a 84 años por defecto
    
    # Asegurar que birth_date es un objeto datetime
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    
    # Si se especifican años de inicio y fin, calcular límites en días
    start_day = 0
    end_day = max_years * DURACIONES['AÑO']  # Predeterminado a 84 años
    
    if start_year is not None and end_year is not None:
        birth_year = birth_date.year
        start_offset_years = max(0, start_year - birth_year)
        end_offset_years = min(max_years, end_year - birth_year + 1)
        
        start_day = start_offset_years * DURACIONES['AÑO']
        end_day = end_offset_years * DURACIONES['AÑO']
    
    # Continuar calculando periodos hasta llegar al límite
    while current_day < end_day:
        for planet in planet_order:
            duration = calculate_duration(planet, 1)
            
            # Verificar si este periodo está dentro del rango de interés
            if current_day + duration <= start_day:
                # El periodo termina antes del rango, saltamos
                current_day += duration
                continue
            
            if current_day >= end_day:
                # El periodo comienza después del rango, terminamos
                break
            
            # Calcular parte del periodo dentro del rango
            period_start_day = max(current_day, start_day)
            period_end_day = min(current_day + duration, end_day)
            period_duration = period_end_day - period_start_day
            
            if period_duration > 0:
                start_date = calculate_date(birth_date, period_start_day)
                end_date = calculate_date(birth_date, period_end_day)
                
                # Determinar signo zodiacal del período
                month_sign_map = {
                    1: "CAPRICORN", 2: "AQUARIUS", 3: "PISCES", 
                    4: "ARIES", 5: "TAURUS", 6: "GEMINI",
                    7: "CANCER", 8: "LEO", 9: "VIRGO", 
                    10: "LIBRA", 11: "SCORPIO", 12: "OPHIUCHUS", 13: "SAGITTARIUS"
                }
                
                signo = month_sign_map.get(start_date.month, "ARIES")
                
                # Determinar regente del signo
                regente_map = {
                    "ARIES": "MARTE",
                    "TAURUS": "VENUS",
                    "GEMINI": "MERCURIO",
                    "CANCER": "LUNA",
                    "LEO": "SOL",
                    "VIRGO": "MERCURIO",
                    "LIBRA": "VENUS",
                    "SCORPIO": "MARTE",
                    "SAGITTARIUS": "JÚPITER",
                    "CAPRICORN": "SOL",
                    "AQUARIUS": "LUNA",
                    "PISCES": "JÚPITER",
                    "OPHIUCHUS": "SATURNO"
                }
                
                regente = regente_map.get(signo, "")
                
                period = {
                    'planet': planet,
                    'level': 1,
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': end_date.strftime('%Y-%m-%d'),
                    'startDay': period_start_day,
                    'durationDays': period_duration,
                    'sign': signo,
                    'regente': regente
                }
                
                # Añadir subperiodos para la parte dentro del rango
                period['subPeriods'] = calculate_sub_periods(
                    planet,
                    2,
                    period_start_day,
                    period_end_day,
                    birth_date,
                    planet_order
                )
                
                all_periods.append(period)
            
            current_day += duration
            if current_day >= end_day:
                break
    
    return all_periods

# Funciones para Relevo Zodiacal
def generar_secuencia(inicio):
    """Genera la secuencia de signos a partir del ascendente."""
    orden = list(SIGNOS.keys())
    idx = orden.index(inicio.lower())
    return orden[idx:] + orden[:idx]

# Función para evaluar la calidad de un período astrológico
def evaluar_calidad_periodo(signo, carta_natal, is_dry):
    """
    Evalúa la calidad de un período basado en la posición de los planetas
    y sus aspectos con el signo activado. Considera a Mercurio como maléfico
    y no considera a Saturno como parte de la secta.
    """
    # Determinar qué planetas son significativos según la secta
    tipo_carta = 'seco' if is_dry else 'humedo'
    benefico_secta = PLANETA_SECTA[tipo_carta]['benefico_secta']
    malefico_contrario = PLANETA_SECTA[tipo_carta]['malefico_contrario']
    benefico_contrario = PLANETA_SECTA[tipo_carta]['benefico_contrario']
    malefico_mercurio = PLANETA_SECTA[tipo_carta]['malefico_mercurio']
    
    # Variables para evaluación
    planetas_en_signo = []
    planetas_aspectan_duro = []
    planetas_aspectan_armonico = []
    
    # Longitud del signo activado (rango aproximado)
    signo_longitud = {
        "ARIES": (354, 30),
        "TAURUS": (30, 60),
        "GEMINI": (60, 90),
        "CANCER": (90, 120),
        "LEO": (120, 150),
        "VIRGO": (150, 186),
        "LIBRA": (186, 210),
        "SCORPIO": (210, 240),
        "SAGITTARIUS": (252, 270),
        "CAPRICORN": (270, 306),
        "AQUARIUS": (306, 324),
        "PISCES": (324, 354),
        "OPHIUCHUS": (240, 252)  # Ajuste aproximado
    }.get(signo.upper(), (0, 30))
    
    signo_inicio = signo_longitud[0]
    signo_fin = signo_longitud[1]
    
    # Evaluar planetas en el signo y aspectos duros
    for planeta in carta_natal:
        if planeta["name"] in ["ASC", "MC", "DSC", "IC", "PARTE_FORTUNA", "PARTE_ESPIRITU"]:
            continue  # Saltar puntos no planetarios
            
        # Comprobar si el planeta está en el signo
        if planeta["sign"].upper() == signo.upper():
            planetas_en_signo.append(planeta["name"])
        
        # Comprobar aspectos duros (oposición y cuadratura)
        longitud_planeta = planeta["longitude"]
        
        # Punto medio del signo para calcular aspectos
        signo_medio = (signo_inicio + signo_fin) / 2
        
        # Calcular diferencia angular para oposición (~180°)
        diferencia_oposicion = abs(longitud_planeta - signo_medio)
        if abs(diferencia_oposicion - 180) <= 8:  # Orbe de 8°
            planetas_aspectan_duro.append({"planeta": planeta["name"], "aspecto": "oposición"})
        
        # Calcular diferencia angular para cuadratura (~90°)
        diferencia_cuadratura = abs(longitud_planeta - signo_medio) % 180
        if abs(diferencia_cuadratura - 90) <= 8:  # Orbe de 8°
            planetas_aspectan_duro.append({"planeta": planeta["name"], "aspecto": "cuadratura"})
            
        # Calcular aspectos armónicos (trígono y sextil)
        diferencia_trigono = abs(longitud_planeta - signo_medio) % 360
        if abs(diferencia_trigono - 120) <= 8:  # Orbe de 8°
            planetas_aspectan_armonico.append({"planeta": planeta["name"], "aspecto": "trígono"})
            
        diferencia_sextil = abs(longitud_planeta - signo_medio) % 360
        if abs(diferencia_sextil - 60) <= 6:  # Orbe de 6°
            planetas_aspectan_armonico.append({"planeta": planeta["name"], "aspecto": "sextil"})
    
    # Evaluar la calidad del período según las reglas interpretativas
    calidad = 0  # Neutral por defecto
    razones = []
    
    # Regla 1: Beneficio de secta a favor en el signo o aspectando
    if benefico_secta in planetas_en_signo:
        calidad += 5
        razones.append(f"El benefico de secta ({benefico_secta}) está presente en {signo}")
    
    # Regla 2: Maléfico contrario a secta en el signo o aspectando
    if malefico_contrario in planetas_en_signo:
        calidad -= 5
        razones.append(f"El maléfico contrario a secta ({malefico_contrario}) está presente en {signo}")
    
    # Regla 3: Mercurio como maléfico en el signo
    if malefico_mercurio in planetas_en_signo:
        calidad -= 3
        razones.append(f"Mercurio (maléfico) está presente en {signo}")
    
    # Evaluar planetas que aspectan por cuadratura u oposición
    for aspecto in planetas_aspectan_duro:
        if aspecto["planeta"] == benefico_secta:
            calidad += 3
            razones.append(f"El benefico de secta ({benefico_secta}) aspecta {signo} por {aspecto['aspecto']}")
        elif aspecto["planeta"] == malefico_contrario:
            calidad -= 4
            razones.append(f"El maléfico contrario a secta ({malefico_contrario}) aspecta {signo} por {aspecto['aspecto']}")
        elif aspecto["planeta"] == benefico_contrario:
            calidad += 2
            razones.append(f"El benefico contrario a secta ({benefico_contrario}) aspecta {signo} por {aspecto['aspecto']}")
        elif aspecto["planeta"] == malefico_mercurio:
            calidad -= 3
            razones.append(f"Mercurio (maléfico) aspecta {signo} por {aspecto['aspecto']}")
    
    # Añadir efecto de aspectos armónicos
    for aspecto in planetas_aspectan_armonico:
        if aspecto["planeta"] in [benefico_secta, benefico_contrario]:
            calidad += 2
            razones.append(f"{aspecto['planeta']} forma {aspecto['aspecto']} armónico con {signo}")
        elif aspecto["planeta"] in [malefico_contrario, malefico_mercurio]:
            calidad += 1  # Aspectos armónicos de maléficos son ligeramente benéficos
            razones.append(f"{aspecto['planeta']} forma {aspecto['aspecto']} armónico con {signo}")
    
    # Determinar calidad final del período
    calidad_texto = "neutral"
    if calidad >= 5:
        calidad_texto = "muy favorable"
    elif calidad >= 3:
        calidad_texto = "favorable"
    elif calidad <= -5:
        calidad_texto = "muy desfavorable"
    elif calidad <= -3:
        calidad_texto = "desfavorable"
    elif calidad > 0:
        calidad_texto = "ligeramente favorable"
    elif calidad < 0:
        calidad_texto = "ligeramente desfavorable"
    
    return {
        "calidad": calidad_texto,
        "puntuacion": calidad,
        "razones": razones,
        "planetas_en_signo": planetas_en_signo,
        "aspectos_duros": planetas_aspectan_duro,
        "aspectos_armonicos": planetas_aspectan_armonico
    }

def calcular_relevodPeriods(fecha_nac, ascendente, carta_natal=None, is_dry=None, start_year=None, end_year=None):
    """Calcula periodos de relevo zodiacal con filtrado opcional de años e interpretación."""
    # Normalizar y validar el ascendente
    ascendente_lower = ascendente.lower().strip()
    
    # Verificar si el ascendente está en la lista de SIGNOS
    if ascendente_lower not in SIGNOS:
        print(f"ADVERTENCIA: Ascendente '{ascendente}' no encontrado en SIGNOS. Usando 'aries' como predeterminado.")
        ascendente_lower = 'aries'
    
    # Ahora usar el ascendente validado
    secuencia = generar_secuencia(ascendente_lower)
    
    # Asegurar que fecha_nac es un objeto datetime
    if isinstance(fecha_nac, str):
        fecha_nac = datetime.strptime(fecha_nac, '%Y-%m-%d')
    
    # Si se especifican años de inicio y fin, calcular límites en días
    start_day = 0
    end_day = 84 * DURACIONES['AÑO']  # Predeterminado a 84 años
    
    if start_year is not None and end_year is not None:
        birth_year = fecha_nac.year
        start_offset_years = max(0, start_year - birth_year)
        end_offset_years = min(84, end_year - birth_year + 1)
        
        start_day = start_offset_years * DURACIONES['AÑO']
        end_day = end_offset_years * DURACIONES['AÑO']
    
    # Mapa de regentes zodiacales
    regente_map = {
        "aries": "MARTE",
        "tauro": "VENUS",
        "geminis": "MERCURIO",
        "cancer": "LUNA",
        "leo": "SOL",
        "virgo": "MERCURIO",
        "libra": "VENUS",
        "escorpio": "MARTE",
        "ofiuco": "SATURNO",
        "sagitario": "JÚPITER",
        "capricornio": "SOL",
        "acuario": "LUNA",
        "pegaso": "JÚPITER",
        "piscis": "JÚPITER"
    }
    
    periodos = []
    
    # Calcular la duración total de un ciclo completo (en días)
    duracion_ciclo_completo = sum(DURACION_POR_NIVEL[signo] * DURACIONES['AÑO'] for signo in secuencia)
    print(f"Duración de un ciclo completo de la secuencia: {duracion_ciclo_completo} días")
    
    # Calcular cuántos ciclos completos hay que saltar
    if start_day > 0:
        ciclos_completos = start_day // duracion_ciclo_completo
        dia_inicio_ajustado = start_day % duracion_ciclo_completo
    else:
        ciclos_completos = 0
        dia_inicio_ajustado = 0
    
    print(f"Saltando {ciclos_completos} ciclos completos, comenzando en día {dia_inicio_ajustado}")
    
    # Día actual, ajustado por ciclos completos saltados
    dia_actual = ciclos_completos * duracion_ciclo_completo
    
    # Continuar calculando periodos hasta llegar al límite
    while dia_actual < end_day:
        # Calcular en qué posición de la secuencia estamos después de varios ciclos
        dias_en_ciclo_actual = dia_actual % duracion_ciclo_completo
        
        # Encontrar el signo correspondiente a la posición actual
        dias_acumulados = 0
        idx_signo_inicial = 0
        
        for i, signo in enumerate(secuencia):
            dias_en_periodo = DURACION_POR_NIVEL[signo] * DURACIONES['AÑO']
            if dias_acumulados <= dias_en_ciclo_actual < dias_acumulados + dias_en_periodo:
                idx_signo_inicial = i
                dia_actual = dia_actual - (dias_en_ciclo_actual - dias_acumulados)  # Ajustar al inicio del signo actual
                break
            dias_acumulados += dias_en_periodo
        
        # Recorrer la secuencia desde el índice correcto
        for i in range(idx_signo_inicial, len(secuencia)):
            signo = secuencia[i]
            dias_en_periodo = DURACION_POR_NIVEL[signo] * DURACIONES['AÑO']
            
            # Verificar si este periodo está dentro del rango de interés
            if dia_actual + dias_en_periodo <= start_day:
                # El periodo termina antes del rango, saltamos
                dia_actual += dias_en_periodo
                continue
            
            if dia_actual >= end_day:
                # El periodo comienza después del rango, terminamos
                break
            
            # Calcular parte del periodo dentro del rango
            periodo_inicio_dia = max(dia_actual, start_day)
            periodo_fin_dia = min(dia_actual + dias_en_periodo, end_day)
            duracion_periodo = periodo_fin_dia - periodo_inicio_dia
            
            if duracion_periodo > 0:
                fecha_inicio = calculate_date(fecha_nac, periodo_inicio_dia)
                fecha_fin = calculate_date(fecha_nac, periodo_inicio_dia + duracion_periodo)
                
                # Obtener el regente del signo
                regente = regente_map.get(signo, "")
                
                # Calcular la edad aproximada en este periodo
                edad_aproximada = periodo_inicio_dia // DURACIONES['AÑO']
                
                periodo = {
                    'signo': signo,
                    'level': 1,
                    'planeta': SIGNOS[signo]['planeta'],
                    'start': fecha_inicio.strftime('%Y-%m-%d'),
                    'end': fecha_fin.strftime('%Y-%m-%d'),
                    'startDay': periodo_inicio_dia,
                    'durationDays': duracion_periodo,
                    'regente': regente,
                    'edad': edad_aproximada  # Incluir la edad para referencia
                }
                
                # Añadir interpretación si tenemos datos de carta natal
                if carta_natal and is_dry is not None:
                    # Convertir el signo minúscula a mayúscula para la evaluación
                    signo_upper = signo.upper()
                    if signo == 'geminis':
                        signo_upper = 'GEMINI'
                    elif signo == 'sagitario':
                        signo_upper = 'SAGITTARIUS'
                    elif signo == 'capricornio':
                        signo_upper = 'CAPRICORN'
                    elif signo == 'acuario':
                        signo_upper = 'AQUARIUS'
                    elif signo == 'escorpio':
                        signo_upper = 'SCORPIO'
                    elif signo == 'piscis':
                        signo_upper = 'PISCES'
                    
                    evaluacion = evaluar_calidad_periodo(signo_upper, carta_natal, is_dry)
                    periodo['calidad'] = evaluacion['calidad']
                    periodo['interpretacion'] = {
                        'calidad': evaluacion['calidad'],
                        'puntuacion': evaluacion['puntuacion'],
                        'razones': evaluacion['razones'],
                        'planetas_en_signo': evaluacion['planetas_en_signo'],
                        'aspectos_duros': evaluacion['aspectos_duros'],
                        'aspectos_armonicos': evaluacion['aspectos_armonicos']
                    }
                
                # Calcular subperiodos para la parte dentro del rango
                periodo['subPeriods'] = calcular_relevodSubperiodos(
                    fecha_nac,
                    periodo_inicio_dia,
                    duracion_periodo,
                    secuencia,
                    i,  # Índice actual en la secuencia
                    2,
                    carta_natal,
                    is_dry
                )
                
                periodos.append(periodo)
            
            # Avanzar al siguiente periodo principal
            dia_actual += dias_en_periodo
            if dia_actual >= end_day:
                break
        
        # Si llegamos al final de la secuencia pero no al límite, volvemos al inicio
        if dia_actual < end_day:
            # Pasar al siguiente ciclo
            print(f"Completado un ciclo, avanzando al siguiente. Día actual: {dia_actual}")
    
    return periodos
    
def calcular_relevodSubperiodos(fecha_nac, dia_inicio, duracion_total, secuencia, idx_inicial, nivel, carta_natal=None, is_dry=None):
    """Calcula subperiodos de relevo zodiacal con interpretación."""
    if nivel > 4:
        return []
    
    periodos = []
    dia_actual = 0
    unidad_tiempo = 'MES' if nivel == 2 else 'SEMANA' if nivel == 3 else 'DIA'
    duracion_unidad = DURACIONES[unidad_tiempo]
    
    # Mapa de regentes zodiacales
    regente_map = {
        "aries": "MARTE",
        "tauro": "VENUS",
        "geminis": "MERCURIO",
        "cancer": "LUNA",
        "leo": "SOL",
        "virgo": "MERCURIO",
        "libra": "VENUS",
        "escorpio": "MARTE",
        "ofiuco": "SATURNO",
        "sagitario": "JÚPITER",
        "capricornio": "SOL",
        "acuario": "LUNA",
        "pegaso": "JÚPITER",
        "piscis": "JÚPITER"
    }
    
    while dia_actual < duracion_total:
        for i in range(len(secuencia)):
            if dia_actual >= duracion_total:
                break
                
            signo = secuencia[(idx_inicial + i) % len(secuencia)]
            duracion_periodo = DURACION_POR_NIVEL[signo] * duracion_unidad
            duracion_real = min(duracion_periodo, duracion_total - dia_actual)
            
            if duracion_real > 0:
                fecha_inicio = calculate_date(fecha_nac, dia_inicio + dia_actual)
                fecha_fin = calculate_date(fecha_nac, dia_inicio + dia_actual + duracion_real)
                
                # Obtener el regente del signo
                regente = regente_map.get(signo, "")
                
                periodo = {
                    'signo': signo,
                    'level': nivel,
                    'planeta': SIGNOS[signo]['planeta'],
                    'start': fecha_inicio.strftime('%Y-%m-%d'),
                    'end': fecha_fin.strftime('%Y-%m-%d'),
                    'startDay': dia_inicio + dia_actual,
                    'durationDays': duracion_real,
                    'regente': regente
                }
                
                # Añadir interpretación si tenemos datos de carta natal
                if carta_natal and is_dry is not None and nivel <= 2:  # Solo para los primeros dos niveles
                    # Convertir el signo minúscula a mayúscula para la evaluación
                    signo_upper = signo.upper()
                    if signo == 'geminis':
                        signo_upper = 'GEMINI'
                    elif signo == 'sagitario':
                        signo_upper = 'SAGITTARIUS'
                    elif signo == 'capricornio':
                        signo_upper = 'CAPRICORN'
                    elif signo == 'acuario':
                        signo_upper = 'AQUARIUS'
                    elif signo == 'escorpio':
                        signo_upper = 'SCORPIO'
                    elif signo == 'piscis':
                        signo_upper = 'PISCES'
                    
                    evaluacion = evaluar_calidad_periodo(signo_upper, carta_natal, is_dry)
                    periodo['calidad'] = evaluacion['calidad']
                    periodo['interpretacion'] = {
                        'calidad': evaluacion['calidad'],
                        'puntuacion': evaluacion['puntuacion'],
                        'razones': evaluacion['razones'],
                        'planetas_en_signo': evaluacion['planetas_en_signo'],
                        'aspectos_duros': evaluacion['aspectos_duros']
                    }
                
                if nivel < 4:
                    periodo['subPeriods'] = calcular_relevodSubperiodos(
                        fecha_nac,
                        dia_inicio + dia_actual,
                        duracion_real,
                        secuencia,
                        (idx_inicial + i) % len(secuencia),
                        nivel + 1,
                        carta_natal,
                        is_dry
                    )
                
                periodos.append(periodo)
                dia_actual += duracion_real
    
    return periodos

# Función para calcular picos planetarios, considerando a Mercurio como maléfico
def calcular_fechas_picos(birth_date, is_dry, ascendente, start_year, end_year):
    """Calcula fechas de picos planetarios, considerando a Mercurio como maléfico."""
    picos = {
        "mayor": [],
        "moderado": [],
        "menor": []
    }
    
    # Convertir fecha de nacimiento a objeto datetime
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    
    # Obtener año de nacimiento para cálculos de rango
    birth_year = birth_date.year
    
    # Para cada tipo de pico y planeta correspondiente
    for tipo, condiciones in PICO_CONDICIONES.items():
        # Planetas benéficos para picos positivos
        for planeta in condiciones['planetas_requeridos']:
            # Calcular el ciclo planeta-específico
            ciclo_base = PLANET_DATA[planeta]['numero']
            
            # Para cada año en el rango de análisis
            for year_offset in range(start_year - birth_year, min(end_year - birth_year + 1, 85)):
                # Verificar si este año está en un ciclo planetario
                if year_offset % ciclo_base == 0:
                    # Calcular las fechas de activación basadas en ángulos
                    # Necesitamos 3 fechas: para Ascendente, Parte de Fortuna y Parte del Espíritu
                    
                    # 1. Fecha basada en el Ascendente
                    month_asc = ((ciclo_base * 2) % 12) + 1
                    day_asc = ((ciclo_base * 3) % 28) + 1
                    
                    # 2. Fecha basada en la Parte de Fortuna
                    month_fortuna = ((ciclo_base * 3) % 12) + 1
                    day_fortuna = ((ciclo_base * 5) % 28) + 1
                    
                    # 3. Fecha basada en la Parte del Espíritu
                    month_espiritu = ((ciclo_base * 5) % 12) + 1
                    day_espiritu = ((ciclo_base * 7) % 28) + 1
                    
                    # Crear las tres fechas
                    fechas = []
                    try:
                        # Fecha para Ascendente
                        year = birth_year + year_offset
                        date_asc = datetime(year, month_asc, min(day_asc, 28 if month_asc == 2 else 30 if month_asc in [4, 6, 9, 11] else 31))
                        fechas.append({
                            "fecha": date_asc.strftime('%Y-%m-%d'),
                            "punto": "Ascendente",
                            "angulo": ciclo_base * 30  # Convertir ciclo a grados multiplicando por 30
                        })
                        
                        # Fecha para Parte de Fortuna
                        date_fortuna = datetime(year, month_fortuna, min(day_fortuna, 28 if month_fortuna == 2 else 30 if month_fortuna in [4, 6, 9, 11] else 31))
                        fechas.append({
                            "fecha": date_fortuna.strftime('%Y-%m-%d'),
                            "punto": "Parte de Fortuna",
                            "angulo": ciclo_base * 36  # Usar un múltiplo diferente
                        })
                        
                        # Fecha para Parte del Espíritu
                        date_espiritu = datetime(year, month_espiritu, min(day_espiritu, 28 if month_espiritu == 2 else 30 if month_espiritu in [4, 6, 9, 11] else 31))
                        fechas.append({
                            "fecha": date_espiritu.strftime('%Y-%m-%d'),
                            "punto": "Parte del Espíritu",
                            "angulo": ciclo_base * 45  # Otro múltiplo diferente
                        })
                    except ValueError as e:
                        print(f"Error creando fechas para {planeta} en año {year}: {e}")
                        continue
                        
                    # Calcular fuerza basada en el tipo de pico
                    fuerza_base = condiciones['min_fuerza']
                    
                    # Añadir todas las fechas calculadas al resultado
                    for fecha_info in fechas:
                        # Añadir el pico al tipo correspondiente con información de ángulos
                        tipo_key = tipo.lower()
                        # Variación de fuerza según el punto
                        if fecha_info["punto"] == "Ascendente":
                            fuerza = fuerza_base + 2  # Mayor fuerza desde el Ascendente
                        elif fecha_info["punto"] == "Parte de Fortuna":
                            fuerza = fuerza_base + 1  # Fuerza intermedia
                        else:
                            fuerza = fuerza_base      # Fuerza base para Parte del Espíritu
                            
                        # Determinar el signo zodiacal para la fecha
                        month_sign_map = {
                            1: "CAPRICORN", 2: "AQUARIUS", 3: "PISCES", 
                            4: "ARIES", 5: "TAURUS", 6: "GEMINI",
                            7: "CANCER", 8: "LEO", 9: "VIRGO", 
                            10: "LIBRA", 11: "SCORPIO", 12: "OPHIUCHUS", 13: "SAGITTARIUS"
                        }
                        
                        # Determinar signo aproximado basado en el mes
                        fecha_dt = datetime.strptime(fecha_info["fecha"], '%Y-%m-%d')
                        signo_aprox = month_sign_map.get(fecha_dt.month, "ARIES")
                        
                        # Determinar regente del signo
                        regente_map = {
                            "ARIES": "MARTE",
                            "TAURUS": "VENUS",
                            "GEMINI": "MERCURIO",
                            "CANCER": "LUNA",
                            "LEO": "SOL",
                            "VIRGO": "MERCURIO",
                            "LIBRA": "VENUS",
                            "SCORPIO": "MARTE",
                            "SAGITTARIUS": "JÚPITER",
                            "CAPRICORN": "SOL",
                            "AQUARIUS": "LUNA",
                            "PISCES": "JÚPITER",
                            "OPHIUCHUS": "SATURNO"  # Añadido para compatibilidad
                        }
                        
                        regente = regente_map.get(signo_aprox, "")
                        
                        picos[tipo_key].append({
                            "fecha": fecha_info["fecha"],
                            "planeta": planeta,
                            "tipo": "benéfico",
                            "fuerza": fuerza,
                            "punto": fecha_info["punto"],
                            "angulo": fecha_info["angulo"],
                            "signo": signo_aprox,
                            "regente": regente,
                            "descripcion": f"Pico {tipo} de {planeta} (benéfico) con fuerza {fuerza} en {signo_aprox} desde {fecha_info['punto']} (ángulo {fecha_info['angulo']}°)"
                        })
                        
        # También considerar picos negativos para planetas maléficos
        for planeta in condiciones['planetas_maleficos']:
            ciclo_base = PLANET_DATA[planeta]['numero']
            
            # Cálculo similar al de los benéficos, pero con fuerza negativa
            for year_offset in range(start_year - birth_year, min(end_year - birth_year + 1, 85)):
                if year_offset % ciclo_base == 0:
                    # Calcular fechas similares para maléficos
                    month_asc = ((ciclo_base * 2) % 12) + 1
                    day_asc = ((ciclo_base * 3) % 28) + 1
                    
                    try:
                        year = birth_year + year_offset
                        date_asc = datetime(year, month_asc, min(day_asc, 28 if month_asc == 2 else 30 if month_asc in [4, 6, 9, 11] else 31))
                        
                        # Determinar el signo
                        month_sign_map = {
                            1: "CAPRICORN", 2: "AQUARIUS", 3: "PISCES", 
                            4: "ARIES", 5: "TAURUS", 6: "GEMINI",
                            7: "CANCER", 8: "LEO", 9: "VIRGO", 
                            10: "LIBRA", 11: "SCORPIO", 12: "SAGITTARIUS"
                        }
                        
                        fecha_dt = date_asc
                        signo_aprox = month_sign_map.get(fecha_dt.month, "ARIES")
                        
                        # Determinar regente del signo
                        regente_map = {
                            "ARIES": "MARTE",
                            "TAURUS": "VENUS",
                            "GEMINI": "MERCURIO",
                            "CANCER": "LUNA",
                            "LEO": "SOL",
                            "VIRGO": "MERCURIO",
                            "LIBRA": "VENUS",
                            "SCORPIO": "MARTE",
                            "SAGITTARIUS": "JÚPITER",
                            "CAPRICORN": "SOL",
                            "AQUARIUS": "LUNA",
                            "PISCES": "JÚPITER",
                            "OPHIUCHUS": "SATURNO"
                        }
                        
                        regente = regente_map.get(signo_aprox, "")
                        
                        # Para maléficos, el nivel es uno menor que el tipo
                        tipo_key = tipo.lower()
                        if tipo_key == "mayor":
                            nivel_malefico = "moderado"  # Degradar un nivel para maléficos
                        elif tipo_key == "moderado":
                            nivel_malefico = "menor"
                        else:
                            nivel_malefico = "menor"
                            
                        fuerza_base = PICO_CONDICIONES[nivel_malefico.upper()]['min_fuerza']
                        
                        if planeta == "MERCURIO":
                            fuerza_mod = -2  # Mercurio tiene efecto negativo más moderado
                        else:
                            fuerza_mod = -3  # Marte tiene efecto negativo más fuerte
                        
                        picos[nivel_malefico].append({
                            "fecha": date_asc.strftime('%Y-%m-%d'),
                            "planeta": planeta,
                            "tipo": "maléfico",
                            "fuerza": fuerza_mod,
                            "punto": "Ascendente",
                            "angulo": ciclo_base * 30,
                            "signo": signo_aprox,
                            "regente": regente,
                            "descripcion": f"Pico {nivel_malefico} de {planeta} (maléfico) con efecto desafiante en {signo_aprox}"
                        })
                        
                    except ValueError as e:
                        print(f"Error creando fechas para maléfico {planeta} en año {year}: {e}")
                        continue
    
    # Ordenar cada tipo de pico por fecha
    picos["mayor"].sort(key=lambda x: x["fecha"])
    picos["moderado"].sort(key=lambda x: x["fecha"])
    picos["menor"].sort(key=lambda x: x["fecha"])
    
    return picos

# Calcular fechas de liberación de enlaces
def calcular_fechas_liberacion(birth_date, is_dry, ascendente, start_year, end_year, punto_referencia=None):
    """Calcula fechas de liberación de enlaces a lo largo del tiempo."""
    liberaciones = []
    
    # Convertir fecha de nacimiento a objeto datetime
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    
    # Obtener año de nacimiento para cálculos de rango
    birth_year = birth_date.year
    
    # Si hay un punto de referencia específico, usar solo ese
    puntos_ref = [punto_referencia] if punto_referencia else ["ASCENDENTE", "PARTE_FORTUNA", "PARTE_ESPIRITU"]
    
    # Para cada punto de referencia
    for punto in puntos_ref:
        punto_info = PUNTOS_REFERENCIA.get(punto, PUNTOS_REFERENCIA["ASCENDENTE"])
        factor_mes = punto_info["factor_mes"]
        factor_dia = punto_info["factor_dia"]
        fuerza_mod = punto_info["fuerza_modificador"]
        
        # Para cada combinación de liberador-liberado
        for liberador, data in LIBERACION_ENLACE.items():
            for liberado in data["libera"]:
                # Calcular el ciclo basado en los números planetarios
                ciclo = PLANET_DATA[liberador]["numero"] + PLANET_DATA[liberado]["numero"]
                
                # Para cada año en el rango de análisis
                for year_offset in range(start_year - birth_year, min(end_year - birth_year + 1, 85)):
                    # Verificar si este año está en un ciclo de liberación
                    if year_offset % ciclo == 0:
                        # Calcular fecha de liberación
                        year = birth_year + year_offset
                        
                        # Mes y día basados en factores específicos del punto de referencia
                        month = ((PLANET_DATA[liberador]["numero"] * factor_mes) % 12) + 1
                        day = ((PLANET_DATA[liberado]["numero"] * factor_dia) % 28) + 1
                        
                        try:
                            # Crear fecha específica
                            liberation_date = datetime(year, month, min(day, 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31))
                            
                            # Calcular ángulo (basado en ciclo * 30°)
                            angulo = (ciclo * 30) % 360
                            
                            # Calcular fuerza de liberación
                            fuerza = PLANET_DATA[liberador]["numero"] + fuerza_mod
                            
                            # Determinar el signo zodiacal para la fecha
                            month_sign_map = {
                                1: "CAPRICORN", 2: "AQUARIUS", 3: "PISCES", 
                                4: "ARIES", 5: "TAURUS", 6: "GEMINI",
                                7: "CANCER", 8: "LEO", 9: "VIRGO", 
                                10: "LIBRA", 11: "SCORPIO", 12: "OPHIUCHUS", 13: "SAGITTARIUS"
                            }
                            
                            signo = month_sign_map.get(month, "ARIES")
                            
                            # Determinar regente del signo
                            regente_map = {
                                "ARIES": "MARTE",
                                "TAURUS": "VENUS",
                                "GEMINI": "MERCURIO",
                                "CANCER": "LUNA",
                                "LEO": "SOL",
                                "VIRGO": "MERCURIO",
                                "LIBRA": "VENUS",
                                "SCORPIO": "MARTE",
                                "SAGITTARIUS": "JÚPITER",
                                "CAPRICORN": "SOL",
                                "AQUARIUS": "LUNA",
                                "PISCES": "JÚPITER",
                                "OPHIUCHUS": "SATURNO"  # Añadido para compatibilidad
                            }
                            
                            regente = regente_map.get(signo, "")
                            
                            # Añadir a la lista de liberaciones
                            liberaciones.append({
                                "fecha": liberation_date.strftime('%Y-%m-%d'),
                                "planeta_liberador": liberador,
                                "planeta_liberado": liberado,
                                "punto": punto,
                                "angulo": angulo,
                                "fuerza": fuerza,
                                "signo": signo,
                                "regente": regente,
                                "condicion": data["condicion"],
                                "descripcion": f"Liberación: {liberador} en {signo} (regente: {regente}) libera a {liberado} (ángulo: {angulo}°)"
                            })
                        except ValueError as e:
                            print(f"Error al crear fecha de liberación: {e}")
                            # Manejar fechas inválidas (como 30 de febrero)
                            continue
    
    # Ordenar por fecha
    liberaciones.sort(key=lambda x: x["fecha"])
    return liberaciones

# Calcular fechas de disolución de enlaces
def calcular_fechas_disolucion(birth_date, is_dry, ascendente, start_year, end_year):
    """Calcula fechas de disolución de enlaces a lo largo del tiempo."""
    disoluciones = []
    
    # Convertir fecha de nacimiento a objeto datetime
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    
    # Obtener la secuencia de planetas según nacimiento seco/húmedo
    planet_order = PLANET_ORDER['seco'] if is_dry else PLANET_ORDER['humedo']
    
    # Obtener año de nacimiento para cálculos de rango
    birth_year = birth_date.year
    
    # Asegurar que todos los años hasta 84 están cubiertos
    for year_offset in range(start_year - birth_year, min(end_year - birth_year + 1, 85)):
        year_date = birth_date.replace(year=birth_year + year_offset)
        
        # Para cada combinación de planetas susceptible a disolución
        for planet1, data in ENLACE_PLANETARIO.items():
            for planet2 in data.get('neutraliza', []):
                # Calcular fecha específica basada en los números planetarios
                month_offset = (PLANET_DATA[planet1]['numero'] + PLANET_DATA[planet2]['numero']) % 12
                if month_offset == 0:
                    month_offset = 12
                
                day_offset = ((PLANET_DATA[planet1]['numero'] * PLANET_DATA[planet2]['numero']) % 28) + 1
                
                try:
                    # Crear fecha específica para este año
                    dissolution_date = year_date.replace(month=month_offset, day=min(day_offset, 28))
                    
                    # Determinar el signo zodiacal para la fecha
                    month_sign_map = {
                        1: "CAPRICORN", 2: "AQUARIUS", 3: "PISCES", 
                        4: "ARIES", 5: "TAURUS", 6: "GEMINI",
                        7: "CANCER", 8: "LEO", 9: "VIRGO", 
                        10: "LIBRA", 11: "SCORPIO", 12: "OPHIUCHUS", 13: "SAGITTARIUS"
                    }
                    
                    signo = month_sign_map.get(month_offset, "ARIES")
                    
                    # Determinar regente del signo
                    regente_map = {
                        "ARIES": "MARTE",
                        "TAURUS": "VENUS",
                        "GEMINI": "MERCURIO",
                        "CANCER": "LUNA",
                        "LEO": "SOL",
                        "VIRGO": "MERCURIO",
                        "LIBRA": "VENUS",
                        "SCORPIO": "MARTE",
                        "SAGITTARIUS": "JÚPITER",
                        "CAPRICORN": "SOL",
                        "AQUARIUS": "LUNA",
                        "PISCES": "JÚPITER",
                        "OPHIUCHUS": "SATURNO"  # Añadido para compatibilidad
                    }
                    
                    regente = regente_map.get(signo, "")
                    
                    # Si la fecha está en el rango requerido
                    if start_year <= dissolution_date.year <= end_year:
                        disoluciones.append({
                            "fecha": dissolution_date.strftime('%Y-%m-%d'),
                            "planeta1": planet1,
                            "planeta2": planet2,
                            "tipo": "disolución",
                            "signo": signo,
                            "regente": regente,
                            "descripcion": f"Disolución de enlace entre {planet1} y {planet2} en {signo} (regente: {regente})"
                        })
                except ValueError as e:
                    # Manejar posibles errores de fecha inválida
                    print(f"Error al crear fecha de disolución: {e}")
                    # Intentar con el último día del mes
                    try:
                        if month_offset == 2:
                            # Febrero
                            dissolution_date = year_date.replace(month=month_offset, day=28)
                        elif month_offset in [4, 6, 9, 11]:
                            # Abril, Junio, Septiembre, Noviembre
                            dissolution_date = year_date.replace(month=month_offset, day=30)
                        else:
                            # Otros meses
                            dissolution_date = year_date.replace(month=month_offset, day=31)
                        
                        # Determinar el signo zodiacal para la fecha
                        month_sign_map = {
                            1: "CAPRICORN", 2: "AQUARIUS", 3: "PISCES", 
                            4: "ARIES", 5: "TAURUS", 6: "GEMINI",
                            7: "CANCER", 8: "LEO", 9: "VIRGO", 
                            10: "LIBRA", 11: "SCORPIO", 12: "SAGITTARIUS"
                        }
                        
                        signo = month_sign_map.get(month_offset, "ARIES")
                        
                        # Determinar regente del signo
                        regente_map = {
                            "ARIES": "MARTE",
                            "TAURUS": "VENUS",
                            "GEMINI": "MERCURIO",
                            "CANCER": "LUNA",
                            "LEO": "SOL",
                            "VIRGO": "MERCURIO",
                            "LIBRA": "VENUS",
                            "SCORPIO": "MARTE",
                            "SAGITTARIUS": "JÚPITER",
                            "CAPRICORN": "SOL",
                            "AQUARIUS": "LUNA",
                            "PISCES": "JÚPITER",
                            "OPHIUCHUS": "SATURNO"  # Añadido para compatibilidad
                        }
                        
                        regente = regente_map.get(signo, "")
                        
                        if start_year <= dissolution_date.year <= end_year:
                            disoluciones.append({
                                "fecha": dissolution_date.strftime('%Y-%m-%d'),
                                "planeta1": planet1,
                                "planeta2": planet2,
                                "tipo": "disolución",
                                "signo": signo,
                                "regente": regente,
                                "descripcion": f"Disolución de enlace entre {planet1} y {planet2} en {signo} (regente: {regente})"
                            })
                    except ValueError:
                        continue
    
    # Ordenar por fecha
    disoluciones.sort(key=lambda x: x["fecha"])
    return disoluciones
    
# Función que crea un componente visual de interpretación para el cliente
def create_interpretacion_html(periodo, parte_referencia="Carta Natal"):
    """
    Crea un componente HTML para mostrar la interpretación
    de un período de tiempo en las predicciones.
    
    Args:
        periodo: Dict con datos del periodo
        parte_referencia: Referencia para la interpretación (por defecto "Carta Natal")
    
    Returns:
        String con HTML formateado
    """
    if not periodo.get('interpretacion'):
        return ""
        
    interp = periodo['interpretacion']
    
    # Colores según calidad
    color_map = {
        "muy favorable": "#28a745",
        "favorable": "#5cb85c",
        "ligeramente favorable": "#a3cfbb",
        "neutral": "#6c757d",
        "ligeramente desfavorable": "#ffc107",
        "desfavorable": "#dc3545",
        "muy desfavorable": "#8B0000"
    }
    
    color = color_map.get(interp['calidad'], "#6c757d")
    
    html = f"""
    <div class="interpretacion-container" style="border-left: 4px solid {color}; padding: 10px; margin-bottom: 15px; background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1);">
        <h5 style="color: {color};">Interpretación según {parte_referencia}</h5>
        <p><strong>Calidad del período:</strong> <span style="color: {color};">{interp['calidad'].upper()}</span></p>
        
        <div class="razones-container">
            <strong>Razones:</strong>
            <ul>
    """
    
    # Añadir razones
    for razon in interp['razones']:
        html += f"<li>{razon}</li>"
    
    # Si no hay razones
    if not interp['razones']:
        html += "<li>No hay factores significativos para este período</li>"
    
    html += """
            </ul>
        </div>
    """
    
    # Añadir planetas en el signo
    if interp.get('planetas_en_signo'):
        html += "<p><strong>Planetas presentes:</strong> " + ", ".join(interp['planetas_en_signo']) + "</p>"
    
    # Añadir aspectos duros
    if interp.get('aspectos_duros'):
        html += "<p><strong>Aspectos duros:</strong> "
        aspectos = [f"{asp['planeta']} ({asp['aspecto']})" for asp in interp['aspectos_duros']]
        html += ", ".join(aspectos) + "</p>"
    
    # Añadir aspectos armónicos
    if interp.get('aspectos_armonicos'):
        html += "<p><strong>Aspectos armónicos:</strong> "
        aspectos = [f"{asp['planeta']} ({asp['aspecto']})" for asp in interp['aspectos_armonicos']]
        html += ", ".join(aspectos) + "</p>"
    
    html += """
    </div>
    """
    
    return html

@app.route('/calculate_forecasts', methods=['POST'])
def calculate_forecasts():
    """Endpoint para calcular picos y liberaciones a lo largo del tiempo con interpretación."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        birth_date = data.get('birthDate')
        is_dry = data.get('isDry')
        ascendente = data.get('ascendente')
        start_year = data.get('startYear')
        end_year = data.get('endYear')
        punto_referencia = data.get('puntoReferencia')  # Punto de referencia
        carta_natal = data.get('cartaNatal')  # Posiciones planetarias de la carta natal
        
        if not birth_date or is_dry is None or not ascendente:
            return jsonify({"error": "Faltan datos obligatorios"}), 400
        
        # Validar punto de referencia
        if punto_referencia and punto_referencia not in PUNTOS_REFERENCIA:
            return jsonify({"error": f"Punto de referencia '{punto_referencia}' no válido. Opciones: {', '.join(PUNTOS_REFERENCIA.keys())}"}), 400
        
        # Asegurar que tenemos un valor para los años y extender hasta 84 años
        birth_year = datetime.strptime(birth_date, '%Y-%m-%d').year
        
        if start_year is None:
            start_year = birth_year
        if end_year is None:
            end_year = birth_year + 84  # Hasta 84 años desde el nacimiento
        else:
            # Asegurar que el rango máximo es 84 años
            end_year = min(end_year, birth_year + 84)
        
        print(f"Calculando pronósticos desde {start_year} hasta {end_year} para nacimiento {birth_date}")
        if punto_referencia:
            print(f"Usando punto de referencia: {punto_referencia}")
        
        # Calcular periodos de fardarias
        fardarias = calculate_fardaria_periods(birth_date, is_dry, start_year, end_year)
        
        # Calcular relevo zodiacal con interpretación si tenemos carta natal
        relevo = calcular_relevodPeriods(birth_date, ascendente, carta_natal, is_dry, start_year, end_year)
        
        # Calcular fechas de disolución de enlaces
        disoluciones = calcular_fechas_disolucion(birth_date, is_dry, ascendente, start_year, end_year)
        
        # Calcular fechas de picos
        picos = calcular_fechas_picos(birth_date, is_dry, ascendente, start_year, end_year)
        
        # Calcular fechas de liberación con el punto de referencia especificado
        liberaciones = calcular_fechas_liberacion(birth_date, is_dry, ascendente, start_year, end_year, punto_referencia)
        
        # Datos de planetas por secta
        datos_secta = PLANETA_SECTA['seco'] if is_dry else PLANETA_SECTA['humedo']
        
        # Preparar resultado
        result = {
            "fardarias": fardarias,
            "relevo": relevo,
            "disoluciones": disoluciones,
            "picos": picos,
            "liberaciones": liberaciones,
            "puntos_referencia": {
                k: {"descripcion": v["descripcion"]} for k, v in PUNTOS_REFERENCIA.items()
            },
            "planetas_secta": datos_secta  # Información sobre los planetas significativos por secta
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error calculando pronósticos: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error en el cálculo: {str(e)}"}), 500

# También necesitamos modificar transit_for_date para incluir el mismo parámetro
@app.route('/transit_for_date', methods=['POST'])
def transit_for_date():
    """Endpoint para calcular tránsitos para una fecha específica."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        transit_date = data.get('date')
        transit_time = data.get('time', '12:00')  # Por defecto mediodía
        city = data.get('city')
        calculate_analysis = data.get('calculateAnalysis', False)
        use_sidereal = data.get('useSidereal', False)  # Parámetro para zodiaco sideral
        
        if not transit_date or not city:
            return jsonify({"error": "Faltan datos obligatorios (date, city)"}), 400
        
        print(f"Calculando tránsitos para: {city}, {transit_date} {transit_time}")
        print(f"Sistema de zodiaco: {'Sideral' if use_sidereal else 'Tropical'}")
        
        # Obtener datos de ciudad (coordenadas)
        ciudades = obtener_datos_ciudad(city)
        
        if isinstance(ciudades, dict) and 'error' in ciudades:
            return jsonify({"error": f"Error obteniendo datos de la ciudad: {ciudades['error']}"}), 400
        
        if not ciudades or len(ciudades) == 0:
            return jsonify({"error": "No se encontró la ciudad"}), 404
        
        # Usar la primera ciudad encontrada
        coordenadas = ciudades[0]
        lat = coordenadas["lat"]
        lon = coordenadas["lon"]
        
        # Obtener zona horaria
        timezone_info = obtener_zona_horaria(coordenadas, transit_date)
        
        # Convertir fecha y hora local a UTC
        utc_datetime = convertir_a_utc(transit_date, transit_time, timezone_info)
        
        # Calcular posiciones planetarias
        positions = calculate_positions_with_skyfield(utc_datetime, lat, lon)
        
        # Si se requiere zodiaco sideral, aplicar la corrección Fagan-Allen
        if use_sidereal:
            for planet in positions:
                # Guardar longitud tropical original
                planet["tropical_longitude"] = planet["longitude"]
                # Ajustar la longitud restando el ayanamsa
                planet["longitude"] = (planet["longitude"] - FAGAN_ALLEN_AYANAMSA + 360) % 360
                # Actualizar el signo basado en la nueva longitud
                planet["sign"] = get_sign(planet["longitude"])
                # Recalcular dignidad basada en el nuevo signo
                planet["dignidad"] = calcular_dignidad_planetaria(planet["name"], planet["longitude"])
        
        # Calcular aspectos
        aspects = calculate_aspects(positions)
        
        # Preparar resultado
        result = {
            "positions": positions,
            "aspects": aspects,
            "date": transit_date,
            "time": transit_time,
            "city": city,
            "zodiacSystem": "sidereal" if use_sidereal else "tropical"
        }
        
        # Si se solicitó análisis avanzado, calcularlo
        if calculate_analysis:
            # Cálculo de enlaces planetarios
            enlaces = calcular_enlaces_planetarios(positions, aspects)
            result["enlaces"] = enlaces
            
            # Cálculo de picos
            pico_mayor = calcular_picos(positions, aspects, "MAYOR")
            pico_moderado = calcular_picos(positions, aspects, "MODERADO")
            pico_menor = calcular_picos(positions, aspects, "MENOR")
            
            result["pico_mayor"] = pico_mayor
            result["pico_moderado"] = pico_moderado
            result["pico_menor"] = pico_menor
            
            # Cálculo de liberación de enlace
            lib_enlace = calcular_liberacion_enlace(positions, aspects)
            result["liberacion_enlace"] = lib_enlace
            
            # Cálculo de presagios
            presagios = calcular_presagios(positions, aspects)
            result["presagios"] = presagios
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error calculando tránsitos: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error en el cálculo: {str(e)}"}), 500

# Modificar la función calculate_chart para aceptar el parámetro useSidereal
# Reemplazar la función calculate_chart en server.py

@app.route('/calculate', methods=['POST'])
def calculate_chart():
    """Endpoint para calcular una carta astral."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400
        
        city = data.get('city')
        date = data.get('date')
        time = data.get('time')
        calculate_analysis = data.get('calculateAnalysis', False)
        use_sidereal = data.get('useSidereal', False)  # Parámetro para zodiaco sideral
        include_stars = data.get('includeStars', False)  # Parámetro para incluir estrellas fijas
        
        if not city or not date or not time:
            return jsonify({"error": "Faltan datos obligatorios (city, date, time)"}), 400
        
        print(f"Calculando carta para: {city}, {date} {time}")
        print(f"Sistema de zodiaco: {'Sideral' if use_sidereal else 'Tropical'}")
        
        # Obtener datos de ciudad (coordenadas)
        ciudades = obtener_datos_ciudad(city)
        
        if isinstance(ciudades, dict) and 'error' in ciudades:
            return jsonify({"error": f"Error obteniendo datos de la ciudad: {ciudades['error']}"}), 400
        
        if not ciudades or len(ciudades) == 0:
            return jsonify({"error": "No se encontró la ciudad"}), 404
        
        # Usar la primera ciudad encontrada
        coordenadas = ciudades[0]
        lat = coordenadas["lat"]
        lon = coordenadas["lon"]
        
        # Obtener zona horaria
        timezone_info = obtener_zona_horaria(coordenadas, date)
        
        # Convertir fecha y hora local a UTC
        utc_datetime = convertir_a_utc(date, time, timezone_info)
        
        # Calcular posiciones planetarias
        positions = calculate_positions_with_skyfield(utc_datetime, lat, lon)
        
        # Si se requiere zodiaco sideral, aplicar la corrección Fagan-Allen
        if use_sidereal:
            for planet in positions:
                # Guardar longitud tropical original
                planet["tropical_longitude"] = planet["longitude"]
                # Ajustar la longitud restando el ayanamsa
                planet["longitude"] = (planet["longitude"] - FAGAN_ALLEN_AYANAMSA + 360) % 360
                # Actualizar el signo basado en la nueva longitud
                planet["sign"] = get_sign(planet["longitude"])
                # Recalcular dignidad basada en el nuevo signo
                planet["dignidad"] = calcular_dignidad_planetaria(planet["name"], planet["longitude"])
        
        # Calcular aspectos
        aspects = calculate_aspects(positions)
        
        # Determinar si el nacimiento es seco o húmedo
        sun_planet = next((p for p in positions if p["name"] == "SOL"), None)
        asc_planet = next((p for p in positions if p["name"] == "ASC"), None)
        
        is_dry = False
        if sun_planet and asc_planet:
            is_dry = is_dry_birth(sun_planet["longitude"], asc_planet["longitude"])
        
        # Preparar resultado
        result = {
            "positions": positions,
            "aspects": aspects,
            "isDry": is_dry,
            "zodiacSystem": "sidereal" if use_sidereal else "tropical",
            "coordinates": {"latitude": lat, "longitude": lon},
            "timezone": timezone_info
        }
        
        # Si se solicitó análisis avanzado, calcularlo
        if calculate_analysis:
            # Cálculo de enlaces planetarios
            enlaces = calcular_enlaces_planetarios(positions, aspects)
            result["enlaces"] = enlaces
            
            # Cálculo de picos
            pico_mayor = calcular_picos(positions, aspects, "MAYOR")
            pico_moderado = calcular_picos(positions, aspects, "MODERADO")
            pico_menor = calcular_picos(positions, aspects, "MENOR")
            
            result["pico_mayor"] = pico_mayor
            result["pico_moderado"] = pico_moderado
            result["pico_menor"] = pico_menor
            
            # Cálculo de liberación de enlace
            lib_enlace = calcular_liberacion_enlace(positions, aspects)
            result["liberacion_enlace"] = lib_enlace
            
            # Cálculo de presagios
            presagios = calcular_presagios(positions, aspects)
            result["presagios"] = presagios
            
        # Calcular posiciones de estrellas fijas si se solicita
        if include_stars:
            stars_positions = calculate_star_positions(date)
            star_aspects = calculate_star_aspects(stars_positions, positions)
            
            # Encontrar estrellas activas (en conjunción con planetas)
            active_stars = [
                {
                    "name": aspect["star"],
                    "longitude": stars_positions[aspect["star"]]["longitude"],
                    "sign": stars_positions[aspect["star"]]["sign"],
                    "effect": aspect["effect"],
                    "planet": aspect["planet"],
                    "angle": aspect["angle"]
                }
                for aspect in star_aspects
            ]
            
            # Añadir a la respuesta
            result["stars"] = {
                "positions": stars_positions,
                "aspects": star_aspects,
                "active_stars": active_stars
            }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error calculando carta: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error en el cálculo: {str(e)}"}), 500

# Funciones auxiliares para el análisis avanzado
def calcular_enlaces_planetarios(positions, aspects):
    """Calcula los enlaces entre planetas basados en aspectos y dignidades."""
    enlaces = []
    
    # Implementación simplificada
    for aspect in aspects:
        if aspect["type"] in ["CONJUNCTION", "TRINE", "SEXTILE"]:
            planet1 = aspect["planet1"]
            planet2 = aspect["planet2"]
            
            # Verificar si los planetas están en ENLACE_PLANETARIO
            if planet1 in ENLACE_PLANETARIO and planet2 in ENLACE_PLANETARIO:
                fortaleza = aspect["fuerza"]
                
                # Verificar si hay disolución
                disolucion = False
                if planet2 in ENLACE_PLANETARIO[planet1].get('neutraliza', []):
                    disolucion = True
                
                # Añadir enlace
                enlaces.append({
                    "planeta1": planet1,
                    "planeta2": planet2,
                    "fuerza": fortaleza,
                    "disolucion": disolucion
                })
    
    return enlaces

def calcular_picos(positions, aspects, tipo_pico):
    """Calcula los picos planetarios según el tipo especificado."""
    picos = []
    
    # Obtener condiciones para el tipo de pico
    condiciones = PICO_CONDICIONES.get(tipo_pico, {})
    dignidades_requeridas = condiciones.get('dignidad', [])
    aspectos_requeridos = condiciones.get('aspectos_requeridos', [])
    planetas_requeridos = condiciones.get('planetas_requeridos', [])
    min_fuerza = condiciones.get('min_fuerza', 0)
    
    # Filtrar planetas con las dignidades requeridas
    for planet in positions:
        if planet["name"] in planetas_requeridos and planet.get("dignidad") in dignidades_requeridas:
            # Buscar aspectos favorables
            planetas_aspectados = []
            
            for aspect in aspects:
                if aspect["type"] in aspectos_requeridos:
                    if aspect["planet1"] == planet["name"]:
                        planetas_aspectados.append(aspect["planet2"])
                    elif aspect["planet2"] == planet["name"]:
                        planetas_aspectados.append(aspect["planet1"])
            
            # Calcular fuerza
            fuerza_base = {
                'domicilio': 4,
                'exaltacion': 5,
                'peregrino': 2
            }.get(planet.get("dignidad", "peregrino"), 0)
            
            fuerza = fuerza_base + len(planetas_aspectados)
            
            if fuerza >= min_fuerza:
                picos.append({
                    "planeta": planet["name"],
                    "signo": planet["sign"],
                    "fuerza": fuerza,
                    "planetas_aspectados": planetas_aspectados
                })
    
    return picos

def calcular_liberacion_enlace(positions, aspects):
    """Calcula las liberaciones de enlaces entre planetas."""
    liberaciones = []
    
    # Para cada planeta que puede liberar
    for liberador, data in LIBERACION_ENLACE.items():
        liberados = data.get('libera', [])
        condicion = data.get('condicion', '')
        
        # Verificar si el liberador tiene aspectos que cumplen la condición
        for aspect in aspects:
            if aspect["type"] == condicion:
                if aspect["planet1"] == liberador and aspect["planet2"] in liberados:
                    liberaciones.append({
                        "planeta_liberador": liberador,
                        "planeta_liberado": aspect["planet2"],
                        "condicion": condicion
                    })
                elif aspect["planet2"] == liberador and aspect["planet1"] in liberados:
                    liberaciones.append({
                        "planeta_liberador": liberador,
                        "planeta_liberado": aspect["planet1"],
                        "condicion": condicion
                    })
    
    return liberaciones

def calcular_presagios(positions, aspects):
    """Calcula presagios buenos y malos basados en posiciones y aspectos."""
    presagios = {
        "buenos": [],
        "malos": []
    }
    
    # Presagios buenos
    condiciones_buenas = PRESAGIO_CONDICIONES.get('BUENO', {})
    planetas_buenos = condiciones_buenas.get('planetas', [])
    aspectos_buenos = condiciones_buenas.get('aspectos', [])
    signos_favorables = condiciones_buenas.get('signos_favorables', {})
    
    for planet in positions:
        if planet["name"] in planetas_buenos:
            signo = planet["sign"]
            
            # Verificar si el planeta está en un signo favorable
            if signo in signos_favorables.get(planet["name"], []):
                # Verificar si tiene aspectos favorables
                tiene_aspectos = False
                
                for aspect in aspects:
                    if aspect["type"] in aspectos_buenos:
                        if aspect["planet1"] == planet["name"] or aspect["planet2"] == planet["name"]:
                            tiene_aspectos = True
                            break
                
                presagios["buenos"].append({
                    "planeta": planet["name"],
                    "signo": signo,
                    "aspectos": tiene_aspectos
                })
    
    # Presagios malos (similar a los buenos)
    condiciones_malas = PRESAGIO_CONDICIONES.get('MALO', {})
    planetas_malos = condiciones_malas.get('planetas', [])
    aspectos_malos = condiciones_malas.get('aspectos', [])
    signos_desfavorables = condiciones_malas.get('signos_desfavorables', {})
    
    for planet in positions:
        if planet["name"] in planetas_malos:
            signo = planet["sign"]
            
            # Verificar si el planeta está en un signo desfavorable
            if signo in signos_desfavorables.get(planet["name"], []):
                # Verificar si tiene aspectos desfavorables
                tiene_aspectos = False
                
                for aspect in aspects:
                    if aspect["type"] in aspectos_malos:
                        if aspect["planet1"] == planet["name"] or aspect["planet2"] == planet["name"]:
                            tiene_aspectos = True
                            break
                
                presagios["malos"].append({
                    "planeta": planet["name"],
                    "signo": signo,
                    "aspectos": tiene_aspectos
                })
    
    return presagios

def calculate_star_positions(date):
    """
    Calcula las posiciones actuales de estrellas fijas ajustando por precesión.
    
    Args:
        date (str): Fecha en formato 'YYYY-MM-DD'
    
    Returns:
        dict: Diccionario de estrellas con posiciones ajustadas
    """
    try:
        # Convertir fecha a año decimal
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        year = date_obj.year + (date_obj.month - 1) / 12 + (date_obj.day - 1) / 365.25
        
        # Calcular años desde J2000 (1 enero 2000)
        years_since_j2000 = year - 2000.0
        
        # Calcular precesión total
        precession = ANNUAL_PRECESSION_RATE * years_since_j2000
        
        # Aplicar precesión a cada estrella
        stars_positions = {}
        for star in FIXED_STARS:
            current_longitude = (star["longitude_J2000"] + precession) % 360
            
            # Determinar el signo actual
            sign = get_sign(current_longitude)
            
            stars_positions[star["name"]] = {
                "longitude": current_longitude,
                "sign": sign,
                "effect": star["effect"],
                "magnitude": star.get("magnitude", 6)
            }
            
        return stars_positions
    except Exception as e:
        print(f"Error calculando posiciones de estrellas: {str(e)}")
        return {}

def calculate_star_aspects(stars_positions, planet_positions, orb=1.0):
    """
    Calcula aspectos entre estrellas fijas y planetas
    
    Args:
        stars_positions (dict): Posiciones de estrellas fijas
        planet_positions (list): Posiciones de planetas
        orb (float): Orbe máximo para considerar conjunción
    
    Returns:
        list: Lista de aspectos entre estrellas y planetas
    """
    aspects = []
    
    for star_name, star_data in stars_positions.items():
        star_longitude = star_data["longitude"]
        star_magnitude = star_data.get("magnitude", 6)
        
        # Ajustar orbe según magnitud de la estrella
        aspect_orb = 2.0 if star_magnitude >= 12 else orb
        
        for planet in planet_positions:
            planet_longitude = planet["longitude"]
            
            # Calcular diferencia angular
            diff = abs(star_longitude - planet_longitude)
            if diff > 180:
                diff = 360 - diff
                
            # Verificar si hay conjunción
            if diff <= aspect_orb:
                aspects.append({
                    "star": star_name,
                    "planet": planet["name"],
                    "type": "Conjunción",
                    "angle": diff,
                    "effect": star_data["effect"]
                })
                
    return aspects

@app.route('/open-file')
def open_file():
    try:
        file_path = request.args.get('path')

        # Si es una URL, devolverla directamente para que JavaScript la abra
        if file_path and file_path.startswith("https://"):
            return jsonify({"url": file_path})

        # Si es un archivo local, verificar existencia y enviarlo
        if file_path and os.path.exists(file_path):
            return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))

        return jsonify({'error': 'Archivo no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/star_interpretation', methods=['GET'])
def get_star_interpretation():
    star_name = request.args.get('name')
    if not star_name:
        return jsonify({"error": "Nombre de estrella no especificado"}), 400
        
    interpretation = STAR_INTERPRETATIONS.get(star_name)
    if not interpretation:
        return jsonify({"error": f"No se encontró interpretación para {star_name}"}), 404
        
    return jsonify(interpretation)

# Para servir el archivo index.html en la ruta raíz
@app.route('/')
def serve_index():
    return send_file('index.html')

# Para servir el favicon específicamente
@app.route('/favicon.png')
def favicon():
    return send_file('favicon.png')

# Para servir cualquier otro archivo estático
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_file(path)
    except:
        return "File not found", 404

# Iniciar la aplicación
if __name__ == "__main__":
    # Precargar recursos
    preload_resources()
    
    # Obtener puerto del entorno o usar 10000 por defecto
    port = int(os.environ.get("PORT", 10000))
    
    # Iniciar la aplicación
    app.run(host="0.0.0.0", port=port)
handleCitySearch  