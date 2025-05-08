import json
import sys
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

# Importaciones opcionales
try:
    from flask_compress import Compress
    COMPRESS_AVAILABLE = True
except ImportError:
    COMPRESS_AVAILABLE = False
    print("ADVERTENCIA: flask_compress no está instalado. La compresión está desactivada.")

try:
    from flask_caching import Cache
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False
    print("ADVERTENCIA: flask_caching no está instalado. El caché está desactivado.")

from datetime import datetime, timezone, timedelta

# Importaciones opcionales para cálculos astronómicos
try:
    from skyfield.api import load, wgs84
    import numpy as np
    SKYFIELD_AVAILABLE = True
    print("Skyfield disponible para cálculos astronómicos precisos")
except ImportError:
    SKYFIELD_AVAILABLE = False
    print("ADVERTENCIA: Skyfield no está instalado. Se usarán cálculos aproximados.")

import os
from pathlib import Path
from functools import lru_cache
import requests
import math

app = Flask(__name__)
# Configurar CORS correctamente
CORS(app, resources={r"/*": {"origins": "*"}})
# Comprimir respuestas si está disponible
if COMPRESS_AVAILABLE:
    Compress(app)
# Configurar caché si está disponible
if CACHE_AVAILABLE:
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Variables globales para recursos precargados
eph = None
ts = None
interpreter = None
time_zone_df = None

API_KEY = "e19afa2a9d6643ea9550aab89eefce0b"

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

FAGAN_ALLEN_AYANAMSA = 24.25  # Valor exacto del Ayanamsa Fagan-Allen en 2025 (24° 15')

# Nuevas constantes para dignidades planetarias
DIGNIDADES = {
    'SOL': {
        'domicilio': ['ESCORPIO', 'GÉMINIS', 'PEGASO'], 
        'exaltacion': ['LEO', 'ARIES', 'CAPRICORNIO', 'VIRGO'], 
        'caida': ['CÁNCER', 'PISCIS', 'LIBRA', 'ACUARIO', 'OFIUCO'], 
        'exilio': ['TAURO', 'SAGITARIO']
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
    'JÚPITER': {
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
        'caida': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO'],
        'exilio': ['CÁNCER', 'PISCIS', 'SAGITARIO']
    },
    'NEPTUNO': {
        'domicilio': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO'], 
        'exaltacion': ['CÁNCER', 'PISCIS', 'SAGITARIO'], 
        'caida': ['LEO', 'ARIES', 'ESCORPIO', 'PEGASO'], 
        'exilio': ['GÉMINIS', 'CAPRICORNIO', 'VIRGO']
    },
    'PLUTÓN': {
        'domicilio': ['GÉMINIS', 'CAPRICORNIO', 'VIRGO'], 
        'exaltacion': ['LEO', 'ARIES', 'ESCORPIO', 'PEGASO'], 
        'caida': ['CÁNCER', 'PISCIS', 'SAGITARIO'], 
        'exilio': ['TAURO', 'LIBRA', 'ACUARIO', 'OFIUCO']
    }
}

# Precarga de recursos al inicio
def preload_resources():
    global eph, ts, interpreter, time_zone_df
    
    print("Precargando recursos...")
    
    # Cargar efemérides desde archivo si Skyfield está disponible
    if SKYFIELD_AVAILABLE:
        try:
            # Cargar desde archivo local
            eph_path = Path('de421.bsp')
            if not eph_path.exists():
                # Intentar cargar desde la carpeta docs
                eph_path = Path('docs') / 'de421.bsp'
            
            print(f"Cargando efemérides desde: {eph_path}")
            eph = load(str(eph_path))
            ts = load.timescale()
            print("Efemérides cargadas correctamente")
        except Exception as e:
            print(f"Error cargando efemérides: {e}")
            # No usar Skyfield si hay error con las efemérides
            global SKYFIELD_AVAILABLE
            SKYFIELD_AVAILABLE = False
    
    # Cargar zona horaria si se encuentra el archivo
    try:
        import csv
        time_zone_df = []
        
        # Buscar archivo de zonas horarias en múltiples ubicaciones
        possible_paths = ['time_zone.csv', './docs/time_zone.csv', '../time_zone.csv']
        csv_path = None
        
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if csv_path:
            with open(csv_path, 'r') as csv_file:
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
        else:
            print("Archivo de zonas horarias no encontrado, se usarán estimaciones")
    except Exception as e:
        print(f"Error cargando zonas horarias: {e}")
        time_zone_df = []
    
    # Cargar intérprete con XML si existe
    try:
        xml_paths = ['interpretations.xml', './docs/interpretations.xml', '../interpretations.xml']
        xml_path = None
        
        for path in xml_paths:
            if os.path.exists(path):
                xml_path = path
                break
        
        if xml_path:
            interpreter = AstrologicalInterpreter(xml_path)
            print("Intérprete astrológico cargado correctamente")
        else:
            print("Archivo XML de interpretaciones no encontrado")
    except Exception as e:
        print(f"Error cargando intérprete: {e}")
        interpreter = None
    
    print("Recursos precargados correctamente")

class AstrologicalInterpreter:
    def __init__(self, xml_path='interpretations.xml'):
        try:
            import xml.etree.ElementTree as ET
            self.tree = ET.parse(xml_path)
            self.root = self.tree.getroot()
            print(f"XML de interpretaciones cargado desde {xml_path}")
        except Exception as e:
            print(f"Error al cargar el archivo XML: {e}")
            # No lanzar excepción, solo reportar el error
            self.root = None

    def get_planet_in_sign(self, planet, sign):
        try:
            if not self.root:
                return None
                
            xpath = f".//PLANET_IN_SIGN14/{planet}/{sign}"
            planet_element = self.root.find(xpath)
            
            if planet_element is not None:
                full_text = planet_element.text.strip() if planet_element.text else ""
                physical_desc = ""
                astral_desc = ""
                
                split_text = full_text.split("En el plano Astral", 1)
                
                if len(split_text) > 0:
                    physical_desc = split_text[0].strip()
                if len(split_text) > 1:
                    astral_desc = "En el plano Astral" + split_text[1].strip()
                
                return {
                    "physical": physical_desc,
                    "astral": astral_desc
                }
            return None
        except Exception as e:
            print(f"Error en get_planet_in_sign: {e}")
            return None

    def get_planet_in_house(self, planet, house):
        try:
            if not self.root:
                return None
                
            house_str = f"HS{house}"
            xpath = f".//PLANET_IN_12HOUSE/{planet}/{house_str}"
            house_element = self.root.find(xpath)
            
            if house_element is not None and house_element.text:
                return house_element.text.strip()
            return None
        except Exception as e:
            print(f"Error en get_planet_in_house: {e}")
            return None

    def get_aspect_interpretation(self, planet1, planet2, aspect_type):
        try:
            if not self.root:
                return None
                
            aspect_angles = {
                "Armónico Relevante": ["0", "60", "120", "180"],
                "Inarmónico Relevante": ["90", "150"],
                "Armónico": ["12", "24", "36", "48", "72", "84", "96", "108", "132", "144", "156", "168"],
                "Inarmónico": ["6", "18", "42", "54", "66", "78", "102", "114", "126", "138", "162", "174"]
            }
            
            for angles in aspect_angles[aspect_type]:
                xpath = f".//PLANET_IN_ASPECT/{planet1}/{planet2}/ASP_{angles}"
                aspect_element = self.root.find(xpath)
                
                if aspect_element is not None and aspect_element.text:
                    return aspect_element.text.strip()
                
                xpath = f".//PLANET_IN_ASPECT/{planet2}/{planet1}/ASP_{angles}"
                aspect_element = self.root.find(xpath)
                
                if aspect_element is not None and aspect_element.text:
                    return aspect_element.text.strip()
            
            return None
        except Exception as e:
            print(f"Error en get_aspect_interpretation: {e}")
            return None

    def get_house_ruler_interpretation(self, ruler_house, house_position):
        try:
            if not self.root:
                return None
                
            xpath = f".//HRULER_IN_HOUSE/RH{ruler_house}/HS{house_position}"
            ruler_element = self.root.find(xpath)
            
            if ruler_element is not None and ruler_element.text:
                return ruler_element.text.strip()
            return None
        except Exception as e:
            print(f"Error en get_house_ruler_interpretation: {e}")
            return None

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
    Obtiene la zona horaria estimada basada en las coordenadas
    """
    try:
        lat = coordenadas["lat"]
        lon = coordenadas["lon"]
        
        # Estimación básica basada en longitud
        estimated_offset = round(lon / 15)  # 15 grados = 1 hora
        
        # Ajustar para países específicos con información conocida
        pais = coordenadas.get("pais", "").lower()
        
        if "spain" in pais or "españa" in pais:
            offset = 1
            abbr = "CET"
            is_dst = determinar_horario_verano_simplificado(fecha, "norte", pais)
            if is_dst:
                offset = 2
                abbr = "CEST"
        elif "argentina" in pais:
            offset = -3
            abbr = "ART"
            is_dst = False
        elif "mexico" in pais or "méxico" in pais:
            offset = -6
            abbr = "CST"
            is_dst = determinar_horario_verano_simplificado(fecha, "norte", pais)
            if is_dst:
                offset = -5
                abbr = "CDT"
        else:
            offset = estimated_offset
            abbr = f"GMT{offset:+d}"
            is_dst = False
        
        return {
            "name": f"GMT{offset:+d}",
            "offset": offset,
            "abbreviation_STD": abbr,
            "abbreviation_DST": abbr,
            "is_dst": is_dst,
            "hemisphere": "norte" if lat >= 0 else "sur"
        }
    
    except Exception as e:
        print(f"Error obteniendo zona horaria: {str(e)}")
        return {
            "name": "UTC",
            "offset": 0,
            "abbreviation_STD": "UTC",
            "abbreviation_DST": "UTC",
            "is_dst": False,
            "hemisphere": "norte",
            "estimated": True
        }

def determinar_horario_verano_simplificado(fecha, hemisferio, pais):
    """Versión simplificada para determinar horario de verano"""
    try:
        # Convertir la fecha a objeto datetime si es string
        if isinstance(fecha, str):
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        else:
            fecha_obj = fecha
            
        mes = fecha_obj.month
        
        # Regla simplificada para Europa
        if "spain" in pais or "europa" in pais:
            # Europa: verano desde finales de marzo hasta finales de octubre
            return 3 <= mes <= 10
        
        # Regla general por hemisferio
        if hemisferio == "norte":
            # Hemisferio Norte: verano de marzo a octubre
            return 3 <= mes <= 10
        else:
            # Hemisferio Sur: verano de octubre a marzo
            return mes >= 10 or mes <= 3
    except:
        # En caso de error, devolver False por defecto
        return False

def convertir_a_utc(fecha, hora, timezone_info):
    """
    Convierte fecha y hora local a UTC considerando zona horaria
    """
    try:
        # Combinar fecha y hora en un objeto datetime
        fecha_hora_str = f"{fecha} {hora}"
        dt_local = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")
        
        # Obtener offset en horas
        offset_hours = timezone_info["offset"]
        
        # Crear un timezone con el offset
        tz = timezone(timedelta(hours=offset_hours))
        
        # Aplicar timezone al datetime
        dt_local_with_tz = dt_local.replace(tzinfo=tz)
        
        # Convertir a UTC
        dt_utc = dt_local_with_tz.astimezone(timezone.utc)
        
        return dt_utc
    except Exception as e:
        print(f"Error en conversión a UTC: {str(e)}")
        # Si falla, usar la hora proporcionada como UTC
        dt_local = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        return dt_local.replace(tzinfo=timezone.utc)

def calculate_positions_with_utc(utc_datetime, lat=None, lon=None, use_sidereal=False):
    """
    Calcula posiciones planetarias con un datetime UTC
    """
    if SKYFIELD_AVAILABLE:
        try:
            return calculate_positions_with_skyfield(utc_datetime, lat, lon, use_sidereal)
        except Exception as e:
            print(f"Error en cálculo con Skyfield: {e}")
    
    # Fallback a cálculos aproximados si Skyfield no está disponible o falla
    return calculate_positions_with_approximation(utc_datetime, lat, lon, use_sidereal)

def calculate_positions_with_skyfield(utc_datetime, lat=None, lon=None, use_sidereal=False):
    """Calcula posiciones con Skyfield (preciso)"""
    print(f"Calculando posiciones con Skyfield para UTC: {utc_datetime}")
    
    # Preparar tiempo para Skyfield
    t = ts.from_datetime(utc_datetime)
    
    # Para calcular movimientos retrógrados, necesitamos puntos adyacentes en el tiempo
    t_before = ts.from_datetime(utc_datetime - timedelta(days=1))  # Un día antes
    t_after = ts.from_datetime(utc_datetime + timedelta(days=1))   # Un día después
    
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
        # Posición actual
        pos = earth.at(t).observe(body).apparent()
        lat_ecl, lon_ecl, dist = pos.ecliptic_latlon(epoch='date')
        
        # Obtener longitud tropical
        longitude = float(lon_ecl.degrees) % 360
        
        # Si se requiere zodiaco sideral, aplicar corrección
        if use_sidereal:
            # Guardar la longitud tropical
            tropical_longitude = longitude
            # Ajustar por el ayanamsa Fagan-Allen
            longitude = (longitude - FAGAN_ALLEN_AYANAMSA + 360) % 360
        
        # Calcular posiciones para determinar el movimiento
        pos_before = earth.at(t_before).observe(body).apparent()
        lat_before, lon_before, dist_before = pos_before.ecliptic_latlon(epoch='date')
        longitude_before = float(lon_before.degrees) % 360
        
        if use_sidereal:
            # Aplicar corrección sideral
            longitude_before = (longitude_before - FAGAN_ALLEN_AYANAMSA + 360) % 360
        
        pos_after = earth.at(t_after).observe(body).apparent()
        lat_after, lon_after, dist_after = pos_after.ecliptic_latlon(epoch='date')
        longitude_after = float(lon_after.degrees) % 360
        
        if use_sidereal:
            # Aplicar corrección sideral
            longitude_after = (longitude_after - FAGAN_ALLEN_AYANAMSA + 360) % 360
        
        # Calcular movimiento diario
        daily_motion_before = (longitude - longitude_before) % 360
        if daily_motion_before > 180:
            daily_motion_before = daily_motion_before - 360
            
        daily_motion_after = (longitude_after - longitude) % 360
        if daily_motion_after > 180:
            daily_motion_after = daily_motion_after - 360
        
        # Determinar estado retrógrado
        motion_status = "direct"  # Valor por defecto
        
        # El Sol y la Luna nunca son retrógrados geocéntricamente
        if body_name not in ['SOL', 'LUNA']:
            # Comprobar movimiento retrógrado (movimiento diario negativo)
            if daily_motion_before < 0 and daily_motion_after < 0:
                motion_status = "retrograde"
            # Comprobar estacionario retrógrado
            elif daily_motion_before >= 0 and daily_motion_after < 0:
                motion_status = "stationary_retrograde"
            # Comprobar estacionario directo
            elif daily_motion_before < 0 and daily_motion_after >= 0:
                motion_status = "stationary_direct"
            
            # Comprobar movimiento muy lento (casi estacionario)
            if abs(daily_motion_before) < 0.1 or abs(daily_motion_after) < 0.1:
                if motion_status == "retrograde":
                    motion_status = "stationary_retrograde"
                elif motion_status == "direct":
                    motion_status = "stationary_direct"
        
        # Obtener el signo
        sign = get_sign(longitude)
        
        # Calcular dignidad basada en el signo
        dignidad = calcular_dignidad_planetaria(body_name, sign)
        
        # Crear el objeto con los datos del planeta
        planet_data = {
            "name": body_name,
            "longitude": longitude,
            "sign": sign,
            "dignidad": dignidad,
            "motion_status": motion_status,
            "daily_motion": (daily_motion_before + daily_motion_after) / 2  # Movimiento diario promedio
        }
        
        # Añadir longitud tropical si se está usando el zodiaco sideral
        if use_sidereal:
            planet_data["tropical_longitude"] = tropical_longitude
            planet_data["tropical_sign"] = get_sign(tropical_longitude)
        
        positions.append(planet_data)
    
    # Calcular ASC, MC y puntos derivados si se proporcionaron coordenadas
    if lat is not None and lon is not None:
        asc, mc = calculate_asc_mc_skyfield(t, lat, lon)
        
        # Ajustar ASC y MC si se usa sideral
        if use_sidereal:
            tropical_asc = asc
            tropical_mc = mc
            asc = (asc - FAGAN_ALLEN_AYANAMSA + 360) % 360
            mc = (mc - FAGAN_ALLEN_AYANAMSA + 360) % 360
        
        positions.append({
            "name": "ASC",
            "longitude": float(asc),
            "sign": get_sign(asc),
            "motion_status": "direct", # ASC siempre es directo
            **({"tropical_longitude": tropical_asc, "tropical_sign": get_sign(tropical_asc)} if use_sidereal else {})
        })
        
        positions.append({
            "name": "MC",
            "longitude": float(mc),
            "sign": get_sign(mc),
            "motion_status": "direct", # MC siempre es directo
            **({"tropical_longitude": tropical_mc, "tropical_sign": get_sign(tropical_mc)} if use_sidereal else {})
        })
        
        # Añadir Descendente (opuesto al ascendente)
        desc = (asc + 180) % 360
        positions.append({
            "name": "DSC",
            "longitude": float(desc),
            "sign": get_sign(desc),
            "motion_status": "direct",
            **({"tropical_longitude": (tropical_asc + 180) % 360, "tropical_sign": get_sign((tropical_asc + 180) % 360)} if use_sidereal else {})
        })
        
        # Añadir Imum Coeli (IC) (opuesto al MC)
        ic = (mc + 180) % 360
        positions.append({
            "name": "IC",
            "longitude": float(ic),
            "sign": get_sign(ic),
            "motion_status": "direct",
            **({"tropical_longitude": (tropical_mc + 180) % 360, "tropical_sign": get_sign((tropical_mc + 180) % 360)} if use_sidereal else {})
        })
        
        # Calcular y añadir Parte de Fortuna y Parte de Espíritu
        sol_planet = next((p for p in positions if p["name"] == "SOL"), None)
        luna_planet = next((p for p in positions if p["name"] == "LUNA"), None)
        
        if sol_planet and luna_planet:
            # Determinar si es carta diurna o nocturna
            is_dry = is_dry_birth(sol_planet["longitude"], asc)
            
            # Cálculo de Parte de Fortuna según el tipo de nacimiento
            if is_dry:  # Nacimiento diurno
                dist_sol_a_luna = (luna_planet["longitude"] - sol_planet["longitude"]) % 360
                parte_fortuna = (asc + dist_sol_a_luna) % 360
            else:  # Nacimiento nocturno
                dist_luna_a_sol = (sol_planet["longitude"] - luna_planet["longitude"]) % 360
                parte_fortuna = (asc + dist_luna_a_sol) % 360
            
            positions.append({
                "name": "PARTE_FORTUNA",
                "longitude": float(parte_fortuna),
                "sign": get_sign(parte_fortuna),
                "motion_status": "direct",
                **({"tropical_longitude": parte_fortuna, "tropical_sign": get_sign(parte_fortuna)} if use_sidereal else {})
            })
            
            # Cálculo de Parte de Espíritu (inverso lógico de la Parte de Fortuna)
            if is_dry:  # Nacimiento diurno
                dist_luna_a_sol = (sol_planet["longitude"] - luna_planet["longitude"]) % 360
                parte_espiritu = (asc + dist_luna_a_sol) % 360
            else:  # Nacimiento nocturno
                dist_sol_a_luna = (luna_planet["longitude"] - sol_planet["longitude"]) % 360
                parte_espiritu = (asc + dist_sol_a_luna) % 360
            
            positions.append({
                "name": "PARTE_ESPIRITU",
                "longitude": float(parte_espiritu),
                "sign": get_sign(parte_espiritu),
                "motion_status": "direct",
                **({"tropical_longitude": parte_espiritu, "tropical_sign": get_sign(parte_espiritu)} if use_sidereal else {})
            })
    
    return positions

def calculate_positions_with_approximation(utc_datetime, lat=None, lon=None, use_sidereal=False):
    """Método alternativo para calcular posiciones planetarias (aproximado)"""
    print("Usando cálculos aproximados para posiciones planetarias")
    try:
        # Simulación simple de posiciones planetarias
        # Basado en tasas medias de movimiento y ciclos
        
        # Obtener días transcurridos desde J2000
        j2000 = datetime(2000, 1, 1, 12, 0).replace(tzinfo=timezone.utc)
        days_since_j2000 = (utc_datetime - j2000).total_seconds() / 86400.0
        
        positions = []
        
        # Posiciones iniciales aproximadas en J2000 (eclíptica tropical)
        base_positions = {
            "SOL": 279.0, 
            "LUNA": 134.0,
            "MERCURIO": 268.0,
            "VENUS": 285.0,
            "MARTE": 94.0,
            "JÚPITER": 316.0,
            "SATURNO": 223.0,
            "URANO": 312.0,
            "NEPTUNO": 295.0,
            "PLUTÓN": 232.0
        }
        
        # Tasas medias de movimiento (grados por día)
        daily_rates = {
            "SOL": 0.9856,
            "LUNA": 13.1764,
            "MERCURIO": 4.0923,
            "VENUS": 1.6021,
            "MARTE": 0.5240,
            "JÚPITER": 0.0830,
            "SATURNO": 0.0334,
            "URANO": 0.0117,
            "NEPTUNO": 0.0060,
            "PLUTÓN": 0.0040
        }
        
        # Calculamos el movimiento retrógrado basado en posiciones relativas
        # Mercurio: retrógrado aproximadamente cada 116 días
        # Venus: retrógrado aproximadamente cada 584 días
        # Marte: retrógrado aproximadamente cada 780 días
        # Júpiter: retrógrado aproximadamente cada 399 días
        # Saturno: retrógrado aproximadamente cada 378 días
        # Urano: retrógrado aproximadamente cada 369 días
        # Neptuno: retrógrado aproximadamente cada 367 días
        # Plutón: retrógrado aproximadamente cada 366 días
        retrograde_cycles = {
            "MERCURIO": 116,
            "VENUS": 584,
            "MARTE": 780,
            "JÚPITER": 399,
            "SATURNO": 378,
            "URANO": 369,
            "NEPTUNO": 367,
            "PLUTÓN": 366
        }
        
        # Duración aproximada del período retrógrado en días
        retrograde_duration = {
            "MERCURIO": 22,
            "VENUS": 42,
            "MARTE": 80,
            "JÚPITER": 120,
            "SATURNO": 140,
            "URANO": 155,
            "NEPTUNO": 158,
            "PLUTÓN": 160
        }
        
        for planet_name, initial_position in base_positions.items():
            # Calcular posición actualizada
            rate = daily_rates.get(planet_name, 0)
            
            # Calcular posición tropical básica
            longitude = (initial_position + rate * days_since_j2000) % 360
            
            # Determinar estado de movimiento
            motion_status = "direct"  # Por defecto
            
            # Sol y Luna nunca son retrógrados geocéntricamente
            if planet_name not in ["SOL", "LUNA"]:
                cycle = retrograde_cycles.get(planet_name, 0)
                duration = retrograde_duration.get(planet_name, 0)
                
                if cycle > 0:
                    # Determinar fase en el ciclo
                    cycle_phase = (days_since_j2000 % cycle) / cycle
                    
                    # La retrogradación ocurre en la mitad del ciclo
                    if abs(cycle_phase - 0.5) * cycle <= duration/2:
                        motion_status = "retrograde"
                    # Estado estacionario cerca del cambio de dirección
                    elif abs(cycle_phase - (0.5 - duration/(2*cycle))) * cycle <= 3:
                        motion_status = "stationary_retrograde"
                    elif abs(cycle_phase - (0.5 + duration/(2*cycle))) * cycle <= 3:
                        motion_status = "stationary_direct"
            
            # Si se requiere zodiaco sideral, aplicar corrección
            if use_sidereal:
                tropical_longitude = longitude
                longitude = (longitude - FAGAN_ALLEN_AYANAMSA + 360) % 360
            
            # Obtener el signo correspondiente
            sign = get_sign(longitude)
            
            # Calcular dignidad planetaria
            dignidad = calcular_dignidad_planetaria(planet_name, sign)
            
            # Crear objeto del planeta
            planet_data = {
                "name": planet_name,
                "longitude": longitude,
                "sign": sign,
                "dignidad": dignidad,
                "motion_status": motion_status
            }
            
            # Añadir datos tropicales si es sideral
            if use_sidereal:
                planet_data["tropical_longitude"] = tropical_longitude
                planet_data["tropical_sign"] = get_sign(tropical_longitude)
            
            positions.append(planet_data)
        
        # Calcular puntos cardinales si tenemos coordenadas
        if lat is not None and lon is not None:
            # Cálculo aproximado del ASC y MC
            asc, mc = calculate_asc_mc_approximation(utc_datetime, lat, lon)
            
            # Ajustar para zodiaco sideral si es necesario
            if use_sidereal:
                tropical_asc = asc
                tropical_mc = mc
                asc = (asc - FAGAN_ALLEN_AYANAMSA + 360) % 360
                mc = (mc - FAGAN_ALLEN_AYANAMSA + 360) % 360
            
            # Añadir ASC y MC a las posiciones
            positions.append({
                "name": "ASC",
                "longitude": asc,
                "sign": get_sign(asc),
                "motion_status": "direct",
                **({"tropical_longitude": tropical_asc, "tropical_sign": get_sign(tropical_asc)} if use_sidereal else {})
            })
            
            positions.append({
                "name": "MC",
                "longitude": mc,
                "sign": get_sign(mc),
                "motion_status": "direct",
                **({"tropical_longitude": tropical_mc, "tropical_sign": get_sign(tropical_mc)} if use_sidereal else {})
            })
            
            # Añadir DSC e IC (opuestos a ASC y MC)
            positions.append({
                "name": "DSC",
                "longitude": (asc + 180) % 360,
                "sign": get_sign((asc + 180) % 360),
                "motion_status": "direct",
                **({"tropical_longitude": (tropical_asc + 180) % 360, "tropical_sign": get_sign((tropical_asc + 180) % 360)} if use_sidereal else {})
            })
            
            positions.append({
                "name": "IC",
                "longitude": (mc + 180) % 360,
                "sign": get_sign((mc + 180) % 360),
                "motion_status": "direct",
                **({"tropical_longitude": (tropical_mc + 180) % 360, "tropical_sign": get_sign((tropical_mc + 180) % 360)} if use_sidereal else {})
            })
            
            # Calcular Parte de Fortuna y Parte de Espíritu
            sol_planet = next((p for p in positions if p["name"] == "SOL"), None)
            luna_planet = next((p for p in positions if p["name"] == "LUNA"), None)
            
            if sol_planet and luna_planet and asc:
                # Determinar si es carta diurna o nocturna
                is_dry = is_dry_birth(sol_planet["longitude"], asc)
                
                # Cálculo de Parte de Fortuna según el tipo de nacimiento
                if is_dry:  # Nacimiento diurno
                    dist_sol_a_luna = (luna_planet["longitude"] - sol_planet["longitude"]) % 360
                    parte_fortuna = (asc + dist_sol_a_luna) % 360
                else:  # Nacimiento nocturno
                    dist_luna_a_sol = (sol_planet["longitude"] - luna_planet["longitude"]) % 360
                    parte_fortuna = (asc + dist_luna_a_sol) % 360
                
                positions.append({
                    "name": "PARTE_FORTUNA",
                    "longitude": float(parte_fortuna),
                    "sign": get_sign(parte_fortuna),
                    "motion_status": "direct",
                    **({"tropical_longitude": parte_fortuna, "tropical_sign": get_sign(parte_fortuna)} if use_sidereal else {})
                })
                
                # Cálculo de Parte de Espíritu (inverso lógico de la Parte de Fortuna)
                if is_dry:  # Nacimiento diurno
                    dist_luna_a_sol = (sol_planet["longitude"] - luna_planet["longitude"]) % 360
                    parte_espiritu = (asc + dist_luna_a_sol) % 360
                else:  # Nacimiento nocturno
                    dist_sol_a_luna = (luna_planet["longitude"] - sol_planet["longitude"]) % 360
                    parte_espiritu = (asc + dist_sol_a_luna) % 360
                
                positions.append({
                    "name": "PARTE_ESPIRITU",
                    "longitude": float(parte_espiritu),
                    "sign": get_sign(parte_espiritu),
                    "motion_status": "direct",
                    **({"tropical_longitude": parte_espiritu, "tropical_sign": get_sign(parte_espiritu)} if use_sidereal else {})
                })
        
        return positions
    except Exception as e:
        print(f"Error en calculate_positions_with_approximation: {e}")
        # Si todo falla, devolver un conjunto mínimo de posiciones simuladas
        return [
            {"name": "SOL", "longitude": 120, "sign": "LEO", "motion_status": "direct", "dignidad": "exaltacion"},
            {"name": "LUNA", "longitude": 186, "sign": "LIBRA", "motion_status": "direct", "dignidad": "exaltacion"},
            {"name": "MERCURIO", "longitude": 135, "sign": "LEO", "motion_status": "direct", "dignidad": "domicilio"},
            {"name": "VENUS", "longitude": 90, "sign": "CÁNCER", "motion_status": "direct", "dignidad": "domicilio"},
            {"name": "MARTE", "longitude": 210, "sign": "ESCORPIO", "motion_status": "retrograde", "dignidad": "exaltacion"},
            {"name": "JÚPITER", "longitude": 270, "sign": "CAPRICORNIO", "motion_status": "direct", "dignidad": "exilio"},
            {"name": "SATURNO", "longitude": 330, "sign": "PISCIS", "motion_status": "retrograde", "dignidad": "exilio"},
            {"name": "URANO", "longitude": 30, "sign": "TAURO", "motion_status": "direct", "dignidad": "caida"},
            {"name": "NEPTUNO", "longitude": 354, "sign": "ARIES", "motion_status": "retrograde", "dignidad": "caida"},
            {"name": "PLUTÓN", "longitude": 252, "sign": "SAGITARIO", "motion_status": "direct", "dignidad": "caida"},
            {"name": "ASC", "longitude": 0, "sign": "ARIES", "motion_status": "direct"},
            {"name": "MC", "longitude": 270, "sign": "CAPRICORNIO", "motion_status": "direct"},
            {"name": "DSC", "longitude": 180, "sign": "LIBRA", "motion_status": "direct"},
            {"name": "IC", "longitude": 90, "sign": "CÁNCER", "motion_status": "direct"},
            {"name": "PARTE_FORTUNA", "longitude": 306, "sign": "ACUARIO", "motion_status": "direct"},
            {"name": "PARTE_ESPIRITU", "longitude": 60, "sign": "GÉMINIS", "motion_status": "direct"}
        ]

def calculate_asc_mc_skyfield(t, lat, lon):
    """Calcula Ascendente y Medio Cielo con Skyfield"""
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
        print(f"Error en calculate_asc_mc_skyfield: {e}")
        # Valores por defecto en caso de error
        return 0, 270

def calculate_asc_mc_approximation(utc_datetime, lat, lon):
    """Cálculo aproximado de Ascendente y Medio Cielo"""
    try:
        # Tiempo sideral Greenwich en grados
        # Fórmula simplificada para GST
        j2000 = datetime(2000, 1, 1, 12, 0).replace(tzinfo=timezone.utc)
        days_since_j2000 = (utc_datetime - j2000).total_seconds() / 86400.0
        
        # T = siglos julianos desde J2000
        T = days_since_j2000 / 36525.0
        
        # GST en grados (aproximación)
        GST = 280.46061837 + 360.98564736629 * days_since_j2000 + 0.000387933 * T * T - T * T * T / 38710000.0
        GST = GST % 360
        
        # Tiempo sideral local
        LST = (GST + lon) % 360
        
        # Medio Cielo (MC) es directamente el LST
        MC = LST
        
        # Cálculo aproximado del Ascendente
        # Usar una fórmula simplificada
        lat_rad = math.radians(lat)
        lst_rad = math.radians(LST)
        obl_rad = math.radians(23.4367)  # Oblicuidad de la eclíptica (aproximada)
        
        # Fórmula para calcular el Ascendente
        tan_asc = -math.cos(lst_rad) / (math.sin(lst_rad) * math.cos(obl_rad) + math.tan(lat_rad) * math.sin(obl_rad))
        ASC = math.degrees(math.atan(tan_asc))
        
        # Ajustar cuadrante
        if 0 <= LST <= 180:
            if math.cos(lst_rad) > 0:
                ASC = (ASC + 180) % 360
        else:
            if math.cos(lst_rad) < 0:
                ASC = (ASC + 180) % 360
        
        ASC = ASC % 360
        
        return ASC, MC
    except Exception as e:
        print(f"Error en calculate_asc_mc_approximation: {e}")
        # Valores predeterminados si falla el cálculo
        return 0, 270

def get_sign(longitude):
    """Determina el signo zodiacal basado en la longitud eclíptica"""
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

def calcular_dignidad_planetaria(planeta, signo):
    """Calcula la dignidad planetaria basada en el signo"""
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
    return "peregrino"

def calculate_positions_aspects(positions):
    """Calcula aspectos entre posiciones planetarias"""
    aspects = []
    traditional_planets = ["SOL", "LUNA", "MERCURIO", "VENUS", "MARTE", "JÚPITER", "SATURNO"]
    
    def calculate_angle(pos1, pos2):
        diff = abs(pos1 - pos2) % 360
        if diff > 180:
            diff = 360 - diff
        return diff
    
    def determine_aspect_type(angle):
        orb = 2
        
        if (abs(angle) <= orb or 
            abs(angle - 60) <= orb or 
            abs(angle - 120) <= orb or
            abs(angle - 180) <= orb):
            return "Armónico Relevante"
        elif (abs(angle - 30) <= orb or
              abs(angle - 90) <= orb or
              abs(angle - 150) <= orb):
            return "Inarmónico Relevante"
        elif any(abs(angle - a) <= orb for a in [12, 24, 36, 48, 72, 84, 96, 108, 132, 144, 156, 168]):
            return "Armónico"
        elif any(abs(angle - a) <= orb for a in [6, 18, 42, 54, 66, 78, 102, 114, 126, 138, 162, 174]):
            return "Inarmónico"
            
        return None

    asc_position = next((p for p in positions if p["name"] == "ASC"), None)
    
    for i, pos1 in enumerate(positions):
        if pos1["name"] not in traditional_planets:
            continue
            
        for pos2 in positions[i+1:]:
            if pos2["name"] not in traditional_planets:
                continue
                
            angle = calculate_angle(pos1["longitude"], pos2["longitude"])
            aspect_type = determine_aspect_type(angle)
            
            if aspect_type:
                aspects.append({
                    "planet1": pos1["name"],
                    "planet2": pos2["name"],
                    "type": get_aspect_key(angle),
                    "angle": angle,
                    "color": get_aspect_color(aspect_type)
                })
        
        # Aspectos con el ASC
        if asc_position:
            angle = calculate_angle(pos1["longitude"], asc_position["longitude"])
            aspect_type = determine_aspect_type(angle)
            
            if aspect_type:
                aspects.append({
                    "planet1": pos1["name"],
                    "planet2": "ASC",
                    "type": get_aspect_key(angle),
                    "angle": angle,
                    "color": get_aspect_color(aspect_type)
                })
    
    return aspects

def get_aspect_key(angle):
    """Obtiene la clave de aspecto basada en el ángulo"""
    angle = round(angle)
    
    if angle <= 2:  # Conjunción
        return "CONJUNCTION"
    elif 58 <= angle <= 62:  # Sextil
        return "SEXTILE"
    elif 88 <= angle <= 92:  # Cuadratura
        return "SQUARE"
    elif 118 <= angle <= 122:  # Trígono
        return "TRINE"
    elif 178 <= angle <= 180:  # Oposición
        return "OPPOSITION"
    
    # Para otros aspectos, usar claves genéricas
    if angle == 6: return "SEIS"
    if angle == 12: return "DOCE"
    if angle == 18: return "DIECIOCHO"
    if angle == 24: return "VEINTICUATRO"
    if angle == 30: return "TREINTA"
    if angle == 36: return "TREINTAYSEIS"
    if angle == 42: return "CUARENTAYDOS"
    if angle == 48: return "CUARENTAYOCHO"
    if angle == 54: return "CICUENTAYCUATRO"
    if angle == 66: return "SESENTAYSEIS"
    if angle == 72: return "QUINTILE"
    if angle == 78: return "SETENTAYOCHO"
    if angle == 84: return "OCHENTAYCUATRO"
    if angle == 96: return "NOVENTAYSEIS"
    if angle == 102: return "CIENTODOS"
    if angle == 108: return "CIENTOOCHO"
    if angle == 114: return "CIENTOCATORCE"
    if angle == 126: return "CIENTOVEINTISEIS"
    if angle == 132: return "CIENTOTREINTAYDOS"
    if angle == 138: return "CIENTOTREINTAYOCHO"
    if angle == 144: return "CIENTOCUARENTAYCUATRO"
    if angle == 150: return "QUINCUNX"
    if angle == 156: return "CIENTOCINCUENTAYSEIS"
    if angle == 162: return "CIENTOSESENTAYDOS"
    if angle == 168: return "CIENTOSESENTAYOCHO"
    if angle == 174: return "CIENTOSETENTAYCUATRO"
    
    # Si no coincide con ninguno, usar un valor genérico
    return f"ANGLE_{angle}"

def get_aspect_color(aspect_type):
    """Obtiene el color para un tipo de aspecto"""
    if aspect_type == "Armónico Relevante":
        return "#000080"  # Azul oscuro
    elif aspect_type == "Inarmónico Relevante":
        return "#FF0000"  # Rojo
    elif aspect_type == "Armónico":
        return "#ADD8E6"  # Azul claro
    elif aspect_type == "Inarmónico":
        return "#ffff00"  # Amarillo
    else:
        return "#888888"  # Gris por defecto

def get_house_number(longitude, asc_longitude):
    """Calcula la casa desde el Ascendente."""
    diff = (longitude - asc_longitude) % 360
    house = 1 + (int(diff / 30))
    if house > 12:
        house = house - 12
    return house

def is_dry_birth(sol_longitude, asc_longitude):
    """Determina si un nacimiento es seco (diurno) o húmedo (nocturno)"""
    # Es seco cuando el Sol está sobre el horizonte
    # Es decir, cuando el Sol está entre las casas 7 y 12 (inclusive)
    diff = (sol_longitude - asc_longitude) % 360
    house = 1 + (int(diff / 30))
    
    # Es seco (diurno) si el Sol está en las casas 7 a 12
    return 7 <= house <= 12

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/cities', methods=['GET'])
def get_cities():
    ciudad = request.args.get("ciudad")
    if not ciudad:
        return jsonify({"error": "Debes proporcionar una ciudad"}), 400

    print(f"Búsqueda recibida para ciudad: {ciudad}")
    
    # API key de Geoapify
    api_key = API_KEY
    
    # Usar la API de Geoapify para autocompletado de ciudades
    url = f"https://api.geoapify.com/v1/geocode/autocomplete?text={ciudad}&apiKey={api_key}&limit=20"
    
    try:
        # Hacer la petición a la API
        response = requests.get(url, timeout=10)
        print(f"Estado de respuesta Geoapify: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error en la API: {response.text}")
            raise Exception(f"Error en la API: {response.status_code}")
            
        data = response.json()
        
        # Crear lista de ciudades encontradas
        ciudades = []
        
        # Verificar si hay resultados
        if "features" in data and len(data["features"]) > 0:
            print(f"Número de resultados: {len(data['features'])}")
            
            for feature in data["features"]:
                props = feature["properties"]
                # Formatear el nombre de la ciudad con país
                nombre_ciudad = props.get("formatted", "")
                if nombre_ciudad:
                    print(f"Ciudad encontrada: {nombre_ciudad}")
                    ciudades.append(nombre_ciudad)
        else:
            print("No se encontraron resultados en la API")
        
        # Si no hay resultados, generar algunas opciones
        if not ciudades:
            print("Generando opciones")
            ciudades = [
                f"{ciudad}, España",
                f"{ciudad}, México",
                f"{ciudad}, Argentina",
                f"{ciudad}, Estados Unidos",
                f"{ciudad}, Colombia"
            ]
        
        print(f"Total ciudades a devolver: {len(ciudades)}")
        
        return jsonify({"ciudades": ciudades})
        
    except Exception as e:
        print(f"Error en búsqueda de ciudades: {str(e)}")
        # En caso de error, generar algunas opciones
        ciudades = [
            f"{ciudad}, España",
            f"{ciudad}, México",
            f"{ciudad}, Argentina",
            f"{ciudad}, Estados Unidos",
            f"{ciudad}, Colombia"
        ]
        
        return jsonify({"ciudades": ciudades})

@app.route('/calculate', methods=['POST', 'OPTIONS'])
def calculate():
    if request.method == 'OPTIONS':
        # Responder a la solicitud preflight de CORS
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
        
    try:
        data = request.get_json()
        if not data or not data.get('city'):
            return jsonify({"error": "Ciudad no especificada"}), 400
            
        city_data = obtener_datos_ciudad(data['city'], data['date'], data['time'])
        
        if isinstance(city_data, dict) and "error" in city_data:
            return jsonify(city_data), 400
            
        if isinstance(city_data, list) and len(city_data) > 0:
            city_data = city_data[0]
        else:
            return jsonify({"error": "No se pudo obtener información de la ciudad"}), 400
        
        try:
            # Obtener sistema zodiacal (tropical o sideral)
            use_sidereal = data.get('useSidereal', False)
            
            # Obtener zona horaria para las coordenadas
            timezone_info = obtener_zona_horaria(city_data, data['date'])
            
            # Convertir fecha y hora local a UTC
            utc_datetime = convertir_a_utc(data['date'], data['time'], timezone_info)
            
            # Calcular posiciones con el datetime UTC
            positions = calculate_positions_with_utc(utc_datetime, city_data["lat"], city_data["lon"], use_sidereal)
            
            # Calcular aspectos entre posiciones
            aspects = calculate_positions_aspects(positions)
            
            # Añadir número de casa a cada posición planetaria
            asc_pos = next((p for p in positions if p["name"] == "ASC"), None)
            if asc_pos:
                for planet in positions:
                    if planet["name"] not in ["ASC", "MC", "DSC", "IC", "PARTE_FORTUNA", "PARTE_ESPIRITU"]:
                        planet["house"] = get_house_number(planet["longitude"], asc_pos["longitude"])
            
            # Determinar si el nacimiento es seco (diurno) o húmedo (nocturno)
            sol_pos = next((p for p in positions if p["name"] == "SOL"), None)
            isDry = None
            if asc_pos and sol_pos:
                isDry = is_dry_birth(sol_pos["longitude"], asc_pos["longitude"])
            
            # Generar interpretaciones si el intérprete está disponible
            interpretations = {
                "planets_in_signs": [],
                "planets_in_houses": [],
                "aspects": [],
                "house_rulers": []
            }
            
            if interpreter and interpreter.root:
                # Interpretar planetas en signos
                for planet in positions:
                    if planet["name"] in ["SOL", "LUNA", "MERCURIO", "VENUS", "MARTE", "JÚPITER", "SATURNO"]:
                        sign_interp = interpreter.get_planet_in_sign(planet["name"], planet["sign"])
                        if sign_interp:
                            interpretations["planets_in_signs"].append({
                                "planet": planet["name"],
                                "sign": planet["sign"],
                                "interpretation": sign_interp
                            })
                
                # Interpretar planetas en casas
                if asc_pos:
                    for planet in positions:
                        if planet["name"] in ["SOL", "LUNA", "MERCURIO", "VENUS", "MARTE", "JÚPITER", "SATURNO"]:
                            house_num = get_house_number(planet["longitude"], asc_pos["longitude"])
                            house_interp = interpreter.get_planet_in_house(planet["name"], house_num)
                            if house_interp:
                                interpretations["planets_in_houses"].append({
                                    "planet": planet["name"],
                                    "house": house_num,
                                    "interpretation": house_interp
                                })
                
                # Interpretar aspectos
                for aspect in aspects:
                    # Obtener el tipo de aspecto
                    aspect_type = None
                    if aspect["type"] in ["CONJUNCTION", "SEXTILE", "TRINE", "OPPOSITION"]:
                        aspect_type = "Armónico Relevante"
                    elif aspect["type"] in ["SQUARE", "QUINCUNX"]:
                        aspect_type = "Inarmónico Relevante"
                    
                    if aspect_type and aspect["planet1"] in ["SOL", "LUNA", "MERCURIO", "VENUS", "MARTE", "JÚPITER", "SATURNO"] and \
                       aspect["planet2"] in ["SOL", "LUNA", "MERCURIO", "VENUS", "MARTE", "JÚPITER", "SATURNO"]:
                        
                        aspect_interp = interpreter.get_aspect_interpretation(aspect["planet1"], aspect["planet2"], aspect_type)
                        if aspect_interp:
                            interpretations["aspects"].append({
                                "planets": f"{aspect['planet1']} - {aspect['planet2']}",
                                "type": aspect_type,
                                "interpretation": aspect_interp
                            })
            
            # Construir respuesta
            response = {
                "positions": positions,
                "coordinates": {
                    "latitude": city_data["lat"],
                    "longitude": city_data["lon"]
                },
                "city": city_data["nombre"],
                "timezone": timezone_info,
                "local_time": f"{data['date']} {data['time']}",
                "utc_time": utc_datetime.strftime("%Y-%m-%d %H:%M"),
                "aspects": aspects,
                "interpretations": interpretations,
                "isDry": isDry,
                "zodiacSystem": "sidereal" if use_sidereal else "tropical"
            }
            
            return jsonify(response)
            
        except Exception as timezone_error:
            print(f"Error con zona horaria: {str(timezone_error)}")
            # Si hay error con la zona horaria, usamos valores básicos
            return jsonify({
                "error": f"Error en cálculos astrológicos: {str(timezone_error)}"
            }), 500
        
    except Exception as e:
        print(f"Error general: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\nIniciando servidor de carta astral optimizado...")
    preload_resources()
    print("Servidor iniciando en modo producción")
    # Obtener puerto del entorno o usar 10002 por defecto
    port = int(os.environ.get("PORT", 10002))
    app.run(host='0.0.0.0', port=port, debug=False)