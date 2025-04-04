def gestionar_productos(lista_productos):
    productos_ordenados = sorted(lista_productos)
    cadena_ordenada = ", ".join(productos_ordenados)
    slugs = list(map(lambda nombre: nombre.lower().replace(" ", "-"), productos_ordenados))
    return {
        "slugs": slugs,
        "cadena_ordenada": cadena_ordenada
    }

productos = [
    "Frijoles Refritos",
    "Coca Cola",
    "Zumo de Naranja", 
    "Café de Olla", 
    "Gorditas de Chicharrón", 
    "Huevos Motuleños"
]

resultados = gestionar_productos(productos)

print(" Lista de slugs:")
print("\n".join(map(lambda slug: f"* {slug}", resultados["slugs"])))

print("\n Cadena de nombres en orden alfabético:")
print(resultados["cadena_ordenada"])