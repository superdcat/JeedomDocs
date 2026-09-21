# IMOU-Plugin

Das **IMOU**-Plugin steuert Ihre IMOU-Kameras von Jeedom aus über die **IMOU Open API** (Cloud), **in nativem PHP**
(ohne Daemon, ohne Python). Je nach den Fähigkeiten jeder Kamera: Ein-/Ausschalten, Überwachung, PTZ,
Scheinwerfer/Sirene, Nachtsicht, Bildeinstellungen, Live-Stream, Vorschaubild, Neustart, Batterie, Türklingel
& Türöffnung, Alarmmeldungen, SD-Karten- und Cloud-Abonnementstatus, Supervision.

> Die IMOU-API bietet keine Echtzeit-Benachrichtigungen: Der Kamerastatus wird durch
> **periodische Abfrage** (Polling) aktualisiert. Eine Änderung, die über die IMOU-Anwendung
> vorgenommen wurde, kann daher einige Minuten brauchen, bis sie in Jeedom erscheint.

## Voraussetzungen

- Ein **IMOU-Entwicklerkonto** auf [open.imoulife.com](https://open.imoulife.com).
- Eine in der Entwicklerkonsole erstellte Anwendung, die eine **`appId`** und ein **`appSecret`** bereitstellt, mit
  dem Integrationsmodus **`accessType = PaaS`** (erforderlich zur Gerätesteuerung).
- Ihre Kameras müssen bereits über die **IMOU Life**-Anwendung mit diesem Konto verknüpft sein.
- **`ffmpeg`**: wird **automatisch** von Jeedom bei der Plugin-Aktivierung installiert (Reiter „Abhängigkeiten").
  Es dient zum Extrahieren von Frames aus dem Live-Stream. Bei einer Docker-Installation prüfen Sie, ob `ffmpeg`
  im Image verfügbar ist.

> ℹ️ **Anzahl steuerbarer Geräte (kostenloser Tarif).** Theoretisch ist das kostenlose IMOU-Entwicklerkonto
> auf **~5 Geräte** begrenzt: darüber hinaus *sollten* Befehle mit einem **Lizenzfehler** von IMOU
> fehlschlagen (dies ist keine Plugin-Einschränkung). **In der Praxis scheint IMOU die Steuerung von mehr
> Kameras** im kostenlosen Tarif zuzulassen – in unseren Tests funktioniert alles normal über 5 hinaus.
> Dieses Verhalten hängt von IMOU ab und kann sich ohne Vorankündigung ändern: Wenn ein Befehl schließlich
> einen Lizenzfehler zurückgibt, gilt dieses Limit, und dann ist ein geeignetes IMOU-Angebot erforderlich.
> In jedem Fall werden die Kameras entdeckt und angezeigt; nur ihre Befehle wären betroffen.

## Konfiguration des Plugins

1. Aktivieren Sie das Plugin (Plugins → Plugin-Verwaltung → IMOU) und lassen Sie Jeedom die Abhängigkeiten installieren.
2. Geben Sie in der Plugin-Konfiguration Folgendes ein:
   - **App ID**: die Kennung Ihrer IMOU-Anwendung;
   - **App Secret**: das zugehörige Geheimnis (**verschlüsselt gespeichert**, niemals im Klartext angezeigt);
   - **Datacenter**: die Region Ihres Kontos (standardmäßig Europa).
3. Klicken Sie auf **Verbindung testen**, um Ihre Zugangsdaten zu überprüfen.

### Erweiterte Einstellungen (optional)

- **API-Aufruf-Kontingent**: `quotaMensuel` (monatliches API-Aufruf-Limit, ~30.000 beim kostenlosen Tarif),
  Warnschwelle. Das Kontingent wird **am 1. jedes Monats zurückgesetzt**. Das Plugin **zählt seine
  Aufrufe** und warnt Sie bei Annäherung an das Limit.
- **Automatische Frequenzregulierung**: Grenzen `refreshIntervalMin`/`refreshIntervalMax`. Das Plugin
  passt die Aktualisierungsfrequenz automatisch an, um innerhalb des monatlichen Aufrufbudgets zu bleiben.
- **Gleichzeitige Live-Streams**: `liveMaxConcurrent` (Anzahl gleichzeitig angezeigter Live-Streams).
- **Datenschätzung**: `dataQuotaGo` / `dataBitrateKbps` (siehe „Kontingent & Supervision").

## Kameras hinzufügen

- Klicken Sie auf **Synchronisieren**: Das Plugin ruft die Kameras des Kontos ab und erstellt **ein Gerät pro
  Kamera** (eines pro Kanal bei Mehrkanalgeräten).
- Benennen Sie die Geräte um und ordnen Sie sie wie gewohnt Ihren Objekten zu: **Ihre Anpassungen bleiben**
  bei den folgenden Synchronisierungen **erhalten**.
- **Selektive Synchronisierung**: Jeder Statusbefehl kann vom automatischen Refresh ausgeschlossen werden
  (Kontrollkästchen „Vom automatischen Refresh ausschließen"), um Aufrufe für nicht benötigte Befehle zu sparen.

> 💡 **Befehle sind abhängig von den Fähigkeiten der Kamera.** Das Plugin erstellt nur Befehle,
> die tatsächlich von jedem Modell unterstützt werden. Wenn ein Befehl (PTZ, Sirene, Nachtsicht, SD-Karte…)
> **nicht erscheint**, deklariert Ihre Kamera diese Fähigkeit nicht — das ist **normal**, kein Fehler.

## Verfügbare Befehle (je nach Kamera)

- **Ein- / Ausschalten** der Kamera.
- **Überwachung** (Bewegungserkennung): aktivieren / deaktivieren.
- **Scheinwerfer / Licht** und **Sirene** (bei kompatiblen Modellen, über das IoT-Modell „Things").
- **PTZ**: Richtungsfeld (oben/unten/links/rechts) und Zoom bei motorisierten Kameras.
- **Nachtsicht**: Modus (automatisch / Infrarot / Farbe je nach Modell).
- **Bildeinstellungen**: Spiegelung, WDR, Datum-/Uhrzeit-Einblendung (OSD), LED-Anzeige…
- **Live-Stream**: aktualisiertes Live-Bild, **per Klick im Vollbild anzeigbar**.
- **Vorschaubild** der Kamera (Quelle nach Wahl: Live-Schnappschuss oder Cover-Bild).
- **Modell (Code)**: technischer Code der Kamera, als **schreibgeschütztes Feld** in der
  Gerätekonfiguration angezeigt (neben der Kennung), nicht als Befehl.
- **Neustart** des Geräts (Aktion mit Bestätigungsabfrage).
- **Batterie & Aufwecken**: Batteriestand (wird in der Jeedom-Gesundheitsüberwachung angezeigt); schlafende Geräte
  werden zum Lesen ihres Zustands aufgeweckt.
- **Video-Türklingel & Türöffnung** (bei kompatiblen Schlössern/Türklingeln; Öffnung mit Bestätigungsabfrage).
- **Alarme & Erkennung**: letztes Ereignis (Bewegung/Mensch), Erkennungs-**empfindlichkeit**, **Schärfungspläne**
  (Tag/Nacht/Permanent-Voreinstellungen), **Personen-/KI-Erkennung**.
- **SD-Karte**: Vorhandensein, Belegung, Kapazität und **Formatierung** (Aktion mit Bestätigungsabfrage).
- **Cloud-Aufzeichnung**: Abonnementstatus (aktiv, Ablauf, Tarif). **Standardmäßig deaktiviert**
  (Option zum Aktivieren, wenn Sie ein Abonnement haben — siehe unten).
- **Online (Status)**: Erreichbarkeit der Kamera, auch zum Einsparen von Aufrufen genutzt (eine offline Kamera wird nicht abgefragt).

### Cloud-Abonnement-Überwachung aktivieren

Die Cloud-Befehle werden standardmäßig **ausgeblendet und nicht abgefragt** (die meisten Konten haben
kein Abonnement). Wenn Sie ein Cloud-Abonnement haben: Machen Sie den Befehl **Cloud aktiv** sichtbar und
deaktivieren Sie dessen Kontrollkästchen „Vom automatischen Refresh ausschließen", um die Überwachung zu aktivieren (einmal pro Stunde geprüft).

## Das „Kamera-Wall"-Panel

Das Plugin fügt dem Jeedom-Menü eine **eigene Seite** hinzu, die ein Raster der Live-Streams Ihrer Kameras anzeigt (mit
PTZ, Sirene, Scheinwerfer je nach Modell). Aktivieren Sie es in der **Plugin-Verwaltung** (Kontrollkästchen „Desktop-Panel anzeigen"),
und wählen Sie dann pro Kamera, ob sie auf der Wall erscheinen soll (Kontrollkästchen „Im Kamera-Panel sichtbar" am Gerät).

## Aktualisierung, Kontingent & Supervision

Das Plugin fragt die IMOU-Cloud periodisch ab (Cron). Zwei **getrennte** Budgets sind zu beachten:

- **API-AUFRUF-Kontingent** (~30.000/Monat beim kostenlosen Tarif): **exakt gezählt** vom Plugin. Die
  Aktualisierungsfrequenz wird **automatisch reguliert**, um innerhalb dieses Budgets zu bleiben, und eine Warnung wird
  bei Annäherung an das Limit ausgegeben. „Langsame" Zustände (SD-Karte, Cloud-Abonnement) werden mit
  niedriger Frequenz aktualisiert (einmal pro Stunde) — und Cloud-Abonnement wird nur abgefragt, wenn Sie es aktiviert haben
  (siehe „Cloud-Abonnement-Überwachung aktivieren").
- **DATEN-Kontingent** (Live-Stream-Volumen, ~3 GB/Monat beim kostenlosen Tarif): Das Plugin liefert eine
  **Schätzung** (Betrachtungszeit × konfigurierte Bitrate `dataBitrateKbps`, verglichen mit `dataQuotaGo`).
  Dies ist ein **informativer Indikator**: Der **tatsächliche** Wert ist im **IMOU-Entwicklerportal** zu finden,
  das maßgeblich ist. Die IMOU-API stellt den tatsächlichen Datenverbrauch nicht bereit.

Der **Gesundheits**-Bildschirm des Plugins fasst die Kamera-Erreichbarkeit, das Aufrufkontingent, die regulierte Aktualisierungsfrequenz und
die Datenschätzung zusammen.

## Datenschutz & Datenstandort

**Video-Streams** und **Befehle** werden über die **IMOU-Cloud-Server** übertragen (Rechenzentrum entsprechend Ihrer
Region — wählen Sie „Europa" für Frankreich). **Kein Video läuft über Jeedom**: Das Plugin sendet
Steuerungsbefehle und empfängt Statusmetadaten sowie aus dem Live-Stream extrahierte Bilder.

## Fehlerbehebung

- **Synchronisierung findet keine Kameras** → prüfen Sie `appId`/`appSecret`/`Datacenter`, den
  **Verbindung testen**-Button, und dass Ihre Kameras in der IMOU Life-Anwendung korrekt mit dem Konto verknüpft sind.
- **Ein Befehl existiert nicht bei meiner Kamera** → die Fähigkeit wird von diesem Modell nicht unterstützt. Das ist normal.
- **Der Live-Stream wird nicht angezeigt** → prüfen Sie, ob die Plugin-**Abhängigkeiten** installiert sind (`ffmpeg`),
  ob die Kamera online ist, und konsultieren Sie die `imou`-Logs auf *debug*-Ebene.
- **Befehle schlagen mit Lizenzfehler fehl** → Sie erreichen möglicherweise das Limit steuerbarer Geräte
  des kostenlosen IMOU-Tarifs (theoretisch ~5, in der Praxis erlaubt IMOU jedoch oft mehr; siehe
  Voraussetzungen). Dann ist ein geeignetes IMOU-Angebot erforderlich – dies ist keine Plugin-Einschränkung.
- **„Uhr nicht synchronisiert" / Signaturfehler** → synchronisieren Sie die Uhr des Jeedom-Servers (NTP):
  eine Abweichung von mehr als 5 Minuten führt dazu, dass IMOU-Anfragen abgelehnt werden.
- **Eine Änderung in der IMOU-App erscheint nicht sofort** → normal, die Aktualisierung erfolgt
  periodisch (keine Echtzeit-Benachrichtigung).

## Bekannte Einschränkungen

- **Keine Echtzeit-Alarme (Push)**: Ereignisse werden durch periodische Abfrage gemeldet, nicht
  durch sofortige Benachrichtigung.
- **Keine Wiedergabe von Aufzeichnungen**: Die IMOU-API stellt keine Wiedergabe-URLs für aufgezeichnete Videos
  (SD oder Cloud) bereit; die Wiedergabe erfolgt in der IMOU-Anwendung.
- **Kein kommerzieller Modellname**: Es wird nur der technische Modellcode angezeigt (es gibt keine zuverlässige
  Zuordnungsdatenbank Code → kommerzieller Name).
- **Erkennungszonen, Firmware-Updates, Gerätezuordnung/-umbenennung auf IMOU-Seite**: nicht verwaltet.

## Deinstallation

Das Deaktivieren und anschließende Entfernen des Plugins in Jeedom entfernt die Geräte und ihre Befehle. Ihre
**IMOU-Zugangsdaten** (`appId`/`appSecret`) bleiben auf Ihrem IMOU-Entwicklerkonto **gültig** und können
wiederverwendet werden; sie werden durch diesen Vorgang auf der IMOU-Seite nicht gelöscht.
