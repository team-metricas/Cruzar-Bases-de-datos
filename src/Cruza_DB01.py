import os
import pandas as pd
#import sys

# Cambio al directorio de datos
os.chdir("../data/")

# Cargo el archivo CSV con punto y coma como separador ( asi es como vino )
archivo_1 = "Base 1 Limpia.csv"
df_limpia = pd.read_csv(archivo_1, sep=';')

# Levanto el excel con datos completos
archivo_excel = "Base 2 Dato adicional Vencimiento.xlsx"

# Solo meto la primera hoja en un DataFrame
df_adicional = pd.read_excel(archivo_excel, sheet_name=0)

# Filtro el dataframe adicional por "tipo_doc" igual a 1
# Existen "tipo_doc" igual a 4, suponemos es pasaportes

df_adicional_filtrado = df_adicional[df_adicional['tipo_doc'] == 1]

# Hago el merge entre df_limpia y el df_adicional_filtrado usando left join
merged_df = df_limpia.merge(df_adicional_filtrado[['nro_doc', 'fec_vencimiento']], 
                            left_on='DNI', right_on='nro_doc', how='left', indicator=True)

# Filtro las filas donde el indicador _merge es 'both' ( SI funciono el join)
join_df = merged_df[merged_df['_merge'] == 'both']

# Filtro las filas donde el indicador _merge es 'left_only' (NO funciono el join)
no_join_df = merged_df[merged_df['_merge'] == 'left_only']

# Elimino las columnas _merge y nro_doc resultantes del merge, ya no me sirve de nada
join_df = join_df.drop(columns=['_merge', 'nro_doc'])
#no_join_df = no_join_df.drop(columns=['_merge', 'nro_doc'])

# Exporto el DataFrame de las filas que SI hicieron join a un CSV
archivo_salida_join = "Cruzados_ok.csv"
join_df.to_csv(archivo_salida_join, index=False, encoding='utf-8-sig', sep=';')

# Exporto el DataFrame de las filas que NO hicieron join a un CSV
archivo_salida_no_join = "Sin_Cruzar.csv"
no_join_df.to_csv(archivo_salida_no_join, index=False, encoding='utf-8-sig', sep=';')

# tamaños de los DataFrames
longitud_df_limpia = len(df_limpia)
longitud_join_df = len(join_df)

print(f'Tamaño de df_limpia : {longitud_df_limpia}')
print(f'Tamaño de Cruzados  : {longitud_join_df}')

# Veo si los tamaños son distintos
if longitud_df_limpia != longitud_join_df:
    print("\t\t\t\t\t\t\t\tTamaños difieren.")
else:
    print("\t\t\t\t\t\t\t\tTamaños son iguales.")

print('------FIN DEL PROCESO------------')


