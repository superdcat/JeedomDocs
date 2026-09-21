# IMOU Plugin

The **IMOU** plugin controls your IMOU cameras from Jeedom via the **IMOU Open API** (cloud), **in native PHP**
(no daemon, no Python). Depending on each camera's capabilities: on/off, monitoring, PTZ,
spotlight/siren, night vision, image settings, live stream, thumbnail, restart, battery, doorbell
& door opening, alarm reporting, SD card and cloud subscription status, supervision.

> The IMOU API does not offer real-time notifications: the camera state is refreshed by
> **periodic polling**. A change made from the IMOU application may therefore take
> a few minutes to appear in Jeedom.

## Requirements

- An **IMOU developer account** on [open.imoulife.com](https://open.imoulife.com).
- An application created in the developer console, providing an **`appId`** and an **`appSecret`**, with
  the integration mode **`accessType = PaaS`** (required to control devices).
- Your cameras already linked to this account via the **IMOU Life** application.
- **`ffmpeg`**: installed **automatically** by Jeedom when the plugin is activated (tab "Dependencies").
  It is used to extract frames from the live stream. On a Docker installation, verify that `ffmpeg` is
  available in the image.

> ℹ️ **Number of controllable devices (free tier).** In theory, the free IMOU developer account is limited
> to **~5 devices**: beyond that, commands *should* fail with a **licence error** returned by IMOU (this is
> not a plugin limitation). **In practice, IMOU appears to allow controlling more cameras** on the free tier
> — in our tests, everything works normally beyond 5. This behaviour depends on IMOU and may change without
> notice: if a command eventually returns a licence error, this limit is what applies, and an appropriate
> IMOU plan is then required. Either way, the cameras are still discovered and displayed; only their commands
> would be affected.

## Plugin configuration

1. Enable the plugin (Plugins → Plugin management → IMOU) and let Jeedom install the dependencies.
2. In the plugin configuration, fill in:
   - **App ID**: the identifier of your IMOU application;
   - **App Secret**: the associated secret (**stored encrypted**, never displayed in plain text);
   - **Datacenter**: the region of your account (Europe by default).
3. Click **Test connection** to validate your credentials.

### Advanced settings (optional)

- **API call quota**: `quotaMensuel` (monthly API call limit, ~30,000 on the free tier),
  alert threshold. The quota resets **on the 1st of each month**. The plugin **counts its calls** and
  alerts you when approaching the limit.
- **Automatic rate regulation**: `refreshIntervalMin`/`refreshIntervalMax` bounds. The plugin
  automatically adjusts the refresh frequency to stay within the monthly call budget.
- **Concurrent live streams**: `liveMaxConcurrent` (number of live streams displayed simultaneously).
- **Data consumption estimate**: `dataQuotaGo` / `dataBitrateKbps` (see "Quota & supervision").

## Adding cameras

- Click **Synchronize**: the plugin retrieves the account's cameras and creates **one device per
  camera** (one per channel for multi-channel devices).
- Rename and organize the devices in your objects as usual: **your customizations are
  preserved** during subsequent synchronizations.
- **Selective synchronization**: each status command can be excluded from automatic refresh
  (checkbox "Exclude from automatic refresh"), to save calls on what you do not need.

> 💡 **Commands are conditional on the camera's capabilities.** The plugin only creates commands
> actually supported by each model. If a command (PTZ, siren, night vision, SD card…)
> **does not appear**, it means your camera does not declare that capability — this is **normal**, not a bug.

## Available commands (depending on the camera)

- **On / Off** the camera.
- **Monitoring** (motion detection): enable / disable.
- **Spotlight / light** and **siren** (on compatible models, via the IoT "Things" model).
- **PTZ**: directional pad (up/down/left/right) and zoom on motorized cameras.
- **Night vision**: mode (auto / infrared / colour depending on the model).
- **Image settings**: flip, WDR, date/time overlay (OSD), LED indicator…
- **Live stream**: refreshed live image, **viewable fullscreen** with a click.
- **Thumbnail** of the camera (source of your choice: live snapshot or cover image).
- **Model (code)**: technical code of the camera, displayed as a **read-only field** in the
  device configuration (next to the identifier), not as a command.
- **Restart** the device (action protected by confirmation).
- **Battery & wake-up**: battery level (reported in Jeedom's Health supervision); dormant devices
  are woken up to read their state.
- **Video doorbell & door opening** (on compatible locks/doorbells; opening protected by
  confirmation).
- **Alarms & detection**: last event (motion/human), detection **sensitivity**, **arming plans**
  (day/night/always-on presets), **human / AI detection**.
- **SD card**: presence, usage, capacity, and **formatting** (action protected by confirmation).
- **Cloud recording**: subscription status (active, expiry, plan). **Disabled by default**
  (option to enable if you have a subscription — see below).
- **Online (state)**: camera reachability, also used to save calls (an offline camera is not polled).

### Enabling cloud subscription monitoring

The cloud commands are created **hidden and not polled** by default (most accounts have no
subscription). If you have a cloud subscription: make the **Cloud active** command visible and
uncheck its "Exclude from automatic refresh" box to enable monitoring (checked once per hour).

## The "camera wall" panel

The plugin adds a **dedicated page** to the Jeedom menu displaying a grid of live streams from your cameras (with
PTZ, siren, spotlight depending on the models). Enable it in **plugin management** (checkbox "Display desktop panel"),
then choose per camera whether it appears on the wall (checkbox "Visible on camera panel" of the device).

## Refresh, quota & supervision

The plugin periodically polls the IMOU cloud (cron). Two **separate** budgets to be aware of:

- **API CALL quota** (~30,000/month on the free tier): **counted exactly** by the plugin. The
  refresh rate is **automatically regulated** to stay within this budget, and an alert is raised
  when approaching the limit. "Slow" states (SD card, cloud subscription) are refreshed at
  low frequency (once per hour) — and cloud subscription is only polled if you have enabled it
  (see "Enabling cloud subscription monitoring").
- **DATA quota** (live stream volume, ~3 GB/month on the free tier): the plugin provides an
  **estimate** (viewing time × configured bitrate `dataBitrateKbps`, compared against `dataQuotaGo`).
  This is an **informational indicator**: the **actual** value is shown in the **IMOU developer portal**,
  which is the authoritative source. The IMOU API does not expose actual data consumption.

The plugin's **Health** screen summarizes camera reachability, the call quota, the regulated refresh rate, and
the data consumption estimate.

## Privacy & data location

**Video streams** and **commands** transit through **IMOU cloud servers** (datacenter according to your
region — choose "Europe" for France). **No video transits through Jeedom**: the plugin sends
control commands and receives state metadata as well as frames extracted from the live stream.

## Troubleshooting

- **Synchronization finds no cameras** → check `appId`/`appSecret`/`Datacenter`, the
  **Test connection** button, and that your cameras are properly linked to the account in the IMOU Life application.
- **A command does not exist on my camera** → the capability is not supported by this model. This is normal.
- **The live stream is not displayed** → check that the plugin **dependencies** are installed (`ffmpeg`),
  that the camera is online, then consult the `imou` logs at *debug* level.
- **Commands fail with a licence error** → you may be reaching the controllable-device limit of the IMOU
  free tier (in theory ~5, though IMOU often allows more in practice; see Requirements). An appropriate IMOU
  plan is then required — this is not a plugin limitation.
- **"Clock out of sync" / signature error** → synchronize the Jeedom server clock (NTP):
  a drift of more than 5 minutes causes IMOU to reject requests.
- **A change made in the IMOU app does not appear immediately** → normal, refresh is
  periodic (no real-time notification).

## Known limitations

- **No real-time alarms (push)**: events are reported by periodic polling, not
  by instant notification.
- **No recording playback**: the IMOU API does not expose playback URLs for recorded videos
  (SD or cloud); playback is done in the IMOU application.
- **No commercial model name**: only the technical model code is displayed (there is no reliable
  code → commercial name mapping database).
- **Detection zones, firmware updates, device association/renaming on the IMOU side**: not managed.

## Uninstalling

Disabling then removing the plugin in Jeedom removes the devices and their commands. Your
**IMOU credentials** (`appId`/`appSecret`) remain **valid** on your IMOU developer account and can
be reused; they are not deleted on the IMOU side by this operation.
