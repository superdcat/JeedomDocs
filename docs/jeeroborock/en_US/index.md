# JeeRoborock

JeeRoborock controls your Roborock robot vacuums from Jeedom, through the Roborock cloud: real-time
status, cleaning commands, fine-grained control (suction, water, route, dock maintenance), room or
zone cleaning, multiple maps, and running the routines ("usages") defined in the Roborock mobile app.

## What the plugin does, and what it does not

JeeRoborock is free software, released under the **GPL v3 or later** license.

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

1. **Jeedom 4.4.7 minimum**, installed on a server running **Debian 12 or 13**. This Debian version is
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

### Commands by model

The plugin has no list of commands "per model". It creates a command when the robot or its dock
**declares** the matching capability, or **answers** when the plugin queries it. A missing command
therefore means "this hardware does not report it (or not yet)", not "the plugin is broken". A robot with
a full dock does not have the same list as a robot without a dock, nor as an older robot from the same
manufacturer.

**Making a missing command appear:**

1. Check that the daemon is running, that the account is linked and that the robot is **online**: as long
   as the robot has not answered once, no command that depends on its capabilities is created.
2. Run the device's **"Refresh"** command, or wait: the status is re-read by itself every 60 seconds at
   rest (30 seconds during a cleaning). Commands are created at this re-read. Then reload the device
   page.
3. After a firmware update of the robot (from the Roborock app) or of the plugin, do the same. Do **not**
   use "Synchronize devices" for this: that button is for discovering the account's robots and uses up
   Roborock quota.
4. If the robot answered that it does not know a setting read by querying (Do Not Disturb, volume), the
   plugin only queries again **once an hour**; if a read fails (robot unreachable), it tries again after
   5 minutes. The "Refresh" command forces an immediate read.
5. Right after "Refresh", the last settings in the list (volume, dock modes) may be missing if the re-read
   ran out of time: run "Refresh" again or wait a minute.

The plugin never deletes a command it has already created.

| Capability | Commands concerned | Condition for appearing |
|---|---|---|
| Dock consumables | "Station filter wear remaining", "Cleaning brush wear remaining", "Dust bag wear remaining" and, except for the bag, their "Reset…" action | The dock has the equipment (mop washing for the filter, cleaning brush, automatic emptying for the bag) **and** the robot reports the counter. Re-read about every hour, or on "Refresh" |
| Tanks and mop | "Clean water tank empty", "Dirty water tank full or missing", "Mop installed" | Tank and dirty-water bin: the dock washes the mops. Mop: the robot reports that it handles the water mode. Created at the next status re-read |
| Child lock | "Child lock", "Enable…", "Disable…" | The robot reports that it handles this setting. Created at the next status re-read |
| Do Not Disturb | Information, start, end, three actions | The robot answers the mode read. Re-read every minute; immediately on "Refresh" |
| Off-peak hours | Information, start, end, three actions | The robot reports the function. Created at the next status re-read |
| Volume | "Volume", "Set the volume" | The robot answers the volume read. Re-read every minute; immediately on "Refresh" |
| Dock modes | "Emptying mode" and "Set the emptying mode"; "Mop washing mode" and "Set the washing mode" | The dock reports automatic emptying (emptying mode) or mop washing (washing mode). Created at the next status re-read |
| Number of passes | No command of its own: a parameter of the "Clean rooms" and "Clean a zone" actions | The robot states, in its status, that it handles repetition. The field is then labeled "Number of passes (1 to 3)"; otherwise the field is not labeled and a number of 2 or 3 is in principle refused by the plugin |
| Current room | "Current room" | A map image has been read, the map is divided into rooms and the robot's position is usable. First image: at the first re-read, then during a cleaning or after a status change |

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

**While the dust bin is being emptied.** When the dock empties the bin (robot status "Vidage du bac à poussière", i.e. emptying the dust bin), the robot does not take a cleaning order into account. The plugin then refuses it, instead of answering "ok" with no effect: this applies to "Start", "Clean rooms", the "Clean <room name>" commands and "Clean a zone". The message shown is "Le robot vide son bac à poussière : l'ordre de nettoyage n'a pas été envoyé. Réessayez dans un instant, quand le vidage sera terminé (robot de nouveau en charge)." (The robot is emptying its dust bin: the cleaning order was not sent. Try again in a moment, when emptying is finished (robot charging again).) In a scenario, the action fails the same way. The other commands (pause, stop, return to base, locate, move to a point) are not affected, nor are routines ("usages"), which are run by the Roborock cloud. If the plugin cannot re-read the robot's status just before the order, the order is sent normally.

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

Depending on your dock's equipment, and if the robot reports the counter, three additional wear values
appear, also as a percentage remaining:

- "Station filter wear remaining": docks that wash the mop;
- "Cleaning brush wear remaining": docks that have one (in practice, some high-end docks);
- "Dust bag wear remaining": docks with automatic emptying.

With no dock, or with a basic dock, these commands do not appear. The station filter and the cleaning
brush each have a "Reset the station filter" or "Reset the cleaning brush" action, with confirmation, like
the others. The dust bag has no reset in the plugin (read-only): if you reset it elsewhere (Roborock app),
the value follows at the next re-read.

These values are re-read about once an hour, immediately with the "Refresh" command, and after a reset.
The percentages may differ slightly from those of the Roborock app.

**Scenario example**: trigger on the "Station filter wear remaining" command, condition "below 10", action
"Send a notification" ("Remember to replace the dock filter"). After the replacement, run the "Reset the
station filter" action (it asks for confirmation): do not put it in an automatic scenario, the counter would
go back to 100% without the part having been replaced.

Three yes/no values, usable in a scenario, also describe the state of the water and of the mop:

- "Clean water tank empty" and "Dirty water tank full or missing": only if your dock washes the mops.
  "Yes" flags a situation to check (fill the tank, empty or put back the bin). The robot cannot tell a
  full dirty-water bin from a missing one, hence the label;
- "Mop installed": only if your robot is equipped with a mop.

This information is separate from "Water shortage": the robot reports it separately, and the values can
be flagged at the same time. They are refreshed with the robot's status (about a minute at rest), or
immediately with "Refresh". If a value is momentarily unavailable, the last known value is kept.

**Scenario example**: trigger on "Clean water tank empty" or "Dirty water tank full or missing" (value
"Yes"), action "Send a notification" ("Check the dock's tank or bin"). A condition on "Mop installed" (value
"No") lets you avoid starting a cleaning with washing when the mop is not fitted.

### Device settings

The **child lock** disables the robot's physical buttons (handy against an overly curious child or pet).
Three commands are dedicated to it:

- "Child lock": yes/no information, usable as a scenario condition (for example to enable the lock only
  if it is not already enabled);
- "Enable child lock" and "Disable child lock": two actions.

These commands only appear **if your robot reports that it handles this setting**. Otherwise none of the
three exists: this is not a fault, two robots do not have the same command list.

After an order, the plugin re-reads the robot's status to check that it took it, as for the settings
described in "Fine-grained control" (up to about twelve seconds, without sending the order again). The
"Child lock" command only shows what the robot actually adopted, never the requested value. The possible
messages:

| Message | Meaning |
| --- | --- |
| "Child lock enabled." / "Child lock disabled." | The robot took the order: the state read back matches. |
| "Child lock activation (or deactivation) sent to the robot (not confirmed as applied)." | The order was sent, but the state could not be read back, or another child lock order replaced it during the check. The displayed state stays the old one. |
| "The robot did not apply the child lock order: the state read back does not match the request." | The robot answers, but did not adopt the setting by the end of the delay. The displayed state is the one read back from the robot. |
| Robot refusal | The robot refused the order; the message says so. |
| Robot offline | The robot does not answer (off, out of range); the order is not taken. |

The plugin never sends an order again by itself: in case of failure, send it again yourself.

**Scenario example**: at the end of the cleaning ("Cleaning" goes to "No"), if the "Child lock" condition is
"No", run the "Enable child lock" action.

A change made from the Roborock app (or the robot's button) is not signaled to the plugin: it shows up in
"Child lock" within about a minute, or immediately with the "Refresh" command.

**Wait a few seconds between two child lock orders.** An order sent less than 5 seconds after the end of
the previous one (check included), on the same robot, is refused with the message "A child lock order was
just sent to this robot: wait a few seconds before sending another one." In a scenario, allow a pause of at
least 5 seconds between two child lock actions.

#### Do Not Disturb

The **Do Not Disturb** mode keeps the robot from starting or speaking during a time range (at night, for
example). Six commands are dedicated to it:

| Command | Type | Role |
| --- | --- | --- |
| Do Not Disturb | Yes/no information | Shows whether the mode is enabled, usable as a scenario condition |
| Do Not Disturb start | Text information | Start time of the range, in HH:MM format |
| Do Not Disturb end | Text information | End time of the range, in HH:MM format |
| Enable Do Not Disturb | Action | Enables the mode with the range saved by the robot |
| Disable Do Not Disturb | Action | Disables the mode |
| Set the Do Not Disturb time range | Action with two fields, Start and End | Saves the range and enables the mode |

These commands only appear **if the robot answers the mode read**. They are created at the latest about a
minute after the robot becomes reachable, or immediately with "Refresh". If they are missing, it is not a
fault: two robots do not have the same command list.

Times are expressed in the **robot's local time**, as in the Roborock app.

**Setting the range**: fill in the Start and End fields in HH:MM format, between 00:00 and 23:59. A
one-digit hour such as 7:30 is accepted and normalized to 07:30. The action can be used in a scenario: the
**Title** field receives the start, the **Message** field the end (their input hints are labeled "Start
(HH:MM)" and "End (HH:MM)"). A range that crosses midnight is accepted (for example 22:00 → 07:00). A start
equal to the end is refused. Setting the range **also enables the mode**.

| Input (start → end) | Result |
|---|---|
| 22:00 → 07:00, or 7:30 → 22:15 | Valid (range crossing midnight, or one-digit hour normalized to 07:30) |
| 00:00 → 23:59 | Valid |
| 24:00 → 07:00, 22:60 → 07:00 | Refused: hour or minute out of bounds |
| 22h00 → 07h00, 2200 → 0700, 22:5 → 07:00 | Refused: the format must be HH:MM (two-digit minutes, ":" separator) |
| (empty field) → 07:00 | Refused: a field is empty |
| 22:00 → 22:00 | Refused: start equal to end |

**Scenario example**: every evening at 9 pm, run the "Set the Do Not Disturb time range" action with start
22:00 and end 07:00. To silence announcements during the day, use "Enable Do Not Disturb" / "Disable Do Not
Disturb" on the range already saved.

**Enable** re-applies the range already saved by the robot. If the robot returns none, the action is
refused: use "Set the Do Not Disturb time range" instead. **Disable** normally keeps the saved range, but
this behavior depends on the robot and remains to be confirmed: if you count on "Enable" afterwards, check
"Do Not Disturb start" and "Do Not Disturb end".

After an order, the plugin re-reads the robot's status to check that it took it (a few seconds, without
sending the order again). The information commands only show what the robot actually adopted. The possible
messages:

| Message | Meaning |
| --- | --- |
| "Do Not Disturb enabled." / "Do Not Disturb disabled." / "Do Not Disturb time range applied." | The robot took the order: the state read back matches. |
| "Do Not Disturb activation (or deactivation) sent to the robot (not confirmed as applied)." / "Do Not Disturb time range sent to the robot (not confirmed as applied)." | The order was sent, but the state could not be read back. The displayed state stays the old one. |
| "The robot did not apply the Do Not Disturb command: the state read back does not match the request." | The robot answers, but did not adopt the setting by the end of the delay. |
| "Invalid time range: enter a start and an end in HH:MM format, between 00:00 and 23:59." | A field is empty or badly formed. Fix it. |
| "Invalid time range: the start and end of the Do Not Disturb range must be different." | Start and end are identical. |
| "The robot returned no usable Do Not Disturb time range: set the range, which also enables the mode." | "Enable" has no range to re-apply: use "Set the Do Not Disturb time range". |
| "A Do Not Disturb command was just sent to this robot: wait a few seconds before sending another one." | Two orders too close together. |
| Robot refusal / robot offline | The robot refused the order or does not answer; the order is not taken. |

The plugin never sends an order again by itself: in case of failure, send it again yourself.

A change made from the Roborock app is not signaled to the plugin: it shows up in Jeedom within about a
minute, or immediately with "Refresh".

**Wait at least 5 seconds between two Do Not Disturb orders** on the same robot, otherwise the last one is
refused ("wait" message). In a scenario, allow a pause of at least 5 seconds between two Do Not Disturb
actions.

#### Off-peak hours

**Off-peak charging** makes the robot wait for the chosen time range (at night, for example, at the
reduced electricity rate) to **recharge its battery**. It only delays charging: it does not block a
cleaning you request. Six commands are dedicated to it:

| Command | Type | Role |
| --- | --- | --- |
| Off-peak charging | Yes/no information | Shows whether the function is enabled, usable as a scenario condition |
| Off-peak start | Text information | Start time of the range, in HH:MM format |
| Off-peak end | Text information | End time of the range, in HH:MM format |
| Enable off-peak charging | Action | Enables the function with the range saved by the robot |
| Disable off-peak charging | Action | Disables the function |
| Set the off-peak time range | Action with two fields, Start (HH:MM) and End (HH:MM) | Saves the range and enables the function |

These commands only appear **if the robot reports the function**. They are created at the latest about a
minute after the robot becomes reachable, or immediately with "Refresh". If they are missing, it is not a
fault: two robots do not have the same command list.

Times are expressed in the **robot's local time**, as in the Roborock app.

**Setting the range**: fill in the Start and End fields in HH:MM format, between 00:00 and 23:59. A
one-digit hour such as 7:30 is accepted and normalized to 07:30. The action can be used in a scenario, with
these two fields. A range that crosses midnight is accepted (for example 23:00 → 07:00). A start equal to
the end is refused. Setting the range **also enables off-peak charging**. In a scenario, the **Title**
field receives the start and the **Message** field the end (input hints "Start (HH:MM)" and "End
(HH:MM)"). Same input rules as for "Do Not Disturb":

| Input (start → end) | Result |
|---|---|
| 23:00 → 07:00, or 7:30 → 22:15 | Valid (the second one is normalized to 07:30) |
| 24:00 → 07:00, 23:60 → 07:00 | Refused: hour or minute out of bounds |
| 23h00 → 07h00, 2300 → 0700, 23:5 → 07:00 | Refused: the format must be HH:MM |
| (empty field) → 07:00 | Refused: a field is empty |
| 23:00 → 23:00 | Refused: start equal to end |

**Scenario example**: once a week, run "Set the off-peak time range" with start 23:00 and end 07:00 to
realign the range with your electricity contract; or trigger "Enable off-peak charging" when your
leaving-home scenario runs.

**Enable** re-applies the range already saved by the robot. If the robot returns none, the action is
refused: use "Set the off-peak time range" instead. **Disable** normally keeps the saved range, but this
behavior depends on the robot and remains to be confirmed: if you count on "Enable" afterwards, check
"Off-peak start" and "Off-peak end".

After an order, the plugin re-reads the robot's status to check that it took it (a few seconds, without
sending the order again). The information commands only show what the robot actually adopted. The possible
messages:

| Message | Meaning |
| --- | --- |
| "Off-peak charging enabled." / "Off-peak charging disabled." / "Off-peak time range applied." | The robot took the order: the state read back matches. |
| "Off-peak charging activation (or deactivation) sent to the robot (application not confirmed)." / "Off-peak time range sent to the robot (application not confirmed)." | The order was sent, but the state could not be read back. The displayed state stays the old one. |
| "The robot did not apply the off-peak charging command: the state read back does not match the request." | The robot answers, but did not adopt the setting by the end of the delay. |
| "Invalid time range: enter a start and an end in HH:MM format, between 00:00 and 23:59." | A field is empty or badly formed. Fix it. |
| "Invalid time range: the off-peak start and end must be different." | Start and end are identical. |
| "The robot returned no usable off-peak time range: set the range, which also enables off-peak charging." | "Enable" has no range to re-apply: use "Set the off-peak time range". |
| "An off-peak charging command was just sent to this robot: wait a few seconds before sending another one." | Two orders too close together. |
| Robot refusal / robot offline | The robot refused the order or does not answer; the order is not taken. |

The plugin never sends an order again by itself: in case of failure, send it again yourself.

A change made from the Roborock app is not signaled to the plugin: it shows up in Jeedom within about a
minute, or immediately with "Refresh".

**Wait at least 5 seconds between two off-peak orders** on the same robot, otherwise the last one is
refused ("wait" message). This pause is independent from the "Do Not Disturb" one: a Do Not Disturb order
does not delay an off-peak order. In a scenario, allow a pause of at least 5 seconds between two off-peak
actions.

#### Volume

The **volume** is that of the robot's voice announcements ("Starting cleaning", "Returning to dock"…),
from 0 to 100%. Two commands are dedicated to it:

| Command | Type | Role |
| --- | --- | --- |
| Volume | Numeric information (%) | Volume read back from the robot, usable as a scenario condition |
| Set the volume | Action with a 0 to 100 slider | Sends the requested volume to the robot |

In a scenario, "Set the volume" accepts a value (for example 40) or an expression (for example a
calculation based on another command).

These commands only appear **if the robot answers the volume read**. They are created at the latest about
a minute after the robot becomes reachable, or immediately with "Refresh". If they are missing, it is not
a fault: two robots do not have the same command list.

**Accepted values**: a whole number from 0 to 100, 0 included (0 mutes the announcements). An empty,
decimal (50.5) or out-of-bounds (-1, 101) value is refused with the message "Invalid volume: enter a whole
number between 0 and 100.", without sending anything to the robot.

After an order, the plugin re-reads the robot's volume to check that it took it (a few seconds, without
sending the order again). The "Volume" command only shows what the robot actually adopted. The possible
messages:

| Message | Meaning |
| --- | --- |
| "Volume applied." | The robot took the order: the volume read back matches. |
| "Volume setting sent to the robot (application not confirmed)." | The order was sent, but the volume could not be read back. The displayed value stays the old one. |
| "The robot did not apply the requested volume: the volume read back does not match the request." | The robot answers, but kept another value. "Volume" shows the value read back. |
| "A volume setting was just sent to this robot: wait a few seconds before sending another." | Two settings too close together. |
| Robot refusal / robot offline | The robot refused the order or does not answer; the order is not taken. |

The plugin never sends an order again by itself: in case of failure, send it again yourself. To hear the
new volume, run the "Locate" command.

**Scenario example**: at 10 pm, run "Set the volume" with the value 20; at 8 am, with the value 50. To halve
the volume, pass an expression based on the "Volume" information command (for example
`round(#[Salon][Robot][Volume]#/2)`, fictitious device name: the result must be a whole number from 0 to
100, otherwise the order is refused, hence the `round`).

**The position of the "Set the volume" slider shows the last value sent from Jeedom, not necessarily the
robot's actual volume, and does not follow a change made in the Roborock app. The reference is the "Volume"
information.**

A change made from the Roborock app is not signaled to the plugin: it shows up in "Volume" within about a
minute, or immediately with "Refresh".

**Wait at least 5 seconds between two volume settings** on the same robot, otherwise the last one is
refused ("wait" message). In a scenario, allow a pause of at least 5 seconds between two "Set the volume"
actions.

#### Emptying mode

The **emptying mode** sets how intensely the dock empties the robot's dust bin. Two commands are dedicated
to it:

| Command | Type | Role |
| --- | --- | --- |
| Emptying mode | Text information | Mode read back from the dock, usable as a scenario condition |
| Set the emptying mode | List-type action | Sends the chosen mode to the dock |

These commands only appear **if the dock reports this setting** (automatic bin emptying): a robot with no
dock, or with a dock that does not empty the bin, has none. They are created at the latest about a minute
after the robot becomes reachable, or immediately with "Refresh". If they are missing, it is not a fault:
two robots do not have the same command list.

**Modes offered**: Intelligent, Léger (Light), Équilibré (Balanced), Max. This list comes from the library
used by the plugin and is the same for all docks: compare it with the one in the Roborock app. If the dock
returns a code the plugin does not know, "Emptying mode" shows "Mode inconnu (N)" (Unknown mode (N)), where
N is that code.

In a scenario, "Set the emptying mode" is chosen by the **mode code** (not by its label), as for the
plugin's other list-type commands.

After an order, the plugin re-reads the dock's mode to check that it was taken (a few seconds, without
sending the order again). "Emptying mode" only shows what the dock actually adopted. The possible
messages:

| Message | Meaning |
| --- | --- |
| "Emptying mode set to "…"." | The dock took the order: the mode read back matches. |
| "Emptying mode "…" sent to the robot (application not confirmed)." | The order was sent, but the mode could not be read back. The displayed value stays the old one. |
| "The dock did not apply the requested emptying mode: the mode read back does not match the request." | The dock answers, but kept another mode. "Emptying mode" shows the mode read back. |
| "This emptying mode is not available on this robot's dock: refresh its status before trying again." | The requested mode is not known for this dock. |
| "An emptying mode setting was just sent to this robot: wait a few seconds before sending another." | Two settings too close together. |
| Robot refusal / robot offline | The robot refused the order or does not answer; the order is not taken. |

The plugin never sends an order again by itself: in case of failure, send it again yourself. The emptying
setting could not be verified on all robots: if your dock does not accept it, the refusal message above
tells you so.

**Scenario example**: trigger "Emptying mode" equal to "Max"; action "Set the emptying mode" with the code
of the "Équilibré" (Balanced) mode (the codes are those of the command's list), to go back to the usual
mode.

A change made from the Roborock app is not signaled to the plugin: it shows up in "Emptying mode" within
about a minute, or immediately with "Refresh".

**Wait at least 5 seconds between two emptying mode settings** on the same robot, otherwise the last one is
refused ("wait" message). In a scenario, allow a pause of at least 5 seconds between two "Set the emptying
mode" actions.

#### Mop washing mode

The **washing mode** sets how intensely the dock washes the mop. Two commands are dedicated to it:

| Command | Type | Role |
| --- | --- | --- |
| Mop washing mode | Text information | Mode read back from the dock, usable as a scenario condition |
| Set the washing mode | List-type action | Sends the chosen mode to the dock |

These commands only appear **if the dock reports this setting**: a robot with no washing dock has none.
They are created at the latest about a minute after the robot becomes reachable, or immediately with
"Refresh". If they are missing, it is not a fault.

**Modes offered**: Léger (Light), Équilibré (Balanced), Profond (Deep), plus **Très profond** (Very deep)
or **Intelligent** depending on the robot. As for emptying, compare with the Roborock app. An unrecognized
code is displayed as "Mode inconnu (N)" (Unknown mode (N)).

In a scenario, "Set the washing mode" is chosen by the **mode code**, not by its label.

After an order, the plugin re-reads the dock's mode. The possible messages are the same as for emptying,
with "washing" in place of "emptying": "Washing mode set to "…".", "Washing mode "…" sent to the robot
(application not confirmed).", "The dock did not apply the requested washing mode…", "This washing mode is
not available on this robot's dock…" and "A washing mode setting was just sent to this robot: wait a few
seconds…". The plugin never sends an order again by itself. This setting has not been verified on all
robots: in case of refusal, the message says so.

**Scenario example**: after a cleaning with washing, if "Mop washing mode" is "Léger" (Light), run "Set the
washing mode" with the code of the "Équilibré" (Balanced) mode before the next scheduled cleaning.

A change made from the Roborock app shows up within about a minute, or immediately with "Refresh".

**Wait at least 5 seconds between two washing mode settings** on the same robot, otherwise the last one is
refused. This pause is independent from the emptying mode one.

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
- the last cleaning also updates itself, with no action needed from you: the plugin re-reads the log as
  soon as the robot has finished its cleaning (including washing and emptying at the dock), then, as long
  as this cleaning does not appear in it, about 1, 3, 8 and 18 minutes later (at least 5 minutes apart
  after a failed re-read). Allow from a few seconds to a few minutes, 30 minutes at most; if the robot
  stayed unreachable for that whole time, one last re-read takes place when it comes back. The plugin
  then stops insisting until the next cleaning; the "Refresh log" button remains available.

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

Map names are displayed **in clear text**, including on robots that transmit them encoded (Roborock S7:
"%20" in place of spaces, "%E9" in place of "é"). If a name already saved still appears encoded, click
**"Refresh map list"** once (or change map): it is rewritten in clear
text, with no other action.

The same tab offers two separate blocks, each with its own button:

- **Map image** — the image of the active map, rebuilt automatically during
  cleanings (at most once every 30 seconds) and refreshable manually via "Refresh the map image".
- **Zone and point** — a **purely informational** block (no input here) showing the
  coordinate frame of the last map retrieved: the usable area in millimeters, the position of the
  charging dock and that of the robot at the time of the map, along with a conversion aid from a pixel
  in the image. It serves to prepare the values to enter into the "Clean a zone" and "Move to a point"
  commands (see "Fine-grained control" below), which remain **device commands**, not fields of this
  panel. With no map image retrieved, only general bounds are known.

### Room where the robot is

The **"Current room"** information command shows the name of the room where the robot is.

- **Where the value comes from**: it is deduced from the robot's position on the map image the plugin has
  already read. It requires no extra call to the robot or to the Roborock cloud.
- **Delay**: during a cleaning, the value is recalculated about every 30 seconds. At rest, it is re-read at
  most about a minute after a status change (for example the return to the dock).
- **Special values** (fixed, always in French, usable as is as constants in a scenario condition):
  - **"Aucune pièce"** (No room): the robot is outside any known room (an undivided corridor, a dock placed
    outside a room…).
  - **"Pièce inconnue"** (Unknown room): the position or the active map is not known, the rooms have not been
    synchronized yet, or the map has just changed.
- **Age**: hover over the tile to read the two dates. The value date is that of the entry into the room;
  the collection date is that of the last map image processed. A motionless robot therefore looks "old":
  this is normal.
- **Scenarios**: a scenario only triggers on a **real change of room**, not on every re-read.
  **Scenario example**: trigger on the "Current room" command, condition "equals Cuisine" (fictitious
  name: use the exact name of your room), action "Send a notification". The scenario only starts when the
  robot enters the room.
- **Missing command**: it is not created if the map is not divided into rooms or if the robot's position is
  not usable. It appears by itself from the first usable image.
- **Robot offline**: the last known value is kept.
- **After a map change**, the value goes to "Pièce inconnue" until you click **"Resynchronize rooms"**. Do
  the same after redividing your rooms in the Roborock app.

### "Map" panel (Home > JeeRoborock)

The map is a **panel**, not a page in the Plugins menu: it opens from the **Home > JeeRoborock** menu, and
is accessible to any user with read rights on at least one robot (not just administrators). It shows the
active map of the selected robot, its timestamp and the legend of detected rooms (segment number / name),
and refreshes itself every 30 seconds as long as the page stays open.

If the entry does not appear in **Home**, check that the **"Display desktop panel"** checkbox is checked on
the plugin management page (**Plugins > Plugin management > JeeRoborock**): it is checked automatically on
installation, but remains editable.

The page has three tabs: **Map and control** (open by default), **Dock and maintenance** and **Daily
timeline**.

#### Control panel

To the right of the map, a panel lets you **control the selected robot** without leaving the page. It
updates without reloading the page and makes no additional request to the Roborock cloud.

- **Status**: the robot's status, battery and, during a cleaning, progress.
- **Total, Room and Area tabs**: switching tabs starts nothing.
  - **Total**: cleans the whole home.
  - **Room**: tick one or more rooms. A room is not offered if its name is missing, duplicated or contains
    a comma: rename it in the Roborock app, then resynchronize the rooms. The number of rooms per order is
    limited: beyond that, start the cleaning in several runs.
  - **Area**: click and drag on the map to draw a rectangle. An area that is too small or goes outside the
    map is refused before sending. The tab is inactive if the map is unavailable.
- **Settings**: suction power, water flow and route. Only the values of **your** robot are offered, and a
  setting it does not handle is not shown. The displayed value is the one the robot actually adopted.
- **Main button**: "Clean everything", "Clean N rooms" or "Clean the area", depending on the tab. During a
  cleaning, it gives way to **Pause** (or **Resume**), **Stop** and **Return to dock**.
- **Robot offline**: the controls are inactive, with a notice. The last map stays visible.

**Cleaning a room, step by step.**

1. Open **Home > JeeRoborock**. If the entry is missing, see the **Display desktop panel** checkbox above.
2. If you have several robots, choose yours in the **Robot** list at the top of the page. With a single
   robot, there is no list.
3. Wait for the map and the status to appear. If a notice says the robot is offline or that you are not
   allowed to control it, the buttons will stay inactive (see Troubleshooting).
4. In the control panel, open the **Room** tab.
5. Tick the room in the list, or tap it on the map: it is highlighted. Tick several if needed. Nothing is
   sent to the robot at this stage.
6. If you wish, set the suction power, the water flow and the route.
7. Click the main button, **Clean 1 room** (or **Clean N rooms**). This click, and only this one, sends the
   order.
8. Follow the status and progress at the top of the panel. Use **Pause**, **Stop** or **Return to dock** if
   needed.

If the room does not appear in the list, or if the button stays inactive, see the Troubleshooting table.

**Interactive map.** The map itself is used to choose and to draw. Nothing is sent to the robot until you
click the main button.

- **Room names**: each room carries its name, written on the map. A room with no name is shown as "Unnamed
  room". If the map does not allow rooms to be delimited, a message says so: choose the rooms from the list
  in the Room tab instead.
- **Choosing a room**: tap or click a room to select it (it is highlighted), tap it again to deselect it.
  The selection is the same as the Room tab's list: ticking or unticking on one side updates the other. You
  can choose several rooms.
- **Rooms that cannot be chosen**: a room with no name, a duplicate, or whose name contains a comma keeps
  its label, but selecting it is refused, with an explanation. Rename it in the Roborock app, then
  resynchronize the rooms from the device page.
- **Room unknown on the current map**: after rooms are redivided or a floor change, a room that was already
  ticked may no longer exist on the map. It is flagged "Room unknown on the current map" and the start
  button stays inactive as long as it is ticked. Untick it, or resynchronize the rooms from the device
  page.
- **Outdated map**: if the displayed map is an old image (robot unreachable), selecting on the map is
  impossible ("Outdated map: selection impossible"). With no map at all, the Room and Area tabs are
  inactive.
- **Drawing an area** (Area tab): click and drag to draw a rectangle. Drag it to move it, pull one of its
  corners to resize it, or click **Clear the area** to remove it. The rectangle is kept when the map
  refreshes, unless the robot changes map floor or you change robot.
- **No-go zones and virtual walls**: those you defined in the Roborock app are drawn on the map, with a
  legend. They are **read-only**: you neither create nor modify them here. A change made in the app only
  appears at the next map retrieval. If your robot has none, or does not provide any, nothing is drawn and
  no message appears. An area you draw over a no-go zone is not blocked by the plugin.
- **Touch screen**: tapping, drawing and moving work on tablets and phones.

**Rights.** An order is only sent on your click, and only if Jeedom allows you to run the robot's commands.
Rights are set in Jeedom's user management, robot by robot. The "user" profile has all rights by default:
to restrict, use a restricted profile. An access code or a confirmation set on a command is respected.

| Your situation | What you see | What you can do |
|---|---|---|
| Administrator | All enabled robots | Everything |
| Execute right on the robot | The robot, its map, its status, the dock and the timeline | Everything: select, draw, start, pause, stop, dock |
| Read-only | The robot, its map, its status, the dock and the timeline, with the notice "You are not allowed to control this robot." | View, select rooms and draw an area (nothing is sent). All action buttons are inactive. |
| No right on the robot | Nothing: the robot is not in the list | Nothing. With no accessible robot at all, the page shows "No Roborock robot accessible with your account." |

A robot that is **disabled** in Jeedom is offered to nobody, administrators included. A direct link to a
robot you are not allowed to read is ignored. Displaying the map, the panel and the timeline costs no call
to the Roborock cloud.

**Remembered robot.** The chosen robot is remembered in your browser (not from one device to another). A
direct link to a specific robot (address parameter) takes precedence over this choice.

**Caution.** If you have just stopped a room cleaning, avoid starting "Clean everything" right away: the
robot may resume the interrupted cleaning instead of starting over on the whole home. Check what it is
doing; if needed, stop it and start again.

**Vacuum then mop.** This block chains two cleanings over the same scope: a **first vacuum-only pass**,
then a **second mop-only pass**. It only appears if your robot can mop (otherwise neither the block nor
the matching commands are created).

- **Starting**: in the **Total** tab, the **Vacuum then mop** button handles the whole home; in the
  **Room** tab, it handles the ticked rooms. It does not exist for the Area tab. The requested number of
  passes (see "Fine-grained control") applies to both passes.
- **Displayed status**: the **Sequence** line shows where the chain stands: "Passage 1 sur 2 :
  aspiration" (pass 1 of 2: vacuuming), "En attente de la base" (waiting for the dock), "Passage 2 sur 2 :
  lavage" (pass 2 of 2: mopping), then, at the end, "Séquence terminée" (sequence finished), "Séquence
  annulée" (sequence cancelled), "Séquence interrompue" (sequence interrupted), "Le second passage n'a pas
  pu démarrer" (the second pass could not start) or "Séquence abandonnée" (sequence abandoned). When the
  sequence stops without reaching its end, the **reason** is shown below it (see Troubleshooting).
- **Cancel**: the **Cancel the sequence** button appears as long as a sequence is active. It stops the
  robot, restores its original settings and prevents the second pass.
- **Closing the panel interrupts nothing**: the sequence is tracked in the background by the plugin, not by
  your browser. Reopen the panel to see the status again.
- With read-only rights, the status is visible but the buttons are inactive.

#### "Dock and maintenance" tab

This tab gathers, for the selected robot, the docking station and maintenance. It updates like the control
panel and **uses no quota** of the Roborock cloud. The detail of each command is in the "Dock, consumables
and maintenance" section above. It is made of three blocks; **only what your robot can do appears**.

- **Actions**: **Empty the bin**, **Wash the mop**, **Dry the mop** and **Stop drying**, as well as the
  **Emptying mode** and **Mop washing mode** lists.
- **Status**: bin emptying, mop washing and drying, clean water, dirty water, mop installed, water
  shortage and **dock incident**. This incident is separate from the robot's error: a robot error is not
  shown there. It is also repeated in a red banner, and the **last update** is shown at the top of the tab.
- **Consumables**: remaining lifetime as a percentage. At **10% or less**, the **To replace** mention
  appears, with an alert banner. The **Reset** button sets the counter back to zero after confirmation, to
  be done once the part is replaced. It does not exist for the bag.

If the robot has no dock, the tab shows **This robot has no dock.**

**Operation in progress.** As long as a dock operation is in progress, **Empty**, **Wash** and **Dry** are
inactive and carry the notice "Operation in progress". The same goes right after an order is sent: the
button stays inactive until the status changes, and for **2 minutes** at most. **Stop drying** is only
active **during a drying**.

**"Robot not at the dock" refusal.** A dock operation requires the robot to be at its dock. Otherwise the
plugin refuses it and says so (see the troubleshooting table). It **never** sends the order again by
itself: bring the robot back to the dock, then start again.

**Robot offline.** The buttons are inactive, with a notice. The last known states stay displayed, with the
date of their last update.

**Rights.** With read-only rights, the tab is view-only: no button is active and a notice explains why.

#### "Daily timeline" tab

This tab shows, on a **time strip**, what the robot did over a day: a colored band, one color per state.
It is **read-only** and **uses no quota** of the Roborock cloud: it only re-reads what the plugin has
already recorded. It is only visible if you have **read** rights on the robot.

**Legend.** Each color matches a category:

| Category | Meaning |
|---|---|
| **Cleaning** | The robot is vacuuming or mopping. |
| **Returning to dock** | The robot is heading back to its dock. |
| **Charging** | The robot is sitting on its dock. |
| **Bin emptying** | The dock is emptying the bin. |
| **Mop washing** | The dock is washing the mop. |
| **Mop drying** | The dock is drying the mop. |
| **In error** | The robot is in error. |
| **Offline** | The robot does not answer. |
| **Other state** | Any state that has no color of its own. |
| **Unknown** | No information received during this period. |

**"Unknown".** This hatched area covers a period **with no data**: daemon stopped, Jeedom switched off. The
plugin **never** extends the last known state. A period is "Unknown" beyond **15 minutes** with no news
from the robot.

**Finished cleanings.** Under the strip, a thin dark band (**Cleaning finished**) highlights the cleanings
of the **cleaning log** that overlap the displayed day.

**Detail.** Hover (mouse) or tap (touch screen) a period to show its detail under the strip.

**Navigation.** The **Previous day** and **Next day** buttons change the day. The **last 7 days** are
kept; older ones are deleted automatically. Times are those of the **Jeedom time zone**. A day with no
record shows **No data for this day.**

**The history starts at the installation of the update.** The plugin has no way to reconstruct the past:
earlier days have no data.

#### Mobile panel (Jeedom app and mobile version)

The control panel is also available on a phone, in the Jeedom mobile app and in the web mobile version of
Jeedom.

**Where to find it.** Open **Home**, then **Plugins**, then **JeeRoborock**. The dedicated tab of the mobile
app's custom menu is reserved for **administrators**: this is a Jeedom limitation, not the plugin's. After
the plugin update, if the entry does not appear, **resynchronize the app**. The administrator can hide this
panel in the plugin configuration, on the Jeedom side.

**What it contains:**

- the robot choice (if you have several);
- the map, with clickable rooms and no-go zones;
- the **Total**, **Room** and **Area** tabs: for an area, draw the rectangle with your finger on the map,
  then move it or resize it by its corners;
- the settings (suction, water flow, route) when the robot offers them;
- the **Pause**, **Resume**, **Stop** and **Return to dock** buttons;
- **Vacuum then mop**, when the robot allows it.

**What it does not contain.** The **Dock and maintenance** page, the **daily timeline** and the table of
detected rooms are not available on mobile: open Jeedom's Map page on a computer.

**Rights.** They are the same as on the desktop: with read-only rights, the panel is view-only.

**Updates.** The display updates by itself as long as the panel is on screen. It is suspended when the app
goes to the background and resumes when you come back.

**After a plugin update.** If the panel behaves oddly, close the app completely then reopen it: an old
version may have stayed in cache.

## Fine-grained control

Depending on the capabilities detected on your robot, the following commands may appear:

- **Suction power** and **water flow** — an information command shows the current level, an action
  command (drop-down list) lets you choose another one among those actually supported by your robot.
- **Mop route** and **cleaning mode** (vacuum only / mop only / vacuum and mop) — same principle:
  information + action drop-down list.
- **Clean rooms** — one command per detected room ("Clean <room name>"), plus a generic
  **"Clean rooms (names separated by commas)"** command that accepts a free-text list of names. As with
  usages, the command name follows renamings made in the Roborock app at the next synchronization —
  including when the room name contains an apostrophe, an ampersand, a hash sign or a percent sign
  ("Salle d'eau", for example) — unless you have manually customized this name in Jeedom, in which case
  your customized name is kept. To clean in several passes, see "Number of passes" below.
- **"Clean a zone (x1,y1,x2,y2 in mm)"** — takes four coordinates `x1,y1,x2,y2` in millimeters and cleans
  the corresponding rectangle. The number of passes is set as for rooms (see below).
- **Number of passes** ("Clean rooms" and "Clean a zone" commands) — fill in the command's **Message**
  field, then enter 1, 2 or 3 (in digits) in the **Title** field.
  - **It is a parameter of the current order, not a setting.** There is no "Number of passes" command to
    set once and for all: give it with each order, otherwise it is a single pass. It is never stored by
    the robot or by the plugin.
  - Empty Title field: a single pass, as before.
  - A number of three digits or more ("100", "2024") or text ("two") is ignored: the cleaning is done in
    one pass, with no message.
  - 0, a number from 4 to 99, a signed or decimal number are refused (see Troubleshooting).
  - The same number applies to each room of the order; for a zone, it applies to the zone.

  | Title field | Result |
  |---|---|
  | (empty), 1 | One pass |
  | 2, 3 | Two or three passes |
  | 0, 4, 10, 99 | Refused: a whole number from 1 to 3 is expected |
  | -1, +2, 2.5, 2,5 | Refused: signed or decimal number |
  | 100, 2024, two, x2 | Ignored: a single pass, with no message |

  **Scenario example**: "Clean rooms" action with, in the Message field, "Cuisine, Salon" (fictitious
  names) and, in the Title field, 2: both rooms are cleaned in two passes. For the zone, the Message field
  receives `x1,y1,x2,y2` and the Title field 2 or 3.
  - The "Clean <room>" buttons always do a single pass.
  - When the Message field is empty, the Title field keeps its usual role (room names or coordinates),
    despite its label.
  - The field is labeled "Number of passes (1 to 3)" only if the robot reports that it handles repetition.
  - The repetition setting of the Roborock app is never modified. Without a number of passes, the robot
    applies its own setting, as before.
  - A number of passes of 2 or 3 is refused by the plugin if the robot, re-read just before the order,
    does not report that it handles repetition. If the re-read fails, the order is sent and it is the
    robot that decides.
- **"Move to a point (x,y in mm)"** — takes two coordinates `x,y` in millimeters.
- **Vacuum then mop** — chains a vacuum-only pass then a mop-only pass. Four commands, created only if the
  robot can mop:
  - **Vacuum then mop (rooms separated by commas, empty for the whole home)** (action): empty **Message**
    field = whole home; otherwise, room names separated by commas (as for "Clean rooms"). The **number of
    passes** goes in the **Title** field (1 to 3), for the "rooms" scope only; it applies to both passes.
    For the whole home, there is no number of passes: a single pass per step.
  - **Cancel the sequence** (action): stops the current sequence. With no active sequence, it answers that
    there is nothing to cancel.
  - **Sequence status** (information): "Aucune séquence" (no sequence), "Passage 1 sur 2 : aspiration",
    "En attente de la base", "Passage 2 sur 2 : lavage", "Séquence terminée", "Séquence annulée",
    "Séquence interrompue", "Le second passage n'a pas pu démarrer" or "Séquence abandonnée" (see the
    translations in the "Vacuum then mop" block above).
  - **Sequence end reason** (information): "Aucun" (none), or the reason why the sequence stopped (see
    Troubleshooting). These two pieces of information are not historized.

  **Scenario example**: "Vacuum then mop" action with "Cuisine, Salon" (fictitious names) in the Message
  field; a second block can wait for "Sequence status" to equal "Séquence terminée".

  **How the sequence runs.**
  - The second pass only starts once the **normal end of the first pass is confirmed by the robot's log**
    and the robot has been **charging steadily for 30 seconds** at its dock (the time of any emptying or
    washing). A robot that is emptying is never restarted: the plugin waits.
  - **Maximum wait for the dock: 15 minutes** after the end of the first pass. Beyond that, the second pass
    is not started.
  - The plugin checks that the robot **did start**: with no start observed within **2 minutes**, the pass
    is declared without effect.
  - **Maximum duration of a pass: 6 hours.** Beyond that, the sequence is stopped.
  - At each end (successful, cancelled or interrupted), the robot's **original settings** (suction, water
    flow, route) are **restored**. During the sequence, the plugin replaces them with "vacuum only" then
    "mop only" settings.
  - **During a sequence, other cleanings are refused**: cleaning rooms, a zone, running a routine, or
    "Start" (except to **resume** a paused cleaning). Cancel the sequence first.
  - **Stop** or **Return to base**, from Jeedom or from the mobile app, end the sequence: the second pass
    is not started.
  - **No automatic retry**: if the second pass cannot start, nothing is sent again. Start the sequence
    again yourself.
  - Starting a sequence on a robot that is already cleaning (or paused) is refused.

After a setting of suction power, water flow, mop route or cleaning mode, the plugin re-reads the robot's
status to check that it has taken it. It allows up to about twelve seconds, without sending the order
again: if the robot takes it right away, the response is not slowed down. The "not applied" message only
appears if the robot still does not have the value after this delay. If you chain two settings very
quickly on the same robot, only the last one is checked: the previous one is reported as "transmis au
robot (application non confirmée)" (sent to the robot, application not confirmed), without error. The
same message appears if the robot stops responding during the check.

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

### Several robots on the same account

A robot that is switched off, discharged or off Wi-Fi no longer prevents you from controlling and
tracking the other robots on your account: it simply shows as **offline**. Reconnection attempts to this
robot do **not** consume the Roborock quota (see "Roborock quotas").

Once switched back on, the robot becomes controllable **again by itself**, with no new authentication or
reinstallation. Allow **6 minutes at most** after its connection returns: the wait between two attempts
gradually lengthens, up to **5 minutes**.

During this short interval, the robot may already appear **online** while its commands are still
refused as **offline**. Wait a few minutes, then try again.

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
| "Le robot vide son bac à poussière : l'ordre de nettoyage n'a pas été envoyé…" (The robot is emptying its dust bin: the cleaning order was not sent…) | A cleaning order ("Start", "Clean rooms", "Clean <room>", "Clean a zone") was given while the dock is emptying the bin; the robot would have ignored it | Wait for the emptying to finish (a few seconds to a minute), then send the order again. In a scenario, wait until the robot status is back to "En charge" (Charging) before retrying |
| "A "vacuum then mop" sequence is in progress on this robot: cancel it before starting another cleaning." | A cleaning (rooms, zone, routine, "Start") was requested during a sequence | Click "Cancel the sequence", or wait for it to end, then start again |
| "The robot already has a cleaning in progress or paused: stop it before starting "vacuum then mop"." | The sequence was started while the robot was cleaning or paused | Stop the cleaning, then start the sequence again |
| Sequence interrupted: "The robot was stopped or sent back to the dock during the sequence…" | You (or the mobile app) used Stop or Return to base | Normal: the second pass is not started. Start the sequence again if needed |
| Sequence interrupted: "The robot stopped with an error during the sequence…" | The robot reported an error (stuck, missing bin…) | Check the robot's status, fix the incident, start again |
| "The robot accepted the cleaning command but did not start." | No start observed within 2 minutes | Check the robot's status (bin, emptying in progress…), then start again |
| "The first pass did not end normally according to the robot's log…" | The robot's log does not classify the first pass as ended normally | The second pass is not started as a precaution: check the cleaning log, start again if needed |
| "The normal end of the first pass could not be confirmed by the robot's log within the waiting time…" ("Le second passage n'a pas pu démarrer") | The robot's log did not confirm the end of the first pass within 15 minutes | The plugin never starts the mopping without this confirmation: start the sequence again, or start a mop-only cleaning by hand |
| "The robot did not become available again within the maximum waiting time…" | After the first pass, the robot did not come back to charge at its dock (steadily for at least 30 seconds) within 15 minutes (taken off the dock, emptying stuck…) | Put the robot back on its dock, then start the sequence again |
| "The robot was restarted outside the sequence…" | A cleaning was started (for example from the mobile app) while waiting for the dock | The second pass is not started: start the sequence again once the robot is at the dock |
| "The current pass did not complete within the maximum expected time…" | A pass lasts more than 6 hours | The sequence is stopped: check the robot |
| "The plugin could not track the robot for several minutes…" | Robot or network unreachable for several minutes | The robot may have continued its pass; its original settings are not restored: check its cleaning mode |
| "The robot's original settings could not be restored…" | The restoration failed at the end of the sequence | Check and fix the robot's cleaning mode |
| "Séquence abandonnée" (sequence abandoned): "The sequence is no longer tracked by the daemon…" | The daemon was stopped or restarted during the sequence (or the daemon died) | The second pass will not be started; the robot may have continued its pass, and its original settings are not restored: check them, then start again if needed |
| "The plugin's Roborock session changed during the sequence…" | The account was changed or removed during the sequence | Same consequence: settings not restored, to be checked |
| "No "vacuum then mop" sequence in progress on this robot: nothing to cancel." | **Cancel the sequence** was requested while no sequence is active (it had already ended) | Nothing to do: check the **Sequence** line |
| "Cancellation recorded: the robot will be stopped…" | The cancellation is taken into account, but an order is still being sent | Normal: wait a few seconds; the status goes to "Séquence annulée" |
| "Sequence cancelled, but stopping the robot failed…" or "Sequence cancelled; the robot's original settings could not be restored." | The robot did not confirm the stop, or restoring its settings failed | Check the robot's status, stop it from the panel if needed, and check its settings |
| "Vacuum then mop" button missing | The robot cannot mop, or the Area tab is open (the sequence only exists for Total and Room) | Normal: open the Total or Room tab; on a robot with no mopping, the function does not exist |
| "Invalid number of passes: enter a whole number from 1 to 3, or leave the field empty for a single pass." | The Title field of a room or zone cleaning (with the Message field filled in) contains a refused number: 0, 4 to 99, signed or decimal | Enter 1, 2 or 3 in digits, or leave the field empty for a single pass |
| "Number of passes not supported by this robot: it does not report supporting repetition…" | A number of passes of 2 or 3 was given, but the robot does not report that it handles repetition | Empty the number-of-passes field: the cleaning is then done in a single pass |
| "Invalid time range: enter a start and an end in HH:MM format, between 00:00 and 23:59." (Do Not Disturb, off-peak hours) | One of the two "Set the … time range" fields is empty, badly formed (22h00, 2200, 22:5) or out of bounds (24:00, 22:60) | Enter both times in HH:MM format (7:30 is accepted), between 00:00 and 23:59, then run again |
| "Invalid time range: the start and end … must be different." | The start and end of the range are identical | Choose two different times (a range crossing midnight, like 22:00 → 07:00, is accepted) |
| "The robot returned no usable … time range: set the range…" | "Enable" (Do Not Disturb or off-peak hours) has no saved range to re-apply | Run "Set the … time range" with a start and an end: this also enables the function |
| "Invalid volume: enter a whole number between 0 and 100." | The value is empty, decimal (50.5), negative or above 100 | Enter a whole number from 0 to 100; in a scenario expression, round with `round(...)` |
| "This emptying (or washing) mode is not available on this robot's dock: refresh its status before trying again." | The requested mode code is not known for this dock (outdated list, or wrong code in a scenario) | Run "Refresh", reload the device page, then choose a mode from the command's list |
| "A … command (or setting) was just sent to this robot: wait a few seconds before sending another one." (child lock, Do Not Disturb, off-peak hours, volume, emptying mode, washing mode) | Two orders of the same type on the same robot less than 5 seconds apart | Wait at least 5 seconds; in a scenario, insert a 5-second pause between the two actions |
| "The robot (or the dock) did not apply …: the state read back does not match the request." (child lock, Do Not Disturb, off-peak hours, volume, emptying mode, washing mode) | The robot answers but did not adopt the setting by the end of the check delay (a few seconds, up to about twelve) | Check the value shown by the matching information command (it shows what the robot actually adopted), send the order again; if it keeps happening, try with the robot at rest or at its dock |
| "This maintenance operation is not available on this robot's dock." | This robot's dock does not support this action | This is normal: the command should not appear if the dock does not support it; refresh the robot's status |
| "The list of routines received from the Roborock cloud is incomplete: as a precaution, no routine was deleted." | The cloud response was truncated, or this robot has more than 64 usages | Run the synchronization again later; nothing was lost in the meantime |
| "The Roborock terms of use have not been accepted." (or "have changed") | Roborock requires accepting (or re-accepting) its terms of use | Open the Roborock mobile app, accept the terms shown, then try again from Jeedom |
| "Robot unknown to the daemon." | The Jeedom device is no longer recognized by the daemon (restart, robot removed from the account…) | Run "Synchronize devices" again |
| "The Roborock cloud is unreachable." | Jeedom cannot reach Roborock's servers | Check the Jeedom server's Internet access |
| A message about an **exceeded timeout**, a **failed connection**, or "several communication attempts failed" | The robot or the Roborock cloud took too long to respond: a transient network incident, or a very busy robot | Try again after a minute; if it keeps happening, check the robot's Wi-Fi connection and the Jeedom server's Internet access |
| "The robot is busy.", "The robot refused the action in its current state." or "The robot reported an error while executing the command." | The robot cannot carry out this request in its current state (cleaning in progress, full bin, mechanical incident…) | Check the robot's status (the "Status" command, or the mobile app), resolve the reported incident then retry the action |
| "This feature is not available on this robot model." or "The robot does not recognize this command." | The robot does not implement this feature, even though the command exists in Jeedom | No action will fix this: this feature does not exist on this hardware, hide the command if it bothers you |
| "No code request in progress (the daemon may have restarted): request a new code." | The daemon restarted between sending and validating the code | Click "Send a code" again, then validate the new code received |
| "… transmis au robot (application non confirmée)." (sent to the robot, application not confirmed) after a setting | The plugin could not check that the robot took the value: another setting was sent right after on the same robot, or the robot stopped responding during the check. This is not an error | Check the value shown by the matching information command; send the setting again if it is not the right one |
| A setting (suction, water flow, route, cleaning mode) is not applied | The robot still does not have the value about twelve seconds after receiving it: it refuses this setting in its current state (generally: not at rest) | Try again once the robot is at rest or at its dock |
| "This suction power / water flow / route / cleaning mode is not available on this robot." | The list of levels known by Jeedom is outdated (the robot no longer reports this value) | Refresh the robot's status then try again |
| "You are not allowed to control this robot." (control panel and Dock and maintenance tab), greyed-out buttons | Your Jeedom account only has read rights on this robot | Ask an administrator to grant you execute rights on this robot (Jeedom user management) |
| "No Roborock robot accessible with your account." (or "Device not found or inaccessible.") | No enabled robot on which your account has read rights; the same message is used for a non-existent or disabled robot | Ask an administrator for read rights, or check that the robot is enabled |
| "401 - Unauthorized access" when opening the Map page | Your Jeedom session expired | Log back into Jeedom |
| The JeeRoborock entry does not appear in Home | The **Display desktop panel** checkbox is unchecked in the plugin management | Check it (see "Map" panel (Home > JeeRoborock)) |
| "Robot offline: commands are inactive until it comes back." | The robot does not answer to the Roborock cloud | Check its power and Wi-Fi; the buttons become active again when the robot returns, with nothing to reload |
| "Feature unavailable for this robot." or a button missing from the panel | The robot does not handle this setting or this action | Normal: the panel only offers what your robot can do |
| "Command refused by the robot." (with no further detail) | The order was refused with no more specific message | Check the robot's status (bin, error, not at the dock), then try again |
| The main button stays inactive, Room tab: "No room available for this robot: synchronize its rooms from the device page." | No room has been synchronized yet | Click "Resynchronize rooms" in the Device tab |
| "Too many rooms selected: start the cleaning in several runs." | The number of rooms per order is limited | Untick some rooms, start in several runs |
| "Some rooms cannot be selected here…" or "This room cannot be selected here…" | The room has no name, its name is duplicated or contains a comma | Rename it in the Roborock app, then resynchronize the rooms |
| "Room unknown on the current map: resynchronize the rooms from the device page." | A ticked room no longer exists on the map (redivision, floor change) | Untick it, or resynchronize the rooms; the start button stays inactive as long as it is ticked |
| "Outdated map: selection impossible." or "The map does not allow rooms to be delimited: select them from the list." | The displayed map is an old image, or contains no room outlines | Choose the rooms from the Room tab's list; the map renews itself during cleanings |
| "Map unavailable: cannot draw an area.", "Area too small: draw a larger rectangle." or "The area must be entirely within the map." | No usable map, or the rectangle is too small or goes beyond the map | Draw a larger rectangle, entirely on the map; with no map, clean by room or in Total |
| "This robot has no dock." (Dock and maintenance tab) | The robot has no docking station | Normal: nothing to do |
| **Empty**, **Wash**, **Dry** buttons inactive, notice "Operation in progress" | A dock operation is in progress, or an order was just sent (2 minutes at most) | Wait; **Stop drying** is only active during a drying |
| "Dock incident" or "One or more consumables need replacing." | The dock reports an incident, or a consumable is at 10% or less | Fix the incident; replace the part then use **Reset** |
| "No data for this day." or "Timeline currently unavailable." (timeline) | No state recorded that day (plugin installed more recently, or day outside the last 7); or the read failed | Change day; for the unavailability, reload the page. The message "Invalid day or outside the retention period." means a day more than 7 days old was requested |
| Mobile: "The panel cannot be loaded: go back to the home page, then reopen it." or "The control panel cannot be loaded. Reload the page." | The robot list or the panel's scripts could not be loaded (network, session, old version in cache) | Reopen the panel; if needed, close the Jeedom app completely then reopen it |
| Mobile: "Not available on mobile" | The Dock and maintenance page, the timeline and the table of detected rooms do not exist on mobile | Normal: open Jeedom's Map page on a computer |
| "Unknown room.", "no known room" or "several rooms share this name" | The entered name does not match any detected room, no room has been synchronized yet, or the name is ambiguous | Resynchronize rooms from the Device tab, use the exact name from the Roborock app, or the command dedicated to this room rather than the generic command |
| The "Current room" command stays on "Pièce inconnue" | The rooms have never been synchronized, or the active map changed | Click "Resynchronize rooms" in the Device tab |
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

## Updating the plugin

The manual control features (panel, interactive map, dock, "vacuum then mop", daily timeline, mobile
panel) require **no action on your part** after the update: no configuration to redo, no device to
recreate. Two steps may nevertheless be useful: restart the daemon (otherwise states show up as "Other
state" on the timeline) and, on mobile, resynchronize or fully close the app.

## Known limitations

- The plugin only controls robots compatible with Roborock's V1 protocol, via the cloud. Older robots
  (A01 protocol) are not supported.
- Labels produced by the robot itself (status, error, dock status, consumable names) are **always in
  French**, whatever language is chosen for the Jeedom interface. The same goes for the "Aucune pièce" and
  "Pièce inconnue" values of the "Current room" command.
- A map change made from the mobile app is now automatically detected, in the background, within about
  a minute: the active map, image and reference frame of the map update with no action from you (the
  room list, however, is cleared and awaits a click on "Resynchronize rooms"). During this short delay,
  the configuration may still show the old floor, and an already-open Device page does not refresh
  itself: reload it. Likewise, the "Current room" command may briefly (a minute at most) designate a room
  of the old floor, then goes to "Pièce inconnue" until the rooms are resynchronized.
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
- A robot that is switched off or off Wi-Fi and reconnects becomes controllable again by itself, but after
  a delay that can reach **6 minutes** (see "Several robots on the same account"): this delay cannot be
  configured.
- Refusing a cleaning order while the bin is being emptied only concerns the "Vidage du bac à poussière"
  (emptying the dust bin) status: the dock's other states (washing, drying) do not trigger this refusal. It
  concerns neither routines ("usages") nor "Move to a point". No order is queued: it is up to you (or your
  scenario) to send it again.
- The automatic update of the last cleaning is **bounded**: five re-reads at most, within 30 minutes after
  the end of the cleaning. Beyond that, the plugin stops insisting; use "Refresh log".
- A map name already saved in encoded form (before the plugin update) stays encoded until the first
  "Refresh map list" or map change.
- Reading room names (the "Rooms" panel of the Device tab) requires the robot to be **online**: it
  fails if the robot is unreachable at the time of the click.
- The map view (the "Home > JeeRoborock" panel) triggers nothing by itself (an order is only sent on your
  click in the control panel) and starts no update: it simply displays, every 30 seconds, the last
  already-known image. This image is only rebuilt during cleanings; at rest, it may therefore date back to
  the robot's last pass.
- Mobile panel: **reduced** version of the control panel. Neither the Dock and maintenance page, nor the
  daily timeline, nor the table of detected rooms are available on mobile: they are only on a computer.
  The dedicated tab of the Jeedom app's custom menu is reserved for administrators. The panel has not been
  tried on every phone: a device may show display defects.
- **No-go zones and virtual walls**: shown on the map **read-only**. To create, move or delete them, use
  the Roborock app; the plugin does not block an area drawn over a no-go zone.
- **Robot offline**: the panel, the Dock and maintenance page and the "vacuum then mop" chain accept no new
  order. Only **Cancel the sequence** remains possible during a sequence. The last states and the last map
  stay displayed.
- **Two robots, two sequences**: each robot has its own "vacuum then mop" sequence, tracked and cancelled
  independently of the other.
- **Dock and maintenance**: on a robot **with no dock**, the tab only shows "This robot has no dock.". On
  a robot with a dock, only the actions and states that this robot can do appear.
- **Daily timeline**: the strip is rebuilt from the states that the **plugin itself recorded** (nothing is
  asked of the Roborock cloud). It contains no data from before the update was installed. Only the **last 7
  days** are kept; older ones are deleted. Beyond a very high volume of records for a single day, the
  recording for that day stops: the end of that day's strip stays empty.
- "Daily timeline" strip: **"Offline"** means the robot **does not answer**; a single timeout is enough, it
  is not necessarily a long outage.
- On the strip, a **pause** during a cleaning, the **move to a target**, **mapping** and **fitting or
  removing the mop** show up as **Other state**. The **drying** that takes place while charging shows up
  as **Charging**: "Mop drying" only covers drying reported as such by the robot.
- After a plugin update, as long as the **daemon has not restarted**, states show up as **Other state** on
  the strip. Restart the daemon.
- The accuracy of **"Unknown"** is on the order of **a few minutes**: its start may precede the actual stop
  by a few minutes. An outage of **less than 15 minutes** without a daemon restart does not show up.
- Only the **last 10 cleanings** of the log can be highlighted on the strip.
- The commands absorbed by the dashboard tile (battery, cleaning, error, connected, online and the five
  control actions) are hidden only once, when the tile is created. If you manually unhide one, the
  plugin never hides it again: your choice is kept.
- On an installation updated from an old plugin version, a one-off technical migration may have
  re-enabled history logging for the "Error" command: if you do not want to log this
  command's history, disable it manually on its configuration.
- Only the **Roborock Qrevo Curv** is tested. The capabilities added by the parity with Home Assistant
  (dock consumables and tanks, child lock, Do Not Disturb, off-peak hours, volume, dock modes, number of
  passes, current room) come with **no guarantee** on another model, the Roborock S7 included: the plugin
  creates the commands that the robot reports or answers, without having been able to verify their actual
  effect on each hardware. An accepted order may be refused by the robot; this is then reported (see
  Troubleshooting).
- The wear of the dock's **dust bag** is read-only: the plugin has no action to reset it. Consumable
  percentages may differ slightly from those of the app.
- Device settings (child lock, Do Not Disturb, off-peak hours, volume, dock modes) are **not pushed** to
  the plugin: a change made from the Roborock app or the robot's button only shows up in Jeedom at the
  next re-read (about a minute, or "Refresh").
- The plugin **never** sends a setting order again by itself after a refusal or a failure: send it again
  yourself. Two orders of the same type on the same robot must be at least 5 seconds apart.
- "Disable" for Do Not Disturb or off-peak hours normally keeps the saved range, but this behavior depends
  on the robot and is not confirmed.
- The number of passes is a parameter of each room or zone cleaning order, never a stored setting. For a
  zone, the way the robot interprets the repetition value could not be confirmed on all models: if "2"
  does not give two passes on your robot, report it. The "Clean <room>" buttons stay at a single pass.
- The emptying and washing mode lists come from the library used by the plugin, not from the dock: a mode
  of the Roborock app may be missing, a mode offered may be refused by the dock. An unknown mode code is
  displayed as "Mode inconnu (N)".
- The "Current room" command depends on the last map image read: it may lag by about a minute at rest, and
  keeps its last value if the robot is offline. After a map change made from the app, it may briefly
  designate a room of the old floor before going to "Pièce inconnue" (see above).

- **Vacuum then mop**: if you change a robot setting (suction, water flow, route) during a sequence, the
  end-of-sequence restoration **overwrites** it. If the plugin stops tracking the sequence ("Séquence
  abandonnée", daemon restart) or if the account is changed, the original settings are **not restored**:
  check them. A cleaning started from the **mobile app** during a pass is not refused by the plugin: it is
  noticed afterwards and the sequence stops without starting the second pass. If the robot does not report
  the cleaning state, the end of a pass may go undetected: the sequence then stops at 6 hours. A custom or
  "smart" original mode is restored to the nearest standard setting.

This page is updated with each new feature shipped by the plugin.
