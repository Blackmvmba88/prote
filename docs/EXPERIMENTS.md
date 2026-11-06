# Experimentos iniciales

## BM-EXP-001 — Firma de movimiento móvil

**Estado:** diseñado; captura real pendiente. Medir latencia, sincronización, deriva y repetibilidad de señales IMU/cámara con anclajes fijos. No afirmar reconstrucción corporal completa con cámara monocular.

## BM-EXP-002 — Mecanismos subactuados

**Estado:** base geométrica 2D implementada; dinámica, contacto, hidráulica y generación automatizada pendientes. Primer test computacional: consistencia de cinemática directa e inversa de dos eslabones.

## BM-EXP-003 — Termofluidos

**Estado:** propuesto, sin CFD. Comparativa con condiciones de frontera iguales: ducto base, antirretorno, canal Tesla. Métricas: caída de presión, rectificación, caudal, energía y temperatura.

## Ejecutar pruebas

```bash
python -m unittest discover -s tests -v
```

## Ejecutar ejemplo

```bash
python -m examples.demo
```

Los modelos aquí no son controles aptos para un producto físico, prótesis ni ensayos humanos.
