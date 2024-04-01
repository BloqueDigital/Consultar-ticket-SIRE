from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/")
async def consultar_api_externa(url: str, token: str):  # Parámetros de consulta en la URL
    try:
        headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            page = data['paginacion']['page']
            des_estado_proceso = data['registros'][0]['desEstadoProceso']
            nom_archivo_reporte = data['registros'][0]['archivoReporte'][0]['nomArchivoReporte']

            datos_json = {
                'page': page,
                'des_estado_proceso': des_estado_proceso,
                'nom_archivo_reporte': nom_archivo_reporte
            }

            return datos_json
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error al realizar la solicitud: {response.status_code}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {err}")