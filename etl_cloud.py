import pandas as pd
import os

# --- CONFIGURACIÓN ---
# Detectamos si es CSV o Excel (a veces este dataset viene en xlsx)
archivo_entrada = 'input/ventas_globales.csv' 
ruta_salida = 'output/ventas_cloud_limpias.csv'

print("1. ☁️ Cargando datos globales...")

try:
    # Intentamos leer como CSV (encoding 'latin1' suele funcionar para datos globales)
    df = pd.read_csv(archivo_entrada, encoding='latin1')
except:
    print("   -> No es CSV, intentando leer como Excel...")
    df = pd.read_excel('input/ventas_globales.xlsx')

print(f"   -> Filas cargadas: {df.shape[0]}")

# --- LIMPIEZA PARA LA NUBE ---
print("2. 🧹 Normalizando para Google Cloud...")

# A. Renombrar columnas (BigQuery NO acepta espacios ni símbolos raros)
# Vamos a estandarizar todo a minúsculas y guiones bajos
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
print("   -> Nombres de columnas corregidos (ej. 'Order Date' -> 'order_date')")

# B. Convertir Fechas (Vital para calcular tiempos de envío)
df['order_date'] = pd.to_datetime(df['order_date'], format='%d-%m-%Y', dayfirst=True, errors='coerce')
df['ship_date'] = pd.to_datetime(df['ship_date'], format='%d-%m-%Y', dayfirst=True, errors='coerce')

# C. Ingeniería de Datos: Calcular "Días de Envío"
# (Fecha de Envío - Fecha de Orden)
df['dias_envio'] = (df['ship_date'] - df['order_date']).dt.days

# D. Eliminar nulos críticos
df = df.dropna(subset=['order_id', 'country', 'profit'])

print(f"   -> Limpieza lista. Filas finales: {df.shape[0]}")

# --- EXPORTACIÓN ---
print("3. 🚀 Generando archivo para BigQuery...")
# Exportamos en CSV estándar (separado por comas, utf-8)
df.to_csv(ruta_salida, index=False, encoding='utf-8')

print(f"¡LISTO! Sube este archivo a la nube: {ruta_salida}")