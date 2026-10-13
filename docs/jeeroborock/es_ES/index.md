# JeeRoborock

JeeRoborock controla tus aspiradoras robot Roborock desde Jeedom, pasando por la nube de Roborock: estado
en tiempo real, órdenes de limpieza, control detallado (aspiración, agua, ruta, mantenimiento de la
estación), limpieza por habitación o por zona, mapas múltiples, y ejecución de las rutinas (« usos »)
definidas en la aplicación móvil Roborock.

## Lo que el plugin hace, y lo que no hace

JeeRoborock es software libre, publicado bajo licencia **GPL v3 o posterior**.

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

1. **Jeedom 4.4.7 como mínimo**, instalado en un servidor con **Debian 12 o 13**. Esta versión de Debian
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

### Órdenes según el modelo

El plugin no conoce una lista de órdenes « por modelo ». Crea una orden cuando el robot o su estación **declara** la capacidad correspondiente, o **responde** cuando el plugin lo interroga. Una orden ausente significa, pues, « este equipo no la anuncia (o todavía no) », no « el plugin está averiado ». Un robot con una estación completa no tiene la misma lista que un robot sin estación, ni que un robot más antiguo del mismo fabricante.

**Hacer que aparezca una orden que falta:**

1. Comprueba que el demonio está iniciado, que la cuenta está vinculada y que el robot está **en línea**: mientras el robot no haya respondido una primera vez, no se crea ninguna orden que dependa de sus capacidades.
2. Lanza la orden **« Actualizar »** del dispositivo, o espera: el estado se relee solo cada 60 segundos en reposo (30 segundos durante una limpieza). Las órdenes se crean en esa relectura. Después, recarga la página del dispositivo.
3. Tras una actualización del firmware del robot (desde la aplicación Roborock) o del plugin, haz lo mismo. **No** uses « Sincronizar dispositivos » para esto: ese botón sirve para descubrir los robots de la cuenta y consume cuota de Roborock.
4. Si el robot ha respondido que no conoce un ajuste leído por interrogación (no molestar, volumen), el plugin solo vuelve a interrogar **una vez por hora**; en caso de fallo de lectura (robot inaccesible), reintenta al cabo de 5 minutos. La orden « Actualizar » fuerza una lectura inmediata.
5. Justo después de « Actualizar », los últimos ajustes de la lista (volumen, modos de la estación) pueden faltar si la relectura se quedó sin tiempo: vuelve a lanzar « Actualizar » o espera un minuto.

El plugin no elimina por sí mismo una orden ya creada.

| Capacidad | Órdenes afectadas | Condición de aparición |
|---|---|---|
| Consumibles de la estación | « Desgaste restante del filtro de la estación », « Desgaste restante del cepillo de limpieza », « Desgaste restante de la bolsa de polvo » y, salvo la bolsa, su acción « Reiniciar… » | La estación posee el equipamiento (lavado de la mopa para el filtro, cepillo de limpieza, vaciado automático para la bolsa) **y** el robot notifica el contador. Se releen aproximadamente cada hora, o con « Actualizar » |
| Depósitos y mopa | « Depósito de agua limpia vacío », « Depósito de agua sucia lleno o ausente », « Mopa instalada » | Depósitos: la estación lava las mopas. Mopa: el robot declara gestionar el modo de agua. Se crean en la siguiente relectura del estado |
| Bloqueo infantil | « Bloqueo infantil », « Activar… », « Desactivar… » | El robot declara gestionar este ajuste. Se crean en la siguiente relectura del estado |
| No molestar | Información, inicio, fin, tres acciones | El robot responde a la lectura del modo. Se relee cada minuto; con « Actualizar », de inmediato |
| Horas valle | Información, inicio, fin, tres acciones | El robot declara la función. Se crean en la siguiente relectura del estado |
| Volumen | « Volumen », « Ajustar el volumen » | El robot responde a la lectura del volumen. Se relee cada minuto; con « Actualizar », de inmediato |
| Modos de la estación | « Modo de vaciado » y « Ajustar el modo de vaciado »; « Modo de lavado de la mopa » y « Ajustar el modo de lavado » | La estación declara el vaciado automático (modo de vaciado) o el lavado de la mopa (modo de lavado). Se crean en la siguiente relectura del estado |
| Número de pasadas | Ninguna orden propia: un parámetro de las acciones « Limpiar habitaciones » y « Limpiar una zona » | El robot indica, en su estado, que gestiona la repetición. Entonces el campo se titula « Número de pasadas (1 a 3) »; si no, el campo no tiene título y un número de 2 o 3 es, en principio, rechazado por el plugin |
| Habitación actual | « Habitación actual » | Se ha leído una imagen del mapa, el mapa está dividido en habitaciones y la posición del robot es utilizable. Primera imagen: en la primera relectura; después, durante una limpieza o tras un cambio de estado |

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
| Limpiando | Sí/no |
| Error | Etiqueta del error en curso, « Aucune » (Ninguno) en caso contrario |
| Superficie limpiada | En m², para la limpieza en curso |
| Duración de limpieza | En minutos, para la limpieza en curso |
| Progreso | En %, para la limpieza en curso |
| En línea / Conectado | « En línea »: el robot respondió a la última relectura (pasa a « fuera de línea » en cuanto una relectura falla por falta de respuesta del robot). « Conectado »: actualidad del dato del lado del plugin (canal con el demonio) |
| Última actualización | Fecha y hora del último dato recibido |
| Iniciar / Pausar / Detener | Control de la limpieza. « Iniciar » **reanuda** una limpieza pausada o interrumpida (incluida una limpieza por habitación o por zona) en lugar de lanzar una nueva; sin limpieza en curso, lanza una limpieza completa |
| Volver a la base | Envía al robot a recargarse |
| Localizar | Hace que el robot emita una señal sonora |
| Actualizar | Relee inmediatamente el estado del robot |

**Durante el vaciado del depósito de polvo.** Cuando la estación vacía el depósito (estado del robot « Vidage du bac à poussière », es decir, vaciado del depósito de polvo), el robot no tiene en cuenta una orden de limpieza. El plugin la rechaza entonces, en lugar de responder « ok » sin efecto: es el caso de « Iniciar », « Limpiar habitaciones », las órdenes « Limpiar <nombre de la habitación> » y « Limpiar una zona ». El mensaje mostrado es « El robot está vaciando su depósito de polvo: no se envió la orden de limpieza. Vuelva a intentarlo en un momento, cuando termine el vaciado (robot de nuevo en carga). » En un escenario, la acción falla de la misma manera. Las demás órdenes (pausa, parada, volver a la base, localizar, desplazarse a un punto) no se ven afectadas, ni tampoco las rutinas (usos), ejecutadas por la nube de Roborock. Si el plugin no logra releer el estado del robot justo antes de la orden, la orden se envía normalmente.

### Estación de carga, consumibles y mantenimiento

Estas órdenes aparecen **solo si tu estación lo permite**:

- estado de vaciado del polvo, de lavado y de secado de la mopa, error de estación, falta de agua. Si
  el código de error notificado por la estación no se reconoce, la etiqueta mostrada es
  « Erreur de station non reconnue » (Error de estación no reconocido; el código bruto sigue siendo
  visible en la orden de código de error de la estación);
- acciones correspondientes: lavar la mopa, secar la mopa, detener el secado, vaciar el depósito —
  disponibles únicamente cuando el robot está **en su base** (incluida la carga); fuera de ese estado,
  el plugin rechaza la acción con un mensaje explícito.

El desgaste de los consumibles detectados por tu robot (cepillo principal, cepillo lateral, filtro,
sensores, rodillo de fregado) se publica en porcentaje restante, cada uno con una acción « Reiniciar… »
a utilizar tras una sustitución física. Esta acción pide confirmación antes de ejecutarse.

Según el equipamiento de tu estación, y si el robot notifica el contador, aparecen tres desgastes
adicionales, también en porcentaje restante:

- « Desgaste restante del filtro de la estación »: estaciones que lavan la mopa;
- « Desgaste restante del cepillo de limpieza »: estaciones que lo tienen (en la práctica, algunas
  estaciones de gama alta);
- « Desgaste restante de la bolsa de polvo »: estaciones con vaciado automático.

Sin estación, o con una estación básica, estas órdenes no aparecen. El filtro de la estación y el
cepillo de limpieza tienen cada uno una acción « Reiniciar el filtro de la estación » o « Reiniciar el
cepillo de limpieza », con confirmación, como las demás. La bolsa de polvo no tiene reinicio en el
plugin (solo lectura): si la pones a cero en otro lugar (aplicación Roborock), el valor la sigue en la
siguiente relectura.

Estos valores se releen aproximadamente una vez por hora, de inmediato con la orden « Actualizar », y
tras un reinicio. Los porcentajes pueden diferir ligeramente de los de la aplicación Roborock.

**Ejemplo de escenario**: disparador sobre la orden « Desgaste restante del filtro de la estación »,
condición « inferior a 10 », acción « Enviar una notificación » (« Recuerda sustituir el filtro de la
estación »). Tras la sustitución, lanza la acción « Reiniciar el filtro de la estación » (pide
confirmación): no la pongas en un escenario automático, el contador volvería al 100 % sin que se
hubiera cambiado la pieza.

Tres informaciones sí/no, utilizables en un escenario, describen también el estado del agua y de la
mopa:

- « Depósito de agua limpia vacío » y « Depósito de agua sucia lleno o ausente »: solo si tu estación
  lava las mopas. « Sí » señala una situación que revisar (llenar el depósito, vaciar o volver a colocar
  el depósito). El robot no distingue un depósito sucio lleno de un depósito ausente, de ahí el nombre;
- « Mopa instalada »: solo si tu robot está equipado con una mopa.

Estas informaciones son distintas de « Falta de agua »: el robot las notifica por separado, y pueden
señalarse a la vez. Se actualizan con el estado del robot (aproximadamente un minuto en reposo), o
de inmediato con « Actualizar ». Si un valor no está disponible momentáneamente, se conserva el último
valor conocido.

**Ejemplo de escenario**: disparador sobre « Depósito de agua limpia vacío » o « Depósito de agua sucia
lleno o ausente » (valor « Sí »), acción « Enviar una notificación » (« Revisa el depósito de la
estación »). Una condición sobre « Mopa instalada » (valor « No ») permite no lanzar una limpieza con
lavado cuando la mopa no está puesta.

### Ajustes del aparato

El **bloqueo infantil** desactiva los botones físicos del robot (práctico contra un niño o un animal demasiado curioso). Tres órdenes están dedicadas a él:

- « Bloqueo infantil »: información sí/no, utilizable como condición de escenario (por ejemplo, para activar el bloqueo solo si no lo está ya);
- « Activar el bloqueo infantil » y « Desactivar el bloqueo infantil »: dos acciones.

Estas órdenes aparecen **solo si tu robot declara gestionar este ajuste**. Si no, no existe ninguna de las tres: no es una avería, dos robots no tienen la misma lista de órdenes.

Tras una orden, el plugin relee el estado del robot para comprobar que lo ha asumido, como para los ajustes descritos en « Control detallado » (hasta una docena de segundos, sin reenviar la orden). La orden « Bloqueo infantil » solo muestra lo que el robot ha adoptado realmente, nunca el valor solicitado. Los mensajes posibles:

| Mensaje | Significado |
| --- | --- |
| « Bloqueo infantil activado. » / « Bloqueo infantil desactivado. » | El robot asumió la orden: el estado releído coincide. |
| « Activación (o Desactivación) del bloqueo infantil enviada al robot (aplicación no confirmada). » | La orden se envió, pero no se pudo releer el estado, o otra orden de bloqueo infantil la sustituyó durante la comprobación. El estado mostrado sigue siendo el anterior. |
| « El robot no ha aplicado la orden de bloqueo infantil: el estado leído no coincide con la solicitud. » | El robot responde, pero no adoptó el ajuste al cabo del plazo. El estado mostrado es el releído en el robot. |
| Rechazo del robot | El robot rechazó la orden; el mensaje lo indica. |
| Robot fuera de línea | El robot no responde (apagado, fuera de alcance); la orden no se asume. |

El plugin nunca reenvía una orden por sí solo: en caso de fallo, vuelve a lanzarla tú mismo.

**Ejemplo de escenario**: al final de la limpieza (« Limpiando » pasa a « No »), si la condición « Bloqueo infantil » vale « No », lanza la acción « Activar el bloqueo infantil ».

Un cambio hecho desde la aplicación Roborock (o con el botón del robot) no se notifica al plugin: aparece en « Bloqueo infantil » en aproximadamente un minuto, o de inmediato con la orden « Actualizar ».

**Espera unos segundos entre dos órdenes de bloqueo infantil.** Una orden enviada menos de 5 segundos después del final de la anterior (comprobación incluida), en el mismo robot, se rechaza con el mensaje « Se acaba de enviar una orden de bloqueo infantil a este robot: espere unos segundos antes de enviar otra. » En un escenario, prevé una pausa de al menos 5 segundos entre dos acciones de bloqueo infantil.

#### No molestar

El modo **no molestar** impide que el robot arranque o hable durante un intervalo horario (por la noche, por ejemplo). Seis órdenes están dedicadas a él:

| Orden | Tipo | Función |
| --- | --- | --- |
| No molestar | Información sí/no | Indica si el modo está activado, utilizable como condición de escenario |
| Inicio de no molestar | Información texto | Hora de inicio del intervalo, en formato HH:MM |
| Fin de no molestar | Información texto | Hora de fin del intervalo, en formato HH:MM |
| Activar no molestar | Acción | Activa el modo con el intervalo guardado por el robot |
| Desactivar no molestar | Acción | Desactiva el modo |
| Definir el intervalo de no molestar | Acción con dos campos, Inicio y Fin | Guarda el intervalo y activa el modo |

Estas órdenes aparecen **solo si el robot responde a la lectura del modo**. Se crean, como muy tarde, aproximadamente un minuto después de que el robot sea accesible, o de inmediato con « Actualizar ». Si faltan, no es una avería: dos robots no tienen la misma lista de órdenes.

Las horas se expresan en la **hora local del robot**, como en la aplicación Roborock.

**Definir el intervalo**: rellena los campos Inicio y Fin en formato HH:MM, entre 00:00 y 23:59. Una hora de un solo dígito como 7:30 se acepta y se normaliza a 07:30. La acción es utilizable en un escenario: el campo **Título** recibe el inicio, el campo **Mensaje** el fin (sus ayudas de entrada se titulan « Inicio (HH:MM) » y « Fin (HH:MM) »). Se acepta un intervalo que cruza la medianoche (por ejemplo 22:00 → 07:00). Un inicio igual al fin se rechaza. Definir el intervalo **también activa el modo**.

| Entrada (inicio → fin) | Resultado |
|---|---|
| 22:00 → 07:00, o 7:30 → 22:15 | Válido (intervalo que cruza la medianoche, u hora de un dígito normalizada a 07:30) |
| 00:00 → 23:59 | Válido |
| 24:00 → 07:00, 22:60 → 07:00 | Rechazada: hora o minuto fuera de límites |
| 22h00 → 07h00, 2200 → 0700, 22:5 → 07:00 | Rechazada: el formato debe ser HH:MM (minutos con dos dígitos, separador « : ») |
| (campo vacío) → 07:00 | Rechazada: un campo está vacío |
| 22:00 → 22:00 | Rechazada: inicio igual al fin |

**Ejemplo de escenario**: todas las noches a las 21 h, lanza la acción « Definir el intervalo de no molestar » con el inicio 22:00 y el fin 07:00. Para silenciar los avisos durante el día, usa mejor « Activar no molestar » / « Desactivar no molestar » sobre el intervalo ya guardado.

**Activar** vuelve a aplicar el intervalo ya guardado por el robot. Si el robot no devuelve ninguno, la acción se rechaza: usa entonces « Definir el intervalo de no molestar ». **Desactivar** conserva normalmente el intervalo guardado, pero ese comportamiento depende del robot y está por confirmar: si cuentas con « Activar » después, comprueba « Inicio de no molestar » y « Fin de no molestar ».

Tras una orden, el plugin relee el estado del robot para comprobar que lo ha asumido (unos segundos, sin reenviar la orden). Las órdenes de información solo muestran lo que el robot ha adoptado realmente. Los mensajes posibles:

| Mensaje | Significado |
| --- | --- |
| « No molestar activado. » / « No molestar desactivado. » / « Intervalo de no molestar aplicado. » | El robot asumió la orden: el estado releído coincide. |
| « Activación (o Desactivación) de no molestar enviada al robot (aplicación no confirmada). » / « Intervalo de no molestar enviado al robot (aplicación no confirmada). » | La orden se envió, pero no se pudo releer el estado. El estado mostrado sigue siendo el anterior. |
| « El robot no aplicó la orden de no molestar: el estado leído no coincide con la solicitud. » | El robot responde, pero no adoptó el ajuste al cabo del plazo. |
| « Intervalo horario no válido: indique un inicio y un fin con formato HH:MM, entre 00:00 y 23:59. » | Un campo está vacío o mal formado. Corrígelo. |
| « Intervalo horario no válido: el inicio y el fin del intervalo de no molestar deben ser distintos. » | Inicio y fin idénticos. |
| « El robot no devolvió ningún intervalo de no molestar utilizable: defina el intervalo, lo que también activa el modo. » | « Activar » no tiene ningún intervalo que volver a aplicar: usa « Definir el intervalo de no molestar ». |
| « Se acaba de enviar una orden de no molestar a este robot: espere unos segundos antes de enviar otra. » | Dos órdenes demasiado seguidas. |
| Rechazo del robot / robot fuera de línea | El robot rechazó la orden o no responde; la orden no se asume. |

El plugin nunca reenvía una orden por sí solo: en caso de fallo, vuelve a lanzarla tú mismo.

Un cambio hecho desde la aplicación Roborock no se notifica al plugin: aparece en Jeedom en aproximadamente un minuto, o de inmediato con « Actualizar ».

**Espera al menos 5 segundos entre dos órdenes de no molestar** en el mismo robot; si no, la última se rechaza (mensaje « espere »). En un escenario, prevé una pausa de al menos 5 segundos entre dos acciones de no molestar.

#### Horas valle

La **recarga en horas valle** hace que el robot espere al intervalo horario elegido (por la noche, por ejemplo, con tarifa eléctrica reducida) para **recargar su batería**. Solo retrasa la recarga: no bloquea una limpieza que tú pidas. Seis órdenes están dedicadas a ella:

| Orden | Tipo | Función |
| --- | --- | --- |
| Recarga en horas valle | Información sí/no | Indica si la función está activada, utilizable como condición de escenario |
| Inicio de las horas valle | Información texto | Hora de inicio de la franja, en formato HH:MM |
| Fin de las horas valle | Información texto | Hora de fin de la franja, en formato HH:MM |
| Activar la recarga en horas valle | Acción | Activa la función con la franja guardada por el robot |
| Desactivar la recarga en horas valle | Acción | Desactiva la función |
| Definir la franja de horas valle | Acción con dos campos, Inicio (HH:MM) y Fin (HH:MM) | Guarda la franja y activa la función |

Estas órdenes aparecen **solo si el robot declara la función**. Se crean, como muy tarde, aproximadamente un minuto después de que el robot sea accesible, o de inmediato con « Actualizar ». Si faltan, no es una avería: dos robots no tienen la misma lista de órdenes.

Las horas se expresan en la **hora local del robot**, como en la aplicación Roborock.

**Definir la franja**: rellena los campos Inicio y Fin en formato HH:MM, entre 00:00 y 23:59. Una hora de un solo dígito como 7:30 se acepta y se normaliza a 07:30. La acción es utilizable en un escenario, con esos dos campos. Se acepta una franja que cruza la medianoche (por ejemplo 23:00 → 07:00). Un inicio igual al fin se rechaza. Definir la franja **también activa la recarga en horas valle**. En un escenario, el campo **Título** recibe el inicio y el campo **Mensaje** el fin (ayudas de entrada « Inicio (HH:MM) » y « Fin (HH:MM) »). Mismas reglas de entrada que « No molestar »:

| Entrada (inicio → fin) | Resultado |
|---|---|
| 23:00 → 07:00, o 7:30 → 22:15 | Válido (la segunda se normaliza a 07:30) |
| 24:00 → 07:00, 23:60 → 07:00 | Rechazada: hora o minuto fuera de límites |
| 23h00 → 07h00, 2300 → 0700, 23:5 → 07:00 | Rechazada: el formato debe ser HH:MM |
| (campo vacío) → 07:00 | Rechazada: un campo está vacío |
| 23:00 → 23:00 | Rechazada: inicio igual al fin |

**Ejemplo de escenario**: una vez por semana, lanza « Definir la franja de horas valle » con el inicio 23:00 y el fin 07:00 para realinear la franja con tu contrato eléctrico; o dispara « Activar la recarga en horas valle » cuando se ejecute tu escenario de salida de casa.

**Activar** vuelve a aplicar la franja ya guardada por el robot. Si el robot no devuelve ninguna, la acción se rechaza: usa entonces « Definir la franja de horas valle ». **Desactivar** conserva normalmente la franja guardada, pero ese comportamiento depende del robot y está por confirmar: si cuentas con « Activar » después, comprueba « Inicio de las horas valle » y « Fin de las horas valle ».

Tras una orden, el plugin relee el estado del robot para comprobar que lo ha asumido (unos segundos, sin reenviar la orden). Las órdenes de información solo muestran lo que el robot ha adoptado realmente. Los mensajes posibles:

| Mensaje | Significado |
| --- | --- |
| « Recarga en horas valle activada. » / « Recarga en horas valle desactivada. » / « Franja de horas valle aplicada. » | El robot asumió la orden: el estado releído coincide. |
| « Activación (o Desactivación) de la recarga en horas valle enviada al robot (aplicación no confirmada). » / « Franja de horas valle enviada al robot (aplicación no confirmada). » | La orden se envió, pero no se pudo releer el estado. El estado mostrado sigue siendo el anterior. |
| « El robot no ha aplicado la orden de recarga en horas valle: el estado leído no coincide con la solicitud. » | El robot responde, pero no adoptó el ajuste al cabo del plazo. |
| « Intervalo horario no válido: indique un inicio y un fin con formato HH:MM, entre 00:00 y 23:59. » | Un campo está vacío o mal formado. Corrígelo. |
| « Franja horaria no válida: el inicio y el fin de las horas valle deben ser diferentes. » | Inicio y fin idénticos. |
| « El robot no ha devuelto ninguna franja de horas valle utilizable: defina la franja, lo que también activa la recarga en horas valle. » | « Activar » no tiene ninguna franja que volver a aplicar: usa « Definir la franja de horas valle ». |
| « Se acaba de enviar una orden de recarga en horas valle a este robot: espere unos segundos antes de enviar otra. » | Dos órdenes demasiado seguidas. |
| Rechazo del robot / robot fuera de línea | El robot rechazó la orden o no responde; la orden no se asume. |

El plugin nunca reenvía una orden por sí solo: en caso de fallo, vuelve a lanzarla tú mismo.

Un cambio hecho desde la aplicación Roborock no se notifica al plugin: aparece en Jeedom en aproximadamente un minuto, o de inmediato con « Actualizar ».

**Espera al menos 5 segundos entre dos órdenes de horas valle** en el mismo robot; si no, la última se rechaza (mensaje « espere »). Esta pausa es independiente de la de « No molestar »: una orden de no molestar no retrasa una orden de horas valle. En un escenario, prevé una pausa de al menos 5 segundos entre dos acciones de horas valle.

#### Volumen

El **volumen** es el de los avisos de voz del robot (« Inicio de la limpieza », « Regreso a la estación »…), de 0 a 100 %. Dos órdenes están dedicadas a él:

| Orden | Tipo | Función |
| --- | --- | --- |
| Volumen | Información numérica (%) | Volumen releído en el robot, utilizable como condición de escenario |
| Ajustar el volumen | Acción con control deslizante de 0 a 100 | Envía el volumen solicitado al robot |

En un escenario, « Ajustar el volumen » acepta un valor (por ejemplo 40) o una expresión (por ejemplo un cálculo a partir de otra orden).

Estas órdenes aparecen **solo si el robot responde a la lectura del volumen**. Se crean, como muy tarde, aproximadamente un minuto después de que el robot sea accesible, o de inmediato con « Actualizar ». Si faltan, no es una avería: dos robots no tienen la misma lista de órdenes.

**Valores aceptados**: un número entero de 0 a 100, 0 incluido (0 silencia los avisos). Un valor vacío, decimal (50.5) o fuera de límites (-1, 101) se rechaza con el mensaje « Volumen no válido: indique un número entero entre 0 y 100. », sin enviar nada al robot.

Tras una orden, el plugin relee el volumen del robot para comprobar que lo ha asumido (unos segundos, sin reenviar la orden). La orden « Volumen » solo muestra lo que el robot ha adoptado realmente. Los mensajes posibles:

| Mensaje | Significado |
| --- | --- |
| « Volumen aplicado. » | El robot asumió la orden: el volumen releído coincide. |
| « Ajuste del volumen enviado al robot (aplicación no confirmada). » | La orden se envió, pero no se pudo releer el volumen. El valor mostrado sigue siendo el anterior. |
| « El robot no aplicó el volumen solicitado: el volumen leído no coincide con la solicitud. » | El robot responde, pero retuvo otro valor. « Volumen » muestra el valor releído. |
| « Se acaba de enviar un ajuste del volumen a este robot: espere unos segundos antes de enviar otro. » | Dos ajustes demasiado seguidos. |
| Rechazo del robot / robot fuera de línea | El robot rechazó la orden o no responde; la orden no se asume. |

El plugin nunca reenvía una orden por sí solo: en caso de fallo, vuelve a lanzarla tú mismo. Para oír el nuevo volumen, lanza la orden « Localizar ».

**Ejemplo de escenario**: a las 22 h, lanza « Ajustar el volumen » con el valor 20; a las 8 h, con el valor 50. Para bajar el volumen a la mitad, pasa una expresión a partir de la orden de información « Volumen » (por ejemplo `round(#[Salon][Robot][Volume]#/2)`, nombre de dispositivo ficticio: el resultado debe ser un número entero de 0 a 100, si no la orden se rechaza, de ahí el `round`).

**La posición del control deslizante de « Ajustar el volumen » muestra el último valor enviado desde Jeedom, no necesariamente el volumen real del robot, y no sigue un cambio hecho en la aplicación Roborock. La referencia es la información « Volumen ».**

Un cambio hecho desde la aplicación Roborock no se notifica al plugin: aparece en « Volumen » en aproximadamente un minuto, o de inmediato con « Actualizar ».

**Espera al menos 5 segundos entre dos ajustes del volumen** en el mismo robot; si no, el último se rechaza (mensaje « espere »). En un escenario, prevé una pausa de al menos 5 segundos entre dos acciones « Ajustar el volumen ».

#### Modo de vaciado

El **modo de vaciado** regula la intensidad con la que la estación vacía el depósito de polvo del robot. Dos órdenes están dedicadas a él:

| Orden | Tipo | Función |
| --- | --- | --- |
| Modo de vaciado | Información texto | Modo releído en la estación, utilizable como condición de escenario |
| Ajustar el modo de vaciado | Acción de tipo lista | Envía el modo elegido a la estación |

Estas órdenes aparecen **solo si la estación declara este ajuste** (vaciado automático del depósito): un robot sin estación, o con una estación que no vacía el depósito, no tiene ninguna. Se crean, como muy tarde, aproximadamente un minuto después de que el robot sea accesible, o de inmediato con « Actualizar ». Si faltan, no es una avería: dos robots no tienen la misma lista de órdenes.

**Modos propuestos**: Intelligent, Léger, Équilibré, Max (etiquetas producidas por el plugin y el robot, que permanecen en francés: inteligente, ligero, equilibrado, máximo). Esta lista procede de la biblioteca utilizada por el plugin y es idéntica para todas las estaciones: compárala con la de la aplicación Roborock. Si la estación devuelve un código que el plugin no conoce, « Modo de vaciado » muestra « Mode inconnu (N) », donde N es ese código.

En un escenario, « Ajustar el modo de vaciado » se elige por el **código del modo** (y no por su etiqueta), como las demás órdenes de tipo lista del plugin.

Tras una orden, el plugin relee el modo de la estación para comprobar que se ha asumido (unos segundos, sin reenviar la orden). « Modo de vaciado » solo muestra lo que la estación ha adoptado realmente. Los mensajes posibles:

| Mensaje | Significado |
| --- | --- |
| « Modo de vaciado ajustado a «…». » | La estación asumió la orden: el modo releído coincide. |
| « Modo de vaciado «…» enviado al robot (aplicación no confirmada). » | La orden se envió, pero no se pudo releer el modo. El valor mostrado sigue siendo el anterior. |
| « La estación no aplicó el modo de vaciado solicitado: el modo leído no coincide con la solicitud. » | La estación responde, pero retuvo otro modo. « Modo de vaciado » muestra el modo releído. |
| « Este modo de vaciado no está disponible en la estación de este robot: actualice su estado antes de volver a intentarlo. » | El modo solicitado no se conoce para esta estación. |
| « Se acaba de enviar un ajuste del modo de vaciado a este robot: espere unos segundos antes de enviar otro. » | Dos ajustes demasiado seguidos. |
| Rechazo del robot / robot fuera de línea | El robot rechazó la orden o no responde; la orden no se asume. |

El plugin nunca reenvía una orden por sí solo: en caso de fallo, vuelve a lanzarla tú mismo. El ajuste del vaciado no ha podido verificarse en todos los robots: si tu estación no lo acepta, el mensaje de rechazo anterior te lo indica.

**Ejemplo de escenario**: disparador « Modo de vaciado » que vale « Max »; acción « Ajustar el modo de vaciado » con el código del modo « Équilibré » (los códigos son los de la lista de la orden), para volver al modo habitual.

Un cambio hecho desde la aplicación Roborock no se notifica al plugin: aparece en « Modo de vaciado » en aproximadamente un minuto, o de inmediato con « Actualizar ».

**Espera al menos 5 segundos entre dos ajustes del modo de vaciado** en el mismo robot; si no, el último se rechaza (mensaje « espere »). En un escenario, prevé una pausa de al menos 5 segundos entre dos acciones « Ajustar el modo de vaciado ».

#### Modo de lavado de la mopa

El **modo de lavado** regula la intensidad del lavado de la mopa por la estación. Dos órdenes están dedicadas a él:

| Orden | Tipo | Función |
| --- | --- | --- |
| Modo de lavado de la mopa | Información texto | Modo releído en la estación, utilizable como condición de escenario |
| Ajustar el modo de lavado | Acción de tipo lista | Envía el modo elegido a la estación |

Estas órdenes aparecen **solo si la estación declara este ajuste**: un robot sin estación de lavado no tiene ninguna. Se crean, como muy tarde, aproximadamente un minuto después de que el robot sea accesible, o de inmediato con « Actualizar ». Si faltan, no es una avería.

**Modos propuestos**: Léger, Équilibré, Profond, más **Très profond** o **Intelligent** según el robot (etiquetas que permanecen en francés: ligero, equilibrado, profundo, muy profundo, inteligente). Como con el vaciado, compara con la aplicación Roborock. Un código no reconocido se muestra « Mode inconnu (N) ».

En un escenario, « Ajustar el modo de lavado » se elige por el **código del modo**, no por su etiqueta.

Tras una orden, el plugin relee el modo de la estación. Los mensajes posibles son los mismos que para el vaciado, con « lavado » en lugar de « vaciado »: « Modo de lavado ajustado a «…». », « Modo de lavado «…» enviado al robot (aplicación no confirmada). », « La estación no aplicó el modo de lavado solicitado… », « Este modo de lavado no está disponible en la estación de este robot… » y « Se acaba de enviar un ajuste del modo de lavado a este robot: espere unos segundos… ». El plugin nunca reenvía una orden por sí solo. Este ajuste no se ha verificado en todos los robots: en caso de rechazo, el mensaje lo indica.

**Ejemplo de escenario**: tras una limpieza con lavado, si « Modo de lavado de la mopa » vale « Léger », lanza « Ajustar el modo de lavado » con el código del modo « Équilibré » antes de la siguiente limpieza programada.

Un cambio hecho desde la aplicación Roborock aparece en aproximadamente un minuto, o de inmediato con « Actualizar ».

**Espera al menos 5 segundos entre dos ajustes del modo de lavado** en el mismo robot; si no, el último se rechaza. Esta pausa es independiente de la del modo de vaciado.

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
- la última limpieza también se actualiza sola, sin acción por tu parte: el plugin relee el registro en
  cuanto el robot ha terminado su limpieza (lavado y vaciado en la estación incluidos), y luego, mientras
  esa limpieza no aparezca en él, aproximadamente 1, 3, 8 y 18 minutos después (al menos 5 minutos de
  separación tras una relectura fallida). Cuenta desde unos segundos hasta unos minutos, 30 como máximo;
  si el robot ha permanecido inaccesible durante todo ese tiempo, tiene lugar una última relectura a su
  regreso. Después el plugin deja de insistir hasta la siguiente limpieza; el botón « Actualizar el
  registro » sigue disponible.

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
Roborock no aparece (ni desaparece) del lado de Jeedom hasta después de hacer clic en « Sincronizar rutinas ». Lánzala, pues, cada vez que modifiques tus usos en la aplicación.

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

Los nombres de mapas se muestran **en claro**, incluso en los robots que los transmiten codificados
(Roborock S7: « %20 » en lugar de los espacios, « %E9 » en lugar de « é »). Si un nombre ya guardado
aparece todavía codificado, haz clic una vez en **« Actualizar la lista de mapas »** (o cambia de mapa): se reescribe en claro, sin ninguna otra manipulación.

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

### Habitación donde se encuentra el robot

La orden de información **« Habitación actual »** indica el nombre de la habitación donde se encuentra el robot.

- **De dónde viene el valor**: se deduce de la posición del robot en la imagen del mapa ya leída por el plugin. No requiere ninguna llamada adicional al robot ni a la nube de Roborock.
- **Retraso**: durante una limpieza, el valor se recalcula aproximadamente cada 30 segundos. En reposo, se relee como mucho un minuto aproximadamente después de un cambio de estado (por ejemplo, el regreso a la base).
- **Valores especiales** (fijos, siempre en francés, utilizables tal cual como constantes en una condición de escenario):
  - **« Aucune pièce »** (ninguna habitación): el robot está fuera de cualquier habitación conocida (pasillo sin delimitar, base situada fuera de una habitación…).
  - **« Pièce inconnue »** (habitación desconocida): la posición o el mapa activo no se conocen, las habitaciones aún no se han sincronizado, o el mapa acaba de cambiar.
- **Antigüedad**: pasa el cursor sobre el mosaico para leer las dos fechas. La fecha de valor es la de la entrada en la habitación; la fecha de recogida es la de la última imagen de mapa procesada. Un robot inmóvil parece, por tanto, « antiguo »: es normal.
- **Escenarios**: un escenario solo se dispara con un **verdadero cambio de habitación**, no en cada relectura.
  **Ejemplo de escenario**: disparador sobre la orden « Habitación actual », condición « vale Cocina » (nombre ficticio: usa el nombre exacto de tu habitación), acción « Enviar una notificación ». El escenario solo se pone en marcha cuando el robot entra en la habitación.
- **Orden ausente**: no se crea si el mapa no está dividido en habitaciones o si la posición del robot no es utilizable. Aparece por sí sola en cuanto hay una primera imagen utilizable.
- **Robot fuera de línea**: se conserva el último valor conocido.
- **Tras un cambio de mapa**, el valor pasa a « Pièce inconnue » hasta que hagas clic en **« Resincronizar habitaciones »**. Haz lo mismo después de volver a dividir tus habitaciones en la aplicación Roborock.

### Panel « Carte » (Inicio > JeeRoborock)

El mapa es un **panel**, no una página del menú Plugins: se abre desde el menú **Inicio >
JeeRoborock**, y es accesible a cualquier usuario con derechos de lectura sobre al menos un robot (no
solo los administradores). Muestra el mapa activo del robot seleccionado, su marca de tiempo y la
leyenda de las habitaciones detectadas (número de segmento / nombre), y se actualiza automáticamente
cada 30 segundos mientras la página permanece abierta.

Si la entrada no aparece en **Inicio**, comprueba que la casilla **Mostrar panel de escritorio** esté
marcada en la página de gestión del plugin (**Plugins > Gestión de plugins > JeeRoborock**): se marca
automáticamente en la instalación, pero sigue siendo modificable.

La página tiene tres pestañas: **Mapa y control** (abierta por defecto), **Estación y mantenimiento** y
**Cronología del día**.

#### Panel de control

A la derecha del mapa, un panel permite **controlar el robot seleccionado** sin salir de la página.
Se actualiza sin recargar la página y no hace ninguna solicitud adicional a la nube de Roborock.

- **Estado**: estado del robot, batería y, durante una limpieza, progreso.
- **Pestañas Total, Habitación y Zona**: cambiar de pestaña no lanza nada.
  - **Total**: limpia toda la vivienda.
  - **Habitación**: marca una o varias habitaciones. Una habitación no se ofrece si su nombre falta, está
    duplicado o contiene una coma: renómbrala en la aplicación Roborock y luego resincroniza las
    habitaciones. El número de habitaciones por orden está limitado: más allá, lanza la limpieza en varias veces.
  - **Zona**: haz clic y arrastra sobre el mapa para trazar un rectángulo. Una zona demasiado pequeña o
    que sale del mapa se rechaza antes del envío. La pestaña está inactiva si el mapa no está disponible.
- **Ajustes**: potencia de aspiración, caudal de agua y recorrido. Solo se ofrecen los valores de **tu**
  robot, y un ajuste que no gestiona no se muestra. El valor mostrado es el que el robot ha adoptado
  realmente.
- **Botón principal**: « Limpiar todo », « Limpiar N habitaciones » o « Limpiar la zona », según la
  pestaña. Durante una limpieza, deja paso a **Pausa** (o **Reanudar**), **Detener** y
  **Volver a la base**.
- **Robot fuera de línea**: las órdenes están inactivas, con una indicación. El último mapa sigue visible.

**Limpiar una habitación, paso a paso.**

1. Abre **Inicio > JeeRoborock**. Si falta la entrada, consulta más arriba la casilla **Mostrar panel de
   escritorio**.
2. Si tienes varios robots, elige el tuyo en la lista **Robot**, en la parte superior de la página. Con un
   solo robot, no hay lista.
3. Espera a que se muestren el mapa y el estado. Si una indicación señala que el robot está fuera de línea o que
   no tienes permiso para controlarlo, los botones seguirán inactivos (ver Resolución de problemas).
4. En el panel de control, abre la pestaña **Habitación**.
5. Marca la habitación en la lista, o tócala en el mapa: se resalta. Marca varias si hace falta. No se
   envía nada al robot en este paso.
6. Si lo deseas, ajusta la potencia de aspiración, el caudal de agua y el recorrido.
7. Haz clic en el botón principal, **Limpiar 1 habitación** (o **Limpiar N habitaciones**). Ese clic, y solo
   él, envía la orden.
8. Sigue el estado y el progreso en la parte superior del panel. Usa **Pausa**, **Detener** o **Volver a la
   base** si es necesario.

Si la habitación no aparece en la lista, o si el botón permanece inactivo, consulta la tabla de
Resolución de problemas.

**Mapa interactivo.** El propio mapa sirve para elegir y trazar. No se envía nada al robot mientras no
hagas clic en el botón principal.

- **Nombres de las habitaciones**: cada habitación lleva su nombre, escrito en el mapa. Una habitación sin
  nombre se muestra « Habitación sin nombre ». Si el mapa no permite delimitar las habitaciones, un mensaje lo
  indica: elige entonces las habitaciones en la lista de la pestaña Habitación.
- **Elegir una habitación**: toca o haz clic en una habitación para seleccionarla (se resalta), tócala de
  nuevo para deseleccionarla. La selección es la misma que la de la lista de la pestaña Habitación: marcar o
  desmarcar en un lado actualiza el otro. Puedes elegir varias habitaciones.
- **Habitaciones no elegibles**: una habitación sin nombre, duplicada o cuyo nombre contiene una coma
  conserva su etiqueta, pero seleccionarla se rechaza, con una explicación. Renómbrala en la aplicación
  Roborock y luego resincroniza las habitaciones desde la página del dispositivo.
- **Habitación desconocida en el mapa actual**: tras una nueva división de las habitaciones o un cambio de
  planta, una habitación ya marcada puede dejar de existir en el mapa. Se señala « Habitación desconocida en el
  mapa actual » y el botón de lanzamiento permanece inactivo mientras esté marcada. Desmárcala, o
  resincroniza las habitaciones desde la página del dispositivo.
- **Mapa antiguo**: si el mapa mostrado es una imagen antigua (robot inaccesible), la selección en el
  mapa es imposible (« Mapa antiguo: selección imposible. »). Sin ningún mapa, las pestañas Habitación y Zona
  están inactivas.
- **Trazar una zona** (pestaña Zona): haz clic y arrastra para trazar un rectángulo. Arrástralo para
  moverlo, tira de una de sus esquinas para cambiar su tamaño, o haz clic en **Borrar la zona** para
  eliminarlo. El rectángulo se conserva cuando el mapa se actualiza, salvo si el robot cambia de planta de
  mapa o si cambias de robot.
- **Zonas prohibidas y muros virtuales**: los que has definido en la aplicación Roborock se dibujan en el
  mapa, con una leyenda. Son de **solo lectura**: no se crean ni se modifican aquí. Una modificación hecha
  en la aplicación solo aparece en la siguiente obtención del mapa. Si tu robot no tiene ninguno, o no los
  proporciona, no se dibuja nada y no aparece ningún mensaje. Una zona que trazas sobre una zona prohibida
  no es bloqueada por el plugin.
- **Pantalla táctil**: tocar, trazar y mover funcionan en tableta y teléfono.

**Derechos.** Una orden solo se envía con tu clic, y solo si Jeedom te autoriza a ejecutar las órdenes
del robot. Los derechos se configuran en la gestión de usuarios de Jeedom, robot por robot. El perfil
« usuario » tiene todos los derechos por defecto: para limitar, usa un perfil restringido. Un código de
acceso o una confirmación puestos en una orden se respetan.

| Tu situación | Lo que ves | Lo que puedes hacer |
|---|---|---|
| Administrador | Todos los robots activados | Todo |
| Derecho de ejecución sobre el robot | El robot, su mapa, su estado, la estación y la cronología | Todo: seleccionar, trazar, lanzar, pausa, parada, estación |
| Solo lectura | El robot, su mapa, su estado, la estación y la cronología, con la indicación « No tiene permiso para controlar este robot. » | Consultar, seleccionar habitaciones y trazar una zona (no se envía nada). Todos los botones de acción están inactivos. |
| Ningún derecho sobre el robot | Nada: el robot no está en la lista | Nada. Sin ningún robot accesible, la página muestra « No hay ningún robot Roborock accesible con su cuenta. » |

Un robot **desactivado** en Jeedom no se ofrece a nadie, administrador incluido. Un enlace directo a un
robot que no tienes derecho a leer se ignora. La visualización del mapa, del panel y de la cronología
no cuesta ninguna llamada a la nube de Roborock.

**Robot memorizado.** El robot elegido se recuerda en tu navegador (no de un aparato a otro). Un enlace
directo a un robot concreto (parámetro de la dirección) prevalece sobre esa elección.

**Precaución.** Si acabas de detener una limpieza por habitación, evita lanzar enseguida « Limpiar
todo »: el robot puede reanudar la limpieza interrumpida en lugar de volver a empezar por toda la vivienda.
Comprueba lo que hace; si es necesario, detenlo y vuelve a lanzar.

**Aspirar y luego fregar.** Este bloque encadena dos limpiezas sobre el mismo alcance: una **primera pasada
solo con aspiración**, y después una **segunda pasada solo con lavado**. Solo aparece si tu robot sabe
lavar (si no, no se crean ni el bloque ni las órdenes correspondientes).

- **Lanzar**: en la pestaña **Total**, el botón **Aspirar y luego fregar** trata toda la vivienda; en la
  pestaña **Habitación**, trata las habitaciones marcadas. No existe para la pestaña Zona. El número de
  pasadas solicitado (ver « Control detallado ») se aplica a las dos pasadas.
- **Estado mostrado**: la línea **Secuencia** indica en qué punto está el encadenamiento: « Passage 1 sur
  2 : aspiration », « En attente de la base », « Passage 2 sur 2 : lavage » y, al final, « Séquence
  terminée », « Séquence annulée », « Séquence interrompue », « Le second passage n'a pas pu démarrer » o
  « Séquence abandonnée » (etiquetas producidas por el demonio, que permanecen en francés: pasada 1 de 2:
  aspirado, a la espera de la base, pasada 2 de 2: lavado, secuencia terminada, cancelada, interrumpida, la
  segunda pasada no pudo iniciarse, secuencia abandonada). Cuando la secuencia se detiene sin llegar al
  final, el **motivo** se muestra debajo (ver Resolución de problemas).
- **Cancelar**: el botón **Cancelar la secuencia** aparece mientras haya una secuencia activa. Detiene el
  robot, restablece sus ajustes originales e impide la segunda pasada.
- **Cerrar el panel no interrumpe nada**: la secuencia la sigue el plugin en segundo plano, no tu
  navegador. Vuelve a abrir el panel para recuperar el estado.
- Con solo el derecho de lectura, el estado es visible pero los botones están inactivos.

#### Pestaña « Estación y mantenimiento »

Esta pestaña reúne, para el robot seleccionado, la estación de carga y el mantenimiento. Se actualiza
como el panel de control y **no consume ninguna cuota** de la nube de Roborock. El detalle de cada
orden está en la sección « Estación de carga, consumibles y mantenimiento » más arriba.
Se compone de tres bloques; **solo aparece lo que tu robot sabe hacer**.

- **Acciones**: **Vaciar el depósito**, **Lavar la mopa**, **Secar la mopa** y **Detener el secado**, así
  como las listas **Modo de vaciado** y **Modo de lavado de la mopa**.
- **Estado**: vaciado del depósito, lavado y secado de la mopa, agua limpia, agua sucia, mopa instalada,
  falta de agua e **incidencia de la estación**. Esta incidencia es distinta del error del robot: un error
  del robot no se muestra ahí. También se recuerda en una banda roja, y la **última actualización** se
  indica en la parte superior de la pestaña.
- **Consumibles**: vida útil restante en porcentaje. Con un **10 % o menos**, aparece la indicación
  **A cambiar**, con una banda de alerta. El botón **Restablecer** pone el contador a cero tras
  confirmación, que hay que hacer una vez sustituida la pieza. No existe para la bolsa.

Si el robot no tiene estación, la pestaña muestra **Este robot no tiene estación.**

**Operación en curso.** Mientras haya una operación de estación en curso, **Vaciar**, **Lavar** y **Secar**
están inactivos y llevan la indicación « Operación en curso ». Lo mismo ocurre justo después del envío de
una orden: el botón permanece inactivo hasta que cambia el estado, y como máximo durante **2 minutos**.
**Detener el secado** solo está activo **durante un secado**.

**Rechazo « robot no está en la base ».** Una operación de estación exige que el robot esté en su base. Si no,
el plugin la rechaza y lo indica (ver la tabla de resolución de problemas). **Nunca** reenvía la orden por
sí solo: lleva el robot a la base y vuelve a empezar.

**Robot fuera de línea.** Los botones están inactivos, con una indicación. Los últimos estados conocidos siguen
mostrándose, con la fecha de su última actualización.

**Derechos.** Con solo el derecho de lectura, la pestaña es de consulta: ningún botón está activo y una
indicación lo explica.

#### Pestaña « Cronología del día »

Esta pestaña muestra, en una **línea de tiempo horaria**, lo que el robot ha hecho a lo largo de un día: una banda de
color, un color por estado. Es de **solo lectura** y **no consume ninguna cuota** de la nube de
Roborock: solo relee lo que el plugin ya ha registrado. Solo es visible si tienes el
derecho de **lectura** sobre el robot.

**Leyenda.** Cada color corresponde a una categoría:

| Categoría | Significado |
|---|---|
| **Limpieza** | El robot aspira o lava. |
| **Regreso a la base** | El robot vuelve a su base. |
| **En carga** | El robot está posado en su base. |
| **Vaciado del depósito** | La estación vacía el depósito. |
| **Lavado de la mopa** | La estación lava la mopa. |
| **Secado de la mopa** | La estación seca la mopa. |
| **En error** | El robot está en error. |
| **Sin conexión** | El robot no responde. |
| **Otro estado** | Cualquier estado que no tiene su propio color. |
| **Desconocido** | No se recibió ninguna información durante este período. |

**« Desconocido ».** Esta zona rayada cubre un período **sin datos**: demonio detenido, Jeedom apagado. El
plugin **nunca** prolonga el último estado conocido. Un período es « Desconocido » a partir de **15
minutos** sin noticias del robot.

**Limpiezas terminadas.** Bajo la línea de tiempo, una fina banda oscura (**Limpieza terminada**) resalta las
limpiezas del **registro de limpiezas** que coinciden con el día mostrado.

**Detalle.** Pasa el cursor (ratón) o toca (pantalla táctil) un período para mostrar su detalle bajo la
línea de tiempo.

**Navegación.** Los botones **Día anterior** y **Día siguiente** cambian de día. Se conservan los **7 últimos
días**; los más antiguos se eliminan automáticamente. Las horas son las de la **zona horaria de Jeedom**. Un día sin
registros muestra **Sin datos para ese día.**

**El historial empieza con la instalación de la actualización.** El plugin no tiene ningún medio de reconstruir
el pasado: los días anteriores no tienen datos.

#### Panel móvil (aplicación y versión móvil de Jeedom)

El panel de control también está disponible en el teléfono, en la aplicación móvil de Jeedom y en la
versión web móvil de Jeedom.

**Dónde encontrarlo.** Abre **Inicio**, después **Plugins**, después **JeeRoborock**. La pestaña dedicada del menú
personalizado de la aplicación móvil está reservada a los **administradores**: es un límite de Jeedom, no
del plugin. Tras la actualización del plugin, si la entrada no aparece, **resincroniza la aplicación**.
El administrador puede ocultar este panel en la configuración del plugin, del lado de Jeedom.

**Lo que contiene:**

- la elección del robot (si tienes varios);
- el mapa, con las habitaciones pulsables y las zonas prohibidas;
- las pestañas **Total**, **Habitación** y **Zona**: para una zona, traza el rectángulo con el dedo sobre el mapa,
  y luego muévelo o cambia su tamaño por sus esquinas;
- los ajustes (aspiración, caudal de agua, recorrido) cuando el robot los ofrece;
- los botones **Pausa**, **Reanudar**, **Detener** y **Volver a la base**;
- **Aspirar y luego fregar**, cuando el robot lo permite.

**Lo que no contiene.** La página **Estación y mantenimiento**, la **cronología del día** y la tabla
de las habitaciones detectadas no están disponibles en móvil: abre la página Mapa de Jeedom en un ordenador.

**Derechos.** Son los mismos que en el escritorio: con solo el derecho de lectura, el panel es de consulta.

**Actualizaciones.** La visualización se actualiza sola mientras el panel está en pantalla. Se suspende
cuando la aplicación pasa a segundo plano y se reanuda a tu regreso.

**Tras una actualización del plugin.** Si el panel se comporta de forma extraña, cierra por completo la
aplicación y vuelve a abrirla: puede haber quedado en caché una versión antigua.

## Control detallado

Según las capacidades detectadas en tu robot, pueden aparecer las siguientes órdenes:

- **Potencia de aspiración** y **caudal de agua** — una orden de información indica el nivel actual,
  una orden de acción (lista desplegable) permite elegir otro entre los realmente soportados por tu
  robot.
- **Recorrido de fregado** y **modo de limpieza** (solo aspiración / solo lavado / aspiración y
  lavado) — mismo principio: información + lista desplegable de acción.
- **Limpiar habitaciones** — una orden por habitación detectada (« Limpiar <nombre de la habitación> »),
  más una orden genérica « Limpiar habitaciones (nombres separados por comas) » que acepta una lista
  de nombres en texto libre. Como ocurre con las rutinas, el nombre de la orden sigue los renombrados
  hechos en la aplicación Roborock en la siguiente sincronización — incluso cuando el nombre de la
  habitación contiene un apóstrofo, un ampersand, una almohadilla o un porcentaje (« Aseo », por
  ejemplo) — salvo si has personalizado ese nombre a mano en Jeedom, en cuyo caso se conserva tu
  nombre personalizado. Para limpiar en varias pasadas, ver « Número de pasadas » más abajo.
- **Limpiar una zona** — recibe cuatro coordenadas `x1,y1,x2,y2` en milímetros y limpia el rectángulo
  correspondiente. El número de pasadas se ajusta como para las habitaciones (ver más abajo).
- **Número de pasadas** (órdenes « Limpiar habitaciones » y « Limpiar una zona ») — rellena el
  campo **Mensaje** de la orden, y luego indica 1, 2 o 3 (en cifras) en el campo **Título**.
  - **Es un parámetro de la orden en curso, no un ajuste.** No existe ninguna orden « Número de
    pasadas » que ajustar de una vez por todas: indícalo en cada orden, si no es una sola pasada.
    Nunca lo memoriza el robot ni el plugin.
  - Campo Título vacío: una sola pasada, como antes.
  - Un número de tres cifras o más (« 100 », « 2024 ») o texto (« dos ») se ignora: la limpieza se
    hace en una pasada, sin mensaje.
  - 0, un número de 4 a 99, un número con signo o decimal se rechazan (ver Resolución de problemas).
  - El mismo número se aplica a cada habitación de la orden; para una zona, se aplica a la zona.

  | Campo Título | Resultado |
  |---|---|
  | (vacío), 1 | Una pasada |
  | 2, 3 | Dos o tres pasadas |
  | 0, 4, 10, 99 | Rechazado: se espera un número entero de 1 a 3 |
  | -1, +2, 2.5, 2,5 | Rechazado: número con signo o decimal |
  | 100, 2024, dos, x2 | Ignorado: una sola pasada, sin mensaje |

  **Ejemplo de escenario**: acción « Limpiar habitaciones » con, en el campo Mensaje, « Cocina,
  Salón » (nombres ficticios) y, en el campo Título, 2: las dos habitaciones se limpian en dos pasadas.
  Para la zona, el campo Mensaje recibe `x1,y1,x2,y2` y el campo Título 2 o 3.
  - Los botones « Limpiar <habitación> » hacen siempre una sola pasada.
  - Cuando el campo Mensaje está vacío, el campo Título conserva su función habitual (nombres de
    habitaciones o coordenadas), a pesar de su título.
  - El campo se titula « Número de pasadas (1 a 3) » solo si el robot declara gestionar la
    repetición.
  - El ajuste de repetición de la aplicación Roborock nunca se modifica. Sin número de pasadas,
    el robot aplica su propio ajuste, como antes.
  - El plugin rechaza un número de pasadas de 2 o 3 si el robot, releído justo antes de la orden, no
    declara gestionar la repetición. Si la relectura falla, la orden se envía y decide el robot.
- **Desplazarse a un punto** — recibe dos coordenadas `x,y` en milímetros.
- **Aspirar y luego fregar** — encadena una pasada solo de aspiración y después una pasada solo de lavado. Cuatro
  órdenes, creadas solo si el robot sabe lavar:
  - **Aspirar y luego fregar (habitaciones separadas por comas, vacío para toda la vivienda)** (acción):
    campo **Mensaje** vacío = toda la vivienda; si no, nombres de habitaciones separados por comas (como
    « Limpiar habitaciones »). El **número de pasadas** se pone en el campo **Título** (1 a 3), solo para el
    alcance « habitaciones »; se aplica a las dos pasadas. Para toda la vivienda, no hay número de
    pasadas: una sola pasada por etapa.
  - **Cancelar la secuencia** (acción): detiene la secuencia en curso. Sin secuencia activa, responde
    que no hay nada que cancelar.
  - **Estado de la secuencia** (información): « Aucune séquence », « Passage 1 sur 2 : aspiration »,
    « En attente de la base », « Passage 2 sur 2 : lavage », « Séquence terminée », « Séquence annulée »,
    « Séquence interrompue », « Le second passage n'a pas pu démarrer » o « Séquence abandonnée »
    (etiquetas producidas por el demonio, que permanecen en francés).
  - **Motivo del fin de la secuencia** (información): « Aucun », o la razón por la que la secuencia se
    detuvo (ver Resolución de problemas). Estas dos informaciones no se historizan.

  **Ejemplo de escenario**: acción « Aspirar y luego fregar » con « Cocina, Salón » (nombres ficticios) en el
  campo Mensaje; un segundo bloque puede esperar a que « Estado de la secuencia » valga « Séquence terminée ».

  **Cómo se desarrolla la secuencia.**
  - La segunda pasada solo arranca cuando el **fin normal de la primera pasada está confirmado por el
    registro del robot** y el robot está **cargando de forma estable desde hace 30 segundos** en su base
    (el tiempo del eventual vaciado o lavado). Un robot que está vaciando nunca se vuelve a lanzar: el plugin
    espera.
  - **Espera máxima de la base: 15 minutos** tras el fin de la primera pasada. Pasado ese plazo, la segunda
    pasada no se lanza.
  - El plugin comprueba que el robot **ha arrancado realmente**: sin arranque constatado en **2 minutos**, la
    pasada se declara sin efecto.
  - **Duración máxima de una pasada: 6 horas.** Pasado ese plazo, la secuencia se detiene.
  - En cada final (logrado, cancelado o interrumpido), los **ajustes originales** del robot (aspiración,
    caudal de agua, recorrido) se **restablecen**. Durante la secuencia, el plugin los sustituye por
    ajustes « solo aspiración » y después « solo lavado ».
  - **Durante una secuencia, las demás limpiezas se rechazan**: limpiar habitaciones, una zona, lanzar
    una rutina, o « Iniciar » (salvo para **reanudar** una limpieza pausada). Cancela primero la
    secuencia.
  - **Detener** o **Volver a la base**, desde Jeedom o desde la aplicación móvil, ponen fin a la
    secuencia: la segunda pasada no se lanza.
  - **Ningún reintento automático**: si la segunda pasada no puede arrancar, no se reenvía nada.
    Vuelve a lanzar la secuencia tú mismo.
  - Lanzar una secuencia en un robot que ya está limpiando (o está en pausa) se rechaza.

Tras un ajuste de potencia de aspiración, caudal de agua, recorrido de fregado o modo de limpieza, el plugin
relee el estado del robot para comprobar que lo ha asumido. Le concede hasta una docena de segundos, sin
reenviar la orden: si el robot la asume enseguida, la respuesta no se ralentiza. El mensaje « no aplicado »
solo aparece si el robot sigue sin tener el valor al cabo de ese plazo. Si encadenas dos ajustes muy
rápido en el mismo robot, solo se verifica el último: el anterior se señala como « enviado al robot
(aplicación no confirmada) », sin error. El mismo mensaje aparece si el robot deja de responder durante la
verificación.

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

### Varios robots en la misma cuenta

Un robot apagado, sin batería o sin Wi-Fi ya no impide controlar y seguir a los demás robots de tu
cuenta: simplemente se muestra **fuera de línea**. Los intentos de reconexión a ese robot **no** consumen
la cuota de Roborock (ver « Cuotas de Roborock »).

Una vez vuelto a encender, el robot vuelve a ser controlable **por sí solo**, sin nueva autenticación ni
reinstalación. Cuenta **6 minutos como máximo** tras el regreso de su conexión: la espera entre dos
intentos se alarga progresivamente, hasta **5 minutos**.

Durante ese breve intervalo, el robot puede aparecer ya **en línea** mientras sus órdenes aún se rechazan
como **fuera de línea**. Espera unos minutos y vuelve a intentarlo.

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
| « Este mapa ya no existe en este robot: actualiza la lista de mapas. » | La lista de mapas mostrada está desactualizada | Haz clic en « Actualizar lista de mapas » y vuelve a intentarlo |
| « Se acaba de realizar un cambio de mapa: espere dos minutos antes de iniciar otro. » | El cambio de mapa es una operación lenta, protegida por una espera de dos minutos | Espera dos minutos antes de relanzar un cambio de mapa |
| « No se pudo decodificar el mapa del robot. Consulta el registro del demonio. » | El dato recibido de la estación es ilegible (incidente puntual del lado del robot o de la nube) | Vuelve a intentarlo más tarde; consulta el registro del demonio si el problema persiste |
| « La imagen del mapa es demasiado grande para transferirse. » | El mapa producido por el robot supera el tamaño que el plugin acepta almacenar | Vuelve a intentarlo más tarde; si el problema persiste, este robot no es compatible con esta función |
| « El robot debe estar en la base para iniciar esta operación. » | Se solicitó una acción de mantenimiento de la estación mientras el robot no estaba en su base | Espera a que el robot vuelva a su base, o lanza « Volver a la base » primero |
| « El robot está vaciando su depósito de polvo: no se envió la orden de limpieza… » | Se dio una orden de limpieza (« Iniciar », « Limpiar habitaciones », « Limpiar <habitación> », « Limpiar una zona ») mientras la estación vacía el depósito; el robot la habría ignorado | Espera a que termine el vaciado (de unos segundos a un minuto) y vuelve a enviar la orden. En un escenario, espera a que el estado del robot haya vuelto a « En charge » (en carga; etiqueta producida por el robot, en francés) antes de reenviarla |
| « Hay una secuencia «aspirar y luego fregar» en curso en este robot: cancélela antes de iniciar otra limpieza. » | Se pidió una limpieza (habitaciones, zona, rutina, « Iniciar ») durante una secuencia | Haz clic en « Cancelar la secuencia », o espera a que termine, y vuelve a lanzar |
| « El robot ya tiene una limpieza en curso o en pausa: deténgala antes de iniciar «aspirar y luego fregar». » | La secuencia se lanzó mientras el robot limpiaba o estaba en pausa | Detén la limpieza y vuelve a lanzar la secuencia |
| Secuencia interrumpida: « El robot se detuvo o volvió a la base durante la secuencia… » | Tú (o la aplicación móvil) usaste Detener o Volver a la base | Normal: la segunda pasada no se lanza. Vuelve a lanzar la secuencia si hace falta |
| Secuencia interrumpida: « El robot se detuvo con un error durante la secuencia… » | El robot señaló un error (atascado, depósito ausente…) | Consulta el estado del robot, resuelve el incidente y vuelve a lanzar |
| « El robot aceptó la orden de limpieza pero no se puso en marcha. » | Ningún arranque constatado en 2 minutos | Comprueba el estado del robot (depósito, vaciado en curso…) y vuelve a lanzar |
| « La primera pasada no terminó con normalidad según el registro del robot… » | El registro del robot no clasifica la primera pasada como terminada con normalidad | La segunda pasada no se lanza por precaución: consulta el registro de limpiezas y vuelve a lanzar si hace falta |
| « El registro del robot no pudo confirmar el fin normal de la primera pasada en el tiempo de espera… » (« Le second passage n'a pas pu démarrer ») | El registro del robot no confirmó el fin de la primera pasada en 15 minutos | El plugin nunca lanza el lavado sin esa confirmación: vuelve a lanzar la secuencia, o lanza un lavado solo a mano |
| « El robot no volvió a estar disponible en el tiempo máximo de espera tras la primera pasada. » | Tras la primera pasada, el robot no volvió a cargar en su base (de forma estable durante al menos 30 segundos) en 15 minutos (retirado de la base, vaciado bloqueado…) | Vuelve a poner el robot en su base y vuelve a lanzar la secuencia |
| « El robot se reinició fuera de la secuencia… » | Se lanzó una limpieza (por ejemplo desde la aplicación móvil) mientras se esperaba a la base | La segunda pasada no se lanza: vuelve a lanzar la secuencia cuando el robot esté en la base |
| « La pasada en curso no terminó en la duración máxima prevista… » | Una pasada dura más de 6 horas | La secuencia se detiene: comprueba el robot |
| « El plugin no pudo seguir al robot durante varios minutos… » | Robot o red inaccesibles durante varios minutos | El robot pudo continuar su pasada; sus ajustes originales no se restablecen: comprueba su modo de limpieza |
| « No se han podido restablecer los ajustes originales del robot… » | El restablecimiento falló al final de la secuencia | Comprueba y corrige el modo de limpieza del robot |
| « Séquence abandonnée »: « El demonio ya no sigue la secuencia… » | El demonio se detuvo o se reinició durante la secuencia (o el demonio murió) | La segunda pasada no se lanzará; el robot pudo continuar su pasada, y sus ajustes originales no se restablecen: compruébalos y vuelve a lanzar si hace falta |
| « La sesión Roborock del plugin cambió durante la secuencia… » | La cuenta se cambió o se retiró durante la secuencia | Misma consecuencia: ajustes no restablecidos, a comprobar |
| « Ninguna secuencia «aspirar y luego fregar» en curso en este robot: nada que cancelar. » | Se pidió **Cancelar la secuencia** sin que hubiera ninguna secuencia activa (ya había terminado) | Nada que hacer: consulta la línea **Secuencia** |
| « Cancelación registrada: el robot se detendrá… » | La cancelación se ha tenido en cuenta, pero todavía se está enviando una orden | Normal: espera unos segundos; el estado pasa a « Séquence annulée » |
| « Secuencia cancelada, pero la detención del robot ha fallado… » o « Secuencia cancelada; no se han podido restablecer los ajustes originales del robot. » | El robot no confirmó la detención, o el restablecimiento de sus ajustes falló | Comprueba el estado del robot, deténlo desde el panel si hace falta, y revisa sus ajustes |
| Botón « Aspirar y luego fregar » ausente | El robot no sabe lavar, o la pestaña Zona está abierta (la secuencia solo existe para Total y Habitación) | Normal: abre la pestaña Total o Habitación; en un robot sin lavado, la función no existe |
| « Número de pasadas no válido: indique un número entero de 1 a 3… » | El campo Título de una limpieza de habitaciones o de zona (con el campo Mensaje rellenado) contiene un número rechazado: 0, 4 a 99, con signo o decimal | Introduce 1, 2 o 3 en cifras, o deja el campo vacío para una sola pasada |
| « Número de pasadas no admitido por este robot… » | Se dio un número de pasadas de 2 o 3, pero el robot no declara gestionar la repetición | Vacía el campo del número de pasadas: la limpieza se hace entonces en una sola pasada |
| « Intervalo horario no válido: indique un inicio y un fin con formato HH:MM, entre 00:00 y 23:59. » (no molestar, horas valle) | Uno de los dos campos de « Definir… » está vacío, mal formado (22h00, 2200, 22:5) o fuera de límites (24:00, 22:60) | Introduce las dos horas en formato HH:MM (7:30 se acepta), entre 00:00 y 23:59, y vuelve a lanzar |
| « Intervalo horario no válido: el inicio y el fin … deben ser distintos. » | El inicio y el fin son idénticos | Elige dos horas distintas (se acepta un intervalo que cruza la medianoche, como 22:00 → 07:00) |
| « El robot no devolvió ningún intervalo … utilizable: defina el intervalo… » | « Activar » (no molestar u horas valle) no tiene ningún intervalo guardado que volver a aplicar | Lanza « Definir… » con un inicio y un fin: eso también activa la función |
| « Volumen no válido: indique un número entero entre 0 y 100. » | El valor está vacío, es decimal (50.5), negativo o superior a 100 | Indica un entero de 0 a 100; en una expresión de escenario, redondea con `round(...)` |
| « Este modo de vaciado (o de lavado) no está disponible en la estación de este robot: actualice su estado antes de volver a intentarlo. » | El código de modo solicitado no se conoce para esta estación (lista desactualizada, o código erróneo en un escenario) | Lanza « Actualizar », recarga la página del dispositivo y elige un modo en la lista de la orden |
| « Se acaba de enviar una orden (o un ajuste) … a este robot: espere unos segundos antes de enviar otra. » (bloqueo infantil, no molestar, horas valle, volumen, modo de vaciado, modo de lavado) | Dos órdenes del mismo tipo en el mismo robot con menos de 5 segundos de diferencia | Espera al menos 5 segundos; en un escenario, intercala una pausa de 5 segundos entre las dos acciones |
| « El robot (o la estación) no aplicó … : el estado leído no coincide con la solicitud. » (bloqueo infantil, no molestar, horas valle, volumen, modo de vaciado, modo de lavado) | El robot responde pero no adoptó el ajuste al cabo del plazo de verificación (unos segundos, hasta una docena) | Comprueba el valor mostrado por la orden de información correspondiente (muestra lo que el robot ha adoptado realmente), vuelve a lanzar la orden; si se repite, prueba con el robot en reposo o en su base |
| « Esta operación de mantenimiento no está disponible en la base de este robot: actualice su estado antes de volver a intentarlo. » | La estación de este robot no admite esta acción | Es normal: la orden no debería aparecer si la estación no lo permite; actualiza el estado del robot |
| « La lista de rutinas recibida de la nube Roborock está incompleta: por precaución, no se ha eliminado ninguna rutina. » | La respuesta de la nube se truncó, o este robot tiene más de 64 usos | Relanza la sincronización más tarde; no se ha perdido nada mientras tanto |
| « No se han aceptado las condiciones de uso de Roborock. » (o « Las condiciones de uso de Roborock han cambiado. ») | Roborock pide validar (o revalidar) sus condiciones de uso | Abre la aplicación móvil Roborock, acepta las condiciones propuestas, y vuelve a intentarlo desde Jeedom |
| « Robot desconocido para el demonio: vuelve a ejecutar una sincronización de dispositivos. » | El dispositivo Jeedom ya no es reconocido por el demonio (reinicio, robot retirado de la cuenta…) | Relanza « Sincronizar dispositivos » |
| « No se puede contactar con la nube Roborock: comprueba el acceso a Internet de Jeedom. » | Jeedom no logra contactar con los servidores de Roborock | Comprueba el acceso a Internet del servidor Jeedom |
| Un mensaje que mencione un plazo superado, una conexión fallida o « Varios intentos de comunicación han fallado: vuelve a intentarlo más tarde. » | El robot o la nube de Roborock tardó demasiado en responder: incidente de red pasajero, o robot muy solicitado | Vuelve a intentarlo tras un minuto; si se repite, comprueba la conexión Wi-Fi del robot y el acceso a Internet del servidor Jeedom |
| « El robot está ocupado: no puede procesar esta solicitud ahora. », « El robot rechazó la acción en su estado actual. » o « El robot indicó un error al ejecutar el comando. » | El robot no puede ejecutar esta solicitud en su estado actual (limpieza en curso, depósito lleno, incidente mecánico…) | Comprueba el estado del robot (orden « Estado », o aplicación móvil), resuelve el incidente notificado y vuelve a lanzar la acción |
| « Esta función no está disponible en este modelo de robot. » o « El robot no reconoce este comando. » | El robot no implementa esta función, aunque la orden exista en Jeedom | Ninguna manipulación desbloqueará la situación: esta función no existe en este equipo, oculta la orden si te molesta |
| « No hay ninguna solicitud de código en curso (es posible que el demonio se haya reiniciado): solicite un nuevo código. » | El demonio se reinició entre el envío y la validación del código | Haz clic de nuevo en « Enviar un código », y valida el nuevo código recibido |
| « … enviado al robot (aplicación no confirmada). » tras un ajuste | El plugin no pudo comprobar que el robot asumiera el valor: se envió otro ajuste justo después al mismo robot, o el robot dejó de responder durante la verificación. No es un error | Comprueba el valor que muestra la orden de información correspondiente; vuelve a enviar el ajuste si no es el correcto |
| Un ajuste (aspiración, caudal de agua, recorrido, modo de limpieza) no se aplica | El robot sigue sin tener el valor una docena de segundos después de recibirlo: rechaza este ajuste en su estado actual (por lo general: no está en reposo) | Vuelve a intentarlo cuando el robot esté en reposo o en su base |
| « Esta potencia de aspiración / este caudal de agua / este recorrido de fregado / este modo de limpieza no está disponible en este robot. » | La lista de niveles conocida por Jeedom está desactualizada (el robot ya no anuncia ese valor) | Actualiza el estado del robot y vuelve a intentarlo |
| « No tiene permiso para controlar este robot. » (panel de control y pestaña Estación y mantenimiento), botones en gris | Tu cuenta de Jeedom solo tiene el derecho de lectura sobre este robot | Pide a un administrador que te conceda el derecho de ejecución sobre este robot (gestión de usuarios de Jeedom) |
| « No hay ningún robot Roborock accesible con su cuenta. » (o « Dispositivo no encontrado o inaccesible. ») | Ningún robot activado sobre el que tu cuenta tenga derecho de lectura; el mismo mensaje sirve también para un robot inexistente o desactivado | Pide el derecho de lectura a un administrador, o comprueba que el robot esté activado |
| « 401 - Acceso no autorizado » al abrir la página Mapa | Tu sesión de Jeedom ha caducado | Vuelve a conectarte a Jeedom |
| La entrada JeeRoborock no aparece en Inicio | La casilla **Mostrar panel de escritorio** está desmarcada en la gestión del plugin | Márcala (ver « Panel « Carte » (Inicio > JeeRoborock) ») |
| « Robot sin conexión: los comandos están inactivos hasta que vuelva. » | El robot no responde a la nube de Roborock | Comprueba su alimentación y su Wi-Fi; los botones vuelven a estar activos cuando el robot regresa, sin recargar nada |
| « Función no disponible para este robot. » o un botón ausente del panel | El robot no gestiona este ajuste o esta acción | Normal: el panel solo ofrece lo que tu robot sabe hacer |
| « Orden rechazada por el robot. » (sin más precisión) | La orden se rechazó sin un mensaje más preciso | Comprueba el estado del robot (depósito, error, no está en la base) y vuelve a lanzar |
| El botón principal permanece inactivo, pestaña Habitación: « No hay ninguna habitación disponible para este robot: sincronice sus habitaciones desde la página del dispositivo. » | Todavía no se ha sincronizado ninguna habitación | Haz clic en « Resincronizar habitaciones » en la pestaña Dispositivo |
| « Demasiadas habitaciones elegidas: inicie la limpieza en varias veces. » | El número de habitaciones por orden está limitado | Desmarca habitaciones, lanza en varias veces |
| « Algunas habitaciones no se pueden elegir aquí… » o « Esta habitación no se puede elegir aquí… » | La habitación no tiene nombre, su nombre está duplicado o contiene una coma | Renómbrala en la aplicación Roborock y resincroniza las habitaciones |
| « Habitación desconocida en el mapa actual: resincronice las habitaciones desde la página del dispositivo. » | Una habitación marcada ya no existe en el mapa (nueva división, cambio de planta) | Desmárcala, o resincroniza las habitaciones; el botón de lanzamiento permanece inactivo mientras esté marcada |
| « Mapa antiguo: selección imposible. » o « El mapa no permite delimitar las habitaciones: elíjalas en la lista. » | El mapa mostrado es una imagen antigua, o no contiene contornos de habitaciones | Elige las habitaciones en la lista de la pestaña Habitación; el mapa se renueva durante las limpiezas |
| « Mapa no disponible: no se puede trazar la zona. », « Zona demasiado pequeña: trace un rectángulo más grande. » o « La zona debe estar completamente dentro del mapa. » | No hay ningún mapa utilizable, o el rectángulo es demasiado pequeño o sobresale del mapa | Traza un rectángulo más grande, completamente dentro del mapa; sin mapa, limpia por habitación o en Total |
| « Este robot no tiene estación. » (pestaña Estación y mantenimiento) | El robot no tiene estación de carga | Normal: nada que hacer |
| Botones **Vaciar**, **Lavar**, **Secar** inactivos, indicación « Operación en curso » | Hay una operación de estación en curso, o se acaba de enviar una orden (2 minutos como máximo) | Espera; **Detener el secado** solo está activo durante un secado |
| « Incidencia de la estación » o « Uno o varios consumibles deben cambiarse. » | La estación señala una incidencia, o un consumible está al 10 % o menos | Resuelve la incidencia; sustituye la pieza y luego usa **Restablecer** |
| « Sin datos para ese día. » o « Cronología no disponible por el momento. » (línea de tiempo) | Ningún estado registrado ese día (plugin instalado desde hace menos tiempo, o día fuera de los 7 últimos); o la lectura falló | Cambia de día; para la indisponibilidad, recarga la página. El mensaje « Día no válido o fuera del período conservado. » significa que se pidió un día de más de 7 días |
| Móvil: « No se puede cargar el panel: vuelva al inicio y ábralo de nuevo. » o « No se puede cargar el panel de comandos. Recargue la página. » | La lista de robots o los scripts del panel no se pudieron cargar (red, sesión, versión antigua en caché) | Vuelve a abrir el panel; si hace falta, cierra por completo la aplicación Jeedom y vuelve a abrirla |
| Móvil: « No disponible en móvil » | La página Estación y mantenimiento, la cronología y la tabla de habitaciones detectadas no existen en móvil | Normal: abre la página Mapa de Jeedom en un ordenador |
| « Habitación desconocida en el mapa actualmente activo de este robot. », « No hay ninguna habitación conocida para este robot. » o « Varias habitaciones tienen este nombre en este robot. » | El nombre introducido no corresponde a ninguna habitación detectada, aún no se ha sincronizado ninguna habitación, o el nombre es ambiguo | Resincroniza las habitaciones desde la pestaña Dispositivo, usa el nombre exacto de la aplicación Roborock, o la orden dedicada a esa habitación en lugar de la orden genérica |
| La orden « Habitación actual » permanece en « Pièce inconnue » | Las habitaciones nunca se han sincronizado, o el mapa activo ha cambiado | Haz clic en « Resincronizar habitaciones » en la pestaña Dispositivo |
| « Estas coordenadas superan los límites del mapa conocido de este robot. » | La zona o el punto introducido supera el mapa actualmente conocido del robot | Comprueba las coordenadas en el bloque « Zona y punto » de la pestaña Dispositivo, o actualiza la imagen del mapa |
| « Este consumible no se controla para este robot: actualiza su estado antes de reiniciarlo. » | La orden de reinicialización se utilizó antes de que el desgaste de ese consumible se hubiera reportado al menos una vez | Actualiza el estado del robot antes de reiniciar ese consumible |
| « Se acaba de realizar una sincronización de rutinas (o de habitaciones): espere un minuto antes de volver a intentarlo. » (rutinas, habitaciones o programaciones) | Ya se realizó una resincronización hace menos de un minuto | Espera un minuto antes de relanzar la misma resincronización |
| « El registro se acaba de actualizar: espere un minuto antes de volver a intentarlo. » | El botón « Actualizar el registro » ya se utilizó hace menos de un minuto | Espera un minuto antes de volver a hacer clic |
| « La generación del informe ha fallado. » | La solicitud a Jeedom no llegó a buen puerto: plazo de 20 segundos superado, conexión interrumpida o error del servidor Jeedom (un demonio detenido, en cambio, da un informe parcial, no este fallo) | Recarga la página de configuración y vuelve a intentarlo; si persiste, consulta el registro `jeeroborock` (menú « Analyse » > « Logs ») |
| « … rutina(s) no se pudieron registrar en Jeedom. Consulte el registro del plugin. » (en el resumen del panel « Rutinas ») | Un uso concreto no se pudo crear ni actualizar del lado de Jeedom durante la sincronización, mientras que el resto se desarrolló con normalidad | Consulta el registro `jeeroborock` (menú « Analyse » > « Logs ») para identificar el uso afectado, y vuelve a lanzar una sincronización |
| « 401 - Acceso no autorizado » al hacer clic en « Generar un informe de diagnóstico » | Tu sesión de Jeedom ha caducado, o tu cuenta no tiene derechos de administrador | Vuelve a conectarte a Jeedom con una cuenta administradora y vuelve a intentarlo |
| « Diagnóstico del demonio no disponible: informe parcial » | El demonio está iniciado, pero no pudo proporcionar la parte técnica del informe (incidente puntual) | El resto del informe sigue siendo utilizable; vuelve a intentarlo más tarde para obtener la sección técnica completa |

Para cualquier otro mensaje, el texto mostrado por el plugin da directamente la causa y, en su caso,
el gesto a realizar — nunca es necesario abrir los registros técnicos para entenderlo.

## Actualización del plugin

Las funciones de control manual (panel, mapa interactivo, estación, « aspirar y luego fregar », cronología
del día, panel móvil) **no requieren ninguna acción por tu parte** tras la actualización: ninguna
configuración que rehacer, ningún dispositivo que volver a crear. No obstante, dos gestos pueden ser útiles:
reiniciar el demonio (si no, los estados aparecen como « Otro estado » en la línea de tiempo) y, en móvil,
resincronizar o cerrar por completo la aplicación.

## Limitaciones conocidas

- El plugin solo controla robots compatibles con el protocolo V1 de Roborock, a través de la nube. Los
  robots más antiguos (protocolo A01) no son compatibles.
- Las etiquetas producidas por el propio robot (estado, error, estado de la estación, nombres de
  consumibles) permanecen **siempre en francés**, sea cual sea el idioma elegido para la interfaz de
  Jeedom. Lo mismo ocurre con los valores « Aucune pièce » y « Pièce inconnue » de la orden
  « Habitación actual ».
- Un cambio de mapa hecho desde la aplicación móvil ahora se detecta automáticamente, en segundo
  plano, en aproximadamente un minuto: el mapa activo, la imagen y el sistema de coordenadas del mapa
  se actualizan sin acción por tu parte (la lista de habitaciones, por su parte, se vacía y espera un
  clic en « Resincronizar habitaciones »). Durante ese breve plazo, la configuración puede seguir
  mostrando la planta anterior, y una página de Dispositivo ya abierta no se actualiza sola: recárgala. Del mismo modo,
  la orden « Habitación actual » puede designar brevemente (un minuto como máximo) una habitación de la planta
  anterior, y luego pasa a « Pièce inconnue » hasta la resincronización de las habitaciones.
- La conexión local mencionada más arriba (« Lo que el plugin hace, y lo que no hace ») no se puede
  desactivar desde Jeedom.
- El plugin muestra la versión del **firmware** del robot (pestaña « Dispositivo », actualizada en la
  sincronización de los dispositivos), pero no señala que haya una actualización disponible ni la
  activa: la actualización del firmware se hace desde la aplicación móvil Roborock.
- Más allá de **64 usos** registrados para un mismo robot, la sincronización de los usos sigue
  añadiendo y renombrando, pero ya no elimina automáticamente los usos desaparecidos de la aplicación.
- La imagen del mapa puede permanecer **ilegible** cuando el robot solo es accesible por la conexión
  local mencionada más arriba, sin pasar por el canal MQTT de la nube (mensaje « No se pudo
  decodificar el mapa del robot »).
- Un robot apagado o sin Wi-Fi que se reconecta vuelve a ser controlable por sí solo, pero tras un plazo que
  puede llegar a **6 minutos** (ver « Varios robots en la misma cuenta »): este plazo no es configurable.
- El rechazo de una orden de limpieza durante el vaciado del depósito solo afecta al estado « Vidage du bac
  à poussière » (vaciado del depósito de polvo): los demás estados de la estación (lavado, secado) no
  provocan este rechazo. No afecta ni a las rutinas (usos) ni a « Desplazarse a un punto ». Ninguna orden
  se pone en espera: te corresponde a ti (o a tu escenario) reenviarla.
- La actualización automática de la última limpieza está **acotada**: cinco relecturas como máximo, en los
  30 minutos posteriores al final de la limpieza. Pasado ese plazo, el plugin deja de insistir; usa
  « Actualizar el registro ».
- Un nombre de mapa ya guardado en forma codificada (antes de la actualización del plugin) sigue
  codificado hasta el primer « Actualizar lista de mapas » o cambio de mapa.
- La lectura de los nombres de habitación (panel « Habitaciones » de la pestaña Dispositivo) exige que
  el robot esté **en línea**: falla si el robot es inaccesible en el momento del clic.
- La vista de mapa (panel « Inicio > JeeRoborock ») no dispara nada por sí misma (una orden solo se envía
  con tu clic en el panel de control) y no lanza ninguna actualización: se limita a mostrar, cada 30
  segundos, la última imagen ya conocida. Esta imagen solo se reconstruye durante las limpiezas; en
  reposo, puede por tanto ser del último paso del robot.
- Panel móvil: versión **reducida** del panel de control. Ni la página Estación y mantenimiento, ni la
  cronología del día, ni la tabla de las habitaciones detectadas están disponibles en móvil: solo lo están en
  ordenador. La pestaña dedicada del menú personalizado de la aplicación Jeedom está reservada a los
  administradores. El panel no se ha probado en todos los teléfonos: un aparato puede presentar
  defectos de visualización.
- **Zonas prohibidas y muros virtuales**: mostrados en el mapa en **solo lectura**. Para crearlos,
  moverlos o eliminarlos, usa la aplicación Roborock; el plugin no bloquea una zona trazada sobre una
  zona prohibida.
- **Robot fuera de línea**: el panel, la página Estación y mantenimiento y el encadenamiento « aspirar y luego
  fregar » no aceptan ninguna orden nueva. Solo **Cancelar la secuencia** sigue siendo posible durante una
  secuencia. Los últimos estados y el último mapa siguen mostrándose.
- **Dos robots, dos secuencias**: cada robot tiene su propia secuencia « aspirar y luego fregar », seguida y
  cancelada independientemente de la del otro.
- **Estación y mantenimiento**: en un robot **sin estación**, la pestaña solo muestra « Este robot no tiene
  estación. ». En un robot con estación, solo aparecen las acciones y los estados que ese robot sabe hacer.
- **Cronología del día**: la línea de tiempo se reconstruye a partir de los estados que el **plugin ha
  registrado él mismo** (no se pide nada a la nube de Roborock). No contiene ningún dato anterior a la
  instalación de la actualización. Solo se conservan los **7 últimos días**; los más antiguos se
  eliminan. Más allá de un volumen de registros muy elevado para un mismo día, el registro de
  ese día se detiene: el final de la línea de tiempo de ese día queda vacío.
- Línea de tiempo « Cronología del día »: **« Sin conexión »** significa que el robot **no responde**; basta
  un solo plazo superado, no es forzosamente un corte largo.
- En la línea de tiempo, una **pausa** en mitad de una limpieza, el **desplazamiento hacia un objetivo**, la
  **cartografía** y la **colocación o retirada de la mopa** aparecen como **Otro estado**. El
  **secado** que tiene lugar durante la carga aparece como **En carga**: « Secado de la mopa » solo
  cubre el secado señalado como tal por el robot.
- Tras una actualización del plugin, mientras el **demonio no se haya reiniciado**, los estados aparecen como
  **Otro estado** en la línea de tiempo. Reinicia el demonio.
- La precisión de **« Desconocido »** es del orden de **unos minutos**: el inicio puede preceder a la parada
  real unos minutos. Un corte de **menos de 15 minutos** sin reinicio del demonio no aparece.
- Solo las **10 últimas limpiezas** del registro pueden resaltarse en la línea de tiempo.
- Las órdenes retomadas por el mosaico del panel de control (batería, limpiando, error, conectado,
  en línea y las cinco acciones de control) se ocultan una sola vez, al crear el mosaico. Si vuelves a
  mostrar una manualmente, el plugin nunca vuelve a ocultarla: tu elección se conserva.
- En una instalación actualizada desde una versión antigua del plugin, una migración técnica puntual
  pudo reactivar la historización de la orden « Error »: si no deseas historizar esta orden,
  desactívala manualmente en su configuración.
- Solo está probado el **Roborock Qrevo Curv**. Las capacidades añadidas por la paridad con Home Assistant
  (consumibles y depósitos de la estación, bloqueo infantil, no molestar, horas valle, volumen, modos de
  la estación, número de pasadas, habitación actual) **no tienen ninguna garantía** en otro modelo, el
  Roborock S7 incluido: el plugin crea las órdenes que el robot declara o a las que responde, sin
  haber podido verificar su efecto real en cada equipo. Una orden aceptada puede ser rechazada por el robot;
  entonces se señala (ver Resolución de problemas).
- El desgaste de la **bolsa de polvo** de la estación es de solo lectura: el plugin no tiene ninguna acción para
  reiniciarlo. Los porcentajes de los consumibles pueden diferir ligeramente de los de la aplicación.
- Los ajustes del aparato (bloqueo infantil, no molestar, horas valle, volumen, modos de la
  estación) **no se envían** al plugin por notificación: un cambio hecho desde la aplicación Roborock o el
  botón del robot solo aparece en Jeedom en la siguiente relectura (aproximadamente un minuto, o « Actualizar »).
- El plugin **nunca** reenvía una orden de ajuste por sí solo tras un rechazo o un fallo: vuelve a lanzarla
  tú mismo. Dos órdenes del mismo tipo en el mismo robot deben espaciarse al menos 5 segundos.
- « Desactivar » no molestar o las horas valle conserva normalmente el intervalo guardado, pero
  ese comportamiento depende del robot y no está confirmado.
- El número de pasadas es un parámetro de cada orden de limpieza por habitación o por zona, nunca un
  ajuste memorizado. Para una zona, la forma en que el robot interpreta el valor de repetición no ha podido
  confirmarse en todos los modelos: si « 2 » no da dos pasadas en tu robot, indícalo.
  Los botones « Limpiar <habitación> » siguen siendo de una sola pasada.
- Las listas de modos de vaciado y de lavado vienen de la biblioteca utilizada por el plugin, no de
  la estación: puede faltar un modo de la aplicación Roborock, y un modo propuesto puede ser rechazado por la
  estación. Un código de modo desconocido se muestra « Mode inconnu (N) ».
- La orden « Habitación actual » depende de la última imagen de mapa leída: puede tener un retraso
  de un minuto aproximadamente en reposo, y conserva su último valor si el robot está fuera de línea. Tras un
  cambio de mapa hecho desde la aplicación, puede designar brevemente una habitación de la planta
  anterior antes de pasar a « Pièce inconnue » (ver más arriba).
- **Aspirar y luego fregar**: si modificas un ajuste del robot (aspiración, caudal de agua, recorrido) durante
  una secuencia, el restablecimiento final lo **sobrescribe**. Si el plugin deja de seguir la secuencia
  (« Séquence abandonnée », reinicio del demonio) o si se cambia la cuenta, los ajustes originales
  **no se restablecen**: compruébalos. Una limpieza lanzada desde la **aplicación móvil** durante una
  pasada no es rechazada por el plugin: se constata a posteriori y la secuencia se detiene sin
  lanzar la segunda pasada. Si el robot no señala el estado de limpieza, puede que no se detecte el fin de una pasada:
  la secuencia se detiene entonces a las 6 horas. Un modo original personalizado o
  « inteligente » se restablece al ajuste estándar más próximo.

Esta página se actualiza con cada nueva funcionalidad entregada por el plugin.
