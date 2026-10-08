# Den BLE-Proxy auf einem Raspberry Pi Zero 2 W installieren

Das Plugin Tesla BLE spricht nicht direkt mit dem Auto: Es läuft über **TeslaBleHttpProxy** (hier das Image des für dieses Plugin gepflegten Forks, siehe [Fork-Image oder wimaha-Image](#fork-image-oder-wimaha-image)), ein kleines Programm, das auf einem Bluetooth-fähigen Gerät in der Nähe des Fahrzeugs läuft. Diese Seite erklärt Schritt für Schritt, wie Sie diesen Proxy auf einem **Raspberry Pi Zero 2 W**, dem empfohlenen Board, installieren und anschließend mit dem Auto koppeln.

```
Jeedom  --WLAN / lokales Netzwerk-->  Raspberry Pi Zero 2 W (TeslaBleHttpProxy)  --Bluetooth-->  Fahrzeug
```

Rechnen Sie mit etwa einer Stunde, Kopplung inbegriffen. Sie brauchen keine Programmierkenntnisse, geben aber einige Befehle in einem Terminal ein.

> **IMPORTANT**
>
> Das Plugin verlangt **mindestens TeslaBleHttpProxy 2.3.0**. Das unten empfohlene Fork-Image (`2.3.0-tb.2`) erfüllt diese Anforderung: Das Plugin ignoriert das Suffix `-tb.N` der Versionsnummer.

## 1. Warum ein Raspberry Pi Zero 2 W?

Das Bluetooth eines Tesla hat eine Reichweite von **5 bis 10 Metern**. Der Proxy muss also in der Garage oder ganz in der Nähe des Stellplatzes stehen, während Jeedom oft woanders im Haus läuft. Ein Raspberry Pi Zero 2 W ist klein, verbraucht sehr wenig Strom und hat WLAN und Bluetooth integriert.

| Merkmal | Raspberry Pi Zero 2 W |
|---|---|
| Prozessor | 4 Kerne ARM Cortex-A53 64 Bit mit 1 GHz |
| Speicher | 512 MB |
| Bluetooth | 4.2, mit Bluetooth Low Energy (BLE) |
| WLAN | nur 2,4 GHz (802.11 b/g/n) |
| Stromversorgung | 5 V, 2,5 A, Micro-USB-Anschluss |

> **Astuce**
>
> Kaufen Sie nicht den älteren **Raspberry Pi Zero W** (ohne die „2“): Sein ARMv6-Prozessor wird von aktuellen Docker-Versionen nicht mehr unterstützt, und sein Bluetooth-Adapter neigt dazu, nach einigen Stunden einzufrieren. Ein Raspberry Pi 3, 4 oder 5 eignet sich ebenfalls, sofern er in Reichweite des Fahrzeugs steht.

## 2. Benötigtes Material

- Ein **Raspberry Pi Zero 2 W**.
- Ein hochwertiges **5-V-/2,5-A-Netzteil** mit Micro-USB, idealerweise das offizielle Netzteil. Ein zu schwaches Netzteil führt zu Bluetooth-Aussetzern, die schwer zu diagnostizieren sind.
- Eine **microSD-Karte eines Markenherstellers** der Klasse **„High Endurance“** (für den Dauerbetrieb ausgelegt), empfohlen werden **16 GB** (mindestens 8 GB mit Raspberry Pi OS Lite 64 Bit). Der Raspberry Pi läuft Tag und Nacht: Eine alte oder einfache Karte verschleißt irgendwann und fällt aus.
- Ein **Gehäuse**, vorzugsweise aus Kunststoff: Ein Metallgehäuse verringert die Funkreichweite.
- Ein Computer mit microSD-Kartenleser, um die Karte vorzubereiten.
- Das **2,4-GHz-WLAN Ihres Routers** muss dort ankommen, wo Sie den Raspberry Pi aufstellen.

## 3. Den Standort wählen

Prüfen Sie den Standort, bevor Sie irgendetwas installieren:

1. Der Raspberry Pi muss **weniger als 5 bis 10 Meter** von dem Platz entfernt sein, an dem das Auto parkt, möglichst ohne dicke Wand oder Garagentor aus Metall dazwischen.
2. Er muss das **2,4-GHz-WLAN** gut empfangen: Prüfen Sie das an dieser Stelle mit Ihrem Smartphone.
3. Er braucht eine **Steckdose** in der Nähe.

## 4. Die microSD-Karte vorbereiten

Verwendet wird das offizielle Werkzeug **Raspberry Pi Imager**, das **Raspberry Pi OS Lite (64-bit)** installiert und WLAN sowie Fernzugriff schon vor dem ersten Start konfiguriert.

1. Laden Sie [Raspberry Pi Imager](https://www.raspberrypi.com/software/) herunter und installieren Sie es auf Ihrem Computer.
2. Stecken Sie die microSD-Karte in den Computer und starten Sie Raspberry Pi Imager.
3. **Modell**: Wählen Sie **Raspberry Pi Zero 2 W**.
4. **Betriebssystem**: Wählen Sie **Raspberry Pi OS (other)**, dann **Raspberry Pi OS Lite (64-bit)**. Die Version „Lite“ hat keine grafische Oberfläche: Das ist gewollt, so bleibt dem Proxy mehr Speicher.
5. **Speicher**: Wählen Sie Ihre microSD-Karte.
6. Wenn Imager anbietet, die **Einstellungen anzupassen**, stimmen Sie zu und tragen Sie ein:
   - den **Hostnamen**, zum Beispiel `teslaproxy`;
   - einen **Benutzernamen** und ein **Passwort** (notieren Sie sich beides);
   - das **WLAN** (Name und Passwort) und das **WLAN-Land** (DE);
   - die **Zeitzone**;
   - **aktivieren Sie SSH** im Reiter **Dienste** (Passwort-Authentifizierung).
7. Starten Sie das Schreiben, warten Sie das Ende der Überprüfung ab und entnehmen Sie dann die Karte.

## 5. Erster Start und Verbindung

1. Stecken Sie die Karte in den Raspberry Pi, stellen Sie ihn an seinem Platz auf und schließen Sie das Netzteil an. Der erste Start dauert einige Minuten.
2. Suchen Sie die **IP-Adresse** des Raspberry Pi in der Oberfläche Ihres Routers (Liste der verbundenen Geräte, Name `teslaproxy`).
3. **Legen Sie diese Adresse fest**: Richten Sie in Ihrem Router für den Raspberry Pi eine **DHCP-Reservierung** (oder „statische Lease“) ein. Das ist unverzichtbar, denn das Plugin speichert diese Adresse.
4. Öffnen Sie auf Ihrem Computer ein Terminal (PowerShell unter Windows, Terminal unter macOS oder Linux) und verbinden Sie sich:

   ```
   ssh <Benutzer>@<IP_des_Pi>
   ```

   Bestätigen Sie beim ersten Mal den Fingerabdruck und geben Sie dann Ihr Passwort ein.

5. Aktualisieren Sie das System:

   ```
   sudo apt-get update && sudo apt-get upgrade -y
   ```

6. Prüfen Sie, ob Bluetooth aktiv ist:

   ```
   bluetoothctl list
   ```

   Es muss eine Zeile `Controller XX:XX:XX:XX:XX:XX teslaproxy [default]` erscheinen. Wenn nichts angezeigt wird, starten Sie den Raspberry Pi neu (`sudo reboot`) und versuchen Sie es erneut.

> **Astuce**
>
> Um WLAN-Aussetzer zu vermeiden, deaktivieren Sie die Energiesparfunktion des WLAN. Ermitteln Sie den Namen Ihrer Verbindung mit `nmcli connection show`, geben Sie dann `sudo nmcli connection modify "<Name_der_Verbindung>" 802-11-wireless.powersave 2` ein und starten Sie neu.

## 6. Docker installieren

Der Proxy wird als **Docker**-Image bereitgestellt, was Installation und Aktualisierungen vereinfacht.

1. Installieren Sie Docker mit dem offiziellen Skript:

   ```
   curl -sSL https://get.docker.com | sh
   ```

2. Prüfen Sie, ob die Installation vollständig durchgelaufen ist:

   ```
   sudo docker run --rm hello-world
   ```

   Es muss die Meldung „Hello from Docker!“ erscheinen. Verlassen Sie sich nicht auf `docker --version`: Der Befehl antwortet, sobald der Client installiert ist, auch wenn die Docker-Engine selbst fehlt. Wenn der Befehl fehlschlägt, siehe [Fehlerbehebung](#12-fehlerbehebung).
3. Erlauben Sie Ihrem Benutzer, Docker zu verwenden:

   ```
   sudo usermod -aG docker $USER
   ```

4. **Melden Sie sich ab** (`exit`) und verbinden Sie sich erneut per SSH, damit dieses Recht übernommen wird.
5. Prüfen Sie, ob Docker ohne `sudo` funktioniert:

   ```
   docker run --rm hello-world
   ```

## 7. TeslaBleHttpProxy installieren

1. Legen Sie einen Ordner für den Proxy an, mit einem Unterordner `key`, der den Schlüssel des Fahrzeugs enthalten wird:

   ```
   cd ~
   mkdir -p TeslaBleHttpProxy/key
   cd TeslaBleHttpProxy
   ```

2. Erstellen Sie die Konfigurationsdatei:

   ```
   nano docker-compose.yml
   ```

3. Fügen Sie diesen Inhalt ein:

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

   Diese Zeilen haben jeweils eine Aufgabe:
   - `image`: das Fork-Image, mit einer **genauen Versionsnummer** (empfohlen: Der Proxy ändert sich nur, wenn Sie es entscheiden, siehe [Das Proxy-Image aktualisieren](#das-proxy-image-aktualisieren)). Für eine neuere Version sehen Sie sich die [veröffentlichten Versionen](https://github.com/superdcat/TeslaBleHttpProxy/releases) an; `:latest` ist möglich, wird aber als Standardeinstellung nicht empfohlen;
   - `volumes`: Der Ordner `key` bewahrt den Schlüssel des Fahrzeugs außerhalb des Containers auf, er übersteht Aktualisierungen; `/var/run/dbus` gibt Zugriff auf das Bluetooth des Raspberry Pi;
   - `restart: always`: Der Proxy startet nach einem Stromausfall von selbst neu (ohne das Image zu wechseln: siehe [Das Proxy-Image aktualisieren](#das-proxy-image-aktualisieren));
   - `network_mode: host`, `privileged` und `cap_add`: Der Proxy braucht direkten Zugriff auf das Netzwerk und den Bluetooth-Adapter;
   - `logging`: begrenzt die Docker-Protokolle auf 3 Dateien von je 10 MB. Der Proxy schreibt fortlaufend: Ohne diese Begrenzung wachsen die Protokolle an und nutzen die microSD-Karte unnötig ab.

4. Speichern Sie mit `Ctrl + X`, dann `Y` und `Enter`.
5. Starten Sie den Proxy:

   ```
   docker compose up -d
   ```

6. Prüfen Sie, ob er antwortet: Öffnen Sie in einem Browser auf Ihrem Computer `http://<IP_des_Pi>:8080/api/proxy/1/version`. Sie müssen eine JSON-Antwort erhalten, die die Version (`2.3.0-tb.2` mit dem obigen Image) und `"flavor":"superdcat"` enthält.

### Fork-Image oder wimaha-Image

Der Proxy ist freie Software von **wimaha** ([TeslaBleHttpProxy](https://github.com/wimaha/TeslaBleHttpProxy)). Diese Seite empfiehlt den **Fork** `ghcr.io/superdcat/tesla-ble-http-proxy`, der seine Routen und Antworten identisch übernimmt: Das Plugin (und evcc) funktionieren mit dem einen wie mit dem anderen auf dieselbe Weise, ohne dass an ihrer Konfiguration etwas geändert werden muss.

Der Fork ergänzt unter anderem: eine Route `/api/proxy/1/capabilities`, die auflistet, was der Proxy kann (und welche Rolle der aktive Schlüssel hat), zusätzliche Befehle und Daten, ein optionales Zugriffs-Token (`apiToken`), die Wahl des Bluetooth-Adapters (`btAdapter`), die Einstellung der Haltedauer der Verbindung (`connectionTimeout`) und die Freigabe des Bluetooth-Adapters im Ruhezustand (`releaseAdapterWhenIdle`).

> **Astuce**
>
> Das **wimaha**-Image (`wimaha/tesla-ble-http-proxy`) bleibt **als Alternative** ab Version 2.3.0 nutzbar: Das Plugin funktioniert damit. Ihm fehlt jedoch alles oben Genannte: keine Route `capabilities`, kein Token, keine Wahl des Bluetooth-Adapters und keine Einstellung der Verbindungshaltedauer. Um es zu verwenden, ersetzen Sie einfach die Zeile `image:` der Datei `docker-compose.yml` durch `image: wimaha/tesla-ble-http-proxy`. Das Plugin hängt nicht davon ab: Mit dem Fork liest es die Route `capabilities`, um sofort zu wissen, welche Befehle Ihr Proxy akzeptiert; mit dem wimaha-Image findet es das im Betrieb heraus, wenn der Proxy einen Befehl ablehnt.

### Optionale Einstellungen

Der Proxy akzeptiert einige Einstellungen, die Sie in `docker-compose.yml` unter `container_name` ergänzen und dann mit `docker compose up -d` anwenden:

```yaml
    environment:
      - scanTimeout=10
      - logLevel=info
```

| Einstellung | Standard | Wann ändern |
|---|---|---|
| `scanTimeout` | 5 s | Das Fahrzeug wird **nicht immer gefunden**: Stellen Sie 10 oder 15 Sekunden ein. |
| `logLevel` | `info` | Stellen Sie für die Dauer einer Diagnose `debug` ein. |
| `vehicleDataCacheTime` | 30 s | Dauer, während der der Proxy dieselben Lade- und Klimatisierungsdaten erneut ausliefert. Behalten Sie den Standardwert bei. |
| `httpListenAddress` | `:8080` | Ändern Sie den Port nur, wenn er bereits belegt ist; tragen Sie den neuen Port dann in die URL des Plugins ein. |
| `apiToken` | leer (keine Authentifizierung) | Schützt den Proxy mit einem Token: Tragen Sie **denselben Wert** unter **API-Token des Proxys** (Konfiguration des Plugins) ein. Erzeugen Sie ihn zum Beispiel mit `openssl rand -hex 32`. Verwenden Sie auf allen Ihren Proxys dasselbe Token. Siehe den Kasten unten. |
| `btAdapter` | leer (Standardadapter) | Der Raspberry Pi hat **mehrere Bluetooth-Adapter** (zum Beispiel einen USB-Stick) und der Proxy muss einen davon verwenden: `hci0` bis `hci15`, in Kleinbuchstaben (zum Beispiel `hci1`). Verfügbar ab `2.3.0-tb.2`. |
| `connectionTimeout` | 29 s | Dauer, während der die Bluetooth-Verbindung nach einem Befehl geöffnet bleibt, von 10 bis 120 Sekunden. Die Frist wird **ab dem Öffnen** der Verbindung gezählt: Weitere Befehle setzen sie nicht zurück. Ein höherer Wert belegt einen der 3 Bluetooth-Plätze des Fahrzeugs länger. Ein ungültiger Wert wird durch 29 ersetzt. Verfügbar ab `2.3.0-tb.2`. |
| `releaseAdapterWhenIdle` | `false` | Stellen Sie `true` **nur** ein, wenn ein anderer Dienst auf dem Raspberry Pi den Bluetooth-Adapter nutzen können muss, während der Proxy nicht arbeitet. Jeder erste Befehl dauert dann etwas länger. Die Einschränkungen finden Sie in den [Umgebungsvariablen des Forks](https://github.com/superdcat/TeslaBleHttpProxy/blob/main/docs/environment_variables.md#releaseadapterwhenidle). Verfügbar ab `2.3.0-tb.2`. |

> **IMPORTANT**
>
> **`apiToken` mit Jeedom aktivieren**, in dieser Reihenfolge:
>
> 1. Fügen Sie die Zeile `- apiToken=<Ihr_Token>` in `docker-compose.yml` ein und führen Sie dann `docker compose up -d` aus;
> 2. Tragen Sie in Jeedom unter **Plugins > Plugin Management > Tesla BLE** dasselbe Token unter **API-Token des Proxys** ein und klicken Sie dann auf **Speichern**;
> 3. Klicken Sie auf **Testen**: Es muss **„API-Token vom Proxy akzeptiert“** anzeigen.
>
> Das Token: 1 bis 256 druckbare ASCII-Zeichen (Buchstaben, Ziffern, Satzzeichen), ohne Akzente und Zeilenumbrüche. Sobald das Token aktiv ist, fragt das Dashboard des Proxys im Browser nach einer Kennung: Benutzername frei wählbar, Passwort = das Token. **evcc** kann dieses Token nicht senden: Aktivieren Sie es nicht, wenn evcc denselben Proxy verwendet. Das Token wird im lokalen Netzwerk im Klartext übertragen: Es ersetzt nicht die Isolierung des Netzwerks (siehe [Sicherheit](#11-sicherheit)).

## 8. Den Schlüssel erzeugen und mit dem Fahrzeug koppeln

Der Proxy fungiert als zusätzlicher Autoschlüssel. Sie müssen diesen Schlüssel also erzeugen und ihn dann im Fahrzeug mit Ihrer **Schlüsselkarte** (der NFC-Karte) autorisieren.

### Die Rolle des Schlüssels wählen

| Rolle | Was sie erlaubt | Für wen |
|---|---|---|
| **Charging Manager** (empfohlen) | Zustand und Daten des Fahrzeugs lesen; wecken; Laden starten und stoppen; Ladestrom einstellen | Nutzung mit Schwerpunkt Laden (Niedertarifzeit, Solar) |
| **Owner** | Alle Befehle, einschließlich Verriegeln, Entriegeln, Hupe, Licht, Wächter-Modus und Klimatisierung | Wenn Sie mehr als nur das Laden steuern möchten |

Der Proxy hat **standardmäßig keine Authentifizierung** (das API-Token des Forks ist optional): Mit einem Owner-Schlüssel kann jedes Gerät in Ihrem lokalen Netzwerk das Fahrzeug entriegeln. Wählen Sie Owner nur, wenn Sie es brauchen, und lesen Sie den Abschnitt [Sicherheit](#11-sicherheit).

### Koppeln

1. Öffnen Sie das Dashboard des Proxys in einem Browser: `http://<IP_des_Pi>:8080/dashboard`.
2. Klicken Sie neben der gewählten Rolle auf **Generate**. Der Schlüssel wird erzeugt, im Ordner `key` gespeichert und aktiviert.
3. Tragen Sie unter **Setup Vehicle** die **VIN** des Fahrzeugs ein (17 Zeichen, sichtbar unten auf dem Hauptbildschirm der Tesla-App).
4. **Wecken Sie das Fahrzeug**: Öffnen Sie die Tesla-App auf Ihrem Smartphone oder öffnen Sie eine Tür. Das Senden des Schlüssels schlägt fehl, wenn das Auto schläft.
5. Klicken Sie auf **Send key**.
6. Legen Sie im Auto Ihre **Schlüsselkarte** auf die Mittelkonsole, an die Stelle, an der das Smartphone gelesen wird. Vor dieser Geste erscheint auf dem Bildschirm keine Meldung.
7. Bestätigen Sie auf dem Bildschirm des Fahrzeugs, falls eine Anfrage zum Hinzufügen eines Schlüssels erscheint.

### Die Kopplung prüfen

Öffnen Sie in einem Browser `http://<IP_des_Pi>:8080/api/1/vehicles/<VIN>/body_controller_state`. Eine JSON-Antwort mit `"result":true` bestätigt, dass der Proxy das Fahrzeug per Bluetooth mit seinem Schlüssel erreicht. Dieses Lesen **weckt** das Auto **nicht**.

## 9. Das Plugin konfigurieren

Der Proxy ist bereit: Fahren Sie mit der [Konfiguration des Plugins](index.md#konfiguration-des-plugins) fort. Einzutragen ist die URL `http://<IP_des_Pi>:8080/`. Die Schaltfläche **Testen** der Konfigurationsseite muss die Version des Proxys anzeigen.

Fügen Sie anschließend pro Fahrzeug ein Gerät mit seiner VIN hinzu, wie unter [Konfiguration der Geräte](index.md#konfiguration-der-gerate) beschrieben.

## 10. Wartung

| Aktion | Befehl (im Ordner `~/TeslaBleHttpProxy`) |
|---|---|
| Die Protokolle des Proxys ansehen | `docker logs --since 12h tesla-ble-http-proxy` |
| Den Proxy aktualisieren | Siehe [Das Proxy-Image aktualisieren](#das-proxy-image-aktualisieren) |
| Das Image der in `docker-compose.yml` eingetragenen Version herunterladen | `docker compose pull` |
| Das Fork-Image manuell herunterladen | `docker pull ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2` (Nummer ersetzen) |
| Den Proxy neu starten | `docker compose restart` |
| Den Raspberry Pi neu starten | `sudo reboot` |

> **Astuce**
>
> **Sichern Sie den Ordner `~/TeslaBleHttpProxy/key`** auf einem anderen Gerät, zum Beispiel mit `scp -r <Benutzer>@<IP_des_Pi>:TeslaBleHttpProxy/key .` von Ihrem Computer aus. Fällt die microSD-Karte aus, genügt es, neu zu installieren und diesen Ordner wieder einzufügen, ohne die Kopplung zu wiederholen.

### Vom wimaha-Image zum Fork-Image wechseln

Wenn Ihr Proxy bereits mit dem Image `wimaha/tesla-ble-http-proxy` läuft, wechseln Sie das Image **ohne erneute Kopplung**: Der Schlüssel bleibt im Ordner `key`, den der neue Container unverändert übernimmt.

1. Verbinden Sie sich per SSH mit dem Raspberry Pi und wechseln Sie in den Ordner des Proxys:

   ```
   cd ~/TeslaBleHttpProxy
   ```

2. Öffnen Sie die Datei: `nano docker-compose.yml`. Ändern Sie **nur** die Zeile `image:`:

   ```yaml
       image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2
   ```

   Ändern Sie weder `volumes` noch den Rest. Speichern Sie mit `Ctrl + X`, dann `Y` und `Enter`.
3. Laden Sie das neue Image herunter und starten Sie den Proxy neu:

   ```
   docker compose pull && docker compose up -d
   ```

   Der Download kann auf einem Raspberry Pi Zero 2 W mehrere Minuten dauern.
4. Prüfen Sie in einem Browser `http://<IP_des_Pi>:8080/api/proxy/1/version`: Die Antwort muss `"flavor":"superdcat"` und die Version `2.3.0-tb.2` enthalten.
5. Öffnen Sie auch `http://<IP_des_Pi>:8080/api/proxy/1/capabilities`: Die Antwort listet die Befehle und Daten des Proxys auf, und `key_role` gibt die Rolle Ihres Schlüssels an (`owner` oder `charging_manager`). Ist `key_role` leer, wird kein Schlüssel erkannt: Prüfen Sie, ob der Ordner `key` korrekt eingebunden ist.
6. Klicken Sie in Jeedom in der Konfiguration des Plugins auf **Testen**: Es zeigt die Version des Proxys an. Am Plugin und an evcc ist sonst nichts zu ändern.

**Zurückwechseln**: Setzen Sie die Zeile `image: wimaha/tesla-ble-http-proxy` wieder in `docker-compose.yml` ein und führen Sie dann `docker compose pull && docker compose up -d` aus. Der Schlüssel im Ordner `key` funktioniert mit beiden Images.

### Das Proxy-Image aktualisieren

> **IMPORTANT**
>
> Ein **Neustart des Raspberry Pi**, `docker compose restart` oder `restart: always` **aktualisieren das Image nicht**: Docker startet das bereits heruntergeladene Image neu. Eine Aktualisierung ist immer eine bewusste Handlung (Option 1) oder eine von Ihnen eingerichtete geplante Aufgabe (Option 2).

**Option 1 (empfohlen): eine genaue Versionsnummer, manuelle Aktualisierung**

Der Proxy steuert Ihr Auto. Eine unkontrollierte Aktualisierung kann ein Verhalten zum falschen Zeitpunkt ändern (zum Beispiel eine geplante Ladung, die nicht mehr startet), und der Download dauert auf einem Raspberry Pi Zero 2 W mehrere Minuten. Behalten Sie daher einen genauen Tag in `docker-compose.yml` bei (`image: ghcr.io/superdcat/tesla-ble-http-proxy:2.3.0-tb.2`) und aktualisieren Sie, wann Sie es entscheiden:

1. Lesen Sie die Hinweise zur neuen Version auf der Seite der [Fork-Versionen](https://github.com/superdcat/TeslaBleHttpProxy/releases).
2. Ändern Sie auf dem Raspberry Pi in `~/TeslaBleHttpProxy` die Versionsnummer am Ende der Zeile `image:` (`nano docker-compose.yml`).
3. Führen Sie `docker compose pull && docker compose up -d` aus.
4. Prüfen Sie `http://<IP_des_Pi>:8080/api/proxy/1/version`: Die angezeigte Version muss die neue sein. Der Ordner `key` bleibt erhalten, es ist keine neue Kopplung nötig.

**Option 2 (optional): `latest` und automatische nächtliche Aktualisierung**

Sie akzeptieren, dass der Proxy jeder neuen Version folgt, ohne dass Sie sie gelesen haben. Auf eigenes Risiko: Eine fehlerhafte Version installiert sich von selbst, und der Proxy ist während des Neustarts kurz unterbrochen (ein laufender Befehl kann fehlschlagen). Wenn Sie sich dafür entscheiden:

1. Setzen Sie in `docker-compose.yml` `image: ghcr.io/superdcat/tesla-ble-http-proxy:latest`.
2. Öffnen Sie die Tabelle der geplanten Aufgaben Ihres Benutzers: `crontab -e`.
3. Fügen Sie diese Zeile hinzu, die täglich um 4 Uhr morgens aktualisiert (ersetzen Sie `<Benutzer>` durch Ihren Benutzernamen: Der Pfad muss **absolut** sein):

   ```
   0 4 * * * cd /home/<Benutzer>/TeslaBleHttpProxy && docker compose pull -q && docker compose up -d && docker image prune -f
   ```

   `docker compose pull -q` lädt das neueste Image ohne Detailausgabe herunter, `docker compose up -d` startet den Proxy nur neu, wenn sich das Image geändert hat, und `docker image prune -f` löscht die alten Images, die die microSD-Karte belegen.
4. Speichern und beenden Sie. Prüfen Sie am nächsten Tag `http://<IP_des_Pi>:8080/api/proxy/1/version`.

Um zu Option 1 zurückzukehren, löschen Sie die Zeile aus `crontab -e` und setzen Sie wieder eine genaue Versionsnummer ein.

## 11. Sicherheit

- Standardmäßig hat der Proxy **weder Passwort noch Verschlüsselung**: Jeder, der Zugang zu Ihrem lokalen Netzwerk hat, kann ihm Befehle senden. Der Fork kann ein Token verlangen (`apiToken`): Aktivieren Sie es und tragen Sie es in der Konfiguration des Plugins ein (siehe [Optionale Einstellungen](#optionale-einstellungen)). Das Token wird im Netzwerk im Klartext übertragen: Es ergänzt die Isolierung des Netzwerks, es ersetzt sie nicht.
- Öffnen Sie den Port 8080 **niemals** zum Internet (keine Portweiterleitung im Router).
- Wenn Ihr Router es erlaubt, stellen Sie den Raspberry Pi in ein isoliertes Netzwerk, in dem nur Jeedom ihn erreichen darf.
- Bevorzugen Sie einen **Charging-Manager**-Schlüssel, wenn Sie nur das Laden steuern.
- Ändern Sie das Standardpasswort jedes Geräts in diesem Netzwerk und halten Sie den Raspberry Pi aktuell (`sudo apt-get update && sudo apt-get upgrade`).

## 12. Fehlerbehebung

| Symptom | Wahrscheinliche Ursache | Was zu tun ist |
|---|---|---|
| `usermod: group 'docker' does not exist` (Schritt 6) | Die Docker-Installation ist nicht vollständig durchgelaufen: Die Engine ist nicht installiert, nur der Client | Prüfen Sie den Speicherplatz mit `df -h /`: Das Root-Dateisystem muss fast die ganze Karte belegen. Führen Sie `sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin` erneut aus und lesen Sie den Fehler. Wenn `df` nach der Vergrößerung bei etwa 2 GB bleibt oder `dmesg` `I/O error` auf `mmcblk0` zeigt, ist die Karte defekt: Ersetzen Sie sie. |
| Die Seite `/api/proxy/1/version` öffnet sich nicht | Proxy gestoppt, falsche IP oder falscher Port | `docker ps` muss `tesla-ble-http-proxy` auflisten; andernfalls `docker compose up -d`. Prüfen Sie die IP im Router. |
| `bluetoothctl list` zeigt nichts an | Bluetooth des Raspberry Pi nicht verfügbar | `sudo reboot`. Prüfen Sie die Stromversorgung (5 V / 2,5 A). |
| „Vehicle is not in range“ oder Fahrzeug wird nicht immer gefunden | Bluetooth-Reichweite unzureichend | Rücken Sie den Raspberry Pi näher heran, vermeiden Sie das Metallgehäuse, erhöhen Sie `scanTimeout`. |
| Das Senden des Schlüssels bewirkt nichts | Fahrzeug schläft oder Schlüsselkarte nicht aufgelegt | Wecken Sie das Auto, senden Sie den Schlüssel erneut, legen Sie die Karte auf die Konsole. |
| Einige Befehle werden abgelehnt | Schlüssel **Charging Manager** | Normal für Verriegelung, Hupe, Licht, Wächter-Modus und Klimatisierung: Erzeugen Sie bei Bedarf einen **Owner**-Schlüssel. |
| Regelmäßige Aussetzer nach einigen Stunden | WLAN im Energiesparmodus, schwaches Netzteil oder eingefrorener Bluetooth-Adapter | Deaktivieren Sie das WLAN-Energiesparen, wechseln Sie das Netzteil, starten Sie den Proxy neu. |
| Unterbrochene Verbindungen mit dem Auto | Zu viele verbundene Bluetooth-Geräte | Das Fahrzeug akzeptiert **3 gleichzeitig verbundene Geräte** (Smartphones, Uhr, Proxy). |
| Der Container startet in einer Schleife neu (`docker ps`: „Restarting“), das Plugin zeigt **Proxy nicht erreichbar**; `docker logs tesla-ble-http-proxy` meldet `Cannot start with this Bluetooth adapter` | `btAdapter` ungültig (etwas anderes als `hci0` bis `hci15` in Kleinbuchstaben) oder Adapter fehlt / lässt sich nicht öffnen | Korrigieren Sie den Wert oder entfernen Sie die Zeile `btAdapter`, dann `docker compose up -d`. Den Namen des Adapters finden Sie mit `bluetoothctl list` oder `hciconfig -a`. |
| Alle Lesevorgänge und Befehle schlagen mit **„API-Token vom Proxy abgelehnt“** fehl (letzter Fehler, Befehl); **Testen** zeigt „Der Proxy verlangt einen API-Token“ oder „API-Token vom Proxy abgelehnt“ | `apiToken` ist in `docker-compose.yml` gesetzt, und das Plugin hat kein oder ein anderes Token | Tragen Sie unter **API-Token des Proxys** genau den Wert von `apiToken` ein, **Speichern**, dann **Testen**. |
| **„Befehl vom Fahrzeug abgelehnt: invalid request body: …“** | Der Fork-Proxy hat den Inhalt des Befehls (fehlender Schlüssel, falscher Typ, Wert außerhalb der Grenzen) vor dem Senden abgelehnt | Das Plugin prüft seine Werte vor dem Senden: Wenn das passiert, notieren Sie den Text nach dem Doppelpunkt (er nennt den Schlüssel) und melden Sie ihn zusammen mit dem Plugin-Protokoll im Debug-Modus. |
| **„Dieser Befehl erfordert einen Schlüssel mit der Rolle Owner: Der Proxy-Schlüssel hat wahrscheinlich die Rolle Charging Manager…“** oder Info **Schlüsselrolle** auf **Charging Manager** | Der Schlüssel hat die Rolle **Charging Manager** | Erzeugen und koppeln Sie einen **Owner**-Schlüssel (siehe [Die Rolle des Schlüssels wählen](#die-rolle-des-schlussels-wahlen)). Die Rolle des aktiven Schlüssels steht in `key_role` unter `http://<IP_des_Pi>:8080/api/proxy/1/capabilities`. |
| Das Fahrzeug wird nach der Installation einer anderen Bluetooth-Software nicht mehr gefunden | Diese Software belegt den Adapter | Der Proxy braucht den Adapter für sich allein: Entfernen Sie den anderen Bluetooth-Dienst von diesem Raspberry Pi. |

## Referenzen

- [TeslaBleHttpProxy, Fork von superdcat](https://github.com/superdcat/TeslaBleHttpProxy): der für das Plugin empfohlene Proxy (README auf Englisch: Befehle, Daten, Fehlerbehebung).
- [Umgebungsvariablen des Forks](https://github.com/superdcat/TeslaBleHttpProxy/blob/main/docs/environment_variables.md) (auf Englisch): Details zu den optionalen Einstellungen.
- [Versionen des Forks](https://github.com/superdcat/TeslaBleHttpProxy/releases): Hinweise und Binärdateien jeder Version.
- Docker-Image `ghcr.io/superdcat/tesla-ble-http-proxy`: Image des Forks, veröffentlicht in der GitHub-Registry (`ghcr.io`).
- [TeslaBleHttpProxy von wimaha](https://github.com/wimaha/TeslaBleHttpProxy): das ursprüngliche Projekt, als Alternative nutzbar.
- [Installationsanleitung des Proxys von wimaha](https://github.com/wimaha/TeslaBleHttpProxy/blob/main/docs/installation.md) (auf Englisch): Quelle der Schritte 6 bis 8.
- [Docker-Image `wimaha/tesla-ble-http-proxy`](https://hub.docker.com/r/wimaha/tesla-ble-http-proxy): Image der wimaha-Alternative.
- [Offizielles Tesla-SDK `vehicle-command`](https://github.com/teslamotors/vehicle-command): die Bibliothek, auf der der Proxy beruht (Schlüssel, Rollen, Bluetooth-Protokoll).
- [Raspberry Pi Imager](https://www.raspberrypi.com/software/): Vorbereitung der microSD-Karte.
- [Produktseite des Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/): Merkmale und empfohlenes Netzteil.
- [Installation von Docker unter Debian](https://docs.docker.com/engine/install/debian/): Docker-Dokumentation, gültig für Raspberry Pi OS 64 Bit (das Skript `get.docker.com` aus Schritt 6 automatisiert sie).
