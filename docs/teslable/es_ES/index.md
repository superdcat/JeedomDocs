# Plugin Tesla BLE

Este plugin permite controlar la carga, la climatización y algunas funciones básicas de sus vehículos **Tesla** desde Jeedom, **mediante Bluetooth (BLE)** y sin pasar por la API en la nube de Tesla.

Jeedom no habla directamente con el vehículo: se apoya en un proxy [TeslaBleHttpProxy](https://github.com/superdcat/TeslaBleHttpProxy) (el fork mantenido para este plugin, derivado del proyecto de [wimaha](https://github.com/wimaha/TeslaBleHttpProxy)), instalado en un pequeño dispositivo con Bluetooth (una Raspberry Pi, véase [Elegir e instalar la Raspberry Pi](#elegir-e-instalar-la-raspberry-pi)) situado al alcance del vehículo, normalmente en el garaje. El plugin consulta este proxy por HTTP en su red local.

```
Jeedom  --HTTP-->  TeslaBleHttpProxy (Raspberry Pi)  --Bluetooth-->  Vehículo
```

## Requisitos previos

- Jeedom 4.5 como mínimo, sobre Debian 11 o 12.
- **TeslaBleHttpProxy 2.3.0 como mínimo**, instalado, operativo y accesible desde Jeedom. Se recomienda la **imagen del fork** `ghcr.io/superdcat/tesla-ble-http-proxy`; la imagen de wimaha (2.3.0 o más reciente) sigue siendo aceptada. El plugin ignora el sufijo `-tb.N` de las versiones del fork: `2.3.0-tb.2` se considera conforme a «2.3.0 como mínimo». Procedimiento completo paso a paso, en una Raspberry Pi Zero 2 W: [Instalar el proxy BLE](installation-proxy.md).
- La **llave del proxy emparejada con el vehículo**. Este paso se realiza íntegramente en la interfaz de TeslaBleHttpProxy (generación de la llave y, después, validación con su tarjeta llave en el vehículo): véase [Instalar el proxy BLE](installation-proxy.md#8-generar-la-llave-y-emparejarla-con-el-vehiculo).
- El **VIN** de cada vehículo que se vaya a controlar (visible en la parte inferior de la pantalla principal de la aplicación Tesla).

> **Consejo**
>
> Antes de configurar el plugin, compruebe que el proxy responde abriendo en un navegador `http://<ip_del_proxy>:<puerto>/api/proxy/1/version` (versión del proxy) y, a continuación, `http://<ip_del_proxy>:<puerto>/api/1/vehicles/<VIN>/body_controller_state`. Debe obtener una respuesta JSON.

### Comprobar y actualizar la versión del proxy

El plugin exige **TeslaBleHttpProxy 2.3.0 como mínimo**. Siga estos pasos para conocer la versión de su proxy y actualizarla si es necesario. Con la imagen del fork, la versión tiene la forma `2.3.0-tb.2` (versión base de wimaha, seguida del número de versión del fork).

**1. Leer la versión actual**

1. En un ordenador de la misma red que el proxy, abra un navegador.
2. En la barra de direcciones, escriba `http://<ip_del_proxy>:<puerto>/api/proxy/1/version`, por ejemplo `http://192.168.1.50:8080/api/proxy/1/version`.
3. Lea la respuesta: contiene `"version"` seguido de la versión del proxy, por ejemplo `2.3.0` con la imagen de wimaha. Con la imagen del fork, la respuesta contiene además `"flavor":"superdcat"` y una versión como `2.3.0-tb.2`.

Si esta versión es **2.3.0 o más reciente**, no tiene nada que hacer por el plugin. De lo contrario, pase al paso 2.

**2. Actualizar la imagen del proxy**

1. Conéctese por SSH a la Raspberry Pi que aloja el proxy.
2. Sitúese en la carpeta que contiene el archivo `docker-compose.yml` del proxy (la carpeta `TeslaBleHttpProxy` si ha seguido [Instalar el proxy BLE](installation-proxy.md)):

   ```
   cd TeslaBleHttpProxy
   ```

3. En `docker-compose.yml`, compruebe la línea `image:`: debe ser `image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2` (o una versión más reciente del fork). Si apunta a la imagen de wimaha, véase [Pasar de la imagen de wimaha a la imagen del fork](installation-proxy.md#pasar-de-la-imagen-de-wimaha-a-la-imagen-del-fork). Si lleva un número de versión concreto, cambie ese número.
4. Descargue la imagen y vuelva a iniciar el proxy con ella:

   ```
   docker compose pull && docker compose up -d
   ```

   Reiniciar la Raspberry Pi o usar `restart: always` **no actualiza la imagen**: véase [Actualizar la imagen del proxy](installation-proxy.md#actualizar-la-imagen-del-proxy).

**3. Volver a comprobar la versión**

Vuelva a abrir `http://<ip_del_proxy>:<puerto>/api/proxy/1/version` en el navegador (espere unos segundos a que el proxy se reinicie) y compruebe que la versión es 2.3.0 o más reciente.

La llave emparejada con el vehículo se almacena en la carpeta `key` montada por el archivo `docker-compose.yml`: se **conserva** con la actualización, no tiene que repetir el emparejamiento.

> **IMPORTANTE**
>
> Con un proxy anterior a la 2.1.1, el plugin no puede leer el estado del vehículo: el bloqueo y el estado de reposo dejan de actualizarse, la presencia ya no vuelve a 1, y el log del plugin indica «Version du proxy non prise en charge : 2.3.0 minimum, mettez le proxy à jour» (_«Versión del proxy no compatible: 2.3.0 como mínimo, actualice el proxy»_) (línea en error).

### Elegir e instalar la Raspberry Pi

El proxy debe estar **al alcance Bluetooth del vehículo** (de 5 a 10 m, por tanto, en general en el garaje). Es la Raspberry Pi la que debe estar cerca del coche, no Jeedom.

| Placa | Veredicto |
|---|---|
| **Raspberry Pi Zero 2 W** | Recomendada: pequeña, de bajo consumo, con imagen Docker del proxy disponible para este procesador. |
| Raspberry Pi Zero W (primera generación) | No recomendada: procesador ARMv6 que las versiones recientes de Docker ya no admiten, y adaptador Bluetooth que tiende a bloquearse al cabo de unas horas. |
| Raspberry Pi 3, 4, 5 o miniPC con Bluetooth | Adecuada, siempre que esté al alcance del vehículo. |

El procedimiento detallado, con los comandos, los ajustes y la resolución de problemas, está en la página [Instalar el proxy BLE](installation-proxy.md). En resumen, la instalación consiste en:

1. Instalar Raspberry Pi OS **64 bits Lite** y Docker.
2. Ejecutar la imagen `ghcr.io/superdcat/tesla-ble-http-proxy` (fork recomendado; la imagen `wimaha/tesla-ble-http-proxy` sigue siendo una alternativa).
3. Abrir `http://<ip_de_la_pi>:8080/dashboard`, generar la llave, introducir el VIN, **despertar el vehículo**, enviar la llave y, a continuación, colocar la tarjeta llave en la consola central para validar.
4. Asignar una **dirección IP fija** a la Raspberry Pi (reserva DHCP en su router), ya que su dirección se registra en el plugin.

Algunos consejos para un funcionamiento estable:

- Utilice una fuente de alimentación de calidad (5 V, 2,5 A): una alimentación débil provoca desconexiones Bluetooth.
- No utilice el Bluetooth de esta Raspberry Pi para otra cosa: el proxy necesita el adaptador para él solo.
- Un vehículo solo admite **3 dispositivos Bluetooth conectados a la vez** (teléfonos, reloj, proxy). Por encima de ese número, las conexiones se vuelven intermitentes.

### Rol de la llave

Con TeslaBleHttpProxy (fork o wimaha 2.3.0), la llave generada por defecto tiene el rol **Charging Manager**. Basta para leer el estado del vehículo y controlar la carga, pero el vehículo **rechaza** algunos comandos. Para utilizarlos, genere y empareje una llave con rol **Owner** desde el panel del proxy (enlace en la configuración del plugin).

| Rol de la llave | Comandos afectados (lista orientativa) |
|---|---|
| **Charging Manager**: funciona | Lecturas (presencia, bloqueo, carga, climatización), **Actualizar**, **Despertar**, **Iniciar la carga**, **Detener la carga**, **Corriente de carga** |
| **Charging Manager**: funciona (funciones de carga avanzada) | **Ajustar según el excedente** y la **Carga en horas valle** solo envían **Corriente de carga**, **Iniciar la carga** y **Detener la carga**: basta una llave Charging Manager. |
| **Charging Manager**: no confirmado | **Añadir una programación de carga** y **Eliminar la programación de carga**: el rol mínimo no está confirmado (probablemente Charging Manager; pruebe y pase a Owner si el vehículo lo rechaza). Estas dos acciones también exigen el proxy del fork (véase [Programar la carga](#programar-la-carga)). |
| **Charging Manager**: rechazado | **Bloquear las puertas**, **Desbloquear las puertas**, **Tocar el claxon**, **Hacer parpadear las luces**, **Modo Centinela**; probablemente también **Iniciar la climatización** y **Detener la climatización** |
| **Charging Manager**: rechazado (probable) | **Consigna del conductor** y **Consigna del pasajero**: se supone que el rol Owner es necesario (no confirmado en uso real). Estas dos acciones también exigen el proxy del fork (véase [Ajustar la consigna de temperatura](#ajustar-la-consigna-de-temperatura)). |
| **Charging Manager**: rechazado (probable) | Las seis acciones **Ajustar la calefacción del asiento …** y **Ajustar la calefacción del volante**: se supone que el rol Owner es necesario (no confirmado en uso real). También exigen el proxy del fork (véase [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante)). |
| **Charging Manager**: rechazado (probable) | **Desempañado máximo**: se supone que el rol Owner es necesario (no confirmado en uso real). Esta acción también exige el proxy del fork (véase [Desempañado máximo](#desempanado-maximo)). |
| **Charging Manager**: rechazado (probable) | **Modo de mantenimiento de clima**: se supone que el rol Owner es necesario (no confirmado en uso real). Esta acción también exige el proxy del fork (véase [Modo perro, camping y mantenimiento de clima](#modo-perro-modo-camping-y-mantenimiento-de-clima)). |
| **Charging Manager**: rechazado (probable) | **Abrir el maletero trasero** y **Abrir el maletero delantero**: se supone que el rol Owner es necesario (no confirmado en uso real). Estas dos acciones también exigen el proxy del fork (véase [Abrir el maletero trasero y el maletero delantero](#abrir-el-maletero-trasero-y-el-maletero-delantero)). |
| **Charging Manager**: rechazado (probable) | **Preacondicionamiento planificado por Jeedom**: solo envía **Iniciar la climatización** y **Detener la climatización**, para los que se supone que el rol Owner es necesario (no confirmado en uso real). Con una llave Charging Manager, solo se hace un intento por salida (véase [Preacondicionamiento planificado por Jeedom](#preacondicionamiento-planificado-por-jeedom)). |
| **Owner** | Todos los comandos |

Esta lista es orientativa: es el vehículo quien decide.

**El plugin reconoce este rechazo.** Cuando el vehículo rechaza por falta de permisos uno de los comandos de la fila «rechazado» anterior:

- se muestra el mensaje «Este comando requiere una llave con rol Owner: la llave del proxy probablemente tiene el rol Charging Manager…» (también se copia en **Último error**);
- la información **Rol de la llave** del dispositivo pasa a **Charging Manager**;
- en la pestaña **Comandos** del dispositivo, estos comandos llevan una insignia gris **Rol insuficiente**.

Los comandos siguen presentes y se pueden utilizar: un escenario que los llame recibe el mismo mensaje. **No aparecen atenuados en el dashboard**: fíese de la información **Rol de la llave**. El plugin no avisa de antemano: el primer rechazo es el que revela el rol.

**Pasar a una llave Owner.** Genere y empareje una llave con rol **Owner** siguiendo [Generar la llave y emparejarla con el vehículo](installation-proxy.md#8-generar-la-llave-y-emparejarla-con-el-vehiculo) (elección del rol: [Elegir el rol de la llave](installation-proxy.md#elegir-el-rol-de-la-llave)). Vuelva a ejecutar a continuación uno de estos comandos: en cuanto tenga éxito, **Rol de la llave** vuelve a **Owner** y la insignia desaparece al recargar la página.

Con la imagen del fork, el rol de la llave activa también se puede leer a mano: abra `http://<ip_del_proxy>:<puerto>/api/proxy/1/capabilities` y mire `key_role` (`owner` o `charging_manager`, vacío si no hay ninguna llave instalada); el plugin no utiliza esta información. El comportamiento del **Límite de carga** y de la apertura y el cierre del puerto de carga con una llave Charging Manager no está confirmado: la [documentación del proxy](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md#step-3-generate-key-for-vehicle) solo menciona el despertar, el inicio y la parada de la carga y la corriente de carga.

> **IMPORTANTE**
>
> Por defecto, el proxy **no tiene ninguna autenticación**. El fork puede exigir un token (`apiToken`): introduzca entonces el mismo en **Token de API del proxy** (véase [Configuración del plugin](#configuracion-del-plugin)). Con una llave Owner, cualquier dispositivo de su red local puede desbloquear el vehículo. Mantenga el proxy en una red de confianza, idealmente aislada, y **no** exponga nunca su puerto a Internet. Si solo controla la carga, prefiera una llave Charging Manager.

## Configuración del plugin

Tras la instalación, active el plugin y abra su página de configuración (**Complementos > Gestión de plugins > Tesla BLE**). Incluye tres ajustes: la URL del proxy, el token de API del proxy (opcional) y el umbral de alerta de Bluetooth bloqueado.

| Campo | Valor esperado |
|---|---|
| **URL del proxy** | La dirección de TeslaBleHttpProxy con su puerto, por ejemplo `http://192.168.1.50:8080/`. Debe empezar por `http://` o `https://`. Se utiliza un único proxy para todos los vehículos. |
| **Token de API del proxy** | Opcional: introdúzcalo solo si el proxy del fork tiene un `apiToken` (mismo valor). El mismo token sirve para todos los proxys. Se guarda **cifrado** y **nunca se vuelve a mostrar**: el campo permanece vacío e indica «Token guardado: deje vacío para conservarlo». Déjelo vacío para conservar el token guardado; **Eliminar el token** lo borra. |
| **Probar** (botón) | Comprueba que el proxy responde y muestra su versión. Prueba la URL y el token introducidos, **aunque no estén guardados** (campo de token vacío: el token guardado). También indica la autenticación: **«Proxy sin autenticación: no se requiere token»**, **«Token de API aceptado por el proxy»**, **«El proxy exige un token de API»** (ningún token introducido ni guardado) o **«Token de API rechazado por el proxy»** (token distinto de `apiToken`). |
| **Abrir el panel del proxy (emparejamiento de las llaves)** (enlace) | Abre el panel del proxy en una pestaña nueva, para generar y emparejar la llave. |
| **Logs del proxy** (botón, línea **Diagnóstico**) | Muestra las últimas líneas de logs del proxy en una ventana, sin sesión SSH en la Raspberry Pi. Utiliza la URL **guardada**. |
| **Umbral de alerta de Bluetooth bloqueado** | Número de lecturas consecutivas con tiempo de espera agotado, mientras el proxy responde, antes de avisarle de que el adaptador Bluetooth de la Raspberry Pi probablemente está bloqueado. Entero de 2 a 288 (se hace una lectura con el intervalo de actualización del vehículo, 5 minutos por defecto: 288 = un día de lecturas con este valor por defecto); déjelo vacío para el valor por defecto, **3**, mostrado en gris. Véase [Alerta de adaptador Bluetooth bloqueado](#alerta-de-adaptador-bluetooth-bloqueado). |
| **Versión mínima del proxy** | Información de solo lectura: la versión mínima de TeslaBleHttpProxy admitida (2.3.0). |

### La URL se normaliza al guardar

No tiene que preocuparse por la forma exacta de la dirección: al guardar, el plugin elimina los espacios alrededor de la URL, pone `http`/`https` en minúsculas y **añade la `/` final** si hace falta: la `/` final y las mayúsculas de `http://` carecen, por tanto, de importancia, `HTTP://192.168.1.50:8080` y `http://192.168.1.50:8080/` designan el mismo proxy. Tras guardar, el campo muestra la dirección corregida.

La URL se rechaza, con un mensaje en rojo y sin modificar el valor anterior, en los casos siguientes:

- está vacía o no empieza por `http://` o `https://`;
- contiene credenciales (`usuario:contraseña@`);
- contiene caracteres no admitidos (espacios intermedios, acentos, parámetros `?...`, ancla `#...`), un puerto no válido, o supera los 255 caracteres.

### Probar el proxy

Haga clic en **Probar**: el plugin consulta la versión del proxy (10 segundos como máximo) y muestra el resultado bajo el campo. La prueba no comprueba ni la llave emparejada ni el vehículo: solo demuestra que el proxy es accesible. Véase [Resolución de problemas](#solucion-de-problemas) para el significado de cada mensaje.

### Enlace al panel del proxy

El enlace aparece en cuanto se guarda (o se prueba) una URL válida. Apunta a `<URL del proxy>dashboard`. Si ha declarado el proxy mediante un **nombre de servicio Docker** (por ejemplo `http://teslablehttpproxy:8080/`), Jeedom sabe acceder a él pero **su navegador no**: el enlace no se abrirá. Abra entonces el panel con la dirección IP de la Raspberry Pi (`http://<ip_de_la_pi>:8080/dashboard`).

### Consultar los logs del proxy

El botón **Logs del proxy** abre una ventana que muestra las **200 últimas líneas** de logs del proxy (la más reciente abajo), con su hora en la zona horaria de Jeedom y su nivel (`[DEBUG]`, `[INFO]`, `[WARN]`, `[ERROR]`). El botón **Actualizar** vuelve a leer los logs. La lectura no solicita el vehículo y responde en 10 segundos como máximo, incluso mientras un comando ocupa el proxy.

- La función requiere el proxy **2.3.0** o más reciente y utiliza la URL **guardada**: después de cambiar la URL, guarde antes de abrir los logs.
- Las líneas se muestran **tal cual**, en texto sin formato: un contenido como `<script>` o `&` aparece literalmente, sin ningún efecto. Cada línea está limitada a 1000 caracteres.
- Los VIN están ocultos (solo se ven los 4 últimos caracteres). Las líneas pueden contener la dirección IP de los clientes del proxy y el contenido de los comandos enviados: revise una captura antes de publicarla en un foro.
- El proxy también conserva sus líneas **Debug**, sea cual sea su nivel de log: las 200 líneas suelen cubrir, por tanto, menos de una hora de actividad. Sus logs se borran cada vez que se reinicia el proxy.
- Las líneas del proxy nunca se copian en el log del plugin. Función reservada a los administradores de Jeedom.

Véase [Mensajes de la ventana Logs del proxy](#mensajes-de-la-ventana-logs-del-proxy) en caso de mensaje de error.

### Alerta de adaptador Bluetooth bloqueado

En algunas Raspberry Pi (en particular la Zero W de primera generación), el adaptador Bluetooth se bloquea al cabo de unas horas: el proxy sigue respondiendo (el botón **Probar** está en verde, **Proxy accesible** vale 1) pero cada lectura del vehículo agota el tiempo de espera. El plugin detecta esta situación y le avisa:

- cuando la lectura del estado de un vehículo agota su tiempo de espera **3 veces seguidas** (o el umbral configurado) mientras el proxy responde, aparece un mensaje **«Adaptador Bluetooth del proxy probablemente bloqueado — …»** en el centro de mensajes de Jeedom, **una sola vez** mientras dure la situación;
- mientras tanto, **Último error** muestra **«Adaptador Bluetooth del proxy probablemente bloqueado: reinicie la Raspberry Pi»**;
- en cuanto una lectura vuelve a tener éxito (incluido un vehículo dormido que responde), el log anota la vuelta a la normalidad (nivel **Info**) y la alerta se rearma: una nueva serie provocará un nuevo mensaje, que sustituye al anterior.

Un tiempo de espera agotado aislado, un vehículo fuera de alcance o un proxy apagado no activan la alerta. El mensaje permanece en el centro de mensajes tras la vuelta a la normalidad: elimínelo usted mismo. Con varios vehículos en el mismo proxy, cada vehículo tiene su propio mensaje. Los clics en **Actualizar** cuentan como lecturas.

Qué hacer: reinicie la Raspberry Pi que aloja el proxy. Si se repite, pase a una Raspberry Pi Zero 2 W y utilice una fuente de alimentación de calidad (5 V, 2,5 A).

## Configuración de los dispositivos

Cada vehículo es un dispositivo. Vaya a **Complementos > Objetos conectados > Tesla BLE**, haga clic en **Añadir** y dé un nombre al vehículo.

En la pestaña **Dispositivo**:

| Campo | Valor esperado |
|---|---|
| **Nombre del dispositivo** | El nombre del vehículo, a su elección. |
| **Objeto padre** | El objeto de Jeedom en el que se ubica el vehículo (o **Ninguno**). |
| **Categoría** | Las categorías de Jeedom del dispositivo (casilla de verificación). |
| **Activar** | Marcada: el vehículo se actualiza con su **intervalo de actualización** (5 minutos por defecto). Desmarcada: ya no se lee, sea cual sea su intervalo. |
| **Visible** | Marcada: el widget del vehículo se muestra en el dashboard. |
| **VIN** | El número de serie del vehículo: **17 caracteres**, cifras y letras **excepto I, O y Q** (ejemplo ficticio: `5YJ3E1EA7KF000000`). Debe ser el declarado en TeslaBleHttpProxy. |
| **URL del proxy de este vehículo** | Opcional. La dirección del proxy del garaje de este vehículo, con su puerto (por ejemplo `http://192.168.1.51:8080/`). **Vacío: el vehículo utiliza la URL de la configuración del plugin.** |
| **Probar este proxy** (botón) | Muestra la versión del proxy que utiliza este vehículo. Prueba el valor introducido, **aunque no esté guardado**; campo vacío: se prueba la URL de la configuración del plugin. |
| **Intervalo de actualización** | Frecuencia de lectura de este vehículo: **1, 2, 5, 10, 15 o 30 minutos**. Por defecto **5 minutos** (los vehículos existentes mantienen este comportamiento tras la actualización). Cuanto más corto es el intervalo, más recientes son los datos, pero más se solicita el proxy y, con el vehículo despierto, más se puede retrasar su puesta en reposo; un intervalo largo cuida la Raspberry Pi. **1 minuto** es adecuado para uno o dos vehículos por proxy (recomendado; ajústelo según su instalación): por encima, una lectura lenta puede superar el minuto. Un valor desconocido se reduce a 5 minutos. Un cambio surte efecto en la lectura siguiente, sin reinicio. Esta lectura nunca despierta el vehículo. |
| **Intervalo durante la carga** | **Desactivado por defecto** (comportamiento sin cambios), o **1, 2, 5, 10 o 15 minutos**. Durante una carga, sustituye al intervalo de actualización **cuando es más corto**; el ritmo normal se recupera en cuanto una lectura ya no detecta la carga. Un minuto como mínimo: Jeedom lanza la actualización cada minuto y el proxy guarda los datos 30 segundos en caché. No despierta nunca el vehículo. Véase [Lectura acelerada durante la carga](#lectura-acelerada-durante-la-carga). |
| **Dejar que el vehículo se duerma** (casilla **Activar**) | Marcada por defecto (incluso en los vehículos existentes tras la actualización). Cuando el vehículo está despierto pero inactivo, el plugin deja de leer los datos de carga y de climatización durante una ventana, para no impedir que se duerma. Desmarcada: se hace una lectura completa en cada pasada, como antes. Véase [Dejar que el vehículo se duerma](#dejar-que-el-vehiculo-se-duerma). |
| **Lecturas sin cambios antes de la ventana** | Número de lecturas sucesivas sin ningún cambio (sin carga, sin ocupante) antes de abrir la ventana: **1, 2, 3, 4, 5, 10 o 15**. Por defecto **3** (15 minutos de inactividad con el intervalo de 5 minutos). |
| **Duración de la ventana** | Tiempo durante el cual los datos dejan de leerse: **15, 20, 30, 45 minutos, 1 hora, 1 hora 30 o 2 horas**. Por defecto **30 minutos**. Sin efecto si no supera el intervalo de actualización: elija una duración superior al intervalo. |
| **Retardo de relectura tras un comando** | Tiempo de espera antes de volver a leer el vehículo tras un comando correcto: **30 segundos (por defecto), 45 segundos, 1 minuto, 1 minuto 30 o 2 minutos**. 30 segundos es el mínimo: es el tiempo durante el cual el proxy guarda sus datos en caché (véase [Relectura tras un comando](#relectura-tras-un-comando)). Aumente el valor si ha alargado esta caché en el proxy. |
| **Leer también la climatización** | **Sí (por defecto)**: se leen la carga y la climatización, como antes de la actualización. **No, solo carga**: solo se piden al proxy los datos de carga, en cada actualización y a petición (**Actualizar**, **Actualizar (con despertar)**, relectura tras un comando). La petición es más corta y solicita menos el enlace Bluetooth (la ganancia debe medirse en su instalación). La información de climatización conserva entonces su último valor y deja de actualizarse; los comandos de climatización siguen siendo utilizables. Volver a **Sí** retoma la lectura de ambas familias en la pasada siguiente, con el vehículo despierto. |
| **Tensión de la red (V)** | Control según el excedente: tensión entre fase y neutro utilizada para convertir la potencia disponible en corriente. Vacío: **230 V**. Entero de 100 a 250. |
| **Fases** | Control según el excedente: **Monofásico (por defecto)** o **Trifásico**. La potencia se divide por la tensión y por este número para obtener la corriente **por fase**. |
| **Paso de ajuste (A)** | Control según el excedente: la corriente calculada se redondea **a la baja** a un múltiplo de este paso. Vacío: **1 A**. Entero de 1 a 16. |
| **Histéresis (A)** | Control según el excedente: ningún comando mientras la corriente calculada se desvíe **menos** de este valor de la última consigna enviada. Vacío: **2 A**. Entero de 0 a 16. |
| **Intervalo mínimo entre comandos (s)** | Control según el excedente: plazo mínimo entre el **final** de un comando del control y el siguiente. Vacío: **120 s**. Entero de 60 a 3600 (un comando puede durar hasta 75 segundos y el proxy guarda los datos 30 segundos en caché). |
| **Corriente mínima de arranque (A)** | Control según el excedente: con la carga detenida, se reanuda cuando la corriente calculada alcanza este valor. Vacío: **6 A**. Entero de 1 a 80. |
| **Umbral de parada (A)** | Control según el excedente: durante la carga, la corriente nunca se ajusta por debajo de este umbral; si sigue calculándose por debajo durante la duración de mantenimiento, la carga se detiene. Vacío: **5 A**. Entero de 1 a 80, **nunca superior a la corriente mínima de arranque**. |
| **Duración de mantenimiento antes de la parada (s)** | Control según el excedente: tiempo durante el cual la corriente calculada debe permanecer por debajo del umbral de parada antes de detener la carga. Vacío: **300 s**. Entero de 0 a 3600. |
| **Control de la carga** (casilla **Activar**, sección **Carga en horas valle**) | **Desmarcada por defecto.** Marcada, Jeedom inicia y detiene la carga durante el intervalo horario siguiente (véase [Carga en horas valle](#carga-en-horas-valle)). Solo se activa si se han indicado el inicio, el fin y el SoC objetivo. |
| **Inicio del intervalo** | Carga en horas valle: hora de inicio del intervalo, en formato `HH:MM` (hora de Jeedom, por ejemplo `22:00`; también se acepta `22h00`). |
| **Fin del intervalo** | Carga en horas valle: hora de fin del intervalo, en formato `HH:MM`, **distinta** del inicio. Un fin anterior al inicio da un intervalo **a caballo sobre la medianoche** (`22:00` a `06:00`). |
| **SoC objetivo (%)** | Carga en horas valle: nivel de batería en el que se detiene la carga durante el intervalo. Entero de **1 a 100**. |
| **Detener al final del intervalo** | Carga en horas valle: **desmarcada por defecto**. Marcada, la carga que siga en curso al final del intervalo se detiene (en la primera lectura del vehículo, en la hora siguiente). Desmarcada, continúa hasta el límite del vehículo. |
| **Control de la climatización** (casilla **Activar**, sección **Preacondicionamiento planificado por Jeedom**) | **Desmarcada por defecto.** Marcada, Jeedom inicia la climatización antes de la hora de salida y después la detiene (véase [Preacondicionamiento planificado por Jeedom](#preacondicionamiento-planificado-por-jeedom)). Solo se activa si se ha indicado la hora de salida, hay al menos un día marcado y **Leer también la climatización** sigue en **Sí**. |
| **Hora de salida** | Preacondicionamiento planificado: hora a la que el vehículo debe estar listo, en formato `HH:MM` (hora de Jeedom, por ejemplo `07:30`; también se acepta `7h30`). |
| **Días** | Preacondicionamiento planificado: días de **salida** afectados (casillas **Lunes** a **Domingo**). El día considerado es el de la hora de salida, aunque la climatización se inicie la víspera antes de medianoche. Ninguna casilla marcada: función rechazada al activarla. |
| **Antelación (min)** | Preacondicionamiento planificado: minutos antes de la hora de salida a los que se inicia la climatización. Entero de **1 a 60**. Vacío: **15 minutos**. |
| **Duración máxima (min)** | Preacondicionamiento planificado: duración, **contada desde el inicio previsto**, al cabo de la cual Jeedom detiene la climatización. Entero de **1 a 120**, **al menos igual a la antelación**. Vacío: **30 minutos** (o la antelación más 15 minutos si supera 15), es decir, una parada **15 minutos después de la salida** con la antelación por defecto. |
| **Solo si está conectado** | Preacondicionamiento planificado: **desmarcada por defecto**. Marcada, la climatización no se inicia si el vehículo está desconectado o si su estado de carga es desconocido. Un punto de carga que no suministra corriente cuenta como conectado: la climatización consume entonces de la batería. |
| **Latitud** (sección **Posición del domicilio**) | Posición del domicilio, para calcular **En casa**: grados decimales de -90 a 90, por ejemplo `48.8566` (se admite la coma, 8 decimales como máximo). **Vacío: la posición de Jeedom** (**Ajustes > Sistema > Configuración**, pestaña **General**). Debe indicarse junto con la **longitud**: si solo se indica una de las dos, se rechaza. Véase [Posición y privacidad](#posicion-y-privacidad). |
| **Longitud** (sección **Posición del domicilio**) | Grados decimales de -180 a 180, por ejemplo `2.3522`. Vacío con la latitud vacía: posición de Jeedom. |
| **Radio (m)** (sección **Posición del domicilio**) | Distancia máxima, en metros, entre el vehículo y el domicilio para que **En casa** valga 1. Entero de **10 a 10000**. Vacío: **100 m**. Sin efecto si el proxy no proporciona la posición del vehículo. |
| **Descripción** | Texto libre, opcional. |

Los botones de la parte superior de la página son los de cualquier dispositivo de Jeedom: **Configuración avanzada**, **Duplicar**, **Guardar** y **Eliminar**. La pestaña **Comandos** enumera los comandos del vehículo (véase [Comandos](#comandos)).

Al guardar:

- El plugin crea los comandos que faltan del dispositivo. **No lanza ninguna actualización**: la página responde enseguida, aunque el proxy esté apagado. La información llega en la lectura siguiente (en el minuto siguiente para un vehículo nuevo), o de inmediato con el comando **Actualizar**.
- El VIN se **normaliza**: se eliminan los espacios y las letras se pasan a mayúsculas. Se puede dejar vacío, pero entonces el vehículo no se lee (véase [Resolución de problemas](#solucion-de-problemas)).
- El VIN es **único**: un vehículo solo puede tener un dispositivo. Un VIN no válido, o ya utilizado por otro dispositivo, se rechaza con un mensaje.
- **Duplicar** un vehículo queda, por tanto, **rechazado**: la copia lleva el mismo VIN. Para un segundo vehículo, utilice **Añadir**.
- La **URL del proxy de este vehículo** se normaliza igual que la de la configuración del plugin (véase [La URL se normaliza al guardar](#la-url-se-normaliza-al-guardar)); una URL no válida se rechaza con el mismo mensaje.

### Un proxy por vehículo (varios garajes)

Si sus vehículos están aparcados en lugares distintos, cada uno con su Raspberry Pi, indique en cada dispositivo la **URL del proxy de este vehículo**. Todas sus lecturas y comandos pasan entonces por este proxy, y el enlace **Abrir el panel del proxy** de la sección de emparejamiento apunta a él. Si un proxy se detiene, solo fallan los vehículos que lo utilizan. Vaciar el campo devuelve el vehículo a la URL de la configuración del plugin en el ciclo siguiente; sus comandos y su historial no cambian.

- Escriba un mismo proxy **siempre con la misma URL** (misma dirección IP o mismo nombre, mismo puerto): el plugin reconoce un proxy por su URL.
- El botón **Logs del proxy** de la configuración del plugin muestra únicamente los logs del proxy de la **configuración del plugin**.

### Emparejar mi llave y verificar el emparejamiento

Bajo el campo **VIN**, la sección **Emparejar mi llave** recuerda los pasos del emparejamiento, que se realiza en el panel del proxy (detalle: [Generar la llave y emparejarla con el vehículo](installation-proxy.md#8-generar-la-llave-y-emparejarla-con-el-vehiculo)). Una vez guardado el VIN e indicada la URL del proxy, muestra además el enlace **Abrir el panel del proxy** (pestaña nueva), el VIN que debe copiarse en **Setup Vehicle** y el botón **Verificar el emparejamiento**.

**Verificar el emparejamiento** lee el estado del vehículo a través del proxy **sin despertarlo** (50 segundos como máximo) y no envía ningún comando. El plugin nunca genera ni elimina una llave: solo lo hace el panel del proxy.

| Mensaje | Qué hacer |
|---|---|
| **Emparejamiento verificado: el vehículo responde a la llave del proxy** | Nada. Con la imagen del fork, la línea **Rol de la llave activa del proxy** indica además Owner o Charging Manager. La información **Rol de la llave** del dispositivo, en cambio, solo cambia en el siguiente comando reservado (véase [Rol de la llave](#rol-de-la-llave)). |
| **Proxy sin llave: …** | Ninguna llave en el proxy: genere una (**Generate**) y envíela después al vehículo. |
| **Llave no emparejada con este vehículo: …** | Despierte el vehículo, envíe la llave (**Send key**) y coloque después la tarjeta llave en la consola central. |
| **Vehículo fuera del alcance Bluetooth del proxy: …** | Acerque el vehículo o la Raspberry Pi y compruebe el VIN. |
| **Proxy inaccesible: …** | Compruebe que el proxy está iniciado y luego su dirección con el botón **Probar este proxy** del dispositivo. |
| **Proxy ocupado por un comando o una lectura: …** | Vuelva a lanzar la verificación en un momento. |

La verificación utiliza el VIN **guardado**: guarde el dispositivo después de modificarlo.

## Topologías: uno o varios proxys, uno o varios vehículos

El plugin puede controlar varios vehículos, con un solo proxy o con varios. La URL de un proxy se introduce en dos lugares: en la **configuración del plugin** (la dirección por defecto, utilizada por todos los vehículos que no tienen la suya) y, opcionalmente, en el campo **URL del proxy de este vehículo** de cada dispositivo.

### Esquemas

Una Raspberry Pi, varios vehículos (mismo garaje): la URL se introduce **una sola vez**, en la configuración del plugin; el campo de cada vehículo se deja vacío.

```
Jeedom ---> Proxy del garaje (Raspberry Pi A) --BLE--> Vehículo 1 (VIN 1)
                                              --BLE--> Vehículo 2 (VIN 2)

URL : configuración del plugin = http://192.168.1.50:8080/
URL : campo de cada vehículo   = vacío
```

Varias Raspberry Pi, varios garajes: la URL de cada proxy se introduce **en el dispositivo de cada vehículo**. La configuración del plugin puede quedarse con el proxy principal (sirve de valor por defecto y para el botón **Logs del proxy**).

```
Jeedom ---> Proxy del garaje A (Raspberry Pi A) --BLE--> Vehículo 1
       |
       +--> Proxy del garaje B (Raspberry Pi B) --BLE--> Vehículo 2

URL : configuración del plugin = http://192.168.1.50:8080/   (proxy A, por defecto)
URL : campo del vehículo 1     = vacío (o http://192.168.1.50:8080/)
URL : campo del vehículo 2     = http://192.168.1.51:8080/
```

### Añadir un segundo vehículo en el mismo proxy

El proxy, la Raspberry Pi y la URL de la configuración del plugin ya están en su sitio para el primer vehículo. Para el segundo:

1. En **Complementos > Objetos conectados > Tesla BLE**, haga clic en **Añadir** (y no en **Duplicar**, que se rechaza: el VIN es único), dé un nombre al vehículo, introduzca su **VIN** y deje **URL del proxy de este vehículo** vacío. **Guarde**.
2. En la sección **Emparejar mi llave** de este nuevo dispositivo, haga clic en **Abrir el panel del proxy**.
3. En el panel, introduzca el VIN del segundo vehículo en **Setup Vehicle**, despierte ese vehículo, haga clic en **Send key** y luego coloque la tarjeta llave en su consola central para validar. Es **la misma llave** del proxy la que debe emparejarse con cada vehículo: no genere una segunda llave. Consulte [Rol de la llave](#rol-de-la-llave) para elegir el rol.
4. Vuelva al dispositivo y haga clic en **Verificar el emparejamiento**: espere a que aparezca **Emparejamiento verificado: el vehículo responde a la llave del proxy**. Si no, consulte la tabla de [Emparejar mi llave y verificar el emparejamiento](#emparejar-mi-llave-y-verificar-el-emparejamiento).
5. Haga clic en **Actualizar** (o espere un minuto): aparece la información del segundo vehículo.

Un vehículo solo acepta **3 dispositivos Bluetooth conectados a la vez** (teléfonos, reloj, proxy): por encima de ese número, las conexiones se vuelven intermitentes. Cada vehículo conserva su propio **Último error**: un vehículo fuera de alcance o cuya llave no está emparejada no molesta al otro. En cambio, comparten la misma Raspberry Pi: los intercambios se hacen uno tras otro (consulte [Por qué las llamadas son secuenciales](#por-que-las-llamadas-son-secuenciales)).

### Añadir un segundo proxy para otro garaje

1. Instale el proxy del segundo garaje en su propia Raspberry Pi, con una dirección IP fija (consulte [Instalar el proxy BLE](installation-proxy.md)), luego genere la llave y empárejela con el vehículo de ese garaje.
2. En el dispositivo de ese vehículo, introduzca en **URL del proxy de este vehículo** la dirección del segundo proxy, con su puerto, por ejemplo `http://192.168.1.51:8080/`.
3. Haga clic en **Probar este proxy**: el mensaje **Proxy accesible — versión X** confirma que **ese** proxy responde (la prueba se realiza sobre el valor introducido, aunque no esté guardado). Si no, consulte [Mensajes del botón Probar](#mensajes-del-boton-probar).
4. **Guarde** y luego utilice **Verificar el emparejamiento** para comprobar la llave de este vehículo.
5. El enlace **Abrir el panel del proxy** de este dispositivo abre entonces el panel del segundo proxy.

La ventana **Logs del proxy** de la configuración del plugin solo muestra el proxy de la **configuración del plugin**: para leer los logs del segundo proxy, ábralos en un navegador (`http://<ip_de_la_segunda_pi>:8080/dashboard`). Cada vehículo tiene su propia información **Proxy accesible**, y la alerta de adaptador bloqueado es propia de cada vehículo. El mismo token de API sirve para todos los proxys.

## Actualización desde la versión 0.x

Si actualiza el plugin desde una versión 0.x: no hay nada que rehacer.

> **IMPORTANT**
>
> Sus **dispositivos, VIN, comandos, historiales, escenarios y ajustes de visualización se conservan**. Los comandos mantienen sus identificadores: los escenarios, los widgets y los historiales que los utilizan siguen funcionando sin modificación.

### Nombres de los comandos

Un dispositivo **migrado desde la versión 0.x conserva los nombres de sus comandos** (por ejemplo «Etat Charge», «Charge Start», «Rafraichir»): para los escenarios solo cuentan los identificadores. Los comandos de un **dispositivo nuevo** llevan los nombres de la tabla de la sección [Comandos](#comandos). Puede renombrar libremente un comando.

Durante la actualización, los comandos que faltan en su dispositivo se añaden **junto a los comandos del mismo tema** (en bloque al final de la lista solo si no existe ningún comando de ese tema, consulte [Orden de los comandos](#orden-de-los-comandos)): **Tiempo de carga restante**, **Puerto de carga abierto**, **Último error**, **Última lectura de los datos**, **Proxy accesible**, **Versión del proxy**, **Rol de la llave** (que vale **Indeterminado** hasta el primer comando reservado al rol Owner), **Duración de la lectura del estado** y **Duración de la lectura de los datos** (vacíos hasta la primera lectura correcta), luego **Antigüedad de los datos (min)** (que vale 99999 hasta la primera lectura conocida), luego **Límite de carga mínimo**, **Límite de carga máximo** y **Corriente de carga máxima** (ocultos, vacíos hasta la primera lectura de los datos) y, por último, diez informaciones de carga ampliadas, también ocultas (consulte [Información](#informaciones)). Un **Máx** de control deslizante que usted hubiera fijado a mano se conserva. En un dispositivo existente, la acción de apertura del puerto de carga puede llamarse «Trappe de Charge Ouvert»: renómbrela si lo desea.

### Autonomía y velocidad de carga

Los comandos **Autonomía** y **Velocidad de carga** ahora se convierten a km y km/h (el vehículo los envía en millas). Los valores ya registrados en el historial siguen en millas: por tanto, el gráfico de **Autonomía** muestra una **ruptura** (un salto de un factor de aproximadamente 1,6) en el momento de la actualización. Los valores anteriores no se convierten.

### Hora de salida programada

El comando **Hora de salida programada** ahora muestra la hora en formato `HH:MM` (por ejemplo `07:30`) y queda vacío cuando no hay ninguna salida programada. Antes devolvía una marca de tiempo numérica: adapte los escenarios que la comparaban con ese número.

Si ha activado el historial de este comando, sigue siendo numérico y ya no se actualiza; un mensaje se lo indica en el centro de mensajes de Jeedom. Para recibir la hora, cambie su subtipo a **Otro** en la pestaña **Comandos** del dispositivo.

### Comandos de acción

- La opción **«Ninguno»** del **Modo Centinela** se elimina (el proxy no la entendía). Un escenario que la enviaba recibe ahora un error: utilice **Activado** o **Desactivado**. La actualización elimina esta opción de los dispositivos existentes, sin tocar los demás ajustes del comando.
- Una **corriente de carga fuera de los límites** del comando, o no entera, se rechaza en lugar de enviarse.
- Un comando que fallaba sin decir nada muestra ahora un **error** y alimenta la información **Último error**.

### Versiones mínimas

| Elemento | Versión |
|---|---|
| Jeedom | 4.5 como mínimo |
| Debian | 11 o 12 |
| TeslaBleHttpProxy | 2.3.0 como mínimo (consulte [Verificar y actualizar la versión del proxy](#comprobar-y-actualizar-la-version-del-proxy)) |

Si su Jeedom tiene una versión inferior a la 4.5, Jeedom rechaza la actualización con el mensaje «Version du core Jeedom non supportée» (*versión del core de Jeedom no compatible*). La versión anterior del plugin se mantiene entonces y sigue funcionando. Actualice primero Jeedom. Debian 10 ya no es compatible.

### Lo que se hace automáticamente

Durante la actualización, y luego al activar el plugin, se ejecuta automáticamente una puesta al día de los dispositivos existentes, por niveles sucesivos. Cada nivel se aplica una sola vez. Según las versiones, corrige o completa ciertos dispositivos (VIN, comandos que faltan, hora de salida programada, eliminación de la opción «Ninguno» del modo Centinela, ajustes de la ventana de sueño…) sin tocar sus ajustes (nombre, visibilidad, historial). Los vehículos existentes reciben la ventana de sueño **activada** (3 lecturas sin cambios, 30 minutos); desmárquela en el dispositivo si no la desea.

Las ocho informaciones de aperturas (puertas, maleteros, puerto de carga, cubierta de caja) se crean **visibles e historizadas**; sus ajustes existentes nunca se modifican.

Las informaciones **Ocupante presente** (visible, historizada) y **Estado de bloqueo detallado** (visible, no historizada) se crean de la misma manera; sus ajustes existentes nunca se sobrescriben.

Las informaciones **Centinela** y **Origen del modo Centinela** (visibles, no historizadas) se crean de la misma manera, con los valores **Desconocido** y **Ninguna** mientras no se haya leído ni ordenado nada; sus ajustes existentes nunca se sobrescriben (consulte [Estado del modo Centinela](#estado-del-modo-centinela)).

Las informaciones **Alerta de aperturas** y **Alerta de vehículo desbloqueado sin ocupante** (ocultas, historizadas) se crean de la misma manera, a **0**; las alertas permanecen **desactivadas** mientras usted no las active (consulte [Alertas de apertura prolongada](#alertas-de-apertura-prolongada)).

Si la puesta al día falla en un vehículo, se reintenta automáticamente en la próxima actualización o activación del plugin.

### Comprobar la puesta al día en el log

Ponga el log del plugin al menos en nivel **Info** (**Configuración del plugin > Logs**), luego actualice o reactive el plugin y abra su log. Las líneas correspondientes empiezan por «Migrations : ».

| Situación | Mensaje en el log |
|---|---|
| Puesta al día correcta | `Migrations : migration N (<description>) appliquée sur X équipement(s) sur Y.` (*migración N (<descripción>) aplicada en X dispositivo(s) de Y*) para cada nivel aplicado, luego `Migrations : niveau de migration N atteint.` (*nivel de migración N alcanzado*) |
| Ya actualizado | `Migrations : aucune migration à appliquer, niveau de migration N.` (*ninguna migración que aplicar, nivel de migración N*) (N = último nivel) |
| Ningún dispositivo (instalación nueva) | `Migrations : aucun équipement à migrer, niveau de migration N (aucune migration exécutée).` (*ningún dispositivo que migrar, nivel de migración N (ninguna migración ejecutada)*) (N = último nivel) |
| Fallo en un dispositivo | `Migrations : échec de la migration N (...) sur l'équipement « <nom> » (id <n>) : ...` (*fallo de la migración N (...) en el dispositivo «<nombre>» (id <n>): ...*) seguido de `Elle sera retentée à la prochaine mise à jour ou activation du plugin.` (*se reintentará en la próxima actualización o activación del plugin*), luego `Migrations : niveau de migration M conservé, X équipement(s) en échec ; les migrations restantes seront retentées à la prochaine mise à jour ou activation du plugin.` (*nivel de migración M conservado, X dispositivo(s) con fallo; las migraciones restantes se reintentarán en la próxima actualización o activación del plugin*) |

Si un mensaje de fallo persiste tras varias actualizaciones, anótelo y comuníquelo junto con el log del plugin.

## Funcionamiento

### Reposo del vehículo y frescura de los datos

Un Tesla despierto se duerme por sí solo tras **unos quince minutos** sin solicitud. Varias cosas lo mantienen despierto: el **modo Centinela**, un **ocupante** a bordo (o una llave de teléfono cercana), una **carga** en curso, la **aplicación Tesla** abierta y toda lectura de sus datos de carga y de climatización. Un vehículo que duerme consume muy poco; un vehículo mantenido despierto consume batería de forma permanente.

Este es el compromiso que conviene conocer: **cuanto más a menudo lea, más frescas serán las informaciones, pero más probabilidades tendrá el vehículo de no dormirse nunca**. Los ajustes de frecuencia de este plugin sirven para elegir su punto de equilibrio (consulte [Resumen de los ajustes de frecuencia y de despertar](#resumen-de-los-ajustes-de-frecuencia-y-de-despertar) y [Recomendaciones según el uso](#recomendaciones-segun-el-uso)).

> **IMPORTANT**
>
> **El plugin nunca despierta el vehículo por sí mismo, salvo acción explícita suya o de un escenario.** Ni la actualización periódica, ni la lectura acelerada durante la carga, ni la relectura tras un comando despiertan el vehículo: leen el estado sin despertarlo y después los datos solo si el vehículo ya está despierto. Para leer los datos de un vehículo que duerme, hay que **pedirlo** con el comando **Actualizar (con despertar)** (consulte [Actualizar con despertar](#actualizar-con-despertar)). **Despertar** y los comandos de acción (carga, climatización, bloqueo…) también despiertan el vehículo, a través del proxy, puesto que usted los ha solicitado.

Para saber si los valores mostrados son recientes, mire **Última lectura de los datos** y **Antigüedad de los datos (min)**: un vehículo que duerme o una ventana de sueño abierta no es un error, pero los valores de carga y de climatización envejecen entonces (consulte [Ejemplo paso a paso: actuar solo con datos recientes](#ejemplo-paso-a-paso-actuar-solo-con-datos-recientes)).

### Actualización de las informaciones

En el **intervalo de cada vehículo** (5 minutos por defecto, ajustable de 1 a 30 minutos en el dispositivo), el plugin actualiza ese vehículo en dos pasos:

1. Consulta el estado del **controlador de carrocería** (`body_controller_state`). Esta consulta no despierta el vehículo. Actualiza la presencia, el bloqueo y el estado de reposo.
2. **Únicamente si el vehículo está despierto**, recupera los datos del vehículo (`vehicle_data`): carga, batería, autonomía y, según el ajuste **Leer también la climatización** del dispositivo (activado por defecto), climatización.

Una tarea de Jeedom, **TeslaBLE::cycleRafraichissement**, se activa **cada minuto** y solo lee los vehículos activos cuyo intervalo ha transcurrido (medido desde el inicio de su última lectura): con un vehículo a 1 minuto y otro a 15 minutos, el primero se lee en cada pasada y el segundo aproximadamente cada 15 minutos. Un vehículo que nunca se ha leído se lee en la pasada siguiente. Un proxy sin ningún vehículo por leer no se solicita. Esta tarea se crea al activar y al actualizar el plugin (consulte [Solución de problemas](#solucion-de-problemas)).

Por tanto, el plugin nunca despierta el vehículo por sí mismo, para no descargar la batería. Mientras el vehículo duerme, las informaciones de carga y de climatización conservan su último valor conocido. Para actualizarlas bajo demanda, utilice el comando **Actualizar (con despertar)** (consulte [Actualizar con despertar](#actualizar-con-despertar)).

Si el vehículo se duerme entre las dos consultas, no es un error: las informaciones de carga y de climatización conservan su último valor y no se muestra nada.

Con **Leer también la climatización** en **No, solo carga**, la consulta de datos solo pide la carga (`vehicle_data?endpoints=charge_state`, visible en el log del plugin en **Debug** y en los logs del proxy). **Última lectura de los datos** y **Duración de la lectura de los datos** fechan entonces la lectura de carga, y **Antigüedad de los datos (min)** cuenta el tiempo transcurrido desde esa lectura de carga: las informaciones de climatización, en cambio, permanecen congeladas.

Si el vehículo está fuera del alcance Bluetooth del proxy, el comando **Presencia del vehículo** pasa a 0. Si es el proxy el que no responde, no tiene llave emparejada o responde demasiado despacio, la presencia conserva su último valor.

**Varios vehículos en un mismo proxy.** Los vehículos de un mismo proxy se leen uno tras otro, cada uno con su propio **Último error** y su propia **Última lectura de los datos**: un vehículo fuera de alcance o cuya llave no está emparejada no impide la lectura de los demás. El ciclo dura como máximo 4 minutos; con 3 vehículos o menos en un mismo proxy, nunca se acorta, ni siquiera en el peor de los casos. Por encima, puede que los últimos vehículos no se lean: compruebe su **Última lectura de los datos**. Cuando un ciclo se acorta, el log recibe **un solo** aviso por episodio («Avertissement non répété jusqu'au prochain cycle complet.» (*aviso no repetido hasta el próximo ciclo completo*)), y después una línea **Info** en el primer ciclo que vuelve a ser completo.

**¿Por qué los datos ya no se mueven?** La información **Último error** da la causa del último fallo de lectura, seguida del motivo devuelto por el proxy cuando lo indica (por ejemplo «Vehículo fuera de alcance — …» o «Proxy sin llave: emparejamiento pendiente — …»). Vuelve a **Ninguna** en cuanto un ciclo de lectura tiene éxito. Un vehículo que duerme no es un error: **Último error** se queda en **Ninguna** y **Vehículo despierto** vale 0. La información **Última lectura de los datos** indica desde cuándo datan los datos de carga y de climatización.

En el log del plugin, un problema solo deja **dos líneas**: una cuando empieza y otra cuando todo vuelve a la normalidad (`Véhicule « <nom> » (id <n>) : retour à la normale après [<catégorie>].` (*vehículo «<nombre>» (id <n>): vuelta a la normalidad tras [<categoría>]*)), aunque dure horas. El nivel de la línea de inicio depende de la causa: **Info** para un vehículo fuera de alcance (situación normal), **Error** para un error de configuración (VIN o URL ausente) o un proxy demasiado antiguo, **Aviso** para los demás. La línea de fin es siempre de nivel **Info**. **Para ver estas líneas, el log del plugin debe estar al menos en nivel Info** (**Configuración del plugin > Logs**). Mientras el problema dura, el detalle de cada ciclo sigue visible en **Debug**.

Los vehículos de un mismo proxy se actualizan **uno tras otro**; los proxys distintos se leen **en paralelo**. Un vehículo fuera de alcance o con error no impide la lectura de los siguientes, y el error se registra en el log con el nombre del vehículo.

- Si un ciclo dura más que el intervalo, Jeedom **salta** las pasadas siguientes mientras no haya terminado: los ciclos nunca se acumulan. El plugin lo escribe entonces en el log al final del ciclo (un aviso por hora como máximo si no se respeta el intervalo ajustado); la frecuencia se retoma en cuanto el ciclo termina.
- Un ciclo no supera los **4 minutos**: si hay muchos vehículos o si el proxy es lento, los vehículos restantes se leen en el ciclo siguiente (aviso que nombra esos vehículos).
- Mientras un comando, un **Actualizar**, un **Actualizar (con despertar)** o una verificación de emparejamiento está en curso o espera al mismo proxy, la lectura del ciclo se salta sin error; la lectura siguiente se pone al día.
- Con varios proxys, el ciclo lee los proxys en paralelo: un proxy detenido, apagado, bloqueado o lento solo retrasa a sus propios vehículos (un proxy detenido cuesta unos segundos, hasta unos 5 s, por vehículo de ese proxy), nunca a los de los demás proxys. El ciclo dura tanto como su proxy más lento. Dos proxys distintos nunca se esperan, tampoco en el ciclo periódico; los comandos y **Actualizar** de los demás proxys tampoco se retrasan.

### Actualizar con despertar

El comando **Actualizar (con despertar)** es la única forma de leer los datos de carga y de climatización de un vehículo que duerme. Primero lee el estado sin despertar, luego despierta el vehículo si hace falta y lee sus datos, en una sola acción: al final, **Vehículo despierto** vale 1 y la carga y la climatización están al día. Cuente en general de 15 a 40 segundos; el plugin espera hasta 75 segundos para la lectura tras el despertar, tiempo durante el cual Jeedom sigue siendo utilizable.

- **Despierta el vehículo** en cada ejecución: el uso repetido consume batería. Tras la lectura, la ventana de sueño (consulte [Dejar que el vehículo se duerma](#dejar-que-el-vehiculo-se-duerma)) y la frecuencia normal recuperan sus reglas; el vehículo puede volver a dormirse.
- **Fuera de alcance**: el estado sin despertar falla en 5 a 25 segundos, no se intenta el despertar y se muestra un mensaje explícito (consulte [Solución de problemas](#solucion-de-problemas)).
- **Escenarios**: el comando se puede utilizar en un escenario y no lo bloquea una ventana de sueño abierta, que él da por terminada. Cuidado de no activarlo en bucle (por ejemplo, ante el cambio de una información del vehículo): cada ejecución despierta el vehículo. En un vehículo dormido, **Vehículo despierto** pasa brevemente a 0 (estado leído antes del despertar) y luego a 1.
- **Actualizar** mantiene su comportamiento: nunca despierta el vehículo.

### Lectura acelerada durante la carga

Para seguir una carga de cerca (control por excedente solar, por ejemplo), ajuste **Intervalo durante la carga** en el dispositivo (desactivado por defecto):

- **Activación.** En cuanto una lectura constata que el vehículo está **cargando** (estado de carga Charging o Starting), el intervalo de carga sustituye al intervalo de actualización, siempre que sea más corto. Con 5 minutos en normal y 1 minuto en carga, los datos se releen cada minuto (observe **Última lectura de los datos**).
- **Vuelta a la normalidad.** En cuanto una lectura ya no constata la carga (fin de carga, cable desconectado, carga suspendida), vehículo dormido, fuera de alcance o proxy inaccesible, el intervalo normal se cuenta desde esa lectura: ningún ciclo de retraso.
- **Suelo de un minuto.** No se ofrece ningún valor por debajo del minuto: Jeedom lanza la actualización cada minuto y el proxy conserva los datos 30 segundos en caché. Un valor inferior registrado por un script se lleva a 1 minuto (aviso en el log), un valor desconocido desactiva el ajuste.
- **Ningún despertar.** El contenido de una lectura no cambia: se lee el estado sin despertar y después los datos solo si el vehículo está despierto. Los datos de un vehículo dormido nunca se leen por causa de este ajuste.

Para seguir el mecanismo, ponga el log del plugin en **Debug**: una línea indica el paso al intervalo de carga y otra la vuelta al intervalo normal.

Límites: la frecuencia de carga solo arranca en la primera lectura que ve la carga (como máximo un intervalo normal después, o de inmediato con **Actualizar**); durante una ventana de sueño abierta, una carga iniciada sin cambio visible del estado sin despertar solo se ve en la lectura de control; si el proxy se ha ajustado con una duración de caché de los datos de al menos 60 segundos, las lecturas a 1 minuto se le sirven desde la caché; una carga suspendida (estado Stopped, cable conectado) no activa la aceleración, y su reanudación solo se ve en el intervalo normal; un vehículo dormido que está cargando no se lee más rápido; un fallo de lectura durante la carga devuelve el intervalo normal hasta la siguiente lectura correcta.

### Dejar que el vehículo se duerma

Un vehículo despierto se duerme por sí solo tras unos quince minutos sin solicitud. Una lectura de los datos de carga y de climatización cada pocos minutos puede impedírselo y consumir batería. Por eso el plugin sabe «hacerse olvidar» cuando no hay nada nuevo que leer:

- **Apertura.** Cuando el vehículo está despierto, **sin carga** (estado de carga Desconectado, Finalizada, Detenida o Sin corriente), **sin ocupante**, y sus datos y su estado están **sin cambios** durante el número de lecturas ajustado (3 por defecto), el plugin abre una **ventana de sueño** (30 minutos por defecto).
- **Durante la ventana**, solo se realiza la lectura del estado sin despertar, en el intervalo del vehículo (presencia, bloqueo, reposo, puertas, maleteros, puerto de carga, ocupante). Los datos de carga y de climatización, la **Última lectura de los datos** y las duraciones de lectura de los datos ya no se actualizan: conservan su último valor, como en un vehículo dormido. El plugin nunca despierta el vehículo para estas comprobaciones.
- **Fin de la ventana**, con reanudación de la lectura completa en la pasada siguiente (en la misma pasada si hay actividad): actividad constatada en el estado sin despertar (desbloqueo, puerta, maletero o puerto de carga, ocupante), comando enviado al vehículo (despertar explícito incluido), botón **Actualizar** o **Actualizar (con despertar)**, vehículo dormido, vehículo fuera de alcance, casilla desmarcada o fin de la duración. Al final de la duración se realiza una **lectura de control**: si nada ha cambiado, la ventana se prolonga.
- **Nunca durante la carga.** Un vehículo cargando, iniciando la carga o en un estado de carga desconocido nunca abre una ventana.
- **Mantenimiento de clima activo.** Mientras **Mantenimiento de clima (perro, camping)** valga `On`, `Dog` o `Party` (u otro valor no previsto), no se abre ninguna ventana: la lectura continúa en el intervalo del vehículo, para que la **Temperatura interior** se mantenga al día en modo perro o camping. `Off`, `Unknown` o una información ausente (por ejemplo, climatización no leída) permiten que se abra la ventana.
- **Climatización no leída.** Con **Leer también la climatización** en **No, solo carga**, la ventana ya no ve la actividad de la climatización (sus informaciones no se leen). Cambiar este ajuste pone a cero el recuento de lecturas sin cambios.

Para seguir el mecanismo, ponga el log del plugin en nivel **Info**: una línea indica la apertura («fenêtre d'endormissement ouverte pour … min … jusqu'à HH:MM environ» (*ventana de sueño abierta durante … min … hasta las HH:MM aproximadamente*)) y otra el final («fin de la fenêtre d'endormissement après … min : …» (*fin de la ventana de sueño tras … min: …*)). En **Debug**, se anota cada pasada suspendida. Para comprobar el efecto, observe **Vehículo despierto**: debería pasar a 0 al cabo del plazo habitual (unos quince minutos), mientras que podía quedarse en 1 sin ventana. Es un efecto esperado, no garantizado: depende del vehículo. Si el vehículo no se duerme, compare con la casilla desmarcada.

Límites: una carga iniciada sin ningún cambio visible del estado sin despertar (cable ya conectado, carga programada o iniciada desde la aplicación) solo se ve en la lectura de control, es decir, como máximo la duración de la ventana más un intervalo después; una climatización iniciada desde la aplicación durante la ventana, igual. La conexión de un cable desde un estado desconectado se ve de inmediato (el puerto se abre). Una llave de teléfono cercana que mantiene al ocupante «presente» impide la apertura de la ventana.

### Ejecución de los comandos

Cada comando de acción se transmite al proxy, que espera la confirmación del vehículo antes de responder. El plugin no necesita despertar el vehículo antes de un comando: el proxy se encarga.

**Valores controlados antes del envío.** Un valor no válido se rechaza de inmediato, con un mensaje, sin enviar nada al proxy:

- **Corriente de carga**: un número entero comprendido entre el **Mín** y el **Máx** del comando (0 a 32 A mientras el vehículo no haya publicado su límite, y después la corriente máxima que anuncia). Un valor decimal (`16,5`) o un texto se rechaza.
- **Límite de carga**: un número entero comprendido entre el **Mín** y el **Máx** del comando (50 a 100 % mientras el vehículo no haya publicado sus límites, y después sus límites mínimo y máximo).
- **Modo Centinela**: **Activado** o **Desactivado** (la antigua opción «Ninguno» ya no existe).

**Límites seguidos del vehículo.** En cada lectura correcta de los datos, el plugin ajusta el **Mín** y el **Máx** de los controles deslizantes **Límite de carga** y **Corriente de carga** a lo que acepta el vehículo (informaciones **Límite de carga mínimo**, **Límite de carga máximo** y **Corriente de carga máxima**), y el control deslizante del widget lo sigue sin recargar la página. Un valor a 0, ausente o incoherente se ignora: se conservan los límites anteriores, como mientras el vehículo duerme. **Un ajuste manual prevalece**: si usted introduce un **Mín** o un **Máx** distinto del que el plugin ha fijado, ya no se modifica nunca (ni siquiera tras varias lecturas o un guardado del dispositivo); un valor introducido igual al que el plugin ha fijado sigue siendo objeto de seguimiento (para fijar un límite, introduzca por tanto un valor distinto del fijado por el plugin); cualquier otro valor, aunque sea igual al del vehículo en ese momento, es un ajuste manual; un límite que usted amplía más allá del del vehículo autoriza una consigna que el vehículo podrá rechazar. Para volver al seguimiento automático, **vacíe** el campo: se restablece en la lectura siguiente. Para fijar un límite (por ejemplo 48 A), ajuste el **Máx** a mano; para actualizar los límites de inmediato, lance **Actualizar (con despertar)**. La corriente máxima puede depender del punto de carga conectado y no se publica cuando el vehículo está desconectado: los límites anteriores se mantienen entonces.

> **Cambio de comportamiento**: una consigna **por encima del máximo anunciado por el vehículo** (por ejemplo 20 A cuando anuncia 16 A) se **rechaza** ahora con un mensaje, en lugar de aceptarse y que luego el vehículo la reduzca silenciosamente.

**En caso de fallo.** Si el proxy o el vehículo rechaza el comando, aparece un mensaje de error en rojo en la interfaz de Jeedom (y en el log del plugin como error), y también se registra en la información **Último error**, donde permanece mostrado hasta el próximo ciclo de lectura correcto (en la lectura siguiente, 5 minutos como máximo por defecto). Por ejemplo «Este comando requiere una llave con rol Owner: la llave del proxy probablemente tiene el rol Charging Manager…» cuando se rechaza un comando reservado al rol Owner: consulte [Rol de la llave](#rol-de-la-llave).

**Tras un comando correcto.** El límite de carga, la corriente de carga y el bloqueo se actualizan de inmediato y después se relee el estado del vehículo (presencia, despierto) sin despertarlo. A continuación, el vehículo se **relee una vez** tras un retardo (30 segundos por defecto, ajustable por vehículo), sin esperar a la lectura periódica, para mostrar los valores reales (consulte [Relectura tras un comando](#relectura-tras-un-comando)). El comando, por su parte, devuelve el control de inmediato.

**Un comando o una lectura a la vez.** Los intercambios con un mismo proxy se hacen uno tras otro: un comando, un **Actualizar** o una verificación de emparejamiento solo espera a los intercambios ya en curso o ya en espera en ese proxy (hasta unos 2 minutos, 15 segundos para la verificación) y pasa antes que las lecturas periódicas, que se apartan y se retoman en el ciclo siguiente. El orden de paso no está garantizado entre varias solicitudes simultáneas. Dos proxys distintos nunca se esperan, ciclo periódico incluido (el ciclo lee los proxys en paralelo: consulte Actualización). Si el proxy y el vehículo están al límite de sus plazos, la respuesta puede tardar de 3 a 4 minutos. Jeedom sigue siendo utilizable durante ese tiempo.

### Relectura tras un comando

Justo después de un comando, el proxy aún devuelve sus datos anteriores (los conserva **30 segundos** en caché). En lugar de mostrar un valor caducado hasta la próxima actualización, el plugin **programa una relectura** del vehículo una vez expirada esa caché:

- **Activación.** Tras todo comando **correcto** (límite de carga, corriente, inicio o parada de la carga, climatización, bloqueo, puerto, etc.). Un comando fallido no programa nada.
- **Retardo.** Por defecto **30 segundos** tras el final del comando, ajustable por vehículo (**Retardo de relectura tras un comando**: 30 segundos, 45 segundos, 1 minuto, 1 minuto 30 o 2 minutos). Nunca menos de 30 segundos, la duración de la caché del proxy: un retardo más corto releería el valor anterior al comando. Si ha alargado esa caché en el proxy, elija un retardo al menos igual.
- **El comando no espera.** Devuelve el control en cuanto se ejecuta; la relectura se lanza en segundo plano.
- **Una sola relectura para varios comandos cercanos.** Corriente y luego límite en pocos segundos: solo la relectura programada tras el **último** comando lee el vehículo, las anteriores se abandonan por sí mismas.
- **Contenido de la relectura.** El de un **Actualizar**: el estado sin despertar y después los datos de carga y de climatización **solo si el vehículo está despierto**. **Nunca despierta el vehículo**: si se ha vuelto a dormir, no es un error: se conservan los últimos valores. Si está fuera de alcance, la presencia pasa a «No»; si el proxy está inaccesible, se rellena «Último error». Pone fin a la ventana de sueño, como un comando, y no desplaza la frecuencia de la actualización periódica.
- **Despertar** relee por tanto también el vehículo a continuación, sin despertarlo de nuevo (el comando acaba de hacerlo).
- **Coste.** Cada comando correcto añade **una lectura Bluetooth** (estado y después datos si está despierto) a través del proxy. Un escenario que ajusta la corriente de carga cada minuto provoca una relectura por minuto, además de la lectura periódica: espacie los comandos de un escenario en lugar de repetirlos. Un claxon o una llamada de luces también desencadena una relectura.
- **Proceso.** Cada relectura es una **tarea puntual** del motor de tareas de Jeedom (**Ajustes > Sistema > Motor de tareas**, **TeslaBLE::relectureApresCommande**): es visible allí de unos segundos a unos minutos y luego desaparece sola. Una relectura sustituida por un comando más reciente desaparece al cabo de unos segundos. No es un demonio y nada se ejecuta de forma permanente. Si el motor de tareas de Jeedom está desactivado, no se realiza ninguna relectura (como con la actualización periódica) y los valores se actualizan en la lectura siguiente.

Para seguir el mecanismo, ponga el log del plugin en **Debug**: una línea indica la programación («relecture programmée dans 30 s» (*relectura programada en 30 s*)), y luego la relectura («lecture sans réveil» (*lectura sin despertar*)) o su abandono («remplacée par une commande plus récente» (*sustituida por un comando más reciente*), «abandonnée : proxy occupé» (*abandonada: proxy ocupado*)).

### Control según el excedente

La acción **Ajustar según el excedente** (`adjust_surplus`) sigue un excedente fotovoltaico **sin saturar el vehículo de comandos Bluetooth**: cada comando puede durar hasta 75 segundos y despierta el vehículo. Su escenario envía la **potencia disponible para la carga** y el plugin decide si realmente hay que actuar. Los valores por defecto deben validarse en uso real (véase [Limitaciones conocidas](#limitaciones-conocidas)).

**El valor enviado es una potencia absoluta, en vatios.** Es lo que el vehículo puede consumir, no una variación. Si su contador mide la **exportación a la red**, la potencia disponible es **la exportación más la potencia de carga actual**: sin esta suma, la consigna caería en cada ajuste. Un valor negativo se reduce a 0 W; un valor que no sea un número de vatios se rechaza con el mensaje **«Valor no válido: la potencia disponible debe ser un número de vatios»**.

**De vatios a amperios.** La corriente por fase es la potencia dividida entre la **tensión** y entre el número de **fases** (dos ajustes del dispositivo, nunca leídos del vehículo), redondeada **a la baja** al **paso de ajuste**. ⚠️ Un punto de carga trifásico configurado como monofásico daría **tres veces** la corriente deseada: compruebe el ajuste **Fases**.

**Cuándo envía un comando el plugin.** Como máximo **un** comando por llamada, entre **Corriente de carga**, **Iniciar la carga** y **Detener la carga**:

- la corriente objetivo está limitada por el **Máx** del control deslizante **Corriente de carga** (un valor calculado más alto se reduce al Máx; en cambio, introducir a mano un valor superior al Máx sigue siendo rechazado) y nunca se fija **por debajo del umbral de parada** durante la carga;
- **no se envía nada** si la corriente objetivo es idéntica a la última consigna enviada, o si difiere de ella en menos que la **histéresis**;
- **como máximo un comando por intervalo**: el **intervalo mínimo** se cuenta desde el **final** del comando anterior, haya tenido éxito o haya fallado;
- **parada**: si la corriente calculada se mantiene por debajo del **umbral de parada** durante la **duración de mantenimiento**, se detiene la carga;
- **arranque**: con la carga detenida, se reanuda cuando la corriente calculada alcanza la **corriente mínima de arranque**. El arranque se hace **en dos tiempos** cuando no se conoce la última consigna, o cuando esta supera la corriente objetivo en al menos la **histéresis**: primero **Corriente de carga**, **Iniciar la carga** en el intervalo siguiente (un intervalo de retraso). Una vez enviada **Corriente de carga** con la carga detenida, la consigna se considera conocida **mientras la carga no haya arrancado**, sea cual sea la cadencia de su escenario: **Iniciar la carga** sale entonces directamente. Sin este protocolo de confirmación, la consigna solo se considera conocida si el último comando del control tiene menos de 10 minutos; también se olvida en cuanto la carga ha terminado, el punto de carga ya no tiene corriente o el vehículo está desconectado (el primer arranque del día siguiente empieza, por tanto, por **Corriente de carga**).

**Abstenciones.** No se envía ningún comando, sin excepción en el escenario, y el motivo aparece en **Último error**: **«Vehículo no conectado: ajuste según el excedente ignorado»**, **«Vehículo fuera del alcance del proxy: …»**, **«Carga finalizada: …»**, **«El punto de carga no suministra corriente: …»** y **«Estado de carga desconocido: lance Actualizar (con despertar)»**. Estos mensajes nunca sustituyen a un error real del último ciclo de lectura, y el siguiente ciclo correcto vuelve a poner **Ninguna**. El control se basa en el último **Estado de la carga** publicado: tras un arranque o una parada que él mismo acaba de ordenar, considera el estado ordenado hasta la siguiente lectura (5 minutos como máximo). Se recomienda activar el **Intervalo durante la carga**.

**Ningún despertar.** El control nunca despierta el vehículo y no lee nada para decidir; una llamada ignorada no contacta con el proxy. Un comando realmente enviado despierta el vehículo como cualquier comando.

**Horas valle.** Durante el intervalo de la **Carga en horas valle** de un vehículo, la llamada a **Ajustar según el excedente** se **ignora** (sin error, sin comando, con una línea Debug en el log): sin esto, un escenario solar que envíe 0 W por la noche detendría la carga de las horas valle. Fuera del intervalo, el control según el excedente funciona como de costumbre (véase [Carga en horas valle](#carga-en-horas-valle)).

**Ejemplo de escenario.** Véase el [ejemplo paso a paso: carga solar con Ajustar según el excedente](#ejemplo-paso-a-paso-carga-solar-con-ajustar-segun-el-excedente). No multiplique las llamadas: el plugin ignora las que no aportan nada.

**Ajustes no válidos.** Un ajuste fuera de límites (paso a 0, intervalo inferior a 60 s, umbral de parada superior a la corriente de arranque…) se **rechaza al guardar** el dispositivo, con un mensaje **«Control según el excedente: …»**.

### Programar la carga

Las acciones **Añadir una programación de carga** (`add_charge_schedule`) y **Eliminar la programación de carga** (`remove_charge_schedule`) crean o eliminan en el vehículo **una programación de carga gestionada por Jeedom**. Se crean **ocultas**: se llaman desde un escenario (o se hacen visibles desde la pestaña **Comandos**).

**Proxy del fork requerido.** El proxy oficial 2.3.0 no sabe programar la carga: la ruta correspondiente no existe en él, la añadió el fork (versiones del tipo `2.3.0-tb.N`). Mientras el proxy no anuncie estos dos comandos, se **rechazan de inmediato**, sin ningún intercambio con el vehículo, con el mensaje **«No compatible con su versión del proxy»**; el resto del dispositivo funciona con normalidad. La disponibilidad sigue el anuncio del proxy (ruta `capabilities`), que se vuelve a leer cuando cambia su versión: tras pasar al proxy del fork (versión del tipo `2.3.0-tb.N`), los comandos pasan a estar disponibles sin reinstalar el plugin. Una actualización del fork **sin cambio del número de versión** solo se tiene en cuenta cuando cambia el número de versión.

**Parámetros.** En el escenario, la acción **Añadir una programación de carga** admite dos campos:

- **Días de la programación** (título): uno o varios días separados por comas, puntos y comas o espacios, sin distinguir mayúsculas de minúsculas: `lun`, `mar`, `mer`, `jeu`, `ven`, `sam`, `dim` (o el nombre completo, o la abreviatura inglesa `mon`… `sun`), `tous` (todos los días) o `semaine` (de lunes a viernes). Ejemplo: `lun,mar,mer,jeu,ven`.
- **Hora de inicio (HH:MM)** (mensaje): de `00:00` a `23:59`, por ejemplo `23:00` (también se acepta `23h00`). Es la **hora local del vehículo**.

Todo parámetro no válido se rechaza **antes** del envío, con un mensaje que explica el formato esperado; no se envía nada al vehículo.

**Coordenadas de Jeedom.** El vehículo solo activa una programación si se encuentra en el lugar indicado. El plugin utiliza las **coordenadas de Jeedom** (Ajustes, Sistema, Configuración, pestaña **General**, apartado **Coordenadas**: latitud y longitud): indíquelas, o el comando se rechaza con el mensaje **«Coordenadas de Jeedom ausentes o no válidas»**. Si el vehículo no está estacionado en ese lugar, la programación existe pero no se activa. Las coordenadas nunca se escriben en los logs.

**Una sola programación, sustituida en cada alta.** El plugin gestiona **una** programación por vehículo y memoriza su identificador: una nueva alta **sustituye** a la programación anterior (se sustituyen los mismos días y hora, sin duplicados en principio: la sustitución por identificador debe confirmarse en uso real). La programación cubre la carga a partir de la hora de inicio; no hay hora de fin, ni corriente, ni límite propios de la programación. Las programaciones creadas en la aplicación Tesla no se modifican ni se eliminan. Si cambia el VIN del dispositivo, el identificador memorizado deja de usarse: la siguiente alta crea una nueva programación.

**Eliminación.** **Eliminar la programación de carga** elimina la programación creada por Jeedom. Si Jeedom no ha creado ninguna (o si ya se eliminó), la acción no hace nada y **no produce ningún error**. Si el vehículo rechaza la eliminación por un motivo distinto de un rol de llave insuficiente (por ejemplo, porque la programación se eliminó en la aplicación), se muestra el mensaje de rechazo y se olvida el identificador: una segunda eliminación es silenciosa y una nueva alta crea una nueva programación.

**Tras el comando.** Se programa una relectura como tras cualquier comando (véase [Relectura tras un comando](#relectura-tras-un-comando)): la información de programación (**Hora de carga programada**…) se actualiza **si el vehículo la devuelve** al leer los datos; la planificación también se comprueba en la aplicación Tesla.

**Rol de la llave.** El rol mínimo necesario no está confirmado (**Charging Manager** probable). Un rechazo de autorización se muestra con la indicación «¿rol de la llave del proxy insuficiente?» (véase [Rol de la llave](#rol-de-la-llave)).

### Carga en horas valle

El plugin puede **iniciar y detener la carga por sí mismo** durante las horas valle de su contrato de electricidad, hasta un **SoC objetivo** elegido. Funciona con el proxy oficial 2.3.0 y **no depende de las programaciones almacenadas en el vehículo** (véase [Programar la carga](#programar-la-carga) para estas). Los ajustes están en la sección **Carga en horas valle** del dispositivo; marque **Activar** (**Control de la carga**), indique **Inicio del intervalo**, **Fin del intervalo** y **SoC objetivo (%)**, y guarde.

**Paso a paso: configurar la carga en horas valle.**

1. Abra **Complementos > Objetos conectados > Tesla BLE** y luego el dispositivo del vehículo (pestaña **Dispositivo**), sección **Carga en horas valle**.
2. Marque **Activar** (**Control de la carga**).
3. Indique **Inicio del intervalo** y **Fin del intervalo** según su contrato de electricidad, en la hora de Jeedom, por ejemplo `22:00` y `06:00` (se admite un intervalo a caballo de la medianoche; el fin debe ser distinto del inicio).
4. Indique **SoC objetivo (%)**: el nivel de batería, de 1 a 100, al que Jeedom detiene la carga. Elija un objetivo **inferior o igual al límite de carga del vehículo**.
5. Marque **Detener al final del intervalo** si la carga no debe continuar más allá de las horas valle (sin marcar: continúa hasta el límite del vehículo).
6. Para una parada precisa en el SoC objetivo, configure también **Intervalo durante la carga** en 1 o 2 minutos (véase más abajo, **Precisión**).
7. **Guarde**. Un ajuste no válido se rechaza con un mensaje **«Carga en horas valle: …»** (véase [Solución de problemas](#solucion-de-problemas)): no se guarda nada.
8. Compruebe: ponga el log del plugin en **Info** (**Configuración del plugin > Logs**). En la primera lectura del vehículo dentro del intervalo, una línea **«charge aux heures creuses : décision …»** (*carga en horas valle: decisión …*) indica lo que el plugin ha decidido y por qué (`charge_start`, `charge_stop`, `aucune`…). Si no arranca nada, consulte [Carga avanzada: síntomas sin mensaje](#carga-avanzada-sintomas-sin-mensaje).

**A tener en cuenta.** Dos comportamientos sorprenden a menudo:

- **Límite de carga del vehículo.** Si el **SoC objetivo** está **por encima** del límite de carga del vehículo, la carga se detiene en el límite del vehículo, sin error ni advertencia: el SoC objetivo nunca se alcanza. En cambio, un SoC objetivo inferior al límite detiene la carga antes.
- **Acción manual.** Un **Iniciar la carga** o un **Detener la carga** lanzado desde Jeedom (widget, escenario) durante el intervalo **suspende el control hasta el siguiente intervalo**: Jeedom nunca contradice su acción. Una carga reanudada desde la aplicación Tesla tras la parada en el SoC objetivo también suspende el control.

**Qué hace el plugin.** En cada lectura del vehículo por el ciclo de actualización:

- **dentro del intervalo**, con el vehículo **conectado** y **por debajo del SoC objetivo**: **Iniciar la carga**;
- **dentro del intervalo**, con una carga en curso cuyo nivel alcanza el SoC objetivo: **Detener la carga**, **aunque el límite de carga del vehículo sea más alto** (el SoC objetivo se compara con el **Nivel de batería (bruto)**, que puede diferir en unos puntos de **Carga de la batería**);
- **al final del intervalo**, si **Detener al final del intervalo** está marcado: la carga que siga en curso se detiene en la primera lectura del vehículo, **dentro de la hora siguiente** al final (pasado ese plazo, la carga ya no se interrumpe);
- **ningún comando innecesario**: no se inicia si la carga ya está en curso o si se ha alcanzado el objetivo, no se detiene si ya está detenida. **Como máximo un comando por lectura.**

**Hora de Jeedom.** El intervalo se lee en la hora de Jeedom (su zona horaria), no en la del vehículo. Un intervalo a caballo de la medianoche (`22:00` a `06:00`) funciona; el inicio está incluido, el fin está excluido.

**Precisión.** La decisión sigue la **frecuencia de lectura** del vehículo: la parada en el SoC objetivo puede superarlo en unos pocos puntos porcentuales si la lectura es espaciada. Para una parada precisa, active el **Intervalo durante la carga** (1 o 2 minutos, véase [Lectura acelerada durante la carga](#lectura-acelerada-durante-la-carga)). Se recomienda un intervalo de actualización de **15 minutos como máximo**: con un intervalo largo, el estado publicado puede estar obsoleto.

**Reposo del vehículo.** El plugin **nunca despierta el vehículo por sí mismo** para decidir: se basa en la información ya publicada. En cambio, **Iniciar la carga despierta el vehículo** (lo hace el proxy por sí solo) como cualquier comando, y un vehículo visto **dormido** **nunca** recibe un comando de parada (una carga publicada por un vehículo dormido es un estado obsoleto). Cuando el estado mostrado corresponde a un vehículo dormido, el mensaje de **Último error** lo indica («estado leído a las HH:MM, vehículo dormido»).

**Ninguna acción en estos casos.** La función está desactivada; el vehículo está **desconectado**, **fuera de alcance** o no se ha podido leer; el punto de carga no suministra corriente; el estado de carga es desconocido; la carga está **finalizada** (límite del vehículo alcanzado); el **SoC objetivo supera el límite del vehículo** (la carga se detiene entonces en ese límite, sin error ni advertencia: elija un objetivo inferior o igual al límite). El motivo es visible en **Último error**: **«Vehículo no conectado: carga en horas valle en espera»**, **«El punto de carga no suministra corriente: carga en horas valle en espera»** o **«Estado de carga desconocido: lance Actualizar (con despertar)»**. Estos mensajes nunca sustituyen a un error real del último ciclo de lectura, y el siguiente ciclo correcto vuelve a poner **Ninguna**.

**Comandos manuales y escenarios (prioridad).** **Iniciar la carga** y **Detener la carga** siguen siendo utilizables en cualquier momento. Un **Iniciar** o un **Detener** lanzado **desde Jeedom** (widget, escenario) **durante el intervalo**, o en la hora siguiente a su final, **suspende el control hasta el siguiente intervalo**: Jeedom nunca contradice su acción, ni detiene la carga al final del intervalo. Al día siguiente, el control se reanuda. El mensaje es solo una línea del log (ningún error). Dos casos se tratan aparte:

- **carga reanudada desde la aplicación Tesla tras la parada en el SoC objetivo**: detectada por una lectura al menos **2 minutos** después de la parada, también suspende el control (**«Carga en horas valle suspendida hasta el siguiente intervalo: carga reiniciada fuera del control»**) y ya no se interrumpe;
- **carga detenida desde la aplicación tras un arranque por Jeedom**: Jeedom **no reinicia** la carga (un solo arranque por conexión); si el arranque no va seguido de una carga, se muestra el mensaje **«Carga iniciada por Jeedom pero detenida o no iniciada: ningún nuevo intento antes del siguiente intervalo»** (véase [Solución de problemas](#solucion-de-problemas)).

**Fallos de comando.** Un comando que falla (rechazo del vehículo, tiempo de espera agotado, rol de llave insuficiente) muestra su mensaje en **Último error** y aparece una advertencia en el log; el nuevo intento tiene lugar en la lectura siguiente, **sin ráfaga**. Tras **3 fallos seguidos**, el control se **suspende hasta el siguiente intervalo** (**«Carga en horas valle suspendida hasta el siguiente intervalo: fallos de comando repetidos»**); una **desconexión** seguida de una reconexión lo reactiva. Un proxy **inaccesible** u **ocupado** no es un fallo: no se envía nada, el plugin lo reintenta en la lectura siguiente (como máximo una advertencia por hora señala un comando aplazado).

**Ajustes no válidos.** Una hora que no tenga el formato `HH:MM`, un SoC objetivo fuera de **1 a 100**, un intervalo vacío (fin igual al inicio) o una función activada sin inicio, fin o SoC objetivo se **rechaza al guardar** el dispositivo, con un mensaje **«Carga en horas valle: …»**; no se guarda nada.

**Otras funciones.** El control según el excedente se **ignora durante el intervalo** (véase [Control según el excedente](#control-segun-el-excedente)). Una programación de carga del vehículo ([Programar la carga](#programar-la-carga)) o de la aplicación Tesla puede **entrar en conflicto** con el intervalo: conserve solo una, ya que el intervalo de Jeedom no está coordinado con ellas. **Un solo intervalo** por vehículo.

### Ajustar la consigna de temperatura

Las acciones **Consigna del conductor** (`set_driver_temp`) y **Consigna del pasajero** (`set_passenger_temp`) ajustan, en °C, la temperatura solicitada en el lado del conductor y en el del pasajero. Son controles deslizantes, vinculados a las informaciones **Temperatura del conductor** y **Temperatura del pasajero**.

**Proxy del fork requerido, comandos ocultos.** El proxy oficial 2.3.0 no sabe ajustar la consigna de temperatura: el comando correspondiente lo añadió el fork (versión `2.3.0-tb.1` como mínimo). Mientras el proxy no anuncie este comando, las dos acciones se **rechazan de inmediato**, sin ningún intercambio con el vehículo, con el mensaje **«No compatible con su versión del proxy»**; el resto del dispositivo funciona con normalidad. Se crean **ocultas**: tras pasar al proxy del fork, marque **Mostrar** en cada una en la pestaña **Comandos** del dispositivo, o llámelas desde un escenario. La disponibilidad sigue el anuncio del proxy (ruta `capabilities`), que se vuelve a leer cuando cambia su versión: tras pasar al fork, los comandos pasan a ser utilizables sin reinstalar el plugin.

**Rango y paso.** El control deslizante va de **15 a 28 °C** en pasos de **0,5 °C**. Una vez leídos los datos del vehículo, sus límites siguen la temperatura mínima y la temperatura máxima ajustables del vehículo, **redondeadas hacia el interior** al grado entero (15,5 pasa a 16; 27,5 pasa a 27) y limitadas a 15-28 °C, rango aceptado por el proxy. Un **Mín** o un **Máx** que usted ajuste a mano en el comando nunca se sobrescribe. Un valor fuera de rango, o que no sea un número, se rechaza **antes** del envío con el mensaje **«Valor no válido: la consigna debe ser un número entre … y … °C»**; no se envía nada al vehículo. Un valor entre dos medios grados se **redondea al medio grado más próximo** (21,3 pasa a 21,5), ya que el vehículo ajusta por medios grados.

**El otro lado parte con su último valor leído.** El vehículo recibe siempre las dos temperaturas en el mismo comando. Ajustar el lado del conductor reenvía, por tanto, también la consigna del pasajero, con el último valor publicado por la información **Temperatura del pasajero**, y viceversa. Si este valor es desconocido (nunca leído, nulo o fuera de 15 a 28 °C), el vehículo recibe el **mismo valor en los dos lados**. Si ha ajustado el otro lado en la pantalla del vehículo desde la última lectura de Jeedom, **esa consigna puede sobrescribirse**: lance **Actualizar (con despertar)** antes de ajustar un lado para partir del valor actualizado.

**Tras el comando.** La información vinculada se actualiza de inmediato, luego se vuelve a leer el estado y se programa una relectura como tras cualquier comando (véase [Relectura tras un comando](#relectura-tras-un-comando)): la consigna realmente aplicada aparece en la relectura. El proxy despierta el vehículo si es necesario.

**Rol de la llave.** Se supone que el rol **Owner** es necesario (por confirmar en uso real). Con una llave Charging Manager, el rechazo del vehículo se muestra con el mensaje de rol insuficiente (véase [Rol de la llave](#rol-de-la-llave)).

### Calefactar los asientos y el volante

Seis acciones ajustan la calefacción: **Ajustar la calefacción del asiento delantero izquierdo** (`set_seat_heater_left`), **delantero derecho** (`set_seat_heater_right`), **trasero izquierdo** (`set_seat_heater_rear_left`), **trasero derecho** (`set_seat_heater_rear_right`), **trasero central** (`set_seat_heater_rear_center`) y **Ajustar la calefacción del volante** (`set_steering_wheel_heater`). Son listas de opciones.

**Proxy del fork requerido (versión `2.3.0-tb.2` como mínimo), comandos ocultos.** El proxy oficial 2.3.0 no sabe ajustar la calefacción de los asientos ni del volante: estos comandos los añadió el fork. Mientras el proxy no anuncie el comando, las seis acciones se **rechazan de inmediato**, sin ningún intercambio con el vehículo, con el mensaje **«No compatible con su versión del proxy»**; el resto del dispositivo funciona con normalidad. Se crean **ocultas**, incluso tras pasar al fork: **le corresponde a usted mostrarlas** (marque **Mostrar** en cada una en la pestaña **Comandos** del dispositivo) o llamarlas desde un escenario. La disponibilidad sigue el anuncio del proxy (ruta `capabilities`), que se vuelve a leer cuando cambia su versión: tras pasar al fork, los comandos pasan a ser utilizables sin reinstalar el plugin.

**Niveles.** Para un asiento: **Apagado** (0), **Bajo** (1), **Medio** (2), **Alto** (3). Un valor enviado por un escenario fuera de 0 a 3, o que no sea un entero, se rechaza **antes** del envío con el mensaje **«Valor no válido: el nivel de calefacción debe ser un entero entre 0 y 3»**. Para el volante: solo **Apagado** (0) o **Encendido** (1), no hay niveles; el plugin no escribe la información **Nivel de calefacción del volante** tras el comando, solo la actualiza la relectura. Un valor distinto de 0 o 1 se rechaza con el mensaje **«Valor no válido: la calefacción del volante debe ser 0 (apagado) o 1 (encendido)»**.

**¿Qué asiento?** Los asientos se designan por su **posición**: «delantero izquierdo» y «delantero derecho» no dependen del lado del volante. Las informaciones existentes conservan su nombre: en conducción a la izquierda, **Calefacción del asiento del conductor** corresponde al **delantero izquierdo** y **Calefacción del asiento del pasajero** al **delantero derecho** (al revés en conducción a la derecha). Los respaldos y la tercera fila no se ofrecen. Un asiento que el vehículo no tiene puede ser rechazado por el vehículo, o aceptado sin efecto y releído a 0 (por verificar en uso real).

**Climatización.** Según la documentación de Tesla, la calefacción de los asientos requiere que la climatización esté en marcha (preacondicionamiento o mantenimiento de clima); sin ella, el vehículo puede rechazar o ignorar el comando. Del mismo modo, en un vehículo con calefacción automática del volante, el comando del volante puede quedar sin efecto. Estos comportamientos deben validarse en uso real.

**Tras el comando.** La información vinculada (por ejemplo **Calefacción del asiento del pasajero**) se actualiza de inmediato con el nivel solicitado, luego se vuelve a leer el estado y se programa una relectura como tras cualquier comando (véase [Relectura tras un comando](#relectura-tras-un-comando)): el nivel realmente aplicado aparece en la relectura. Con **Leer también la climatización** en **No, solo carga**, estas informaciones no se vuelven a leer: conservan el valor anunciado. El proxy despierta el vehículo si es necesario.

**Rol de la llave.** Se supone que el rol **Owner** es necesario (por confirmar en uso real). Con una llave Charging Manager, el rechazo del vehículo se muestra con el mensaje de rol insuficiente (véase [Rol de la llave](#rol-de-la-llave)).

### Desempañado máximo

Una acción **Desempañado máximo** (`set_preconditioning_max`) activa o detiene el desempañado máximo del vehículo (desempañado y deshielo de los cristales y de los retrovisores). Es una lista de opciones: **Apagado** (0) o **Encendido** (1). Está vinculada a la información **Modo desempañado** (`defrost_mode`, valores `Off`, `Normal` o `Max`), y las informaciones de desempañado delantero y trasero (`is_front_defroster_on`, `is_rear_defroster_on`) se vuelven a leer con ella.

**Proxy del fork requerido (versión `2.3.0-tb.1` como mínimo), comando oculto.** El proxy oficial 2.3.0 no sabe controlar el desempañado máximo: el comando lo añadió el fork. Mientras el proxy no anuncie el comando, la acción se **rechaza de inmediato**, sin ningún intercambio con el vehículo, con el mensaje **«No compatible con su versión del proxy»**; el resto del dispositivo funciona con normalidad. Se crea **oculta**, incluso tras pasar al fork: **le corresponde a usted mostrarla** (marque **Mostrar** en la pestaña **Comandos** del dispositivo) o llamarla desde un escenario. La disponibilidad sigue el anuncio del proxy (ruta `capabilities`), que se vuelve a leer cuando cambia su versión: tras la actualización del proxy, el comando pasa a ser utilizable sin reinstalar el plugin.

> ⚠️ **Consumo y despertar.** Activar el desempañado máximo **despierta el vehículo** (a través del proxy) y **consume batería** mientras funciona. El plugin **nunca** lo inicia por sí mismo: solo lo envía una acción suya (widget o escenario). Acuérdese de detenerlo, por ejemplo con un segundo escenario tras la duración deseada.

**Valores.** Un valor enviado por un escenario distinto de 0 o 1 se rechaza **antes** del envío con el mensaje **«Valor no válido: el desempañado máximo debe ser 0 (apagado) o 1 (encendido)»**.

**Tras el comando.** **Modo desempañado** pasa de inmediato a `Max` (encendido) o `Off` (apagado), luego se vuelve a leer el estado y se programa una relectura como tras cualquier comando (véase [Relectura tras un comando](#relectura-tras-un-comando)): el valor real aparece en la relectura (al apagar, el vehículo puede indicar `Normal` si la climatización sigue funcionando). Los desempañados delantero y trasero solo se actualizan en esta relectura. Con **Leer también la climatización** en **No, solo carga**, o si el vehículo se vuelve a dormir, estas informaciones no se vuelven a leer: conservan el valor anunciado.

**Rol de la llave.** Se supone que el rol **Owner** es necesario (por confirmar en uso real). Con una llave Charging Manager, el rechazo del vehículo se muestra con el mensaje de rol insuficiente y la insignia **Rol insuficiente** (véase [Rol de la llave](#rol-de-la-llave)).

### Modo perro, modo camping y mantenimiento de clima

Una acción **Modo de mantenimiento de clima** (`set_climate_keeper_mode`) elige el mantenimiento de la climatización del vehículo estacionado: **Apagado** (0), **Mantenimiento** (1), **Modo perro** (2) o **Modo camping** (3). Está vinculada a la información **Mantenimiento de clima (perro, camping)** (`climate_keeper_mode`, valores `Off`, `On`, `Dog`, `Party` o `Unknown`): el modo camping aparece allí con el nombre `Party` según el vehículo (por confirmar en uso real).

**Proxy del fork requerido (versión `2.3.0-tb.1` como mínimo), comando oculto.** El proxy oficial 2.3.0 no sabe controlar el mantenimiento de clima: el comando lo añadió el fork. Mientras el proxy no anuncie el comando, la acción se **rechaza de inmediato**, sin ningún intercambio con el vehículo, con el mensaje **«No compatible con su versión del proxy»**; el resto del dispositivo funciona con normalidad. Se crea **oculta**, incluso tras pasar al fork: **le corresponde a usted mostrarla** (marque **Mostrar** en la pestaña **Comandos** del dispositivo) o llamarla desde un escenario. La disponibilidad sigue el anuncio del proxy (ruta `capabilities`), que se vuelve a leer cuando cambia su versión: tras la actualización del proxy, el comando pasa a ser utilizable sin reinstalar el plugin.

> ⚠️ **Batería y despertar.** Elegir un mantenimiento **despierta el vehículo** (a través del proxy) y **consume batería durante mucho tiempo**; el vehículo puede rechazarlo (batería baja, estado del vehículo). El plugin **nunca** lo inicia por sí mismo y nunca lo detiene: solo lo envía una acción suya (widget o escenario).

> ⚠️ **Animal.** Este modo **no sustituye una vigilancia de la temperatura** del habitáculo para un animal. La lectura sigue el intervalo de actualización del vehículo: una alerta debe basarse en la **Temperatura interior** y en un intervalo adecuado.

**Valores.** Un valor enviado por un escenario fuera de 0 a 3 se rechaza **antes** del envío con el mensaje **«Valor no válido: el modo de mantenimiento de clima debe ser 0 (apagado), 1 (mantenimiento), 2 (perro) o 3 (camping)»**.

**Tras el comando.** **Mantenimiento de clima (perro, camping)** pasa de inmediato a `Off`, `On`, `Dog` o `Party`, luego se vuelve a leer el estado y se programa una relectura como tras cualquier comando (véase [Relectura tras un comando](#relectura-tras-un-comando)): el valor real aparece en la relectura. Con **Leer también la climatización** en **No, solo carga** (deje **Sí** para este modo), o si el vehículo se vuelve a dormir, la información no se vuelve a leer: conserva el valor anunciado, y la ventana de sueño puede abrirse (véase [Dejar que el vehículo se duerma](#dejar-que-el-vehiculo-se-duerma)).

**Rol de la llave.** Se supone que el rol **Owner** es necesario (por confirmar en uso real). Con una llave Charging Manager, el rechazo del vehículo se muestra con el mensaje de rol insuficiente y la insignia **Rol insuficiente** (véase [Rol de la llave](#rol-de-la-llave)).

### Preacondicionamiento planificado por Jeedom

El plugin puede **iniciar la climatización antes de la hora de salida** y luego detenerla, con la temperatura ya configurada en el vehículo. Funciona con el proxy oficial 2.3.0 (comandos **Iniciar la climatización** y **Detener la climatización**), sin fork. Los ajustes están en la sección **Preacondicionamiento planificado por Jeedom** del dispositivo; no la confunda con la información **Preacondicionamiento planificado** (`scheduled_preconditioning_time`), que **lee** la programación hecha en el vehículo.

**Paso a paso: configurar el preacondicionamiento planificado.**

1. Abra **Complementos > Objetos conectados > Tesla BLE** y luego el dispositivo del vehículo (pestaña **Dispositivo**), sección **Preacondicionamiento planificado por Jeedom**.
2. Indique la **Hora de salida**, en la hora de Jeedom, por ejemplo `07:30`.
3. Marque los **Días** de salida correspondientes.
4. Configure la **Antelación (min)** (vacío: 15 minutos) y la **Duración máxima (min)** (vacío: 30 minutos, o la antelación más 15 minutos si la antelación supera 15). Con 15 y 30, la climatización arranca a las `07:15` y se detiene a las `07:45`.
5. Marque **Solo si está conectado** si la climatización no debe consumir la batería de un vehículo desconectado.
6. Marque **Activar** (**Control de la climatización**) y luego **guarde**. Un ajuste no válido se rechaza con un mensaje **«Preacondicionamiento planificado: …»** (véase [Solución de problemas](#solucion-de-problemas)): no se guarda nada.
7. Compruebe: ponga el log del plugin en **Info**. En la primera lectura del vehículo dentro de la ventana, una línea **«préconditionnement planifié : décision …»** (*preacondicionamiento planificado: decisión …*) indica lo que el plugin ha decidido y por qué.

**Ejemplo de uso: salida entre semana a las 7:30.** Configure **Hora de salida** en `07:30`, marque de **Lunes** a **Viernes**, deje **Antelación** en 15 y **Duración máxima** en 30, marque **Solo si está conectado** y **Activar**. El vehículo permanece conectado por la noche:

- Si utiliza también la [Carga en horas valle](#carga-en-horas-valle) (por ejemplo de `22:00` a `06:00`), la carga termina antes de la ventana del preacondicionamiento, que va de `07:15` a `07:45`: las dos funciones no se estorban.
- De lunes a viernes, en la primera lectura del vehículo después de las `07:15`, la climatización se inicia si está detenida y si el vehículo está conectado. El log del plugin (nivel **Info**) muestra **«préconditionnement planifié : décision `auto_conditioning_start` (demarrage) »** (*preacondicionamiento planificado: decisión `auto_conditioning_start` (arranque)*), y la información **Climatización activada** pasa a 1 en la lectura siguiente.
- En la primera lectura posterior a las `07:45`, si la climatización sigue funcionando tras este arranque por Jeedom, se detiene (decisión `auto_conditioning_stop`).
- El sábado y el domingo no ocurre nada. Si sale antes de las `07:45`, detenga usted mismo la climatización desde Jeedom: Jeedom no la reinicia después.

**La ventana.** Empieza en la hora de salida **menos la antelación** y dura la **duración máxima** a partir de ese inicio (inicio incluido, fin excluido). El día que cuenta es el de la **hora de salida**: una salida a las `00:10` con 20 minutos de antelación arranca la víspera a las `23:50`, y hay que marcar el día siguiente. Todo está en la **hora de Jeedom** (su zona horaria), no en la del vehículo; una salida que cae en la hora omitida del cambio al horario de verano se desplaza una hora.

**Qué hace el plugin.** En cada lectura correcta del vehículo por el ciclo de actualización, **dentro de la ventana**: si la climatización está detenida (y, con la opción, el vehículo conectado), **Iniciar la climatización** (**un solo arranque correcto por salida**); **en la primera lectura posterior al final de la ventana** (dentro de la hora), si la climatización sigue funcionando tras un arranque de Jeedom, **Detener la climatización**. Como máximo **un comando por lectura**, ningún comando innecesario.

**Precisión.** La decisión sigue la **frecuencia de lectura** del vehículo: el arranque puede llegar unos minutos después de la hora prevista, y la parada superar el final en un intervalo. Se aconseja un intervalo de actualización de **5 minutos como máximo**. Con un intervalo más largo que la duración de la ventana, ninguna lectura cae dentro: ni arranque ni parada. Todavía es posible un arranque **después de la hora de salida**, mientras la ventana no haya terminado.

**Reposo del vehículo.** El plugin **nunca despierta el vehículo por sí mismo** para decidir y nunca envía un comando de despertar, pero **Iniciar la climatización despierta el vehículo** (lo hace el proxy por sí solo) y consume batería. Un vehículo visto **dormido** **nunca** recibe un comando de parada: su climatización se considera detenida.

**Prioridad a sus acciones.** Jeedom nunca contradice su acción:

- un **Iniciar la climatización** o **Detener la climatización** lanzado **desde Jeedom** (widget, escenario) durante la ventana **suspende el preacondicionamiento hasta la salida siguiente**, y la climatización no se detiene al final de la ventana;
- una climatización **ya en marcha** al entrar en la ventana (o iniciada desde la aplicación Tesla, o por la programación del vehículo) no se reinicia ni se detiene;
- una climatización **detenida desde la aplicación** tras el arranque de Jeedom (detectada por una lectura al menos **2 minutos** después del comando) no se reinicia en bucle;
- un **modo perro, camping, mantenimiento** o un **desempañado máximo** en curso nunca se detiene ni se sustituye.

Desactivar la función o modificar sus ajustes **durante la ventana no detiene** una climatización ya iniciada.

**Rol de la llave.** Se supone que el rol **Owner** es necesario (por confirmar en uso real). Con una llave Charging Manager, el vehículo rechaza el comando: el mensaje de rol insuficiente se muestra en **Último error**, la información **Rol de la llave** pasa a **Charging Manager**, y **solo se hace un intento por salida** (véase [Rol de la llave](#rol-de-la-llave)).

**Fallos de comando.** Un comando que falla (rechazo del vehículo, tiempo de espera agotado) muestra su mensaje en **Último error** y aparece una advertencia en el log; el nuevo intento tiene lugar en la lectura siguiente, **sin ráfaga**. Tras **3 fallos seguidos**, el control se **suspende hasta la salida siguiente**. Un proxy **inaccesible** u **ocupado** no es un fallo: no se envía nada, el plugin lo reintenta en la lectura siguiente.

**Ninguna acción en estos casos.** La función está desactivada o el día no está marcado; el vehículo no se ha podido leer o está **fuera de alcance**; con la opción, el vehículo está **desconectado** o su estado de carga es desconocido; el estado de la climatización es desconocido; la climatización ya está funcionando. El motivo es visible en **Último error** para los casos útiles (**«Vehículo no conectado: preacondicionamiento planificado no iniciado»**, **«Estado de carga desconocido: lance Actualizar (con despertar)»**), sin sustituir nunca a un error real del último ciclo de lectura.

**Otras funciones.** El preacondicionamiento planificado es **independiente** de la programación hecha en el vehículo ([Preacondicionamiento planificado](#informaciones) leído por el plugin): si el vehículo ya está preacondicionando, la climatización se ve activa y Jeedom no interviene. Puede encadenarse, en la misma pasada, con la [Carga en horas valle](#carga-en-horas-valle): los dos comandos salen uno tras otro. El plugin no tiene en cuenta la presencia de un ocupante: una climatización iniciada por Jeedom y todavía en marcha en la primera lectura posterior al final de la ventana se detiene.

### Confirmación de las acciones sensibles

Cinco acciones piden una **confirmación** antes del envío, en el dashboard y en el móvil: **Desbloquear las puertas** (`door_unlock`), **Abrir el puerto de carga** (`charge_port_door_open`), **Modo Centinela** (`set_sentry_mode`), **Abrir el maletero trasero** (`open_trunk_rear`) y **Abrir el maletero delantero** (`open_trunk_front`). Las demás acciones (bloquear, tocar la bocina, luces, carga, climatización…) se envían al primer clic.

- **Un clic abre una ventana de confirmación.** No se envía nada mientras no haya confirmado.
- **Casilla «Confirmar la acción».** Se encuentra en los parámetros avanzados del comando (pestaña **Comandos** del dispositivo, rueda dentada del comando). Está **marcada al crearse**; desmárquela para quitar la confirmación de un comando, márquela en otro para añadirla. El complemento nunca reescribe su elección (actualización incluida: en un dispositivo existente, la actualización establece la confirmación una sola vez, salvo donde usted ya la hubiera configurado).
- **Un escenario no se ve afectado.** Una acción llamada desde un escenario se ejecuta **sin confirmación**. Una llamada por la API JSON-RPC de Jeedom debe pasar `confirmAction=1`; de lo contrario, Jeedom la rechaza.

> **IMPORTANTE: esto no es una protección de seguridad.** La confirmación es una salvaguarda de la interfaz contra el clic accidental, nada más. El proxy no tiene **ninguna autenticación** por defecto: cualquier máquina de su red que pueda alcanzarlo puede desbloquear o abrir el vehículo **sin pasar por Jeedom**, por tanto sin confirmación. Mantenga el proxy en una red de confianza, nunca expuesto a Internet (véase [Rol de la llave](#rol-de-la-llave)).

Para **Modo Centinela**, el estado mostrado tras la orden se describe en [Estado del modo Centinela](#estado-del-modo-centinela) (origen **Real** o **Última orden**).

### Abrir el maletero trasero y el maletero delantero

Dos acciones abren un maletero a distancia: **Abrir el maletero trasero** (`open_trunk_rear`) y **Abrir el maletero delantero** (`open_trunk_front`, el maletero delantero o frunk). Envían el mismo comando del proxy, `actuate_trunk`, con el maletero deseado. El estado se lee en las informaciones **Maletero trasero** (`trunk_rear`) y **Maletero delantero** (`trunk_front`).

**Se requiere el proxy del fork (versión `2.3.0-tb.2` como mínimo), comandos ocultos.** El proxy oficial 2.3.0 no tiene este comando: lo añadió el fork. Mientras el proxy no anuncie el comando, las dos acciones se **rechazan de inmediato**, sin ningún intercambio con el vehículo, con el mensaje **«No compatible con su versión del proxy»**. Se crean **ocultas**, incluso después de pasar al fork: **le corresponde a usted mostrarlas** (marque **Mostrar** en la pestaña **Comandos** del dispositivo) o llamarlas desde un escenario. La disponibilidad sigue el anuncio del proxy (ruta `capabilities`), que se vuelve a leer cuando cambia su versión: tras actualizar el proxy, las acciones pasan a ser utilizables sin reinstalar el complemento ni recrear el dispositivo. Para estas dos acciones, el complemento no muestra ni la insignia **Función no disponible** ni la insignia **Rol insuficiente**: el rechazo se muestra al hacer clic.

**Confirmación.** Un clic pide una **confirmación** antes del envío, como para las demás acciones sensibles: véase [Confirmación de las acciones sensibles](#confirmacion-de-las-acciones-sensibles) (casilla **Confirmar la acción**, escenario sin confirmación, JSON-RPC `confirmAction=1`).

**Verificación antes de abrir el maletero trasero.** Para el maletero trasero, el vehículo trata el comando como una **alternancia**: en un portón motorizado ya abierto, lo **cerraría**. Por ello el complemento relee primero el estado del vehículo (sin despertarlo) y solo envía el comando si el maletero trasero se lee **cerrado**. Tres rechazos posibles, ningún envío, y **Último error** no se modifica:

- **«Maletero ya abierto o en movimiento: comando no enviado»**: el maletero trasero está abierto, entreabierto, abriéndose o cerrándose;
- **«Estado del maletero desconocido: comando no enviado»**: el vehículo no da un estado utilizable para este maletero;
- **«Estado del maletero ilegible, comando no enviado: …»**: la relectura ha fallado (proxy inaccesible, vehículo fuera de alcance…), la causa sigue al mensaje.

El estado releído se publica en las informaciones antes del rechazo: si el maletero ya estaba abierto, **Maletero trasero** pasa a 1. El **maletero delantero** no se relee: no se cierra a distancia, el comando solo puede abrirlo. **El complemento nunca cierra un maletero.**

> ⚠️ **Despertar.** Estos comandos **despiertan el vehículo** (a través del proxy), y el complemento nunca los lanza por sí mismo: solo una acción por su parte (widget o escenario) los envía.

**Después del comando.** No se supone ningún valor: se relee el estado y luego se programa una relectura como después de cualquier comando (véase [Relectura tras un comando](#relectura-tras-un-comando)). **Maletero trasero** o **Maletero delantero** pasa a 1 cuando el vehículo anuncia el maletero abierto, a veces en la relectura siguiente.

**Rol de la llave.** Se supone necesario el rol **Owner** (por confirmar en uso real). Con una llave Charging Manager, el rechazo del vehículo se muestra con el mensaje de rol insuficiente (véase [Rol de la llave](#rol-de-la-llave)).

### Estado del modo Centinela

Dos informaciones indican si el modo Centinela está activo: **Centinela** (`sentry_mode`) vale **Activada**, **Desactivada** o **Desconocido**, y **Origen del modo Centinela** (`sentry_mode_source`) indica de dónde procede ese valor. El comando que lo activa o desactiva es **Modo Centinela** (`set_sentry_mode`).

| Origen | Qué significa |
|---|---|
| **Real** | El valor se ha **leído en el vehículo**. Disponible con el **proxy del fork en versión `2.3.0-tb.2` como mínimo** y un vehículo **despierto**: un vehículo dormido no se lee, y la información conserva entonces el **último valor leído** (véase [Reposo del vehículo y frescura de los datos](#reposo-del-vehiculo-y-frescura-de-los-datos)). Un cambio hecho desde la aplicación Tesla o la pantalla del vehículo se ve en la lectura siguiente. |
| **Última orden** | El complemento no puede leer el modo Centinela (proxy oficial 2.3.0, o fork más antiguo): el valor es el de la **última orden correcta enviada por Jeedom**. Un cambio hecho desde la aplicación, la pantalla del vehículo o un **corte automático** **no se ve**. |
| **Ninguna** | Todavía no se ha leído ni ordenado nada: **Centinela** vale **Desconocido** (nunca un falso «Desactivada»). |

**Después de una orden.** Una orden **correcta** publica de inmediato el valor ordenado con el origen **Última orden**, aunque el proxy sepa leer el modo Centinela; en la relectura siguiente, el origen vuelve a **Real**. Durante el tiempo de la **relectura tras un comando** (30 segundos por defecto, véase [Relectura tras un comando](#relectura-tras-un-comando)), se ignora una lectura real que contradiga la orden: el proxy sirve todavía el estado anterior. Una orden **rechazada** o con error no cambia nada.

**Estados del vehículo.** Solo `Off` da **Desactivada**. Los demás estados (`Idle`, `Armed`, `Aware`, `Panic`, `Quiet`) dan **Activada**: `Idle`, el modo Centinela en reposo, se cuenta como **Activada** (por confirmar en uso real). Un valor desconocido o ausente deja la información sin cambios.

**Reinicio de Jeedom.** El último valor conocido y su origen se **conservan** y se recuperan al arrancar, incluso tras un corte de alimentación.

> **En un escenario.** Las etiquetas **Activada**, **Desactivada**, **Desconocido**, **Real**, **Última orden** y **Ninguna** **siguen el idioma de Jeedom**: compárelas en el idioma actual de su Jeedom. Para saber si el valor es fiable, pruebe **Origen del modo Centinela** (por ejemplo **Real**) además de **Centinela**.

### Alertas de apertura prolongada

El complemento puede **avisarle** cuando una apertura (puerta, maletero trasero, maletero delantero, portón, puerto de carga) permanece abierta, o cuando el vehículo permanece **desbloqueado sin ocupante**, durante más tiempo que la duración que usted elija. Las alertas están **desactivadas por defecto** y se configuran **por vehículo**, en el bloque **Alertas de apertura prolongada** de la página del dispositivo:

| Ajuste | Función |
|---|---|
| **Apertura que sigue abierta**: **Activar** | Activa la alerta de las aperturas. |
| **Duración antes de la alerta (min)** | De 1 a 1440 minutos. **Obligatoria** para activar la alerta; una duración no válida se rechaza al guardar. |
| **Vehículo desbloqueado sin ocupante**: **Activar** | Activa la alerta del bloqueo, con **su propia duración** (**Duración antes de la alerta (min)**). |

Las dos alertas son independientes. Una alerta consiste en:

- **un mensaje** en el centro de mensajes de Jeedom, que nombra el vehículo y la apertura (por ejemplo «Mi Tesla: apertura «Maletero delantero» abierta desde hace más de 10 min»), **una sola vez por episodio**; **varias aperturas abiertas a la vez dan varios mensajes**, uno por apertura;
- **la información a 1**: **Alerta de aperturas** (`closures_alert`) mientras al menos una apertura haya permanecido abierta más allá de la duración, **Alerta de vehículo desbloqueado sin ocupante** (`unlocked_alert`) para el bloqueo. Utilícelas como disparador de un escenario para recibir una notificación por el medio que prefiera; están **ocultas** e **historizadas**: muéstrelas si lo desea.

Cuando todo vuelve a estar cerrado (o rebloqueado, o hay un ocupante presente), la información vuelve a **0** y una nueva apertura prolongada volverá a alertar. **El mensaje permanece en el centro de mensajes** tras el cierre: Jeedom no lo retira, elimínelo usted mismo.

**Precisión.** Las alertas se evalúan **en cada lectura correcta del estado del vehículo**, es decir, a la frecuencia de actualización (5 minutos por defecto, véase [Actualización de las informaciones](#actualizacion-de-las-informaciones)). La duración se cuenta desde la **primera lectura que ve la anomalía**: la alerta se envía **entre la duración elegida y esa duración más dos intervalos de actualización** después de la apertura real; «abierta desde hace más de 10 min» es por tanto siempre cierto.

**Nunca una alerta sobre un valor caducado.** Cuando el proxy es inaccesible, el vehículo está fuera de alcance o la lectura falla, **no se evalúa nada** y la duración no se acumula. Si la interrupción supera **dos intervalos de actualización más dos minutos**, el cronómetro **vuelve a cero** al regresar las lecturas; una alerta ya emitida sigue emitida, sin nuevo mensaje.

**Puerto de carga.** El puerto abierto cuenta como anomalía **solo si el vehículo se ha visto desconectado** (último **Estado de la carga** leído: `Disconnected`). Conectado, en carga o estado desconocido: ninguna alerta para el puerto.

**Presencia desconocida.** «Desbloqueado sin ocupante» solo se evalúa si el vehículo está **desbloqueado** y el **Ocupante presente** vale **0**: una presencia desconocida no dispara nada (véase [Información](#informaciones)).

### Posición y privacidad

La posición del vehículo es un **dato personal**: dice dónde está usted y cuándo no está. El complemento la protege por defecto, pero algunas precauciones quedan a su cargo.

**Qué se lee y cuándo.** La posición solo la proporciona el **proxy del fork** (`2.3.0-tb.2` como mínimo): el proxy oficial 2.3.0 no la sirve, y las informaciones no existen entonces (véase [Datos ampliados: qué está disponible](#datos-ampliados-que-esta-disponible)). Se lee como máximo **cada 15 minutos**, solo cuando el vehículo está **despierto y al alcance Bluetooth** del proxy, nunca despertándolo. Como el proxy está en su garaje, la posición leída es en la práctica la del domicilio. Una posición ausente, en 0/0, fuera de rango o **con más de una hora de antigüedad** se ignora: las informaciones conservan su último valor.

**No visible y no historizada por defecto.** **Latitud** y **Longitud** se crean **ocultas** y **no historizadas**: no aparecen ni en el widget ni en un gráfico, y no se conserva nada. Para utilizarlas:

1. Abra la pestaña **Comandos** del dispositivo.
2. En **Latitud** y **Longitud**, marque **Mostrar** para verlas en el widget, e **Historizar** para conservar sus valores.
3. **Guarde**. Esta elección no se sobrescribe nunca después.

Atención: una posición historizada se almacena en la base de datos de Jeedom y en sus copias de seguridad, como cualquier historial. Historice solo si lo necesita.

**El domicilio y el radio.** La información **En casa** vale **1** cuando el vehículo está a menos de **Radio (m)** del domicilio, **0** más allá. El domicilio se configura en la pestaña **Dispositivo**, sección **Posición del domicilio** (véase [Configuración de los dispositivos](#configuracion-de-los-dispositivos)):

| Ajuste | Valor |
|---|---|
| **Latitud** y **Longitud** | Las coordenadas de su domicilio. **Ambas vacías: la posición de Jeedom** (**Ajustes > Sistema > Configuración**, pestaña **General**). Se rechaza que solo una esté rellenada. |
| **Radio (m)** | Entero de **10 a 10000**. Vacío: **100 m**. Un GPS impreciso o un garaje subterráneo pueden requerir un radio mayor. |

Al guardar el dispositivo, **En casa** se recalcula de inmediato a partir de la última posición leída (si **Latitud** y **Longitud** existen en el dispositivo), sin esperar a la lectura siguiente.

**Límites de En casa.** Es una información binaria que no sabe decir «desconocido»:

- **Nunca se escribe** mientras el **domicilio** (ninguna coordenada indicada, ninguna posición en Jeedom) o la **posición** (nunca leída, ignorada) sean desconocidos. **Antes de cualquier cálculo, el mosaico muestra 0**: por tanto no prueba que el vehículo se haya ido.
- **No vuelve a 0** cuando el vehículo se va: fuera del alcance Bluetooth, ya no se lee ninguna posición y la información conserva su **último valor** (1). También conserva su valor si borra el domicilio o si la posición se vuelve demasiado antigua.
- **En un escenario**, pruebe `== 1` (nunca `== 0` ni «distinto de 1»), y **combínelo con Presencia del vehículo**: «En casa vale 1 **y** Presencia del vehículo vale 1» significa que el vehículo está en su casa y es accesible. **Presencia del vehículo a 0** indica que ya no está al alcance del proxy, es decir, en la práctica que se ha ido.

**El log `event` de Jeedom.** El complemento **nunca** escribe una coordenada (del vehículo o del domicilio) ni una distancia en su propio log, a ningún nivel, ni siquiera en **Debug**. Pero Jeedom registra por sí mismo cada nuevo valor de una información en su log **`event`** (**Análisis > Registros**): **Latitud** y **Longitud** aparecen allí, **incluso ocultas y no historizadas**. Para protegerse, a su elección: baje el nivel del log `event` en los ajustes de logs de Jeedom (**Ajustes > Sistema > Configuración**, pestaña **Logs**), o elimine las informaciones **Latitud** y **Longitud** del dispositivo (**En casa** sigue calculándose). El complemento recrea los comandos que faltan en cada guardado del dispositivo: elimínelos de nuevo si vuelven. Revise también una captura del log antes de publicarla en un foro.

**El proxy debe seguir protegido.** El proxy oficial no tiene **ninguna autenticación**: cualquier dispositivo de su red local puede pedirle la posición del vehículo. El proxy del fork, el único que sirve la posición, **puede** exigir un **token de API** (opcional: ajuste **Token de API del proxy** de la configuración del complemento), que protege también la posición. En cualquier caso, mantenga el proxy en una red de confianza y **nunca** exponga su puerto a Internet (véase [Rol de la llave](#rol-de-la-llave) y [Configuración del complemento](#configuracion-del-plugin)).

### Por qué las llamadas son secuenciales

Un proxy tiene **un solo adaptador Bluetooth** y una sola cola de intercambios con los vehículos: dos peticiones enviadas a la vez se estorbarían. Por ello el complemento hace pasar los intercambios de un mismo proxy **uno tras otro**, todos los vehículos incluidos (lecturas del ciclo, comandos, **Actualizar**, **Verificar el emparejamiento**).

- **Un mismo proxy**: un solo intercambio a la vez. Si hay un comando en curso, la lectura del ciclo se omite y se reanuda en la pasada siguiente (el minuto siguiente); un comando o un **Actualizar** espera su turno. Cuando la espera dura demasiado (unos 2 minutos), el complemento desiste y muestra **Proxy ocupado**: reintente dentro de un momento (véase [Solución de problemas](#solucion-de-problemas)).
- **Proxys distintos**: se leen **en paralelo** y nunca se esperan entre sí. Un proxy lento o detenido solo retrasa sus propios vehículos; el ciclo dura tanto como su proxy más lento.
- **En el peor caso** (proxy muy lento, cada lectura llegando a su plazo máximo), un ciclo de 4 minutos lee **3 vehículos por proxy** como máximo; más allá, los últimos pueden no leerse en ese ciclo. En la práctica, una lectura dura unos segundos.

### Resumen de los ajustes de frecuencia y de despertar

Todos estos ajustes se encuentran en la pestaña **Dispositivo** de cada vehículo (véase [Configuración de los dispositivos](#configuracion-de-los-dispositivos)). Los valores por defecto se aplican también a los vehículos existentes tras la actualización.

| Ajuste | Por defecto | Valores posibles | Efecto sobre la batería del vehículo |
|---|---|---|---|
| **Intervalo de actualización** | 5 minutos | 1, 2, 5, 10, 15 o 30 minutos | Cuanto más largo, menos se solicita el vehículo. Por sí solo, nunca despierta el vehículo. |
| **Intervalo durante la carga** | Desactivado | Desactivado, o 1, 2, 5, 10 o 15 minutos | Sin efecto fuera de la carga; durante la carga el vehículo está despierto de todos modos. |
| **Dejar que el vehículo se duerma** | Marcado | Marcado o desmarcado | Marcado: el complemento deja de leer los datos cuando el vehículo está inactivo, para que pueda dormirse. |
| **Lecturas sin cambios antes de la ventana** | 3 | 1, 2, 3, 4, 5, 10 o 15 | Cuanto más bajo, antes se abre la ventana. |
| **Duración de la ventana** | 30 minutos | 15, 20, 30, 45 minutos, 1 h, 1 h 30 o 2 h | Cuanto más larga, más tiempo tiene el vehículo para dormirse, pero más tiempo permanecen estáticos los datos. |
| **Retardo de relectura tras un comando** | 30 segundos | 30 segundos, 45 segundos, 1 minuto, 1 minuto 30 o 2 minutos | Una lectura por comando correcto, sin despertar. |
| **Leer también la climatización** | Sí | Sí, o No (solo carga) | «Solo carga» acorta la petición de datos (ganancia por medir en su instalación). |
| **Actualizar (con despertar)** (comando `refresh_wakeup`) | | Acción, para lanzar a mano o desde un escenario | **Despierta** el vehículo en cada ejecución. |
| **Antigüedad de los datos (min)** (información `data_age`) | | Minutos transcurridos desde la última lectura correcta de los datos; **99999** = ninguna lectura conocida (o más de 69 días) | Ninguno: cálculo local, no se consulta el proxy. |

La **duración de la ventana** solo tiene efecto si supera el intervalo de actualización. Detalle de cada ajuste: [Actualización de las informaciones](#actualizacion-de-las-informaciones), [Lectura acelerada durante la carga](#lectura-acelerada-durante-la-carga), [Dejar que el vehículo se duerma](#dejar-que-el-vehiculo-se-duerma) y [Relectura tras un comando](#relectura-tras-un-comando).

### Recomendaciones según el uso

Los valores siguientes son **puntos de partida indicativos, que debe ajustar según sus propias mediciones**: el efecto real sobre la batería depende del modelo, del software del vehículo y de su entorno, y el complemento no garantiza que el vehículo se duerma. Aquí no se anuncia ningún porcentaje de batería por falta de una medición fiable; la tabla cuantifica lo que el complemento hace realmente: el número de lecturas de datos por hora y el tiempo que se deja al vehículo para dormirse.

| Uso | Intervalo de actualización | Intervalo durante la carga | Ventana de sueño | Leer también la climatización | Lecturas de datos (vehículo despierto, inactivo, fuera de carga) |
|---|---|---|---|---|---|
| **Supervisión simple** (presencia, bloqueo, nivel de batería) | 10 a 15 minutos | Desactivado | Marcada, 3 lecturas sin cambios, 30 minutos (valores por defecto) | Sí | 4 a 6 por hora como máximo; **ninguna** durante los 30 minutos de una ventana abierta |
| **Control solar** (ajustar la corriente según la producción) | 5 minutos | **1 minuto** | Marcada, 3 lecturas sin cambios, 30 minutos (valores por defecto) | No (solo carga), si no utiliza la climatización | 12 por hora fuera de carga; **60 por hora durante la carga** (la ventana nunca se abre en carga) |
| **Seguimiento cercano** (carga o preacondicionamiento vigilados de cerca) | 1 a 2 minutos | 1 minuto | Marcada, 3 lecturas sin cambios, 30 minutos | Sí | 30 a 60 por hora: el vehículo no duerme mientras la ventana no esté abierta; reserve este perfil para un periodo concreto |
| **Varios vehículos en un proxy** (3 como máximo) | 10 a 15 minutos | Desactivado, salvo para el vehículo controlado | Marcada | Sí | Las lecturas de un mismo proxy pasan una tras otra: mantenga intervalos largos |

Para el control solar, mantenga también el **Retardo de relectura tras un comando** en 30 segundos y espacie las órdenes de **Corriente de carga** de su escenario (se lanza una relectura después de cada comando correcto).

**Medir el efecto en su caso.** Anote el nivel de **Carga de la batería** por la noche y por la mañana, con el vehículo aparcado y sin ocupante, durante unas noches con **Dejar que el vehículo se duerma** marcado, y luego unas noches desmarcado. Historice **Vehículo despierto** para ver cuánto tiempo ha permanecido despierto el vehículo: compare las dos series antes de ajustar el intervalo o la duración de la ventana.

## Widget y visualización

Esta sección describe lo que el plugin muestra en el dashboard y en la interfaz web móvil de Jeedom: el **mosaico del vehículo**, los **tipos genéricos**, la **imagen del modelo** y el **orden de los comandos**. Estas funciones no exigen una versión de Jeedom más reciente que la del plugin (véase [Requisitos previos](#requisitos-previos)) y no recurren a ningún sitio de Internet: todo se muestra desde su Jeedom.

**Lo que el plugin nunca reescribe**: un tipo genérico que usted haya elegido, una imagen que haya subido o quitado, el orden de los comandos que haya modificado y su elección entre el mosaico y el widget estándar. Cada subsección precisa la regla exacta.

### Mosaico del vehículo

Cada vehículo se muestra por defecto en forma de **mosaico**: un resumen legible de un vistazo, seguido de sus demás comandos visibles.

El resumen contiene, de arriba abajo:

- la **imagen del modelo** (si existe, véase [Imagen del modelo](#imagen-del-modelo)) ;
- **Batería** (el nivel, en grande) y **Límite de carga** ;
- **Autonomía** (en km) y **Estado de carga** (etiqueta traducida: cargando, finalizada, desconectado…) ;
- dos indicadores: **Bloqueado** o **Desbloqueado**, y **En alcance** o **Fuera de alcance** ;
- la frescura de los datos: **Datos de hace** seguido de una duración (minutos, horas o días), o **Ninguna lectura conocida** ;
- el **último error**, en una línea roja, **solo si lo hay** (no se muestra nada cuando vale «Ninguno») ;
- seis botones: **Iniciar la carga**, **Detener la carga**, **Bloquear las puertas**, **Desbloquear las puertas**, **Despertar** y **Actualizar**.

Los comandos **visibles** del dispositivo que el resumen no incluye (por ejemplo la temperatura, las aperturas, el modo Centinela) se muestran **debajo** del resumen, como en el widget estándar y en el orden de la pestaña **Comandos**. Los comandos que incluye el resumen no se repiten debajo.

<!-- Capture à ajouter en recette : images/tuile-dashboard-normal.png (tuile d'un véhicule éveillé, données récentes, sur le dashboard) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-normal.png (même tuile sur l'interface mobile web) -->

#### Los cuatro estados del mosaico

| Estado | Lo que usted ve |
|---|---|
| **Normal** (vehículo despierto, lectura reciente) | Batería, límite, autonomía, estado de carga, **En alcance**, bloqueo, **Datos de hace** unos minutos; sin línea de error. |
| **Vehículo dormido** | Los **últimos valores leídos** siguen mostrándose (el plugin nunca despierta el vehículo por sí mismo) y la duración **Datos de hace** va creciendo. No se muestra ningún error: es normal. Utilice **Actualizar (con despertar)** o el botón **Despertar** para obtener valores recientes (véase [Actualización de la información](#actualizacion-de-las-informaciones)). |
| **Fuera de alcance** | El indicador muestra **Fuera de alcance**. Los valores son los últimos conocidos; la línea roja de **último error** aparece si el proxy o el vehículo han señalado un problema (véase [Información «Último error» (lectura)](#informacion-ultimo-error-lectura)). |
| **Error o nunca leído** | Un valor ausente, vacío o no numérico se muestra como **Desconocido** (nunca 0 % ni una fecha inventada); la frescura muestra **Ninguna lectura conocida** mientras ninguna lectura haya tenido éxito; la línea roja indica el último error. |

<!-- Capture à ajouter en recette : images/tuile-dashboard-endormi.png (tuile d'un véhicule endormi, valeurs anciennes) -->
<!-- Capture à ajouter en recette : images/tuile-dashboard-hors-portee.png (pastille Hors de portée) -->
<!-- Capture à ajouter en recette : images/tuile-dashboard-erreur.png (ligne d'erreur et valeurs Inconnu) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-endormi.png (tuile d'un véhicule endormi sur l'interface mobile web) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-hors-portee.png (pastille Hors de portée sur l'interface mobile web) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-erreur.png (ligne d'erreur et valeurs Inconnu sur l'interface mobile web) -->

#### Comportamiento de los botones

- Un botón ejecuta **el comando correspondiente** del vehículo, igual que el botón de ese comando en el widget estándar: mismas reglas, mismos mensajes.
- Un botón **atenuado en gris** corresponde a un comando **ausente** del dispositivo o **no compatible** con su proxy (mensaje **No compatible con su versión del proxy**, véase [Error al enviar un comando](#error-al-enviar-un-comando)). **Actualizar** solo aparece en gris si el comando está ausente.
- Durante la ejecución, el botón aparece **atenuado** y deja de responder; vuelve a estar disponible **en cuanto el comando termina**, con éxito o con error, y como máximo transcurridos 4 minutos. En caso de error, Jeedom muestra su mensaje de error habitual.
- El mosaico se **actualiza solo**, sin recargar la página, cuando cambia un valor.
- El mosaico **no añade ninguna confirmación**: una posible confirmación sigue siendo la de Jeedom para el comando (véase [Confirmación de las acciones sensibles](#confirmacion-de-las-acciones-sensibles)).
- En la **aplicación móvil nativa** de Jeedom no se utiliza el mosaico: la aplicación se basa en los [tipos genéricos](#tipos-genericos).

#### Volver al widget estándar

Hágalo si prefiere los widgets de comando de Jeedom.

1. Abra **Complementos > Objetos conectados > Tesla BLE** y haga clic en el vehículo.
2. Haga clic en **Configuración avanzada** (en la parte superior de la página del dispositivo).
3. Desmarque la casilla **Plantilla de widget**.
4. Haga clic en **Guardar** y luego recargue el dashboard.

El vehículo se muestra entonces con el **widget estándar** de Jeedom: un cuadro por cada comando visible, **sin la imagen del modelo** (esta imagen solo la dibuja el mosaico).

#### Restablecer el widget del plugin

1. Abra la **Configuración avanzada** del vehículo, como arriba.
2. **Marque** la casilla **Plantilla de widget**.
3. Haga clic en **Guardar** y luego recargue el dashboard.

El mosaico vuelve; no se modifica ningún comando.

#### Dispositivos existentes tras la actualización

Con la actualización, el mosaico se **activa** en cada dispositivo existente, **salvo** si ya tenía una personalización de visualización: disposición **en tabla**, o widget de comando elegido a mano. Esos dispositivos conservan el widget estándar; marque la casilla **Plantilla de widget** si desea el mosaico. Un dispositivo cuya casilla **Plantilla de widget** ya se había configurado también conserva su elección.

#### Ocultar los comandos individuales sin perder el mosaico

El mosaico lee los comandos del vehículo **aunque estén ocultos**. Para aligerar la visualización bajo el resumen, abra la pestaña **Comandos** y desmarque **Mostrar** en los comandos que ya no quiera ver: el resumen y sus seis botones no cambian.

#### Límites del mosaico

- La duración **Datos de hace** no se «envejece» en el navegador entre dos actualizaciones: sigue el valor de **Antigüedad de los datos (min)**, que el plugin recalcula cada minuto.
- El widget estándar **no** muestra la imagen del modelo.
- Si el mosaico no se puede dibujar, Jeedom muestra en su lugar el **widget estándar** y el plugin lo registra en su log (véase [Mensajes del log del plugin](#mensajes-del-log-del-plugin)).

### Tipos genéricos

Un **tipo genérico** es una etiqueta que Jeedom coloca en un comando (batería, temperatura, apertura, cerradura…) para que la **aplicación móvil**, los **asistentes de voz** y los plugins de terceros sepan lo que representa. El plugin los asigna por usted.

Para verlos o cambiarlos: en el dispositivo, pestaña **Comandos**, haga clic en la **rueda dentada** del comando y localice el campo **Tipo genérico**. Los nombres exactos de los tipos dependen de su versión de Jeedom; la tabla indica también su identificador.

| Comando | Tipo genérico asignado |
|---|---|
| **Carga de la batería** | Batería (`BATTERY`) |
| **Tensión del cargador** | Tensión (`VOLTAGE`) |
| **Energía de carga acumulada** | Consumo (`CONSUMPTION`) |
| **Temperatura interior**, **Temperatura exterior** | Temperatura (`TEMPERATURE`) |
| **Bloqueo del vehículo** | Estado de la cerradura (`LOCK_STATE`) |
| **Puerta delantera del conductor**, **Puerta delantera del pasajero**, **Puerta trasera del conductor**, **Puerta trasera del pasajero**, **Maletero trasero**, **Maletero delantero**, **Puerto de carga (apertura)**, **Cubierta de caja** | Apertura (`OPENING`) |
| **Presión del neumático delantero izquierdo**, **delantero derecho**, **trasero izquierdo**, **trasero derecho** | Presión (`PRESSURE`) |
| **Bloquear las puertas** | Cerradura, cerrar (`LOCK_CLOSE`) |
| **Desbloquear las puertas** | Cerradura, abrir (`LOCK_OPEN`) |
| **Iniciar la carga** | Enchufe, encendido (`ENERGY_ON`) |
| **Detener la carga** | Enchufe, apagado (`ENERGY_OFF`) |

Las informaciones de presión solo existen si su proxy las anuncia (véase [Datos ampliados: qué está disponible](#datos-ampliados-que-esta-disponible)).

> **ATENCIÓN: estos tipos hacen accesibles acciones a las acciones agrupadas de Jeedom.** Si coloca el vehículo en un **objeto** de Jeedom, las **acciones de resumen** del objeto y las acciones de escenario «Tipo genérico» pueden **desbloquear el vehículo** (cerradura: abrir) o **iniciar y detener su carga** (enchufe: encendido y apagado), **sin ninguna confirmación de interfaz**. Si no lo desea, ponga el **Tipo genérico** de esos comandos en **Ninguno**: esa elección se conserva.

Cuándo asigna el plugin un tipo:

- **en la creación** de un comando (dispositivo nuevo, comando añadido por una actualización) ;
- **una sola vez** en los comandos existentes, en la actualización que incorpora los tipos, y **únicamente en un comando cuyo tipo esté vacío**.

Un tipo que usted haya elegido **nunca se sobrescribe**, aunque difiera del del plugin.

**Límite: un tipo vaciado a mano** (**Ninguno**) no se vuelve a asignar al guardar el dispositivo ni con el ciclo de actualización. Solo puede volver a asignarse en dos casos: el comando es **eliminado y recreado** por el plugin (vuelve a empezar con el tipo por defecto), o el plugin **repite** la asignación de los tipos en los comandos existentes, lo cual solo ocurre tras una actualización interrumpida por un error en otro dispositivo. En esos casos, vuelva a poner **Ninguno**.

### Imagen del modelo

El plugin asocia a cada vehículo una **imagen de su modelo**, deducido del **VIN**. Se muestra en el **mosaico** y en la **lista de dispositivos** de Jeedom. Son pictogramas neutros incluidos con el plugin, sin descarga.

| Modelo (decodificado a partir del VIN) | Imagen |
|---|---|
| Model S, Model 3, Model X, Model Y, Cybertruck | Pictograma del modelo |
| Semi, Roadster, modelo desconocido | Ninguna: se sigue mostrando el **icono del plugin** |

Reglas:

- La imagen se asigna **al guardar el dispositivo** (y al actualizar el plugin) si el modelo es conocido y si el vehículo **no tiene una imagen personal**.
- Una **imagen personal** (que usted haya subido) **nunca se toca**.
- **Sustituir** la imagen: abra la **Configuración avanzada** del vehículo y suba la suya. Se conserva.
- **Quitar** la imagen: en la **Configuración avanzada**, utilice **Quitar la imagen**. **Esta eliminación es definitiva**: el plugin nunca vuelve a poner la imagen por sí solo, aunque guarde el dispositivo o actualice el plugin. En su lugar se muestra el icono del plugin.
- **No existe ningún botón** para recuperar la imagen del plugin tras quitarla: para tener una imagen, suba la suya.
- Si el **VIN** cambia a un modelo sin imagen, se quita la imagen asignada por el plugin; una imagen que usted haya elegido se conserva.
- Si Jeedom no puede escribir en su carpeta de imágenes, o si la imagen del plugin es ilegible (reinstale el plugin), el plugin escribe una advertencia en su log y se sigue mostrando el icono del plugin (véase [Mensajes del log del plugin](#mensajes-del-log-del-plugin)).

### Orden de los comandos

Los comandos de un dispositivo nuevo se ordenan **por tema**, en este orden:

1. **Estado**: presencia, bloqueo, vigilia, ocupante, centinela, antigüedad de los datos, último error ;
2. **Carga**: batería, autonomía, estado de carga, límites, potencia, energía, programaciones ;
3. **Clima**: temperaturas, climatización, calefacciones, desempañado ;
4. **Aperturas**: puertas, maleteros, puerto de carga, alertas ;
5. **Vehículo**: modelo, kilometraje, conducción, posición, neumáticos, actualización de software ;
6. **Supervisión del proxy**: proxy accesible, versión, rol de la llave, duraciones de lectura ;
7. **Acciones**: lectura (actualizar, despertar), carga, clima, acceso (puertas, maleteros, centinela, luces, claxon).

Reglas:

- El orden se asigna **únicamente en la creación de cada comando**. **Nunca se reescribe**: una actualización del plugin **no mueve ningún comando existente**.
- Un comando **añadido más tarde** (por una actualización) se coloca **junto a un comando de su tema**; en caso de empate de posición, Jeedom los desempata por nombre. Si **no existe ningún** comando de ese tema en el dispositivo, se añade **en bloque al final de la lista**.
- Para **reorganizar**: abra la pestaña **Comandos** del dispositivo, **arrastre y suelte** las filas en el orden deseado y luego haga clic en **Guardar**. Su orden se conserva.
- El orden de la pestaña **Comandos** es también el de la visualización bajo el mosaico o en el widget estándar.

## Comandos

Las tablas siguientes indican, para cada comando, su **identificador** (`logicalId`, estable: es el que encuentran los escenarios), su tipo y su subtipo, y su unidad. Los nombres son los de un **dispositivo nuevo**; un dispositivo migrado desde la 0.x conserva sus nombres anteriores (véase [Actualización desde la versión 0.x](#actualizacion-desde-la-version-0x)).

### Carga avanzada: qué está disponible

Resumen de lo que añade la carga avanzada. Las informaciones se crean **ocultas** (muéstrelas desde la pestaña **Comandos**); el detalle de cada una está en las tablas [Informaciones](#informaciones) y [Acciones](#acciones).

| Nombre | Identificador | Unidad | Función | Detalle |
|---|---|---|---|---|
| Límite de carga mínimo | `charge_limit_soc_min` | % | Límite más bajo aceptado por el vehículo; ajusta el **Mín** del control deslizante **Límite de carga** | [Límites seguidos del vehículo](#ejecucion-de-los-comandos) |
| Límite de carga máximo | `charge_limit_soc_max` | % | Límite más alto aceptado; ajusta el **Máx** del mismo control deslizante | [Límites seguidos del vehículo](#ejecucion-de-los-comandos) |
| Corriente de carga máxima | `charge_current_request_max` | A | Corriente máxima anunciada por el vehículo; ajusta el **Máx** del control deslizante **Corriente de carga** | [Límites seguidos del vehículo](#ejecucion-de-los-comandos) |
| Estado de carga (traducido) | `charging_state_label` | | Estado de carga en el idioma de Jeedom, para la visualización | [Informaciones](#informaciones) |
| Autonomía nominal | `battery_range` | km | Autonomía nominal | [Informaciones](#informaciones) |
| Autonomía estimada | `est_battery_range` | km | Autonomía según su conducción reciente | [Informaciones](#informaciones) |
| Nivel de batería (bruto) | `battery_level` | % | Nivel de batería tal como lo comunica el vehículo | [Informaciones](#informaciones) |
| Potencia de carga | `charger_power` | kW | Potencia entregada al vehículo | [Informaciones](#informaciones) |
| Corriente de carga real | `charger_actual_current` | A | Corriente realmente entregada | [Informaciones](#informaciones) |
| Fases de carga | `charger_phases` | | Número de fases utilizadas | [Informaciones](#informaciones) |
| Energía añadida | `charge_energy_added` | kWh | Energía añadida durante la sesión en curso (o la última) | [Informaciones](#informaciones) |
| Cable de carga | `conn_charge_cable` | | Tipo de cable conectado | [Informaciones](#informaciones) |
| Carga rápida | `fast_charger_present` | | 1 si está conectado a un punto de carga rápida | [Informaciones](#informaciones) |
| Energía de carga acumulada | `charge_energy_total` | kWh | Índice que solo crece, para el seguimiento de energía | [Contadores de energía de carga](#contadores-de-energia-de-carga) |
| Hora de carga programada | `scheduled_charging_start_time` | | Hora de inicio de la carga diferida (`HH:MM`) | [Programaciones leídas en el vehículo](#informaciones) |
| Fin de las horas valle | `off_peak_hours_end_time` | | Fin de las horas valle del vehículo (`HH:MM`) | [Programaciones leídas en el vehículo](#informaciones) |
| Preacondicionamiento planificado | `scheduled_preconditioning_time` | | Hora de salida prevista por el preacondicionamiento (`HH:MM`) | [Programaciones leídas en el vehículo](#informaciones) |
| Ajustar según el excedente | `adjust_surplus` | W | Acción: recibe la potencia disponible y decide si envía o no un comando | [Control según el excedente](#control-segun-el-excedente) |
| Añadir una programación de carga | `add_charge_schedule` | | Acción: crea o sustituye la programación gestionada por Jeedom (proxy del fork) | [Programar la carga](#programar-la-carga) |
| Eliminar la programación de carga | `remove_charge_schedule` | | Acción: elimina esa programación (proxy del fork) | [Programar la carga](#programar-la-carga) |

Las acciones de la carga avanzada también están ocultas. Dos funciones se configuran en el dispositivo en lugar de mediante un comando:

| Ajustes del dispositivo | Función | Detalle |
|---|---|---|
| **Tensión de la red**, **Fases**, **Paso de ajuste**, **Histéresis**, **Intervalo mínimo entre comandos**, **Corriente mínima de arranque**, **Umbral de parada**, **Duración de mantenimiento antes de la parada** | Control según el excedente (valores por defecto: 230 V, monofásico, 1 A, 2 A, 120 s, 6 A, 5 A, 300 s) | [Configuración de los dispositivos](#configuracion-de-los-dispositivos) y [Control según el excedente](#control-segun-el-excedente) |
| **Control de la carga**, **Inicio del intervalo**, **Fin del intervalo**, **SoC objetivo (%)**, **Detener al final del intervalo** | Carga en horas valle (desactivada por defecto) | [Carga en horas valle](#carga-en-horas-valle) |

### Clima y confort: qué está disponible

Resumen de lo que permiten la climatización y el confort. El proxy oficial 2.3.0 lo lee todo, pero no sabe ajustar la consigna de temperatura, los asientos, el volante, el desempañado máximo ni el mantenimiento de clima: esos comandos exigen el **proxy del fork** (versiones `2.3.0-tb.N`) y se crean **ocultos**. Se **supone** que el rol de llave **Owner** es necesario para las acciones (no confirmado en uso real: «por confirmar»).

| Función | Identificador | Disponibilidad | Rol de llave | Efecto en el vehículo | Detalle |
|---|---|---|---|---|---|
| Informaciones de climatización (de **Climatización automática** a **Calefacción de la batería**, incluido **Mantenimiento de clima (perro, camping)**) | `is_auto_conditioning_on`… `battery_heater` | Proxy oficial 2.3.0 | Charging Manager basta (lectura) | Solo lectura, sin despertar: conservan su último valor mientras el vehículo duerme. Se crean ocultas | [Informaciones](#informaciones) |
| Consigna del conductor, Consigna del pasajero | `set_driver_temp`, `set_passenger_temp` | Proxy del fork, `2.3.0-tb.1` como mínimo | Owner supuesto | Ajusta la temperatura solicitada; ambos lados se envían a la vez; el proxy despierta el vehículo | [Ajustar la consigna de temperatura](#ajustar-la-consigna-de-temperatura) |
| Calefacción de los cinco asientos, calefacción del volante | `set_seat_heater_left`, `set_seat_heater_right`, `set_seat_heater_rear_left`, `set_seat_heater_rear_right`, `set_seat_heater_rear_center`, `set_steering_wheel_heater` | Proxy del fork, `2.3.0-tb.2` como mínimo | Owner supuesto | Calienta el asiento o el volante; en principio requiere la climatización en marcha; el proxy despierta el vehículo | [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante) |
| Desempañado máximo | `set_preconditioning_max` | Proxy del fork, `2.3.0-tb.1` como mínimo | Owner supuesto | **Despierta** el vehículo y **consume batería** mientras funciona; no se detiene solo | [Desempañado máximo](#desempanado-maximo) |
| Modo de mantenimiento de clima (mantenimiento, perro, camping) | `set_climate_keeper_mode` | Proxy del fork, `2.3.0-tb.1` como mínimo | Owner supuesto | **Despierta** el vehículo y **consume batería durante mucho tiempo**; no se detiene solo | [Modo perro, camping y mantenimiento de clima](#modo-perro-modo-camping-y-mantenimiento-de-clima) |
| Iniciar la climatización, Detener la climatización | `auto_conditioning_start`, `auto_conditioning_stop` | Proxy oficial 2.3.0 | Owner supuesto (rechazo probable con Charging Manager) | Inicia o detiene el preacondicionamiento; el inicio despierta el vehículo y consume batería | [Acciones](#acciones) |
| Preacondicionamiento planificado por Jeedom (ajuste del dispositivo) | Ninguno: sección **Preacondicionamiento planificado por Jeedom** | Proxy oficial 2.3.0 | Owner supuesto (un solo intento por salida con Charging Manager) | Jeedom inicia la climatización antes de la hora de salida y luego la detiene; el inicio despierta el vehículo y consume batería | [Preacondicionamiento planificado por Jeedom](#preacondicionamiento-planificado-por-jeedom) |

> ⚠️ **Batería.** El desempañado máximo, el mantenimiento de clima y la climatización iniciada con antelación **despiertan el vehículo** y **gastan su batería**. No se indica aquí ningún consumo cifrado por falta de una medición fiable. El **modo perro** no sustituye a una vigilancia de la temperatura del habitáculo para un animal.

**Por qué algunos comandos se rechazan u ocultan.** El proxy oficial 2.3.0 no tiene los comandos de consigna, de asientos, de volante, de desempañado máximo ni de mantenimiento de clima: el fork los añade y los **anuncia** mediante su ruta `capabilities`. Mientras el proxy no anuncie el comando, el plugin lo rechaza al instante con **«No compatible con su versión del proxy»**, sin enviar nada al vehículo. Estos comandos se crean **ocultos**, también tras pasar al fork: marque **Mostrar** en la pestaña **Comandos**, o llámelos desde un escenario. Tras pasar al fork, **no es necesario reinstalar el plugin**: la disponibilidad se vuelve a leer cuando cambia la versión del proxy. Si después el vehículo rechaza el comando por falta de permisos, hace falta una llave **Owner**: véase [Rol de la llave](#rol-de-la-llave) y el procedimiento de emparejamiento [Generar la llave y emparejarla con el vehículo](installation-proxy.md#8-generar-la-llave-y-emparejarla-con-el-vehiculo). Los síntomas sin mensaje se describen en [Clima y confort: síntomas sin mensaje](#clima-y-confort-sintomas-sin-mensaje).

### Aperturas y seguridad: qué está disponible

Resumen de las aperturas, la presencia, el bloqueo, el modo Centinela y las alertas. Las lecturas funcionan con el **proxy oficial 2.3.0** y una llave **Charging Manager**. Los comandos de apertura de los maleteros exigen el **proxy del fork** (versiones `2.3.0-tb.N`) y se crean **ocultos**. El rol de llave **Owner** es necesario para bloquear, desbloquear y controlar el modo Centinela, y se **supone** necesario para los maleteros (no confirmado en uso real: «por confirmar»).

| Función | Identificador | Disponibilidad | Rol de llave | Confirmación solicitada | Detalle |
|---|---|---|---|---|---|
| Las ocho aperturas (cuatro puertas, **Maletero trasero**, **Maletero delantero**, **Puerto de carga (apertura)**, **Cubierta de caja**) | `door_front_driver`, `door_front_passenger`, `door_rear_driver`, `door_rear_passenger`, `trunk_rear`, `trunk_front`, `charge_port_closure`, `tonneau` | Proxy oficial 2.3.0 | Charging Manager basta (lectura) | No aplica | [Informaciones](#informaciones) |
| **Ocupante presente** | `user_present` | Proxy oficial 2.3.0 | Charging Manager basta (lectura) | No aplica | [Informaciones](#informaciones) |
| **Bloqueo del vehículo**, **Estado de bloqueo detallado** | `vehicule_lock`, `lock_state` | Proxy oficial 2.3.0 | Charging Manager basta (lectura) | No aplica | [Informaciones](#informaciones) |
| **Centinela**, **Origen del modo Centinela** | `sentry_mode`, `sentry_mode_source` | Proxy oficial 2.3.0: valor de la **última orden**. Proxy del fork `2.3.0-tb.2` como mínimo: valor **real** (vehículo despierto) | Charging Manager basta (lectura) | No aplica | [Estado del modo Centinela](#estado-del-modo-centinela) |
| **Alerta de aperturas**, **Alerta de vehículo desbloqueado sin ocupante** y los ajustes **Alertas de apertura prolongada** | `closures_alert`, `unlocked_alert` | Proxy oficial 2.3.0 (ajustes en el dispositivo, alertas desactivadas por defecto) | Charging Manager basta (lectura) | No aplica | [Alertas de apertura prolongada](#alertas-de-apertura-prolongada) |
| Bloquear las puertas, Desbloquear las puertas | `door_lock`, `door_unlock` | Proxy oficial 2.3.0 | **Owner** (rechazado con Charging Manager) | Desbloquear: **sí** | [Acciones](#acciones) |
| Abrir el puerto de carga, Cerrar el puerto de carga | `charge_port_door_open`, `charge_port_door_close` | Proxy oficial 2.3.0 | No confirmado (véase [Rol de la llave](#rol-de-la-llave)) | Abrir: **sí** | [Acciones](#acciones) |
| Modo Centinela | `set_sentry_mode` | Proxy oficial 2.3.0 | **Owner** (rechazado con Charging Manager) | **Sí** | [Estado del modo Centinela](#estado-del-modo-centinela) |
| Abrir el maletero trasero, Abrir el maletero delantero | `open_trunk_rear`, `open_trunk_front` | Proxy del fork, `2.3.0-tb.2` como mínimo | Owner supuesto | **Sí** | [Abrir el maletero trasero y el maletero delantero](#abrir-el-maletero-trasero-y-el-maletero-delantero) |

Las acciones que piden una confirmación se describen en [Confirmación de las acciones sensibles](#confirmacion-de-las-acciones-sensibles). La diferencia **Real** / **Última orden** del modo Centinela se explica en [Estado del modo Centinela](#estado-del-modo-centinela): pruebe **Origen del modo Centinela** antes de fiarse de **Centinela**.

> **IMPORTANTE: red de confianza.** El proxy no tiene **ni autenticación ni cifrado (TLS)** por defecto; el fork puede exigir un token de API, opcional. Con una llave Owner, cualquier equipo de su red local puede desbloquear el vehículo o abrir un maletero sin pasar por Jeedom, y la confirmación de Jeedom no lo impide. Mantenga el proxy en una red de confianza, idealmente aislada, y **nunca** exponga su puerto a Internet (véase [Rol de la llave](#rol-de-la-llave)).

**Por qué los comandos de maletero se rechazan u ocultan.** El proxy oficial 2.3.0 no tiene el comando que acciona un maletero: el fork lo añade y lo **anuncia** mediante su ruta `capabilities`. Mientras el proxy no lo anuncie, el plugin rechaza **Abrir el maletero trasero** y **Abrir el maletero delantero** al instante con **«No compatible con su versión del proxy»**, sin enviar nada al vehículo. Para activarlos: instale o actualice el proxy del fork (`2.3.0-tb.2` como mínimo), sin reinstalar el plugin ni recrear el dispositivo (la disponibilidad se vuelve a leer cuando cambia la versión del proxy). Los dos comandos se crean **ocultos**, también tras pasar al fork: marque **Mostrar** en la pestaña **Comandos**, o llámelos desde un escenario. Si después el vehículo lo rechaza por falta de permisos, hace falta una llave **Owner**. Los síntomas sin mensaje se describen en [Aperturas y seguridad: síntomas sin mensaje](#aperturas-y-seguridad-sintomas-sin-mensaje).

### Datos ampliados: qué está disponible

Resumen de las informaciones del apartado «datos ampliados»: modelo, kilometraje y conducción, presión de los neumáticos, actualización de software y posición. El detalle de cada información (nombre, identificador, visibilidad, historización) está en la tabla [Informaciones](#informaciones). Todas son **solo lectura**, sin despertar el vehículo.

| Dato | Identificadores | Unidad | Requisito del proxy | Frecuencia de lectura |
|---|---|---|---|---|
| Modelo y año | `model`, `model_year` | | **Ninguno**: decodificados a partir del VIN, sin consultar al proxy | Al guardar el dispositivo, al actualizar el plugin y al iniciar Jeedom |
| Kilometraje y conducción | `odometer`, `shift_state`, `speed`, `power` | km, km/h, kW | El proxy debe **anunciar** `drive_state` | En cada lectura de los datos (vehículo despierto) |
| Presión de los neumáticos | `tpms_pressure_fl`, `_fr`, `_rl`, `_rr` | bar | El proxy debe **anunciar** `tire_pressure` | Como máximo cada **15 minutos**, vehículo despierto |
| Actualización de software | `software_update_status`, `software_update_version`, `software_update_progress` | % (progreso) | El proxy debe **anunciar** `software_update` | Como máximo cada **15 minutos**, vehículo despierto |
| Posición | `latitude`, `longitude`, `at_home` | ° | El proxy debe **anunciar** `location_data` | Como máximo cada **15 minutos**, vehículo despierto |

**¿Qué proxy?** Un proxy «anuncia» un dato cuando su ruta `capabilities` lo enumera (`http://<ip_del_proxy>:<puerto>/api/proxy/1/capabilities`, véase [Rol de la llave](#rol-de-la-llave)). El **proxy del fork** `2.3.0-tb.2` como mínimo anuncia estas cuatro categorías; el **proxy oficial 2.3.0 no las ofrece**. En cuanto al kilometraje, la función está integrada en el proyecto de wimaha pero sin versión publicada en la fecha de esta documentación: solo se leerá con una versión que lo **anuncie**. El plugin nunca se fía de un número de versión, solo de ese anuncio: compruebe **Versión del proxy** y, si es necesario, la dirección anterior.

**Por qué falta un dato ampliado.** En un proxy que no anuncia una categoría, las informaciones correspondientes **no se crean**: no aparecen en la pestaña **Comandos** (no existe ningún valor «No compatible» que se muestre). Solo **Modelo** y **Año del modelo** están siempre presentes. Para obtenerlas:

1. Compruebe **Versión del proxy** del dispositivo y luego instale o actualice el **proxy del fork** (véase [Comprobar y actualizar la versión del proxy](#comprobar-y-actualizar-la-version-del-proxy)).
2. Espere al siguiente ciclo de actualización (un minuto como máximo): en la **redetección**, cuando cambia la versión del proxy, el plugin vuelve a leer lo que anuncia el proxy y **crea por sí solo** las informaciones que han pasado a estar disponibles. No hace falta reinstalar el plugin ni recrear el dispositivo. Un **Guardar** en el dispositivo también hace que se creen las informaciones que faltan si el proxy las anuncia.
3. Compruebe que se rellenan: permanecen vacías hasta la primera lectura, con el **vehículo despierto** (lance **Actualizar (con despertar)** para provocarla). Las presiones, la actualización y la posición esperan además a que hayan transcurrido 15 minutos desde el intento anterior.

Si un proxy **anuncia** una categoría pero el vehículo o el proxy la **rechazan** (**«Función no compatible con este proxy — …»**), el plugin deja de solicitarla hasta el próximo cambio de versión del proxy: véase [Datos ampliados: síntomas sin mensaje](#datos-ampliados-sintomas-sin-mensaje).

**Valores y unidades.**

- **Kilometraje**: convertido de millas a kilómetros, con una décima. Un contador nulo o aberrante se ignora. Historizado por defecto.
- **Marcha**: `P`, `R`, `N` o `D`. **Vacío** significa «no comunicado»: el plugin escribe entonces una cadena vacía, de modo que una prueba `== "D"` no sigue siendo verdadera tras la parada.
- **Velocidad** y **Potencia**: el plugin supone una velocidad en mph (convertida a km/h) y una potencia en kW, admitiéndose negativa. Estas dos unidades no están confirmadas por una documentación del vehículo: compare con la pantalla de su vehículo antes de utilizarlas. Se crean ocultas, porque al estar el proxy en el garaje, casi nunca valen otra cosa que 0 o la potencia de carga.
- **Presión de los neumáticos**: en **bar**, sin conversión. Un valor nulo, negativo o superior a 10 bar se ignora (la información conserva su último valor o queda vacía). Los neumáticos solo se leen con el vehículo despierto: los últimos valores siguen mostrándose cuando duerme.
- **Actualización**: cuatro etiquetas, **Ninguna**, **Disponible** (también una instalación programada), **Descarga en curso** (también en espera de Wi-Fi) e **Instalación en curso**. **Versión propuesta** vale **Ninguna** fuera de una actualización, y **Desconocida** cuando hay una actualización activa sin versión comunicada. **Progreso** vale 0 fuera de la descarga y la instalación. Estas etiquetas siguen el idioma de Jeedom: en un escenario, pruebe preferentemente **Progreso** o compare en el idioma actual.
- **Modelo** y **Año del modelo**: decodificados a partir del VIN (modelo: 4.º carácter; año: 10.º carácter, de 2008 a 2037). Un VIN vacío, que no sea de Tesla o que no se pueda decodificar da **Desconocido**. Son **visibles** y **no historizados**.
- **Posición**: véase [Posición y privacidad](#posicion-y-privacidad).

Los datos ampliados se leen junto con los datos de carga: por tanto siguen la **ventana de sueño** (ninguna lectura durante la ventana, véase [Dejar que el vehículo se duerma](#dejar-que-el-vehiculo-se-duerma)) y conservan su último valor mientras el vehículo duerme. El rechazo de una sola categoría no impide las demás lecturas, y nunca modifica **Último error** para las presiones, la actualización y la posición.

### Informaciones

«H»: historizada por defecto. «V»: visible por defecto en el widget. Puede cambiar estos dos ajustes en la pestaña **Comandos**.

| Nombre | Identificador | Tipo / subtipo | Unidad | H | V | Descripción |
|---|---|---|---|---|---|---|
| Presencia del vehículo | `isPresent` | info / binario | | sí | sí | 1 si el proxy alcanza el vehículo por Bluetooth, 0 si está fuera de alcance |
| Vehículo despierto | `vehicule_isAwake` | info / binario | | sí | sí | 1 si el vehículo está despierto, 0 si duerme o si se desconoce su estado de reposo |
| Bloqueo del vehículo | `vehicule_lock` | info / binario | | sí | sí | 1 si el vehículo está bloqueado, incluso desde el interior, 0 si está desbloqueado, aunque sea parcialmente |
| Puerta delantera del conductor | `door_front_driver` | info / binario | | sí | sí | 1 si la puerta está abierta, incluso entreabierta, abriéndose o cerrándose, 0 si está cerrada |
| Puerta delantera del pasajero | `door_front_passenger` | info / binario | | sí | sí | Misma regla que la puerta delantera del conductor |
| Puerta trasera del conductor | `door_rear_driver` | info / binario | | sí | sí | Misma regla que la puerta delantera del conductor |
| Puerta trasera del pasajero | `door_rear_passenger` | info / binario | | sí | sí | Misma regla que la puerta delantera del conductor |
| Maletero trasero | `trunk_rear` | info / binario | | sí | sí | 1 si el maletero está abierto (incluso entreabierto o en movimiento), 0 si está cerrado |
| Maletero delantero | `trunk_front` | info / binario | | sí | sí | 1 si el maletero delantero está abierto (incluso entreabierto o en movimiento), 0 si está cerrado |
| Puerto de carga (apertura) | `charge_port_closure` | info / binario | | sí | sí | 1 si el puerto de carga está abierto (incluso entreabierto o en movimiento), 0 si está cerrado. Se lee incluso con el vehículo dormido, a diferencia de **Puerto de carga abierto** |
| Cubierta de caja | `tonneau` | info / binario | | sí | sí | 1 si la cubierta de caja (Cybertruck) está abierta, 0 si está cerrada; 0 también en un vehículo que no la tiene |
| Ocupante presente | `user_present` | info / binario | | sí | sí | 1 si el vehículo detecta a una persona a bordo, 0 en caso contrario; estado desconocido = último valor |
| Estado de bloqueo detallado | `lock_state` | info / texto | | no | sí | Etiqueta del bloqueo: **Desbloqueado**, **Bloqueado**, **Bloqueado desde el interior** o **Desbloqueo selectivo**; un valor desconocido se muestra tal cual. Sigue el idioma de Jeedom: en un escenario, pruebe **Bloqueo del vehículo** y **Ocupante presente**, ya que una etiqueta comparada depende del idioma |
| Centinela | `sentry_mode` | info / texto | | no | sí | **Activada**, **Desactivada** o **Desconocido** (ninguna lectura ni orden conocidas). Véase [Estado del modo Centinela](#estado-del-modo-centinela). Sigue el idioma de Jeedom: en un escenario, compare en el idioma actual de Jeedom y pruebe **Origen del modo Centinela** para saber de dónde procede el valor |
| Origen del modo Centinela | `sentry_mode_source` | info / texto | | no | sí | **Real** (leída en el vehículo), **Última orden** (deducida del último comando correcto del plugin) o **Ninguna** (todavía no se ha leído ni ordenado nada). Misma regla de idioma que **Centinela** |
| Alerta de aperturas | `closures_alert` | info / binario | | sí | no | 1 mientras una apertura haya permanecido abierta más tiempo que la duración configurada (solo con la alerta activada), 0 en caso contrario. Véase [Alertas de apertura prolongada](#alertas-de-apertura-prolongada). |
| Alerta de vehículo desbloqueado sin ocupante | `unlocked_alert` | info / binario | | sí | no | 1 mientras el vehículo haya permanecido desbloqueado sin ocupante más tiempo que la duración configurada (solo con la alerta activada), 0 en caso contrario. Véase [Alertas de apertura prolongada](#alertas-de-apertura-prolongada). |
| Estado de la carga | `charging_state` | info / texto | | no | sí | Estado de la carga devuelto por el vehículo, sin traducción: `Charging`, `Disconnected`, `Complete`, `Stopped`, `Starting`, `NoPower`, `Calibrating` o `Unknown`. Este es el valor que debe probarse en un escenario |
| Estado de carga (traducido) | `charging_state_label` | info / texto | | no | no | El estado de carga en el idioma de Jeedom (**Cargando**, **Desconectado**, **Finalizada**, **Detenida**, **Inicio**, **Sin corriente**, **Calibración**, **Desconocido**), para la visualización. Un estado que el plugin no conoce se muestra tal como lo envía el vehículo. Sigue el idioma de Jeedom: en un escenario, pruebe **Estado de la carga**, nunca esta etiqueta |
| Límite carga | `charge_limit_soc` | info / numérico | % | sí | sí | Límite de carga configurado |
| Límite de carga mínimo | `charge_limit_soc_min` | info / numérico | % | no | no | Límite de carga más bajo que acepta el vehículo (sirve de **Min** al deslizador **Límite de carga**) |
| Límite de carga máximo | `charge_limit_soc_max` | info / numérico | % | no | no | Límite de carga más alto que acepta el vehículo (sirve de **Max** al deslizador **Límite de carga**) |
| Carga de la batería | `usable_battery_level` | info / numérico | % | sí | sí | Nivel de batería utilizable |
| Nivel de batería (bruto) | `battery_level` | info / numérico | % | no | no | Nivel de batería tal como lo informa el vehículo, de 0 a 100 %. Puede diferir en algunos puntos de **Carga de la batería** (nivel utilizable) |
| Autonomía | `ideal_battery_range` | info / numérico | km | sí | no | Autonomía llamada ideal, convertida a kilómetros (el vehículo la devuelve en millas) |
| Autonomía nominal | `battery_range` | info / numérico | km | no | no | Autonomía nominal, convertida a kilómetros. Suele ser idéntica a la autonomía llamada ideal |
| Autonomía estimada | `est_battery_range` | info / numérico | km | no | no | Autonomía estimada según su conducción reciente, convertida a kilómetros |
| Tensión del cargador | `charger_voltage` | info / numérico | V | no | no | Tensión suministrada por el punto de carga |
| Velocidad de carga | `charge_rate` | info / numérico | km/h | no | no | Autonomía recuperada por hora de carga, convertida a km/h (el vehículo la devuelve en millas por hora) |
| Potencia de carga | `charger_power` | info / numérico | kW | no | no | Potencia suministrada al vehículo, en kilovatios (el vehículo la devuelve en general como un valor entero) |
| Corriente de carga real | `charger_actual_current` | info / numérico | A | no | no | Corriente realmente suministrada, que no debe confundirse con la corriente configurada (**Corriente de carga (A)**) |
| Fases de carga | `charger_phases` | info / numérico | | no | no | Número de fases utilizadas por la carga; en general 0 cuando el vehículo no carga |
| Energía añadida | `charge_energy_added` | info / numérico | kWh | no | no | Energía añadida a la batería durante la sesión de carga en curso (o la última); el vehículo la pone a cero en cada nueva sesión, un valor negativo se ignora |
| Energía de carga acumulada | `charge_energy_total` | info / numérico | kWh | sí | no | Contador que solo crece: suma de las energías de sesión, calculada por el plugin (véase [Contadores de energía de carga](#contadores-de-energia-de-carga)) |
| Corriente de carga (A) | `charge_amps` | info / numérico | A | sí | sí | Corriente de carga configurada |
| Corriente solicitada de carga | `charge_current_request` | info / numérico | A | sí | sí | Corriente solicitada por el vehículo |
| Corriente de carga máxima | `charge_current_request_max` | info / numérico | A | no | no | Corriente máxima que el vehículo anuncia poder solicitar al punto de carga (sirve de **Max** al deslizador **Corriente de carga**) |
| Tiempo de carga | `minutes_to_full_charge` | info / texto | | no | sí | Tiempo restante hasta el final de la carga, en formato `HHhMM` |
| Tiempo de carga restante | `charge_minutes_remaining` | info / numérico | min | no | no | El mismo tiempo restante, en minutos (utilizable en un escenario o en un gráfico) |
| Puerto de carga abierto | `charge_port_door_state` | info / binario | | no | no | 1 si el puerto de carga está abierto, 0 si está cerrado |
| Bloqueo del puerto de carga | `charge_port_latch` | info / texto | | no | no | Estado del cierre del cable de carga, tal como lo devuelve el vehículo |
| Cable de carga | `conn_charge_cable` | info / texto | | no | no | Tipo de cable conectado, tal como lo devuelve el vehículo, por ejemplo `IEC` (Tipo 2, Europa), `SAE` (Norteamérica), `GB_AC` o `GB_DC` (China); `SNA` cuando no se detecta ningún cable |
| Carga rápida | `fast_charger_present` | info / binario | | no | no | 1 si el vehículo está conectado a un punto de carga rápida |
| Modo de carga programada | `scheduled_charging_mode` | info / texto | | no | no | Modo de carga programada, tal como lo devuelve el vehículo: `ScheduledChargingModeOff` (ninguna programación), `ScheduledChargingModeStartAt` (carga diferida) o `ScheduledChargingModeDepartBy` (salida programada) |
| Hora de salida programada | `scheduled_departure_time` | info / texto | | no | no | Hora de salida programada en formato `HH:MM` (hora del vehículo); vacía si no hay ninguna salida programada |
| Hora de carga programada | `scheduled_charging_start_time` | info / texto | | no | no | Hora de inicio de la carga diferida en formato `HH:MM` (hora de Jeedom); vacía fuera del modo de carga diferida. Oculta por defecto |
| Fin de las horas valle | `off_peak_hours_end_time` | info / texto | | no | no | Hora de fin de las horas valle en formato `HH:MM`; informada solo en modo de salida programada, vacía en caso contrario o cuando el vehículo indica medianoche. Oculta por defecto |
| Preacondicionamiento planificado | `scheduled_preconditioning_time` | info / texto | | no | no | Hora de salida objetivo del preacondicionamiento, en formato `HH:MM`; informada en modo de salida programada cuando el preacondicionamiento está activado, vacía en caso contrario. Oculta por defecto |
| Temperatura interior | `inside_temp` | info / numérico | °C | sí | sí | Temperatura en el habitáculo, a la décima de grado |
| Temperatura exterior | `outside_temp` | info / numérico | °C | sí | sí | Temperatura exterior, a la décima de grado |
| Temperatura del conductor | `driver_temp_setting` | info / numérico | °C | no | no | Consigna de climatización del lado del conductor |
| Temperatura del pasajero | `passenger_temp_setting` | info / numérico | °C | no | no | Consigna de climatización del lado del pasajero |
| Climatización activada | `is_climate_on` | info / binario | | no | no | 1 si la climatización está en funcionamiento |
| Calefacción del asiento del conductor | `seat_heater_left` | info / numérico | | no | no | Nivel de calefacción del asiento del conductor (0 a 3) |
| Calefacción del asiento del pasajero | `seat_heater_right` | info / numérico | | no | no | Nivel de calefacción del asiento del pasajero (0 a 3) |
| Calefacción del volante | `steering_wheel_heater` | info / binario | | no | no | 1 si la calefacción del volante está activa |
| Modo desempañado | `defrost_mode` | info / texto | | no | no | Estado del desempañado |
| Climatización automática | `is_auto_conditioning_on` | info / binario | | no | no | 1 si la climatización automática está activa |
| Preacondicionamiento en curso | `is_preconditioning` | info / binario | | no | no | 1 durante un preacondicionamiento del habitáculo o de la batería (no debe confundirse con **Preacondicionamiento planificado**, la hora programada) |
| Desempañado delantero | `is_front_defroster_on` | info / binario | | no | no | 1 si el desempañado del parabrisas está activo |
| Desempañado trasero | `is_rear_defroster_on` | info / binario | | no | no | 1 si el desempañado de la luneta trasera está activo |
| Velocidad de ventilación | `fan_status` | info / numérico | | no | no | Nivel de ventilación, valor bruto del vehículo (escala no documentada por Tesla) |
| Mantenimiento de clima (perro, camping) | `climate_keeper_mode` | info / texto | | no | no | Modo de mantenimiento de clima, tal como lo devuelve el vehículo: `Off`, `On` (mantenimiento), `Dog` (modo perro), `Party` (modo camping), `Unknown` |
| Protección contra sobrecalentamiento | `cabin_overheat_protection` | info / texto | | no | no | Protección contra el sobrecalentamiento del habitáculo, tal como la devuelve el vehículo: `CabinOverheatProtectionOff`, `CabinOverheatProtectionOn`, `CabinOverheatProtectionFanOnly` (solo ventilación) |
| Calefacción del asiento trasero izquierdo | `seat_heater_rear_left` | info / numérico | | no | no | Nivel de calefacción del asiento trasero izquierdo (0 a 3); 0 también si el vehículo no está equipado con él |
| Calefacción del asiento trasero derecho | `seat_heater_rear_right` | info / numérico | | no | no | Nivel de calefacción del asiento trasero derecho (0 a 3); 0 también si el vehículo no está equipado con él |
| Calefacción del asiento trasero central | `seat_heater_rear_center` | info / numérico | | no | no | Nivel de calefacción del asiento trasero central (0 a 3); 0 también si el vehículo no está equipado con él |
| Nivel de calefacción del volante | `steering_wheel_heat_level` | info / numérico | | no | no | Nivel de calefacción del volante: **0 desconocido, 1 apagado, 2 bajo, 3 alto** (véase la advertencia más abajo) |
| Temperatura mín. ajustable | `min_avail_temp` | info / numérico | °C | no | no | Temperatura mínima ajustable en el vehículo, a la décima |
| Temperatura máx. ajustable | `max_avail_temp` | info / numérico | °C | no | no | Temperatura máxima ajustable en el vehículo, a la décima |
| Calefacción de la batería | `battery_heater` | info / binario | | no | no | 1 si la calefacción de la batería está activa |
| Último error | `last_error` | info / texto | | no | sí | Causa del último fallo de lectura o de comando, seguida del motivo del proxy cuando este lo da; **Ninguna** cuando todo va bien. Utilizable en un escenario |
| Última lectura de los datos | `last_data_update` | info / texto | | no | sí | Fecha y hora (hora de Jeedom, `AAAA-MM-DD HH:MM:SS`) de la última lectura correcta de los datos de carga y de climatización |
| Antigüedad de los datos (min) | `data_age` | info / numérico | min | no | sí | Minutos transcurridos desde la **Última lectura de los datos**, recalculados cada minuto sin consultar al proxy. Vale 0 tras cada lectura correcta y aumenta mientras ninguna lectura se complete (vehículo dormido, proxy inaccesible, ventana de sueño). **99999** = ninguna lectura conocida, o más de 69 días |
| Proxy accesible | `proxy_reachable` | info / binario | | no | sí | 1 si el proxy respondió en el último ciclo de actualización, 0 si está apagado, inaccesible, no responde a tiempo o devuelve algo distinto de una respuesta válida del proxy (dirección errónea, proxy demasiado antiguo). Un vehículo fuera de alcance o dormido no lo pone a 0. Utilizable en un escenario |
| Versión del proxy | `proxy_version` | info / texto | | no | sí | Versión devuelta por el proxy en el último ciclo (**desconocida** si es ilegible); conserva su último valor cuando el proxy no responde |
| Rol de la llave | `key_role` | info / texto | | no | sí | Rol probable de la llave del proxy para este vehículo: **Charging Manager** tras el rechazo de un comando reservado al rol Owner por falta de derechos, **Owner** en cuanto uno de esos comandos se completa, **Indeterminado** mientras no se haya enviado ninguno (véase [Rol de la llave](#rol-de-la-llave)). En un escenario, pruebe `Owner` o `Charging Manager` (nunca se traducen); «Indeterminado» sigue el idioma de Jeedom |
| Duración de la lectura del estado | `state_read_duration` | info / numérico | s | no | sí | Tiempo, en segundos con décimas, de la última lectura correcta del estado del vehículo (presencia, bloqueo, reposo) en el ciclo de actualización o mediante **Actualizar**. Un fallo no lo modifica: conserva la duración del último éxito. Historícela para seguir la salud del enlace Bluetooth (véase [Lectura lenta del proxy](#lectura-lenta-del-proxy)) |
| Duración de la lectura de los datos | `data_read_duration` | info / numérico | s | no | sí | Tiempo de la última lectura correcta de los datos de carga y de climatización. Sin cambios mientras el vehículo duerme (ninguna lectura). Un valor cercano a 0 es normal justo después de otra lectura: el proxy conserva estos datos en memoria 30 segundos |
| Modelo | `model` | info / texto | | no | sí | Modelo decodificado del VIN, sin consultar al proxy: **Model S**, **Model X**, **Model 3**, **Model Y**, **Cybertruck**, **Semi** o **Roadster**; **Desconocido** si el VIN no es el de un Tesla reconocido. Véase [Datos ampliados: qué está disponible](#datos-ampliados-que-esta-disponible) |
| Año del modelo | `model_year` | info / texto | | no | sí | Año del modelo decodificado del VIN (por ejemplo `2023`); **Desconocido** si no se puede decodificar |
| Kilometraje | `odometer` | info / numérico | km | sí | sí | Cuentakilómetros, convertido a kilómetros (el vehículo lo devuelve en millas). Se crea solo si el proxy anuncia `drive_state` |
| Marcha | `shift_state` | info / texto | | no | no | Marcha engranada: `P`, `R`, `N` o `D`; **vacía** cuando el vehículo no la comunica. Se crea solo si el proxy anuncia `drive_state` |
| Velocidad | `speed` | info / numérico | km/h | no | no | Velocidad, supuesta en mph en el vehículo y convertida a km/h (por confirmar en uso real). Se crea solo si el proxy anuncia `drive_state` |
| Potencia | `power` | info / numérico | kW | no | no | Potencia instantánea, valor del vehículo en kilovatios, se admite negativa (por confirmar en uso real). Se crea solo si el proxy anuncia `drive_state` |
| Presión del neumático delantero izquierdo | `tpms_pressure_fl` | info / numérico | bar | no | sí | Presión del neumático, en bar, sin conversión. Se crea solo si el proxy anuncia `tire_pressure` |
| Presión del neumático delantero derecho | `tpms_pressure_fr` | info / numérico | bar | no | sí | Ídem, neumático delantero derecho |
| Presión del neumático trasero izquierdo | `tpms_pressure_rl` | info / numérico | bar | no | sí | Ídem, neumático trasero izquierdo |
| Presión del neumático trasero derecho | `tpms_pressure_rr` | info / numérico | bar | no | sí | Ídem, neumático trasero derecho |
| Actualización | `software_update_status` | info / texto | | no | sí | **Ninguna**, **Disponible**, **Descarga en curso** o **Instalación en curso** (un estado inesperado del proxy se muestra tal cual). Se crea solo si el proxy anuncia `software_update` |
| Versión propuesta | `software_update_version` | info / texto | | no | sí | Versión de la actualización propuesta; **Ninguna** fuera de una actualización, **Desconocida** si hay una actualización activa sin versión informada |
| Progreso | `software_update_progress` | info / numérico | % | no | no | Avance de la descarga o de la instalación; 0 fuera de estas dos fases |
| Latitud | `latitude` | info / numérico | ° | no | no | Latitud del vehículo en grados decimales. **Oculta y no historizada**: dato personal (véase [Posición y privacidad](#posicion-y-privacidad)). Se crea solo si el proxy anuncia `location_data` |
| Longitud | `longitude` | info / numérico | ° | no | no | Longitud del vehículo, mismas reglas que la latitud |
| En casa | `at_home` | info / binario | | no | sí | 1 si el vehículo está dentro del radio del domicilio, 0 fuera de él; **nunca se escribe** mientras se desconozcan el domicilio o la posición |

La información **Carga de la batería** alimenta también el seguimiento de batería de Jeedom (página **Análisis > Dispositivos**); **Nivel de batería (bruto)** no la alimenta.

Cada información de carga y de climatización se actualiza de forma independiente: si el vehículo no devuelve una de ellas, conserva su último valor y las demás se actualizan igualmente.

**Informaciones de carga ampliadas.** Las diez informaciones de carga adicionales (**Estado de carga (traducido)**, **Autonomía nominal**, **Autonomía estimada**, **Nivel de batería (bruto)**, **Potencia de carga**, **Corriente de carga real**, **Fases de carga**, **Energía añadida**, **Cable de carga** y **Carga rápida**) se crean **ocultas**, incluso en un dispositivo existente durante la actualización: muestre las que le interesen desde la pestaña **Comandos**, su elección de visualización y de historización nunca se sobrescribe. Permanecen vacías hasta la primera lectura de los datos de un vehículo despierto y después conservan su último valor mientras duerme (véase **Antigüedad de los datos (min)**): al final de una carga, la potencia y la corriente real pueden por tanto quedarse en su último valor hasta la siguiente lectura. El detalle de cada estado de carga sigue en **Estado de la carga**.

**Aperturas.** Las ocho informaciones de apertura (**Puerta delantera del conductor** a **Cubierta de caja**) se leen **sin despertar el vehículo**, en cada actualización de las informaciones, como la presencia y el bloqueo. Un estado que el vehículo no sabe dar (desconocido, fallo de desbloqueo) deja el **último valor** en su sitio, sin mensaje. **Puerto de carga (apertura)** (leído incluso dormido) y **Puerto de carga abierto** (leído solo con el vehículo despierto) pueden diferir unos instantes, incluso justo después de un comando de apertura o de cierre del puerto: el valor converge tras la relectura diferida. Si el vehículo no proporciona en absoluto el estado de sus aperturas, el proxy las transmite como cerradas: aparecen entonces **cerradas** (solo un estado explícitamente desconocido deja el último valor). Con un proxy anterior a 2.3.0, es necesaria una actualización del proxy: las aperturas no se publican (véase [Comprobar y actualizar la versión del proxy](#comprobar-y-actualizar-la-version-del-proxy)).

**Ocupante y bloqueo detallado.** Estas dos informaciones, **Ocupante presente** y **Estado de bloqueo detallado**, se leen **sin despertar el vehículo**, en cada actualización de las informaciones, al mismo tiempo que la presencia y el bloqueo. Una presencia desconocida deja el **último valor** en su sitio: con el vehículo dormido, la información puede quedarse congelada, no se fíe de ella sola para una seguridad. Un vehículo **bloqueado desde el interior** deja **Bloqueo del vehículo** en 1. Tras un comando de bloqueo, el estado detallado se actualiza en cuanto el vehículo lo confirma. Un estado de bloqueo que el plugin no conoce se muestra tal como lo envía el vehículo. No confunda **Ocupante presente** con **Presencia del vehículo** (vehículo al alcance Bluetooth del proxy). Con un proxy anterior a 2.3.0, es necesaria una actualización del proxy: estas informaciones no se publican (véase [Comprobar y actualizar la versión del proxy](#comprobar-y-actualizar-la-version-del-proxy)).

**Programaciones leídas en el vehículo.** Tres informaciones de texto `HH:MM`, creadas **ocultas**, reflejan la programación del vehículo en cada lectura de los datos (incluida la lectura «solo carga»): **Hora de carga programada** (modo de carga diferida), **Fin de las horas valle** y **Preacondicionamiento planificado** (modo de salida programada). Con el modo **Off**, o fuera del modo correspondiente, están **vacías** (nunca `00:00`): pruebe `== ""` en un escenario. El modo en sí permanece en **Modo de carga programada**, sin cambios. Conservan su último valor mientras el vehículo duerme y se vacían en la primera lectura posterior a la desactivación de la programación. Precisiones: la **hora de carga** se muestra en la zona horaria de Jeedom; **Fin de las horas valle** es el valor del ajuste, esté o no activa la opción, y permanece vacía cuando el vehículo indica medianoche; **Preacondicionamiento planificado** es la hora de salida objetivo, mostrada incluso los días en que la programación no se aplica; los días afectados y las programaciones con varias franjas no se leen. Un dato ilegible deja la información sin cambios (mención en el log en modo debug).

**Informaciones de climatización ampliadas.** Las catorce informaciones anteriores, de **Climatización automática** a **Calefacción de la batería**, se crean **ocultas** y no historizadas, incluso en un dispositivo existente durante la actualización: muestre las que le interesen desde la pestaña **Comandos**, su elección nunca se sobrescribe. Se leen junto con los datos de carga y de climatización, sin petición adicional y sin despertar nunca el vehículo: conservan su último valor mientras duerme. Un campo que el vehículo no devuelve deja la información sin cambios sin impedir que las demás se actualicen. Los valores son los del vehículo, sin transformación.

- **Escala de la calefacción del volante.** Atención: no es la de los asientos. Es la escala del protocolo Tesla: anote los valores en su vehículo antes de usarla en un escenario.

  | Valor | Significado |
  |---|---|
  | 0 | desconocido (o volante sin equipar) |
  | 1 | apagado |
  | 2 | bajo |
  | 3 | alto |

  **Una prueba «mayor que 0» es por tanto falsa**: el valor 1 significa que la calefacción está apagada. Para saber si el volante calienta, pruebe `>= 2`. La información existente **Calefacción del volante** (`steering_wheel_heater`) sigue siendo el simple indicador activo / inactivo. Para los asientos, 0 es «apagado» y 3 «alto».
- **Equipamiento ausente.** Un asiento trasero o un volante que el vehículo no tiene se informa como 0, igual que un equipamiento apagado: la información no permite distinguirlos.
- **Temperaturas mín. y máx. ajustables.** Son los límites de ajuste de la climatización del vehículo (por ejemplo 15 y 28 °C). Un valor ausente, nulo o fuera del intervalo de 5 a 40 °C se ignora; si el mínimo no es estrictamente inferior al máximo, ambos se ignoran (mención en el log en modo debug). Conservarán entonces su último valor.
- **Calefacción de la batería.** Se lee en los datos de climatización del vehículo. El campo equivalente de los datos de carga no lo proporciona el proxy 2.3.0 y se quedaría siempre en 0: no se utiliza.
- **Mantenimiento de clima (perro, camping).** Valores posibles: `Off`, `On`, `Dog` (modo perro), `Party` (modo camping), `Unknown`. La asociación de `Party` con el modo camping está por confirmar en su vehículo. Un valor ilegible deja la información sin cambios.
- **Protección contra sobrecalentamiento.** Valores posibles: `CabinOverheatProtectionOff`, `CabinOverheatProtectionOn`, `CabinOverheatProtectionFanOnly`. Un vehículo que no informa el ajuste se notifica como `CabinOverheatProtectionOff`.
- **Velocidad de ventilación.** Valor bruto cuya escala no está documentada: anótelo en su vehículo antes de usarlo en un escenario.
- **Preacondicionamiento y desempañados.** Pasan a 1 en la lectura de los datos que sigue a su activación; un ciclo solo tiene lugar si el vehículo está despierto, y el proxy conserva sus datos 30 segundos en memoria. No es una lectura desencadenada por el evento.

**Actualización del plugin.** Las tres informaciones de programación se crean **ocultas** en cada dispositivo existente y permanecen vacías hasta la primera lectura de los datos de un vehículo despierto. La información **Energía de carga acumulada** se crea **oculta** e **historizada** en cada dispositivo existente durante la actualización. Permanece vacía hasta la primera lectura de los datos de un vehículo despierto y después parte de 0: la energía ya cargada antes de la actualización no se recupera. Del mismo modo, las acciones **Ajustar según el excedente**, **Añadir una programación de carga** y **Eliminar la programación de carga** se añaden **ocultas** a cada dispositivo existente; sus ajustes conservan sus valores por defecto mientras no los modifique, y no se modifica ningún comando existente. Las catorce informaciones de climatización ampliadas también se crean **ocultas** en cada dispositivo existente, sin modificar ninguna información de climatización ya presente.

### Contadores de energía de carga

Para seguir su consumo de carga, el plugin mantiene un **índice que solo crece**: la información **Energía de carga acumulada** (kWh). El vehículo, por su parte, pone **Energía añadida** a cero en cada nueva sesión de carga; por tanto no es un contador utilizable tal cual.

- **Parte de 0** en la creación de la información (activación de la función), sin recuperar el historial.
- **Cálculo por diferencia**: en cada lectura de los datos, el plugin suma al acumulado la energía ganada desde la lectura anterior. Una sesión que cae por debajo del **90 %** del valor visto anteriormente (umbral del 10 %) es una nueva sesión: se suma entera. Una pequeña bajada aislada se ignora. Un valor negativo, ilegible o superior a 1000 kWh (considerado aberrante) se ignora. Una nueva sesión que ya alcance el 90 % de la anterior desde la primera lectura se contabiliza de menos.
- **Precisión limitada por la frecuencia de lectura**: el plugin solo conoce la energía en los momentos en que lee los datos, es decir, solo con el vehículo despierto y a la frecuencia configurada (véase [Lectura acelerada durante la carga](#lectura-acelerada-durante-la-carga)). Una carga entera iniciada y terminada entre dos lecturas puede contabilizarse de menos, y una carga hecha fuera del alcance del proxy solo se cuenta en parte, a la vuelta. A la inversa, una lectura aberrante puede a veces hacer contar una energía por duplicado: el acumulado nunca disminuye, pero no se garantiza que sea exacto.
- **Energía del lado de la batería**: es la energía añadida a la batería, inferior a la del contador o del punto de carga (pérdidas de carga).
- **Plugin Energía de Jeedom**: declare **Energía de carga acumulada** como comando de consumo; en principio: índice absoluto, sin marcar «Consumo por día» (a comprobar según la versión del plugin Energía).
- **Nunca se pone a cero** al hacer clic en **Guardar** ni con una actualización del plugin. No existe una puesta a cero manual. Eliminar la información pone el acumulado a 0 (se vuelve a crear vacía en el siguiente guardado); un dispositivo duplicado parte del acumulado del original.

### Acciones

Las acciones marcadas como «oculta» no se muestran en el widget por defecto; hágalas visibles desde la pestaña **Comandos** del dispositivo.

| Nombre | Identificador | Tipo / subtipo | Unidad | Descripción |
|---|---|---|---|---|
| Actualizar | `refresh` | acción / otro | | Relanza de inmediato la lectura de las informaciones (un posible error aparece en **Último error**) |
| Actualizar (con despertar) | `refresh_wakeup` | acción / otro | | Despierta el vehículo si hace falta, después lee sus datos de carga y de climatización y los publica, en una sola acción (véase [Actualizar con despertar](#actualizar-con-despertar)). Solo una acción suya o de un escenario puede hacerlo: la lectura periódica nunca despierta el vehículo |
| Despertar | `wake_up` | acción / otro | | Despierta el vehículo, sin leer sus datos. Innecesario antes de un comando: el proxy despierta el vehículo por sí solo. Una relectura sin despertar sigue al comando (véase [Relectura tras un comando](#relectura-tras-un-comando)); para obtener valores frescos de inmediato, prefiera **Actualizar (con despertar)** |
| Iniciar la carga | `charge_start` | acción / otro | | Inicia la carga |
| Detener la carga | `charge_stop` | acción / otro | | Detiene la carga |
| Corriente de carga | `set_charging_amps` | acción / deslizador | A | Ajusta la corriente de carga (entero, entre el Min y el Max del comando; 0 a 32 A mientras el vehículo no haya publicado su límite, luego su corriente máxima; ajuste el Max a mano para fijarlo, o lance una lectura con despertar para actualizar los límites) |
| Límite de carga | `set_charge_limit` | acción / deslizador | % | Ajusta el límite de carga, entre el Min y el Max del comando (50 a 100 % mientras el vehículo no haya publicado sus límites, luego sus límites) |
| Ajustar según el excedente | `adjust_surplus` | acción / deslizador | W | Recibe la **potencia disponible para la carga** (en vatios, valor **absoluto**, no una variación) y decide por sí sola si hay que enviar un comando (véase [Control según el excedente](#control-segun-el-excedente)). Se crea **oculta**: se llama desde un escenario. |
| Añadir una programación de carga | `add_charge_schedule` | acción / mensaje | | Crea o reemplaza la programación de carga gestionada por Jeedom: el **título** lleva los días (`lun,mar,mer,jeu,ven`), el **mensaje** la hora de inicio (`23:00`). **Se requiere el proxy del fork**, con las coordenadas de Jeedom indicadas (véase [Programar la carga](#programar-la-carga)). Se crea **oculta**. |
| Eliminar la programación de carga | `remove_charge_schedule` | acción / otro | | Elimina la programación creada por Jeedom; sin efecto ni error si no hay ninguna. **Se requiere el proxy del fork** (véase [Programar la carga](#programar-la-carga)). Se crea **oculta**. |
| Iniciar la climatización | `auto_conditioning_start` | acción / otro | | Lanza el preacondicionamiento |
| Detener la climatización | `auto_conditioning_stop` | acción / otro | | Detiene el preacondicionamiento |
| Consigna del conductor | `set_driver_temp` | acción / deslizador | °C | Ajusta la temperatura solicitada del lado del conductor, de 15 a 28 °C en pasos de 0,5 °C; el lado del pasajero conserva su último valor leído. **Se requiere el proxy del fork**. Se crea **oculta** (véase [Ajustar la consigna de temperatura](#ajustar-la-consigna-de-temperatura)). |
| Consigna del pasajero | `set_passenger_temp` | acción / deslizador | °C | Ajusta la temperatura solicitada del lado del pasajero, de 15 a 28 °C en pasos de 0,5 °C; el lado del conductor conserva su último valor leído. **Se requiere el proxy del fork**. Se crea **oculta** (véase [Ajustar la consigna de temperatura](#ajustar-la-consigna-de-temperatura)). |
| Ajustar la calefacción del asiento delantero izquierdo | `set_seat_heater_left` | acción / lista | | Ajusta la calefacción del asiento delantero izquierdo: Apagado, Bajo, Medio o Alto (0 a 3). **Se requiere el proxy del fork**. Se crea **oculta** (véase [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante)). |
| Ajustar la calefacción del asiento delantero derecho | `set_seat_heater_right` | acción / lista | | Ajusta la calefacción del asiento delantero derecho: Apagado, Bajo, Medio o Alto (0 a 3). **Se requiere el proxy del fork**. Se crea **oculta** (véase [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante)). |
| Ajustar la calefacción del asiento trasero izquierdo | `set_seat_heater_rear_left` | acción / lista | | Ajusta la calefacción del asiento trasero izquierdo: Apagado, Bajo, Medio o Alto (0 a 3). **Se requiere el proxy del fork**. Se crea **oculta** (véase [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante)). |
| Ajustar la calefacción del asiento trasero derecho | `set_seat_heater_rear_right` | acción / lista | | Ajusta la calefacción del asiento trasero derecho: Apagado, Bajo, Medio o Alto (0 a 3). **Se requiere el proxy del fork**. Se crea **oculta** (véase [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante)). |
| Ajustar la calefacción del asiento trasero central | `set_seat_heater_rear_center` | acción / lista | | Ajusta la calefacción del asiento trasero central: Apagado, Bajo, Medio o Alto (0 a 3). **Se requiere el proxy del fork**. Se crea **oculta** (véase [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante)). |
| Ajustar la calefacción del volante | `set_steering_wheel_heater` | acción / lista | | Enciende o apaga la calefacción del volante (Apagado o Encendido, sin nivel). **Se requiere el proxy del fork**. Se crea **oculta** (véase [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante)). |
| Desempañado máximo | `set_preconditioning_max` | acción / lista | | Activa (Encendido) o detiene (Apagado) el desempañado máximo del vehículo; despierta el vehículo y consume batería. **Se requiere el proxy del fork**. Se crea **oculta** (véase [Desempañado máximo](#desempanado-maximo)). |
| Modo de mantenimiento de clima | `set_climate_keeper_mode` | acción / lista | | Elige el mantenimiento de clima: Apagado (0), Mantenimiento (1), Modo perro (2) o Modo camping (3); despierta el vehículo y consume batería. **Se requiere el proxy del fork**. Se crea **oculta** (véase [Modo perro, camping y mantenimiento de clima](#modo-perro-modo-camping-y-mantenimiento-de-clima)). |
| Abrir el puerto de carga | `charge_port_door_open` | acción / otro | | Abre el puerto de carga (oculta) |
| Cerrar el puerto de carga | `charge_port_door_close` | acción / otro | | Cierra el puerto de carga (oculta) |
| Hacer parpadear las luces | `flash_lights` | acción / otro | | Hace parpadear los faros (oculta) |
| Tocar el claxon | `honk_horn` | acción / otro | | Acciona el claxon |
| Bloquear las puertas | `door_lock` | acción / otro | | Bloquea el vehículo (oculta) |
| Desbloquear las puertas | `door_unlock` | acción / otro | | Desbloquea el vehículo (oculta) |
| Abrir el maletero trasero | `open_trunk_rear` | acción / otro | | Abre el maletero trasero, tras una relectura del estado: rechazada si el maletero se lee abierto, en movimiento o desconocido; despierta el vehículo. **Se requiere el proxy del fork**, se solicita confirmación. Se crea **oculta** (véase [Abrir el maletero trasero y el frunk](#abrir-el-maletero-trasero-y-el-maletero-delantero)). |
| Abrir el maletero delantero | `open_trunk_front` | acción / otro | | Abre el maletero delantero; despierta el vehículo. **Se requiere el proxy del fork**, se solicita confirmación. Se crea **oculta** (véase [Abrir el maletero trasero y el frunk](#abrir-el-maletero-trasero-y-el-maletero-delantero)). |
| Modo Centinela | `set_sentry_mode` | acción / lista | | Activa o desactiva el modo Centinela (**Activado** o **Desactivado**) (oculta). El estado se lee en **Centinela** y **Origen del modo Centinela** (véase [Estado del modo Centinela](#estado-del-modo-centinela)) |

## Ejemplos de uso

- **Carga solar**: en un escenario, envíe la potencia disponible a **Ajustar según el excedente** (consulte el [ejemplo paso a paso: carga solar](#ejemplo-paso-a-paso-carga-solar-con-ajustar-segun-el-excedente) y [Control según el excedente](#control-segun-el-excedente)).
- **Horas valle**: active la **Carga en horas valle** del dispositivo (intervalo, SoC objetivo): Jeedom inicia y detiene la carga por sí mismo (consulte la [guía paso a paso para configurar la carga en horas valle](#carga-en-horas-valle)). También puede, sin esta función, activar **Iniciar la carga** al comienzo de las horas valle y **Detener la carga** al final desde un escenario.
- **Precalentamiento**: active el **Preacondicionamiento planificado por Jeedom** del dispositivo (hora de salida, días, antelación): Jeedom inicia y detiene la climatización por sí mismo (consulte el [ejemplo de uso](#preacondicionamiento-planificado-por-jeedom)). También puede, sin esta función, lanzar **Iniciar la climatización** desde un escenario unos minutos antes de su salida.
- **Alerta**: reciba una notificación si **Bloqueo del vehículo** sigue en 0 por la noche.
- **Fallo de comunicación**: reciba una notificación cuando **Último error** pase a algo distinto de **Ninguna** (proxy inaccesible, proxy sin llave emparejada...). Un vehículo dormido no la activa.
- **Control de frescura**: ajuste la corriente de carga solo si los datos tienen menos de 5 minutos; en caso contrario, no haga nada (consulte el ejemplo paso a paso «actuar solo con datos recientes» más abajo).
- **Maletero que se queda abierto**: active la alerta de apertura prolongada y dispare una notificación (consulte el [ejemplo paso a paso: recibir un aviso cuando el maletero se queda abierto](#ejemplo-paso-a-paso-recibir-un-aviso-cuando-el-maletero-se-queda-abierto)).

### Ejemplo paso a paso: carga solar con Ajustar según el excedente

Este escenario envía periódicamente a **Ajustar según el excedente** la potencia que su producción solar puede dedicar a la carga; el plugin decide por sí solo si realmente debe cambiar la corriente, iniciar o detener la carga (consulte [Control según el excedente](#control-segun-el-excedente)).

**Requisitos previos**

- El vehículo está **conectado** (de lo contrario el plugin se abstiene: **«Vehículo no conectado: ajuste según el excedente ignorado»**).
- **Intervalo durante la carga** configurado en **1 minuto** en el dispositivo: el control decide según el último **Estado de la carga** leído, es decir, según la frescura de las lecturas.
- Una medida de su **exportación a la red** en vatios (contador, pasarela del inversor) o, en su defecto, la **Potencia de carga** del vehículo.
- La acción **Ajustar según el excedente** no necesita estar visible: se llama desde el escenario (la llave del proxy Charging Manager es suficiente, consulte [Rol de la llave](#rol-de-la-llave)).

**Ajustes iniciales.** En la sección **Control según el excedente** del dispositivo, los campos que se dejan vacíos toman estos valores. Son **puntos de partida orientativos, que debe validar en su instalación**: todavía no se ha realizado ninguna medición que los confirme.

| Ajuste | Valor inicial | Adáptelo si |
|---|---|---|
| **Tensión de la red (V)** | 230 | su tensión fase-neutro es diferente |
| **Fases** | Monofásico | su punto de carga es **trifásico**: elija Trifásico; de lo contrario, la corriente objetivo es tres veces demasiado alta |
| **Paso de ajuste (A)** | 1 | desea menos variaciones (paso mayor) |
| **Histéresis (A)** | 2 | la corriente cambia con demasiada frecuencia (valor mayor) |
| **Intervalo mínimo entre comandos (s)** | 120 (60 como mínimo) | se solicita demasiado al vehículo (valor mayor) |
| **Corriente mínima de arranque (A)** | 6 | su vehículo o su punto de carga exige una corriente más alta para arrancar |
| **Umbral de parada (A)** | 5 (nunca superior al de arranque) | desea detener antes o después |
| **Duración de mantenimiento antes de la parada (s)** | 300 | los pasos nubosos detienen la carga con demasiada frecuencia (valor mayor) |

**Crear el escenario**

1. Abra **Herramientas > Escenarios**, haga clic en **Añadir** y asigne un nombre al escenario, por ejemplo «Carga solar Tesla». En **Modo del escenario**, elija **Programado** e indique una ejecución **cada 2 a 5 minutos** (por ejemplo `*/2 * * * *` para cada 2 minutos). Llamarlo con más frecuencia no sirve de nada: el plugin ignora las llamadas que no aportan nada.
2. Abra la pestaña **Escenario**, haga clic en **+ Bloque** y elija **Si/Entonces/Sino**.
3. En **SI**, introduzca un control de frescura, por ejemplo `#[Garaje][Tesla][Antigüedad de los datos (min)]# <= 5` (consulte el [ejemplo paso a paso: actuar solo con datos recientes](#ejemplo-paso-a-paso-actuar-solo-con-datos-recientes)). Este control es **opcional**.
4. En **ENTONCES**, añada una **Acción** de asignación de variable: nombre `puissance_dispo`, valor = **exportación a la red + potencia de carga**, en **vatios**. Por ejemplo `#[Garaje][Contador][Exportación a la red]# + #[Garaje][Tesla][Potencia de carga]# * 1000`.
5. Siempre en **ENTONCES**, añada una **Acción**: el comando **Ajustar según el excedente** del vehículo, con el valor `variable(puissance_dispo)` (lectura de la variable asignada en el paso anterior).
6. **Guarde** y, a continuación, lance el escenario una primera vez manualmente.

**Por qué «exportación + potencia de carga».** El valor enviado es la potencia **absoluta** que el vehículo puede consumir. La exportación medida por el contador ya está **reducida** por lo que consume el vehículo: si no se suma la potencia de carga actual, la consigna volvería a bajar en cada ajuste. Si su contador indica la exportación con signo negativo, corrija el signo para obtener vatios positivos. De todos modos, un valor negativo se reduce a 0 W.

**Si la única fuente es la Potencia de carga del vehículo.** Está en **kilovatios** y con frecuencia es **entera**: multiplique por 1000 (como arriba) y espere un valor aproximado. Si dispone de ella, es preferible la medida de un contador o del punto de carga.

**Comprobar que funciona.** Ponga el log del plugin en **Debug** (**Configuración del plugin > Logs**) y lance el escenario: cada llamada escribe una línea **«pilotage selon le surplus : … W, courant calculé … A, cible … A, décision … (motif)»** (*control según el excedente: … W, corriente calculada … A, objetivo … A, decisión … (motivo)*). Las decisiones posibles son, entre otras, `set_charging_amps`, `charge_start`, `charge_stop`, `aucune` e `ignorer`; el motivo explica por qué (histéresis, intervalo mínimo, corriente ya en el objetivo...). Una abstención del plugin aparece también en **Último error**.

**Qué ocurre por la noche.**

- Sin producción, la potencia disponible cae a **0 W**: la corriente calculada pasa por debajo del **Umbral de parada** y la carga se **detiene** una vez transcurrida la **Duración de mantenimiento antes de la parada** (300 s por defecto). Al día siguiente se reinicia cuando la corriente calculada alcanza la **Corriente mínima de arranque**.
- Si utiliza también la [Carga en horas valle](#carga-en-horas-valle), la llamada a **Ajustar según el excedente** se **ignora durante el intervalo** (sin error): el escenario solar no detiene, por tanto, la carga de las horas valle. Fuera del intervalo, el control según el excedente retoma el mando.

### Ejemplo paso a paso: recibir un aviso cuando el proxy está inaccesible

La información **Proxy accesible** vale 1 mientras el proxy responde al ciclo de actualización (se publica en cada pasada en la que se lee un vehículo de este proxy, según su intervalo) y pasa a 0 cuando está apagado, inaccesible o no responde dentro de los plazos. Un vehículo fuera de alcance o dormido no la hace pasar a 0. Cree un escenario que le avise:

1. Abra **Herramientas > Escenarios**, haga clic en **Añadir** y asigne un nombre al escenario, por ejemplo «Alerta proxy Tesla». En **Modo del escenario**, elija **Provocado** (el escenario se lanza cuando cambia su disparador).
2. En **Disparador(es)**, haga clic en **+ Disparador** y elija el comando **Proxy accesible** de su vehículo. Se escribe `#[Objeto][Vehículo][Proxy accesible]#` (por ejemplo `#[Garaje][Tesla][Proxy accesible]#`). Con varios vehículos o varios proxys, añada el **Proxy accesible** de cada vehículo.
3. Abra la pestaña **Escenario**, haga clic en **+ Bloque** y elija **Si/Entonces/Sino**.
4. En el campo **SI**, introduzca la condición `#[Objeto][Vehículo][Proxy accesible]# == 0` (o elija el comando con el botón de selección y añada después `== 0`).
5. En **ENTONCES**, añada una **Acción**: un comando de notificación de su instalación (aplicación móvil, Telegram, correo electrónico...) o el comando **Añadir un mensaje** del centro de mensajes de Jeedom. Introduzca el texto, por ejemplo «El proxy Tesla ya no responde: compruebe la Raspberry Pi del garaje».
6. Para recibir también un aviso del restablecimiento, añada en **SINO** una segunda notificación, por ejemplo «El proxy Tesla vuelve a responder».
7. **Guarde** y pruebe apagando la Raspberry Pi: en la siguiente lectura (como máximo, en el intervalo más corto de los vehículos de este proxy, 5 minutos por defecto), **Proxy accesible** pasa a 0 y se envía la notificación. Vuelva a encenderla: en el siguiente ciclo, la información vuelve a 1 y se envía la notificación de restablecimiento.

El escenario se dispara en cada cambio del valor, es decir, en la avería y luego en el restablecimiento, no en cada ciclo. Para conocer la causa exacta (llave, alcance, adaptador bloqueado), consulte **Último error**.

### Ejemplo paso a paso: actuar solo con datos recientes

La información **Antigüedad de los datos (min)** indica el número de minutos transcurridos desde la última lectura correcta de los datos de carga y de climatización. Vale 0 justo después de una lectura y aumenta mientras no se complete ninguna lectura: vehículo dormido, ventana de sueño abierta, proxy inaccesible. Vale **99999** mientras no se conozca ninguna lectura (dispositivo nuevo, plugin recién actualizado). El siguiente escenario, para un control solar, ajusta la **Corriente de carga** solo si este valor es reciente:

1. Abra **Herramientas > Escenarios**, haga clic en **Añadir** y asigne un nombre al escenario, por ejemplo «Carga solar Tesla». En **Modo del escenario**, elija **Programado** e indique una ejecución cada 5 minutos.
2. Abra la pestaña **Escenario**, haga clic en **+ Bloque** y elija **Si/Entonces/Sino**.
3. En el campo **SI**, introduzca la condición `#[Objeto][Vehículo][Antigüedad de los datos (min)]# <= 5` (por ejemplo `#[Garaje][Tesla][Antigüedad de los datos (min)]# <= 5`), o elija el comando con el botón de selección y añada después `<= 5`.
4. En **ENTONCES**, añada una **Acción**: el comando **Corriente de carga** del vehículo, con el valor calculado por su escenario a partir de la producción solar.
5. En **SINO**, no ponga **nada** (la corriente de carga se queda como estaba) o añada una notificación, por ejemplo «Datos de Tesla demasiado antiguos: corriente de carga sin cambios».
6. **Guarde** y, a continuación, configure **Intervalo durante la carga** en **1 minuto** en el dispositivo: durante la carga, la antigüedad de los datos se mantiene en 1 minuto como máximo y la condición se cumple.

¿Por qué **5**? Es el intervalo de actualización por defecto: más allá, ha faltado al menos una lectura. Adapte el umbral a su frecuencia (un poco más que el intervalo utilizado durante la carga).

Por qué **99999** es algo bueno aquí: mientras no se conozca ninguna lectura, la condición `<= 5` es **falsa**, el escenario se abstiene y no envía ninguna corriente. Es prudente por construcción.

> **Atención**
>
> **No** utilice **Antigüedad de los datos (min)** como **disparador** de un escenario en modo **Provocado**: esta información se recalcula **cada minuto** y cambia, por tanto, constantemente; el escenario se lanzaría en bucle (y se enviaría una notificación cada vez).

**Variante: alerta «datos de más de 2 horas».** Cree un escenario en modo **Programado** (por ejemplo, cada hora) con la condición `#[Objeto][Vehículo][Antigüedad de los datos (min)]# >= 120 ET #[Objeto][Vehículo][Antigüedad de los datos (min)]# < 99999` y una notificación en **ENTONCES**. El límite `< 99999` evita una falsa alerta cuando no se conoce ninguna lectura; es preferible `>= 120` a una igualdad exacta (`== 120`), que solo se cumple durante un minuto y puede pasarse por alto. Un vehículo que duerme mucho tiempo activa esta alerta sin que haya ninguna avería: es una simple constatación de frescura. Para obtener datos recientes, lance **Actualizar (con despertar)**.

### Ejemplo paso a paso: recibir un aviso cuando el maletero se queda abierto

Este escenario le avisa cuando una apertura (maletero trasero, maletero delantero, puerta, puerto de carga) permanece abierta más de 10 minutos. Se basa en la alerta de apertura prolongada (consulte [Alertas de apertura prolongada](#alertas-de-apertura-prolongada)); una llave Charging Manager es suficiente, ya que se trata de lecturas.

1. Abra la página de su vehículo (**Complementos > Objetos conectados > Tesla BLE**) y vaya al bloque **Alertas de apertura prolongada**.
2. En **Apertura que sigue abierta**, marque **Activar** e introduzca **Duración antes de la alerta (min)**: `10`. La duración es obligatoria, de 1 a 1440 minutos.
3. **Guarde**. Un mensaje de error al guardar indica una duración vacía o no válida (consulte [Mensajes al guardar](#mensajes-al-guardar)).
4. Abra la pestaña **Comandos** y marque **Mostrar** en **Alerta de aperturas** (está oculta por defecto, pero ya historizada). **Guarde**.
5. Abra **Herramientas > Escenarios**, haga clic en **Añadir** y asigne un nombre al escenario, por ejemplo «Alerta maletero abierto». En **Modo del escenario**, elija **Provocado**.
6. En **Disparador(es)**, añada el comando **Alerta de aperturas** de su vehículo, por ejemplo `#[Garaje][Tesla][Alerta de aperturas]#`.
7. En la pestaña **Escenario**, añada un bloque **Si/Entonces/Sino** con la condición `#[Garaje][Tesla][Alerta de aperturas]# == 1`. El escenario se lanza también al volver a 0: sin esta condición, se le avisaría al cerrar.
8. En **ENTONCES**, añada una **Acción** de notificación de su instalación (aplicación móvil, Telegram, correo electrónico...) con un texto como «Una apertura del Tesla ha permanecido abierta más de 10 minutos». El centro de mensajes de Jeedom recibe por su parte un mensaje que nombra la apertura, sin configurar nada.
9. **Guarde** y pruebe: abra el maletero trasero manualmente y espere la duración elegida **más dos intervalos de actualización** (hasta 20 minutos con 10 minutos y el intervalo por defecto de 5 minutos). **Alerta de aperturas** pasa a 1, el mensaje aparece en el centro de mensajes y se envía la notificación.
10. Cierre el maletero: en la siguiente lectura, **Alerta de aperturas** vuelve a 0 y el escenario se lanza sin notificar. El mensaje permanece en el centro de mensajes: elimínelo.

Para un vehículo dejado desbloqueado, proceda de la misma manera con **Vehículo desbloqueado sin ocupante** y la información **Alerta de vehículo desbloqueado sin ocupante**.

**Consejos de uso de la presencia de un ocupante.** **Ocupante presente** (`user_present`) vale 1 cuando el vehículo detecta a una persona a bordo.

- **Condición «nadie a bordo».** En un escenario, pruebe `#[Garaje][Tesla][Ocupante presente]# == 0` antes de una acción que solo tiene sentido con el vehículo vacío (por ejemplo, volver a lanzar un bloqueo). Combínela con **Bloqueo del vehículo** y pruebe estas dos informaciones en lugar de la etiqueta **Estado de bloqueo detallado**, que cambia con el idioma de Jeedom.
- **Presencia desconocida = último valor.** Cuando el vehículo no proporciona el estado (está dormido), la información conserva su último valor: puede mostrar «nadie» aunque haya quedado una persona a bordo, o lo contrario. Compruebe **Antigüedad de los datos (min)** si la decisión es importante.
- **No es una medida de seguridad.** No la utilice nunca para proteger a una persona o a un animal (por ejemplo, para decidir apagar la climatización: un niño o un animal que se haya quedado a bordo puede no ser detectado). No la confunda con **Presencia del vehículo**, que solo indica que el vehículo está al alcance Bluetooth del proxy.

## Versiones, idiomas y asistencia

### Versión estable o versión beta

El plugin se publica en el Market de Jeedom en dos versiones: la **estable** (recomendada) y la **beta** (versión candidata, que recibe las novedades en primer lugar, reservada a los beta-testers).

- **Instalar.** En **Complementos > Gestión de plugins > Market**, abra **Tesla BLE** y haga clic en **Installer stable** o **Installer beta** (*Instalar estable* / *Instalar beta*). El Market sincroniza las versiones cada noche: una novedad puede tardar un día en aparecer.
- **Saber qué está instalado.** En la parte superior de la página del plugin, el nombre va seguido de su ID entre paréntesis y, después, del tipo de versión (estable, beta).
- **Volver a la estable.** En la misma página, haga clic en **Installer stable** (*Instalar estable*). Si el log **cron** de Jeedom muestra después un error cada minuto, véase [Tarea del ciclo de actualización](#tarea-del-ciclo-de-actualizacion).

> **IMPORTANTE**: Jeedom advierte de que no se recomienda en absoluto instalar un plugin beta en un Jeedom que no sea beta. Evite la beta en un Jeedom de producción.

### Leer el changelog

El [changelog](changelog.md) es **único**: sirve tanto para la estable como para la beta. Las entradas están fechadas, las más recientes arriba, y llevan el prefijo **Añadido**, **Corrección**, **Evolución** o **Documentación**.

Se publica antes que la versión estable: una entrada reciente puede describir una novedad que todavía solo está disponible en beta. Una actualización del plugin sin entrada en el changelog solo afecta a la documentación, a una traducción o a un texto.

### Idiomas disponibles

La interfaz (configuración, dispositivo, mensajes, widget del vehículo y nombres de los comandos **creados**) y la documentación existen en francés, inglés, alemán y español.

- **Interfaz.** Sigue el **idioma de Jeedom**: **Ajustes > Sistema > Configuración**, pestaña **General**, campo **Idioma** (ajuste global de Jeedom). Un texto sin traducir se muestra en francés.
- **Comandos ya creados.** Conservan su nombre; para las etiquetas comparadas en un escenario, véase [Estado del modo centinela](#estado-del-modo-centinela).
- **Documentación.** El botón **Documentación** de Jeedom abre la versión francesa. Para cambiar de idioma, utilice el selector del sitio de documentación (`https://jeedomdocs.decastro.fr/teslable/`, `/en/teslable/`, `/de/teslable/` o `/es/teslable/`).

### Notificar un defecto

No existe un tema oficial para este plugin. Abra un tema en el foro de la comunidad Jeedom (<https://community.jeedom.com>), en la categoría de los plugins, con **Tesla BLE** en el título. Indique:

- la versión del plugin y su canal (estable o beta);
- la versión de Jeedom y la de Debian;
- la versión y el tipo del proxy (el de wimaha o el fork);
- un extracto del log **TeslaBLE** en nivel **Debug**.

Revise estos datos antes de publicarlos: no deje nunca su token, ni su VIN completo, ni ninguna dirección IP que no desee hacer pública. Véase [Consultar los logs del proxy](#consultar-los-logs-del-proxy).

## Limitaciones conocidas

- **Tras un comando**, solo se actualizan inmediatamente el límite de carga, la corriente de carga y el bloqueo. Las demás informaciones se actualizan tras la **relectura programada** (30 segundos por defecto, consulte [Relectura tras un comando](#relectura-tras-un-comando)), o en la siguiente lectura si el proxy está ocupado. Si el vehículo se ha vuelto a dormir, se conservan los últimos valores (sin error y sin despertar); fuera de alcance, la presencia pasa a «No»; si el proxy está inaccesible, se rellena «Último error».
- **Vehículo dormido**: la información de carga y de climatización solo se lee con el vehículo despierto (el plugin nunca lo despierta por sí mismo). Utilice **Actualizar (con despertar)**.
- **Ventana de sueño**: durante la ventana, la información de carga y de climatización y la **Última lectura de los datos** permanecen congeladas (duración por defecto 30 minutos). Una carga o una climatización iniciada desde la aplicación sin cambio visible del estado sin despertar solo se detecta en la lectura de control. Desmarque **Dejar que el vehículo se duerma** en el dispositivo para obtener una lectura completa en cada pasada.
- **Llave Charging Manager**: el bloqueo, el claxon, las luces y el modo Centinela son rechazados por el vehículo. El plugin lo detecta (información **Rol de la llave**) pero no atenúa estos comandos en el dashboard (consulte [Rol de la llave](#rol-de-la-llave)).
- **Climatización solo en carga**: con **Leer también la climatización** en **No, solo carga**, toda la información de climatización (temperaturas, calefacciones, desempañado, ventilación, mantenimiento de clima, climatización activa, etc.) deja de actualizarse y conserva su último valor; los comandos de climatización siguen disponibles.
- **Contador de energía de carga**: su precisión depende de la frecuencia de lectura, puede subestimar una carga corta o realizada fuera de alcance y no se pone a cero; solo se lee a la frecuencia de las lecturas, por lo que una frecuencia espaciada lo hace menos preciso (consulte [Contadores de energía de carga](#contadores-de-energia-de-carga)).
- **Control según el excedente**: los umbrales por defecto (arranque 6 A, parada 5 A, mantenimiento 300 s) deben validarse con su vehículo; la referencia es la **última consigna enviada por el control** (un ajuste manual concurrente solo se detecta tras una diferencia superior a la histéresis, una parada o una desconexión); una llamada de escenario puede esperar hasta unos 210 segundos; la decisión se basa en el último **Estado de la carga** leído, es decir, en la frescura de las lecturas (consulte [Lectura acelerada durante la carga](#lectura-acelerada-durante-la-carga)).
- **Control solar: solicitud Bluetooth y reposo.** Durante la carga, el vehículo está despierto de todos modos, pero el control según el excedente lo solicita: con **Intervalo durante la carga** en 1 minuto, hay una lectura **cada minuto**, **cada comando realmente enviado despierta el vehículo** y **sigue una relectura a cada comando correcto** (consulte [Relectura tras un comando](#relectura-tras-un-comando)). Un vehículo que recibe comandos durante todo el día tiene, por tanto, pocas posibilidades de dormirse. Espacie las llamadas (**Intervalo mínimo entre comandos**, histéresis, escenario cada 2 a 5 minutos). **No se publica ninguna medición del desgaste del enlace Bluetooth ni de la batería**: no deduzca de ello ninguna garantía ni riesgo cuantificado.
- **Carga en horas valle**: la decisión sigue la frecuencia de lectura (parada en el SoC objetivo aproximado sin **Intervalo durante la carga**); un vehículo dormido nunca se detiene, y su estado publicado puede estar caducado; **iniciar la carga despierta el vehículo**; un inicio que no va seguido de una carga **no se reintenta** antes del siguiente intervalo (un solo inicio por conexión); un **Iniciar** o **Detener** lanzado desde Jeedom durante el intervalo suspende el control hasta el siguiente intervalo; un intervalo que comienza en la hora omitida en el **cambio a la hora de verano** solo arranca al final de esa hora, y una acción manual realizada durante esa hora puede ignorarse; un solo intervalo por vehículo; el plazo de 2 minutos para comprobar el resultado de un comando debe validarse en uso real (consulte [Carga en horas valle](#carga-en-horas-valle)).
- **Preacondicionamiento planificado por Jeedom**: el rol Owner (supuesto) debe confirmarse en uso real; la decisión sigue la frecuencia de lectura (inicio y parada con unos minutos de margen, nada si ninguna lectura cae dentro de la ventana; se recomienda un intervalo de 5 minutos como máximo); **iniciar la climatización despierta el vehículo** y consume batería; un vehículo visto dormido nunca se detiene; una climatización que sigue funcionando en la primera lectura posterior al final de la ventana se detiene, incluso con un ocupante; desactivar la función durante la ventana no detiene una climatización ya iniciada; la temperatura utilizada es la ya configurada en el vehículo; una sola ventana por vehículo, la programación del vehículo no se lee para decidir; requiere **Leer también la climatización** en **Sí** (consulte [Preacondicionamiento planificado por Jeedom](#preacondicionamiento-planificado-por-jeedom)).
- **Programaciones de carga**: **Hora de carga programada** supone que el vehículo devuelve, en modo de carga diferida, una marca de tiempo válida por Bluetooth (por confirmar en uso real: de lo contrario, la información queda vacía); **Fin de las horas valle** se publica aunque la opción de horas valle esté desmarcada (el proxy no transmite su estado); los días de aplicación y los intervalos múltiples no se leen.
- **Programar la carga**: reservado al proxy del fork (rechazo inmediato con el proxy 2.3.0, cuya versión oficial no tiene la ruta de programación: el fork la añade, versiones `2.3.0-tb.N`); una sola programación gestionada por Jeedom por vehículo, solo con hora de inicio; sigue las coordenadas de Jeedom, que deben corresponder al lugar de estacionamiento; la hora es la del vehículo; el reemplazo sin duplicados, el rol de llave mínimo y la actualización de la información de programación tras el comando deben confirmarse en uso real (consulte [Programar la carga](#programar-la-carga)).
- **Consigna de temperatura**: reservada al proxy del fork (rechazo inmediato con el proxy 2.3.0); los dos lados se envían siempre juntos, el otro lado con su último valor leído (una consigna ajustada en la pantalla del vehículo desde la última lectura puede sobrescribirse); el control deslizante está limitado a 15 a 28 °C, de medio grado en medio grado; el rol Owner supuesto necesario y el nivel de temperatura (una consigna que no pasa a «HI») deben confirmarse en uso real (consulte [Ajustar la consigna de temperatura](#ajustar-la-consigna-de-temperatura)).
- **Calefacción de los asientos y del volante**: reservada al proxy del fork, versión `2.3.0-tb.2` como mínimo (rechazo inmediato con el proxy 2.3.0); las seis acciones permanecen **ocultas**: debe mostrarlas usted mismo tras pasar al fork; sin reposacabezas ni tercera fila; volante solo con encendido/apagado; el comportamiento con la climatización apagada, con un asiento ausente y con un volante de calefacción automática debe validarse en uso real.
- **Desempañado máximo**: reservado al proxy del fork, versión `2.3.0-tb.1` como mínimo (rechazo inmediato con el proxy 2.3.0); la acción permanece **oculta**: debe mostrarla usted mismo tras pasar al fork; despierta el vehículo, consume batería y no se detiene sola; con **Leer también la climatización** en **No, solo carga**, o si el vehículo se vuelve a dormir, **Modo desempañado** conserva el valor optimista (un `Off` mostrado puede ser falso si el vehículo indica `Normal`); el rol Owner y el comportamiento al detenerse (`Off` o `Normal`) deben validarse en uso real.
- **Modo perro, camping y mantenimiento de clima**: reservado al proxy del fork, versión `2.3.0-tb.1` como mínimo (rechazo inmediato con el proxy 2.3.0); la acción permanece **oculta**: debe mostrarla usted mismo tras pasar al fork; despierta el vehículo, consume batería durante mucho tiempo, no se detiene sola y no sustituye una vigilancia de la temperatura para un animal; con **Leer también la climatización** en **No, solo carga**, o si el vehículo se vuelve a dormir, **Mantenimiento de clima (perro, camping)** conserva el valor anunciado; la ventana de sueño no se abre mientras se lea un mantenimiento (`On`, `Dog`, `Party`); el rol Owner, el nombre `Party` del modo camping y el valor releído tras una parada deben validarse en uso real.
- **Abrir el maletero trasero y el maletero delantero**: reservado al proxy del fork, versión `2.3.0-tb.2` como mínimo (rechazo inmediato con el proxy 2.3.0); las dos acciones permanecen **ocultas**: debe mostrarlas usted mismo tras pasar al fork; despiertan el vehículo; el maletero trasero solo se abre si se lee cerrado (la relectura puede no detectar una apertura reciente, y un portón motorizado puede entonces volver a cerrarse); un pestillo señalado como «no liberado» (fallo de apertura anterior) se trata como cerrado y el comando se reenvía, comportamiento por validar en uso real; el maletero delantero no se vuelve a leer; el plugin nunca vuelve a cerrar un maletero; el rol Owner supuesto necesario y el comportamiento en un maletero motorizado (o un maletero delantero motorizado) deben validarse en uso real.
- **Estado del modo Centinela**: la lectura real exige el proxy del fork en versión `2.3.0-tb.2` como mínimo y un vehículo **despierto**; de lo contrario, la información sigue la **última orden** enviada por Jeedom y no detecta ni un cambio hecho desde la aplicación, la pantalla del vehículo o un apagado automático, ni un valor leído en un vehículo dormido (se conserva el último valor leído); el estado `Idle` se cuenta como **Activada** (por confirmar en uso real); las etiquetas siguen el idioma de Jeedom (consulte [Estado del modo Centinela](#estado-del-modo-centinela)).
- **Alertas de apertura prolongada**: la duración solo se cuenta en lecturas correctas, a la frecuencia de actualización (alerta entre la duración y la duración más dos intervalos). Si se **vacía la caché de Jeedom** durante una alerta, el episodio se olvida: la información vuelve a 0 y luego a 1 tras una duración completa, con un segundo mensaje. Un **Estado de la carga** congelado en un vehículo dormido (por ejemplo «Stopped» o «Complete» caducado tras una desconexión) oculta un puerto de carga olvidado abierto. Sin la información de aperturas del vehículo (ocho estados cerrados o ausentes), el episodio se considera cerrado. El mensaje no se retira del centro de mensajes al cerrar.
- **Datos ampliados** (modelo, kilometraje y conducción, neumáticos, actualización de software, posición): a excepción del modelo y del año, exigen el **proxy del fork** (`2.3.0-tb.2` como mínimo) que los **anuncia**; de lo contrario no se crean. Solo se leen con el **vehículo despierto** y al alcance Bluetooth (las presiones, la actualización y la posición como máximo cada 15 minutos, no durante una ventana de sueño). Las unidades de **Velocidad** (mph) y de **Potencia** (kW) son supuestas y deben confirmarse en uso real. **En casa** es binaria: nunca se escribe sin domicilio ni posición (el mosaico muestra 0 antes del primer cálculo) y no vuelve a 0 cuando el vehículo se va; pruebe `== 1` con **Presencia del vehículo**. El log `event` de Jeedom registra latitud y longitud aunque estén ocultas (consulte [Posición y privacidad](#posicion-y-privacidad)).
- **Widget y visualización**: un **tipo genérico** vaciado a mano (**Ninguno**) puede volver a asignarse si se elimina y se vuelve a crear el comando, o si se repite la asignación de los tipos tras una actualización interrumpida (consulte [Tipos genéricos](#tipos-genericos)); una **imagen retirada** con **Quitar la imagen** **nunca se vuelve a asignar** y ningún botón restablece la imagen del plugin; el **orden de los comandos** solo se asigna en la creación y nunca se reescribe; la duración **Datos de hace** del mosaico no se envejece en el navegador; el **widget estándar** no muestra la imagen del modelo (consulte [Widget y visualización](#widget-y-visualizacion)).
- **Un solo dispositivo por vehículo** (VIN único).
- **Hora de salida programada historizada**: si estaba historizada antes de la actualización, sigue siendo numérica y ya no se actualiza mientras su subtipo no se cambie a **Otro**.
- **Proxy declarado con un nombre de servicio Docker**: el enlace al panel no se abre en el navegador (consulte [Enlace al panel del proxy](#enlace-al-panel-del-proxy)).

### Límites cuantificados

| Límite | Valor |
|---|---|
| Dispositivos Bluetooth por vehículo | **3** a la vez (teléfonos, reloj, proxy). Por encima, conexiones intermitentes. |
| Vehículos por proxy | **3 como máximo** para que el ciclo nunca se acorte en el peor caso; por encima, compruebe la **Última lectura de los datos** de cada vehículo. |
| Duración de un ciclo | Lanzado **cada minuto** para los vehículos vencidos (5 minutos de intervalo por defecto), 4 minutos como máximo; dura tanto como su proxy más lento (los proxys se leen en paralelo). |
| Espera de un proxy ocupado | Unos 2 minutos (110 segundos para una lectura, 15 segundos para la verificación del emparejamiento), luego **Proxy ocupado**. |
| Rol de la llave | **Charging Manager** por defecto: solo lecturas y carga, incluido el control según el excedente y la carga en horas valle; **Owner** para el bloqueo, el desbloqueo, el claxon, las luces, el modo Centinela, los maleteros (supuesto) y el preacondicionamiento planificado (consulte [Rol de la llave](#rol-de-la-llave)). |
| Autenticación del proxy | **Ninguna por defecto**: manténgalo en una red de confianza, nunca expuesto a Internet. El proxy del fork puede exigir un **token de API** (opcional, el mismo token para todos los proxys), que protege el acceso pero no sustituye a una red de confianza. |
| Dispositivos por vehículo | Uno solo (VIN único). |
| Logs del proxy | Proxy **2.3.0** como mínimo; solo se muestra el proxy de la configuración del plugin. |

## Solución de problemas

Ponga el log del plugin en nivel **Debug** (**Configuración del plugin > Registros**) para ver cada URL llamada y cada respuesta del proxy. Las líneas de inicio y de fin de avería requieren al menos el nivel **Info**.

Los mensajes están clasificados según el lugar donde los vea.

### Mensajes del botón Probar

| Mensaje | Causa | Acción |
|---|---|---|
| **«URL del proxy no indicada»** | El campo está vacío. | Introduzca la dirección del proxy. |
| **«URL no válida: debe empezar por http:// o https://…»** | La dirección está mal escrita (esquema ausente, caracteres no admitidos, puerto no válido). | Corríjala, por ejemplo `http://192.168.1.50:8080/`. La `/` final se añade sola. |
| **«URL no válida: las credenciales (usuario:contraseña@) no son compatibles»** | La dirección contiene credenciales. | Quite `usuario:contraseña@`: el proxy no tiene autenticación. |
| **«Proxy accesible — versión X»** (verde) | Todo va bien. | No hay nada que hacer. |
| **«Proxy accesible — versión X»** + **«Versión del proxy no compatible: 2.3.0 como mínimo, actualice el proxy»** (naranja) | El proxy responde, pero su versión es demasiado antigua. | Actualícelo (vea [Verificar y actualizar la versión del proxy](#comprobar-y-actualizar-la-version-del-proxy)). |
| **«Proxy accesible — versión desconocida»** (verde) | El proxy responde, pero no da un número de versión utilizable (instalación manual, por ejemplo). | Compruebe la versión a mano con la dirección del Consejo de los requisitos previos. |
| **«Versión del proxy no comunicada: proxy anterior a 2.1.3, o URL incorrecta»** (naranja) | El proxy responde «no encontrado» a la consulta de la versión. | Compruebe la dirección y el puerto; si no, actualice el proxy. |
| **«Proxy inaccesible»** (rojo, detalle `cURL …`) | Nada responde en esa dirección. | Compruebe la dirección, el puerto, que el proxy está iniciado y que la Raspberry Pi está encendida. |
| **«Tiempo de espera agotado»** (rojo) | El proxy no responde en 10 segundos. | Compruebe la Raspberry Pi (alimentación, Wi-Fi) y reinicie el proxy. |
| **«Respuesta no válida del proxy»** (rojo) | Lo que responde no es TeslaBleHttpProxy (puerto equivocado, otro servicio). | Compruebe la dirección y el puerto. |
| **«Ninguna respuesta del servidor Jeedom: consulte el log TeslaBLE»** | Jeedom no ha respondido a la prueba pasados 45 segundos. | Inténtelo de nuevo y luego consulte el log del plugin. |
| **«Error interno del plugin: consulte el log TeslaBLE»** | Error imprevisto del plugin. | Consulte el log del plugin y comuníquelo con ese log. |

La prueba solo consulta la versión del proxy: una prueba en verde no demuestra ni que la llave esté emparejada ni que el vehículo esté al alcance. Para eso, utilice el botón **Verificar el emparejamiento** del dispositivo (vea [Emparejar mi llave y verificar el emparejamiento](#emparejar-mi-llave-y-verificar-el-emparejamiento)).

### Mensajes al guardar

- **«URL no válida: …»** (configuración del plugin o URL del proxy de un vehículo): mismas causas que para el botón **Probar**. Se conserva la URL anterior.
- **«Ninguna URL de proxy configurada: …»** (último error de un vehículo o botón **Probar este proxy**): ni el vehículo ni la configuración del plugin tienen una URL de proxy. Indique una de las dos.
- **«VIN no válido: se esperan 17 caracteres, cifras y letras excepto I, O y Q»**: corrija el VIN del dispositivo (los espacios se quitan solos).
- **«Este VIN ya lo utiliza el dispositivo …»**: otro dispositivo ya tiene este VIN, lo que ocurre también con **Duplicar**. Elimine el duplicado o corrija el VIN.
- **«Carga en horas valle: la hora de inicio (o de fin) debe tener el formato HH:MM, de 00:00 a 23:59»**, **«… el SoC objetivo debe ser un entero entre 1 y 100 %»**, **«… el intervalo horario está vacío, la hora de fin debe ser distinta de la hora de inicio»** y **«… indique la hora de inicio, la hora de fin y el SoC objetivo para activar la función»**: ajuste de **Carga en horas valle** no válido; corríjalo (no se ha guardado nada).
- **«Control según el excedente: …»**: ajuste del control según el excedente fuera de los límites (vea [Control según el excedente](#control-segun-el-excedente)).
- **«Preacondicionamiento planificado: la hora de salida debe tener el formato HH:MM, de 00:00 a 23:59»**, **«… la antelación debe ser un entero entre 1 y 60 minutos»**, **«… la duración máxima debe ser un entero entre 1 y 120 minutos»**, **«… la duración máxima debe ser al menos igual a la antelación»**, **«… indique la hora de salida para activar la función»**, **«… marque al menos un día para activar la función»** y **«… “Leer también la climatización” debe seguir en Sí para activar la función»**: ajuste de **Preacondicionamiento planificado por Jeedom** no válido; corríjalo (no se ha guardado nada).
- **«Alertas de apertura prolongada: la duración antes de la alerta … debe ser un entero entre 1 y 1440 minutos, obligatorio para activar la alerta»**: la duración de la alerta (apertura que sigue abierta, o vehículo desbloqueado sin ocupante) está vacía aunque la alerta esté activada, o no es un entero de 1 a 1440 (vea [Alertas de apertura prolongada](#alertas-de-apertura-prolongada)). No se guarda nada.
- **«Posición del domicilio no válida: indique la latitud (de -90 a 90) y la longitud (de -180 a 180) en grados decimales, 8 decimales como máximo, o deje ambas vacías para usar la posición de Jeedom»**: solo una de las dos coordenadas del domicilio está indicada, o una está fuera de rango, no es numérica o tiene demasiados decimales, o el par vale 0/0. Corríjalas (o vacíe los dos campos para usar la posición de Jeedom); no se ha guardado nada. El valor introducido nunca se copia en el mensaje (vea [Posición y confidencialidad](#posicion-y-privacidad)).
- **«Radio del domicilio no válido: número entero de metros, de 10 a 10000»**: el **Radio (m)** no es un entero de 10 a 10000. Corríjalo (o vacíe el campo para 100 m); no se ha guardado nada.
- **«Error interno del plugin: consulte el log TeslaBLE»**: error imprevisto al guardar; el detalle está en el log del plugin.

### Centro de mensajes de Jeedom (tras una actualización)

- **«El VIN del dispositivo … no es válido: corríjalo en su página de configuración…»**: el VIN guardado por una versión antigua no es válido. Corríjalo.
- **«El dispositivo … tiene el mismo VIN que el dispositivo …»**: dos dispositivos para un mismo vehículo. Elimine el duplicado o corrija su VIN.
- **«La información … está historizada: sigue siendo numérica y ya no se actualiza…»**: vea [Hora de salida programada](#hora-de-salida-programada).
- **«Adaptador Bluetooth del proxy probablemente bloqueado — …»**: vea [Alerta de adaptador Bluetooth bloqueado](#alerta-de-adaptador-bluetooth-bloqueado). Reinicie la Raspberry Pi.
- **«…: apertura “…” abierta desde hace más de … min»** y **«…: vehículo desbloqueado sin ocupante desde hace más de … min»**: alertas de apertura prolongada, un mensaje por apertura y por episodio (vea [Alertas de apertura prolongada](#alertas-de-apertura-prolongada)). El mensaje no se retira al cerrar: elimínelo.

### Información «Último error» (lectura)

| Texto mostrado | Causa | Acción |
|---|---|---|
| **Ninguna** | El último ciclo de lectura ha tenido éxito (o el vehículo duerme, lo que no es un error). | No hay nada que hacer. |
| **Proxy inaccesible** | El proxy no responde en la dirección configurada. | Compruebe la URL, que el proxy está iniciado, la alimentación y el Wi-Fi de la Raspberry Pi. |
| **Tiempo de espera agotado** | El proxy o el vehículo responde demasiado despacio. | Compruebe la Raspberry Pi (alimentación, Wi-Fi) y reinicie el proxy si se repite. |
| **Adaptador Bluetooth del proxy probablemente bloqueado: reinicie la Raspberry Pi** | Varias lecturas seguidas han agotado su tiempo de espera aunque el proxy responde: vea [Alerta de adaptador Bluetooth bloqueado](#alerta-de-adaptador-bluetooth-bloqueado). | Reinicie la Raspberry Pi. |
| **Proxy sin llave: emparejamiento pendiente — …** | No hay ninguna llave en el proxy: todavía no ha generado ni instalado ninguna. | Genere una llave (**Generate**) en el panel del proxy, envíela al vehículo y valide con la tarjeta llave (enlace en la configuración del plugin o en **Emparejar mi llave**). |
| **Vehículo fuera de alcance — …** | El proxy no encuentra el vehículo por Bluetooth. La **Presencia del vehículo** pasa a 0. | Acerque la Raspberry Pi al vehículo; compruebe que el proxy tiene el Bluetooth para él solo y que el vehículo no tiene ya 3 dispositivos conectados. |
| **Vehículo no conectado / fuera del alcance del proxy / Carga finalizada / El punto de carga no suministra corriente: ajuste según el excedente ignorado** o **Estado de carga desconocido: lance Actualizar (con despertar)** | El control según el excedente no ha enviado ningún comando por este motivo (vea [Control según el excedente](#control-segun-el-excedente)). | Conecte el vehículo, acerque el proxy, o lance **Actualizar (con despertar)** si el estado es desconocido. |
| **Vehículo no conectado / El punto de carga no suministra corriente: carga en horas valle en espera** (seguido eventualmente de **(estado leído a las HH:MM, vehículo dormido)**) o **Estado de carga desconocido: lance Actualizar (con despertar)** | La carga en horas valle no ha enviado ningún comando por este motivo. Sufijo «vehículo dormido»: el estado mostrado data de la última lectura antes de que se durmiera y puede estar desfasado. | Conecte el vehículo, o lance **Actualizar (con despertar)** si el estado es desconocido o desfasado (vea [Carga en horas valle](#carga-en-horas-valle)). |
| **Carga en horas valle suspendida hasta el siguiente intervalo: carga reiniciada fuera del control** | La carga se reinició desde la aplicación de Tesla después de la parada en el SoC objetivo: Jeedom ya no la interrumpe. | No hay nada que hacer: el control se reanuda en el intervalo siguiente. |
| **Carga en horas valle suspendida hasta el siguiente intervalo: fallos de comando repetidos** | Tres comandos seguidos han fallado (vea el mensaje de error del comando en el log, advertencia). | Corrija la causa (llave, alcance, proxy); desconectar y volver a conectar reanuda el control, si no se reanuda en el intervalo siguiente. |
| **Carga iniciada por Jeedom pero detenida o no iniciada: ningún nuevo intento antes del siguiente intervalo** | No se ha comprobado una carga iniciada por Jeedom (detenida desde la aplicación, punto de carga que la rechaza, arranque demasiado lento). **No se hace ningún nuevo intento** para no despertar el vehículo en bucle. | Compruebe el punto de carga y el vehículo; inicie la carga a mano si hace falta (eso suspende el control hasta el intervalo siguiente). |
| **Vehículo no conectado: preacondicionamiento planificado no iniciado** (seguido eventualmente de **(estado leído a las HH:MM, vehículo dormido)**) o **Estado de carga desconocido: lance Actualizar (con despertar)** | Con la opción **Solo si está conectado**, el preacondicionamiento planificado no ha iniciado la climatización por este motivo. El mensaje de estado desconocido aparece también, incluso sin la opción, cuando se desconoce el estado de la climatización del vehículo despierto. | Conecte el vehículo, desmarque la opción, o lance **Actualizar (con despertar)** si el estado es desconocido o desfasado (vea [Preacondicionamiento planificado por Jeedom](#preacondicionamiento-planificado-por-jeedom)). |
| **Preacondicionamiento planificado suspendido hasta la próxima salida: se requiere rol Owner para la llave del proxy** | El vehículo ha rechazado **Iniciar la climatización**: la llave del proxy tiene probablemente el rol Charging Manager. Solo se hace un intento por salida. | Empareje una llave **Owner** (vea [Rol de la llave](#rol-de-la-llave)); el control se reanuda en la salida siguiente. |
| **Preacondicionamiento planificado suspendido hasta la próxima salida: fallos de comando repetidos** | Tres comandos seguidos han fallado (vea el mensaje de error del comando en el log, advertencia). | Corrija la causa (llave, alcance, proxy); el control se reanuda en la salida siguiente. |
| **Solicitud rechazada por el vehículo: llave del proxy no emparejada con este vehículo** | La llave activa del proxy no está emparejada con este vehículo (con varios vehículos, la misma llave debe estar emparejada con cada uno). Los demás vehículos no se ven afectados. | Utilice **Emparejar mi llave** y luego **Verificar el emparejamiento** en el dispositivo de este vehículo. |
| **Solicitud rechazada por el vehículo — …** | El vehículo ha rechazado la lectura; el motivo del proxy sigue al mensaje. | Lea el motivo indicado después del mensaje; compruebe también el emparejamiento de la llave. |
| **Función no compatible con este proxy — …** | La lectura solicitada no existe en su versión del proxy (por ejemplo el kilometraje `drive_state` solicitado a un proxy que lo rechaza). | Actualice el proxy (proxy del fork para los datos ampliados: vea [Datos ampliados: qué está disponible](#datos-ampliados-que-esta-disponible)). |
| **Respuesta no válida del proxy** | El proxy ha devuelto una respuesta inesperada. | Compruebe la dirección, actualice el proxy y reinícielo si se repite. |
| **Versión del proxy no compatible: 2.3.0 como mínimo, actualice el proxy** | El proxy es anterior a 2.1.1: el estado del vehículo ya no se puede leer. | Actualice el proxy (vea [Verificar y actualizar la versión del proxy](#comprobar-y-actualizar-la-version-del-proxy)). El log señala también esta línea como error. |
| **Proxy ocupado: lectura del vehículo no realizada, inténtelo de nuevo en un momento** | Un **Actualizar** ha esperado más de 110 segundos: el proxy estaba ocupado con un comando o una lectura. No se ha hecho ninguna lectura. | Lance **Actualizar** de nuevo en un momento; la siguiente lectura automática también lo recupera. |
| **Actualización con despertar fallida: …** | El comando **Actualizar (con despertar)** ha fallado: la causa (vehículo fuera de alcance, proxy inaccesible, vehículo que se niega a despertar…) sigue al mensaje. Las informaciones de carga y de climatización conservan su último valor (la **Presencia del vehículo** pasa a 0 si el vehículo está fuera de alcance). | Lea la causa indicada; acerque la Raspberry Pi al vehículo si hace falta y vuelva a lanzar. |
| **Tiempo de espera agotado durante el despertar del vehículo: puede haberse despertado, vuelva a intentarlo en un momento** | El despertar y la lectura han superado 75 segundos. El vehículo puede haberse despertado de todos modos. | Lance **Actualizar (con despertar)** de nuevo en un momento. |
| **El VIN no está configurado para este dispositivo** | El VIN del dispositivo está vacío. | Indique el VIN en el dispositivo y guarde. |
| **URL no válida: …** | La URL del proxy está vacía o no es válida en la configuración del plugin. | Indíquela (vea [Configuración del plugin](#configuracion-del-plugin)). |

El texto se trunca a 127 caracteres. Un vehículo que duerme no es un error: vea [Actualización de la información](#actualizacion-de-las-informaciones).

### Error al enviar un comando

Estos mensajes se muestran en rojo en Jeedom y se copian también en **Último error**.

| Mensaje | Causa | Acción |
|---|---|---|
| **«Este comando requiere una llave con rol Owner: la llave del proxy probablemente tiene el rol Charging Manager…»** | El vehículo ha rechazado por falta de derechos un comando reservado al rol Owner (bloqueo, desbloqueo, claxon, luces, modo Centinela, maleteros, climatización): su llave tiene muy probablemente el rol Charging Manager. | Vea [Rol de la llave](#rol-de-la-llave): empareje una llave Owner. |
| **«Comando rechazado por el vehículo (¿rol de la llave del proxy insuficiente?): …»** | Fallo de autorización en otro comando: rol de llave insuficiente o estado del vehículo. | Vea [Rol de la llave](#rol-de-la-llave); con una llave Owner, compruebe el estado del vehículo. |
| **«Comando rechazado por el vehículo: …»** | El vehículo ha rechazado el comando; el motivo devuelto sigue al mensaje. | Corrija según el motivo indicado. |
| **«Proxy inaccesible, comando no enviado»** | El proxy no responde: el comando no ha salido. | Compruebe la URL y la alimentación de la Raspberry Pi. |
| **«Tiempo de espera agotado: el comando puede haberse ejecutado, compruebe el estado del vehículo»** o **«Enlace con el proxy interrumpido: el comando puede haberse ejecutado…»** | Puede que el vehículo haya ejecutado el comando de todos modos. | Compruebe el estado del vehículo antes de volver a enviarlo. |
| **«Proxy ocupado: comando no enviado, inténtelo de nuevo en un momento»** | Otro comando o lectura ocupa el proxy desde hace casi 2 minutos. | Inténtelo de nuevo. |
| **«Maletero ya abierto o en movimiento: comando no enviado»** | Antes de abrir el maletero trasero, el plugin lo ha leído abierto, entreabierto o en movimiento: un comando de alternancia podría cerrarlo. | No hay nada que hacer: cierre el maletero si hace falta y vuelva a lanzar la acción (vea [Abrir el maletero trasero y el maletero delantero](#abrir-el-maletero-trasero-y-el-maletero-delantero)). |
| **«Estado del maletero desconocido: comando no enviado»** | El vehículo no da un estado utilizable para el maletero trasero: el plugin no envía nada por prudencia. | Lance **Actualizar** y luego la acción; si el estado sigue siendo desconocido, abra el maletero a mano. |
| **«Estado del maletero ilegible, comando no enviado: …»** | Ha fallado la relectura del estado antes de la apertura: la causa sigue al mensaje. | Corrija la causa (proxy, alcance Bluetooth) y vuelva a lanzar. |
| **«Valor no válido: la corriente debe ser un entero entre … y … A»** | La corriente es decimal, texto o está fuera de los límites Mín/Máx del comando. | Corrija el valor. El **Máx** sigue la corriente máxima anunciada por el vehículo; para fijarlo más alto, ajústelo a mano (el vehículo podría rechazar la consigna). |
| **«Valor no válido: el límite debe ser un entero entre X e Y %»** | Límite fuera de los límites del comando (los del vehículo, o de 50 a 100 % mientras no haya publicado ninguno) o no entero. | Corrija el valor. |
| **«Valor no válido: el modo Centinela debe ser activado o desactivado»** | Valor distinto de **Activado** o **Desactivado** (la antigua opción «Ninguno» ya no existe). | Utilice **Activado** o **Desactivado**. |
| **«Valor no válido: el nivel de calefacción debe ser un entero entre 0 y 3»** o **«Valor no válido: la calefacción del volante debe ser 0 (apagado) o 1 (encendido)»** | Un escenario envía un valor fuera de la lista del comando de calefacción de un asiento o del volante. | Utilice los niveles de la lista (vea [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante)). |
| **«Valor no válido: el desempañado máximo debe ser 0 (apagado) o 1 (encendido)»** | Un escenario envía un valor fuera de la lista del comando **Desempañado máximo**. | Utilice 0 (Apagado) o 1 (Encendido) (vea [Desempañado máximo](#desempanado-maximo)). |
| **«Valor no válido: el modo de mantenimiento de clima debe ser 0 (apagado), 1 (mantenimiento), 2 (perro) o 3 (camping)»** | Un escenario envía un valor fuera de la lista del comando **Modo de mantenimiento de clima**. | Utilice 0 (Apagado), 1 (Mantenimiento), 2 (Modo perro) o 3 (Modo camping) (vea [Modo perro, camping y mantenimiento de clima](#modo-perro-modo-camping-y-mantenimiento-de-clima)). |
| **«Fallo del comando: …»** | Otra causa (proxy sin llave, vehículo fuera de alcance, respuesta no válida…): la causa sigue al mensaje. | Vea la tabla **Último error** más arriba. |
| **«No compatible con su versión del proxy»** | El comando (por ejemplo **Abrir el maletero trasero**, **Abrir el maletero delantero**, **Añadir una programación de carga**, **Consigna del conductor**, **Ajustar la calefacción del asiento delantero izquierdo**, **Desempañado máximo** o **Modo de mantenimiento de clima**) no existe en su proxy: no se ha enviado nada. | Instale el proxy del fork (vea [Programar la carga](#programar-la-carga), [Ajustar la consigna de temperatura](#ajustar-la-consigna-de-temperatura), [Calentar los asientos y el volante](#calefactar-los-asientos-y-el-volante), [Desempañado máximo](#desempanado-maximo) y [Modo perro, camping y mantenimiento de clima](#modo-perro-modo-camping-y-mantenimiento-de-clima)). |
| **«Valor no válido: la consigna debe ser un número entre … y … °C»** | El valor de **Consigna del conductor** o **Consigna del pasajero** no es un número, o sale del rango del control deslizante (de 15 a 28 °C, o los límites del vehículo). | Envíe un número dentro del rango indicado por el mensaje. |
| **«Días de la programación no válidos: …»** o **«Hora de inicio no válida: …»** | Los días o la hora de **Añadir una programación de carga** no tienen el formato esperado. | Corríjalos (`lun,mar,mer,jeu,ven`; `23:00`). |
| **«Coordenadas de Jeedom ausentes o no válidas: …»** | La latitud y la longitud de Jeedom no están indicadas (o valen 0 y 0). | Indíquelas en Ajustes, Sistema, Configuración, pestaña **General**. |
| **«Valor no válido: la potencia disponible debe ser un número de vatios»** | El valor enviado a **Ajustar según el excedente** no es un número (texto, variable vacía o desconocida, cálculo que falla). | Compruebe el valor del escenario: un número de vatios, por ejemplo `1800`; un valor negativo se reduce a 0 W (vea [Control según el excedente](#control-segun-el-excedente)). |
| **«Comando no compatible con el plugin»** | El comando no es uno de los del plugin (comando añadido a mano, o identificador modificado). | No modifique el identificador de los comandos del plugin. |

### Tarea del ciclo de actualización

En **Ajustes > Sistema > Motor de tareas**, la tarea **TeslaBLE::cycleRafraichissement** (cada minuto, tiempo límite de 5 minutos) lanza la actualización de los vehículos. Se crea al activar y al actualizar el plugin, y se vuelve a poner en la hora siguiente si se ha eliminado; una tarea que usted mismo desactive sigue desactivada.

- **Ya no se actualiza ningún vehículo**: compruebe que la tarea existe y que está activada. Si falta, **desactive y vuelva a activar el plugin** para recrearla. Un mensaje de error «Tâche de rafraîchissement non installée» (*Tarea de actualización no instalada*) en el log del plugin señala un fallo de creación. Un mensaje «Tâche de rafraîchissement non supprimée» (*Tarea de actualización no eliminada*) al desactivar el plugin pide eliminar **TeslaBLE::cycleRafraichissement** a mano en el motor de tareas.
- **Desactivar** el plugin elimina la tarea (si no, el motor de tareas registraría un error cada minuto); al reactivarlo se recrea. Sus dispositivos, comandos y ajustes no se tocan.
- **Vuelta a una versión anterior del plugin** (por ejemplo de la beta a la estable): esa versión no conoce la tarea y el log **cron** de Jeedom muestra un error «Classe ou fonction non trouvée» (*Clase o función no encontrada*) cada minuto. Elimine entonces la tarea **TeslaBLE::cycleRafraichissement** a mano en el motor de tareas.

### Tareas puntuales de relectura

En **Ajustes > Sistema > Motor de tareas**, puede ver pasar tareas **TeslaBLE::relectureApresCommande**: una por comando con éxito (vea [Relectura tras un comando](#relectura-tras-un-comando)). Se eliminan solas una vez hecha o abandonada la relectura; no las toque. Una tarea que haya quedado ahí (Jeedom reiniciado durante la espera) la retira el siguiente comando con éxito. **Desactivar** el plugin retira todas estas tareas. Un mensaje «Tâches de relecture non supprimées» (*Tareas de relectura no eliminadas*) en el log pide eliminarlas a mano.

### Despertar y frecuencia

| Síntoma | Causa | Acción |
|---|---|---|
| **El vehículo ya no se duerme** | Una de las causas siguientes lo mantiene despierto: la casilla **Dejar que el vehículo se duerma** está desmarcada; la **Duración de la ventana** no supera el intervalo de actualización (la ventana no tiene entonces efecto); un ocupante o una llave de teléfono cerca; una carga en curso (la ventana nunca se abre durante la carga); el modo Centinela; otro servicio que consulta el vehículo (aplicación de Tesla, evcc, otra integración); un intervalo muy corto; un escenario que lanza **Actualizar (con despertar)** o **Despertar** en bucle. | Marque la casilla, elija una duración de ventana superior al intervalo, alargue el intervalo, desactive el modo Centinela si es posible, compruebe los escenarios. Ponga el log en **Info**: la línea «fenêtre d'endormissement ouverte pour … min» (*ventana de sueño abierta durante … min*) confirma que la ventana se abre; si no, uno de los criterios anteriores lo impide. El efecto sobre el sueño no está garantizado: depende del vehículo. |
| **Los valores de carga y de climatización no cambian durante la noche** | Es normal: el vehículo duerme (el plugin no lo despierta) o la ventana de sueño está abierta. **Última lectura de los datos** se queda fija y **Antigüedad de los datos (min)** aumenta. **Último error** se queda en **Ninguna**. | No hay nada que hacer. Para tener valores actualizados enseguida, lance **Actualizar (con despertar)** (despierta el vehículo). Si quiere lecturas permanentes, desmarque **Dejar que el vehículo se duerma**, aceptando el impacto en la batería. |
| **El valor mostrado tras un comando es el antiguo** | El proxy guarda sus datos **30 segundos** en caché: la relectura programada tras el comando espera ese plazo. Otras causas: el proxy estaba ocupado (relectura abandonada, la lectura periódica lo recupera), el vehículo se ha vuelto a dormir (se conservan los últimos valores), la caché del proxy se ha alargado más allá del **Retardo de relectura tras un comando**, o el motor de tareas de Jeedom está desactivado. | Espere 30 segundos. Si la caché de su proxy es más larga, alargue el **Retardo de relectura tras un comando** en la misma medida. Si no, lance **Actualizar** (o **Actualizar (con despertar)** para un vehículo dormido). Vea [Relectura tras un comando](#relectura-tras-un-comando). |
| **«Actualización con despertar fallida: …»** en **Último error** | La causa (vehículo fuera de alcance, proxy inaccesible, vehículo que se niega a despertar…) sigue al mensaje. Los valores conservan su último estado. | Lea la causa, corríjala y vuelva a lanzar. Vea la tabla **Último error** más arriba. |
| **«Tiempo de espera agotado durante el despertar del vehículo: puede haberse despertado, vuelva a intentarlo en un momento»** | El despertar y la lectura han superado 75 segundos. | Lance **Actualizar (con despertar)** de nuevo en un momento. |
| **«Proxy ocupado: lectura del vehículo no realizada, inténtelo de nuevo en un momento»** | El proxy estaba ocupado con un comando o una lectura durante más de 110 segundos. | Lance **Actualizar** (o **Actualizar (con despertar)**) de nuevo en un momento. |
| **Antigüedad de los datos (min)** vale **99999** | No se conoce ninguna lectura de datos con éxito (dispositivo nuevo, plugin actualizado, vehículo dormido desde la instalación). | Lance **Actualizar (con despertar)** una primera vez; la información pasa a 0. |
| **El intervalo durante la carga no se respeta** | La aceleración solo empieza en la primera lectura que ve la carga; un vehículo dormido en carga, una carga suspendida o un proxy cuya caché supera los 60 segundos limitan también el efecto (vea [Lectura acelerada durante la carga](#lectura-acelerada-durante-la-carga)). | Espere un intervalo normal, o lance **Actualizar**. |

Las advertencias del log vinculadas a estos ajustes (valor de **Intervalo durante la carga** reducido a 1 minuto o desactivado, **Retardo de relectura tras un comando** reducido a 30 segundos, ciclo más largo que el intervalo ajustado, tareas de actualización o de relectura no instaladas o no eliminadas) se describen en [Mensajes del log del plugin](#mensajes-del-log-del-plugin) y [Tarea del ciclo de actualización](#tarea-del-ciclo-de-actualizacion). Las líneas **Info** de apertura y de fin de la ventana de sueño se describen en [Dejar que el vehículo se duerma](#dejar-que-el-vehiculo-se-duerma).

### Mensajes del log del plugin

- **«Cycle de rafraîchissement sauté : le cycle précédent n'est pas terminé. »** (*Ciclo de actualización omitido: el ciclo anterior no ha terminado.*): usted ha lanzado la tarea a mano (**Ajustes > Sistema > Motor de tareas**) mientras un ciclo estaba en marcha. Jeedom, por su parte, nunca vuelve a lanzar por sí mismo una tarea en curso (vea los dos mensajes siguientes).
- **«… pilotage selon le surplus : … courant calculé N A, cible M A, décision `…` (motif) »** (Debug) (*control según el excedente: … corriente calculada N A, objetivo M A, decisión `…` (motivo)*): el detalle de cada llamada a **Ajustar según el excedente** (ningún VIN); **«appel ignoré, un ajustement est déjà en cours »** (*llamada ignorada, ya hay un ajuste en curso*): otra llamada del mismo vehículo no había terminado. **«pilotage selon le surplus impossible, aucune commande envoyée : … »** (Advertencia, una vez por hora como máximo) (*control según el excedente imposible, ningún comando enviado: …*): fallo interno antes del envío, por ejemplo de la caché de Jeedom; el escenario no se interrumpe.
- **«… charge aux heures creuses : décision `…` (motif) »** (Info al cambiar de motivo, Debug después; ningún VIN) (*carga en horas valle: decisión `…` (motivo)*): lo que el plugin ha decidido tras la lectura (`charge_start`, `charge_stop`, `aucune` o `ignorer`, con el motivo: `demarrage`, `cible_atteinte`, `fin_plage`, `en_charge`, `charge_perimee`, `limite_vehicule`, `suspendue_manuel`…). **«commande `…` en échec (N sur 3) »** (Advertencia en el primer fallo y en la suspensión) (*comando `…` fallido (N de 3)*); **«commande `…` reportée au prochain passage (proxy occupé | budget du cycle atteint) »** (Advertencia, una vez por hora como máximo) (*comando `…` aplazado al siguiente paso (proxy ocupado | presupuesto del ciclo alcanzado)*): no se ha enviado nada, el plugin lo reintenta en la lectura siguiente; **«pilotage impossible, aucune commande envoyée : … »** (Advertencia, una vez por hora como máximo) (*control imposible, ningún comando enviado: …*): fallo interno antes del envío, por ejemplo de la caché de Jeedom.
- **«Cycle de rafraîchissement de N s, plus long que l'intervalle de rafraîchissement le plus court (M min) : Jeedom a sauté le passage suivant… »** (Advertencia, una vez por hora como máximo) (*Ciclo de actualización de N s, más largo que el intervalo de actualización más corto (M min): Jeedom ha omitido el paso siguiente…*): un ciclo ha durado más que el intervalo ajustado, en general porque el proxy o la Raspberry Pi responde despacio; no se mantiene la frecuencia ajustada. Alargue el intervalo del vehículo afectado (o su intervalo durante la carga), reparta los vehículos entre varios proxies, o compruebe la alimentación y la conexión Wi-Fi de la Raspberry Pi.
- **«Cycle de rafraîchissement de N s : Jeedom a sauté le passage de la minute suivante, sans cumul de cycles. »** (Debug) (*Ciclo de actualización de N s: Jeedom ha omitido el paso del minuto siguiente, sin acumulación de ciclos.*): un ciclo ha superado un minuto aunque todos los intervalos ajustados son más largos; no hay nada que hacer.
- **«Cycle de rafraîchissement écourté… véhicule(s) non lu(s) à ce cycle »** (*Ciclo de actualización acortado… vehículo(s) no leído(s) en este ciclo*): el ciclo ha alcanzado su duración máxima de 4 minutos; los vehículos citados no se han leído en este ciclo. Se leerán en el ciclo siguiente si el proxy responde con normalidad; hasta 3 vehículos por proxy, el ciclo no se acorta, más allá compruebe la **Última lectura de los datos** de cada vehículo. La advertencia se emite **una sola vez por episodio** (precisa «Avertissement non répété jusqu'au prochain cycle complet. » (*Advertencia no repetida hasta el próximo ciclo completo.*)), aunque el episodio dure varias horas; si se repite, el proxy responde demasiado despacio: vea más arriba.
- **«Cycle de rafraîchissement de nouveau complet : … »** (Info) (*Ciclo de actualización de nuevo completo: …*): fin de un episodio de ciclo acortado; se han leído todos los vehículos.
- **«Véhicule … traité en … s. »** (Debug) (*Vehículo … procesado en … s.*): duración de la lectura de cada vehículo en el ciclo, incluido un vehículo omitido (proxy ocupado, la línea «sautée» (*omitida*) la precede) o con error. Las líneas **Requête** (*Solicitud*) y **Réponse HTTP … en … ms** (*Respuesta HTTP … en … ms*) dan el detalle de las llamadas; la línea Réponse recuerda su solicitud (método y dirección), porque las líneas de varios proxies leídos en paralelo se entremezclan en el log.
- **«Lecture du véhicule … reportée : proxy occupé… »** (*Lectura del vehículo … aplazada: proxy ocupado…*): un **Actualizar** ha esperado más de 110 segundos a un proxy ocupado con un comando o una lectura; la lectura no se ha hecho y el mensaje **Proxy ocupado: lectura del vehículo no realizada…** aparece en **Último error**.
- **«Lecture du véhicule … sautée : une commande ou une lecture est en cours vers le proxy. »** (Debug) (*Lectura del vehículo … omitida: hay un comando o una lectura en curso hacia el proxy.*): el ciclo automático se aparta ante el intercambio en curso; la lectura se hace en el ciclo siguiente.
- **«Proxy obtenu pour le véhicule … après … s d'attente… »** (Debug) (*Proxy obtenido para el vehículo … tras … s de espera…*): un comando o una lectura esperaba el proxy desde hacía al menos un segundo.
- **«Verrou du proxy indisponible… »** o **«Verrou du cycle de rafraîchissement indisponible… »** (*Bloqueo del proxy no disponible…* / *Bloqueo del ciclo de actualización no disponible…*): el plugin no puede escribir en la carpeta temporal de Jeedom. Compruebe los permisos de esa carpeta; el plugin sigue funcionando sin la protección contra los intercambios simultáneos.
- **«Commandes : … le nom … est déjà pris… »** (*Comandos: … el nombre … ya está en uso…*): el plugin no ha podido dar la etiqueta prevista a un comando porque otro comando del dispositivo la tiene. Cambie el nombre de uno de los dos y luego guarde el dispositivo.
- **«Adaptateur Bluetooth du proxy probablement figé pour le véhicule … »** (advertencia) (*Adaptador Bluetooth del proxy probablemente bloqueado para el vehículo …*) y **«Adaptateur Bluetooth du proxy de nouveau opérationnel pour le véhicule … »** (Info) (*Adaptador Bluetooth del proxy de nuevo operativo para el vehículo …*): inicio y fin de un episodio, vea [Alerta de adaptador Bluetooth bloqueado](#alerta-de-adaptador-bluetooth-bloqueado).
- **«Véhicule … : fenêtre d'endormissement ouverte pour … min après … lecture(s) inchangée(s), hors charge… »** (Info) (*Vehículo …: ventana de sueño abierta durante … min tras … lectura(s) sin cambios, fuera de carga…*): el plugin deja de leer los datos de carga y de climatización hasta la hora indicada; vea [Dejar que el vehículo se duerma](#dejar-que-el-vehiculo-se-duerma). **«fin de la fenêtre d'endormissement après … min : … »** (Info) (*fin de la ventana de sueño tras … min: …*) da la razón de la reanudación (actividad constatada con el campo modificado, comando, actualización solicitada, ajuste desactivado, duración transcurrida, vehículo fuera de alcance); **«… : véhicule endormi après … min de fenêtre. »** (*…: vehículo dormido tras … min de ventana.*) señala que el vehículo se ha dormido. En Debug: «lecture des données suspendue» (*lectura de los datos suspendida*), «lecture de contrôle» (*lectura de control*), «prolongée» (*prolongada*).
- **«Véhicule … en charge (Charging), intervalle pendant la charge appliqué : N min au lieu de M. »** y **«Véhicule … : état de charge …, intervalle normal rétabli : M min. »** (Debug) (*Vehículo … en carga (Charging), intervalo durante la carga aplicado: N min en lugar de M.* / *Vehículo …: estado de carga …, intervalo normal restablecido: M min.*): inicio y fin de la lectura acelerada, vea [Lectura acelerada durante la carga](#lectura-acelerada-durante-la-carga). Una **advertencia** «intervalle pendant la charge inférieur au plancher d'une minute» (*intervalo durante la carga inferior al mínimo de un minuto*) o «… invalide, réglage désactivé» (*… no válido, ajuste desactivado*) señala un valor corregido al guardar.
- **«Véhicule … : relecture programmée dans N s (commande …). »** (*Vehículo …: relectura programada en N s (comando …).*), **«… : lecture sans réveil. »** (*…: lectura sin despertar.*), **«Relecture du véhicule … remplacée par une commande plus récente. »** (*Relectura del vehículo … sustituida por un comando más reciente.*), **«… abandonnée : proxy occupé… »** (*… abandonada: proxy ocupado…*) y **«Relecture ignorée : … »** (*Relectura ignorada: …*) (Debug): desarrollo de una relectura tras un comando, vea [Relectura tras un comando](#relectura-tras-un-comando). No hay nada que hacer.
- **«Véhicule … : relecture non programmée : … »** (advertencia, una vez por hora como máximo) (*Vehículo …: relectura no programada: …*): no se ha podido crear la tarea de relectura; el comando ha tenido éxito y los valores estarán actualizados en la lectura siguiente. Si el mensaje vuelve, compruebe el motor de tareas de Jeedom.
- **«Équipement … : délai de relecture après commande invalide, ramené à 30 secondes. »** (advertencia) (*Dispositivo …: retardo de relectura tras un comando no válido, reducido a 30 segundos.*): se ha guardado un valor fuera de la lista (por un script, una API o una restauración); elija un retardo de la lista del dispositivo.
- **«Véhicule … : le proxy annonce désormais … ; information(s) créée(s) : … »** (Info) (*Vehículo …: el proxy anuncia ahora …; información(es) creada(s): …*): tras un cambio de versión del proxy, el plugin ha creado las informaciones de datos ampliados que han pasado a estar disponibles (vea [Datos ampliados: qué está disponible](#datos-ampliados-que-esta-disponible)). **«… informations de données étendues non créées …, nouvel essai à la prochaine lecture de ces données »** (advertencia, una vez por hora como máximo) (*… informaciones de datos ampliados no creadas …, nuevo intento en la próxima lectura de estos datos*): la creación ha fallado (error de registro de Jeedom); se reintenta sola, o con **Guardar** en el dispositivo.
- **«Véhicule … : fonction `donnees:…` refusée par le proxy (not supported), indisponible jusqu'au prochain changement de version du proxy. »** (Info) (*Vehículo …: función `donnees:…` rechazada por el proxy (not supported), no disponible hasta el próximo cambio de versión del proxy.*): el proxy ha rechazado una categoría que anunciaba; el plugin ya no la solicita antes de una actualización del proxy. **«Capacités du proxy du véhicule … : version …, origine …, action(s) indisponible(s) : … »** (Info) (*Capacidades del proxy del vehículo …: versión …, origen …, acción(es) no disponible(s): …*): lectura de lo que anuncia el proxy, al cambiar de versión.
- **«Lecture de la position (ou des pressions des pneus, ou de la mise à jour logicielle) du véhicule … en échec : … »** (advertencia, una vez por episodio) (*Lectura de la posición (o de las presiones de los neumáticos, o de la actualización de software) del vehículo … fallida: …*) y **«… rétablie. »** (Info) (*… restablecida.*): el vehículo o el proxy ha rechazado esa lectura. Las demás lecturas no se ven afectadas y **Último error** no se modifica. En Debug, **«Position (ou Pressions des pneus, ou Mise à jour logicielle) du véhicule … non lue(s) : … »** (*Posición (o Presiones de los neumáticos, o Actualización de software) del vehículo … no leída(s): …*) da el motivo de una lectura no hecha (vehículo dormido, fuera de alcance, presupuesto de lectura alcanzado, ninguna información en el dispositivo) y **«Position du véhicule … inchangée : … »** (*Posición del vehículo … sin cambios: …*) el de una posición ignorada (desfasada, 0/0, fuera de rango); nunca figura ninguna coordenada en ellos.
- **«Tuile du véhicule … : rendu impossible, widget standard affiché (…) »** (Error) (*Mosaico del vehículo …: representación imposible, widget estándar mostrado (…)*): el mosaico no se ha podido dibujar; Jeedom muestra en su lugar el widget estándar. Anote el motivo entre paréntesis; desmarcar **Plantilla de widget** en la **Configuración avanzada** suprime el mensaje (vea [Mosaico del vehículo](#mosaico-del-vehiculo)).
- **«Image du véhicule … non posée : image du modèle … absente ou illisible dans le plugin (réinstallez le plugin) ; … »** (Advertencia) (*Imagen del vehículo … no colocada: imagen del modelo … ausente o ilegible en el plugin (reinstale el plugin); …*): falta el archivo de imagen suministrado con el plugin o está dañado. Reinstale el plugin. **«… non posée : dossier data/eqLogic de Jeedom non accessible en écriture ; … »** (Advertencia) (*… no colocada: carpeta data/eqLogic de Jeedom sin acceso de escritura; …*): Jeedom no puede escribir su imagen; compruebe los permisos de la carpeta `data/eqLogic` de Jeedom. En ambos casos, el icono del plugin (o la imagen actual) sigue mostrándose. **«Image du véhicule … non posée : … »** (*Imagen del vehículo … no colocada: …*) seguido de otro motivo (Advertencia): la escritura ha fallado; el dispositivo no se modifica. **«… retirée : le modèle n'a plus d'image. »** (Debug) (*… retirada: el modelo ya no tiene imagen.*): el VIN designa ahora un modelo sin imagen.
- **«Migrations : … »** (*Migraciones: …*): vea [Comprobar la actualización en el log](#comprobar-la-puesta-al-dia-en-el-log).

### Lectura lenta del proxy

El plugin mide la duración de cada lectura, sin ninguna petición adicional, y la publica en **Duración de la lectura del estado** y **Duración de la lectura de los datos**. Cuando una lectura correcta supera los **10 segundos** (estado) o los **20 segundos** (datos), el log recibe **una sola** advertencia **«Lecture lente du proxy pour le véhicule … »** (*Lectura lenta del proxy para el vehículo …*), que no se repite mientras la lectura siga siendo lenta. Cuando la duración vuelve a **7 segundos** (estado) o **14 segundos** (datos), una línea **Info** «Lecture du proxy redevenue normale… » (*Lectura del proxy de nuevo normal…*) lo indica. Estos umbrales son fijos.

Causas habituales: Raspberry Pi demasiado alejada del vehículo (pared, suelo de hormigón, coche aparcado lejos), Raspberry Pi saturada (otro cliente del proxy, como evcc, la mantiene ocupada) o con una alimentación deficiente. Acerque la Raspberry Pi o cambie su alimentación y observe después la duración en los ciclos siguientes.

Una lectura fallida (proxy inaccesible, tiempo de espera agotado) no modifica estas informaciones: su duración aparece en el mensaje de fallo del log («… après 25.0 s : … » (*… tras 25.0 s: …*)). La duración de un comando se escribe en el log en nivel **Debug** («Commande … exécutée en 3.2 s. » (*Comando … ejecutado en 3.2 s.*)).

### Proxy del fork: token, adaptador, cuerpo rechazado

| Lo que ve | Causa | Acción |
|---|---|---|
| **«Token de API rechazado por el proxy»** en **Último error**, o **«Token de API rechazado por el proxy: comando no enviado»** al enviar un comando | El proxy del fork tiene un `apiToken` y el plugin no tiene token o tiene uno distinto. La presencia del vehículo no se modifica; el log recibe **una sola** línea **Error** por episodio. | Introduzca el valor exacto de `apiToken` en **Token de API del proxy**, **Guardar** y luego **Probar** («Token de API aceptado por el proxy»). |
| **«Token de API no válido: …»** o **«Token de API no compatible con Jeedom …»** | El token introducido contiene un carácter no admitido (acento, salto de línea, más de 256 caracteres) o una forma que Jeedom no sabe almacenar. | Genere otro token (`openssl rand -hex 32`) y cópielo en `apiToken` y en el plugin. |
| **Proxy inaccesible** aunque la Raspberry Pi esté encendida | El proxy del fork se detiene al arrancar si `btAdapter` no es válido o si el adaptador no existe; Docker lo reinicia en bucle. | En la Raspberry Pi, `docker logs tesla-ble-http-proxy`: busque `Cannot start with this Bluetooth adapter`. Corrija o elimine `btAdapter` (vea [Instalar el proxy BLE](installation-proxy.md#12-solucion-de-problemas)). |
| **«Comando rechazado por el vehículo: invalid request body: …»** | El proxy del fork ha rechazado el contenido del comando antes de enviarlo. | El texto tras los dos puntos nombra la clave implicada; comuníquelo junto con el log del plugin en Debug. |

### Mensajes de la ventana Logs del proxy

| Mensaje | Causa | Acción |
|---|---|---|
| **«Logs no disponibles (se requiere proxy ≥ 2.3.0)»** | El servidor de la URL registrada no ofrece logs: proxy anterior a 2.3.0, o URL que no designa al proxy. | Compruebe la URL con el botón **Probar** y actualice el proxy si su versión es inferior a 2.3.0. |
| **«Proxy inaccesible: compruebe que está iniciado y luego su dirección con el botón Probar»** | El proxy está detenido, la Raspberry Pi apagada o la dirección es incorrecta. | Inicie el proxy y compruebe después la URL con **Probar**. |
| **«URL del proxy ausente o no válida: indíquela, guarde y vuelva a abrir los logs»** | No hay ninguna URL válida registrada. | Indique la URL, guarde y vuelva a abrir la ventana. |
| **«Token de API rechazado por el proxy»** | El proxy del fork tiene un `apiToken` que el plugin no envía o que es distinto. | Introduzca el token (vea la tabla anterior). |
| Mensaje de fallo seguido de **«réponse HTTP 500 au lieu de 200 : Failed to encode logs »** (*respuesta HTTP 500 en lugar de 200: Failed to encode logs*) | El proxy ya no consigue releer su propia memoria de logs (fallo conocido del proxy). | Reinicie el proxy (`docker compose restart` en la Raspberry Pi). |
| **«Ninguna línea de log en el proxy»** | El proxy todavía no ha registrado nada. | Actualice tras un ciclo del plugin. |

### Carga avanzada: síntomas sin mensaje

Ponga el log del plugin en **Debug**: las líneas **«pilotage selon le surplus : … décision … (motif) »** (*control según el excedente: … decisión … (motivo)*) y **«charge aux heures creuses : décision … (motif) »** (*carga en horas valle: decisión … (motivo)*) dan la razón de cada decisión (vea [Mensajes del log del plugin](#mensajes-del-log-del-plugin)).

| Síntoma | Causas posibles | Acción |
|---|---|---|
| **La corriente de carga no cambia** (control según el excedente) | La corriente objetivo es idéntica a la última consigna o se aparta de ella menos que la **Histéresis** (motivos `identique`, `hysteresis`); no ha transcurrido el **Intervalo mínimo entre comandos** (contado desde el **final** del comando anterior); la corriente objetivo se limita al **Máx** del cursor **Corriente de carga** (límite del vehículo o valor ajustado a mano); el vehículo no está conectado, está fuera de alcance o la carga ha finalizado (vea **Último error**); **Intervalo durante la carga** desactivado: el **Estado de la carga** leído es antiguo; el intervalo de **Carga en horas valle** está en curso (la llamada se ignora); **Fases** ajustado a Monofásico con un punto de carga trifásico. | Lea la línea Debug «decisión … (motivo)»; reduzca la histéresis o el intervalo mínimo si los cambios son demasiado escasos; ponga **Intervalo durante la carga** en 1 minuto; compruebe **Tensión de la red** y **Fases**; verifique el **Máx** del cursor en la pestaña **Comandos**. |
| **La carga se detiene por la noche** (control según el excedente) | Sin producción, la potencia enviada cae a 0 W: la corriente calculada queda por debajo del **Umbral de parada** y la carga se detiene tras la **Duración de mantenimiento antes de la parada**. | Es normal. Para cargar por la noche, utilice la **Carga en horas valle** (el control según el excedente se ignora entonces durante el intervalo). |
| **La carga no se reanuda por la mañana** (control según el excedente) | La corriente calculada no alcanza la **Corriente mínima de arranque**; el arranque se hace en dos tiempos (**Corriente de carga** y luego **Iniciar la carga**, en el intervalo siguiente); el vehículo está desconectado o su estado de carga es desconocido; el escenario ya no está programado o su guarda de frescura (**Antigüedad de los datos (min)**) es falsa. | Compruebe la potencia enviada en la línea Debug, espere uno o dos intervalos y revise el escenario. Si el estado de carga es desconocido: **Actualizar (con despertar)**. |
| **La carga en horas valle no se inicia** | La función no está marcada o falta un campo; la hora actual (**hora de Jeedom**, no la del vehículo) está fuera del intervalo; el vehículo no está conectado o el punto de carga no suministra corriente (vea **Último error**); el **SoC objetivo** es inferior o igual al nivel actual de la batería (objetivo ya alcanzado); el **límite de carga del vehículo** es inferior o igual al nivel actual (carga finalizada); el control está **suspendido hasta el intervalo siguiente** (acción manual desde Jeedom, carga reanudada desde la aplicación, 3 fallos de comando o arranque ya intentado sin carga constatada); un vehículo dormido solo se ve con un estado obsoleto; el intervalo de actualización es largo (la decisión solo se toma en una lectura). | Compruebe los ajustes y la zona horaria de Jeedom; lea la línea Info «charge aux heures creuses : décision … (motif) » (*carga en horas valle: decisión … (motivo)*) (por ejemplo `suspendue_manuel`, `limite_vehicule`, `cible_atteinte`, `hors_plage`); consulte **Último error**; lance **Actualizar (con despertar)** si el estado está obsoleto; desconectar y volver a conectar el vehículo reactiva un control suspendido tras varios fallos. |
| **Un comando se rechaza o se ignora** | **Rechazado**: **«Este comando requiere una llave con rol Owner…»** o **«Comando rechazado por el vehículo (¿rol de la llave del proxy insuficiente?) …»** (vea [Rol de la llave](#rol-de-la-llave): el control según el excedente y las horas valle solo exigen Charging Manager); **«No compatible con su versión del proxy»** (programación de carga: se requiere el proxy del fork); **«Valor no válido: …»** (valor fuera de límites o no numérico). **Ignorado** (ningún error, ningún comando): abstenciones del control según el excedente o de la carga en horas valle (**Último error** indica la razón: vehículo no conectado, fuera de alcance, carga finalizada, punto de carga sin corriente, estado de carga desconocido) y llamada a **Ajustar según el excedente** durante el intervalo de las horas valle. | Vea las tablas **Último error** y **Error al enviar un comando** más arriba. |

### Clima y confort: síntomas sin mensaje

Ponga el log del plugin en **Debug**: la línea **«préconditionnement planifié : décision … (motif) »** (*preacondicionamiento planificado: decisión … (motivo)*) da la razón de cada decisión del preacondicionamiento planificado (vea [Mensajes del log del plugin](#mensajes-del-log-del-plugin)).

| Síntoma | Causas posibles | Acción |
|---|---|---|
| **Falta un comando de confort en el widget** (consigna, asientos, volante, desempañado máximo, mantenimiento de clima) | Estos comandos se crean **ocultos**, incluso con el proxy del fork. | Marque **Mostrar** en cada uno en la pestaña **Comandos** del dispositivo (vea [Clima y confort: qué está disponible](#clima-y-confort-que-esta-disponible)). |
| **El comando se rechaza de inmediato con «No compatible con su versión del proxy»** | El proxy no lo anuncia: proxy oficial 2.3.0 o versión del fork demasiado antigua (`2.3.0-tb.1` como mínimo para la consigna de temperatura, el desempañado máximo y el mantenimiento de clima, `2.3.0-tb.2` para los asientos y el volante). | Instale o actualice el proxy del fork; no hace falta reinstalar el plugin. Compruebe **Versión del proxy** y vuelva a lanzar el comando. |
| **El comando se acepta pero no cambia nada** | **Asiento** ausente del vehículo, aceptado sin efecto (releído a 0); **climatización apagada**: la calefacción de los asientos suele requerirla; **volante con calefacción automática**; **Leer también la climatización** en **No, solo carga**: las informaciones no se releen y conservan el valor anunciado; el vehículo se ha vuelto a dormir antes de la relectura. | Encienda la climatización, deje **Leer también la climatización** en **Sí**, lance **Actualizar (con despertar)** y vuelva a leer el valor (estos comportamientos están por validar en uso real). |
| **El comando se rechaza con un mensaje de rol** | Llave del proxy con rol Charging Manager: el vehículo rechaza las acciones de confort. | Empareje una llave **Owner** (vea [Rol de la llave](#rol-de-la-llave)). |
| **El preacondicionamiento planificado no se inicia** | Función no marcada; **día** de salida no marcado (cuenta el día de la hora de salida); **intervalo de actualización** más largo que la duración de la ventana (ninguna lectura cae en ella); con **Solo si está conectado**, vehículo desconectado; climatización **ya en marcha** (motivo `deja_active`); **Leer también la climatización** en **No, solo carga** (rechazado al guardar); vehículo fuera de alcance o no leído; control **suspendido** hasta la salida siguiente (acción manual desde Jeedom, 3 fallos de comando o llave Charging Manager: un solo intento por salida). | Compruebe los ajustes y la zona horaria de Jeedom; reduzca el intervalo de actualización (se aconsejan 5 minutos como máximo); lea la línea **Info** «préconditionnement planifié : décision … (motif) » (*preacondicionamiento planificado: decisión … (motivo)*) (por ejemplo `hors_fenetre`, `deja_active`, `suspendue_manuel`) y **Último error**; empareje una llave **Owner** si hace falta. |
| **La climatización arranca tarde o no se detiene a la hora** | La decisión solo se toma en una lectura del vehículo: el arranque y la parada siguen la frecuencia de lectura. Un vehículo visto dormido nunca recibe una parada. | Reduzca el intervalo de actualización; detenga la climatización desde Jeedom si hace falta. |
| **Un desempañado máximo o un mantenimiento de clima no se detiene** | El plugin nunca los detiene por sí mismo; el preacondicionamiento planificado tampoco los sustituye ni los detiene. | Envíe **Apagado** desde el widget o un escenario. |

Los mensajes mostrados para estas funciones (**Valor no válido: …**, **Preacondicionamiento planificado: …**, **Vehículo no conectado: preacondicionamiento planificado no iniciado**, **No compatible con su versión del proxy**) se describen en [Mensajes al guardar](#mensajes-al-guardar), [Información «Último error» (lectura)](#informacion-ultimo-error-lectura) y [Error al enviar un comando](#error-al-enviar-un-comando).

### Aperturas y seguridad: síntomas sin mensaje

Mensajes de esta función: **«Maletero ya abierto o en movimiento…»**, **«Estado del maletero desconocido…»**, **«Estado del maletero ilegible…»** y **«No compatible con su versión del proxy»** en [Error al enviar un comando](#error-al-enviar-un-comando); el rechazo de una duración de alerta en [Mensajes al guardar](#mensajes-al-guardar); los mensajes de alerta en [Centro de mensajes de Jeedom (tras una actualización)](#centro-de-mensajes-de-jeedom-tras-una-actualizacion); el rechazo de rol en [Rol de la llave](#rol-de-la-llave).

| Síntoma | Causas posibles | Acción |
|---|---|---|
| **Una apertura se queda en 0 aunque está abierta** | El vehículo duerme: el estado no se relee y se conserva el último valor; un estado desconocido deja el último valor; proxy anterior a 2.3.0 (aperturas no publicadas); el proxy transmite las aperturas como cerradas cuando el vehículo no las proporciona. | Compruebe **Antigüedad de los datos (min)** y **Presencia del vehículo**; lance **Actualizar**; verifique **Versión del proxy** (vea [Comprobar y actualizar la versión del proxy](#comprobar-y-actualizar-la-version-del-proxy)). |
| **Centinela en «Última orden» que no sigue a la aplicación** | Proxy oficial 2.3.0 o fork demasiado antiguo: el valor es el de la última orden de Jeedom. Con el fork `2.3.0-tb.2`, un vehículo dormido también conserva su último valor leído. | Pase al proxy del fork (`2.3.0-tb.2` como mínimo) y lance **Actualizar (con despertar)**; vea [Estado del modo Centinela](#estado-del-modo-centinela). |
| **La alerta no se envía** | Alerta no activada o duración vacía (rechazada al guardar); duración aún no transcurrida (la alerta sale entre la duración y la duración más dos intervalos de actualización); proxy inaccesible, vehículo fuera de alcance o lectura fallida (no se evalúa nada); puerto de carga abierto con el vehículo conectado o cargando (no hay alerta para el puerto de carga); presencia de un ocupante o presencia desconocida (alerta «vehículo desbloqueado sin ocupante»); caché de Jeedom vaciada durante el episodio; escenario que no comprueba **Alerta de aperturas** `== 1`. | Compruebe el bloque **Alertas de apertura prolongada**, **Último error** y **Antigüedad de los datos (min)**; vea [Alertas de apertura prolongada](#alertas-de-apertura-prolongada). |
| **El mensaje de alerta sigue en el centro de mensajes** | Jeedom no retira el mensaje al cerrarse. | Elimínelo a mano. |
| **No aparece ninguna confirmación antes de una acción sensible** | La casilla **Confirmar la acción** está desmarcada en el comando; la acción se lanza desde un escenario o la API (nunca hay confirmación); el comando no es una de las cinco acciones afectadas. | Marque la casilla en los parámetros avanzados del comando; vea [Confirmación de las acciones sensibles](#confirmacion-de-las-acciones-sensibles). |
| **El maletero no aparece en el widget** | **Abrir el maletero trasero** y **Abrir el maletero delantero** se crean **ocultos**, incluso con el proxy del fork. | Marque **Mostrar** en la pestaña **Comandos** (vea [Aperturas y seguridad: qué está disponible](#aperturas-y-seguridad-que-esta-disponible)). |
| **El maletero trasero no se abre** | El plugin rechaza una puerta trasera motorizada ya abierta para no cerrarla; el vehículo ha rechazado por falta de derechos (**Rol de la llave**); proxy oficial 2.3.0. | Lea **Último error** y el mensaje mostrado; vea [Abrir el maletero trasero y el maletero delantero](#abrir-el-maletero-trasero-y-el-maletero-delantero). |

### Datos ampliados: síntomas sin mensaje

Mensajes de esta función: el rechazo del domicilio y del radio en [Mensajes al guardar](#mensajes-al-guardar), **«Función no compatible con este proxy — …»** en [Información «Último error» (lectura)](#informacion-ultimo-error-lectura), las líneas de log en [Mensajes del log del plugin](#mensajes-del-log-del-plugin).

| Síntoma | Causas posibles | Acción |
|---|---|---|
| **Kilometraje, Marcha, Velocidad, Potencia, presiones, Actualización o posición ausentes** de la pestaña **Comandos** | El proxy no anuncia la categoría (proxy oficial 2.3.0 o versión del fork demasiado antigua): las informaciones **no se crean**. | Compruebe **Versión del proxy**, instale el proxy del fork (`2.3.0-tb.2` como mínimo), espere un ciclo (nueva detección) o **Guarde** el dispositivo: vea [Datos ampliados: qué está disponible](#datos-ampliados-que-esta-disponible). |
| **Las informaciones existen pero siguen vacías** | Todavía no ha habido ninguna lectura: el vehículo duerme o está fuera de alcance, o hay una **ventana de sueño** abierta; para las presiones, la actualización y la posición, han pasado menos de 15 minutos desde el intento anterior. | Lance **Actualizar (con despertar)**; compruebe **Antigüedad de los datos (min)** y **Presencia del vehículo**. |
| **Las informaciones ya no se actualizan** tras pasar al fork | El proxy ha rechazado la categoría (línea Info «refusée par le proxy (not supported) » (*rechazada por el proxy (not supported)*) en el log); el plugin solo la vuelve a pedir en el siguiente cambio de versión del proxy. | Actualice el proxy del fork; un cambio de versión reinicia la detección. |
| **Kilometraje congelado** | Vehículo dormido (ninguna lectura, se conserva el último valor) o ventana de sueño abierta. | Es normal. **Actualizar (con despertar)** para una lectura inmediata. |
| **Presión a 0 o ausente** | Un valor nulo, negativo o superior a 10 bar se ignora: la información conserva su último valor, o queda vacía si nunca se ha leído; el vehículo no comunica la presión de un neumático. | Espere a la lectura siguiente, con el vehículo despierto; compruebe en la pantalla del vehículo. |
| **Velocidad o Potencia parecen incorrectas** | Unidades supuestas (mph y kW), no confirmadas; al estar el proxy en el garaje, estos valores casi nunca son significativos. | Compare con la pantalla del vehículo; no los use para una decisión crítica. |
| **Actualización muestra «Desconocida» o una etiqueta en bruto** | Hay una actualización activa sin versión comunicada por el vehículo («Desconocida»), o el proxy devuelve un estado que el plugin no conoce (se muestra tal cual). | No hay nada que hacer; la versión aparece en cuanto el vehículo la comunica. |
| **Modelo o Año del modelo valen «Desconocido»** | El VIN está vacío, no es el de una Tesla reconocida o su 10.º carácter no es un año descodificable. | Compruebe el **VIN** del dispositivo y **guarde**. |
| **En casa se queda en 0 (o no aparece)** | Antes del primer cálculo, el mosaico muestra 0: la información **nunca se escribe** mientras el domicilio o la posición sean desconocidos. No se ha indicado ninguna coordenada de domicilio y no hay posición en Jeedom; posición nunca leída (proxy oficial, vehículo dormido); **Radio (m)** demasiado pequeño. | Indique el **domicilio** y el **radio** en el dispositivo, o la posición de Jeedom; espere a una lectura de la posición (15 minutos como máximo). Vea [Posición y privacidad](#posicion-y-privacidad). |
| **En casa se queda en 1 aunque el vehículo se haya ido** | Fuera del alcance Bluetooth, ya no se lee ninguna posición: la información conserva su último valor. | Combine `En casa == 1` con **Presencia del vehículo** en sus escenarios. |
| **La posición no se actualiza** | Vehículo dormido o fuera de alcance; posición considerada demasiado antigua (más de una hora) o en 0/0, ignorada; menos de 15 minutos desde la lectura anterior; **Latitud** y **Longitud** eliminadas (solo **En casa** sigue calculándose). | Lance **Actualizar (con despertar)**; compruebe **Presencia del vehículo** y **Antigüedad de los datos (min)**. |
| **La latitud y la longitud aparecen en un log de Jeedom** | El log `event` de Jeedom registra cada nuevo valor de una información, incluso oculta; no es el log del plugin. | Vea [Posición y privacidad](#posicion-y-privacidad): baje el nivel del log `event` o elimine estas dos informaciones. |
| **No veo Latitud y Longitud en el widget** | Se crean **ocultas** y **sin historizar**, a propósito. | Marque **Mostrar** (y **Historizar** si hace falta) en la pestaña **Comandos**. |

### Widget y visualización: síntomas sin mensaje

Mensajes de esta función: las líneas de log en [Mensajes del log del plugin](#mensajes-del-log-del-plugin).

| Síntoma | Causas posibles | Acción |
|---|---|---|
| **Veo las viñetas de los comandos, no el mosaico** | La casilla **Plantilla de widget** está desmarcada (elección hecha, o dispositivo que tenía una disposición en tabla o un widget de comando personalizado antes de la actualización); el plugin ha tenido que recurrir al widget estándar (línea **Tuile du véhicule … rendu impossible** (*Mosaico del vehículo … representación imposible*) en el log). | Marque **Plantilla de widget** en la **Configuración avanzada**, guarde y recargue la página; vea [Restablecer el widget del plugin](#restablecer-el-widget-del-plugin). |
| **No veo la imagen del vehículo** | Modelo sin imagen (Semi, Roadster, VIN desconocido); imagen quitada por usted (retirada definitiva); widget estándar (sin imagen); carpeta de imágenes de Jeedom sin acceso de escritura o imagen del plugin ilegible (advertencia en el log). | Compruebe **Modelo** y el **VIN**; marque **Plantilla de widget**; suba su imagen en la **Configuración avanzada**. Vea [Imagen del modelo](#imagen-del-modelo). |
| **La imagen no vuelve tras «Quitar la imagen»** | La retirada es **definitiva**: el plugin nunca la vuelve a poner. | Suba la imagen que prefiera. |
| **Los comandos están desordenados, o un comando reciente está al final del todo** | El orden solo se establece en la creación y nunca se reescribe; un comando añadido por una actualización se coloca junto a su tema, o al final de la lista si ese tema no existe en el dispositivo. | Arrastre y suelte las líneas en la pestaña **Comandos** y luego **Guarde**; vea [Orden de los comandos](#orden-de-los-comandos). |
| **Ha vuelto un tipo genérico que yo había vaciado** | El comando se eliminó y se volvió a crear, o la asignación de los tipos se repitió tras una actualización interrumpida. | Vuelva a poner **Ninguno** en la configuración avanzada del comando; vea [Tipos genéricos](#tipos-genericos). |
| **Un botón del mosaico aparece en gris** | El comando correspondiente no existe en el dispositivo o su proxy no lo admite. | Compruebe la pestaña **Comandos** y **Versión del proxy** (vea [Comprobar y actualizar la versión del proxy](#comprobar-y-actualizar-la-version-del-proxy)). |
| **Un botón sigue atenuado** | El comando está en curso (un comando puede durar varias decenas de segundos). Se rearma como máximo a los 4 minutos. | Espere; si falla, lea el mensaje de Jeedom y **Último error**. |
| **El mosaico muestra «Desconocido» o «Ninguna lectura conocida»** | Todavía no ha tenido éxito ninguna lectura, o el valor no es numérico: nunca se inventa un valor. | Lance **Actualizar (con despertar)**; compruebe **Presencia del vehículo** y **Último error**. |
| **La duración «Datos de hace» no cambia mientras miro la página** | No envejece en el navegador; sigue a **Antigüedad de los datos (min)**, recalculada cada minuto. | Es normal: espere al minuto siguiente. |
| **La aplicación móvil nativa no muestra el mosaico** | El mosaico solo afecta al dashboard y a la interfaz móvil web; la aplicación se basa en los tipos genéricos. | Compruebe los tipos genéricos de los comandos; vea [Tipos genéricos](#tipos-genericos). |

### Síntomas sin mensaje

- **Proxy accesible vale 0 aunque el proxy está encendido**: el proxy responde «no encontrado» a la pregunta de estado si su versión es anterior a 2.1.3 o si la dirección no designa al proxy. Compruebe la versión y la dirección con **Probar** o **Probar este proxy** y actualice después el proxy (vea [Comprobar y actualizar la versión del proxy](#comprobar-y-actualizar-la-version-del-proxy)).
- **Presencia del vehículo se queda en 0**: el proxy no encuentra el vehículo por Bluetooth. Acerque la Raspberry Pi al vehículo.
- **La información de carga ya no se mueve aunque Último error vale Ninguno**: el vehículo duerme. Es el comportamiento normal, vea [Actualización de las informaciones](#actualizacion-de-las-informaciones).
- **Ninguna petición tiene éxito**: pruebe la URL con el botón **Probar** (el `/` final lo gestiona el plugin) y luego desde un navegador.
- **El enlace del panel de control no se abre** aunque el proxy funciona: la URL contiene un nombre de servicio Docker que su navegador no conoce. Abra `http://<ip_de_la_pi>:8080/dashboard`.
- **El gráfico de la Autonomía da un salto**: es normal tras la actualización desde la 0.x (millas y luego km), vea [Autonomía y velocidad de carga](#autonomia-y-velocidad-de-carga).
- **No veo las líneas de inicio y fin de avería en el log**: ponga el log del plugin al menos en nivel **Info**.
- **El proxy deja de responder al cabo de unas horas**: es un problema frecuente en la Raspberry Pi Zero W de primera generación. Reinicie el proxy o pase a una Raspberry Pi Zero 2 W. Si el proxy aún responde pero las lecturas agotan el tiempo de espera, el plugin se lo advierte: vea [Alerta de adaptador Bluetooth bloqueado](#alerta-de-adaptador-bluetooth-bloqueado).
- **Conexiones Bluetooth intermitentes**: el vehículo solo acepta 3 dispositivos conectados a la vez; desconecte un teléfono o un reloj.
