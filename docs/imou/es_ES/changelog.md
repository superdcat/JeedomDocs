# Registro de cambios del plugin IMOU

>**IMPORTANTE**
>
>Si no hay información sobre la actualización, es que solo se refiere a una actualización de documentación, de traducción o de texto.

# 1.0

Primera versión completa, por dominio funcional:

- **Base**: configuración (appId/appSecret/datacenter cifrados), prueba de conexión, descubrimiento y
  sincronización de cámaras (personalizaciones conservadas, sincronización selectiva por comando).
- **Control**: encendido/apagado, vigilancia (detección de movimiento), foco/luz, sirena (a través del
  modelo IoT «Things»), PTZ (almohadilla direccional + zoom), visión nocturna, ajustes de imagen
  (volteo, WDR, OSD, LED).
- **Video e imágenes**: transmisión en vivo (imágenes del directo), visualización a pantalla completa, página «panel de cámaras»,
  miniatura de cámara (fuente a elegir).
- **Alarmas y detección**: último evento (movimiento/persona), sensibilidad de detección, planes de
  armado (preajustes), detección humana/IA.
- **Gestión de dispositivos**: visualización del código de modelo (solo código técnico), reinicio, seguimiento de
  batería y activación de dispositivos en reposo.
- **Control de acceso**: timbre de video, apertura de puerta (hardware compatible).
- **Almacenamiento**: estado de la tarjeta SD (presencia, uso, capacidad) + formateo; estado del abono
  cloud (solo lectura, desactivado por defecto — activar si tiene un abono cloud IMOU).
- **Supervisión y robustez**: estado en línea / salud, gestión de errores y reintentos,
  estadísticas y cuota de llamadas con alerta, regulación automática de la frecuencia de actualización,
  estimación del consumo de datos de la transmisión en vivo.

# 0.1

- Versión inicial (en desarrollo).
