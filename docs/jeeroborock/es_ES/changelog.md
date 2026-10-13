# Changelog JeeRoborock

>**IMPORTANTE**
>
>Si no hay información sobre la actualización, es porque esta se refiere únicamente a una actualización de documentación, de traducción o de texto.

El plugin está en versión **0.x**. Se desarrolla y se prueba en un **Roborock Qrevo Curv**
(protocolo V1): las funcionalidades siguientes son operativas en este equipo, y deberían serlo
también en los demás robots V1 de la cuenta, ya que cada orden solo se crea si el robot declara la
capacidad correspondiente.

El plugin respeta las **cuotas de la nube de Roborock**, compartidas con la aplicación móvil: el
descubrimiento de los robots y las sincronizaciones (usos, habitaciones, mapas) se hacen **a
demanda**, y ningún intento de conexión se relanza automáticamente.

## Lo que es funcional

**Cuenta e instalación**

- Instalación de la dependencia `python-roborock` y demonio dedicado, con supervisión de su estado.
- Autenticación en la nube de Roborock mediante **código de un solo uso recibido por correo
  electrónico**: no se solicita ni se almacena ninguna contraseña.
- Botón « Probar la conexión », estado de la cuenta mostrado en la página de configuración, y
  mensaje explícito « Reautenticación requerida » cuando se pierde la
  sesión.

**Dispositivos y estados**

- Descubrimiento de los robots de la cuenta y creación de un dispositivo por robot, ilustrado con la
  foto del modelo. Un robot nunca corresponde más que a un único dispositivo Jeedom: cualquier
  intento de duplicación se rechaza con un mensaje explícito.
- Información reportada: estado, batería, en limpieza, error (etiqueta y código), superficie
  limpiada, duración de limpieza, avance, en línea, conectado, última actualización.
- Estación de carga: vaciado de polvo, lavado de mopa, secado de mopa, error de estación, falta de
  agua.
- Consumibles: desgaste restante en % para el cepillo principal, el cepillo lateral, el filtro, los
  sensores y el rodillo de mopa.
- Ajustes habituales en lectura: potencia de aspiración, caudal de agua, ruta de mopa, modo de
  limpieza.
- Un robot apagado o sin Wi-Fi no bloquea a los demás robots de la cuenta: se muestra fuera de línea y
  vuelve a ser controlable por sí solo (6 minutos como máximo tras su regreso).
- Actualización **en tiempo real** por el demonio (30 s en limpieza, 60 s en reposo), y cambio a
  « desconectado » si el dato envejece.
- Mosaico del panel de control (escritorio y móvil) que reúne foto, estado, batería y acciones de
  control.

**Control**

- Acciones básicas: Iniciar, Pausar, Detener, Volver a la base, Localizar, Actualizar.
- Rutinas (« usos ») definidas en la aplicación móvil: una orden de acción por uso, gestionadas
  desde el panel « Rutinas » de la pestaña Dispositivo (lista de usos conocidos, sincronización a
  demanda).
- Ajustes: potencia de aspiración, caudal de agua, ruta de mopa, modo de limpieza.
- Mantenimiento en la estación: lavar la mopa, secarla, detener el secado, vaciar el depósito.
- Limpieza por habitación (una orden por habitación, más una orden genérica por nombres), limpieza
  de una zona rectangular y desplazamiento hacia un punto.
- Reinicialización del contador de desgaste de cada consumible, con confirmación.

**Mapa**

- Inventario de las habitaciones nombradas y de los mapas memorizados (plantas), cambio de mapa
  activo, desde la pestaña Dispositivo. Un cambio de planta hecho desde la aplicación móvil también
  se sigue automáticamente, sin acción por tu parte.
- Panel « Mapa » (menú **Inicio**) accesible a los usuarios no administradores: imagen del mapa,
  fecha de la última actualización, leyenda de las habitaciones, actualización automática.

**Registro, estadísticas y programaciones**

- Última limpieza (inicio, duración, superficie, motivo de fin, error) y panel de historial de las
  10 últimas limpiezas, con botón de actualización. La última limpieza también se actualiza sola tras el
  fin de una limpieza.
- Cuatro contadores acumulados historizados por defecto: duración total, superficie total, número
  de limpiezas, número de vaciados del depósito.
- Programaciones creadas en la aplicación móvil, consultables en solo lectura desde la pestaña
  Dispositivo.

**Documentación**

- Página de ayuda completa del plugin: instalación, vinculación de la cuenta, dispositivos y
  órdenes, usos, mapa, control detallado, reautenticación, cuotas y guía de resolución de problemas.
  Disponible en francés, inglés, alemán y español.

**Diagnóstico y soporte**

- Informe de diagnóstico generado con un clic desde la configuración del plugin, sin ningún dato
  sensible, para copiar o descargar para una solicitud de asistencia.

## Lo que no está previsto

El plugin no muestra el canal utilizado para contactar con cada robot (conexión local o nube), y no
sigue ni actualiza el firmware: estas dos funciones se han descartado. La actualización del firmware
se hace desde la aplicación Roborock.

# 13/10/2026

- Añadido: modo « No molestar » controlable desde Jeedom cuando el robot lo admite: activado o no, horas de inicio y de fin de la franja, y tres acciones « Activar », « Desactivar » y « Definir la franja » (inicio y fin en formato HH:MM, utilizable en escenarios); la visualización muestra lo que el robot ha guardado realmente <!-- UC54 -->
- Documentación: el apartado « Ajustes del aparato » describe el modo « No molestar » (documentación en francés) <!-- UC54 -->
- Añadido: recarga en horas valle controlable desde Jeedom cuando el robot la admite: activada o no, inicio y fin de la franja, y tres acciones « Activar », « Desactivar » y « Definir la franja » (HH:MM, utilizable en escenarios); el robot solo retrasa su recarga, una limpieza solicitada no se bloquea <!-- UC55 -->
- Documentación: el apartado « Ajustes del aparato » describe la recarga en horas valle (documentación en francés) <!-- UC55 -->
- Añadido: volumen de los avisos de voz del robot mostrado en porcentaje y ajustable de 0 a 100 desde Jeedom cuando el robot lo admite: información « Volumen » y control deslizante « Ajustar el volumen », utilizable en escenarios; el valor mostrado es el releído en el robot <!-- UC56 -->
- Documentación: el apartado « Ajustes del aparato » describe el volumen (documentación en francés) <!-- UC56 -->
- Añadido: modos de la base visibles y ajustables desde Jeedom cuando la base los ofrece: información « Modo de vaciado » y « Modo de lavado de la mopa », listas « Ajustar el modo de vaciado » y « Ajustar el modo de lavado », utilizables en escenarios; el modo mostrado es el releído en el robot <!-- UC57 -->
- Documentación: el apartado « Ajustes del aparato » describe los modos de vaciado y de lavado de la base (documentación en francés) <!-- UC57 -->
- Añadido: la limpieza de estancias por nombre y la limpieza de zona aceptan un número de pasadas (1, 2 o 3) en su campo « Título », para pasar dos o tres veces por una estancia o una zona; sin valor, una sola pasada como antes, y el ajuste de repetición de la aplicación Roborock nunca se modifica <!-- UC58 -->
- Documentación: el capítulo « Control fino » explica el número de pasadas de la limpieza por estancia y por zona, y la resolución de problemas sus dos mensajes de rechazo (documentación en francés) <!-- UC58 -->
- Añadido: nueva información « Habitación actual »: el nombre de la estancia donde se encuentra el robot, deducido de su posición en el mapa, sin llamada adicional al robot ni a la nube; vale « Aucune pièce » (ninguna estancia) fuera de toda estancia y « Pièce inconnue » (estancia desconocida) cuando la posición o el mapa no se conocen, y un escenario solo se activa ante un cambio real de estancia <!-- UC60 -->
- Corrección: la imagen del mapa ya no se queda fija en la posición anterior cuando el robot vuelve a su base poco después de la última lectura: se vuelve a leer en el minuto siguiente <!-- UC60 -->
- Documentación: el apartado « Mapa y estancias » describe la información « Habitación actual », sus valores y su retraso, y la resolución de problemas cubre el caso en que se queda en « Pièce inconnue » (documentación en francés) <!-- UC60 -->
- Documentación: nueva sección «Comandos según el modelo» (por qué falta un comando y cómo hacerlo aparecer), formatos de entrada de las franjas horarias y del número de pasadas, ejemplos de escenario para los consumibles y depósitos de la estación, el bloqueo infantil, no molestar, las horas valle, el volumen, los modos de la estación, el número de pasadas y la habitación actual; limitaciones conocidas y solución de problemas completadas (por ahora solo en la página en francés). <!-- UC119 -->
- Añadido: la página «Mapa» muestra un panel de control junto al mapa: elección del robot (recordada en el navegador), pestañas Total, Habitación y Zona (rectángulo dibujado en el mapa), ajustes de potencia de aspiración, caudal de agua y recorrido con solo los valores del robot, un gran botón de inicio y luego pausa, reanudar, parar y volver a la base sin salir de la página; un usuario sin derecho de ejecución lo ve todo en gris, y no se envía ninguna petición adicional a la nube <!-- UC61 -->
- Documentación: el apartado del panel «Mapa» describe el panel de control: pestañas, ajustes, botones, robot desconectado, derechos y memorización del robot elegido (documentación en francés) <!-- UC61 -->
- Añadido: en la página «Mapa», los nombres de las habitaciones se muestran en el mapa y tocar o hacer clic en una habitación la marca en la pestaña Habitación; las zonas prohibidas y paredes virtuales definidas en la aplicación Roborock se dibujan en solo lectura; el rectángulo de la pestaña Zona se puede mover, redimensionar por una esquina y borrar antes de iniciar, y se conserva cuando el mapa se actualiza <!-- UC62 -->
- Documentación: el apartado del panel «Mapa» describe el mapa interactivo: nombres y selección de habitaciones en el mapa, habitaciones no seleccionables o desconocidas, zona desplazable y redimensionable, zonas prohibidas en solo lectura (documentación en francés) <!-- UC62 -->
- Añadido: la página «Mapa» incorpora una pestaña «Estación y mantenimiento»: vaciar el depósito, lavar y secar la mopa, ajustar los modos de vaciado y lavado, seguir el estado de la estación, de los depósitos de agua y el desgaste de los consumibles, con una alerta cuando hay que cambiar una pieza o la estación señala una incidencia; solo aparecen las funciones de su robot, y una operación ya en curso no se puede volver a lanzar <!-- UC63 -->
- Documentación: el apartado del panel «Mapa» describe la pestaña «Estación y mantenimiento»: bloques, robot sin estación, operación en curso, robot desconectado y derechos (documentación en francés) <!-- UC63 -->
- Añadido: nueva acción «Aspirar y luego fregar» en el panel «Mapa» y en escenarios: el robot solo aspira y luego vuelve a pasar solo fregando, en toda la vivienda o en las habitaciones elegidas, espera a estar de nuevo listo en la base entre las dos pasadas, muestra en qué punto está la secuencia, se puede cancelar en cualquier momento y recupera después sus ajustes de origen; la segunda pasada nunca se lanza si la primera se detuvo o terminó mal <!-- UC64 -->
- Documentación: la documentación describe la acción «Aspirar y luego fregar»: panel, comandos de escenario, espera entre pasadas, cancelación, motivos de fin y límites (documentación en francés) <!-- UC64 -->
- Añadido: la página «Mapa» gana una pestaña «Cronología del día»: una línea de tiempo por horas para cada robot muestra lo que hizo (limpieza, regreso a la base, carga, vaciado, lavado, secado, error, sin conexión), resalta las limpiezas terminadas y marca como «Desconocido» los periodos sin datos; los últimos 7 días siguen disponibles, sin consumir cuota <!-- UC65 -->
- Documentación: la documentación describe la pestaña «Cronología del día»: leyenda, periodos «Desconocido», limpiezas resaltadas, navegación, conservación y limitaciones (documentación en francés) <!-- UC65 -->

# 12/10/2026

- Corrección: un robot apagado, sin batería o sin Wi-Fi ya no impide controlar los demás robots de la cuenta: se muestra sin conexión, sus intentos de reconexión ya no consumen la cuota de Roborock y vuelve a ser controlable por sí solo en los 6 minutos siguientes a su regreso. <!-- UC44 -->
- Documentación: nuevo apartado « Varios robots en la misma cuenta » en « Tiempo real y actualidad » (documentación en francés). <!-- UC44 -->
- Corrección: cambiar la potencia de aspiración, el caudal de agua, el recorrido de la mopa o el modo de limpieza ya no indica por error « no aplicado » cuando el robot, por ejemplo en su base, toma el ajuste unos segundos más tarde: el plugin le deja ahora hasta unos doce segundos antes de concluir, sin ralentizar la respuesta cuando el ajuste se toma de inmediato. <!-- UC45 -->
- Documentación: el apartado « Control fino » explica la verificación de los ajustes tras el envío y se precisa la entrada de resolución de problemas « no aplicado » (documentación en francés). <!-- UC45 -->
- Corrección: una orden de limpieza (Iniciar, limpieza por habitación o por zona, desde el panel o desde un escenario) enviada mientras la base vacía el depósito de polvo ya no se anuncia como transmitida cuando el robot la ignora: se rechaza con un mensaje que invita a reintentarlo cuando termine el vaciado <!-- UC46 -->
- Documentación: la sección «Estado y control básico» y la tabla de solución de problemas explican por qué se rechaza una orden de limpieza durante el vaciado del depósito <!-- UC46 -->
- Corrección: los comandos « Última limpieza » vuelven a actualizarse por sí solos después de cada limpieza, normalmente en pocos minutos: si el robot aún no ha registrado la limpieza o no responde (lavado de la mopa, vaciado), el plugin vuelve a leer su registro hasta cinco veces en 30 minutos, sin consumir cuota de Roborock. <!-- UC47 -->
- Documentación: apartado « Registro de limpiezas »: plazos de la actualización automática de la última limpieza (documentación en francés). <!-- UC47 -->
- Corrección: los nombres de mapas que algunos robots envían codificados (S7: «%20» en lugar de espacios, «%E9» en lugar de «é») se muestran ahora en claro; para un robot ya configurado, haga clic una vez en «Actualizar la lista de mapas» en la pestaña Equipo. <!-- UC48 -->
- Evolución: la ficha del plugin indica ahora la licencia GPL v3 o posterior (texto oficial incluido) y exige Jeedom 4.4.7 como mínimo, la primera versión que instala las dependencias Python del plugin en un entorno propio; en Jeedom 4.4, el mosaico del robot se muestra con el icono del plugin. <!-- UC50 -->
- Documentación: versión mínima de Jeedom (4.4.7) y licencia (GPL v3 o posterior), robot desconectado cuando hay varios robots en la cuenta, ajustes confirmados tras un breve retraso, orden de limpieza rechazada durante el vaciado del depósito, actualización automática de la última limpieza, nombres de mapas legibles; limitaciones conocidas y solución de problemas completadas. <!-- UC109 -->
- Añadido: los consumibles de la estación aparecen como porcentaje de desgaste restante (filtro de la estación, cepillo de limpieza, bolsa de polvo, según la estación); el filtro y el cepillo se reinician tras confirmación, la bolsa de polvo es de solo lectura <!-- UC51 -->
- Documentación: el apartado « Estación de carga, consumibles y mantenimiento » describe los consumibles de la estación (documentación en francés) <!-- UC51 -->
- Añadido: tres informaciones sí/no utilizables en escenarios, creadas solo si el robot y su estación las admiten: « Depósito de agua limpia vacío », « Depósito de agua sucia lleno o ausente » y « Mopa instalada » <!-- UC52 -->
- Documentación: el apartado « Estación de carga, consumibles y mantenimiento » describe el estado de los depósitos de agua y de la mopa (documentación en francés) <!-- UC52 -->
- Añadido: bloqueo infantil controlable desde Jeedom cuando el robot lo admite: una información sí/no « Bloqueo infantil » utilizable en escenarios y dos acciones « Activar el bloqueo infantil » / « Desactivar el bloqueo infantil »; el estado mostrado es el releído en el robot <!-- UC53 -->
- Documentación: el nuevo apartado « Ajustes del aparato » describe el bloqueo infantil (documentación en francés) <!-- UC53 -->

# 01/10/2026

- Corrección: el botón «Sincronizar rutinas» de la pestaña Equipo ya no se queda sin efecto: al pulsarlo se vuelve a lanzar la sincronización, y el equipo se vuelve a mostrar por sí solo cuando se han añadido o eliminado rutinas. <!-- UC35 -->

# 29/09/2026

- Corrección: la limpieza de una estancia (botón «Limpiar» de una estancia o comando por nombres) ya no termina con «Error interno del demonio»: vuelve a enviarse al robot. Si una estancia solicitada no se reconoce, el plugin aconseja ahora volver a sincronizar las estancias. <!-- UC24 -->

# 24/09/2026

- Corrección: el informe de diagnóstico vuelve a incluir la parte técnica proporcionada por el demonio: ya no muestra «Diagnóstico del demonio no disponible: informe parcial» cuando el demonio funciona. El nivel de log y el historial de errores del robot también se indican correctamente. <!-- UC30 -->

# 23/09/2026

- Corrección: el botón « Iniciar » ahora reanuda una limpieza puesta en pausa en lugar de relanzar un ciclo completo, incluso en una limpieza por habitación o por zona.
- Corrección: ahora se reconoce una sesión Roborock caducada también durante la sincronización de los usos, su ejecución, la lectura de las habitaciones y la prueba de conexión: el plugin muestra « Reautenticación requerida » en lugar de un error genérico. <!-- UC36 -->
- Añadido: nuevo informe de diagnóstico en la configuración del plugin: estado del demonio, de la cuenta y de los robots, versión de python-roborock y errores recientes, sin ningún identificador, token, número de serie ni dirección de correo electrónico, para copiar o descargar con un clic. <!-- UC30 -->
- Documentación: la documentación del plugin explica cómo generar y transmitir un informe de diagnóstico para una solicitud de asistencia. <!-- UC30 -->
- Documentación: la documentación precisa que el plugin sigue dependiendo de la nube de Roborock incluso cuando se intenta una conexión local al robot, indica qué hay que adjuntar a una solicitud de ayuda y qué nunca hay que publicar, y completa la guía de resolución de problemas del informe de diagnóstico. <!-- UC59 -->
- Evolución: los usos tienen su panel « Rutinas » en la pestaña Dispositivo del robot: lista de usos conocidos, botón de sincronización y regla mostrada antes del clic; un uso eliminado en la aplicación Roborock ahora se elimina de Jeedom en lugar de marcarse como obsoleto, y el resumen lo nombra. <!-- UC35 -->
- Corrección: un nombre de uso personalizado en Jeedom ya no es sobrescrito por el nombre de la aplicación Roborock en la segunda sincronización. <!-- UC35 -->
- Documentación: sección de los usos reescrita (panel « Rutinas », regla de sincronización, casos en los que no se elimina nada). <!-- UC35 -->
- Documentación de los usos completada: cuándo lanzar su sincronización, lo que cuesta (ninguna cuota), qué ocurre en caso de fallo, y recordatorio de que el botón de sincronización de dispositivos no sincroniza los usos. <!-- UC89 -->
- Corrección: un cambio de planta hecho desde la aplicación móvil Roborock ahora es detectado por Jeedom en un minuto: el mapa activo se actualiza, y la lista de habitaciones, la imagen y el sistema de coordenadas de la planta anterior se invalidan como en un cambio hecho desde Jeedom. <!-- UC38 -->
- Documentación: la documentación describe el seguimiento automático de un cambio de planta hecho desde la aplicación móvil y sus límites restantes. <!-- UC38 -->
- Corrección: el nombre de una orden de habitación que contiene un apóstrofo, un ampersand, una almohadilla o un porcentaje ahora sigue los renombrados hechos en la aplicación Roborock, conservando a la vez un nombre personalizado en Jeedom. <!-- UC39 -->
- Corrección: un robot ya no puede asociarse a dos dispositivos Jeedom: el botón « Duplicar » se retira y cualquier intento se rechaza con un mensaje que nombra el dispositivo existente. <!-- UC39 -->
- Corrección: los nombres largos y acentuados de habitaciones, usos, mapas y robots ya no se cortan a mitad de un carácter. <!-- UC39 -->
- Documentación: la documentación precisa que un robot corresponde a un único dispositivo Jeedom y que el nombre de las órdenes de habitación sigue los renombrados hechos en la aplicación. <!-- UC39 -->
- Corrección: el indicador « En línea » ahora sigue realmente la pérdida y el retorno de conexión del robot, un error de estación desconocido se muestra como « Erreur de station non reconnue » (Error de estación no reconocido) en lugar de « Aucune » (Ninguno), y los campos no enviados por el robot (estación, superficie, avance) ya no quedan fijos cuando el robot envía muchas actualizaciones. <!-- UC40 -->
- Documentación: la documentación ahora distingue los indicadores « En línea » y « Conectado » y menciona la etiqueta « Erreur de station non reconnue » (Error de estación no reconocido). <!-- UC40 -->
- Evolución: endurecimiento interno: el plugin rechaza una actualización anormalmente voluminosa proveniente de su demonio, el archivo fuente del formulario de configuración ya no es accesible desde la web, el demonio señala al arrancar una versión no validada de la biblioteca de renderizado de mapas o un registro no limitado de la biblioteca Roborock, y la ventana de ejemplo heredada de la plantilla de plugin se retira. <!-- UC41 -->
- Corrección: dos clics seguidos (o dos pestañas) en un mismo botón de sincronización — usos, habitaciones, mapas, imagen de mapa, registro, programaciones — ya no pasan ambos: el segundo se rechaza con el mensaje habitual de solicitud demasiado próxima. <!-- UC42 -->
- Documentación: se completan las limitaciones conocidas (mapa ilegible solo con conexión local, habitaciones legibles únicamente con el robot en línea, vista de mapa no actualizada en reposo, sin vista de mapa en móvil, órdenes del mosaico vueltas a mostrar nunca vueltas a ocultar, historización del error reactivada tras una actualización antigua), la resolución de problemas cubre el fallo parcial de una sincronización de usos, y el resumen de funcionalidades cita el panel « Rutinas » y el seguimiento de un cambio de planta hecho en móvil. <!-- UC99 -->
- Documentación: la página de ayuda y el changelog ahora están disponibles en inglés, en alemán y en español. <!-- UC99 -->
- Corrección: mosaico del robot: el aviso de un consumible que hay que sustituir indica ahora cuál (cepillo principal, filtro, sensores…). <!-- UC15 -->

# 22/09/2026

- Evolución: en la página de configuración del plugin, el código de conexión ahora se introduce justo debajo de la dirección de correo electrónico, antes del estado de la cuenta, en el orden en que se desarrolla el procedimiento. <!-- UC04 -->
- Evolución: un recordatorio indica que hay que guardar la configuración tras introducir el correo electrónico, antes de solicitar un código. <!-- UC04 -->
- Documentación: página de ayuda completa del plugin — instalación, vinculación de la cuenta Roborock mediante código por correo, dispositivos y órdenes, usos, mosaico del panel de control, mapa y habitaciones, control detallado, tiempo real, reautenticación, cuotas de Roborock y guía de resolución de problemas. <!-- UC49 -->
- Añadido: la última limpieza (inicio, duración, superficie, motivo de fin y error eventual) ahora se reporta en el dispositivo, con un historial de las 10 últimas limpiezas consultable desde la página del robot y un botón para actualizarlo. <!-- UC26 -->
- Documentación: la documentación del plugin describe el registro de limpiezas: la información reportada, el panel de historial y la regla del botón de actualización. <!-- UC26 -->
- Añadido: cuatro estadísticas acumuladas por robot (duración total de limpieza, superficie total limpiada, número de limpiezas, número de vaciados del depósito), historizadas por defecto para seguir su evolución en el tiempo. <!-- UC27 -->
- Documentación: la documentación del plugin describe las estadísticas acumuladas: los cuatro contadores, su historización por defecto y el comportamiento tras una puesta a cero desde la aplicación Roborock. <!-- UC27 -->
- Añadido: las programaciones de limpieza definidas en la aplicación Roborock son consultables desde Jeedom, en solo lectura: recurrencia y estado activo o inactivo de cada una. <!-- UC28 -->
- Documentación: la guía de resolución de problemas de la página de ayuda cubre ahora todos los mensajes que requieren una acción por tu parte: cuenta no vinculada, dirección de correo rechazada, plazo superado, robot ocupado, ajuste no disponible en el robot y cambio de mapa demasiado próximo. <!-- UC49 -->

# 21/09/2026

**Documentación**

- La documentación y el changelog se publican en
  [jeedomdocs.decastro.fr/jeeroborock](https://jeedomdocs.decastro.fr/jeeroborock/).
- Changelog único para todas las versiones: se suprime el changelog « beta ».

**Mapa y habitaciones**

- Inventario de las **habitaciones nombradas** de la cuenta, con correspondencia hacia los segmentos
  del robot, en un panel « Habitaciones » de la pestaña Dispositivo.
- **Mapas múltiples (plantas)**: lista de mapas memorizados, mapa activo y cambio de mapa. Un cambio
  de mapa invalida la lista de habitaciones y la imagen, que se resincronizan.
- **Imagen del mapa** obtenida y actualizada automáticamente por el demonio.
- Nuevo panel **« Mapa »** (menú Inicio), primera superficie del plugin accesible a los usuarios no
  administradores: imagen del mapa, marca de tiempo, leyenda de las habitaciones y actualización cada
  30 segundos. La imagen ya no se sirve por URL directa: cada acceso verifica los derechos del
  usuario sobre el dispositivo.

**Control detallado**

- **Potencia de aspiración**: información y orden de ajuste, limitada a los niveles realmente
  soportados por el robot.
- **Caudal de agua** de la mopa: información y orden de ajuste.
- **Ruta de mopa** y **modo de limpieza** (solo aspiración, solo lavado, aspiración y lavado):
  información y órdenes de ajuste.
- **Mantenimiento en la estación**: « Lavar la mopa », « Secar la mopa », « Detener el secado »,
  « Vaciar el depósito ». Estas acciones solo se crean si la estación lo permite, y se rechazan con
  un mensaje claro si el robot no está en su base.
- **Limpieza por habitación**: una orden por habitación de la vivienda, más una orden genérica
  « Limpiar habitaciones (nombres separados por comas) ». Las órdenes siguen el renombrado de las habitaciones en la aplicación móvil.
- **Limpieza de una zona** (x1,y1,x2,y2 en mm) y **desplazamiento hacia un punto** (x,y en mm), con
  validación de las coordenadas antes de enviarlas al robot.

**Identidad visual**

- Icono del plugin derivado del logo de Roborock.

# 20/09/2026

- **Errores detallados**: etiqueta de error en francés, código asociado, valor « Aucune » (Ninguno)
  cuando el robot no señala nada, e historización del error. Un error que la biblioteca no conoce ya
  no se presenta como « ninguna anomalía ».
- **Mosaico del panel de control** del robot (escritorio y móvil): foto, estado, indicador de
  batería y las cinco acciones de control, sin ninguna llamada a la nube al mostrarlo. Las órdenes
  retomadas por el mosaico se ocultan pero siguen siendo ejecutables por los escenarios, vistas y
  diseños.
- **Foto del robot** como ilustración del dispositivo (lista de dispositivos y página de
  configuración).
- Correcciones en el reporte de los eventos.

# 19/09/2026

- **Tiempo real**: el demonio lleva la cadencia de actualización (30 s en limpieza, 60 s en reposo)
  y recibe las actualizaciones enviadas por el robot. El cron de Jeedom se convierte en un vigilante
  de actualidad y pasa el robot a « desconectado » más allá de 3 minutos sin datos.
- **Robustez y reautenticación**: estado « Reautenticación requerida » explícito y persistente, temporizaciones progresivas en las sondas y en el reinicio del
  demonio, y endurecimiento del registro (ningún secreto en los logs, sea cual sea el nivel).
- **Consumibles**: desgaste restante en % para los cinco consumibles realmente reportados por el
  robot, y una acción de reinicialización por consumible.
- **Estado de la estación de carga**: vaciado de polvo, lavado de mopa, secado de mopa, error de
  estación y código asociado, falta de agua. Esta información solo se crea si la estación la expone.
- Correcciones del demonio: arranque, envío del código por correo electrónico, adición de un
  dispositivo.

# 18/09/2026

- **Puente PHP hacia el demonio**: canal local único, con traducción al francés de los códigos de
  error del demonio.
- **Autenticación** en la nube de Roborock mediante código de un solo uso recibido por correo
  electrónico.
- Botón **« Probar la conexión »** y visualización del estado de la cuenta en la página de
  configuración del plugin.
- **Descubrimiento de los robots** de la cuenta y creación de un dispositivo por robot.
- **Órdenes de información**: estado, batería, en limpieza, error, superficie limpiada, duración de
  limpieza, avance, en línea, conectado, última actualización.
- **Órdenes de acción**: Iniciar, Pausar, Detener, Volver a la base, Localizar, Actualizar.
- **Rutinas (« usos »)**: sincronización de los usos definidos en la aplicación móvil y una orden de
  acción por uso. Pasan por la nube de Roborock, por lo que funcionan incluso cuando el robot no es
  accesible en directo.

# 17/09/2026

- Primera versión: página de configuración del plugin (correo electrónico de la cuenta Roborock,
  puerto del canal local del demonio), instalación de la dependencia `python-roborock` y ciclo de
  vida del demonio.
