# Tesla BLE plugin

This plugin lets you control charging, climate control and a few basic functions of your **Tesla** vehicles from Jeedom, **over Bluetooth (BLE)** and without going through Tesla's cloud API.

Jeedom does not talk directly to the vehicle: it relies on a [TeslaBleHttpProxy](https://github.com/superdcat/TeslaBleHttpProxy) proxy (the fork maintained for this plugin, derived from the project by [wimaha](https://github.com/wimaha/TeslaBleHttpProxy)), installed on a small Bluetooth-equipped device (a Raspberry Pi, see [Choosing and installing the Raspberry Pi](#choosing-and-installing-the-raspberry-pi)) placed within range of the vehicle, typically in the garage. The plugin queries this proxy over HTTP on your local network.

```
Jeedom  --HTTP-->  TeslaBleHttpProxy (Raspberry Pi)  --Bluetooth-->  Vehicle
```

## Requirements

- Jeedom 4.5 minimum, on Debian 11 or 12.
- **TeslaBleHttpProxy 2.3.0 minimum**, installed, working and reachable from Jeedom. The **fork image** `ghcr.io/superdcat/tesla-ble-http-proxy` is recommended; the wimaha image (2.3.0 or newer) is still accepted. The plugin ignores the `-tb.N` suffix of fork versions: `2.3.0-tb.2` is considered compliant with “2.3.0 minimum”. Complete step-by-step procedure, on a Raspberry Pi Zero 2 W: [Installing the BLE proxy](installation-proxy.md).
- The **proxy key paired with the vehicle**. This step is done entirely in the TeslaBleHttpProxy interface (key generation, then validation with your key card in the vehicle): see [Installing the BLE proxy](installation-proxy.md#8-generating-the-key-and-pairing-it-with-the-vehicle).
- The **VIN** of each vehicle to control (shown at the bottom of the main screen of the Tesla app).

> **Tip**
>
> Before configuring the plugin, check that the proxy responds by opening `http://<proxy_ip>:<port>/api/proxy/1/version` in a browser (proxy version), then `http://<proxy_ip>:<port>/api/1/vehicles/<VIN>/body_controller_state`. You should get a JSON response.

### Checking and updating the proxy version

The plugin requires **TeslaBleHttpProxy 2.3.0 minimum**. Follow these steps to find out your proxy version, then update it if needed. With the fork image, the version looks like `2.3.0-tb.2` (wimaha base version, then the fork's version number).

**1. Read the current version**

1. On a computer on the same network as the proxy, open a browser.
2. In the address bar, type `http://<proxy_ip>:<port>/api/proxy/1/version`, for example `http://192.168.1.50:8080/api/proxy/1/version`.
3. Read the response: it contains `"version"` followed by the proxy version, for example `2.3.0` with the wimaha image. With the fork image, the response also contains `"flavor":"superdcat"` and a version such as `2.3.0-tb.2`.

If this version is **2.3.0 or newer**, there is nothing to do for the plugin. Otherwise, go to step 2.

**2. Update the proxy image**

1. Connect via SSH to the Raspberry Pi that hosts the proxy.
2. Go to the folder that contains the proxy's `docker-compose.yml` file (the `TeslaBleHttpProxy` folder if you followed [Installing the BLE proxy](installation-proxy.md)):

   ```
   cd TeslaBleHttpProxy
   ```

3. In `docker-compose.yml`, check the `image:` line: it must be `image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2` (or a newer fork version). If it points to the wimaha image, see [Switching from the wimaha image to the fork image](installation-proxy.md#switching-from-the-wimaha-image-to-the-fork-image). If it carries a specific version number, change that number.
4. Download the image, then restart the proxy with it:

   ```
   docker compose pull && docker compose up -d
   ```

   Restarting the Raspberry Pi or `restart: always` **do not update the image**: see [Updating the proxy image](installation-proxy.md#updating-the-proxy-image).

**3. Check the version again**

Reopen `http://<proxy_ip>:<port>/api/proxy/1/version` in the browser (wait a few seconds for the proxy to restart) and check that the version is indeed 2.3.0 or newer.

The key paired with the vehicle is stored in the `key` folder mounted by the `docker-compose.yml` file: it is **kept** by the update, you do not have to pair again.

> **IMPORTANT**
>
> With a proxy older than 2.1.1, the plugin cannot read the vehicle state: the lock state and the sleep state are no longer updated, presence no longer goes back to 1, and the plugin log shows “Version du proxy non prise en charge : 2.3.0 minimum, mettez le proxy à jour” (error line) (*“Proxy version not supported: 2.3.0 minimum, update the proxy”*).

### Choosing and installing the Raspberry Pi

The proxy must be **within Bluetooth range of the vehicle** (5 to 10 m, so usually in the garage). It is the Raspberry Pi that must be close to the car, not Jeedom.

| Board | Verdict |
|---|---|
| **Raspberry Pi Zero 2 W** | Recommended: small, low power, Docker proxy image available for this processor. |
| Raspberry Pi Zero W (first generation) | Not recommended: ARMv6 processor that is no longer supported by recent Docker versions, and a Bluetooth adapter that tends to freeze after a few hours. |
| Raspberry Pi 3, 4, 5 or mini-PC with Bluetooth | Suitable, as long as it is within range of the vehicle. |

The detailed procedure, with commands, settings and troubleshooting, is on the [Installing the BLE proxy](installation-proxy.md) page. In short, the installation consists of:

1. Installing Raspberry Pi OS **64-bit Lite** and Docker.
2. Running the `ghcr.io/superdcat/tesla-ble-http-proxy` image (fork recommended; the `wimaha/tesla-ble-http-proxy` image remains an alternative).
3. Opening `http://<pi_ip>:8080/dashboard`, generating the key, entering the VIN, **waking up the vehicle**, sending the key, then placing the key card on the center console to validate.
4. Giving the Raspberry Pi a **fixed IP address** (DHCP reservation on your router), since its address is saved in the plugin.

A few tips for stable operation:

- Use a quality power supply (5 V, 2.5 A): a weak power supply causes Bluetooth disconnections.
- Do not use this Raspberry Pi's Bluetooth for anything else: the proxy needs the adapter for itself.
- A vehicle only accepts **3 Bluetooth devices connected at the same time** (phones, watch, proxy). Beyond that, connections become intermittent.

### Key role

With TeslaBleHttpProxy (fork or wimaha 2.3.0), the key generated by default has the **Charging Manager** role. It is enough to read the vehicle state and control charging, but the vehicle **refuses** some commands. To use them, generate and pair a key with the **Owner** role from the proxy dashboard (link in the plugin configuration).

| Key role | Commands concerned (indicative list) |
|---|---|
| **Charging Manager**: works | Reads (presence, lock, charging, climate control), **Refresh**, **Wake up**, **Start charging**, **Stop charging**, **Set charge current** |
| **Charging Manager**: works (advanced charging functions) | **Adjust to surplus** and **Off-peak hours charging** only send **Set charge current**, **Start charging** and **Stop charging**: a Charging Manager key is enough. |
| **Charging Manager**: not confirmed | **Add charge schedule** and **Delete charge schedule**: the minimum role is not confirmed (Charging Manager probable; try it, and switch to Owner if the vehicle refuses). These two actions also require the fork proxy (see [Scheduling charging](#scheduling-charging)). |
| **Charging Manager**: refused | **Lock doors**, **Unlock doors**, **Honk horn**, **Flash lights**, **Sentry Mode**; probably also **Start climate control** and **Stop climate control** |
| **Charging Manager**: refused (probable) | **Driver setpoint** and **Passenger setpoint**: the Owner role is assumed to be required (not confirmed in real use). These two actions also require the fork proxy (see [Setting the temperature setpoint](#setting-the-temperature-setpoint)). |
| **Charging Manager**: refused (probable) | The six **Set … seat heater** actions and **Set steering wheel heater**: the Owner role is assumed to be required (not confirmed in real use). They also require the fork proxy (see [Heating the seats and steering wheel](#heating-the-seats-and-the-steering-wheel)). |
| **Charging Manager**: refused (probable) | **Max defrost**: the Owner role is assumed to be required (not confirmed in real use). This action also requires the fork proxy (see [Max defrost](#max-defrost)). |
| **Charging Manager**: refused (probable) | **Climate keeper mode**: the Owner role is assumed to be required (not confirmed in real use). This action also requires the fork proxy (see [Dog mode, camp mode and climate keeper](#dog-mode-camp-mode-and-climate-keeping)). |
| **Charging Manager**: refused (probable) | **Open rear trunk** and **Open frunk**: the Owner role is assumed to be required (not confirmed in real use). These two actions also require the fork proxy (see [Opening the rear trunk and the frunk](#opening-the-rear-trunk-and-the-frunk)). |
| **Charging Manager**: refused (probable) | **Preconditioning scheduled by Jeedom**: it only sends **Start climate control** and **Stop climate control**, for which the Owner role is assumed to be required (not confirmed in real use). With a Charging Manager key, only one attempt is made per departure (see [Preconditioning scheduled by Jeedom](#preconditioning-scheduled-by-jeedom)). |
| **Owner** | All commands |

This list is indicative: the vehicle decides.

**The plugin recognizes this refusal.** When one of the commands in the “refused” rows above is refused by the vehicle for lack of rights:

- the message “This command requires an Owner role key: the proxy key probably has the Charging Manager role…” is displayed (it is also copied into **Last error**);
- the **Key role** information of the equipment changes to **Charging Manager**;
- in the **Commands** tab of the equipment, these commands carry a gray **Insufficient role** badge.

The commands remain present and usable: a scenario that calls them receives the same message. They are **not grayed out on the dashboard**: rely on the **Key role** information. The plugin does not warn you in advance: it is the first refusal that reveals the role.

**Switching to an Owner key.** Generate and pair a key with the **Owner** role by following [Generating the key and pairing it with the vehicle](installation-proxy.md#8-generating-the-key-and-pairing-it-with-the-vehicle) (role choice: [Choosing the key role](installation-proxy.md#choosing-the-key-role)). Then run one of these commands again: as soon as it succeeds, **Key role** goes back to **Owner** and the badge disappears when the page is reloaded.

With the fork image, the role of the active key can also be read by hand: open `http://<proxy_ip>:<port>/api/proxy/1/capabilities` and look at `key_role` (`owner` or `charging_manager`, empty if no key is installed); the plugin does not use this information. The behavior of **Set charge limit** and of opening and closing the charge port with a Charging Manager key is not confirmed: the [proxy documentation](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md#step-3-generate-key-for-vehicle) only mentions waking up, starting and stopping charging and the charge current.

> **IMPORTANT**
>
> The proxy has **no authentication** by default. The fork can require a token (`apiToken`): in that case, enter the same one in **Proxy API token** (see [Plugin configuration](#plugin-configuration)). With an Owner key, any device on your local network can unlock the vehicle. Keep the proxy on a trusted network, ideally isolated, and **never** expose its port on the Internet. If you only control charging, prefer a Charging Manager key.

## Plugin configuration

After installation, enable the plugin then open its configuration page (**Plugins > Plugins management > Tesla BLE**). It has three settings: the proxy URL, the proxy API token (optional) and the frozen Bluetooth alert threshold.

| Field | Expected value |
|---|---|
| **Proxy URL** | The address of TeslaBleHttpProxy with its port, for example `http://192.168.1.50:8080/`. It must start with `http://` or `https://`. A single proxy is used for all vehicles. |
| **Proxy API token** | Optional: fill in only if the fork proxy has an `apiToken` (same value). The same token is used for all proxies. It is saved **encrypted** and **is never displayed again**: the field stays empty and shows “Token saved: leave empty to keep it”. Leave it empty to keep the saved token; **Delete the token** erases it. |
| **Test** (button) | Checks that the proxy responds and shows its version. It tests the URL and token entered, **even if not saved** (empty token field: the saved token). It also reports the authentication: **“Proxy without authentication: no token required”**, **“API token accepted by the proxy”**, **“The proxy requires an API token”** (no token entered or saved) or **“API token refused by the proxy”** (token different from `apiToken`). |
| **Open the proxy dashboard (key pairing)** (link) | Opens the proxy dashboard in a new tab, to generate and pair the key. |
| **Proxy logs** (button, **Diagnostics** row) | Shows the last lines of the proxy logs in a window, without an SSH session on the Raspberry Pi. Uses the **saved** URL. |
| **Frozen Bluetooth alert threshold** | Number of consecutive timed-out reads, while the proxy responds, before warning you that the Raspberry Pi's Bluetooth adapter is probably frozen. Whole number from 2 to 288 (a read takes place at the vehicle's refresh interval, 5 minutes by default: 288 = one day of reads at this default); leave empty for the default value, **3**, shown in gray. See [Frozen Bluetooth adapter alert](#frozen-bluetooth-adapter-alert). |
| **Minimum proxy version** | Read-only information: the minimum TeslaBleHttpProxy version supported (2.3.0). |

### The URL is normalized when saved

You do not have to worry about the exact form of the address: when saving, the plugin removes the spaces around the URL, lowercases `http`/`https` and **adds the trailing `/`** if needed: the trailing `/` and the case of `http://` therefore do not matter, `HTTP://192.168.1.50:8080` and `http://192.168.1.50:8080/` designate the same proxy. After saving, the field shows the corrected address.

The URL is refused, with a red message and without the old value being modified, in the following cases:

- it is empty or does not start with `http://` or `https://`;
- it contains credentials (`user:password@`);
- it contains disallowed characters (spaces in the middle, accents, `?...` parameters, `#...` anchor), an invalid port, or exceeds 255 characters.

### Testing the proxy

Click **Test**: the plugin queries the proxy version (10 seconds at most) and shows the result under the field. The test checks neither the paired key nor the vehicle: it only proves that the proxy is reachable. See [Troubleshooting](#troubleshooting) for the meaning of each message.

### Link to the proxy dashboard

The link appears as soon as a valid URL is saved (or tested). It points to `<proxy URL>dashboard`. If you declared the proxy with a **Docker service name** (for example `http://teslablehttpproxy:8080/`), Jeedom can reach it but **your browser cannot**: the link will not open. Then open the dashboard with the Raspberry Pi's IP address (`http://<pi_ip>:8080/dashboard`).

### Viewing the proxy logs

The **Proxy logs** button opens a window that shows the **last 200 lines** of the proxy logs (most recent at the bottom), with their time in the Jeedom time zone and their level (`[DEBUG]`, `[INFO]`, `[WARN]`, `[ERROR]`). The **Refresh** button re-reads the logs. Reading does not wake the vehicle and responds within 10 seconds at most, even while a command is keeping the proxy busy.

- The function requires proxy **2.3.0** or newer and uses the **saved** URL: after changing the URL, save before opening the logs.
- The lines are displayed **as is**, in plain text: content such as `<script>` or `&` appears literally, with no effect. Each line is limited to 1000 characters.
- VINs are masked (only the last 4 characters remain visible). Lines may contain the IP address of the proxy's clients and the content of the commands sent: reread a screenshot before publishing it on a forum.
- The proxy also keeps its **Debug** lines, whatever its log level: the 200 lines therefore often cover less than an hour of activity. Its logs are erased each time the proxy restarts.
- The proxy lines are never copied into the plugin log. Function reserved for Jeedom administrators.

See [Messages of the Proxy logs window](#proxy-logs-window-messages) in case of an error message.

### Frozen Bluetooth adapter alert

On some Raspberry Pi boards (notably the first-generation Zero W), the Bluetooth adapter freezes after a few hours: the proxy still responds (the **Test** button is green, **Proxy reachable** is 1) but every vehicle read times out. The plugin detects this situation and warns you:

- when reading a vehicle's state times out **3 times in a row** (or the configured threshold) while the proxy responds, a message **“Proxy Bluetooth adapter probably frozen — …”** appears in the Jeedom message center, **only once** as long as the situation lasts;
- meanwhile, **Last error** shows **“Proxy Bluetooth adapter probably frozen: restart the Raspberry Pi”**;
- as soon as a read succeeds again (including a sleeping vehicle that responds), the log notes the return to normal (**Info** level) and the alert is re-armed: a new series will trigger a new message, which replaces the old one.

An isolated timeout, an out-of-range vehicle or a powered-off proxy do not trigger the alert. The message stays in the message center after the return to normal: delete it yourself. With several vehicles on the same proxy, each vehicle has its own message. Clicks on **Refresh** count as reads.

What to do: restart the Raspberry Pi that hosts the proxy. If it happens again, switch to a Raspberry Pi Zero 2 W and use a quality power supply (5 V, 2.5 A).

## Equipment configuration

Each vehicle is an equipment. Go to **Plugins > Connected objects > Tesla BLE**, click **Add** and give the vehicle a name.

In the **Equipment** tab:

| Field | Expected value |
|---|---|
| **Equipment name** | The name of the vehicle, your choice. |
| **Parent object** | The Jeedom object in which to place the vehicle (or **None**). |
| **Category** | The equipment's Jeedom categories (checkbox). |
| **Enable** | Checked: the vehicle is refreshed at its **refresh interval** (5 minutes by default). Unchecked: it is no longer read, whatever its interval. |
| **Visible** | Checked: the vehicle widget is displayed on the dashboard. |
| **VIN** | The vehicle's serial number: **17 characters**, digits and letters **except I, O and Q** (fictitious example: `5YJ3E1EA7KF000000`). It must be the one declared in TeslaBleHttpProxy. |
| **Proxy URL of this vehicle** | Optional. The address of the proxy in this vehicle's garage, with its port (for example `http://192.168.1.51:8080/`). **Empty: the vehicle uses the URL from the plugin configuration.** |
| **Test this proxy** (button) | Shows the version of the proxy this vehicle uses. It tests the value entered, **even if not saved**; empty field: the URL from the plugin configuration is tested. |
| **Refresh interval** | How often this vehicle is read: **1, 2, 5, 10, 15 or 30 minutes**. Default **5 minutes** (existing vehicles keep this behavior after the update). The shorter the interval, the fresher the information, but the more the proxy is used and, with the vehicle awake, the more its falling asleep may be delayed; a long interval spares the Raspberry Pi. **1 minute** suits one or two vehicles per proxy (recommended; adjust to your installation): beyond that, a slow read may exceed one minute. An unknown value is brought back to 5 minutes. A change takes effect at the next read, without restart. This read never wakes the vehicle. |
| **Interval while charging** | **Disabled by default** (behavior unchanged), or **1, 2, 5, 10 or 15 minutes**. During charging, it replaces the refresh interval **when it is shorter**; the normal rate resumes as soon as a read no longer finds charging. One minute at minimum: Jeedom launches the refresh every minute and the proxy keeps data cached for 30 seconds. Never wakes the vehicle. See [Faster reading while charging](#accelerated-read-during-charging). |
| **Let the vehicle fall asleep** (**Enable** checkbox) | Checked by default (including on existing vehicles after the update). When the vehicle is awake but inactive, the plugin stops reading charging and climate data during a window, so as not to prevent it from falling asleep. Unchecked: a full read takes place at every pass, as before. See [Letting the vehicle fall asleep](#let-the-vehicle-fall-asleep). |
| **Unchanged reads before the window** | Number of successive reads without any change (not charging, no occupant) before opening the window: **1, 2, 3, 4, 5, 10 or 15**. Default **3** (15 minutes of inactivity at the 5-minute interval). |
| **Window duration** | Duration during which data is no longer read: **15, 20, 30, 45 minutes, 1 hour, 1 hour 30 minutes or 2 hours**. Default **30 minutes**. No effect if it does not exceed the refresh interval: choose a duration longer than the interval. |
| **Re-read delay after command** | Waiting time before re-reading the vehicle after a successful command: **30 seconds (default), 45 seconds, 1 minute, 1 minute 30 seconds or 2 minutes**. 30 seconds is the minimum: it is how long the proxy keeps its data cached (see [Re-reading after a command](#re-read-after-a-command)). Lengthen it if you have lengthened this cache in the proxy. |
| **Also read the climate** | **Yes (default)**: charging and climate are read, as before the update. **No, charge only**: only charging data is requested from the proxy, at every refresh as well as on demand (**Refresh**, **Refresh (with wake-up)**, re-read after a command). The request is shorter and puts less load on the Bluetooth link (the gain is to be measured on your installation). The climate information then keeps its last value and is no longer updated; the climate commands remain usable. Switching back to **Yes** resumes reading both families at the next pass, with the vehicle awake. |
| **Grid voltage (V)** | Surplus control: phase-to-neutral voltage used to convert the available power into current. Empty: **230 V**. Whole number from 100 to 250. |
| **Phases** | Surplus control: **Single-phase (default)** or **Three-phase**. The power is divided by the voltage and by this number to get the current **per phase**. |
| **Adjustment step (A)** | Surplus control: the calculated current is rounded **down** to a multiple of this step. Empty: **1 A**. Whole number from 1 to 16. |
| **Hysteresis (A)** | Surplus control: no command as long as the calculated current differs by **less** than this value from the last setpoint sent. Empty: **2 A**. Whole number from 0 to 16. |
| **Minimum interval between commands (s)** | Surplus control: minimum delay between the **end** of one control command and the next. Empty: **120 s**. Whole number from 60 to 3600 (a command can last up to 75 seconds and the proxy keeps data cached for 30 seconds). |
| **Minimum starting current (A)** | Surplus control: with charging stopped, it is restarted when the calculated current reaches this value. Empty: **6 A**. Whole number from 1 to 80. |
| **Stop threshold (A)** | Surplus control: during charging, the current is never set below this threshold; if it stays calculated below it for the hold time, charging is stopped. Empty: **5 A**. Whole number from 1 to 80, **never greater than the minimum starting current**. |
| **Hold time before stopping (s)** | Surplus control: how long the calculated current must stay below the stop threshold before charging is stopped. Empty: **300 s**. Whole number from 0 to 3600. |
| **Charging control** (**Enable** checkbox, **Off-peak hours charging** section) | **Unchecked by default.** Checked, Jeedom starts and stops charging during the time range below (see [Off-peak hours charging](#off-peak-hours-charging)). It only activates if the start, the end and the target SoC are filled in. |
| **Range start** | Off-peak hours charging: start time of the range, in `HH:MM` format (Jeedom time, for example `22:00`; `22h00` is also accepted). |
| **Range end** | Off-peak hours charging: end time of the range, in `HH:MM` format, **different** from the start. An end earlier than the start gives a range **spanning midnight** (`22:00` to `06:00`). |
| **Target SoC (%)** | Off-peak hours charging: battery level at which charging is stopped during the range. Whole number from **1 to 100**. |
| **Stop at end of range** | Off-peak hours charging: **unchecked by default**. Checked, charging still in progress at the end of the range is stopped (at the first read of the vehicle, within the following hour). Unchecked, it continues up to the vehicle's limit. |
| **Climate control** (**Enable** checkbox, **Preconditioning scheduled by Jeedom** section) | **Unchecked by default.** Checked, Jeedom starts climate control before the departure time then stops it (see [Preconditioning scheduled by Jeedom](#preconditioning-scheduled-by-jeedom)). It only activates if the departure time is filled in, at least one day is checked and **Also read the climate** remains on **Yes**. |
| **Departure time** | Scheduled preconditioning: time at which the vehicle must be ready, in `HH:MM` format (Jeedom time, for example `07:30`; `7h30` is also accepted). |
| **Days** | Scheduled preconditioning: **departure** days concerned (**Monday** to **Sunday** checkboxes). The day used is that of the departure time, even if climate control starts the day before, before midnight. No box checked: function refused at activation. |
| **Lead time (min)** | Scheduled preconditioning: minutes before the departure time at which climate control is started. Whole number from **1 to 60**. Empty: **15 minutes**. |
| **Maximum duration (min)** | Scheduled preconditioning: duration, **counted from the planned start**, after which Jeedom stops climate control. Whole number from **1 to 120**, **at least equal to the lead time**. Empty: **30 minutes** (or the lead time plus 15 minutes if it exceeds 15), i.e. a stop **15 minutes after departure** with the default lead time. |
| **Only if plugged in** | Scheduled preconditioning: **unchecked by default**. Checked, climate control is not started if the vehicle is unplugged or if its charging state is unknown. A charger that supplies no current counts as plugged in: climate control then draws from the battery. |
| **Latitude** (**Home position** section) | Home position, to compute **At home**: decimal degrees from -90 to 90, for example `48.8566` (comma accepted, 8 decimals at most). **Empty: the Jeedom position** (**Settings > System > Configuration**, **General** tab). To be filled in together with the **longitude**: only one of the two is refused. See [Position and privacy](#position-and-privacy). |
| **Longitude** (**Home position** section) | Decimal degrees from -180 to 180, for example `2.3522`. Empty with the latitude empty: Jeedom position. |
| **Radius (m)** (**Home position** section) | Maximum distance, in meters, between the vehicle and home for **At home** to be 1. Whole number from **10 to 10000**. Empty: **100 m**. No effect if the proxy does not provide the vehicle position. |
| **Description** | Free text, optional. |

The buttons at the top of the page are those of any Jeedom equipment: **Advanced configuration**, **Duplicate**, **Save** and **Delete**. The **Commands** tab lists the vehicle's commands (see [Commands](#commands)).

On save:

- The plugin creates the equipment's missing commands. **It launches no refresh**: the page responds immediately, even if the proxy is off. The information arrives at the next read (within the following minute for a new vehicle), or immediately with the **Refresh** command.
- The VIN is **normalized**: spaces removed, letters uppercased. It can be left empty, but the vehicle is then not read (see [Troubleshooting](#troubleshooting)).
- The VIN is **unique**: a vehicle can only have one equipment. An invalid VIN, or one already used by another equipment, is refused with a message.
- **Duplicating** a vehicle is therefore **refused**: the copy carries the same VIN. For a second vehicle, use **Add**.
- The **Proxy URL of this vehicle** is normalized like the one in the plugin configuration (see [The URL is normalized when saved](#the-url-is-normalized-when-saved)); an invalid URL is refused with the same message.

### One proxy per vehicle (several garages)

If your vehicles are parked in different places, each with its own Raspberry Pi, fill in the **Proxy URL of this vehicle** on each equipment. All its reads and commands then go through this proxy, and the **Open the proxy dashboard** link in the pairing section points to it. If a proxy stops, only the vehicles that use it go into error. Emptying the field brings the vehicle back to the URL from the plugin configuration at the next cycle; its commands and history do not change.

- Always write a given proxy **with the same URL** (same IP address or same name, same port): the plugin recognizes a proxy by its URL.
- The **Proxy logs** button in the plugin configuration shows the logs of the **plugin configuration** proxy only.

### Pairing my key and checking the pairing

Under the **VIN** field, the **Pair my key** section recalls the pairing steps, which are done in the proxy dashboard (details: [Generating the key and pairing it with the vehicle](installation-proxy.md#8-generating-the-key-and-pairing-it-with-the-vehicle)). Once the VIN is saved and the proxy URL filled in, it also shows the **Open the proxy dashboard** link (new tab), the VIN to copy into **Setup Vehicle**, and the **Check pairing** button.

**Check pairing** reads the vehicle state through the proxy **without waking it** (50 seconds at most) and sends no command. The plugin never generates or deletes a key: only the proxy dashboard does.

| Message | What to do |
|---|---|
| **Pairing verified: the vehicle responds to the proxy key** | Nothing. With the fork image, the **Role of the active proxy key** line also shows Owner or Charging Manager. The **Key role** information of the equipment, however, only changes at the next restricted command (see [Key role](#key-role)). |
| **Proxy without key: …** | No key on the proxy: generate one (**Generate**), then send it to the vehicle. |
| **Key not paired with this vehicle: …** | Wake up the vehicle, send the key (**Send key**), then place the key card on the center console. |
| **Vehicle out of Bluetooth range of the proxy: …** | Move the vehicle or the Raspberry Pi closer, check the VIN. |
| **Proxy unreachable: …** | Check that the proxy is running, then its address with the equipment's **Test this proxy** button. |
| **Proxy busy with a command or a read: …** | Run the check again in a moment. |

The check uses the **saved** VIN: save the equipment after changing it.

## Topologies: one or several proxies, one or several vehicles

The plugin can control several vehicles, with a single proxy or with several. A proxy URL is entered in two places: in the **plugin configuration** (the default address, used by all vehicles that do not have their own) and, optionally, in the **Proxy URL of this vehicle** field of each equipment.

### Diagrams

One Raspberry Pi, several vehicles (same garage): the URL is entered **only once**, in the plugin configuration; the field of each vehicle stays empty.

```
Jeedom ---> Garage proxy (Raspberry Pi A) --BLE--> Vehicle 1 (VIN 1)
                                          --BLE--> Vehicle 2 (VIN 2)

URL: plugin configuration  = http://192.168.1.50:8080/
URL: field of each vehicle = empty
```

Several Raspberry Pis, several garages: the URL of each proxy is entered **in the equipment of each vehicle**. The plugin configuration can stay on the main proxy (it serves as the default value and for the **Proxy logs** button).

```
Jeedom ---> Garage A proxy (Raspberry Pi A) --BLE--> Vehicle 1
       |
       +--> Garage B proxy (Raspberry Pi B) --BLE--> Vehicle 2

URL: plugin configuration = http://192.168.1.50:8080/   (proxy A, default)
URL: vehicle 1 field      = empty (or http://192.168.1.50:8080/)
URL: vehicle 2 field      = http://192.168.1.51:8080/
```

### Adding a second vehicle on the same proxy

The proxy, the Raspberry Pi and the URL in the plugin configuration are already in place for the first vehicle. For the second one:

1. In **Plugins > Connected objects > Tesla BLE**, click **Add** (not **Duplicate**, which is refused: the VIN is unique), name the vehicle, enter its **VIN** and leave **Proxy URL of this vehicle** empty. **Save**.
2. In the **Pair my key** section of this new equipment, click **Open the proxy dashboard**.
3. In the dashboard, enter the VIN of the second vehicle in **Setup Vehicle**, wake up that vehicle, click **Send key**, then place the key card on its center console to confirm. The **same key** of the proxy must be paired with each vehicle: do not generate a second key. See [Key role](#key-role) for choosing the role.
4. Go back to the equipment and click **Check pairing**: wait for **Pairing verified: the vehicle responds to the proxy key**. Otherwise, see the table in [Pair my key and check the pairing](#pairing-my-key-and-checking-the-pairing).
5. Click **Refresh** (or wait one minute): the information of the second vehicle appears.

A vehicle only accepts **3 Bluetooth devices connected at the same time** (phones, watch, proxy): beyond that, connections become intermittent. Each vehicle keeps its own **Last error**: a vehicle that is out of range or whose key is not paired does not affect the other. They do, however, share the same Raspberry Pi: exchanges take place one after the other (see [Why calls are sequential](#why-calls-are-sequential)).

### Adding a second proxy for another garage

1. Install the proxy of the second garage on its own Raspberry Pi, with a fixed IP address (see [Installing the BLE proxy](installation-proxy.md)), then generate the key and pair it with the vehicle of that garage.
2. In the equipment of that vehicle, enter the address of the second proxy, with its port, in **Proxy URL of this vehicle**, for example `http://192.168.1.51:8080/`.
3. Click **Test this proxy**: the message **Proxy reachable — version X** confirms that **this** proxy responds (the test applies to the entered value, even if it is not saved). Otherwise, see [Test button messages](#test-button-messages).
4. **Save**, then use **Check pairing** to check the key of this vehicle.
5. The **Open the proxy dashboard** link of this equipment then opens the dashboard of the second proxy.

The **Proxy logs** window in the plugin configuration only shows the proxy of the **plugin configuration**: to read the logs of the second proxy, open its own in a browser (`http://<second_pi_ip>:8080/dashboard`). Each vehicle has its own **Proxy reachable** information, and the frozen adapter alert is specific to each vehicle. The same API token is used for all proxies.

## Updating from version 0.x

You are updating the plugin from a 0.x version: nothing needs to be redone.

> **IMPORTANT**
>
> Your **equipment, VINs, commands, histories, scenarios and display settings are kept**. Commands keep their identifiers: the scenarios, widgets and histories that use them keep working without any change.

### Command names

An equipment **migrated from version 0.x keeps the names of its commands** (for example “Etat Charge”, “Charge Start”, “Rafraichir”): only the identifiers matter for scenarios. The commands of a **new equipment** carry the labels from the table in the [Commands](#commands) section. You can freely rename a command.

During the update, the commands missing from your equipment are added **next to the commands of the same theme** (as a block at the end of the list only if no command of that theme exists, see [Command order](#command-order)): **Charge time remaining**, **Charge port open**, **Last error**, **Last data read**, **Proxy reachable**, **Proxy version**, **Key role** (which is **Undetermined** until the first command reserved for the Owner role), **State read duration** and **Data read duration** (empty until the first successful read), then **Data age (min)** (which is 99999 until the first known read), then **Minimum charge limit**, **Maximum charge limit** and **Maximum charge current** (hidden, empty until the first data read), and finally ten extended charge information items, also hidden (see [Information](#information-commands)). A slider **Max** that you had set by hand is kept. On an existing equipment, the action that opens the charge port may be called “Trappe de Charge Ouvert”: rename it if needed.

### Range and charge rate

The **Range** and **Charge rate** commands are now converted to km and km/h (the vehicle sends them in miles). Values already recorded in the history stay in miles: the **Range** graph therefore shows a **break** (a jump by a factor of about 1.6) at the time of the update. Earlier values are not converted.

### Scheduled departure time

The **Scheduled departure time** command now displays the time in `HH:MM` format (for example `07:30`), and stays empty when no departure is scheduled. It used to give a numeric timestamp: adapt the scenarios that compared it to that number.

If you enabled history on this command, it stays numeric and is no longer updated; a message tells you so in the Jeedom message center. To receive the time, change its sub-type to **Other** in the **Commands** tab of the equipment.

### Action commands

- The **“None”** option of **Sentry Mode** is removed (the proxy did not understand it). A scenario that sent it now receives an error: use **Enabled** or **Disabled**. The update removes this option from existing equipment, without touching the other settings of the command.
- A **charge current out of the bounds** of the command, or not a whole number, is refused instead of being sent.
- A command that used to fail silently now displays an **error** and feeds the **Last error** information.

### Minimum versions

| Item | Version |
|---|---|
| Jeedom | 4.5 minimum |
| Debian | 11 or 12 |
| TeslaBleHttpProxy | 2.3.0 minimum (see [Checking and updating the proxy version](#checking-and-updating-the-proxy-version)) |

If your Jeedom is below version 4.5, Jeedom refuses the update with the message “Version du core Jeedom non supportée” (*“Jeedom core version not supported”*). The old version of the plugin then stays in place and keeps working. Update Jeedom first. Debian 10 is no longer supported.

### What is done automatically

On update, then on plugin activation, an upgrade of the existing equipment runs automatically, in successive levels. Each level is applied only once. Depending on the versions, it fixes or completes some equipment (VIN, missing commands, scheduled departure time, removal of the “None” option of Sentry Mode, sleep window settings…) without touching your settings (name, visibility, history). Existing vehicles receive the sleep window **enabled** (3 unchanged reads, 30 minutes); uncheck it in the equipment if you do not want it.

The eight opening information items (doors, trunks, charge port, tonneau cover) are created **visible and historized**; your existing settings are never modified.

The **Occupant present** (visible, historized) and **Detailed lock state** (visible, not historized) information items are created the same way; your existing settings are never overwritten.

The **Sentry** and **Sentry source** information items (visible, not historized) are created the same way, with the values **Unknown** and **None** as long as nothing has been read or ordered; your existing settings are never overwritten (see [Sentry Mode state](#sentry-mode-state)).

The **Openings alert** and **Unlocked unoccupied alert** information items (hidden, historized) are created the same way, at **0**; the alerts stay **disabled** until you enable them (see [Prolonged opening alerts](#prolonged-opening-alerts)).

If the upgrade fails on a vehicle, it is automatically retried at the next update or activation of the plugin.

### Checking the upgrade in the log

Set the plugin log to at least the **Info** level (**Plugin configuration > Logs**), then update or reactivate the plugin and open its log. The lines concerned start with “Migrations :” (*Migrations:*).

| Situation | Message in the log |
|---|---|
| Upgrade succeeded | `Migrations : migration N (<description>) appliquée sur X équipement(s) sur Y.` (*Migrations: migration N (<description>) applied on X equipment(s) out of Y.*) for each level applied, then `Migrations : niveau de migration N atteint.` (*Migrations: migration level N reached.*) |
| Already up to date | `Migrations : aucune migration à appliquer, niveau de migration N.` (*Migrations: no migration to apply, migration level N.*) (N = last level) |
| No equipment (fresh install) | `Migrations : aucun équipement à migrer, niveau de migration N (aucune migration exécutée).` (*Migrations: no equipment to migrate, migration level N (no migration run).*) (N = last level) |
| Failure on an equipment | `Migrations : échec de la migration N (...) sur l'équipement « <nom> » (id <n>) : ...` (*Migrations: migration N (...) failed on equipment “<name>” (id <n>): ...*) followed by `Elle sera retentée à la prochaine mise à jour ou activation du plugin.` (*It will be retried at the next update or activation of the plugin.*), then `Migrations : niveau de migration M conservé, X équipement(s) en échec ; les migrations restantes seront retentées à la prochaine mise à jour ou activation du plugin.` (*Migrations: migration level M kept, X equipment(s) failed; the remaining migrations will be retried at the next update or activation of the plugin.*) |

If a failure message persists after several updates, note it down and report it together with the plugin log.

## How it works

### Vehicle sleep and data freshness

An awake Tesla falls asleep on its own after **about fifteen minutes** without any request. Several things keep it awake: **Sentry Mode**, an **occupant** on board (or a phone key nearby), a **charge** in progress, the **Tesla app** being open, and any read of its charge and climate data. A sleeping vehicle uses very little; a vehicle kept awake constantly draws on the battery.

This is the trade-off to know: **the more often you read, the fresher the information, but the more likely the vehicle is to never fall asleep**. The rate settings of this plugin let you choose your balance point (see [Summary of rate and wake-up settings](#summary-of-the-rate-and-wake-up-settings) and [Recommendations by use](#recommendations-by-use)).

> **IMPORTANT**
>
> **The plugin never wakes the vehicle on its own, except through an explicit action from you or from a scenario.** Neither the periodic refresh, nor the accelerated read during charging, nor the re-read after a command wakes the vehicle: they read the state without waking it, then the data only if the vehicle is already awake. To read the data of a sleeping vehicle, you have to **ask for it** with the **Refresh (with wake-up)** command (see [Refresh with wake-up](#refresh-with-wake-up)). **Wake up** and the action commands (charge, climate, lock…) also wake the vehicle, through the proxy, since you requested them.

To know whether the displayed values are recent, look at **Last data read** and **Data age (min)**: a sleeping vehicle or an open sleep window is not an error, but the charge and climate values then get older (see [Step-by-step example: only act on recent data](#step-by-step-example-only-act-on-recent-data)).

### Refreshing the information

At the **interval of each vehicle** (5 minutes by default, adjustable from 1 to 30 minutes in the equipment), the plugin refreshes that vehicle in two steps:

1. It queries the **body controller** state (`body_controller_state`). This request does not wake the vehicle. It updates presence, lock and sleep state.
2. **Only if the vehicle is awake**, it retrieves the vehicle data (`vehicle_data`): charge, battery, range and, depending on the **Also read the climate** setting of the equipment (enabled by default), climate.

A Jeedom task, **TeslaBLE::cycleRafraichissement**, fires **every minute** and only reads the active vehicles whose interval has elapsed (measured from the start of their last read): with one vehicle at 1 minute and another at 15 minutes, the first is read on every run and the second about every 15 minutes. A vehicle that has never been read is read on the very next run. A proxy with no vehicle to read is not queried. This task is created on plugin activation and update (see [Troubleshooting](#troubleshooting)).

The plugin therefore never wakes the vehicle on its own, so as not to drain the battery. As long as the vehicle sleeps, the charge and climate information keeps its last known value. To refresh it on demand, use the **Refresh (with wake-up)** command (see [Refresh with wake-up](#refresh-with-wake-up)).

If the vehicle falls asleep between the two requests, this is not an error: the charge and climate information keeps its last value and nothing is displayed.

With **Also read the climate** set to **No, charge only**, the data request only asks for the charge (`vehicle_data?endpoints=charge_state`, visible in the plugin log at **Debug** level and in the proxy logs). **Last data read** and **Data read duration** then date the charge read, and **Data age (min)** counts the time elapsed since that charge read: the climate information, for its part, stays frozen.

If the vehicle is out of Bluetooth range of the proxy, the **Vehicle presence** command goes to 0. If it is the proxy that does not respond, has no paired key or responds too slowly, the presence keeps its last value.

**Several vehicles on the same proxy.** The vehicles of the same proxy are read one after the other, each with its own **Last error** and its own **Last data read**: a vehicle that is out of range or whose key is not paired does not prevent the others from being read. The cycle lasts at most 4 minutes; with 3 vehicles or fewer on the same proxy, it is never cut short, even in the worst case. Beyond that, the last vehicles may not be read: check their **Last data read**. When a cycle is cut short, the log receives **a single** warning per episode (“Avertissement non répété jusqu'au prochain cycle complet.” (*Warning not repeated until the next complete cycle.*)), then an **Info** line at the first complete cycle again.

**Why has the data stopped changing?** The **Last error** information gives the cause of the last read failure, followed by the reason returned by the proxy when it gives one (for example “Vehicle out of range — …” or “Proxy without key: pairing required — …”). It returns to **None** as soon as a read cycle succeeds. A sleeping vehicle is not an error: **Last error** stays at **None** and **Vehicle awake** is 0. The **Last data read** information tells you how old the charge and climate data are.

In the plugin log, a problem leaves only **two lines**: one when it starts, one when everything is back to normal (`Véhicule « <nom> » (id <n>) : retour à la normale après [<catégorie>].` (*Vehicle “<name>” (id <n>): back to normal after [<category>].*)), even if it lasts for hours. The level of the starting line depends on the cause: **Info** for a vehicle out of range (normal situation), **Error** for a configuration error (missing VIN or URL) or a proxy that is too old, **Warning** for the others. The ending line is always at **Info** level. **To see these lines, the plugin log must be at least at Info level** (**Plugin configuration > Logs**). As long as the problem lasts, the detail of each cycle stays visible at **Debug** level.

The vehicles of the same proxy are refreshed **one after the other**; different proxies are read **in parallel**. A vehicle that is out of range or in error does not prevent the following ones from being read, and the error is recorded in the log with the vehicle name.

- If a cycle lasts longer than the interval, Jeedom **skips** the following runs until it is finished: cycles never pile up. The plugin then writes it to the log at the end of the cycle (one warning per hour at most if the set interval is not met); the rate resumes as soon as the cycle is finished.
- A cycle does not exceed **4 minutes**: if there are many vehicles or the proxy is slow, the remaining vehicles are read at the next cycle (warning naming those vehicles).
- While a command, a **Refresh**, a **Refresh (with wake-up)** or a pairing check is in progress or is waiting for the same proxy, the cycle read is skipped without error; the next read catches up.
- With several proxies, the cycle reads the proxies in parallel: a proxy that is stopped, powered off, frozen or slow only delays its own vehicles (a stopped proxy costs a few seconds, up to about 5 s, per vehicle of that proxy), never those of the other proxies. The cycle lasts as long as its slowest proxy. Two different proxies never wait for each other, including in the periodic cycle; the commands and **Refresh** of the other proxies are not delayed either.

### Refresh with wake-up

The **Refresh (with wake-up)** command is the only way to read the charge and climate data of a sleeping vehicle. It first reads the state without waking, then wakes the vehicle if needed and reads its data, in a single action: at the end, **Vehicle awake** is 1 and the charge and climate are up to date. Allow 15 to 40 seconds in general; the plugin waits up to 75 seconds for the read after wake-up, during which Jeedom stays usable.

- **It wakes the vehicle** on every execution: repeated use drains the battery. After the read, the sleep window (see [Let the vehicle fall asleep](#let-the-vehicle-fall-asleep)) and the normal rate resume their rules; the vehicle may fall asleep again.
- **Out of range**: the state read without wake-up fails after 5 to 25 seconds, the wake-up is not attempted and an explicit message is displayed (see [Troubleshooting](#troubleshooting)).
- **Scenarios**: the command can be used in a scenario and is not blocked by an open sleep window, which it ends. Be careful not to trigger it in a loop (for example on the change of a vehicle information): each execution wakes the vehicle. On a sleeping vehicle, **Vehicle awake** briefly goes to 0 (state read before the wake-up) then to 1.
- **Refresh** keeps its behavior: it never wakes the vehicle.

### Accelerated read during charging

To follow a charge closely (solar surplus control, for example), set **Interval while charging** in the equipment (disabled by default):

- **Trigger.** As soon as a read finds that the vehicle is **charging** (charge state Charging or Starting), the charge interval replaces the refresh interval, provided it is shorter. With 5 minutes normally and 1 minute while charging, the data is re-read every minute (watch **Last data read**).
- **Return to normal.** As soon as a read no longer finds charging (end of charge, cable unplugged, charge suspended), vehicle asleep, out of range or proxy unreachable, the normal interval is counted from that read: no cycle of delay.
- **One-minute floor.** No value under one minute is offered: Jeedom runs the refresh every minute and the proxy keeps the data in cache for 30 seconds. A lower value saved by a script is brought back to 1 minute (warning in the log), an unknown value disables the setting.
- **No wake-up.** The content of a read does not change: the state is read without waking, then the data only if the vehicle is awake. The data of a sleeping vehicle is never read because of this setting.

To follow the mechanism, set the plugin log to **Debug**: one line indicates the switch to the charge interval, another the return to the normal interval.

Limits: the charge rate only starts at the first read that sees the charge (at most one normal interval later, or immediately with **Refresh**); during an open sleep window, a charge started without any visible change in the state read without waking is only seen at the check read; if the proxy has been set with a data cache duration of at least 60 seconds, the 1-minute reads are served to it from the cache; a suspended charge (Stopped state, cable plugged in) does not trigger the acceleration, and its resumption is only seen at the normal interval; a sleeping vehicle that is charging is not read faster; a read failure during charging brings back the normal interval until the next successful read.

### Let the vehicle fall asleep

An awake vehicle falls asleep on its own after about fifteen minutes without any request. A read of the charge and climate data every few minutes can prevent it and drain the battery. The plugin can therefore “make itself forgotten” when there is nothing new to read:

- **Opening.** When the vehicle is awake, **not charging** (charge state Disconnected, Complete, Stopped or No power), **without an occupant**, and its data and state are **unchanged** over the set number of reads (3 by default), the plugin opens a **sleep window** (30 minutes by default).
- **During the window**, only the read of the state without waking is done, at the vehicle interval (presence, lock, sleep, doors, trunks, charge port, occupant). The charge and climate data, **Last data read** and the data read durations are no longer updated: they keep their last value, as for a sleeping vehicle. The plugin never wakes the vehicle for these checks.
- **End of the window**, with a return to the full read from the next run (the same run for an activity): activity seen on the state without waking (unlock, door, trunk or charge port, occupant), command sent to the vehicle (explicit wake-up included), **Refresh** or **Refresh (with wake-up)** button, vehicle asleep, vehicle out of range, box unchecked, or end of the duration. At the end of the duration, a **check read** takes place: if nothing has changed, the window is extended.
- **Never while charging.** A vehicle that is charging, starting to charge or in an unknown charge state never opens a window.
- **Climate keeper active.** As long as **Climate keeper (dog, camp)** is `On`, `Dog` or `Party` (or another unexpected value), no window opens: the read continues at the vehicle interval, so that the **Interior temperature** stays up to date in dog or camp mode. `Off`, `Unknown` or a missing information item (for example climate not read) let the window open.
- **Climate not read.** With **Also read the climate** set to **No, charge only**, the window no longer sees climate activity (its information is not read). Toggling this setting resets the count of unchanged reads.

To follow the mechanism, set the plugin log to **Info** level: one line indicates the opening (“fenêtre d'endormissement ouverte pour … min … jusqu'à HH:MM environ” (*sleep window opened for … min … until about HH:MM*)) and another the end (“fin de la fenêtre d'endormissement après … min : …” (*end of the sleep window after … min: …*)). At **Debug** level, each suspended run is noted. To check the effect, watch **Vehicle awake**: it should go to 0 after the usual delay (about fifteen minutes), whereas it could stay at 1 without a window. This is an expected effect, not a guaranteed one: it depends on the vehicle. If the vehicle does not fall asleep, compare with the box unchecked.

Limits: a charge started without any visible change in the state read without waking (cable already plugged in, charge scheduled or started from the app) is only seen at the check read, that is at most the duration of the window plus one interval later; likewise for climate started from the app during the window. Plugging in a cable from a disconnected state is seen immediately (the charge port opens). A nearby phone key that keeps the occupant “present” prevents the window from opening.

### Command execution

Each action command is passed to the proxy, which waits for the vehicle's confirmation before responding. The plugin does not need to wake the vehicle before a command: the proxy takes care of it.

**Values checked before sending.** An invalid value is refused immediately, with a message, without sending anything to the proxy:

- **Charge current**: a whole number between the **Min** and the **Max** of the command (0 to 32 A as long as the vehicle has not published its bound, then the maximum current it announces). A decimal value (`16.5`) or a text is refused.
- **Charge limit**: a whole number between the **Min** and the **Max** of the command (50 to 100% as long as the vehicle has not published its bounds, then its minimum and maximum limits).
- **Sentry Mode**: **Enabled** or **Disabled** (the old “None” option no longer exists).

**Bounds followed from the vehicle.** At each successful data read, the plugin sets the **Min** and the **Max** of the **Set charge limit** and **Set charge current** sliders to what the vehicle accepts (**Minimum charge limit**, **Maximum charge limit** and **Maximum charge current** information items), and the widget slider follows without reloading the page. A value of 0, missing or inconsistent is ignored: the previous bounds are kept, as while the vehicle sleeps. **A manual setting takes precedence**: if you yourself enter a **Min** or a **Max** different from the one the plugin set, it is never modified again (even after several reads or a save of the equipment); an entered value equal to the one the plugin set stays followed (to freeze a bound, therefore enter a value different from the one set by the plugin); any other value, even equal to the vehicle's at that moment, is a manual setting; a bound that you widen beyond the vehicle's allows a setpoint that the vehicle may refuse. To return to automatic following, **empty** the field: it is restored at the next read. To freeze a bound (for example 48 A), set the **Max** by hand; to update the bounds right away, run **Refresh (with wake-up)**. The maximum current may depend on the charger plugged in and is not published when the vehicle is unplugged: the previous bounds then stay in place.

> **Change of behavior**: a setpoint **above the maximum announced by the vehicle** (for example 20 A when it announces 16 A) is now **refused** with a message, instead of being accepted and then silently brought back by the vehicle.

**On failure.** If the proxy or the vehicle refuses the command, an error message appears in red in the Jeedom interface (and in the plugin log as an error), and it is also recorded in the **Last error** information, where it stays displayed until the next successful read cycle (at the next read, 5 minutes at most by default). For example “This command requires an Owner role key: the proxy key probably has the Charging Manager role…” when a command reserved for the Owner role is refused: see [Key role](#key-role).

**After a successful command.** The charge limit, the charge current and the lock are updated immediately, then the vehicle state (presence, awake) is re-read without waking it. The vehicle is then **re-read once** after a delay (30 seconds by default, adjustable per vehicle), without waiting for the periodic read, to display the actual values (see [Re-read after a command](#re-read-after-a-command)). The command itself returns immediately.

**One command or read at a time.** Exchanges with the same proxy take place one after the other: a command, a **Refresh** or a pairing check only waits for the exchanges already in progress or already waiting on that proxy (up to about 2 minutes, 15 seconds for the check) and goes ahead of the periodic reads, which step aside and resume at the next cycle. The order of passage is not guaranteed between several simultaneous requests. Two different proxies never wait for each other, periodic cycle included (the cycle reads the proxies in parallel: see Refreshing). If the proxy and the vehicle are at the limit of their timeouts, the response may take 3 to 4 minutes. Jeedom stays usable during this time.

### Re-read after a command

Right after a command, the proxy still returns its previous data (it keeps them in cache for **30 seconds**). Rather than displaying an outdated value until the next refresh, the plugin **schedules a re-read** of the vehicle once that cache has expired:

- **Trigger.** After any **successful** command (charge limit, current, start or stop of charging, climate, lock, charge port, etc.). A failed command schedules nothing.
- **Delay.** By default **30 seconds** after the end of the command, adjustable per vehicle (**Re-read delay after command**: 30 seconds, 45 seconds, 1 minute, 1 minute 30 seconds or 2 minutes). Never less than 30 seconds, the proxy cache duration: a shorter delay would re-read the value from before the command. If you have lengthened this cache in the proxy, choose a delay at least equal to it.
- **The command does not wait.** It returns as soon as it is executed; the re-read runs in the background.
- **A single re-read for several commands close together.** Current then limit within a few seconds: only the re-read scheduled after the **last** command reads the vehicle, the previous ones give up on their own.
- **Content of the re-read.** That of a **Refresh**: the state without waking, then the charge and climate data **only if the vehicle is awake**. **It never wakes the vehicle**: if it has fallen asleep again, this is not an error: the last values are kept. If it is out of range, the presence goes to “No”; if the proxy is unreachable, “Last error” is filled in. It ends the sleep window, like a command, and does not shift the rate of the periodic refresh.
- **Wake up** therefore also re-reads the vehicle afterwards, without waking it again (the command has just done so).
- **Cost.** Each successful command adds **one Bluetooth read** (state, then data if awake) through the proxy. A scenario that sets the charge current every minute causes one re-read per minute, in addition to the periodic read: space out the commands of a scenario rather than repeating them. A horn honk or a light flash also triggers a re-read.
- **Process.** Each re-read is a **one-off task** of the Jeedom task engine (**Settings > System > Task engine**, **TeslaBLE::relectureApresCommande**): it is visible there for a few seconds to a few minutes, then disappears on its own. A re-read replaced by a more recent command disappears after a few seconds. This is not a daemon and nothing runs permanently. If the Jeedom task engine is disabled, no re-read takes place (as for the periodic refresh) and the values are updated at the next read.

To follow the mechanism, set the plugin log to **Debug**: one line indicates the scheduling (“relecture programmée dans 30 s” (*re-read scheduled in 30 s*)), then the re-read (“lecture sans réveil” (*read without wake-up*)) or its abandonment (“remplacée par une commande plus récente” (*replaced by a more recent command*), “abandonnée : proxy occupé” (*abandoned: proxy busy*)).

### Surplus control

The **Adjust to surplus** action (`adjust_surplus`) follows a photovoltaic surplus **without flooding the vehicle with Bluetooth commands**: each command can take up to 75 seconds and wakes the vehicle up. Your scenario sends the **power available for charging**, and the plugin decides whether it really needs to act. The default values must be validated in real-world use (see [Known limitations](#known-limitations)).

**The value sent is an absolute power, in watts.** It is what the vehicle can consume, not a variation. If your meter measures the **grid export**, the available power is **the export plus the current charging power**: without this addition, the setpoint would drop back at every adjustment. A negative value is brought back to 0 W; a value that is not a number of watts is refused with the message **“Invalid value: the available power must be a number of watts”**.

**From watts to amps.** The current per phase is the power divided by the **voltage** and by the number of **phases** (two equipment settings, never read from the vehicle), rounded **down** to the **adjustment step**. ⚠️ A three-phase charger set to single-phase would give **three times** the wanted current: check the **Phases** setting.

**When the plugin sends a command.** At most **one** command per call, among **Set charge current**, **Start charging** and **Stop charging**:

- the target current is capped by the **Max** of the **Set charge current** slider (a calculated value that is higher is brought back to the Max; conversely, typing by hand a value above the Max is still refused) and is never set **below the stop threshold** while charging;
- **nothing is sent** if the target current is identical to the last setpoint sent, or differs from it by less than the **hysteresis**;
- **at most one command per interval**: the **minimum interval** is counted from the **end** of the previous command, whether it succeeded or failed;
- **stop**: if the calculated current stays below the **stop threshold** for the **hold time**, charging is stopped;
- **start**: with charging stopped, it is restarted when the calculated current reaches the **minimum starting current**. The start happens in **two steps** when the last setpoint is not known, or when it exceeds the target current by at least the **hysteresis**: **Set charge current** first, **Start charging** at the next interval (one interval of delay). Once **Set charge current** has been sent while stopped, the setpoint is considered known **until charging has started**, whatever the rate of your scenario: **Start charging** then goes out directly. Without this handshake, the setpoint is considered known only if the last control command is less than 10 minutes old; it is also forgotten as soon as charging is complete, the charger has no more current, or the vehicle is unplugged (the first start the next day therefore begins with **Set charge current**).

**Abstentions.** No command is sent, with no exception in the scenario, and the reason appears in **Last error**: **“Vehicle not plugged in: surplus adjustment ignored”**, **“Vehicle out of range of the proxy: …”**, **“Charging complete: …”**, **“The charger supplies no current: …”** and **“Charging state unknown: run Refresh (with wake-up)”**. These messages never replace a real error from the last read cycle, and the next successful cycle puts back **None**. The control relies on the last published **Charge state**: after a start or a stop it has just commanded, it considers the commanded state until the next read (5 minutes at most). Enabling the **Interval while charging** is recommended.

**No wake-up.** The control never wakes the vehicle up and reads nothing to decide; an ignored call does not contact the proxy. A command that is actually sent wakes the vehicle up like any command.

**Off-peak hours.** During the range of a vehicle’s **Off-peak hours charging**, the **Adjust to surplus** call is **ignored** (no error, no command, a Debug line in the log): without this, a solar scenario that sends 0 W at night would stop the off-peak hours charging. Outside the range, surplus control works as usual (see [Off-peak hours charging](#off-peak-hours-charging)).

**Example scenario.** See the [step-by-step example: solar charging with Adjust to surplus](#step-by-step-example-solar-charging-with-adjust-to-surplus). Do not multiply the calls: the plugin ignores those that bring nothing.

**Invalid settings.** An out-of-range setting (step at 0, interval under 60 s, stop threshold higher than the starting current…) is **refused when the equipment is saved**, with a message **“Surplus control: …”**.

### Scheduling charging

The **Add charge schedule** (`add_charge_schedule`) and **Delete charge schedule** (`remove_charge_schedule`) actions create or remove in the vehicle **one charge schedule managed by Jeedom**. They are created **hidden**: you call them from a scenario (or make them visible from the **Commands** tab).

**Fork proxy required.** The official 2.3.0 proxy cannot schedule charging: the corresponding route does not exist in it, it was added by the fork (versions of the form `2.3.0-tb.N`). As long as the proxy does not announce these two commands, they are **refused immediately**, with no exchange at all with the vehicle, with the message **“Not supported by your proxy version”**; the rest of the equipment works normally. Availability follows the proxy’s announcement (`capabilities` route), read again when its version changes: after switching to the fork proxy (version of the form `2.3.0-tb.N`), the commands become available without reinstalling the plugin. An update of the fork **without a change of version number** is only taken into account when the version number changes.

**Parameters.** In the scenario, the **Add charge schedule** action takes two fields:

- **Schedule days** (title): one or more days separated by commas, semicolons or spaces, case-insensitive: `lun`, `mar`, `mer`, `jeu`, `ven`, `sam`, `dim` (or the full name, or the English abbreviation `mon`… `sun`), `tous` (every day) or `semaine` (Monday to Friday). Example: `lun,mar,mer,jeu,ven`.
- **Start time (HH:MM)** (message): from `00:00` to `23:59`, for example `23:00` (`23h00` is also accepted). This is the **vehicle’s local time**.

Any invalid parameter is refused **before** sending, with a message that explains the expected format; nothing is sent to the vehicle.

**Jeedom coordinates.** The vehicle triggers a schedule only if it is at the indicated location. The plugin uses the **Jeedom coordinates** (Settings, System, Configuration, **General** tab, **Coordinates** section: latitude and longitude): fill them in, otherwise the command is refused with the message **“Jeedom coordinates missing or invalid”**. If the vehicle is not parked at that location, the schedule exists but does not trigger. The coordinates are never written to the logs.

**A single schedule, replaced at each addition.** The plugin manages **one** schedule per vehicle and remembers its identifier: a new addition **replaces** the previous schedule (same days and time replaced, with no duplicate in principle: replacement by identifier is to be confirmed in real-world use). The schedule covers charging from the start time; there is no end time, no current and no limit specific to the schedule. Schedules created in the Tesla app are neither modified nor deleted. If you change the equipment’s VIN, the remembered identifier is no longer used: the next addition creates a new schedule.

**Deletion.** **Delete charge schedule** removes the schedule created by Jeedom. If Jeedom has created none (or if it is already deleted), the action does nothing and produces **no error**. If the vehicle refuses the deletion for a reason other than an insufficient key role (for example because the schedule was deleted in the app), the refusal message is displayed and the identifier is forgotten: a second deletion is silent and a new addition creates a new schedule.

**After the command.** A re-read is scheduled as after any command (see [Re-read after a command](#re-read-after-a-command)): the schedule information (**Scheduled charge time**…) is updated **if the vehicle returns it** when the data is read; also check the schedule in the Tesla app.

**Key role.** The minimum role needed is not confirmed (**Charging Manager** probable). An authorization refusal is displayed with the indication “insufficient proxy key role?” (see [Key role](#key-role)).

### Off-peak hours charging

The plugin can **start and stop charging itself** during the off-peak hours of your electricity contract, up to a chosen **target SoC**. This works with the official 2.3.0 proxy and **does not depend on the schedules stored in the vehicle** (see [Scheduling charging](#scheduling-charging) for those). The settings are in the **Off-peak hours charging** section of the equipment; tick **Enable** (**Charging control**), fill in **Range start**, **Range end** and **Target SoC (%)**, then save.

**Step by step: configuring off-peak hours charging.**

1. Open **Plugins > Connected objects > Tesla BLE**, then the vehicle’s equipment (**Equipment** tab), **Off-peak hours charging** section.
2. Tick **Enable** (**Charging control**).
3. Fill in **Range start** and **Range end** according to your electricity contract, in Jeedom time, for example `22:00` and `06:00` (a range spanning midnight is accepted; the end must differ from the start).
4. Fill in **Target SoC (%)**: the battery level, from 1 to 100, at which Jeedom stops charging. Choose a target **lower than or equal to the vehicle’s charge limit**.
5. Tick **Stop at end of range** if charging must not continue beyond the off-peak hours (unticked: it continues up to the vehicle’s limit).
6. For a precise stop at the target SoC, also set **Interval while charging** to 1 or 2 minutes (see below, **Accuracy**).
7. **Save**. An invalid setting is refused with a message **“Off-peak hours charging: …”** (see [Troubleshooting](#troubleshooting)): nothing is saved.
8. Check: set the plugin log to **Info** (**Plugin configuration > Logs**). At the first read of the vehicle within the range, a line **“charge aux heures creuses : décision …”** *(off-peak hours charging: decision …)* shows what the plugin decided and why (`charge_start`, `charge_stop`, `aucune`…). If nothing starts, see [Advanced charging: symptoms without a message](#advanced-charging-symptoms-without-a-message).

**Key points.** Two behaviors often come as a surprise:

- **Vehicle charge limit.** If the **target SoC** is **above** the vehicle’s charge limit, charging stops at the vehicle’s limit, with no error or warning: the target SoC is never reached. Conversely, a target SoC lower than the limit stops charging earlier.
- **Manual action.** A **Start charging** or **Stop charging** launched from Jeedom (widget, scenario) during the range **suspends the control until the next range**: Jeedom never contradicts your action. A charge restarted from the Tesla app after the stop at the target SoC also suspends the control.

**What the plugin does.** At each read of the vehicle by the refresh cycle:

- **within the range**, vehicle **plugged in** and **below the target SoC**: **Start charging**;
- **within the range**, charging in progress whose level reaches the target SoC: **Stop charging**, **even if the vehicle’s charge limit is higher** (the target SoC is compared with the **Battery level (raw)**, which can differ by a few points from **Battery level**);
- **at the end of the range**, if **Stop at end of range** is ticked: charging still in progress is stopped at the first read of the vehicle, **within the hour that follows** the end (after that, charging is no longer interrupted);
- **no useless command**: no start if charging is already in progress or if the target is reached, no stop if it is already stopped. **At most one command per read.**

**Jeedom time.** The range is read in Jeedom time (its time zone), not the vehicle’s. A range spanning midnight (`22:00` to `06:00`) works; the start is included, the end is excluded.

**Accuracy.** The decision follows the vehicle’s **read rate**: the stop at the target SoC can overshoot by a few percent if reads are spaced out. For a precise stop, enable the **Interval while charging** (1 or 2 minutes, see [Accelerated reading while charging](#accelerated-read-during-charging)). A refresh interval of **15 minutes at most** is recommended: with a long interval, the published state can be stale.

**Vehicle sleep.** The plugin **never wakes the vehicle up on its own** to decide: it relies on the information already published. On the other hand, **Start charging wakes the vehicle up** (the proxy does it by itself) like any command, and a vehicle seen **asleep** **never** receives a stop command (a charge published by a sleeping vehicle is a stale state). When the displayed state comes from a sleeping vehicle, the **Last error** message says so (“état lu à HH:MM, véhicule endormi” *(state read at HH:MM, vehicle asleep)*).

**No action in these cases.** The function is disabled; the vehicle is **unplugged**, **out of range** or could not be read; the charger supplies no current; the charging state is unknown; charging is **complete** (vehicle limit reached); the **target SoC exceeds the vehicle’s limit** (charging then stops at that limit, with no error or warning: choose a target lower than or equal to the limit). The reason is visible in **Last error**: **“Vehicle not plugged in: off-peak hours charging pending”**, **“The charger supplies no current: off-peak hours charging pending”** or **“Charging state unknown: run Refresh (with wake-up)”**. These messages never replace a real error from the last read cycle, and the next successful cycle puts back **None**.

**Manual commands and scenarios (priority).** **Start charging** and **Stop charging** remain usable at any time. A **Start** or a **Stop** launched **from Jeedom** (widget, scenario) **during the range**, or within the hour after its end, **suspends the control until the next range**: Jeedom never contradicts your action, and does not stop charging at the end of the range either. The next day, the control resumes. The message is only a line in the log (no error). Two cases are handled separately:

- **charging restarted from the Tesla app after the stop at the target SoC**: detected by a read at least **2 minutes** after the stop, it also suspends the control (**“Off-peak hours charging suspended until the next range: charging restarted outside the control”**) and is no longer interrupted;
- **charging stopped from the app after a start by Jeedom**: Jeedom **does not restart** charging (a single start per plug-in); if the start is not followed by charging, the message **“Charging started by Jeedom but stopped or not started: no new attempt before the next range”** is displayed (see [Troubleshooting](#troubleshooting)).

**Command failures.** A command that fails (vehicle refusal, timeout, insufficient key role) displays its message in **Last error** and a warning appears in the log; the new attempt takes place at the next read, **with no burst**. After **3 failures in a row**, the control is **suspended until the next range** (**“Off-peak hours charging suspended until the next range: repeated command failures”**); an **unplugging** followed by a re-plugging restarts it. A proxy that is **unreachable** or **busy** is not a failure: nothing is sent, the plugin tries again at the next read (a warning at most once per hour signals a postponed command).

**Invalid settings.** A time that is not in `HH:MM` format, a target SoC outside **1 to 100**, an empty range (end equal to start) or a function enabled without start, end or target SoC is **refused when the equipment is saved**, with a message **“Off-peak hours charging: …”**; nothing is saved.

**Other functions.** Surplus control is **ignored during the range** (see [Surplus control](#surplus-control)). A charge schedule of the vehicle ([Scheduling charging](#scheduling-charging)) or of the Tesla app can **conflict** with the range: keep only one, since Jeedom’s range is not coordinated with them. **A single range** per vehicle.

### Setting the temperature setpoint

The **Driver setpoint** (`set_driver_temp`) and **Passenger setpoint** (`set_passenger_temp`) actions set, in °C, the requested temperature on the driver side and on the passenger side. They are sliders, linked to the **Driver temperature** and **Passenger temperature** information.

**Fork proxy required, hidden commands.** The official 2.3.0 proxy cannot set the temperature setpoint: the corresponding command was added by the fork (version `2.3.0-tb.1` at minimum). As long as the proxy does not announce this command, the two actions are **refused immediately**, with no exchange at all with the vehicle, with the message **“Not supported by your proxy version”**; the rest of the equipment works normally. They are created **hidden**: after switching to the fork proxy, tick **Display** on each of them in the equipment’s **Commands** tab, or call them from a scenario. Availability follows the proxy’s announcement (`capabilities` route), read again when its version changes: after switching to the fork, the commands become usable without reinstalling the plugin.

**Range and step.** The slider goes from **15 to 28 °C** in steps of **0.5 °C**. Once the vehicle data has been read, its bounds follow the vehicle’s adjustable minimum and maximum temperature, **rounded inwards** to the whole degree (15.5 becomes 16; 27.5 becomes 27) and limited to 15 to 28 °C, the range accepted by the proxy. A **Min** or a **Max** that you set by hand on the command is never overwritten. A value out of range, or that is not a number, is refused **before** sending with the message **“Invalid value: the setpoint must be a number between … and … °C”**; nothing is sent to the vehicle. A value between two half-degrees is **rounded to the nearest half-degree** (21.3 becomes 21.5), because the vehicle adjusts by half-degree.

**The other side restarts with its last read value.** The vehicle always receives both temperatures in the same command. Setting the driver side therefore also resends the passenger setpoint, with the last value published by the **Passenger temperature** information, and vice versa. If this value is unknown (never read, null or outside 15 to 28 °C), the vehicle receives the **same value on both sides**. If you set the other side on the vehicle’s screen since Jeedom’s last read, **that setpoint can be overwritten**: run **Refresh (with wake-up)** before setting one side so as to start from the up-to-date value.

**After the command.** The linked information is updated right away, then the state is read again and a re-read is scheduled as after any command (see [Re-read after a command](#re-read-after-a-command)): the setpoint actually applied appears at the re-read. The vehicle is woken up by the proxy if needed.

**Key role.** The **Owner** role is assumed to be necessary (to be confirmed in real-world use). With a Charging Manager key, the vehicle’s refusal is displayed with the insufficient role message (see [Key role](#key-role)).

### Heating the seats and the steering wheel

Six actions set the heating: **Set front left seat heater** (`set_seat_heater_left`), **front right** (`set_seat_heater_right`), **rear left** (`set_seat_heater_rear_left`), **rear right** (`set_seat_heater_rear_right`), **rear center** (`set_seat_heater_rear_center`) and **Set steering wheel heater** (`set_steering_wheel_heater`). They are choice lists.

**Fork proxy required (version `2.3.0-tb.2` at minimum), hidden commands.** The official 2.3.0 proxy cannot set the seat or steering wheel heating: these commands were added by the fork. As long as the proxy does not announce the command, the six actions are **refused immediately**, with no exchange at all with the vehicle, with the message **“Not supported by your proxy version”**; the rest of the equipment works normally. They are created **hidden**, including after switching to the fork: **it is up to you to display them** (tick **Display** on each of them in the equipment’s **Commands** tab) or to call them from a scenario. Availability follows the proxy’s announcement (`capabilities` route), read again when its version changes: after switching to the fork, the commands become usable without reinstalling the plugin.

**Levels.** For a seat: **Off** (0), **Low** (1), **Medium** (2), **High** (3). A value sent by a scenario outside 0 to 3, or that is not an integer, is refused **before** sending with the message **“Invalid value: the heat level must be a whole number between 0 and 3”**. For the steering wheel: **Off** (0) or **On** (1) only, there is no level; the plugin does not write the **Steering wheel heat level** information after the command, only the re-read updates it. A value other than 0 or 1 is refused with the message **“Invalid value: the steering wheel heater must be 0 (off) or 1 (on)”**.

**Which seat?** Seats are designated by their **position**: “front left” and “front right” do not depend on the side of the steering wheel. The existing information keeps its name: on a left-hand-drive vehicle, **Driver seat heater** corresponds to the **front left** and **Passenger seat heater** to the **front right** (the reverse on a right-hand-drive vehicle). Seat backs and the third row are not offered. A seat that the vehicle does not have can be refused by the vehicle, or accepted with no effect and read back at 0 (to be checked in real-world use).

**Climate control.** According to Tesla’s documentation, seat heating requires the climate control to be running (preconditioning or climate keeping); without it, the command can be refused or ignored by the vehicle. Likewise, on a vehicle with automatic steering wheel heating, the steering wheel command can remain without effect. These behaviors are to be validated in real-world use.

**After the command.** The linked information (for example **Passenger seat heater**) is updated right away with the requested level, then the state is read again and a re-read is scheduled as after any command (see [Re-read after a command](#re-read-after-a-command)): the level actually applied appears at the re-read. With **Also read the climate** set to **No, charge only**, this information is not read again: it keeps the announced value. The vehicle is woken up by the proxy if needed.

**Key role.** The **Owner** role is assumed to be necessary (to be confirmed in real-world use). With a Charging Manager key, the vehicle’s refusal is displayed with the insufficient role message (see [Key role](#key-role)).

### Max defrost

A **Max defrost** action (`set_preconditioning_max`) enables or stops the vehicle’s max defrost (demisting and defrosting of the windows and mirrors). It is a choice list: **Off** (0) or **On** (1). It is linked to the **Defrost mode** information (`defrost_mode`, values `Off`, `Normal` or `Max`), and the front and rear defrost information (`is_front_defroster_on`, `is_rear_defroster_on`) is read again with it.

**Fork proxy required (version `2.3.0-tb.1` at minimum), hidden command.** The official 2.3.0 proxy cannot control max defrost: the command was added by the fork. As long as the proxy does not announce the command, the action is **refused immediately**, with no exchange at all with the vehicle, with the message **“Not supported by your proxy version”**; the rest of the equipment works normally. It is created **hidden**, including after switching to the fork: **it is up to you to display it** (tick **Display** in the equipment’s **Commands** tab) or to call it from a scenario. Availability follows the proxy’s announcement (`capabilities` route), read again when its version changes: after the proxy update, the command becomes usable without reinstalling the plugin.

> ⚠️ **Consumption and wake-up.** Enabling max defrost **wakes the vehicle up** (via the proxy) and **uses battery** as long as it runs. The plugin **never** starts it on its own: only an action from you (widget or scenario) sends it. Remember to stop it, for example with a second scenario after the desired duration.

**Values.** A value sent by a scenario other than 0 or 1 is refused **before** sending with the message **“Invalid value: max defrost must be 0 (off) or 1 (on)”**.

**After the command.** **Defrost mode** immediately changes to `Max` (on) or `Off` (off), then the state is read again and a re-read is scheduled as after any command (see [Re-read after a command](#re-read-after-a-command)): the actual value appears at the re-read (when stopping, the vehicle may report `Normal` if the climate control is still running). The front and rear defrost are only updated at this re-read. With **Also read the climate** set to **No, charge only**, or if the vehicle falls asleep again, this information is not read again: it keeps the announced value.

**Key role.** The **Owner** role is assumed to be necessary (to be confirmed in real-world use). With a Charging Manager key, the vehicle’s refusal is displayed with the insufficient role message and the **Insufficient role** badge (see [Key role](#key-role)).

### Dog mode, camp mode and climate keeping

A **Climate keeper mode** action (`set_climate_keeper_mode`) chooses the climate keeping of the parked vehicle: **Off** (0), **Keep** (1), **Dog mode** (2) or **Camp mode** (3). It is linked to the **Climate keeper (dog, camp)** information (`climate_keeper_mode`, values `Off`, `On`, `Dog`, `Party` or `Unknown`): camp mode appears there under the name `Party` according to the vehicle (to be confirmed in real-world use).

**Fork proxy required (version `2.3.0-tb.1` at minimum), hidden command.** The official 2.3.0 proxy cannot control climate keeping: the command was added by the fork. As long as the proxy does not announce the command, the action is **refused immediately**, with no exchange at all with the vehicle, with the message **“Not supported by your proxy version”**; the rest of the equipment works normally. It is created **hidden**, including after switching to the fork: **it is up to you to display it** (tick **Display** in the equipment’s **Commands** tab) or to call it from a scenario. Availability follows the proxy’s announcement (`capabilities` route), read again when its version changes: after the proxy update, the command becomes usable without reinstalling the plugin.

> ⚠️ **Battery and wake-up.** Choosing a keeping mode **wakes the vehicle up** (via the proxy) and **uses battery over a long period**; the vehicle may refuse (low battery, vehicle state). The plugin **never** starts it on its own and never stops it: only an action from you (widget or scenario) sends it.

> ⚠️ **Pet.** This mode **does not replace monitoring the temperature** of the cabin for a pet. Reading follows the vehicle’s refresh interval: an alert must rely on the **Interior temperature** and on a suitable interval.

**Values.** A value sent by a scenario outside 0 to 3 is refused **before** sending with the message **“Invalid value: the climate keeper mode must be 0 (off), 1 (keep), 2 (dog) or 3 (camp)”**.

**After the command.** **Climate keeper (dog, camp)** immediately changes to `Off`, `On`, `Dog` or `Party`, then the state is read again and a re-read is scheduled as after any command (see [Re-read after a command](#re-read-after-a-command)): the actual value appears at the re-read. With **Also read the climate** set to **No, charge only** (leave it on **Yes** for this mode), or if the vehicle falls asleep again, the information is not read again: it keeps the announced value, and the sleep window may open (see [Letting the vehicle fall asleep](#let-the-vehicle-fall-asleep)).

**Key role.** The **Owner** role is assumed to be necessary (to be confirmed in real-world use). With a Charging Manager key, the vehicle’s refusal is displayed with the insufficient role message and the **Insufficient role** badge (see [Key role](#key-role)).

### Preconditioning scheduled by Jeedom

The plugin can **start the climate control before the departure time** and then stop it, with the temperature already set in the vehicle. This works with the official 2.3.0 proxy (**Start climate control** and **Stop climate control** commands), without the fork. The settings are in the **Preconditioning scheduled by Jeedom** section of the equipment; do not confuse it with the **Scheduled preconditioning** information (`scheduled_preconditioning_time`), which **reads** the schedule set in the vehicle.

**Step by step: configuring scheduled preconditioning.**

1. Open **Plugins > Connected objects > Tesla BLE**, then the vehicle’s equipment (**Equipment** tab), **Preconditioning scheduled by Jeedom** section.
2. Fill in the **Departure time**, in Jeedom time, for example `07:30`.
3. Tick the departure **Days** concerned.
4. Set the **Lead time (min)** (empty: 15 minutes) and the **Maximum duration (min)** (empty: 30 minutes, or the lead time plus 15 minutes if the lead time exceeds 15). With 15 and 30, the climate control starts at `07:15` and stops at `07:45`.
5. Tick **Only if plugged in** if the climate control must not draw on the battery of an unplugged vehicle.
6. Tick **Enable** (**Climate control**), then **save**. An invalid setting is refused with a message **“Scheduled preconditioning: …”** (see [Troubleshooting](#troubleshooting)): nothing is saved.
7. Check: set the plugin log to **Info**. At the first read of the vehicle within the window, a line **“préconditionnement planifié : décision …”** *(scheduled preconditioning: decision …)* shows what the plugin decided and why.

**Usage example: weekday departure at 7:30.** Set **Departure time** to `07:30`, tick **Monday** to **Friday**, leave **Lead time** at 15 and **Maximum duration** at 30, tick **Only if plugged in** and **Enable**. The vehicle stays plugged in overnight:

- If you also use [Off-peak hours charging](#off-peak-hours-charging) (for example `22:00` to `06:00`), charging ends before the preconditioning window, which runs from `07:15` to `07:45`: the two functions do not get in each other’s way.
- From Monday to Friday, at the first read of the vehicle after `07:15`, the climate control is started if it is stopped and if the vehicle is plugged in. The plugin log (**Info** level) shows **“préconditionnement planifié : décision `auto_conditioning_start` (demarrage)”** *(scheduled preconditioning: decision `auto_conditioning_start` (start))*, and the **Climate on** information changes to 1 at the next read.
- At the first read after `07:45`, if the climate control is still running after this start by Jeedom, it is stopped (decision `auto_conditioning_stop`).
- On Saturday and Sunday, nothing happens. If you leave before `07:45`, stop the climate control yourself from Jeedom: Jeedom does not restart it afterwards.

**The window.** It starts at the departure time **minus the lead time** and lasts the **maximum duration** from that start (start included, end excluded). The day taken into account is that of the **departure time**: a departure at `00:10` with 20 minutes of lead time starts the day before at `23:50`, and it is the next day that must be ticked. Everything is in **Jeedom time** (its time zone), not the vehicle’s; a departure that falls in the hour skipped by the switch to daylight saving time is shifted by one hour.

**What the plugin does.** At each successful read of the vehicle by the refresh cycle, **within the window**: if the climate control is stopped (and, with the option, the vehicle plugged in), **Start climate control** (**a single successful start per departure**); **at the first read after the end of the window** (within the hour), if the climate control is still running after a Jeedom start, **Stop climate control**. At most **one command per read**, no useless command.

**Accuracy.** The decision follows the vehicle’s **read rate**: the start can come a few minutes after the planned time, and the stop can overshoot the end by one interval. A refresh interval of **5 minutes at most** is advised. With an interval longer than the window duration, no read falls inside it: neither start nor stop. A start is still possible **after the departure time**, as long as the window is not over.

**Vehicle sleep.** The plugin **never wakes the vehicle up on its own** to decide and never sends a wake-up command, but **Start climate control wakes the vehicle up** (the proxy does it by itself) and uses battery. A vehicle seen **asleep** **never** receives a stop command: its climate control is considered stopped.

**Priority to your actions.** Jeedom never contradicts your action:

- a **Start climate control** or **Stop climate control** launched **from Jeedom** (widget, scenario) during the window **suspends preconditioning until the next departure**, and the climate control is not stopped at the end of the window;
- a climate control **already running** when the window is entered (or started from the Tesla app, or by the vehicle’s schedule) is neither restarted nor stopped;
- a climate control **stopped from the app** after the Jeedom start (detected by a read at least **2 minutes** after the command) is not restarted in a loop;
- a **dog mode, camp mode, climate keeping** or a **max defrost** in progress is never stopped or replaced.

Disabling the function or changing its settings **during the window does not stop** a climate control that has already started.

**Key role.** The **Owner** role is assumed to be necessary (to be confirmed in real-world use). With a Charging Manager key, the vehicle refuses the command: the insufficient role message is displayed in **Last error**, the **Key role** information changes to **Charging Manager**, and **a single attempt is made per departure** (see [Key role](#key-role)).

**Command failures.** A command that fails (vehicle refusal, timeout) displays its message in **Last error** and a warning appears in the log; the new attempt takes place at the next read, **with no burst**. After **3 failures in a row**, the control is **suspended until the next departure**. A proxy that is **unreachable** or **busy** is not a failure: nothing is sent, the plugin tries again at the next read.

**No action in these cases.** The function is disabled or the day is not ticked; the vehicle could not be read or is **out of range**; with the option, the vehicle is **unplugged** or its charging state is unknown; the climate control state is unknown; the climate control is already running. The reason is visible in **Last error** for the useful cases (**“Vehicle not plugged in: scheduled preconditioning not started”**, **“Charging state unknown: run Refresh (with wake-up)”**), without ever replacing a real error from the last read cycle.

**Other functions.** Scheduled preconditioning is **independent** of the schedule set in the vehicle ([Scheduled preconditioning](#information-commands) read by the plugin): if the vehicle is already preconditioning, the climate control is seen as active and Jeedom does not intervene. It can chain, in the same pass, with [Off-peak hours charging](#off-peak-hours-charging): the two commands go out one after the other. The plugin does not take occupant presence into account: a climate control started by Jeedom and still running at the first read after the end of the window is stopped.

### Confirmation of sensitive actions

Five actions require a **confirmation** before being sent, on the dashboard and on mobile: **Unlock doors** (`door_unlock`), **Open charge port** (`charge_port_door_open`), **Sentry Mode** (`set_sentry_mode`), **Open rear trunk** (`open_trunk_rear`) and **Open frunk** (`open_trunk_front`). The other actions (lock, honk, lights, charging, climate…) are sent on the first click.

- **One click opens a confirmation window.** Nothing is sent until you have confirmed.
- **“Confirm action” checkbox.** It is in the command's advanced parameters (**Commands** tab of the equipment, the command's cogwheel). It is **checked at creation**; uncheck it to remove the confirmation from a command, check it on another one to add one. Your choice is never overwritten by the plugin (updates included: on an existing equipment, the update sets the confirmation only once, except where you had already set it).
- **A scenario is not concerned.** An action called from a scenario runs **without confirmation**. A call through Jeedom's JSON-RPC API must pass `confirmAction=1`, otherwise Jeedom refuses it.

> **IMPORTANT: this is not a security protection.** The confirmation is a user-interface safeguard against accidental clicks, nothing more. By default the proxy has **no authentication**: any machine on your network that can reach it can unlock or open the vehicle **without going through Jeedom**, and therefore without confirmation. Keep the proxy on a trusted network, never exposed to the Internet (see [Key role](#key-role)).

For **Sentry Mode**, the state displayed after the order is described in [Sentry Mode state](#sentry-mode-state) (source **Actual** or **Last order**).

### Opening the rear trunk and the frunk

Two actions open a trunk remotely: **Open rear trunk** (`open_trunk_rear`) and **Open frunk** (`open_trunk_front`, the front trunk). They send the same proxy command, `actuate_trunk`, with the targeted trunk. The state is read in the **Rear trunk** (`trunk_rear`) and **Front trunk (frunk)** (`trunk_front`) information.

**Fork proxy required (version `2.3.0-tb.2` at minimum), commands hidden.** The official 2.3.0 proxy does not have this command: it was added by the fork. As long as the proxy does not announce the command, both actions are **refused immediately**, without any exchange with the vehicle, with the message **“Not supported by your proxy version”**. They are created **hidden**, including after switching to the fork: **it is up to you to display them** (check **Display** in the **Commands** tab of the equipment) or to call them from a scenario. Availability follows the proxy's announcement (`capabilities` route), re-read when its version changes: after the proxy update, the actions become usable without reinstalling the plugin or recreating the equipment. For these two actions, the plugin displays neither the **Function unavailable** badge nor the **Insufficient role** badge: the refusal is displayed on click.

**Confirmation.** A click asks for a **confirmation** before sending, as for the other sensitive actions: see [Confirmation of sensitive actions](#confirmation-of-sensitive-actions) (**Confirm action** checkbox, scenario without confirmation, JSON-RPC `confirmAction=1`).

**Check before opening the rear trunk.** For the rear trunk, the vehicle handles the command as a **toggle**: on a motorized liftgate that is already open, it would **close** it. The plugin therefore first re-reads the vehicle state (without waking it) and sends the command only if the rear trunk is read as **closed**. Three possible refusals, nothing is sent, and **Last error** is not modified:

- **“Coffre déjà ouvert ou en mouvement : commande non envoyée”** (*Trunk already open or moving: command not sent*): the rear trunk is open, ajar, opening or closing;
- **“État du coffre inconnu : commande non envoyée”** (*Trunk state unknown: command not sent*): the vehicle gives no usable state for this trunk;
- **“État du coffre illisible, commande non envoyée : …”** (*Trunk state unreadable, command not sent: …*): the re-read failed (proxy unreachable, vehicle out of range…), the cause follows the message.

The re-read state is published in the information before the refusal: if the trunk was already open, **Rear trunk** changes to 1. The **frunk** is not re-read: it does not close remotely, the command can only open it. **The plugin never closes a trunk.**

> ⚠️ **Wake-up.** These commands **wake up the vehicle** (via the proxy), and the plugin never launches them on its own: only an action from you (widget or scenario) sends them.

**After the command.** No value is assumed: the state is re-read, then a re-read is scheduled as after any command (see [Re-read after a command](#re-read-after-a-command)). **Rear trunk** or **Front trunk (frunk)** changes to 1 when the vehicle reports the trunk as open, sometimes at the next re-read.

**Key role.** The **Owner** role is assumed to be required (to be confirmed in real use). With a Charging Manager key, the vehicle's refusal is displayed with the insufficient role message (see [Key role](#key-role)).

### Sentry Mode state

Two pieces of information tell whether Sentry Mode is on: **Sentry** (`sentry_mode`) is **Active**, **Inactive** or **Unknown**, and **Sentry source** (`sentry_mode_source`) tells where this value comes from. The command that turns it on or off is **Sentry Mode** (`set_sentry_mode`).

| Source | What it means |
|---|---|
| **Actual** | The value was **read from the vehicle**. Available with the **fork proxy in version `2.3.0-tb.2` at minimum** and an **awake** vehicle: a sleeping vehicle is not read, so the information keeps the **last value read** (see [Vehicle sleep and data freshness](#vehicle-sleep-and-data-freshness)). A change made from the Tesla app or the vehicle screen is seen at the next read. |
| **Last order** | The plugin cannot read Sentry Mode (official 2.3.0 proxy, or older fork): the value is that of the **last successful order sent by Jeedom**. A change made from the app, the vehicle screen or an **automatic shutoff** is **not seen**. |
| **None** | Nothing has been read or ordered yet: **Sentry** is **Unknown** (never a false “Inactive”). |

**After an order.** A **successful** order immediately publishes the ordered value with the source **Last order**, even if the proxy can read Sentry Mode; at the next read, the source goes back to **Actual**. During the **re-read after a command** period (30 seconds by default, see [Re-read after a command](#re-read-after-a-command)), an actual read that contradicts the order is ignored: the proxy is still serving the old state. A **refused** order or one in error changes nothing.

**Vehicle states.** Only `Off` gives **Inactive**. The other states (`Idle`, `Armed`, `Aware`, `Panic`, `Quiet`) give **Active**: `Idle`, Sentry Mode at rest, is counted as **Active** (to be confirmed in real use). An unknown or missing value leaves the information unchanged.

**Jeedom restart.** The last known value and its source are **kept** and restored at startup, including after a power outage.

> **In a scenario.** The labels **Active**, **Inactive**, **Unknown**, **Actual**, **Last order** and **None** **follow Jeedom's language**: compare them in the current language of your Jeedom. To know whether the value is reliable, test **Sentry source** (for example **Actual**) in addition to **Sentry**.

### Prolonged opening alerts

The plugin can **warn you** when an opening (door, rear trunk, frunk, tonneau, charge port) stays open, or when the vehicle stays **unlocked with no occupant**, longer than the delay you choose. Alerts are **disabled by default** and are set **per vehicle**, in the **Prolonged opening alerts** block of the equipment page:

| Setting | Role |
|---|---|
| **Opening left open**: **Enable** | Enables the openings alert. |
| **Delay before alert (min)** | From 1 to 1440 minutes. **Required** to enable the alert; an invalid delay is refused on save. |
| **Vehicle unlocked with no occupant**: **Enable** | Enables the lock alert, with **its own delay** (**Delay before alert (min)**). |

The two alerts are independent. An alert consists of:

- **a message** in Jeedom's message center, naming the vehicle and the opening (for example “My Tesla: opening “Front trunk (frunk)” open for more than 10 min”), **only once per episode**; **several openings open at the same time give several messages**, one per opening;
- **the info set to 1**: **Openings alert** (`closures_alert`) as long as at least one opening has stayed open beyond the delay, **Unlocked unoccupied alert** (`unlocked_alert`) for the lock. Use them as a scenario trigger to be notified by the means of your choice; they are **hidden** and **historized**: display them if you wish.

When everything is closed again (or locked again, or an occupant is present), the info goes back to **0** and a new prolonged opening will alert again. **The message stays in the message center** after closing: Jeedom does not remove it, delete it yourself.

**Accuracy.** Alerts are evaluated **at each successful read of the vehicle state**, hence at the refresh rate (5 minutes by default, see [Information refresh](#refreshing-the-information)). The delay is counted from the **first read that sees the anomaly**: the alert is sent **between the chosen delay and that delay plus two refresh intervals** after the actual opening; “open for more than 10 min” is therefore always true.

**Never an alert on a stale value.** When the proxy is unreachable, the vehicle is out of range or the read fails, **nothing is evaluated** and the delay does not accumulate. If the interruption exceeds **two refresh intervals plus two minutes**, the timer **restarts from zero** when reads resume; an alert already sent stays sent, with no new message.

**Charge port.** An open charge port counts as an anomaly **only if the vehicle was seen unplugged** (last **Charge state** read: `Disconnected`). Plugged in, charging, or unknown state: no alert for the charge port.

**Unknown presence.** “Unlocked with no occupant” is evaluated only if the vehicle is **unlocked** and **Occupant present** is **0**: an unknown presence triggers nothing (see [Information](#information-commands)).

### Position and privacy

The vehicle's position is **personal data**: it says where you are and when you are not there. The plugin protects it by default, but a few precautions remain your responsibility.

**What is read, and when.** The position is provided only by the **fork proxy** (`2.3.0-tb.2` at minimum): the official 2.3.0 proxy does not serve it, and the information then does not exist (see [Extended data: what is available](#extended-data-what-is-available)). It is read at most **every 15 minutes**, only when the vehicle is **awake and within Bluetooth range** of the proxy, never by waking it. As the proxy is in your garage, the position read is in practice that of your home. A position that is missing, at 0/0, out of range or **older than one hour** is ignored: the information keeps its last value.

**Not visible and not historized by default.** **Latitude** and **Longitude** are created **hidden** and **not historized**: they appear neither on the widget nor in a graph, and nothing is kept. To use them:

1. Open the **Commands** tab of the equipment.
2. On **Latitude** and **Longitude**, check **Display** to see them on the widget, and **Historize** to keep their values.
3. **Save**. This choice is never overwritten afterwards.

Note: a historized position is stored in Jeedom's database and in its backups, like any history. Only historize if you need it.

**The home and the radius.** The **At home** information is **1** when the vehicle is within **Radius (m)** of the home, **0** beyond. The home is set in the **Equipment** tab, **Home position** section (see [Equipment configuration](#equipment-configuration)):

| Setting | Value |
|---|---|
| **Latitude** and **Longitude** | The coordinates of your home. **Both empty: Jeedom's position** (**Settings > System > Configuration**, **General** tab). Only one filled in is refused. |
| **Radius (m)** | Integer from **10 to 10000**. Empty: **100 m**. An inaccurate GPS or an underground garage may require a larger radius. |

When the equipment is saved, **At home** is recalculated immediately from the last position read (if **Latitude** and **Longitude** exist on the equipment), without waiting for the next read.

**Limits of At home.** It is a binary information that cannot say “unknown”:

- It is **never written** as long as the **home** (no coordinates entered, no position in Jeedom) or the **position** (never read, ignored) are unknown. **Before any calculation, the tile displays 0**: it therefore does not prove that the vehicle has left.
- It **does not go back to 0** when the vehicle leaves: out of Bluetooth range, no position is read anymore and the information keeps its **last value** (1). It also keeps its value if you clear the home or if the position becomes too old.
- **In a scenario**, test `== 1` (never `== 0` or “different from 1”), and **combine with Vehicle presence**: “At home is 1 **and** Vehicle presence is 1” means the vehicle is at your place and reachable. **Vehicle presence at 0** signals that it is no longer within range of the proxy, that is, in practice gone.

**Jeedom's `event` log.** The plugin **never** writes a coordinate (vehicle or home) or a distance in its own log, at any level, even in **Debug**. But Jeedom itself records each new value of an information in its **`event`** log (**Analysis > Logs**): **Latitude** and **Longitude** appear there, **even hidden and not historized**. To protect yourself from this, choose one: lower the level of the `event` log in Jeedom's log settings (**Settings > System > Configuration**, **Logs** tab), or delete the **Latitude** and **Longitude** information from the equipment (**At home** is still calculated). The plugin recreates the missing commands on each save of the equipment: delete them again if they come back. Also review a log capture before publishing it on a forum.

**The proxy must stay protected.** The official proxy has **no authentication**: any device on your local network can ask it for the vehicle's position. The fork proxy, the only one to serve the position, **can** require an **API token** (optional: **Proxy API token** setting in the plugin configuration), which also protects the position. In all cases, keep the proxy on a trusted network and **never** expose its port to the Internet (see [Key role](#key-role) and [Plugin configuration](#plugin-configuration)).

### Why calls are sequential

A proxy has only **one Bluetooth adapter** and a single queue of exchanges with the vehicles: two requests sent at the same time would interfere. The plugin therefore makes the exchanges of a given proxy go **one after the other**, all vehicles combined (cycle reads, commands, **Refresh**, **Check pairing**).

- **A single proxy**: only one exchange at a time. If a command is in progress, the cycle read steps aside and resumes at the next pass (the next minute); a command or a **Refresh** waits its turn. When the wait lasts too long (about 2 minutes), the plugin gives up and displays **Proxy busy**: try again in a moment (see [Troubleshooting](#troubleshooting)).
- **Different proxies**: they are read **in parallel** and never wait for each other. A slow or stopped proxy only delays its own vehicles; the cycle lasts as long as its slowest proxy.
- **In the worst case** (very slow proxy, each read going to its maximum delay), a 4-minute cycle reads **at most 3 vehicles per proxy**; beyond that, the last ones may not be read in that cycle. In practice, a read lasts a few seconds.

### Summary of the rate and wake-up settings

All these settings are in the **Equipment** tab of each vehicle (see [Equipment configuration](#equipment-configuration)). The defaults also apply to existing vehicles after the update.

| Setting | Default | Possible values | Effect on the vehicle's battery |
|---|---|---|---|
| **Refresh interval** | 5 minutes | 1, 2, 5, 10, 15 or 30 minutes | The longer it is, the less the vehicle is polled. On its own, it never wakes the vehicle. |
| **Interval while charging** | Disabled | Disabled, or 1, 2, 5, 10 or 15 minutes | No effect when not charging; while charging the vehicle is awake anyway. |
| **Let the vehicle fall asleep** | Checked | Checked or unchecked | Checked: the plugin stops reading data when the vehicle is idle, so that it can fall asleep. |
| **Unchanged reads before the window** | 3 | 1, 2, 3, 4, 5, 10 or 15 | The lower it is, the faster the window opens. |
| **Window duration** | 30 minutes | 15, 20, 30, 45 minutes, 1 h, 1 h 30 or 2 h | The longer it is, the more time the vehicle has to fall asleep, but the longer the data stay frozen. |
| **Re-read delay after command** | 30 seconds | 30 seconds, 45 seconds, 1 minute, 1 minute 30 or 2 minutes | One read per successful command, without wake-up. |
| **Also read the climate** | Yes | Yes, or No (charge only) | “Charge only” shortens the data request (gain to be measured on your installation). |
| **Refresh (with wake-up)** (command `refresh_wakeup`) | | Action, to be launched by hand or from a scenario | **Wakes up** the vehicle on each execution. |
| **Data age (min)** (information `data_age`) | | Minutes elapsed since the last successful data read; **99999** = no known read (or more than 69 days) | None: local calculation, the proxy is not queried. |

The **window duration** only has an effect if it exceeds the refresh interval. Details of each setting: [Information refresh](#refreshing-the-information), [Faster reading while charging](#accelerated-read-during-charging), [Let the vehicle fall asleep](#let-the-vehicle-fall-asleep) and [Re-read after a command](#re-read-after-a-command).

### Recommendations by use

The values below are **indicative starting points, to be adjusted based on your own measurements**: the actual effect on the battery depends on the model, the vehicle's software and its environment, and the plugin does not guarantee that the vehicle will fall asleep. No battery percentage is stated here for lack of a reliable measurement; the table quantifies what the plugin actually does: the number of data reads per hour and the time left for the vehicle to fall asleep.

| Use | Refresh interval | Interval while charging | Sleep window | Also read the climate | Data reads (vehicle awake, idle, not charging) |
|---|---|---|---|---|---|
| **Simple monitoring** (presence, lock, battery level) | 10 to 15 minutes | Disabled | Checked, 3 unchanged reads, 30 minutes (defaults) | Yes | 4 to 6 per hour at most; **none** during the 30 minutes of an open window |
| **Solar control** (adjusting the current according to production) | 5 minutes | **1 minute** | Checked, 3 unchanged reads, 30 minutes (defaults) | No (charge only), if you do not use the climate | 12 per hour when not charging; **60 per hour while charging** (the window never opens while charging) |
| **Close monitoring** (charging or preconditioning watched closely) | 1 to 2 minutes | 1 minute | Checked, 3 unchanged reads, 30 minutes | Yes | 30 to 60 per hour: the vehicle does not sleep until the window is open; reserve this profile for a specific period |
| **Several vehicles on one proxy** (3 at most) | 10 to 15 minutes | Disabled, except for the controlled vehicle | Checked | Yes | Reads from the same proxy go one after the other: keep intervals long |

For solar control, also keep the **Re-read delay after command** at 30 seconds and space out the **Set charge current** orders of your scenario (a re-read is launched after each successful command).

**Measuring the effect at your place.** Note the **Battery level** in the evening and in the morning, with the vehicle parked and unoccupied, for a few nights with **Let the vehicle fall asleep** checked, then a few nights unchecked. Historize **Vehicle awake** to see how long the vehicle stayed awake: compare the two series before adjusting the interval or the window duration.

## Widget and display

This section describes what the plugin displays on the Jeedom dashboard and on the Jeedom mobile web interface: the **vehicle tile**, the **generic types**, the **model image** and the **command order**. These features do not require a more recent version of Jeedom than the one the plugin needs (see [Prerequisites](#requirements)) and do not call any Internet site: everything is displayed from your Jeedom.

**What the plugin never overwrites**: a generic type you have chosen, an image you have uploaded or removed, the command order you have changed and your choice between the tile and the standard widget. Each subsection states the exact rule.

### Vehicle tile

Each vehicle is displayed by default as a **tile**: a summary readable at a glance, followed by your other visible commands.

The summary contains, from top to bottom:

- the **model image** (if there is one, see [Model image](#model-image));
- **Battery** (the level, in large type) and **Charge limit**;
- **Range** (in km) and **Charging status** (translated label: charging, complete, unplugged…);
- two badges: **Locked** or **Unlocked**, and **In range** or **Out of range**;
- data freshness: **Data from … ago** followed by a duration (minutes, hours or days), or **No known read**;
- the **last error**, on a red line, **only if there is one** (nothing is displayed when it is “None”);
- six buttons: **Start charging**, **Stop charging**, **Lock doors**, **Unlock doors**, **Wake up** and **Refresh**.

The **visible** commands of the equipment that the summary does not include (for example the temperature, the openings, Sentry Mode) are displayed **below** the summary, as in the standard widget and in the order of the **Commands** tab. Commands included in the summary are not repeated below.

<!-- Capture à ajouter en recette : images/tuile-dashboard-normal.png (tuile d'un véhicule éveillé, données récentes, sur le dashboard) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-normal.png (même tuile sur l'interface mobile web) -->

#### The four states of the tile

| State | What you see |
|---|---|
| **Normal** (vehicle awake, recent read) | Battery, limit, range, charging status, **In range**, lock state, **Data from … ago** a few minutes; no error line. |
| **Vehicle asleep** | The **last values read** remain displayed (the plugin never wakes the vehicle on its own) and the **Data from … ago** duration keeps growing. No error is displayed: this is normal. Use **Refresh (with wake-up)** or the **Wake up** button to get fresh values (see [Refreshing the information](#refreshing-the-information)). |
| **Out of range** | The badge shows **Out of range**. The values are the last known ones; the red **last error** line appears if the proxy or the vehicle reported a problem (see [“Last error” info (read)](#last-error-info-read)). |
| **Error or never read** | A missing, empty or non-numeric value is displayed as **Unknown** (never 0 % or an invented date); freshness shows **No known read** as long as no read has succeeded; the red line gives the last error. |

<!-- Capture à ajouter en recette : images/tuile-dashboard-endormi.png (tuile d'un véhicule endormi, valeurs anciennes) -->
<!-- Capture à ajouter en recette : images/tuile-dashboard-hors-portee.png (pastille Hors de portée) -->
<!-- Capture à ajouter en recette : images/tuile-dashboard-erreur.png (ligne d'erreur et valeurs Inconnu) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-endormi.png (tuile d'un véhicule endormi sur l'interface mobile web) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-hors-portee.png (pastille Hors de portée sur l'interface mobile web) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-erreur.png (ligne d'erreur et valeurs Inconnu sur l'interface mobile web) -->

#### Button behavior

- A button runs **the matching command** of the vehicle, like that command's button in the standard widget: same rules, same messages.
- A **greyed-out** button corresponds to a command that is **missing** from the equipment or **not supported** by your proxy (message **Not supported by your proxy version**, see [Error when sending a command](#error-when-sending-a-command)). **Refresh** is greyed out only if the command is missing.
- While the command is running, the button is **dimmed** and no longer reacts; it becomes usable again **as soon as the command is finished**, whether successful or in error, and after 4 minutes at the latest. In case of error, Jeedom displays its usual error message.
- The tile **updates by itself**, without reloading the page, when a value changes.
- The tile adds **no confirmation**: any confirmation remains Jeedom's own for the command (see [Confirmation of sensitive actions](#confirmation-of-sensitive-actions)).
- On the Jeedom **native mobile app**, the tile is not used: the app relies on the [generic types](#generic-types).

#### Going back to the standard widget

Do this if you prefer Jeedom's command widgets.

1. Open **Plugins > Connected objects > Tesla BLE** and click the vehicle.
2. Click **Advanced configuration** (at the top of the equipment page).
3. Uncheck the **Widget template** box.
4. Click **Save**, then reload the dashboard.

The vehicle is then displayed with Jeedom's **standard widget**: one thumbnail per visible command, **without the model image** (this image is drawn only by the tile).

#### Restoring the plugin widget

1. Open the vehicle's **Advanced configuration**, as above.
2. **Check** the **Widget template** box.
3. Click **Save**, then reload the dashboard.

The tile comes back; no command is modified.

#### Existing equipment after the update

On update, the tile is **enabled** on every existing equipment, **except** if it already had a display customization: **table** layout, or a command widget chosen by hand. These equipments keep the standard widget; check the **Widget template** box if you want the tile. An equipment whose **Widget template** box had already been set also keeps its choice.

#### Hiding individual commands without losing the tile

The tile reads the vehicle's commands **even if they are hidden**. To lighten the display below the summary, open the **Commands** tab and uncheck **Display** on the commands you no longer want to see: the summary and its six buttons do not change.

#### Limits of the tile

- The **Data from … ago** duration is not “aged” in the browser between two updates: it follows the value of **Data age (min)**, recalculated every minute by the plugin.
- The standard widget does **not** display the model image.
- If the tile cannot be drawn, Jeedom displays the **standard widget** instead and the plugin writes it to its log (see [Plugin log messages](#plugin-log-messages)).

### Generic types

A **generic type** is a label that Jeedom puts on a command (battery, temperature, opening, lock…) so that the **mobile app**, **voice assistants** and third-party plugins know what it represents. The plugin sets them for you.

To see or change them: on the equipment, **Commands** tab, click the **cogwheel** of the command and find the **Generic type** field. The exact type labels depend on your Jeedom version; the table also gives their identifier.

| Command | Generic type set |
|---|---|
| **Battery level** | Battery (`BATTERY`) |
| **Charger voltage** | Voltage (`VOLTAGE`) |
| **Cumulative charge energy** | Consumption (`CONSUMPTION`) |
| **Interior temperature**, **Exterior temperature** | Temperature (`TEMPERATURE`) |
| **Vehicle lock** | Lock state (`LOCK_STATE`) |
| **Driver front door**, **Passenger front door**, **Driver rear door**, **Passenger rear door**, **Rear trunk**, **Front trunk (frunk)**, **Charge port (opening)**, **Tonneau cover** | Opening (`OPENING`) |
| **Front left tire pressure**, **front right**, **rear left**, **rear right** | Pressure (`PRESSURE`) |
| **Lock doors** | Lock, close (`LOCK_CLOSE`) |
| **Unlock doors** | Lock, open (`LOCK_OPEN`) |
| **Start charging** | Socket, on (`ENERGY_ON`) |
| **Stop charging** | Socket, off (`ENERGY_OFF`) |

The pressure infos exist only if your proxy announces them (see [Extended data: what is available](#extended-data-what-is-available)).

> **WARNING: these types make actions reachable by Jeedom's grouped actions.** If you place the vehicle in a Jeedom **object**, the object's **summary actions** and the “Generic type” scenario actions can **unlock the vehicle** (lock: open) or **start and stop its charging** (socket: on and off), **without any interface confirmation**. If you do not want this, set the **Generic type** of these commands to **None**: this choice is kept.

When the plugin sets a type:

- **on creation** of a command (new equipment, command added by an update);
- **only once** on existing commands, at the update that brings the types, and **only on a command whose type is empty**.

A type you have chosen is **never overwritten**, even if it differs from the plugin's.

**Limit: a type cleared by hand** (**None**) is not set again by saving the equipment or by the refresh cycle. It can be in only two cases: the command is **deleted and then recreated** by the plugin (it starts again with the default type), or the plugin **replays** the setting of types on existing commands, which only happens after an update interrupted by an error on another equipment. In these cases, set **None** again.

### Model image

The plugin associates with each vehicle an **image of its model**, deduced from the **VIN**. It is displayed on the **tile** and in Jeedom's **equipment list**. These are neutral pictograms supplied with the plugin, with no download.

| Model (decoded from the VIN) | Image |
|---|---|
| Model S, Model 3, Model X, Model Y, Cybertruck | Model pictogram |
| Semi, Roadster, unknown model | None: the **plugin icon** stays displayed |

Rules:

- The image is set **when the equipment is saved** (and when the plugin is updated) if the model is known and the vehicle **has no personal image**.
- A **personal image** (one you have uploaded) is **never touched**.
- **Replace** the image: open the vehicle's **Advanced configuration** and upload your own. It is kept.
- **Remove** the image: in the **Advanced configuration**, use **Remove image**. **This removal is permanent**: the plugin never puts the image back by itself, even if you save the equipment or update the plugin. The plugin icon is displayed instead.
- There is **no button** to get the plugin image back after a removal: to have an image, upload your own.
- If the **VIN** changes to a model without an image, the image set by the plugin is removed; an image you chose stays.
- If Jeedom cannot write to its images folder, or if the plugin image is unreadable (reinstall the plugin), the plugin writes a warning to its log and the plugin icon stays displayed (see [Plugin log messages](#plugin-log-messages)).

### Command order

The commands of a new equipment are arranged **by theme**, in this order:

1. **Status**: presence, lock, wake state, occupant, sentry, data age, last error;
2. **Charging**: battery, range, charging status, limits, power, energy, schedules;
3. **Climate**: temperatures, climate control, heaters, defrost;
4. **Openings**: doors, trunks, charge port, alerts;
5. **Vehicle**: model, odometer, driving, position, tires, software update;
6. **Proxy monitoring**: proxy reachable, version, key role, read durations;
7. **Actions**: read (refresh, wake up), charging, climate, access (doors, trunks, Sentry Mode, lights, horn).

Rules:

- The order is set **only when each command is created**. It is **never rewritten**: a plugin update **moves no existing command**.
- A command **added later** (by an update) is placed **next to a command of its theme**; if positions are equal, Jeedom sorts them by name. If **no** command of that theme exists on the equipment, it is added **as a block at the end of the list**.
- To **reorder**: open the equipment's **Commands** tab, **drag and drop** the rows into the order you want, then click **Save**. Your order is kept.
- The order of the **Commands** tab is also the display order below the tile or in the standard widget.

## Commands

The tables below give, for each command, its **identifier** (`logicalId`, stable: scenarios find commands by it), its type and sub-type, and its unit. The labels are those of a **new equipment**; an equipment migrated from 0.x keeps its old names (see [Updating from version 0.x](#updating-from-version-0x)).

### Advanced charging: what is available

Summary of what advanced charging adds. The infos are created **hidden** (display them from the **Commands** tab); the detail of each one is in the [Information](#information-commands) and [Actions](#actions) tables.

| Label | Identifier | Unit | Role | Detail |
|---|---|---|---|---|
| Minimum charge limit | `charge_limit_soc_min` | % | Lowest limit accepted by the vehicle; sets the **Min** of the **Set charge limit** slider | [Tracked vehicle bounds](#command-execution) |
| Maximum charge limit | `charge_limit_soc_max` | % | Highest limit accepted; sets the **Max** of the same slider | [Tracked vehicle bounds](#command-execution) |
| Maximum charge current | `charge_current_request_max` | A | Maximum current announced by the vehicle; sets the **Max** of the **Set charge current** slider | [Tracked vehicle bounds](#command-execution) |
| Charge state (translated) | `charging_state_label` | | Charging state as translated text, for display | [Information](#information-commands) |
| Rated range | `battery_range` | km | Rated range | [Information](#information-commands) |
| Estimated range | `est_battery_range` | km | Range based on your recent driving | [Information](#information-commands) |
| Battery level (raw) | `battery_level` | % | Battery level as the vehicle reports it | [Information](#information-commands) |
| Charging power | `charger_power` | kW | Power delivered to the vehicle | [Information](#information-commands) |
| Actual charge current | `charger_actual_current` | A | Current actually delivered | [Information](#information-commands) |
| Charge phases | `charger_phases` | | Number of phases used | [Information](#information-commands) |
| Energy added | `charge_energy_added` | kWh | Energy added during the current (or last) session | [Information](#information-commands) |
| Charge cable | `conn_charge_cable` | | Type of cable connected | [Information](#information-commands) |
| Fast charging | `fast_charger_present` | | 1 if plugged into a fast charging station | [Information](#information-commands) |
| Cumulative charge energy | `charge_energy_total` | kWh | Index that only increases, for energy tracking | [Charging energy counters](#charge-energy-counters) |
| Scheduled charge time | `scheduled_charging_start_time` | | Start time of the delayed charging (`HH:MM`) | [Schedules read from the vehicle](#information-commands) |
| Off-peak hours end | `off_peak_hours_end_time` | | End of the vehicle's off-peak hours (`HH:MM`) | [Schedules read from the vehicle](#information-commands) |
| Scheduled preconditioning | `scheduled_preconditioning_time` | | Departure time targeted by preconditioning (`HH:MM`) | [Schedules read from the vehicle](#information-commands) |
| Adjust to surplus | `adjust_surplus` | W | Action: receives the available power and decides whether or not to send a command | [Surplus control](#surplus-control) |
| Add charge schedule | `add_charge_schedule` | | Action: creates or replaces the schedule managed by Jeedom (fork proxy) | [Scheduling charging](#scheduling-charging) |
| Delete charge schedule | `remove_charge_schedule` | | Action: deletes this schedule (fork proxy) | [Scheduling charging](#scheduling-charging) |

The advanced charging actions are hidden too. Two functions are set in the equipment rather than through a command:

| Equipment settings | Function | Detail |
|---|---|---|
| **Grid voltage**, **Phases**, **Adjustment step**, **Hysteresis**, **Minimum interval between commands**, **Minimum starting current**, **Stop threshold**, **Hold time before stopping** | Surplus control (defaults: 230 V, single-phase, 1 A, 2 A, 120 s, 6 A, 5 A, 300 s) | [Equipment configuration](#equipment-configuration) and [Surplus control](#surplus-control) |
| **Charging control**, **Range start**, **Range end**, **Target SoC (%)**, **Stop at end of range** | Off-peak hours charging (disabled by default) | [Off-peak hours charging](#off-peak-hours-charging) |

### Climate and comfort: what is available

Summary of what climate control and comfort allow. The official 2.3.0 proxy reads everything, but cannot set the temperature setpoint, the seats, the steering wheel, max defrost or the climate keeper: these commands require the **fork proxy** (versions `2.3.0-tb.N`) and are created **hidden**. The **Owner** key role is **assumed** to be required for the actions (not confirmed in real use: “to be confirmed”).

| Function | Identifier | Availability | Key role | Effect on the vehicle | Detail |
|---|---|---|---|---|---|
| Climate infos (from **Auto climate** to **Battery heater**, including **Climate keeper (dog, camp)**) | `is_auto_conditioning_on`… `battery_heater` | Official proxy 2.3.0 | Charging Manager is enough (read) | Read-only, no wake-up: they keep their last value while the vehicle sleeps. Created hidden | [Information](#information-commands) |
| Driver setpoint, Passenger setpoint | `set_driver_temp`, `set_passenger_temp` | Fork proxy, `2.3.0-tb.1` at minimum | Owner assumed | Sets the requested temperature; both sides go together; the proxy wakes the vehicle | [Setting the temperature setpoint](#setting-the-temperature-setpoint) |
| Heating of the five seats, steering wheel heater | `set_seat_heater_left`, `set_seat_heater_right`, `set_seat_heater_rear_left`, `set_seat_heater_rear_right`, `set_seat_heater_rear_center`, `set_steering_wheel_heater` | Fork proxy, `2.3.0-tb.2` at minimum | Owner assumed | Heats the seat or the steering wheel; in principle requires climate control to be on; the proxy wakes the vehicle | [Heating the seats and the steering wheel](#heating-the-seats-and-the-steering-wheel) |
| Max defrost | `set_preconditioning_max` | Fork proxy, `2.3.0-tb.1` at minimum | Owner assumed | **Wakes** the vehicle and **uses battery** as long as it runs; does not stop by itself | [Max defrost](#max-defrost) |
| Climate keeper mode (keep, dog, camp) | `set_climate_keeper_mode` | Fork proxy, `2.3.0-tb.1` at minimum | Owner assumed | **Wakes** the vehicle and **uses battery over a long period**; does not stop by itself | [Dog mode, camp mode and climate keeper](#dog-mode-camp-mode-and-climate-keeping) |
| Start climate control, Stop climate control | `auto_conditioning_start`, `auto_conditioning_stop` | Official proxy 2.3.0 | Owner assumed (probable refusal with Charging Manager) | Starts or stops preconditioning; starting wakes the vehicle and uses battery | [Actions](#actions) |
| Preconditioning scheduled by Jeedom (equipment setting) | None: **Preconditioning scheduled by Jeedom** section | Official proxy 2.3.0 | Owner assumed (a single attempt per departure with Charging Manager) | Jeedom starts climate control before the departure time then stops it; starting wakes the vehicle and uses battery | [Preconditioning scheduled by Jeedom](#preconditioning-scheduled-by-jeedom) |

> ⚠️ **Battery.** Max defrost, the climate keeper and climate control started in advance **wake the vehicle** and **draw on its battery**. No figure for the consumption is given here for lack of a reliable measurement. **Dog mode** does not replace monitoring the cabin temperature for a pet.

**Why some commands are refused or hidden.** The official 2.3.0 proxy does not have the setpoint, seat, steering wheel, max defrost or climate keeper commands: the fork adds them and **announces** them through its `capabilities` route. As long as the proxy does not announce the command, the plugin refuses it immediately with **“Not supported by your proxy version”**, without sending anything to the vehicle. These commands are created **hidden**, even after switching to the fork: check **Display** in the **Commands** tab, or call them from a scenario. After switching to the fork, **no reinstallation of the plugin** is needed: availability is read again when the proxy version changes. If the vehicle then refuses the command for lack of rights, an **Owner** key is needed: see [Key role](#key-role) and the pairing procedure [Generating the key and pairing it with the vehicle](installation-proxy.md#8-generating-the-key-and-pairing-it-with-the-vehicle). Symptoms without a message are described in [Climate and comfort: symptoms without a message](#climate-and-comfort-symptoms-without-a-message).

### Openings and security: what is available

Summary of the openings, presence, lock, Sentry Mode and alerts. Reads work with the **official 2.3.0 proxy** and a **Charging Manager** key. The trunk-opening commands require the **fork proxy** (versions `2.3.0-tb.N`) and are created **hidden**. The **Owner** key role is required to lock, unlock and control Sentry Mode, and **assumed** to be required for the trunks (not confirmed in real use: “to be confirmed”).

| Function | Identifier | Availability | Key role | Confirmation requested | Detail |
|---|---|---|---|---|---|
| The eight openings (four doors, **Rear trunk**, **Front trunk (frunk)**, **Charge port (opening)**, **Tonneau cover**) | `door_front_driver`, `door_front_passenger`, `door_rear_driver`, `door_rear_passenger`, `trunk_rear`, `trunk_front`, `charge_port_closure`, `tonneau` | Official proxy 2.3.0 | Charging Manager is enough (read) | Not applicable | [Information](#information-commands) |
| **Occupant present** | `user_present` | Official proxy 2.3.0 | Charging Manager is enough (read) | Not applicable | [Information](#information-commands) |
| **Vehicle lock**, **Detailed lock state** | `vehicule_lock`, `lock_state` | Official proxy 2.3.0 | Charging Manager is enough (read) | Not applicable | [Information](#information-commands) |
| **Sentry**, **Sentry source** | `sentry_mode`, `sentry_mode_source` | Official proxy 2.3.0: value of the **last order**. Fork proxy `2.3.0-tb.2` at minimum: **actual** value (vehicle awake) | Charging Manager is enough (read) | Not applicable | [Sentry Mode state](#sentry-mode-state) |
| **Openings alert**, **Unlocked unoccupied alert** and the **Prolonged opening alerts** settings | `closures_alert`, `unlocked_alert` | Official proxy 2.3.0 (settings in the equipment, alerts disabled by default) | Charging Manager is enough (read) | Not applicable | [Prolonged opening alerts](#prolonged-opening-alerts) |
| Lock doors, Unlock doors | `door_lock`, `door_unlock` | Official proxy 2.3.0 | **Owner** (refused with Charging Manager) | Unlock: **yes** | [Actions](#actions) |
| Open charge port, Close charge port | `charge_port_door_open`, `charge_port_door_close` | Official proxy 2.3.0 | Not confirmed (see [Key role](#key-role)) | Open: **yes** | [Actions](#actions) |
| Sentry Mode | `set_sentry_mode` | Official proxy 2.3.0 | **Owner** (refused with Charging Manager) | **Yes** | [Sentry Mode state](#sentry-mode-state) |
| Open rear trunk, Open frunk | `open_trunk_rear`, `open_trunk_front` | Fork proxy, `2.3.0-tb.2` at minimum | Owner assumed | **Yes** | [Opening the rear trunk and the frunk](#opening-the-rear-trunk-and-the-frunk) |

The actions that ask for a confirmation are described in [Confirmation of sensitive actions](#confirmation-of-sensitive-actions). The **Actual** / **Last order** difference of the Sentry Mode is explained in [Sentry Mode state](#sentry-mode-state): test **Sentry source** before relying on **Sentry**.

> **IMPORTANT: trusted network.** The proxy has **neither authentication nor encryption (TLS)** by default; the fork can require an API token, which is optional. With an Owner key, any machine on your local network can unlock the vehicle or open a trunk without going through Jeedom, and Jeedom's confirmation does not hold it back. Keep the proxy on a trusted network, ideally an isolated one, and **never** expose its port to the Internet (see [Key role](#key-role)).

**Why the trunk commands are refused or hidden.** The official 2.3.0 proxy does not have the command that operates a trunk: the fork adds it and **announces** it through its `capabilities` route. As long as the proxy does not announce it, the plugin refuses **Open rear trunk** and **Open frunk** immediately with **“Not supported by your proxy version”**, without sending anything to the vehicle. To enable them: install or update the fork proxy (`2.3.0-tb.2` at minimum), without reinstalling the plugin or recreating the equipment (availability is read again when the proxy version changes). Both commands are created **hidden**, even after switching to the fork: check **Display** in the **Commands** tab, or call them from a scenario. If the vehicle then refuses for lack of rights, an **Owner** key is needed. Symptoms without a message are described in [Openings and security: symptoms without a message](#openings-and-security-symptoms-without-a-message).

### Extended data: what is available

Summary of the infos of the “extended data” group: model, odometer and driving, tire pressure, software update and position. The detail of each info (label, identifier, visibility, historization) is in the [Information](#information-commands) table. All are **read-only**, with no vehicle wake-up.

| Data | Identifiers | Unit | Proxy prerequisite | Read rate |
|---|---|---|---|---|
| Model and year | `model`, `model_year` | | **None**: decoded from the VIN, without querying the proxy | When the equipment is saved, when the plugin is updated and when Jeedom starts |
| Odometer and driving | `odometer`, `shift_state`, `speed`, `power` | km, km/h, kW | The proxy must **announce** `drive_state` | At every data read (vehicle awake) |
| Tire pressure | `tpms_pressure_fl`, `_fr`, `_rl`, `_rr` | bar | The proxy must **announce** `tire_pressure` | At most every **15 minutes**, vehicle awake |
| Software update | `software_update_status`, `software_update_version`, `software_update_progress` | % (progress) | The proxy must **announce** `software_update` | At most every **15 minutes**, vehicle awake |
| Position | `latitude`, `longitude`, `at_home` | ° | The proxy must **announce** `location_data` | At most every **15 minutes**, vehicle awake |

**Which proxy?** A proxy “announces” a piece of data when its `capabilities` route lists it (`http://<proxy_ip>:<port>/api/proxy/1/capabilities`, see [Key role](#key-role)). The **fork proxy** `2.3.0-tb.2` at minimum announces these four categories; the **official 2.3.0 proxy does not serve them**. For the odometer, the feature is merged into wimaha's project but with no published release at the date of this documentation: it will be read only with a release that **announces** it. The plugin never relies on a version number, only on this announcement: check **Proxy version** and, if needed, the address above.

**Why an extended data item is missing.** On a proxy that does not announce a category, the matching infos **are not created**: they do not appear in the **Commands** tab (no “Not supported” value is displayed). Only **Model** and **Model year** are always present. To get them:

1. Check the equipment's **Proxy version**, then install or update the **fork proxy** (see [Checking and updating the proxy version](#checking-and-updating-the-proxy-version)).
2. Wait for the next refresh cycle (one minute at most): at **re-detection**, when the proxy version changes, the plugin reads again what the proxy announces and **creates by itself** the infos that have become available. No plugin reinstallation or equipment recreation is needed. A **Save** on the equipment also creates the missing infos if the proxy announces them.
3. Check that they fill in: they stay empty until the first read, **vehicle awake** (run **Refresh (with wake-up)** to trigger it). Pressures, update and position also wait until 15 minutes have elapsed since the previous attempt.

If a proxy **announces** a category but the vehicle or the proxy **refuses** it (**“Function not supported by this proxy — …”**), the plugin stops requesting it until the next change of the proxy version: see [Extended data: symptoms without a message](#extended-data-symptoms-without-a-message).

**Values and units.**

- **Odometer**: converted from miles to kilometers, to the tenth. A zero or absurd counter is ignored. Historized by default.
- **Gear**: `P`, `R`, `N` or `D`. **Empty** means “not reported”: the plugin then writes an empty string, so a `== "D"` test does not stay true after stopping.
- **Speed** and **Power**: the plugin assumes a speed in mph (converted to km/h) and a power in kW, negative allowed. These two units are not confirmed by any vehicle documentation: compare with your vehicle's screen before relying on them. Created hidden, because with the proxy in the garage they are almost never anything other than 0 or the charging power.
- **Tire pressure**: in **bar**, with no conversion. A zero, negative or greater than 10 bar value is ignored (the info keeps its last value or stays empty). Tires are read only on an awake vehicle: the last values stay displayed when it sleeps.
- **Software update**: four labels, **None**, **Available** (also a scheduled installation), **Downloading** (also waiting for Wi-Fi) and **Installing**. **Offered version** is **None** outside an update, and **Unknown** when an update is active with no version reported. **Progress** is 0 outside downloading and installing. These labels follow Jeedom's language: in a scenario, preferably test **Progress** or compare in the current language.
- **Model** and **Model year**: decoded from the VIN (model: 4th character; year: 10th character, from 2008 to 2037). An empty, non-Tesla or undecodable VIN gives **Unknown**. They are **visible** and **not historized**.
- **Position**: see [Position and privacy](#position-and-privacy).

Extended data is read together with charging data: it therefore follows the **sleep window** (no read during the window, see [Letting the vehicle fall asleep](#let-the-vehicle-fall-asleep)) and keeps its last value while the vehicle sleeps. A refusal of a single category does not prevent the other reads, and never changes **Last error** for pressures, the update and position.

### Information commands

“H”: historized by default. “V”: visible by default on the widget. You can change both settings in the **Commands** tab.

| Label | Identifier | Type / subtype | Unit | H | V | Description |
|---|---|---|---|---|---|---|
| Vehicle presence | `isPresent` | info / binary | | yes | yes | 1 if the proxy reaches the vehicle over Bluetooth, 0 if it is out of range |
| Vehicle awake | `vehicule_isAwake` | info / binary | | yes | yes | 1 if the vehicle is awake, 0 if it is asleep or its sleep state is unknown |
| Vehicle lock | `vehicule_lock` | info / binary | | yes | yes | 1 if the vehicle is locked, including from the inside, 0 if it is unlocked, even partially |
| Driver front door | `door_front_driver` | info / binary | | yes | yes | 1 if the door is open, including ajar, opening or closing, 0 if it is closed |
| Passenger front door | `door_front_passenger` | info / binary | | yes | yes | Same rule as the driver front door |
| Driver rear door | `door_rear_driver` | info / binary | | yes | yes | Same rule as the driver front door |
| Passenger rear door | `door_rear_passenger` | info / binary | | yes | yes | Same rule as the driver front door |
| Rear trunk | `trunk_rear` | info / binary | | yes | yes | 1 if the trunk is open (including ajar or moving), 0 if it is closed |
| Front trunk (frunk) | `trunk_front` | info / binary | | yes | yes | 1 if the front trunk is open (including ajar or moving), 0 if it is closed |
| Charge port (opening) | `charge_port_closure` | info / binary | | yes | yes | 1 if the charge port is open (including ajar or moving), 0 if it is closed. Read even when the vehicle is asleep, unlike **Charge port open** |
| Tonneau cover | `tonneau` | info / binary | | yes | yes | 1 if the tonneau cover (Cybertruck) is open, 0 if it is closed; also 0 on a vehicle that does not have one |
| Occupant present | `user_present` | info / binary | | yes | yes | 1 if the vehicle detects a person on board, 0 otherwise; unknown state = last value |
| Detailed lock state | `lock_state` | info / text | | no | yes | Lock label: **Unlocked**, **Locked**, **Locked from inside** or **Selective unlock**; an unknown value is displayed as is. It follows the Jeedom language: in a scenario, test **Vehicle lock** and **Occupant present**, as a compared label depends on the language |
| Sentry | `sentry_mode` | info / text | | no | yes | **Active**, **Inactive** or **Unknown** (no known reading or order). See [Sentry Mode state](#sentry-mode-state). It follows the Jeedom language: in a scenario, compare in the current Jeedom language, and test **Sentry source** to know where the value comes from |
| Sentry source | `sentry_mode_source` | info / text | | no | yes | **Actual** (read from the vehicle), **Last order** (deduced from the last successful plugin command) or **None** (nothing has been read or ordered yet). Same language rule as **Sentry** |
| Openings alert | `closures_alert` | info / binary | | yes | no | 1 as long as an opening has stayed open longer than the configured duration (only when the alert is enabled), 0 otherwise. See [Prolonged opening alerts](#prolonged-opening-alerts). |
| Unlocked unoccupied alert | `unlocked_alert` | info / binary | | yes | no | 1 as long as the vehicle has stayed unlocked without an occupant longer than the configured duration (only when the alert is enabled), 0 otherwise. See [Prolonged opening alerts](#prolonged-opening-alerts). |
| Charge state | `charging_state` | info / text | | no | yes | Charge state returned by the vehicle, untranslated: `Charging`, `Disconnected`, `Complete`, `Stopped`, `Starting`, `NoPower`, `Calibrating` or `Unknown`. This is the value to test in a scenario |
| Charge state (translated) | `charging_state_label` | info / text | | no | no | The charge state as a label in the Jeedom language (**Charging**, **Disconnected**, **Complete**, **Stopped**, **Starting**, **No power**, **Calibrating**, **Unknown**), for display. A state that the plugin does not know is displayed as the vehicle sends it. It follows the Jeedom language: in a scenario, test **Charge state**, never this label |
| Charge limit | `charge_limit_soc` | info / numeric | % | yes | yes | Configured charge limit |
| Minimum charge limit | `charge_limit_soc_min` | info / numeric | % | no | no | Lowest charge limit the vehicle accepts (used as the **Min** of the **Set charge limit** slider) |
| Maximum charge limit | `charge_limit_soc_max` | info / numeric | % | no | no | Highest charge limit the vehicle accepts (used as the **Max** of the **Set charge limit** slider) |
| Battery level | `usable_battery_level` | info / numeric | % | yes | yes | Usable battery level |
| Battery level (raw) | `battery_level` | info / numeric | % | no | no | Battery level as the vehicle reports it, from 0 to 100%. It may differ by a few points from **Battery level** (usable level) |
| Range | `ideal_battery_range` | info / numeric | km | yes | no | So-called ideal range, converted to kilometers (the vehicle returns it in miles) |
| Rated range | `battery_range` | info / numeric | km | no | no | Rated range, converted to kilometers. It is generally identical to the so-called ideal range |
| Estimated range | `est_battery_range` | info / numeric | km | no | no | Range estimated from your recent driving, converted to kilometers |
| Charger voltage | `charger_voltage` | info / numeric | V | no | no | Voltage delivered by the charging station |
| Charge rate | `charge_rate` | info / numeric | km/h | no | no | Range recovered per hour of charging, converted to km/h (the vehicle returns it in miles per hour) |
| Charging power | `charger_power` | info / numeric | kW | no | no | Power delivered to the vehicle, in kilowatts (the vehicle generally returns it as a whole number) |
| Actual charge current | `charger_actual_current` | info / numeric | A | no | no | Current actually delivered, not to be confused with the configured current (**Charge current (A)**) |
| Charge phases | `charger_phases` | info / numeric | | no | no | Number of phases used by the charge; generally 0 when the vehicle is not charging |
| Energy added | `charge_energy_added` | info / numeric | kWh | no | no | Energy added to the battery during the current (or last) charging session; the vehicle resets it to zero at each new session, a negative value is ignored |
| Cumulative charge energy | `charge_energy_total` | info / numeric | kWh | yes | no | Counter that only increases: sum of the session energies, computed by the plugin (see [Charge energy counters](#charge-energy-counters)) |
| Charge current (A) | `charge_amps` | info / numeric | A | yes | yes | Configured charge current |
| Requested charge current | `charge_current_request` | info / numeric | A | yes | yes | Current requested by the vehicle |
| Maximum charge current | `charge_current_request_max` | info / numeric | A | no | no | Maximum current the vehicle says it can request from the charging station (used as the **Max** of the **Set charge current** slider) |
| Charge time | `minutes_to_full_charge` | info / text | | no | yes | Time remaining until the end of the charge, in `HHhMM` format |
| Charge time remaining | `charge_minutes_remaining` | info / numeric | min | no | no | The same remaining time, in minutes (usable in a scenario or a graph) |
| Charge port open | `charge_port_door_state` | info / binary | | no | no | 1 if the charge port is open, 0 if it is closed |
| Charge port latch | `charge_port_latch` | info / text | | no | no | State of the charging cable latch, as returned by the vehicle |
| Charge cable | `conn_charge_cable` | info / text | | no | no | Type of connected cable, as returned by the vehicle, for example `IEC` (Type 2, Europe), `SAE` (North America), `GB_AC` or `GB_DC` (China); `SNA` when no cable is detected |
| Fast charging | `fast_charger_present` | info / binary | | no | no | 1 if the vehicle is plugged into a fast charging station |
| Scheduled charging mode | `scheduled_charging_mode` | info / text | | no | no | Scheduled charging mode, as returned by the vehicle: `ScheduledChargingModeOff` (no schedule), `ScheduledChargingModeStartAt` (delayed charge) or `ScheduledChargingModeDepartBy` (scheduled departure) |
| Scheduled departure time | `scheduled_departure_time` | info / text | | no | no | Scheduled departure time in `HH:MM` format (vehicle time); empty if no departure is scheduled |
| Scheduled charge time | `scheduled_charging_start_time` | info / text | | no | no | Start time of the delayed charge in `HH:MM` format (Jeedom time); empty outside delayed charge mode. Hidden by default |
| Off-peak hours end | `off_peak_hours_end_time` | info / text | | no | no | End time of the off-peak hours in `HH:MM` format; filled in scheduled departure mode only, empty otherwise or when the vehicle reports midnight. Hidden by default |
| Scheduled preconditioning | `scheduled_preconditioning_time` | info / text | | no | no | Departure time targeted by preconditioning, in `HH:MM` format; filled in scheduled departure mode when preconditioning is enabled, empty otherwise. Hidden by default |
| Interior temperature | `inside_temp` | info / numeric | °C | yes | yes | Cabin temperature, to the tenth of a degree |
| Exterior temperature | `outside_temp` | info / numeric | °C | yes | yes | Outside temperature, to the tenth of a degree |
| Driver temperature | `driver_temp_setting` | info / numeric | °C | no | no | Climate setpoint on the driver side |
| Passenger temperature | `passenger_temp_setting` | info / numeric | °C | no | no | Climate setpoint on the passenger side |
| Climate on | `is_climate_on` | info / binary | | no | no | 1 if the climate control is running |
| Driver seat heater | `seat_heater_left` | info / numeric | | no | no | Driver seat heating level (0 to 3) |
| Passenger seat heater | `seat_heater_right` | info / numeric | | no | no | Passenger seat heating level (0 to 3) |
| Steering wheel heater | `steering_wheel_heater` | info / binary | | no | no | 1 if the steering wheel heater is active |
| Defrost mode | `defrost_mode` | info / text | | no | no | Defrost state |
| Auto climate | `is_auto_conditioning_on` | info / binary | | no | no | 1 if automatic climate control is active |
| Preconditioning active | `is_preconditioning` | info / binary | | no | no | 1 during cabin or battery preconditioning (not to be confused with **Scheduled preconditioning**, the scheduled time) |
| Front defrost | `is_front_defroster_on` | info / binary | | no | no | 1 if the windshield defrost is active |
| Rear defrost | `is_rear_defroster_on` | info / binary | | no | no | 1 if the rear window defrost is active |
| Fan speed | `fan_status` | info / numeric | | no | no | Fan step, raw vehicle value (scale not documented by Tesla) |
| Climate keeper (dog, camp) | `climate_keeper_mode` | info / text | | no | no | Climate keeper mode, as returned by the vehicle: `Off`, `On` (keep), `Dog` (Dog mode), `Party` (Camp mode), `Unknown` |
| Overheat protection | `cabin_overheat_protection` | info / text | | no | no | Cabin overheat protection, as returned by the vehicle: `CabinOverheatProtectionOff`, `CabinOverheatProtectionOn`, `CabinOverheatProtectionFanOnly` (fan only) |
| Rear left seat heater | `seat_heater_rear_left` | info / numeric | | no | no | Rear left seat heating level (0 to 3); also 0 if the vehicle is not equipped with it |
| Rear right seat heater | `seat_heater_rear_right` | info / numeric | | no | no | Rear right seat heating level (0 to 3); also 0 if the vehicle is not equipped with it |
| Rear center seat heater | `seat_heater_rear_center` | info / numeric | | no | no | Rear center seat heating level (0 to 3); also 0 if the vehicle is not equipped with it |
| Steering wheel heat level | `steering_wheel_heat_level` | info / numeric | | no | no | Steering wheel heating level: **0 unknown, 1 off, 2 low, 3 high** (see the warning below) |
| Minimum adjustable temperature | `min_avail_temp` | info / numeric | °C | no | no | Lowest temperature that can be set in the vehicle, to the tenth |
| Maximum adjustable temperature | `max_avail_temp` | info / numeric | °C | no | no | Highest temperature that can be set in the vehicle, to the tenth |
| Battery heater | `battery_heater` | info / binary | | no | no | 1 if the battery heater is active |
| Last error | `last_error` | info / text | | no | yes | Cause of the last read or command failure, followed by the proxy's reason when it gives one; **None** when everything is fine. Usable in a scenario |
| Last data read | `last_data_update` | info / text | | no | yes | Date and time (Jeedom time, `YYYY-MM-DD HH:MM:SS`) of the last successful read of the charge and climate data |
| Data age (min) | `data_age` | info / numeric | min | no | yes | Minutes elapsed since the **Last data read**, recalculated every minute without querying the proxy. It is 0 after each successful read and increases as long as no read succeeds (vehicle asleep, proxy unreachable, sleep window). **99999** = no known read, or more than 69 days |
| Proxy reachable | `proxy_reachable` | info / binary | | no | yes | 1 if the proxy answered at the last refresh cycle, 0 if it is off, unreachable, does not answer in time or returns something other than a valid proxy response (wrong address, proxy too old). A vehicle that is out of range or asleep does not set it to 0. Usable in a scenario |
| Proxy version | `proxy_version` | info / text | | no | yes | Version returned by the proxy at the last cycle (**unknown** if it is unreadable); keeps its last value when the proxy does not answer |
| Key role | `key_role` | info / text | | no | yes | Probable role of the proxy key for this vehicle: **Charging Manager** after a command reserved for the Owner role was refused for lack of rights, **Owner** as soon as one of these commands succeeds, **Undetermined** as long as none has been sent (see [Key role](#key-role)). In a scenario, test `Owner` or `Charging Manager` (never translated); “Undetermined” follows the Jeedom language |
| State read duration | `state_read_duration` | info / numeric | s | no | yes | Time, in seconds to the tenth, of the last successful read of the vehicle state (presence, lock, sleep) at the refresh cycle or through **Refresh**. A failure does not change it: it keeps the duration of the last success. Historize it to track the health of the Bluetooth link (see [Slow proxy read](#slow-proxy-reads)) |
| Data read duration | `data_read_duration` | info / numeric | s | no | yes | Time of the last successful read of the charge and climate data. Unchanged while the vehicle sleeps (no read). A value close to 0 is normal right after another read: the proxy keeps this data in memory for 30 seconds |
| Model | `model` | info / text | | no | yes | Model decoded from the VIN, without querying the proxy: **Model S**, **Model X**, **Model 3**, **Model Y**, **Cybertruck**, **Semi** or **Roadster**; **Unknown** if the VIN is not that of a recognized Tesla. See [Extended data: what is available](#extended-data-what-is-available) |
| Model year | `model_year` | info / text | | no | yes | Model year decoded from the VIN (for example `2023`); **Unknown** if it cannot be decoded |
| Odometer | `odometer` | info / numeric | km | yes | yes | Odometer, converted to kilometers (the vehicle returns it in miles). Created only if the proxy announces `drive_state` |
| Gear | `shift_state` | info / text | | no | no | Engaged gear: `P`, `R`, `N` or `D`; **empty** when the vehicle does not report it. Created only if the proxy announces `drive_state` |
| Speed | `speed` | info / numeric | km/h | no | no | Speed, assumed to be in mph on the vehicle side and converted to km/h (to be confirmed in real use). Created only if the proxy announces `drive_state` |
| Power | `power` | info / numeric | kW | no | no | Instantaneous power, vehicle value in kilowatts, negative allowed (to be confirmed in real use). Created only if the proxy announces `drive_state` |
| Front left tire pressure | `tpms_pressure_fl` | info / numeric | bar | no | yes | Tire pressure, in bar, without conversion. Created only if the proxy announces `tire_pressure` |
| Front right tire pressure | `tpms_pressure_fr` | info / numeric | bar | no | yes | Same, front right tire |
| Rear left tire pressure | `tpms_pressure_rl` | info / numeric | bar | no | yes | Same, rear left tire |
| Rear right tire pressure | `tpms_pressure_rr` | info / numeric | bar | no | yes | Same, rear right tire |
| Software update | `software_update_status` | info / text | | no | yes | **None**, **Available**, **Downloading** or **Installing** (an unexpected status from the proxy is displayed as is). Created only if the proxy announces `software_update` |
| Offered version | `software_update_version` | info / text | | no | yes | Version of the offered update; **None** when there is no update, **Unknown** if an update is active with no reported version |
| Progress | `software_update_progress` | info / numeric | % | no | no | Progress of the download or installation; 0 outside these two phases |
| Latitude | `latitude` | info / numeric | ° | no | no | Vehicle latitude in decimal degrees. **Hidden and not historized**: personal data (see [Location and privacy](#position-and-privacy)). Created only if the proxy announces `location_data` |
| Longitude | `longitude` | info / numeric | ° | no | no | Vehicle longitude, same rules as the latitude |
| At home | `at_home` | info / binary | | no | yes | 1 if the vehicle is within the home radius, 0 beyond it; **never written** as long as the home or the position is unknown |

The **Battery level** information also feeds Jeedom's battery tracking (**Analysis > Equipments** page); **Battery level (raw)** does not feed it.

Each charge and climate information is updated independently: if the vehicle does not return one of them, it keeps its last value and the others are still refreshed.

**Extended charge information.** The ten additional charge information commands (**Charge state (translated)**, **Rated range**, **Estimated range**, **Battery level (raw)**, **Charging power**, **Actual charge current**, **Charge phases**, **Energy added**, **Charge cable** and **Fast charging**) are created **hidden**, including on an existing equipment during the update: show the ones you are interested in from the **Commands** tab, your display and historization choice is never overwritten. They stay empty until the first data read of an awake vehicle, then keep their last value while it sleeps (see **Data age (min)**): at the end of a charge, the power and the actual current may therefore stay at their last value until the next read. The detail of each charge state remains carried by **Charge state**.

**Openings.** The eight opening information commands (**Driver front door** to **Tonneau cover**) are read **without waking the vehicle**, at each information refresh, like presence and lock. A state that the vehicle cannot give (unknown, unlock failure) leaves the **last value** in place, without a message. **Charge port (opening)** (read even when asleep) and **Charge port open** (read only when the vehicle is awake) may differ for a few moments, including right after a command to open or close the charge port: the value converges after the delayed re-read. If the vehicle does not provide the state of its openings at all, the proxy passes them on as closed: they then appear **closed** (only an explicitly unknown state leaves the last value). With a proxy older than 2.3.0, a proxy update is required: the openings are not published (see [Checking and updating the proxy version](#checking-and-updating-the-proxy-version)).

**Occupant and detailed lock.** These two information commands, **Occupant present** and **Detailed lock state**, are read **without waking the vehicle**, at each information refresh, together with presence and lock. An unknown presence leaves the **last value** in place: with the vehicle asleep, the information may stay frozen, do not rely on it alone for security. A vehicle **locked from the inside** leaves **Vehicle lock** at 1. After a lock command, the detailed state follows as soon as the vehicle confirms. A lock state that the plugin does not know is displayed as the vehicle sends it. Do not confuse **Occupant present** with **Vehicle presence** (vehicle within Bluetooth range of the proxy). With a proxy older than 2.3.0, a proxy update is required: this information is not published (see [Checking and updating the proxy version](#checking-and-updating-the-proxy-version)).

**Schedules read from the vehicle.** Three `HH:MM` text information commands, created **hidden**, reflect the vehicle's schedule at each data read (including in “charge only” reads): **Scheduled charge time** (delayed charge mode), **Off-peak hours end** and **Scheduled preconditioning** (scheduled departure mode). With the **Off** mode, or outside the relevant mode, they are **empty** (never `00:00`): test `== ""` in a scenario. The mode itself stays in **Scheduled charging mode**, unchanged. They keep their last value while the vehicle sleeps and are emptied at the first read after the schedule is disabled. Details: the **charge time** is displayed in the Jeedom time zone; **Off-peak hours end** is the value of the setting, whether the option is enabled or not, and stays empty when the vehicle reports midnight; **Scheduled preconditioning** is the targeted departure time, displayed even on days when the schedule does not apply; the days concerned and multi-slot schedules are not read. An unreadable piece of data leaves the information unchanged (mention in the log in debug mode).

**Extended climate information.** The fourteen information commands above, from **Auto climate** to **Battery heater**, are created **hidden** and not historized, including on an existing equipment during the update: show the ones you are interested in from the **Commands** tab, your choice is never overwritten. They are read with the charge and climate data, without any extra request and without ever waking the vehicle: they keep their last value while it sleeps. A field that the vehicle does not return leaves the information unchanged without preventing the others from updating. The values are those of the vehicle, without transformation.

- **Steering wheel heater scale.** Warning: it is not the same as the seats. It is the Tesla protocol scale: note the values on your vehicle before using it in a scenario.

  | Value | Meaning |
  |---|---|
  | 0 | unknown (or steering wheel not equipped) |
  | 1 | off |
  | 2 | low |
  | 3 | high |

  **A “greater than 0” test is therefore false**: the value 1 means the heater is off. To know whether the steering wheel is heating, test `>= 2`. The existing information **Steering wheel heater** (`steering_wheel_heater`) remains the simple active / inactive indicator. For the seats, 0 is “off” and 3 is “high”.
- **Missing equipment.** A rear seat or a steering wheel that the vehicle does not have is reported as 0, like equipment that is off: the information does not allow telling them apart.
- **Minimum and maximum adjustable temperatures.** These are the limits for setting the vehicle's climate control (for example 15 and 28 °C). A missing or zero value, or one outside the 5 to 40 °C range, is ignored; if the minimum is not strictly lower than the maximum, both are ignored (mention in the log in debug mode). They then keep their last value.
- **Battery heater.** It is read from the vehicle's climate data. The equivalent field in the charge data is not provided by proxy 2.3.0 and would always stay at 0: it is not used.
- **Climate keeper (dog, camp).** Possible values: `Off`, `On`, `Dog` (Dog mode), `Party` (Camp mode), `Unknown`. The association of `Party` with Camp mode is to be confirmed on your vehicle. An unreadable value leaves the information unchanged.
- **Overheat protection.** Possible values: `CabinOverheatProtectionOff`, `CabinOverheatProtectionOn`, `CabinOverheatProtectionFanOnly`. A vehicle that does not report the setting is reported as `CabinOverheatProtectionOff`.
- **Fan speed.** Raw value whose scale is not documented: note it on your vehicle before using it in a scenario.
- **Preconditioning and defrosts.** They switch to 1 at the data read that follows their trigger; a cycle only happens if the vehicle is awake, and the proxy keeps its data in memory for 30 seconds. This is not a read triggered by the event.

**Plugin update.** The three schedule information commands are created **hidden** on each existing equipment and stay empty until the first data read of an awake vehicle. The **Cumulative charge energy** information is created **hidden** and **historized** on each existing equipment during the update. It stays empty until the first data read of an awake vehicle, then starts at 0: the energy already charged before the update is not caught up. Likewise, the **Adjust to surplus**, **Add charge schedule** and **Delete charge schedule** actions are added **hidden** to each existing equipment; its settings keep their default values until you change them, and no existing command is modified. The fourteen extended climate information commands are also created **hidden** on each existing equipment, without modifying any climate information already present.

### Charge energy counters

To track your charging consumption, the plugin keeps an **index that only increases**: the **Cumulative charge energy** information (kWh). The vehicle, for its part, resets **Energy added** to zero at each new charging session; it is therefore not a counter that can be used as is.

- **It starts at 0** when the information is created (feature activation), without catching up on history.
- **Computed by difference**: at each data read, the plugin adds to the total the energy gained since the previous read. A session that falls below **90%** of the previously seen value (10% threshold) is a new session: it is added in full. A small isolated drop is ignored. A negative or unreadable value, or one above 1000 kWh (considered aberrant), is ignored. A new session that already reaches 90% of the previous one at the very first read is undercounted.
- **Accuracy limited by the read rate**: the plugin only knows the energy when it reads the data, so only when the vehicle is awake and at the configured rate (see [Faster reading during charging](#accelerated-read-during-charging)). A whole charge started and finished between two reads may be undercounted, and a charge done out of range of the proxy is only partly counted, on return. Conversely, an aberrant read may sometimes cause energy to be counted twice: the total never decreases, but it is not guaranteed to be exact.
- **Battery-side energy**: this is the energy added to the battery, lower than that of the meter or the charging station (charging losses).
- **Jeedom Energy plugin**: declare **Cumulative charge energy** as a consumption command; in principle: absolute index, without checking “Consumption per day” (to be verified depending on the Energy plugin version).
- **Never reset** by a click on **Save** or by a plugin update. There is no manual reset. Deleting the information resets the total to 0 (it is recreated empty at the next save); a duplicated equipment starts from the original's total.

### Actions

Actions marked “hidden” are not displayed on the widget by default; make them visible from the equipment's **Commands** tab.

| Label | Identifier | Type / subtype | Unit | Description |
|---|---|---|---|---|
| Refresh | `refresh` | action / other | | Immediately restarts the reading of the information (any error appears in **Last error**) |
| Refresh (with wake-up) | `refresh_wakeup` | action / other | | Wakes the vehicle if needed, then reads its charge and climate data and publishes them, in a single action (see [Refresh with wake-up](#refresh-with-wake-up)). Only an action from you or from a scenario can do this: the periodic read never wakes the vehicle |
| Wake up | `wake_up` | action / other | | Wakes the vehicle, without reading its data. Unnecessary before a command: the proxy wakes the vehicle by itself. A read without wake-up follows the command (see [Re-read after a command](#re-read-after-a-command)); to get fresh values right away, prefer **Refresh (with wake-up)** |
| Start charging | `charge_start` | action / other | | Starts the charge |
| Stop charging | `charge_stop` | action / other | | Stops the charge |
| Set charge current | `set_charging_amps` | action / slider | A | Sets the charge current (whole number, between the command's Min and Max; 0 to 32 A until the vehicle has published its limit, then its maximum current; set the Max by hand to fix it, or run a read with wake-up to update the limits) |
| Set charge limit | `set_charge_limit` | action / slider | % | Sets the charge limit, between the command's Min and Max (50 to 100% until the vehicle has published its limits, then its limits) |
| Adjust to surplus | `adjust_surplus` | action / slider | W | Receives the **power available for charging** (in watts, **absolute** value, not a variation) and decides by itself whether a command needs to be sent (see [Surplus-based control](#surplus-control)). Created **hidden**: it is called from a scenario. |
| Add charge schedule | `add_charge_schedule` | action / message | | Creates or replaces the charge schedule managed by Jeedom: the **title** carries the days (`lun,mar,mer,jeu,ven`), the **message** the start time (`23:00`). **Fork proxy required**, Jeedom coordinates filled in (see [Scheduling the charge](#scheduling-charging)). Created **hidden**. |
| Delete charge schedule | `remove_charge_schedule` | action / other | | Deletes the schedule created by Jeedom; no effect and no error if there is none. **Fork proxy required** (see [Scheduling the charge](#scheduling-charging)). Created **hidden**. |
| Start climate control | `auto_conditioning_start` | action / other | | Starts preconditioning |
| Stop climate control | `auto_conditioning_stop` | action / other | | Stops preconditioning |
| Driver setpoint | `set_driver_temp` | action / slider | °C | Sets the requested temperature on the driver side, from 15 to 28 °C in steps of 0.5 °C; the passenger side restarts with its last read value. **Fork proxy required**. Created **hidden** (see [Setting the temperature setpoint](#setting-the-temperature-setpoint)). |
| Passenger setpoint | `set_passenger_temp` | action / slider | °C | Sets the requested temperature on the passenger side, from 15 to 28 °C in steps of 0.5 °C; the driver side restarts with its last read value. **Fork proxy required**. Created **hidden** (see [Setting the temperature setpoint](#setting-the-temperature-setpoint)). |
| Set front left seat heater | `set_seat_heater_left` | action / list | | Sets the front left seat heater: Off, Low, Medium or High (0 to 3). **Fork proxy required**. Created **hidden** (see [Heating the seats and the steering wheel](#heating-the-seats-and-the-steering-wheel)). |
| Set front right seat heater | `set_seat_heater_right` | action / list | | Sets the front right seat heater: Off, Low, Medium or High (0 to 3). **Fork proxy required**. Created **hidden** (see [Heating the seats and the steering wheel](#heating-the-seats-and-the-steering-wheel)). |
| Set rear left seat heater | `set_seat_heater_rear_left` | action / list | | Sets the rear left seat heater: Off, Low, Medium or High (0 to 3). **Fork proxy required**. Created **hidden** (see [Heating the seats and the steering wheel](#heating-the-seats-and-the-steering-wheel)). |
| Set rear right seat heater | `set_seat_heater_rear_right` | action / list | | Sets the rear right seat heater: Off, Low, Medium or High (0 to 3). **Fork proxy required**. Created **hidden** (see [Heating the seats and the steering wheel](#heating-the-seats-and-the-steering-wheel)). |
| Set rear center seat heater | `set_seat_heater_rear_center` | action / list | | Sets the rear center seat heater: Off, Low, Medium or High (0 to 3). **Fork proxy required**. Created **hidden** (see [Heating the seats and the steering wheel](#heating-the-seats-and-the-steering-wheel)). |
| Set steering wheel heater | `set_steering_wheel_heater` | action / list | | Turns the steering wheel heater on or off (Off or On, no level). **Fork proxy required**. Created **hidden** (see [Heating the seats and the steering wheel](#heating-the-seats-and-the-steering-wheel)). |
| Max defrost | `set_preconditioning_max` | action / list | | Activates (On) or stops (Off) the vehicle's maximum defrost; wakes the vehicle and uses battery. **Fork proxy required**. Created **hidden** (see [Max defrost](#max-defrost)). |
| Climate keeper mode | `set_climate_keeper_mode` | action / list | | Chooses the climate keeper: Off (0), Keep (1), Dog mode (2) or Camp mode (3); wakes the vehicle and uses battery. **Fork proxy required**. Created **hidden** (see [Dog mode, camp mode and climate keeper](#dog-mode-camp-mode-and-climate-keeping)). |
| Open charge port | `charge_port_door_open` | action / other | | Opens the charge port (hidden) |
| Close charge port | `charge_port_door_close` | action / other | | Closes the charge port (hidden) |
| Flash lights | `flash_lights` | action / other | | Flashes the headlights (hidden) |
| Honk horn | `honk_horn` | action / other | | Sounds the horn |
| Lock doors | `door_lock` | action / other | | Locks the vehicle (hidden) |
| Unlock doors | `door_unlock` | action / other | | Unlocks the vehicle (hidden) |
| Open rear trunk | `open_trunk_rear` | action / other | | Opens the rear trunk, after a re-read of the state: refused if the trunk is read as open, moving or unknown; wakes the vehicle. **Fork proxy required**, confirmation requested. Created **hidden** (see [Opening the rear trunk and the frunk](#opening-the-rear-trunk-and-the-frunk)). |
| Open frunk | `open_trunk_front` | action / other | | Opens the front trunk; wakes the vehicle. **Fork proxy required**, confirmation requested. Created **hidden** (see [Opening the rear trunk and the frunk](#opening-the-rear-trunk-and-the-frunk)). |
| Sentry Mode | `set_sentry_mode` | action / list | | Enables or disables Sentry Mode (**Enabled** or **Disabled**) (hidden). The state is read in **Sentry** and **Sentry source** (see [Sentry Mode state](#sentry-mode-state)) |

## Usage examples

- **Solar charging**: in a scenario, send the available power to **Adjust to surplus** (see the [step-by-step example: solar charging](#step-by-step-example-solar-charging-with-adjust-to-surplus) and [Surplus control](#surplus-control)).
- **Off-peak hours**: enable **Off-peak hours charging** on the equipment (range, target SoC): Jeedom starts and stops charging by itself (see the [step-by-step guide to set up off-peak hours charging](#off-peak-hours-charging)). Without this function, you can also trigger **Start charging** at the beginning of the off-peak hours and **Stop charging** at their end from a scenario.
- **Pre-heating**: enable **Preconditioning scheduled by Jeedom** on the equipment (departure time, days, lead time): Jeedom starts and stops the climate control by itself (see the [usage example](#preconditioning-scheduled-by-jeedom)). Without this function, you can also run **Start climate control** from a scenario a few minutes before you leave.
- **Alert**: get a notification if **Vehicle lock** stays at 0 in the evening.
- **Link failure**: get a notification when **Last error** changes to anything other than **None** (proxy unreachable, proxy without paired key...). A sleeping vehicle does not trigger it.
- **Freshness guard**: only adjust the charge current if the data is less than 5 minutes old, otherwise do nothing (see the step-by-step example “only act on recent data” below).
- **Trunk left open**: enable the prolonged opening alert and trigger a notification (see the [step-by-step example: get alerted when the trunk stays open](#step-by-step-example-get-alerted-when-the-trunk-stays-open)).

### Step-by-step example: solar charging with Adjust to surplus

This scenario regularly sends to **Adjust to surplus** the power that your solar production can devote to charging; the plugin decides by itself whether it really needs to change the current, or start or stop charging (see [Surplus control](#surplus-control)).

**Prerequisites**

- The vehicle is **plugged in** (otherwise the plugin does nothing: **“Vehicle not plugged in: surplus adjustment ignored”**).
- **Interval while charging** set to **1 minute** in the equipment: the control decides based on the last **Charge state** read, hence on the freshness of the reads.
- A measurement of your **grid export** in watts (meter, inverter gateway), or failing that the vehicle's **Charging power**.
- The **Adjust to surplus** action does not need to be visible: it is called from the scenario (the Charging Manager proxy key is enough, see [Key role](#key-role)).

**Starting settings.** In the **Surplus control** section of the equipment, the fields left empty take these values. They are **indicative starting points, to be validated on your installation**: no measurement has been made yet to confirm them.

| Setting | Starting value | Adjust if |
|---|---|---|
| **Grid voltage (V)** | 230 | your phase-to-neutral voltage is different |
| **Phases** | Single-phase | your charger is **three-phase**: choose Three-phase, otherwise the target current is three times too high |
| **Adjustment step (A)** | 1 | you want fewer variations (larger step) |
| **Hysteresis (A)** | 2 | the current changes too often (larger value) |
| **Minimum interval between commands (s)** | 120 (60 minimum) | the vehicle is queried too much (larger value) |
| **Minimum starting current (A)** | 6 | your vehicle or your charger requires a higher current to start |
| **Stop threshold (A)** | 5 (never higher than the start current) | you want to stop earlier or later |
| **Hold time before stopping (s)** | 300 | passing clouds stop the charge too often (larger value) |

**Create the scenario**

1. Open **Tools > Scenarios**, click **Add** and name the scenario, for example “Tesla solar charging”. In **Scenario mode**, choose **Scheduled** and set a run **every 2 to 5 minutes** (for example `*/2 * * * *` for every 2 minutes). Calling more often is pointless: the plugin ignores calls that bring nothing.
2. Open the **Scenario** tab, click **+ Block** and choose **If/Then/Else**.
3. In **IF**, enter a freshness guard, for example `#[Garage][Tesla][Data age (min)]# <= 5` (see the [step-by-step example: only act on recent data](#step-by-step-example-only-act-on-recent-data)). This guard is **optional**.
4. In **THEN**, add a variable-assignment **Action**: name `available_power`, value = **grid export + charging power**, in **watts**. For example `#[Garage][Meter][Grid export]# + #[Garage][Tesla][Charging power]# * 1000`.
5. Still in **THEN**, add an **Action**: the vehicle's **Adjust to surplus** command, with the value `variable(available_power)` (reading the variable assigned in the previous step).
6. **Save**, then run the scenario once by hand.

**Why “export + charging power”.** The value sent is the **absolute** power that the vehicle can consume. The export measured by the meter is already **reduced** by what the vehicle consumes: without adding the current charging power, the setpoint would drop back at every adjustment. If your meter gives the export with a negative sign, fix the sign to get positive watts. A negative value is brought back to 0 W anyway.

**If the only source is the vehicle's Charging power.** It is in **kilowatts** and often a **whole number**: multiply by 1000 (as above) and expect a coarse value. If you have one, prefer the measurement from a meter or from the charger.

**Check that it works.** Set the plugin log to **Debug** (**Plugin configuration > Logs**) and run the scenario: each call writes a line **“pilotage selon le surplus : … W, courant calculé … A, cible … A, décision … (motif)” (*surplus control: … W, computed current … A, target … A, decision … (reason)*)**. The possible decisions include `set_charging_amps`, `charge_start`, `charge_stop`, `aucune` and `ignorer`; the reason explains why (hysteresis, minimum interval, current already at the target...). An abstention by the plugin also appears in **Last error**.

**What happens at night.**

- Without production, the available power drops to **0 W**: the computed current falls below the **Stop threshold**, and the charge is **stopped** once the **Hold time before stopping** has elapsed (300 s by default). The next day, it restarts when the computed current reaches the **Minimum starting current**.
- If you also use [Off-peak hours charging](#off-peak-hours-charging), the **Adjust to surplus** call is **ignored during the range** (without error): the solar scenario therefore does not stop the off-peak charge. Outside the range, surplus control takes over again.

### Step-by-step example: get alerted when the proxy is unreachable

The **Proxy reachable** info is 1 as long as the proxy answers the refresh cycle (published at every pass where a vehicle of this proxy is read, according to its interval) and goes to 0 when it is off, unreachable or does not answer in time. A vehicle that is out of range or asleep does not make it go to 0. Create a scenario that warns you:

1. Open **Tools > Scenarios**, click **Add** and name the scenario, for example “Tesla proxy alert”. In **Scenario mode**, choose **Triggered** (the scenario runs when its trigger changes).
2. In **Trigger(s)**, click **+ Trigger** and choose the **Proxy reachable** command of your vehicle. It is written `#[Object][Vehicle][Proxy reachable]#` (for example `#[Garage][Tesla][Proxy reachable]#`). With several vehicles or several proxies, add the **Proxy reachable** of each vehicle.
3. Open the **Scenario** tab, click **+ Block** and choose **If/Then/Else**.
4. In the **IF** field, enter the condition `#[Object][Vehicle][Proxy reachable]# == 0` (or choose the command with the selection button, then add `== 0`).
5. In **THEN**, add an **Action**: a notification command of your installation (mobile app, Telegram, e-mail...) or the **Add a message** command of the Jeedom message center. Enter the text, for example “The Tesla proxy no longer responds: check the garage Raspberry Pi”.
6. To also be warned when it comes back, add a second notification in **ELSE**, for example “The Tesla proxy responds again”.
7. **Save**, then test by turning off the Raspberry Pi: at the next read (at most the shortest interval of the vehicles of this proxy, 5 minutes by default), **Proxy reachable** goes to 0 and the notification is sent. Turn it back on: at the next cycle, the info goes back to 1 and the recovery notification is sent.

The scenario is triggered at every change of the value, so at the failure and then at the recovery, not at every cycle. For the precise cause (key, range, frozen adapter), check **Last error**.

### Step-by-step example: only act on recent data

The **Data age (min)** info gives the number of minutes elapsed since the last successful read of the charge and climate data. It is 0 right after a read and increases as long as no read succeeds: vehicle asleep, sleep window open, proxy unreachable. It is **99999** as long as no read is known (new equipment, plugin just updated). The following scenario, for solar control, only adjusts the **Set charge current** if this value is recent:

1. Open **Tools > Scenarios**, click **Add** and name the scenario, for example “Tesla solar charging”. In **Scenario mode**, choose **Scheduled** and set a run every 5 minutes.
2. Open the **Scenario** tab, click **+ Block** and choose **If/Then/Else**.
3. In the **IF** field, enter the condition `#[Object][Vehicle][Data age (min)]# <= 5` (for example `#[Garage][Tesla][Data age (min)]# <= 5`), or choose the command with the selection button then add `<= 5`.
4. In **THEN**, add an **Action**: the vehicle's **Set charge current** command, with the value computed by your scenario from the solar production.
5. In **ELSE**, put **nothing** (the charge current stays what it was), or add a notification, for example “Tesla data too old: charge current unchanged”.
6. **Save**, then set **Interval while charging** to **1 minute** in the equipment: during charging, the data age stays at 1 minute at most and the condition is true.

Why **5**? It is the default refresh interval: beyond it, at least one read was missed. Adapt the threshold to your rate (a little more than the interval used while charging).

Why **99999** is a good thing here: as long as no read is known, the condition `<= 5` is **false**, the scenario does nothing and sends no current. It is cautious by design.

> **Warning**
>
> Do **not** use **Data age (min)** as the **trigger** of a scenario in **Triggered** mode: this info is recalculated **every minute** and therefore changes constantly, the scenario would run in a loop (and a notification would be sent every time).

**Variant: “data older than 2 hours” alert.** Create a scenario in **Scheduled** mode (for example every hour) with the condition `#[Object][Vehicle][Data age (min)]# >= 120 AND #[Object][Vehicle][Data age (min)]# < 99999` and a notification in **THEN**. The `< 99999` bound avoids a false alert when no read is known; prefer `>= 120` to an exact equality (`== 120`), which is only true for one minute and may be skipped. A vehicle that sleeps for a long time triggers this alert without any failure: it is a simple freshness check. To get fresh data, run **Refresh (with wake-up)**.

### Step-by-step example: get alerted when the trunk stays open

This scenario warns you when an opening (rear trunk, frunk, door, charge port) stays open for more than 10 minutes. It relies on the prolonged opening alert (see [Prolonged opening alerts](#prolonged-opening-alerts)); a Charging Manager key is enough, as these are reads.

1. Open the page of your vehicle (**Plugins > Connected objects > Tesla BLE**) and go to the **Prolonged opening alerts** block.
2. In **Opening left open**, check **Enable** and enter **Delay before alert (min)**: `10`. The delay is required, from 1 to 1440 minutes.
3. **Save**. An error message on saving reports an empty or invalid delay (see [Messages on saving](#messages-on-save)).
4. Open the **Commands** tab and check **Display** on **Openings alert** (it is hidden by default, but already historized). **Save**.
5. Open **Tools > Scenarios**, click **Add** and name the scenario, for example “Trunk open alert”. In **Scenario mode**, choose **Triggered**.
6. In **Trigger(s)**, add the **Openings alert** command of your vehicle, for example `#[Garage][Tesla][Openings alert]#`.
7. In the **Scenario** tab, add an **If/Then/Else** block with the condition `#[Garage][Tesla][Openings alert]# == 1`. The scenario also runs when it goes back to 0: without this condition, you would be notified when closing.
8. In **THEN**, add a notification **Action** of your installation (mobile app, Telegram, e-mail...) with a text such as “A Tesla opening has been left open for more than 10 minutes”. The Jeedom message center receives for its part a message naming the opening, without any configuration.
9. **Save**, then test: open the rear trunk by hand and wait for the chosen delay **plus two refresh intervals** (up to 20 minutes with 10 minutes and the default interval of 5 minutes). **Openings alert** goes to 1, the message appears in the message center and the notification is sent.
10. Close the trunk: at the next read, **Openings alert** goes back to 0 and the scenario runs without notifying. The message stays in the message center: delete it.

For a vehicle left unlocked, proceed in the same way with **Vehicle unlocked with no occupant** and the **Unlocked unoccupied alert** info.

**Usage tips for occupant presence.** **Occupant present** (`user_present`) is 1 when the vehicle detects a person on board.

- **“Nobody on board” condition.** In a scenario, test `#[Garage][Tesla][Occupant present]# == 0` before an action that only makes sense with an empty vehicle (for example re-running a lock). Combine it with **Vehicle lock** and test these two infos rather than the **Detailed lock state** label, which changes with the Jeedom language.
- **Unknown presence = last value.** When the vehicle does not report the state (it is asleep), the info keeps its last value: it may show “nobody” while a person stayed on board, or the opposite. Check **Data age (min)** if the decision matters.
- **It is not a safety feature.** Never use it to protect a person or an animal (for example to decide to switch off the climate control: a child or an animal left on board may not be detected). Do not confuse it with **Vehicle presence**, which only says that the vehicle is within Bluetooth range of the proxy.

## Versions, languages and support

### Stable or beta version

The plugin is published on the Jeedom Market in two versions: the **stable** one (recommended) and the **beta** one (release candidate, which receives new features first, reserved for beta testers).

- **Install.** In **Plugins > Plugins management > Market**, open **Tesla BLE** and click **Install stable** or **Install beta**. The Market synchronizes versions every night: a new feature may take a day to appear.
- **Know what is installed.** At the top of the plugin page, the name is followed by its ID in parentheses, then the version type (stable, beta).
- **Go back to stable.** On the same page, click **Install stable**. If the Jeedom **cron** log then shows an error every minute, see [Refresh cycle task](#refresh-cycle-task).

> **IMPORTANT**: Jeedom warns that putting a beta plugin on a non-beta Jeedom is really not recommended. Avoid the beta on a production Jeedom.

### Reading the changelog

The [changelog](changelog.md) is **single**: it serves both the stable and the beta. Entries are dated, the most recent at the top, and prefixed with **Added**, **Fix**, **Change** or **Documentation**.

It is published before the stable version: a recent entry may describe a new feature that is only available in beta for now. A plugin update with no changelog entry only concerns documentation, a translation or text.

### Available languages

The interface (configuration, equipment, messages, vehicle tile and names of **created** commands) and the documentation exist in French, English, German and Spanish.

- **Interface.** It follows the **Jeedom language**: **Settings > System > Configuration**, **General** tab, **Language** field (global Jeedom setting). Untranslated text is displayed in French.
- **Commands already created.** They keep their name; for labels compared in a scenario, see [Sentry Mode state](#sentry-mode-state).
- **Documentation.** The Jeedom **Documentation** button opens the French version. To change language, use the selector of the documentation site (`https://jeedomdocs.decastro.fr/teslable/`, `/en/teslable/`, `/de/teslable/` or `/es/teslable/`).

### Reporting a defect

There is no official topic for this plugin. Open a topic on the Jeedom community forum (<https://community.jeedom.com>), in the plugins category, with **Tesla BLE** in the title. Include:

- the plugin version and its channel (stable or beta);
- the Jeedom version and the Debian version;
- the proxy version and type (wimaha's or the fork);
- an excerpt of the **TeslaBLE** log at **Debug** level.

Review these items before publishing them: never leave your token, your full VIN or any IP address you do not want to make public. See [Viewing the proxy logs](#viewing-the-proxy-logs).

## Known limitations

- **After a command**, only the charge limit, the charge current and the lock are updated immediately. The other infos are up to date after the **scheduled re-read** (30 seconds by default, see [Re-read after a command](#re-read-after-a-command)), or at the next read if the proxy is busy. If the vehicle has gone back to sleep, the last values are kept (no error, no wake-up); when out of range, presence goes to “No”; if the proxy is unreachable, “Last error” is filled in.
- **Vehicle asleep**: the charge and climate infos are only read when the vehicle is awake (the plugin never wakes it up by itself). Use **Refresh (with wake-up)**.
- **Sleep window**: during the window, the charge and climate infos and the **Last data read** are frozen (default duration 30 minutes). A charge or climate started from the app without a visible change of the state without wake-up is only seen at the check read. Uncheck **Let the vehicle fall asleep** in the equipment for a full read at every pass.
- **Charging Manager key**: lock, horn, lights and Sentry Mode are refused by the vehicle. The plugin detects it (**Key role** info) but does not grey out these commands on the dashboard (see [Key role](#key-role)).
- **Climate in charge only**: with **Also read the climate** set to **No, charge only**, all the climate infos (temperatures, heaters, defrost, fan, climate keeper, climate on, etc.) are no longer updated and keep their last value; the climate commands remain available.
- **Charge energy counter**: its accuracy depends on the read rate, it may undercount a short charge or one done out of range and it is not reset to zero; it is only read at the rate of the reads, so a spaced-out rate makes it less accurate (see [Charge energy counters](#charge-energy-counters)).
- **Surplus control**: the default thresholds (start 6 A, stop 5 A, hold 300 s) must be validated with your vehicle; the reference is the **last setpoint sent by the control** (a concurrent manual setting is only seen after a gap greater than the hysteresis, a stop or an unplugging); a scenario call may wait up to about 210 seconds; the decision is based on the last **Charge state** read, hence on the freshness of the reads (see [Accelerated read while charging](#accelerated-read-during-charging)).
- **Solar control: Bluetooth load and sleep.** While charging, the vehicle is awake anyway, but surplus control puts a load on it: with **Interval while charging** at 1 minute, a read takes place **every minute**, **every command actually sent wakes up the vehicle** and **a re-read follows every successful command** (see [Re-read after a command](#re-read-after-a-command)). A vehicle that receives commands all day therefore has little chance of falling asleep. Space out the calls (**Minimum interval between commands**, hysteresis, scenario every 2 to 5 minutes). **No measurement of Bluetooth link or battery wear is published**: do not infer any guarantee or quantified risk from it.
- **Off-peak hours charging**: the decision follows the read rate (stop at the approximate target SoC without **Interval while charging**); a sleeping vehicle is never stopped, and its published state may be stale; **starting the charge wakes up the vehicle**; a start not followed by a charge is **not retried** before the next range (a single start per plug-in); a **Start** or **Stop** issued from Jeedom during the range suspends the control until the next range; a range that begins in the hour skipped at the **daylight saving time change** only starts at the end of that hour, and a manual action made during that hour may be ignored; a single range per vehicle; the 2-minute delay to observe the result of a command must be validated in real use (see [Off-peak hours charging](#off-peak-hours-charging)).
- **Preconditioning scheduled by Jeedom**: the Owner role (assumed) must be confirmed in real use; the decision follows the read rate (start and stop within a few minutes, nothing if no read falls in the window; an interval of 5 minutes at most is recommended); **starting the climate control wakes up the vehicle** and uses battery; a vehicle seen asleep is never stopped; a climate control that is still running at the first read after the end of the window is stopped, even with an occupant; disabling the function during the window does not stop a climate control already started; the temperature used is the one already set in the vehicle; a single window per vehicle, the vehicle's schedule is not read to decide; requires **Also read the climate** set to **Yes** (see [Preconditioning scheduled by Jeedom](#preconditioning-scheduled-by-jeedom)).
- **Charge schedules**: **Scheduled charge time** assumes that the vehicle returns, in scheduled charging mode, a valid timestamp over Bluetooth (to be confirmed in real use: otherwise the info stays empty); **Off-peak hours end** is published even if the off-peak hours option is unchecked (the proxy does not report its state); the days of application and multiple ranges are not read.
- **Schedule charging**: reserved for the fork proxy (immediate refusal with proxy 2.3.0, whose official version does not have the scheduling route: the fork adds it, versions `2.3.0-tb.N`); a single Jeedom-managed schedule per vehicle, with start time only; it follows the Jeedom coordinates, which must match the parking location; the time is the vehicle's; replacement without duplicates, the minimal key role and the update of the schedule infos after the command must be confirmed in real use (see [Schedule charging](#scheduling-charging)).
- **Temperature setpoint**: reserved for the fork proxy (immediate refusal with proxy 2.3.0); both sides are always sent together, the other side with its last read value (a setpoint set on the vehicle screen since the last read may be overwritten); the slider is limited to 15 to 28 °C, in half-degree steps; the Owner role assumed to be necessary and the temperature level (a setpoint that does not go to “HI”) must be confirmed in real use (see [Set the temperature setpoint](#setting-the-temperature-setpoint)).
- **Seat and steering wheel heating**: reserved for the fork proxy, version `2.3.0-tb.2` at least (immediate refusal with proxy 2.3.0); the six actions stay **hidden**: display them yourself after switching to the fork; no seat backs and no third row; steering wheel on/off only; the behavior with the climate control off, with a missing seat and with an automatically heated steering wheel must be validated in real use.
- **Max defrost**: reserved for the fork proxy, version `2.3.0-tb.1` at least (immediate refusal with proxy 2.3.0); the action stays **hidden**: display it yourself after switching to the fork; it wakes up the vehicle and uses battery, and does not stop by itself; with **Also read the climate** set to **No, charge only**, or if the vehicle falls asleep again, **Defrost mode** keeps the optimistic value (a displayed `Off` may be wrong if the vehicle says `Normal`); the Owner role and the behavior when stopped (`Off` or `Normal`) must be validated in real use.
- **Dog mode, camp mode and climate keeper**: reserved for the fork proxy, version `2.3.0-tb.1` at least (immediate refusal with proxy 2.3.0); the action stays **hidden**: display it yourself after switching to the fork; it wakes up the vehicle, uses battery over a long period, does not stop by itself and does not replace temperature monitoring for an animal; with **Also read the climate** set to **No, charge only**, or if the vehicle falls asleep again, **Climate keeper (dog, camp)** keeps the announced value; the sleep window does not open as long as a keeper (`On`, `Dog`, `Party`) is read; the Owner role, the `Party` name of camp mode and the value read back after a stop must be validated in real use.
- **Open the rear trunk and the frunk**: reserved for the fork proxy, version `2.3.0-tb.2` at least (immediate refusal with proxy 2.3.0); both actions stay **hidden**: display them yourself after switching to the fork; they wake up the vehicle; the rear trunk is only opened if it is read as closed (the re-read may miss a recent opening, and a power liftgate may then close again); a latch reported as “not released” (previous opening failure) is treated as closed and the command is sent again, behavior to be validated in real use; the frunk is not re-read; the plugin never closes a trunk; the Owner role assumed to be necessary and the behavior on a power trunk (or a power frunk) must be validated in real use.
- **Sentry Mode state**: the actual read requires the fork proxy in version `2.3.0-tb.2` at least and an **awake** vehicle; otherwise the info follows the **last order** sent by Jeedom and sees neither a change made from the app, the vehicle screen or an automatic shutdown, nor a value read on a sleeping vehicle (last read value kept); the `Idle` state is counted as **Active** (to be confirmed in real use); the labels follow the Jeedom language (see [Sentry Mode state](#sentry-mode-state)).
- **Prolonged opening alerts**: the delay is only counted on successful reads, at the refresh rate (alert between the delay and the delay plus two intervals). If the **Jeedom cache is cleared** during an alert, the episode is forgotten: the info goes back to 0 then to 1 after a full delay, with a second message. A **Charge state** frozen on a sleeping vehicle (for example “Stopped” or “Complete” stale after an unplugging) hides a charge port left open. Without the vehicle's openings information (eight states closed or absent), the episode is considered closed. The message is not removed from the message center on closing.
- **Extended data** (model, mileage and driving, tires, software update, position): with the exception of the model and the year, they require the **fork proxy** (`2.3.0-tb.2` at least) that **announces** them; otherwise they are not created. They are only read with the **vehicle awake** and within Bluetooth range (pressures, update and position at most every 15 minutes, not during a sleep window). The units of **Speed** (mph) and **Power** (kW) are assumed and must be confirmed in real use. **At home** is binary: never written without a home or position (the tile shows 0 before the first computation), it does not go back to 0 when the vehicle leaves; test `== 1` with **Vehicle presence**. The Jeedom `event` log records latitude and longitude even when masked (see [Position and privacy](#position-and-privacy)).
- **Widget and display**: a **generic type** cleared by hand (**None**) may be set again if the command is deleted then recreated, or if the setting of the types is replayed after an interrupted update (see [Generic types](#generic-types)); an **image removed** with **Remove the image** is **never set again** and no button restores the plugin image; the **command order** is only set at creation and never rewritten; the **Data from … ago** duration of the tile is not aged in the browser; the **standard widget** does not display the model image (see [Widget and display](#widget-and-display)).
- **A single equipment per vehicle** (unique VIN).
- **Historized scheduled departure time**: if it was historized before the update, it stays numeric and is no longer updated until its sub-type is changed to **Other**.
- **Proxy declared by a Docker service name**: the link to the dashboard does not open in the browser (see [Link to the proxy dashboard](#link-to-the-proxy-dashboard)).

### Numeric limits

| Limit | Value |
|---|---|
| Bluetooth devices per vehicle | **3** at the same time (phones, watch, proxy). Beyond that, intermittent connections. |
| Vehicles per proxy | **3 at most** so that the cycle is never cut short in the worst case; beyond that, check the **Last data read** of each vehicle. |
| Cycle duration | Run **every minute** for the vehicles that are due (5-minute interval by default), 4 minutes at most; it lasts as long as its slowest proxy (the proxies are read in parallel). |
| Wait for a busy proxy | About 2 minutes (110 seconds for a read, 15 seconds for the pairing check), then **Proxy busy**. |
| Key role | **Charging Manager** by default: reads and charging only, including surplus control and off-peak hours charging; **Owner** for locking, unlocking, horn, lights, Sentry Mode, trunks (assumed) and scheduled preconditioning (see [Key role](#key-role)). |
| Proxy authentication | **None by default**: keep it on a trusted network, never exposed on the Internet. The fork proxy can require an **API token** (optional, same token for all proxies), which protects access but does not replace a trusted network. |
| Equipment per vehicle | Only one (unique VIN). |
| Proxy logs | Proxy **2.3.0** minimum; only the proxy from the plugin configuration is displayed. |

## Troubleshooting

Set the plugin log to **Debug** level (**Plugin configuration > Logs**) to see every URL called and every proxy response. The outage start and end lines require at least the **Info** level.

Messages are sorted by where you see them.

### Test button messages

| Message | Cause | Action |
|---|---|---|
| **“Proxy URL not set”** | The field is empty. | Enter the proxy address. |
| **“Invalid URL: it must start with http:// or https://…”** | The address is badly entered (missing scheme, disallowed characters, invalid port). | Correct it, for example `http://192.168.1.50:8080/`. The trailing `/` is added automatically. |
| **“Invalid URL: credentials (user:password@) are not supported”** | The address contains credentials. | Remove `user:password@`: the proxy has no authentication. |
| **“Proxy reachable — version X”** (green) | Everything is fine. | Nothing to do. |
| **“Proxy reachable — version X”** + **“Proxy version not supported: 2.3.0 minimum, update the proxy”** (orange) | The proxy responds but its version is too old. | Update it (see [Check and update the proxy version](#checking-and-updating-the-proxy-version)). |
| **“Proxy reachable — unknown version”** (green) | The proxy responds but does not give a usable version number (manual installation for example). | Check the version by hand with the address from the prerequisites Tip. |
| **“Proxy version not reported: proxy older than 2.1.3, or incorrect URL”** (orange) | The proxy answers “not found” to the version query. | Check the address and port; otherwise update the proxy. |
| **“Proxy unreachable”** (red, detail `cURL …`) | Nothing responds at this address. | Check the address, the port, that the proxy is running and that the Raspberry Pi is powered on. |
| **“Timeout”** (red) | The proxy does not respond within 10 seconds. | Check the Raspberry Pi (power supply, Wi-Fi), restart the proxy. |
| **“Invalid proxy response”** (red) | What responds is not TeslaBleHttpProxy (wrong port, another service). | Check the address and port. |
| **“No response from the Jeedom server: check the TeslaBLE log”** | Jeedom did not respond to the test after 45 seconds. | Try again, then check the plugin log. |
| **“Internal plugin error: check the TeslaBLE log”** | Unexpected plugin error. | Check the plugin log and report the error with this log. |

The test only queries the proxy version: a green test proves neither that the key is paired nor that the vehicle is in range. For that, use the **Check pairing** button of the equipment (see [Pair my key and check pairing](#pairing-my-key-and-checking-the-pairing)).

### Messages on save

- **“Invalid URL: …”** (plugin configuration or a vehicle’s proxy URL): same causes as for the **Test** button. The previous URL is kept.
- **“No proxy URL configured: …”** (a vehicle’s last error or the **Test this proxy** button): neither the vehicle nor the plugin configuration has a proxy URL. Fill in one of the two.
- **“Invalid VIN: 17 characters expected, digits and letters except I, O and Q”**: correct the equipment’s VIN (spaces are removed automatically).
- **“This VIN is already used by equipment …”**: another equipment already has this VIN, which also happens with **Duplicate**. Delete the duplicate or correct the VIN.
- **“Off-peak hours charging: the start (or end) time must be in HH:MM format, from 00:00 to 23:59”**, **“… the target SoC must be a whole number between 1 and 100 %”**, **“… the time range is empty, the end time must differ from the start time”** and **“… enter the start time, end time and target SoC to enable the function”**: invalid **Off-peak hours charging** setting; correct it (nothing was saved).
- **“Surplus control: …”**: surplus control setting out of bounds (see [Surplus control](#surplus-control)).
- **“Scheduled preconditioning: the departure time must be in HH:MM format, from 00:00 to 23:59”**, **“… the lead time must be a whole number between 1 and 60 minutes”**, **“… the maximum duration must be a whole number between 1 and 120 minutes”**, **“… the maximum duration must be at least equal to the lead time”**, **“… enter the departure time to enable the function”**, **“… select at least one day to enable the function”** and **“… ‘Also read the climate’ must remain set to Yes to enable the function”**: invalid **Preconditioning scheduled by Jeedom** setting; correct it (nothing was saved).
- **“Prolonged opening alerts: the delay before alert … must be a whole number between 1 and 1440 minutes, required to enable the alert”**: the alert delay (opening left open, or vehicle unlocked with no occupant) is empty while the alert is enabled, or is not a whole number from 1 to 1440 (see [Prolonged opening alerts](#prolonged-opening-alerts)). Nothing is saved.
- **“Invalid home position: enter the latitude (from -90 to 90) and the longitude (from -180 to 180) in decimal degrees, 8 decimals at most, or leave both empty to use the Jeedom position”**: only one of the two home coordinates is filled in, or one is out of range, non-numeric, has too many decimals, or the pair is 0/0. Correct them (or empty both fields to use the Jeedom position); nothing was saved. The value entered is never copied into the message (see [Position and privacy](#position-and-privacy)).
- **“Invalid home radius: whole number of meters, from 10 to 10000”**: the **Radius (m)** is not a whole number from 10 to 10000. Correct it (or empty the field for 100 m); nothing was saved.
- **“Internal plugin error: check the TeslaBLE log”**: unexpected error on save; the detail is in the plugin log.

### Jeedom message center (after an update)

- **“The VIN of equipment … is invalid: correct it in its configuration page…”**: the VIN saved by an older version is not valid. Correct it.
- **“Equipment … has the same VIN as equipment …”**: two equipments for the same vehicle. Delete the duplicate or correct its VIN.
- **“The info … is historized: it stays numeric and is no longer updated…”**: see [Scheduled departure time](#scheduled-departure-time).
- **“Proxy Bluetooth adapter probably frozen — …”**: see [Frozen Bluetooth adapter alert](#frozen-bluetooth-adapter-alert). Restart the Raspberry Pi.
- **“…: opening “…” open for more than … min”** and **“…: vehicle unlocked with no occupant for more than … min”**: prolonged opening alerts, one message per opening and per episode (see [Prolonged opening alerts](#prolonged-opening-alerts)). The message is not removed on closing: delete it.

### “Last error” info (read)

| Displayed text | Cause | Action |
|---|---|---|
| **None** | The last read cycle succeeded (or the vehicle is asleep, which is not an error). | Nothing to do. |
| **Proxy unreachable** | The proxy does not respond at the configured address. | Check the URL, that the proxy is running, and the Raspberry Pi’s power supply and Wi-Fi. |
| **Timeout** | The proxy or the vehicle responds too slowly. | Check the Raspberry Pi (power supply, Wi-Fi), restart the proxy if it keeps happening. |
| **Proxy Bluetooth adapter probably frozen: restart the Raspberry Pi** | Several reads in a row timed out while the proxy responds: see [Frozen Bluetooth adapter alert](#frozen-bluetooth-adapter-alert). | Restart the Raspberry Pi. |
| **Proxy without key: pairing required — …** | No key on the proxy: it has not yet generated or installed any. | Generate a key (**Generate**) in the proxy dashboard, send it to the vehicle and validate with the key card (link in the plugin configuration or in **Pair my key**). |
| **Vehicle out of range — …** | The proxy cannot find the vehicle over Bluetooth. **Vehicle presence** goes to 0. | Move the Raspberry Pi closer to the vehicle; check that the proxy has Bluetooth to itself and that the vehicle does not already have 3 connected devices. |
| **Vehicle not plugged in / out of range of the proxy / Charging complete / The charger supplies no current: surplus adjustment ignored** or **Charging state unknown: run Refresh (with wake-up)** | Surplus control sent no command for this reason (see [Surplus control](#surplus-control)). | Plug in the vehicle, move the proxy closer, or run **Refresh (with wake-up)** for the unknown state. |
| **Vehicle not plugged in / The charger supplies no current: off-peak hours charging pending** (possibly followed by **(state read at HH:MM, vehicle asleep)**) or **Charging state unknown: run Refresh (with wake-up)** | Off-peak hours charging sent no command for this reason. “Vehicle asleep” suffix: the displayed state dates from the last read before it fell asleep and may be stale. | Plug in the vehicle, or run **Refresh (with wake-up)** for an unknown or stale state (see [Off-peak hours charging](#off-peak-hours-charging)). |
| **Off-peak hours charging suspended until the next range: charging restarted outside the control** | Charging was restarted from the Tesla app after stopping at the target SoC: Jeedom no longer interrupts it. | Nothing to do: control resumes at the next range. |
| **Off-peak hours charging suspended until the next range: repeated command failures** | Three commands in a row failed (see the command’s error message in the log, warning). | Fix the cause (key, range, proxy); unplugging then plugging back in restarts control, otherwise it resumes at the next range. |
| **Charging started by Jeedom but stopped or not started: no new attempt before the next range** | A charge started by Jeedom was not observed (stopped from the app, charger refusing, start too slow). **No new attempt** is made so as not to wake the vehicle in a loop. | Check the charger and the vehicle; start charging by hand if needed (this suspends control until the next range). |
| **Vehicle not plugged in: scheduled preconditioning not started** (possibly followed by **(state read at HH:MM, vehicle asleep)**) or **Charging state unknown: run Refresh (with wake-up)** | With the **Only if plugged in** option, scheduled preconditioning did not start climate control for this reason. The unknown state message also appears, even without the option, when the climate state of the awake vehicle is unknown. | Plug in the vehicle, untick the option, or run **Refresh (with wake-up)** for an unknown or stale state (see [Preconditioning scheduled by Jeedom](#preconditioning-scheduled-by-jeedom)). |
| **Scheduled preconditioning suspended until the next departure: Owner role required for the proxy key** | The vehicle refused **Start climate control**: the proxy key probably has the Charging Manager role. Only one attempt is made per departure. | Pair an **Owner** key (see [Key role](#key-role)); control resumes at the next departure. |
| **Scheduled preconditioning suspended until the next departure: repeated command failures** | Three commands in a row failed (see the command’s error message in the log, warning). | Fix the cause (key, range, proxy); control resumes at the next departure. |
| **Request refused by the vehicle: proxy key not paired with this vehicle** | The proxy’s active key is not paired with this vehicle (with several vehicles, the same key must be paired with each). The other vehicles are not affected. | Use **Pair my key** then **Check pairing** on this vehicle’s equipment. |
| **Request refused by the vehicle — …** | The vehicle refused the read; the proxy’s reason follows the message. | Read the reason given after the message; also check the key pairing. |
| **Function not supported by this proxy — …** | The requested read does not exist in your proxy version (for example the odometer `drive_state` requested from a proxy that refuses it). | Update the proxy (fork proxy for extended data: see [Extended data: what is available](#extended-data-what-is-available)). |
| **Invalid proxy response** | The proxy returned an unexpected response. | Check the address, update the proxy, restart it if it keeps happening. |
| **Proxy version not supported: 2.3.0 minimum, update the proxy** | The proxy is older than 2.1.1: the vehicle state can no longer be read. | Update the proxy (see [Check and update the proxy version](#checking-and-updating-the-proxy-version)). The log also reports this line as an error. |
| **Proxy busy: vehicle read not performed, try again in a moment** | A **Refresh** waited more than 110 seconds: the proxy was busy with a command or a read. No read took place. | Run **Refresh** again in a moment; the next automatic read also catches up. |
| **Refresh with wake-up failed: …** | The **Refresh (with wake-up)** command failed: the cause (vehicle out of range, proxy unreachable, vehicle refusing to wake up…) follows the message. The charge and climate info keep their last value (**Vehicle presence** goes to 0 if the vehicle is out of range). | Read the cause given; move the Raspberry Pi closer to the vehicle if needed, then run again. |
| **Timeout while waking the vehicle: it may have woken up, try again in a moment** | The wake-up and the read exceeded 75 seconds. The vehicle may have woken up anyway. | Run **Refresh (with wake-up)** again in a moment. |
| **The VIN is not configured for this equipment** | The equipment’s VIN is empty. | Enter the VIN in the equipment then save. |
| **Invalid URL: …** | The proxy URL is empty or invalid in the plugin configuration. | Enter it (see [Plugin configuration](#plugin-configuration)). |

The text is truncated to 127 characters. A sleeping vehicle is not an error: see [Refreshing the information](#refreshing-the-information).

### Error when sending a command

These messages are displayed in red in Jeedom and are also copied into **Last error**.

| Message | Cause | Action |
|---|---|---|
| **“This command requires an Owner role key: the proxy key probably has the Charging Manager role…”** | The vehicle refused for lack of rights a command reserved for the Owner role (lock, unlock, horn, lights, Sentry Mode, trunks, climate control): your key very probably has the Charging Manager role. | See [Key role](#key-role): pair an Owner key. |
| **“Command refused by the vehicle (insufficient proxy key role?): …”** | Authorization failure on another command: insufficient key role or vehicle state. | See [Key role](#key-role); with an Owner key, check the vehicle state. |
| **“Command refused by the vehicle: …”** | The vehicle refused the command; the reason returned follows the message. | Fix according to the reason given. |
| **“Proxy unreachable, command not sent”** | The proxy does not respond: the command did not go out. | Check the URL and the Raspberry Pi’s power supply. |
| **“Timeout: the command may have been executed, check the vehicle state”** or **“Connection with the proxy interrupted: the command may have been executed…”** | The vehicle may have executed the command anyway. | Check the vehicle state before sending it again. |
| **“Proxy busy: command not sent, try again in a moment”** | Another command or read has been occupying the proxy for almost 2 minutes. | Try again. |
| **“Trunk already open or moving: command not sent”** | Before opening the rear trunk, the plugin read it as open, ajar or moving: a toggle command might close it. | Nothing to do: close the trunk if needed, then run the action again (see [Open the rear trunk and the frunk](#opening-the-rear-trunk-and-the-frunk)). |
| **“Trunk state unknown: command not sent”** | The vehicle gives no usable state for the rear trunk: the plugin sends nothing as a precaution. | Run **Refresh** then the action; if the state stays unknown, open the trunk by hand. |
| **“Trunk state unreadable, command not sent: …”** | Re-reading the state before opening failed: the cause follows the message. | Fix the cause (proxy, Bluetooth range) and run again. |
| **“Invalid value: the current must be a whole number between … and … A”** | The current is a decimal, text or outside the command’s Min/Max bounds. | Correct the value. The **Max** follows the maximum current reported by the vehicle; to fix it higher, set it by hand (the vehicle may refuse the setpoint). |
| **“Invalid value: the limit must be a whole number between X and Y %”** | Limit outside the command’s bounds (the vehicle’s, or 50 to 100 % until it has published any) or not a whole number. | Correct the value. |
| **“Invalid value: Sentry Mode must be enabled or disabled”** | Value other than **Enabled** or **Disabled** (the former “None” option no longer exists). | Use **Enabled** or **Disabled**. |
| **“Invalid value: the heat level must be a whole number between 0 and 3”** or **“Invalid value: the steering wheel heater must be 0 (off) or 1 (on)”** | A scenario sends a value outside the list of a seat or steering wheel heater command. | Use the levels of the list (see [Heating the seats and the steering wheel](#heating-the-seats-and-the-steering-wheel)). |
| **“Invalid value: max defrost must be 0 (off) or 1 (on)”** | A scenario sends a value outside the list of the **Max defrost** command. | Use 0 (Off) or 1 (On) (see [Max defrost](#max-defrost)). |
| **“Invalid value: the climate keeper mode must be 0 (off), 1 (keep), 2 (dog) or 3 (camp)”** | A scenario sends a value outside the list of the **Climate keeper mode** command. | Use 0 (Off), 1 (Keep), 2 (Dog mode) or 3 (Camp mode) (see [Dog mode, camp mode and climate keeper](#dog-mode-camp-mode-and-climate-keeping)). |
| **“Command failed: …”** | Other cause (proxy without key, vehicle out of range, invalid response…): the cause follows the message. | See the **Last error** table above. |
| **“Not supported by your proxy version”** | The command (for example **Open rear trunk**, **Open frunk**, **Add charge schedule**, **Driver setpoint**, **Set front left seat heater**, **Max defrost** or **Climate keeper mode**) does not exist in your proxy: nothing was sent. | Install the fork proxy (see [Scheduling charging](#scheduling-charging), [Setting the temperature setpoint](#setting-the-temperature-setpoint), [Heating the seats and the steering wheel](#heating-the-seats-and-the-steering-wheel), [Max defrost](#max-defrost) and [Dog mode, camp mode and climate keeper](#dog-mode-camp-mode-and-climate-keeping)). |
| **“Invalid value: the setpoint must be a number between … and … °C”** | The value of **Driver setpoint** or **Passenger setpoint** is not a number, or is outside the slider range (15 to 28 °C, or the vehicle’s bounds). | Send a number within the range given by the message. |
| **“Invalid schedule days: …”** or **“Invalid start time: …”** | The days or the time of **Add charge schedule** do not have the expected format. | Correct them (`lun,mar,mer,jeu,ven`; `23:00`). |
| **“Jeedom coordinates missing or invalid: …”** | Jeedom’s latitude and longitude are not filled in (or are 0 and 0). | Fill them in under Settings, System, Configuration, **General** tab. |
| **“Invalid value: the available power must be a number of watts”** | The value sent to **Adjust to surplus** is not a number (text, empty or unknown variable, failing calculation). | Check the scenario value: a number of watts, for example `1800`; a negative value is brought back to 0 W (see [Surplus control](#surplus-control)). |
| **“Command not supported by the plugin”** | The command is not one of the plugin’s (command added by hand, or modified identifier). | Do not modify the identifier of the plugin’s commands. |

### Refresh cycle task

In **Settings > System > Task engine**, the task **TeslaBLE::cycleRafraichissement** (every minute, 5-minute timeout) runs the vehicle refresh. It is created when the plugin is activated and updated, and put back within the hour if it was deleted; a task you disable yourself stays disabled.

- **No vehicle is refreshed anymore**: check that the task exists and is enabled. If it is missing, **disable then re-enable the plugin** to recreate it. An error message “Tâche de rafraîchissement non installée” *(Refresh task not installed)* in the plugin log signals a creation failure. A message “Tâche de rafraîchissement non supprimée” *(Refresh task not deleted)* when disabling the plugin asks you to delete **TeslaBLE::cycleRafraichissement** by hand in the task engine.
- **Disabling** the plugin deletes the task (otherwise the task engine would log an error every minute); re-enabling it recreates it. Your equipments, commands and settings are not touched.
- **Rolling back to an earlier plugin version** (for example from beta to stable): that version does not know the task and Jeedom’s **cron** log shows a “Classe ou fonction non trouvée” *(Class or function not found)* error every minute. Then delete the task **TeslaBLE::cycleRafraichissement** by hand in the task engine.

### One-off re-read tasks

In **Settings > System > Task engine**, you may see **TeslaBLE::relectureApresCommande** tasks pass by: one per successful command (see [Re-read after a command](#re-read-after-a-command)). They delete themselves once the re-read is done or abandoned; do not touch them. A task left there (Jeedom restarted during the wait) is removed by the next successful command. **Disabling** the plugin removes all these tasks. A message “Tâches de relecture non supprimées” *(Re-read tasks not deleted)* in the log asks you to delete them by hand.

### Wake-up and rate

| Symptom | Cause | Action |
|---|---|---|
| **The vehicle no longer falls asleep** | One of the following keeps it awake: the **Let the vehicle fall asleep** box is unticked; the **Window duration** does not exceed the refresh interval (the window then has no effect); an occupant or a nearby phone key; charging in progress (the window never opens while charging); Sentry Mode; another service querying the vehicle (Tesla app, evcc, another integration); a very short interval; a scenario that runs **Refresh (with wake-up)** or **Wake up** in a loop. | Tick the box, choose a window duration greater than the interval, lengthen the interval, turn off Sentry if possible, check the scenarios. Set the log to **Info**: the line “fenêtre d’endormissement ouverte pour … min” *(sleep window opened for … min)* confirms that the window opens; otherwise one of the criteria above prevents it. The effect on sleep is not guaranteed: it depends on the vehicle. |
| **Charge and climate values do not change overnight** | This is normal: the vehicle is asleep (the plugin does not wake it) or the sleep window is open. **Last data read** stays frozen and **Data age (min)** increases. **Last error** stays at **None**. | Nothing to do. For up-to-date values right away, run **Refresh (with wake-up)** (it wakes the vehicle). If you want permanent reads, untick **Let the vehicle fall asleep**, accepting the impact on the battery. |
| **The value displayed after a command is the old one** | The proxy keeps its data in cache for **30 seconds**: the re-read scheduled after the command waits for this delay. Other causes: the proxy was busy (re-read abandoned, the periodic read catches up), the vehicle fell asleep again (the last values are kept), the proxy cache was lengthened beyond the **Re-read delay after command**, or Jeedom’s task engine is disabled. | Wait 30 seconds. If your proxy’s cache is longer, lengthen the **Re-read delay after command** accordingly. Otherwise run **Refresh** (or **Refresh (with wake-up)** for a sleeping vehicle). See [Re-read after a command](#re-read-after-a-command). |
| **“Refresh with wake-up failed: …”** in **Last error** | The cause (vehicle out of range, proxy unreachable, vehicle refusing to wake up…) follows the message. The values keep their last state. | Read the cause, fix it, run again. See the **Last error** table above. |
| **“Timeout while waking the vehicle: it may have woken up, try again in a moment”** | The wake-up and the read exceeded 75 seconds. | Run **Refresh (with wake-up)** again in a moment. |
| **“Proxy busy: vehicle read not performed, try again in a moment”** | The proxy was busy with a command or a read for more than 110 seconds. | Run **Refresh** (or **Refresh (with wake-up)**) again in a moment. |
| **Data age (min)** is **99999** | No successful data read is known (new equipment, plugin updated, vehicle asleep since installation). | Run **Refresh (with wake-up)** once; the info goes to 0. |
| **The interval while charging is not respected** | The acceleration only starts at the first read that sees the charge; a sleeping vehicle that is charging, a suspended charge or a proxy whose cache exceeds 60 seconds also limit the effect (see [Accelerated reading while charging](#accelerated-read-during-charging)). | Wait for a normal interval, or run **Refresh**. |

The log warnings related to these settings (**Interval while charging** value brought back to 1 minute or disabled, **Re-read delay after command** brought back to 30 seconds, cycle longer than the set interval, refresh or re-read tasks not installed or not deleted) are described in [Plugin log messages](#plugin-log-messages) and [Refresh cycle task](#refresh-cycle-task). The **Info** lines for the opening and end of the sleep window are described in [Let the vehicle fall asleep](#let-the-vehicle-fall-asleep).

### Plugin log messages

- **“Cycle de rafraîchissement sauté : le cycle précédent n'est pas terminé.”** *(Refresh cycle skipped: the previous cycle is not finished.)*: you ran the task by hand (**Settings > System > Task engine**) while a cycle was running. Jeedom itself never relaunches a running task on its own (see the next two messages).
- **“… pilotage selon le surplus : … courant calculé N A, cible M A, décision `…` (motif)”** *(… surplus control: … computed current N A, target M A, decision `…` (reason))* (Debug): the detail of each **Adjust to surplus** call (no VIN); **“appel ignoré, un ajustement est déjà en cours”** *(call ignored, an adjustment is already in progress)*: another call for the same vehicle was not finished. **“pilotage selon le surplus impossible, aucune commande envoyée : …”** *(surplus control impossible, no command sent: …)* (Warning, at most once per hour): internal failure before sending, for example of Jeedom’s cache; the scenario is not interrupted.
- **“… charge aux heures creuses : décision `…` (motif)”** *(… off-peak hours charging: decision `…` (reason))* (Info on reason change, Debug afterwards; no VIN): what the plugin decided after the read (`charge_start`, `charge_stop`, `aucune` or `ignorer`, with the reason: `demarrage`, `cible_atteinte`, `fin_plage`, `en_charge`, `charge_perimee`, `limite_vehicule`, `suspendue_manuel`…). **“commande `…` en échec (N sur 3)”** *(command `…` failed (N of 3))* (Warning on first failure and on suspension); **“commande `…` reportée au prochain passage (proxy occupé | budget du cycle atteint)”** *(command `…` postponed to the next pass (proxy busy | cycle budget reached))* (Warning, at most once per hour): nothing was sent, the plugin tries again at the next read; **“pilotage impossible, aucune commande envoyée : …”** *(control impossible, no command sent: …)* (Warning, at most once per hour): internal failure before sending, for example of Jeedom’s cache.
- **“Cycle de rafraîchissement de N s, plus long que l'intervalle de rafraîchissement le plus court (M min) : Jeedom a sauté le passage suivant…”** *(Refresh cycle of N s, longer than the shortest refresh interval (M min): Jeedom skipped the next pass…)* (Warning, at most once per hour): a cycle lasted longer than the set interval, usually because the proxy or the Raspberry Pi responds slowly; the set rate is not kept. Lengthen the concerned vehicle’s interval (or its interval while charging), spread the vehicles across several proxies, or check the Raspberry Pi’s power supply and Wi-Fi connection.
- **“Cycle de rafraîchissement de N s : Jeedom a sauté le passage de la minute suivante, sans cumul de cycles.”** *(Refresh cycle of N s: Jeedom skipped the next minute’s pass, with no cycle accumulation.)* (Debug): a cycle exceeded one minute while all the set intervals are longer; nothing to do.
- **“Cycle de rafraîchissement écourté… véhicule(s) non lu(s) à ce cycle”** *(Refresh cycle cut short… vehicle(s) not read in this cycle)*: the cycle reached its maximum duration of 4 minutes; the vehicles named were not read in this cycle. They will be at the next cycle if the proxy responds normally; up to 3 vehicles per proxy, the cycle is not cut short, beyond that check the **Last data read** of each vehicle. The warning is only issued **once per episode** (it states “Avertissement non répété jusqu'au prochain cycle complet.” *(Warning not repeated until the next complete cycle.)*), even if the episode lasts several hours; if it keeps happening, the proxy responds too slowly: see above.
- **“Cycle de rafraîchissement de nouveau complet : …”** *(Refresh cycle complete again: …)* (Info): end of a cut-short cycle episode; all vehicles were read.
- **“Véhicule … traité en … s.”** *(Vehicle … processed in … s.)* (Debug): duration of each vehicle’s read in the cycle, including a skipped vehicle (proxy busy, the “skipped” line precedes it) or one in error. The **Requête** *(Request)* and **Réponse HTTP … en … ms** *(HTTP response … in … ms)* lines give the detail of the calls; the Response line repeats its request (method and address), because the lines of several proxies read in parallel are interleaved in the log.
- **“Lecture du véhicule … reportée : proxy occupé…”** *(Read of vehicle … postponed: proxy busy…)*: a **Refresh** waited more than 110 seconds for a proxy busy with a command or a read; the read did not take place and the message **Proxy busy: vehicle read not performed…** appears in **Last error**.
- **“Lecture du véhicule … sautée : une commande ou une lecture est en cours vers le proxy.”** *(Read of vehicle … skipped: a command or a read is in progress to the proxy.)* (Debug): the automatic cycle steps aside for the exchange in progress; the read is done at the next cycle.
- **“Proxy obtenu pour le véhicule … après … s d'attente…”** *(Proxy obtained for vehicle … after … s of waiting…)* (Debug): a command or a read had been waiting for the proxy for at least one second.
- **“Verrou du proxy indisponible…”** *(Proxy lock unavailable…)* or **“Verrou du cycle de rafraîchissement indisponible…”** *(Refresh cycle lock unavailable…)*: the plugin cannot write to Jeedom’s temporary folder. Check the rights on this folder; the plugin keeps working without the protection against simultaneous exchanges.
- **“Commandes : … le nom … est déjà pris…”** *(Commands: … the name … is already taken…)*: the plugin could not give a command its intended label because another command of the equipment has it. Rename one of the two, then save the equipment.
- **“Adaptateur Bluetooth du proxy probablement figé pour le véhicule …”** *(Proxy Bluetooth adapter probably frozen for vehicle …)* (warning) and **“Adaptateur Bluetooth du proxy de nouveau opérationnel pour le véhicule …”** *(Proxy Bluetooth adapter operational again for vehicle …)* (Info): start and end of an episode, see [Frozen Bluetooth adapter alert](#frozen-bluetooth-adapter-alert).
- **“Véhicule … : fenêtre d'endormissement ouverte pour … min après … lecture(s) inchangée(s), hors charge…”** *(Vehicle …: sleep window opened for … min after … unchanged read(s), not charging…)* (Info): the plugin stops reading the charge and climate data until the time indicated; see [Let the vehicle fall asleep](#let-the-vehicle-fall-asleep). **“fin de la fenêtre d'endormissement après … min : …”** *(end of the sleep window after … min: …)* (Info) gives the reason for resuming (activity observed with the changed field, command, refresh requested, setting disabled, time elapsed, vehicle out of range); **“… : véhicule endormi après … min de fenêtre.”** *(…: vehicle asleep after … min of window.)* signals that the vehicle fell asleep. In Debug: “lecture des données suspendue” *(data read suspended)*, “lecture de contrôle” *(check read)*, “prolongée” *(extended)*.
- **“Véhicule … en charge (Charging), intervalle pendant la charge appliqué : N min au lieu de M.”** *(Vehicle … charging (Charging), interval while charging applied: N min instead of M.)* and **“Véhicule … : état de charge …, intervalle normal rétabli : M min.”** *(Vehicle …: charge state …, normal interval restored: M min.)* (Debug): start and end of accelerated reading, see [Accelerated reading while charging](#accelerated-read-during-charging). A **warning** “intervalle pendant la charge inférieur au plancher d'une minute” *(interval while charging below the one-minute floor)* or “… invalide, réglage désactivé” *(… invalid, setting disabled)* signals a value corrected on save.
- **“Véhicule … : relecture programmée dans N s (commande …).”** *(Vehicle …: re-read scheduled in N s (command …).)*, **“… : lecture sans réveil.”** *(…: read without wake-up.)*, **“Relecture du véhicule … remplacée par une commande plus récente.”** *(Re-read of vehicle … replaced by a more recent command.)*, **“… abandonnée : proxy occupé…”** *(… abandoned: proxy busy…)* and **“Relecture ignorée : …”** *(Re-read ignored: …)* (Debug): course of a re-read after a command, see [Re-read after a command](#re-read-after-a-command). Nothing to do.
- **“Véhicule … : relecture non programmée : …”** *(Vehicle …: re-read not scheduled: …)* (warning, at most once per hour): the re-read task could not be created; the command succeeded and the values will be up to date at the next read. If the message comes back, check Jeedom’s task engine.
- **“Équipement … : délai de relecture après commande invalide, ramené à 30 secondes.”** *(Equipment …: invalid re-read delay after command, brought back to 30 seconds.)* (warning): a value outside the list was saved (by a script, an API or a restore); choose a delay from the equipment’s list.
- **“Véhicule … : le proxy annonce désormais … ; information(s) créée(s) : …”** *(Vehicle …: the proxy now announces … ; info(s) created: …)* (Info): after a proxy version change, the plugin created the extended data info that became available (see [Extended data: what is available](#extended-data-what-is-available)). **“… informations de données étendues non créées …, nouvel essai à la prochaine lecture de ces données”** *(… extended data info not created …, new attempt at the next read of this data)* (warning, at most once per hour): creation failed (Jeedom save error); it is retried automatically, or by **Save** on the equipment.
- **“Véhicule … : fonction `donnees:…` refusée par le proxy (not supported), indisponible jusqu'au prochain changement de version du proxy.”** *(Vehicle …: function `donnees:…` refused by the proxy (not supported), unavailable until the next proxy version change.)* (Info): the proxy refused a category it announced; the plugin no longer requests it before a proxy update. **“Capacités du proxy du véhicule … : version …, origine …, action(s) indisponible(s) : …”** *(Proxy capabilities of vehicle …: version …, origin …, unavailable action(s): …)* (Info): reading of what the proxy announces, on version change.
- **“Lecture de la position (ou des pressions des pneus, ou de la mise à jour logicielle) du véhicule … en échec : …”** *(Read of the position (or tire pressures, or software update) of vehicle … failed: …)* (warning, once per episode) and **“… rétablie.”** *(… restored.)* (Info): the vehicle or the proxy refused this read. The other reads are not affected and **Last error** is not modified. In Debug, **“Position (ou Pressions des pneus, ou Mise à jour logicielle) du véhicule … non lue(s) : …”** *(Position (or Tire pressures, or Software update) of vehicle … not read: …)* gives the reason for a read not done (vehicle asleep, out of range, read budget reached, no info on the equipment) and **“Position du véhicule … inchangée : …”** *(Position of vehicle … unchanged: …)* that of an ignored position (stale, 0/0, out of range); no coordinate ever appears in it.
- **“Tuile du véhicule … : rendu impossible, widget standard affiché (…)”** *(Vehicle tile …: rendering impossible, standard widget displayed (…))* (Error): the tile could not be drawn; Jeedom displays the standard widget instead. Note the reason in parentheses; unticking **Widget template** in the **Advanced configuration** removes the message (see [Vehicle tile](#vehicle-tile)).
- **“Image du véhicule … non posée : image du modèle … absente ou illisible dans le plugin (réinstallez le plugin) ; …”** *(Vehicle image … not set: model image … missing or unreadable in the plugin (reinstall the plugin); …)* (Warning): the image file supplied with the plugin is missing or damaged. Reinstall the plugin. **“… non posée : dossier data/eqLogic de Jeedom non accessible en écriture ; …”** *(… not set: Jeedom’s data/eqLogic folder not writable; …)* (Warning): Jeedom cannot write its image; check the rights on Jeedom’s `data/eqLogic` folder. In both cases, the plugin icon (or the current image) stays displayed. **“Image du véhicule … non posée : …”** *(Vehicle image … not set: …)* followed by another reason (Warning): the write failed; the equipment is not modified. **“… retirée : le modèle n'a plus d'image.”** *(… removed: the model no longer has an image.)* (Debug): the VIN now designates a model without an image.
- **“Migrations : …”** *(Migrations: …)*: see [Check the upgrade in the log](#checking-the-upgrade-in-the-log).

### Slow proxy reads

The plugin measures the duration of each read, without any extra request, and publishes it in **State read duration** and **Data read duration**. When a successful read exceeds **10 seconds** (state) or **20 seconds** (data), the log receives **a single** warning **« Lecture lente du proxy pour le véhicule … »** (*slow proxy read for vehicle …*), which is not repeated while the read stays slow. When the duration falls back to **7 seconds** (state) or **14 seconds** (data), an **Info** line « Lecture du proxy redevenue normale… » (*proxy read back to normal…*) reports it. These thresholds are fixed.

Usual causes: Raspberry Pi too far from the vehicle (wall, concrete floor, car parked far away), Raspberry Pi overloaded (another proxy client, such as evcc, keeping it busy) or poorly powered. Move the Raspberry Pi closer or change its power supply, then watch the duration over the following cycles.

A failed read (proxy unreachable, timeout) does not change this information: its duration appears in the failure message in the log (« … après 25.0 s : … », *… after 25.0 s: …*). The duration of a command is written to the log at **Debug** level (« Commande … exécutée en 3.2 s. », *Command … executed in 3.2 s.*).

### Fork proxy: token, adapter, rejected body

| What you see | Cause | Action |
|---|---|---|
| **“API token refused by the proxy”** in **Last error**, or **“API token refused by the proxy: command not sent”** when sending a command | The fork proxy has an `apiToken`, and the plugin has no token or a different one. Vehicle presence is not changed; the log receives **a single** **Error** line per episode. | Enter the exact value of `apiToken` in **Proxy API token**, **Save**, then **Test** (“API token accepted by the proxy”). |
| **“Invalid API token: …”** or **“API token not supported by Jeedom …”** | The token entered contains a character that is not allowed (accent, line break, more than 256 characters), or a form that Jeedom cannot store. | Generate another token (`openssl rand -hex 32`), and enter it in `apiToken` and in the plugin. |
| **Proxy unreachable** while the Raspberry Pi is on | The fork proxy stops at startup if `btAdapter` is invalid or if the adapter does not exist; Docker restarts it in a loop. | On the Raspberry Pi, `docker logs tesla-ble-http-proxy`: look for `Cannot start with this Bluetooth adapter`. Fix or remove `btAdapter` (see [Installing the BLE proxy](installation-proxy.md#12-troubleshooting)). |
| **“Command refused by the vehicle: invalid request body: …”** | The fork proxy rejected the content of the command before sending it. | The text after the colon names the key at fault; report it together with the plugin log in Debug. |

### Proxy Logs window messages

| Message | Cause | Action |
|---|---|---|
| **“Logs unavailable (proxy ≥ 2.3.0 required)”** | The server at the saved URL does not provide logs: proxy older than 2.3.0, or a URL that does not point to the proxy. | Check the URL with the **Test** button, then update the proxy if its version is lower than 2.3.0. |
| **“Proxy unreachable: check that it is running, then its address with the Test button”** | The proxy is stopped, the Raspberry Pi is off, or the address is wrong. | Start the proxy, then check the URL with **Test**. |
| **“Proxy URL missing or invalid: enter it, save, then reopen the logs”** | No valid URL is saved. | Enter the URL, save, then reopen the window. |
| **“API token refused by the proxy”** | The fork proxy has an `apiToken` that the plugin does not send or that differs. | Enter the token (see the table above). |
| Failure message followed by **“HTTP response 500 instead of 200: Failed to encode logs”** | The proxy can no longer read back its own log memory (known proxy defect). | Restart the proxy (`docker compose restart` on the Raspberry Pi). |
| **“No log line on the proxy”** | The proxy has not logged anything yet. | Refresh after a plugin cycle. |

### Advanced charging: symptoms without a message

Set the plugin log to **Debug**: the lines **« pilotage selon le surplus : … décision … (motif) »** (*surplus control: … decision … (reason)*) and **« charge aux heures creuses : décision … (motif) »** (*off-peak hours charging: decision … (reason)*) give the reason for each decision (see [Plugin log messages](#plugin-log-messages)).

| Symptom | Possible causes | Action |
|---|---|---|
| **The charge current does not change** (surplus control) | The target current is identical to the last setpoint, or differs from it by less than the **Hysteresis** (reasons `identique`, `hysteresis`); the **Minimum interval between commands** has not elapsed (counted from the **end** of the previous command); the target current is capped at the **Max** of the **Set charge current** slider (vehicle limit or manually set value); the vehicle is not plugged in, out of range or charging is complete (see **Last error**); **Interval while charging** disabled: the **Charge state** read is old; the **Off-peak hours charging** range is in progress (the call is ignored); **Phases** set to Single-phase with a three-phase charger. | Read the Debug line “decision … (reason)”; reduce the hysteresis or the minimum interval if changes are too infrequent; set **Interval while charging** to 1 minute; check **Grid voltage (V)** and **Phases**; check the slider **Max** in the **Commands** tab. |
| **Charging stops at night** (surplus control) | With no production, the power sent drops to 0 W: the calculated current falls below the **Stop threshold** and charging is stopped after the **Hold time before stopping**. | Normal. To charge at night, use **Off-peak hours charging** (surplus control is then ignored during the range). |
| **Charging does not restart in the morning** (surplus control) | The calculated current does not reach the **Minimum starting current**; starting takes two steps (**Set charge current** then **Start charging**, at the next interval); the vehicle is unplugged or its charge state is unknown; the scenario is no longer scheduled or its freshness guard (**Data age (min)**) is false. | Check the power sent in the Debug line, wait one or two intervals, check the scenario. For an unknown charge state: **Refresh (with wake-up)**. |
| **Off-peak hours charging does not start** | The function is not checked or a field is missing; the current time (**Jeedom time**, not the vehicle's) is outside the range; the vehicle is not plugged in, or the charger supplies no current (see **Last error**); the **Target SoC** is lower than or equal to the current battery level (target already reached); the **vehicle charge limit** is lower than or equal to the current level (charging complete); control is **suspended until the next range** (manual action from Jeedom, charging restarted from the app, 3 command failures, or start already attempted with no charging observed); a sleeping vehicle is only seen with a stale state; the refresh interval is long (the decision is only made on a read). | Check the settings and the Jeedom time zone; read the Info line “off-peak hours charging: decision … (reason)” (for example `suspendue_manuel`, `limite_vehicule`, `cible_atteinte`, `hors_plage`); note **Last error**; run **Refresh (with wake-up)** for a stale state; unplugging then plugging back in restarts control suspended after failures. |
| **A command is refused or ignored** | **Refused**: **“This command requires an Owner role key…”** or **“Command refused by the vehicle (insufficient proxy key role?) …”** (see [Key role](#key-role): surplus control and off-peak hours only require Charging Manager); **“Not supported by your proxy version”** (charge scheduling: fork proxy required); **“Invalid value: …”** (value out of range or not numeric). **Ignored** (no error, no command): abstentions of surplus control or off-peak hours charging (**Last error** gives the reason: vehicle not plugged in, out of range, charging complete, charger without current, unknown charge state) and a call to **Adjust to surplus** during the off-peak hours range. | See the **Last error** and **Error when sending a command** tables above. |

### Climate and comfort: symptoms without a message

Set the plugin log to **Debug**: the line **« préconditionnement planifié : décision … (motif) »** (*scheduled preconditioning: decision … (reason)*) gives the reason for each scheduled preconditioning decision (see [Plugin log messages](#plugin-log-messages)).

| Symptom | Possible causes | Action |
|---|---|---|
| **A comfort command is missing from the widget** (setpoint, seats, steering wheel, max defrost, climate keeper) | These commands are created **hidden**, even with the fork proxy. | Check **Display** on each of them in the equipment **Commands** tab (see [Climate and comfort: what is available](#climate-and-comfort-what-is-available)). |
| **The command is refused immediately with “Not supported by your proxy version”** | The proxy does not advertise it: official proxy 2.3.0, or a fork version that is too old (`2.3.0-tb.1` at minimum for the temperature setpoint, max defrost and climate keeper, `2.3.0-tb.2` for the seats and the steering wheel). | Install or update the fork proxy; no plugin reinstall is needed. Check **Proxy version** then run the command again. |
| **The command is accepted but nothing changes** | **Seat** missing from the vehicle, accepted with no effect (read back as 0); **climate off**: seat heating normally requires it; **auto-heated steering wheel**; **Also read the climate** set to **No, charge only**: the information is not read back and keeps the announced value; the vehicle fell asleep again before the re-read. | Turn the climate on, leave **Also read the climate** on **Yes**, run **Refresh (with wake-up)**, then read the value again (these behaviors are to be validated in real use). |
| **The command is refused with a role message** | Proxy key with the Charging Manager role: the vehicle refuses comfort actions. | Pair an **Owner** key (see [Key role](#key-role)). |
| **Scheduled preconditioning does not start** | Function not checked; departure **day** not checked (the day of the departure time is what counts); **refresh interval** longer than the window duration (no read falls within it); with **Only if plugged in**, vehicle unplugged; climate **already on** (reason `deja_active`); **Also read the climate** set to **No, charge only** (refused on save); vehicle out of range or not read; control **suspended** until the next departure (manual action from Jeedom, 3 command failures, or Charging Manager key: a single attempt per departure). | Check the settings and the Jeedom time zone; reduce the refresh interval (5 minutes at most recommended); read the **Info** line “scheduled preconditioning: decision … (reason)” (for example `hors_fenetre`, `deja_active`, `suspendue_manuel`) and **Last error**; pair an **Owner** key if needed. |
| **The climate starts late or does not stop on time** | The decision is only made on a vehicle read: starting and stopping follow the read rate. A vehicle seen asleep never receives a stop. | Reduce the refresh interval; stop the climate from Jeedom if needed. |
| **A max defrost or a climate keeper does not stop** | The plugin never stops them by itself; scheduled preconditioning neither replaces nor stops them. | Send **Off** from the widget or a scenario. |

The messages displayed for these functions (**Invalid value: …**, **Scheduled preconditioning: …**, **Vehicle not plugged in: scheduled preconditioning not started**, **Not supported by your proxy version**) are described in [Messages on save](#messages-on-save), [“Last error” information (read)](#last-error-info-read) and [Error when sending a command](#error-when-sending-a-command).

### Openings and security: symptoms without a message

Messages of this function: **“Trunk already open or moving…”**, **“Trunk state unknown…”**, **“Trunk state unreadable…”** and **“Not supported by your proxy version”** in [Error when sending a command](#error-when-sending-a-command); the refusal of an alert duration in [Messages on save](#messages-on-save); the alert messages in [Jeedom message center (after an update)](#jeedom-message-center-after-an-update); the role refusal in [Key role](#key-role).

| Symptom | Possible causes | Action |
|---|---|---|
| **An opening stays at 0 although it is open** | The vehicle is asleep: the state is not re-read and the last value remains; an unknown state leaves the last value; proxy older than 2.3.0 (openings not published); the proxy reports openings as closed when the vehicle does not provide them. | Check **Data age (min)** and **Vehicle presence**; run **Refresh**; check **Proxy version** (see [Checking and updating the proxy version](#checking-and-updating-the-proxy-version)). |
| **Sentry in “Last order” does not follow the app** | Official proxy 2.3.0 or a fork that is too old: the value is that of the last Jeedom order. With the fork `2.3.0-tb.2`, a sleeping vehicle also keeps its last read value. | Switch to the fork proxy (`2.3.0-tb.2` at minimum) and run **Refresh (with wake-up)**; see [Sentry Mode state](#sentry-mode-state). |
| **The alert is not sent** | Alert not enabled or duration empty (refused on save); duration not yet elapsed (the alert is sent between the duration and the duration plus two refresh intervals); proxy unreachable, vehicle out of range or read failed (nothing is evaluated); charge port open while the vehicle is plugged in or charging (no alert for the charge port); occupant present or presence unknown (“unlocked with no occupant” alert); Jeedom cache cleared during the episode; scenario that does not test **Openings alert** `== 1`. | Check the **Prolonged opening alerts** block, **Last error** and **Data age (min)**; see [Prolonged opening alerts](#prolonged-opening-alerts). |
| **The alert message is still in the message center** | Jeedom does not remove the message when the opening closes. | Delete it by hand. |
| **No confirmation is displayed before a sensitive action** | The **Confirm action** box is unchecked on the command; the action is launched from a scenario or the API (never a confirmation); the command is not one of the five actions concerned. | Check the box in the command's advanced parameters; see [Confirmation of sensitive actions](#confirmation-of-sensitive-actions). |
| **The trunk does not appear on the widget** | **Open rear trunk** and **Open frunk** are created **hidden**, even with the fork proxy. | Check **Display** in the **Commands** tab (see [Openings and security: what is available](#openings-and-security-what-is-available)). |
| **The rear trunk does not open** | A motorized liftgate that is already open is refused by the plugin so as not to close it; the vehicle refused for lack of rights (**Key role**); official proxy 2.3.0. | Read **Last error** and the displayed message; see [Opening the rear trunk and the frunk](#opening-the-rear-trunk-and-the-frunk). |

### Extended data: symptoms without a message

Messages of this function: the refusal of the home and radius in [Messages on save](#messages-on-save), **“Function not supported by this proxy — …”** in [“Last error” information (read)](#last-error-info-read), the log lines in [Plugin log messages](#plugin-log-messages).

| Symptom | Possible causes | Action |
|---|---|---|
| **Odometer, Gear, Speed, Power, pressures, Software update or position missing** from the **Commands** tab | The proxy does not advertise the category (official proxy 2.3.0, or a fork version that is too old): the information is **not created**. | Check **Proxy version**, install the fork proxy (`2.3.0-tb.2` at minimum), wait one cycle (re-detection) or **Save** the equipment: see [Extended data: what is available](#extended-data-what-is-available). |
| **The information exists but stays empty** | No read has taken place yet: the vehicle is asleep or out of range, or a **sleep window** is open; for pressures, software update and position, less than 15 minutes since the previous attempt. | Run **Refresh (with wake-up)**; check **Data age (min)** and **Vehicle presence**. |
| **The information is no longer updated** after switching to the fork | The proxy refused the category (Info line « refusée par le proxy (not supported) » (*refused by the proxy (not supported)*) in the log); the plugin only asks for it again at the next proxy version change. | Update the fork proxy; a version change restarts the detection. |
| **Odometer frozen** | Vehicle asleep (no read, last value kept) or sleep window open. | Normal. **Refresh (with wake-up)** for an immediate read. |
| **Pressure at 0 or missing** | A zero, negative or greater than 10 bar value is ignored: the information keeps its last value, or stays empty if it has never been read; the vehicle does not report a tire's pressure. | Wait for the next read, with the vehicle awake; check on the vehicle screen. |
| **Speed or Power seem wrong** | Assumed units (mph and kW), unconfirmed; since the proxy is in the garage, these values are almost never meaningful. | Compare with the vehicle screen; do not use them for a critical decision. |
| **Software update shows “Unknown” or a raw label** | An update is active with no version reported by the vehicle (“Unknown”), or the proxy returns a status the plugin does not know (displayed as is). | Nothing to do; the version appears as soon as the vehicle reports it. |
| **Model or Model year are “Unknown”** | The VIN is empty, or is not that of a recognized Tesla, or its 10th character is not a decodable year. | Check the equipment **VIN** and **save**. |
| **At home stays at 0 (or does not appear)** | Before the first calculation, the tile shows 0: the information is **never written** while the home or the position is unknown. No home coordinates entered and no position in Jeedom; position never read (official proxy, vehicle asleep); **Radius (m)** too small. | Enter the **home** and the **radius** in the equipment, or the Jeedom position; wait for a position read (15 minutes at most). See [Position and privacy](#position-and-privacy). |
| **At home stays at 1 although the vehicle has left** | Out of Bluetooth range, no position is read any more: the information keeps its last value. | Combine `At home == 1` with **Vehicle presence** in your scenarios. |
| **The position is not updated** | Vehicle asleep or out of range; position judged too old (more than an hour) or at 0/0, ignored; less than 15 minutes since the previous read; **Latitude** and **Longitude** deleted (only **At home** is still calculated). | Run **Refresh (with wake-up)**; check **Vehicle presence** and **Data age (min)**. |
| **The latitude and longitude appear in a Jeedom log** | The Jeedom `event` log records every new value of an information, even hidden; this is not the plugin log. | See [Position and privacy](#position-and-privacy): lower the `event` log level or delete these two information commands. |
| **I do not see Latitude and Longitude on the widget** | They are created **hidden** and **not historized**, on purpose. | Check **Display** (and **Historize** if needed) in the **Commands** tab. |

### Widget and display: symptoms without a message

Messages of this function: the log lines in [Plugin log messages](#plugin-log-messages).

| Symptom | Possible causes | Action |
|---|---|---|
| **I see the command thumbnails, not the tile** | The **Widget template** box is unchecked (a choice made, or equipment that had a table layout or a custom command widget before the update); the plugin had to fall back to the standard widget (line **Tuile du véhicule … rendu impossible** (*vehicle tile … rendering impossible*) in the log). | Check **Widget template** in the **Advanced configuration**, save and reload the page; see [Restoring the plugin widget](#restoring-the-plugin-widget). |
| **I do not see the vehicle image** | Model without an image (Semi, Roadster, unknown VIN); image removed by you (permanent removal); standard widget (no image); Jeedom image folder not writable or plugin image unreadable (warning in the log). | Check **Model** and the **VIN**; check **Widget template**; upload your image in the **Advanced configuration**. See [Model image](#model-image). |
| **The image does not come back after “Remove image”** | The removal is **permanent**: the plugin never puts it back. | Upload the image of your choice. |
| **Commands are out of order, or a recent command is at the very bottom** | The order is only set at creation and never rewritten; a command added by an update is placed near its theme, or at the end of the list if that theme does not exist on the equipment. | Drag and drop the rows in the **Commands** tab then **Save**; see [Command order](#command-order). |
| **A generic type I had emptied came back** | The command was deleted then recreated, or the setting of types was replayed after an interrupted update. | Set **None** again in the command's advanced configuration; see [Generic types](#generic-types). |
| **A tile button is greyed out** | The matching command does not exist on the equipment, or your proxy does not support it. | Check the **Commands** tab and **Proxy version** (see [Checking and updating the proxy version](#checking-and-updating-the-proxy-version)). |
| **A button stays dimmed** | The command is in progress (a command can take several tens of seconds). It re-arms after 4 minutes at the latest. | Wait; on failure, read the Jeedom message and **Last error**. |
| **The tile shows “Unknown” or “No known read”** | No read has succeeded yet, or the value is not numeric: never an invented value. | Run **Refresh (with wake-up)**; check **Vehicle presence** and **Last error**. |
| **The “Data from … ago” duration does not change while I look at the page** | It is not aged in the browser; it follows **Data age (min)**, recalculated every minute. | Normal: wait for the next minute. |
| **The native mobile app does not show the tile** | The tile only applies to the dashboard and the mobile web interface; the app relies on generic types. | Check the commands' generic types; see [Generic types](#generic-types). |

### Symptoms without a message

- **Proxy reachable is 0 although the proxy is on**: the proxy answers “not found” to the health question if its version is older than 2.1.3, or if the address does not point to the proxy. Check the version and the address with **Test** or **Test this proxy**, then update the proxy (see [Checking and updating the proxy version](#checking-and-updating-the-proxy-version)).
- **Vehicle presence stays at 0**: the proxy does not find the vehicle over Bluetooth. Move the Raspberry Pi closer to the vehicle.
- **Charging information no longer moves although Last error is None**: the vehicle is asleep. This is normal behavior, see [Information refresh](#refreshing-the-information).
- **No request succeeds**: test the URL with the **Test** button (the trailing `/` is handled by the plugin), then from a browser.
- **The dashboard link does not open** although the proxy works: the URL contains a Docker service name that your browser does not know. Open `http://<pi_ip>:8080/dashboard`.
- **The Range graph makes a jump**: normal after updating from 0.x (miles then km), see [Range and charging speed](#range-and-charge-rate).
- **I do not see the outage start and end lines in the log**: set the plugin log to at least **Info** level.
- **The proxy stops responding after a few hours**: this is a frequent problem on the first-generation Raspberry Pi Zero W. Restart the proxy or switch to a Raspberry Pi Zero 2 W. If the proxy still responds but reads time out, the plugin warns you: see [Frozen Bluetooth adapter alert](#frozen-bluetooth-adapter-alert).
- **Intermittent Bluetooth connections**: the vehicle only accepts 3 connected devices at a time; disconnect a phone or a watch.
