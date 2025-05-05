// Constantes globales
const DIMENSIONS = {
    centerX: 300,
    centerY: 300,
    radius: 280,
    middleRadius: 190, // Radio para la carta externa (tránsitos)
    innerRadius: 110,  // Radio para la carta interna (natal)
    glyphRadius: 265
};

const SIGNS = [
    {name: 'ARIES', start: 354, length: 36, symbol: '♈', color: '#FFE5E5'},
    {name: 'TAURUS', start: 30, length: 30, symbol: '♉', color: '#E5FFE5'},
    {name: 'GEMINI', start: 60, length: 30, symbol: '♊', color: '#FFFFE5'},
    {name: 'CANCER', start: 90, length: 30, symbol: '♋', color: '#E5FFFF'},
    {name: 'LEO', start: 120, length: 30, symbol: '♌', color: '#FFE5E5'},
    {name: 'VIRGO', start: 150, length: 36, symbol: '♍', color: '#E5FFE5'},
    {name: 'LIBRA', start: 186, length: 24, symbol: '♎', color: '#FFFFE5'},
    {name: 'SCORPIO', start: 210, length: 30, symbol: '♏', color: '#E5FFFF'},
    {name: 'OPHIUCHUS', start: 240, length: 12, symbol: '⛎', color: '#FFFFE5'},
    {name: 'SAGITTARIUS', start: 252, length: 18, symbol: '♐', color: '#FFE5E5'},
    {name: 'CAPRICORN', start: 270, length: 36, symbol: '♑', color: '#E5FFE5'},
    {name: 'AQUARIUS', start: 306, length: 18, symbol: '♒', color: '#FFFFE5'},
    {name: 'PEGASUS', start: 324, length: 6, symbol: '∩', color: '#E5FFFF'},
    {name: 'PISCES', start: 330, length: 24, symbol: '♓', color: '#E5FFFF'}
];

const PLANET_SYMBOLS = {
    'SOL': '☉',
    'LUNA': '☽',
    'MERCURIO': '☿',
    'VENUS': '♀',
    'MARTE': '♂',
    'JÚPITER': '♃',
    'SATURNO': '♄',
    'URANO': '♅',
    'NEPTUNO': '♆',
    'PLUTÓN': '♇',
    'ASC': 'ASC',
    'MC': 'MC',
    'DSC': 'DSC',
    'IC': 'IC',
    'PARTE_FORTUNA': 'PF',
    'PARTE_ESPIRITU': 'PE'
};

const ASPECTS = {
    'CONJUNCTION': { angle: 0, orb: 2, color: '#000080', name: 'Armónico Relevante' },
    'SEXTILE': { angle: 60, orb: 2, color: '#000080', name: 'Armónico Relevante' },
    'SQUARE': { angle: 90, orb: 2, color: '#FF0000', name: 'Inarmónico Relevante' },
    'TRINE': { angle: 120, orb: 2, color: '#000080', name: 'Armónico Relevante' },
    'OPPOSITION': { angle: 180, orb: 2, color: '#000080', name: 'Armónico Relevante' }
};

const COLORS = {
    RED: '#FF0000',
    GREEN: '#00FF00',
    BLUE: '#0000FF',
    YELLOW: '#FFFF00'
};

const DIGNIDAD_LABELS = {
    'domicilio': 'Domicilio',
    'exaltacion': 'Exaltación',
    'peregrino': 'Peregrino',
    'caida': 'Caída',
    'exilio': 'Exilio'
};

// Tasa de precesión anual en grados para ajustar posiciones estelares
const ANNUAL_PRECESSION_RATE = 50.2908 / 3600.0;  // Aproximadamente 50 segundos de arco por año

// Base de datos completa de estrellas fijas - Incluyendo las 52 estrellas
const FIXED_STARS = [
    {
        name: "Aldebaran",
        longitude_J2000: 69.00,
        effect: "Honor, inteligencia y riqueza",
        filePath: "https://www.izarren.top/aldebaran",
        magnitude: 12,
        interpretacion: {
            physical: "Potenciación de la autoridad natural y la capacidad de liderazgo. Amplifica la capacidad intelectual y mejora la toma de decisiones.",
            astral: "Conexión con sabios y guías ancestrales. Capacidad para conectar con la sabiduría de los antiguos."
        }
    },
    {
        name: "Antares",
        longitude_J2000: 249.18,
        effect: "Impulsividad y éxito arriesgado",
        filePath: "https://www.izarren.top/antares",
        magnitude: 12,
        interpretacion: {
            physical: "Incremento de la fuerza vital, energía y resistencia física. Puede conducir a impulsividad y comportamiento temerario.",
            astral: "Potencia la intuición marcial y la conexión con energías de naturaleza guerrera. Otorga la capacidad de percibir amenazas."
        }
    },
    {
        name: "Regulus",
        longitude_J2000: 148.51,
        effect: "Poder, éxito y honores",
        filePath: "https://www.izarren.top/regulus",
        magnitude: 12,
        interpretacion: {
            physical: "Desarrolla presencia magnética y reconocimiento social. Favorece el acceso a posiciones de poder y liderazgo.",
            astral: "Conecta con la energía solar del liderazgo espiritual. Otorga visión y concentración para propósitos elevados."
        }
    },
    {
        name: "Spica",
        longitude_J2000: 203.52,
        effect: "Beneficios a través del arte y ciencia",
        filePath: "https://www.izarren.top/spica",
        magnitude: 12,
        interpretacion: {
            physical: "Incrementa la habilidad en las artes y ciencias. Potencia la capacidad de expresión artística y el pensamiento científico.",
            astral: "Favorece la inspiración divina y la conexión con musas. Amplifica la capacidad de recibir ideas innovadoras."
        }
    },
    {
        name: "Sirius",
        longitude_J2000: 102.30,
        effect: "Honor, renombre y riqueza",
        filePath: "https://www.izarren.top/sirio",
        magnitude: 12,
        interpretacion: {
            physical: "Incrementa la fortuna material y el reconocimiento público. Favorece el éxito en las empresas iniciadas.",
            astral: "Conexión con fuerzas espirituales de guía y protección. Amplía la capacidad de comunicación con seres de luz."
        }
    },
    {
        name: "Algol",
        longitude_J2000: 56.3,
        effect: "Desafíos y transformación",
        filePath: "https://www.izarren.top/algol",
        magnitude: 12,
        interpretacion: {
            physical: "Puede traer crisis y desafíos repentinos que requieren transformación. Intensifica las experiencias límite.",
            astral: "Confrontación con el lado oscuro y transformativo del ser. Potencia para enfrentarse a los propios miedos y superarlos."
        }
    },
    {
        name: "Capella",
        longitude_J2000: 81.40,
        effect: "Honor y riqueza",
        filePath: "https://www.izarren.top/capella",
        magnitude: 12,
        interpretacion: {
            physical: "Favorece la acumulación de riqueza y bienes materiales. Mejora la capacidad administrativa.",
            astral: "Conexión con la abundancia universal. Potencia la capacidad de manifestar los deseos materiales."
        }
    },
    {
        name: "Vega",
        longitude_J2000: 284.03,
        effect: "Beneficios artísticos y creatividad",
        filePath: "https://www.izarren.top/vega",
        magnitude: 12,
        interpretacion: {
            physical: "Incrementa el talento musical y artístico. Favorece la expresión creativa en todas sus formas.",
            astral: "Conexión con las armonías cósmicas y la música de las esferas. Potencia los sueños visionarios y proféticos."
        }
    },
    {
        name: "Pollux",
        longitude_J2000: 113.31,
        effect: "Éxito atlético y marcial",
        filePath: "https://www.izarren.top/pollux",
        magnitude: 12,
        interpretacion: {
            physical: "Incrementa la fuerza física y la capacidad atlética. Mejora las habilidades competitivas y marciales.",
            astral: "Potencia las capacidades psíquicas relacionadas con la proyección de fuerza. Aumenta la capacidad de defensa energética."
        }
    },
    {
        name: "Fomalhaut",
        longitude_J2000: 333.0,
        effect: "Éxito espiritual y místico",
        filePath: "https://www.izarren.top/fomalhaut",
        magnitude: 6,
        interpretacion: {
            physical: "Favorece las vocaciones artísticas y espirituales. Otorga carisma y capacidad de inspirar a otros.",
            astral: "Abre portales hacia otras dimensiones y favorece el contacto con entidades angélicas. Amplifica la visión mística."
        }
    },
    {
        name: "Proción",
        longitude_J2000: 114.19,
        effect: "Éxito y honores a través del esfuerzo",
        filePath: "https://www.izarren.top/procyon",
        magnitude: 12,
        interpretacion: {
            physical: "Recompensa el trabajo duro y la perseverancia. Favorece el reconocimiento por méritos propios.",
            astral: "Conexión con guías que potencian la determinación y voluntad. Ayuda a superar obstáculos kármicos."
        }
    },
    {
        name: "Betelgeuse",
        longitude_J2000: 88.17,
        effect: "Elevación social",
        filePath: "https://www.izarren.top/betelgeuse",
        magnitude: 12,
        interpretacion: {
            physical: "Favorece el ascenso social y la obtención de posiciones de autoridad. Otorga presencia magnética.",
            astral: "Amplifica la capacidad de liderazgo espiritual y la conexión con maestros ascendidos. Potencia la misión de vida."
        }
    },
    // Añadir más estrellas si es necesario...
    {
        name: "Arcturus",
        longitude_J2000: 204.15,
        effect: "Éxito a través de la autodeterminación",
        filePath: "https://www.izarren.top/arcturus",
        magnitude: 12
    },
    {
        name: "Alphecca",
        longitude_J2000: 221.52,
        effect: "Dones artísticos y diplomacia",
        filePath: "https://www.izarren.top/alphecca",
        magnitude: 12
    },
    {
        name: "Castor",
        longitude_J2000: 113.17,
        effect: "Inteligencia y escritura",
        filePath: "https://www.izarren.top/castor",
        magnitude: 6
    }
];

// Variables globales
let natalPlanets = [];
let transitPlanets = [];
let internalAspects = [];
let interChartAspects = [];
let enlaces = []; // Enlaces planetarios para análisis avanzado
let selectedPlanet = null;
let selectedAspect = null;
let selectedStar = null;  // Para estrellas fijas
let activeStars = [];     // Estrellas fijas activas
let isDry = null;
let ascendenteName = '';
let birthDate = null;
let apiBaseUrl = "";  // Reemplazar con la URL correcta del backend si es necesario

// Variables para análisis avanzado
window.pico_mayor = [];
window.pico_moderado = [];
window.pico_menor = [];
window.liberacion_enlace = [];
window.presagios = {buenos: [], malos: []};

// Inicialización de la aplicación cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    console.log("Inicializando aplicación...");
    
    // Inicializar elementos DOM
    const cityInput = document.getElementById('city');
    const cityList = document.getElementById('cityList');
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
    const transitCityInput = document.getElementById('transitCity');
    const transitCityList = document.getElementById('transitCityList');
    const transitDateInput = document.getElementById('transitDate');
    const transitTimeInput = document.getElementById('transitTime');
    const showTransitsToggle = document.getElementById('showTransits');
    const calculateAnalysisToggle = document.getElementById('calculateAnalysis');
    const includeStarsToggle = document.getElementById('includeStars');
    const useSiderealZodiacToggle = document.getElementById('useSiderealZodiac');
    const transitsContainer = document.getElementById('transitsContainer');
    const calculateBtn = document.getElementById('calculateBtn');
    const chartContent = document.getElementById('chartContent');
    const chartSvg = document.getElementById('chartSvg');
    const chartTooltip = document.getElementById('chartTooltip');
    const errorAlert = document.getElementById('errorAlert');
    const infoBox = document.getElementById('infoBox');
    const loadingIndicator = document.getElementById('loadingIndicator');
    
    // Establecer fecha y hora actuales
    const now = new Date();
    dateInput.value = now.toISOString().split('T')[0];
    timeInput.value = now.toTimeString().slice(0, 5);
    
    transitDateInput.value = now.toISOString().split('T')[0];
    transitTimeInput.value = now.toTimeString().slice(0, 5);
    
    // Establecer ciudad predeterminada
    cityInput.value = "Bilbao, España";
    transitCityInput.value = "Bilbao, España";
    
    // Event listeners para búsqueda de ciudades
    cityInput.addEventListener('input', debounce(function() {
        handleCitySearch(cityInput.value, false);
    }, 300));
    
    transitCityInput.addEventListener('input', debounce(function() {
        handleCitySearch(transitCityInput.value, true);
    }, 300));
    
    // Event listeners para toggles y botones
    showTransitsToggle.addEventListener('change', toggleTransits);
    calculateBtn.addEventListener('click', calculateChart);
    
    // Event listener para toggle de zodiaco sideral
    useSiderealZodiacToggle.addEventListener('change', function() {
        // Si ya tenemos una carta calculada, volver a calcularla
        if (natalPlanets && natalPlanets.length > 0) {
            console.log("Recalculando carta con nuevo sistema zodiacal: " + (this.checked ? "Sideral" : "Tropical"));
            calculateChart();
        }
    });
    
    // Configurar inicialmente los controles de tránsitos
    toggleTransits();
    
    // Ocultar loading
    loadingIndicator.style.display = 'none';

    console.log("Aplicación inicializada correctamente");
});

// Función para búsqueda de ciudades
function handleCitySearch(searchText, isTransit) {
    const searchQuery = searchText.trim();
    const resultsContainer = isTransit ? document.getElementById('transitCityList') : document.getElementById('cityList');
    
    if (searchQuery.length < 3) {
        resultsContainer.innerHTML = '';
        return;
    }
    
    console.log(`Buscando ciudad: ${searchQuery} (${isTransit ? 'tránsito' : 'natal'})`);
    
    // Usar API de Geoapify para búsqueda de ciudades
    const API_KEY = "e19afa2a9d6643ea9550aab89eefce0b";
    const url = `https://api.geoapify.com/v1/geocode/search?text=${encodeURIComponent(searchQuery)}&apiKey=${API_KEY}`;
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la respuesta: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos de ciudades:", data);
            // Limpiar datalist
            resultsContainer.innerHTML = '';
            
            // Añadir opciones
            if (data.features && data.features.length > 0) {
                // Convertir los resultados de Geoapify al formato esperado por la aplicación
                const ciudades = data.features.map(feature => ({
                    nombre: feature.properties.formatted,
                    lat: feature.properties.lat,
                    lon: feature.properties.lon,
                    pais: feature.properties.country || ""
                }));
                
                ciudades.forEach(ciudad => {
                    const option = document.createElement('option');
                    option.value = ciudad.nombre;
                    option.setAttribute('data-lat', ciudad.lat);
                    option.setAttribute('data-lon', ciudad.lon);
                    resultsContainer.appendChild(option);
                });
            } else {
                // Ciudades de ejemplo si no hay resultados
                const examples = [
                    { nombre: "Bilbao, España", lat: 43.263, lon: -2.935 },
                    { nombre: "Madrid, España", lat: 40.416, lon: -3.703 },
                    { nombre: "Barcelona, España", lat: 41.385, lon: 2.173 },
                    { nombre: "Valencia, España", lat: 39.469, lon: -0.376 },
                    { nombre: "Sevilla, España", lat: 37.389, lon: -5.984 }                        
                ];
                
                examples.forEach(ciudad => {
                    const option = document.createElement('option');
                    option.value = ciudad.nombre;
                    option.setAttribute('data-lat', ciudad.lat);
                    option.setAttribute('data-lon', ciudad.lon);
                    resultsContainer.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Error buscando ciudades:', error);
            showError(`Error buscando ciudades: ${error.message}`);
            
            // Proporcionar algunas ciudades de ejemplo en caso de error
            resultsContainer.innerHTML = '';
            const examples = [
                { nombre: "Bilbao, España", lat: 43.263, lon: -2.935 },
                { nombre: "Madrid, España", lat: 40.416, lon: -3.703 },
                { nombre: "Barcelona, España", lat: 41.385, lon: 2.173 },
                { nombre: "Valencia, España", lat: 39.469, lon: -0.376 },
                { nombre: "Sevilla, España", lat: 37.389, lon: -5.984 }                        
            ];
            
            examples.forEach(ciudad => {
                const option = document.createElement('option');
                option.value = ciudad.nombre;
                option.setAttribute('data-lat', ciudad.lat);
                option.setAttribute('data-lon', ciudad.lon);
                resultsContainer.appendChild(option);
            });
        });
}

// Función para mostrar/ocultar sección de tránsitos
function toggleTransits() {
    const showTransitsToggle = document.getElementById('showTransits');
    const transitsContainer = document.getElementById('transitsContainer');
    
    const isChecked = showTransitsToggle.checked;
    
    if (isChecked) {
        transitsContainer.style.opacity = '1';
        transitsContainer.style.pointerEvents = 'auto';
    } else {
        transitsContainer.style.opacity = '0.5';
        transitsContainer.style.pointerEvents = 'none';
    }
}

// Función para obtener la opción seleccionada de una ciudad
function getSelectedCityCoordinates(inputElement, datalistElement) {
    const cityValue = inputElement.value;
    
    // Buscar la opción en el datalist que coincida con el valor introducido
    for (let i = 0; i < datalistElement.options.length; i++) {
        const option = datalistElement.options[i];
        if (option.value === cityValue) {
            return {
                lat: parseFloat(option.getAttribute('data-lat')),
                lon: parseFloat(option.getAttribute('data-lon'))
            };
        }
    }
    
    // Coordenadas por defecto si no se encuentra (Bilbao)
    return { lat: 43.263, lon: -2.935 };
}

// Función para mostrar información de nacimiento incluyendo sistema de zodiaco
function showBirthInfo(ascendente, esSeco) {
    const ascendenteInfo = document.getElementById('ascendenteInfo');
    const birthTypeInfo = document.getElementById('birthTypeInfo');
    const zodiacTypeInfo = document.getElementById('zodiacTypeInfo');
    const infoBox = document.getElementById('infoBox');
    
    ascendenteInfo.textContent = `Ascendente: ${ascendente}`;
    birthTypeInfo.textContent = `Tu nacimiento es de tipo ${esSeco ? 'seco' : 'húmedo'}`;
    
    // Agregar información sobre el sistema de zodiaco
    const useSiderealZodiac = document.getElementById('useSiderealZodiac').checked;
    zodiacTypeInfo.textContent = `Sistema: ${useSiderealZodiac ? 'Zodiaco Sideral (Fagan-Allen, 24° 15\')' : 'Zodiaco Tropical'}`;
    
    infoBox.classList.remove('d-none');
}

// Función principal para calcular la carta astral
function calculateChart() {
    // Validar entradas
    const cityInput = document.getElementById('city');
    const cityList = document.getElementById('cityList');
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
    const transitCityInput = document.getElementById('transitCity');
    const transitCityList = document.getElementById('transitCityList');
    const transitDateInput = document.getElementById('transitDate');
    const transitTimeInput = document.getElementById('transitTime');
    const showTransitsToggle = document.getElementById('showTransits');
    const calculateAnalysisToggle = document.getElementById('calculateAnalysis');
    const includeStarsToggle = document.getElementById('includeStars');
    const loadingIndicator = document.getElementById('loadingIndicator');
    
    if (!cityInput.value || !dateInput.value || !timeInput.value) {
        showError("Debes ingresar ciudad, fecha y hora para la carta natal.");
        return;
    }
    
    if (showTransitsToggle.checked && (!transitCityInput.value || !transitDateInput.value || !transitTimeInput.value)) {
        showError("Debes ingresar ciudad, fecha y hora para los tránsitos.");
        return;
    }
    
    // Mostrar loading
    loadingIndicator.style.display = 'flex';
    hideError();
    
    // Obtener coordenadas de la ciudad seleccionada
    const natalCoords = getSelectedCityCoordinates(cityInput, cityList);
    
    console.log("Calculando carta astral...");
    console.log("Datos natal:", {
        city: cityInput.value,
        date: dateInput.value,
        time: timeInput.value,
        lat: natalCoords.lat,
        lon: natalCoords.lon
    });
    
    // Guardar fecha de nacimiento para uso posterior
    birthDate = dateInput.value;
    
    // Obtener el estado del toggle del zodiaco sideral
    const useSiderealZodiac = document.getElementById('useSiderealZodiac').checked;
    console.log("Usando zodiaco sideral:", useSiderealZodiac);

    // Preparar los datos para enviar al servidor
    const chartData = {
        city: cityInput.value,
        date: dateInput.value,
        time: timeInput.value,
        calculateAnalysis: calculateAnalysisToggle.checked,
        useSidereal: useSiderealZodiac,
        includeStars: includeStarsToggle.checked
    };

    // Realizar petición al servidor o usar datos simulados
    if (apiBaseUrl) {
        // Si tenemos una URL de API, hacer petición al servidor
        fetch(`${apiBaseUrl}/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(chartData)
        })
        .then(response => response.json())
        .then(data => {
            processChartData(data);
            
            // Calcular tránsitos si están activados
            if (showTransitsToggle.checked) {
                calculateTransits();
            } else {
                // Si no hay tránsitos, renderizar la carta
                renderChart();
                loadingIndicator.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error calculando carta:', error);
            showError(`Error calculando carta: ${error.message}`);
            loadingIndicator.style.display = 'none';
            
            // Si hay error, usar datos simulados
            useSimulatedData();
        });
    } else {
        // Si no hay API, usar datos simulados
        useSimulatedData();
    }
}

// Función para procesar datos de la carta
function processChartData(data) {
    if (data.error) {
        showError(data.error);
        return;
    }
    
    // Guardar datos planetarios
    natalPlanets = data.positions || [];
    
    // Guardar aspectos
    internalAspects = data.aspects || [];
    
    // Guardar información de nacimiento
    isDry = data.isDry !== undefined ? data.isDry : null;
    
    // Guardar ascendente
    const asc = natalPlanets.find(p => p.name === "ASC");
    if (asc) {
        ascendenteName = asc.sign;
        
        // Mostrar info de nacimiento
        showBirthInfo(asc.sign, isDry);
    }
    
    // Si hay datos avanzados, guardarlos
    if (data.enlaces) {
        enlaces = data.enlaces;
        window.enlaces = enlaces;
    }
    
    if (data.pico_mayor) window.pico_mayor = data.pico_mayor;
    if (data.pico_moderado) window.pico_moderado = data.pico_moderado;
    if (data.pico_menor) window.pico_menor = data.pico_menor;
    if (data.liberacion_enlace) window.liberacion_enlace = data.liberacion_enlace;
    if (data.presagios) window.presagios = data.presagios;
    
    // Procesar estrellas fijas si están incluidas
    const includeStarsToggle = document.getElementById('includeStars');
    if (includeStarsToggle.checked) {
        if (data.stars && data.stars.active_stars) {
            activeStars = data.stars.active_stars;
        } else {
            // Si no hay datos de estrellas, calcularlas localmente
            activeStars = calculateFixedStars();
        }
    }
    
    console.log("Datos de carta procesados correctamente");
}

// Función para usar datos simulados
function useSimulatedData() {
    console.log("Usando datos simulados para carta");
    
    // Simular posiciones planetarias
    natalPlanets = mockCalculatePositions(true);
    
    // Calcular aspectos
    internalAspects = calculateAspects(natalPlanets);
    
    // Determinar tipo de nacimiento
    const asc = natalPlanets.find(p => p.name === "ASC");
    const sol = natalPlanets.find(p => p.name === "SOL");
    if (asc && sol) {
        isDry = is_dry_birth(sol.longitude, asc.longitude);
        
        // Guardar ascendente para uso posterior
        ascendenteName = asc.sign;
        
        // Mostrar info de nacimiento
        showBirthInfo(asc.sign, isDry);
    }
    
    // Simular datos avanzados
    simularDatosAvanzados();
    
    // Calcular estrellas fijas
    const includeStarsToggle = document.getElementById('includeStars');
    if (includeStarsToggle.checked) {
        activeStars = calculateFixedStars();
    }
    
    // Calcular tránsitos si están activados
    const showTransitsToggle = document.getElementById('showTransits');
    if (showTransitsToggle.checked) {
        calculateTransits();
    } else {
        // Si no hay tránsitos, renderizar la carta
        renderChart();
        document.getElementById('loadingIndicator').style.display = 'none';
    }
}

// Función para simular datos avanzados
function simularDatosAvanzados() {
    // Enlaces planetarios
    enlaces = [
        { planeta1: "SOL", planeta2: "VENUS", fuerza: 8, disolucion: false },
        { planeta1: "LUNA", planeta2: "JÚPITER", fuerza: 7, disolucion: false },
        { planeta1: "MERCURIO", planeta2: "MARTE", fuerza: 4, disolucion: false },
        { planeta1: "VENUS", planeta2: "SATURNO", fuerza: 3, disolucion: true }
    ];
    window.enlaces = enlaces;
    
    // Picos mayores
    window.pico_mayor = [
        { planeta: "SOL", signo: "LEO", fuerza: 9, planetas_aspectados: ["JÚPITER", "VENUS"] },
        { planeta: "JÚPITER", signo: "SAGITTARIUS", fuerza: 8, planetas_aspectados: ["SOL"] }
    ];
    
    // Picos moderados
    window.pico_moderado = [
        { planeta: "VENUS", signo: "TAURUS", fuerza: 7, planetas_aspectados: ["LUNA"] },
        { planeta: "LUNA", signo: "CANCER", fuerza: 6, planetas_aspectados: ["VENUS"] }
    ];
    
    // Picos menores
    window.pico_menor = [
        { planeta: "MERCURIO", signo: "GEMINI", fuerza: 5, planetas_aspectados: ["SOL"] }
    ];
    
    // Liberación de enlace
    window.liberacion_enlace = [
        { planeta_liberador: "SOL", planeta_liberado: "MARTE", condicion: "CONJUNCTION" },
        { planeta_liberador: "LUNA", planeta_liberado: "VENUS", condicion: "CONJUNCTION" }
    ];
    
    // Presagios
    window.presagios = {
        buenos: [
            { planeta: "JÚPITER", signo: "SAGITTARIUS", aspectos: true },
            { planeta: "VENUS", signo: "TAURUS", aspectos: false }
        ],
        malos: [
            { planeta: "MARTE", signo: "SCORPIO", aspectos: true }
        ]
    };
}

// Función para calcular tránsitos
function calculateTransits() {
    console.log("Calculando tránsitos...");
    
    const transitCityInput = document.getElementById('transitCity');
    const transitCityList = document.getElementById('transitCityList');
    const transitDateInput = document.getElementById('transitDate');
    const transitTimeInput = document.getElementById('transitTime');
    const calculateAnalysisToggle = document.getElementById('calculateAnalysis');
    const useSiderealZodiacToggle = document.getElementById('useSiderealZodiac');
    const loadingIndicator = document.getElementById('loadingIndicator');
    
    // Obtener coordenadas de la ciudad de tránsito
    const transitCoords = getSelectedCityCoordinates(transitCityInput, transitCityList);
    
    // Preparar datos para la petición
    const transitData = {
        city: transitCityInput.value,
        date: transitDateInput.value,
        time: transitTimeInput.value,
        calculateAnalysis: calculateAnalysisToggle.checked,
        useSidereal: useSiderealZodiacToggle.checked
    };
    
    if (apiBaseUrl) {
        // Si tenemos una URL de API, hacer petición al servidor
        fetch(`${apiBaseUrl}/transit_for_date`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transitData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Guardar posiciones de tránsito
            transitPlanets = data.positions || [];
            
            // Calcular aspectos entre cartas
            interChartAspects = calculateAspects(natalPlanets, transitPlanets);
            
            // Renderizar carta
            renderChart();
            loadingIndicator.style.display = 'none';
        })
        .catch(error => {
            console.error('Error calculando tránsitos:', error);
            
            // Usar datos simulados para tránsitos
            transitPlanets = mockCalculatePositions(false);
            interChartAspects = calculateAspects(natalPlanets, transitPlanets);
            
            renderChart();
            loadingIndicator.style.display = 'none';
        });
    } else {
        // Si no hay API, usar datos simulados
        transitPlanets = mockCalculatePositions(false);
        interChartAspects = calculateAspects(natalPlanets, transitPlanets);
        
        renderChart();
        loadingIndicator.style.display = 'none';
    }
}

// Función para calcular aspectos entre planetas
function calculateAspects(planets1, planets2) {
    if (!planets2) planets2 = planets1;
    
    const isSameChart = planets1 === planets2;
    const aspects = [];
    
    // Filtrar planetas tradicionales
    const traditionalPlanets = ["SOL", "LUNA", "MERCURIO", "VENUS", "MARTE", "JÚPITER", "SATURNO"];
    const validPlanets1 = planets1.filter(p => traditionalPlanets.includes(p.name));
    const validPlanets2 = planets2.filter(p => traditionalPlanets.includes(p.name));
    
    for (let i = 0; i < validPlanets1.length; i++) {
        // Si es la misma carta, evitar aspectos duplicados
        const startJ = isSameChart ? i + 1 : 0;
        
        for (let j = startJ; j < validPlanets2.length; j++) {
            const planet1 = validPlanets1[i];
            const planet2 = validPlanets2[j];
            
            if (planet1 === planet2) continue;
            
            let diff = Math.abs(planet1.longitude - planet2.longitude);
            if (diff > 180) diff = 360 - diff;
            
            // Comprobar aspectos importantes
            for (const aspectType in ASPECTS) {
                const aspect = ASPECTS[aspectType];
                
                if (Math.abs(diff - aspect.angle) <= aspect.orb) {
                    aspects.push({
                        planet1: planet1.name,
                        planet2: planet2.name,
                        type: aspectType,
                        angle: diff,
                        color: aspect.color,
                        isInterChart: !isSameChart,
                        fuerza: 0 // Se calculará en el backend si está disponible
                    });
                    break;
                }
            }
        }
    }
    
    return aspects;
}

// Función para determinar si un nacimiento es seco o húmedo
function is_dry_birth(sun_longitude, asc_longitude) {
    // Es seco cuando el Sol está entre las casas 6 y 11 (inclusive)
    let diff = (sun_longitude - asc_longitude) % 360;
    if (diff < 0) diff += 360;
    
    const house = Math.floor(diff / 30) + 1;
    
    // Es seco si el Sol está en las casas 6 a 11
    return house >= 6 && house <= 11;
}

// Función de utilidad para calcular distancia entre puntos zodiacales
function distancia_zodiaco(punto_inicio, punto_fin) {
    // Normalizar
    punto_inicio = (punto_inicio % 360 + 360) % 360;
    punto_fin = (punto_fin % 360 + 360) % 360;
    
    // Calcular distancia en sentido normal (antihorario)
    let dist = (punto_fin - punto_inicio + 360) % 360;
    
    return dist;
}

// Función para calcular estrellas fijas
function calculateFixedStars() {
    const dateInput = document.getElementById('date');
    if (!dateInput.value || !natalPlanets) {
        return [];
    }
    
    const date = dateInput.value;
    
    // Procesar cada estrella
    const stars = FIXED_STARS.map(star => {
        // Calcular posición actual
        const currentLongitude = getCurrentStarPosition(star, date);
        
        // Determinar signo basado en longitud
        const sign = getSign(currentLongitude);
        
        // Encontrar planetas en conjunción
        const conjunctPlanets = findConjunctPlanets(star, natalPlanets, date);
        
        // Determinar si la estrella está activa (tiene conjunciones)
        const isActive = conjunctPlanets.length > 0;
        
        return {
            ...star,
            longitude: currentLongitude,
            sign: sign,
            conjunctPlanets: conjunctPlanets,
            selected: selectedStar === star.name,
            isActive: isActive
        };
    }).filter(star => star.isActive); // Solo devolver estrellas activas
    
    console.log(`Calculadas ${stars.length} estrellas fijas activas`);
    return stars;
}

// Función para calcular la posición actual de una estrella
function getCurrentStarPosition(star, dateStr) {
    // Convertir fecha a objeto Date
    const currentDate = new Date(dateStr);
    // Calcular año decimal
    const year = currentDate.getFullYear() + (currentDate.getMonth() + 1) / 12;
    // Años desde J2000
    const yearsSinceJ2000 = year - 2000.0;
    // Calcular precesión
    const precession = ANNUAL_PRECESSION_RATE * yearsSinceJ2000;
    // Devolver longitud ajustada
    return (star.longitude_J2000 + precession) % 360;
}

// Función para encontrar planetas en conjunción con una estrella
function findConjunctPlanets(star, planetsList, dateStr) {
    const currentLongitude = getCurrentStarPosition(star, dateStr);
    const orb = star.magnitude >= 12 ? 2.40 : 1.20;
    
    return planetsList.filter(planet => {
        const diff = Math.abs(currentLongitude - planet.longitude);
        const adjustedDiff = Math.min(diff, 360 - diff);
        return adjustedDiff <= orb;
    }).map(planet => ({
        name: planet.name,
        diff: Math.min(
            Math.abs(currentLongitude - planet.longitude),
            360 - Math.abs(currentLongitude - planet.longitude)
        ).toFixed(2)
    }));
}

// Función para obtener el signo zodiacal desde longitud
function getSign(longitude) {
    longitude = longitude % 360;
    
    for (const sign of SIGNS) {
        if (sign.start <= longitude && longitude < (sign.start + sign.length)) {
            return sign.name;
        }
        // Caso especial para Aries que cruza 0°
        if (sign.name === 'ARIES' && (longitude >= sign.start || longitude < 30)) {
            return sign.name;
        }
    }
    
    return "ARIES";  // Valor por defecto
}

// Función para renderizar la carta astral
function renderChart() {
    console.log("Renderizando carta astral...");
    
    const chartSvg = document.getElementById('chartSvg');
    
    // Limpiar SVG
    chartSvg.innerHTML = '';
    
    // Dibujar elementos
    drawZodiacWheel();
    drawAspects();
    drawPlanets(natalPlanets, true);
    
    const showTransitsToggle = document.getElementById('showTransits');
    if (showTransitsToggle.checked && transitPlanets.length > 0) {
        drawPlanets(transitPlanets, false);
    }
    
    // Dibujar estrellas fijas si están activadas
    const includeStarsToggle = document.getElementById('includeStars');
    if (includeStarsToggle.checked && activeStars && activeStars.length > 0) {
        drawFixedStars();
    }
    
    // Actualizar listas de información
    updatePlanetsList();
    updateAspectsList();
    updateAdvancedInfo();
    
    // Renderizar componente de estrellas fijas si están activadas
    if (includeStarsToggle.checked) {
        renderFixedStarsComponent();
    }
    
    // Mostrar la carta
    document.getElementById('chartContent').style.display = 'flex';
    
    console.log("Carta astral renderizada");
}

// Función para dibujar la rueda zodiacal
function drawZodiacWheel() {
    const chartSvg = document.getElementById('chartSvg');
    
    // Dibujar círculo exterior
    const outerCircle = createSvgElement('circle', {
        cx: DIMENSIONS.centerX,
        cy: DIMENSIONS.centerY,
        r: DIMENSIONS.radius,
        fill: 'none',
        stroke: '#333',
        'stroke-width': 2
    });
    chartSvg.appendChild(outerCircle);
    
    // Dibujar signos zodiacales
    SIGNS.forEach(sign => {
        const midAngle = ((sign.start + sign.length/2 - 90) * Math.PI) / 180;
        const glyphX = DIMENSIONS.centerX + DIMENSIONS.glyphRadius * Math.cos(midAngle);
        const glyphY = DIMENSIONS.centerY + DIMENSIONS.glyphRadius * Math.sin(midAngle);
        
        // Dibujar sector
        const path = createSvgElement('path', {
            d: createArcPath(sign.start, sign.start + sign.length),
            fill: sign.color,
            stroke: '#333',
            'stroke-width': 1
        });
        chartSvg.appendChild(path);
        
        // Añadir símbolo
        const text = createSvgElement('text', {
            x: glyphX,
            y: glyphY,
            'text-anchor': 'middle',
            'alignment-baseline': 'middle',
            'font-size': 20
        });
        text.textContent = sign.symbol;
        chartSvg.appendChild(text);
    });
    
    // Dibujar círculo interior
    const innerCircle = createSvgElement('circle', {
        cx: DIMENSIONS.centerX,
        cy: DIMENSIONS.centerY,
        r: DIMENSIONS.innerRadius,
        fill: 'white',
        stroke: '#333',
        'stroke-width': 1
    });
    chartSvg.appendChild(innerCircle);
}

// Función para dibujar aspectos
function drawAspects() {
    const chartSvg = document.getElementById('chartSvg');
    
    // Dibujar aspectos internos
    internalAspects.forEach((aspect, index) => {
        const planet1 = natalPlanets.find(p => p.name === aspect.planet1);
        const planet2 = natalPlanets.find(p => p.name === aspect.planet2);
        
        if (!planet1 || !planet2) return;
        
        const angle1 = (planet1.longitude - 90) * Math.PI / 180;
        const angle2 = (planet2.longitude - 90) * Math.PI / 180;
        
        const x1 = DIMENSIONS.centerX + DIMENSIONS.innerRadius * Math.cos(angle1);
        const y1 = DIMENSIONS.centerY + DIMENSIONS.innerRadius * Math.sin(angle1);
        const x2 = DIMENSIONS.centerX + DIMENSIONS.innerRadius * Math.cos(angle2);
        const y2 = DIMENSIONS.centerY + DIMENSIONS.innerRadius * Math.sin(angle2);
        
        const line = createSvgElement('line', {
            x1: x1,
            y1: y1,
            x2: x2,
            y2: y2,
            stroke: aspect.color,
            'stroke-width': selectedAspect === aspect ? '3' : '1',
            'data-aspect-index': index,
            'class': 'aspect-line internal-aspect'
        });
        
        line.addEventListener('click', () => {
            selectAspect(aspect, 'internal');
        });
        
        line.addEventListener('mouseover', (e) => {
            const aspectName = ASPECTS[aspect.type]?.name || aspect.type;
            showTooltip(e, `${aspect.planet1} ${aspectName} ${aspect.planet2} (${aspect.angle.toFixed(1)}°)`);
        });
        
        line.addEventListener('mouseout', () => {
            hideTooltip();
        });
        
        chartSvg.appendChild(line);
    });
    
    // Dibujar aspectos entre cartas
    const showTransitsToggle = document.getElementById('showTransits');
    if (showTransitsToggle.checked && transitPlanets.length > 0) {
        interChartAspects.forEach((aspect, index) => {
            const planet1 = natalPlanets.find(p => p.name === aspect.planet1);
            const planet2 = transitPlanets.find(p => p.name === aspect.planet2);
            
            if (!planet1 || !planet2) return;
            
            const angle1 = (planet1.longitude - 90) * Math.PI / 180;
            const angle2 = (planet2.longitude - 90) * Math.PI / 180;
            
            const x1 = DIMENSIONS.centerX + DIMENSIONS.innerRadius * Math.cos(angle1);
            const y1 = DIMENSIONS.centerY + DIMENSIONS.innerRadius * Math.sin(angle1);
            const x2 = DIMENSIONS.centerX + DIMENSIONS.middleRadius * Math.cos(angle2);
            const y2 = DIMENSIONS.centerY + DIMENSIONS.middleRadius * Math.sin(angle2);
            
            const line = createSvgElement('line', {
                x1: x1,
                y1: y1,
                x2: x2,
                y2: y2,
                stroke: aspect.color,
                'stroke-width': selectedAspect === aspect ? '3' : '1',
                'stroke-dasharray': '3,3',
                'data-aspect-index': index,
                'class': 'aspect-line inter-aspect'
            });
            
            line.addEventListener('click', () => {
                selectAspect(aspect, 'inter');
            });
            
            line.addEventListener('mouseover', (e) => {
                const aspectName = ASPECTS[aspect.type]?.name || aspect.type;
                showTooltip(e, `${aspect.planet1} ${aspectName} ${aspect.planet2} (${aspect.angle.toFixed(1)}°)`);
            });
            
            line.addEventListener('mouseout', () => {
                hideTooltip();
            });
            
            chartSvg.appendChild(line);
        });
    }
}

// Función para dibujar planetas
function drawPlanets(planets, isNatal) {
    const chartSvg = document.getElementById('chartSvg');
    const radius = isNatal ? DIMENSIONS.innerRadius : DIMENSIONS.middleRadius;
    
    planets.forEach((planet, index) => {
        // Ajustar posición para evitar superposiciones
        const adjustmentData = adjustPlanetLabel(planet, planets);
        const adjustedAngle = ((planet.longitude + adjustmentData.angleOffset - 90) * Math.PI) / 180;
        const x = DIMENSIONS.centerX + radius * Math.cos(adjustedAngle);
        const y = DIMENSIONS.centerY + radius * Math.sin(adjustedAngle);
        
        // Determinar posición de la etiqueta
        const labelX = DIMENSIONS.centerX + adjustmentData.radius * Math.cos(adjustedAngle);
        const labelY = DIMENSIONS.centerY + adjustmentData.radius * Math.sin(adjustedAngle);
        
        // Estado de selección
        const isSelected = selectedPlanet === planet;
        
        // Color del planeta
        const planetColor = getPlanetColor(planet.name, planet.longitude);
        
        // Dibujar círculo para el planeta
        const circle = createSvgElement('circle', {
            cx: x,
            cy: y,
            r: isSelected ? "6" : "4",
            fill: planetColor,
            stroke: '#000',
            'stroke-width': isSelected ? "2" : "1",
            'data-planet-index': index,
            'data-is-natal': isNatal,
            'class': 'planet-symbol'
        });
        
        // Añadir eventos al círculo
        circle.addEventListener('click', () => {
            selectPlanet(planet, isNatal);
        });
        
        circle.addEventListener('mouseover', (e) => {
            // Añadir estado retrógrado al tooltip si aplica
            let retroInfo = '';
            if (planet.motion_status === 'retrograde') {
                retroInfo = ' (Retrógrado)';
            } else if (planet.motion_status === 'stationary_retrograde') {
                retroInfo = ' (Estacionario Retrógrado)';
            } else if (planet.motion_status === 'stationary_direct') {
                retroInfo = ' (Estacionario Directo)';
            }
            
            showTooltip(e, `${planet.name}${retroInfo} en ${planet.sign} (${planet.longitude.toFixed(1)}°)`);
        });
        
        circle.addEventListener('mouseout', () => {
            hideTooltip();
        });
        
        chartSvg.appendChild(circle);
        
        // Para planetas retrógrados, añadir un indicador visual
        if (planet.motion_status === 'retrograde' || 
            planet.motion_status === 'stationary_retrograde' || 
            planet.motion_status === 'stationary_direct') {
            
            // Añadir un pequeño indicador del movimiento retrógrado
            const retroIndicator = createSvgElement('circle', {
                cx: x,
                cy: y - 10, // Posición encima del planeta
                r: 3,
                fill: planet.motion_status === 'retrograde' ? '#dc3545' : 
                     planet.motion_status === 'stationary_retrograde' ? '#fd7e14' : '#20c997',
                'pointer-events': 'none'
            });
            
            chartSvg.appendChild(retroIndicator);
        }
        
        // Añadir símbolo del planeta
        // Venus y Marte en negrita, resto normal
        if (planet.name === 'VENUS' || planet.name === 'MARTE') {
            // Para Venus y Marte aplicar un efecto negrita más fuerte
            // Primero dibujar un contorno grueso
            const textOutline = createSvgElement('text', {
                x: labelX,
                y: labelY,
                'text-anchor': 'middle',
                'alignment-baseline': 'middle',
                'font-size': 14,
                'fill': '#000000',
                'stroke': '#000000', 
                'stroke-width': 1,  // Contorno más grueso para Venus y Marte
                'font-weight': 'bold',
                'pointer-events': 'none'
            });
            textOutline.textContent = PLANET_SYMBOLS[planet.name] || planet.name;
            chartSvg.appendChild(textOutline);
            
            // Y luego el texto principal encima para un efecto más fuerte
            const textMain = createSvgElement('text', {
                x: labelX,
                y: labelY,
                'text-anchor': 'middle',
                'alignment-baseline': 'middle',
                'font-size': 14,
                'fill': '#000000',
                'font-weight': 'bold',
                'pointer-events': 'none'
            });
            textMain.textContent = PLANET_SYMBOLS[planet.name] || planet.name;
            chartSvg.appendChild(textMain);
        } else {
            // Para otros planetas, texto normal sin efecto negrita adicional
            const text = createSvgElement('text', {
                x: labelX,
                y: labelY,
                'text-anchor': 'middle',
                'alignment-baseline': 'middle',
                'font-size': 14,
                'fill': '#000000',
                'font-weight': 'normal',
                'pointer-events': 'none'
            });
            text.textContent = PLANET_SYMBOLS[planet.name] || planet.name;
            chartSvg.appendChild(text);
        }
    });
}

// Función para dibujar estrellas fijas
function drawFixedStars() {
    const chartSvg = document.getElementById('chartSvg');
    
    // Limpiar estrellas existentes
    const existingStarsGroup = chartSvg.querySelector('.fixed-stars-group');
    if (existingStarsGroup) {
        existingStarsGroup.remove();
    }
    
    // Verificar si tenemos los datos necesarios
    if (!activeStars || activeStars.length === 0) return;
    
    // Crear un grupo para todos los elementos de estrellas
    const starsGroup = createSvgElement('g', {
        'class': 'fixed-stars-group'
    });
    
    // Dibujar cada estrella
    activeStars.forEach((star) => {
        // Calcular posición en la carta
        const starAngle = ((star.longitude - 90) * Math.PI) / 180;
        
        // Posicionar estrellas entre los círculos exterior y medio
        const radius = DIMENSIONS.radius - 20; // Ligeramente dentro de la rueda exterior
        
        const x = DIMENSIONS.centerX + radius * Math.cos(starAngle);
        const y = DIMENSIONS.centerY + radius * Math.sin(starAngle);
        
        // Dibujar punto de estrella
        const starPoint = createSvgElement('circle', {
            cx: x,
            cy: y,
            r: star.magnitude >= 12 ? '4' : '3',
            fill: '#FFD700',
            stroke: '#000',
            'stroke-width': selectedStar === star.name ? '2' : '0.5',
            'class': `star-point ${selectedStar === star.name ? 'selected' : ''}`,
            'data-star-name': star.name
        });
        
        // Agregar evento de clic
        starPoint.addEventListener('click', () => {
            handleStarClick(star.name);
        });
        
        // Agregar eventos de mouseover/mouseout para retroalimentación visual
        starPoint.addEventListener('mouseover', (e) => {
            starPoint.setAttribute('r', star.magnitude >= 12 ? '5' : '4');
            starPoint.setAttribute('fill', '#FFC800');
            
            // Mostrar tooltip con información de la estrella
            const tooltipText = `${star.name} en ${star.sign} (${star.longitude.toFixed(1)}°)
                              Conjunción con: ${star.conjunctPlanets.map(p => `${p.name} (${p.diff}°)`).join(', ')}`;
            showTooltip(e, tooltipText);
        });
        
        starPoint.addEventListener('mouseout', () => {
            starPoint.setAttribute('r', star.magnitude >= 12 ? '4' : '3');
            starPoint.setAttribute('fill', '#FFD700');
            hideTooltip();
        });
        
        // Agregar punto de estrella al grupo
        starsGroup.appendChild(starPoint);
        
        // Para estrella seleccionada o estrellas muy brillantes, agregar una pequeña etiqueta
        if (selectedStar === star.name || star.magnitude >= 12) {
            const labelX = DIMENSIONS.centerX + (radius + 12) * Math.cos(starAngle);
            const labelY = DIMENSIONS.centerY + (radius + 12) * Math.sin(starAngle);
            
            const starLabel = createSvgElement('text', {
                x: labelX,
                y: labelY,
                'text-anchor': 'middle',
                'alignment-baseline': 'middle',
                'font-size': '8',
                'font-weight': 'bold',
                'class': 'star-label'
            });
            starLabel.textContent = star.name.split(' ')[0]; // Solo la primera palabra
            
            starsGroup.appendChild(starLabel);
        }
    });
    
    // Agregar el grupo de estrellas al SVG principal
    chartSvg.appendChild(starsGroup);
}

// Función para renderizar el componente de estrellas fijas
function renderFixedStarsComponent() {
    const fixedStarsContainer = document.getElementById('fixedStarsContainer');
    
    if (!fixedStarsContainer) return;
    
    // Generar HTML para estrellas fijas
    let starsHtml = '';
    
    if (!activeStars || activeStars.length === 0) {
        starsHtml = '<div class="alert alert-info">No hay estrellas fijas activas en esta carta.</div>';
    } else {
        starsHtml = `
            <div class="search-container mb-3">
                <input type="text" class="form-control" id="starsSearchInput"
                    placeholder="Buscar estrellas por nombre, efecto o signo...">
            </div>
            
            <div class="stars-list">
        `;
        
        // Filtrar estrellas si un planeta está seleccionado
        const displayedStars = selectedPlanet 
            ? activeStars.filter(star => star.conjunctPlanets.some(p => p.name === selectedPlanet.name))
            : activeStars;
            
        if (displayedStars.length === 0) {
            starsHtml += `<p>No hay estrellas en conjunción con ${selectedPlanet?.name || ''}.</p>`;
        } else {
            displayedStars.forEach(star => {
                starsHtml += `
                    <div class="star-item ${star.name === selectedStar ? 'selected' : ''}" 
                        data-star-name="${star.name}" onclick="handleStarClick('${star.name}')">
                        <div class="star-header">
                            <span class="star-symbol">★</span>
                            <strong>${star.name}</strong> - ${star.sign} (${star.longitude.toFixed(2)}°)
                        </div>
                        
                        <div class="star-details">
                            <div>
                                <strong>Conjunción con:</strong> ${
                                    star.conjunctPlanets.map(p => `${p.name} (${p.diff}°)`).join(', ')
                                }
                            </div>
                            <div><strong>Efecto:</strong> ${star.effect}</div>
                            ${star.filePath ? `
                            <div><strong>Más info:</strong> 
                                <a href="#" class="star-link" onclick="event.preventDefault(); event.stopPropagation(); openStarLink('${star.filePath}');">
                                    Ver información detallada
                                </a>
                            </div>
                            ` : ''}
                            
                            ${star.interpretacion ? `
                            <div class="star-interpretation">
                                ${star.interpretacion.physical ? `
                                <div class="physical-plane">
                                    <div class="plane-title">Plano Físico:</div>
                                    <div>${star.interpretacion.physical}</div>
                                </div>
                                ` : ''}
                                
                                ${star.interpretacion.astral ? `
                                <div class="astral-plane">
                                    <div class="plane-title">Plano Astral:</div>
                                    <div>${star.interpretacion.astral}</div>
                                </div>
                                ` : ''}
                            </div>
                            ` : ''}
                        </div>
                    </div>
                `;
            });
        }
        
        starsHtml += `</div>`;
    }
    
    fixedStarsContainer.innerHTML = starsHtml;
    
    // Agregar listener para búsqueda
    const searchInput = document.getElementById('starsSearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchValue = e.target.value.toLowerCase();
            const starItems = document.querySelectorAll('.star-item');
            
            starItems.forEach(item => {
                const starName = item.getAttribute('data-star-name');
                const star = activeStars.find(s => s.name === starName);
                
                if (!star) return;
                
                const matchesSearch = 
                    star.name.toLowerCase().includes(searchValue) ||
                    star.effect.toLowerCase().includes(searchValue) ||
                    star.sign.toLowerCase().includes(searchValue);
                    
                item.style.display = matchesSearch ? 'block' : 'none';
            });
        });
    }
}

// Función para ajustar la posición de etiquetas de planetas
function adjustPlanetLabel(planet, allPlanets) {
    // Verificar si hay planetas cercanos para evitar superposición
    const baseLongitude = planet.longitude;
    const nearbyPlanets = allPlanets.filter(p => 
        p !== planet && 
        Math.abs(p.longitude - baseLongitude) < 5);
    
    // Si hay planetas cercanos, ajustar el offset
    if (nearbyPlanets.length > 0) {
        // Ajustar offset según posición
        const offset = (nearbyPlanets.length * 3) % 20;
        return {
            angleOffset: offset,
            radius: DIMENSIONS.innerRadius - 10 - (offset * 0.5)
        };
    }
    
    // Si no hay ajuste necesario
    return {
        angleOffset: 0,
        radius: DIMENSIONS.innerRadius - 5
    };
}

// Función para obtener color planetario
function getPlanetColor(planetName, longitude) {
    // Colores pastel
    const PASTEL_COLORS = {
        RED: '#FF9999',       // Pastel red
        GREEN: '#99FF99',     // Pastel green
        BLUE: '#9999FF',      // Pastel blue
        YELLOW: '#FFFF99',    // Pastel yellow
        ORANGE: '#FFD699',    // Pastel orange
        PURPLE: '#D699FF',    // Pastel purple
        CYAN: '#99FFFF',      // Pastel cyan
        PINK: '#FF99FF',      // Pastel pink
        GRAY: '#E0E0E0'       // Light gray for cardinal points
    };
    
    // Color según tipo de planeta
    if (planetName === 'ASC' || planetName === 'MC' || planetName === 'DSC' || planetName === 'IC' ||
        planetName === 'PARTE_FORTUNA' || planetName === 'PARTE_ESPIRITU') {
        return PASTEL_COLORS.GRAY;  // Puntos cardinales
    } else if (planetName === 'JÚPITER') {
        if ((longitude >= 306.00 && longitude <= 360.00) || (longitude >= 0.00 && longitude <= 150.00)) 
            return PASTEL_COLORS.BLUE;
        else if (longitude > 150.00 && longitude < 306.00) 
            return PASTEL_COLORS.RED;
        else
            return PASTEL_COLORS.BLUE;
    } else if (planetName === 'SATURNO') {
        if ((longitude >= 330.00 && longitude <= 360.00) || (longitude >= 0.00 && longitude <= 150.00))
            return PASTEL_COLORS.YELLOW;
        else if (longitude > 240.00 && longitude <= 252.00) 
            return PASTEL_COLORS.YELLOW;
        else if (longitude > 252.00 && longitude <= 330.00) 
            return PASTEL_COLORS.RED;
        else if (longitude > 150.00 && longitude <= 240.00) 
            return PASTEL_COLORS.RED;
        else
            return PASTEL_COLORS.YELLOW;
    } else if (longitude > 150.00 && longitude <= 330.00) {
        if (planetName === 'SOL' || planetName === 'MERCURIO' || planetName === 'URANO')
            return PASTEL_COLORS.GREEN;
        else if (planetName === 'VENUS' || planetName === 'LUNA')
            return PASTEL_COLORS.YELLOW;
        else if (planetName === 'MARTE' || planetName === 'PLUTÓN')
            return PASTEL_COLORS.BLUE;
        else if (planetName === 'NEPTUNO')
            return PASTEL_COLORS.RED;
        else
            return PASTEL_COLORS.GRAY;
    } else {
        if (planetName === 'SOL' || planetName === 'MARTE' || planetName === 'PLUTÓN')
            return PASTEL_COLORS.RED;
        else if (planetName === 'VENUS')
            return PASTEL_COLORS.GREEN;
        else if (planetName === 'MERCURIO' || planetName === 'URANO')
            return PASTEL_COLORS.YELLOW;
        else if (planetName === 'LUNA' || planetName === 'NEPTUNO')
            return PASTEL_COLORS.BLUE;
        else
            return PASTEL_COLORS.GRAY;
    }
}

// Función para actualizar la lista de planetas
function updatePlanetsList() {
    const natalPlanetsContainer = document.getElementById('natalPlanets');
    const transitPlanetsContainer = document.getElementById('transitPlanets');
    
    // Actualizar lista de planetas natales
    natalPlanetsContainer.innerHTML = '';
    
    natalPlanets.forEach(planet => {
        const planetItem = document.createElement('div');
        planetItem.className = `planet-list-item ${selectedPlanet === planet ? 'selected' : ''}`;
        
        // Determinar clase CSS para dignidad
        let dignityClass = '';
        if (planet.dignidad) {
            dignityClass = `dignity-${planet.dignidad}`;
        }
        
        // Determinar símbolo retrógrado
        let retroSymbol = '';
        if (planet.motion_status === 'retrograde') {
            retroSymbol = ' <span class="retrograde">℞</span>'; // Símbolo Rx
        } else if (planet.motion_status === 'stationary_retrograde') {
            retroSymbol = ' <span class="stationary-retrograde">Sr</span>'; // Símbolo Sr
        } else if (planet.motion_status === 'stationary_direct') {
            retroSymbol = ' <span class="stationary-direct">Sd</span>'; // Símbolo Sd
        }
        
        planetItem.innerHTML = `
            <strong>${PLANET_SYMBOLS[planet.name] || planet.name}</strong>${retroSymbol}: 
            ${planet.sign} ${planet.longitude.toFixed(1)}° 
            <span class="${dignityClass}">${planet.dignidad ? `(${DIGNIDAD_LABELS[planet.dignidad]})` : ''}</span>
        `;
        
        planetItem.addEventListener('click', () => {
            selectPlanet(planet, true);
        });
        
        natalPlanetsContainer.appendChild(planetItem);
    });
    
    // Actualizar lista de planetas de tránsito
    transitPlanetsContainer.innerHTML = '';
    
    const showTransitsToggle = document.getElementById('showTransits');
    if (showTransitsToggle.checked && transitPlanets.length > 0) {
        transitPlanets.forEach(planet => {
            const planetItem = document.createElement('div');
            planetItem.className = `planet-list-item ${selectedPlanet === planet ? 'selected' : ''}`;
            
            // Determinar clase CSS para dignidad
            let dignityClass = '';
            if (planet.dignidad) {
                dignityClass = `dignity-${planet.dignidad}`;
            }
            
            // Determinar símbolo retrógrado
            let retroSymbol = '';
            if (planet.motion_status === 'retrograde') {
                retroSymbol = ' <span class="retrograde">℞</span>'; // Símbolo Rx
            } else if (planet.motion_status === 'stationary_retrograde') {
                retroSymbol = ' <span class="stationary-retrograde">Sr</span>'; // Símbolo Sr
            } else if (planet.motion_status === 'stationary_direct') {
                retroSymbol = ' <span class="stationary-direct">Sd</span>'; // Símbolo Sd
            }
            
            planetItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[planet.name] || planet.name}</strong>${retroSymbol}: 
                ${planet.sign} ${planet.longitude.toFixed(1)}° 
                <span class="${dignityClass}">${planet.dignidad ? `(${DIGNIDAD_LABELS[planet.dignidad]})` : ''}</span>
            `;
            
            planetItem.addEventListener('click', () => {
                selectPlanet(planet, false);
            });
            
            transitPlanetsContainer.appendChild(planetItem);
        });
    } else {
        transitPlanetsContainer.innerHTML = '<p>No hay datos de tránsitos.</p>';
    }
}

// Función para actualizar la lista de aspectos
function updateAspectsList() {
    const internalAspectsContainer = document.getElementById('internalAspects');
    const interChartAspectsContainer = document.getElementById('interChartAspects');
    
    // Actualizar aspectos internos
    internalAspectsContainer.innerHTML = '';
    
    if (internalAspects && internalAspects.length > 0) {
        internalAspects.forEach(aspect => {
            const aspectItem = document.createElement('div');
            aspectItem.className = `aspect-list-item ${selectedAspect === aspect ? 'selected' : ''}`;
            
            const aspectName = ASPECTS[aspect.type]?.name || aspect.type;
            const aspectStrength = aspect.fuerza ? ` (Fuerza: ${aspect.fuerza.toFixed(1)})` : '';
            
            aspectItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[aspect.planet1] || aspect.planet1}</strong> 
                <span style="color: ${ASPECTS[aspect.type].color};">${aspectName}</span> 
                <strong>${PLANET_SYMBOLS[aspect.planet2] || aspect.planet2}</strong>
                ${aspectStrength}
            `;
            
            aspectItem.addEventListener('click', () => {
                selectAspect(aspect, 'internal');
            });
            
            internalAspectsContainer.appendChild(aspectItem);
        });
    } else {
        internalAspectsContainer.innerHTML = '<p>No hay aspectos internos.</p>';
    }
    
    // Actualizar aspectos entre cartas
    interChartAspectsContainer.innerHTML = '';
    
    const showTransitsToggle = document.getElementById('showTransits');
    if (showTransitsToggle.checked && interChartAspects && interChartAspects.length > 0) {
        interChartAspects.forEach(aspect => {
            const aspectItem = document.createElement('div');
            aspectItem.className = `aspect-list-item ${selectedAspect === aspect ? 'selected' : ''}`;
            
            const aspectName = ASPECTS[aspect.type]?.name || aspect.type;
            
            aspectItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[aspect.planet1] || aspect.planet1}</strong> (natal)
                <span style="color: ${ASPECTS[aspect.type].color};">${aspectName}</span> 
                <strong>${PLANET_SYMBOLS[aspect.planet2] || aspect.planet2}</strong> (tránsito)
            `;
            
            aspectItem.addEventListener('click', () => {
                selectAspect(aspect, 'inter');
            });
            
            interChartAspectsContainer.appendChild(aspectItem);
        });
    } else {
        interChartAspectsContainer.innerHTML = '<p>No hay aspectos entre cartas.</p>';
    }
}

// Función para actualizar la información avanzada
function updateAdvancedInfo() {
    const enlacesPlanetariosContainer = document.getElementById('enlacesPlanetarios');
    const picoMayorContainer = document.getElementById('picoMayor');
    const picoModeradoContainer = document.getElementById('picoModerado');
    const picoMenorContainer = document.getElementById('picoMenor');
    const liberacionEnlaceContainer = document.getElementById('liberacionEnlace');
    const presagiosContainer = document.getElementById('presagios');
    
    // Verificar si los contenedores existen
    if (!enlacesPlanetariosContainer || !picoMayorContainer) return;
    
    const calculateAnalysisToggle = document.getElementById('calculateAnalysis');
    
    // Solo actualizar si calculateAnalysis está activado
    if (!calculateAnalysisToggle.checked) {
        enlacesPlanetariosContainer.innerHTML = '<p>Activa "Análisis Avanzado" para ver esta información.</p>';
        picoMayorContainer.innerHTML = '';
        picoModeradoContainer.innerHTML = '';
        picoMenorContainer.innerHTML = '';
        liberacionEnlaceContainer.innerHTML = '';
        presagiosContainer.innerHTML = '';
        return;
    }
    
    // Si no hay datos avanzados, mostrar mensaje
    if (!window.enlaces || window.enlaces === undefined) {
        enlacesPlanetariosContainer.innerHTML = '<p>No hay datos de análisis avanzado disponibles.</p>';
        return;
    }
    
    // Enlaces planetarios
    enlacesPlanetariosContainer.innerHTML = '';
    if (window.enlaces && window.enlaces.length > 0) {
        window.enlaces.forEach(enlace => {
            const enlaceItem = document.createElement('div');
            
            // Determinar clase de fuerza
            let fuerzaClass = 'enlace-medio';
            if (enlace.fuerza >= 8) fuerzaClass = 'enlace-fuerte';
            else if (enlace.fuerza <= 3) fuerzaClass = 'enlace-debil';
            
            enlaceItem.className = `enlace-item ${fuerzaClass}`;
            
            enlaceItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[enlace.planeta1] || enlace.planeta1}</strong> →
                <strong>${PLANET_SYMBOLS[enlace.planeta2] || enlace.planeta2}</strong>
                (Fuerza: ${enlace.fuerza})
                ${enlace.disolucion ? '<span class="badge bg-warning">Disuelto</span>' : ''}
            `;
            
            enlacesPlanetariosContainer.appendChild(enlaceItem);
        });
    } else {
        enlacesPlanetariosContainer.innerHTML = '<p>No hay enlaces planetarios significativos.</p>';
    }
    
    // Picos
    picoMayorContainer.innerHTML = '';
    if (window.pico_mayor && window.pico_mayor.length > 0) {
        window.pico_mayor.forEach(pico => {
            const picoItem = document.createElement('div');
            picoItem.className = 'pico-item';
            
            picoItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[pico.planeta] || pico.planeta}</strong>
                en ${pico.signo} con fuerza ${pico.fuerza}
                ${pico.planetas_aspectados ? `<br>Aspectos favorables con: ${pico.planetas_aspectados.join(', ')}` : ''}
            `;
            
            picoMayorContainer.appendChild(picoItem);
        });
    } else {
        picoMayorContainer.innerHTML = '<p>No hay picos mayores.</p>';
    }
    
    // Pico moderado
    picoModeradoContainer.innerHTML = '';
    if (window.pico_moderado && window.pico_moderado.length > 0) {
        window.pico_moderado.forEach(pico => {
            const picoItem = document.createElement('div');
            picoItem.className = 'pico-item';
            
            picoItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[pico.planeta] || pico.planeta}</strong>
                en ${pico.signo} con fuerza ${pico.fuerza}
                ${pico.planetas_aspectados ? `<br>Aspectos favorables con: ${pico.planetas_aspectados.join(', ')}` : ''}
            `;
            
            picoModeradoContainer.appendChild(picoItem);
        });
    } else {
        picoModeradoContainer.innerHTML = '<p>No hay picos moderados.</p>';
    }
    
    // Pico menor
    picoMenorContainer.innerHTML = '';
    if (window.pico_menor && window.pico_menor.length > 0) {
        window.pico_menor.forEach(pico => {
            const picoItem = document.createElement('div');
            picoItem.className = 'pico-item';
            
            picoItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[pico.planeta] || pico.planeta}</strong>
                en ${pico.signo} con fuerza ${pico.fuerza}
                ${pico.planetas_aspectados ? `<br>Aspectos favorables con: ${pico.planetas_aspectados.join(', ')}` : ''}
            `;
            
            picoMenorContainer.appendChild(picoItem);
        });
    } else {
        picoMenorContainer.innerHTML = '<p>No hay picos menores.</p>';
    }
    
    // Liberación de enlace
    liberacionEnlaceContainer.innerHTML = '';
    if (window.liberacion_enlace && window.liberacion_enlace.length > 0) {
        window.liberacion_enlace.forEach(liberacion => {
            const libItem = document.createElement('div');
            libItem.className = 'enlace-item enlace-fuerte';
            
            libItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[liberacion.planeta_liberador] || liberacion.planeta_liberador}</strong>
                libera a
                <strong>${PLANET_SYMBOLS[liberacion.planeta_liberado] || liberacion.planeta_liberado}</strong>
                mediante ${liberacion.condicion}
            `;
            
            liberacionEnlaceContainer.appendChild(libItem);
        });
    } else {
        liberacionEnlaceContainer.innerHTML = '<p>No hay liberaciones de enlace.</p>';
    }
    
    // Presagios
    presagiosContainer.innerHTML = '';
    let hasPresagios = false;
    
    if (window.presagios?.buenos && window.presagios.buenos.length > 0) {
        hasPresagios = true;
        const presagiosBuenosTitle = document.createElement('h5');
        presagiosBuenosTitle.textContent = 'Presagios Favorables';
        presagiosContainer.appendChild(presagiosBuenosTitle);
        
        window.presagios.buenos.forEach(presagio => {
            const presItem = document.createElement('div');
            presItem.className = 'enlace-item enlace-fuerte';
            
            presItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[presagio.planeta] || presagio.planeta}</strong>
                en ${presagio.signo}
                ${presagio.aspectos ? `con aspectos favorables` : ''}
            `;
            
            presagiosContainer.appendChild(presItem);
        });
    }
    
    if (window.presagios?.malos && window.presagios.malos.length > 0) {
        hasPresagios = true;
        const presagiosMalosTitle = document.createElement('h5');
        presagiosMalosTitle.textContent = 'Presagios Desfavorables';
        presagiosMalosTitle.className = 'mt-3';
        presagiosContainer.appendChild(presagiosMalosTitle);
        
        window.presagios.malos.forEach(presagio => {
            const presItem = document.createElement('div');
            presItem.className = 'enlace-item enlace-debil';
            
            presItem.innerHTML = `
                <strong>${PLANET_SYMBOLS[presagio.planeta] || presagio.planeta}</strong>
                en ${presagio.signo}
                ${presagio.aspectos ? `con aspectos desfavorables` : ''}
            `;
            
            presagiosContainer.appendChild(presItem);
        });
    }
    
    if (!hasPresagios) {
        presagiosContainer.innerHTML = '<p>No hay presagios significativos.</p>';
    }
}

// Función para seleccionar un planeta
function selectPlanet(planet, isNatal) {
    // Deseleccionar aspecto si hay alguno
    selectedAspect = null;
    selectedStar = null;
    
    // Alternar selección
    if (selectedPlanet === planet) {
        selectedPlanet = null;
    } else {
        selectedPlanet = planet;
    }
    
    // Volver a renderizar la carta para mostrar la selección
    renderChart();
}

// Función para seleccionar un aspecto
function selectAspect(aspect, type) {
    // Deseleccionar planeta si hay alguno
    selectedPlanet = null;
    selectedStar = null;
    
    // Alternar selección
    if (selectedAspect === aspect) {
        selectedAspect = null;
    } else {
        selectedAspect = aspect;
    }
    
    // Volver a renderizar la carta para mostrar la selección
    renderChart();
}

// Función para manejar el clic en una estrella
function handleStarClick(starName) {
    // Comprobar si es la misma estrella (conmutar selección)
    selectedStar = selectedStar === starName ? null : starName;
    
    // Limpiar selecciones de planetas y aspectos
    selectedPlanet = null;
    selectedAspect = null;
    
    // Volver a renderizar la carta para mostrar la selección
    renderChart();
    
    // Si hay una URL para abrir, intentar abrirla
    if (selectedStar) {
        const star = activeStars.find(s => s.name === selectedStar);
        if (star && star.filePath) {
            openStarLink(star.filePath);
        }
    }
}

// Función para abrir enlaces de estrellas fijas
function openStarLink(filePath) {
    if (filePath) {
        // Si es una URL externa, abrirla directamente en una nueva pestaña
        if (filePath.startsWith("https://")) {
            window.open(filePath, "_blank");
        }
    }
}

// Función para crear un elemento SVG
function createSvgElement(type, attributes = {}) {
    const element = document.createElementNS('http://www.w3.org/2000/svg', type);
    
    for (const [key, value] of Object.entries(attributes)) {
        element.setAttribute(key, value);
    }
    
    return element;
}

// Función para crear un path de arco SVG
function createArcPath(startAngle, endAngle) {
    // Convertir ángulos a radianes
    const startRad = (startAngle - 90) * Math.PI / 180;
    const endRad = (endAngle - 90) * Math.PI / 180;
    
    // Calcular puntos
    const startX = DIMENSIONS.centerX + DIMENSIONS.radius * Math.cos(startRad);
    const startY = DIMENSIONS.centerY + DIMENSIONS.radius * Math.sin(startRad);
    const endX = DIMENSIONS.centerX + DIMENSIONS.radius * Math.cos(endRad);
    const endY = DIMENSIONS.centerY + DIMENSIONS.radius * Math.sin(endRad);
    
    // Determinar flag de arco grande
    const largeArcFlag = endAngle - startAngle <= 180 ? '0' : '1';
    
    // Construir el string del path
    return `M ${DIMENSIONS.centerX} ${DIMENSIONS.centerY} L ${startX} ${startY} A ${DIMENSIONS.radius} ${DIMENSIONS.radius} 0 ${largeArcFlag} 1 ${endX} ${endY} Z`;
}

// Función para mostrar mensajes de error
function showError(message) {
    console.error("Error:", message);
    const errorAlert = document.getElementById('errorAlert');
    errorAlert.textContent = message;
    errorAlert.classList.remove('d-none');
}

// Función para ocultar mensajes de error
function hideError() {
    const errorAlert = document.getElementById('errorAlert');
    errorAlert.textContent = '';
    errorAlert.classList.add('d-none');
}

// Función para mostrar tooltip
function showTooltip(event, text) {
    const chartTooltip = document.getElementById('chartTooltip');
    const chartSvg = document.getElementById('chartSvg');
    
    chartTooltip.textContent = text;
    chartTooltip.style.display = 'block';
    
    // Posicionar el tooltip cerca del cursor
    const rect = chartSvg.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    chartTooltip.style.left = `${x + 15}px`;
    chartTooltip.style.top = `${y + 15}px`;
}

// Función para ocultar tooltip
function hideTooltip() {
    const chartTooltip = document.getElementById('chartTooltip');
    chartTooltip.style.display = 'none';
}

// Función debounce para limitar llamadas a funciones
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}

// Simulación de datos planetarios para fines de demostración
function mockCalculatePositions(is_natal=true, asc_sign=null, asc_longitude=null) {
    const base_positions = [
        {"name": "SOL", "longitude": 120 + (is_natal ? 0 : 30), "sign": "LEO", "dignidad": "exaltacion", "motion_status": "direct"},
        {"name": "LUNA", "longitude": 186 + (is_natal ? 0 : 24), "sign": "LIBRA", "dignidad": "exaltacion", "motion_status": "direct"},
        {"name": "MERCURIO", "longitude": 135 + (is_natal ? 0 : 10), "sign": "LEO", "dignidad": "", "motion_status": "retrograde"},
        {"name": "VENUS", "longitude": 90 + (is_natal ? 0 : 10), "sign": "CANCER", "dignidad": "exaltacion", "motion_status": "direct"},
        {"name": "MARTE", "longitude": 210 + (is_natal ? 0 : 30), "sign": "SCORPIO", "dignidad": "domicilio", "motion_status": "direct"},
        {"name": "JÚPITER", "longitude": 270 + (is_natal ? 0 : 20), "sign": "CAPRICORN", "dignidad": "caida", "motion_status": "retrograde"},
        {"name": "SATURNO", "longitude": 330 + (is_natal ? 0 : 20), "sign": "PISCES", "dignidad": "exilio", "motion_status": "stationary_retrograde"},
        {"name": "URANO", "longitude": 30 + (is_natal ? 0 : 2), "sign": "TAURUS", "dignidad": "", "motion_status": "retrograde"},
        {"name": "NEPTUNO", "longitude": 354 + (is_natal ? 0 : 1), "sign": "ARIES", "dignidad": "", "motion_status": "direct"},
        {"name": "PLUTÓN", "longitude": 252 + (is_natal ? 0 : 2), "sign": "SAGITTARIUS", "dignidad": "", "motion_status": "stationary_direct"},
        {"name": "ASC", "longitude": asc_longitude || 0, "sign": asc_sign || "ARIES", "dignidad": "", "motion_status": "direct"},
        {"name": "MC", "longitude": 270, "sign": "CAPRICORN", "dignidad": "", "motion_status": "direct"}
    ];
    
    // Si no es natal, añadir una variación aleatoria a las posiciones
    if (!is_natal) {
        for (let planet of base_positions) {
            // Esta variación mantiene la lógica del archivo original
            planet.longitude = (planet.longitude + Math.random() * 20 - 10) % 360;
            planet.sign = getSign(planet.longitude);
            if (planet.name in DIGNIDADES) {
                planet.dignidad = calcularDignidadPlanetaria(planet.name, planet.longitude);
            }
        }
    }
    
    // Añadir Descendente y IC si es carta natal
    if (is_natal) {
        const asc = base_positions.find(p => p.name === "ASC");
        const mc = base_positions.find(p => p.name === "MC");
        
        if (asc) {
            // Añadir DSC (opuesto al ASC)
            const dscLongitude = (asc.longitude + 180) % 360;
            base_positions.push({
                "name": "DSC",
                "longitude": dscLongitude,
                "sign": getSign(dscLongitude),
                "dignidad": "",
                "motion_status": "direct"
            });
        }
        
        if (mc) {
            // Añadir IC (opuesto al MC)
            const icLongitude = (mc.longitude + 180) % 360;
            base_positions.push({
                "name": "IC",
                "longitude": icLongitude,
                "sign": getSign(icLongitude),
                "dignidad": "",
                "motion_status": "direct"
            });
        }
        
        // Añadir Parte de Fortuna y Parte del Espíritu
        const sol = base_positions.find(p => p.name === "SOL");
        const luna = base_positions.find(p => p.name === "LUNA");
        
        if (asc && sol && luna) {
            // Determinar si es seco o húmedo según la posición del Sol
            const is_dry = is_dry_birth(sol.longitude, asc.longitude);
            
            // Cálculo correcto según nacimiento seco o húmedo
            let parte_fortuna, parte_espiritu;
            
            if (is_dry) {  // Carta seca (diurna)
                // Para carta diurna: Parte de Fortuna = ASC + dist(Sol→Luna)
                const dist_sol_a_luna = (luna.longitude - sol.longitude + 360) % 360;
                parte_fortuna = (asc.longitude + dist_sol_a_luna) % 360;
                
                // Para carta diurna: Parte del Espíritu = ASC + dist(Luna→Sol)
                const dist_luna_a_sol = (sol.longitude - luna.longitude + 360) % 360;
                parte_espiritu = (asc.longitude + dist_luna_a_sol) % 360;
            } else {  // Carta húmeda (nocturna)
                // Para carta nocturna: Parte de Fortuna = ASC + dist(Luna→Sol)
                const dist_luna_a_sol = (sol.longitude - luna.longitude + 360) % 360;
                parte_fortuna = (asc.longitude + dist_luna_a_sol) % 360;
                
                // Para carta nocturna: Parte del Espíritu = ASC + dist(Sol→Luna)
                const dist_sol_a_luna = (luna.longitude - sol.longitude + 360) % 360;
                parte_espiritu = (asc.longitude + dist_sol_a_luna) % 360;
            }
            
            base_positions.push({
                "name": "PARTE_FORTUNA",
                "longitude": parte_fortuna,
                "sign": getSign(parte_fortuna),
                "dignidad": "",
                "motion_status": "direct"
            });
            
            base_positions.push({
                "name": "PARTE_ESPIRITU",
                "longitude": parte_espiritu,
                "sign": getSign(parte_espiritu),
                "dignidad": "",
                "motion_status": "direct"
            });
        }
    }
    
    return base_positions;
}

// Función auxiliar para calcular dignidad planetaria
function calcularDignidadPlanetaria(planeta, longitud) {
    const signo = getSign(longitud);
    
    // Simplificado para demo
    const dignidades = {
        'SOL': { 'domicilio': ['LEO'], 'exaltacion': ['ARIES'], 'caida': ['LIBRA'], 'exilio': ['AQUARIUS'] },
        'LUNA': { 'domicilio': ['CANCER'], 'exaltacion': ['TAURUS'], 'caida': ['SCORPIO'], 'exilio': ['CAPRICORN'] },
        'MERCURIO': { 'domicilio': ['GEMINI', 'VIRGO'], 'exaltacion': ['VIRGO'], 'caida': ['PISCES'], 'exilio': ['SAGITTARIUS', 'PISCES'] },
        'VENUS': { 'domicilio': ['TAURUS', 'LIBRA'], 'exaltacion': ['PISCES'], 'caida': ['VIRGO'], 'exilio': ['SCORPIO', 'ARIES'] },
        'MARTE': { 'domicilio': ['ARIES', 'SCORPIO'], 'exaltacion': ['CAPRICORN'], 'caida': ['CANCER'], 'exilio': ['TAURUS', 'LIBRA'] },
        'JÚPITER': { 'domicilio': ['SAGITTARIUS', 'PISCES'], 'exaltacion': ['CANCER'], 'caida': ['CAPRICORN'], 'exilio': ['GEMINI', 'VIRGO'] },
        'SATURNO': { 'domicilio': ['CAPRICORN', 'AQUARIUS'], 'exaltacion': ['LIBRA'], 'caida': ['ARIES'], 'exilio': ['CANCER', 'LEO'] }
    };
    
    if (planeta in dignidades) {
        if (dignidades[planeta]['domicilio'].includes(signo)) {
            return "domicilio";
        } else if (dignidades[planeta]['exaltacion'].includes(signo)) {
            return "exaltacion";
        } else if (dignidades[planeta]['caida'].includes(signo)) {
            return "caida";
        } else if (dignidades[planeta]['exilio'].includes(signo)) {
            return "exilio";
        }
    }
    
    return "";
}

// Exportar funciones para acceso global
window.handleCitySearch = handleCitySearch;
window.calculateChart = calculateChart;
window.handleStarClick = handleStarClick;
window.openStarLink = openStarLink;