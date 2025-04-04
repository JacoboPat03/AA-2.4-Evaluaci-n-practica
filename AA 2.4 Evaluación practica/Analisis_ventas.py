from functools import reduce

# Tipo de cambio abril 2025
TIPO_CAMBIO = 20.46

def analizar_ventas(ventas_mxn):
    promedio_mxn = reduce(lambda x, y: x + y, ventas_mxn) / len(ventas_mxn)
    ventas_usd = list(map(lambda mxn: mxn / TIPO_CAMBIO, ventas_mxn))
    ventas_mayores_150 = list(filter(lambda usd: usd > 150, ventas_usd))
    total_mayores_150 = reduce(lambda x, y: x + y, ventas_mayores_150, 0)

    return {
        'promedio_mxn': promedio_mxn,
        'ventas_usd': ventas_usd,
        'ventas_mayores_150': ventas_mayores_150,
        'total_mayores_150': total_mayores_150
    }

ventas_ejemplo = [1500, 2500, 3200, 4500, 6000, 1200, 8000]
resultados = analizar_ventas(ventas_ejemplo)

print("\n Promedio de ventas en pesos mexicanos:")
print(f"   {resultados['promedio_mxn']:.2f}")

print("\n Ventas de la semana en dólares:")
print("  " + "\n   ".join(map(lambda v: f"{v:.2f}", resultados['ventas_usd'])))

print("\nc. Ventas en dólares mayores a 150:")
print("   " + "\n   ".join(map(lambda v: f"{v:.2f}", resultados['ventas_mayores_150'])))

print("\nd. Suma total de las ventas mayores a 150 USD:")
print(f"  {resultados['total_mayores_150']:.2f}")
