# JeeRoborock Changelog

>**IMPORTANT**
>
>If there is no information about an update, it means that update only concerns documentation,
>translation or text changes.

# 10/13/2026

- Added: "Do not disturb" mode controllable from Jeedom when the robot supports it: enabled or not, start and end times of the time window, and three actions "Enable", "Disable" and "Set the time window" (start and end in HH:MM format, usable in scenarios); the display shows what the robot actually saved <!-- UC54 -->
- Documentation: the "Device settings" topic describes the "Do not disturb" mode (French documentation) <!-- UC54 -->
- Added: off-peak charging controllable from Jeedom when the robot supports it: enabled or not, start and end of the time window, and three actions "Enable", "Disable" and "Set the time window" (HH:MM, usable in scenarios); the robot only delays its charging, a requested cleaning is not blocked <!-- UC55 -->
- Documentation: the "Device settings" topic describes off-peak charging (French documentation) <!-- UC55 -->
- Added: robot voice prompt volume shown as a percentage and adjustable from 0 to 100 from Jeedom when the robot supports it: "Volume" information and "Set the volume" slider, usable in scenarios; the displayed value is the one read back from the robot <!-- UC56 -->
- Documentation: the "Device settings" topic describes the volume (French documentation) <!-- UC56 -->
- Added: dock modes shown and adjustable from Jeedom when the dock offers them: "Emptying mode" and "Mop washing mode" information, "Set the emptying mode" and "Set the washing mode" lists, usable in scenarios; the displayed mode is the one read back from the robot <!-- UC57 -->
- Documentation: the "Device settings" topic describes the dock emptying and washing modes (French documentation) <!-- UC57 -->
- Added: cleaning rooms by name and zone cleaning accept a number of passes (1, 2 or 3) in their "Title" field, to go over a room or zone two or three times; with no value, a single pass as before, and the repeat setting of the Roborock app is never changed <!-- UC58 -->
- Documentation: the "Fine control" chapter explains the number of passes for room and zone cleaning, and troubleshooting covers its two refusal messages (French documentation) <!-- UC58 -->
- Added: new "Current room" information: the name of the room the robot is in, deduced from its position on the map, with no extra call to the robot or the cloud; it reads "Aucune pièce" (no room) outside any room and "Pièce inconnue" (unknown room) when the position or the map is not known, and a scenario only triggers on an actual change of room <!-- UC60 -->
- Fix: the map image no longer stays stuck on the old position when the robot returns to its dock shortly after the last read: it is read again within the following minute <!-- UC60 -->
- Documentation: the "Map and rooms" topic describes the "Current room" information, its values and its delay, and troubleshooting covers the case where it stays on "Pièce inconnue" (French documentation) <!-- UC60 -->
- Documentation: new "Commands by model" section (why a command is missing and how to make it appear), input formats for time ranges and number of passes, scenario examples for dock consumables and tanks, child lock, do not disturb, off-peak hours, volume, dock modes, number of passes and current room; known limitations and troubleshooting completed (French page only for now). <!-- UC119 -->
- Added: the "Map" page shows a control panel next to the map: robot choice (remembered in the browser), Total, Room and Zone tabs (rectangle drawn on the map), suction power, water flow and route settings limited to the robot's own values, a large start button then pause, resume, stop and return to dock without leaving the page; a user without execute rights sees everything greyed out, and no extra request is sent to the cloud <!-- UC61 -->
- Documentation: the "Map" panel topic describes the control panel: tabs, settings, buttons, offline robot, rights and how the chosen robot is remembered (French documentation) <!-- UC61 -->
- Added: on the "Map" page, room names are shown on the map and tapping or clicking a room ticks it in the Room tab; no-go zones and virtual walls set in the Roborock app are drawn read-only; the Zone tab rectangle can be moved, resized by a corner and cleared before starting, and it is kept when the map refreshes <!-- UC62 -->
- Documentation: the "Map" panel topic describes the interactive map: room names and room selection on the map, rooms that cannot be chosen or are unknown, movable and resizable zone, read-only no-go zones (French documentation) <!-- UC62 -->
- Added: the "Map" page gets a "Dock and maintenance" tab: empty the bin, wash and dry the mop, set the emptying and washing modes, follow the dock status, the water tanks and consumable wear, with an alert when a part needs replacing or the dock reports a fault; only your robot's features are shown, and an operation already running cannot be started again <!-- UC63 -->
- Documentation: the "Map" panel topic describes the "Dock and maintenance" tab: blocks, robot without a dock, operation in progress, offline robot and rights (French documentation) <!-- UC63 -->
- Added: new "Vacuum then mop" action in the "Map" panel and in scenarios: the robot vacuums only, then goes over the same area again mopping only, on the whole home or the chosen rooms, waits until it is ready again at the dock between the two passes, shows where the sequence stands, can be cancelled at any time and gets its original settings back afterwards; the second pass is never started if the first one was stopped or ended abnormally <!-- UC64 -->
- Documentation: the documentation describes the "Vacuum then mop" action: panel, scenario commands, waiting between passes, cancellation, end reasons and limits (French documentation) <!-- UC64 -->
- Added: the "Map" page gets a "Daily timeline" tab: a per-robot hourly timeline shows what it did (cleaning, returning to the dock, charging, emptying, washing, drying, error, offline), highlights finished cleanings and marks periods without data as "Unknown"; the last 7 days remain available, without using any quota <!-- UC65 -->
- Documentation: the documentation describes the "Daily timeline" tab: legend, "Unknown" periods, highlighted cleanings, navigation, retention and limits (French documentation) <!-- UC65 -->
- Added: panel in the Jeedom mobile app: pick your robot, see the map and start a full or room cleaning from your phone, in light or dark theme; the Station and maintenance page and the day timeline remain desktop-only <!-- UC66 -->
- Documentation: new section on the mobile panel (access, content, missing features) <!-- UC66 -->
- Documentation: manual control: step-by-step guide to clean a room from the panel, rights table (administrator, execute, read-only, no access), new troubleshooting rows (rights, offline robot, room and zone selection, dock, day timeline, mobile panel, cancelling "vacuum then mop"), known limitations completed and new "Updating the plugin" section (French page only for now) <!-- UC129 -->
- Added: welcome message in the Jeedom message center, only once per version, on installation and on each plugin update: installed version, links to the documentation, the Market and the forum topic, and a reminder of the "Assistance" button to report a bug and of the diagnostic report to attach to it <!-- UC67 -->
- Added: the "Assistance" button pre-fills the Community topic with a collapsed "JeeRoborock information" block: daemon and account status, model and firmware of each robot (numbered, without name or identifier), versions, last error and any quota refusal, without any personal data <!-- UC68 -->

# 10/12/2026

- Fix: a robot that is switched off, out of battery or off Wi-Fi no longer prevents controlling the other robots of the account: it shows as offline, its reconnection attempts no longer use the Roborock quota, and it becomes controllable again on its own within 6 minutes of coming back. <!-- UC44 -->
- Documentation: new "Several robots on the same account" topic in "Real time and freshness" (French documentation). <!-- UC44 -->
- Fix: changing the suction power, water flow, mop route or cleaning mode no longer wrongly reports "not applied" when the robot, for example on its dock, takes the setting a few seconds later: the plugin now gives it up to about twelve seconds before concluding, without slowing down the answer when the setting is taken immediately. <!-- UC45 -->
- Documentation: the "Fine control" topic explains how settings are checked after sending, and the "not applied" troubleshooting entry is clarified (French documentation). <!-- UC45 -->
- Fix: a cleaning order (Start, room or zone cleaning, from the dashboard as well as from a scenario) sent while the dock is emptying the dust bin is no longer reported as sent while the robot ignores it: it is refused with a message asking you to try again once emptying is over <!-- UC46 -->
- Documentation: the "Status and basic control" section and the troubleshooting table explain why a cleaning order is refused while the bin is being emptied <!-- UC46 -->
- Fix: the "last cleaning" commands once again update by themselves after each cleaning, usually within a few minutes: if the robot has not recorded the cleaning yet or does not answer (mop washing, bin emptying), the plugin reads its log again up to five times over 30 minutes, without using any Roborock quota. <!-- UC47 -->
- Documentation: "Cleaning log" section: timing of the automatic update of the last cleaning (French documentation). <!-- UC47 -->
- Fix: map names sent encoded by some robots (S7: "%20" instead of spaces, "%E9" instead of "é") are now displayed in plain text; for a robot already configured, click "Refresh map list" once in the Equipment tab. <!-- UC48 -->
- Change: the plugin page now states the GPL v3 or later licence (official text included) and requires Jeedom 4.4.7 or later, the first version that installs the plugin's Python dependencies in a dedicated environment; on Jeedom 4.4, the robot tile is shown with the plugin icon. <!-- UC50 -->
- Documentation: minimum Jeedom version (4.4.7) and licence (GPL v3 or later), offline robot when several robots are on the account, settings confirmed after a short delay, cleaning order refused while the bin is being emptied, automatic update of the last cleaning, map names shown in plain text; known limitations and troubleshooting completed. <!-- UC109 -->
- Added: dock consumables now appear as remaining wear percentage (station filter, cleaning brush, dust bag, depending on the dock); the filter and the brush can be reset after confirmation, the dust bag is read-only <!-- UC51 -->
- Documentation: the "Docking station, consumables and maintenance" topic describes the dock consumables (French documentation) <!-- UC51 -->
- Added: three yes/no information commands usable in scenarios, created only if the robot and its dock support them: "Clean water tank empty", "Dirty water tank full or missing" and "Mop installed" <!-- UC52 -->
- Documentation: the "Docking station, consumables and maintenance" topic describes the state of the water tanks and of the mop (French documentation) <!-- UC52 -->
- Added: child lock controllable from Jeedom when the robot supports it: a yes/no "Child lock" information usable in scenarios and two actions "Enable child lock" / "Disable child lock", the displayed state being the one read back from the robot <!-- UC53 -->
- Documentation: the new "Device settings" topic describes the child lock (French documentation) <!-- UC53 -->

# 10/01/2026

- Fix: the "Synchronize routines" button on the Device tab no longer does nothing: clicking it starts the synchronization again, and the device is then redisplayed on its own when routines have been added or removed. <!-- UC35 -->

# 09/29/2026

- Fix: cleaning a room (a room's "Clean" button or clean-by-name command) no longer ends with "Internal daemon error": it is sent to the robot again. If a requested room is not recognised, the plugin now suggests resynchronising the rooms. <!-- UC24 -->

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
