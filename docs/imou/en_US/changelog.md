# IMOU plugin changelog

>**IMPORTANT**
>
>If there is no information about the update, it only concerns documentation, translation or text updates.

# 1.0

First complete version, by functional domain:

- **Foundation**: configuration (appId/appSecret/datacenter encrypted), connection test, camera discovery and
  synchronization (customizations preserved, selective synchronization per command).
- **Control**: on/off, monitoring (motion detection), spotlight/light, siren (via the
  IoT "Things" model), PTZ (directional pad + zoom), night vision, image settings
  (flip, WDR, OSD, LED).
- **Video & images**: live stream (live frames), fullscreen display, "camera panel" page,
  camera thumbnail (source of your choice).
- **Alarms & detection**: last event (motion/human), detection sensitivity, arming plans
  (presets), human/AI detection.
- **Device management**: model code display (technical code only), restart, battery monitoring
  & wake-up of dormant devices.
- **Access control**: video doorbell, door opening (compatible hardware).
- **Storage**: SD card status (presence, usage, capacity) + formatting; cloud subscription
  status (read-only, disabled by default — enable if you have an IMOU cloud subscription).
- **Supervision & robustness**: online status / health, error handling and retries,
  call statistics and quota with alert, automatic refresh rate regulation,
  live stream data consumption estimate.

# 0.1

- Initial version (under development).
