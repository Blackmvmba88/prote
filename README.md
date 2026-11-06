# 🐍 BlackMamba Motion Lab

**Motor universal de movimiento · Síntesis de mecanismos · Robótica adaptativa**

**Estado:** investigación conceptual, fase inicial.  
**División:** BlackMamba Corp / BlackMamba LABS.

> Investigar sistemas nuevos para distribuir, sincronizar, adaptar y recuperar movimiento y energía, antes de fabricar hardware.

## Visión

Un laboratorio de captura de movimiento que **empieza en un celular** (cámara, giroscopio, acelerómetro y reloj) y evoluciona hacia la generación computacional de mecanismos. El objetivo es evaluar diseños reutilizables para robótica industrial, educación, prótesis, exoesqueletos y asistencia funcional. No asumimos que un único diseño sirva físicamente para todos los casos.

## Arquitectura propuesta

```text
TELÉFONO
 Cámara + anclajes fijos ─┐
 IMU + reloj sincronizado ├─> Captura y calibración
                         └─> Fusión de sensores
                                   |
                          Firma de movimiento
                                   |
                      Generador de mecanismos
                                   |
                  Simulación física y multifísica
                                   |
                   Optimización multiobjetivo
                                   |
                   Validación, métricas y reporte
                                   |
                  Prototipos físicos (fase futura)
```

## Investigación

1. **Firma inercial y anclajes:** referencias fijas en el espacio, trayectoria, fases y repetibilidad de la marcha o gestos.
2. **Distribución cinemática:** engranes diferenciales, tendones, bielas, levas y mecanismos subactuados; buscar menos actuadores sin perder funciones requeridas.
3. **Manos robóticas:** comparar transmisión rígida, tendones y microhidráulica híbrida, incluidas tareas funcionales de mano y brazo.
4. **Termofluidos:** comparar circuitos convencionales, válvulas antirretorno y canales Tesla; medir caudal, pérdidas, rectificación y potencia de bombeo. Una válvula Tesla no regula activamente presión.
5. **Rodilla, tobillo y pie:** estudiar fases de marcha, impacto, estabilidad, amortiguación y almacenamiento elástico de energía.
6. **Aplicaciones:** manufactura, robótica educativa, asistencia funcional, prótesis y exoesqueletos, cada uno con validaciones específicas.

## Experimentos propuestos

### BM-EXP-001 · Celular como laboratorio

**Hipótesis:** referencias visuales fijas y una IMU reducen deriva respecto a una estimación exclusivamente inercial, cuando los marcadores son visibles.

**Procedimiento:** calibrar cámara y sensores, registrar 10 repeticiones, conservar timestamps y señales crudas, comparar trayectorias con y sin corrección visual. Medir deriva, latencia, error de pose y repetibilidad.

### BM-EXP-002 · Distribución de movimiento en dedos

Comparar virtualmente (A) tres dedos con actuadores independientes, (B) tendones con distribución mecánica y (C) hidráulica + tendones. Mantener mismas cargas, geometrías de referencia y condiciones de contacto. Medir fuerza de agarre, error, energía, masa estimada y éxito frente a perturbaciones.

### BM-EXP-003 · Termofluidos

Simular (A) conducto base, (B) antirretorno mecánico y (C) geometría Tesla, con el mismo fluido y condiciones de frontera. Evaluar caída de presión, rectificación de flujo, potencia consumida y sensibilidad al régimen de operación.

## Criterios técnicos

- Comparar con referencias convencionales antes de afirmar ventajas u originalidad.
- Optimizar trayectoria, fuerza/torque, consumo, masa y número de actuadores con métricas normalizadas y frentes de Pareto.
- Separar **diseño**, **simulación**, **validación experimental** y **uso real**.
- Captura corporal con consentimiento; preferir procesamiento local.
- Sin ensayos sobre personas de prótesis o exoesqueletos durante fases tempranas. Cualquier hardware futuro requiere límites independientes de fuerza, velocidad y presión.

## Hoja de ruta

| Etapa | Entregable | Estado |
|---|---|---|
| 0 | Requisitos y README | Documentado |
| 1 | Captura de cámara/IMU con anclajes | Pendiente |
| 2 | Firma temporal y detección de fases | Pendiente |
| 3 | Simulador cinemático paramétrico | Pendiente |
| 4 | Generador de mecanismos | Pendiente |
| 5 | Simulación hidráulica y térmica | Pendiente |
| 6 | Optimización y validación | Pendiente |
| 7 | Banco físico no vestible | Futuro |

## Estado verificable

Este documento es una **especificación inicial**. No se afirma haber implementado, simulado ni probado el controlador. Las imágenes y sketches compartidos son referencias conceptuales, no planos verificados.

**Siguiente entrega:** modelo de movimiento 2D reproducible con pruebas automáticas y esquema de captura móvil.

---
**BlackMamba Corp · BlackMamba LABS**  
*Movimiento como información. Mecánica como arquitectura. Experimentación como método.*
