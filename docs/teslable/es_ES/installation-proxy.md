# Instalar el proxy BLE en una Raspberry Pi Zero 2 W

El complemento Tesla BLE no se comunica directamente con el coche: pasa por **TeslaBleHttpProxy** (aquí la imagen del fork mantenido para este complemento, véase [Imagen del fork o imagen de wimaha](#imagen-del-fork-o-imagen-de-wimaha)), un pequeño programa que se ejecuta en un dispositivo con Bluetooth colocado cerca del vehículo. Esta página explica, paso a paso, cómo instalar este proxy en una **Raspberry Pi Zero 2 W**, la placa recomendada, y cómo emparejarlo después con el coche.

```
Jeedom  --Wi-Fi / red local-->  Raspberry Pi Zero 2 W (TeslaBleHttpProxy)  --Bluetooth-->  Vehículo
```

Cuente con aproximadamente una hora, emparejamiento incluido. No necesita ningún conocimiento de programación, pero escribirá algunos comandos en un terminal.

> **IMPORTANTE**
>
> El complemento exige **TeslaBleHttpProxy 2.3.0 como mínimo**. La imagen del fork recomendada a continuación (`2.3.0-tb.2`) cumple este mínimo: el complemento ignora el sufijo `-tb.N` del número de versión.

## 1. ¿Por qué una Raspberry Pi Zero 2 W?

El Bluetooth de un Tesla tiene un alcance de **5 a 10 metros**. Por tanto, el proxy debe estar en el garaje o muy cerca de la plaza de aparcamiento, mientras que Jeedom suele estar en otra parte de la casa. Una Raspberry Pi Zero 2 W es pequeña, consume muy poco y tiene Wi-Fi y Bluetooth integrados.

| Característica | Raspberry Pi Zero 2 W |
|---|---|
| Procesador | 4 núcleos ARM Cortex-A53 de 64 bits a 1 GHz |
| Memoria | 512 MB |
| Bluetooth | 4.2, con Bluetooth Low Energy (BLE) |
| Wi-Fi | Solo 2,4 GHz (802.11 b/g/n) |
| Alimentación | 5 V, 2,5 A, conector micro-USB |

> **Consejo**
>
> No compre la antigua **Raspberry Pi Zero W** (sin el «2»): su procesador ARMv6 ya no es compatible con las versiones recientes de Docker, y su adaptador Bluetooth tiende a bloquearse al cabo de unas horas. Una Raspberry Pi 3, 4 o 5 también sirve, si está al alcance del vehículo.

## 2. Material necesario

- Una **Raspberry Pi Zero 2 W**.
- Una **fuente de alimentación de 5 V / 2,5 A** micro-USB de calidad, idealmente la oficial. Una fuente demasiado débil provoca cortes de Bluetooth difíciles de diagnosticar.
- Una **tarjeta microSD de marca**, de gama **«High Endurance»** (diseñada para un funcionamiento continuo), de **16 GB** recomendados (8 GB como mínimo con Raspberry Pi OS Lite de 64 bits). La Raspberry Pi funciona día y noche: una tarjeta vieja o de gama básica acaba desgastándose y averiándose.
- Una **carcasa**, preferiblemente de plástico: una carcasa metálica reduce el alcance de la radio.
- Un ordenador con lector de tarjetas microSD, para preparar la tarjeta.
- El **Wi-Fi de su router en 2,4 GHz** debe llegar al lugar donde instalará la Raspberry Pi.

## 3. Elegir la ubicación

Antes de instalar nada, compruebe la ubicación:

1. La Raspberry Pi debe estar a **menos de 5 a 10 metros** del lugar donde aparca el coche, si es posible sin muro grueso ni puerta de garaje metálica entre ambos.
2. Debe recibir correctamente el **Wi-Fi de 2,4 GHz**: compruébelo con su teléfono en ese lugar.
3. Necesita un **enchufe eléctrico** cercano.

## 4. Preparar la tarjeta microSD

Se utiliza la herramienta oficial **Raspberry Pi Imager**, que instala **Raspberry Pi OS Lite (64-bit)** y configura el Wi-Fi y el acceso remoto incluso antes del primer arranque.

1. Descargue e instale [Raspberry Pi Imager](https://www.raspberrypi.com/software/) en su ordenador.
2. Inserte la tarjeta microSD en el ordenador e inicie Raspberry Pi Imager.
3. **Modelo**: elija **Raspberry Pi Zero 2 W**.
4. **Sistema operativo**: elija **Raspberry Pi OS (other)** y después **Raspberry Pi OS Lite (64-bit)**. La versión «Lite» no tiene interfaz gráfica: es intencionado, deja más memoria al proxy.
5. **Almacenamiento**: elija su tarjeta microSD.
6. Cuando Imager le proponga **personalizar los ajustes**, acepte e indique:
   - el **nombre de host**, por ejemplo `teslaproxy`;
   - un **nombre de usuario** y una **contraseña** (anótelos);
   - la **red Wi-Fi** (nombre y contraseña) y el **país del Wi-Fi** (ES);
   - la **zona horaria**;
   - en la pestaña **Servicios**, **active SSH** (autenticación por contraseña).
7. Inicie la escritura, espere al final de la verificación y retire la tarjeta.

## 5. Primer arranque y conexión

1. Inserte la tarjeta en la Raspberry Pi, colóquela en su ubicación y conecte la alimentación. El primer arranque tarda unos minutos.
2. Busque la **dirección IP** de la Raspberry Pi en la interfaz de su router (lista de dispositivos conectados, nombre `teslaproxy`).
3. **Fije esta dirección**: en su router, cree una **reserva DHCP** (o «concesión estática») para la Raspberry Pi. Es indispensable, porque el complemento guarda esta dirección.
4. Desde su ordenador, abra un terminal (PowerShell en Windows, Terminal en macOS o Linux) y conéctese:

   ```
   ssh <usuario>@<pi_ip>
   ```

   Acepte la huella digital la primera vez y escriba su contraseña.

5. Actualice el sistema:

   ```
   sudo apt-get update && sudo apt-get upgrade -y
   ```

6. Compruebe que el Bluetooth está activo:

   ```
   bluetoothctl list
   ```

   Debe aparecer una línea `Controller XX:XX:XX:XX:XX:XX teslaproxy [default]`. Si no aparece nada, reinicie la Raspberry Pi (`sudo reboot`) y vuelva a intentarlo.

> **Consejo**
>
> Para evitar los cortes de Wi-Fi, desactive el ahorro de energía del Wi-Fi. Localice el nombre de su conexión con `nmcli connection show`, luego escriba `sudo nmcli connection modify "<nombre_de_la_conexion>" 802-11-wireless.powersave 2` y reinicie.

## 6. Instalar Docker

El proxy se distribuye en forma de imagen **Docker**, lo que simplifica la instalación y las actualizaciones.

1. Instale Docker con el script oficial:

   ```
   curl -sSL https://get.docker.com | sh
   ```

2. Compruebe que la instalación se ha completado:

   ```
   sudo docker run --rm hello-world
   ```

   Debe aparecer un mensaje «Hello from Docker!». No se conforme con `docker --version`: responde en cuanto el cliente está instalado, aunque el motor de Docker no lo esté. Si el comando falla, véase [Solución de problemas](#12-solucion-de-problemas).
3. Autorice a su usuario a utilizar Docker:

   ```
   sudo usermod -aG docker $USER
   ```

4. **Cierre la sesión** (`exit`) y vuelva a conectarse por SSH para que este permiso se aplique.
5. Compruebe que Docker funciona sin `sudo`:

   ```
   docker run --rm hello-world
   ```

## 7. Instalar TeslaBleHttpProxy

1. Cree una carpeta para el proxy, con una subcarpeta `key` que contendrá la llave del vehículo:

   ```
   cd ~
   mkdir -p TeslaBleHttpProxy/key
   cd TeslaBleHttpProxy
   ```

2. Cree el archivo de configuración:

   ```
   nano docker-compose.yml
   ```

3. Pegue este contenido:

   ```yaml
   services:
     tesla-ble-http-proxy:
       image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2
       container_name: tesla-ble-http-proxy
       volumes:
         - ~/TeslaBleHttpProxy/key:/key
         - /var/run/dbus:/var/run/dbus
       restart: always
       privileged: true
       network_mode: host
       cap_add:
         - NET_ADMIN
         - SYS_ADMIN
       logging:
         driver: json-file
         options:
           max-size: "10m"
           max-file: "3"
   ```

   Cada una de estas líneas tiene su función:
   - `image`: la imagen del fork, con un **número de versión preciso** (recomendado: el proxy solo cambia cuando usted lo decide, véase [Actualizar la imagen del proxy](#actualizar-la-imagen-del-proxy)). Para una versión más reciente, consulte las [versiones publicadas](https://github.com/superdcat/TeslaBleHttpProxy/releases); `:latest` es posible, pero desaconsejado como ajuste por defecto;
   - `volumes`: la carpeta `key` conserva la llave del vehículo fuera del contenedor, y sobrevive a las actualizaciones; `/var/run/dbus` da acceso al Bluetooth de la Raspberry Pi;
   - `restart: always`: el proxy se reinicia solo tras un corte de corriente (sin cambiar de imagen: véase [Actualizar la imagen del proxy](#actualizar-la-imagen-del-proxy));
   - `network_mode: host`, `privileged` y `cap_add`: el proxy necesita un acceso directo a la red y al adaptador Bluetooth;
   - `logging`: limita los registros de Docker a 3 archivos de 10 MB. El proxy escribe de forma continua: sin este límite, los registros crecen y desgastan la tarjeta microSD para nada.

4. Guarde con `Ctrl + X`, luego `Y` y `Intro`.
5. Inicie el proxy:

   ```
   docker compose up -d
   ```

6. Compruebe que responde: desde un navegador de su ordenador, abra `http://<pi_ip>:8080/api/proxy/1/version`. Debe obtener una respuesta JSON que contenga la versión (`2.3.0-tb.2` con la imagen anterior) y `"flavor":"superdcat"`.

### Imagen del fork o imagen de wimaha

El proxy es un software libre de **wimaha** ([TeslaBleHttpProxy](https://github.com/wimaha/TeslaBleHttpProxy)). Esta página recomienda el **fork** `ghcr.io/superdcat/tesla-ble-http-proxy`, que mantiene sus rutas y sus respuestas idénticas: el complemento (y evcc) funcionan igual con una u otra, sin cambiar nada en su configuración.

El fork añade, entre otras cosas: una ruta `/api/proxy/1/capabilities` que lista lo que el proxy sabe hacer (y el rol de la llave activa), comandos y datos adicionales, un token de acceso opcional (`apiToken`), la elección del adaptador Bluetooth (`btAdapter`), el ajuste de la duración de mantenimiento de la conexión (`connectionTimeout`) y la liberación del adaptador Bluetooth en reposo (`releaseAdapterWhenIdle`).

> **Consejo**
>
> La imagen de **wimaha** (`wimaha/tesla-ble-http-proxy`) sigue siendo utilizable **como alternativa**, a partir de la versión 2.3.0: el complemento funciona con ella. Le falta todo lo anterior: no hay ruta `capabilities`, ni token, ni elección del adaptador Bluetooth, ni ajuste del mantenimiento de la conexión. Para utilizarla, sustituya simplemente la línea `image:` del archivo `docker-compose.yml` por `image: wimaha/tesla-ble-http-proxy`. El complemento no depende de ello: con el fork, lee la ruta `capabilities` para saber desde el principio qué comandos acepta su proxy; con la imagen de wimaha, lo descubre al usarlo, cuando el proxy rechaza un comando.

### Ajustes opcionales

El proxy acepta algunos ajustes, que se añaden en `docker-compose.yml` bajo `container_name` y se aplican con `docker compose up -d`:

```yaml
    environment:
      - scanTimeout=10
      - logLevel=info
```

| Ajuste | Por defecto | Cuándo cambiarlo |
|---|---|---|
| `scanTimeout` | 5 s | El vehículo **no siempre se encuentra**: pase a 10 o 15 segundos. |
| `logLevel` | `info` | Ponga `debug` mientras dure un diagnóstico. |
| `vehicleDataCacheTime` | 30 s | Tiempo durante el cual el proxy vuelve a servir los mismos datos de carga y de climatización. Mantenga el valor por defecto. |
| `httpListenAddress` | `:8080` | Cambie el puerto solo si ya está ocupado; en ese caso, indique el nuevo puerto en la URL del complemento. |
| `apiToken` | vacío (sin autenticación) | Protege el proxy con un token: introduzca el **mismo valor** en **Token de API del proxy** (configuración del complemento). Genérelo, por ejemplo, con `openssl rand -hex 32`. Utilice el mismo token en todos sus proxys. Véase el recuadro siguiente. |
| `btAdapter` | vacío (adaptador por defecto) | La Raspberry Pi tiene **varios adaptadores Bluetooth** (por ejemplo una llave USB) y el proxy debe utilizar uno de ellos: de `hci0` a `hci15`, en minúsculas (por ejemplo `hci1`). Disponible a partir de `2.3.0-tb.2`. |
| `connectionTimeout` | 29 s | Tiempo durante el cual la conexión Bluetooth permanece abierta tras un comando, de 10 a 120 segundos. El plazo se cuenta **desde la apertura** de la conexión: los comandos siguientes no lo reinician. Un valor más largo ocupa durante más tiempo uno de los 3 espacios Bluetooth del vehículo. Un valor no válido se sustituye por 29. Disponible a partir de `2.3.0-tb.2`. |
| `releaseAdapterWhenIdle` | `false` | Ponga `true` **solo** si otro servicio de la Raspberry Pi debe poder utilizar el adaptador Bluetooth cuando el proxy no está trabajando. Entonces cada primer comando tarda un poco más. Véanse los límites en las [variables de entorno del fork](https://github.com/superdcat/TeslaBleHttpProxy/blob/main/docs/environment_variables.md#releaseadapterwhenidle). Disponible a partir de `2.3.0-tb.2`. |

> **IMPORTANTE**
>
> **Activar `apiToken` con Jeedom**, en este orden:
>
> 1. añada la línea `- apiToken=<su_token>` en `docker-compose.yml` y luego `docker compose up -d`;
> 2. en Jeedom, **Complementos > Gestión de plugins > Tesla BLE**, introduzca el mismo token en **Token de API del proxy** y pulse **Guardar**;
> 3. haga clic en **Probar**: debe mostrar **«Token de API aceptado por el proxy»**.
>
> El token: de 1 a 256 caracteres ASCII imprimibles (letras, cifras, puntuación), sin acentos ni saltos de línea. Una vez activo el token, el panel del proxy pide un identificador en el navegador: nombre de usuario libre, contraseña = el token. **evcc** no sabe enviar este token: no lo active si evcc utiliza el mismo proxy. El token circula en claro por la red local: no sustituye al aislamiento de la red (véase [Seguridad](#11-seguridad)).

## 8. Generar la llave y emparejarla con el vehículo

El proxy actúa como una llave de coche adicional. Por tanto, hay que generar esta llave y luego autorizarla en el vehículo con su **tarjeta llave** (la tarjeta NFC).

### Elegir el rol de la llave

| Rol | Lo que permite | Para quién |
|---|---|---|
| **Charging Manager** (recomendado) | Leer el estado y los datos del vehículo; despertar; iniciar y detener la carga; ajustar la corriente de carga | Uso centrado en la carga (horas valle, solar) |
| **Owner** | Todos los comandos, incluidos bloqueo, desbloqueo, claxon, luces, modo Centinela y climatización | Si desea controlar algo más que la carga |

El proxy **no tiene ninguna autenticación por defecto** (el token de API del fork es opcional): con una llave Owner, cualquier dispositivo de su red local puede desbloquear el vehículo. Elija Owner solo si lo necesita, y lea la sección [Seguridad](#11-seguridad).

### Emparejar

1. Abra el panel del proxy en un navegador: `http://<pi_ip>:8080/dashboard`.
2. Haga clic en **Generate** (*Generar*) junto al rol elegido. La llave se crea, se guarda en la carpeta `key` y se activa.
3. En **Setup Vehicle** (*Configurar vehículo*), introduzca el **VIN** del vehículo (17 caracteres, visible en la parte inferior de la pantalla principal de la aplicación Tesla).
4. **Despierte el vehículo**: abra la aplicación Tesla en su teléfono o abra una puerta. El envío de la llave falla si el coche duerme.
5. Haga clic en **Send key** (*Enviar llave*).
6. En el coche, **coloque su tarjeta llave** sobre la consola central, en el lugar de lectura del teléfono. No aparece ningún mensaje en la pantalla antes de este gesto.
7. Confirme en la pantalla del vehículo si aparece una solicitud de adición de llave.

### Comprobar el emparejamiento

Abra en un navegador `http://<pi_ip>:8080/api/1/vehicles/<VIN>/body_controller_state`. Una respuesta JSON con `"result":true` confirma que el proxy se comunica con el vehículo por Bluetooth con su llave. Esta lectura **no despierta** el coche.

## 9. Configurar el complemento

El proxy está listo: pase a la [configuración del complemento](index.md#configuracion-del-plugin). La URL que hay que introducir es `http://<pi_ip>:8080/`. El botón **Probar** de la página de configuración debe mostrar la versión del proxy.

Añada después un dispositivo por vehículo con su VIN, como se describe en [Configuración de los dispositivos](index.md#configuracion-de-los-dispositivos).

## 10. Mantenimiento

| Acción | Comando (en la carpeta `~/TeslaBleHttpProxy`) |
|---|---|
| Ver los registros del proxy | `docker logs --since 12h tesla-ble-http-proxy` |
| Actualizar el proxy | Véase [Actualizar la imagen del proxy](#actualizar-la-imagen-del-proxy) |
| Descargar la imagen de la versión escrita en `docker-compose.yml` | `docker compose pull` |
| Descargar la imagen del fork a mano | `docker pull ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2` (cambie el número) |
| Reiniciar el proxy | `docker compose restart` |
| Reiniciar la Raspberry Pi | `sudo reboot` |

> **Consejo**
>
> **Haga una copia de seguridad de la carpeta `~/TeslaBleHttpProxy/key`** en otro dispositivo, por ejemplo con `scp -r <usuario>@<pi_ip>:TeslaBleHttpProxy/key .` desde su ordenador. Si la tarjeta microSD se avería, bastará con reinstalar y volver a colocar esta carpeta, sin repetir el emparejamiento.

### Pasar de la imagen de wimaha a la imagen del fork

Si su proxy ya funciona con la imagen `wimaha/tesla-ble-http-proxy`, cambie de imagen **sin repetir el emparejamiento**: la llave permanece en la carpeta `key`, que el nuevo contenedor retoma tal cual.

1. Conéctese por SSH a la Raspberry Pi y sitúese en la carpeta del proxy:

   ```
   cd ~/TeslaBleHttpProxy
   ```

2. Abra el archivo: `nano docker-compose.yml`. Cambie **únicamente** la línea `image:`:

   ```yaml
       image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2
   ```

   No toque ni `volumes` ni el resto. Guarde con `Ctrl + X`, luego `Y` y `Intro`.
3. Descargue la nueva imagen y reinicie el proxy:

   ```
   docker compose pull && docker compose up -d
   ```

   La descarga puede tardar varios minutos en una Raspberry Pi Zero 2 W.
4. Compruebe, en un navegador, `http://<pi_ip>:8080/api/proxy/1/version`: la respuesta debe contener `"flavor":"superdcat"` y la versión `2.3.0-tb.2`.
5. Abra también `http://<pi_ip>:8080/api/proxy/1/capabilities`: la respuesta lista los comandos y los datos del proxy, y `key_role` indica el rol de su llave (`owner` o `charging_manager`). Si `key_role` está vacío, no se reconoce ninguna llave: compruebe que la carpeta `key` está bien montada.
6. En Jeedom, haga clic en **Probar** en la configuración del complemento: muestra la versión del proxy. No hay que modificar nada más ni en el complemento ni en evcc.

**Volver atrás**: vuelva a poner la línea `image: wimaha/tesla-ble-http-proxy` en `docker-compose.yml` y luego `docker compose pull && docker compose up -d`. La llave de la carpeta `key` funciona con las dos imágenes.

### Actualizar la imagen del proxy

> **IMPORTANTE**
>
> Un **reinicio de la Raspberry Pi**, `docker compose restart` o `restart: always` **no actualizan la imagen**: Docker vuelve a lanzar la imagen ya descargada. Una actualización es siempre una acción voluntaria (opción 1) o una tarea programada que usted ha creado (opción 2).

**Opción 1 (recomendada): un número de versión preciso, actualización a mano**

El proxy controla su coche. Una actualización no controlada puede cambiar un comportamiento en el peor momento (una carga programada que ya no se inicia, por ejemplo), y la descarga tarda varios minutos en una Raspberry Pi Zero 2 W. Mantenga, por tanto, una etiqueta precisa en `docker-compose.yml` (`image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2`) y actualice cuando usted lo decida:

1. Lea las notas de la nueva versión en la página de [versiones del fork](https://github.com/superdcat/TeslaBleHttpProxy/releases).
2. En la Raspberry Pi, en `~/TeslaBleHttpProxy`, cambie el número de versión al final de la línea `image:` (`nano docker-compose.yml`).
3. Ejecute `docker compose pull && docker compose up -d`.
4. Compruebe `http://<pi_ip>:8080/api/proxy/1/version`: la versión mostrada debe ser la nueva. La carpeta `key` se conserva, sin nuevo emparejamiento.

**Opción 2 (opcional): `latest` y actualización automática por la noche**

Usted acepta que el proxy siga cada nueva versión sin que la haya leído. Bajo su responsabilidad: una versión defectuosa se instala sola, y el proxy se corta unos instantes durante el reinicio (un comando en curso puede fallar). Si la elige:

1. En `docker-compose.yml`, ponga `image: ghcr.io/superdcat/tesla-ble-http-proxy:latest`.
2. Abra la tabla de tareas programadas de su usuario: `crontab -e`.
3. Añada esta línea, que actualiza todos los días a las 4 de la madrugada (sustituya `<usuario>` por su nombre de usuario: la ruta debe ser **absoluta**):

   ```
   0 4 * * * cd /home/<usuario>/TeslaBleHttpProxy && docker compose pull -q && docker compose up -d && docker image prune -f
   ```

   `docker compose pull -q` descarga la última imagen sin mostrar detalles, `docker compose up -d` solo reinicia el proxy si la imagen ha cambiado, y `docker image prune -f` elimina las imágenes antiguas que ocupan la tarjeta microSD.
4. Guarde y salga. Compruebe al día siguiente `http://<pi_ip>:8080/api/proxy/1/version`.

Para volver a la opción 1, elimine la línea de `crontab -e` y vuelva a poner un número de versión preciso.

## 11. Seguridad

- Por defecto, el proxy **no tiene ni contraseña ni cifrado**: cualquiera que acceda a su red local puede enviarle comandos. El fork sabe pedir un token (`apiToken`): actívelo e introdúzcalo en la configuración del complemento (véase [Ajustes opcionales](#ajustes-opcionales)). El token circula en claro por la red: complementa el aislamiento de la red, no lo sustituye.
- **No abra nunca** el puerto 8080 hacia Internet (sin redirección de puertos en el router).
- Si su router lo permite, coloque la Raspberry Pi en una red aislada, con Jeedom como único dispositivo autorizado a acceder a ella.
- Prefiera una llave **Charging Manager** si solo controla la carga.
- Cambie la contraseña por defecto de todo dispositivo de esta red y mantenga la Raspberry Pi actualizada (`sudo apt-get update && sudo apt-get upgrade`).

## 12. Solución de problemas

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `usermod: group 'docker' does not exist` (paso 6) | La instalación de Docker no se ha completado: el motor no está instalado, solo el cliente | Compruebe el espacio con `df -h /`: la raíz debe ocupar casi toda la tarjeta. Vuelva a ejecutar `sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin` y lea el error. Si `df` sigue en unos 2 GB tras la ampliación, o si `dmesg` muestra `I/O error` en `mmcblk0`, la tarjeta es defectuosa: sustitúyala. |
| La página `/api/proxy/1/version` no se abre | Proxy detenido, IP o puerto incorrectos | `docker ps` debe listar `tesla-ble-http-proxy`; si no, `docker compose up -d`. Compruebe la IP en el router. |
| `bluetoothctl list` no muestra nada | Bluetooth de la Raspberry Pi no disponible | `sudo reboot`. Compruebe la alimentación (5 V / 2,5 A). |
| «Vehicle is not in range» (*El vehículo no está al alcance*) o vehículo no siempre encontrado | Alcance Bluetooth insuficiente | Acerque la Raspberry Pi, evite la carcasa metálica, aumente `scanTimeout`. |
| El envío de la llave no hace nada | Vehículo dormido, o tarjeta llave no colocada | Despierte el coche, vuelva a enviar la llave, coloque la tarjeta en la consola. |
| Algunos comandos son rechazados | Llave **Charging Manager** | Normal para el bloqueo, el claxon, las luces, el modo Centinela y la climatización: genere una llave **Owner** si es necesario. |
| Cortes regulares tras unas horas | Wi-Fi en ahorro de energía, alimentación débil o adaptador Bluetooth bloqueado | Desactive el ahorro de energía del Wi-Fi, cambie de fuente de alimentación, reinicie el proxy. |
| Conexiones intermitentes con el coche | Demasiados dispositivos Bluetooth conectados | El vehículo acepta **3 dispositivos conectados a la vez** (teléfonos, reloj, proxy). |
| El contenedor se reinicia en bucle (`docker ps`: «Restarting»), el complemento muestra **Proxy inaccesible**; `docker logs tesla-ble-http-proxy` indica `Cannot start with this Bluetooth adapter` | `btAdapter` no válido (otra cosa que `hci0` a `hci15` en minúsculas) o adaptador ausente / imposible de abrir | Corrija el valor o elimine la línea `btAdapter` y luego `docker compose up -d`. Busque el nombre del adaptador con `bluetoothctl list` o `hciconfig -a`. |
| Todas las lecturas y comandos fallan con **«Token de API rechazado por el proxy»** (último error, comando); **Probar** muestra «El proxy exige un token de API» o «Token de API rechazado por el proxy» | `apiToken` está definido en `docker-compose.yml`, y el complemento no tiene token o tiene uno distinto | Introduzca en **Token de API del proxy** exactamente el valor de `apiToken`, **Guardar** y luego **Probar**. |
| **«Comando rechazado por el vehículo: invalid request body: …»** | El proxy del fork ha rechazado el contenido del comando (clave ausente, tipo incorrecto, valor fuera de límites) antes de enviarlo | El complemento verifica sus valores antes del envío: si esto ocurre, anote el texto después de los dos puntos (nombra la clave) y comuníquelo con el registro del complemento en Debug. |
| **«Este comando requiere una llave con rol Owner: la llave del proxy probablemente tiene el rol Charging Manager…»**, o información **Rol de la llave** en **Charging Manager** | La llave tiene el rol **Charging Manager** | Genere y empareje una llave **Owner** (véase [Elegir el rol de la llave](#elegir-el-rol-de-la-llave)). El rol de la llave activa se lee en `key_role` en la dirección `http://<pi_ip>:8080/api/proxy/1/capabilities`. |
| El vehículo ya no se encuentra tras la instalación de otro software Bluetooth | Este software ocupa el adaptador | El proxy necesita el adaptador para él solo: retire el otro servicio Bluetooth de esta Raspberry Pi. |

## Referencias

- [TeslaBleHttpProxy, fork de superdcat](https://github.com/superdcat/TeslaBleHttpProxy): el proxy recomendado para el complemento (README en inglés: comandos, datos, solución de problemas).
- [Variables de entorno del fork](https://github.com/superdcat/TeslaBleHttpProxy/blob/main/docs/environment_variables.md) (en inglés): detalle de los ajustes opcionales.
- [Versiones del fork](https://github.com/superdcat/TeslaBleHttpProxy/releases): notas y binarios de cada versión.
- Imagen Docker `ghcr.io/superdcat/tesla-ble-http-proxy`: imagen del fork, publicada en el registro de GitHub (`ghcr.io`).
- [TeslaBleHttpProxy de wimaha](https://github.com/wimaha/TeslaBleHttpProxy): el proyecto original, utilizable como alternativa.
- [Guía de instalación del proxy de wimaha](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md) (en inglés): fuente de los pasos 6 a 8.
- [Imagen Docker `wimaha/tesla-ble-http-proxy`](https://hub.docker.com/r/wimaha/tesla-ble-http-proxy): imagen de la alternativa wimaha.
- [SDK oficial de Tesla `vehicle-command`](https://github.com/teslamotors/vehicle-command): la biblioteca en la que se basa el proxy (llaves, roles, protocolo Bluetooth).
- [Raspberry Pi Imager](https://www.raspberrypi.com/software/): preparación de la tarjeta microSD.
- [Ficha de producto de la Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/): características y alimentación recomendada.
- [Instalación de Docker en Debian](https://docs.docker.com/engine/install/debian/): documentación de Docker, válida para Raspberry Pi OS de 64 bits (el script `get.docker.com` del paso 6 lo automatiza).
