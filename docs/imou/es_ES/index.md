# Plugin IMOU

El plugin **IMOU** controla sus cámaras IMOU desde Jeedom a través de la **IMOU Open API** (nube), **en PHP nativo**
(sin demonio, sin Python). Según las capacidades de cada cámara: encendido/apagado, vigilancia, PTZ,
foco/sirena, visión nocturna, ajustes de imagen, transmisión en vivo, miniatura, reinicio, batería, timbre
& apertura de puerta, notificación de alarmas, estado de la tarjeta SD y del abono cloud, supervisión.

> La API de IMOU no ofrece notificaciones en tiempo real: el estado de las cámaras se actualiza mediante
> **consulta periódica** (polling). Un cambio realizado desde la aplicación IMOU puede tardar
> algunos minutos en aparecer en Jeedom.

## Requisitos previos

- Una **cuenta de desarrollador IMOU** en [open.imoulife.com](https://open.imoulife.com).
- Una aplicación creada en la consola de desarrollador, que proporciona un **`appId`** y un **`appSecret`**, con
  el modo de integración **`accessType = PaaS`** (necesario para controlar los dispositivos).
- Sus cámaras ya asociadas a esta cuenta mediante la aplicación **IMOU Life**.
- **`ffmpeg`**: instalado **automáticamente** por Jeedom al activar el plugin (pestaña «Dependencias»).
  Se utiliza para extraer imágenes de la transmisión en vivo. En una instalación Docker, verifique que `ffmpeg`
  esté disponible en la imagen.

> ℹ️ **Número de dispositivos controlables (plan gratuito).** En teoría, la cuenta de desarrollador IMOU
> gratuita está limitada a **~5 dispositivos**: por encima de eso, los comandos *deberían* fallar con un
> **error de licencia** devuelto por IMOU (esto no es una limitación del plugin). **En la práctica, IMOU
> parece permitir controlar más cámaras** en el plan gratuito — en nuestras pruebas, todo funciona con
> normalidad más allá de 5. Este comportamiento depende de IMOU y puede cambiar sin previo aviso: si un
> comando acaba devolviendo un error de licencia, es este límite el que se aplica, y entonces se requiere un
> plan IMOU adecuado. En cualquier caso, las cámaras se descubren y se muestran; solo sus comandos se verían
> afectados.

## Configuración del plugin

1. Active el plugin (Plugins → Gestión de plugins → IMOU) y deje que Jeedom instale las dependencias.
2. En la configuración del plugin, introduzca:
   - **App ID**: el identificador de su aplicación IMOU;
   - **App Secret**: el secreto asociado (**almacenado cifrado**, nunca mostrado en texto claro);
   - **Datacenter**: la región de su cuenta (Europa por defecto).
3. Haga clic en **Probar la conexión** para validar sus credenciales.

### Ajustes avanzados (opcionales)

- **Cuota de llamadas API**: `quotaMensuel` (límite mensual de llamadas a la API, ~30 000 en el plan gratuito),
  umbral de alerta. La cuota se reinicia **el día 1 de cada mes**. El plugin **cuenta sus llamadas** y le
  avisa al acercarse al límite.
- **Regulación automática de la frecuencia**: límites `refreshIntervalMin`/`refreshIntervalMax`. El plugin
  ajusta automáticamente la frecuencia de actualización para mantenerse dentro del presupuesto mensual de llamadas.
- **Transmisiones en vivo concurrentes**: `liveMaxConcurrent` (número de transmisiones en vivo mostradas simultáneamente).
- **Estimación del consumo de datos**: `dataQuotaGo` / `dataBitrateKbps` (véase «Cuota y supervisión»).

## Añadir cámaras

- Haga clic en **Sincronizar**: el plugin recupera las cámaras de la cuenta y crea **un equipo por
  cámara** (uno por canal para los dispositivos multicanal).
- Renombre y organice los equipos en sus objetos como de costumbre: **sus personalizaciones se
  conservan** en las sincronizaciones posteriores.
- **Sincronización selectiva**: cada comando de estado puede excluirse de la actualización automática
  (casilla «Excluir de la actualización automática»), para ahorrar llamadas en lo que no necesita.

> 💡 **Los comandos dependen de las capacidades de la cámara.** El plugin solo crea los comandos
> realmente admitidos por cada modelo. Si un comando (PTZ, sirena, visión nocturna, tarjeta SD…)
> **no aparece**, es que su cámara no declara esa capacidad — es **normal**, no un error.

## Comandos disponibles (según la cámara)

- **Encender / Apagar** la cámara.
- **Vigilancia** (detección de movimiento): activar / desactivar.
- **Foco / luz** y **sirena** (en modelos compatibles, a través del modelo IoT «Things»).
- **PTZ**: almohadilla direccional (arriba/abajo/izquierda/derecha) y zoom en cámaras motorizadas.
- **Visión nocturna**: modo (automático / infrarrojo / color según el modelo).
- **Ajustes de imagen**: volteo, WDR, superposición de fecha/hora (OSD), indicador LED…
- **Transmisión en vivo**: imagen en vivo actualizada, **visualizable a pantalla completa** con un clic.
- **Miniatura** de la cámara (fuente a elegir: instantánea del vivo o imagen de portada).
- **Modelo (código)**: código técnico de la cámara, mostrado como **campo de solo lectura** en la
  configuración del equipo (junto al identificador), no como comando.
- **Reinicio** del dispositivo (acción protegida por confirmación).
- **Batería y activación**: nivel de batería (notificado en la supervisión de Salud de Jeedom); los dispositivos
  en reposo se activan para leer su estado.
- **Timbre de video & apertura de puerta** (en cerraduras/timbres compatibles; apertura protegida por
  confirmación).
- **Alarmas y detección**: último evento (movimiento/persona), **sensibilidad** de detección, **planes de
  armado** (preajustes día/noche/permanente), **detección humana / IA**.
- **Tarjeta SD**: presencia, uso, capacidad y **formateo** (acción protegida por confirmación).
- **Grabación en nube**: estado del abono (activo, expiración, plan). **Desactivado por defecto**
  (opción para activar si tiene un abono — véase más abajo).
- **En línea (estado)**: accesibilidad de la cámara, también utilizada para ahorrar llamadas (una cámara
  fuera de línea no se consulta).

### Activar el seguimiento del abono cloud

Los comandos cloud se crean **ocultos y sin consulta** por defecto (la mayoría de las cuentas no tienen
abono). Si tiene un abono cloud: haga visible el comando **Cloud activo** y
desmarque su casilla «Excluir de la actualización automática» para activar el seguimiento (comprobado una vez por hora).

## El panel «muro de cámaras»

El plugin añade una **página dedicada** al menú de Jeedom que muestra una cuadrícula de las transmisiones en vivo de sus cámaras (con
PTZ, sirena, foco según los modelos). Actívela en la **gestión del plugin** (casilla «Mostrar panel desktop»),
y elija por cámara si aparece en el muro (casilla «Visible en el panel de cámaras» del equipo).

## Actualización, cuota y supervisión

El plugin consulta la nube IMOU periódicamente (cron). Hay dos presupuestos **distintos** a conocer:

- **Cuota de LLAMADAS API** (~30 000/mes en el plan gratuito): **contada exactamente** por el plugin. La
  frecuencia de actualización es **regulada automáticamente** para mantenerse dentro de este presupuesto, y se emite una alerta
  al acercarse al límite. Los estados «lentos» (tarjeta SD, abono cloud) se actualizan con
  baja frecuencia (una vez por hora) — y el abono cloud solo se consulta si lo ha activado
  (véase «Activar el seguimiento del abono cloud»).
- **Cuota de DATOS** (volumen de la transmisión en vivo, ~3 GB/mes en el plan gratuito): el plugin proporciona una
  **estimación** (tiempo de visualización × tasa de bits configurada `dataBitrateKbps`, comparada con `dataQuotaGo`).
  Es un **indicador informativo**: el valor **real** es el del **portal de desarrolladores IMOU**,
  que es la fuente oficial. La API de IMOU no expone el consumo de datos real.

La pantalla de **Salud** del plugin resume la accesibilidad de las cámaras, la cuota de llamadas, la frecuencia regulada y
la estimación del consumo de datos.

## Privacidad y localización de los datos

Los **flujos de video** y los **comandos** pasan por los **servidores cloud de IMOU** (centro de datos según su
región — elija «Europa» para Francia). **Ningún video pasa por Jeedom**: el plugin envía
comandos de control y recibe metadatos de estado así como imágenes extraídas de la transmisión en vivo.

## Resolución de problemas

- **La sincronización no encuentra ninguna cámara** → verifique `appId`/`appSecret`/`Datacenter`, el botón
  **Probar la conexión**, y que sus cámaras estén correctamente asociadas a la cuenta en la aplicación IMOU Life.
- **Un comando no existe en mi cámara** → la capacidad no está admitida por este modelo. Es normal.
- **La transmisión en vivo no se muestra** → verifique que las **dependencias** del plugin estén instaladas (`ffmpeg`),
  que la cámara esté en línea, y consulte los registros `imou` en nivel *debug*.
- **Los comandos fallan con un error de licencia** → puede que esté alcanzando el límite de dispositivos
  controlables del plan gratuito de IMOU (en teoría ~5, aunque en la práctica IMOU suele permitir más;
  véase Requisitos previos). Entonces se requiere un plan IMOU adecuado — esto no es una limitación del plugin.
- **«Reloj desincronizado» / error de firma** → sincronice el reloj del servidor Jeedom (NTP):
  una desviación de más de 5 minutos hace que IMOU rechace las solicitudes.
- **Un cambio hecho en la app IMOU no aparece de inmediato** → normal, la actualización es
  periódica (sin notificación en tiempo real).

## Limitaciones conocidas

- **Sin alarmas en tiempo real (push)**: los eventos se notifican por consulta periódica, no
  por notificación instantánea.
- **Sin reproducción de grabaciones**: la API de IMOU no expone URLs de reproducción para videos grabados
  (SD o nube); la reproducción se realiza en la aplicación IMOU.
- **Sin nombre comercial del modelo**: solo se muestra el código técnico del modelo (no existe una base de datos
  fiable de correspondencia código → nombre comercial).
- **Zonas de detección, actualizaciones de firmware, asociación/renombrado del lado IMOU**: no gestionados.

## Desinstalación

Desactivar y luego eliminar el plugin en Jeedom elimina los equipos y sus comandos. Sus
**credenciales IMOU** (`appId`/`appSecret`) siguen siendo **válidas** en su cuenta de desarrollador IMOU y pueden
reutilizarse; no se eliminan del lado IMOU por esta operación.
