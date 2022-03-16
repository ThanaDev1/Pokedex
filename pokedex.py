from flask import Flask, request, render_template
import requests, json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def rootpage():
    url = 'http://pokeapi.co/api/v2/pokemon/'
    busqueda = ''
    nombre = ''
    id = ''
    imagen = ''
    respuesta = ''
    estadisticas = {}
    tipos = []

    if request.method == 'POST':
        busqueda = str(request.form.get('busqueda'))

        peticion = requests.get(url + str(busqueda))

        try:
            respuesta = json.loads(peticion.content)

            nombre = f"{respuesta['name'].capitalize()}"

            id = f"{respuesta['id']}"

            for x in range(len(respuesta['stats'])):
                dicLocal = {
                    respuesta['stats'][x]['stat']['name']:respuesta['stats'][x]['base_stat']
                }
                estadisticas.update(dicLocal)
            imagen = respuesta['sprites']['other']['official-artwork']['front_default']

            for x in range(len(respuesta['types'])):
                tipos.append(respuesta['types'][x]['type']['name'])

        except json.JSONDecodeError:
            print("Busqueda no valida")
        except KeyError:
            print("No se permite una busqueda vacia.")



    return render_template("index.html", 
                            nombre=nombre, 
                            id=id, 
                            estadisticas=estadisticas,
                            imagen=imagen,
                            tipos=tipos)


app.run()