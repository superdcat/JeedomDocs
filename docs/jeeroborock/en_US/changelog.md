# JeeRoborock Changelog

>**IMPORTANT**
>
>If there is no information about an update, it means that update only concerns documentation,
>translation or text changes.

The plugin is in version **0.x**. It is developed and tested on a **Roborock Qrevo Curv**
(V1 protocol): the features below are operational on this hardware, and should be on other V1 robots
on the account, since each command is only created if the robot reports the matching capability.

The plugin respects the **Roborock cloud quotas**, shared with the mobile app: robot discovery and
synchronizations (usages, rooms, maps) happen **on demand**, and no connection attempt is retried
automatically.

## What is functional

**Account and installation**

- Installation of the `python-roborock` dependency and dedicated daemon, with monitoring of its state.
- Authentication to the Roborock cloud via a **one-time code received by e-mail**: no password is
  requested or stored.
- "Test the connection" button, account status shown on the configuration page, and an explicit
  "re-authentication required" message when the session is lost.

**Devices and states**

- Discovery of the account's robots and creation of one device per robot, illustrated with the model's
  photo. A robot never corresponds to more than one Jeedom device: any duplication attempt is refused
  with an explicit message.
- Information reported: status, battery, cleaning, error (label and code), area cleaned, cleaning
  duration, progress, online, connected, last update.
- Dock: dust emptying, mop washing, mop drying, dock error, water shortage.
- Consumables: remaining wear in % for the main brush, side brush, filter, sensors and mop roller.
- Common settings, read-only: suction power, water flow, mop route, cleaning mode.
- **Real-time** update by the daemon (30 s while cleaning, 60 s at rest), and switch to "disconnected"
  if the data grows stale.
- Dashboard tile (desktop and mobile) combining photo, status, battery and control actions.

**Control**

- Basic actions: Start, Pause, Stop, Return to base, Locate, Refresh.
- Routines ("usages") defined in the mobile app: one action command per usage, managed from the
  "Routines" panel of the Device tab (list of known usages, synchronization on demand).
- Settings: suction power, water flow, mop route, cleaning mode.
- Dock maintenance: wash the mop, dry it, stop drying, empty the bin.
- Room cleaning (one command per room, plus a generic command by names), rectangular zone cleaning and
  moving to a point.
- Resetting the wear counter of each consumable, with confirmation.

**Map**

- Inventory of named rooms and stored maps (floors), changing the active map, from the Device tab. A
  floor change made from the mobile app is also tracked automatically, with no action from you.
- "Map" panel (**Home** menu) accessible to non-administrator users: map image, date of the
  last update, room legend, automatic refresh.

**Log, statistics and schedules**

- Last cleaning (start, duration, area, end reason, error) and a history panel of the last 10 cleanings,
  with a refresh button.
- Four cumulative counters historized by default: total duration, total area, number of cleanings,
  number of bin empties.
- Schedules created in the mobile app, viewable read-only from the Device tab.

**Documentation**

- Complete plugin help page: installation, account linking, devices and commands, usages, map, fine
  control, re-authentication, quotas and troubleshooting guide.
  Available in French, English, German and Spanish.

**Diagnostics and support**

- Diagnostic report generated in one click from the plugin configuration, with no sensitive data, to
  copy or download for a support request.

## What is not planned

The plugin does not display the channel used to reach each robot (local connection or cloud), and does
not track or update the firmware: these two features have been set aside. Firmware updates are done
from the Roborock app.

# 09/24/2026

- Fix: the diagnostic report once again includes the technical section provided by the daemon: it no longer shows "Daemon diagnostics unavailable: partial report" when the daemon is running. The log level and the robot's error history are also correctly filled in. <!-- UC30 -->

# 09/23/2026

- Fix: the "Start" button now resumes a paused cleaning instead of restarting a full cycle, including
  for room or zone cleaning.
- Fix: an expired Roborock session is now also recognized during usage synchronization, usage
  execution, room reading and the connection test: the plugin shows "re-authentication required"
  instead of a generic error. <!-- UC36 -->
- Added: a new diagnostic report in the plugin configuration: daemon, account and robot status,
  python-roborock version and recent errors, with no identifier, token, serial number or e-mail
  address, to copy or download in one click. <!-- UC30 -->
- Documentation: the plugin documentation explains how to generate and send a diagnostic report for a
  support request. <!-- UC30 -->
- Documentation: the documentation clarifies that the plugin remains dependent on the Roborock cloud
  even when a local connection to the robot is attempted, states what to include with a help request
  and what should never be published, and completes the troubleshooting guide for the diagnostic
  report. <!-- UC59 -->
- Change: usages now have their own "Routines" panel in the robot's Device tab: list of known usages, a
  synchronization button and the rule shown before the click; a usage deleted in the Roborock app is
  now deleted from Jeedom instead of being marked obsolete, and the report names it. <!-- UC35 -->
- Fix: a usage name customized in Jeedom is no longer overwritten by the Roborock app's name at the
  second synchronization. <!-- UC35 -->
- Documentation: the usages section was rewritten ("Routines" panel, synchronization rule, cases where
  nothing is deleted). <!-- UC35 -->
- Usage documentation completed: when to run their synchronization, what it costs (no quota), what
  happens on failure, and a reminder that the device synchronization button does not synchronize
  usages. <!-- UC89 -->
- Fix: a floor change made from the Roborock mobile app is now detected by Jeedom within a minute: the
  active map is updated, and the room list, image and coordinate frame of the old floor are invalidated
  just as with a change made from Jeedom. <!-- UC38 -->
- Documentation: the documentation describes the automatic tracking of a floor change made from the
  mobile app and its remaining limitations. <!-- UC38 -->
- Fix: the name of a room command containing an apostrophe, an ampersand, a hash sign or a percent sign
  now follows renamings made in the Roborock app, while keeping a customized name in Jeedom. <!-- UC39 -->
- Fix: a robot can no longer be linked to two Jeedom devices: the "Duplicate" button is removed and any
  attempt is refused with a message naming the existing device. <!-- UC39 -->
- Fix: long, accented names for rooms, usages, maps and robots are no longer cut in the middle of a
  character. <!-- UC39 -->
- Documentation: the documentation clarifies that a robot corresponds to a single Jeedom device and that
  room command names follow renamings made in the app. <!-- UC39 -->
- Fix: the "Online" indicator now truly follows the robot's connection loss and recovery, an unknown
  dock error now shows as "Erreur de station non reconnue" (Unrecognized dock error) instead of
  "Aucune" (None), and fields not pushed by the robot (dock, area, progress) no longer stay frozen
  when the robot sends many updates. <!-- UC40 -->
- Documentation: the documentation now distinguishes the "Online" and "Connected" indicators and
  mentions the "Erreur de station non reconnue" (Unrecognized dock error) label. <!-- UC40 -->
- Change: internal hardening: the plugin refuses an abnormally large update coming from its daemon, the
  configuration form's source file is no longer accessible over the web, the daemon reports at startup
  an unvalidated version of the map-rendering library or an unthrottled Roborock library logger, and the
  sample window inherited from the plugin template is removed. <!-- UC41 -->
- Fix: two close clicks (or two tabs) on the same synchronization button — usages, rooms, maps, map
  image, log, schedules — no longer both go through: the second is refused with the usual "request too
  soon" message. <!-- UC42 -->
- Documentation: known limitations are completed (unreadable map with local connection only, rooms
  readable only when the robot is online, map view not refreshed at rest, no map view on mobile, tile
  commands that are unhidden are never hidden again, error history logging re-enabled after an old
  update), troubleshooting now covers a partial usage synchronization failure, and the feature summary
  mentions the "Routines" panel and tracking of a floor change made on mobile. <!-- UC99 -->
- Documentation: the help page and changelog are now available in English, German and Spanish. <!-- UC99 -->
- Fix: robot tile: the notice of a consumable to replace now states which one (main brush, filter, sensors…). <!-- UC15 -->

# 09/22/2026

- Change: on the plugin's configuration page, the login code field now sits right under the e-mail
  address, before the account status, in the order the procedure actually happens. <!-- UC04 -->
- Change: a reminder states that the configuration must be saved after entering the e-mail, before
  requesting a code. <!-- UC04 -->
- Documentation: complete plugin help page — installation, linking the Roborock account by e-mail code,
  devices and commands, usages, dashboard tile, map and rooms, fine control, real time,
  re-authentication, Roborock quotas and troubleshooting guide. <!-- UC49 -->
- Added: the last cleaning (start, duration, area, end reason and any error) is now reported on the
  device, with a history of the last 10 cleanings viewable from the robot's page and a button to refresh
  it. <!-- UC26 -->
- Documentation: the plugin documentation describes the cleaning log: the information reported, the
  history panel and the refresh button's rule. <!-- UC26 -->
- Added: four cumulative statistics per robot (total cleaning duration, total area cleaned, number of
  cleanings, number of bin empties), historized by default to track their evolution over time. <!-- UC27 -->
- Documentation: the plugin documentation describes the cumulative statistics: the four counters, their
  default history logging and behavior after a reset from the Roborock app. <!-- UC27 -->
- Added: cleaning schedules defined in the Roborock app can be viewed from Jeedom, read-only: recurrence
  and active/inactive status of each. <!-- UC28 -->
- Documentation: the help page's troubleshooting guide now covers every message that requires an action
  from you: account not linked, rejected e-mail address, timeout exceeded, robot busy, setting
  unavailable on the robot, and map change too soon. <!-- UC49 -->

# 09/21/2026

**Documentation**

- The documentation and changelog are published at
  [jeedomdocs.decastro.fr/jeeroborock](https://jeedomdocs.decastro.fr/jeeroborock/).
- Single changelog for all versions: the "beta" changelog is removed.

**Map and rooms**

- Inventory of the account's **named rooms**, matched to the robot's segments, in a "Rooms" panel of
  the Device tab.
- **Multiple maps (floors)**: list of stored maps, active map and map change. Changing the map
  invalidates the room list and the image, which are then resynchronized.
- **Map image** retrieved and automatically refreshed by the daemon.
- New **"Map"** panel (Home menu), the plugin's first surface accessible to non-administrator
  users: map image, timestamp, room legend and refresh every 30 seconds. The image is no longer served
  by direct URL: every access checks the user's rights on the device.

**Fine control**

- **Suction power**: information and setting command, limited to the levels actually supported by the
  robot.
- Mop **water flow**: information and setting command.
- **Mop route** and **cleaning mode** (vacuum only, mop only, vacuum and mop): information and setting
  commands.
- **Dock maintenance**: "Wash the mop", "Dry the mop", "Stop drying", "Empty the dust bin". These actions are
  only created if the dock supports them, and are refused with a clear message if the robot is not at
  its dock.
- **Room cleaning**: one command per room in the home, plus a generic "Clean rooms (names separated by
  commas)" command. The commands follow room renamings made in the mobile app.
- **Zone cleaning** (x1,y1,x2,y2 in mm) and **moving to a point** (x,y in mm), with coordinate
  validation before sending to the robot.

**Visual identity**

- Plugin icon derived from the Roborock logo.

# 09/20/2026

- **Detailed errors**: error label in French, associated code, "Aucune" (None) value when the robot
  reports nothing, and error history logging. An error unknown to the library is no longer shown as
  "no error."
- Robot **dashboard tile** (desktop and mobile): photo, status, battery gauge and the five control
  actions, with no cloud call when displayed. The commands absorbed by the tile are hidden but remain
  runnable from scenarios, views and designs.
- **Robot photo** as the device's illustration (device list and configuration page).
- Fixes to event reporting.

# 09/19/2026

- **Real time**: the daemon carries the refresh cadence (30 s while cleaning, 60 s at rest) and
  receives updates pushed by the robot. The Jeedom cron becomes a freshness watchdog and switches the
  robot to "disconnected" beyond 3 minutes without data.
- **Robustness and re-authentication**: explicit, persistent "re-authentication required" state,
  progressive backoff on probes and on daemon restarts, and hardened logging (no secrets in logs, at
  any log level).
- **Consumables**: remaining wear in % for the five consumables actually reported by the robot, and a
  reset action per consumable.
- **Dock status**: dust emptying, mop washing, mop drying, dock error and associated code, water
  shortage. This information is only created if the dock exposes it.
- Daemon fixes: startup, sending the code by e-mail, adding a device.

# 09/18/2026

- **PHP-to-daemon bridge**: single local channel, with French translation of the daemon's error codes.
- **Authentication** to the Roborock cloud via a one-time code received by e-mail.
- **"Test the connection"** button and account status display on the plugin's configuration page.
- **Discovery of the account's robots** and creation of one device per robot.
- **Information commands**: status, battery, cleaning, error, area cleaned, cleaning duration,
  progress, online, connected, last update.
- **Action commands**: Start, Pause, Stop, Return to base, Locate, Refresh.
- **Routines ("usages")**: synchronization of usages defined in the mobile app and one action command
  per usage. They go through the Roborock cloud, so they work even when the robot is not directly
  reachable.

# 09/17/2026

- First version: plugin configuration page (Roborock account e-mail, local daemon channel port),
  installation of the `python-roborock` dependency and daemon lifecycle.
