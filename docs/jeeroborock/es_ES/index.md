# JeeRoborock

JeeRoborock controla tus aspiradoras robot Roborock desde Jeedom, pasando por la nube de Roborock: estado
en tiempo real, órdenes de limpieza, control detallado (aspiración, agua, ruta, mantenimiento de la
estación), limpieza por habitación o por zona, mapas múltiples, y ejecución de las rutinas (« usos »)
definidas en la aplicación móvil Roborock.

## Lo que el plugin hace, y lo que no hace

- El control pasa por la **nube de Roborock**: Jeedom debe tener acceso a Internet, y tu robot debe
  estar conectado a tu red y a la nube de Roborock para responder. Algunas operaciones dependen
  estrictamente de la nube y **no funcionan sin Internet**: la conexión a la cuenta, el inventario de
  los robots, la ejecución de los usos, la lectura de las programaciones y la obtención de la foto del
  robot.
- La biblioteca utilizada por el plugin **puede**, cuando tu robot está en la misma red local que
  Jeedom, intentar una conexión directa al aparato para acelerar ciertos intercambios. Este
  comportamiento no es ajustable ni desactivable desde Jeedom, y no cambia nada de lo anterior: el
  plugin sigue dependiendo de la nube de Roborock para funcionar.
- El plugin está pensado para los robots compatibles con el protocolo **V1** de Roborock. El equipo de
  referencia, sobre el que se prueba todo, es el **Roborock Qrevo Curv**. Otros robots V1 pueden
  funcionar, pero las órdenes disponibles varían según las capacidades que el propio robot anuncia —
  ver más abajo.
- Un robot **compartido** contigo por otra cuenta Roborock aparece normalmente en la lista, pero
  algunas acciones pueden serle rechazadas por la nube de Roborock.

## Requisitos previos e instalación

1. **Jeedom 4.2 como mínimo**, instalado en un servidor con **Debian 12 o 13**. Esta versión de Debian
   es necesaria para que la dependencia del plugin funcione; por debajo (Debian 11 por ejemplo), la
   activación del plugin se rechaza.
2. Desde la página del plugin, deja que Jeedom instale su dependencia Python. El indicador de
   dependencias de la página « Plugins » se pone en verde una vez terminada la instalación; cuenta
   hasta unos quince minutos según la máquina.
3. **Activa el plugin** y después inicia su demonio (la interfaz lo hace automáticamente al activarlo).
   Sin el demonio iniciado, el plugin no puede ni conectarse a Roborock ni releer el estado de un robot:
   la página de configuración lo indica con « El demonio no responde. »

## Vincular tu cuenta Roborock

La autenticación se hace mediante un **código de un solo uso enviado por correo electrónico**: no hay
campo de contraseña, y la contraseña de tu cuenta Roborock nunca se solicita ni se almacena.

Desde la página de configuración del plugin (menú Plugins > JeeRoborock > Configuración):

1. Introduce tu **dirección de correo electrónico** de la cuenta Roborock en el campo « Correo
   electrónico de la cuenta Roborock ».
2. **Guarda la configuración** (botón de guardado de la página) antes de solicitar un código: es ese
   valor guardado el que utiliza el demonio.
3. Haz clic en **« Enviar un código »**. Roborock te envía un código numérico por correo electrónico
   (hasta 12 caracteres).
4. Introduce ese código en el campo previsto y haz clic en **« Validar el código »**.
5. El estado de la cuenta pasa de « Cuenta Roborock no vinculada » a « Cuenta Roborock vinculada ».

Un botón **« Probar la conexión »** permite verificar en cualquier momento que la sesión guardada sigue
siendo válida, sin consumir tu cuota de conexiones.

Lo que el plugin conserva: tu dirección de correo electrónico y un token de sesión cifrado (entregado
por Roborock en el momento de validar el código). La contraseña de tu cuenta, las claves propias de
cada robot y los tokens de sesión en bruto nunca salen del demonio y nunca son visibles desde la
interfaz de Jeedom.

### Canal local con el demonio

El campo **« Puerto del canal local »** (61350 por defecto) es el puerto TCP utilizado en la propia
máquina Jeedom para dialogar con el demonio. Cámbialo solo en caso de conflicto con otro software
instalado en el mismo servidor. El botón **« Comprobar el canal »** confirma que el demonio responde y
que el canal de retorno hacia Jeedom (las actualizaciones espontáneas) funciona.

## Sincronización de los dispositivos

El botón **« Sincronizar dispositivos »**, en la página de inicio del plugin, consulta tu cuenta
Roborock para descubrir tus robots y crear los dispositivos Jeedom correspondientes.

**No** es un botón de actualización: el inventario de los robots vinculados a tu cuenta está sujeto a
una cuota de Roborock estrictamente limitada y compartida con la aplicación móvil (ver más abajo). Haz
clic en este botón solo cuando añadas o retires un robot de tu cuenta Roborock, no para actualizar el
estado de un robot ya conocido — ese estado se actualiza solo (ver « Tiempo real y actualidad »).

Un robot compartido por otra cuenta se identifica con una etiqueta **« Robot compartido »** en su
tarjeta, dentro de la lista de dispositivos.

Este botón **no** sincroniza los usos: un robot recién descubierto todavía no tiene ninguno. Los usos
se sincronizan robot por robot, desde el panel **« Rutinas »** de la pestaña « Dispositivo » (botón
« Sincronizar rutinas », ver « Rutinas (« usos ») » más abajo).

Un robot nunca corresponde más que a **un único dispositivo Jeedom**: la página de configuración de un
dispositivo JeeRoborock no ofrece el botón nativo « Duplicar », y cualquier intento de crear un segundo
dispositivo para un robot ya conocido (incluso por una vía distinta de la interfaz, como la API) se
rechaza, con un mensaje que nombra el dispositivo existente. Si se creó un duplicado antes de esta
protección, no se elimina automáticamente: es cosa tuya eliminar el que de los dos ya no sirve, y se
escribe una advertencia en el registro del plugin para ayudarte a localizarlo.

## Lo que contiene un dispositivo

Cada robot se convierte en un dispositivo Jeedom. La lista de órdenes que porta **depende de las
capacidades que el robot anuncia realmente**: dos robots, incluso de modelos parecidos, no tienen
necesariamente exactamente la misma lista. Una orden ausente significa una capacidad no detectada en
ese robot, no un defecto del plugin.

### Información general

La pestaña « Dispositivo » muestra en solo lectura el modelo, el firmware, la versión de protocolo, el
número de serie, el identificador Roborock y el nombre dado al robot en la aplicación Roborock. Esta
información proviene de la cuenta Roborock y se actualiza mediante la sincronización de los
dispositivos.

### Estado y control básico

| Orden | Lo que indica o hace |
|---|---|
| Estado | La etiqueta del estado actual del robot (limpiando, en pausa, con error…) |
| Batería | Nivel de carga en % |
| En limpieza | Sí/no |
| Error | Etiqueta del error en curso, « Aucune » (Ninguno) en caso contrario |
| Superficie limpiada | En m², para la limpieza en curso |
| Duración de limpieza | En minutos, para la limpieza en curso |
| Avance | En %, para la limpieza en curso |
| En línea / Conectado | « En línea »: el robot respondió a la última relectura (pasa a « fuera de línea » en cuanto una relectura falla por falta de respuesta del robot). « Conectado »: actualidad del dato del lado del plugin (canal con el demonio) |
| Última actualización | Fecha y hora del último dato recibido |
| Iniciar / Pausar / Detener | Control de la limpieza. « Iniciar » **reanuda** una limpieza pausada o interrumpida (incluida una limpieza por habitación o por zona) en lugar de relanzar una nueva; sin limpieza en curso, lanza una limpieza completa |
| Volver a la base | Envía al robot a recargarse |
| Localizar | Hace que el robot emita una señal sonora |
| Actualizar | Relee inmediatamente el estado del robot |

### Estación de carga, consumibles y mantenimiento

Estas órdenes aparecen **solo si tu estación lo permite**:

- estado de vaciado del polvo, de lavado y de secado de la mopa, error de estación, falta de agua. Si
  el código de error notificado por la estación no se reconoce, la etiqueta mostrada es
  « Erreur de station non reconnue » (Error de estación no reconocido; el código bruto sigue siendo
  visible en la orden de código de error de estación);
- acciones correspondientes: lavar la mopa, secar la mopa, detener el secado, vaciar el depósito —
  disponibles únicamente cuando el robot está **en su base** (incluida la carga); fuera de ese estado,
  el plugin rechaza la acción con un mensaje explícito.

El desgaste de los consumibles detectados por tu robot (cepillo principal, cepillo lateral, filtro,
sensores, rodillo de mopa) se publica en porcentaje restante, cada uno con una acción « Reinicializar… »
a utilizar tras una sustitución física. Esta acción pide confirmación antes de ejecutarse.

### Registro de limpiezas

Siete órdenes de solo lectura informan de la **última limpieza** conocida:

| Orden | Lo que indica |
|---|---|
| Última limpieza | Resumen en una línea, por ejemplo « Terminado — 42 min, 31,5 m² »; vale « Aucun nettoyage connu » (Ninguna limpieza conocida) mientras no se haya reportado ninguna limpieza |
| Inicio de la última limpieza | Marca de tiempo del inicio (oculta por defecto) — es la única de las siete que se compara aritméticamente, a utilizar en un escenario del tipo « el robot no ha pasado desde hace tres días » |
| Duración de la última limpieza | En minutos, redondeada al minuto más cercano (posible desviación de ±30 s respecto a la aplicación móvil) |
| Superficie de la última limpieza | En m², redondeada a 0,1 m² |
| Motivo de fin de la última limpieza | Por ejemplo « Terminado » o « Limpieza interrumpida » |
| Clave del motivo de fin de la última limpieza | Valor técnico estable asociado al motivo (oculto por defecto) — preferible a la etiqueta para comprobar una condición en un escenario |
| Error de la última limpieza | Etiqueta del error asociado a esa limpieza, « Aucune » (Ninguno) si todo fue bien |

La pestaña « Dispositivo » también ofrece un panel **« Registro de limpiezas »** que lista las 10
últimas limpiezas conocidas (inicio, fin, duración, superficie, motivo de fin, error), con la fecha de
la última sincronización. Un botón **« Actualizar el registro »** relee este historial en Roborock:

- está protegido por la misma protección antirráfaga de un minuto que los demás botones de
  resincronización del plugin — hacer clic de nuevo demasiado pronto muestra « Le journal vient d'être
  rafraîchi : patientez une minute avant de relancer. » (El registro acaba de actualizarse: espera un
  minuto antes de relanzar);
- la primera actualización puede traer solo unos pocos registros y completarse en el siguiente clic:
  es un funcionamiento normal, no una avería, ya que la recuperación está acotada en el tiempo;
- el registro también se actualiza solo al final de cada limpieza, sin acción por tu parte.

Si la nube de Roborock no está accesible en el momento de la consulta, los valores ya conocidos de la
última limpieza y del historial se siguen mostrando tal cual — nunca se ponen a cero. Es la fecha de
última sincronización del panel la que indica si el dato sigue siendo reciente.

### Estadísticas acumuladas

Cuatro órdenes de solo lectura informan del uso **global** de tu robot desde su puesta en servicio:

| Orden | Lo que indica |
|---|---|
| Duración total de limpieza | En horas, redondeada a la décima |
| Superficie total limpiada | En m², redondeada a la décima |
| Número total de limpiezas | Número entero |
| Número total de vaciados del depósito | Número entero; solo aparece si tu estación sabe vaciar el depósito |

Son contadores **acumulados** llevados por el propio robot, no un cálculo hecho por Jeedom:
corresponden a lo que muestra la aplicación móvil Roborock. A diferencia de la mayoría de las demás
órdenes del plugin, están **historizadas por defecto**, para que puedas seguir una curva de uso en el
tiempo sin necesidad de configuración previa.

Su actualización es automática: al final de cada limpieza, y como mucho una vez por hora en caso
contrario. No hay ningún botón que pulsar, y ninguna consecuencia sobre las cuotas de Roborock — el
dato llega por el mismo canal que el registro de limpiezas anterior.

Si pones estos contadores a cero desde la aplicación Roborock (o tras un reinicio de fábrica), las
órdenes de Jeedom seguirán esa bajada: copian fielmente el robot, no memorizan un máximo. Una caída
visible en el historial tras esa puesta a cero es, por tanto, normal, no una anomalía. Si un valor no
es utilizable en el momento de la lectura (robot inaccesible, dato aberrante), la orden simplemente
conserva su valor anterior en lugar de caer a cero.

### Programaciones de la aplicación

La pestaña « Dispositivo » ofrece un panel **« Programaciones de la aplicación »**, en forma de tabla
(Recurrencia / Repetición / Estado). Esta lista no se rellena sola: haz clic en **« Leer las
programaciones »** para poblarla. Una marca de tiempo bajo la tabla indica la fecha de la última
lectura; sin un clic previo, la tabla invita a hacer clic en el botón.

Cada fila corresponde a una programación creada en la aplicación móvil Roborock e indica:

- su **recurrencia**, mostrada **tal como la devuelve la nube**, sin traducirla a días de la semana ni
  a una hora legible. No es un defecto de visualización: la forma exacta de esta información no está
  garantizada como idéntica según los modelos de robot, así que el plugin la muestra en bruto en lugar
  de arriesgarse a una interpretación errónea;
- si está **repetida** o no (Sí / No);
- si está **Activa** o **Desactivada**.

Esta lectura es **solo eso**: no es posible crear, modificar ni eliminar ninguna programación desde
Jeedom. Todo se gestiona en la aplicación Roborock, que sigue siendo la única fuente de verdad. Tras
una modificación hecha en la aplicación móvil (desactivación, cambio de horario...), vuelve a hacer
clic en « Leer las programaciones » para ver el estado actualizado del lado de Jeedom — no se
actualiza solo.

Dos lecturas con menos de un minuto de diferencia muestran un mensaje invitando a esperar un minuto:
no es un error, es la misma protección antirráfaga que los demás botones de resincronización del
plugin.

Si el panel muestra **« Programaciones no disponibles para este robot. »**, es un resultado normal, no una avería: no todos los modelos de robot
proporcionan esta información a la nube de Roborock. El resto del plugin sigue funcionando con
normalidad en ese caso.

No confundas estas programaciones con las **rutinas (« usos »)** descritas más abajo: las rutinas son
escenarios de limpieza ejecutables a demanda desde Jeedom, las programaciones son activaciones horarias
gestionadas por la aplicación móvil y solo consultables aquí. Estas programaciones no crean ninguna
orden y por tanto no pueden usarse en un escenario Jeedom — es una visualización informativa, una
decisión asumida y no un olvido.

## Rutinas (« usos »)

Los « usos » son las rutinas de limpieza que has creado en la aplicación móvil Roborock. Una vez
sincronizadas, cada una se convierte en una orden de acción en el dispositivo, ejecutable desde Jeedom
como cualquier otra orden, o desde un escenario.

Estas rutinas se ejecutan pasando por la nube de Roborock y por tanto funcionan **incluso si el canal
directo con el robot no está disponible** — solo se necesita una conexión a Internet del lado de
Jeedom y un robot conocido por tu cuenta.

### El panel « Rutinas »

La pestaña « Dispositivo » de un robot incluye una sección **« Rutinas »**, bajo el bloque « Inventario
Roborock ». Muestra:

- la **lista de los usos que Jeedom conoce** para ese robot, uno por línea; cuando el nombre de la
  orden ha sido personalizado en Jeedom, el nombre original en la aplicación Roborock se recuerda en
  una segunda columna, para facilitar la correspondencia;
- el botón **« Sincronizar rutinas »** — es el **único** lugar donde se encuentra, ya no está en la
  barra de herramientas de la página;
- la **regla de sincronización**, recordada claramente antes de cualquier clic: conserva los usos que
  todavía están presentes en la aplicación (mismas órdenes, mismos escenarios), elimina los que ya no
  están, y añade los nuevos.

Si todavía no se conoce ningún uso, el panel lo indica explícitamente en lugar de mostrar una lista
vacía: lanza una sincronización, o crea primero un uso en la aplicación Roborock.

Mostrar este panel no dispara ninguna llamada al demonio ni a la nube de Roborock: la lista proviene
de lo que Jeedom ya sabe, sin consumir cuota.

### Lo que hace una sincronización

- **Uso todavía presente en la aplicación** → nada se toca: misma orden, mismo identificador,
  utilizable de forma idéntica en un escenario. Solo el nombre sigue al de la aplicación si ha
  cambiado — y únicamente si no lo has personalizado en Jeedom, en cuyo caso se conserva tu nombre.
- **Uso desaparecido de la aplicación** (eliminado del lado móvil) → su orden Jeedom se **elimina**.
  ⚠️ Un escenario que lo referenciaba pierde su referencia, sin aviso de Jeedom en el momento en que
  esto ocurre: por eso el resumen mostrado tras la sincronización **nombra** cada uso eliminado, para
  que sepas qué corregir.
- **Uso nuevo en la aplicación** → se añade una orden, sin tocar las demás.

Una orden de uso no se elimina **a mano** desde Jeedom: ocúltala si te molesta, o elimina el uso
correspondiente en la aplicación y luego relanza una sincronización.

Dos sincronizaciones con menos de un minuto de diferencia muestran un mensaje invitando a esperar: no
es un error, es la misma protección antirráfaga que los demás botones de resincronización del plugin.
Una sincronización sin ningún cambio del lado de la aplicación es una operación neutra, y lo indica
(« Sin cambios: sus rutinas ya están actualizadas. »).

Si la lista recibida de la nube de Roborock está **incompleta** (respuesta truncada, o más de 64 usos
en ese robot), la sincronización aplica de todos modos las adiciones y los renombrados, pero **no
elimina nada**: por precaución, una lista incompleta nunca se interpreta como « estos usos han
desaparecido ».

Si actualizas el plugin desde una versión anterior que marcaba ciertos usos como « obsoletos », la
primera sincronización siguiente los elimina, como cualquier uso ausente de la aplicación — ningún uso
puede quedar ya en ese estado de forma duradera.

### Cuándo lanzarla, y lo que cuesta

No hay **ninguna sincronización automática**: un uso creado, renombrado o eliminado en la aplicación
Roborock no aparece (ni desaparece) del lado de Jeedom hasta después de hacer clic en « Sincronizar los
usos ». Lánzala, pues, cada vez que modifiques tus usos en la aplicación.

No consume **ni** la cuota de conexión **ni** la de inventario de aparatos (ver « Cuotas Roborock » más
abajo) — pero dos clics con menos de un minuto de diferencia se rechazan, con una invitación a esperar.

Consejo preventivo: antes de eliminar un uso en la aplicación, localiza los escenarios de Jeedom que
usan su orden. Perderán su referencia en cuanto se produzca la siguiente sincronización.

Si la cuenta no está vinculada, si el demonio está detenido o si se requiere una reautenticación, el
panel sigue mostrando la lista de usos ya conocidos, y el botón muestra un mensaje explícito: en todos
estos casos, **no se elimina ningún uso**.

## Mosaico del panel de control

Cada robot dispone de un mosaico de panel de control que reúne su foto (o, en su defecto, el icono del
plugin), su estado, un indicador de batería y las acciones de control habituales (iniciar, pausa,
detener, volver a la base, localizar).

Las órdenes que el mosaico reúne así ya no aparecen **por separado** en la lista estándar de órdenes
del panel: siguen siendo, no obstante, plenamente utilizables en un escenario, en una vista o en un
diseño personalizado, exactamente como antes. No se eliminan, solo se ocultan de esa visualización
agrupada.

## Mapa y habitaciones

### Paneles de la página del dispositivo

La pestaña « Dispositivo » de un robot ofrece dos paneles adicionales:

- **Habitaciones** — la correspondencia entre los segmentos detectados por el robot y los nombres de
  habitación que has dado en la aplicación Roborock. Un botón **« Resincronizar las habitaciones »**
  relee esta correspondencia; hazlo tras añadir, eliminar o renombrar una habitación del lado de
  Roborock.
- **Mapas** — la lista de mapas memorizados por el robot (útil si tu vivienda tiene varias plantas),
  con el mapa activo, un selector para elegir otro y un botón **« Cambiar de mapa »**. El cambio de
  mapa es una operación lenta (el robot debe recargar el mapa solicitado): el plugin rechaza una nueva
  solicitud de cambio durante dos minutos tras la anterior. **Cambiar de mapa invalida
  automáticamente la lista de habitaciones y la imagen del mapa mostradas**, que luego se
  resincronizan.

La misma pestaña ofrece dos bloques distintos, cada uno con su propio botón:

- **Imagen del mapa** — la imagen del mapa activo, reconstruida automáticamente durante las limpiezas
  (como máximo una vez cada 30 segundos) y actualizable manualmente mediante « Actualizar la imagen
  del mapa ».
- **Zona y punto** — un bloque **puramente informativo** (sin entrada de datos aquí) que muestra el
  sistema de coordenadas del último mapa obtenido: la zona utilizable en milímetros, la posición de la
  base de carga y la del robot en el momento del mapa, así como una ayuda de conversión desde un píxel
  de la imagen. Sirve para preparar los valores a introducir en las órdenes « Limpiar una zona »
  y « Desplazarse a un punto » (ver « Control
  detallado » más abajo), que siguen siendo **órdenes del dispositivo**, no campos de este panel. Sin
  una imagen de mapa obtenida, solo se conocen límites generales.

### Panel « Carte » (Inicio > JeeRoborock)

El mapa es un **panel**, no una página del menú Plugins: se abre desde el menú **Inicio >
JeeRoborock**, y es accesible a cualquier usuario con derechos de lectura sobre al menos un robot (no
solo los administradores). Muestra el mapa activo del robot seleccionado, su marca de tiempo y la
leyenda de las habitaciones detectadas (número de segmento / nombre), y se actualiza automáticamente
cada 30 segundos mientras la página permanece abierta.

Si la entrada no aparece en **Inicio**, comprueba que la casilla **Mostrar panel de escritorio** esté
marcada en la página de gestión del plugin (**Plugins > Gestión de plugins > JeeRoborock**): se marca
automáticamente en la instalación, pero sigue siendo modificable.

## Control detallado

Según las capacidades detectadas en tu robot, pueden aparecer las siguientes órdenes:

- **Potencia de aspiración** y **caudal de agua** — una orden de información indica el nivel actual,
  una orden de acción (lista desplegable) permite elegir otro entre los realmente soportados por tu
  robot.
- **Ruta de mopa** y **modo de limpieza** (solo aspiración / solo lavado / aspiración y lavado) —
  mismo principio: información + lista desplegable de acción.
- **Limpiar habitaciones** — una orden por habitación detectada (« Limpiar <nombre de la habitación> »),
  más una orden genérica « Limpiar habitaciones (nombres separados por comas) » que acepta una lista
  de nombres en texto libre. Como ocurre con los usos, el nombre de la orden sigue los renombrados
  hechos en la aplicación Roborock en la siguiente sincronización — incluso cuando el nombre de la
  habitación contiene un apóstrofo, un ampersand, una almohadilla o un porcentaje (« Aseo », por
  ejemplo) — salvo si has personalizado ese nombre a mano en Jeedom, en cuyo caso se conserva tu
  nombre personalizado.
- **Limpiar una zona** — recibe cuatro coordenadas `x1,y1,x2,y2` en milímetros y limpia el rectángulo
  correspondiente.
- **Desplazarse a un punto** — recibe dos coordenadas `x,y` en milímetros.

Las coordenadas de zona y de punto se expresan en el mismo sistema de referencia que el utilizado para
el mapa (ver « Mapa y habitaciones »).

## Tiempo real y actualidad

Una vez sincronizado un robot, su estado se actualiza automáticamente, sin acción por tu parte:
- cada **30 segundos** durante una limpieza;
- cada **60 segundos** en reposo.

La orden **« Última actualización »** indica la marca de tiempo del dato más reciente recibido.

El indicador **« En línea »** reacciona rápido: pasa a **fuera de línea** en cuanto una relectura
periódica falla por falta de respuesta del robot (en reposo, una relectura ocurre aproximadamente cada
minuto; aproximadamente cada 40 segundos en limpieza), y vuelve a **en línea** en cuanto una lectura
tiene éxito, se recibe una actualización espontánea del robot, o se le confirma una acción. El regreso
a « en línea » puede tardar solo unos segundos (el robot envía una actualización) o, en el peor caso en
que el robot haya permanecido inaccesible mucho tiempo, hasta una decena de minutos (las relecturas se
espacian progresivamente tras varios fallos).

Independientemente de este mecanismo, si **ningún** dato ha podido obtenerse desde hace más de
**3 minutos**, el plugin pasa los dos indicadores « En línea » **y** « Conectado » a **desconectado**:
es una señal de robot inaccesible (apagado, fuera de red, o nube de Roborock no disponible), no un
error del propio plugin.

## Reautenticación requerida

Cuando la sesión guardada en Roborock ha caducado o ha sido revocada, el plugin muestra
« Reautenticación requerida » (mensaje visible en las órdenes afectadas,
y en los intentos de acción).

**El plugin nunca intenta reconectarse por sí solo.** Este paso exige leer un código recibido en tu
buzón de correo, algo que ningún automatismo puede hacer en tu lugar. Para salir de esta situación:

1. Abre la configuración del plugin.
2. Haz clic en **« Enviar un código »**, recupera el código recibido por correo electrónico.
3. Introdúcelo y haz clic en **« Validar el código »**.

Una vez validado correctamente, todo se reanuda con normalidad, sin ninguna otra intervención.

## Cuotas de Roborock

Los servidores de Roborock imponen cuotas **estrictas y compartidas con la aplicación móvil de tu
cuenta**: un número limitado de conexiones por minuto/hora/día, y un número limitado de llamadas de
inventario de tus aparatos en las mismas ventanas de tiempo.

Cuando un mensaje indica que se ha alcanzado una cuota, **espera**: no es un error del plugin, y
reintentarlo de inmediato solo empeora la situación — también penalizarías el uso de la aplicación
móvil en esa misma cuenta, hasta que el contador se reinicie. El plugin nunca relanza automáticamente
un intento tras un rechazo por cuota.

La sincronización y la ejecución de los usos no entran en estas cuotas.

## Resolución de problemas

### Informe de diagnóstico

Antes de pedir ayuda, genera un informe de diagnóstico: desde la **configuración del plugin**, bloque
**« Diagnóstico y soporte »**, haz clic en **« Generar un informe de diagnóstico »**. El informe
aparece en una zona de texto, listo para transmitir.

Reúne el estado del entorno (versiones del plugin, de Jeedom y del demonio, incluida la versión de la
biblioteca Roborock utilizada), el estado de la conexión a la cuenta, la lista de los robots — cada uno
identificado por su número de dispositivo Jeedom y un identificador de aparato parcialmente
enmascarado —, los errores recientes reportados por Jeedom y el demonio, y un anexo técnico. Nunca
contiene identificador de conexión, token, clave de robot, número de serie ni dirección de correo
electrónico, sea cual sea el contenido; los nombres que has dado a tus robots o a tus habitaciones
tampoco figuran en él.

Dos botones permiten obtenerlo: **« Copiar el informe »** (portapapeles) y **« Descargar el informe »**
(archivo de texto). Si la copia automática no funciona — es el caso más frecuente cuando Jeedom se
sirve por HTTP en lugar de HTTPS — el texto queda seleccionado: cópialo con Ctrl+C. Si un foro de
soporte limita la longitud de un mensaje, adjunta mejor el archivo descargado.

Si el demonio está detenido en el momento de la generación, el informe lo señala al principio
(« Demonio inaccesible: informe parcial ») y sigue siendo
utilizable a pesar de todo: la información todavía conocida del lado de Jeedom (último estado, marca
de tiempo de la última comunicación) figura igualmente. Si está iniciado pero la sección técnica no
pudo generarse, el informe lo indica con un aviso distinto (« Diagnóstico del demonio no disponible:
informe parcial »); en ese caso también, el
resto del informe sigue siendo utilizable.

Esta acción está reservada a los administradores de Jeedom.

### Qué adjuntar a una solicitud de ayuda

Además del informe, describe en tu mensaje: el **síntoma preciso** (lo que observas, y en qué orden o
qué pantalla), **lo que ya has probado**, y la **hora aproximada** en la que ocurrió el problema. Estas
tres informaciones permiten localizar el incidente en un informe o un registro; el informe por sí solo
no basta para adivinar el contexto.

**Nunca publiques tal cual**, en un foro o en un ticket público:

- tu **dirección de correo electrónico** de la cuenta Roborock o el **código** recibido por correo
  electrónico;
- un **token**, un identificador de sesión o cualquier valor que se parezca a una clave técnica;
- el **contenido bruto** de los registros del plugin o del demonio (menú Jeedom « Analyse » >
  « Logs », o archivos bajo `log/`): a diferencia del informe de diagnóstico, estos registros **no
  están depurados**;
- una **captura de pantalla** que dejara ver alguno de estos elementos.

El informe de diagnóstico generado desde la página de configuración está, por su parte, concebido para
transmitirse tal cual (ver más arriba).

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| El indicador de dependencias permanece bloqueado / en rojo | Instalación de la dependencia Python no terminada o fallida | Espera la duración de instalación indicada por Jeedom; en caso de fallo persistente, comprueba el acceso a Internet del servidor y relanza la instalación desde la página « Plugins » |
| « El demonio no responde. » | El demonio no está iniciado, o acaba de detenerse | Inicia (o reinicia) el demonio desde la configuración del plugin |
| « El robot está fuera de línea: no responde a la nube Roborock. » | El robot está apagado, fuera de red, o no tiene conexión con la nube de Roborock | Comprueba que el robot esté encendido y conectado a tu red Wi-Fi, igual que desde la aplicación móvil |
| « La cuenta Roborock no está vinculada: autentícate desde la configuración del plugin. » | Se solicitó una acción mientras aún no se había vinculado ninguna cuenta | Sigue el procedimiento de vinculación de la cuenta, sección « Vincular tu cuenta Roborock » |
| « La dirección de correo electrónico de la cuenta Roborock no es válida. » o « Ninguna cuenta Roborock corresponde a esta dirección de correo electrónico. » | La dirección introducida tiene un error, o no es la de la cuenta Roborock | Introduce la dirección exacta utilizada en la aplicación móvil Roborock, guarda la configuración, y vuelve a solicitar un código |
| Código de conexión nunca recibido por correo electrónico | Dirección de correo incorrecta, o mensaje filtrado por tu correo | Comprueba la dirección guardada, revisa tu carpeta de correo no deseado, reintenta « Enviar un código » tras unos minutos |
| « Código de conexión no válido o caducado. » | El código se copió mal o ha caducado | Vuelve a solicitar un código nuevo y valídalo rápidamente |
| « Demasiadas solicitudes de código de conexión: espere unos minutos antes de volver a intentarlo. » | Demasiadas solicitudes de código muy seguidas | Espera unos minutos antes de volver a solicitar un código |
| « Sesión de Roborock caducada: es necesaria una nueva autenticación mediante código por correo electrónico. » / « Reautenticación requerida » | La sesión guardada ya no es válida del lado de Roborock | Sigue el procedimiento « Reautenticación requerida » más arriba |
| « Se alcanzó la cuota de llamadas de Roborock: espere antes de volver a intentarlo. » | La cuota, compartida con la aplicación móvil, está temporalmente agotada | Espera antes de reintentar; no relances la acción en bucle |
| Una orden esperada no aparece en el dispositivo | El robot no anuncia la capacidad correspondiente | Es normal: la lista de órdenes depende de lo que el robot declara saber hacer, no es un fallo |
| « Este mapa ya no existe en este robot: actualiza la lista de mapas. » | La lista de mapas mostrada está desactualizada | Haz clic en « Actualizar la lista de mapas » y vuelve a intentarlo |
| « Se acaba de realizar un cambio de mapa: espera dos minutos antes de iniciar otro. » | El cambio de mapa es una operación lenta, protegida por una espera de dos minutos | Espera dos minutos antes de relanzar un cambio de mapa |
| « No se pudo decodificar el mapa del robot. Consulta el registro del demonio. » | El dato recibido de la estación es ilegible (incidente puntual del lado del robot o de la nube) | Vuelve a intentarlo más tarde; consulta el registro del demonio si el problema persiste |
| « La imagen del mapa es demasiado grande para transferirse. » | El mapa producido por el robot supera el tamaño que el plugin acepta almacenar | Vuelve a intentarlo más tarde; si el problema persiste, este robot no es compatible con esta función |
| « El robot debe estar en la base para iniciar esta operación. » | Se solicitó una acción de mantenimiento de la estación mientras el robot no estaba en su base | Espera a que el robot vuelva a su base, o lanza « Volver a la base » primero |
| « Esta operación de mantenimiento no está disponible en la base de este robot: actualiza su estado antes de volver a intentarlo. » | La estación de este robot no admite esta acción | Es normal: la orden no debería aparecer si la estación no lo permite; actualiza el estado del robot |
| « La lista de rutinas recibida de la nube Roborock está incompleta: por precaución, no se ha eliminado ninguna rutina. » | La respuesta de la nube se truncó, o este robot tiene más de 64 usos | Relanza la sincronización más tarde; no se ha perdido nada mientras tanto |
| « No se han aceptado las condiciones de uso de Roborock. » (o « Las condiciones de uso de Roborock han cambiado. ») | Roborock pide validar (o revalidar) sus condiciones de uso | Abre la aplicación móvil Roborock, acepta las condiciones propuestas, y vuelve a intentarlo desde Jeedom |
| « Robot desconocido para el demonio: vuelve a ejecutar una sincronización de dispositivos. » | El dispositivo Jeedom ya no es reconocido por el demonio (reinicio, robot retirado de la cuenta…) | Relanza « Sincronizar dispositivos » |
| « No se puede contactar con la nube Roborock: comprueba el acceso a Internet de Jeedom. » | Jeedom no logra contactar con los servidores de Roborock | Comprueba el acceso a Internet del servidor Jeedom |
| Un mensaje que mencione un plazo superado, una conexión fallida o « Varios intentos de comunicación han fallado: vuelve a intentarlo más tarde. » | El robot o la nube de Roborock tardó demasiado en responder: incidente de red pasajero, o robot muy solicitado | Vuelve a intentarlo tras un minuto; si se repite, comprueba la conexión Wi-Fi del robot y el acceso a Internet del servidor Jeedom |
| « El robot está ocupado: no puede procesar esta solicitud ahora. », « El robot rechazó la acción en su estado actual. » o « El robot indicó un error al ejecutar el comando. » | El robot no puede ejecutar esta solicitud en su estado actual (limpieza en curso, depósito lleno, incidente mecánico…) | Comprueba el estado del robot (orden « État », o aplicación móvil), resuelve el incidente notificado y vuelve a lanzar la acción |
| « Esta función no está disponible en este modelo de robot. » o « El robot no reconoce este comando. » | El robot no implementa esta función, aunque la orden exista en Jeedom | Ninguna manipulación desbloqueará la situación: esta función no existe en este equipo, oculta la orden si te molesta |
| « No hay ninguna solicitud de código en curso (es posible que el demonio se haya reiniciado): solicita un nuevo código. » | El demonio se reinició entre el envío y la validación del código | Haz clic de nuevo en « Enviar un código », y valida el nuevo código recibido |
| Un ajuste (aspiración, caudal de agua, ruta, modo de limpieza) no se aplica | El robot rechaza este ajuste en su estado actual (por lo general: no está en reposo) | Vuelve a intentarlo cuando el robot esté en reposo o en su base |
| « Esta potencia de aspiración / este caudal de agua / este recorrido de fregado / este modo de limpieza no está disponible en este robot. » | La lista de niveles conocida por Jeedom está desactualizada (el robot ya no anuncia ese valor) | Actualiza el estado del robot y vuelve a intentarlo |
| « Habitación desconocida en el mapa actualmente activo de este robot. », « No hay ninguna habitación conocida para este robot. » o « Varias habitaciones tienen este nombre en este robot. » | El nombre introducido no corresponde a ninguna habitación detectada, aún no se ha sincronizado ninguna habitación, o el nombre es ambiguo | Resincroniza las habitaciones desde la pestaña Dispositivo, usa el nombre exacto de la aplicación Roborock, o la orden dedicada a esa habitación en lugar de la orden genérica |
| « Estas coordenadas superan los límites del mapa conocido de este robot. » | La zona o el punto introducido supera el mapa actualmente conocido del robot | Comprueba las coordenadas en el bloque « Zona y punto » de la pestaña Dispositivo, o actualiza la imagen del mapa |
| « Este consumible no se controla para este robot: actualiza su estado antes de reiniciarlo. » | La orden de reinicialización se utilizó antes de que el desgaste de ese consumible se hubiera reportado al menos una vez | Actualiza el estado del robot antes de reinicializar ese consumible |
| « Se acaba de realizar una sincronización de rutinas (o de habitaciones): espera un minuto antes de volver a intentarlo. » (usos, habitaciones o programaciones) | Ya se realizó una resincronización hace menos de un minuto | Espera un minuto antes de relanzar la misma resincronización |
| « El registro se acaba de actualizar: espere un minuto antes de volver a intentarlo. » | El botón « Actualizar el registro » ya se utilizó hace menos de un minuto | Espera un minuto antes de volver a hacer clic |
| « La generación del informe ha fallado. » | La solicitud a Jeedom no llegó a buen puerto: plazo de 20 segundos superado, conexión interrumpida o error del servidor Jeedom (un demonio detenido, en cambio, da un informe parcial, no este fallo) | Recarga la página de configuración y vuelve a intentarlo; si persiste, consulta el registro `jeeroborock` (menú « Analyse » > « Logs ») |
| « … rutina(s) no se pudieron registrar en Jeedom. Consulte el registro del plugin. » (en el resumen del panel « Rutinas ») | Un uso concreto no se pudo crear ni actualizar del lado de Jeedom durante la sincronización, mientras que el resto se desarrolló con normalidad | Consulta el registro `jeeroborock` (menú « Analyse » > « Logs ») para identificar el uso afectado, y vuelve a lanzar una sincronización |
| « 401 - Acceso no autorizado » al hacer clic en « Generar un informe de diagnóstico » | Tu sesión de Jeedom ha caducado, o tu cuenta no tiene derechos de administrador | Vuelve a conectarte a Jeedom con una cuenta administradora y vuelve a intentarlo |
| « Diagnóstico del demonio no disponible: informe parcial » | El demonio está iniciado, pero no pudo proporcionar la parte técnica del informe (incidente puntual) | El resto del informe sigue siendo utilizable; vuelve a intentarlo más tarde para obtener la sección técnica completa |

Para cualquier otro mensaje, el texto mostrado por el plugin da directamente la causa y, en su caso,
el gesto a realizar — nunca es necesario abrir los registros técnicos para entenderlo.

## Limitaciones conocidas

- El plugin solo controla robots compatibles con el protocolo V1 de Roborock, a través de la nube. Los
  robots más antiguos (protocolo A01) no son compatibles.
- Las etiquetas producidas por el propio robot (estado, error, estado de la estación, nombres de
  consumibles) permanecen **siempre en francés**, sea cual sea el idioma elegido para la interfaz de
  Jeedom.
- Un cambio de mapa hecho desde la aplicación móvil ahora se detecta automáticamente, en segundo
  plano, en aproximadamente un minuto: el mapa activo, la imagen y el sistema de coordenadas del mapa
  se actualizan sin acción por tu parte (la lista de habitaciones, por su parte, se vacía y espera un
  clic en « Resincronizar las habitaciones »). Durante ese breve plazo, la configuración puede seguir
  mostrando la planta anterior, y una página de Dispositivo ya abierta no se actualiza sola: recárgala.
- La conexión local mencionada más arriba (« Lo que el plugin hace, y lo que no hace ») no se puede
  desactivar desde Jeedom.
- El plugin muestra la versión del **firmware** del robot (pestaña « Dispositivo », actualizada en la
  sincronización de los dispositivos), pero no señala que haya una actualización disponible ni la
  activa: la actualización del firmware se hace desde la aplicación móvil Roborock.
- Más allá de **64 usos** registrados para un mismo robot, la sincronización de los usos sigue
  añadiendo y renombrando, pero ya no elimina automáticamente los usos desaparecidos de la aplicación.
- La imagen del mapa puede permanecer **ilegible** cuando el robot solo es accesible por la conexión
  local mencionada más arriba, sin pasar por el canal MQTT de la nube (mensaje « La carte du robot n'a
  pas pu être décodée » — No se ha podido decodificar el mapa del robot).
- La lectura de los nombres de habitación (panel « Habitaciones » de la pestaña Dispositivo) exige que
  el robot esté **en línea**: falla si el robot es inaccesible en el momento del clic.
- La vista de mapa (panel « Inicio > JeeRoborock ») no dispara por sí misma ninguna actualización: se
  limita a mostrar, cada 30 segundos, la última imagen ya conocida. Esta imagen solo se reconstruye
  durante las limpiezas; en reposo, puede por tanto ser del último paso del robot.
- No existe una vista de mapa en la aplicación móvil de Jeedom: el panel de mapa solo está disponible
  en la interfaz de escritorio.
- Las órdenes retomadas por el mosaico del panel de control (batería, en limpieza, error, conectado,
  en línea y las cinco acciones de control) se ocultan una sola vez, al crear el mosaico. Si vuelves a
  mostrar una manualmente, el plugin nunca vuelve a ocultarla: tu elección se conserva.
- En una instalación actualizada desde una versión antigua del plugin, una migración técnica puntual
  pudo reactivar la historización de la orden « Error »: si no deseas historizar esta orden,
  desactívala manualmente en su configuración.

Esta página se actualiza con cada nueva funcionalidad entregada por el plugin.
