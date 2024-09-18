import requests

def get_location(ip):  # El usuario ingresará la IP
    """
    Función que toma una dirección IP como argumento y devuelve
    la información de ubicación (país, región y ciudad) basada en esa IP.
    """
    # Construye la URL para la API, incluyendo la IP en el endpoint
    url = f"https://freeipapi.com/api/json/{ip}"  
    
    # Hace una solicitud GET a la API usando la URL construida
    response = requests.get(url)   # (El módulo que estamos usando es request.get)
    
    # Verifica si la respuesta HTTP fue exitosa (status code 200).    
    response.raise_for_status()  # Si no lo fue, lanza una excepción HTTPError.
    
    # Convierte la respuesta JSON en un diccionario de Python
    data = response.json()  
    
    # import ipdb; ipdb.set_trace() #Este comando inserta un "punto de interrupción" o "breakpoint" con  IPython Debugger.
    # podemos revisar data por concola con ipdb> data . Salimos con q + enter
    
    # Retorna un diccionario con los datos relevantes (país, región y ciudad)
    return {
        "country": data["countryName"],  # Extrae el nombre del país del JSON
        "region": data["regionName"],    # Extrae el nombre de la región del JSON
        "city": data["cityName"],        # Extrae el nombre de la ciudad del JSON
    }

