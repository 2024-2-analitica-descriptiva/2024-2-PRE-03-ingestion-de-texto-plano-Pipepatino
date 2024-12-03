"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd

import pandas as pd

def pregunta_01():
    """
    Construye y retorna un DataFrame de Pandas a partir del archivo 'clusters_report.txt'.

    Requisitos:
        - El DataFrame debe replicar la estructura del archivo original.
        - Los nombres de las columnas deben estar en minúsculas y reemplazar espacios por guiones bajos.
        - Las palabras clave deben estar separadas por comas y con un solo espacio entre palabras.

    Returns:
        pd.DataFrame: DataFrame con la información procesada del archivo.
    """
    # Leer el archivo utilizando `pd.read_fwf` con parámetros ajustados a la estructura del archivo.
    df = pd.read_fwf(
        "files/input/clusters_report.txt",
        widths=[9, 16, 16, 77],  # Ancho fijo para cada columna.
        skiprows=lambda row_counter: row_counter < 4,  # Omitir las primeras 4 filas (encabezado).
        names=["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"],
        converters={
            # Quitar el símbolo '%' y reemplazar ',' por '.' para normalizar porcentajes.
            "porcentaje_de_palabras_clave": lambda x: x.strip(" %").replace(",", ".") if x is not None else x
        }
    ).ffill()  # Rellenar valores NaN con el último valor no nulo.

    # Agrupar filas repetidas para consolidar las palabras clave de cada cluster.
    df = df.groupby(
        ["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave"]
    )["principales_palabras_clave"].agg(
        lambda x: ' '.join(x)  # Combinar palabras clave de filas agrupadas en un único string.
    ).reset_index()  # Restablecer el índice para que sea secuencial.

    # Limpiar y normalizar las palabras clave.
    df["principales_palabras_clave"] = df["principales_palabras_clave"].agg(
        lambda x: ' '.join(x.split()).replace(".", "")  # Eliminar múltiples espacios y puntos innecesarios.
    )

    # Convertir columnas a los tipos de datos requeridos.
    df["cantidad_de_palabras_clave"] = df["cantidad_de_palabras_clave"].astype(int)  # Asegurar enteros.
    df["porcentaje_de_palabras_clave"] = df["porcentaje_de_palabras_clave"].astype(float)  # Convertir a flotante.

    return df

# Ejecutar la función y mostrar el DataFrame resultante.
print(pregunta_01())
