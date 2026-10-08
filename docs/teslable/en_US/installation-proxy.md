# Installing the BLE proxy on a Raspberry Pi Zero 2 W

The Tesla BLE plugin does not talk to the car directly: it goes through **TeslaBleHttpProxy** (here the image of the fork maintained for this plugin, see [Fork image or wimaha image](#fork-image-or-wimaha-image)), a small program that runs on a Bluetooth-equipped device placed near the vehicle. This page explains, step by step, how to install this proxy on a **Raspberry Pi Zero 2 W**, the recommended board, then how to pair it with the car.

```
Jeedom  --Wi-Fi / local network-->  Raspberry Pi Zero 2 W (TeslaBleHttpProxy)  --Bluetooth-->  Vehicle
```

Allow about one hour, pairing included. You need no programming knowledge, but you will type a few commands in a terminal.

> **IMPORTANT**
>
> The plugin requires **TeslaBleHttpProxy 2.3.0 minimum**. The recommended fork image below (`2.3.0-tb.2`) meets this minimum: the plugin ignores the `-tb.N` suffix of the version number.

## 1. Why a Raspberry Pi Zero 2 W?

A Tesla's Bluetooth range is **5 to 10 meters**. The proxy must therefore be in the garage or very close to the parking spot, while Jeedom is often elsewhere in the house. A Raspberry Pi Zero 2 W is small, uses very little power, and has built-in Wi-Fi and Bluetooth.

| Feature | Raspberry Pi Zero 2 W |
|---|---|
| Processor | 4-core 64-bit ARM Cortex-A53 at 1 GHz |
| Memory | 512 MB |
| Bluetooth | 4.2, with Bluetooth Low Energy (BLE) |
| Wi-Fi | 2.4 GHz only (802.11 b/g/n) |
| Power supply | 5 V, 2.5 A, micro-USB socket |

> **Tip**
>
> Do not buy the old **Raspberry Pi Zero W** (without the “2”): its ARMv6 processor is no longer supported by recent versions of Docker, and its Bluetooth adapter tends to freeze after a few hours. A Raspberry Pi 3, 4 or 5 also works, as long as it is within range of the vehicle.

## 2. Required hardware

- A **Raspberry Pi Zero 2 W**.
- A good-quality **5 V / 2.5 A** micro-USB **power supply**, ideally the official one. An underpowered supply causes Bluetooth dropouts that are hard to diagnose.
- A **name-brand microSD card** from the **“High Endurance”** range (designed for continuous operation), **16 GB** recommended (8 GB at the very least with Raspberry Pi OS Lite 64-bit). The Raspberry Pi runs day and night: an old or entry-level card eventually wears out and fails.
- A **case**, preferably plastic: a metal case reduces the radio range.
- A computer with a microSD card reader, to prepare the card.
- Your router's **2.4 GHz Wi-Fi** must reach the place where you will install the Raspberry Pi.

## 3. Choosing the location

Before installing anything, check the location:

1. The Raspberry Pi must be **within 5 to 10 meters** of where the car parks, with no thick wall or metal garage door between the two if possible.
2. It must get a good **2.4 GHz Wi-Fi** signal: check with your phone at that spot.
3. It needs a **power outlet** nearby.

## 4. Preparing the microSD card

We use the official **Raspberry Pi Imager** tool, which installs **Raspberry Pi OS Lite (64-bit)** and sets up Wi-Fi and remote access before the very first boot.

1. Download and install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your computer.
2. Insert the microSD card into the computer and launch Raspberry Pi Imager.
3. **Model**: choose **Raspberry Pi Zero 2 W**.
4. **Operating system**: choose **Raspberry Pi OS (other)**, then **Raspberry Pi OS Lite (64-bit)**. The “Lite” version has no graphical interface: this is intentional, it leaves more memory for the proxy.
5. **Storage**: choose your microSD card.
6. When Imager offers to **customize the settings**, accept and fill in:
   - the **hostname**, for example `teslaproxy`;
   - a **username** and a **password** (write them down);
   - the **Wi-Fi network** (name and password) and the **Wi-Fi country** (FR);
   - the **time zone**;
   - in the **Services** tab, **enable SSH** (password authentication).
7. Start the write, wait for the verification to finish, then remove the card.

## 5. First boot and connection

1. Insert the card into the Raspberry Pi, place it at its location and plug in the power supply. The first boot takes a few minutes.
2. Find the Raspberry Pi's **IP address** in your router's interface (list of connected devices, name `teslaproxy`).
3. **Fix this address**: in your router, create a **DHCP reservation** (or “static lease”) for the Raspberry Pi. This is essential, because the plugin stores this address.
4. From your computer, open a terminal (PowerShell on Windows, Terminal on macOS or Linux) and connect:

   ```
   ssh <user>@<pi_ip>
   ```

   Accept the fingerprint the first time, then type your password.

5. Update the system:

   ```
   sudo apt-get update && sudo apt-get upgrade -y
   ```

6. Check that Bluetooth is active:

   ```
   bluetoothctl list
   ```

   A line `Controller XX:XX:XX:XX:XX:XX teslaproxy [default]` must appear. If nothing appears, restart the Raspberry Pi (`sudo reboot`) and try again.

> **Tip**
>
> To avoid Wi-Fi dropouts, disable Wi-Fi power saving. Find the name of your connection with `nmcli connection show`, then type `sudo nmcli connection modify "<connection_name>" 802-11-wireless.powersave 2` and restart.

## 6. Installing Docker

The proxy is distributed as a **Docker** image, which simplifies installation and updates.

1. Install Docker with the official script:

   ```
   curl -sSL https://get.docker.com | sh
   ```

2. Check that the installation completed:

   ```
   sudo docker run --rm hello-world
   ```

   A “Hello from Docker!” message must appear. Do not settle for `docker --version`: it answers as soon as the client is installed, even if the Docker engine is not. If the command fails, see [Troubleshooting](#12-troubleshooting).
3. Allow your user to use Docker:

   ```
   sudo usermod -aG docker $USER
   ```

4. **Log out** (`exit`) then log back in over SSH so that this permission takes effect.
5. Check that Docker works without `sudo`:

   ```
   docker run --rm hello-world
   ```

## 7. Installing TeslaBleHttpProxy

1. Create a folder for the proxy, with a `key` subfolder that will hold the vehicle's key:

   ```
   cd ~
   mkdir -p TeslaBleHttpProxy/key
   cd TeslaBleHttpProxy
   ```

2. Create the configuration file:

   ```
   nano docker-compose.yml
   ```

3. Paste this content into it:

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

   Each of these lines has a purpose:
   - `image`: the fork image, with a **precise version number** (recommended: the proxy only changes when you decide, see [Updating the proxy image](#updating-the-proxy-image)). For a more recent version, see the [published releases](https://github.com/superdcat/TeslaBleHttpProxy/releases); `:latest` is possible, but not recommended as the default setting;
   - `volumes`: the `key` folder keeps the vehicle's key outside the container, so it survives updates; `/var/run/dbus` gives access to the Raspberry Pi's Bluetooth;
   - `restart: always`: the proxy restarts by itself after a power cut (without changing image: see [Updating the proxy image](#updating-the-proxy-image));
   - `network_mode: host`, `privileged` and `cap_add`: the proxy needs direct access to the network and to the Bluetooth adapter;
   - `logging`: limits the Docker logs to 3 files of 10 MB. The proxy writes continuously: without this limit, the logs keep growing and wear out the microSD card for nothing.

4. Save with `Ctrl + X`, then `Y` and `Enter`.
5. Start the proxy:

   ```
   docker compose up -d
   ```

6. Check that it responds: from a browser on your computer, open `http://<pi_ip>:8080/api/proxy/1/version`. You must get a JSON response containing the version (`2.3.0-tb.2` with the image above) and `"flavor":"superdcat"`.

### Fork image or wimaha image

The proxy is free software by **wimaha** ([TeslaBleHttpProxy](https://github.com/wimaha/TeslaBleHttpProxy)). This page recommends the **fork** `ghcr.io/superdcat/tesla-ble-http-proxy`, which keeps its routes and responses identical: the plugin (and evcc) work the same way with either one, without changing their configuration.

The fork notably adds: a `/api/proxy/1/capabilities` route that lists what the proxy can do (and the role of the active key), additional commands and data, an optional access token (`apiToken`), the choice of the Bluetooth adapter (`btAdapter`), the setting of how long the connection is kept open (`connectionTimeout`) and the release of the Bluetooth adapter when idle (`releaseAdapterWhenIdle`).

> **Tip**
>
> The **wimaha** image (`wimaha/tesla-ble-http-proxy`) remains usable **as an alternative**, from version 2.3.0: the plugin works with it. It lacks everything listed above: no `capabilities` route, no token, no choice of the Bluetooth adapter and no setting for keeping the connection open. To use it, simply replace the `image:` line of the `docker-compose.yml` file with `image: wimaha/tesla-ble-http-proxy`. The plugin does not depend on it: with the fork, it reads the `capabilities` route to know right away which commands your proxy accepts; with the wimaha image, it finds out through use, when the proxy refuses a command.

### Optional settings

The proxy accepts a few settings, to be added in `docker-compose.yml` under `container_name`, then applied with `docker compose up -d`:

```yaml
    environment:
      - scanTimeout=10
      - logLevel=info
```

| Setting | Default | When to change it |
|---|---|---|
| `scanTimeout` | 5 s | The vehicle is **not always found**: raise it to 10 or 15 seconds. |
| `logLevel` | `info` | Set `debug` for the duration of a diagnosis. |
| `vehicleDataCacheTime` | 30 s | How long the proxy serves the same charge and climate data again. Keep the default value. |
| `httpListenAddress` | `:8080` | Change the port only if it is already taken; then carry the new port over to the plugin's URL. |
| `apiToken` | empty (no authentication) | Protects the proxy with a token: enter the **same value** in **Proxy API token** (plugin configuration). Generate it for example with `openssl rand -hex 32`. Use the same token on all your proxies. See the box below. |
| `btAdapter` | empty (default adapter) | The Raspberry Pi has **several Bluetooth adapters** (for example a USB dongle) and the proxy must use one of them: `hci0` to `hci15`, in lowercase (for example `hci1`). Available from `2.3.0-tb.2`. |
| `connectionTimeout` | 29 s | How long the Bluetooth connection stays open after a command, from 10 to 120 seconds. The delay is counted **from the opening** of the connection: subsequent commands do not restart it. A longer value occupies one of the vehicle's 3 Bluetooth slots for longer. An invalid value is replaced by 29. Available from `2.3.0-tb.2`. |
| `releaseAdapterWhenIdle` | `false` | Set `true` **only** if another service on the Raspberry Pi must be able to use the Bluetooth adapter when the proxy is not working. Each first command then takes a little longer. See the limits in the [fork's environment variables](https://github.com/superdcat/TeslaBleHttpProxy/blob/main/docs/environment_variables.md#releaseadapterwhenidle). Available from `2.3.0-tb.2`. |

> **IMPORTANT**
>
> **Enabling `apiToken` with Jeedom**, in this order:
>
> 1. add the line `- apiToken=<your token>` in `docker-compose.yml`, then `docker compose up -d`;
> 2. in Jeedom, **Plugins > Plugins management > Tesla BLE**, enter the same token in **Proxy API token**, then **Save**;
> 3. click **Test**: it must display **“API token accepted by the proxy”**.
>
> The token: 1 to 256 printable ASCII characters (letters, digits, punctuation), without accents or line breaks. Once the token is active, the proxy dashboard asks for a login in the browser: free-form username, password = the token. **evcc** cannot send this token: do not enable it if evcc uses the same proxy. The token travels in clear text over the local network: it does not replace network isolation (see [Security](#11-security)).

## 8. Generating the key and pairing it with the vehicle

The proxy acts as an additional car key. You therefore need to generate this key, then authorize it in the vehicle with your **key card** (the NFC card).

### Choosing the key role

| Role | What it allows | Who it is for |
|---|---|---|
| **Charging Manager** (recommended) | Read the vehicle's state and data; wake up; start and stop charging; set the charging current | Charging-focused use (off-peak hours, solar) |
| **Owner** | All commands, including lock, unlock, horn, lights, Sentry Mode and climate control | If you want to control more than just charging |

The proxy has **no authentication by default** (the fork's API token is optional): with an Owner key, any device on your local network can unlock the vehicle. Choose Owner only if you need it, and read the [Security](#11-security) section.

### Pairing

1. Open the proxy dashboard in a browser: `http://<pi_ip>:8080/dashboard`.
2. Click **Generate** next to the chosen role. The key is created, saved in the `key` folder and activated.
3. In **Setup Vehicle**, enter the vehicle's **VIN** (17 characters, visible at the bottom of the main screen of the Tesla app).
4. **Wake up the vehicle**: open the Tesla app on your phone or open a door. Sending the key fails if the car is asleep.
5. Click **Send key**.
6. In the car, **place your key card** on the center console, at the phone reading spot. No message appears on the screen before this gesture.
7. Confirm on the vehicle's screen if a request to add a key is displayed.

### Checking the pairing

In a browser, open `http://<pi_ip>:8080/api/1/vehicles/<VIN>/body_controller_state`. A JSON response with `"result":true` confirms that the proxy reaches the vehicle over Bluetooth with its key. This reading **does not wake up** the car.

## 9. Configuring the plugin

The proxy is ready: go on to the [plugin configuration](index.md#plugin-configuration). The URL to enter is `http://<pi_ip>:8080/`. The **Test** button on the configuration page must display the proxy version.

Then add one equipment per vehicle with its VIN, as described in [Equipment configuration](index.md#equipment-configuration).

## 10. Maintenance

| Action | Command (in the `~/TeslaBleHttpProxy` folder) |
|---|---|
| View the proxy logs | `docker logs --since 12h tesla-ble-http-proxy` |
| Update the proxy | See [Updating the proxy image](#updating-the-proxy-image) |
| Download the image of the version written in `docker-compose.yml` | `docker compose pull` |
| Download the fork image by hand | `docker pull ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2` (replace the number) |
| Restart the proxy | `docker compose restart` |
| Restart the Raspberry Pi | `sudo reboot` |

> **Tip**
>
> **Back up the `~/TeslaBleHttpProxy/key` folder** to another device, for example with `scp -r <user>@<pi_ip>:TeslaBleHttpProxy/key .` from your computer. If the microSD card fails, you will only need to reinstall and put this folder back in place, without pairing again.

### Switching from the wimaha image to the fork image

If your proxy already runs with the `wimaha/tesla-ble-http-proxy` image, change image **without pairing again**: the key stays in the `key` folder, which the new container picks up as is.

1. Connect to the Raspberry Pi over SSH and go to the proxy folder:

   ```
   cd ~/TeslaBleHttpProxy
   ```

2. Open the file: `nano docker-compose.yml`. Change **only** the `image:` line:

   ```yaml
       image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2
   ```

   Touch neither `volumes` nor anything else. Save with `Ctrl + X`, then `Y` and `Enter`.
3. Download the new image and restart the proxy:

   ```
   docker compose pull && docker compose up -d
   ```

   The download can take several minutes on a Raspberry Pi Zero 2 W.
4. Check, in a browser, `http://<pi_ip>:8080/api/proxy/1/version`: the response must contain `"flavor":"superdcat"` and the version `2.3.0-tb.2`.
5. Also open `http://<pi_ip>:8080/api/proxy/1/capabilities`: the response lists the proxy's commands and data, and `key_role` indicates the role of your key (`owner` or `charging_manager`). If `key_role` is empty, no key is recognized: check that the `key` folder is properly mounted.
6. In Jeedom, click **Test** in the plugin configuration: it displays the proxy version. Nothing else needs to be changed on the plugin or evcc side.

**Going back**: put the line `image: wimaha/tesla-ble-http-proxy` back in `docker-compose.yml`, then `docker compose pull && docker compose up -d`. The key in the `key` folder works with both images.

### Updating the proxy image

> **IMPORTANT**
>
> A **restart of the Raspberry Pi**, `docker compose restart` or `restart: always` **do not update the image**: Docker restarts the image that was already downloaded. An update is always a deliberate action (option 1) or a scheduled task that you created (option 2).

**Option 1 (recommended): a precise version number, updated by hand**

The proxy controls your car. An uncontrolled update can change a behavior at the wrong time (a scheduled charge that no longer starts, for example), and the download takes several minutes on a Raspberry Pi Zero 2 W. So keep a precise tag in `docker-compose.yml` (`image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2`) and update when you decide to:

1. Read the notes of the new version on the [fork releases](https://github.com/superdcat/TeslaBleHttpProxy/releases) page.
2. On the Raspberry Pi, in `~/TeslaBleHttpProxy`, change the version number at the end of the `image:` line (`nano docker-compose.yml`).
3. Run `docker compose pull && docker compose up -d`.
4. Check `http://<pi_ip>:8080/api/proxy/1/version`: the displayed version must be the new one. The `key` folder is kept, no new pairing.

**Option 2 (optional): `latest` and automatic update at night**

You accept that the proxy follows every new version without you having read it. At your own risk: a faulty version installs itself, and the proxy is cut off for a few moments during the restart (a command in progress may fail). If you choose it:

1. In `docker-compose.yml`, set `image: ghcr.io/superdcat/tesla-ble-http-proxy:latest`.
2. Open your user's scheduled task table: `crontab -e`.
3. Add this line, which updates every day at 4 a.m. (replace `<user>` with your username: the path must be **absolute**):

   ```
   0 4 * * * cd /home/<user>/TeslaBleHttpProxy && docker compose pull -q && docker compose up -d && docker image prune -f
   ```

   `docker compose pull -q` downloads the latest image without showing any detail, `docker compose up -d` restarts the proxy only if the image has changed, and `docker image prune -f` removes the old images that take up space on the microSD card.
4. Save and quit. The next day, check `http://<pi_ip>:8080/api/proxy/1/version`.

To go back to option 1, delete the line from `crontab -e` and put a precise version number back.

## 11. Security

- By default, the proxy has **neither a password nor encryption**: anyone with access to your local network can send it commands. The fork can require a token (`apiToken`): enable it and enter it in the plugin configuration (see [Optional settings](#optional-settings)). The token travels in clear text over the network: it complements network isolation, it does not replace it.
- **Never** open port 8080 to the Internet (no port forwarding on the router).
- If your router allows it, place the Raspberry Pi on an isolated network, with Jeedom as the only device allowed to reach it.
- Prefer a **Charging Manager** key if you only control charging.
- Change the default password of every device on this network and keep the Raspberry Pi up to date (`sudo apt-get update && sudo apt-get upgrade`).

## 12. Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| `usermod: group 'docker' does not exist` (step 6) | The Docker installation did not complete: the engine is not installed, only the client is | Check the space with `df -h /`: the root partition should take up almost the whole card. Run `sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin` again and read the error. If `df` stays at about 2 GB after resizing, or if `dmesg` shows `I/O error` on `mmcblk0`, the card is faulty: replace it. |
| The `/api/proxy/1/version` page does not open | Proxy stopped, wrong IP or wrong port | `docker ps` must list `tesla-ble-http-proxy`; otherwise `docker compose up -d`. Check the IP in the router. |
| `bluetoothctl list` shows nothing | Raspberry Pi Bluetooth unavailable | `sudo reboot`. Check the power supply (5 V / 2.5 A). |
| “Vehicle is not in range” or vehicle not always found | Insufficient Bluetooth range | Move the Raspberry Pi closer, avoid the metal case, increase `scanTimeout`. |
| Sending the key does nothing | Vehicle asleep, or key card not placed | Wake up the car, send the key again, place the card on the console. |
| Some commands are refused | **Charging Manager** key | Normal for lock, horn, lights, Sentry Mode and climate control: generate an **Owner** key if needed. |
| Regular dropouts after a few hours | Wi-Fi in power-saving mode, weak power supply, or frozen Bluetooth adapter | Disable Wi-Fi power saving, change the power supply, restart the proxy. |
| Intermittent connections with the car | Too many connected Bluetooth devices | The vehicle accepts **3 connected devices at a time** (phones, watch, proxy). |
| The container restarts in a loop (`docker ps`: “Restarting”), the plugin displays **Proxy unreachable**; `docker logs tesla-ble-http-proxy` shows `Cannot start with this Bluetooth adapter` | Invalid `btAdapter` (anything other than `hci0` to `hci15` in lowercase) or adapter missing / cannot be opened | Fix the value or remove the `btAdapter` line, then `docker compose up -d`. Look up the adapter name with `bluetoothctl list` or `hciconfig -a`. |
| All reads and commands fail with **“API token refused by the proxy”** (last error, command); **Test** displays “The proxy requires an API token” or “API token refused by the proxy” | `apiToken` is set in `docker-compose.yml`, and the plugin has no token or a different token | Enter exactly the value of `apiToken` in **Proxy API token**, **Save**, then **Test**. |
| **“Command refused by the vehicle: invalid request body: …”** | The fork proxy refused the content of the command (missing key, wrong type, out-of-range value) before sending it | The plugin checks its values before sending: if this happens, note the text after the colon (it names the key) and report it with the plugin log in Debug. |
| **“This command requires an Owner role key: the proxy key probably has the Charging Manager role…”**, or the **Key role** information set to **Charging Manager** | The key has the **Charging Manager** role | Generate and pair an **Owner** key (see [Choosing the key role](#choosing-the-key-role)). The role of the active key can be read in `key_role` at `http://<pi_ip>:8080/api/proxy/1/capabilities`. |
| The vehicle is no longer found after installing other Bluetooth software | That software occupies the adapter | The proxy needs the adapter to itself: remove the other Bluetooth service from this Raspberry Pi. |

## References

- [TeslaBleHttpProxy, superdcat fork](https://github.com/superdcat/TeslaBleHttpProxy): the recommended proxy for the plugin (README in English: commands, data, troubleshooting).
- [The fork's environment variables](https://github.com/superdcat/TeslaBleHttpProxy/blob/main/docs/environment_variables.md) (in English): details of the optional settings.
- [Fork releases](https://github.com/superdcat/TeslaBleHttpProxy/releases): notes and binaries for each version.
- Docker image `ghcr.io/superdcat/tesla-ble-http-proxy`: the fork image, published on the GitHub registry (`ghcr.io`).
- [wimaha's TeslaBleHttpProxy](https://github.com/wimaha/TeslaBleHttpProxy): the original project, usable as an alternative.
- [wimaha's proxy installation guide](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md) (in English): source of steps 6 to 8.
- [Docker image `wimaha/tesla-ble-http-proxy`](https://hub.docker.com/r/wimaha/tesla-ble-http-proxy): image of the wimaha alternative.
- [Official Tesla SDK `vehicle-command`](https://github.com/teslamotors/vehicle-command): the library the proxy is built on (keys, roles, Bluetooth protocol).
- [Raspberry Pi Imager](https://www.raspberrypi.com/software/): preparing the microSD card.
- [Raspberry Pi Zero 2 W product page](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/): specifications and recommended power supply.
- [Installing Docker on Debian](https://docs.docker.com/engine/install/debian/): Docker documentation, valid for Raspberry Pi OS 64-bit (the `get.docker.com` script of step 6 automates it).
