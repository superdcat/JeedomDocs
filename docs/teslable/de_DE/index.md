# Plugin Tesla BLE

Mit diesem Plugin steuern Sie von Jeedom aus das Laden, die Klimatisierung und einige Grundfunktionen Ihrer **Tesla**-Fahrzeuge, **per Bluetooth (BLE)** und ohne die Cloud-API von Tesla.

Jeedom spricht nicht direkt mit dem Fahrzeug: Es stützt sich auf einen [TeslaBleHttpProxy](https://github.com/superdcat/TeslaBleHttpProxy) (den für dieses Plugin gepflegten Fork, abgeleitet vom Projekt von [wimaha](https://github.com/wimaha/TeslaBleHttpProxy)), der auf einem kleinen Gerät mit Bluetooth (einem Raspberry Pi, siehe [Den Raspberry Pi auswählen und installieren](#den-raspberry-pi-auswahlen-und-installieren)) in Reichweite des Fahrzeugs läuft, typischerweise in der Garage. Das Plugin fragt diesen Proxy per HTTP in Ihrem lokalen Netzwerk ab.

```
Jeedom  --HTTP-->  TeslaBleHttpProxy (Raspberry Pi)  --Bluetooth-->  Fahrzeug
```

## Voraussetzungen

- Jeedom 4.5 oder höher, unter Debian 11 oder 12.
- **TeslaBleHttpProxy 2.3.0 oder höher**, installiert, funktionsfähig und von Jeedom aus erreichbar. Das **Fork-Image** `ghcr.io/superdcat/tesla-ble-http-proxy` wird empfohlen; das Image von wimaha (2.3.0 oder neuer) wird weiterhin akzeptiert. Das Plugin ignoriert das Suffix `-tb.N` der Fork-Versionen: `2.3.0-tb.2` gilt als konform mit „mindestens 2.3.0“. Vollständige Schritt-für-Schritt-Anleitung auf einem Raspberry Pi Zero 2 W: [Den BLE-Proxy installieren](installation-proxy.md).
- Der **mit dem Fahrzeug gekoppelte Schlüssel des Proxys**. Dieser Schritt erfolgt vollständig in der Oberfläche von TeslaBleHttpProxy (Schlüssel erzeugen, dann mit Ihrer Schlüsselkarte im Fahrzeug bestätigen): siehe [Den BLE-Proxy installieren](installation-proxy.md#8-den-schlussel-erzeugen-und-mit-dem-fahrzeug-koppeln).
- Die **VIN** jedes zu steuernden Fahrzeugs (unten auf dem Hauptbildschirm der Tesla-App sichtbar).

> **Tipp**
>
> Bevor Sie das Plugin konfigurieren, prüfen Sie, ob der Proxy antwortet, indem Sie in einem Browser `http://<Proxy_IP>:<port>/api/proxy/1/version` (Version des Proxys) und dann `http://<Proxy_IP>:<port>/api/1/vehicles/<VIN>/body_controller_state` öffnen. Sie müssen eine JSON-Antwort erhalten.

### Die Version des Proxys prüfen und aktualisieren

Das Plugin verlangt **TeslaBleHttpProxy 2.3.0 oder höher**. Mit diesen Schritten ermitteln Sie die Version Ihres Proxys und aktualisieren sie bei Bedarf. Beim Fork-Image hat die Version die Form `2.3.0-tb.2` (Basisversion von wimaha, dann die Versionsnummer des Forks).

**1. Die aktuelle Version auslesen**

1. Öffnen Sie auf einem Computer im selben Netzwerk wie der Proxy einen Browser.
2. Geben Sie in die Adressleiste `http://<Proxy_IP>:<port>/api/proxy/1/version` ein, zum Beispiel `http://192.168.1.50:8080/api/proxy/1/version`.
3. Lesen Sie die Antwort: Sie enthält `"version"` gefolgt von der Version des Proxys, zum Beispiel `2.3.0` mit dem Image von wimaha. Beim Fork-Image enthält die Antwort außerdem `"flavor":"superdcat"` und eine Version wie `2.3.0-tb.2`.

Ist diese Version **2.3.0 oder neuer**, müssen Sie für das Plugin nichts tun. Andernfalls fahren Sie mit Schritt 2 fort.

**2. Das Image des Proxys aktualisieren**

1. Verbinden Sie sich per SSH mit dem Raspberry Pi, der den Proxy hostet.
2. Wechseln Sie in den Ordner, der die Datei `docker-compose.yml` des Proxys enthält (der Ordner `TeslaBleHttpProxy`, wenn Sie [Den BLE-Proxy installieren](installation-proxy.md) befolgt haben):

   ```
   cd TeslaBleHttpProxy
   ```

3. Prüfen Sie in `docker-compose.yml` die Zeile `image:`: Sie muss `image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2` lauten (oder eine neuere Version des Forks). Verweist sie auf das Image von wimaha, siehe [Vom wimaha-Image zum Fork-Image wechseln](installation-proxy.md#vom-wimaha-image-zum-fork-image-wechseln). Trägt sie eine feste Versionsnummer, ändern Sie diese Nummer.
4. Laden Sie das Image herunter und starten Sie den Proxy damit neu:

   ```
   docker compose pull && docker compose up -d
   ```

   Ein Neustart des Raspberry Pi oder `restart: always` **aktualisieren das Image nicht**: siehe [Das Image des Proxys aktualisieren](installation-proxy.md#das-proxy-image-aktualisieren).

**3. Die Version erneut prüfen**

Öffnen Sie `http://<Proxy_IP>:<port>/api/proxy/1/version` erneut im Browser (warten Sie einige Sekunden, bis der Proxy neu gestartet ist) und kontrollieren Sie, dass die Version tatsächlich 2.3.0 oder neuer ist.

Der mit dem Fahrzeug gekoppelte Schlüssel liegt im Ordner `key`, der durch die Datei `docker-compose.yml` eingebunden wird: Er bleibt bei der Aktualisierung **erhalten**, Sie müssen die Kopplung nicht wiederholen.

> **WICHTIG**
>
> Mit einem Proxy, der älter als 2.1.1 ist, kann das Plugin den Fahrzeugzustand nicht lesen: Verriegelung und Schlafzustand werden nicht mehr aktualisiert, die Anwesenheit springt nicht mehr auf 1, und das Log des Plugins zeigt „Version du proxy non prise en charge : 2.3.0 minimum, mettez le proxy à jour“ (*Proxy-Version nicht unterstützt: mindestens 2.3.0, aktualisieren Sie den Proxy*) (Zeile als Fehler).

### Den Raspberry Pi auswählen und installieren

Der Proxy muss sich **in Bluetooth-Reichweite des Fahrzeugs** befinden (5 bis 10 m, also in der Regel in der Garage). Der Raspberry Pi muss nahe am Auto stehen, nicht Jeedom.

| Board | Urteil |
|---|---|
| **Raspberry Pi Zero 2 W** | Empfohlen: klein, sparsam, Docker-Image des Proxys für diesen Prozessor verfügbar. |
| Raspberry Pi Zero W (erste Generation) | Nicht empfohlen: ARMv6-Prozessor, der von neueren Docker-Versionen nicht mehr unterstützt wird, und ein Bluetooth-Adapter, der nach einigen Stunden zum Einfrieren neigt. |
| Raspberry Pi 3, 4, 5 oder Mini-PC mit Bluetooth | Geeignet, sofern in Reichweite des Fahrzeugs. |

Die ausführliche Anleitung mit Befehlen, Einstellungen und Fehlerbehebung finden Sie auf der Seite [Den BLE-Proxy installieren](installation-proxy.md). Zusammengefasst besteht die Installation aus Folgendem:

1. Raspberry Pi OS **64 Bit Lite** und Docker installieren.
2. Das Image `ghcr.io/superdcat/tesla-ble-http-proxy` starten (Fork empfohlen; das Image `wimaha/tesla-ble-http-proxy` bleibt eine Alternative).
3. `http://<Pi_IP>:8080/dashboard` öffnen, den Schlüssel erzeugen, die VIN eingeben, das **Fahrzeug aufwecken**, den Schlüssel senden und dann die Schlüsselkarte zur Bestätigung auf die Mittelkonsole legen.
4. Dem Raspberry Pi eine **feste IP-Adresse** geben (DHCP-Reservierung in Ihrem Router), da seine Adresse im Plugin gespeichert wird.

Einige Tipps für einen stabilen Betrieb:

- Verwenden Sie ein hochwertiges Netzteil (5 V, 2,5 A): Ein schwaches Netzteil verursacht Bluetooth-Verbindungsabbrüche.
- Verwenden Sie das Bluetooth dieses Raspberry Pi nicht für etwas anderes: Der Proxy braucht den Adapter ganz für sich.
- Ein Fahrzeug akzeptiert nur **3 gleichzeitig verbundene Bluetooth-Geräte** (Smartphones, Uhr, Proxy). Darüber hinaus werden die Verbindungen unregelmäßig.

### Rolle des Schlüssels

Mit TeslaBleHttpProxy (Fork oder wimaha 2.3.0) hat der standardmäßig erzeugte Schlüssel die Rolle **Charging Manager**. Er genügt, um den Fahrzeugzustand zu lesen und das Laden zu steuern, aber das Fahrzeug **verweigert** bestimmte Befehle. Um sie zu nutzen, erzeugen und koppeln Sie einen Schlüssel mit der Rolle **Owner** über das Dashboard des Proxys (Link in der Konfiguration des Plugins).

| Rolle des Schlüssels | Betroffene Befehle (Richtliste) |
|---|---|
| **Charging Manager**: funktioniert | Lesevorgänge (Anwesenheit, Verriegelung, Laden, Klimatisierung), **Aktualisieren**, **Aufwecken**, **Laden starten**, **Laden beenden**, **Ladestrom** |
| **Charging Manager**: funktioniert (Funktionen des erweiterten Ladens) | **Nach Überschuss anpassen** und **Laden zur Niedertarifzeit** senden nur **Ladestrom**, **Laden starten** und **Laden beenden**: Ein Charging-Manager-Schlüssel genügt. |
| **Charging Manager**: nicht bestätigt | **Ladeplan hinzufügen** und **Ladeplan löschen**: Die Mindestrolle ist nicht bestätigt (wahrscheinlich Charging Manager; probieren Sie es aus und wechseln Sie zu Owner, wenn das Fahrzeug ablehnt). Diese beiden Aktionen erfordern außerdem den Proxy des Forks (siehe [Das Laden programmieren](#ladeplan-erstellen)). |
| **Charging Manager**: abgelehnt | **Türen verriegeln**, **Türen entriegeln**, **Hupen**, **Lichter blinken lassen**, **Wächter-Modus einstellen**; wahrscheinlich auch **Klimaanlage starten** und **Klimaanlage stoppen** |
| **Charging Manager**: abgelehnt (wahrscheinlich) | **Sollwert Fahrer** und **Sollwert Beifahrer**: Die Rolle Owner wird als erforderlich angenommen (im realen Betrieb nicht bestätigt). Diese beiden Aktionen erfordern außerdem den Proxy des Forks (siehe [Den Temperatursollwert einstellen](#temperatursollwert-einstellen)). |
| **Charging Manager**: abgelehnt (wahrscheinlich) | Die sechs Aktionen **Sitzheizung … einstellen** und **Lenkradheizung einstellen**: Die Rolle Owner wird als erforderlich angenommen (im realen Betrieb nicht bestätigt). Sie erfordern außerdem den Proxy des Forks (siehe [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen)). |
| **Charging Manager**: abgelehnt (wahrscheinlich) | **Maximale Enteisung**: Die Rolle Owner wird als erforderlich angenommen (im realen Betrieb nicht bestätigt). Diese Aktion erfordert außerdem den Proxy des Forks (siehe [Maximale Enteisung](#maximale-enteisung)). |
| **Charging Manager**: abgelehnt (wahrscheinlich) | **Klimahaltemodus**: Die Rolle Owner wird als erforderlich angenommen (im realen Betrieb nicht bestätigt). Diese Aktion erfordert außerdem den Proxy des Forks (siehe [Hunde-, Camp- und Klimahaltemodus](#hundemodus-campmodus-und-klimahaltemodus)). |
| **Charging Manager**: abgelehnt (wahrscheinlich) | **Kofferraum hinten öffnen** und **Frunk öffnen**: Die Rolle Owner wird als erforderlich angenommen (im realen Betrieb nicht bestätigt). Diese beiden Aktionen erfordern außerdem den Proxy des Forks (siehe [Den hinteren Kofferraum und den Frunk öffnen](#kofferraum-hinten-und-frunk-offnen)). |
| **Charging Manager**: abgelehnt (wahrscheinlich) | **Von Jeedom geplante Vorklimatisierung**: Sie sendet nur **Klimaanlage starten** und **Klimaanlage stoppen**, für die die Rolle Owner als erforderlich angenommen wird (im realen Betrieb nicht bestätigt). Mit einem Charging-Manager-Schlüssel erfolgt pro Abfahrt nur ein Versuch (siehe [Von Jeedom geplante Vorklimatisierung](#von-jeedom-geplante-vorklimatisierung)). |
| **Owner** | Alle Befehle |

Diese Liste ist eine Richtlinie: Das Fahrzeug entscheidet.

**Das Plugin erkennt diese Ablehnung.** Wenn eine der Befehle der Zeile „abgelehnt“ oben vom Fahrzeug mangels Berechtigung abgelehnt wird:

- erscheint die Meldung „Dieser Befehl erfordert einen Schlüssel mit der Rolle Owner: Der Proxy-Schlüssel hat wahrscheinlich die Rolle Charging Manager …“ (sie wird auch in **Letzter Fehler** kopiert);
- wechselt die Information **Schlüsselrolle** des Geräts auf **Charging Manager**;
- tragen diese Befehle im Tab **Befehle** des Geräts ein graues Abzeichen **Unzureichende Rolle**.

Die Befehle bleiben vorhanden und nutzbar: Ein Szenario, das sie aufruft, erhält dieselbe Meldung. Sie sind **im Dashboard nicht ausgegraut**: Verlassen Sie sich auf die Information **Schlüsselrolle**. Das Plugin warnt Sie nicht im Voraus: Erst die erste Ablehnung verrät die Rolle.

**Zu einem Owner-Schlüssel wechseln.** Erzeugen und koppeln Sie einen Schlüssel mit der Rolle **Owner** gemäß [Den Schlüssel erzeugen und mit dem Fahrzeug koppeln](installation-proxy.md#8-den-schlussel-erzeugen-und-mit-dem-fahrzeug-koppeln) (Rollenwahl: [Die Rolle des Schlüssels wählen](installation-proxy.md#die-rolle-des-schlussels-wahlen)). Führen Sie anschließend einen dieser Befehle erneut aus: Sobald er gelingt, springt **Schlüsselrolle** zurück auf **Owner**, und das Abzeichen verschwindet beim Neuladen der Seite.

Beim Fork-Image lässt sich die Rolle des aktiven Schlüssels auch von Hand auslesen: Öffnen Sie `http://<Proxy_IP>:<port>/api/proxy/1/capabilities` und sehen Sie sich `key_role` an (`owner` oder `charging_manager`, leer, wenn kein Schlüssel installiert ist); das Plugin nutzt diese Information nicht. Das Verhalten von **Ladelimit** sowie vom Öffnen und Schließen der Ladeklappe mit einem Charging-Manager-Schlüssel ist nicht bestätigt: Die [Dokumentation des Proxys](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md#step-3-generate-key-for-vehicle) nennt nur das Aufwecken, das Starten und Beenden des Ladens sowie den Ladestrom.

> **WICHTIG**
>
> Der Proxy hat standardmäßig **keinerlei Authentifizierung**. Der Fork kann ein Token (`apiToken`) verlangen: Geben Sie dann dasselbe in **API-Token des Proxys** ein (siehe [Konfiguration des Plugins](#konfiguration-des-plugins)). Mit einem Owner-Schlüssel kann jedes Gerät in Ihrem lokalen Netzwerk das Fahrzeug entriegeln. Halten Sie den Proxy in einem vertrauenswürdigen, idealerweise isolierten Netzwerk und geben Sie seinen Port **niemals** im Internet frei. Steuern Sie nur das Laden, bevorzugen Sie einen Charging-Manager-Schlüssel.

## Konfiguration des Plugins

Aktivieren Sie das Plugin nach der Installation und öffnen Sie dann seine Konfigurationsseite (**Plugins > Plugin Management > Tesla BLE**). Sie enthält drei Einstellungen: die URL des Proxys, das API-Token des Proxys (optional) und den Schwellenwert der Warnung bei blockiertem Bluetooth.

| Feld | Erwarteter Wert |
|---|---|
| **Proxy-URL** | Die Adresse von TeslaBleHttpProxy mit ihrem Port, zum Beispiel `http://192.168.1.50:8080/`. Sie muss mit `http://` oder `https://` beginnen. Für alle Fahrzeuge wird ein einziger Proxy verwendet. |
| **API-Token des Proxys** | Optional: nur auszufüllen, wenn der Proxy des Forks ein `apiToken` hat (derselbe Wert). Dasselbe Token dient für alle Proxys. Es wird **verschlüsselt** gespeichert und **nie wieder angezeigt**: Das Feld bleibt leer und zeigt „Token gespeichert: Leer lassen, um ihn beizubehalten“. Lassen Sie es leer, um das gespeicherte Token zu behalten; **Token löschen** entfernt es. |
| **Testen** (Schaltfläche) | Prüft, ob der Proxy antwortet, und zeigt seine Version an. Sie testet die eingegebene URL und das eingegebene Token, **auch ungespeichert** (Token-Feld leer: das gespeicherte Token). Sie zeigt auch die Authentifizierung an: **„Proxy ohne Authentifizierung: Kein Token erforderlich“**, **„API-Token vom Proxy akzeptiert“**, **„Der Proxy verlangt einen API-Token“** (weder ein Token eingegeben noch gespeichert) oder **„API-Token vom Proxy abgelehnt“** (Token weicht von `apiToken` ab). |
| **Dashboard des Proxys öffnen (Schlüsselkopplung)** (Link) | Öffnet das Dashboard des Proxys in einem neuen Tab, um den Schlüssel zu erzeugen und zu koppeln. |
| **Proxy-Logs** (Schaltfläche, Zeile **Diagnose**) | Zeigt die letzten Log-Zeilen des Proxys in einem Fenster an, ohne SSH-Sitzung auf dem Raspberry Pi. Verwendet die **gespeicherte** URL. |
| **Schwellenwert der Bluetooth-Blockierungswarnung** | Anzahl aufeinanderfolgender Lesevorgänge mit Zeitüberschreitung bei antwortendem Proxy, bevor Sie gewarnt werden, dass der Bluetooth-Adapter des Raspberry Pi wahrscheinlich blockiert ist. Ganze Zahl von 2 bis 288 (ein Lesevorgang erfolgt im Aktualisierungsintervall des Fahrzeugs, standardmäßig 5 Minuten: 288 = ein Tag an Lesevorgängen bei diesem Standard); leer lassen für den Standardwert **3**, grau angezeigt. Siehe [Warnung bei blockiertem Bluetooth-Adapter](#warnung-bei-blockiertem-bluetooth-adapter). |
| **Mindestversion des Proxys** | Schreibgeschützte Information: die minimal unterstützte Version von TeslaBleHttpProxy (2.3.0). |

### Die URL wird beim Speichern normalisiert

Sie müssen sich nicht um die genaue Form der Adresse kümmern: Beim Speichern entfernt das Plugin die Leerzeichen um die URL, setzt `http`/`https` in Kleinbuchstaben und **fügt den abschließenden `/` hinzu**, falls nötig: Der abschließende `/` und die Schreibweise von `http://` spielen also keine Rolle, `HTTP://192.168.1.50:8080` und `http://192.168.1.50:8080/` bezeichnen denselben Proxy. Nach dem Speichern zeigt das Feld die korrigierte Adresse.

Die URL wird mit einer roten Meldung abgelehnt, ohne dass der alte Wert geändert wird, in folgenden Fällen:

- sie ist leer oder beginnt nicht mit `http://` oder `https://`;
- sie enthält Zugangsdaten (`Benutzer:Passwort@`);
- sie enthält unzulässige Zeichen (Leerzeichen in der Mitte, Akzente, Parameter `?...`, Anker `#...`), einen ungültigen Port oder überschreitet 255 Zeichen.

### Den Proxy testen

Klicken Sie auf **Testen**: Das Plugin fragt die Version des Proxys ab (höchstens 10 Sekunden) und zeigt das Ergebnis unter dem Feld an. Der Test prüft weder den gekoppelten Schlüssel noch das Fahrzeug: Er belegt nur, dass der Proxy erreichbar ist. Die Bedeutung jeder Meldung finden Sie unter [Fehlerbehebung](#fehlerbehebung).

### Link zum Dashboard des Proxys

Der Link erscheint, sobald eine gültige URL gespeichert (oder getestet) wurde. Er verweist auf `<Proxy-URL>dashboard`. Haben Sie den Proxy über einen **Docker-Dienstnamen** angegeben (zum Beispiel `http://teslablehttpproxy:8080/`), kann Jeedom ihn erreichen, **Ihr Browser aber nicht**: Der Link lässt sich dann nicht öffnen. Öffnen Sie das Dashboard in diesem Fall mit der IP-Adresse des Raspberry Pi (`http://<Pi_IP>:8080/dashboard`).

### Die Logs des Proxys einsehen

Die Schaltfläche **Proxy-Logs** öffnet ein Fenster mit den **letzten 200 Zeilen** der Logs des Proxys (die neueste unten), mit ihrer Uhrzeit in der Zeitzone von Jeedom und ihrem Level (`[DEBUG]`, `[INFO]`, `[WARN]`, `[ERROR]`). Die Schaltfläche **Aktualisieren** liest die Logs neu ein. Das Lesen belastet das Fahrzeug nicht und antwortet in höchstens 10 Sekunden, selbst wenn ein Befehl den Proxy gerade beschäftigt.

- Die Funktion erfordert den Proxy **2.3.0** oder neuer und verwendet die **gespeicherte** URL: Speichern Sie nach einer Änderung der URL, bevor Sie die Logs öffnen.
- Die Zeilen werden **unverändert** als reiner Text angezeigt: Ein Inhalt wie `<script>` oder `&` erscheint wörtlich, ohne jede Wirkung. Jede Zeile ist auf 1000 Zeichen begrenzt.
- Die VIN werden maskiert (nur die letzten 4 Zeichen bleiben sichtbar). Die Zeilen können die IP-Adresse der Clients des Proxys und den Inhalt gesendeter Befehle enthalten: Lesen Sie einen Screenshot noch einmal durch, bevor Sie ihn in einem Forum veröffentlichen.
- Der Proxy behält auch seine **Debug**-Zeilen, unabhängig von seinem Log-Level: Die 200 Zeilen decken daher oft weniger als eine Stunde Aktivität ab. Seine Logs werden bei jedem Neustart des Proxys gelöscht.
- Die Zeilen des Proxys werden nie in das Log des Plugins kopiert. Funktion nur für Jeedom-Administratoren.

Bei einer Fehlermeldung siehe [Meldungen des Fensters Proxy-Logs](#meldungen-des-fensters-proxy-logs).

### Warnung bei blockiertem Bluetooth-Adapter

Bei manchen Raspberry Pi (insbesondere dem Zero W der ersten Generation) friert der Bluetooth-Adapter nach einigen Stunden ein: Der Proxy antwortet weiterhin (die Schaltfläche **Testen** ist grün, **Proxy erreichbar** steht auf 1), aber jeder Lesevorgang beim Fahrzeug läuft ab. Das Plugin erkennt diese Situation und warnt Sie:

- Wenn das Lesen des Fahrzeugzustands **3 Mal hintereinander** (oder den eingestellten Schwellenwert) in die Zeitüberschreitung läuft, während der Proxy antwortet, erscheint im Nachrichtenzentrum von Jeedom die Meldung **„Bluetooth-Adapter des Proxys wahrscheinlich blockiert — …“**, **nur einmal**, solange die Situation andauert;
- währenddessen zeigt **Letzter Fehler** **„Bluetooth-Adapter des Proxys wahrscheinlich blockiert: Starten Sie den Raspberry Pi neu“**;
- sobald ein Lesevorgang wieder gelingt (auch bei einem schlafenden Fahrzeug, das antwortet), vermerkt das Log die Rückkehr zum Normalzustand (Level **Info**) und die Warnung wird neu scharf geschaltet: Eine neue Serie löst eine neue Meldung aus, die die alte ersetzt.

Eine einzelne Zeitüberschreitung, ein Fahrzeug außer Reichweite oder ein ausgeschalteter Proxy lösen die Warnung nicht aus. Die Meldung bleibt nach der Rückkehr zum Normalzustand im Nachrichtenzentrum: Löschen Sie sie selbst. Bei mehreren Fahrzeugen am selben Proxy hat jedes Fahrzeug seine eigene Meldung. Klicks auf **Aktualisieren** zählen als Lesevorgänge.

Was zu tun ist: Starten Sie den Raspberry Pi, der den Proxy hostet, neu. Wiederholt sich das, wechseln Sie zu einem Raspberry Pi Zero 2 W und verwenden Sie ein hochwertiges Netzteil (5 V, 2,5 A).

## Konfiguration der Geräte

Jedes Fahrzeug ist ein Gerät. Gehen Sie zu **Plugins > Verbundene Objekte > Tesla BLE**, klicken Sie auf **Hinzufügen** und geben Sie dem Fahrzeug einen Namen.

Im Tab **Gerät**:

| Feld | Erwarteter Wert |
|---|---|
| **Name des Geräts** | Der Name des Fahrzeugs, frei wählbar. |
| **Übergeordnetes Objekt** | Das Jeedom-Objekt, in dem das Fahrzeug abgelegt wird (oder **Keine**). |
| **Kategorie** | Die Jeedom-Kategorien des Geräts (Kontrollkästchen). |
| **Aktivieren** | Angekreuzt: Das Fahrzeug wird in seinem **Aktualisierungsintervall** aktualisiert (standardmäßig 5 Minuten). Nicht angekreuzt: Es wird nicht mehr gelesen, unabhängig von seinem Intervall. |
| **Sichtbar** | Angekreuzt: Das Widget des Fahrzeugs wird im Dashboard angezeigt. |
| **VIN** | Die Seriennummer des Fahrzeugs: **17 Zeichen**, Ziffern und Buchstaben **außer I, O und Q** (fiktives Beispiel: `5YJ3E1EA7KF000000`). Sie muss der in TeslaBleHttpProxy hinterlegten entsprechen. |
| **Proxy-URL dieses Fahrzeugs** | Optional. Die Adresse des Proxys in der Garage dieses Fahrzeugs, mit Port (zum Beispiel `http://192.168.1.51:8080/`). **Leer: Das Fahrzeug verwendet die URL aus der Konfiguration des Plugins.** |
| **Diesen Proxy testen** (Schaltfläche) | Zeigt die Version des Proxys an, den dieses Fahrzeug verwendet. Sie testet den eingegebenen Wert, **auch ungespeichert**; bei leerem Feld wird die URL aus der Konfiguration des Plugins getestet. |
| **Aktualisierungsintervall** | Lesehäufigkeit dieses Fahrzeugs: **1, 2, 5, 10, 15 oder 30 Minuten**. Standardmäßig **5 Minuten** (bestehende Fahrzeuge behalten dieses Verhalten nach der Aktualisierung). Je kürzer das Intervall, desto frischer die Informationen, aber desto stärker wird der Proxy belastet und, bei wachem Fahrzeug, desto mehr kann sein Einschlafen verzögert werden; ein langes Intervall schont den Raspberry Pi. **1 Minute** passt für ein oder zwei Fahrzeuge pro Proxy (empfohlen; an Ihre Installation anzupassen): Darüber hinaus kann ein langsamer Lesevorgang die Minute überschreiten. Ein unbekannter Wert wird auf 5 Minuten zurückgesetzt. Eine Änderung wirkt beim nächsten Lesevorgang, ohne Neustart. Dieser Lesevorgang weckt das Fahrzeug nie auf. |
| **Intervall während des Ladens** | **Standardmäßig deaktiviert** (Verhalten unverändert), oder **1, 2, 5, 10 oder 15 Minuten**. Während eines Ladevorgangs ersetzt es das Aktualisierungsintervall, **wenn es kürzer ist**; der normale Takt gilt wieder, sobald ein Lesevorgang das Laden nicht mehr feststellt. Mindestens eine Minute: Jeedom startet die Aktualisierung jede Minute, und der Proxy hält die Daten 30 Sekunden im Cache. Weckt das Fahrzeug nie auf. Siehe [Beschleunigtes Lesen während des Ladens](#beschleunigtes-lesen-wahrend-des-ladens). |
| **Fahrzeug einschlafen lassen** (Kontrollkästchen **Aktivieren**) | Standardmäßig angekreuzt (auch bei bestehenden Fahrzeugen nach der Aktualisierung). Ist das Fahrzeug wach, aber inaktiv, liest das Plugin während eines Zeitfensters keine Lade- und Klimadaten mehr, um das Einschlafen nicht zu verhindern. Nicht angekreuzt: Bei jedem Durchlauf erfolgt wie zuvor ein vollständiger Lesevorgang. Siehe [Das Fahrzeug einschlafen lassen](#fahrzeug-einschlafen-lassen). |
| **Unveränderte Lesevorgänge vor dem Zeitfenster** | Anzahl aufeinanderfolgender Lesevorgänge ohne jede Änderung (außer Laden, ohne Insassen), bevor das Zeitfenster geöffnet wird: **1, 2, 3, 4, 5, 10 oder 15**. Standardmäßig **3** (15 Minuten Inaktivität bei einem Intervall von 5 Minuten). |
| **Dauer des Zeitfensters** | Dauer, während der die Daten nicht mehr gelesen werden: **15, 20, 30, 45 Minuten, 1 Stunde, 1 Stunde 30 oder 2 Stunden**. Standardmäßig **30 Minuten**. Ohne Wirkung, wenn sie das Aktualisierungsintervall nicht überschreitet: Wählen Sie eine Dauer, die größer ist als das Intervall. |
| **Verzögerung des erneuten Lesens nach Befehl** | Wartezeit, bevor das Fahrzeug nach einem erfolgreichen Befehl erneut gelesen wird: **30 Sekunden (Standard), 45 Sekunden, 1 Minute, 1 Minute 30 oder 2 Minuten**. 30 Sekunden ist das Minimum: So lange hält der Proxy seine Daten im Cache (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)). Verlängern Sie sie, wenn Sie diesen Cache im Proxy verlängert haben. |
| **Klimaanlage ebenfalls lesen** | **Ja (Standard)**: Laden und Klimaanlage werden gelesen, wie vor der Aktualisierung. **Nein, nur Laden**: Beim Proxy werden nur die Ladedaten angefordert, bei jeder Aktualisierung wie auch auf Anforderung (**Aktualisieren**, **Aktualisieren (mit Aufwecken)**, erneutes Lesen nach Befehl). Die Anfrage ist kürzer und belastet die Bluetooth-Verbindung weniger (der Gewinn ist an Ihrer Installation zu messen). Die Klimainformationen behalten dann ihren letzten Wert und werden nicht mehr aktualisiert; die Klimabefehle bleiben nutzbar. Der Wechsel zurück auf **Ja** nimmt das Lesen beider Familien beim nächsten Durchlauf bei wachem Fahrzeug wieder auf. |
| **Netzspannung (V)** | Überschusssteuerung: Spannung zwischen Phase und Neutralleiter, mit der die verfügbare Leistung in Strom umgerechnet wird. Leer: **230 V**. Ganze Zahl von 100 bis 250. |
| **Phasen** | Überschusssteuerung: **Einphasig (Standard)** oder **Dreiphasig**. Die Leistung wird durch die Spannung und durch diese Zahl geteilt, um den Strom **pro Phase** zu erhalten. |
| **Anpassungsschritt (A)** | Überschusssteuerung: Der berechnete Strom wird **abwärts** auf ein Vielfaches dieses Schritts gerundet. Leer: **1 A**. Ganze Zahl von 1 bis 16. |
| **Hysterese (A)** | Überschusssteuerung: Kein Befehl, solange der berechnete Strom um **weniger** als diesen Wert vom zuletzt gesendeten Sollwert abweicht. Leer: **2 A**. Ganze Zahl von 0 bis 16. |
| **Mindestintervall zwischen Befehlen (s)** | Überschusssteuerung: Mindestverzögerung zwischen dem **Ende** eines Befehls der Steuerung und dem nächsten. Leer: **120 s**. Ganze Zahl von 60 bis 3600 (ein Befehl kann bis zu 75 Sekunden dauern, und der Proxy hält die Daten 30 Sekunden im Cache). |
| **Minimaler Startstrom (A)** | Überschusssteuerung: Bei gestopptem Laden wird es neu gestartet, wenn der berechnete Strom diesen Wert erreicht. Leer: **6 A**. Ganze Zahl von 1 bis 80. |
| **Abschaltschwelle (A)** | Überschusssteuerung: Während des Ladens wird der Strom nie unter diese Schwelle gesenkt; bleibt er während der Haltedauer darunter berechnet, wird das Laden gestoppt. Leer: **5 A**. Ganze Zahl von 1 bis 80, **nie größer als der minimale Startstrom**. |
| **Haltedauer vor dem Abschalten (s)** | Überschusssteuerung: Dauer, während der der berechnete Strom unter der Abschaltschwelle bleiben muss, bevor das Laden gestoppt wird. Leer: **300 s**. Ganze Zahl von 0 bis 3600. |
| **Ladesteuerung** (Kontrollkästchen **Aktivieren**, Abschnitt **Laden zur Niedertarifzeit**) | **Standardmäßig nicht angekreuzt.** Angekreuzt, startet und stoppt Jeedom das Laden während des unten angegebenen Zeitraums (siehe [Laden zur Niedertarifzeit](#laden-zur-niedertarifzeit)). Sie wird nur aktiv, wenn Beginn, Ende und Ziel-SoC angegeben sind. |
| **Beginn des Zeitraums** | Laden zur Niedertarifzeit: Startzeit des Zeitraums im Format `HH:MM` (Jeedom-Zeit, zum Beispiel `22:00`; `22h00` wird ebenfalls akzeptiert). |
| **Ende des Zeitraums** | Laden zur Niedertarifzeit: Endzeit des Zeitraums im Format `HH:MM`, **verschieden** vom Beginn. Ein Ende vor dem Beginn ergibt einen Zeitraum **über Mitternacht** (`22:00` bis `06:00`). |
| **Ziel-SoC (%)** | Laden zur Niedertarifzeit: Batteriestand, bei dem das Laden während des Zeitraums gestoppt wird. Ganze Zahl von **1 bis 100**. |
| **Am Ende des Zeitraums stoppen** | Laden zur Niedertarifzeit: **Standardmäßig nicht angekreuzt**. Angekreuzt, wird ein am Ende des Zeitraums noch laufendes Laden gestoppt (beim ersten Lesen des Fahrzeugs innerhalb der folgenden Stunde). Nicht angekreuzt, läuft es bis zur Grenze des Fahrzeugs weiter. |
| **Klimasteuerung** (Kontrollkästchen **Aktivieren**, Abschnitt **Von Jeedom geplante Vorklimatisierung**) | **Standardmäßig nicht angekreuzt.** Angekreuzt, startet Jeedom die Klimaanlage vor der Abfahrtszeit und stoppt sie dann (siehe [Von Jeedom geplante Vorklimatisierung](#von-jeedom-geplante-vorklimatisierung)). Sie wird nur aktiv, wenn die Abfahrtszeit angegeben ist, mindestens ein Tag angekreuzt ist und **Klimaanlage ebenfalls lesen** auf **Ja** bleibt. |
| **Abfahrtszeit** | Geplante Vorklimatisierung: Uhrzeit, zu der das Fahrzeug bereit sein muss, im Format `HH:MM` (Jeedom-Zeit, zum Beispiel `07:30`; `7h30` wird ebenfalls akzeptiert). |
| **Tage** | Geplante Vorklimatisierung: betroffene **Abfahrts**tage (Kontrollkästchen **Montag** bis **Sonntag**). Maßgeblich ist der Tag der Abfahrtszeit, auch wenn die Klimaanlage am Vortag vor Mitternacht startet. Kein Kontrollkästchen angekreuzt: Die Funktion wird bei der Aktivierung abgelehnt. |
| **Vorlauf (min)** | Geplante Vorklimatisierung: Minuten vor der Abfahrtszeit, zu denen die Klimaanlage gestartet wird. Ganze Zahl von **1 bis 60**. Leer: **15 Minuten**. |
| **Maximale Dauer (min)** | Geplante Vorklimatisierung: Dauer, **ab dem geplanten Start gezählt**, nach der Jeedom die Klimaanlage stoppt. Ganze Zahl von **1 bis 120**, **mindestens gleich dem Vorlauf**. Leer: **30 Minuten** (oder der Vorlauf plus 15 Minuten, wenn er 15 überschreitet), also ein Stopp **15 Minuten nach der Abfahrt** mit dem Standard-Vorlauf. |
| **Nur wenn angeschlossen** | Geplante Vorklimatisierung: **Standardmäßig nicht angekreuzt**. Angekreuzt, wird die Klimaanlage nicht gestartet, wenn das Fahrzeug nicht angeschlossen ist oder sein Ladezustand unbekannt ist. Eine Ladestation, die keinen Strom liefert, gilt als angeschlossen: Die Klimaanlage zieht dann Energie aus der Batterie. |
| **Breitengrad** (Abschnitt **Position des Zuhauses**) | Position des Zuhauses, zur Berechnung von **Zu Hause**: Dezimalgrad von -90 bis 90, zum Beispiel `48.8566` (Komma zulässig, höchstens 8 Dezimalstellen). **Leer: die Position von Jeedom** (**Einstellungen > Systeme > Konfiguration**, Tab **Allgemein**). Zusammen mit dem **Längengrad** auszufüllen: Nur einer der beiden wird abgelehnt. Siehe [Position und Datenschutz](#position-und-datenschutz). |
| **Längengrad** (Abschnitt **Position des Zuhauses**) | Dezimalgrad von -180 bis 180, zum Beispiel `2.3522`. Leer bei leerem Breitengrad: Position von Jeedom. |
| **Radius (m)** (Abschnitt **Position des Zuhauses**) | Maximaler Abstand in Metern zwischen Fahrzeug und Zuhause, damit **Zu Hause** den Wert 1 hat. Ganze Zahl von **10 bis 10000**. Leer: **100 m**. Ohne Wirkung, wenn der Proxy die Position des Fahrzeugs nicht liefert. |
| **Beschreibung** | Freitext, optional. |

Die Schaltflächen oben auf der Seite sind die jedes Jeedom-Geräts: **Erweiterte Konfiguration**, **Duplizieren**, **Speichern** und **Löschen**. Der Tab **Befehle** listet die Befehle des Fahrzeugs auf (siehe [Befehle](#befehle)).

Beim Speichern:

- Das Plugin legt die fehlenden Befehle des Geräts an. **Es startet keine Aktualisierung**: Die Seite antwortet sofort, auch wenn der Proxy ausgeschaltet ist. Die Informationen treffen beim nächsten Lesevorgang ein (innerhalb der folgenden Minute bei einem neuen Fahrzeug) oder sofort mit dem Befehl **Aktualisieren**.
- Die VIN wird **normalisiert**: Leerzeichen entfernt, Buchstaben in Großbuchstaben. Sie kann leer bleiben, das Fahrzeug wird dann aber nicht gelesen (siehe [Fehlerbehebung](#fehlerbehebung)).
- Die VIN ist **eindeutig**: Ein Fahrzeug kann nur ein einziges Gerät haben. Eine ungültige oder bereits von einem anderen Gerät verwendete VIN wird mit einer Meldung abgelehnt.
- **Duplizieren** eines Fahrzeugs wird daher **abgelehnt**: Die Kopie trägt dieselbe VIN. Verwenden Sie für ein zweites Fahrzeug **Hinzufügen**.
- Die **Proxy-URL dieses Fahrzeugs** wird wie die aus der Konfiguration des Plugins normalisiert (siehe [Die URL wird beim Speichern normalisiert](#die-url-wird-beim-speichern-normalisiert)); eine ungültige URL wird mit derselben Meldung abgelehnt.

### Ein Proxy pro Fahrzeug (mehrere Garagen)

Stehen Ihre Fahrzeuge an verschiedenen Orten, jedes mit seinem Raspberry Pi, tragen Sie bei jedem Gerät die **Proxy-URL dieses Fahrzeugs** ein. Alle seine Lesevorgänge und Befehle laufen dann über diesen Proxy, und der Link **Dashboard des Proxys öffnen** im Kopplungsabschnitt verweist auf ihn. Fällt ein Proxy aus, gehen nur die Fahrzeuge in den Fehlerzustand, die ihn verwenden. Wird das Feld geleert, kehrt das Fahrzeug im nächsten Zyklus zur URL aus der Konfiguration des Plugins zurück; seine Befehle und sein Verlauf ändern sich nicht.

- Schreiben Sie denselben Proxy **immer mit derselben URL** (dieselbe IP-Adresse oder derselbe Name, derselbe Port): Das Plugin erkennt einen Proxy an seiner URL.
- Die Schaltfläche **Proxy-Logs** der Konfiguration des Plugins zeigt nur die Logs des Proxys aus der **Konfiguration des Plugins**.

### Meinen Schlüssel koppeln und die Kopplung prüfen

Unter dem Feld **VIN** erinnert der Abschnitt **Meinen Schlüssel koppeln** an die Schritte der Kopplung, die im Dashboard des Proxys erfolgt (Details: [Den Schlüssel erzeugen und mit dem Fahrzeug koppeln](installation-proxy.md#8-den-schlussel-erzeugen-und-mit-dem-fahrzeug-koppeln)). Sobald die VIN gespeichert und die Proxy-URL eingetragen ist, zeigt er außerdem den Link **Dashboard des Proxys öffnen** (neuer Tab), die in **Setup Vehicle** zu übernehmende VIN und die Schaltfläche **Kopplung prüfen**.

**Kopplung prüfen** liest den Fahrzeugzustand über den Proxy **ohne es aufzuwecken** (höchstens 50 Sekunden) und sendet keinen Befehl. Das Plugin erzeugt oder löscht nie einen Schlüssel: Nur das Dashboard des Proxys tut das.

| Meldung | Was zu tun ist |
|---|---|
| **Kopplung geprüft: Das Fahrzeug antwortet auf den Proxy-Schlüssel** | Nichts. Beim Fork-Image zeigt die Zeile **Rolle des aktiven Proxy-Schlüssels** zusätzlich Owner oder Charging Manager an. Die Information **Schlüsselrolle** des Geräts ändert sich dagegen erst beim nächsten vorbehaltenen Befehl (siehe [Rolle des Schlüssels](#rolle-des-schlussels)). |
| **Proxy ohne Schlüssel: …** | Kein Schlüssel auf dem Proxy: Erzeugen Sie einen (**Generate**) und senden Sie ihn dann an das Fahrzeug. |
| **Schlüssel nicht mit diesem Fahrzeug gekoppelt: …** | Wecken Sie das Fahrzeug auf, senden Sie den Schlüssel (**Send key**) und legen Sie dann die Schlüsselkarte auf die Mittelkonsole. |
| **Fahrzeug außerhalb der Bluetooth-Reichweite des Proxys: …** | Bringen Sie Fahrzeug oder Raspberry Pi näher zusammen, prüfen Sie die VIN. |
| **Proxy nicht erreichbar: …** | Prüfen Sie, ob der Proxy gestartet ist, dann seine Adresse mit der Schaltfläche **Diesen Proxy testen** des Geräts. |
| **Proxy durch einen Befehl oder Lesevorgang ausgelastet: …** | Starten Sie die Prüfung gleich erneut. |

Die Prüfung verwendet die **gespeicherte** VIN: Speichern Sie das Gerät, nachdem Sie sie geändert haben.

## Topologien: ein oder mehrere Proxys, ein oder mehrere Fahrzeuge

Das Plugin kann mehrere Fahrzeuge steuern, mit einem einzigen Proxy oder mit mehreren. Eine Proxy-URL wird an zwei Stellen eingegeben: in der **Plugin-Konfiguration** (die Standardadresse, die von allen Fahrzeugen ohne eigene Adresse verwendet wird) und optional im Feld **Proxy-URL dieses Fahrzeugs** jedes Geräts.

### Schemata

Ein Raspberry Pi, mehrere Fahrzeuge (dieselbe Garage): Die URL wird **nur einmal** in der Plugin-Konfiguration eingegeben; das Feld jedes Fahrzeugs bleibt leer.

```
Jeedom ---> Proxy der Garage (Raspberry Pi A) --BLE--> Fahrzeug 1 (VIN 1)
                                              --BLE--> Fahrzeug 2 (VIN 2)

URL: Plugin-Konfiguration   = http://192.168.1.50:8080/
URL: Feld jedes Fahrzeugs   = leer
```

Mehrere Raspberry Pi, mehrere Garagen: Die URL jedes Proxys wird **im Gerät jedes Fahrzeugs** eingegeben. Die Plugin-Konfiguration kann auf dem Haupt-Proxy bleiben (sie dient als Standardwert und für die Schaltfläche **Proxy-Logs**).

```
Jeedom ---> Proxy der Garage A (Raspberry Pi A) --BLE--> Fahrzeug 1
       |
       +--> Proxy der Garage B (Raspberry Pi B) --BLE--> Fahrzeug 2

URL: Plugin-Konfiguration   = http://192.168.1.50:8080/   (Proxy A, Standard)
URL: Feld von Fahrzeug 1    = leer (oder http://192.168.1.50:8080/)
URL: Feld von Fahrzeug 2    = http://192.168.1.51:8080/
```

### Ein zweites Fahrzeug am selben Proxy hinzufügen

Der Proxy, der Raspberry Pi und die URL in der Plugin-Konfiguration sind für das erste Fahrzeug bereits eingerichtet. Für das zweite:

1. Klicken Sie unter **Plugins > Verbundene Objekte > Tesla BLE** auf **Hinzufügen** (und nicht auf **Duplizieren**, was abgelehnt wird: Die VIN ist eindeutig), benennen Sie das Fahrzeug, geben Sie seine **VIN** ein und lassen Sie **Proxy-URL dieses Fahrzeugs** leer. **Speichern** Sie.
2. Klicken Sie im Abschnitt **Meinen Schlüssel koppeln** dieses neuen Geräts auf **Dashboard des Proxys öffnen**.
3. Geben Sie im Dashboard die VIN des zweiten Fahrzeugs unter **Setup Vehicle** ein, wecken Sie dieses Fahrzeug auf, klicken Sie auf **Send key** und legen Sie dann die Schlüsselkarte zur Bestätigung auf die Mittelkonsole. Es muss **derselbe Schlüssel** des Proxys mit jedem Fahrzeug gekoppelt werden: Erzeugen Sie keinen zweiten Schlüssel. Zur Wahl der Rolle siehe [Schlüsselrolle](#rolle-des-schlussels).
4. Kehren Sie zum Gerät zurück und klicken Sie auf **Kopplung prüfen**: Warten Sie auf **Kopplung geprüft: Das Fahrzeug antwortet auf den Proxy-Schlüssel**. Andernfalls siehe die Tabelle unter [Meinen Schlüssel koppeln und die Kopplung prüfen](#meinen-schlussel-koppeln-und-die-kopplung-prufen).
5. Klicken Sie auf **Aktualisieren** (oder warten Sie eine Minute): Die Informationen des zweiten Fahrzeugs erscheinen.

Ein Fahrzeug akzeptiert nur **3 gleichzeitig verbundene Bluetooth-Geräte** (Telefone, Uhr, Proxy): Darüber hinaus werden die Verbindungen instabil. Jedes Fahrzeug behält seinen eigenen **Letzter Fehler**: Ein Fahrzeug außer Reichweite oder mit nicht gekoppeltem Schlüssel stört das andere nicht. Sie teilen sich dagegen denselben Raspberry Pi: Die Abfragen erfolgen nacheinander (siehe [Warum die Aufrufe nacheinander erfolgen](#warum-die-aufrufe-nacheinander-erfolgen)).

### Einen zweiten Proxy für eine andere Garage hinzufügen

1. Installieren Sie den Proxy der zweiten Garage auf einem eigenen Raspberry Pi mit fester IP-Adresse (siehe [BLE-Proxy installieren](installation-proxy.md)), erzeugen Sie dann den Schlüssel und koppeln Sie ihn mit dem Fahrzeug dieser Garage.
2. Geben Sie im Gerät dieses Fahrzeugs in **Proxy-URL dieses Fahrzeugs** die Adresse des zweiten Proxys mit seinem Port ein, zum Beispiel `http://192.168.1.51:8080/`.
3. Klicken Sie auf **Diesen Proxy testen**: Die Meldung **Proxy erreichbar — Version X** bestätigt, dass **dieser** Proxy antwortet (der Test bezieht sich auf den eingegebenen Wert, auch wenn er nicht gespeichert ist). Andernfalls siehe [Meldungen der Schaltfläche Testen](#meldungen-der-schaltflache-testen).
4. **Speichern** Sie und verwenden Sie dann **Kopplung prüfen**, um den Schlüssel dieses Fahrzeugs zu kontrollieren.
5. Der Link **Dashboard des Proxys öffnen** dieses Geräts öffnet dann das Dashboard des zweiten Proxys.

Das Fenster **Proxy-Logs** in der Plugin-Konfiguration zeigt nur den Proxy der **Plugin-Konfiguration**: Um die Logs des zweiten Proxys zu lesen, öffnen Sie dessen Dashboard in einem Browser (`http://<IP_des_zweiten_Pi>:8080/dashboard`). Jedes Fahrzeug hat seine eigene Information **Proxy erreichbar**, und die Warnung bei blockiertem Adapter gilt jeweils für ein einzelnes Fahrzeug. Derselbe API-Token gilt für alle Proxys.

## Update von Version 0.x

Sie aktualisieren das Plugin von einer Version 0.x: Es muss nichts neu eingerichtet werden.

> **IMPORTANT**
>
> Ihre **Geräte, VIN, Befehle, Verläufe, Szenarien und Anzeigeeinstellungen bleiben erhalten**. Die Befehle behalten ihre Kennungen: Die Szenarien, Widgets und Verläufe, die sie verwenden, funktionieren ohne Änderung weiter.

### Namen der Befehle

Ein **von Version 0.x migriertes Gerät behält die Namen seiner Befehle** (zum Beispiel „Etat Charge“, „Charge Start“, „Rafraichir“): Für die Szenarien zählen nur die Kennungen. Die Befehle eines **neuen Geräts** tragen die Bezeichnungen aus der Tabelle im Abschnitt [Befehle](#befehle). Sie können einen Befehl frei umbenennen.

Beim Update werden die in Ihrem Gerät fehlenden Befehle **neben den Befehlen desselben Themas** hinzugefügt (nur dann als Block am Ende der Liste, wenn für dieses Thema noch kein Befehl existiert, siehe [Reihenfolge der Befehle](#reihenfolge-der-befehle)): **Verbleibende Ladezeit**, **Ladeklappe geöffnet**, **Letzter Fehler**, **Letzte Datenabfrage**, **Proxy erreichbar**, **Proxy-Version**, **Schlüsselrolle** (die bis zum ersten Befehl, der der Rolle Owner vorbehalten ist, **Unbestimmt** lautet), **Dauer Statusabfrage** und **Dauer Datenabfrage** (leer bis zur ersten erfolgreichen Abfrage), dann **Alter der Daten (min)** (der bis zur ersten bekannten Abfrage 99999 beträgt), dann **Minimale Ladegrenze**, **Maximale Ladegrenze** und **Maximaler Ladestrom** (ausgeblendet, leer bis zur ersten Datenabfrage), schließlich zehn erweiterte Ladeinformationen, ebenfalls ausgeblendet (siehe [Informationen](#informationen)). Ein **Max** eines Schiebereglers, das Sie von Hand angepasst hatten, bleibt erhalten. Bei einem bestehenden Gerät kann die Aktion zum Öffnen der Ladeklappe „Trappe de Charge Ouvert“ heißen: Benennen Sie sie bei Bedarf um.

### Reichweite und Ladegeschwindigkeit

Die Befehle **Reichweite** und **Ladegeschwindigkeit** werden nun in km und km/h umgerechnet (das Fahrzeug sendet sie in Meilen). Die bereits im Verlauf gespeicherten Werte bleiben in Meilen: Das Diagramm der **Reichweite** zeigt daher beim Update einen **Sprung** (um einen Faktor von etwa 1,6). Die früheren Werte werden nicht umgerechnet.

### Geplante Abfahrtszeit

Der Befehl **Geplante Abfahrtszeit** zeigt die Uhrzeit nun im Format `HH:MM` an (zum Beispiel `07:30`) und bleibt leer, solange keine Abfahrt geplant ist. Früher lieferte er einen numerischen Zeitstempel: Passen Sie Szenarien an, die ihn mit dieser Zahl verglichen haben.

Wenn Sie die Historisierung dieses Befehls aktiviert haben, bleibt er numerisch und wird nicht mehr aktualisiert; eine Meldung in der Nachrichtenzentrale von Jeedom weist Sie darauf hin. Um die Uhrzeit zu erhalten, ändern Sie seinen Untertyp im Reiter **Befehle** des Geräts auf **Andere**.

### Aktionsbefehle

- Die Option **„Keine“** des **Wächter-Modus einstellen** entfällt (der Proxy verstand sie nicht). Ein Szenario, das sie sendete, erhält nun einen Fehler: Verwenden Sie **Aktiviert** oder **Deaktiviert**. Das Update entfernt diese Option bei bestehenden Geräten, ohne die übrigen Einstellungen des Befehls anzutasten.
- Ein **Ladestrom außerhalb der Grenzen** des Befehls oder ein nicht ganzzahliger Wert wird abgelehnt, statt gesendet zu werden.
- Ein Befehl, der bisher stillschweigend fehlschlug, zeigt nun einen **Fehler** an und speist die Information **Letzter Fehler**.

### Mindestversionen

| Element | Version |
|---|---|
| Jeedom | mindestens 4.5 |
| Debian | 11 oder 12 |
| TeslaBleHttpProxy | mindestens 2.3.0 (siehe [Proxy-Version prüfen und aktualisieren](#die-version-des-proxys-prufen-und-aktualisieren)) |

Wenn Ihr Jeedom eine Version unter 4.5 hat, lehnt Jeedom das Update mit der Meldung „Version du core Jeedom non supportée“ (*Nicht unterstützte Jeedom-Core-Version*) ab. Die alte Version des Plugins bleibt dann installiert und funktioniert weiter. Aktualisieren Sie zuerst Jeedom. Debian 10 wird nicht mehr unterstützt.

### Was automatisch geschieht

Beim Update und anschließend bei der Aktivierung des Plugins läuft automatisch eine Aktualisierung der bestehenden Geräte in aufeinanderfolgenden Stufen. Jede Stufe wird nur ein einziges Mal angewendet. Je nach Version korrigiert oder ergänzt sie bestimmte Geräte (VIN, fehlende Befehle, geplante Abfahrtszeit, Entfernen der Option „Keine“ des Wächter-Modus, Einstellungen des Einschlaffensters …), ohne Ihre Einstellungen (Name, Sichtbarkeit, Historisierung) anzutasten. Bestehende Fahrzeuge erhalten das Einschlaffenster **aktiviert** (3 unveränderte Lesevorgänge, 30 Minuten); deaktivieren Sie das Kontrollkästchen im Gerät, wenn Sie es nicht wünschen.

Die acht Informationen zu den Öffnungen (Türen, Kofferräume, Ladeklappe, Tonneau-Abdeckung) werden **sichtbar und historisiert** angelegt; Ihre bestehenden Einstellungen werden nie verändert.

Die Informationen **Insasse anwesend** (sichtbar, historisiert) und **Detaillierter Verriegelungsstatus** (sichtbar, nicht historisiert) werden auf die gleiche Weise angelegt; Ihre bestehenden Einstellungen werden nie überschrieben.

Die Informationen **Wächter-Modus** und **Herkunft des Wächter-Modus** (sichtbar, nicht historisiert) werden auf die gleiche Weise angelegt, mit den Werten **Unbekannt** und **Keine**, solange nichts gelesen oder angeordnet wurde; Ihre bestehenden Einstellungen werden nie überschrieben (siehe [Status des Wächter-Modus](#zustand-des-wachter-modus)).

Die Informationen **Öffnungsalarm** und **Alarm entriegelt ohne Insassen** (ausgeblendet, historisiert) werden auf die gleiche Weise mit **0** angelegt; die Warnungen bleiben **deaktiviert**, bis Sie sie aktivieren (siehe [Warnungen bei längerer Öffnung](#warnungen-bei-langerer-offnung)).

Schlägt die Aktualisierung bei einem Fahrzeug fehl, wird sie beim nächsten Update oder bei der nächsten Aktivierung des Plugins automatisch wiederholt.

### Die Aktualisierung im Log nachvollziehen

Stellen Sie das Log des Plugins mindestens auf die Stufe **Info** (**Plugin-Konfiguration > Logs**), aktualisieren oder reaktivieren Sie dann das Plugin und öffnen Sie sein Log. Die betreffenden Zeilen beginnen mit „Migrations :“ (*Migrationen:*).

| Situation | Meldung im Log |
|---|---|
| Aktualisierung erfolgreich | `Migrations : migration N (<description>) appliquée sur X équipement(s) sur Y.` für jede angewendete Stufe, dann `Migrations : niveau de migration N atteint.` |
| Bereits aktuell | `Migrations : aucune migration à appliquer, niveau de migration N.` (N = letzte Stufe) |
| Kein Gerät (Neuinstallation) | `Migrations : aucun équipement à migrer, niveau de migration N (aucune migration exécutée).` (N = letzte Stufe) |
| Fehler bei einem Gerät | `Migrations : échec de la migration N (...) sur l'équipement « <nom> » (id <n>) : ...` gefolgt von `Elle sera retentée à la prochaine mise à jour ou activation du plugin.`, dann `Migrations : niveau de migration M conservé, X équipement(s) en échec ; les migrations restantes seront retentées à la prochaine mise à jour ou activation du plugin.` |

Bleibt eine Fehlermeldung nach mehreren Updates bestehen, notieren Sie sie und melden Sie sie zusammen mit dem Log des Plugins.

## Funktionsweise

### Ruhezustand des Fahrzeugs und Aktualität der Daten

Ein waches Tesla schläft von selbst nach **etwa fünfzehn Minuten** ohne Anforderung ein. Mehrere Dinge halten es wach: der **Wächter-Modus**, ein **Insasse** an Bord (oder ein Telefonschlüssel in der Nähe), ein laufender **Ladevorgang**, die geöffnete **Tesla-App** und jede Abfrage seiner Lade- und Klimadaten. Ein schlafendes Fahrzeug verbraucht sehr wenig; ein wachgehaltenes Fahrzeug verbraucht dauerhaft Batterie.

Das ist der Kompromiss, den man kennen muss: **Je häufiger Sie lesen, desto aktueller sind die Informationen, aber desto größer ist die Chance, dass das Fahrzeug nie einschläft**. Die Takt-Einstellungen dieses Plugins dienen dazu, Ihren Mittelweg zu wählen (siehe [Übersicht der Einstellungen zu Takt und Aufwecken](#ubersicht-der-einstellungen-fur-takt-und-aufwecken) und [Empfehlungen nach Verwendung](#empfehlungen-je-nach-verwendung)).

> **IMPORTANT**
>
> **Das Plugin weckt das Fahrzeug nie von selbst auf, außer auf ausdrückliche Aktion von Ihnen oder einem Szenario.** Weder die periodische Aktualisierung noch das beschleunigte Lesen während des Ladens noch das erneute Lesen nach einem Befehl wecken das Fahrzeug: Sie lesen den Zustand ohne Aufwecken und die Daten nur, wenn das Fahrzeug bereits wach ist. Um die Daten eines schlafenden Fahrzeugs zu lesen, müssen Sie es mit dem Befehl **Aktualisieren (mit Aufwecken)** **anfordern** (siehe [Aktualisieren mit Aufwecken](#aktualisieren-mit-aufwecken)). **Aufwecken** und die Aktionsbefehle (Laden, Klimatisierung, Verriegelung …) wecken das Fahrzeug ebenfalls über den Proxy, da Sie sie angefordert haben.

Um zu wissen, ob die angezeigten Werte aktuell sind, sehen Sie sich **Letzte Datenabfrage** und **Alter der Daten (min)** an: Ein schlafendes Fahrzeug oder ein geöffnetes Einschlaffenster ist kein Fehler, aber die Lade- und Klimawerte veralten dann (siehe [Schritt-für-Schritt-Beispiel: Nur auf aktuelle Daten reagieren](#schritt-fur-schritt-beispiel-nur-auf-aktuelle-daten-reagieren)).

### Aktualisierung der Informationen

Im **Intervall jedes Fahrzeugs** (standardmäßig 5 Minuten, im Gerät von 1 bis 30 Minuten einstellbar) aktualisiert das Plugin dieses Fahrzeug in zwei Schritten:

1. Es fragt den Zustand des **Karosseriesteuergeräts** ab (`body_controller_state`). Diese Anfrage weckt das Fahrzeug nicht. Sie aktualisiert Anwesenheit, Verriegelung und Schlafzustand.
2. **Nur wenn das Fahrzeug wach ist**, ruft es die Fahrzeugdaten ab (`vehicle_data`): Laden, Batterie, Reichweite und, je nach Einstellung **Klimaanlage ebenfalls lesen** des Geräts (standardmäßig aktiviert), die Klimatisierung.

Eine Jeedom-Aufgabe, **TeslaBLE::cycleRafraichissement**, wird **jede Minute** ausgelöst und liest nur die aktiven Fahrzeuge, deren Intervall abgelaufen ist (gemessen ab Beginn ihrer letzten Abfrage): Bei einem Fahrzeug mit 1 Minute und einem anderen mit 15 Minuten wird das erste bei jedem Durchlauf gelesen und das zweite etwa alle 15 Minuten. Ein Fahrzeug, das noch nie gelesen wurde, wird beim nächsten Durchlauf gelesen. Ein Proxy, für den kein Fahrzeug zu lesen ist, wird nicht angefragt. Diese Aufgabe wird bei der Aktivierung und beim Update des Plugins angelegt (siehe [Fehlerbehebung](#fehlerbehebung)).

Das Plugin weckt das Fahrzeug also nie von selbst auf, um die Batterie nicht zu entleeren. Solange das Fahrzeug schläft, behalten die Lade- und Klimainformationen ihren letzten bekannten Wert. Um sie auf Anforderung zu aktualisieren, verwenden Sie den Befehl **Aktualisieren (mit Aufwecken)** (siehe [Aktualisieren mit Aufwecken](#aktualisieren-mit-aufwecken)).

Schläft das Fahrzeug zwischen den beiden Anfragen ein, ist das kein Fehler: Die Lade- und Klimainformationen behalten ihren letzten Wert und es wird nichts angezeigt.

Steht **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden**, fordert die Datenanfrage nur das Laden an (`vehicle_data?endpoints=charge_state`, sichtbar im Log des Plugins in **Debug** und in den Logs des Proxys). **Letzte Datenabfrage** und **Dauer Datenabfrage** datieren dann die Ladeabfrage, und **Alter der Daten (min)** zählt die seit dieser Ladeabfrage vergangene Zeit: Die Klimainformationen bleiben dagegen eingefroren.

Ist das Fahrzeug außerhalb der Bluetooth-Reichweite des Proxys, wechselt der Befehl **Fahrzeug anwesend** auf 0. Antwortet der Proxy nicht, hat er keinen gekoppelten Schlüssel oder antwortet er zu langsam, behält die Anwesenheit ihren letzten Wert.

**Mehrere Fahrzeuge an einem Proxy.** Die Fahrzeuge eines Proxys werden nacheinander gelesen, jedes mit seinem eigenen **Letzter Fehler** und seiner eigenen **Letzte Datenabfrage**: Ein Fahrzeug außer Reichweite oder mit nicht gekoppeltem Schlüssel verhindert nicht das Lesen der anderen. Der Zyklus dauert höchstens 4 Minuten; bei 3 oder weniger Fahrzeugen an einem Proxy wird er selbst im ungünstigsten Fall nie verkürzt. Darüber hinaus werden die letzten Fahrzeuge unter Umständen nicht gelesen: Prüfen Sie deren **Letzte Datenabfrage**. Wird ein Zyklus verkürzt, erhält das Log **eine einzige** Warnung pro Vorfall („Avertissement non répété jusqu'au prochain cycle complet.“ (*Warnung wird bis zum nächsten vollständigen Zyklus nicht wiederholt.*)), danach eine **Info**-Zeile beim ersten wieder vollständigen Zyklus.

**Warum bewegen sich die Daten nicht mehr?** Die Information **Letzter Fehler** nennt die Ursache der letzten fehlgeschlagenen Abfrage, gefolgt vom Grund, den der Proxy liefert, sofern er einen angibt (zum Beispiel „Fahrzeug außer Reichweite — …“ oder „Proxy ohne Schlüssel: Kopplung erforderlich — …“). Sie kehrt auf **Keine** zurück, sobald ein Abfragezyklus erfolgreich ist. Ein schlafendes Fahrzeug ist kein Fehler: **Letzter Fehler** bleibt auf **Keine** und **Fahrzeug wach** steht auf 0. Die Information **Letzte Datenabfrage** zeigt an, von wann die Lade- und Klimadaten stammen.

Im Log des Plugins hinterlässt ein Problem nur **zwei Zeilen**: eine, wenn es beginnt, und eine, wenn wieder alles normal ist (`Véhicule « <nom> » (id <n>) : retour à la normale après [<catégorie>].`) (*Fahrzeug „<nom>“ (id <n>): Rückkehr zum Normalzustand nach [<catégorie>].*), auch wenn es stundenlang andauert. Die Stufe der Anfangszeile hängt von der Ursache ab: **Info** für ein Fahrzeug außer Reichweite (Normalsituation), **Fehler** bei einem Konfigurationsfehler (fehlende VIN oder URL) oder einem zu alten Proxy, **Warnung** bei den übrigen. Die Schlusszeile hat immer die Stufe **Info**. **Um diese Zeilen zu sehen, muss das Log des Plugins mindestens auf Stufe Info stehen** (**Plugin-Konfiguration > Logs**). Solange das Problem andauert, bleiben die Einzelheiten jedes Zyklus in **Debug** sichtbar.

Die Fahrzeuge eines Proxys werden **nacheinander** aktualisiert; verschiedene Proxys werden **parallel** gelesen. Ein Fahrzeug außer Reichweite oder mit Fehler verhindert nicht das Lesen der folgenden, und der Fehler wird mit dem Namen des Fahrzeugs im Log vermerkt.

- Dauert ein Zyklus länger als das Intervall, **überspringt** Jeedom die folgenden Durchläufe, bis er beendet ist: Die Zyklen summieren sich nie auf. Das Plugin schreibt dies dann am Ende des Zyklus ins Log (höchstens eine Warnung pro Stunde, wenn das eingestellte Intervall nicht eingehalten wird); der Takt setzt wieder ein, sobald der Zyklus beendet ist.
- Ein Zyklus überschreitet nie **4 Minuten**: Bei vielen Fahrzeugen oder einem langsamen Proxy werden die verbleibenden Fahrzeuge im nächsten Zyklus gelesen (Warnung mit den Namen dieser Fahrzeuge).
- Solange ein Befehl, ein **Aktualisieren**, ein **Aktualisieren (mit Aufwecken)** oder eine Kopplungsprüfung läuft oder auf denselben Proxy wartet, wird das Lesen des Zyklus ohne Fehler übersprungen; das nächste Lesen holt es nach.
- Bei mehreren Proxys liest der Zyklus die Proxys parallel: Ein gestoppter, ausgeschalteter, blockierter oder langsamer Proxy verzögert nur seine eigenen Fahrzeuge (ein gestoppter Proxy kostet einige Sekunden, bis zu etwa 5 s, pro Fahrzeug dieses Proxys), nie die der anderen Proxys. Der Zyklus dauert so lange wie sein langsamster Proxy. Zwei verschiedene Proxys warten nie aufeinander, auch nicht im periodischen Zyklus; auch die Befehle und **Aktualisieren** der anderen Proxys werden nicht verzögert.

### Aktualisieren mit Aufwecken

Der Befehl **Aktualisieren (mit Aufwecken)** ist die einzige Möglichkeit, die Lade- und Klimadaten eines schlafenden Fahrzeugs zu lesen. Er liest zuerst den Zustand ohne Aufwecken, weckt dann bei Bedarf das Fahrzeug und liest dessen Daten, in einer einzigen Aktion: Am Ende steht **Fahrzeug wach** auf 1, und Laden und Klimatisierung sind aktuell. Rechnen Sie in der Regel mit 15 bis 40 Sekunden; das Plugin wartet bis zu 75 Sekunden auf das Lesen nach dem Aufwecken, in denen Jeedom nutzbar bleibt.

- **Er weckt das Fahrzeug** bei jeder Ausführung auf: Häufige Verwendung verbraucht Batterie. Nach dem Lesen gelten für das Einschlaffenster (siehe [Fahrzeug einschlafen lassen](#fahrzeug-einschlafen-lassen)) und den normalen Takt wieder ihre Regeln; das Fahrzeug kann wieder einschlafen.
- **Außer Reichweite**: Der Zustand ohne Aufwecken schlägt nach 5 bis 25 Sekunden fehl, das Aufwecken wird nicht versucht und es erscheint eine eindeutige Meldung (siehe [Fehlerbehebung](#fehlerbehebung)).
- **Szenarien**: Der Befehl ist in einem Szenario nutzbar und wird durch ein geöffnetes Einschlaffenster nicht blockiert; er beendet es. Achten Sie darauf, ihn nicht in einer Schleife auszulösen (zum Beispiel bei der Änderung einer Fahrzeuginformation): Jede Ausführung weckt das Fahrzeug. Bei einem schlafenden Fahrzeug wechselt **Fahrzeug wach** kurz auf 0 (vor dem Aufwecken gelesener Zustand) und dann auf 1.
- **Aktualisieren** behält sein Verhalten: Es weckt das Fahrzeug nie auf.

### Beschleunigtes Lesen während des Ladens

Um einen Ladevorgang genau zu verfolgen (zum Beispiel bei Steuerung nach Solarüberschuss), stellen Sie im Gerät **Intervall während des Ladens** ein (standardmäßig deaktiviert):

- **Auslösung.** Sobald ein Lesevorgang feststellt, dass das Fahrzeug **lädt** (Ladezustand Charging oder Starting), ersetzt das Ladeintervall das Aktualisierungsintervall, sofern es kürzer ist. Bei 5 Minuten im Normalbetrieb und 1 Minute beim Laden werden die Daten jede Minute neu gelesen (beobachten Sie **Letzte Datenabfrage**).
- **Rückkehr zum Normalbetrieb.** Sobald ein Lesevorgang das Laden nicht mehr feststellt (Ladeende, Kabel abgezogen, Laden unterbrochen), das Fahrzeug schläft, außer Reichweite ist oder der Proxy nicht erreichbar ist, wird das normale Intervall ab diesem Lesevorgang gezählt: keine Zyklusverzögerung.
- **Untergrenze von einer Minute.** Es wird kein Wert unter einer Minute angeboten: Jeedom startet die Aktualisierung jede Minute und der Proxy hält die Daten 30 Sekunden im Cache. Ein von einem Skript gespeicherter kleinerer Wert wird auf 1 Minute angehoben (Warnung im Log), ein unbekannter Wert deaktiviert die Einstellung.
- **Kein Aufwecken.** Der Inhalt eines Lesevorgangs ändert sich nicht: Der Zustand wird ohne Aufwecken gelesen, die Daten nur, wenn das Fahrzeug wach ist. Die Daten eines schlafenden Fahrzeugs werden aufgrund dieser Einstellung nie gelesen.

Um den Mechanismus zu verfolgen, stellen Sie das Log des Plugins auf **Debug**: Eine Zeile zeigt den Wechsel zum Ladeintervall, eine andere die Rückkehr zum normalen Intervall.

Einschränkungen: Der Ladetakt beginnt erst beim ersten Lesevorgang, der das Laden sieht (höchstens ein normales Intervall später, oder sofort mit **Aktualisieren**); während eines geöffneten Einschlaffensters wird ein Ladevorgang, der ohne sichtbare Änderung des Zustands ohne Aufwecken gestartet wurde, erst beim Kontrolllesen gesehen; wurde der Proxy mit einer Cache-Dauer der Daten von mindestens 60 Sekunden eingestellt, werden ihm die Lesevorgänge im 1-Minuten-Takt aus dem Cache geliefert; ein unterbrochener Ladevorgang (Zustand Stopped, Kabel angeschlossen) löst die Beschleunigung nicht aus, und seine Wiederaufnahme wird erst im normalen Intervall gesehen; ein schlafendes Fahrzeug beim Laden wird nicht schneller gelesen; ein fehlgeschlagener Lesevorgang während des Ladens setzt das normale Intervall bis zum nächsten erfolgreichen Lesevorgang wieder ein.

### Fahrzeug einschlafen lassen

Ein waches Fahrzeug schläft nach etwa fünfzehn Minuten ohne Anforderung von selbst ein. Eine Abfrage der Lade- und Klimadaten alle paar Minuten kann es daran hindern und die Batterie belasten. Das Plugin kann sich daher „in Vergessenheit bringen“, wenn es nichts Neues zu lesen gibt:

- **Öffnung.** Ist das Fahrzeug wach, **nicht am Laden** (Ladezustand Nicht angeschlossen, Abgeschlossen, Gestoppt oder Ohne Stromversorgung), **ohne Insassen**, und sind seine Daten und sein Zustand über die eingestellte Anzahl von Lesevorgängen (standardmäßig 3) **unverändert**, öffnet das Plugin ein **Einschlaffenster** (standardmäßig 30 Minuten).
- **Während des Fensters** wird nur der Zustand ohne Aufwecken gelesen, im Intervall des Fahrzeugs (Anwesenheit, Verriegelung, Schlafzustand, Türen, Kofferräume, Ladeklappe, Insasse). Die Lade- und Klimadaten, die **Letzte Datenabfrage** und die Dauern der Datenabfrage werden nicht mehr aktualisiert: Sie behalten ihren letzten Wert, wie bei einem schlafenden Fahrzeug. Das Plugin weckt das Fahrzeug für diese Prüfungen nie auf.
- **Ende des Fensters**, mit Wiederaufnahme des vollständigen Lesens beim nächsten Durchlauf (beim selben Durchlauf bei Aktivität): Aktivität im Zustand ohne Aufwecken (Entriegelung, Tür, Kofferraum oder Ladeklappe, Insasse), an das Fahrzeug gesendeter Befehl (ausdrückliches Aufwecken eingeschlossen), Schaltfläche **Aktualisieren** oder **Aktualisieren (mit Aufwecken)**, schlafendes Fahrzeug, Fahrzeug außer Reichweite, deaktiviertes Kontrollkästchen oder Ablauf der Dauer. Nach Ablauf der Dauer erfolgt ein **Kontrolllesen**: Hat sich nichts geändert, wird das Fenster verlängert.
- **Nie beim Laden.** Ein ladendes Fahrzeug, ein Fahrzeug beim Ladestart oder in einem unbekannten Ladezustand öffnet nie ein Fenster.
- **Klimahaltemodus aktiv.** Solange **Klimahaltemodus (Hund, Camp)** `On`, `Dog` oder `Party` (oder einen anderen nicht vorgesehenen Wert) hat, öffnet sich kein Fenster: Das Lesen läuft im Intervall des Fahrzeugs weiter, damit die **Innentemperatur** im Hunde- oder Campmodus aktuell bleibt. `Off`, `Unknown` oder eine fehlende Information (zum Beispiel nicht gelesene Klimatisierung) lassen das Fenster sich öffnen.
- **Klimatisierung nicht gelesen.** Steht **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden**, sieht das Fenster die Aktivität der Klimatisierung nicht mehr (ihre Informationen werden nicht gelesen). Das Umschalten dieser Einstellung setzt den Zähler der unveränderten Lesevorgänge zurück.

Um den Mechanismus zu verfolgen, stellen Sie das Log des Plugins auf die Stufe **Info**: Eine Zeile zeigt die Öffnung („fenêtre d'endormissement ouverte pour … min … jusqu'à HH:MM environ“ (*Einschlaffenster für … min geöffnet … bis etwa HH:MM*)) und eine weitere das Ende („fin de la fenêtre d'endormissement après … min : …“ (*Ende des Einschlaffensters nach … min: …*)). In **Debug** wird jeder ausgesetzte Durchlauf vermerkt. Um die Wirkung zu prüfen, beobachten Sie **Fahrzeug wach**: Es sollte nach der üblichen Zeit (etwa fünfzehn Minuten) auf 0 wechseln, während es ohne Fenster auf 1 bleiben konnte. Das ist ein erwarteter, aber nicht garantierter Effekt: Er hängt vom Fahrzeug ab. Schläft das Fahrzeug nicht ein, vergleichen Sie mit deaktiviertem Kontrollkästchen.

Einschränkungen: Ein Ladevorgang, der ohne sichtbare Änderung des Zustands ohne Aufwecken gestartet wurde (Kabel bereits angeschlossen, geplantes oder aus der App gestartetes Laden), wird erst beim Kontrolllesen gesehen, also höchstens die Dauer des Fensters plus ein Intervall später; eine aus der App während des Fensters gestartete Klimatisierung ebenso. Das Anschließen eines Kabels aus dem nicht angeschlossenen Zustand wird sofort gesehen (die Ladeklappe öffnet sich). Ein Telefonschlüssel in der Nähe, der den Insassen als „anwesend“ hält, verhindert die Öffnung des Fensters.

### Ausführung der Befehle

Jeder Aktionsbefehl wird an den Proxy übermittelt, der die Bestätigung des Fahrzeugs abwartet, bevor er antwortet. Das Plugin muss das Fahrzeug vor einem Befehl nicht aufwecken: Das übernimmt der Proxy.

**Vor dem Senden geprüfte Werte.** Ein ungültiger Wert wird sofort mit einer Meldung abgelehnt, ohne dass etwas an den Proxy gesendet wird:

- **Ladestrom**: eine ganze Zahl zwischen dem **Min** und dem **Max** des Befehls (0 bis 32 A, solange das Fahrzeug seine Grenze nicht veröffentlicht hat, danach der maximale Strom, den es meldet). Ein Dezimalwert (`16,5`) oder ein Text wird abgelehnt.
- **Ladelimit**: eine ganze Zahl zwischen dem **Min** und dem **Max** des Befehls (50 bis 100 %, solange das Fahrzeug seine Grenzen nicht veröffentlicht hat, danach seine minimale und maximale Grenze).
- **Wächter-Modus einstellen**: **Aktiviert** oder **Deaktiviert** (die frühere Option „Keine“ gibt es nicht mehr).

**Vom Fahrzeug nachgeführte Grenzen.** Bei jeder erfolgreichen Datenabfrage setzt das Plugin das **Min** und das **Max** der Schieberegler **Ladelimit** und **Ladestrom** auf das, was das Fahrzeug akzeptiert (Informationen **Minimale Ladegrenze**, **Maximale Ladegrenze** und **Maximaler Ladestrom**), und der Schieberegler des Widgets folgt, ohne die Seite neu zu laden. Ein Wert von 0, ein fehlender oder unplausibler Wert wird ignoriert: Die vorherigen Grenzen bleiben erhalten, wie wenn das Fahrzeug schläft. **Eine manuelle Einstellung hat Vorrang**: Wenn Sie selbst ein **Min** oder **Max** eingeben, das vom vom Plugin gesetzten abweicht, wird es nie wieder verändert (auch nicht nach mehreren Lesevorgängen oder beim Speichern des Geräts); ein eingegebener Wert, der dem vom Plugin gesetzten entspricht, wird weiter nachgeführt (um eine Grenze festzuhalten, geben Sie also einen Wert ein, der sich vom vom Plugin gesetzten unterscheidet); jeder andere Wert, selbst wenn er in diesem Moment dem des Fahrzeugs entspricht, ist eine manuelle Einstellung; eine Grenze, die Sie über die des Fahrzeugs hinaus erweitern, erlaubt einen Sollwert, den das Fahrzeug eventuell ablehnt. Um zur automatischen Nachführung zurückzukehren, **leeren** Sie das Feld: Es wird beim nächsten Lesevorgang wiederhergestellt. Um eine Grenze festzuhalten (zum Beispiel 48 A), stellen Sie das **Max** von Hand ein; um die Grenzen sofort zu aktualisieren, starten Sie **Aktualisieren (mit Aufwecken)**. Der maximale Strom kann von der angeschlossenen Ladestation abhängen und wird nicht veröffentlicht, wenn das Fahrzeug nicht angeschlossen ist: Die vorherigen Grenzen bleiben dann bestehen.

> **Verhaltensänderung**: Ein Sollwert **über dem vom Fahrzeug gemeldeten Maximum** (zum Beispiel 20 A, wenn es 16 A meldet) wird nun mit einer Meldung **abgelehnt**, statt akzeptiert und dann vom Fahrzeug stillschweigend reduziert zu werden.

**Bei einem Fehlschlag.** Lehnt der Proxy oder das Fahrzeug den Befehl ab, erscheint eine Fehlermeldung in Rot in der Jeedom-Oberfläche (und im Log des Plugins als Fehler), und sie wird auch in der Information **Letzter Fehler** gespeichert, wo sie bis zum nächsten erfolgreichen Abfragezyklus angezeigt bleibt (beim nächsten Lesevorgang, standardmäßig höchstens 5 Minuten). Zum Beispiel „Dieser Befehl erfordert einen Schlüssel mit der Rolle Owner: Der Proxy-Schlüssel hat wahrscheinlich die Rolle Charging Manager …“, wenn ein der Rolle Owner vorbehaltener Befehl abgelehnt wird: siehe [Schlüsselrolle](#rolle-des-schlussels).

**Nach einem erfolgreichen Befehl.** Das Ladelimit, der Ladestrom und die Verriegelung werden sofort aktualisiert, dann wird der Zustand des Fahrzeugs (Anwesenheit, Wachzustand) ohne Aufwecken neu gelesen. Das Fahrzeug wird anschließend **einmal erneut gelesen** nach einer Verzögerung (standardmäßig 30 Sekunden, pro Fahrzeug einstellbar), ohne den periodischen Lesevorgang abzuwarten, um die tatsächlichen Werte anzuzeigen (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)). Der Befehl selbst gibt sofort die Kontrolle zurück.

**Ein Befehl oder ein Lesevorgang zugleich.** Die Abfragen an einen Proxy erfolgen nacheinander: Ein Befehl, ein **Aktualisieren** oder eine Kopplungsprüfung wartet nur auf die bereits laufenden oder bereits wartenden Abfragen dieses Proxys (bis zu etwa 2 Minuten, 15 Sekunden bei der Prüfung) und hat Vorrang vor den periodischen Lesevorgängen, die zurückstehen und im nächsten Zyklus wieder aufgenommen werden. Die Reihenfolge bei mehreren gleichzeitigen Anforderungen ist nicht garantiert. Zwei verschiedene Proxys warten nie aufeinander, auch nicht im periodischen Zyklus (der Zyklus liest die Proxys parallel: siehe Aktualisierung). Sind Proxy und Fahrzeug an der Grenze ihrer Zeitlimits, kann die Antwort 3 bis 4 Minuten dauern. Jeedom bleibt in dieser Zeit nutzbar.

### Erneutes Lesen nach einem Befehl

Unmittelbar nach einem Befehl liefert der Proxy noch seine früheren Daten (er hält sie **30 Sekunden** im Cache). Statt bis zur nächsten Aktualisierung einen veralteten Wert anzuzeigen, **plant** das Plugin ein **erneutes Lesen** des Fahrzeugs, sobald dieser Cache abgelaufen ist:

- **Auslösung.** Nach jedem **erfolgreichen** Befehl (Ladelimit, Strom, Start oder Stopp des Ladens, Klimatisierung, Verriegelung, Ladeklappe usw.). Ein fehlgeschlagener Befehl plant nichts.
- **Verzögerung.** Standardmäßig **30 Sekunden** nach Ende des Befehls, pro Fahrzeug einstellbar (**Verzögerung des erneuten Lesens nach Befehl**: 30 Sekunden, 45 Sekunden, 1 Minute, 1 Minute 30 oder 2 Minuten). Nie weniger als 30 Sekunden, die Cache-Dauer des Proxys: Eine kürzere Verzögerung würde den Wert vor dem Befehl erneut lesen. Wenn Sie diesen Cache im Proxy verlängert haben, wählen Sie eine mindestens gleich lange Verzögerung.
- **Der Befehl wartet nicht.** Er gibt die Kontrolle zurück, sobald er ausgeführt ist; das erneute Lesen läuft im Hintergrund.
- **Ein einziges erneutes Lesen für mehrere dicht aufeinanderfolgende Befehle.** Strom, dann Limit innerhalb weniger Sekunden: Nur das nach dem **letzten** Befehl geplante erneute Lesen liest das Fahrzeug, die vorherigen brechen von selbst ab.
- **Inhalt des erneuten Lesens.** Der eines **Aktualisieren**: der Zustand ohne Aufwecken, dann die Lade- und Klimadaten **nur, wenn das Fahrzeug wach ist**. **Es weckt das Fahrzeug nie auf**: Ist es wieder eingeschlafen, ist das kein Fehler: Die letzten Werte bleiben erhalten. Ist es außer Reichweite, wechselt die Anwesenheit auf „Nein“; ist der Proxy nicht erreichbar, wird „Letzter Fehler“ gefüllt. Es beendet das Einschlaffenster, wie ein Befehl, und verschiebt nicht den Takt der periodischen Aktualisierung.
- **Aufwecken** liest das Fahrzeug daher anschließend ebenfalls erneut, ohne es nochmals aufzuwecken (der Befehl hat es gerade getan).
- **Kosten.** Jeder erfolgreiche Befehl fügt **einen Bluetooth-Lesevorgang** hinzu (Zustand, dann Daten, wenn wach) über den Proxy. Ein Szenario, das den Ladestrom jede Minute einstellt, löst jede Minute ein erneutes Lesen zusätzlich zum periodischen Lesevorgang aus: Legen Sie die Befehle eines Szenarios mit Abstand statt sie zu wiederholen. Auch eine Hupe oder eine Lichthupe löst ein erneutes Lesen aus.
- **Prozess.** Jedes erneute Lesen ist eine **einmalige Aufgabe** des Jeedom-Cron-Systems (**Einstellungen > Systeme > Cron-System**, **TeslaBLE::relectureApresCommande**): Sie ist dort einige Sekunden bis einige Minuten sichtbar und verschwindet dann von selbst. Ein durch einen neueren Befehl ersetztes erneutes Lesen verschwindet nach einigen Sekunden. Es ist kein Daemon und es läuft nichts dauerhaft. Ist das Cron-System von Jeedom deaktiviert, findet kein erneutes Lesen statt (wie bei der periodischen Aktualisierung), und die Werte werden beim nächsten Lesevorgang aktualisiert.

Um den Mechanismus zu verfolgen, stellen Sie das Log des Plugins auf **Debug**: Eine Zeile zeigt die Planung („relecture programmée dans 30 s“ (*erneutes Lesen in 30 s geplant*)), dann das erneute Lesen („lecture sans réveil“ (*Lesen ohne Aufwecken*)) oder seinen Abbruch („remplacée par une commande plus récente“ (*durch einen neueren Befehl ersetzt*), „abandonnée : proxy occupé“ (*abgebrochen: Proxy ausgelastet*)).

### Überschusssteuerung

Die Aktion **Nach Überschuss anpassen** (`adjust_surplus`) folgt einem Photovoltaik-Überschuss, **ohne das Fahrzeug mit Bluetooth-Befehlen zu überlasten**: Jeder Befehl kann bis zu 75 Sekunden dauern und weckt das Fahrzeug auf. Ihr Szenario sendet die **für das Laden verfügbare Leistung**, und das Plugin entscheidet, ob tatsächlich gehandelt werden muss. Die Standardwerte sind im realen Betrieb zu validieren (siehe [Bekannte Einschränkungen](#bekannte-einschrankungen)).

**Der gesendete Wert ist eine absolute Leistung in Watt.** Es ist das, was das Fahrzeug verbrauchen kann, keine Änderung. Wenn Ihr Zähler den **Netzexport** misst, ist die verfügbare Leistung **der Export plus die aktuelle Ladeleistung**: Ohne diese Addition würde der Sollwert bei jeder Anpassung wieder absinken. Ein negativer Wert wird auf 0 W gesetzt; ein Wert, der keine Wattzahl ist, wird mit der Meldung **„Ungültiger Wert: Die verfügbare Leistung muss eine Anzahl Watt sein“** abgelehnt.

**Vom Watt zum Ampere.** Der Strom pro Phase ergibt sich aus der Leistung geteilt durch die **Spannung** und durch die Anzahl der **Phasen** (zwei Einstellungen des Geräts, die nie vom Fahrzeug gelesen werden), **abgerundet** auf den **Anpassungsschritt**. ⚠️ Eine dreiphasige Ladestation, die auf einphasig eingestellt ist, ergäbe den **dreifachen** gewünschten Strom: Prüfen Sie die Einstellung **Phasen**.

**Wann das Plugin einen Befehl sendet.** Höchstens **ein** Befehl pro Aufruf, aus **Ladestrom**, **Laden starten** und **Laden beenden**:

- Der Zielstrom ist durch das **Max** des Schiebereglers **Ladestrom** begrenzt (ein höherer berechneter Wert wird auf das Max gesetzt; umgekehrt bleibt die manuelle Eingabe eines Werts über dem Max abgelehnt) und wird während des Ladens nie **unter die Abschaltschwelle** gesetzt;
- **Nichts wird gesendet**, wenn der Zielstrom mit dem zuletzt gesendeten Sollwert identisch ist oder um weniger als die **Hysterese** davon abweicht;
- **höchstens ein Befehl pro Intervall**: Das **Mindestintervall** wird ab dem **Ende** des vorherigen Befehls gezählt, ob er erfolgreich war oder fehlgeschlagen ist;
- **Stopp**: Wenn der berechnete Strom während der **Haltedauer** unter der **Abschaltschwelle** bleibt, wird das Laden beendet;
- **Start**: Bei beendetem Laden wird es neu gestartet, sobald der berechnete Strom den **minimalen Startstrom** erreicht. Der Start erfolgt in **zwei Schritten**, wenn der letzte Sollwert nicht bekannt ist oder wenn er den Zielstrom um mindestens die **Hysterese** übersteigt: zuerst **Ladestrom**, dann **Laden starten** im nächsten Intervall (ein Intervall Verzögerung). Sobald **Ladestrom** im Stillstand gesendet wurde, gilt der Sollwert **so lange als bekannt, bis das Laden gestartet ist**, unabhängig vom Takt Ihres Szenarios: **Laden starten** wird dann direkt gesendet. Ohne diesen Handshake gilt der Sollwert nur dann als bekannt, wenn der letzte Befehl der Steuerung weniger als 10 Minuten zurückliegt; er wird außerdem vergessen, sobald das Laden abgeschlossen ist, die Ladestation keinen Strom mehr liefert oder das Fahrzeug abgesteckt wird (der erste Start am nächsten Tag beginnt also mit **Ladestrom**).

**Enthaltungen.** Es wird kein Befehl gesendet, ohne Ausnahme im Szenario, und der Grund erscheint unter **Letzter Fehler**: **„Fahrzeug nicht angeschlossen: Anpassung nach Überschuss ignoriert“**, **„Fahrzeug außerhalb der Reichweite des Proxys: …“**, **„Laden abgeschlossen: …“**, **„Die Ladestation liefert keinen Strom: …“** und **„Ladezustand unbekannt: Starten Sie Aktualisieren (mit Aufwecken)“**. Diese Meldungen ersetzen nie einen echten Fehler des letzten Lesezyklus, und der nächste erfolgreiche Zyklus setzt den Wert auf **Keine** zurück. Die Steuerung stützt sich auf den zuletzt veröffentlichten **Ladestatus**: Nach einem Start oder Stopp, den sie soeben befohlen hat, geht sie bis zum nächsten Lesevorgang (höchstens 5 Minuten) vom befohlenen Zustand aus. Die Aktivierung des **Intervalls während des Ladens** wird empfohlen.

**Kein Aufwecken.** Die Steuerung weckt das Fahrzeug nie auf und liest nichts, um zu entscheiden; ein ignorierter Aufruf kontaktiert den Proxy nicht. Ein tatsächlich gesendeter Befehl weckt das Fahrzeug wie jeder Befehl auf.

**Niedertarifzeit.** Während des Zeitraums des **Ladens zur Niedertarifzeit** eines Fahrzeugs wird der Aufruf von **Nach Überschuss anpassen** **ignoriert** (ohne Fehler, ohne Befehl, mit einer Debug-Zeile im Log): Andernfalls würde ein Solar-Szenario, das nachts 0 W sendet, das Laden zur Niedertarifzeit beenden. Außerhalb des Zeitraums funktioniert die Überschusssteuerung wie gewohnt (siehe [Laden zur Niedertarifzeit](#laden-zur-niedertarifzeit)).

**Beispielszenario.** Siehe das [Schritt-für-Schritt-Beispiel: Solarladen mit Nach Überschuss anpassen](#schritt-fur-schritt-beispiel-solarladen-mit-nach-uberschuss-anpassen). Vervielfachen Sie die Aufrufe nicht: Das Plugin ignoriert diejenigen, die nichts bringen.

**Ungültige Einstellungen.** Eine Einstellung außerhalb der Grenzen (Schritt bei 0, Intervall unter 60 s, Abschaltschwelle über dem Startstrom …) wird **beim Speichern** des Geräts mit einer Meldung **„Überschusssteuerung: …“** abgelehnt.

### Ladeplan erstellen

Die Aktionen **Ladeplan hinzufügen** (`add_charge_schedule`) und **Ladeplan löschen** (`remove_charge_schedule`) erstellen oder entfernen im Fahrzeug **einen von Jeedom verwalteten Ladeplan**. Sie werden **ausgeblendet** erstellt: Man ruft sie aus einem Szenario auf (oder macht sie im Reiter **Befehle** sichtbar).

**Proxy des Forks erforderlich.** Der offizielle Proxy 2.3.0 kann das Laden nicht planen: Die entsprechende Route existiert bei ihm nicht, sie wurde vom Fork hinzugefügt (Versionen der Form `2.3.0-tb.N`). Solange der Proxy diese beiden Befehle nicht meldet, werden sie **sofort abgelehnt**, ganz ohne Austausch mit dem Fahrzeug, mit der Meldung **„Von Ihrer Proxy-Version nicht unterstützt“**; der Rest des Geräts funktioniert normal. Die Verfügbarkeit folgt der Meldung des Proxys (Route `capabilities`), die erneut gelesen wird, wenn sich seine Version ändert: Nach dem Wechsel zum Proxy des Forks (Version der Form `2.3.0-tb.N`) werden die Befehle verfügbar, ohne das Plugin neu zu installieren. Ein Update des Forks **ohne Änderung der Versionsnummer** wird erst berücksichtigt, wenn sich die Versionsnummer ändert.

**Parameter.** Im Szenario nimmt die Aktion **Ladeplan hinzufügen** zwei Felder entgegen:

- **Tage des Ladeplans** (Titel): ein oder mehrere Tage, getrennt durch Kommas, Semikolons oder Leerzeichen, ohne Beachtung der Groß- und Kleinschreibung: `lun`, `mar`, `mer`, `jeu`, `ven`, `sam`, `dim` (oder der ganze Name, oder die englische Abkürzung `mon` … `sun`), `tous` (alle Tage) oder `semaine` (Montag bis Freitag). Beispiel: `lun,mar,mer,jeu,ven`.
- **Startzeit (HH:MM)** (Nachricht): von `00:00` bis `23:59`, zum Beispiel `23:00` (`23h00` wird ebenfalls akzeptiert). Es ist die **Ortszeit des Fahrzeugs**.

Jeder ungültige Parameter wird **vor** dem Senden mit einer Meldung abgelehnt, die das erwartete Format erklärt; es wird nichts an das Fahrzeug gesendet.

**Koordinaten von Jeedom.** Das Fahrzeug löst einen Ladeplan nur aus, wenn es sich am angegebenen Ort befindet. Das Plugin verwendet die **Koordinaten von Jeedom** (Einstellungen, Systeme, Konfiguration, Reiter **Allgemein**, Rubrik **Koordinaten**: Breitengrad und Längengrad): Tragen Sie sie ein, sonst wird der Befehl mit der Meldung **„Koordinaten von Jeedom fehlen oder sind ungültig“** abgelehnt. Wenn das Fahrzeug nicht an diesem Ort geparkt ist, existiert der Ladeplan, wird aber nicht ausgelöst. Die Koordinaten werden nie in die Logs geschrieben.

**Ein einziger Ladeplan, bei jedem Hinzufügen ersetzt.** Das Plugin verwaltet **einen** Ladeplan pro Fahrzeug und merkt sich seine Kennung: Ein neues Hinzufügen **ersetzt** den vorherigen Ladeplan (gleiche Tage und Uhrzeit werden ersetzt, grundsätzlich ohne Duplikat: Das Ersetzen anhand der Kennung ist im realen Betrieb noch zu bestätigen). Der Ladeplan deckt das Laden ab der Startzeit ab; es gibt weder eine Endzeit noch einen Strom oder ein Limit, die dem Ladeplan eigen wären. Ladepläne, die in der Tesla-App erstellt wurden, werden weder geändert noch gelöscht. Wenn Sie die VIN des Geräts ändern, wird die gemerkte Kennung nicht mehr verwendet: Das nächste Hinzufügen erstellt einen neuen Ladeplan.

**Löschen.** **Ladeplan löschen** entfernt den von Jeedom erstellten Ladeplan. Wenn Jeedom keinen erstellt hat (oder er bereits gelöscht ist), tut die Aktion nichts und erzeugt **keinen Fehler**. Wenn das Fahrzeug das Löschen aus einem anderen Grund als einer unzureichenden Schlüsselrolle ablehnt (zum Beispiel weil der Ladeplan in der App gelöscht wurde), wird die Ablehnungsmeldung angezeigt und die Kennung vergessen: Ein zweites Löschen verläuft still, und ein neues Hinzufügen erstellt einen neuen Ladeplan.

**Nach dem Befehl.** Ein erneutes Lesen wird wie nach jedem Befehl eingeplant (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)): Die Informationen zum Ladeplan (**Geplante Ladezeit** …) werden aktualisiert, **sofern das Fahrzeug sie** beim Lesen der Daten **zurückgibt**; die Planung sollte auch in der Tesla-App geprüft werden.

**Schlüsselrolle.** Die mindestens erforderliche Rolle ist nicht bestätigt (**Charging Manager** wahrscheinlich). Eine Berechtigungsablehnung wird mit dem Hinweis „Rolle des Proxy-Schlüssels unzureichend?“ angezeigt (siehe [Schlüsselrolle](#rolle-des-schlussels)).

### Laden zur Niedertarifzeit

Das Plugin kann das Laden während der Niedertarifzeit Ihres Stromvertrags bis zu einem gewählten **Ziel-SoC** **selbst starten und beenden**. Das funktioniert mit dem offiziellen Proxy 2.3.0 und **hängt nicht von den im Fahrzeug gespeicherten Ladeplänen ab** (siehe [Ladeplan erstellen](#ladeplan-erstellen) für diese). Die Einstellungen befinden sich im Abschnitt **Laden zur Niedertarifzeit** des Geräts; aktivieren Sie **Aktivieren** (**Ladesteuerung**), tragen Sie **Beginn des Zeitraums**, **Ende des Zeitraums** und **Ziel-SoC (%)** ein und speichern Sie dann.

**Schritt für Schritt: Laden zur Niedertarifzeit konfigurieren.**

1. Öffnen Sie **Plugins > Verbundene Objekte > Tesla BLE** und dann das Gerät des Fahrzeugs (Reiter **Gerät**), Abschnitt **Laden zur Niedertarifzeit**.
2. Aktivieren Sie **Aktivieren** (**Ladesteuerung**).
3. Tragen Sie **Beginn des Zeitraums** und **Ende des Zeitraums** gemäß Ihrem Stromvertrag in der Zeit von Jeedom ein, zum Beispiel `22:00` und `06:00` (ein Zeitraum über Mitternacht hinaus wird akzeptiert; das Ende muss sich vom Beginn unterscheiden).
4. Tragen Sie **Ziel-SoC (%)** ein: den Batteriestand, von 1 bis 100, bei dem Jeedom das Laden beendet. Wählen Sie ein Ziel **kleiner oder gleich dem Ladelimit des Fahrzeugs**.
5. Aktivieren Sie **Am Ende des Zeitraums stoppen**, wenn das Laden nicht über die Niedertarifzeit hinaus fortgesetzt werden soll (deaktiviert: Es läuft bis zum Limit des Fahrzeugs weiter).
6. Für ein präzises Beenden beim Ziel-SoC stellen Sie außerdem **Intervall während des Ladens** auf 1 oder 2 Minuten (siehe weiter unten, **Genauigkeit**).
7. **Speichern** Sie. Eine ungültige Einstellung wird mit einer Meldung **„Laden zur Niedertarifzeit: …“** abgelehnt (siehe [Fehlerbehebung](#fehlerbehebung)): Nichts wird gespeichert.
8. Prüfen Sie: Stellen Sie das Log des Plugins auf **Info** (**Konfiguration des Plugins > Logs**). Beim ersten Lesen des Fahrzeugs im Zeitraum zeigt eine Zeile **„charge aux heures creuses : décision …“** *(Laden zur Niedertarifzeit: Entscheidung …)*, was das Plugin entschieden hat und warum (`charge_start`, `charge_stop`, `aucune` …). Wenn nichts startet, siehe [Erweitertes Laden: Symptome ohne Meldung](#erweitertes-laden-symptome-ohne-meldung).

**Gut zu wissen.** Zwei Verhaltensweisen überraschen oft:

- **Ladelimit des Fahrzeugs.** Liegt der **Ziel-SoC** **über** dem Ladelimit des Fahrzeugs, endet das Laden am Limit des Fahrzeugs, ohne Fehler oder Warnung: Der Ziel-SoC wird nie erreicht. Umgekehrt beendet ein Ziel-SoC unter dem Limit das Laden früher.
- **Manuelle Aktion.** Ein **Laden starten** oder **Laden beenden**, das von Jeedom aus (Widget, Szenario) während des Zeitraums ausgelöst wird, **setzt die Steuerung bis zum nächsten Zeitraum aus**: Jeedom widerspricht Ihrer Aktion nie. Ein Laden, das nach dem Stopp beim Ziel-SoC aus der Tesla-App neu gestartet wird, setzt die Steuerung ebenfalls aus.

**Was das Plugin tut.** Bei jedem Lesen des Fahrzeugs durch den Aktualisierungszyklus:

- **im Zeitraum**, Fahrzeug **angeschlossen** und **unter dem Ziel-SoC**: **Laden starten**;
- **im Zeitraum**, laufendes Laden, dessen Stand den Ziel-SoC erreicht: **Laden beenden**, **auch wenn das Ladelimit des Fahrzeugs höher ist** (der Ziel-SoC wird mit dem **Batteriestand (roh)** verglichen, der um einige Punkte von der **Batterieladung** abweichen kann);
- **am Ende des Zeitraums**, wenn **Am Ende des Zeitraums stoppen** aktiviert ist: Das noch laufende Laden wird beim ersten Lesen des Fahrzeugs **innerhalb der Stunde nach** dem Ende beendet (danach wird das Laden nicht mehr unterbrochen);
- **kein unnötiger Befehl**: kein Start, wenn das Laden bereits läuft oder das Ziel erreicht ist, kein Stopp, wenn es bereits beendet ist. **Höchstens ein Befehl pro Lesevorgang.**

**Zeit von Jeedom.** Der Zeitraum wird in der Zeit von Jeedom (seiner Zeitzone) gelesen, nicht in der des Fahrzeugs. Ein Zeitraum über Mitternacht (`22:00` bis `06:00`) funktioniert; der Beginn ist eingeschlossen, das Ende ausgeschlossen.

**Genauigkeit.** Die Entscheidung folgt dem **Lesetakt** des Fahrzeugs: Das Beenden beim Ziel-SoC kann bei weit auseinanderliegenden Lesevorgängen um einige Prozent überschritten werden. Für ein präzises Beenden aktivieren Sie das **Intervall während des Ladens** (1 oder 2 Minuten, siehe [Beschleunigtes Lesen während des Ladens](#beschleunigtes-lesen-wahrend-des-ladens)). Ein Aktualisierungsintervall von **höchstens 15 Minuten** wird empfohlen: Bei einem langen Intervall kann der veröffentlichte Zustand veraltet sein.

**Ruhezustand des Fahrzeugs.** Das Plugin **weckt das Fahrzeug nie von sich aus auf**, um zu entscheiden: Es stützt sich auf die bereits veröffentlichten Informationen. Dagegen **weckt Laden starten das Fahrzeug auf** (der Proxy tut dies selbst) wie jeder Befehl, und ein als **schlafend** erkanntes Fahrzeug erhält **nie** einen Stoppbefehl (ein von einem schlafenden Fahrzeug veröffentlichtes Laden ist ein veralteter Zustand). Wenn der angezeigte Zustand von einem schlafenden Fahrzeug stammt, gibt die Meldung unter **Letzter Fehler** dies an („Zustand um HH:MM gelesen, Fahrzeug schläft“).

**Keine Aktion in diesen Fällen.** Die Funktion ist deaktiviert; das Fahrzeug ist **abgesteckt**, **außer Reichweite** oder konnte nicht gelesen werden; die Ladestation liefert keinen Strom; der Ladezustand ist unbekannt; das Laden ist **abgeschlossen** (Limit des Fahrzeugs erreicht); der **Ziel-SoC überschreitet das Limit des Fahrzeugs** (das Laden endet dann an diesem Limit, ohne Fehler oder Warnung: Wählen Sie ein Ziel kleiner oder gleich dem Limit). Der Grund ist unter **Letzter Fehler** sichtbar: **„Fahrzeug nicht angeschlossen: Laden zur Niedertarifzeit wartet“**, **„Die Ladestation liefert keinen Strom: Laden zur Niedertarifzeit wartet“** oder **„Ladezustand unbekannt: Starten Sie Aktualisieren (mit Aufwecken)“**. Diese Meldungen ersetzen nie einen echten Fehler des letzten Lesezyklus, und der nächste erfolgreiche Zyklus setzt den Wert auf **Keine** zurück.

**Manuelle Befehle und Szenarien (Priorität).** **Laden starten** und **Laden beenden** bleiben jederzeit verwendbar. Ein **Start** oder **Stopp**, der **von Jeedom aus** (Widget, Szenario) **während des Zeitraums** oder in der Stunde nach seinem Ende ausgelöst wird, **setzt die Steuerung bis zum nächsten Zeitraum aus**: Jeedom widerspricht Ihrer Aktion nie und beendet das Laden am Ende des Zeitraums auch nicht. Am nächsten Tag setzt die Steuerung wieder ein. Die Meldung ist nur eine Zeile im Log (kein Fehler). Zwei Fälle werden gesondert behandelt:

- **aus der Tesla-App neu gestartetes Laden nach dem Stopp beim Ziel-SoC**: festgestellt durch einen Lesevorgang mindestens **2 Minuten** nach dem Stopp, setzt es die Steuerung ebenfalls aus (**„Laden zur Niedertarifzeit bis zum nächsten Zeitraum ausgesetzt: Laden außerhalb der Steuerung neu gestartet“**) und wird nicht mehr unterbrochen;
- **aus der App gestopptes Laden nach einem Start durch Jeedom**: Jeedom **startet das Laden nicht neu** (nur ein Start pro Anschluss); folgt auf den Start kein Laden, erscheint die Meldung **„Laden von Jeedom gestartet, aber gestoppt oder nicht gestartet: Kein neuer Versuch vor dem nächsten Zeitraum“** (siehe [Fehlerbehebung](#fehlerbehebung)).

**Befehlsfehler.** Ein fehlgeschlagener Befehl (Ablehnung durch das Fahrzeug, Zeitüberschreitung, unzureichende Schlüsselrolle) zeigt seine Meldung unter **Letzter Fehler** an, und im Log erscheint eine Warnung; der neue Versuch erfolgt beim nächsten Lesevorgang, **ohne Salve**. Nach **3 aufeinanderfolgenden Fehlern** wird die Steuerung **bis zum nächsten Zeitraum ausgesetzt** (**„Laden zur Niedertarifzeit bis zum nächsten Zeitraum ausgesetzt: Wiederholte Befehlsfehler“**); ein **Abstecken** mit anschließendem erneutem Anschließen setzt sie wieder in Gang. Ein **nicht erreichbarer** oder **ausgelasteter** Proxy ist kein Fehler: Es wird nichts gesendet, das Plugin versucht es beim nächsten Lesevorgang erneut (höchstens eine Warnung pro Stunde meldet einen verschobenen Befehl).

**Ungültige Einstellungen.** Eine Uhrzeit, die nicht im Format `HH:MM` vorliegt, ein Ziel-SoC außerhalb von **1 bis 100**, ein leerer Zeitraum (Ende gleich Beginn) oder eine aktivierte Funktion ohne Beginn, Ende oder Ziel-SoC wird **beim Speichern** des Geräts mit einer Meldung **„Laden zur Niedertarifzeit: …“** abgelehnt; nichts wird gespeichert.

**Andere Funktionen.** Die Überschusssteuerung wird **während des Zeitraums ignoriert** (siehe [Überschusssteuerung](#uberschusssteuerung)). Ein Ladeplan des Fahrzeugs ([Ladeplan erstellen](#ladeplan-erstellen)) oder der Tesla-App kann mit dem Zeitraum **in Konflikt geraten**: Behalten Sie nur einen bei, da der Zeitraum von Jeedom nicht mit ihnen abgestimmt ist. **Nur ein Zeitraum** pro Fahrzeug.

### Temperatursollwert einstellen

Die Aktionen **Sollwert Fahrer** (`set_driver_temp`) und **Sollwert Beifahrer** (`set_passenger_temp`) stellen in °C die gewünschte Temperatur auf der Fahrer- und der Beifahrerseite ein. Es sind Schieberegler, verknüpft mit den Informationen **Temperatur Fahrer** und **Temperatur Beifahrer**.

**Proxy des Forks erforderlich, Befehle ausgeblendet.** Der offizielle Proxy 2.3.0 kann den Temperatursollwert nicht einstellen: Der entsprechende Befehl wurde vom Fork hinzugefügt (mindestens Version `2.3.0-tb.1`). Solange der Proxy diesen Befehl nicht meldet, werden die beiden Aktionen **sofort abgelehnt**, ganz ohne Austausch mit dem Fahrzeug, mit der Meldung **„Von Ihrer Proxy-Version nicht unterstützt“**; der Rest des Geräts funktioniert normal. Sie werden **ausgeblendet** erstellt: Nach dem Wechsel zum Proxy des Forks aktivieren Sie **Anzeigen** bei jeder von ihnen im Reiter **Befehle** des Geräts, oder Sie rufen sie aus einem Szenario auf. Die Verfügbarkeit folgt der Meldung des Proxys (Route `capabilities`), die erneut gelesen wird, wenn sich seine Version ändert: Nach dem Wechsel zum Fork sind die Befehle verwendbar, ohne das Plugin neu zu installieren.

**Bereich und Schritt.** Der Schieberegler reicht von **15 bis 28 °C** in Schritten von **0,5 °C**. Sobald die Fahrzeugdaten gelesen sind, folgen seine Grenzen der minimalen und maximalen einstellbaren Temperatur des Fahrzeugs, **nach innen gerundet** auf ganze Grad (15,5 wird zu 16; 27,5 wird zu 27) und auf 15 bis 28 °C begrenzt, den vom Proxy akzeptierten Bereich. Ein **Min** oder **Max**, das Sie von Hand am Befehl einstellen, wird nie überschrieben. Ein Wert außerhalb des Bereichs oder ein Wert, der keine Zahl ist, wird **vor** dem Senden mit der Meldung **„Ungültiger Wert: Der Sollwert muss eine Zahl zwischen … und … °C sein“** abgelehnt; es wird nichts an das Fahrzeug gesendet. Ein Wert zwischen zwei halben Graden wird **auf das nächste halbe Grad gerundet** (21,3 wird zu 21,5), da das Fahrzeug in halben Graden einstellt.

**Die andere Seite wird mit ihrem zuletzt gelesenen Wert erneut gesendet.** Das Fahrzeug erhält beide Temperaturen immer im selben Befehl. Das Einstellen der Fahrerseite sendet also auch den Beifahrersollwert erneut, mit dem zuletzt veröffentlichten Wert der Information **Temperatur Beifahrer**, und umgekehrt. Ist dieser Wert unbekannt (nie gelesen, null oder außerhalb von 15 bis 28 °C), erhält das Fahrzeug **denselben Wert auf beiden Seiten**. Wenn Sie die andere Seite seit dem letzten Lesen von Jeedom am Bildschirm des Fahrzeugs eingestellt haben, **kann dieser Sollwert überschrieben werden**: Starten Sie **Aktualisieren (mit Aufwecken)**, bevor Sie eine Seite einstellen, um vom aktuellen Wert auszugehen.

**Nach dem Befehl.** Die verknüpfte Information wird sofort aktualisiert, dann wird der Zustand erneut gelesen und ein erneutes Lesen wie nach jedem Befehl eingeplant (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)): Der tatsächlich angewendete Sollwert erscheint beim erneuten Lesen. Das Fahrzeug wird bei Bedarf vom Proxy aufgeweckt.

**Schlüsselrolle.** Die Rolle **Owner** wird als erforderlich angenommen (im realen Betrieb zu bestätigen). Bei einem Charging-Manager-Schlüssel wird die Ablehnung durch das Fahrzeug mit der Meldung zur unzureichenden Rolle angezeigt (siehe [Schlüsselrolle](#rolle-des-schlussels)).

### Sitze und Lenkrad heizen

Sechs Aktionen stellen die Heizung ein: **Sitzheizung vorne links einstellen** (`set_seat_heater_left`), **vorne rechts** (`set_seat_heater_right`), **hinten links** (`set_seat_heater_rear_left`), **hinten rechts** (`set_seat_heater_rear_right`), **hinten Mitte** (`set_seat_heater_rear_center`) und **Lenkradheizung einstellen** (`set_steering_wheel_heater`). Es sind Auswahllisten.

**Proxy des Forks erforderlich (mindestens Version `2.3.0-tb.2`), Befehle ausgeblendet.** Der offizielle Proxy 2.3.0 kann weder die Sitz- noch die Lenkradheizung einstellen: Diese Befehle wurden vom Fork hinzugefügt. Solange der Proxy den Befehl nicht meldet, werden die sechs Aktionen **sofort abgelehnt**, ganz ohne Austausch mit dem Fahrzeug, mit der Meldung **„Von Ihrer Proxy-Version nicht unterstützt“**; der Rest des Geräts funktioniert normal. Sie werden **ausgeblendet** erstellt, auch nach dem Wechsel zum Fork: **Sie müssen sie anzeigen** (aktivieren Sie **Anzeigen** bei jeder von ihnen im Reiter **Befehle** des Geräts) oder aus einem Szenario aufrufen. Die Verfügbarkeit folgt der Meldung des Proxys (Route `capabilities`), die erneut gelesen wird, wenn sich seine Version ändert: Nach dem Wechsel zum Fork sind die Befehle verwendbar, ohne das Plugin neu zu installieren.

**Stufen.** Für einen Sitz: **Aus** (0), **Niedrig** (1), **Mittel** (2), **Hoch** (3). Ein von einem Szenario gesendeter Wert außerhalb von 0 bis 3 oder ein Wert, der keine ganze Zahl ist, wird **vor** dem Senden mit der Meldung **„Ungültiger Wert: Die Heizstufe muss eine ganze Zahl zwischen 0 und 3 sein“** abgelehnt. Für das Lenkrad: nur **Aus** (0) oder **Ein** (1), es gibt keine Stufen; das Plugin schreibt die Information **Lenkradheizungsstufe** nach dem Befehl nicht, nur das erneute Lesen aktualisiert sie. Ein Wert außer 0 oder 1 wird mit der Meldung **„Ungültiger Wert: Die Lenkradheizung muss 0 (Aus) oder 1 (Ein) sein“** abgelehnt.

**Welcher Sitz?** Die Sitze werden über ihre **Position** bezeichnet: „vorne links“ und „vorne rechts“ hängen nicht von der Lenkradseite ab. Die bestehenden Informationen behalten ihren Namen: Bei Linkslenkung entspricht **Sitzheizung Fahrer** dem Sitz **vorne links** und **Sitzheizung Beifahrer** dem Sitz **vorne rechts** (umgekehrt bei Rechtslenkung). Die Rückenlehnen und die dritte Reihe werden nicht angeboten. Ein Sitz, den das Fahrzeug nicht hat, kann vom Fahrzeug abgelehnt oder ohne Wirkung akzeptiert und mit 0 neu gelesen werden (im realen Betrieb zu prüfen).

**Klimaanlage.** Laut der Dokumentation von Tesla erfordert die Sitzheizung, dass die Klimaanlage läuft (Vorklimatisierung oder Klimahaltemodus); ohne sie kann der Befehl vom Fahrzeug abgelehnt oder ignoriert werden. Ebenso kann bei einem Fahrzeug mit automatischer Lenkradheizung der Lenkradbefehl wirkungslos bleiben. Diese Verhaltensweisen sind im realen Betrieb zu validieren.

**Nach dem Befehl.** Die verknüpfte Information (zum Beispiel **Sitzheizung Beifahrer**) wird sofort mit der angeforderten Stufe aktualisiert, dann wird der Zustand erneut gelesen und ein erneutes Lesen wie nach jedem Befehl eingeplant (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)): Die tatsächlich angewendete Stufe erscheint beim erneuten Lesen. Steht **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden**, werden diese Informationen nicht erneut gelesen: Sie behalten den gemeldeten Wert. Das Fahrzeug wird bei Bedarf vom Proxy aufgeweckt.

**Schlüsselrolle.** Die Rolle **Owner** wird als erforderlich angenommen (im realen Betrieb zu bestätigen). Bei einem Charging-Manager-Schlüssel wird die Ablehnung durch das Fahrzeug mit der Meldung zur unzureichenden Rolle angezeigt (siehe [Schlüsselrolle](#rolle-des-schlussels)).

### Maximale Enteisung

Eine Aktion **Maximale Enteisung** (`set_preconditioning_max`) aktiviert oder beendet die maximale Enteisung des Fahrzeugs (Entfeuchten und Enteisen der Scheiben und Spiegel). Es ist eine Auswahlliste: **Aus** (0) oder **Ein** (1). Sie ist mit der Information **Enteisungsmodus** (`defrost_mode`, Werte `Off`, `Normal` oder `Max`) verknüpft, und die Informationen zur vorderen und hinteren Enteisung (`is_front_defroster_on`, `is_rear_defroster_on`) werden zusammen mit ihr erneut gelesen.

**Proxy des Forks erforderlich (mindestens Version `2.3.0-tb.1`), Befehl ausgeblendet.** Der offizielle Proxy 2.3.0 kann die maximale Enteisung nicht steuern: Der Befehl wurde vom Fork hinzugefügt. Solange der Proxy den Befehl nicht meldet, wird die Aktion **sofort abgelehnt**, ganz ohne Austausch mit dem Fahrzeug, mit der Meldung **„Von Ihrer Proxy-Version nicht unterstützt“**; der Rest des Geräts funktioniert normal. Sie wird **ausgeblendet** erstellt, auch nach dem Wechsel zum Fork: **Sie müssen sie anzeigen** (aktivieren Sie **Anzeigen** im Reiter **Befehle** des Geräts) oder aus einem Szenario aufrufen. Die Verfügbarkeit folgt der Meldung des Proxys (Route `capabilities`), die erneut gelesen wird, wenn sich seine Version ändert: Nach dem Update des Proxys ist der Befehl verwendbar, ohne das Plugin neu zu installieren.

> ⚠️ **Verbrauch und Aufwecken.** Das Aktivieren der maximalen Enteisung **weckt das Fahrzeug auf** (über den Proxy) und **verbraucht Batterie**, solange sie läuft. Das Plugin startet sie **nie** von sich aus: Nur eine Aktion von Ihnen (Widget oder Szenario) sendet sie. Denken Sie daran, sie zu beenden, zum Beispiel mit einem zweiten Szenario nach der gewünschten Dauer.

**Werte.** Ein von einem Szenario gesendeter Wert außer 0 oder 1 wird **vor** dem Senden mit der Meldung **„Ungültiger Wert: Die maximale Enteisung muss 0 (Aus) oder 1 (Ein) sein“** abgelehnt.

**Nach dem Befehl.** **Enteisungsmodus** wechselt sofort auf `Max` (Ein) oder `Off` (Aus), dann wird der Zustand erneut gelesen und ein erneutes Lesen wie nach jedem Befehl eingeplant (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)): Der tatsächliche Wert erscheint beim erneuten Lesen (beim Beenden kann das Fahrzeug `Normal` anzeigen, wenn die Klimaanlage noch läuft). Die vordere und hintere Enteisung werden erst bei diesem erneuten Lesen aktualisiert. Steht **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden** oder schläft das Fahrzeug wieder ein, werden diese Informationen nicht erneut gelesen: Sie behalten den gemeldeten Wert.

**Schlüsselrolle.** Die Rolle **Owner** wird als erforderlich angenommen (im realen Betrieb zu bestätigen). Bei einem Charging-Manager-Schlüssel wird die Ablehnung durch das Fahrzeug mit der Meldung zur unzureichenden Rolle und dem Badge **Unzureichende Rolle** angezeigt (siehe [Schlüsselrolle](#rolle-des-schlussels)).

### Hundemodus, Campmodus und Klimahaltemodus

Eine Aktion **Klimahaltemodus** (`set_climate_keeper_mode`) wählt das Halten der Klimatisierung des geparkten Fahrzeugs: **Aus** (0), **Halten** (1), **Hundemodus** (2) oder **Campmodus** (3). Sie ist mit der Information **Klimahaltemodus (Hund, Camp)** (`climate_keeper_mode`, Werte `Off`, `On`, `Dog`, `Party` oder `Unknown`) verknüpft: Der Campmodus erscheint dort unter dem Namen `Party`, wie vom Fahrzeug gemeldet (im realen Betrieb zu bestätigen).

**Proxy des Forks erforderlich (mindestens Version `2.3.0-tb.1`), Befehl ausgeblendet.** Der offizielle Proxy 2.3.0 kann das Halten der Klimatisierung nicht steuern: Der Befehl wurde vom Fork hinzugefügt. Solange der Proxy den Befehl nicht meldet, wird die Aktion **sofort abgelehnt**, ganz ohne Austausch mit dem Fahrzeug, mit der Meldung **„Von Ihrer Proxy-Version nicht unterstützt“**; der Rest des Geräts funktioniert normal. Sie wird **ausgeblendet** erstellt, auch nach dem Wechsel zum Fork: **Sie müssen sie anzeigen** (aktivieren Sie **Anzeigen** im Reiter **Befehle** des Geräts) oder aus einem Szenario aufrufen. Die Verfügbarkeit folgt der Meldung des Proxys (Route `capabilities`), die erneut gelesen wird, wenn sich seine Version ändert: Nach dem Update des Proxys ist der Befehl verwendbar, ohne das Plugin neu zu installieren.

> ⚠️ **Batterie und Aufwecken.** Die Wahl eines Haltemodus **weckt das Fahrzeug auf** (über den Proxy) und **verbraucht über lange Zeit Batterie**; das Fahrzeug kann ablehnen (schwache Batterie, Fahrzeugzustand). Das Plugin startet ihn **nie** von sich aus und beendet ihn nie: Nur eine Aktion von Ihnen (Widget oder Szenario) sendet ihn.

> ⚠️ **Tier.** Dieser Modus **ersetzt keine Überwachung der Temperatur** im Innenraum bei einem Tier. Das Lesen folgt dem Aktualisierungsintervall des Fahrzeugs: Ein Alarm muss sich auf die **Innentemperatur** und ein passendes Intervall stützen.

**Werte.** Ein von einem Szenario gesendeter Wert außerhalb von 0 bis 3 wird **vor** dem Senden mit der Meldung **„Ungültiger Wert: Der Klimahaltemodus muss 0 (Aus), 1 (Halten), 2 (Hund) oder 3 (Camp) sein“** abgelehnt.

**Nach dem Befehl.** **Klimahaltemodus (Hund, Camp)** wechselt sofort auf `Off`, `On`, `Dog` oder `Party`, dann wird der Zustand erneut gelesen und ein erneutes Lesen wie nach jedem Befehl eingeplant (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)): Der tatsächliche Wert erscheint beim erneuten Lesen. Steht **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden** (lassen Sie es für diesen Modus auf **Ja**) oder schläft das Fahrzeug wieder ein, wird die Information nicht erneut gelesen: Sie behält den gemeldeten Wert, und das Einschlaffenster kann sich öffnen (siehe [Das Fahrzeug einschlafen lassen](#fahrzeug-einschlafen-lassen)).

**Schlüsselrolle.** Die Rolle **Owner** wird als erforderlich angenommen (im realen Betrieb zu bestätigen). Bei einem Charging-Manager-Schlüssel wird die Ablehnung durch das Fahrzeug mit der Meldung zur unzureichenden Rolle und dem Badge **Unzureichende Rolle** angezeigt (siehe [Schlüsselrolle](#rolle-des-schlussels)).

### Von Jeedom geplante Vorklimatisierung

Das Plugin kann **die Klimaanlage vor der Abfahrtszeit starten** und anschließend beenden, mit der bereits im Fahrzeug eingestellten Temperatur. Das funktioniert mit dem offiziellen Proxy 2.3.0 (Befehle **Klimaanlage starten** und **Klimaanlage stoppen**), ohne Fork. Die Einstellungen befinden sich im Abschnitt **Von Jeedom geplante Vorklimatisierung** des Geräts; verwechseln Sie ihn nicht mit der Information **Geplante Vorklimatisierung** (`scheduled_preconditioning_time`), die die im Fahrzeug vorgenommene Planung **liest**.

**Schritt für Schritt: Geplante Vorklimatisierung konfigurieren.**

1. Öffnen Sie **Plugins > Verbundene Objekte > Tesla BLE** und dann das Gerät des Fahrzeugs (Reiter **Gerät**), Abschnitt **Von Jeedom geplante Vorklimatisierung**.
2. Tragen Sie die **Abfahrtszeit** in der Zeit von Jeedom ein, zum Beispiel `07:30`.
3. Aktivieren Sie die betroffenen Abfahrts-**Tage**.
4. Stellen Sie den **Vorlauf (min)** (leer: 15 Minuten) und die **Maximale Dauer (min)** (leer: 30 Minuten, oder der Vorlauf plus 15 Minuten, wenn der Vorlauf 15 übersteigt) ein. Mit 15 und 30 startet die Klimaanlage um `07:15` und endet um `07:45`.
5. Aktivieren Sie **Nur wenn angeschlossen**, wenn die Klimaanlage nicht die Batterie eines abgesteckten Fahrzeugs belasten soll.
6. Aktivieren Sie **Aktivieren** (**Klimasteuerung**) und **speichern** Sie dann. Eine ungültige Einstellung wird mit einer Meldung **„Geplante Vorklimatisierung: …“** abgelehnt (siehe [Fehlerbehebung](#fehlerbehebung)): Nichts wird gespeichert.
7. Prüfen Sie: Stellen Sie das Log des Plugins auf **Info**. Beim ersten Lesen des Fahrzeugs im Zeitfenster zeigt eine Zeile **„préconditionnement planifié : décision …“** *(Geplante Vorklimatisierung: Entscheidung …)*, was das Plugin entschieden hat und warum.

**Anwendungsbeispiel: Abfahrt werktags um 7:30 Uhr.** Stellen Sie **Abfahrtszeit** auf `07:30`, aktivieren Sie **Montag** bis **Freitag**, lassen Sie **Vorlauf** bei 15 und **Maximale Dauer** bei 30, aktivieren Sie **Nur wenn angeschlossen** und **Aktivieren**. Das Fahrzeug bleibt nachts angeschlossen:

- Wenn Sie auch das [Laden zur Niedertarifzeit](#laden-zur-niedertarifzeit) verwenden (zum Beispiel `22:00` bis `06:00`), endet das Laden vor dem Zeitfenster der Vorklimatisierung, das von `07:15` bis `07:45` reicht: Die beiden Funktionen stören sich nicht.
- Von Montag bis Freitag wird beim ersten Lesen des Fahrzeugs nach `07:15` die Klimaanlage gestartet, wenn sie gestoppt ist und das Fahrzeug angeschlossen ist. Das Log des Plugins (Stufe **Info**) zeigt **„préconditionnement planifié : décision `auto_conditioning_start` (demarrage)“** *(Geplante Vorklimatisierung: Entscheidung `auto_conditioning_start` (Start))*, und die Information **Klimaanlage aktiviert** wechselt beim nächsten Lesen auf 1.
- Beim ersten Lesen nach `07:45` wird die Klimaanlage, falls sie nach diesem Start durch Jeedom noch läuft, gestoppt (Entscheidung `auto_conditioning_stop`).
- Samstags und sonntags passiert nichts. Wenn Sie vor `07:45` losfahren, stoppen Sie die Klimaanlage selbst von Jeedom aus: Jeedom startet sie danach nicht erneut.

**Das Zeitfenster.** Es beginnt zur Abfahrtszeit **minus dem Vorlauf** und dauert die **maximale Dauer** ab diesem Beginn (Beginn eingeschlossen, Ende ausgeschlossen). Maßgeblich ist der Tag der **Abfahrtszeit**: Eine Abfahrt um `00:10` mit 20 Minuten Vorlauf startet am Vortag um `23:50`, und es ist der Tag des folgenden Tages, der aktiviert werden muss. Alles gilt in der **Zeit von Jeedom** (seiner Zeitzone), nicht in der des Fahrzeugs; eine Abfahrt, die in die bei der Umstellung auf die Sommerzeit übersprungene Stunde fällt, wird um eine Stunde verschoben.

**Was das Plugin tut.** Bei jedem erfolgreichen Lesen des Fahrzeugs durch den Aktualisierungszyklus, **im Zeitfenster**: Wenn die Klimaanlage gestoppt ist (und mit der Option das Fahrzeug angeschlossen), **Klimaanlage starten** (**ein einziger erfolgreicher Start pro Abfahrt**); **beim ersten Lesen nach dem Ende des Zeitfensters** (innerhalb der Stunde), wenn die Klimaanlage nach einem Start durch Jeedom noch läuft, **Klimaanlage stoppen**. Höchstens **ein Befehl pro Lesevorgang**, kein unnötiger Befehl.

**Genauigkeit.** Die Entscheidung folgt dem **Lesetakt** des Fahrzeugs: Der Start kann einige Minuten nach der vorgesehenen Zeit erfolgen, und der Stopp das Ende um ein Intervall überschreiten. Ein Aktualisierungsintervall von **höchstens 5 Minuten** wird empfohlen. Ist das Intervall länger als die Dauer des Zeitfensters, fällt kein Lesevorgang hinein: weder Start noch Stopp. Ein Start ist noch **nach der Abfahrtszeit** möglich, solange das Zeitfenster nicht beendet ist.

**Ruhezustand des Fahrzeugs.** Das Plugin **weckt das Fahrzeug nie von sich aus auf**, um zu entscheiden, und sendet nie einen Aufweckbefehl, aber **Klimaanlage starten weckt das Fahrzeug auf** (der Proxy tut dies selbst) und verbraucht Batterie. Ein als **schlafend** erkanntes Fahrzeug erhält **nie** einen Stoppbefehl: Seine Klimaanlage gilt als gestoppt.

**Vorrang für Ihre Aktionen.** Jeedom widerspricht Ihrer Aktion nie:

- Ein **Klimaanlage starten** oder **Klimaanlage stoppen**, das **von Jeedom aus** (Widget, Szenario) während des Zeitfensters ausgelöst wird, **setzt die Vorklimatisierung bis zur nächsten Abfahrt aus**, und die Klimaanlage wird am Ende des Zeitfensters nicht gestoppt;
- eine Klimaanlage, die bei Eintritt in das Zeitfenster **bereits läuft** (oder aus der Tesla-App oder durch die Planung des Fahrzeugs gestartet wurde), wird weder neu gestartet noch gestoppt;
- eine Klimaanlage, die nach dem Start durch Jeedom **aus der App gestoppt** wurde (festgestellt durch einen Lesevorgang mindestens **2 Minuten** nach dem Befehl), wird nicht in einer Schleife neu gestartet;
- ein laufender **Hundemodus, Campmodus, Haltemodus** oder eine **maximale Enteisung** wird nie gestoppt oder ersetzt.

Das Deaktivieren der Funktion oder das Ändern ihrer Einstellungen **während des Zeitfensters stoppt** eine bereits gestartete Klimaanlage **nicht**.

**Schlüsselrolle.** Die Rolle **Owner** wird als erforderlich angenommen (im realen Betrieb zu bestätigen). Bei einem Charging-Manager-Schlüssel lehnt das Fahrzeug den Befehl ab: Die Meldung zur unzureichenden Rolle erscheint unter **Letzter Fehler**, die Information **Schlüsselrolle** wechselt auf **Charging Manager**, und **pro Abfahrt wird nur ein Versuch unternommen** (siehe [Schlüsselrolle](#rolle-des-schlussels)).

**Befehlsfehler.** Ein fehlgeschlagener Befehl (Ablehnung durch das Fahrzeug, Zeitüberschreitung) zeigt seine Meldung unter **Letzter Fehler** an, und im Log erscheint eine Warnung; der neue Versuch erfolgt beim nächsten Lesevorgang, **ohne Salve**. Nach **3 aufeinanderfolgenden Fehlern** wird die Steuerung **bis zur nächsten Abfahrt ausgesetzt**. Ein **nicht erreichbarer** oder **ausgelasteter** Proxy ist kein Fehler: Es wird nichts gesendet, das Plugin versucht es beim nächsten Lesevorgang erneut.

**Keine Aktion in diesen Fällen.** Die Funktion ist deaktiviert oder der Tag ist nicht aktiviert; das Fahrzeug konnte nicht gelesen werden oder ist **außer Reichweite**; mit der Option ist das Fahrzeug **abgesteckt** oder sein Ladezustand ist unbekannt; der Zustand der Klimaanlage ist unbekannt; die Klimaanlage läuft bereits. Der Grund ist für die relevanten Fälle unter **Letzter Fehler** sichtbar (**„Fahrzeug nicht angeschlossen: Geplante Vorklimatisierung nicht gestartet“**, **„Ladezustand unbekannt: Starten Sie Aktualisieren (mit Aufwecken)“**), ohne je einen echten Fehler des letzten Lesezyklus zu ersetzen.

**Andere Funktionen.** Die geplante Vorklimatisierung ist **unabhängig** von der im Fahrzeug vorgenommenen Planung ([Geplante Vorklimatisierung](#informationen), vom Plugin gelesen): Wenn das Fahrzeug bereits vorklimatisiert, gilt die Klimaanlage als aktiv, und Jeedom greift nicht ein. Sie kann im selben Durchlauf mit dem [Laden zur Niedertarifzeit](#laden-zur-niedertarifzeit) aufeinanderfolgen: Die beiden Befehle werden nacheinander gesendet. Das Plugin berücksichtigt die Anwesenheit eines Insassen nicht: Eine von Jeedom gestartete Klimaanlage, die beim ersten Lesen nach dem Ende des Zeitfensters noch läuft, wird gestoppt.

### Bestätigung sensibler Aktionen

Fünf Aktionen verlangen vor dem Senden eine **Bestätigung**, auf dem Dashboard und auf Mobilgeräten: **Türen entriegeln** (`door_unlock`), **Ladeklappe öffnen** (`charge_port_door_open`), **Wächter-Modus einstellen** (`set_sentry_mode`), **Kofferraum hinten öffnen** (`open_trunk_rear`) und **Frunk öffnen** (`open_trunk_front`). Die übrigen Aktionen (verriegeln, hupen, Lichter, Laden, Klima …) werden schon beim ersten Klick gesendet.

- **Ein Klick öffnet ein Bestätigungsfenster.** Es wird nichts gesendet, solange Sie nicht bestätigt haben.
- **Kontrollkästchen „Aktion bestätigen“.** Es befindet sich in den erweiterten Parametern des Befehls (Reiter **Befehle** des Geräts, Zahnrad des Befehls). Es ist **bei der Erstellung angehakt**; entfernen Sie den Haken, um die Bestätigung eines Befehls aufzuheben, und setzen Sie ihn bei einem anderen, um eine hinzuzufügen. Ihre Wahl wird vom Plugin nie überschrieben (auch nicht bei einem Update: Bei einem bestehenden Gerät setzt das Update die Bestätigung nur einmal, außer dort, wo Sie sie bereits eingestellt hatten).
- **Ein Szenario ist nicht betroffen.** Eine aus einem Szenario aufgerufene Aktion wird **ohne Bestätigung** ausgeführt. Ein Aufruf über die JSON-RPC-API von Jeedom muss `confirmAction=1` übergeben, sonst lehnt Jeedom ihn ab.

> **WICHTIG: Das ist kein Sicherheitsschutz.** Die Bestätigung ist eine Schutzvorkehrung der Oberfläche gegen versehentliches Klicken, mehr nicht. Der Proxy hat standardmäßig **keine Authentifizierung**: Jeder Rechner in Ihrem Netzwerk, der ihn erreichen kann, kann das Fahrzeug entriegeln oder öffnen, **ohne Jeedom zu durchlaufen**, also ohne Bestätigung. Betreiben Sie den Proxy in einem vertrauenswürdigen Netzwerk und setzen Sie ihn nie dem Internet aus (siehe [Rolle des Schlüssels](#rolle-des-schlussels)).

Für **Wächter-Modus einstellen** wird der nach dem Befehl angezeigte Zustand unter [Zustand des Wächter-Modus](#zustand-des-wachter-modus) beschrieben (Herkunft **Tatsächlich** oder **Letzter Befehl**).

### Kofferraum hinten und Frunk öffnen

Zwei Aktionen öffnen einen Kofferraum aus der Ferne: **Kofferraum hinten öffnen** (`open_trunk_rear`) und **Frunk öffnen** (`open_trunk_front`, der vordere Kofferraum). Sie senden denselben Proxy-Befehl, `actuate_trunk`, mit dem jeweils gemeinten Kofferraum. Der Zustand wird in den Informationen **Kofferraum hinten** (`trunk_rear`) und **Frunk (vorderer Kofferraum)** (`trunk_front`) gelesen.

**Proxy des Forks erforderlich (mindestens Version `2.3.0-tb.2`), Befehle ausgeblendet.** Der offizielle Proxy 2.3.0 kennt diesen Befehl nicht: Er wurde vom Fork hinzugefügt. Solange der Proxy den Befehl nicht meldet, werden beide Aktionen **sofort abgelehnt**, ohne jeden Austausch mit dem Fahrzeug, mit der Meldung **„Von Ihrer Proxy-Version nicht unterstützt“**. Sie werden **ausgeblendet** erstellt, auch nach dem Wechsel zum Fork: **Sie müssen sie selbst einblenden** (haken Sie **Anzeigen** im Reiter **Befehle** des Geräts an) oder sie aus einem Szenario aufrufen. Die Verfügbarkeit folgt der Meldung des Proxys (Route `capabilities`), die neu gelesen wird, wenn sich seine Version ändert: Nach dem Update des Proxys sind die Aktionen nutzbar, ohne das Plugin neu zu installieren oder das Gerät neu zu erstellen. Für diese beiden Aktionen zeigt das Plugin weder das Badge **Funktion nicht verfügbar** noch das Badge **Unzureichende Rolle** an: Die Ablehnung wird beim Klick angezeigt.

**Bestätigung.** Ein Klick verlangt vor dem Senden eine **Bestätigung**, wie bei den anderen sensiblen Aktionen: siehe [Bestätigung sensibler Aktionen](#bestatigung-sensibler-aktionen) (Kontrollkästchen **Aktion bestätigen**, Szenario ohne Bestätigung, JSON-RPC `confirmAction=1`).

**Prüfung vor dem Öffnen des hinteren Kofferraums.** Beim hinteren Kofferraum behandelt das Fahrzeug den Befehl als **Umschalter**: Bei einer bereits geöffneten motorisierten Heckklappe würde er sie **schließen**. Das Plugin liest daher zuerst den Fahrzeugzustand neu (ohne es aufzuwecken) und sendet den Befehl nur, wenn der hintere Kofferraum als **geschlossen** gelesen wird. Drei mögliche Ablehnungen, kein Senden, und **Letzter Fehler** wird nicht verändert:

- **„Kofferraum bereits offen oder in Bewegung: Befehl nicht gesendet“**: Der hintere Kofferraum ist offen, angelehnt, öffnet sich gerade oder schließt sich gerade;
- **„Kofferraumzustand unbekannt: Befehl nicht gesendet“**: Das Fahrzeug liefert für diesen Kofferraum keinen verwertbaren Zustand;
- **„Kofferraumzustand nicht lesbar, Befehl nicht gesendet: …“**: Das erneute Lesen ist fehlgeschlagen (Proxy nicht erreichbar, Fahrzeug außer Reichweite …), die Ursache folgt auf die Meldung.

Der erneut gelesene Zustand wird vor der Ablehnung in den Informationen veröffentlicht: Wenn der Kofferraum bereits offen war, springt **Kofferraum hinten** auf 1. Der **Frunk** wird nicht neu gelesen: Er schließt sich nicht aus der Ferne, der Befehl kann ihn nur öffnen. **Das Plugin schließt nie einen Kofferraum.**

> ⚠️ **Aufwecken.** Diese Befehle **wecken das Fahrzeug auf** (über den Proxy), und das Plugin startet sie nie von selbst: Nur eine Handlung von Ihnen (Widget oder Szenario) sendet sie.

**Nach dem Befehl.** Es wird kein Wert angenommen: Der Zustand wird neu gelesen, danach wird wie nach jedem Befehl ein erneutes Lesen eingeplant (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)). **Kofferraum hinten** oder **Frunk (vorderer Kofferraum)** springt auf 1, sobald das Fahrzeug den Kofferraum als offen meldet, manchmal erst beim nächsten Lesen.

**Rolle des Schlüssels.** Die Rolle **Owner** gilt als erforderlich (im realen Einsatz zu bestätigen). Mit einem Charging-Manager-Schlüssel wird die Ablehnung des Fahrzeugs mit der Meldung zur unzureichenden Rolle angezeigt (siehe [Rolle des Schlüssels](#rolle-des-schlussels)).

### Zustand des Wächter-Modus

Zwei Informationen geben an, ob der Wächter-Modus aktiv ist: **Wächter-Modus** (`sentry_mode`) hat den Wert **Aktiv**, **Inaktiv** oder **Unbekannt**, und **Herkunft des Wächter-Modus** (`sentry_mode_source`) gibt an, woher dieser Wert stammt. Der Befehl, der ihn aktiviert oder deaktiviert, ist **Wächter-Modus einstellen** (`set_sentry_mode`).

| Herkunft | Bedeutung |
|---|---|
| **Tatsächlich** | Der Wert wurde **am Fahrzeug gelesen**. Verfügbar mit dem **Proxy des Forks ab Version `2.3.0-tb.2`** und einem **wachen** Fahrzeug: Ein schlafendes Fahrzeug wird nicht gelesen, die Information behält dann den **zuletzt gelesenen Wert** (siehe [Fahrzeugschlaf und Aktualität der Daten](#ruhezustand-des-fahrzeugs-und-aktualitat-der-daten)). Eine Änderung über die Tesla-App oder den Bildschirm des Fahrzeugs wird beim nächsten Lesen erkannt. |
| **Letzter Befehl** | Das Plugin kann den Wächter-Modus nicht lesen (offizieller Proxy 2.3.0 oder älterer Fork): Der Wert ist der des **letzten erfolgreichen, von Jeedom gesendeten Befehls**. Eine Änderung über die App, den Bildschirm des Fahrzeugs oder eine **automatische Abschaltung** wird **nicht erkannt**. |
| **Keine** | Es wurde noch nichts gelesen oder angeordnet: **Wächter-Modus** hat den Wert **Unbekannt** (nie ein falsches „Inaktiv“). |

**Nach einem Befehl.** Ein **erfolgreicher** Befehl veröffentlicht sofort den angeordneten Wert mit der Herkunft **Letzter Befehl**, auch wenn der Proxy den Wächter-Modus lesen kann; beim nächsten erneuten Lesen wechselt die Herkunft wieder auf **Tatsächlich**. Während der Dauer des **erneuten Lesens nach einem Befehl** (standardmäßig 30 Sekunden, siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)) wird ein tatsächlicher Lesewert, der dem Befehl widerspricht, ignoriert: Der Proxy liefert noch den alten Zustand. Ein **abgelehnter** oder fehlgeschlagener Befehl ändert nichts.

**Zustände des Fahrzeugs.** Nur `Off` ergibt **Inaktiv**. Die anderen Zustände (`Idle`, `Armed`, `Aware`, `Panic`, `Quiet`) ergeben **Aktiv**: `Idle`, der Wächter-Modus im Ruhezustand, wird als **Aktiv** gezählt (im realen Einsatz zu bestätigen). Ein unbekannter oder fehlender Wert lässt die Information unverändert.

**Neustart von Jeedom.** Der zuletzt bekannte Wert und seine Herkunft werden **beibehalten** und beim Start wieder übernommen, auch nach einem Stromausfall.

> **In einem Szenario.** Die Bezeichnungen **Aktiv**, **Inaktiv**, **Unbekannt**, **Tatsächlich**, **Letzter Befehl** und **Keine** **folgen der Sprache von Jeedom**: Vergleichen Sie sie in der aktuellen Sprache Ihres Jeedom. Um zu wissen, ob der Wert zuverlässig ist, testen Sie zusätzlich zu **Wächter-Modus** auch **Herkunft des Wächter-Modus** (zum Beispiel **Tatsächlich**).

### Warnungen bei längerer Öffnung

Das Plugin kann Sie **warnen**, wenn eine Öffnung (Tür, hinterer Kofferraum, Frunk, Tonneau-Abdeckung, Ladeklappe) länger offen bleibt oder wenn das Fahrzeug länger **entriegelt ohne Insassen** bleibt, als Sie es festlegen. Die Warnungen sind **standardmäßig deaktiviert** und werden **pro Fahrzeug** im Block **Warnungen bei längerer Öffnung** der Geräteseite eingestellt:

| Einstellung | Funktion |
|---|---|
| **Offen gebliebene Öffnung**: **Aktivieren** | Aktiviert die Warnung für Öffnungen. |
| **Dauer bis zur Warnung (min)** | Von 1 bis 1440 Minuten. **Pflichtangabe**, um die Warnung zu aktivieren; eine ungültige Dauer wird beim Speichern abgelehnt. |
| **Fahrzeug ohne Insassen entriegelt**: **Aktivieren** | Aktiviert die Verriegelungswarnung, mit **eigener Dauer** (**Dauer bis zur Warnung (min)**). |

Die beiden Warnungen sind unabhängig voneinander. Eine Warnung besteht aus:

- **einer Meldung** in der Nachrichtenzentrale von Jeedom, die das Fahrzeug und die Öffnung nennt (zum Beispiel „Meine Tesla: Öffnung ‚Frunk (vorderer Kofferraum)‘ seit mehr als 10 min geöffnet“), **nur einmal pro Vorfall**; **mehrere gleichzeitig offene Öffnungen ergeben mehrere Meldungen**, eine pro Öffnung;
- **der Info auf 1**: **Öffnungsalarm** (`closures_alert`), solange mindestens eine Öffnung länger als die Dauer offen geblieben ist, **Alarm entriegelt ohne Insassen** (`unlocked_alert`) für die Verriegelung. Verwenden Sie sie als Auslöser eines Szenarios, um über das Mittel Ihrer Wahl benachrichtigt zu werden; sie sind **ausgeblendet** und **historisiert**: Blenden Sie sie ein, wenn Sie möchten.

Sobald alles geschlossen (oder wieder verriegelt) ist oder ein Insasse anwesend ist, springt die Info auf **0** zurück, und eine neue längere Öffnung löst erneut eine Warnung aus. **Die Meldung bleibt nach dem Schließen in der Nachrichtenzentrale**: Jeedom entfernt sie nicht, löschen Sie sie selbst.

**Genauigkeit.** Die Warnungen werden **bei jedem erfolgreichen Lesen des Fahrzeugzustands** ausgewertet, also im Takt der Aktualisierung (standardmäßig 5 Minuten, siehe [Aktualisierung der Informationen](#aktualisierung-der-informationen)). Die Dauer wird ab dem **ersten Lesen gezählt, das die Auffälligkeit sieht**: Die Warnung wird **zwischen der gewählten Dauer und dieser Dauer plus zwei Aktualisierungsintervallen** nach dem tatsächlichen Öffnen ausgelöst; „seit mehr als 10 min geöffnet“ stimmt also immer.

**Nie eine Warnung auf einem veralteten Wert.** Wenn der Proxy nicht erreichbar ist, das Fahrzeug außer Reichweite ist oder das Lesen fehlschlägt, wird **nichts ausgewertet** und die Dauer summiert sich nicht auf. Dauert die Unterbrechung länger als **zwei Aktualisierungsintervalle plus zwei Minuten**, beginnt der Zeitzähler bei der Rückkehr der Lesevorgänge **bei null von vorn**; eine bereits ausgegebene Warnung bleibt ausgegeben, ohne neue Meldung.

**Ladeklappe.** Die geöffnete Klappe zählt **nur dann** als Auffälligkeit, **wenn das Fahrzeug als abgesteckt gesehen wurde** (zuletzt gelesener **Ladestatus**: `Disconnected`). Angeschlossen, beim Laden oder bei unbekanntem Zustand: keine Warnung für die Klappe.

**Unbekannte Anwesenheit.** „Entriegelt ohne Insassen“ wird nur ausgewertet, wenn das Fahrzeug **entriegelt** ist und **Insasse anwesend** den Wert **0** hat: Eine unbekannte Anwesenheit löst nichts aus (siehe [Informationen](#informationen)).

### Position und Datenschutz

Die Position des Fahrzeugs ist ein **personenbezogenes Datum**: Sie verrät, wo Sie sind und wann Sie nicht dort sind. Das Plugin schützt sie standardmäßig, einige Vorkehrungen bleiben aber Ihre Sache.

**Was gelesen wird und wann.** Die Position wird nur vom **Proxy des Forks** (mindestens `2.3.0-tb.2`) geliefert: Der offizielle Proxy 2.3.0 liefert sie nicht, und die Informationen existieren dann nicht (siehe [Erweiterte Daten: was verfügbar ist](#erweiterte-daten-was-verfugbar-ist)). Sie wird höchstens **alle 15 Minuten** gelesen, nur wenn das Fahrzeug **wach und in Bluetooth-Reichweite** des Proxys ist, nie durch Aufwecken. Da der Proxy in Ihrer Garage steht, ist die gelesene Position praktisch die des Zuhauses. Eine fehlende Position, bei 0/0, außerhalb des gültigen Bereichs oder **älter als eine Stunde** wird ignoriert: Die Informationen behalten ihren letzten Wert.

**Standardmäßig nicht sichtbar und nicht historisiert.** **Breitengrad** und **Längengrad** werden **ausgeblendet** und **nicht historisiert** erstellt: Sie erscheinen weder auf dem Widget noch in einem Diagramm, und nichts wird aufbewahrt. Um sie zu nutzen:

1. Öffnen Sie den Reiter **Befehle** des Geräts.
2. Haken Sie bei **Breitengrad** und **Längengrad** **Anzeigen** an, um sie auf dem Widget zu sehen, und **Historisieren**, um die Werte aufzubewahren.
3. **Speichern** Sie. Diese Wahl wird danach nie überschrieben.

Achtung: Eine historisierte Position wird wie jeder Verlauf in der Datenbank von Jeedom und in deren Sicherungen gespeichert. Historisieren Sie nur, wenn Sie es brauchen.

**Das Zuhause und der Radius.** Die Information **Zu Hause** hat den Wert **1**, wenn das Fahrzeug weniger als **Radius (m)** vom Zuhause entfernt ist, darüber hinaus **0**. Das Zuhause wird im Reiter **Gerät**, Abschnitt **Position des Zuhauses**, eingestellt (siehe [Konfiguration der Geräte](#konfiguration-der-gerate)):

| Einstellung | Wert |
|---|---|
| **Breitengrad** und **Längengrad** | Die Koordinaten Ihres Zuhauses. **Beide leer: die Position von Jeedom** (**Einstellungen > Systeme > Konfiguration**, Reiter **Allgemein**). Nur eine einzige auszufüllen wird abgelehnt. |
| **Radius (m)** | Ganze Zahl von **10 bis 10000**. Leer: **100 m**. Ein ungenaues GPS oder eine Tiefgarage kann einen größeren Radius erfordern. |

Beim Speichern des Geräts wird **Zu Hause** sofort anhand der zuletzt gelesenen Position neu berechnet (wenn **Breitengrad** und **Längengrad** am Gerät existieren), ohne das nächste Lesen abzuwarten.

**Grenzen von Zu Hause.** Es ist eine binäre Information, die nicht „unbekannt“ ausdrücken kann:

- Sie wird **nie geschrieben**, solange das **Zuhause** (keine Koordinaten eingetragen, keine Position in Jeedom) oder die **Position** (nie gelesen, ignoriert) unbekannt sind. **Vor jeder Berechnung zeigt die Kachel 0**: Sie beweist also nicht, dass das Fahrzeug weggefahren ist.
- Sie **springt nicht auf 0 zurück**, wenn das Fahrzeug wegfährt: Außerhalb der Bluetooth-Reichweite wird keine Position mehr gelesen, und die Information behält ihren **letzten Wert** (1). Sie behält ihren Wert auch, wenn Sie das Zuhause löschen oder die Position zu alt wird.
- **In einem Szenario** testen Sie `== 1` (nie `== 0` oder „ungleich 1“) und **kombinieren Sie mit Fahrzeug anwesend**: „Zu Hause hat den Wert 1 **und** Fahrzeug anwesend hat den Wert 1“ bedeutet, dass das Fahrzeug bei Ihnen und erreichbar ist. **Fahrzeug anwesend auf 0** zeigt an, dass es nicht mehr in Reichweite des Proxys ist, also praktisch weggefahren.

**Das Log `event` von Jeedom.** Das Plugin schreibt **nie** eine Koordinate (Fahrzeug oder Zuhause) oder eine Entfernung in sein eigenes Log, auf keiner Stufe, auch nicht bei **Debug**. Jeedom selbst protokolliert aber jeden neuen Wert einer Information in seinem Log **`event`** (**Analyse > Protokolle**): **Breitengrad** und **Längengrad** erscheinen dort, **auch ausgeblendet und nicht historisiert**. Um sich davor zu schützen, gibt es zur Wahl: die Stufe des Logs `event` in den Log-Einstellungen von Jeedom senken (**Einstellungen > Systeme > Konfiguration**, Reiter **Logs**) oder die Informationen **Breitengrad** und **Längengrad** des Geräts löschen (**Zu Hause** wird weiterhin berechnet). Das Plugin erstellt die fehlenden Befehle bei jedem Speichern des Geräts neu: Löschen Sie sie erneut, wenn sie wiederkommen. Prüfen Sie außerdem einen Log-Screenshot, bevor Sie ihn in einem Forum veröffentlichen.

**Der Proxy muss geschützt bleiben.** Der offizielle Proxy hat **keine Authentifizierung**: Jedes Gerät in Ihrem lokalen Netzwerk kann ihn nach der Position des Fahrzeugs fragen. Der Proxy des Forks, der als Einziger die Position liefert, **kann** einen **API-Token** verlangen (optional: Einstellung **API-Token des Proxys** der Plugin-Konfiguration), der auch die Position schützt. Betreiben Sie den Proxy in jedem Fall in einem vertrauenswürdigen Netzwerk und setzen Sie seinen Port **nie** dem Internet aus (siehe [Rolle des Schlüssels](#rolle-des-schlussels) und [Konfiguration des Plugins](#konfiguration-des-plugins)).

### Warum die Aufrufe nacheinander erfolgen

Ein Proxy hat nur **einen einzigen Bluetooth-Adapter** und eine einzige Warteschlange für den Austausch mit den Fahrzeugen: Zwei gleichzeitig gesendete Anfragen würden sich stören. Das Plugin lässt daher den Austausch eines Proxys **nacheinander** ablaufen, alle Fahrzeuge zusammen (Lesevorgänge des Zyklus, Befehle, **Aktualisieren**, **Kopplung prüfen**).

- **Ein und derselbe Proxy**: nur ein Austausch gleichzeitig. Läuft gerade ein Befehl, entfällt das Lesen des Zyklus und wird beim nächsten Durchlauf (in der Minute darauf) nachgeholt; ein Befehl oder ein **Aktualisieren** wartet, bis er an der Reihe ist. Dauert das Warten zu lange (etwa 2 Minuten), gibt das Plugin auf und zeigt **Proxy ausgelastet** an: Versuchen Sie es gleich erneut (siehe [Fehlerbehebung](#fehlerbehebung)).
- **Verschiedene Proxys**: Sie werden **parallel** gelesen und warten nie aufeinander. Ein langsamer oder angehaltener Proxy verzögert nur seine eigenen Fahrzeuge; der Zyklus dauert so lange wie sein langsamster Proxy.
- **Im schlimmsten Fall** (sehr langsamer Proxy, jedes Lesen erreicht seine maximale Frist) liest ein 4-Minuten-Zyklus höchstens **3 Fahrzeuge pro Proxy**; darüber hinaus werden die letzten in diesem Zyklus möglicherweise nicht gelesen. In der Praxis dauert ein Lesen einige Sekunden.

### Übersicht der Einstellungen für Takt und Aufwecken

Alle diese Einstellungen befinden sich im Reiter **Gerät** jedes Fahrzeugs (siehe [Konfiguration der Geräte](#konfiguration-der-gerate)). Die Standardwerte gelten nach dem Update auch für bestehende Fahrzeuge.

| Einstellung | Standard | Mögliche Werte | Auswirkung auf die Fahrzeugbatterie |
|---|---|---|---|
| **Aktualisierungsintervall** | 5 Minuten | 1, 2, 5, 10, 15 oder 30 Minuten | Je länger, desto weniger wird das Fahrzeug beansprucht. Allein weckt es das Fahrzeug nie auf. |
| **Intervall während des Ladens** | Deaktiviert | Deaktiviert oder 1, 2, 5, 10 oder 15 Minuten | Ohne Wirkung außerhalb des Ladens; während des Ladens ist das Fahrzeug ohnehin wach. |
| **Fahrzeug einschlafen lassen** | Angehakt | Angehakt oder nicht angehakt | Angehakt: Das Plugin hört auf, Daten zu lesen, wenn das Fahrzeug inaktiv ist, damit es einschlafen kann. |
| **Unveränderte Lesevorgänge vor dem Zeitfenster** | 3 | 1, 2, 3, 4, 5, 10 oder 15 | Je niedriger, desto schneller öffnet sich das Zeitfenster. |
| **Dauer des Zeitfensters** | 30 Minuten | 15, 20, 30, 45 Minuten, 1 Stunde, 1 Stunde 30 oder 2 Stunden | Je länger, desto mehr Zeit hat das Fahrzeug zum Einschlafen, aber desto länger bleiben die Daten eingefroren. |
| **Verzögerung des erneuten Lesens nach Befehl** | 30 Sekunden | 30 Sekunden, 45 Sekunden, 1 Minute, 1 Minute 30 oder 2 Minuten | Ein Lesevorgang pro erfolgreichem Befehl, ohne Aufwecken. |
| **Klimaanlage ebenfalls lesen** | Ja | Ja oder Nein, nur Laden | „Nur Laden“ verkürzt die Datenabfrage (Gewinn auf Ihrer Installation zu messen). |
| **Aktualisieren (mit Aufwecken)** (Befehl `refresh_wakeup`) | | Aktion, von Hand oder aus einem Szenario zu starten | **Weckt** das Fahrzeug bei jeder Ausführung **auf**. |
| **Alter der Daten (min)** (Information `data_age`) | | Minuten seit dem letzten erfolgreichen Lesen der Daten; **99999** = kein Lesen bekannt (oder mehr als 69 Tage) | Keine: lokale Berechnung, der Proxy wird nicht abgefragt. |

Die **Dauer des Zeitfensters** wirkt nur, wenn sie das Aktualisierungsintervall übersteigt. Einzelheiten zu jeder Einstellung: [Aktualisierung der Informationen](#aktualisierung-der-informationen), [Beschleunigtes Lesen während des Ladens](#beschleunigtes-lesen-wahrend-des-ladens), [Fahrzeug einschlafen lassen](#fahrzeug-einschlafen-lassen) und [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl).

### Empfehlungen je nach Verwendung

Die folgenden Werte sind **unverbindliche Ausgangspunkte, die Sie anhand Ihrer eigenen Messungen anpassen sollten**: Die tatsächliche Auswirkung auf die Batterie hängt vom Modell, von der Software des Fahrzeugs und seiner Umgebung ab, und das Plugin garantiert nicht, dass das Fahrzeug einschläft. Mangels verlässlicher Messung wird hier kein Batterieprozentsatz angegeben; die Tabelle beziffert, was das Plugin tatsächlich tut: die Anzahl der Datenabfragen pro Stunde und die Zeit, die dem Fahrzeug zum Einschlafen bleibt.

| Verwendung | Aktualisierungsintervall | Intervall während des Ladens | Einschlaffenster | Klimaanlage ebenfalls lesen | Datenabfragen (Fahrzeug wach, inaktiv, nicht beim Laden) |
|---|---|---|---|---|---|
| **Einfache Überwachung** (Anwesenheit, Verriegelung, Batteriestand) | 10 bis 15 Minuten | Deaktiviert | Angehakt, 3 unveränderte Lesevorgänge, 30 Minuten (Standardwerte) | Ja | höchstens 4 bis 6 pro Stunde; **keine** während der 30 Minuten eines geöffneten Fensters |
| **Solarsteuerung** (Strom nach Erzeugung anpassen) | 5 Minuten | **1 Minute** | Angehakt, 3 unveränderte Lesevorgänge, 30 Minuten (Standardwerte) | Nein (nur Laden), wenn Sie die Klimaanlage nicht nutzen | 12 pro Stunde außerhalb des Ladens; **60 pro Stunde beim Laden** (das Fenster öffnet sich beim Laden nie) |
| **Engmaschige Überwachung** (Laden oder Vorklimatisierung genau beobachtet) | 1 bis 2 Minuten | 1 Minute | Angehakt, 3 unveränderte Lesevorgänge, 30 Minuten | Ja | 30 bis 60 pro Stunde: Das Fahrzeug schläft nicht, solange das Fenster nicht geöffnet ist; reservieren Sie dieses Profil für einen bestimmten Zeitraum |
| **Mehrere Fahrzeuge an einem Proxy** (höchstens 3) | 10 bis 15 Minuten | Deaktiviert, außer für das gesteuerte Fahrzeug | Angehakt | Ja | Die Lesevorgänge eines Proxys laufen nacheinander ab: Halten Sie die Intervalle lang |

Für die Solarsteuerung belassen Sie außerdem die **Verzögerung des erneuten Lesens nach Befehl** bei 30 Sekunden und legen Sie die **Ladestrom**-Befehle Ihres Szenarios zeitlich auseinander (nach jedem erfolgreichen Befehl wird ein erneutes Lesen gestartet).

**Die Wirkung bei sich zu Hause messen.** Notieren Sie abends und morgens den Stand von **Batterieladung**, bei geparktem Fahrzeug ohne Insassen, einige Nächte lang mit angehaktem **Fahrzeug einschlafen lassen**, dann einige Nächte ohne Haken. Historisieren Sie **Fahrzeug wach**, um zu sehen, wie lange das Fahrzeug wach geblieben ist: Vergleichen Sie die beiden Reihen, bevor Sie das Intervall oder die Dauer des Zeitfensters anpassen.

## Widget und Anzeige

Dieser Abschnitt beschreibt, was das Plugin auf dem Dashboard und der mobilen Weboberfläche von Jeedom anzeigt: die **Fahrzeugkachel**, die **generischen Typen**, das **Modellbild** und die **Reihenfolge der Befehle**. Für diese Funktionen ist keine neuere Jeedom-Version erforderlich als für das Plugin selbst (siehe [Voraussetzungen](#voraussetzungen)), und sie rufen keine Internetseite auf: Alles wird von Ihrem Jeedom aus angezeigt.

**Was das Plugin niemals überschreibt**: einen von Ihnen gewählten generischen Typ, ein von Ihnen hochgeladenes oder entferntes Bild, die von Ihnen geänderte Reihenfolge der Befehle und Ihre Wahl zwischen Kachel und Standard-Widget. Jeder Unterabschnitt nennt die genaue Regel.

### Fahrzeugkachel

Jedes Fahrzeug wird standardmäßig als **Kachel** angezeigt: eine auf einen Blick lesbare Zusammenfassung, gefolgt von Ihren übrigen sichtbaren Befehlen.

Die Zusammenfassung enthält von oben nach unten:

- das **Modellbild** (sofern vorhanden, siehe [Modellbild](#modellbild));
- **Batterie** (der Stand, groß dargestellt) und **Ladelimit**;
- **Reichweite** (in km) und **Ladezustand** (übersetzte Bezeichnung: lädt, abgeschlossen, getrennt …);
- zwei Plaketten: **Verriegelt** oder **Entriegelt** sowie **In Reichweite** oder **Außer Reichweite**;
- die Aktualität der Daten: **Daten von vor** gefolgt von einer Dauer (Minuten, Stunden oder Tage), oder **Keine bekannte Messung**;
- der **letzte Fehler** in einer roten Zeile, **nur wenn es einen gibt** (bei „Keine“ wird nichts angezeigt);
- sechs Schaltflächen: **Laden starten**, **Laden beenden**, **Türen verriegeln**, **Türen entriegeln**, **Aufwecken** und **Aktualisieren**.

Die **sichtbaren** Befehle des Geräts, die die Zusammenfassung nicht übernimmt (zum Beispiel die Temperatur, die Öffnungen, der Wächter-Modus), werden **unterhalb** der Zusammenfassung angezeigt, wie im Standard-Widget und in der Reihenfolge des Tabs **Befehle**. Die von der Zusammenfassung übernommenen Befehle werden darunter nicht wiederholt.

<!-- Capture à ajouter en recette : images/tuile-dashboard-normal.png (tuile d'un véhicule éveillé, données récentes, sur le dashboard) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-normal.png (même tuile sur l'interface mobile web) -->

#### Die vier Zustände der Kachel

| Zustand | Was Sie sehen |
|---|---|
| **Normal** (Fahrzeug wach, aktuelle Messung) | Batterie, Limit, Reichweite, Ladezustand, **In Reichweite**, Verriegelung, **Daten von vor** einigen Minuten; keine Fehlerzeile. |
| **Fahrzeug schläft** | Die **zuletzt gelesenen Werte** bleiben angezeigt (das Plugin weckt das Fahrzeug nie von sich aus), und die Dauer **Daten von vor** wächst. Es wird kein Fehler angezeigt: Das ist normal. Verwenden Sie **Aktualisieren (mit Aufwecken)** oder die Schaltfläche **Aufwecken**, um aktuelle Werte zu erhalten (siehe [Aktualisierung der Informationen](#aktualisierung-der-informationen)). |
| **Außer Reichweite** | Die Plakette zeigt **Außer Reichweite** an. Die Werte sind die zuletzt bekannten; die rote Zeile **letzter Fehler** erscheint, wenn der Proxy oder das Fahrzeug ein Problem gemeldet haben (siehe [Information „Letzter Fehler“ (Lesen)](#information-letzter-fehler-abfrage)). |
| **Fehler oder nie gelesen** | Ein fehlender, leerer oder nicht numerischer Wert wird als **Unbekannt** angezeigt (nie 0 % oder ein erfundenes Datum); die Aktualität zeigt **Keine bekannte Messung**, solange keine Messung gelungen ist; die rote Zeile nennt den letzten Fehler. |

<!-- Capture à ajouter en recette : images/tuile-dashboard-endormi.png (tuile d'un véhicule endormi, valeurs anciennes) -->
<!-- Capture à ajouter en recette : images/tuile-dashboard-hors-portee.png (pastille Hors de portée) -->
<!-- Capture à ajouter en recette : images/tuile-dashboard-erreur.png (ligne d'erreur et valeurs Inconnu) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-endormi.png (tuile d'un véhicule endormi sur l'interface mobile web) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-hors-portee.png (pastille Hors de portée sur l'interface mobile web) -->
<!-- Capture à ajouter en recette : images/tuile-mobile-erreur.png (ligne d'erreur et valeurs Inconnu sur l'interface mobile web) -->

#### Verhalten der Schaltflächen

- Eine Schaltfläche löst **den entsprechenden Befehl** des Fahrzeugs aus, wie die Schaltfläche dieses Befehls im Standard-Widget: gleiche Regeln, gleiche Meldungen.
- Eine **ausgegraute** Schaltfläche entspricht einem Befehl, der im Gerät **fehlt** oder von Ihrem Proxy **nicht unterstützt** wird (Meldung **Von Ihrer Proxy-Version nicht unterstützt**, siehe [Fehler beim Senden eines Befehls](#fehler-beim-senden-eines-befehls)). **Aktualisieren** ist nur ausgegraut, wenn der Befehl fehlt.
- Während der Ausführung ist die Schaltfläche **abgeblendet** und reagiert nicht mehr; sie ist **sobald der Befehl abgeschlossen ist** wieder verwendbar, ob erfolgreich oder fehlerhaft, spätestens nach 4 Minuten. Bei einem Fehler zeigt Jeedom seine übliche Fehlermeldung an.
- Die Kachel **aktualisiert sich von selbst**, ohne die Seite neu zu laden, wenn sich ein Wert ändert.
- Die Kachel fügt **keine Bestätigung** hinzu: Eine etwaige Bestätigung bleibt die von Jeedom für den Befehl (siehe [Bestätigung sensibler Aktionen](#bestatigung-sensibler-aktionen)).
- In der **nativen mobilen App** von Jeedom wird die Kachel nicht verwendet: Die App stützt sich auf die [generischen Typen](#generische-typen).

#### Zum Standard-Widget zurückkehren

Tun Sie dies, wenn Sie die Befehls-Widgets von Jeedom bevorzugen.

1. Öffnen Sie **Plugins > Verbundene Objekte > Tesla BLE** und klicken Sie auf das Fahrzeug.
2. Klicken Sie auf **Erweiterte Konfiguration** (oben auf der Geräteseite).
3. Deaktivieren Sie das Kontrollkästchen **Widget-Template**.
4. Klicken Sie auf **Speichern** und laden Sie dann das Dashboard neu.

Das Fahrzeug wird dann mit dem **Standard-Widget** von Jeedom angezeigt: eine Kachel pro sichtbarem Befehl, **ohne das Modellbild** (dieses Bild wird nur von der Kachel gezeichnet).

#### Das Widget des Plugins wiederherstellen

1. Öffnen Sie die **Erweiterte Konfiguration** des Fahrzeugs, wie oben.
2. **Aktivieren** Sie das Kontrollkästchen **Widget-Template**.
3. Klicken Sie auf **Speichern** und laden Sie dann das Dashboard neu.

Die Kachel kehrt zurück; kein Befehl wird geändert.

#### Bestehende Geräte nach dem Update

Beim Update wird die Kachel auf jedem bestehenden Gerät **aktiviert**, **außer** es hatte bereits eine angepasste Darstellung: Anordnung **als Tabelle** oder ein von Hand gewähltes Befehls-Widget. Diese Geräte behalten das Standard-Widget; aktivieren Sie das Kontrollkästchen **Widget-Template**, wenn Sie die Kachel möchten. Ein Gerät, bei dem das Kontrollkästchen **Widget-Template** bereits eingestellt war, behält ebenfalls seine Wahl.

#### Einzelne Befehle ausblenden, ohne die Kachel zu verlieren

Die Kachel liest die Befehle des Fahrzeugs **auch dann, wenn sie ausgeblendet sind**. Um die Anzeige unter der Zusammenfassung zu entlasten, öffnen Sie den Tab **Befehle** und deaktivieren Sie **Anzeigen** bei den Befehlen, die Sie nicht mehr sehen möchten: Die Zusammenfassung und ihre sechs Schaltflächen ändern sich nicht.

#### Grenzen der Kachel

- Die Dauer **Daten von vor** wird im Browser zwischen zwei Aktualisierungen nicht „fortgeschrieben“: Sie folgt dem Wert von **Alter der Daten (min)**, den das Plugin jede Minute neu berechnet.
- Das Standard-Widget zeigt das Modellbild **nicht** an.
- Kann die Kachel nicht gezeichnet werden, zeigt Jeedom stattdessen das **Standard-Widget** an, und das Plugin schreibt dies in sein Log (siehe [Meldungen im Log des Plugins](#meldungen-des-plugin-logs)).

### Generische Typen

Ein **generischer Typ** ist eine Kennzeichnung, die Jeedom auf einen Befehl setzt (Batterie, Temperatur, Öffnung, Schloss …), damit die **mobile App**, die **Sprachassistenten** und Drittanbieter-Plugins wissen, was er darstellt. Das Plugin setzt sie für Sie.

Um sie anzusehen oder zu ändern: Klicken Sie am Gerät im Tab **Befehle** auf das **Zahnrad** des Befehls und suchen Sie das Feld **Generischer Typ**. Die genauen Bezeichnungen der Typen hängen von Ihrer Jeedom-Version ab; die Tabelle nennt auch ihre Kennung.

| Befehl | Gesetzter generischer Typ |
|---|---|
| **Batterieladung** | Batterie (`BATTERY`) |
| **Ladespannung** | Spannung (`VOLTAGE`) |
| **Kumulierte Ladeenergie** | Verbrauch (`CONSUMPTION`) |
| **Innentemperatur**, **Außentemperatur** | Temperatur (`TEMPERATURE`) |
| **Fahrzeugverriegelung** | Schlosszustand (`LOCK_STATE`) |
| **Tür vorne Fahrer**, **Tür vorne Beifahrer**, **Tür hinten Fahrer**, **Tür hinten Beifahrer**, **Kofferraum hinten**, **Frunk (vorderer Kofferraum)**, **Ladeklappe (Öffnung)**, **Tonneau-Abdeckung** | Öffnung (`OPENING`) |
| **Reifendruck vorne links**, **vorne rechts**, **hinten links**, **hinten rechts** | Druck (`PRESSURE`) |
| **Türen verriegeln** | Schloss, schließen (`LOCK_CLOSE`) |
| **Türen entriegeln** | Schloss, öffnen (`LOCK_OPEN`) |
| **Laden starten** | Steckdose, Ein (`ENERGY_ON`) |
| **Laden beenden** | Steckdose, Aus (`ENERGY_OFF`) |

Die Druckinformationen gibt es nur, wenn Ihr Proxy sie meldet (siehe [Erweiterte Daten: Was verfügbar ist](#erweiterte-daten-was-verfugbar-ist)).

> **ACHTUNG: Diese Typen machen Aktionen für die Gruppenaktionen von Jeedom zugänglich.** Wenn Sie das Fahrzeug in einem Jeedom-**Objekt** platzieren, können die **Zusammenfassungsaktionen** des Objekts und die Szenarioaktionen „Generischer Typ“ **das Fahrzeug entriegeln** (Schloss: öffnen) oder **sein Laden starten und beenden** (Steckdose: Ein und Aus), **ohne jede Bestätigung in der Oberfläche**. Wenn Sie das nicht möchten, setzen Sie den **Generischen Typ** dieser Befehle auf **Keine**: Diese Wahl bleibt erhalten.

Wann das Plugin einen Typ setzt:

- **bei der Erstellung** eines Befehls (neues Gerät, durch ein Update hinzugefügter Befehl);
- **ein einziges Mal** bei den bestehenden Befehlen, beim Update, das die Typen mitbringt, und **ausschließlich bei einem Befehl, dessen Typ leer ist**.

Ein von Ihnen gewählter Typ wird **nie überschrieben**, auch wenn er vom Typ des Plugins abweicht.

**Einschränkung: Ein von Hand geleerter Typ** (**Keine**) wird weder durch ein Speichern des Geräts noch durch den Aktualisierungszyklus neu gesetzt. Er kann nur in zwei Fällen neu gesetzt werden: Der Befehl wird vom Plugin **gelöscht und neu erstellt** (er startet dann mit dem Standardtyp), oder das Plugin **wiederholt** das Setzen der Typen auf den bestehenden Befehlen, was nur nach einem Update vorkommt, das durch einen Fehler an einem anderen Gerät unterbrochen wurde. Setzen Sie in diesen Fällen erneut **Keine**.

### Modellbild

Das Plugin ordnet jedem Fahrzeug ein **Bild seines Modells** zu, das aus der **VIN** abgeleitet wird. Es wird auf der **Kachel** und in der **Geräteliste** von Jeedom angezeigt. Dabei handelt es sich um neutrale Piktogramme, die mit dem Plugin geliefert werden, ohne Download.

| Modell (aus der VIN decodiert) | Bild |
|---|---|
| Model S, Model 3, Model X, Model Y, Cybertruck | Piktogramm des Modells |
| Semi, Roadster, unbekanntes Modell | Keines: Das **Plugin-Symbol** bleibt angezeigt |

Regeln:

- Das Bild wird **beim Speichern des Geräts** (und beim Update des Plugins) gesetzt, wenn das Modell bekannt ist und das Fahrzeug **kein eigenes Bild hat**.
- Ein **eigenes Bild** (das Sie hochgeladen haben) wird **nie angetastet**.
- Das Bild **ersetzen**: Öffnen Sie die **Erweiterte Konfiguration** des Fahrzeugs und laden Sie Ihr eigenes hoch. Es bleibt erhalten.
- Das Bild **entfernen**: Verwenden Sie in der **Erweiterten Konfiguration** **Bild entfernen**. **Dieses Entfernen ist endgültig**: Das Plugin setzt das Bild nie von sich aus wieder, auch nicht, wenn Sie das Gerät speichern oder das Plugin aktualisieren. Stattdessen wird das Plugin-Symbol angezeigt.
- Es gibt **keine Schaltfläche**, um das Bild des Plugins nach dem Entfernen zurückzuholen: Wenn Sie ein Bild haben möchten, laden Sie Ihr eigenes hoch.
- Ändert sich die **VIN** zu einem Modell ohne Bild, wird das vom Plugin gesetzte Bild entfernt; ein von Ihnen gewähltes Bild bleibt.
- Kann Jeedom nicht in seinen Bilderordner schreiben oder ist das Bild des Plugins nicht lesbar (installieren Sie das Plugin neu), schreibt das Plugin eine Warnung in sein Log, und das Plugin-Symbol bleibt angezeigt (siehe [Meldungen im Log des Plugins](#meldungen-des-plugin-logs)).

### Reihenfolge der Befehle

Die Befehle eines neuen Geräts werden **nach Themen** in dieser Reihenfolge angeordnet:

1. **Status**: Anwesenheit, Verriegelung, Wachzustand, Insasse, Wächter-Modus, Alter der Daten, letzter Fehler;
2. **Laden**: Batterie, Reichweite, Ladezustand, Limits, Leistung, Energie, Zeitpläne;
3. **Klima**: Temperaturen, Klimaanlage, Heizungen, Enteisung;
4. **Öffnungen**: Türen, Kofferräume, Ladeklappe, Warnungen;
5. **Fahrzeug**: Modell, Kilometerstand, Fahren, Position, Reifen, Software-Update;
6. **Proxy-Überwachung**: Proxy erreichbar, Version, Schlüsselrolle, Lesedauern;
7. **Aktionen**: Lesen (aktualisieren, aufwecken), Laden, Klima, Zugang (Türen, Kofferräume, Wächter-Modus, Lichter, Hupe).

Regeln:

- Die Reihenfolge wird **nur bei der Erstellung jedes Befehls** gesetzt. Sie wird **nie neu geschrieben**: Ein Update des Plugins **verschiebt keinen bestehenden Befehl**.
- Ein **später hinzugefügter** Befehl (durch ein Update) wird **neben einem Befehl seines Themas** eingeordnet; bei gleicher Position unterscheidet Jeedom sie nach dem Namen. Gibt es am Gerät **keinen** Befehl dieses Themas, wird er **gesammelt am Ende der Liste** hinzugefügt.
- Zum **Neuordnen**: Öffnen Sie den Tab **Befehle** des Geräts, **ziehen** Sie die Zeilen per Drag-and-drop in die gewünschte Reihenfolge und klicken Sie dann auf **Speichern**. Ihre Reihenfolge bleibt erhalten.
- Die Reihenfolge des Tabs **Befehle** ist auch die der Anzeige unter der Kachel oder im Standard-Widget.

## Befehle

Die folgenden Tabellen nennen für jeden Befehl seine **Kennung** (`logicalId`, stabil: Die Szenarien finden ihn darüber), seinen Typ und Untertyp sowie seine Einheit. Die Bezeichnungen sind die eines **neuen Geräts**; ein von der Version 0.x migriertes Gerät behält seine alten Namen (siehe [Update von der Version 0.x](#update-von-version-0x)).

### Erweitertes Laden: Was verfügbar ist

Zusammenfassung dessen, was das erweiterte Laden hinzufügt. Die Informationen werden **ausgeblendet** erstellt (zeigen Sie sie im Tab **Befehle** an); die Einzelheiten zu jeder stehen in den Tabellen [Informationen](#informationen) und [Aktionen](#aktionen).

| Bezeichnung | Kennung | Einheit | Funktion | Details |
|---|---|---|---|---|
| Minimale Ladegrenze | `charge_limit_soc_min` | % | Niedrigstes vom Fahrzeug akzeptiertes Limit; stellt das **Min** des Schiebereglers **Ladelimit** ein | [Nachgeführte Grenzen des Fahrzeugs](#ausfuhrung-der-befehle) |
| Maximale Ladegrenze | `charge_limit_soc_max` | % | Höchstes akzeptiertes Limit; stellt das **Max** desselben Schiebereglers ein | [Nachgeführte Grenzen des Fahrzeugs](#ausfuhrung-der-befehle) |
| Maximaler Ladestrom | `charge_current_request_max` | A | Vom Fahrzeug gemeldeter Höchststrom; stellt das **Max** des Schiebereglers **Ladestrom** ein | [Nachgeführte Grenzen des Fahrzeugs](#ausfuhrung-der-befehle) |
| Ladestatus (übersetzt) | `charging_state_label` | | Ladezustand in der Sprache von Jeedom, für die Anzeige | [Informationen](#informationen) |
| Nennreichweite | `battery_range` | km | Nennreichweite | [Informationen](#informationen) |
| Geschätzte Reichweite | `est_battery_range` | km | Reichweite entsprechend Ihrer jüngsten Fahrweise | [Informationen](#informationen) |
| Batteriestand (roh) | `battery_level` | % | Batteriestand, wie ihn das Fahrzeug meldet | [Informationen](#informationen) |
| Ladeleistung | `charger_power` | kW | Ans Fahrzeug abgegebene Leistung | [Informationen](#informationen) |
| Tatsächlicher Ladestrom | `charger_actual_current` | A | Tatsächlich abgegebener Strom | [Informationen](#informationen) |
| Ladephasen | `charger_phases` | | Anzahl der verwendeten Phasen | [Informationen](#informationen) |
| Hinzugefügte Energie | `charge_energy_added` | kWh | Während der laufenden (oder letzten) Sitzung hinzugefügte Energie | [Informationen](#informationen) |
| Ladekabel | `conn_charge_cable` | | Typ des angeschlossenen Kabels | [Informationen](#informationen) |
| Schnellladen | `fast_charger_present` | | 1, wenn an einer Schnellladesäule angeschlossen | [Informationen](#informationen) |
| Kumulierte Ladeenergie | `charge_energy_total` | kWh | Ein nur steigender Zähler für die Energieerfassung | [Zähler der Ladeenergie](#ladeenergiezahler) |
| Geplante Ladezeit | `scheduled_charging_start_time` | | Startzeit des verzögerten Ladens (`HH:MM`) | [Im Fahrzeug gelesene Zeitpläne](#informationen) |
| Ende der Niedertarifzeit | `off_peak_hours_end_time` | | Ende der Niedertarifzeit des Fahrzeugs (`HH:MM`) | [Im Fahrzeug gelesene Zeitpläne](#informationen) |
| Geplante Vorklimatisierung | `scheduled_preconditioning_time` | | Vom Vorklimatisieren angepeilte Abfahrtszeit (`HH:MM`) | [Im Fahrzeug gelesene Zeitpläne](#informationen) |
| Nach Überschuss anpassen | `adjust_surplus` | W | Aktion: Erhält die verfügbare Leistung und entscheidet, ob ein Befehl gesendet wird | [Steuerung nach Überschuss](#uberschusssteuerung) |
| Ladeplan hinzufügen | `add_charge_schedule` | | Aktion: Erstellt oder ersetzt den von Jeedom verwalteten Ladeplan (Proxy des Forks) | [Das Laden planen](#ladeplan-erstellen) |
| Ladeplan löschen | `remove_charge_schedule` | | Aktion: Löscht diesen Ladeplan (Proxy des Forks) | [Das Laden planen](#ladeplan-erstellen) |

Die Aktionen des erweiterten Ladens sind ebenfalls ausgeblendet. Zwei Funktionen werden am Gerät statt über einen Befehl eingestellt:

| Geräteeinstellungen | Funktion | Details |
|---|---|---|
| **Netzspannung**, **Phasen**, **Anpassungsschritt**, **Hysterese**, **Mindestintervall zwischen Befehlen**, **Minimaler Startstrom**, **Abschaltschwelle**, **Haltedauer vor dem Abschalten** | Steuerung nach Überschuss (Standardwerte: 230 V, einphasig, 1 A, 2 A, 120 s, 6 A, 5 A, 300 s) | [Konfiguration der Geräte](#konfiguration-der-gerate) und [Steuerung nach Überschuss](#uberschusssteuerung) |
| **Ladesteuerung**, **Beginn des Zeitraums**, **Ende des Zeitraums**, **Ziel-SoC (%)**, **Am Ende des Zeitraums stoppen** | Laden zur Niedertarifzeit (standardmäßig deaktiviert) | [Laden zur Niedertarifzeit](#laden-zur-niedertarifzeit) |

### Klima und Komfort: Was verfügbar ist

Zusammenfassung dessen, was Klimaanlage und Komfort ermöglichen. Der offizielle Proxy 2.3.0 liest alles, kann aber weder den Temperatur-Sollwert, die Sitze, das Lenkrad, die maximale Enteisung noch das Klimahalten einstellen: Diese Befehle erfordern den **Proxy des Forks** (Versionen `2.3.0-tb.N`) und werden **ausgeblendet** erstellt. Die Schlüsselrolle **Owner** wird für die Aktionen als erforderlich **angenommen** (im realen Einsatz nicht bestätigt: „zu bestätigen“).

| Funktion | Kennung | Verfügbarkeit | Schlüsselrolle | Wirkung auf das Fahrzeug | Details |
|---|---|---|---|---|---|
| Klimainformationen (von **Klimaautomatik** bis **Batterieheizung**, darunter **Klimahaltemodus (Hund, Camp)**) | `is_auto_conditioning_on`… `battery_heater` | Offizieller Proxy 2.3.0 | Charging Manager genügt (Lesen) | Nur Lesen, kein Aufwecken: Sie behalten ihren letzten Wert, solange das Fahrzeug schläft. Ausgeblendet erstellt | [Informationen](#informationen) |
| Sollwert Fahrer, Sollwert Beifahrer | `set_driver_temp`, `set_passenger_temp` | Proxy des Forks, mindestens `2.3.0-tb.1` | Owner angenommen | Stellt die gewünschte Temperatur ein; beide Seiten werden gemeinsam gesendet; der Proxy weckt das Fahrzeug | [Den Temperatur-Sollwert einstellen](#temperatursollwert-einstellen) |
| Heizung der fünf Sitze, Lenkradheizung | `set_seat_heater_left`, `set_seat_heater_right`, `set_seat_heater_rear_left`, `set_seat_heater_rear_right`, `set_seat_heater_rear_center`, `set_steering_wheel_heater` | Proxy des Forks, mindestens `2.3.0-tb.2` | Owner angenommen | Heizt den Sitz oder das Lenkrad; verlangt grundsätzlich eine laufende Klimaanlage; der Proxy weckt das Fahrzeug | [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen) |
| Maximale Enteisung | `set_preconditioning_max` | Proxy des Forks, mindestens `2.3.0-tb.1` | Owner angenommen | **Weckt** das Fahrzeug und **verbraucht Batterie**, solange sie läuft; endet nicht von selbst | [Maximale Enteisung](#maximale-enteisung) |
| Modus Klimahalten (Halten, Hund, Camp) | `set_climate_keeper_mode` | Proxy des Forks, mindestens `2.3.0-tb.1` | Owner angenommen | **Weckt** das Fahrzeug und **verbraucht über lange Zeit Batterie**; endet nicht von selbst | [Hundemodus, Campmodus und Klimahalten](#hundemodus-campmodus-und-klimahaltemodus) |
| Klimaanlage starten, Klimaanlage stoppen | `auto_conditioning_start`, `auto_conditioning_stop` | Offizieller Proxy 2.3.0 | Owner angenommen (wahrscheinlich abgelehnt mit Charging Manager) | Startet oder stoppt die Vorklimatisierung; der Start weckt das Fahrzeug und verbraucht Batterie | [Aktionen](#aktionen) |
| Von Jeedom geplante Vorklimatisierung (Geräteeinstellung) | Keine: Abschnitt **Von Jeedom geplante Vorklimatisierung** | Offizieller Proxy 2.3.0 | Owner angenommen (ein einziger Versuch pro Abfahrt mit Charging Manager) | Jeedom startet die Klimaanlage vor der Abfahrtszeit und stoppt sie dann; der Start weckt das Fahrzeug und verbraucht Batterie | [Von Jeedom geplante Vorklimatisierung](#von-jeedom-geplante-vorklimatisierung) |

> ⚠️ **Batterie.** Die maximale Enteisung, das Klimahalten und die im Voraus gestartete Klimaanlage **wecken das Fahrzeug** und **entnehmen Energie aus seiner Batterie**. Mangels verlässlicher Messung wird hier kein beziffterter Verbrauch angegeben. Der **Hundemodus** ersetzt nicht die Überwachung der Innenraumtemperatur bei einem Tier.

**Warum manche Befehle abgelehnt oder ausgeblendet werden.** Der offizielle Proxy 2.3.0 hat die Befehle für Sollwert, Sitze, Lenkrad, maximale Enteisung und Klimahalten nicht: Der Fork fügt sie hinzu und **meldet** sie über seine Route `capabilities`. Solange der Proxy den Befehl nicht meldet, lehnt das Plugin ihn sofort mit **„Von Ihrer Proxy-Version nicht unterstützt“** ab, ohne etwas an das Fahrzeug zu senden. Diese Befehle werden **ausgeblendet** erstellt, auch nach dem Wechsel zum Fork: Aktivieren Sie **Anzeigen** im Tab **Befehle** oder rufen Sie sie aus einem Szenario auf. Nach dem Wechsel zum Fork ist **keine Neuinstallation des Plugins** nötig: Die Verfügbarkeit wird neu gelesen, wenn sich die Version des Proxys ändert. Lehnt das Fahrzeug den Befehl anschließend wegen fehlender Rechte ab, ist ein **Owner**-Schlüssel erforderlich: siehe [Rolle des Schlüssels](#rolle-des-schlussels) und das Kopplungsverfahren [Den Schlüssel erzeugen und mit dem Fahrzeug koppeln](installation-proxy.md#8-den-schlussel-erzeugen-und-mit-dem-fahrzeug-koppeln). Die Symptome ohne Meldung sind unter [Klima und Komfort: Symptome ohne Meldung](#klima-und-komfort-symptome-ohne-meldung) beschrieben.

### Öffnungen und Sicherheit: Was verfügbar ist

Zusammenfassung der Öffnungen, der Anwesenheit, der Verriegelung, des Wächter-Modus und der Warnungen. Das Lesen funktioniert mit dem **offiziellen Proxy 2.3.0** und einem **Charging Manager**-Schlüssel. Die Befehle zum Öffnen der Kofferräume erfordern den **Proxy des Forks** (Versionen `2.3.0-tb.N`) und werden **ausgeblendet** erstellt. Die Schlüsselrolle **Owner** ist zum Verriegeln, Entriegeln und Steuern des Wächter-Modus erforderlich und wird für die Kofferräume als erforderlich **angenommen** (im realen Einsatz nicht bestätigt: „zu bestätigen“).

| Funktion | Kennung | Verfügbarkeit | Schlüsselrolle | Angeforderte Bestätigung | Details |
|---|---|---|---|---|---|
| Die acht Öffnungen (vier Türen, **Kofferraum hinten**, **Frunk (vorderer Kofferraum)**, **Ladeklappe (Öffnung)**, **Tonneau-Abdeckung**) | `door_front_driver`, `door_front_passenger`, `door_rear_driver`, `door_rear_passenger`, `trunk_rear`, `trunk_front`, `charge_port_closure`, `tonneau` | Offizieller Proxy 2.3.0 | Charging Manager genügt (Lesen) | Nicht zutreffend | [Informationen](#informationen) |
| **Insasse anwesend** | `user_present` | Offizieller Proxy 2.3.0 | Charging Manager genügt (Lesen) | Nicht zutreffend | [Informationen](#informationen) |
| **Fahrzeugverriegelung**, **Detaillierter Verriegelungsstatus** | `vehicule_lock`, `lock_state` | Offizieller Proxy 2.3.0 | Charging Manager genügt (Lesen) | Nicht zutreffend | [Informationen](#informationen) |
| **Wächter-Modus**, **Herkunft des Wächter-Modus** | `sentry_mode`, `sentry_mode_source` | Offizieller Proxy 2.3.0: Wert des **letzten Befehls**. Proxy des Forks mindestens `2.3.0-tb.2`: **tatsächlicher** Wert (Fahrzeug wach) | Charging Manager genügt (Lesen) | Nicht zutreffend | [Zustand des Wächter-Modus](#zustand-des-wachter-modus) |
| **Öffnungsalarm**, **Alarm entriegelt ohne Insassen** und die Einstellungen **Warnungen bei längerer Öffnung** | `closures_alert`, `unlocked_alert` | Offizieller Proxy 2.3.0 (Einstellungen am Gerät, Warnungen standardmäßig deaktiviert) | Charging Manager genügt (Lesen) | Nicht zutreffend | [Warnungen bei längerer Öffnung](#warnungen-bei-langerer-offnung) |
| Türen verriegeln, Türen entriegeln | `door_lock`, `door_unlock` | Offizieller Proxy 2.3.0 | **Owner** (abgelehnt mit Charging Manager) | Entriegeln: **ja** | [Aktionen](#aktionen) |
| Ladeklappe öffnen, Ladeklappe schließen | `charge_port_door_open`, `charge_port_door_close` | Offizieller Proxy 2.3.0 | Nicht bestätigt (siehe [Rolle des Schlüssels](#rolle-des-schlussels)) | Öffnen: **ja** | [Aktionen](#aktionen) |
| Wächter-Modus einstellen | `set_sentry_mode` | Offizieller Proxy 2.3.0 | **Owner** (abgelehnt mit Charging Manager) | **Ja** | [Zustand des Wächter-Modus](#zustand-des-wachter-modus) |
| Kofferraum hinten öffnen, Frunk öffnen | `open_trunk_rear`, `open_trunk_front` | Proxy des Forks, mindestens `2.3.0-tb.2` | Owner angenommen | **Ja** | [Den hinteren Kofferraum und den Frunk öffnen](#kofferraum-hinten-und-frunk-offnen) |

Die Aktionen, die eine Bestätigung verlangen, sind unter [Bestätigung sensibler Aktionen](#bestatigung-sensibler-aktionen) beschrieben. Der Unterschied **Tatsächlich** / **Letzter Befehl** beim Wächter-Modus wird unter [Zustand des Wächter-Modus](#zustand-des-wachter-modus) erklärt: Testen Sie **Herkunft des Wächter-Modus**, bevor Sie sich auf **Wächter-Modus** verlassen.

> **WICHTIG: vertrauenswürdiges Netzwerk.** Der Proxy hat standardmäßig **weder Authentifizierung noch Verschlüsselung (TLS)**; der Fork kann einen API-Token verlangen, optional. Mit einem Owner-Schlüssel kann jeder Rechner in Ihrem lokalen Netzwerk das Fahrzeug entriegeln oder einen Kofferraum öffnen, ohne über Jeedom zu gehen, und die Bestätigung von Jeedom hält ihn nicht auf. Betreiben Sie den Proxy in einem vertrauenswürdigen, idealerweise isolierten Netzwerk und setzen Sie seinen Port **niemals** dem Internet aus (siehe [Rolle des Schlüssels](#rolle-des-schlussels)).

**Warum die Kofferraum-Befehle abgelehnt oder ausgeblendet werden.** Der offizielle Proxy 2.3.0 hat den Befehl, der einen Kofferraum betätigt, nicht: Der Fork fügt ihn hinzu und **meldet** ihn über seine Route `capabilities`. Solange der Proxy ihn nicht meldet, lehnt das Plugin **Kofferraum hinten öffnen** und **Frunk öffnen** sofort mit **„Von Ihrer Proxy-Version nicht unterstützt“** ab, ohne etwas an das Fahrzeug zu senden. Um sie zu aktivieren: Installieren oder aktualisieren Sie den Proxy des Forks (mindestens `2.3.0-tb.2`), ohne das Plugin neu zu installieren oder das Gerät neu zu erstellen (die Verfügbarkeit wird neu gelesen, wenn sich die Version des Proxys ändert). Beide Befehle werden **ausgeblendet** erstellt, auch nach dem Wechsel zum Fork: Aktivieren Sie **Anzeigen** im Tab **Befehle** oder rufen Sie sie aus einem Szenario auf. Lehnt das Fahrzeug anschließend wegen fehlender Rechte ab, ist ein **Owner**-Schlüssel erforderlich. Die Symptome ohne Meldung sind unter [Öffnungen und Sicherheit: Symptome ohne Meldung](#offnungen-und-sicherheit-symptome-ohne-meldung) beschrieben.

### Erweiterte Daten: Was verfügbar ist

Zusammenfassung der Informationen des Bereichs „erweiterte Daten“: Modell, Kilometerstand und Fahren, Reifendruck, Software-Update und Position. Die Einzelheiten zu jeder Information (Bezeichnung, Kennung, Sichtbarkeit, Historisierung) stehen in der Tabelle [Informationen](#informationen). Alle sind **reine Lesewerte**, ohne Aufwecken des Fahrzeugs.

| Daten | Kennungen | Einheit | Voraussetzung am Proxy | Lesetakt |
|---|---|---|---|---|
| Modell und Jahr | `model`, `model_year` | | **Keine**: aus der VIN decodiert, ohne den Proxy abzufragen | Beim Speichern des Geräts, beim Update des Plugins und beim Start von Jeedom |
| Kilometerstand und Fahren | `odometer`, `shift_state`, `speed`, `power` | km, km/h, kW | Der Proxy muss `drive_state` **melden** | Bei jedem Lesen der Daten (Fahrzeug wach) |
| Reifendruck | `tpms_pressure_fl`, `_fr`, `_rl`, `_rr` | bar | Der Proxy muss `tire_pressure` **melden** | Höchstens alle **15 Minuten**, Fahrzeug wach |
| Software-Update | `software_update_status`, `software_update_version`, `software_update_progress` | % (Fortschritt) | Der Proxy muss `software_update` **melden** | Höchstens alle **15 Minuten**, Fahrzeug wach |
| Position | `latitude`, `longitude`, `at_home` | ° | Der Proxy muss `location_data` **melden** | Höchstens alle **15 Minuten**, Fahrzeug wach |

**Welcher Proxy?** Ein Proxy „meldet“ eine Angabe, wenn seine Route `capabilities` sie auflistet (`http://<IP_des_Proxys>:<port>/api/proxy/1/capabilities`, siehe [Rolle des Schlüssels](#rolle-des-schlussels)). Der **Proxy des Forks** mindestens `2.3.0-tb.2` meldet diese vier Kategorien; der **offizielle Proxy 2.3.0 liefert sie nicht**. Beim Kilometerstand ist die Funktion in das Projekt von wimaha eingeflossen, aber zum Zeitpunkt dieser Dokumentation ohne veröffentlichte Version: Sie wird nur mit einer Version gelesen, die sie **meldet**. Das Plugin verlässt sich nie auf eine Versionsnummer, nur auf diese Meldung: Prüfen Sie **Proxy-Version** und bei Bedarf die obige Adresse.

**Warum erweiterte Daten fehlen.** Bei einem Proxy, der eine Kategorie nicht meldet, werden die entsprechenden Informationen **nicht erstellt**: Sie erscheinen nicht im Tab **Befehle** (es gibt keinen angezeigten Wert „Nicht unterstützt“). Nur **Modell** und **Modelljahr** sind immer vorhanden. Um sie zu erhalten:

1. Prüfen Sie die **Proxy-Version** des Geräts und installieren oder aktualisieren Sie dann den **Proxy des Forks** (siehe [Die Version des Proxys prüfen und aktualisieren](#die-version-des-proxys-prufen-und-aktualisieren)).
2. Warten Sie den nächsten Aktualisierungszyklus ab (höchstens eine Minute): Bei der **Neuerkennung**, wenn sich die Version des Proxys ändert, liest das Plugin neu, was der Proxy meldet, und **erstellt von selbst** die nun verfügbaren Informationen. Weder eine Neuinstallation des Plugins noch eine Neuerstellung des Geräts ist nötig. Ein **Speichern** am Gerät lässt die fehlenden Informationen ebenfalls erstellen, wenn der Proxy sie meldet.
3. Prüfen Sie, dass sie sich füllen: Sie bleiben bis zum ersten Lesen bei **wachem Fahrzeug** leer (starten Sie **Aktualisieren (mit Aufwecken)**, um es auszulösen). Reifendrücke, Update und Position warten zusätzlich ab, dass 15 Minuten seit dem vorherigen Versuch vergangen sind.

Wenn ein Proxy eine Kategorie **meldet**, das Fahrzeug oder der Proxy sie aber **ablehnt** (**„Funktion von diesem Proxy nicht unterstützt — …“**), hört das Plugin auf, sie anzufordern, bis sich die Version des Proxys das nächste Mal ändert: siehe [Erweiterte Daten: Symptome ohne Meldung](#erweiterte-daten-symptome-ohne-meldung).

**Werte und Einheiten.**

- **Kilometerstand**: von Meilen in Kilometer umgerechnet, auf Zehntel genau. Ein Zähler von null oder ein unplausibler wird ignoriert. Standardmäßig historisiert.
- **Gang**: `P`, `R`, `N` oder `D`. **Leer** bedeutet „nicht mitgeteilt“: Das Plugin schreibt dann eine leere Zeichenkette, ein Test `== "D"` bleibt daher nach dem Anhalten nicht wahr.
- **Geschwindigkeit** und **Leistung**: Das Plugin geht von einer Geschwindigkeit in mph (in km/h umgerechnet) und einer Leistung in kW aus, negativ zulässig. Diese beiden Einheiten sind durch keine Fahrzeugdokumentation bestätigt: Vergleichen Sie mit dem Display Ihres Fahrzeugs, bevor Sie sich darauf verlassen. Ausgeblendet erstellt, da sie, weil der Proxy in der Garage steht, fast nie etwas anderes als 0 oder die Ladeleistung ergeben.
- **Reifendruck**: in **bar**, ohne Umrechnung. Ein Wert von null, ein negativer oder ein Wert über 10 bar wird ignoriert (die Information behält ihren letzten Wert oder bleibt leer). Die Reifen werden nur bei wachem Fahrzeug gelesen: Die letzten Werte bleiben angezeigt, wenn es schläft.
- **Update**: vier Bezeichnungen, **Keine**, **Verfügbar** (auch eine geplante Installation), **Download läuft** (auch beim Warten auf WLAN) und **Installation läuft**. **Vorgeschlagene Version** ist **Keine** außerhalb eines Updates und **Unbekannte**, wenn ein Update ohne gemeldete Version aktiv ist. **Fortschritt** ist 0 außerhalb von Download und Installation. Diese Bezeichnungen folgen der Sprache von Jeedom: Testen Sie in einem Szenario vorzugsweise **Fortschritt** oder vergleichen Sie in der aktuellen Sprache.
- **Modell** und **Modelljahr**: aus der VIN decodiert (Modell: 4. Zeichen; Jahr: 10. Zeichen, von 2008 bis 2037). Eine leere, nicht von Tesla stammende oder nicht decodierbare VIN ergibt **Unbekannt**. Sie sind **sichtbar** und **nicht historisiert**.
- **Position**: siehe [Position und Datenschutz](#position-und-datenschutz).

Die erweiterten Daten werden mit den Ladedaten gelesen: Sie folgen daher dem **Einschlaffenster** (kein Lesen während des Fensters, siehe [Das Fahrzeug einschlafen lassen](#fahrzeug-einschlafen-lassen)) und behalten ihren letzten Wert, solange das Fahrzeug schläft. Die Ablehnung einer einzelnen Kategorie verhindert die anderen Lesevorgänge nicht und ändert bei Reifendrücken, Update und Position nie **Letzter Fehler**.

### Informationen

„H“: standardmäßig historisiert. „V“: standardmäßig im Widget sichtbar. Sie können diese beiden Einstellungen auf dem Reiter **Befehle** ändern.

| Bezeichnung | Kennung | Typ / Untertyp | Einheit | H | V | Beschreibung |
|---|---|---|---|---|---|---|
| Fahrzeug anwesend | `isPresent` | Info / binär | | ja | ja | 1, wenn der Proxy das Fahrzeug per Bluetooth erreicht, 0, wenn es außer Reichweite ist |
| Fahrzeug wach | `vehicule_isAwake` | Info / binär | | ja | ja | 1, wenn das Fahrzeug wach ist, 0, wenn es schläft oder sein Schlafzustand unbekannt ist |
| Fahrzeugverriegelung | `vehicule_lock` | Info / binär | | ja | ja | 1, wenn das Fahrzeug verriegelt ist, auch von innen, 0, wenn es entriegelt ist, auch nur teilweise |
| Tür vorne Fahrer | `door_front_driver` | Info / binär | | ja | ja | 1, wenn die Tür offen ist, auch angelehnt, beim Öffnen oder beim Schließen, 0, wenn sie geschlossen ist |
| Tür vorne Beifahrer | `door_front_passenger` | Info / binär | | ja | ja | Gleiche Regel wie bei der Tür vorne Fahrer |
| Tür hinten Fahrer | `door_rear_driver` | Info / binär | | ja | ja | Gleiche Regel wie bei der Tür vorne Fahrer |
| Tür hinten Beifahrer | `door_rear_passenger` | Info / binär | | ja | ja | Gleiche Regel wie bei der Tür vorne Fahrer |
| Kofferraum hinten | `trunk_rear` | Info / binär | | ja | ja | 1, wenn der Kofferraum offen ist (auch angelehnt oder in Bewegung), 0, wenn er geschlossen ist |
| Frunk (vorderer Kofferraum) | `trunk_front` | Info / binär | | ja | ja | 1, wenn der vordere Kofferraum offen ist (auch angelehnt oder in Bewegung), 0, wenn er geschlossen ist |
| Ladeklappe (Öffnung) | `charge_port_closure` | Info / binär | | ja | ja | 1, wenn die Ladeklappe offen ist (auch angelehnt oder in Bewegung), 0, wenn sie geschlossen ist. Wird auch bei schlafendem Fahrzeug gelesen, anders als **Ladeklappe geöffnet** |
| Tonneau-Abdeckung | `tonneau` | Info / binär | | ja | ja | 1, wenn die Tonneau-Abdeckung (Cybertruck) offen ist, 0, wenn sie geschlossen ist; auch 0 bei einem Fahrzeug, das keine hat |
| Insasse anwesend | `user_present` | Info / binär | | ja | ja | 1, wenn das Fahrzeug eine Person an Bord erkennt, sonst 0; unbekannter Zustand = letzter Wert |
| Detaillierter Verriegelungsstatus | `lock_state` | Info / Text | | nein | ja | Bezeichnung der Verriegelung: **Entriegelt**, **Verriegelt**, **Von innen verriegelt** oder **Selektive Entriegelung**; ein unbekannter Wert wird unverändert angezeigt. Er folgt der Sprache von Jeedom: Testen Sie in einem Szenario **Fahrzeugverriegelung** und **Insasse anwesend**, denn eine verglichene Bezeichnung hängt von der Sprache ab |
| Wächter-Modus | `sentry_mode` | Info / Text | | nein | ja | **Aktiv**, **Inaktiv** oder **Unbekannt** (weder Messwert noch Befehl bekannt). Siehe [Status des Wächter-Modus](#zustand-des-wachter-modus). Er folgt der Sprache von Jeedom: Vergleichen Sie in einem Szenario in der aktuellen Sprache von Jeedom und testen Sie **Herkunft des Wächter-Modus**, um zu wissen, woher der Wert stammt |
| Herkunft des Wächter-Modus | `sentry_mode_source` | Info / Text | | nein | ja | **Tatsächlich** (am Fahrzeug gelesen), **Letzter Befehl** (aus dem letzten erfolgreichen Befehl des Plugins abgeleitet) oder **Keine** (noch nichts gelesen oder angeordnet). Gleiche Sprachregel wie bei **Wächter-Modus** |
| Öffnungsalarm | `closures_alert` | Info / binär | | ja | nein | 1, solange eine Öffnung länger als die eingestellte Dauer offen geblieben ist (nur bei aktiviertem Alarm), sonst 0. Siehe [Alarme bei längerer Öffnung](#warnungen-bei-langerer-offnung). |
| Alarm entriegelt ohne Insassen | `unlocked_alert` | Info / binär | | ja | nein | 1, solange das Fahrzeug länger als die eingestellte Dauer ohne Insassen entriegelt geblieben ist (nur bei aktiviertem Alarm), sonst 0. Siehe [Alarme bei längerer Öffnung](#warnungen-bei-langerer-offnung). |
| Ladestatus | `charging_state` | Info / Text | | nein | ja | Vom Fahrzeug gemeldeter Ladezustand, ohne Übersetzung: `Charging`, `Disconnected`, `Complete`, `Stopped`, `Starting`, `NoPower`, `Calibrating` oder `Unknown`. Dieser Wert ist in einem Szenario zu testen |
| Ladestatus (übersetzt) | `charging_state_label` | Info / Text | | nein | nein | Der Ladezustand in der Sprache von Jeedom (**Lädt**, **Getrennt**, **Abgeschlossen**, **Gestoppt**, **Start**, **Kein Strom**, **Kalibrierung**, **Unbekannt**) zur Anzeige. Ein Zustand, den das Plugin nicht kennt, wird so angezeigt, wie das Fahrzeug ihn sendet. Er folgt der Sprache von Jeedom: Testen Sie in einem Szenario **Ladestatus**, nie diese Bezeichnung |
| Ladegrenze | `charge_limit_soc` | Info / numerisch | % | ja | ja | Konfigurierte Ladegrenze |
| Minimale Ladegrenze | `charge_limit_soc_min` | Info / numerisch | % | nein | nein | Niedrigste Ladegrenze, die das Fahrzeug akzeptiert (dient als **Min** für den Schieberegler **Ladelimit**) |
| Maximale Ladegrenze | `charge_limit_soc_max` | Info / numerisch | % | nein | nein | Höchste Ladegrenze, die das Fahrzeug akzeptiert (dient als **Max** für den Schieberegler **Ladelimit**) |
| Batterieladung | `usable_battery_level` | Info / numerisch | % | ja | ja | Nutzbarer Batteriestand |
| Batteriestand (roh) | `battery_level` | Info / numerisch | % | nein | nein | Batteriestand, wie das Fahrzeug ihn meldet, von 0 bis 100 %. Er kann um einige Punkte von **Batterieladung** (nutzbarer Stand) abweichen |
| Reichweite | `ideal_battery_range` | Info / numerisch | km | ja | nein | Sogenannte ideale Reichweite, in Kilometer umgerechnet (das Fahrzeug liefert sie in Meilen) |
| Nennreichweite | `battery_range` | Info / numerisch | km | nein | nein | Nennreichweite, in Kilometer umgerechnet. Sie ist in der Regel identisch mit der sogenannten idealen Reichweite |
| Geschätzte Reichweite | `est_battery_range` | Info / numerisch | km | nein | nein | Anhand Ihrer jüngsten Fahrweise geschätzte Reichweite, in Kilometer umgerechnet |
| Ladespannung | `charger_voltage` | Info / numerisch | V | nein | nein | Von der Ladestation gelieferte Spannung |
| Ladegeschwindigkeit | `charge_rate` | Info / numerisch | km/h | nein | nein | Pro Ladestunde gewonnene Reichweite, in km/h umgerechnet (das Fahrzeug liefert sie in Meilen pro Stunde) |
| Ladeleistung | `charger_power` | Info / numerisch | kW | nein | nein | An das Fahrzeug gelieferte Leistung in Kilowatt (das Fahrzeug liefert sie in der Regel als ganzzahligen Wert) |
| Tatsächlicher Ladestrom | `charger_actual_current` | Info / numerisch | A | nein | nein | Tatsächlich gelieferter Strom, nicht zu verwechseln mit dem konfigurierten Strom (**Ladestrom (A)**) |
| Ladephasen | `charger_phases` | Info / numerisch | | nein | nein | Anzahl der beim Laden verwendeten Phasen; in der Regel 0, wenn das Fahrzeug nicht lädt |
| Hinzugefügte Energie | `charge_energy_added` | Info / numerisch | kWh | nein | nein | Während der laufenden (oder der letzten) Ladesitzung zur Batterie hinzugefügte Energie; das Fahrzeug setzt sie bei jeder neuen Sitzung auf null zurück, ein negativer Wert wird ignoriert |
| Kumulierte Ladeenergie | `charge_energy_total` | Info / numerisch | kWh | ja | nein | Zähler, der nur ansteigt: Summe der Sitzungsenergien, vom Plugin berechnet (siehe [Ladeenergiezähler](#ladeenergiezahler)) |
| Ladestrom (A) | `charge_amps` | Info / numerisch | A | ja | ja | Konfigurierter Ladestrom |
| Angeforderter Ladestrom | `charge_current_request` | Info / numerisch | A | ja | ja | Vom Fahrzeug angeforderter Strom |
| Maximaler Ladestrom | `charge_current_request_max` | Info / numerisch | A | nein | nein | Maximaler Strom, den das Fahrzeug nach eigener Angabe von der Ladestation anfordern kann (dient als **Max** für den Schieberegler **Ladestrom**) |
| Ladezeit | `minutes_to_full_charge` | Info / Text | | nein | ja | Verbleibende Zeit bis zum Ende des Ladevorgangs im Format `HHhMM` |
| Verbleibende Ladezeit | `charge_minutes_remaining` | Info / numerisch | min | nein | nein | Dieselbe verbleibende Zeit in Minuten (verwendbar in einem Szenario oder einem Diagramm) |
| Ladeklappe geöffnet | `charge_port_door_state` | Info / binär | | nein | nein | 1, wenn die Ladeklappe offen ist, 0, wenn sie geschlossen ist |
| Ladeklappen-Verriegelung | `charge_port_latch` | Info / Text | | nein | nein | Zustand der Verriegelung des Ladekabels, wie vom Fahrzeug gemeldet |
| Ladekabel | `conn_charge_cable` | Info / Text | | nein | nein | Typ des angeschlossenen Kabels, wie vom Fahrzeug gemeldet, zum Beispiel `IEC` (Typ 2, Europa), `SAE` (Nordamerika), `GB_AC` oder `GB_DC` (China); `SNA`, wenn kein Kabel erkannt wird |
| Schnellladen | `fast_charger_present` | Info / binär | | nein | nein | 1, wenn das Fahrzeug an einer Schnellladestation angeschlossen ist |
| Modus geplantes Laden | `scheduled_charging_mode` | Info / Text | | nein | nein | Modus des geplanten Ladens, wie vom Fahrzeug gemeldet: `ScheduledChargingModeOff` (keine Planung), `ScheduledChargingModeStartAt` (verzögertes Laden) oder `ScheduledChargingModeDepartBy` (geplante Abfahrt) |
| Geplante Abfahrtszeit | `scheduled_departure_time` | Info / Text | | nein | nein | Geplante Abfahrtszeit im Format `HH:MM` (Fahrzeugzeit); leer, wenn keine Abfahrt geplant ist |
| Geplante Ladezeit | `scheduled_charging_start_time` | Info / Text | | nein | nein | Startzeit des verzögerten Ladens im Format `HH:MM` (Zeit von Jeedom); leer außerhalb des Modus für verzögertes Laden. Standardmäßig ausgeblendet |
| Ende der Niedertarifzeit | `off_peak_hours_end_time` | Info / Text | | nein | nein | Endzeit der Niedertarifzeit im Format `HH:MM`; nur im Modus geplante Abfahrt gefüllt, sonst leer oder wenn das Fahrzeug Mitternacht angibt. Standardmäßig ausgeblendet |
| Geplante Vorklimatisierung | `scheduled_preconditioning_time` | Info / Text | | nein | nein | Zielabfahrtszeit der Vorklimatisierung im Format `HH:MM`; im Modus geplante Abfahrt gefüllt, wenn die Vorklimatisierung aktiviert ist, sonst leer. Standardmäßig ausgeblendet |
| Innentemperatur | `inside_temp` | Info / numerisch | °C | ja | ja | Temperatur im Innenraum, auf ein Zehntelgrad genau |
| Außentemperatur | `outside_temp` | Info / numerisch | °C | ja | ja | Außentemperatur, auf ein Zehntelgrad genau |
| Temperatur Fahrer | `driver_temp_setting` | Info / numerisch | °C | nein | nein | Klimasollwert auf der Fahrerseite |
| Temperatur Beifahrer | `passenger_temp_setting` | Info / numerisch | °C | nein | nein | Klimasollwert auf der Beifahrerseite |
| Klimaanlage aktiviert | `is_climate_on` | Info / binär | | nein | nein | 1, wenn die Klimaanlage läuft |
| Sitzheizung Fahrer | `seat_heater_left` | Info / numerisch | | nein | nein | Heizstufe des Fahrersitzes (0 bis 3) |
| Sitzheizung Beifahrer | `seat_heater_right` | Info / numerisch | | nein | nein | Heizstufe des Beifahrersitzes (0 bis 3) |
| Lenkradheizung | `steering_wheel_heater` | Info / binär | | nein | nein | 1, wenn die Lenkradheizung aktiv ist |
| Enteisungsmodus | `defrost_mode` | Info / Text | | nein | nein | Zustand der Enteisung |
| Klimaautomatik | `is_auto_conditioning_on` | Info / binär | | nein | nein | 1, wenn die Klimaautomatik aktiv ist |
| Vorklimatisierung läuft | `is_preconditioning` | Info / binär | | nein | nein | 1 während einer Vorklimatisierung des Innenraums oder der Batterie (nicht zu verwechseln mit **Geplante Vorklimatisierung**, der programmierten Uhrzeit) |
| Enteisung vorne | `is_front_defroster_on` | Info / binär | | nein | nein | 1, wenn die Windschutzscheibenenteisung aktiv ist |
| Enteisung hinten | `is_rear_defroster_on` | Info / binär | | nein | nein | 1, wenn die Heckscheibenenteisung aktiv ist |
| Lüftergeschwindigkeit | `fan_status` | Info / numerisch | | nein | nein | Lüfterstufe, Rohwert des Fahrzeugs (von Tesla nicht dokumentierte Skala) |
| Klimahaltemodus (Hund, Camp) | `climate_keeper_mode` | Info / Text | | nein | nein | Modus des Klimahaltens, wie vom Fahrzeug gemeldet: `Off`, `On` (Halten), `Dog` (Hundemodus), `Party` (Campmodus), `Unknown` |
| Überhitzungsschutz | `cabin_overheat_protection` | Info / Text | | nein | nein | Schutz vor Überhitzung des Innenraums, wie vom Fahrzeug gemeldet: `CabinOverheatProtectionOff`, `CabinOverheatProtectionOn`, `CabinOverheatProtectionFanOnly` (nur Belüftung) |
| Sitzheizung hinten links | `seat_heater_rear_left` | Info / numerisch | | nein | nein | Heizstufe des Rücksitzes links (0 bis 3); auch 0, wenn das Fahrzeug nicht damit ausgestattet ist |
| Sitzheizung hinten rechts | `seat_heater_rear_right` | Info / numerisch | | nein | nein | Heizstufe des Rücksitzes rechts (0 bis 3); auch 0, wenn das Fahrzeug nicht damit ausgestattet ist |
| Sitzheizung hinten Mitte | `seat_heater_rear_center` | Info / numerisch | | nein | nein | Heizstufe des mittleren Rücksitzes (0 bis 3); auch 0, wenn das Fahrzeug nicht damit ausgestattet ist |
| Lenkradheizungsstufe | `steering_wheel_heat_level` | Info / numerisch | | nein | nein | Heizstufe des Lenkrads: **0 unbekannt, 1 aus, 2 niedrig, 3 hoch** (siehe den Hinweis weiter unten) |
| Min. einstellbare Temperatur | `min_avail_temp` | Info / numerisch | °C | nein | nein | Im Fahrzeug einstellbare Mindesttemperatur, auf ein Zehntel genau |
| Max. einstellbare Temperatur | `max_avail_temp` | Info / numerisch | °C | nein | nein | Im Fahrzeug einstellbare Höchsttemperatur, auf ein Zehntel genau |
| Batterieheizung | `battery_heater` | Info / binär | | nein | nein | 1, wenn die Batterieheizung aktiv ist |
| Letzter Fehler | `last_error` | Info / Text | | nein | ja | Ursache des letzten Fehlschlags beim Lesen oder bei einem Befehl, gefolgt vom Grund des Proxys, wenn er einen angibt; **Keine**, wenn alles in Ordnung ist. In einem Szenario verwendbar |
| Letzte Datenabfrage | `last_data_update` | Info / Text | | nein | ja | Datum und Uhrzeit (Zeit von Jeedom, `JJJJ-MM-TT HH:MM:SS`) der letzten erfolgreichen Abfrage der Lade- und Klimadaten |
| Alter der Daten (min) | `data_age` | Info / numerisch | min | nein | ja | Seit der **Letzten Datenabfrage** vergangene Minuten, jede Minute neu berechnet, ohne den Proxy abzufragen. Ist nach jeder erfolgreichen Abfrage 0 und steigt, solange keine Abfrage gelingt (Fahrzeug schläft, Proxy nicht erreichbar, Einschlaffenster). **99999** = keine Abfrage bekannt oder mehr als 69 Tage |
| Proxy erreichbar | `proxy_reachable` | Info / binär | | nein | ja | 1, wenn der Proxy im letzten Aktualisierungszyklus geantwortet hat, 0, wenn er ausgeschaltet oder nicht erreichbar ist, nicht rechtzeitig antwortet oder etwas anderes als eine gültige Proxy-Antwort sendet (falsche Adresse, zu alter Proxy). Ein Fahrzeug außer Reichweite oder im Schlaf setzt ihn nicht auf 0. In einem Szenario verwendbar |
| Proxy-Version | `proxy_version` | Info / Text | | nein | ja | Vom Proxy im letzten Zyklus gesendete Version (**unbekannt**, wenn sie unlesbar ist); behält ihren letzten Wert, wenn der Proxy nicht antwortet |
| Schlüsselrolle | `key_role` | Info / Text | | nein | ja | Wahrscheinliche Rolle des Proxy-Schlüssels für dieses Fahrzeug: **Charging Manager**, nachdem ein der Rolle Owner vorbehaltener Befehl mangels Rechten abgelehnt wurde, **Owner**, sobald einer dieser Befehle gelingt, **Unbestimmt**, solange noch keiner gesendet wurde (siehe [Schlüsselrolle](#rolle-des-schlussels)). Testen Sie in einem Szenario `Owner` oder `Charging Manager` (nie übersetzt); „Unbestimmt“ folgt der Sprache von Jeedom |
| Dauer Statusabfrage | `state_read_duration` | Info / numerisch | s | nein | ja | Zeit in Sekunden, auf ein Zehntel genau, der letzten erfolgreichen Abfrage des Fahrzeugstatus (Anwesenheit, Verriegelung, Schlaf) im Aktualisierungszyklus oder durch **Aktualisieren**. Ein Fehlschlag ändert sie nicht: Sie behält die Dauer des letzten Erfolgs. Historisieren Sie sie, um den Zustand der Bluetooth-Verbindung zu verfolgen (siehe [Langsame Abfrage des Proxys](#langsames-lesen-des-proxys)) |
| Dauer Datenabfrage | `data_read_duration` | Info / numerisch | s | nein | ja | Zeit der letzten erfolgreichen Abfrage der Lade- und Klimadaten. Unverändert, solange das Fahrzeug schläft (keine Abfrage). Ein Wert nahe 0 ist direkt nach einer anderen Abfrage normal: Der Proxy hält diese Daten 30 Sekunden im Speicher |
| Modell | `model` | Info / Text | | nein | ja | Aus der VIN dekodiertes Modell, ohne den Proxy abzufragen: **Model S**, **Model X**, **Model 3**, **Model Y**, **Cybertruck**, **Semi** oder **Roadster**; **Unbekannt**, wenn die VIN nicht zu einem erkannten Tesla gehört. Siehe [Erweiterte Daten: was verfügbar ist](#erweiterte-daten-was-verfugbar-ist) |
| Modelljahr | `model_year` | Info / Text | | nein | ja | Aus der VIN dekodiertes Modelljahr (zum Beispiel `2023`); **Unbekannt**, wenn es nicht dekodierbar ist |
| Kilometerstand | `odometer` | Info / numerisch | km | ja | ja | Kilometerzähler, in Kilometer umgerechnet (das Fahrzeug liefert ihn in Meilen). Nur erstellt, wenn der Proxy `drive_state` meldet |
| Gang | `shift_state` | Info / Text | | nein | nein | Eingelegter Gang: `P`, `R`, `N` oder `D`; **leer**, wenn das Fahrzeug ihn nicht mitteilt. Nur erstellt, wenn der Proxy `drive_state` meldet |
| Geschwindigkeit | `speed` | Info / numerisch | km/h | nein | nein | Geschwindigkeit, fahrzeugseitig in mph angenommen und in km/h umgerechnet (im realen Betrieb zu bestätigen). Nur erstellt, wenn der Proxy `drive_state` meldet |
| Leistung | `power` | Info / numerisch | kW | nein | nein | Momentanleistung, Wert des Fahrzeugs in Kilowatt, negativ möglich (im realen Betrieb zu bestätigen). Nur erstellt, wenn der Proxy `drive_state` meldet |
| Reifendruck vorne links | `tpms_pressure_fl` | Info / numerisch | bar | nein | ja | Reifendruck in bar, ohne Umrechnung. Nur erstellt, wenn der Proxy `tire_pressure` meldet |
| Reifendruck vorne rechts | `tpms_pressure_fr` | Info / numerisch | bar | nein | ja | Dito, Reifen vorne rechts |
| Reifendruck hinten links | `tpms_pressure_rl` | Info / numerisch | bar | nein | ja | Dito, Reifen hinten links |
| Reifendruck hinten rechts | `tpms_pressure_rr` | Info / numerisch | bar | nein | ja | Dito, Reifen hinten rechts |
| Software-Update | `software_update_status` | Info / Text | | nein | ja | **Keine**, **Verfügbar**, **Download läuft** oder **Installation läuft** (ein unerwarteter Status des Proxys wird unverändert angezeigt). Nur erstellt, wenn der Proxy `software_update` meldet |
| Vorgeschlagene Version | `software_update_version` | Info / Text | | nein | ja | Version des angebotenen Updates; **Keine** ohne Update, **Unbekannte**, wenn ein Update ohne gemeldete Version aktiv ist |
| Fortschritt | `software_update_progress` | Info / numerisch | % | nein | nein | Fortschritt des Downloads oder der Installation; 0 außerhalb dieser beiden Phasen |
| Breitengrad | `latitude` | Info / numerisch | ° | nein | nein | Breitengrad des Fahrzeugs in Dezimalgrad. **Ausgeblendet und nicht historisiert**: personenbezogene Daten (siehe [Position und Datenschutz](#position-und-datenschutz)). Nur erstellt, wenn der Proxy `location_data` meldet |
| Längengrad | `longitude` | Info / numerisch | ° | nein | nein | Längengrad des Fahrzeugs, gleiche Regeln wie beim Breitengrad |
| Zu Hause | `at_home` | Info / binär | | nein | ja | 1, wenn sich das Fahrzeug im Radius des Wohnorts befindet, 0 darüber hinaus; **nie geschrieben**, solange der Wohnort oder die Position unbekannt sind |

Die Info **Batterieladung** speist auch die Batterieüberwachung von Jeedom (Seite **Analyse > Geräte**); **Batteriestand (roh)** speist sie nicht.

Jede Lade- und Klimainfo wird unabhängig aktualisiert: Liefert das Fahrzeug eine davon nicht, behält sie ihren letzten Wert, und die anderen werden trotzdem aktualisiert.

**Erweiterte Ladeinfos.** Die zehn zusätzlichen Ladeinfos (**Ladestatus (übersetzt)**, **Nennreichweite**, **Geschätzte Reichweite**, **Batteriestand (roh)**, **Ladeleistung**, **Tatsächlicher Ladestrom**, **Ladephasen**, **Hinzugefügte Energie**, **Ladekabel** und **Schnellladen**) werden **ausgeblendet** erstellt, auch bei einem bestehenden Gerät während des Updates: Blenden Sie die gewünschten auf dem Reiter **Befehle** ein, Ihre Auswahl für Anzeige und Historisierung wird nie überschrieben. Sie bleiben leer bis zur ersten Datenabfrage eines wachen Fahrzeugs und behalten dann ihren letzten Wert, solange es schläft (siehe **Alter der Daten (min)**): Am Ende des Ladevorgangs können Leistung und tatsächlicher Strom also bis zur nächsten Abfrage auf ihrem letzten Wert bleiben. Die Einzelheiten jedes Ladezustands bleiben in **Ladestatus**.

**Öffnungen.** Die acht Öffnungsinfos (**Tür vorne Fahrer** bis **Tonneau-Abdeckung**) werden **ohne das Fahrzeug aufzuwecken** bei jeder Aktualisierung der Infos gelesen, wie Anwesenheit und Verriegelung. Ein Zustand, den das Fahrzeug nicht angeben kann (unbekannt, Entriegelung fehlgeschlagen), lässt den **letzten Wert** ohne Meldung bestehen. **Ladeklappe (Öffnung)** (auch bei schlafendem Fahrzeug gelesen) und **Ladeklappe geöffnet** (nur bei wachem Fahrzeug gelesen) können einige Augenblicke voneinander abweichen, auch direkt nach einem Befehl zum Öffnen oder Schließen der Klappe: Der Wert gleicht sich nach dem verzögerten erneuten Lesen an. Liefert das Fahrzeug den Zustand seiner Öffnungen überhaupt nicht, meldet der Proxy sie als geschlossen: Sie erscheinen dann als **geschlossen** (nur ein ausdrücklich unbekannter Zustand lässt den letzten Wert bestehen). Bei einem Proxy vor 2.3.0 ist ein Update des Proxys nötig: Die Öffnungen werden nicht veröffentlicht (siehe [Die Version des Proxys prüfen und aktualisieren](#die-version-des-proxys-prufen-und-aktualisieren)).

**Insasse und detaillierte Verriegelung.** Diese beiden Infos, **Insasse anwesend** und **Detaillierter Verriegelungsstatus**, werden **ohne das Fahrzeug aufzuwecken** bei jeder Aktualisierung der Infos gelesen, zusammen mit Anwesenheit und Verriegelung. Eine unbekannte Anwesenheit lässt den **letzten Wert** bestehen: Bei schlafendem Fahrzeug kann die Info eingefroren bleiben, verlassen Sie sich für die Sicherheit nicht allein darauf. Ein **von innen verriegeltes** Fahrzeug lässt **Fahrzeugverriegelung** auf 1. Nach einem Verriegelungsbefehl folgt der detaillierte Status, sobald das Fahrzeug bestätigt. Ein Verriegelungsstatus, den das Plugin nicht kennt, wird so angezeigt, wie das Fahrzeug ihn sendet. Verwechseln Sie **Insasse anwesend** nicht mit **Fahrzeug anwesend** (Fahrzeug in Bluetooth-Reichweite des Proxys). Bei einem Proxy vor 2.3.0 ist ein Update des Proxys nötig: Diese Infos werden nicht veröffentlicht (siehe [Die Version des Proxys prüfen und aktualisieren](#die-version-des-proxys-prufen-und-aktualisieren)).

**Im Fahrzeug gelesene Planungen.** Drei Text-Infos `HH:MM`, **ausgeblendet** erstellt, geben bei jeder Datenabfrage (auch bei der Abfrage „nur Laden“) die Planung des Fahrzeugs wieder: **Geplante Ladezeit** (Modus verzögertes Laden), **Ende der Niedertarifzeit** und **Geplante Vorklimatisierung** (Modus geplante Abfahrt). Im Modus **Off** oder außerhalb des betreffenden Modus sind sie **leer** (nie `00:00`): Testen Sie `== ""` in einem Szenario. Der Modus selbst bleibt unverändert in **Modus geplantes Laden**. Sie behalten ihren letzten Wert, solange das Fahrzeug schläft, und werden bei der ersten Abfrage nach der Deaktivierung der Planung geleert. Präzisierungen: Die **Ladezeit** wird in der Zeitzone von Jeedom angezeigt; **Ende der Niedertarifzeit** ist der Wert der Einstellung, ob die Option aktiv ist oder nicht, und bleibt leer, wenn das Fahrzeug Mitternacht angibt; **Geplante Vorklimatisierung** ist die Zielabfahrtszeit, auch an Tagen angezeigt, an denen die Planung nicht gilt; die betroffenen Tage und Planungen mit mehreren Zeitfenstern werden nicht gelesen. Ein unlesbarer Wert lässt die Info unverändert (Vermerk im Protokoll im Debug-Modus).

**Erweiterte Klimainfos.** Die vierzehn Infos oben, von **Klimaautomatik** bis **Batterieheizung**, werden **ausgeblendet** und nicht historisiert erstellt, auch bei einem bestehenden Gerät während des Updates: Blenden Sie die gewünschten auf dem Reiter **Befehle** ein, Ihre Auswahl wird nie überschrieben. Sie werden zusammen mit den Lade- und Klimadaten gelesen, ohne zusätzliche Anfrage und ohne je das Fahrzeug aufzuwecken: Sie behalten ihren letzten Wert, solange es schläft. Ein Feld, das das Fahrzeug nicht liefert, lässt die Info unverändert, ohne die Aktualisierung der anderen zu verhindern. Die Werte sind die des Fahrzeugs, ohne Umwandlung.

- **Skala der Lenkradheizung.** Achtung: Sie ist nicht die der Sitze. Es ist die Skala des Tesla-Protokolls: Ermitteln Sie die Werte an Ihrem Fahrzeug, bevor Sie sie in einem Szenario verwenden.

  | Wert | Bedeutung |
  |---|---|
  | 0 | unbekannt (oder Lenkrad nicht ausgestattet) |
  | 1 | aus |
  | 2 | niedrig |
  | 3 | hoch |

  **Ein Test „größer als 0“ ist also falsch**: Der Wert 1 bedeutet, dass die Heizung aus ist. Um zu wissen, ob das Lenkrad heizt, testen Sie `>= 2`. Die bestehende Info **Lenkradheizung** (`steering_wheel_heater`) bleibt der einfache Indikator aktiv / inaktiv. Bei den Sitzen ist 0 „aus“ und 3 „hoch“.
- **Fehlende Ausstattung.** Ein Rücksitz oder ein Lenkrad, das das Fahrzeug nicht hat, wird mit 0 gemeldet, wie eine ausgeschaltete Ausstattung: Die Info erlaubt es nicht, sie zu unterscheiden.
- **Min. und max. einstellbare Temperaturen.** Es sind die Einstellgrenzen der Klimaanlage des Fahrzeugs (zum Beispiel 15 und 28 °C). Ein fehlender, null oder außerhalb des Bereichs von 5 bis 40 °C liegender Wert wird ignoriert; ist das Minimum nicht strikt kleiner als das Maximum, werden beide ignoriert (Vermerk im Protokoll im Debug-Modus). Sie behalten dann ihren letzten Wert.
- **Batterieheizung.** Sie wird aus den Klimadaten des Fahrzeugs gelesen. Das entsprechende Feld der Ladedaten wird vom Proxy 2.3.0 nicht geliefert und bliebe immer auf 0: Es wird nicht verwendet.
- **Klimahaltemodus (Hund, Camp).** Mögliche Werte: `Off`, `On`, `Dog` (Hundemodus), `Party` (Campmodus), `Unknown`. Die Zuordnung von `Party` zum Campmodus ist an Ihrem Fahrzeug zu bestätigen. Ein unlesbarer Wert lässt die Info unverändert.
- **Überhitzungsschutz.** Mögliche Werte: `CabinOverheatProtectionOff`, `CabinOverheatProtectionOn`, `CabinOverheatProtectionFanOnly`. Ein Fahrzeug, das die Einstellung nicht meldet, wird als `CabinOverheatProtectionOff` gemeldet.
- **Lüftergeschwindigkeit.** Rohwert, dessen Skala nicht dokumentiert ist: Ermitteln Sie ihn an Ihrem Fahrzeug, bevor Sie ihn in einem Szenario verwenden.
- **Vorklimatisierung und Enteisungen.** Sie wechseln bei der Datenabfrage nach ihrer Auslösung auf 1; ein Zyklus findet nur statt, wenn das Fahrzeug wach ist, und der Proxy hält seine Daten 30 Sekunden im Speicher. Es ist keine durch das Ereignis ausgelöste Abfrage.

**Update des Plugins.** Die drei Planungsinfos werden bei jedem bestehenden Gerät **ausgeblendet** erstellt und bleiben leer bis zur ersten Datenabfrage eines wachen Fahrzeugs. Die Info **Kumulierte Ladeenergie** wird bei jedem bestehenden Gerät während des Updates **ausgeblendet** und **historisiert** erstellt. Sie bleibt leer bis zur ersten Datenabfrage eines wachen Fahrzeugs und beginnt dann bei 0: Die vor dem Update bereits geladene Energie wird nicht nachgeholt. Ebenso werden die Aktionen **Nach Überschuss anpassen**, **Ladeplan hinzufügen** und **Ladeplan löschen** bei jedem bestehenden Gerät **ausgeblendet** hinzugefügt; seine Einstellungen behalten ihre Standardwerte, solange Sie sie nicht ändern, und kein bestehender Befehl wird geändert. Die vierzehn erweiterten Klimainfos werden ebenfalls bei jedem bestehenden Gerät **ausgeblendet** erstellt, ohne eine bereits vorhandene Klimainfo zu ändern.

### Ladeenergiezähler

Um Ihren Ladeverbrauch zu verfolgen, führt das Plugin einen **Index, der nur ansteigt**: die Info **Kumulierte Ladeenergie** (kWh). Das Fahrzeug dagegen setzt **Hinzugefügte Energie** bei jeder neuen Ladesitzung auf null zurück; sie ist daher kein unmittelbar verwendbarer Zähler.

- **Er beginnt bei 0** bei der Erstellung der Info (Aktivierung der Funktion), ohne Nachholen des Verlaufs.
- **Berechnung per Differenz**: Bei jeder Datenabfrage addiert das Plugin zum Gesamtwert die seit der vorherigen Abfrage gewonnene Energie. Eine Sitzung, die unter **90 %** des zuvor gesehenen Werts fällt (Schwelle von 10 %), ist eine neue Sitzung: Sie wird vollständig addiert. Ein kleiner einzelner Rückgang wird ignoriert. Ein negativer, unlesbarer oder über 1000 kWh liegender Wert (als unplausibel eingestuft) wird ignoriert. Eine neue Sitzung, die schon bei der ersten Abfrage 90 % der vorherigen erreicht, wird zu niedrig gezählt.
- **Durch den Abfragetakt begrenzte Genauigkeit**: Das Plugin kennt die Energie nur zu den Zeitpunkten, an denen es die Daten liest, also nur bei wachem Fahrzeug und im eingestellten Takt (siehe [Beschleunigte Abfrage während des Ladens](#beschleunigtes-lesen-wahrend-des-ladens)). Ein ganzer Ladevorgang, der zwischen zwei Abfragen beginnt und endet, kann zu niedrig gezählt werden, und ein Ladevorgang außer Reichweite des Proxys wird bei der Rückkehr nur teilweise gezählt. Umgekehrt kann eine unplausible Abfrage manchmal dazu führen, dass Energie doppelt gezählt wird: Der Gesamtwert sinkt nie, ist aber nicht garantiert exakt.
- **Energie auf Batterieseite**: Es ist die zur Batterie hinzugefügte Energie, die unter der des Zählers oder der Ladestation liegt (Ladeverluste).
- **Energie-Plugin von Jeedom**: Deklarieren Sie **Kumulierte Ladeenergie** als Verbrauchsbefehl; grundsätzlich: absoluter Index, ohne „Verbrauch pro Tag“ anzukreuzen (je nach Version des Energie-Plugins zu prüfen).
- **Nie auf null zurückgesetzt** durch einen Klick auf **Speichern** oder durch ein Update des Plugins. Ein manuelles Zurücksetzen gibt es nicht. Das Löschen der Info setzt den Gesamtwert auf 0 zurück (sie wird bei der nächsten Speicherung leer neu erstellt); ein dupliziertes Gerät startet mit dem Gesamtwert des Originals.

### Aktionen

Die als „ausgeblendet“ gekennzeichneten Aktionen werden standardmäßig nicht im Widget angezeigt; machen Sie sie auf dem Reiter **Befehle** des Geräts sichtbar.

| Bezeichnung | Kennung | Typ / Untertyp | Einheit | Beschreibung |
|---|---|---|---|---|
| Aktualisieren | `refresh` | Aktion / andere | | Startet sofort das Lesen der Infos neu (ein eventueller Fehler erscheint in **Letzter Fehler**) |
| Aktualisieren (mit Aufwecken) | `refresh_wakeup` | Aktion / andere | | Weckt das Fahrzeug bei Bedarf auf, liest dann seine Lade- und Klimadaten und veröffentlicht sie, in einer einzigen Aktion (siehe [Aktualisieren mit Aufwecken](#aktualisieren-mit-aufwecken)). Nur eine Aktion von Ihnen oder aus einem Szenario kann das bewirken: Die regelmäßige Abfrage weckt das Fahrzeug nie auf |
| Aufwecken | `wake_up` | Aktion / andere | | Weckt das Fahrzeug auf, ohne seine Daten zu lesen. Vor einem Befehl unnötig: Der Proxy weckt das Fahrzeug selbst auf. Nach dem Befehl folgt ein erneutes Lesen ohne Aufwecken (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)); um sofort frische Werte zu erhalten, bevorzugen Sie **Aktualisieren (mit Aufwecken)** |
| Laden starten | `charge_start` | Aktion / andere | | Startet das Laden |
| Laden beenden | `charge_stop` | Aktion / andere | | Beendet das Laden |
| Ladestrom | `set_charging_amps` | Aktion / Schieberegler | A | Stellt den Ladestrom ein (ganze Zahl, zwischen Min und Max des Befehls; 0 bis 32 A, solange das Fahrzeug seine Grenze nicht veröffentlicht hat, danach sein maximaler Strom; stellen Sie das Max von Hand ein, um es festzulegen, oder starten Sie eine Abfrage mit Aufwecken, um die Grenzen zu aktualisieren) |
| Ladelimit | `set_charge_limit` | Aktion / Schieberegler | % | Stellt die Ladegrenze ein, zwischen Min und Max des Befehls (50 bis 100 %, solange das Fahrzeug seine Grenzen nicht veröffentlicht hat, danach seine Limits) |
| Nach Überschuss anpassen | `adjust_surplus` | Aktion / Schieberegler | W | Empfängt die **für das Laden verfügbare Leistung** (in Watt, **absoluter** Wert, keine Änderung) und entscheidet selbst, ob ein Befehl gesendet werden muss (siehe [Steuerung nach Überschuss](#uberschusssteuerung)). **Ausgeblendet** erstellt: Sie wird aus einem Szenario aufgerufen. |
| Ladeplan hinzufügen | `add_charge_schedule` | Aktion / Nachricht | | Erstellt oder ersetzt den von Jeedom verwalteten Ladeplan: Der **Titel** enthält die Tage (`lun,mar,mer,jeu,ven`), die **Nachricht** die Startzeit (`23:00`). **Fork-Proxy erforderlich**, Koordinaten von Jeedom eingetragen (siehe [Das Laden planen](#ladeplan-erstellen)). **Ausgeblendet** erstellt. |
| Ladeplan löschen | `remove_charge_schedule` | Aktion / andere | | Löscht den von Jeedom erstellten Plan; ohne Wirkung und ohne Fehler, wenn es keinen gibt. **Fork-Proxy erforderlich** (siehe [Das Laden planen](#ladeplan-erstellen)). **Ausgeblendet** erstellt. |
| Klimaanlage starten | `auto_conditioning_start` | Aktion / andere | | Startet die Vorklimatisierung |
| Klimaanlage stoppen | `auto_conditioning_stop` | Aktion / andere | | Stoppt die Vorklimatisierung |
| Sollwert Fahrer | `set_driver_temp` | Aktion / Schieberegler | °C | Stellt die gewünschte Temperatur auf der Fahrerseite von 15 bis 28 °C in Schritten von 0,5 °C ein; die Beifahrerseite behält ihren zuletzt gelesenen Wert. **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Den Temperatursollwert einstellen](#temperatursollwert-einstellen)). |
| Sollwert Beifahrer | `set_passenger_temp` | Aktion / Schieberegler | °C | Stellt die gewünschte Temperatur auf der Beifahrerseite von 15 bis 28 °C in Schritten von 0,5 °C ein; die Fahrerseite behält ihren zuletzt gelesenen Wert. **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Den Temperatursollwert einstellen](#temperatursollwert-einstellen)). |
| Sitzheizung vorne links einstellen | `set_seat_heater_left` | Aktion / Liste | | Stellt die Heizung des Sitzes vorne links ein: Aus, Niedrig, Mittel oder Hoch (0 bis 3). **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen)). |
| Sitzheizung vorne rechts einstellen | `set_seat_heater_right` | Aktion / Liste | | Stellt die Heizung des Sitzes vorne rechts ein: Aus, Niedrig, Mittel oder Hoch (0 bis 3). **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen)). |
| Sitzheizung hinten links einstellen | `set_seat_heater_rear_left` | Aktion / Liste | | Stellt die Heizung des Sitzes hinten links ein: Aus, Niedrig, Mittel oder Hoch (0 bis 3). **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen)). |
| Sitzheizung hinten rechts einstellen | `set_seat_heater_rear_right` | Aktion / Liste | | Stellt die Heizung des Sitzes hinten rechts ein: Aus, Niedrig, Mittel oder Hoch (0 bis 3). **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen)). |
| Sitzheizung hinten Mitte einstellen | `set_seat_heater_rear_center` | Aktion / Liste | | Stellt die Heizung des Sitzes hinten Mitte ein: Aus, Niedrig, Mittel oder Hoch (0 bis 3). **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen)). |
| Lenkradheizung einstellen | `set_steering_wheel_heater` | Aktion / Liste | | Schaltet die Lenkradheizung ein oder aus (Aus oder Ein, ohne Stufe). **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen)). |
| Maximale Enteisung | `set_preconditioning_max` | Aktion / Liste | | Aktiviert (Ein) oder beendet (Aus) die maximale Enteisung des Fahrzeugs; weckt das Fahrzeug auf und verbraucht Batterie. **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Maximale Enteisung](#maximale-enteisung)). |
| Klimahaltemodus | `set_climate_keeper_mode` | Aktion / Liste | | Wählt das Klimahalten: Aus (0), Halten (1), Hundemodus (2) oder Campmodus (3); weckt das Fahrzeug auf und verbraucht Batterie. **Fork-Proxy erforderlich**. **Ausgeblendet** erstellt (siehe [Hunde-, Camp- und Klimahaltemodus](#hundemodus-campmodus-und-klimahaltemodus)). |
| Ladeklappe öffnen | `charge_port_door_open` | Aktion / andere | | Öffnet die Ladeklappe (ausgeblendet) |
| Ladeklappe schließen | `charge_port_door_close` | Aktion / andere | | Schließt die Ladeklappe (ausgeblendet) |
| Lichter blinken lassen | `flash_lights` | Aktion / andere | | Lässt die Scheinwerfer blinken (ausgeblendet) |
| Hupen | `honk_horn` | Aktion / andere | | Betätigt die Hupe |
| Türen verriegeln | `door_lock` | Aktion / andere | | Verriegelt das Fahrzeug (ausgeblendet) |
| Türen entriegeln | `door_unlock` | Aktion / andere | | Entriegelt das Fahrzeug (ausgeblendet) |
| Kofferraum hinten öffnen | `open_trunk_rear` | Aktion / andere | | Öffnet den hinteren Kofferraum nach erneutem Lesen des Zustands: abgelehnt, wenn der Kofferraum als offen, in Bewegung oder unbekannt gelesen wird; weckt das Fahrzeug auf. **Fork-Proxy erforderlich**, Bestätigung wird verlangt. **Ausgeblendet** erstellt (siehe [Den hinteren Kofferraum und den Frunk öffnen](#kofferraum-hinten-und-frunk-offnen)). |
| Frunk öffnen | `open_trunk_front` | Aktion / andere | | Öffnet den vorderen Kofferraum; weckt das Fahrzeug auf. **Fork-Proxy erforderlich**, Bestätigung wird verlangt. **Ausgeblendet** erstellt (siehe [Den hinteren Kofferraum und den Frunk öffnen](#kofferraum-hinten-und-frunk-offnen)). |
| Wächter-Modus einstellen | `set_sentry_mode` | Aktion / Liste | | Aktiviert oder deaktiviert den Wächter-Modus (**Aktiviert** oder **Deaktiviert**) (ausgeblendet). Der Zustand wird in **Wächter-Modus** und **Herkunft des Wächter-Modus** gelesen (siehe [Status des Wächter-Modus](#zustand-des-wachter-modus)) |

## Anwendungsbeispiele

- **Solarladen**: Senden Sie in einem Szenario die verfügbare Leistung an **Nach Überschuss anpassen** (siehe das [Schritt-für-Schritt-Beispiel: Solarladen](#schritt-fur-schritt-beispiel-solarladen-mit-nach-uberschuss-anpassen) und [Überschusssteuerung](#uberschusssteuerung)).
- **Niedertarifzeit**: Aktivieren Sie **Laden zur Niedertarifzeit** des Geräts (Zeitraum, Ziel-SoC): Jeedom startet und beendet das Laden selbst (siehe die [Schritt-für-Schritt-Anleitung zur Einrichtung des Ladens zur Niedertarifzeit](#laden-zur-niedertarifzeit)). Ohne diese Funktion können Sie auch aus einem Szenario heraus **Laden starten** zu Beginn der Niedertarifzeit und **Laden beenden** an deren Ende auslösen.
- **Vorheizen**: Aktivieren Sie **Von Jeedom geplante Vorklimatisierung** des Geräts (Abfahrtszeit, Tage, Vorlauf): Jeedom startet und stoppt die Klimaanlage selbst (siehe das [Anwendungsbeispiel](#von-jeedom-geplante-vorklimatisierung)). Ohne diese Funktion können Sie auch aus einem Szenario heraus **Klimaanlage starten**, einige Minuten vor Ihrer Abfahrt.
- **Warnung**: Lassen Sie sich benachrichtigen, wenn **Fahrzeugverriegelung** abends auf 0 bleibt.
- **Verbindungsausfall**: Lassen Sie sich benachrichtigen, wenn **Letzter Fehler** auf etwas anderes als **Keine** wechselt (Proxy nicht erreichbar, Proxy ohne gekoppelten Schlüssel...). Ein schlafendes Fahrzeug löst sie nicht aus.
- **Aktualitätsprüfung**: Passen Sie den Ladestrom nur an, wenn die Daten weniger als 5 Minuten alt sind, sonst tun Sie nichts (siehe das Schritt-für-Schritt-Beispiel „nur auf aktuelle Daten reagieren“ weiter unten).
- **Kofferraum bleibt offen**: Aktivieren Sie die Warnung bei längerer Öffnung und lösen Sie eine Benachrichtigung aus (siehe das [Schritt-für-Schritt-Beispiel: gewarnt werden, wenn der Kofferraum offen bleibt](#schritt-fur-schritt-beispiel-gewarnt-werden-wenn-der-kofferraum-offen-bleibt)).

### Schritt-für-Schritt-Beispiel: Solarladen mit Nach Überschuss anpassen

Dieses Szenario sendet regelmäßig an **Nach Überschuss anpassen** die Leistung, die Ihre Solaranlage für das Laden aufbringen kann; das Plugin entscheidet selbst, ob der Strom tatsächlich geändert oder das Laden gestartet bzw. beendet werden muss (siehe [Überschusssteuerung](#uberschusssteuerung)).

**Voraussetzungen**

- Das Fahrzeug ist **angeschlossen** (sonst greift das Plugin nicht ein: **„Fahrzeug nicht angeschlossen: Anpassung nach Überschuss ignoriert“**).
- **Intervall während des Ladens** ist im Gerät auf **1 Minute** eingestellt: Die Steuerung entscheidet anhand des zuletzt gelesenen **Ladestatus**, also anhand der Aktualität der Lesevorgänge.
- Eine Messung Ihrer **Netzeinspeisung** in Watt (Zähler, Wechselrichter-Gateway) oder ersatzweise die **Ladeleistung** des Fahrzeugs.
- Die Aktion **Nach Überschuss anpassen** muss nicht sichtbar sein: Sie wird aus dem Szenario aufgerufen (der Schlüssel des Charging-Manager-Proxys genügt, siehe [Schlüsselrolle](#rolle-des-schlussels)).

**Ausgangseinstellungen.** Im Abschnitt **Überschusssteuerung** des Geräts übernehmen leere Felder diese Werte. Es sind **Richtwerte als Ausgangspunkt, die Sie an Ihrer Anlage prüfen müssen**: Bisher wurde keine Messung zu ihrer Bestätigung durchgeführt.

| Einstellung | Ausgangswert | Anpassen, wenn |
|---|---|---|
| **Netzspannung (V)** | 230 | Ihre Spannung zwischen Phase und Neutralleiter abweicht |
| **Phasen** | Einphasig | Ihre Ladestation **dreiphasig** ist: Wählen Sie Dreiphasig, sonst ist der Zielstrom dreimal zu hoch |
| **Anpassungsschritt (A)** | 1 | Sie weniger Schwankungen wünschen (größerer Schritt) |
| **Hysterese (A)** | 2 | sich der Strom zu oft ändert (größerer Wert) |
| **Mindestintervall zwischen Befehlen (s)** | 120 (mindestens 60) | das Fahrzeug zu stark beansprucht wird (größerer Wert) |
| **Minimaler Startstrom (A)** | 6 | Ihr Fahrzeug oder Ihre Ladestation einen höheren Strom zum Starten verlangt |
| **Abschaltschwelle (A)** | 5 (nie höher als der Start) | Sie früher oder später stoppen möchten |
| **Haltedauer vor dem Abschalten (s)** | 300 | vorüberziehende Wolken das Laden zu oft beenden (größerer Wert) |

**Szenario erstellen**

1. Öffnen Sie **Werkzeuge > Szenarien**, klicken Sie auf **Hinzufügen** und benennen Sie das Szenario, zum Beispiel „Tesla Solarladen“. Wählen Sie unter **Szenario-Modus** **Programmiert** und legen Sie eine Ausführung **alle 2 bis 5 Minuten** fest (zum Beispiel `*/2 * * * *` für alle 2 Minuten). Häufigere Aufrufe bringen nichts: Das Plugin ignoriert Aufrufe, die nichts bewirken.
2. Öffnen Sie den Reiter **Szenario**, klicken Sie auf **+ Block** und wählen Sie **Wenn/Dann/Sonst**.
3. Geben Sie unter **WENN** eine Aktualitätsprüfung ein, zum Beispiel `#[Garage][Tesla][Alter der Daten (min)]# <= 5` (siehe das [Schritt-für-Schritt-Beispiel: nur auf aktuelle Daten reagieren](#schritt-fur-schritt-beispiel-nur-auf-aktuelle-daten-reagieren)). Diese Prüfung ist **optional**.
4. Fügen Sie unter **DANN** eine **Aktion** zur Variablenzuweisung hinzu: Name `puissance_dispo`, Wert = **Netzeinspeisung + Ladeleistung**, in **Watt**. Zum Beispiel `#[Garage][Zähler][Netzeinspeisung]# + #[Garage][Tesla][Ladeleistung]# * 1000`.
5. Fügen Sie weiterhin unter **DANN** eine **Aktion** hinzu: den Befehl **Nach Überschuss anpassen** des Fahrzeugs, mit dem Wert `variable(puissance_dispo)` (Lesen der im vorherigen Schritt zugewiesenen Variable).
6. **Speichern Sie** und starten Sie das Szenario ein erstes Mal von Hand.

**Warum „Einspeisung + Ladeleistung“.** Der gesendete Wert ist die **absolute** Leistung, die das Fahrzeug aufnehmen kann. Die vom Zähler gemessene Einspeisung ist bereits um den Verbrauch des Fahrzeugs **vermindert**: Ohne Addition der aktuellen Ladeleistung würde der Sollwert bei jeder Anpassung wieder sinken. Wenn Ihr Zähler die Einspeisung mit negativem Vorzeichen liefert, korrigieren Sie das Vorzeichen, um positive Watt zu erhalten. Ein negativer Wert wird ohnehin auf 0 W gesetzt.

**Wenn die einzige Quelle die Ladeleistung des Fahrzeugs ist.** Sie wird in **Kilowatt** angegeben und oft **ganzzahlig**: Multiplizieren Sie mit 1000 (wie oben) und erwarten Sie einen groben Wert. Bevorzugen Sie, falls vorhanden, die Messung eines Zählers oder der Ladestation.

**Prüfen, ob es funktioniert.** Stellen Sie das Log des Plugins auf **Debug** (**Plugin-Konfiguration > Logs**) und starten Sie das Szenario: Jeder Aufruf schreibt eine Zeile **« pilotage selon le surplus : … W, courant calculé … A, cible … A, décision … (motif) »** (*Überschusssteuerung: … W, berechneter Strom … A, Ziel … A, Entscheidung … (Grund)*). Mögliche Entscheidungen sind unter anderem `set_charging_amps`, `charge_start`, `charge_stop`, `aucune` und `ignorer`; der Grund erklärt, warum (Hysterese, Mindestintervall, Strom bereits am Ziel...). Eine Enthaltung des Plugins erscheint auch unter **Letzter Fehler**.

**Was nachts geschieht.**

- Ohne Erzeugung sinkt die verfügbare Leistung auf **0 W**: Der berechnete Strom fällt unter die **Abschaltschwelle**, und das Laden wird **beendet**, sobald die **Haltedauer vor dem Abschalten** abgelaufen ist (standardmäßig 300 s). Am nächsten Tag startet es wieder, sobald der berechnete Strom den **Minimalen Startstrom** erreicht.
- Wenn Sie außerdem das [Laden zur Niedertarifzeit](#laden-zur-niedertarifzeit) verwenden, wird der Aufruf von **Nach Überschuss anpassen** **während des Zeitraums ignoriert** (ohne Fehler): Das Solar-Szenario beendet das Laden zur Niedertarifzeit also nicht. Außerhalb des Zeitraums übernimmt die Überschusssteuerung wieder.

### Schritt-für-Schritt-Beispiel: gewarnt werden, wenn der Proxy nicht erreichbar ist

Die Information **Proxy erreichbar** hat den Wert 1, solange der Proxy im Aktualisierungszyklus antwortet (sie wird bei jedem Durchlauf veröffentlicht, bei dem ein Fahrzeug dieses Proxys gelesen wird, gemäß seinem Intervall), und wechselt auf 0, wenn er ausgeschaltet oder nicht erreichbar ist oder nicht rechtzeitig antwortet. Ein Fahrzeug außer Reichweite oder im Schlaf setzt sie nicht auf 0. Erstellen Sie ein Szenario, das Sie warnt:

1. Öffnen Sie **Werkzeuge > Szenarien**, klicken Sie auf **Hinzufügen** und benennen Sie das Szenario, zum Beispiel „Tesla Proxy-Warnung“. Wählen Sie unter **Szenario-Modus** **Ausgelöst** (das Szenario startet, wenn sich sein Auslöser ändert).
2. Klicken Sie unter **Auslöser** auf **+ Auslöser** und wählen Sie den Befehl **Proxy erreichbar** Ihres Fahrzeugs. Er lautet `#[Objekt][Fahrzeug][Proxy erreichbar]#` (zum Beispiel `#[Garage][Tesla][Proxy erreichbar]#`). Bei mehreren Fahrzeugen oder mehreren Proxys fügen Sie **Proxy erreichbar** jedes Fahrzeugs hinzu.
3. Öffnen Sie den Reiter **Szenario**, klicken Sie auf **+ Block** und wählen Sie **Wenn/Dann/Sonst**.
4. Geben Sie im Feld **WENN** die Bedingung `#[Objekt][Fahrzeug][Proxy erreichbar]# == 0` ein (oder wählen Sie den Befehl mit der Auswahlschaltfläche und ergänzen Sie `== 0`).
5. Fügen Sie unter **DANN** eine **Aktion** hinzu: einen Benachrichtigungsbefehl Ihrer Installation (mobile App, Telegram, E-Mail…) oder den Befehl **Nachricht hinzufügen** der Nachrichtenzentrale von Jeedom. Geben Sie den Text ein, zum Beispiel „Der Tesla-Proxy antwortet nicht mehr: Prüfen Sie den Raspberry Pi in der Garage“.
6. Um auch über die Rückkehr informiert zu werden, fügen Sie unter **SONST** eine zweite Benachrichtigung hinzu, zum Beispiel „Der Tesla-Proxy antwortet wieder“.
7. **Speichern Sie** und testen Sie, indem Sie den Raspberry Pi ausschalten: Beim nächsten Lesevorgang (spätestens im kürzesten Intervall der Fahrzeuge dieses Proxys, standardmäßig 5 Minuten) wechselt **Proxy erreichbar** auf 0, und die Benachrichtigung wird versendet. Schalten Sie ihn wieder ein: Im nächsten Zyklus springt die Information zurück auf 1, und die Benachrichtigung über die Rückkehr wird versendet.

Das Szenario wird bei jeder Wertänderung ausgelöst, also beim Ausfall und bei der Rückkehr, nicht bei jedem Zyklus. Die genaue Ursache (Schlüssel, Reichweite, blockierter Adapter) finden Sie unter **Letzter Fehler**.

### Schritt-für-Schritt-Beispiel: nur auf aktuelle Daten reagieren

Die Information **Alter der Daten (min)** gibt die Anzahl der Minuten an, die seit dem letzten erfolgreichen Lesen der Lade- und Klimadaten vergangen sind. Sie ist direkt nach einem Lesevorgang 0 und steigt, solange kein Lesevorgang gelingt: Fahrzeug schläft, Einschlaffenster offen, Proxy nicht erreichbar. Sie hat den Wert **99999**, solange kein Lesevorgang bekannt ist (neues Gerät, Plugin gerade aktualisiert). Das folgende Szenario für eine Solarsteuerung passt den **Ladestrom** nur an, wenn dieser Wert aktuell ist:

1. Öffnen Sie **Werkzeuge > Szenarien**, klicken Sie auf **Hinzufügen** und benennen Sie das Szenario, zum Beispiel „Tesla Solarladen“. Wählen Sie unter **Szenario-Modus** **Programmiert** und legen Sie eine Ausführung alle 5 Minuten fest.
2. Öffnen Sie den Reiter **Szenario**, klicken Sie auf **+ Block** und wählen Sie **Wenn/Dann/Sonst**.
3. Geben Sie im Feld **WENN** die Bedingung `#[Objekt][Fahrzeug][Alter der Daten (min)]# <= 5` ein (zum Beispiel `#[Garage][Tesla][Alter der Daten (min)]# <= 5`), oder wählen Sie den Befehl mit der Auswahlschaltfläche und ergänzen Sie `<= 5`.
4. Fügen Sie unter **DANN** eine **Aktion** hinzu: den Befehl **Ladestrom** des Fahrzeugs, mit dem Wert, den Ihr Szenario aus der Solarerzeugung berechnet.
5. Lassen Sie unter **SONST** **nichts** stehen (der Ladestrom bleibt, wie er war), oder fügen Sie eine Benachrichtigung hinzu, zum Beispiel „Tesla-Daten zu alt: Ladestrom unverändert“.
6. **Speichern Sie** und stellen Sie dann **Intervall während des Ladens** im Gerät auf **1 Minute**: Während des Ladens beträgt das Alter der Daten höchstens 1 Minute, und die Bedingung ist wahr.

Warum **5**? Das ist das Standard-Aktualisierungsintervall: Darüber hinaus ist mindestens ein Lesevorgang ausgefallen. Passen Sie den Schwellenwert an Ihren Takt an (etwas mehr als das während des Ladens verwendete Intervall).

Warum **99999** hier gut ist: Solange kein Lesevorgang bekannt ist, ist die Bedingung `<= 5` **falsch**, das Szenario enthält sich und sendet keinen Strom. Es ist von Natur aus vorsichtig.

> **Achtung**
>
> Verwenden Sie **Alter der Daten (min)** **nicht** als **Auslöser** eines Szenarios im Modus **Ausgelöst**: Diese Information wird **jede Minute** neu berechnet und ändert sich daher ständig, das Szenario würde in einer Endlosschleife starten (und jedes Mal würde eine Benachrichtigung versendet).

**Variante: Warnung „Daten älter als 2 Stunden“.** Erstellen Sie ein Szenario im Modus **Programmiert** (zum Beispiel stündlich) mit der Bedingung `#[Objekt][Fahrzeug][Alter der Daten (min)]# >= 120 && #[Objekt][Fahrzeug][Alter der Daten (min)]# < 99999` und einer Benachrichtigung unter **DANN**. Die Grenze `< 99999` vermeidet einen Fehlalarm, wenn kein Lesevorgang bekannt ist; bevorzugen Sie `>= 120` gegenüber einer exakten Gleichheit (`== 120`), die nur eine Minute lang wahr ist und übersprungen werden kann. Ein Fahrzeug, das lange schläft, löst diese Warnung aus, ohne dass eine Störung vorliegt: Es handelt sich lediglich um eine Feststellung zur Aktualität. Um aktuelle Daten zu erhalten, starten Sie **Aktualisieren (mit Aufwecken)**.

### Schritt-für-Schritt-Beispiel: gewarnt werden, wenn der Kofferraum offen bleibt

Dieses Szenario warnt Sie, wenn eine Öffnung (Kofferraum hinten, Frunk, Tür, Ladeklappe) länger als 10 Minuten offen bleibt. Es beruht auf der Warnung bei längerer Öffnung (siehe [Warnungen bei längerer Öffnung](#warnungen-bei-langerer-offnung)); ein Charging-Manager-Schlüssel genügt, da es sich um Lesevorgänge handelt.

1. Öffnen Sie die Seite Ihres Fahrzeugs (**Plugins > Verbundene Objekte > Tesla BLE**) und gehen Sie zum Block **Warnungen bei längerer Öffnung**.
2. Aktivieren Sie unter **Offen gebliebene Öffnung** das Kontrollkästchen **Aktivieren** und geben Sie **Dauer bis zur Warnung (min)** ein: `10`. Die Dauer ist obligatorisch, von 1 bis 1440 Minuten.
3. **Speichern Sie**. Eine Fehlermeldung beim Speichern weist auf eine leere oder ungültige Dauer hin (siehe [Meldungen beim Speichern](#meldungen-beim-speichern)).
4. Öffnen Sie den Reiter **Befehle** und aktivieren Sie **Anzeigen** bei **Öffnungsalarm** (er ist standardmäßig ausgeblendet, aber bereits historisiert). **Speichern Sie**.
5. Öffnen Sie **Werkzeuge > Szenarien**, klicken Sie auf **Hinzufügen** und benennen Sie das Szenario, zum Beispiel „Alarm Kofferraum offen“. Wählen Sie unter **Szenario-Modus** **Ausgelöst**.
6. Fügen Sie unter **Auslöser** den Befehl **Öffnungsalarm** Ihres Fahrzeugs hinzu, zum Beispiel `#[Garage][Tesla][Öffnungsalarm]#`.
7. Fügen Sie im Reiter **Szenario** einen Block **Wenn/Dann/Sonst** mit der Bedingung `#[Garage][Tesla][Öffnungsalarm]# == 1` hinzu. Das Szenario startet auch bei der Rückkehr auf 0: Ohne diese Bedingung würden Sie beim Schließen benachrichtigt.
8. Fügen Sie unter **DANN** eine **Aktion** zur Benachrichtigung Ihrer Installation hinzu (mobile App, Telegram, E-Mail…) mit einem Text wie „Eine Öffnung des Tesla ist länger als 10 Minuten offen geblieben“. Die Nachrichtenzentrale von Jeedom erhält ihrerseits ohne jede Konfiguration eine Nachricht, die die Öffnung benennt.
9. **Speichern Sie** und testen Sie: Öffnen Sie den Kofferraum hinten von Hand und warten Sie die gewählte Dauer **plus zwei Aktualisierungsintervalle** ab (bis zu 20 Minuten bei 10 Minuten und dem Standardintervall von 5 Minuten). **Öffnungsalarm** wechselt auf 1, die Nachricht erscheint in der Nachrichtenzentrale, und die Benachrichtigung wird versendet.
10. Schließen Sie den Kofferraum: Beim nächsten Lesevorgang springt **Öffnungsalarm** zurück auf 0, und das Szenario startet, ohne zu benachrichtigen. Die Nachricht bleibt in der Nachrichtenzentrale: Löschen Sie sie.

Verfahren Sie bei einem unverriegelt zurückgelassenen Fahrzeug genauso mit **Fahrzeug ohne Insassen entriegelt** und der Information **Alarm entriegelt ohne Insassen**.

**Hinweise zur Insassenerkennung.** **Insasse anwesend** (`user_present`) hat den Wert 1, wenn das Fahrzeug eine Person an Bord erkennt.

- **Bedingung „niemand an Bord“.** Testen Sie in einem Szenario `#[Garage][Tesla][Insasse anwesend]# == 0` vor einer Aktion, die nur bei leerem Fahrzeug sinnvoll ist (zum Beispiel ein erneutes Verriegeln). Kombinieren Sie sie mit **Fahrzeugverriegelung** und testen Sie diese beiden Informationen statt der Bezeichnung **Detaillierter Verriegelungsstatus**, die sich mit der Sprache von Jeedom ändert.
- **Unbekannte Anwesenheit = letzter Wert.** Wenn das Fahrzeug den Zustand nicht meldet (es schläft), behält die Information ihren letzten Wert: Sie kann „niemand“ anzeigen, obwohl eine Person an Bord geblieben ist, oder umgekehrt. Prüfen Sie **Alter der Daten (min)**, wenn die Entscheidung wichtig ist.
- **Das ist keine Sicherheitsfunktion.** Verwenden Sie sie niemals zum Schutz einer Person oder eines Tieres (zum Beispiel um zu entscheiden, die Klimaanlage auszuschalten: Ein an Bord gebliebenes Kind oder Tier wird möglicherweise nicht erkannt). Verwechseln Sie sie nicht mit **Fahrzeug anwesend**, das nur besagt, dass sich das Fahrzeug in Bluetooth-Reichweite des Proxys befindet.

## Versionen, Sprachen und Support

### Stabile oder Beta-Version

Das Plugin wird im Jeedom-Market in zwei Versionen veröffentlicht: der **stabilen** (empfohlen) und der **Beta** (Release Candidate, der Neuerungen als Erstes erhält und Beta-Testern vorbehalten ist).

- **Installieren.** Öffnen Sie unter **Plugins > Plugin Management > Market** das Plugin **Tesla BLE** und klicken Sie auf **Installer stable** (*Stabile installieren*) oder **Installer beta** (*Beta installieren*). Der Market synchronisiert die Versionen jede Nacht: Eine Neuerung kann einen Tag brauchen, bis sie erscheint.
- **Wissen, was installiert ist.** Oben auf der Seite des Plugins folgt auf den Namen seine ID in Klammern, dann der Versionstyp (stable, beta).
- **Zur stabilen Version zurückkehren.** Klicken Sie auf derselben Seite auf **Installer stable** (*Stabile installieren*). Zeigt das **Cron**-Log von Jeedom danach jede Minute einen Fehler, siehe [Aufgabe des Aktualisierungszyklus](#aufgabe-des-aktualisierungszyklus).

> **WICHTIG**: Jeedom weist darauf hin, dass es wirklich nicht empfohlen wird, ein Beta-Plugin auf einem Jeedom ohne Beta zu installieren. Vermeiden Sie die Beta auf einem produktiven Jeedom.

### Das Changelog lesen

Das [Changelog](changelog.md) ist **einheitlich**: Es gilt für die stabile Version wie für die Beta. Die Einträge sind datiert, die neuesten stehen oben, und ihnen ist **Neu**, **Korrektur**, **Weiterentwicklung** oder **Dokumentation** vorangestellt.

Es wird vor der stabilen Version veröffentlicht: Ein aktueller Eintrag kann eine Neuerung beschreiben, die noch nur in der Beta verfügbar ist. Eine Aktualisierung des Plugins ohne Eintrag im Changelog betrifft nur die Dokumentation, eine Übersetzung oder Text.

### Verfügbare Sprachen

Die Oberfläche (Konfiguration, Gerät, Meldungen, Fahrzeug-Kachel und Namen der **angelegten** Befehle) und die Dokumentation gibt es auf Französisch, Englisch, Deutsch und Spanisch.

- **Oberfläche.** Sie folgt der **Sprache von Jeedom**: **Einstellungen > Systeme > Konfiguration**, Tab **Allgemein**, Feld **Sprache** (globale Einstellung von Jeedom). Ein nicht übersetzter Text wird auf Französisch angezeigt.
- **Bereits angelegte Befehle.** Sie behalten ihren Namen; zu den in einem Szenario verglichenen Bezeichnungen siehe [Status des Wächter-Modus](#zustand-des-wachter-modus).
- **Dokumentation.** Die Schaltfläche **Dokumentation** von Jeedom öffnet die französische Version. Um die Sprache zu wechseln, verwenden Sie die Auswahl der Dokumentationsseite (`https://jeedomdocs.decastro.fr/teslable/`, `/en/teslable/`, `/de/teslable/` oder `/es/teslable/`).

### Einen Fehler melden

Es gibt kein offizielles Thema für dieses Plugin. Eröffnen Sie ein Thema im Forum der Jeedom-Community (<https://community.jeedom.com>), in der Kategorie der Plugins, mit **Tesla BLE** im Titel. Geben Sie an:

- die Version des Plugins und seinen Kanal (stabil oder Beta);
- die Version von Jeedom und die von Debian;
- die Version und den Typ des Proxys (den von wimaha oder den Fork);
- einen Auszug des Logs **TeslaBLE** auf Stufe **Debug**.

Lesen Sie diese Angaben vor der Veröffentlichung noch einmal durch: Lassen Sie darin niemals Ihr Token, Ihre vollständige VIN oder eine IP-Adresse, die Sie nicht öffentlich machen möchten. Siehe [Die Logs des Proxys einsehen](#die-logs-des-proxys-einsehen).

## Bekannte Einschränkungen

- **Nach einem Befehl** werden nur das Ladelimit, der Ladestrom und die Verriegelung sofort aktualisiert. Die übrigen Informationen sind nach dem **geplanten erneuten Lesen** aktuell (standardmäßig 30 Sekunden, siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)) oder beim nächsten Lesevorgang, wenn der Proxy ausgelastet ist. Ist das Fahrzeug wieder eingeschlafen, bleiben die letzten Werte erhalten (kein Fehler, kein Aufwecken); außer Reichweite wechselt die Anwesenheit auf „Nein“; ist der Proxy nicht erreichbar, wird „Letzter Fehler“ befüllt.
- **Schlafendes Fahrzeug**: Die Lade- und Klimainformationen werden nur bei wachem Fahrzeug gelesen (das Plugin weckt es nie von selbst). Verwenden Sie **Aktualisieren (mit Aufwecken)**.
- **Einschlaffenster**: Während des Fensters sind die Lade- und Klimainformationen sowie die **Letzte Datenabfrage** eingefroren (Standarddauer 30 Minuten). Ein über die App gestartetes Laden oder Klimatisieren ohne sichtbare Zustandsänderung ohne Aufwecken wird erst beim Kontrolllesen erkannt. Deaktivieren Sie **Fahrzeug einschlafen lassen** im Gerät für einen vollständigen Lesevorgang bei jedem Durchlauf.
- **Charging-Manager-Schlüssel**: Verriegeln, Hupe, Lichter und Wächter-Modus werden vom Fahrzeug abgelehnt. Das Plugin erkennt dies (Information **Schlüsselrolle**), blendet diese Befehle im Dashboard aber nicht grau aus (siehe [Schlüsselrolle](#rolle-des-schlussels)).
- **Klimaanlage nur Laden**: Wenn **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden** steht, werden alle Klimainformationen (Temperaturen, Heizungen, Enteisung, Lüftung, Klimahaltemodus, aktive Klimaanlage usw.) nicht mehr aktualisiert und behalten ihren letzten Wert; die Klimabefehle bleiben verfügbar.
- **Ladeenergiezähler**: Seine Genauigkeit hängt vom Lesetakt ab, er kann ein kurzes oder außer Reichweite durchgeführtes Laden zu niedrig zählen und wird nicht auf null zurückgesetzt; er wird nur im Takt der Lesevorgänge gelesen, ein weiter Takt macht ihn also ungenauer (siehe [Ladeenergiezähler](#ladeenergiezahler)).
- **Überschusssteuerung**: Die Standardschwellen (Start 6 A, Stopp 5 A, Halten 300 s) sind mit Ihrem Fahrzeug zu prüfen; Referenz ist der **letzte von der Steuerung gesendete Sollwert** (eine konkurrierende manuelle Einstellung wird erst nach einer Abweichung über der Hysterese, einem Stopp oder einem Abstecken erkannt); ein Szenarioaufruf kann bis zu etwa 210 Sekunden warten; die Entscheidung beruht auf dem zuletzt gelesenen **Ladestatus**, also auf der Aktualität der Lesevorgänge (siehe [Beschleunigtes Lesen während des Ladens](#beschleunigtes-lesen-wahrend-des-ladens)).
- **Solarsteuerung: Bluetooth-Beanspruchung und Schlaf.** Während des Ladens ist das Fahrzeug ohnehin wach, doch die Überschusssteuerung beansprucht es: Bei **Intervall während des Ladens** von 1 Minute findet **jede Minute** ein Lesevorgang statt, **jeder tatsächlich gesendete Befehl weckt das Fahrzeug**, und **auf jeden erfolgreichen Befehl folgt ein erneutes Lesen** (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)). Ein Fahrzeug, das den ganzen Tag Befehle erhält, schläft daher kaum ein. Verteilen Sie die Aufrufe weiter (**Mindestintervall zwischen Befehlen**, Hysterese, Szenario alle 2 bis 5 Minuten). **Es werden keine Messungen zum Verschleiß der Bluetooth-Verbindung oder der Batterie veröffentlicht**: Leiten Sie daraus weder eine Garantie noch ein bezifferbares Risiko ab.
- **Laden zur Niedertarifzeit**: Die Entscheidung folgt dem Lesetakt (Stopp beim ungefähren Ziel-SoC ohne **Intervall während des Ladens**); ein schlafendes Fahrzeug wird nie gestoppt, und sein veröffentlichter Zustand kann veraltet sein; **Laden zu starten weckt das Fahrzeug**; ein Start, auf den kein Laden folgt, wird vor dem nächsten Zeitraum **nicht wiederholt** (ein einziger Start pro Anschließen); ein aus Jeedom während des Zeitraums gesendetes **Starten** oder **Beenden** setzt die Steuerung bis zum nächsten Zeitraum aus; ein Zeitraum, der in der bei der **Sommerzeitumstellung** übersprungenen Stunde beginnt, startet erst am Ende dieser Stunde, und eine in dieser Stunde ausgeführte manuelle Aktion kann ignoriert werden; nur ein Zeitraum pro Fahrzeug; die Frist von 2 Minuten zur Feststellung des Ergebnisses eines Befehls ist im realen Einsatz zu prüfen (siehe [Laden zur Niedertarifzeit](#laden-zur-niedertarifzeit)).
- **Von Jeedom geplante Vorklimatisierung**: Die (vermutete) Rolle Owner ist im realen Einsatz zu bestätigen; die Entscheidung folgt dem Lesetakt (Start und Stopp auf einige Minuten genau, nichts, wenn kein Lesevorgang in das Fenster fällt; ein Intervall von höchstens 5 Minuten wird empfohlen); **die Klimaanlage zu starten weckt das Fahrzeug** und verbraucht Batterie; ein als schlafend gesehenes Fahrzeug wird nie gestoppt; eine Klimaanlage, die beim ersten Lesen nach Ende des Fensters noch läuft, wird gestoppt, auch bei einem Insassen; das Deaktivieren der Funktion während des Fensters stoppt eine bereits gestartete Klimaanlage nicht; verwendet wird die bereits im Fahrzeug eingestellte Temperatur; nur ein Fenster pro Fahrzeug, die Programmierung des Fahrzeugs wird für die Entscheidung nicht gelesen; erfordert **Klimaanlage ebenfalls lesen** auf **Ja** (siehe [Von Jeedom geplante Vorklimatisierung](#von-jeedom-geplante-vorklimatisierung)).
- **Ladepläne**: **Geplante Ladezeit** setzt voraus, dass das Fahrzeug im Modus verzögertes Laden einen gültigen Zeitstempel über Bluetooth zurückgibt (im realen Einsatz zu bestätigen: sonst bleibt die Information leer); **Ende der Niedertarifzeit** wird auch veröffentlicht, wenn die Niedertarifoption deaktiviert ist (der Proxy übermittelt ihren Zustand nicht); die Anwendungstage und mehrere Zeiträume werden nicht gelesen.
- **Laden planen**: Nur dem Fork-Proxy vorbehalten (sofortige Ablehnung mit dem Proxy 2.3.0, dessen offizielle Version die Planungsroute nicht hat: Der Fork fügt sie hinzu, Versionen `2.3.0-tb.N`); nur ein von Jeedom verwalteter Ladeplan pro Fahrzeug, nur mit Startzeit; er folgt den Koordinaten von Jeedom, die dem Abstellort entsprechen müssen; die Zeit ist die des Fahrzeugs; das Ersetzen ohne Duplikat, die minimale Schlüsselrolle und die Aktualisierung der Planungsinformationen nach dem Befehl sind im realen Einsatz zu bestätigen (siehe [Laden planen](#ladeplan-erstellen)).
- **Temperatursollwert**: Nur dem Fork-Proxy vorbehalten (sofortige Ablehnung mit dem Proxy 2.3.0); beide Seiten werden immer zusammen gesendet, die andere Seite mit ihrem zuletzt gelesenen Wert (ein seit dem letzten Lesen am Fahrzeugbildschirm eingestellter Sollwert kann überschrieben werden); der Schieberegler ist auf 15 bis 28 °C in halben Graden begrenzt; die als nötig vermutete Rolle Owner und die Temperaturstufe (ein Sollwert, der nicht auf „HI“ wechselt) sind im realen Einsatz zu bestätigen (siehe [Temperatursollwert einstellen](#temperatursollwert-einstellen)).
- **Sitz- und Lenkradheizung**: Nur dem Fork-Proxy vorbehalten, mindestens Version `2.3.0-tb.2` (sofortige Ablehnung mit dem Proxy 2.3.0); die sechs Aktionen bleiben **ausgeblendet**: Blenden Sie sie nach dem Wechsel zum Fork selbst ein; keine Kopfstützen und keine dritte Reihe; Lenkrad nur Ein/Aus; das Verhalten bei ausgeschalteter Klimaanlage, bei fehlendem Sitz und bei einem Lenkrad mit automatischer Heizung ist im realen Einsatz zu prüfen.
- **Maximale Enteisung**: Nur dem Fork-Proxy vorbehalten, mindestens Version `2.3.0-tb.1` (sofortige Ablehnung mit dem Proxy 2.3.0); die Aktion bleibt **ausgeblendet**: Blenden Sie sie nach dem Wechsel zum Fork selbst ein; sie weckt das Fahrzeug, verbraucht Batterie und endet nicht von selbst; bei **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden** oder wenn das Fahrzeug wieder einschläft, behält **Enteisungsmodus** den optimistischen Wert (ein angezeigtes `Off` kann falsch sein, wenn das Fahrzeug `Normal` meldet); die Rolle Owner und das Verhalten beim Stopp (`Off` oder `Normal`) sind im realen Einsatz zu prüfen.
- **Hunde-, Camp- und Klimahaltemodus**: Nur dem Fork-Proxy vorbehalten, mindestens Version `2.3.0-tb.1` (sofortige Ablehnung mit dem Proxy 2.3.0); die Aktion bleibt **ausgeblendet**: Blenden Sie sie nach dem Wechsel zum Fork selbst ein; sie weckt das Fahrzeug, verbraucht über lange Zeit Batterie, endet nicht von selbst und ersetzt nicht die Temperaturüberwachung für ein Tier; bei **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden** oder wenn das Fahrzeug wieder einschläft, behält **Klimahaltemodus (Hund, Camp)** den angekündigten Wert; das Einschlaffenster öffnet sich nicht, solange ein Haltemodus (`On`, `Dog`, `Party`) gelesen wird; die Rolle Owner, der Name `Party` des Campmodus und der nach einem Stopp gelesene Wert sind im realen Einsatz zu prüfen.
- **Kofferraum hinten und Frunk öffnen**: Nur dem Fork-Proxy vorbehalten, mindestens Version `2.3.0-tb.2` (sofortige Ablehnung mit dem Proxy 2.3.0); die beiden Aktionen bleiben **ausgeblendet**: Blenden Sie sie nach dem Wechsel zum Fork selbst ein; sie wecken das Fahrzeug; der hintere Kofferraum wird nur geöffnet, wenn er als geschlossen gelesen wird (das erneute Lesen kann eine kürzliche Öffnung verpassen, und eine motorisierte Heckklappe kann sich dann wieder schließen); ein als „nicht gelöst“ gemeldeter Riegel (vorheriger Öffnungsfehler) wird als geschlossen behandelt und der Befehl erneut gesendet, Verhalten im realen Einsatz zu prüfen; der Frunk wird nicht erneut gelesen; das Plugin schließt nie einen Kofferraum; die als nötig vermutete Rolle Owner und das Verhalten bei einem motorisierten Kofferraum (oder motorisiertem Frunk) sind im realen Einsatz zu prüfen.
- **Status des Wächter-Modus**: Das tatsächliche Lesen erfordert den Fork-Proxy in Version `2.3.0-tb.2` oder höher und ein **waches** Fahrzeug; sonst folgt die Information dem **letzten von Jeedom gesendeten Befehl** und sieht weder eine über die App, den Fahrzeugbildschirm oder eine automatische Abschaltung vorgenommene Änderung noch einen an einem schlafenden Fahrzeug gelesenen Wert (der zuletzt gelesene Wert bleibt erhalten); der Zustand `Idle` zählt als **Aktiv** (im realen Einsatz zu bestätigen); die Bezeichnungen folgen der Sprache von Jeedom (siehe [Status des Wächter-Modus](#zustand-des-wachter-modus)).
- **Warnungen bei längerer Öffnung**: Die Dauer wird nur über erfolgreiche Lesevorgänge im Aktualisierungstakt gezählt (Warnung zwischen der Dauer und der Dauer plus zwei Intervallen). Wird der **Cache von Jeedom geleert**, während eine Warnung läuft, wird die Episode vergessen: Die Info springt auf 0 und nach einer vollen Dauer wieder auf 1, mit einer zweiten Nachricht. Ein eingefrorener **Ladestatus** an einem schlafenden Fahrzeug (zum Beispiel veraltetes „Stopped“ oder „Complete“ nach dem Abstecken) verdeckt eine offen vergessene Ladeklappe. Ohne die Öffnungsinformation des Fahrzeugs (acht geschlossene oder fehlende Zustände) gilt die Episode als beendet. Die Nachricht wird beim Schließen nicht aus der Nachrichtenzentrale entfernt.
- **Erweiterte Daten** (Modell, Kilometerstand und Fahrt, Reifen, Software-Update, Position): Mit Ausnahme von Modell und Baujahr erfordern sie den **Fork-Proxy** (mindestens `2.3.0-tb.2`), der sie **ankündigt**; sonst werden sie nicht erstellt. Sie werden nur bei **wachem Fahrzeug** in Bluetooth-Reichweite gelesen (Drücke, Update und Position höchstens alle 15 Minuten, nicht während eines Einschlaffensters). Die Einheiten von **Geschwindigkeit** (mph) und **Leistung** (kW) sind vermutet und im realen Einsatz zu bestätigen. **Zu Hause** ist binär: nie geschrieben ohne Zuhause oder Position (die Kachel zeigt vor der ersten Berechnung 0), sie springt nicht auf 0 zurück, wenn das Fahrzeug losfährt; testen Sie `== 1` mit **Fahrzeug anwesend**. Das `event`-Log von Jeedom speichert Breiten- und Längengrad auch dann, wenn sie ausgeblendet sind (siehe [Position und Datenschutz](#position-und-datenschutz)).
- **Widget und Anzeige**: Ein von Hand geleerter **generischer Typ** (**Keine**) kann neu gesetzt werden, wenn der Befehl gelöscht und neu erstellt wird oder wenn das Setzen der Typen nach einem unterbrochenen Update erneut ausgeführt wird (siehe [Generische Typen](#generische-typen)); ein mit **Bild entfernen** **entferntes Bild** wird **nie wieder gesetzt**, und keine Schaltfläche stellt das Bild des Plugins wieder her; die **Reihenfolge der Befehle** wird nur bei der Erstellung gesetzt und nie überschrieben; die Dauer **Daten von vor** der Kachel wird im Browser nicht fortgeschrieben; das **Standard-Widget** zeigt das Modellbild nicht an (siehe [Widget und Anzeige](#widget-und-anzeige)).
- **Nur ein Gerät pro Fahrzeug** (eindeutige VIN).
- **Historisierte geplante Abfahrtszeit**: Wurde sie vor dem Update historisiert, bleibt sie numerisch und wird nicht mehr aktualisiert, solange ihr Untertyp nicht auf **Andere** geändert wird.
- **Durch einen Docker-Dienstnamen deklarierter Proxy**: Der Link zum Dashboard öffnet sich nicht im Browser (siehe [Link zum Dashboard des Proxys](#link-zum-dashboard-des-proxys)).

### Zahlenmäßige Grenzen

| Grenze | Wert |
|---|---|
| Bluetooth-Geräte pro Fahrzeug | **3** gleichzeitig (Telefone, Uhr, Proxy). Darüber hinaus unterbrochene Verbindungen. |
| Fahrzeuge pro Proxy | **höchstens 3**, damit der Zyklus im ungünstigsten Fall nie verkürzt wird; darüber hinaus prüfen Sie die **Letzte Datenabfrage** jedes Fahrzeugs. |
| Dauer eines Zyklus | Wird **jede Minute** für fällige Fahrzeuge gestartet (standardmäßig 5 Minuten Intervall), höchstens 4 Minuten; er dauert so lange wie sein langsamster Proxy (die Proxys werden parallel gelesen). |
| Wartezeit auf einen ausgelasteten Proxy | Etwa 2 Minuten (110 Sekunden für einen Lesevorgang, 15 Sekunden für die Kopplungsprüfung), danach **Proxy ausgelastet**. |
| Schlüsselrolle | **Charging Manager** standardmäßig: nur Lesen und Laden, einschließlich Überschusssteuerung und Laden zur Niedertarifzeit; **Owner** für Verriegeln, Entriegeln, Hupe, Lichter, Wächter-Modus, Kofferräume (vermutet) und die geplante Vorklimatisierung (siehe [Schlüsselrolle](#rolle-des-schlussels)). |
| Authentifizierung des Proxys | **Standardmäßig keine**: Betreiben Sie ihn in einem vertrauenswürdigen Netzwerk, niemals aus dem Internet erreichbar. Der Fork-Proxy kann einen **API-Token** verlangen (optional, derselbe Token für alle Proxys), der den Zugriff schützt, aber ein vertrauenswürdiges Netzwerk nicht ersetzt. |
| Geräte pro Fahrzeug | Nur eines (eindeutige VIN). |
| Logs des Proxys | Proxy **2.3.0** mindestens; nur der Proxy der Plugin-Konfiguration wird angezeigt. |

## Fehlerbehebung

Stellen Sie das Log des Plugins auf die Stufe **Debug** (**Plugin-Konfiguration > Logs**), um jede aufgerufene URL und jede Antwort des Proxys zu sehen. Die Zeilen zu Beginn und am Ende einer Störung erfordern mindestens die Stufe **Info**.

Die Meldungen sind danach geordnet, wo Sie sie sehen.

### Meldungen der Schaltfläche Testen

| Meldung | Ursache | Maßnahme |
|---|---|---|
| **„Proxy-URL nicht angegeben“** | Das Feld ist leer. | Tragen Sie die Adresse des Proxys ein. |
| **„Ungültige URL: Sie muss mit http:// oder https:// beginnen…“** | Die Adresse ist falsch eingegeben (Schema fehlt, nicht zulässige Zeichen, ungültiger Port). | Korrigieren Sie sie, zum Beispiel `http://192.168.1.50:8080/`. Der abschließende `/` wird automatisch ergänzt. |
| **„Ungültige URL: Zugangsdaten (Benutzer:Passwort@) werden nicht unterstützt“** | Die Adresse enthält Zugangsdaten. | Entfernen Sie `Benutzer:Passwort@`: Der Proxy hat keine Authentifizierung. |
| **„Proxy erreichbar — Version X“** (grün) | Alles in Ordnung. | Nichts zu tun. |
| **„Proxy erreichbar — Version X“** + **„Proxy-Version nicht unterstützt: mindestens 2.3.0, aktualisieren Sie den Proxy“** (orange) | Der Proxy antwortet, aber seine Version ist zu alt. | Aktualisieren Sie ihn (siehe [Version des Proxys prüfen und aktualisieren](#die-version-des-proxys-prufen-und-aktualisieren)). |
| **„Proxy erreichbar — Version unbekannt“** (grün) | Der Proxy antwortet, liefert aber keine verwertbare Versionsnummer (zum Beispiel bei manueller Installation). | Prüfen Sie die Version von Hand mit der Adresse aus dem Tipp zu den Voraussetzungen. |
| **„Proxy-Version nicht mitgeteilt: Proxy älter als 2.1.3 oder falsche URL“** (orange) | Der Proxy antwortet auf die Versionsabfrage mit „nicht gefunden“. | Prüfen Sie Adresse und Port; aktualisieren Sie andernfalls den Proxy. |
| **„Proxy nicht erreichbar“** (rot, Detail `cURL …`) | Unter dieser Adresse antwortet nichts. | Prüfen Sie Adresse und Port, ob der Proxy gestartet ist und ob der Raspberry Pi eingeschaltet ist. |
| **„Zeitüberschreitung“** (rot) | Der Proxy antwortet nicht innerhalb von 10 Sekunden. | Prüfen Sie den Raspberry Pi (Stromversorgung, WLAN) und starten Sie den Proxy neu. |
| **„Ungültige Antwort des Proxys“** (rot) | Was antwortet, ist nicht TeslaBleHttpProxy (falscher Port, anderer Dienst). | Prüfen Sie Adresse und Port. |
| **„Keine Antwort vom Jeedom-Server: Siehe Log TeslaBLE“** | Jeedom hat den Test nach 45 Sekunden nicht beantwortet. | Versuchen Sie es erneut und sehen Sie dann im Log des Plugins nach. |
| **„Interner Plugin-Fehler: Siehe Log TeslaBLE“** | Unerwarteter Fehler des Plugins. | Sehen Sie im Log des Plugins nach und melden Sie den Fehler mit diesem Log. |

Der Test fragt nur die Version des Proxys ab: Ein grüner Test beweist weder, dass der Schlüssel gekoppelt ist, noch dass sich das Fahrzeug in Reichweite befindet. Verwenden Sie dafür die Schaltfläche **Kopplung prüfen** des Geräts (siehe [Meinen Schlüssel koppeln und die Kopplung prüfen](#meinen-schlussel-koppeln-und-die-kopplung-prufen)).

### Meldungen beim Speichern

- **„Ungültige URL: …“** (Plugin-Konfiguration oder Proxy-URL eines Fahrzeugs): dieselben Ursachen wie bei der Schaltfläche **Testen**. Die alte URL bleibt erhalten.
- **„Keine Proxy-URL konfiguriert: …“** (letzter Fehler eines Fahrzeugs oder Schaltfläche **Diesen Proxy testen**): Weder das Fahrzeug noch die Plugin-Konfiguration haben eine Proxy-URL. Tragen Sie eine der beiden ein.
- **„Ungültige VIN: 17 Zeichen erwartet, Ziffern und Buchstaben außer I, O und Q“**: Korrigieren Sie die VIN des Geräts (Leerzeichen werden automatisch entfernt).
- **„Diese VIN wird bereits vom Gerät … verwendet“**: Ein anderes Gerät trägt bereits diese VIN, was auch bei **Duplizieren** vorkommt. Löschen Sie das Duplikat oder korrigieren Sie die VIN.
- **„Laden zur Niedertarifzeit: Die Startzeit (oder Endzeit) muss im Format HH:MM sein, von 00:00 bis 23:59“**, **„… Der Ziel-SoC muss eine ganze Zahl zwischen 1 und 100 % sein“**, **„… Der Zeitraum ist leer, die Endzeit muss sich von der Startzeit unterscheiden“** und **„… Tragen Sie Startzeit, Endzeit und Ziel-SoC ein, um die Funktion zu aktivieren“**: Die Einstellung von **Laden zur Niedertarifzeit** ist ungültig; korrigieren Sie sie (es wurde nichts gespeichert).
- **„Überschusssteuerung: …“**: Die Einstellung der Überschusssteuerung liegt außerhalb der Grenzen (siehe [Überschusssteuerung](#uberschusssteuerung)).
- **„Geplante Vorklimatisierung: Die Abfahrtszeit muss im Format HH:MM sein, von 00:00 bis 23:59“**, **„… Der Vorlauf muss eine ganze Zahl zwischen 1 und 60 Minuten sein“**, **„… Die maximale Dauer muss eine ganze Zahl zwischen 1 und 120 Minuten sein“**, **„… Die maximale Dauer muss mindestens dem Vorlauf entsprechen“**, **„… Tragen Sie die Abfahrtszeit ein, um die Funktion zu aktivieren“**, **„… Wählen Sie mindestens einen Tag aus, um die Funktion zu aktivieren“** und **„… „Klimaanlage ebenfalls lesen“ muss auf Ja bleiben, um die Funktion zu aktivieren“**: Die Einstellung von **Von Jeedom geplante Vorklimatisierung** ist ungültig; korrigieren Sie sie (es wurde nichts gespeichert).
- **„Warnungen bei längerer Öffnung: Die Dauer bis zur Warnung … muss eine ganze Zahl zwischen 1 und 1440 Minuten sein, Pflichtangabe zum Aktivieren der Warnung“**: Die Dauer der Warnung (offen gebliebene Öffnung oder entriegeltes Fahrzeug ohne Insassen) ist leer, obwohl die Warnung aktiviert ist, oder keine ganze Zahl von 1 bis 1440 (siehe [Warnungen bei längerer Öffnung](#warnungen-bei-langerer-offnung)). Es wird nichts gespeichert.
- **„Ungültige Position des Zuhauses: Tragen Sie Breitengrad (von -90 bis 90) und Längengrad (von -180 bis 180) in Dezimalgrad mit höchstens 8 Nachkommastellen ein, oder lassen Sie beide leer, um die Position von Jeedom zu verwenden“**: Nur eine der beiden Koordinaten des Zuhauses ist angegeben, oder eine liegt außerhalb des Bereichs, ist nicht numerisch oder hat zu viele Nachkommastellen, oder das Paar lautet 0/0. Korrigieren Sie sie (oder leeren Sie beide Felder, um die Position von Jeedom zu verwenden); es wurde nichts gespeichert. Der eingegebene Wert wird nie in die Meldung übernommen (siehe [Position und Datenschutz](#position-und-datenschutz)).
- **„Ungültiger Radius des Zuhauses: ganze Zahl in Metern, von 10 bis 10000“**: Der **Radius (m)** ist keine ganze Zahl von 10 bis 10000. Korrigieren Sie ihn (oder leeren Sie das Feld für 100 m); es wurde nichts gespeichert.
- **„Interner Plugin-Fehler: Siehe Log TeslaBLE“**: Unerwarteter Fehler beim Speichern; die Details stehen im Log des Plugins.

### Nachrichtenzentrale von Jeedom (nach einem Update)

- **„Die VIN des Geräts … ist ungültig: Korrigieren Sie sie auf seiner Konfigurationsseite…“**: Die von einer älteren Version gespeicherte VIN ist nicht gültig. Korrigieren Sie sie.
- **„Das Gerät … hat dieselbe VIN wie das Gerät …“**: Zwei Geräte für ein und dasselbe Fahrzeug. Löschen Sie das Duplikat oder korrigieren Sie seine VIN.
- **„Die Information … wird historisiert: Sie bleibt numerisch und wird nicht mehr aktualisiert…“**: siehe [Geplante Abfahrtszeit](#geplante-abfahrtszeit).
- **„Bluetooth-Adapter des Proxys wahrscheinlich blockiert — …“**: siehe [Warnung bei blockiertem Bluetooth-Adapter](#warnung-bei-blockiertem-bluetooth-adapter). Starten Sie den Raspberry Pi neu.
- **„…: Öffnung „…“ seit mehr als … min geöffnet“** und **„…: Fahrzeug seit mehr als … min ohne Insassen entriegelt“**: Warnungen bei längerer Öffnung, eine Meldung pro Öffnung und pro Vorfall (siehe [Warnungen bei längerer Öffnung](#warnungen-bei-langerer-offnung)). Die Meldung wird beim Schließen nicht entfernt: Löschen Sie sie.

### Information „Letzter Fehler“ (Abfrage)

| Angezeigter Text | Ursache | Maßnahme |
|---|---|---|
| **Keine** | Der letzte Abfragezyklus war erfolgreich (oder das Fahrzeug schläft, was kein Fehler ist). | Nichts zu tun. |
| **Proxy nicht erreichbar** | Der Proxy antwortet nicht unter der konfigurierten Adresse. | Prüfen Sie die URL, ob der Proxy gestartet ist, sowie Stromversorgung und WLAN des Raspberry Pi. |
| **Zeitüberschreitung** | Der Proxy oder das Fahrzeug antwortet zu langsam. | Prüfen Sie den Raspberry Pi (Stromversorgung, WLAN) und starten Sie den Proxy neu, wenn es sich wiederholt. |
| **Bluetooth-Adapter des Proxys wahrscheinlich blockiert: Starten Sie den Raspberry Pi neu** | Mehrere Abfragen hintereinander haben ihre Zeitgrenze überschritten, obwohl der Proxy antwortet: siehe [Warnung bei blockiertem Bluetooth-Adapter](#warnung-bei-blockiertem-bluetooth-adapter). | Starten Sie den Raspberry Pi neu. |
| **Proxy ohne Schlüssel: Kopplung erforderlich — …** | Auf dem Proxy ist kein Schlüssel vorhanden: Er hat noch keinen erzeugt oder installiert. | Erzeugen Sie einen Schlüssel (**Generate**) im Dashboard des Proxys, senden Sie ihn an das Fahrzeug und bestätigen Sie mit der Schlüsselkarte (Link in der Plugin-Konfiguration oder unter **Meinen Schlüssel koppeln**). |
| **Fahrzeug außer Reichweite — …** | Der Proxy findet das Fahrzeug nicht per Bluetooth. Die **Fahrzeug anwesend** wechselt auf 0. | Bringen Sie den Raspberry Pi näher an das Fahrzeug; prüfen Sie, dass der Proxy das Bluetooth für sich allein hat und dass am Fahrzeug nicht bereits 3 Geräte verbunden sind. |
| **Fahrzeug nicht angeschlossen / Fahrzeug außerhalb der Reichweite des Proxys / Laden abgeschlossen / Die Ladestation liefert keinen Strom: Anpassung nach Überschuss ignoriert** oder **Ladezustand unbekannt: Starten Sie Aktualisieren (mit Aufwecken)** | Die Überschusssteuerung hat aus diesem Grund keinen Befehl gesendet (siehe [Überschusssteuerung](#uberschusssteuerung)). | Schließen Sie das Fahrzeug an, bringen Sie den Proxy näher, oder starten Sie **Aktualisieren (mit Aufwecken)** bei unbekanntem Zustand. |
| **Fahrzeug nicht angeschlossen / Die Ladestation liefert keinen Strom: Laden zur Niedertarifzeit wartet** (gegebenenfalls gefolgt von **(Zustand um HH:MM gelesen, Fahrzeug schläft)**) oder **Ladezustand unbekannt: Starten Sie Aktualisieren (mit Aufwecken)** | Das Laden zur Niedertarifzeit hat aus diesem Grund keinen Befehl gesendet. Zusatz „Fahrzeug schläft“: Der angezeigte Zustand stammt von der letzten Abfrage vor dem Einschlafen und kann veraltet sein. | Schließen Sie das Fahrzeug an, oder starten Sie **Aktualisieren (mit Aufwecken)** bei unbekanntem oder veraltetem Zustand (siehe [Laden zur Niedertarifzeit](#laden-zur-niedertarifzeit)). |
| **Laden zur Niedertarifzeit bis zum nächsten Zeitraum ausgesetzt: Laden außerhalb der Steuerung neu gestartet** | Das Laden wurde nach dem Stopp beim Ziel-SoC über die Tesla-App neu gestartet: Jeedom unterbricht es nicht mehr. | Nichts zu tun: Die Steuerung wird im nächsten Zeitraum fortgesetzt. |
| **Laden zur Niedertarifzeit bis zum nächsten Zeitraum ausgesetzt: Wiederholte Befehlsfehler** | Drei Befehle hintereinander sind fehlgeschlagen (siehe die Fehlermeldung des Befehls im Log, Warnung). | Beheben Sie die Ursache (Schlüssel, Reichweite, Proxy); ein Abziehen und erneutes Anschließen startet die Steuerung neu, sonst wird sie im nächsten Zeitraum fortgesetzt. |
| **Laden von Jeedom gestartet, aber gestoppt oder nicht gestartet: Kein neuer Versuch vor dem nächsten Zeitraum** | Ein von Jeedom gestartetes Laden wurde nicht festgestellt (aus der App gestoppt, Ladestation verweigert, Start zu langsam). Es wird **kein neuer Versuch** unternommen, um das Fahrzeug nicht in einer Schleife aufzuwecken. | Prüfen Sie Ladestation und Fahrzeug; starten Sie das Laden bei Bedarf von Hand (das setzt die Steuerung bis zum nächsten Zeitraum aus). |
| **Fahrzeug nicht angeschlossen: Geplante Vorklimatisierung nicht gestartet** (gegebenenfalls gefolgt von **(Zustand um HH:MM gelesen, Fahrzeug schläft)**) oder **Ladezustand unbekannt: Starten Sie Aktualisieren (mit Aufwecken)** | Mit der Option **Nur wenn angeschlossen** hat die geplante Vorklimatisierung die Klimaanlage aus diesem Grund nicht gestartet. Die Meldung zum unbekannten Zustand erscheint auch ohne die Option, wenn der Klimazustand des wachen Fahrzeugs unbekannt ist. | Schließen Sie das Fahrzeug an, deaktivieren Sie die Option, oder starten Sie **Aktualisieren (mit Aufwecken)** bei unbekanntem oder veraltetem Zustand (siehe [Von Jeedom geplante Vorklimatisierung](#von-jeedom-geplante-vorklimatisierung)). |
| **Geplante Vorklimatisierung bis zur nächsten Abfahrt ausgesetzt: Rolle Owner für den Proxy-Schlüssel erforderlich** | Das Fahrzeug hat **Klimaanlage starten** abgelehnt: Der Schlüssel des Proxys hat wahrscheinlich die Rolle Charging Manager. Pro Abfahrt wird nur ein Versuch unternommen. | Koppeln Sie einen **Owner**-Schlüssel (siehe [Rolle des Schlüssels](#rolle-des-schlussels)); die Steuerung wird bei der nächsten Abfahrt fortgesetzt. |
| **Geplante Vorklimatisierung bis zur nächsten Abfahrt ausgesetzt: Wiederholte Befehlsfehler** | Drei Befehle hintereinander sind fehlgeschlagen (siehe die Fehlermeldung des Befehls im Log, Warnung). | Beheben Sie die Ursache (Schlüssel, Reichweite, Proxy); die Steuerung wird bei der nächsten Abfahrt fortgesetzt. |
| **Anfrage vom Fahrzeug abgelehnt: Proxy-Schlüssel nicht mit diesem Fahrzeug gekoppelt** | Der aktive Schlüssel des Proxys ist nicht mit diesem Fahrzeug gekoppelt (bei mehreren Fahrzeugen muss derselbe Schlüssel bei jedem gekoppelt sein). Die anderen Fahrzeuge sind nicht betroffen. | Verwenden Sie **Meinen Schlüssel koppeln** und dann **Kopplung prüfen** am Gerät dieses Fahrzeugs. |
| **Anfrage vom Fahrzeug abgelehnt — …** | Das Fahrzeug hat die Abfrage abgelehnt; der Grund des Proxys folgt auf die Meldung. | Lesen Sie den nach der Meldung angegebenen Grund; prüfen Sie auch die Kopplung des Schlüssels. |
| **Funktion von diesem Proxy nicht unterstützt — …** | Die angeforderte Abfrage existiert in Ihrer Version des Proxys nicht (zum Beispiel der Kilometerstand `drive_state`, angefordert bei einem Proxy, der ihn ablehnt). | Aktualisieren Sie den Proxy (Fork-Proxy für die erweiterten Daten: siehe [Erweiterte Daten: was verfügbar ist](#erweiterte-daten-was-verfugbar-ist)). |
| **Ungültige Antwort des Proxys** | Der Proxy hat eine unerwartete Antwort geliefert. | Prüfen Sie die Adresse, aktualisieren Sie den Proxy und starten Sie ihn neu, wenn es sich wiederholt. |
| **Proxy-Version nicht unterstützt: mindestens 2.3.0, aktualisieren Sie den Proxy** | Der Proxy ist älter als 2.1.1: Der Fahrzeugzustand ist nicht mehr lesbar. | Aktualisieren Sie den Proxy (siehe [Version des Proxys prüfen und aktualisieren](#die-version-des-proxys-prufen-und-aktualisieren)). Das Log meldet diese Zeile auch als Fehler. |
| **Proxy ausgelastet: Fahrzeug nicht gelesen, versuchen Sie es gleich erneut** | Ein **Aktualisieren** hat mehr als 110 Sekunden gewartet: Der Proxy war durch einen Befehl oder eine Abfrage ausgelastet. Es hat keine Abfrage stattgefunden. | Starten Sie **Aktualisieren** gleich erneut; die nächste automatische Abfrage holt es ebenfalls nach. |
| **Aktualisierung mit Aufwecken fehlgeschlagen: …** | Der Befehl **Aktualisieren (mit Aufwecken)** ist fehlgeschlagen: Die Ursache (Fahrzeug außer Reichweite, Proxy nicht erreichbar, Fahrzeug, das sich nicht aufwecken lässt…) folgt auf die Meldung. Die Lade- und Klimainformationen behalten ihren letzten Wert (**Fahrzeug anwesend** wechselt auf 0, wenn das Fahrzeug außer Reichweite ist). | Lesen Sie die angegebene Ursache; bringen Sie den Raspberry Pi bei Bedarf näher an das Fahrzeug und starten Sie erneut. |
| **Zeitüberschreitung beim Aufwecken des Fahrzeugs: Es kann aufgewacht sein, versuchen Sie es gleich erneut** | Aufwecken und Abfrage haben 75 Sekunden überschritten. Das Fahrzeug kann dennoch aufgewacht sein. | Starten Sie **Aktualisieren (mit Aufwecken)** gleich erneut. |
| **Die VIN ist für dieses Gerät nicht konfiguriert** | Die VIN des Geräts ist leer. | Tragen Sie die VIN im Gerät ein und speichern Sie. |
| **Ungültige URL: …** | Die Proxy-URL in der Plugin-Konfiguration ist leer oder ungültig. | Tragen Sie sie ein (siehe [Plugin-Konfiguration](#konfiguration-des-plugins)). |

Der Text wird auf 127 Zeichen gekürzt. Ein schlafendes Fahrzeug ist kein Fehler: siehe [Aktualisierung der Informationen](#aktualisierung-der-informationen).

### Fehler beim Senden eines Befehls

Diese Meldungen erscheinen in Jeedom in Rot und werden auch in **Letzter Fehler** kopiert.

| Meldung | Ursache | Maßnahme |
|---|---|---|
| **„Dieser Befehl erfordert einen Schlüssel mit der Rolle Owner: Der Proxy-Schlüssel hat wahrscheinlich die Rolle Charging Manager…“** | Das Fahrzeug hat einen der Rolle Owner vorbehaltenen Befehl mangels Rechten abgelehnt (Verriegeln, Entriegeln, Hupe, Lichter, Wächter-Modus, Kofferräume, Klimaanlage): Ihr Schlüssel hat sehr wahrscheinlich die Rolle Charging Manager. | Siehe [Rolle des Schlüssels](#rolle-des-schlussels): Koppeln Sie einen Owner-Schlüssel. |
| **„Befehl vom Fahrzeug abgelehnt (Rolle des Proxy-Schlüssels unzureichend?): …“** | Autorisierungsfehler bei einem anderen Befehl: unzureichende Rolle des Schlüssels oder Fahrzeugzustand. | Siehe [Rolle des Schlüssels](#rolle-des-schlussels); prüfen Sie bei einem Owner-Schlüssel den Fahrzeugzustand. |
| **„Befehl vom Fahrzeug abgelehnt: …“** | Das Fahrzeug hat den Befehl abgelehnt; der zurückgegebene Grund folgt auf die Meldung. | Beheben Sie es entsprechend dem angegebenen Grund. |
| **„Proxy nicht erreichbar, Befehl nicht gesendet“** | Der Proxy antwortet nicht: Der Befehl wurde nicht gesendet. | Prüfen Sie die URL und die Stromversorgung des Raspberry Pi. |
| **„Zeitüberschreitung: Der Befehl wurde möglicherweise ausgeführt, prüfen Sie den Fahrzeugstatus“** oder **„Verbindung zum Proxy unterbrochen: Der Befehl wurde möglicherweise ausgeführt…“** | Das Fahrzeug hat den Befehl möglicherweise dennoch ausgeführt. | Kontrollieren Sie den Fahrzeugstatus, bevor Sie ihn erneut senden. |
| **„Proxy ausgelastet: Befehl nicht gesendet, versuchen Sie es gleich erneut“** | Ein anderer Befehl oder eine Abfrage belegt den Proxy seit fast 2 Minuten. | Versuchen Sie es erneut. |
| **„Kofferraum bereits offen oder in Bewegung: Befehl nicht gesendet“** | Vor dem Öffnen des hinteren Kofferraums hat das Plugin ihn als offen, angelehnt oder in Bewegung gelesen: Ein Umschaltbefehl würde ihn möglicherweise schließen. | Nichts zu tun: Schließen Sie den Kofferraum bei Bedarf und starten Sie die Aktion erneut (siehe [Hinteren Kofferraum und Frunk öffnen](#kofferraum-hinten-und-frunk-offnen)). |
| **„Kofferraumzustand unbekannt: Befehl nicht gesendet“** | Das Fahrzeug liefert keinen verwertbaren Zustand für den hinteren Kofferraum: Das Plugin sendet vorsichtshalber nichts. | Starten Sie **Aktualisieren** und dann die Aktion erneut; bleibt der Zustand unbekannt, öffnen Sie den Kofferraum von Hand. |
| **„Kofferraumzustand nicht lesbar, Befehl nicht gesendet: …“** | Das erneute Lesen des Zustands vor dem Öffnen ist fehlgeschlagen: Die Ursache folgt auf die Meldung. | Beheben Sie die Ursache (Proxy, Bluetooth-Reichweite) und starten Sie erneut. |
| **„Ungültiger Wert: Der Strom muss eine ganze Zahl zwischen … und … A sein“** | Der Strom ist dezimal, Text oder liegt außerhalb der Min/Max-Grenzen des Befehls. | Korrigieren Sie den Wert. Das **Max** folgt dem vom Fahrzeug gemeldeten maximalen Strom; um es höher festzusetzen, stellen Sie es von Hand ein (das Fahrzeug kann den Sollwert ablehnen). |
| **„Ungültiger Wert: Das Limit muss eine ganze Zahl zwischen X und Y % sein“** | Limit außerhalb der Grenzen des Befehls (die des Fahrzeugs, oder 50 bis 100 %, solange es keine veröffentlicht hat) oder keine ganze Zahl. | Korrigieren Sie den Wert. |
| **„Ungültiger Wert: Der Wächter-Modus muss aktiviert oder deaktiviert sein“** | Ein anderer Wert als **Aktiviert** oder **Deaktiviert** (die alte Option „Keine“ gibt es nicht mehr). | Verwenden Sie **Aktiviert** oder **Deaktiviert**. |
| **„Ungültiger Wert: Die Heizstufe muss eine ganze Zahl zwischen 0 und 3 sein“** oder **„Ungültiger Wert: Die Lenkradheizung muss 0 (Aus) oder 1 (Ein) sein“** | Ein Szenario sendet einen Wert außerhalb der Liste des Befehls für die Heizung eines Sitzes oder des Lenkrads. | Verwenden Sie die Stufen der Liste (siehe [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen)). |
| **„Ungültiger Wert: Die maximale Enteisung muss 0 (Aus) oder 1 (Ein) sein“** | Ein Szenario sendet einen Wert außerhalb der Liste des Befehls **Maximale Enteisung**. | Verwenden Sie 0 (Aus) oder 1 (Ein) (siehe [Maximale Enteisung](#maximale-enteisung)). |
| **„Ungültiger Wert: Der Klimahaltemodus muss 0 (Aus), 1 (Halten), 2 (Hund) oder 3 (Camp) sein“** | Ein Szenario sendet einen Wert außerhalb der Liste des Befehls **Klimahaltemodus**. | Verwenden Sie 0 (Aus), 1 (Halten), 2 (Hundemodus) oder 3 (Campmodus) (siehe [Hunde-, Camp- und Klimahaltemodus](#hundemodus-campmodus-und-klimahaltemodus)). |
| **„Befehl fehlgeschlagen: …“** | Andere Ursache (Proxy ohne Schlüssel, Fahrzeug außer Reichweite, ungültige Antwort…): Die Ursache folgt auf die Meldung. | Siehe die Tabelle **Letzter Fehler** oben. |
| **„Von Ihrer Proxy-Version nicht unterstützt“** | Der Befehl (zum Beispiel **Kofferraum hinten öffnen**, **Frunk öffnen**, **Ladeplan hinzufügen**, **Sollwert Fahrer**, **Sitzheizung vorne links einstellen**, **Maximale Enteisung** oder **Klimahaltemodus**) existiert in Ihrem Proxy nicht: Es wurde nichts gesendet. | Installieren Sie den Fork-Proxy (siehe [Laden planen](#ladeplan-erstellen), [Temperatur-Sollwert einstellen](#temperatursollwert-einstellen), [Sitze und Lenkrad heizen](#sitze-und-lenkrad-heizen), [Maximale Enteisung](#maximale-enteisung) und [Hunde-, Camp- und Klimahaltemodus](#hundemodus-campmodus-und-klimahaltemodus)). |
| **„Ungültiger Wert: Der Sollwert muss eine Zahl zwischen … und … °C sein“** | Der Wert von **Sollwert Fahrer** oder **Sollwert Beifahrer** ist keine Zahl oder liegt außerhalb des Bereichs des Schiebereglers (15 bis 28 °C, oder die Grenzen des Fahrzeugs). | Senden Sie eine Zahl im von der Meldung angegebenen Bereich. |
| **„Ungültige Tage des Ladeplans: …“** oder **„Ungültige Startzeit: …“** | Die Tage oder die Uhrzeit von **Ladeplan hinzufügen** haben nicht das erwartete Format. | Korrigieren Sie sie (`mon,tue,wed,thu,fri` ; `23:00`). |
| **„Koordinaten von Jeedom fehlen oder sind ungültig: …“** | Breiten- und Längengrad von Jeedom sind nicht angegeben (oder lauten 0 und 0). | Tragen Sie sie unter Einstellungen, Systeme, Konfiguration, Reiter **Allgemein** ein. |
| **„Ungültiger Wert: Die verfügbare Leistung muss eine Anzahl Watt sein“** | Der an **Nach Überschuss anpassen** gesendete Wert ist keine Zahl (Text, leere oder unbekannte Variable, fehlgeschlagene Berechnung). | Prüfen Sie den Wert des Szenarios: eine Anzahl Watt, zum Beispiel `1800`; ein negativer Wert wird auf 0 W zurückgesetzt (siehe [Überschusssteuerung](#uberschusssteuerung)). |
| **„Befehl vom Plugin nicht unterstützt“** | Der Befehl gehört nicht zu den Befehlen des Plugins (von Hand hinzugefügter Befehl oder geänderte Kennung). | Ändern Sie die Kennung der Befehle des Plugins nicht. |

### Aufgabe des Aktualisierungszyklus

Unter **Einstellungen > Systeme > Cron-System** startet die Aufgabe **TeslaBLE::cycleRafraichissement** (jede Minute, Zeitgrenze von 5 Minuten) die Aktualisierung der Fahrzeuge. Sie wird bei der Aktivierung und beim Update des Plugins erstellt und innerhalb einer Stunde wiederhergestellt, wenn sie gelöscht wurde; eine Aufgabe, die Sie selbst deaktivieren, bleibt deaktiviert.

- **Es wird kein Fahrzeug mehr aktualisiert**: Prüfen Sie, ob die Aufgabe existiert und aktiviert ist. Fehlt sie, **deaktivieren und reaktivieren Sie das Plugin**, um sie neu zu erstellen. Eine Fehlermeldung „Tâche de rafraîchissement non installée“ (*Aktualisierungsaufgabe nicht installiert*) im Log des Plugins meldet einen Fehler bei der Erstellung. Eine Meldung „Tâche de rafraîchissement non supprimée“ (*Aktualisierungsaufgabe nicht gelöscht*) bei der Deaktivierung des Plugins verlangt, **TeslaBLE::cycleRafraichissement** von Hand im Cron-System zu löschen.
- Das **Deaktivieren** des Plugins löscht die Aufgabe (sonst würde das Cron-System jede Minute einen Fehler protokollieren); das Reaktivieren erstellt sie neu. Ihre Geräte, Befehle und Einstellungen bleiben unberührt.
- **Rückkehr zu einer älteren Version des Plugins** (zum Beispiel von der Beta zur stabilen Version): Diese Version kennt die Aufgabe nicht, und das **Cron**-Log von Jeedom zeigt jede Minute einen Fehler „Classe ou fonction non trouvée“ (*Klasse oder Funktion nicht gefunden*). Löschen Sie dann die Aufgabe **TeslaBLE::cycleRafraichissement** von Hand im Cron-System.

### Einmalige Aufgaben zum erneuten Lesen

Unter **Einstellungen > Systeme > Cron-System** können Sie Aufgaben **TeslaBLE::relectureApresCommande** vorbeikommen sehen: eine pro erfolgreichem Befehl (siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl)). Sie löschen sich selbst, sobald das erneute Lesen erfolgt oder abgebrochen ist; berühren Sie sie nicht. Eine dort verbliebene Aufgabe (Jeedom wurde während des Wartens neu gestartet) wird vom nächsten erfolgreichen Befehl entfernt. Das **Deaktivieren** des Plugins entfernt alle diese Aufgaben. Eine Meldung „Tâches de relecture non supprimées“ (*Aufgaben zum erneuten Lesen nicht gelöscht*) im Log verlangt, sie von Hand zu löschen.

### Aufwecken und Takt

| Symptom | Ursache | Maßnahme |
|---|---|---|
| **Das Fahrzeug schläft nicht mehr ein** | Eine der folgenden Ursachen hält es wach: Das Kontrollkästchen **Fahrzeug einschlafen lassen** ist nicht gesetzt; die **Dauer des Zeitfensters** übersteigt das Aktualisierungsintervall nicht (das Fenster ist dann wirkungslos); ein Insasse oder ein Telefonschlüssel in der Nähe; ein laufendes Laden (das Fenster öffnet sich beim Laden nie); der Wächter-Modus; ein anderer Dienst, der das Fahrzeug abfragt (Tesla-App, evcc, andere Integration); ein sehr kurzes Intervall; ein Szenario, das **Aktualisieren (mit Aufwecken)** oder **Aufwecken** in einer Schleife startet. | Setzen Sie das Kontrollkästchen, wählen Sie eine Fensterdauer, die größer als das Intervall ist, verlängern Sie das Intervall, schalten Sie nach Möglichkeit den Wächter-Modus aus, prüfen Sie die Szenarien. Stellen Sie das Log auf **Info**: Die Zeile „fenêtre d'endormissement ouverte pour … min“ (*Einschlaffenster geöffnet für … min*) bestätigt, dass sich das Fenster öffnet; andernfalls hindert eines der obigen Kriterien es daran. Die Wirkung auf den Ruhezustand ist nicht garantiert: Sie hängt vom Fahrzeug ab. |
| **Die Lade- und Klimawerte ändern sich nachts nicht** | Das ist normal: Das Fahrzeug schläft (das Plugin weckt es nicht auf) oder das Einschlaffenster ist geöffnet. **Letzte Datenabfrage** bleibt eingefroren und **Alter der Daten (min)** steigt. **Letzter Fehler** bleibt bei **Keine**. | Nichts zu tun. Für sofort aktuelle Werte starten Sie **Aktualisieren (mit Aufwecken)** (es weckt das Fahrzeug auf). Wenn Sie dauerhafte Abfragen wünschen, deaktivieren Sie **Fahrzeug einschlafen lassen** und nehmen die Auswirkung auf die Batterie in Kauf. |
| **Der nach einem Befehl angezeigte Wert ist der alte** | Der Proxy hält seine Daten **30 Sekunden** im Cache: Das nach dem Befehl geplante erneute Lesen wartet diese Zeit ab. Weitere Ursachen: Der Proxy war ausgelastet (erneutes Lesen abgebrochen, die periodische Abfrage holt es nach), das Fahrzeug ist wieder eingeschlafen (die letzten Werte bleiben erhalten), der Cache des Proxys wurde über die **Verzögerung des erneuten Lesens nach Befehl** hinaus verlängert, oder das Cron-System von Jeedom ist deaktiviert. | Warten Sie 30 Sekunden. Ist der Cache Ihres Proxys länger, verlängern Sie die **Verzögerung des erneuten Lesens nach Befehl** entsprechend. Starten Sie sonst **Aktualisieren** (oder **Aktualisieren (mit Aufwecken)** bei einem schlafenden Fahrzeug). Siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl). |
| **„Aktualisierung mit Aufwecken fehlgeschlagen: …“** in **Letzter Fehler** | Die Ursache (Fahrzeug außer Reichweite, Proxy nicht erreichbar, Fahrzeug, das sich nicht aufwecken lässt…) folgt auf die Meldung. Die Werte behalten ihren letzten Stand. | Lesen Sie die Ursache, beheben Sie sie, starten Sie erneut. Siehe die Tabelle **Letzter Fehler** oben. |
| **„Zeitüberschreitung beim Aufwecken des Fahrzeugs: Es kann aufgewacht sein, versuchen Sie es gleich erneut“** | Aufwecken und Abfrage haben 75 Sekunden überschritten. | Starten Sie **Aktualisieren (mit Aufwecken)** gleich erneut. |
| **„Proxy ausgelastet: Fahrzeug nicht gelesen, versuchen Sie es gleich erneut“** | Der Proxy war mehr als 110 Sekunden durch einen Befehl oder eine Abfrage ausgelastet. | Starten Sie **Aktualisieren** (oder **Aktualisieren (mit Aufwecken)**) gleich erneut. |
| **Alter der Daten (min)** beträgt **99999** | Es ist keine erfolgreiche Datenabfrage bekannt (neues Gerät, aktualisiertes Plugin, Fahrzeug seit der Installation schlafend). | Starten Sie **Aktualisieren (mit Aufwecken)** ein erstes Mal; die Information wechselt auf 0. |
| **Das Intervall während des Ladens wird nicht eingehalten** | Die Beschleunigung beginnt erst bei der ersten Abfrage, die das Laden sieht; ein schlafendes Fahrzeug beim Laden, ein ausgesetztes Laden oder ein Proxy, dessen Cache 60 Sekunden überschreitet, begrenzen die Wirkung ebenfalls (siehe [Beschleunigte Abfrage während des Ladens](#beschleunigtes-lesen-wahrend-des-ladens)). | Warten Sie ein normales Intervall ab, oder starten Sie **Aktualisieren**. |

Die Warnungen des Logs zu diesen Einstellungen (Wert von **Intervall während des Ladens** auf 1 Minute zurückgesetzt oder deaktiviert, **Verzögerung des erneuten Lesens nach Befehl** auf 30 Sekunden zurückgesetzt, Zyklus länger als das eingestellte Intervall, Aktualisierungs- oder Leseaufgaben nicht installiert oder nicht gelöscht) sind unter [Meldungen des Plugin-Logs](#meldungen-des-plugin-logs) und [Aufgabe des Aktualisierungszyklus](#aufgabe-des-aktualisierungszyklus) beschrieben. Die **Info**-Zeilen zum Öffnen und Ende des Einschlaffensters sind unter [Fahrzeug einschlafen lassen](#fahrzeug-einschlafen-lassen) beschrieben.

### Meldungen des Plugin-Logs

- **„Cycle de rafraîchissement sauté : le cycle précédent n'est pas terminé.“** (*Aktualisierungszyklus übersprungen: Der vorherige Zyklus ist nicht beendet.*): Sie haben die Aufgabe von Hand gestartet (**Einstellungen > Systeme > Cron-System**), während ein Zyklus lief. Jeedom selbst startet eine laufende Aufgabe nie von sich aus neu (siehe die beiden folgenden Meldungen).
- **„… pilotage selon le surplus : … courant calculé N A, cible M A, décision `…` (motif)“** (*… Überschusssteuerung: … berechneter Strom N A, Ziel M A, Entscheidung `…` (Grund)*) (Debug): das Detail jedes Aufrufs von **Nach Überschuss anpassen** (keine VIN); **„appel ignoré, un ajustement est déjà en cours“** (*Aufruf ignoriert, eine Anpassung läuft bereits*): Ein anderer Aufruf desselben Fahrzeugs war nicht beendet. **„pilotage selon le surplus impossible, aucune commande envoyée : …“** (*Überschusssteuerung unmöglich, kein Befehl gesendet: …*) (Warnung, höchstens einmal pro Stunde): interne Störung vor dem Senden, zum Beispiel des Caches von Jeedom; das Szenario wird nicht unterbrochen.
- **„… charge aux heures creuses : décision `…` (motif)“** (*… Laden zur Niedertarifzeit: Entscheidung `…` (Grund)*) (Info bei Änderung des Grundes, danach Debug; keine VIN): was das Plugin nach der Abfrage entschieden hat (`charge_start`, `charge_stop`, `aucune` oder `ignorer`, mit dem Grund: `demarrage`, `cible_atteinte`, `fin_plage`, `en_charge`, `charge_perimee`, `limite_vehicule`, `suspendue_manuel`…). **„commande `…` en échec (N sur 3)“** (*Befehl `…` fehlgeschlagen (N von 3)*) (Warnung beim ersten Fehler und bei der Aussetzung); **„commande `…` reportée au prochain passage (proxy occupé | budget du cycle atteint)“** (*Befehl `…` auf den nächsten Durchlauf verschoben (Proxy ausgelastet | Zyklusbudget erreicht)*) (Warnung, höchstens einmal pro Stunde): Es wurde nichts gesendet, das Plugin versucht es bei der nächsten Abfrage erneut; **„pilotage impossible, aucune commande envoyée : …“** (*Steuerung unmöglich, kein Befehl gesendet: …*) (Warnung, höchstens einmal pro Stunde): interne Störung vor dem Senden, zum Beispiel des Caches von Jeedom.
- **„Cycle de rafraîchissement de N s, plus long que l'intervalle de rafraîchissement le plus court (M min) : Jeedom a sauté le passage suivant…“** (*Aktualisierungszyklus von N s, länger als das kürzeste Aktualisierungsintervall (M min): Jeedom hat den nächsten Durchlauf übersprungen…*) (Warnung, höchstens einmal pro Stunde): Ein Zyklus hat länger gedauert als das eingestellte Intervall, in der Regel weil der Proxy oder der Raspberry Pi langsam antwortet; der eingestellte Takt wird nicht eingehalten. Verlängern Sie das Intervall des betroffenen Fahrzeugs (oder sein Intervall während des Ladens), verteilen Sie die Fahrzeuge auf mehrere Proxys, oder prüfen Sie Stromversorgung und WLAN-Verbindung des Raspberry Pi.
- **„Cycle de rafraîchissement de N s : Jeedom a sauté le passage de la minute suivante, sans cumul de cycles.“** (*Aktualisierungszyklus von N s: Jeedom hat den Durchlauf der nächsten Minute übersprungen, ohne Zyklusanhäufung.*) (Debug): Ein Zyklus hat eine Minute überschritten, obwohl alle eingestellten Intervalle länger sind; nichts zu tun.
- **„Cycle de rafraîchissement écourté… véhicule(s) non lu(s) à ce cycle“** (*Aktualisierungszyklus verkürzt… Fahrzeug(e) in diesem Zyklus nicht gelesen*): Der Zyklus hat seine maximale Dauer von 4 Minuten erreicht; die genannten Fahrzeuge wurden in diesem Zyklus nicht gelesen. Sie werden im nächsten Zyklus gelesen, wenn der Proxy normal antwortet; bis zu 3 Fahrzeuge pro Proxy wird der Zyklus nicht verkürzt, darüber hinaus prüfen Sie die **Letzte Datenabfrage** jedes Fahrzeugs. Die Warnung wird nur **einmal pro Vorfall** ausgegeben (sie nennt „Avertissement non répété jusqu'au prochain cycle complet.“ (*Warnung wird bis zum nächsten vollständigen Zyklus nicht wiederholt.*)), selbst wenn der Vorfall mehrere Stunden dauert; wiederholt es sich, antwortet der Proxy zu langsam: siehe oben.
- **„Cycle de rafraîchissement de nouveau complet : …“** (*Aktualisierungszyklus wieder vollständig: …*) (Info): Ende eines Vorfalls mit verkürztem Zyklus; alle Fahrzeuge wurden gelesen.
- **„Véhicule … traité en … s.“** (*Fahrzeug … in … s verarbeitet.*) (Debug): Dauer der Abfrage jedes Fahrzeugs im Zyklus, einschließlich eines übersprungenen Fahrzeugs (Proxy ausgelastet, die Zeile „sautée“ geht voraus) oder eines Fahrzeugs mit Fehler. Die Zeilen **Requête** (*Anfrage*) und **Réponse HTTP … en … ms** (*HTTP-Antwort … in … ms*) geben die Details der Aufrufe an; die Zeile Réponse nennt ihre Anfrage (Methode und Adresse) erneut, da sich die Zeilen mehrerer parallel gelesener Proxys im Log vermischen.
- **„Lecture du véhicule … reportée : proxy occupé…“** (*Abfrage des Fahrzeugs … verschoben: Proxy ausgelastet…*): Ein **Aktualisieren** hat mehr als 110 Sekunden auf einen durch einen Befehl oder eine Abfrage ausgelasteten Proxy gewartet; die Abfrage hat nicht stattgefunden, und die Meldung **Proxy ausgelastet: Fahrzeug nicht gelesen…** erscheint in **Letzter Fehler**.
- **„Lecture du véhicule … sautée : une commande ou une lecture est en cours vers le proxy.“** (*Abfrage des Fahrzeugs … übersprungen: Ein Befehl oder eine Abfrage läuft zum Proxy.*) (Debug): Der automatische Zyklus weicht dem laufenden Austausch aus; die Abfrage erfolgt im nächsten Zyklus.
- **„Proxy obtenu pour le véhicule … après … s d'attente…“** (*Proxy für das Fahrzeug … nach … s Wartezeit erhalten…*) (Debug): Ein Befehl oder eine Abfrage hat mindestens eine Sekunde auf den Proxy gewartet.
- **„Verrou du proxy indisponible…“** (*Sperre des Proxys nicht verfügbar…*) oder **„Verrou du cycle de rafraîchissement indisponible…“** (*Sperre des Aktualisierungszyklus nicht verfügbar…*): Das Plugin kann nicht in das temporäre Verzeichnis von Jeedom schreiben. Prüfen Sie die Rechte dieses Verzeichnisses; das Plugin funktioniert ohne den Schutz vor gleichzeitigen Zugriffen weiter.
- **„Commandes : … le nom … est déjà pris…“** (*Befehle: … der Name … ist bereits vergeben…*): Das Plugin konnte einem Befehl die vorgesehene Bezeichnung nicht geben, weil ein anderer Befehl des Geräts sie trägt. Benennen Sie einen der beiden um und speichern Sie dann das Gerät.
- **„Adaptateur Bluetooth du proxy probablement figé pour le véhicule …“** (*Bluetooth-Adapter des Proxys wahrscheinlich blockiert für das Fahrzeug …*) (Warnung) und **„Adaptateur Bluetooth du proxy de nouveau opérationnel pour le véhicule …“** (*Bluetooth-Adapter des Proxys wieder betriebsbereit für das Fahrzeug …*) (Info): Beginn und Ende eines Vorfalls, siehe [Warnung bei blockiertem Bluetooth-Adapter](#warnung-bei-blockiertem-bluetooth-adapter).
- **„Véhicule … : fenêtre d'endormissement ouverte pour … min après … lecture(s) inchangée(s), hors charge…“** (*Fahrzeug …: Einschlaffenster geöffnet für … min nach … unveränderten Abfrage(n), außerhalb des Ladens…*) (Info): Das Plugin hört auf, die Lade- und Klimadaten bis zur angegebenen Uhrzeit abzufragen; siehe [Fahrzeug einschlafen lassen](#fahrzeug-einschlafen-lassen). **„fin de la fenêtre d'endormissement après … min : …“** (*Ende des Einschlaffensters nach … min: …*) (Info) nennt den Grund der Wiederaufnahme (festgestellte Aktivität mit dem geänderten Feld, Befehl, angeforderte Aktualisierung, deaktivierte Einstellung, abgelaufene Dauer, Fahrzeug außer Reichweite); **„… : véhicule endormi après … min de fenêtre.“** (*…: Fahrzeug nach … min Fenster eingeschlafen.*) meldet, dass das Fahrzeug eingeschlafen ist. Im Debug: „lecture des données suspendue“ (*Datenabfrage ausgesetzt*), „lecture de contrôle“ (*Kontrollabfrage*), „prolongée“ (*verlängert*).
- **„Véhicule … en charge (Charging), intervalle pendant la charge appliqué : N min au lieu de M.“** (*Fahrzeug … lädt (Charging), Intervall während des Ladens angewendet: N min statt M.*) und **„Véhicule … : état de charge …, intervalle normal rétabli : M min.“** (*Fahrzeug …: Ladezustand …, normales Intervall wiederhergestellt: M min.*) (Debug): Beginn und Ende der beschleunigten Abfrage, siehe [Beschleunigte Abfrage während des Ladens](#beschleunigtes-lesen-wahrend-des-ladens). Eine **Warnung** „intervalle pendant la charge inférieur au plancher d'une minute“ (*Intervall während des Ladens unter der Untergrenze von einer Minute*) oder „… invalide, réglage désactivé“ (*… ungültig, Einstellung deaktiviert*) meldet einen beim Speichern korrigierten Wert.
- **„Véhicule … : relecture programmée dans N s (commande …).“** (*Fahrzeug …: erneutes Lesen in N s geplant (Befehl …).*), **„… : lecture sans réveil.“** (*…: Abfrage ohne Aufwecken.*), **„Relecture du véhicule … remplacée par une commande plus récente.“** (*Erneutes Lesen des Fahrzeugs … durch einen neueren Befehl ersetzt.*), **„… abandonnée : proxy occupé…“** (*… abgebrochen: Proxy ausgelastet…*) und **„Relecture ignorée : …“** (*Erneutes Lesen ignoriert: …*) (Debug): Ablauf eines erneuten Lesens nach einem Befehl, siehe [Erneutes Lesen nach einem Befehl](#erneutes-lesen-nach-einem-befehl). Nichts zu tun.
- **„Véhicule … : relecture non programmée : …“** (*Fahrzeug …: erneutes Lesen nicht geplant: …*) (Warnung, höchstens einmal pro Stunde): Die Aufgabe zum erneuten Lesen konnte nicht erstellt werden; der Befehl war erfolgreich, und die Werte sind bei der nächsten Abfrage aktuell. Kehrt die Meldung wieder, prüfen Sie das Cron-System von Jeedom.
- **„Équipement … : délai de relecture après commande invalide, ramené à 30 secondes.“** (*Gerät …: Verzögerung des erneuten Lesens nach Befehl ungültig, auf 30 Sekunden zurückgesetzt.*) (Warnung): Ein Wert außerhalb der Liste wurde gespeichert (durch ein Skript, eine API oder eine Wiederherstellung); wählen Sie eine Verzögerung aus der Liste des Geräts.
- **„Véhicule … : le proxy annonce désormais … ; information(s) créée(s) : …“** (*Fahrzeug …: Der Proxy meldet jetzt …; Information(en) erstellt: …*) (Info): Nach einem Versionswechsel des Proxys hat das Plugin die nun verfügbaren Informationen der erweiterten Daten erstellt (siehe [Erweiterte Daten: was verfügbar ist](#erweiterte-daten-was-verfugbar-ist)). **„… informations de données étendues non créées …, nouvel essai à la prochaine lecture de ces données“** (*… Informationen der erweiterten Daten nicht erstellt …, neuer Versuch bei der nächsten Abfrage dieser Daten*) (Warnung, höchstens einmal pro Stunde): Die Erstellung ist fehlgeschlagen (Speicherfehler von Jeedom); sie wird von selbst oder per **Speichern** am Gerät erneut versucht.
- **„Véhicule … : fonction `donnees:…` refusée par le proxy (not supported), indisponible jusqu'au prochain changement de version du proxy.“** (*Fahrzeug …: Funktion `donnees:…` vom Proxy abgelehnt (not supported), nicht verfügbar bis zum nächsten Versionswechsel des Proxys.*) (Info): Der Proxy hat eine Kategorie abgelehnt, die er meldete; das Plugin fordert sie vor einem Update des Proxys nicht mehr an. **„Capacités du proxy du véhicule … : version …, origine …, action(s) indisponible(s) : …“** (*Fähigkeiten des Proxys des Fahrzeugs …: Version …, Herkunft …, nicht verfügbare Aktion(en): …*) (Info): Auslesen dessen, was der Proxy meldet, bei Versionswechsel.
- **„Lecture de la position (ou des pressions des pneus, ou de la mise à jour logicielle) du véhicule … en échec : …“** (*Abfrage der Position (oder der Reifendrücke oder des Software-Updates) des Fahrzeugs … fehlgeschlagen: …*) (Warnung, einmal pro Vorfall) und **„… rétablie.“** (*… wiederhergestellt.*) (Info): Das Fahrzeug oder der Proxy hat diese Abfrage abgelehnt. Die anderen Abfragen sind nicht betroffen, und **Letzter Fehler** wird nicht verändert. Im Debug nennt **„Position (ou Pressions des pneus, ou Mise à jour logicielle) du véhicule … non lue(s) : …“** (*Position (oder Reifendrücke oder Software-Update) des Fahrzeugs … nicht gelesen: …*) den Grund einer nicht erfolgten Abfrage (Fahrzeug schläft, außer Reichweite, Abfragebudget erreicht, keine Information am Gerät) und **„Position du véhicule … inchangée : …“** (*Position des Fahrzeugs … unverändert: …*) den einer ignorierten Position (veraltet, 0/0, außerhalb des Bereichs); darin steht nie eine Koordinate.
- **„Tuile du véhicule … : rendu impossible, widget standard affiché (…)“** (*Kachel des Fahrzeugs …: Darstellung unmöglich, Standard-Widget angezeigt (…)*) (Fehler): Die Kachel konnte nicht gezeichnet werden; Jeedom zeigt stattdessen das Standard-Widget an. Notieren Sie den Grund in Klammern; das Deaktivieren von **Widget-Template** in der **Erweiterten Konfiguration** unterdrückt die Meldung (siehe [Kachel des Fahrzeugs](#fahrzeugkachel)).
- **„Image du véhicule … non posée : image du modèle … absente ou illisible dans le plugin (réinstallez le plugin) ; …“** (*Bild des Fahrzeugs … nicht gesetzt: Bild des Modells … fehlt im Plugin oder ist nicht lesbar (installieren Sie das Plugin neu); …*) (Warnung): Die mit dem Plugin gelieferte Bilddatei fehlt oder ist beschädigt. Installieren Sie das Plugin neu. **„… non posée : dossier data/eqLogic de Jeedom non accessible en écriture ; …“** (*… nicht gesetzt: Verzeichnis data/eqLogic von Jeedom nicht beschreibbar; …*) (Warnung): Jeedom kann sein Bild nicht schreiben; prüfen Sie die Rechte des Verzeichnisses `data/eqLogic` von Jeedom. In beiden Fällen bleibt das Icon des Plugins (oder das aktuelle Bild) angezeigt. **„Image du véhicule … non posée : …“** (*Bild des Fahrzeugs … nicht gesetzt: …*), gefolgt von einem anderen Grund (Warnung): Das Schreiben ist fehlgeschlagen; das Gerät wird nicht verändert. **„… retirée : le modèle n'a plus d'image.“** (*… entfernt: Das Modell hat kein Bild mehr.*) (Debug): Die VIN bezeichnet jetzt ein Modell ohne Bild.
- **„Migrations : …“** (*Migrationen: …*): siehe [Das Upgrade im Log feststellen](#die-aktualisierung-im-log-nachvollziehen).

### Langsames Lesen des Proxys

Das Plugin misst die Dauer jedes Lesevorgangs, ohne jede zusätzliche Anfrage, und veröffentlicht sie in **Dauer Statusabfrage** und **Dauer Datenabfrage**. Überschreitet ein erfolgreicher Lesevorgang **10 Sekunden** (Status) bzw. **20 Sekunden** (Daten), erhält das Log **eine einzige** Warnung **„Lecture lente du proxy pour le véhicule …“** *(Langsames Lesen des Proxys für das Fahrzeug …)*, die nicht wiederholt wird, solange das Lesen langsam bleibt. Sinkt die Dauer wieder auf **7 Sekunden** (Status) bzw. **14 Sekunden** (Daten), meldet dies eine Zeile der Stufe **Info** „Lecture du proxy redevenue normale…“ *(Lesen des Proxys wieder normal …)*. Diese Schwellenwerte sind fest.

Übliche Ursachen: Raspberry Pi zu weit vom Fahrzeug entfernt (Wand, Betonboden, weit entfernt geparktes Auto), Raspberry Pi überlastet (ein anderer Client des Proxys, etwa evcc, beansprucht ihn) oder schlecht mit Strom versorgt. Stellen Sie den Raspberry Pi näher ans Fahrzeug oder wechseln Sie sein Netzteil und beobachten Sie dann die Dauer in den folgenden Zyklen.

Ein fehlgeschlagener Lesevorgang (Proxy nicht erreichbar, Zeitüberschreitung) verändert diese Informationen nicht: Seine Dauer steht in der Fehlermeldung des Logs („… après 25.0 s : …“ *(… nach 25.0 s: …)*). Die Dauer eines Befehls wird im Log auf der Stufe **Debug** geschrieben („Commande … exécutée en 3.2 s.“ *(Befehl … in 3.2 s ausgeführt.)*).

### Proxy des Forks: Token, Adapter, abgelehnter Body

| Was Sie sehen | Ursache | Maßnahme |
|---|---|---|
| **„API-Token vom Proxy abgelehnt“** in **Letzter Fehler**, oder **„API-Token vom Proxy abgelehnt: Befehl nicht gesendet“** beim Senden eines Befehls | Der Proxy des Forks hat einen `apiToken`, und das Plugin hat keinen Token oder einen anderen. Die Fahrzeuganwesenheit bleibt unverändert; das Log erhält **eine einzige** Zeile der Stufe **Fehler** pro Episode. | Tragen Sie den genauen Wert von `apiToken` in **API-Token des Proxys** ein, **Speichern**, dann **Testen** („API-Token vom Proxy akzeptiert“). |
| **„Ungültiger API-Token: …“** oder **„API-Token wird von Jeedom nicht unterstützt …“** | Der eingegebene Token enthält ein nicht zulässiges Zeichen (Akzent, Zeilenumbruch, mehr als 256 Zeichen) oder hat eine Form, die Jeedom nicht speichern kann. | Erzeugen Sie einen anderen Token (`openssl rand -hex 32`) und tragen Sie ihn in `apiToken` und im Plugin ein. |
| **Proxy nicht erreichbar**, obwohl der Raspberry Pi eingeschaltet ist | Der Proxy des Forks beendet sich beim Start, wenn `btAdapter` ungültig ist oder der Adapter nicht existiert; Docker startet ihn in einer Schleife neu. | Auf dem Raspberry Pi: `docker logs tesla-ble-http-proxy`, suchen Sie nach `Cannot start with this Bluetooth adapter`. Korrigieren oder entfernen Sie `btAdapter` (siehe [BLE-Proxy installieren](installation-proxy.md#12-fehlerbehebung)). |
| **„Befehl vom Fahrzeug abgelehnt: invalid request body: …“** | Der Proxy des Forks hat den Inhalt des Befehls abgelehnt, bevor er ihn gesendet hat. | Der Text nach dem Doppelpunkt nennt den betroffenen Schlüssel; melden Sie ihn zusammen mit dem Plugin-Log auf Debug. |

### Meldungen des Fensters Proxy-Logs

| Meldung | Ursache | Maßnahme |
|---|---|---|
| **„Logs nicht verfügbar (Proxy ≥ 2.3.0 erforderlich)“** | Der Server unter der gespeicherten URL liefert keine Logs: Proxy älter als 2.3.0 oder URL, die nicht auf den Proxy verweist. | Prüfen Sie die URL mit der Schaltfläche **Testen** und aktualisieren Sie dann den Proxy, wenn seine Version unter 2.3.0 liegt. |
| **„Proxy nicht erreichbar: Prüfen Sie, ob er gestartet ist, dann seine Adresse mit der Schaltfläche Testen“** | Der Proxy ist gestoppt, der Raspberry Pi ausgeschaltet oder die Adresse falsch. | Starten Sie den Proxy und prüfen Sie dann die URL mit **Testen**. |
| **„Proxy-URL fehlt oder ist ungültig: Tragen Sie sie ein, speichern Sie und öffnen Sie die Logs erneut“** | Es ist keine gültige URL gespeichert. | Tragen Sie die URL ein, speichern Sie und öffnen Sie das Fenster erneut. |
| **„API-Token vom Proxy abgelehnt“** | Der Proxy des Forks hat einen `apiToken`, den das Plugin nicht sendet oder der abweicht. | Tragen Sie den Token ein (siehe die Tabelle oben). |
| Fehlermeldung gefolgt von **„HTTP-Antwort 500 statt 200: Failed to encode logs“** | Der Proxy kann seinen eigenen Log-Speicher nicht mehr lesen (bekannter Fehler des Proxys). | Starten Sie den Proxy neu (`docker compose restart` auf dem Raspberry Pi). |
| **„Keine Logzeile auf dem Proxy“** | Der Proxy hat noch nichts protokolliert. | Aktualisieren Sie nach einem Zyklus des Plugins. |

### Erweitertes Laden: Symptome ohne Meldung

Stellen Sie das Plugin-Log auf **Debug**: Die Zeilen **„pilotage selon le surplus : … décision … (motif)“** *(Überschusssteuerung: … Entscheidung … (Grund))* und **„charge aux heures creuses : décision … (motif)“** *(Laden zur Niedertarifzeit: Entscheidung … (Grund))* nennen den Grund jeder Entscheidung (siehe [Meldungen des Plugin-Logs](#meldungen-des-plugin-logs)).

| Symptom | Mögliche Ursachen | Maßnahme |
|---|---|---|
| **Der Ladestrom ändert sich nicht** (Überschusssteuerung) | Der Zielstrom ist identisch mit dem letzten Sollwert oder weicht weniger als die **Hysterese** davon ab (Gründe `identique`, `hysteresis`); das **Mindestintervall zwischen Befehlen** ist nicht verstrichen (gezählt ab dem **Ende** des vorherigen Befehls); der Zielstrom wird auf das **Max** des Reglers **Ladestrom** zurückgesetzt (Grenze des Fahrzeugs oder von Hand eingestellter Wert); das Fahrzeug ist nicht angeschlossen, außer Reichweite oder das Laden ist abgeschlossen (siehe **Letzter Fehler**); **Intervall während des Ladens** deaktiviert: der gelesene **Ladestatus** ist alt; der Zeitraum von **Laden zur Niedertarifzeit** läuft (der Aufruf wird ignoriert); **Phasen** steht auf Einphasig bei einer dreiphasigen Ladestation. | Lesen Sie die Debug-Zeile „décision … (motif)“ *(Entscheidung … (Grund))*; verringern Sie die Hysterese oder das Mindestintervall, wenn die Änderungen zu selten sind; stellen Sie **Intervall während des Ladens** auf 1 Minute; prüfen Sie **Netzspannung (V)** und **Phasen**; prüfen Sie das **Max** des Reglers im Reiter **Befehle**. |
| **Das Laden stoppt nachts** (Überschusssteuerung) | Ohne Erzeugung fällt die gesendete Leistung auf 0 W: Der berechnete Strom sinkt unter die **Abschaltschwelle**, und das Laden wird nach der **Haltedauer vor dem Abschalten** gestoppt. | Normal. Um nachts zu laden, verwenden Sie **Laden zur Niedertarifzeit** (die Überschusssteuerung wird dann während des Zeitraums ignoriert). |
| **Das Laden startet morgens nicht neu** (Überschusssteuerung) | Der berechnete Strom erreicht den **Minimalen Startstrom** nicht; der Start erfolgt in zwei Schritten (**Ladestrom**, dann **Laden starten**, im nächsten Intervall); das Fahrzeug ist abgesteckt oder sein Ladezustand ist unbekannt; das Szenario ist nicht mehr geplant oder seine Aktualitätsprüfung (**Alter der Daten (min)**) ist falsch. | Prüfen Sie die in der Debug-Zeile gesendete Leistung, warten Sie ein bis zwei Intervalle, prüfen Sie das Szenario. Bei unbekanntem Ladezustand: **Aktualisieren (mit Aufwecken)**. |
| **Das Laden zur Niedertarifzeit startet nicht** | Die Funktion ist nicht angehakt oder ein Feld fehlt; die aktuelle Uhrzeit (**Uhrzeit von Jeedom**, nicht die des Fahrzeugs) liegt außerhalb des Zeitraums; das Fahrzeug ist nicht angeschlossen oder die Ladestation liefert keinen Strom (siehe **Letzter Fehler**); der **Ziel-SoC** ist kleiner oder gleich dem aktuellen Batteriestand (Ziel bereits erreicht); das **Ladelimit des Fahrzeugs** ist kleiner oder gleich dem aktuellen Stand (Laden abgeschlossen); die Steuerung ist **bis zum nächsten Zeitraum ausgesetzt** (manuelle Aktion von Jeedom aus, aus der App neu gestartetes Laden, 3 Befehlsfehler oder ein bereits versuchter Start ohne festgestelltes Laden); ein schlafendes Fahrzeug wird nur mit einem veralteten Status gesehen; das Aktualisierungsintervall ist lang (die Entscheidung wird nur bei einem Lesevorgang getroffen). | Prüfen Sie die Einstellungen und die Zeitzone von Jeedom; lesen Sie die Info-Zeile „charge aux heures creuses : décision … (motif)“ *(Laden zur Niedertarifzeit: Entscheidung … (Grund))* (zum Beispiel `suspendue_manuel`, `limite_vehicule`, `cible_atteinte`, `hors_plage`); beachten Sie **Letzter Fehler**; starten Sie **Aktualisieren (mit Aufwecken)** bei veraltetem Status; ein Abziehen mit anschließendem Wiederanstecken startet eine nach Fehlern ausgesetzte Steuerung neu. |
| **Ein Befehl wird abgelehnt oder ignoriert** | **Abgelehnt**: **„Dieser Befehl erfordert einen Schlüssel mit der Rolle Owner …“** oder **„Befehl vom Fahrzeug abgelehnt (Rolle des Proxy-Schlüssels unzureichend?) …“** (siehe [Rolle des Schlüssels](#rolle-des-schlussels): Überschusssteuerung und Niedertarifzeit erfordern nur Charging Manager); **„Von Ihrer Proxy-Version nicht unterstützt“** (Ladeplan: Proxy des Forks erforderlich); **„Ungültiger Wert: …“** (Wert außerhalb der Grenzen oder nicht numerisch). **Ignoriert** (kein Fehler, kein Befehl): Enthaltungen der Überschusssteuerung oder des Ladens zur Niedertarifzeit (**Letzter Fehler** nennt den Grund: Fahrzeug nicht angeschlossen, außer Reichweite, Laden abgeschlossen, Ladestation ohne Strom, Ladezustand unbekannt) und Aufruf von **Nach Überschuss anpassen** während des Niedertarif-Zeitraums. | Siehe die Tabellen **Letzter Fehler** und **Fehler beim Senden eines Befehls** oben. |

### Klima und Komfort: Symptome ohne Meldung

Stellen Sie das Plugin-Log auf **Debug**: Die Zeile **„préconditionnement planifié : décision … (motif)“** *(Geplante Vorklimatisierung: Entscheidung … (Grund))* nennt den Grund jeder Entscheidung der geplanten Vorklimatisierung (siehe [Meldungen des Plugin-Logs](#meldungen-des-plugin-logs)).

| Symptom | Mögliche Ursachen | Maßnahme |
|---|---|---|
| **Ein Komfortbefehl fehlt im Widget** (Sollwert, Sitze, Lenkrad, maximale Enteisung, Klimahaltemodus) | Diese Befehle werden **ausgeblendet** erstellt, auch mit dem Proxy des Forks. | Haken Sie **Anzeigen** bei jedem im Reiter **Befehle** des Geräts an (siehe [Klima und Komfort: was verfügbar ist](#klima-und-komfort-was-verfugbar-ist)). |
| **Der Befehl wird sofort mit „Von Ihrer Proxy-Version nicht unterstützt“ abgelehnt** | Der Proxy meldet ihn nicht an: offizieller Proxy 2.3.0 oder zu alte Version des Forks (mindestens `2.3.0-tb.1` für Temperatursollwert, maximale Enteisung und Klimahaltemodus, `2.3.0-tb.2` für Sitze und Lenkrad). | Installieren oder aktualisieren Sie den Proxy des Forks; eine Neuinstallation des Plugins ist nicht nötig. Prüfen Sie die **Proxy-Version** und starten Sie den Befehl dann erneut. |
| **Der Befehl wird akzeptiert, aber nichts ändert sich** | **Sitz** am Fahrzeug nicht vorhanden, ohne Wirkung akzeptiert (auf 0 gelesen); **Klimaanlage aus**: Die Sitzheizung fordert sie grundsätzlich an; **Lenkrad mit automatischer Heizung**; **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden**: Die Informationen werden nicht neu gelesen und behalten den angekündigten Wert; das Fahrzeug ist vor dem erneuten Lesen wieder eingeschlafen. | Schalten Sie die Klimaanlage ein, lassen Sie **Klimaanlage ebenfalls lesen** auf **Ja**, starten Sie **Aktualisieren (mit Aufwecken)** und lesen Sie den Wert dann erneut (dieses Verhalten ist im realen Einsatz zu bestätigen). |
| **Der Befehl wird mit einer Rollenmeldung abgelehnt** | Proxy-Schlüssel mit der Rolle Charging Manager: Das Fahrzeug lehnt Komfortaktionen ab. | Koppeln Sie einen **Owner**-Schlüssel (siehe [Rolle des Schlüssels](#rolle-des-schlussels)). |
| **Die geplante Vorklimatisierung startet nicht** | Funktion nicht angehakt; Abfahrts-**Tag** nicht angehakt (maßgeblich ist der Tag der Abfahrtszeit); **Aktualisierungsintervall** länger als die Dauer des Zeitfensters (kein Lesevorgang fällt hinein); mit **Nur wenn angeschlossen** ist das Fahrzeug abgesteckt; Klimaanlage **läuft bereits** (Grund `deja_active`); **Klimaanlage ebenfalls lesen** auf **Nein, nur Laden** (bei der Speicherung abgelehnt); Fahrzeug außer Reichweite oder nicht gelesen; Steuerung **ausgesetzt** bis zur nächsten Abfahrt (manuelle Aktion von Jeedom aus, 3 Befehlsfehler oder Charging-Manager-Schlüssel: nur ein Versuch pro Abfahrt). | Prüfen Sie die Einstellungen und die Zeitzone von Jeedom; verringern Sie das Aktualisierungsintervall (höchstens 5 Minuten empfohlen); lesen Sie die Zeile **Info** „préconditionnement planifié : décision … (motif)“ *(Geplante Vorklimatisierung: Entscheidung … (Grund))* (zum Beispiel `hors_fenetre`, `deja_active`, `suspendue_manuel`) und **Letzter Fehler**; koppeln Sie bei Bedarf einen **Owner**-Schlüssel. |
| **Die Klimaanlage startet verspätet oder stoppt nicht zur rechten Zeit** | Die Entscheidung wird nur bei einem Lesevorgang des Fahrzeugs getroffen: Start und Stopp folgen dem Lesetakt. Ein schlafend gesehenes Fahrzeug erhält nie einen Stopp. | Verringern Sie das Aktualisierungsintervall; stoppen Sie die Klimaanlage bei Bedarf von Jeedom aus. |
| **Eine maximale Enteisung oder ein Klimahaltemodus stoppt nicht** | Das Plugin stoppt sie nie von selbst; die geplante Vorklimatisierung ersetzt oder stoppt sie ebenfalls nicht. | Senden Sie **Aus** über das Widget oder ein Szenario. |

Die für diese Funktionen angezeigten Meldungen (**Ungültiger Wert: …**, **Geplante Vorklimatisierung: …**, **Fahrzeug nicht angeschlossen: Geplante Vorklimatisierung nicht gestartet**, **Von Ihrer Proxy-Version nicht unterstützt**) sind in [Meldungen beim Speichern](#meldungen-beim-speichern), [Information „Letzter Fehler“ (Lesen)](#information-letzter-fehler-abfrage) und [Fehler beim Senden eines Befehls](#fehler-beim-senden-eines-befehls) beschrieben.

### Öffnungen und Sicherheit: Symptome ohne Meldung

Meldungen dieser Funktion: **„Kofferraum bereits offen oder in Bewegung …“**, **„Kofferraumzustand unbekannt …“**, **„Kofferraumzustand nicht lesbar …“** und **„Von Ihrer Proxy-Version nicht unterstützt“** in [Fehler beim Senden eines Befehls](#fehler-beim-senden-eines-befehls); die Ablehnung einer Warndauer in [Meldungen beim Speichern](#meldungen-beim-speichern); die Warnmeldungen in [Nachrichtenzentrale von Jeedom (nach einem Update)](#nachrichtenzentrale-von-jeedom-nach-einem-update); die Rollenablehnung in [Rolle des Schlüssels](#rolle-des-schlussels).

| Symptom | Mögliche Ursachen | Maßnahme |
|---|---|---|
| **Eine Öffnung bleibt auf 0, obwohl sie offen ist** | Das Fahrzeug schläft: Der Status wird nicht neu gelesen und der letzte Wert bleibt; ein unbekannter Status lässt den letzten Wert stehen; Proxy älter als 2.3.0 (Öffnungen nicht veröffentlicht); der Proxy meldet die Öffnungen als geschlossen, wenn das Fahrzeug sie nicht liefert. | Prüfen Sie **Alter der Daten (min)** und **Fahrzeug anwesend**; starten Sie **Aktualisieren**; prüfen Sie die **Proxy-Version** (siehe [Proxy-Version prüfen und aktualisieren](#die-version-des-proxys-prufen-und-aktualisieren)). |
| **Wächter-Modus in „Letzter Befehl“ folgt der App nicht** | Offizieller Proxy 2.3.0 oder zu alter Fork: Der Wert ist der des letzten Befehls von Jeedom. Mit dem Fork `2.3.0-tb.2` behält ein schlafendes Fahrzeug außerdem seinen zuletzt gelesenen Wert. | Wechseln Sie zum Proxy des Forks (mindestens `2.3.0-tb.2`) und starten Sie **Aktualisieren (mit Aufwecken)**; siehe [Status des Wächter-Modus](#zustand-des-wachter-modus). |
| **Die Warnung wird nicht gesendet** | Warnung nicht aktiviert oder Dauer leer (bei der Speicherung abgelehnt); Dauer noch nicht verstrichen (die Warnung wird zwischen der Dauer und der Dauer plus zwei Aktualisierungsintervallen gesendet); Proxy nicht erreichbar, Fahrzeug außer Reichweite oder Lesevorgang fehlgeschlagen (nichts wird ausgewertet); Ladeklappe offen, während das Fahrzeug angeschlossen ist oder lädt (keine Warnung für die Ladeklappe); Insasse anwesend oder Anwesenheit unbekannt (Warnung „entriegelt ohne Insassen“); Cache von Jeedom während der Episode geleert; Szenario, das **Öffnungsalarm** `== 1` nicht prüft. | Prüfen Sie den Block **Warnungen bei längerer Öffnung**, **Letzter Fehler** und **Alter der Daten (min)**; siehe [Warnungen bei längerer Öffnung](#warnungen-bei-langerer-offnung). |
| **Die Warnmeldung bleibt in der Nachrichtenzentrale** | Jeedom entfernt die Meldung beim Schließen nicht. | Löschen Sie sie von Hand. |
| **Vor einer sensiblen Aktion erscheint keine Bestätigung** | Das Kontrollkästchen **Aktion bestätigen** ist beim Befehl nicht angehakt; die Aktion wird aus einem Szenario oder der API gestartet (nie eine Bestätigung); der Befehl gehört nicht zu den fünf betroffenen Aktionen. | Haken Sie das Kontrollkästchen in den erweiterten Parametern des Befehls an; siehe [Bestätigung sensibler Aktionen](#bestatigung-sensibler-aktionen). |
| **Der Kofferraum erscheint nicht im Widget** | **Kofferraum hinten öffnen** und **Frunk öffnen** werden **ausgeblendet** erstellt, auch mit dem Proxy des Forks. | Haken Sie **Anzeigen** im Reiter **Befehle** an (siehe [Öffnungen und Sicherheit: was verfügbar ist](#offnungen-und-sicherheit-was-verfugbar-ist)). |
| **Der hintere Kofferraum öffnet sich nicht** | Eine bereits geöffnete motorisierte Heckklappe wird vom Plugin abgelehnt, um sie nicht zu schließen; das Fahrzeug hat mangels Rechten abgelehnt (**Schlüsselrolle**); offizieller Proxy 2.3.0. | Lesen Sie **Letzter Fehler** und die angezeigte Meldung; siehe [Hinteren Kofferraum und Frunk öffnen](#kofferraum-hinten-und-frunk-offnen). |

### Erweiterte Daten: Symptome ohne Meldung

Meldungen dieser Funktion: die Ablehnung von Zuhause und Radius in [Meldungen beim Speichern](#meldungen-beim-speichern), **„Funktion von diesem Proxy nicht unterstützt — …“** in [Information „Letzter Fehler“ (Lesen)](#information-letzter-fehler-abfrage), die Logzeilen in [Meldungen des Plugin-Logs](#meldungen-des-plugin-logs).

| Symptom | Mögliche Ursachen | Maßnahme |
|---|---|---|
| **Kilometerstand, Gang, Geschwindigkeit, Leistung, Drücke, Software-Update oder Position fehlen** im Reiter **Befehle** | Der Proxy meldet die Kategorie nicht an (offizieller Proxy 2.3.0 oder zu alte Version des Forks): Die Informationen werden **nicht erstellt**. | Prüfen Sie die **Proxy-Version**, installieren Sie den Proxy des Forks (mindestens `2.3.0-tb.2`), warten Sie einen Zyklus (erneute Erkennung) oder **Speichern** Sie das Gerät: siehe [Erweiterte Daten: was verfügbar ist](#erweiterte-daten-was-verfugbar-ist). |
| **Die Informationen existieren, bleiben aber leer** | Es hat noch kein Lesevorgang stattgefunden: Das Fahrzeug schläft oder ist außer Reichweite, oder ein **Einschlaffenster** ist offen; bei Drücken, Software-Update und Position sind seit dem vorherigen Versuch weniger als 15 Minuten vergangen. | Starten Sie **Aktualisieren (mit Aufwecken)**; prüfen Sie **Alter der Daten (min)** und **Fahrzeug anwesend**. |
| **Die Informationen werden nach dem Wechsel zum Fork nicht mehr aktualisiert** | Der Proxy hat die Kategorie abgelehnt (Info-Zeile „refusée par le proxy (not supported)“ *(vom Proxy abgelehnt (not supported))* im Log); das Plugin fragt sie erst beim nächsten Versionswechsel des Proxys wieder an. | Aktualisieren Sie den Proxy des Forks; ein Versionswechsel startet die Erkennung neu. |
| **Kilometerstand eingefroren** | Fahrzeug schläft (kein Lesevorgang, letzter Wert bleibt) oder Einschlaffenster offen. | Normal. **Aktualisieren (mit Aufwecken)** für einen sofortigen Lesevorgang. |
| **Druck bei 0 oder fehlend** | Ein Wert von null, negativ oder über 10 bar wird ignoriert: Die Information behält ihren letzten Wert oder bleibt leer, wenn sie nie gelesen wurde; das Fahrzeug übermittelt den Druck eines Reifens nicht. | Warten Sie bei wachem Fahrzeug auf den nächsten Lesevorgang; prüfen Sie am Bildschirm des Fahrzeugs. |
| **Geschwindigkeit oder Leistung scheinen falsch** | Angenommene, nicht bestätigte Einheiten (mph und kW); da der Proxy in der Garage steht, sind diese Werte fast nie aussagekräftig. | Vergleichen Sie mit dem Bildschirm des Fahrzeugs; verwenden Sie sie nicht für eine kritische Entscheidung. |
| **Software-Update zeigt „Unbekannte“ oder eine Rohbezeichnung** | Ein Update ist aktiv, ohne dass das Fahrzeug eine Version meldet („Unbekannte“), oder der Proxy liefert einen Status, den das Plugin nicht kennt (unverändert angezeigt). | Nichts zu tun; die Version erscheint, sobald das Fahrzeug sie mitteilt. |
| **Modell oder Modelljahr stehen auf „Unbekannt“** | Die VIN ist leer, gehört nicht zu einem erkannten Tesla oder ihr 10. Zeichen ist kein decodierbares Jahr. | Prüfen Sie die **VIN** des Geräts und **speichern** Sie. |
| **Zu Hause bleibt bei 0 (oder erscheint nicht)** | Vor der ersten Berechnung zeigt die Kachel 0: Die Information wird **nie geschrieben**, solange Zuhause oder Position unbekannt sind. Keine Koordinaten von Zuhause eingetragen und keine Position in Jeedom; Position nie gelesen (offizieller Proxy, schlafendes Fahrzeug); **Radius (m)** zu klein. | Tragen Sie **Zuhause** und **Radius** im Gerät oder die Position von Jeedom ein; warten Sie auf einen Lesevorgang der Position (höchstens 15 Minuten). Siehe [Position und Datenschutz](#position-und-datenschutz). |
| **Zu Hause bleibt bei 1, obwohl das Fahrzeug weggefahren ist** | Außerhalb der Bluetooth-Reichweite wird keine Position mehr gelesen: Die Information behält ihren letzten Wert. | Kombinieren Sie in Ihren Szenarien `Zu Hause == 1` mit **Fahrzeug anwesend**. |
| **Die Position wird nicht aktualisiert** | Fahrzeug schläft oder ist außer Reichweite; Position als zu alt (mehr als eine Stunde) oder bei 0/0 eingestuft und ignoriert; weniger als 15 Minuten seit dem vorherigen Lesevorgang; **Breitengrad** und **Längengrad** gelöscht (nur **Zu Hause** wird noch berechnet). | Starten Sie **Aktualisieren (mit Aufwecken)**; prüfen Sie **Fahrzeug anwesend** und **Alter der Daten (min)**. |
| **Breiten- und Längengrad erscheinen in einem Log von Jeedom** | Das Log `event` von Jeedom zeichnet jeden neuen Wert einer Information auf, auch einer ausgeblendeten; es ist nicht das Log des Plugins. | Siehe [Position und Datenschutz](#position-und-datenschutz): Senken Sie die Stufe des Logs `event` oder löschen Sie diese beiden Informationen. |
| **Ich sehe Breitengrad und Längengrad nicht im Widget** | Sie werden absichtlich **ausgeblendet** und **nicht historisiert** erstellt. | Haken Sie **Anzeigen** (und bei Bedarf **Historisieren**) im Reiter **Befehle** an. |

### Widget und Anzeige: Symptome ohne Meldung

Meldungen dieser Funktion: die Logzeilen in [Meldungen des Plugin-Logs](#meldungen-des-plugin-logs).

| Symptom | Mögliche Ursachen | Maßnahme |
|---|---|---|
| **Ich sehe die Befehls-Vignetten, nicht die Kachel** | Das Kontrollkästchen **Widget-Template** ist nicht angehakt (getroffene Wahl, oder ein Gerät, das vor dem Update ein Tabellenlayout oder ein benutzerdefiniertes Befehls-Widget hatte); das Plugin musste auf das Standard-Widget zurückfallen (Zeile **Tuile du véhicule … rendu impossible** *(Kachel des Fahrzeugs … Darstellung nicht möglich)* im Log). | Haken Sie **Widget-Template** in der **Erweiterten Konfiguration** an, speichern Sie und laden Sie die Seite neu; siehe [Widget des Plugins wiederherstellen](#das-widget-des-plugins-wiederherstellen). |
| **Ich sehe das Fahrzeugbild nicht** | Modell ohne Bild (Semi, Roadster, unbekannte VIN); von Ihnen entferntes Bild (endgültige Entfernung); Standard-Widget (ohne Bild); Bildordner von Jeedom nicht beschreibbar oder Bild des Plugins unlesbar (Warnung im Log). | Prüfen Sie **Modell** und **VIN**; haken Sie **Widget-Template** an; laden Sie Ihr Bild in der **Erweiterten Konfiguration** hoch. Siehe [Bild des Modells](#modellbild). |
| **Das Bild kehrt nach „Bild entfernen“ nicht zurück** | Die Entfernung ist **endgültig**: Das Plugin setzt es nie wieder ein. | Laden Sie ein Bild Ihrer Wahl hoch. |
| **Die Befehle sind durcheinander, oder ein neuer Befehl steht ganz unten** | Die Reihenfolge wird nur bei der Erstellung festgelegt und nie neu geschrieben; ein durch ein Update hinzugefügter Befehl wird in der Nähe seines Themas eingeordnet oder am Ende der Liste, wenn dieses Thema am Gerät nicht existiert. | Verschieben Sie die Zeilen per Drag-and-drop im Reiter **Befehle** und **speichern** Sie; siehe [Reihenfolge der Befehle](#reihenfolge-der-befehle). |
| **Ein von mir geleerter generischer Typ ist zurückgekehrt** | Der Befehl wurde gelöscht und neu erstellt, oder das Setzen der Typen wurde nach einem unterbrochenen Update wiederholt. | Setzen Sie **Keine** in der erweiterten Konfiguration des Befehls; siehe [Generische Typen](#generische-typen). |
| **Eine Schaltfläche der Kachel ist ausgegraut** | Der entsprechende Befehl existiert am Gerät nicht, oder Ihr Proxy unterstützt ihn nicht. | Prüfen Sie den Reiter **Befehle** und die **Proxy-Version** (siehe [Proxy-Version prüfen und aktualisieren](#die-version-des-proxys-prufen-und-aktualisieren)). |
| **Eine Schaltfläche bleibt abgeschwächt** | Der Befehl läuft noch (ein Befehl kann mehrere Dutzend Sekunden dauern). Sie wird spätestens nach 4 Minuten wieder freigegeben. | Warten Sie; lesen Sie bei einem Fehlschlag die Meldung von Jeedom und **Letzter Fehler**. |
| **Die Kachel zeigt „Unbekannt“ oder „Keine bekannte Messung“** | Es war noch kein Lesevorgang erfolgreich, oder der Wert ist nicht numerisch: nie ein erfundener Wert. | Starten Sie **Aktualisieren (mit Aufwecken)**; prüfen Sie **Fahrzeug anwesend** und **Letzter Fehler**. |
| **Die Dauer „Daten von vor“ ändert sich nicht, während ich die Seite ansehe** | Sie wird im Browser nicht fortgeschrieben; sie folgt **Alter der Daten (min)**, das jede Minute neu berechnet wird. | Normal: Warten Sie die nächste Minute ab. |
| **Die native mobile App zeigt die Kachel nicht** | Die Kachel betrifft nur das Dashboard und die mobile Weboberfläche; die App stützt sich auf die generischen Typen. | Prüfen Sie die generischen Typen der Befehle; siehe [Generische Typen](#generische-typen). |

### Symptome ohne Meldung

- **Proxy erreichbar steht auf 0, obwohl der Proxy eingeschaltet ist**: Der Proxy antwortet „nicht gefunden“ auf die Gesundheitsabfrage, wenn seine Version älter als 2.1.3 ist oder die Adresse nicht auf den Proxy verweist. Prüfen Sie Version und Adresse mit **Testen** oder **Diesen Proxy testen** und aktualisieren Sie dann den Proxy (siehe [Proxy-Version prüfen und aktualisieren](#die-version-des-proxys-prufen-und-aktualisieren)).
- **Fahrzeug anwesend bleibt bei 0**: Der Proxy findet das Fahrzeug per Bluetooth nicht. Stellen Sie den Raspberry Pi näher ans Fahrzeug.
- **Die Ladeinformationen bewegen sich nicht mehr, obwohl Letzter Fehler Keine anzeigt**: Das Fahrzeug schläft. Das ist das normale Verhalten, siehe [Aktualisierung der Informationen](#aktualisierung-der-informationen).
- **Keine Anfrage gelingt**: Testen Sie die URL mit der Schaltfläche **Testen** (der abschließende `/` wird vom Plugin behandelt), dann über einen Browser.
- **Der Link zum Dashboard öffnet sich nicht**, obwohl der Proxy funktioniert: Die URL enthält einen Docker-Dienstnamen, den Ihr Browser nicht kennt. Öffnen Sie `http://<IP_des_Pi>:8080/dashboard`.
- **Das Diagramm der Reichweite macht einen Sprung**: Normal nach dem Update von 0.x (Meilen, dann km), siehe [Reichweite und Ladegeschwindigkeit](#reichweite-und-ladegeschwindigkeit).
- **Ich sehe die Zeilen für Beginn und Ende der Störung im Log nicht**: Stellen Sie das Plugin-Log mindestens auf die Stufe **Info**.
- **Der Proxy antwortet nach einigen Stunden nicht mehr**: Das ist ein häufiges Problem beim Raspberry Pi Zero W der ersten Generation. Starten Sie den Proxy neu oder wechseln Sie zu einem Raspberry Pi Zero 2 W. Antwortet der Proxy noch, aber die Lesevorgänge laufen ab, warnt Sie das Plugin: siehe [Warnung bei blockiertem Bluetooth-Adapter](#warnung-bei-blockiertem-bluetooth-adapter).
- **Unterbrochene Bluetooth-Verbindungen**: Das Fahrzeug akzeptiert nur 3 gleichzeitig verbundene Geräte; trennen Sie ein Telefon oder eine Uhr.
