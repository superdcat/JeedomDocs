# JeeRoborock

JeeRoborock controls your Roborock robot vacuums from Jeedom, through the Roborock cloud: real-time
status, cleaning commands, fine-grained control (suction, water, route, dock maintenance), room or
zone cleaning, multiple maps, and running the routines ("usages") defined in the Roborock mobile app.

## What the plugin does, and what it does not

- Control goes through the **Roborock cloud**: Jeedom must have Internet access, and your robot must
  be connected to your network and to the Roborock cloud in order to respond. Some operations strictly
  depend on the cloud and **do not work without Internet**: linking the account, the robot inventory,
  running routines, reading schedules, and retrieving the robot photo.
- The library used by the plugin **may**, when your robot is on the same local network as Jeedom, try
  a direct connection to the device to speed up some exchanges. This behavior is neither adjustable
  nor switchable from Jeedom, and it changes nothing about the points above: the plugin remains
  dependent on the Roborock cloud to work.
- The plugin targets robots compatible with Roborock's **V1** protocol. The reference hardware, on
  which everything is tested, is the **Roborock Qrevo Curv**. Other V1 robots may work, but their
  available commands vary according to the capabilities the robot itself reports — see below.
- A robot **shared** with you by another Roborock account normally appears in the list, but some
  actions may be refused for it by the Roborock cloud.

## Requirements and installation

1. **Jeedom 4.2 minimum**, installed on a server running **Debian 12 or 13**. This Debian version is
   required for the plugin's dependency to work; below that (Debian 11, for example), activating the
   plugin is refused.
2. From the plugin page, let Jeedom install its Python dependency. The dependency indicator on the
   "Plugins" page turns green once installation is complete; expect up to about fifteen minutes
   depending on the machine.
3. **Enable the plugin** then start its daemon (the interface does this automatically on activation).
   Without a running daemon, the plugin can neither connect to Roborock nor read a robot's status: the
   configuration page shows this as "The daemon is not responding."

## Linking your Roborock account

Authentication uses a **one-time code sent by e-mail**: there is no password field, and your Roborock
account password is never requested nor stored.

From the plugin's configuration page (menu Plugins > JeeRoborock > Configuration):

1. Enter your Roborock account **e-mail address** in the "Roborock account e-mail" field.
2. **Save the configuration** (the page's save button) before requesting a code: it is this saved
   value that the daemon uses.
3. Click **"Send a code"**. Roborock sends you a numeric code by e-mail (up to 12 characters).
4. Enter this code in the field provided and click **"Validate the code"**.
5. The account status changes from "Roborock account not linked" to "Roborock account linked".

A **"Test the connection"** button lets you check at any time that the saved session is still valid,
without using up your connection quota.

What the plugin keeps: your e-mail address and an encrypted session token (issued by Roborock when the
code is validated). Your account password, the keys specific to each robot and the raw session tokens
never leave the daemon and are never visible from the Jeedom interface.

### Local channel with the daemon

The **"Local channel port"** field (61350 by default) is the TCP port used on the Jeedom machine
itself to talk to the daemon. Only change it if there is a conflict with other software installed on
the same server. The **"Check the channel"** button confirms that the daemon is responding and that
the return channel to Jeedom (spontaneous updates) works.

## Device synchronization

The **"Synchronize devices"** button, on the plugin's home page, queries your Roborock account to
discover your robots and create the corresponding Jeedom devices.

This is **not** a refresh button: the inventory of robots linked to your account is subject to a
strictly limited Roborock quota shared with the mobile app (see below). Only click this button when
you add or remove a robot from your Roborock account, not to refresh the status of an already-known
robot — that status updates itself (see "Real time and freshness").

A robot shared by another account is marked with a **"Shared robot"** label on its card, in the device
list.

This button does **not** synchronize routines: a freshly discovered robot has none yet. Routines are
synchronized robot by robot, from the **"Routines"** panel of the "Device" tab (the "Synchronize
routines" button, see "Routines (\"usages\")" below).

A robot never corresponds to more than **one Jeedom device**: the configuration page of a JeeRoborock
device does not offer the native "Duplicate" button, and any attempt to create a second device for an
already-known robot (including via a route other than the interface, such as the API) is refused, with
a message naming the existing device. If a duplicate was created before this protection existed, it is
not automatically deleted: it is up to you to delete whichever of the two is no longer needed, with a
warning written to the plugin's log to help you spot it.

## What a device contains

Each robot becomes a Jeedom device. The list of commands it carries **depends on the capabilities the
robot actually reports**: two robots, even of similar models, do not necessarily have exactly the same
list. A missing command means a capability not detected on that robot, not a plugin defect.

### General information

The "Device" tab shows, read-only, the model, firmware, protocol version, serial number, Roborock
identifier and the name given to the robot in the Roborock app. This information comes from the
Roborock account and is updated by device synchronization.

### Status and basic control

| Command | What it indicates or does |
|---|---|
| État (Status) | The robot's current status label (cleaning, paused, in error…) |
| Batterie (Battery) | Charge level in % |
| En nettoyage (Cleaning) | Yes/no |
| Erreur (Error) | Label of the current error, "Aucune" (None) otherwise |
| Surface nettoyée (Area cleaned) | In m², for the ongoing cleaning |
| Durée de nettoyage (Cleaning duration) | In minutes, for the ongoing cleaning |
| Avancement (Progress) | In %, for the ongoing cleaning |
| En ligne / Connecté (Online / Connected) | "Online": the robot answered the last poll (switches to "Offline" as soon as a poll fails to get a response from the robot). "Connected": data freshness on the plugin side (channel with the daemon) |
| Dernière mise à jour (Last update) | Date and time of the last data received |
| Démarrer / Mettre en pause / Arrêter (Start / Pause / Stop) | Cleaning control. "Start" **resumes** a paused or interrupted cleaning (including a room or zone cleaning) rather than starting a new one; with no cleaning in progress, it starts a full cleaning |
| Retour à la base (Return to base) | Sends the robot to recharge |
| Localiser (Locate) | Makes the robot emit a sound signal |
| Rafraîchir (Refresh) | Immediately re-reads the robot's status |

### Dock, consumables and maintenance

These commands only appear **if your dock supports them**:

- dust emptying, mop washing and mop drying status, dock error, water shortage. If the error code
  reported by the dock is not recognized, the label shown is "Erreur de station non reconnue"
  ("Unrecognized dock error") (the raw code remains visible in the dock error code command);
- corresponding actions: wash the mop, dry the mop, stop drying, empty the bin — available only when
  the robot is **at its dock** (including while charging); outside that state, the plugin refuses the
  action with an explicit message.

The wear of the consumables detected by your robot (main brush, side brush, filter, sensors, mop
roller) is published as a percentage remaining, each with a "Reset…" action to use after a physical
replacement. This action requires confirmation before it runs.

### Cleaning log

Seven read-only commands report the **last known cleaning**:

| Command | What it indicates |
|---|---|
| Dernier nettoyage (Last cleaning) | One-line summary, for example "Terminé — 42 min, 31,5 m²" ("Done — 42 min, 31.5 m²"); reads "No cleaning known for this robot." until a cleaning has been reported |
| Début du dernier nettoyage (Start of last cleaning) | Timestamp of the start (hidden by default) — the only one of the seven that can be compared arithmetically, to use in a scenario such as "the robot has not run for three days" |
| Durée du dernier nettoyage (Duration of last cleaning) | In minutes, rounded to the nearest minute (possible ±30 s gap with the mobile app) |
| Surface du dernier nettoyage (Area of last cleaning) | In m², rounded to 0.1 m² |
| Motif de fin du dernier nettoyage (End reason of last cleaning) | For example "Terminé" ("Done") or "Nettoyage interrompu" ("Cleaning interrupted") |
| Clé de motif de fin du dernier nettoyage (End reason key of last cleaning) | Stable technical value tied to the reason (hidden by default) — preferred over the label to test a condition in a scenario |
| Erreur du dernier nettoyage (Error of last cleaning) | Label of the error tied to that cleaning, "Aucune" (None) if everything went well |

The "Device" tab also offers a **"Cleaning log"** panel listing the last 10
known cleanings (start, end, duration, area, end reason, error), with the date of the last
synchronization. A **"Refresh log"** button re-reads this history from
Roborock:

- it is protected by the same one-minute anti-flood guard as the plugin's other resynchronization
  buttons — clicking again too soon shows "The log has just been refreshed: wait a minute before
  trying again.";
- the first refresh may only bring back a few records and complete on the next click: this is normal
  behavior, not a failure, since retrieval is time-bounded;
- the log also updates itself at the end of each cleaning, with no action needed from you.

If the Roborock cloud is unreachable at the time of viewing, the already-known values of the last
cleaning and of the history stay displayed as they are — they are never reset to zero. It is the
panel's last synchronization date that tells you whether the data is still fresh.

### Cumulative statistics

Four read-only commands report your robot's **overall** usage since it was put into service:

| Command | What it indicates |
|---|---|
| Durée totale de nettoyage (Total cleaning duration) | In hours, rounded to one decimal |
| Surface totale nettoyée (Total area cleaned) | In m², rounded to one decimal |
| Nombre total de nettoyages (Total number of cleanings) | Whole number |
| Nombre total de vidages du bac (Total number of bin empties) | Whole number; only appears if your dock can empty the bin |

These are **cumulative** counters kept by the robot itself, not a calculation done by Jeedom: they
match what the Roborock mobile app shows. Unlike most other commands in the plugin, they are
**historized by default**, so you can track a usage curve over time with no prior setting.

Their update is automatic: at the end of each cleaning, and at most once an hour otherwise. There is
no button to click, and no impact on Roborock quotas — the data arrives over the same channel as the
cleaning log above.

If you reset these counters to zero from the Roborock app (or after a factory reset), the Jeedom
commands will follow this drop: they faithfully mirror the robot, they do not keep a maximum. A visible
drop in the history after such a reset is therefore normal, not an anomaly. If a value is not usable at
the time it is read (robot unreachable, aberrant data), the command simply keeps its previous value
rather than falling back to zero.

### App schedules

The "Device" tab offers an **"Application schedules"** panel, shown as a
table (Recurrence / Repeat / Status). This list does not fill itself: click **"Read schedules"**
to populate it. A timestamp below the table shows the date of the
last read; with no prior click, the table invites you to click the button.

Each row corresponds to a schedule created in the Roborock mobile app and shows:

- its **recurrence**, displayed **exactly as returned by the cloud**, with no translation into weekdays
  or a readable time. This is not a display defect: the exact form of this information is not
  guaranteed to be identical across robot models, so the plugin passes it through raw rather than risk
  a wrong interpretation;
- whether it is **repeated** or not (Yes / No);
- whether it is **Active** or **Disabled**.

This reading is **one-way only**: no schedule can be created, modified or deleted from Jeedom.
Everything is managed in the Roborock app, which remains the single source of truth. After a change
made in the mobile app (disabling, changing the time...), click "Read schedules" again to see
the up-to-date status on the Jeedom side — it does not update itself.

Two reads less than a minute apart show a message asking you to wait a minute: this is not an error, it
is the same anti-flood protection as the plugin's other resynchronization buttons.

If the panel shows **"Schedules not available for this robot."**, that is a normal result, not a
failure: not all robot models provide this information to
the Roborock cloud. The rest of the plugin keeps working normally in this case.

Do not confuse these schedules with the **routines ("usages")** described below: routines are cleaning
scenarios that can be run on demand from Jeedom, schedules are time-based triggers managed by the
mobile app and only viewable here. These schedules create no command and therefore cannot be used in a
Jeedom scenario — this is a display for information, a deliberate choice rather than an oversight.

## Routines ("usages")

"Usages" are the cleaning routines you created in the Roborock mobile app. Once synchronized, each one
becomes an action command on the device, runnable from Jeedom like any other command, or from a
scenario.

These routines run through the Roborock cloud and therefore work **even if the direct channel with the
robot is unavailable** — only an Internet connection on the Jeedom side and a robot known to your
account are required.

### The "Routines" panel

A robot's "Device" tab includes a **"Routines"** section, below the "Roborock inventory" block. It shows:

- the **list of usages Jeedom knows** for this robot, one per line; when a command's name has been
  customized in Jeedom, the original name from the Roborock app is recalled in a second column, to help
  you match them up;
- the **"Synchronize routines"** button — this is the **only** place it appears, it is no longer in the
  page toolbar;
- the **synchronization rule**, stated plainly before any click: it keeps the usages still present in
  the app (same commands, same scenarios), deletes those that are no longer there, and adds the new
  ones.

If no usage is known yet, the panel says so explicitly rather than showing an empty list: run a
synchronization, or first create a usage in the Roborock app.

Displaying this panel triggers no call to the daemon or to the Roborock cloud: the list comes from what
Jeedom already knows, with no quota used.

### What a synchronization does

- **Usage still present in the app** → nothing is touched: same command, same identifier, usable
  identically in a scenario. Only the name follows that of the app if it changed — and only if you have
  not customized it in Jeedom, in which case your name is kept.
- **Usage gone from the app** (deleted on the mobile side) → its Jeedom command is **deleted**.
  ⚠️ A scenario that referenced it loses its reference, with no warning from Jeedom at the moment this
  happens: that is why the report shown after synchronization **names** each deleted usage, so you know
  what to fix.
- **New usage in the app** → a command is added, without touching the others.

A usage command cannot be deleted **by hand** from Jeedom: hide it if it bothers you, or delete the
corresponding usage in the app then run a synchronization again.

Two synchronizations less than a minute apart show a message asking you to wait: this is not an error,
it is the same anti-flood protection as the plugin's other resynchronization buttons. A synchronization
with no change on the app side is a neutral operation, and says so
("No changes: your routines are already up to date.").

If the list received from the Roborock cloud is **incomplete** (truncated response, or more than 64
usages on this robot), synchronization still applies additions and renamings, but **deletes nothing**:
as a precaution, an incomplete list is never interpreted as "these usages have disappeared."

If you update the plugin from an earlier version that marked some usages as "obsolete," the next
synchronization deletes them, like any usage missing from the app — no usage can remain durably stuck
in that state anymore.

### When to run it, and what it costs

There is **no automatic synchronization**: a usage created, renamed or deleted in the Roborock app only
appears (or disappears) on the Jeedom side after clicking "Synchronize routines". Run it, therefore,
every time you change your usages in the app.

It uses up **neither** the connection quota **nor** the device inventory quota (see "Roborock quotas"
below) — but two clicks less than a minute apart are refused, with an invitation to wait.

Preventive tip: before deleting a usage in the app, identify the Jeedom scenarios that use its command.
They will lose their reference as soon as the next synchronization runs.

If the account is not linked, if the daemon is stopped or if re-authentication is required, the panel
keeps showing the list of already-known usages, and the button shows an explicit message: in all these
cases, **no usage is deleted**.

## Dashboard tile

Each robot has a dashboard tile combining its photo (or, failing that, the plugin's icon), its status,
a battery gauge and the current control actions (start, pause, stop, return to base, locate).

The commands thus gathered by the tile no longer appear **separately** in the dashboard's standard
command list: they remain, however, fully usable in a scenario, in a view or in a custom design,
exactly as before. They are not deleted, only hidden from this grouped display.

## Map and rooms

### Panels on the device page

A robot's "Device" tab offers two additional panels:

- **Rooms** — the correspondence between the segments detected by the robot and the room names
  you gave in the Roborock app. A **"Resynchronize rooms"** button re-reads this correspondence; do
  this after adding, deleting or renaming a room in Roborock.
- **Maps** — the list of maps stored by the robot (useful if your home has several floors),
  with the active map, a selector to choose another one and a **"Change map"** button. Changing the map
  is a slow operation (the robot has to reload the requested map): the plugin refuses a new change
  request for two minutes after the previous one. **Changing the map automatically invalidates the
  displayed room list and map image**, which are then resynchronized.

The same tab offers two separate blocks, each with its own button:

- **Map image** — the image of the active map, rebuilt automatically during
  cleanings (at most once every 30 seconds) and refreshable manually via "Refresh the map image".
- **Zone and point** — a **purely informational** block (no input here) showing the
  coordinate frame of the last map retrieved: the usable area in millimeters, the position of the
  charging dock and that of the robot at the time of the map, along with a conversion aid from a pixel
  in the image. It serves to prepare the values to enter into the "Clean a zone" and "Move to a point"
  commands (see "Fine-grained control" below), which remain **device commands**, not fields of this
  panel. With no map image retrieved, only general bounds are known.

### "Map" panel (Home > JeeRoborock)

The map is a **panel**, not a page in the Plugins menu: it opens from the **Home > JeeRoborock** menu,
and is accessible to any user with read rights on at least one robot (not just administrators). It
shows the active map of the selected robot, its timestamp and the legend of detected rooms (segment
number / name), and refreshes itself every 30 seconds as long as the page stays open.

If the entry does not appear in **Home**, check that the **"Display desktop panel"** checkbox is
checked on the plugin management page (**Plugins > Plugin management > JeeRoborock**): it is checked
automatically on installation, but remains editable.

## Fine-grained control

Depending on the capabilities detected on your robot, the following commands may appear:

- **Suction power** and **water flow** — an information command
  shows the current level, an action command (drop-down list) lets you choose another one among those
  actually supported by your robot.
- **Mop route** and **cleaning mode** (vacuum only / mop
  only / vacuum and mop) — same principle: information + action drop-down list.
- **Clean rooms** — one command per detected room ("Clean <room name>"), plus a generic
  **"Clean rooms (names separated by commas)"** command that accepts a free-text list of names. As with
  usages, the command name follows renamings made in the Roborock app at the next synchronization —
  including when the room name contains an apostrophe, an ampersand, a hash sign or a percent sign
  ("Salle d'eau", for example) — unless you have manually customized this name in Jeedom, in which case
  your customized name is kept.
- **"Clean a zone (x1,y1,x2,y2 in mm)"** — takes four coordinates `x1,y1,x2,y2` in millimeters and
  cleans the corresponding rectangle.
- **"Move to a point (x,y in mm)"** — takes two coordinates `x,y` in millimeters.

Zone and point coordinates are expressed in the same frame used for the map (see "Map and rooms").

## Real time and freshness

Once a robot is synchronized, its status updates automatically, with no action from you:
- every **30 seconds** during a cleaning;
- every **60 seconds** at rest.

The **"Last update"** command shows the timestamp of the most recent data
received.

The **"Online"** indicator reacts quickly: it switches to **"Offline"** as soon as a
periodic poll fails to get a response from the robot (at rest, a poll happens roughly every minute;
roughly every 40 seconds while cleaning), and comes back **"Online"** as soon as a read succeeds, an
update is received spontaneously from the robot, or an action is confirmed to it. Coming back "Online"
can take only a few seconds (the robot sends an update) or, in the worst case where the robot has
stayed unreachable for a long time, up to about ten minutes (polls space out progressively after
several failures).

Independently of this mechanism, if **no** data could be obtained for more than **3 minutes**, the
plugin switches both the "Online" **and** "Connected" indicators to
**"Disconnected"**: this signals an unreachable robot (powered off, off the network, or the Roborock
cloud unavailable), not an error of the plugin itself.

## Re-authentication required

When the session saved with Roborock has expired or been revoked, the plugin shows
**"Re-authentication required"** (a message visible on the affected
commands, and on action attempts).

**The plugin never tries to reconnect on its own.** This step requires reading a code received in your
mailbox, which no automation can do in your place. To resolve it:

1. Open the plugin configuration.
2. Click **"Send a code"**, retrieve the code received by e-mail.
3. Enter it and click **"Validate the code"**.

Once validation succeeds, everything resumes normally, with no further action needed.

## Roborock quotas

Roborock's servers impose **strict quotas shared with the mobile app of your account**: a limited
number of connections per minute/hour/day, and a limited number of device inventory calls over the same
time windows.

When a message says a quota has been reached, **wait**: this is not a plugin error, and retrying right
away only makes things worse — you would also penalize the mobile app's use on that same account, until
the counter resets. The plugin never automatically retries after a quota refusal.

Synchronization and running usages do not count against these quotas.

## Troubleshooting

### Diagnostic report

Before asking for help, generate a diagnostic report: from the **plugin configuration**, in the
**"Diagnostics and support"** block, click **"Generate a diagnostic report"**. The report appears
in a text area, ready to send.

It gathers the state of the environment (plugin, Jeedom and daemon versions, including the version of
the Roborock library used), the account connection status, the list of robots — each identified by its
Jeedom device number and a partially masked device identifier —, the recent errors reported by Jeedom
and the daemon, and a technical appendix. It **never** contains a login identifier, a token, a robot
key, a serial number or an e-mail address, no matter the content; the names you gave your robots or
your rooms do not appear either.

Two buttons let you retrieve it: **"Copy the report"** (clipboard) and
**"Download the report"** (text file). If automatic copying does not work —
the most common case when Jeedom is served over HTTP rather than HTTPS — the text remains selected:
copy it with Ctrl+C. If a support forum limits message length, attach the downloaded file instead.

If the daemon is stopped at the time of generation, the report flags this at the top
("Daemon unreachable: partial report") and remains usable anyway: the information still known on the
Jeedom side (last state, timestamp of last communication) appears anyway. If it is running but the
technical section could not be produced, the report indicates this with a different banner
("Daemon diagnostics unavailable: partial report"); here too, the rest
of the report stays usable.

This action is reserved for Jeedom administrators.

### What to include with a help request

In addition to the report, describe in your message: the **precise symptom** (what you observe, and on
which command or screen), **what you have already tried**, and the **approximate time** the problem
occurred. These three pieces of information make it possible to find the incident in a report or a log;
the report alone is not enough to guess the context.

**Never publish as-is**, on a forum or in a public ticket:

- your Roborock account **e-mail address** or the **code** received by e-mail;
- a **token**, a session identifier or any value that looks like a technical key;
- the **raw content** of the plugin or daemon logs (Jeedom menu "Analyse" ("Analysis") > "Logs", or
  files under `log/`): unlike the diagnostic report, these logs **are not scrubbed**;
- a **screenshot** that would reveal any of these elements.

The diagnostic report generated from the configuration page is, on the other hand, designed to be sent
as-is (see above).

| Symptom | Likely cause | What to do |
|---|---|---|
| The dependency indicator stays stuck / red | Python dependency installation not finished or failed | Wait the installation time indicated by Jeedom; if it keeps failing, check the server's Internet access and restart the installation from the "Plugins" page |
| "The daemon is not responding." | The daemon is not started, or was just stopped | Start (or restart) the daemon from the plugin configuration |
| "The robot is offline: it is not responding to the Roborock cloud." | The robot is off, off the network, or has no connection to the Roborock cloud | Check that the robot is on and connected to your Wi-Fi network, as from the mobile app |
| "The Roborock account is not linked." | An action was requested while no account has been linked yet | Follow the account linking procedure, section "Linking your Roborock account" |
| "The Roborock account e-mail address is invalid." or "No Roborock account matches this e-mail address." | The entered address has a typo, or is not that of the Roborock account | Enter the exact address used in the Roborock mobile app, save the configuration, then request a code again |
| Login code never received by e-mail | Incorrect e-mail address, or message filtered by your mail provider | Check the saved address, check your spam folder, try "Send a code" again after a few minutes |
| "Login code invalid or expired." | The code was mistyped or has expired | Request a new code and validate it quickly |
| "Too many login code requests." | Too many code requests close together | Wait a few minutes before requesting a code again |
| "Roborock session expired." / "Re-authentication required" | The saved session is no longer valid on the Roborock side | Follow the "Re-authentication required" procedure above |
| "Roborock call quota reached." | The quota, shared with the mobile app, is temporarily exhausted | Wait before trying again; do not retry the action in a loop |
| An expected command does not appear on the device | The robot does not report the corresponding capability | This is normal: the command list depends on what the robot declares it can do, not a bug |
| "This map no longer exists on this robot." | The displayed map list is outdated | Click "Refresh map list" then try again |
| "A map change was just made: wait two minutes before starting another one." | Changing the map is a slow operation, protected by a two-minute guard | Wait two minutes before starting another map change |
| "The robot map could not be decoded." | The data received from the dock is unreadable (one-off incident on the robot or cloud side) | Try again later; check the daemon log if the problem persists |
| "The map image is too large to be transferred." | The map produced by the robot exceeds the size the plugin accepts to store | Try again later; if the problem persists, this robot is not compatible with this feature |
| "The robot must be at the dock to start this operation." | A dock maintenance action was requested while the robot is not at its dock | Wait for the robot to return to its dock, or run "Return to base" first |
| "This maintenance operation is not available on this robot's dock." | This robot's dock does not support this action | This is normal: the command should not appear if the dock does not support it; refresh the robot's status |
| "The list of routines received from the Roborock cloud is incomplete: as a precaution, no routine was deleted." | The cloud response was truncated, or this robot has more than 64 usages | Run the synchronization again later; nothing was lost in the meantime |
| "The Roborock terms of use have not been accepted." (or "have changed") | Roborock requires accepting (or re-accepting) its terms of use | Open the Roborock mobile app, accept the terms shown, then try again from Jeedom |
| "Robot unknown to the daemon." | The Jeedom device is no longer recognized by the daemon (restart, robot removed from the account…) | Run "Synchronize devices" again |
| "The Roborock cloud is unreachable." | Jeedom cannot reach Roborock's servers | Check the Jeedom server's Internet access |
| A message about an **exceeded timeout**, a **failed connection**, or "several communication attempts failed" | The robot or the Roborock cloud took too long to respond: a transient network incident, or a very busy robot | Try again after a minute; if it keeps happening, check the robot's Wi-Fi connection and the Jeedom server's Internet access |
| "The robot is busy.", "The robot refused the action in its current state." or "The robot reported an error while executing the command." | The robot cannot carry out this request in its current state (cleaning in progress, full bin, mechanical incident…) | Check the robot's status (the "Status" command, or the mobile app), resolve the reported incident then retry the action |
| "This feature is not available on this robot model." or "The robot does not recognize this command." | The robot does not implement this feature, even though the command exists in Jeedom | No action will fix this: this feature does not exist on this hardware, hide the command if it bothers you |
| "No code request in progress (the daemon may have restarted): request a new code." | The daemon restarted between sending and validating the code | Click "Send a code" again, then validate the new code received |
| A setting (suction, water flow, route, cleaning mode) is not applied | The robot refuses this setting in its current state (generally: not at rest) | Try again once the robot is at rest or at its dock |
| "This suction power / water flow / route / cleaning mode is not available on this robot." | The list of levels known by Jeedom is outdated (the robot no longer reports this value) | Refresh the robot's status then try again |
| "Unknown room.", "no known room" or "several rooms share this name" | The entered name does not match any detected room, no room has been synchronized yet, or the name is ambiguous | Resynchronize rooms from the Device tab, use the exact name from the Roborock app, or the command dedicated to this room rather than the generic command |
| "These coordinates fall outside the known map limits of this robot." | The entered zone or point goes beyond the map currently known for the robot | Check the coordinates in the "Zone and point" block of the Device tab, or refresh the map image |
| "This consumable is not tracked for this robot." | The reset command was used before this consumable's wear had ever been reported | Refresh the robot's status before resetting this consumable |
| "A routine synchronization has just been performed" / "A room synchronization has just been performed: wait a minute before trying again." (usages, rooms or schedules) | A resynchronization already happened less than a minute ago | Wait a minute before running the same resynchronization again |
| "The log has just been refreshed: wait a minute before trying again." | The "Refresh log" button was already used less than a minute ago | Wait a minute before clicking again |
| "Report generation failed." | The request to Jeedom did not complete: 20-second timeout exceeded, connection interrupted or a Jeedom server error (a stopped daemon, on the other hand, gives a partial report, not this failure) | Reload the configuration page and try again; if it persists, check the `jeeroborock` log (menu "Analyse" ("Analysis") > "Logs") |
| "… routine(s) could not be saved in Jeedom. Check the plugin log." (in the report of the "Routines" panel) | A particular usage could not be created or updated on the Jeedom side during synchronization, while the rest went normally | Check the `jeeroborock` log (menu "Analyse" ("Analysis") > "Logs") to identify the usage concerned, then run a synchronization again |
| "401 - Unauthorized access" when clicking "Generate a diagnostic report" | Your Jeedom session expired, or your account does not have administrator rights | Log back into Jeedom with an administrator account then try again |
| "Daemon diagnostics unavailable: partial report" | The daemon is running, but could not provide the technical part of the report (one-off incident) | The rest of the report remains usable; try again later to get the full technical section |

For any other message, the text shown by the plugin directly gives the cause and, where relevant, the
action to take — it is never necessary to open technical logs to understand it.

## Known limitations

- The plugin only controls robots compatible with Roborock's V1 protocol, via the cloud. Older robots
  (A01 protocol) are not supported.
- Labels produced by the robot itself (status, error, dock status, consumable names) are **always in
  French**, whatever language is chosen for the Jeedom interface.
- A map change made from the mobile app is now automatically detected, in the background, within about
  a minute: the active map, image and reference frame of the map update with no action from you (the
  room list, however, is cleared and awaits a click on "Resynchronize rooms"). During this short delay,
  the configuration may still show the old floor, and an already-open Device page does not refresh
  itself: reload it.
- The local connection mentioned above ("What the plugin does, and what it does not") cannot be
  disabled from Jeedom.
- The plugin shows the robot's **firmware** version (Device tab, updated at device synchronization), but
  does not report that an update is available and does not trigger it: firmware updates are done from
  the Roborock mobile app.
- Beyond **64 usages** registered for the same robot, routine synchronization keeps adding and renaming,
  but no longer automatically deletes usages that disappeared from the app.
- The map image may stay **unreadable** when the robot is only reachable over the local connection
  mentioned above, without going through the cloud MQTT channel (message "The robot map could not be
  decoded.").
- Reading room names (the "Rooms" panel of the Device tab) requires the robot to be **online**: it
  fails if the robot is unreachable at the time of the click.
- The map view (the "Home > JeeRoborock" panel) does not itself trigger any update: it simply displays,
  every 30 seconds, the last already-known image. This image is only rebuilt during cleanings; at rest,
  it may therefore date back to the robot's last pass.
- There is no map view on the Jeedom mobile app: the map panel is only available on the desktop
  interface.
- The commands absorbed by the dashboard tile (battery, cleaning, error, connected, online and the five
  control actions) are hidden only once, when the tile is created. If you manually unhide one, the
  plugin never hides it again: your choice is kept.
- On an installation updated from an old plugin version, a one-off technical migration may have
  re-enabled history logging for the "Error" command: if you do not want to log this
  command's history, disable it manually on its configuration.

This page is updated with each new feature shipped by the plugin.
