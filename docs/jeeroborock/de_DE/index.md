# JeeRoborock

JeeRoborock steuert Ihre Roborock-Saugroboter von Jeedom aus über die Roborock-Cloud: Status in
Echtzeit, Reinigungsbefehle, Feinsteuerung (Saugleistung, Wasser, Route, Wartung der Station),
Reinigung nach Raum oder Zone, mehrere Karten sowie die Ausführung der in der Roborock-App
festgelegten Routinen („Routinen“).

## Was das Plugin tut, und was nicht

- Die Steuerung läuft über die **Roborock-Cloud**: Jeedom muss Internetzugang haben, und Ihr Roboter
  muss mit Ihrem Netzwerk und der Roborock-Cloud verbunden sein, um zu antworten. Einige Vorgänge
  hängen zwingend von der Cloud ab und **funktionieren nicht ohne Internet**: die Anmeldung am Konto,
  die Bestandsaufnahme der Roboter, die Ausführung der Routinen, das Lesen der Zeitpläne und das
  Abrufen des Roboterfotos.
- Die vom Plugin verwendete Bibliothek **kann**, wenn sich Ihr Roboter im selben lokalen Netzwerk wie
  Jeedom befindet, eine direkte Verbindung zum Gerät versuchen, um bestimmte Abläufe zu beschleunigen.
  Dieses Verhalten ist von Jeedom aus weder einstellbar noch abschaltbar, und es ändert nichts an den
  obigen Punkten: Das Plugin bleibt für seine Funktion von der Roborock-Cloud abhängig.
- Das Plugin richtet sich an Roboter, die mit dem **V1**-Protokoll von Roborock kompatibel sind. Das
  Referenzgerät, auf dem alles getestet wird, ist der **Roborock Qrevo Curv**. Andere V1-Roboter
  können funktionieren, aber ihre verfügbaren Befehle hängen von den Fähigkeiten ab, die der Roboter
  selbst meldet — siehe weiter unten.
- Ein Roboter, der von einem anderen Roborock-Konto mit Ihnen **geteilt** wurde, erscheint normal in
  der Liste, aber bestimmte Aktionen können ihm von der Roborock-Cloud verweigert werden.

## Voraussetzungen und Installation

1. **Jeedom mindestens 4.2**, installiert auf einem Server mit **Debian 12 oder 13**. Diese
   Debian-Version wird benötigt, damit die Abhängigkeit des Plugins funktioniert; darunter (z. B.
   Debian 11) wird die Aktivierung des Plugins verweigert.
2. Lassen Sie Jeedom von der Plugin-Seite aus seine Python-Abhängigkeit installieren. Die
   Abhängigkeitsanzeige der Seite „Plugins“ wird grün, sobald die Installation abgeschlossen ist;
   rechnen Sie je nach Rechner mit bis zu etwa 15 Minuten.
3. **Aktivieren Sie das Plugin** und starten Sie anschließend seinen Daemon (die Oberfläche tut dies
   bei der Aktivierung automatisch). Ohne gestarteten Daemon kann sich das Plugin weder mit Roborock
   verbinden noch den Status eines Roboters auslesen: Die Konfigurationsseite zeigt dies mit „Der
   Daemon antwortet nicht“ an.

## Ihr Roborock-Konto verknüpfen

Die Authentifizierung erfolgt über einen **per E-Mail gesendeten Einmalcode**: Es gibt kein
Passwortfeld, und das Passwort Ihres Roborock-Kontos wird nie abgefragt oder gespeichert.

Auf der Konfigurationsseite des Plugins (Menü Plugins > JeeRoborock > Konfiguration):

1. Tragen Sie Ihre **E-Mail-Adresse** des Roborock-Kontos in das Feld „E-Mail des Roborock-Kontos“ ein.
2. **Speichern Sie die Konfiguration** (Speicherschaltfläche der Seite), bevor Sie einen Code
   anfordern: Genau dieser gespeicherte Wert wird vom Daemon verwendet.
3. Klicken Sie auf **„Code senden“**. Roborock sendet Ihnen einen numerischen Code per E-Mail (bis zu
   12 Zeichen).
4. Geben Sie diesen Code in das vorgesehene Feld ein und klicken Sie auf **„Code bestätigen“**.
5. Der Kontostatus wechselt von „Roborock-Konto nicht verknüpft“ zu „Roborock-Konto verknüpft“.

Eine Schaltfläche **„Verbindung testen“** ermöglicht es, jederzeit zu prüfen, ob die gespeicherte
Sitzung noch gültig ist, ohne Ihr Verbindungskontingent zu verbrauchen.

Was das Plugin speichert: Ihre E-Mail-Adresse und ein verschlüsseltes Sitzungstoken (das bei der
Codebestätigung von Roborock ausgestellt wird). Das Passwort Ihres Kontos, die roboterspezifischen
Schlüssel und die rohen Sitzungstoken verlassen den Daemon nie und sind von der Jeedom-Oberfläche aus
nie sichtbar.

### Lokaler Kanal mit dem Daemon

Das Feld **„Port des lokalen Kanals“** (standardmäßig 61350) ist der TCP-Port, der auf der
Jeedom-Maschine selbst für die Kommunikation mit dem Daemon verwendet wird. Ändern Sie ihn nur bei
einem Konflikt mit einer anderen auf demselben Server installierten Software. Die Schaltfläche
**„Kanal prüfen“** bestätigt, dass der Daemon antwortet und dass der Rückkanal zu Jeedom (spontane
Aktualisierungen) funktioniert.

## Synchronisierung der Geräte

Die Schaltfläche **„Geräte synchronisieren“** auf der Startseite des Plugins fragt Ihr
Roborock-Konto ab, um Ihre Roboter zu erkennen und die entsprechenden Jeedom-Geräte zu erstellen.

Dies ist **kein** Aktualisierungsbutton: Die Bestandsaufnahme der mit Ihrem Konto verknüpften Roboter
unterliegt einem streng begrenzten, mit der mobilen App geteilten Roborock-Kontingent (siehe weiter
unten). Klicken Sie diese Schaltfläche nur an, wenn Sie einen Roboter zu Ihrem Roborock-Konto
hinzufügen oder daraus entfernen, nicht um den Status eines bereits bekannten Roboters zu
aktualisieren — dieser Status aktualisiert sich von selbst (siehe „Echtzeit und Aktualität“).

Ein von einem anderen Konto geteilter Roboter wird durch ein Etikett **„Geteilter Roboter“** auf
seiner Karte in der Geräteliste kenntlich gemacht.

Diese Schaltfläche synchronisiert **nicht** die Routinen: Ein neu erkannter Roboter hat noch keine.
Die Routinen werden Roboter für Roboter über das Panel **„Routinen“** im Reiter „Gerät“
synchronisiert (Schaltfläche „Routinen synchronisieren“, siehe „Routinen („Routinen“)“ unten).

Ein Roboter entspricht immer nur **einem einzigen Jeedom-Gerät**: Die Konfigurationsseite eines
JeeRoborock-Geräts bietet nicht die native Schaltfläche „Duplizieren“ an, und jeder Versuch, ein
zweites Gerät für einen bereits bekannten Roboter zu erstellen (auch auf anderem Weg als über die
Oberfläche, wie z. B. die API), wird verweigert, mit einer Meldung, die das vorhandene Gerät nennt.
Wurde vor dieser Schutzmaßnahme bereits ein Duplikat erstellt, wird es nicht automatisch gelöscht: Es
liegt an Ihnen, dasjenige der beiden zu löschen, das nicht mehr benötigt wird; eine Warnung wird
dazu im Protokoll des Plugins vermerkt, damit Sie es leichter erkennen können.

## Was ein Gerät enthält

Jeder Roboter wird zu einem Jeedom-Gerät. Die Liste der Befehle, die er trägt, **hängt von den
Fähigkeiten ab, die der Roboter tatsächlich meldet**: Zwei Roboter, auch mit ähnlichen Modellen, haben
nicht zwangsläufig genau dieselbe Liste. Ein fehlender Befehl bedeutet eine bei diesem Roboter nicht
erkannte Fähigkeit, keinen Fehler des Plugins.

### Allgemeine Informationen

Der Reiter „Gerät“ zeigt schreibgeschützt das Modell, die Firmware, die Protokollversion, die
Seriennummer, die Roborock-Kennung und den in der Roborock-App vergebenen Namen des Roboters an.
Diese Informationen stammen aus dem Roborock-Konto und werden bei der Gerätesynchronisierung
aktualisiert.

### Status und Grundsteuerung

| Befehl | Was er anzeigt oder tut |
|---|---|
| Status | Die aktuelle Statusbezeichnung des Roboters (reinigt, pausiert, im Fehler…) |
| Batterie | Ladestand in % |
| Reinigt | Ja/Nein |
| Fehler | Bezeichnung des aktuellen Fehlers, „Aucune“ (Keine) sonst |
| Gereinigte Fläche | In m², für die laufende Reinigung |
| Reinigungsdauer | In Minuten, für die laufende Reinigung |
| Fortschritt | In %, für die laufende Reinigung |
| Online / Verbunden | „Online“: Der Roboter hat auf das letzte Auslesen geantwortet (wechselt zu „offline“, sobald ein Auslesen mangels Antwort des Roboters fehlschlägt). „Verbunden“: Aktualität der Daten auf Plugin-Seite (Kanal mit dem Daemon) |
| Letzte Aktualisierung | Datum und Uhrzeit der zuletzt empfangenen Daten |
| Starten / Pausieren / Stoppen | Steuerung der Reinigung. „Starten“ **setzt** eine pausierte oder unterbrochene Reinigung **fort** (auch eine Reinigung nach Raum oder Zone), statt eine neue zu starten; ohne laufende Reinigung startet es eine vollständige Reinigung |
| Zurück zur Basis | Schickt den Roboter zum Laden zurück |
| Orten | Lässt den Roboter ein akustisches Signal ausgeben |
| Aktualisieren | Liest den Status des Roboters sofort erneut aus |

### Dockingstation, Verbrauchsmaterial und Wartung

Diese Befehle erscheinen **nur, wenn Ihre Station dies zulässt**:

- Status der Staubentleerung, der Wischmopp-Wäsche und -Trocknung, Stationsfehler, Wassermangel.
  Wird der von der Station gemeldete Fehlercode nicht erkannt, lautet die angezeigte Bezeichnung
  „Erreur de station non reconnue“ (Nicht erkannter Stationsfehler) (der Rohcode bleibt im
  Stationsfehlercode-Befehl sichtbar);
- entsprechende Aktionen: Wischmopp waschen, Wischmopp trocknen, Trocknen stoppen, Staubbehälter
  leeren — nur verfügbar, wenn der Roboter sich **an seiner Basis** befindet (auch beim Laden); außerhalb
  dieses Zustands verweigert das Plugin die Aktion mit einer expliziten Meldung.

Der Verschleiß der von Ihrem Roboter erkannten Verbrauchsmaterialien (Hauptbürste, Seitenbürste,
Filter, Sensoren, Wischwalze) wird als verbleibender Prozentsatz veröffentlicht, jeweils mit einer
Aktion „Zurücksetzen…“, die nach einem physischen Austausch zu verwenden ist. Diese Aktion verlangt
eine Bestätigung vor der Ausführung.

### Reinigungsprotokoll

Sieben schreibgeschützte Befehle informieren über die **letzte bekannte Reinigung**:

| Befehl | Was er anzeigt |
|---|---|
| Letzte Reinigung | Zusammenfassung in einer Zeile, z. B. „Terminé — 42 min, 31,5 m²“ (Abgeschlossen — 42 min, 31,5 m²); lautet „Aucun nettoyage connu“ (Keine bekannte Reinigung), solange keine Reinigung gemeldet wurde |
| Beginn der letzten Reinigung | Zeitstempel des Beginns (standardmäßig ausgeblendet) — als Einzige der sieben lässt er sich arithmetisch vergleichen, zu verwenden in einem Szenario wie „der Roboter war seit drei Tagen nicht mehr im Einsatz“ |
| Dauer der letzten Reinigung | In Minuten, auf die nächste Minute gerundet (Abweichung von bis zu ±30 s gegenüber der mobilen App möglich) |
| Fläche der letzten Reinigung | In m², auf 0,1 m² gerundet |
| Grund für das Ende der letzten Reinigung | Zum Beispiel „Terminé“ (Abgeschlossen) oder „Nettoyage interrompu“ (Reinigung unterbrochen) |
| Technischer Schlüssel für den Grund des Endes der letzten Reinigung | Stabiler technischer Wert zum Grund (standardmäßig ausgeblendet) — in einem Szenario der Bezeichnung vorzuziehen, um eine Bedingung zu prüfen |
| Fehler der letzten Reinigung | Bezeichnung des mit dieser Reinigung verbundenen Fehlers, „Aucune“ (Keine), wenn alles gut verlaufen ist |

Der Reiter „Gerät“ bietet außerdem ein Panel **„Reinigungsprotokoll“**, das die 10 letzten bekannten
Reinigungen auflistet (Beginn, Ende, Dauer, Fläche, Endgrund, Fehler), mit dem Datum der letzten
Synchronisierung. Eine Schaltfläche **„Protokoll aktualisieren“** liest diesen Verlauf erneut bei
Roborock aus:

- sie ist durch dieselbe Anti-Flut-Sperre von einer Minute geschützt wie die übrigen
  Resynchronisierungsbuttons des Plugins — zu frühes erneutes Klicken zeigt „Le journal vient d'être
  rafraîchi : patientez une minute avant de relancer.“ (Das Protokoll wurde gerade aktualisiert:
  Warten Sie eine Minute, bevor Sie es erneut versuchen.) an;
- die erste Aktualisierung liefert unter Umständen nur wenige Einträge und vervollständigt sich beim
  nächsten Klick: Das ist ein normales Verhalten, kein Ausfall, da der Abruf zeitlich begrenzt ist;
- das Protokoll aktualisiert sich auch von selbst am Ende jeder Reinigung, ohne Ihr Zutun.

Ist die Roborock-Cloud zum Zeitpunkt der Abfrage nicht erreichbar, bleiben die bereits bekannten Werte
der letzten Reinigung und des Verlaufs unverändert angezeigt — sie werden nie auf null zurückgesetzt.
Das Datum der letzten Synchronisierung des Panels zeigt an, ob die Daten noch aktuell sind.

### Kumulierte Statistiken

Vier schreibgeschützte Befehle informieren über die **globale** Nutzung Ihres Roboters seit seiner
Inbetriebnahme:

| Befehl | Was er anzeigt |
|---|---|
| Gesamte Reinigungsdauer | In Stunden, auf eine Nachkommastelle gerundet |
| Gesamte gereinigte Fläche | In m², auf eine Nachkommastelle gerundet |
| Gesamtzahl der Reinigungen | Ganzzahl |
| Gesamtzahl der Behälterentleerungen | Ganzzahl; erscheint nur, wenn Ihre Station den Behälter leeren kann |

Dies sind **kumulierte** Zähler, die vom Roboter selbst geführt werden, keine von Jeedom
durchgeführte Berechnung: Sie entsprechen dem, was die Roborock-App anzeigt. Im Gegensatz zu den
meisten anderen Befehlen des Plugins sind sie **standardmäßig historisiert**, damit Sie ohne vorherige
Einstellung eine Nutzungskurve über die Zeit verfolgen können.

Ihre Aktualisierung erfolgt automatisch: am Ende jeder Reinigung, und ansonsten höchstens einmal pro
Stunde. Es gibt keine Schaltfläche zu klicken und keine Auswirkung auf die Roborock-Kontingente — die
Daten kommen über denselben Kanal wie das obige Reinigungsprotokoll.

Wenn Sie diese Zähler von der Roborock-App aus zurücksetzen (oder nach einem Werksreset), folgen die
Jeedom-Befehle diesem Rückgang: Sie geben den Roboter getreu wieder und speichern kein Maximum. Ein
sichtbarer Einbruch im Verlauf nach einem solchen Zurücksetzen ist daher normal, keine Anomalie. Ist
ein Wert zum Zeitpunkt der Abfrage nicht verwertbar (Roboter nicht erreichbar, fehlerhafte Daten),
behält der Befehl einfach seinen vorherigen Wert, statt auf null zurückzufallen.

### App-Zeitpläne

Der Reiter „Gerät“ bietet ein Panel **„App-Zeitpläne“** in Form einer Tabelle (Wiederholung /
Wiederholt / Status). Diese Liste füllt sich nicht von selbst: Klicken Sie auf **„Zeitpläne lesen“**,
um sie zu befüllen. Ein Zeitstempel unter der Tabelle gibt das Datum des letzten Lesens an; ohne
vorherigen Klick lädt die Tabelle zum Klicken auf die Schaltfläche ein.

Jede Zeile entspricht einem in der Roborock-App erstellten Zeitplan und gibt an:

- seine **Wiederholung**, angezeigt **genau so, wie die Cloud sie liefert**, ohne Übersetzung in
  Wochentage oder eine lesbare Uhrzeit. Das ist kein Anzeigefehler: Die genaue Form dieser Information
  ist nicht garantiert je nach Robotermodell identisch, das Plugin gibt sie daher roh wieder, statt
  eine falsche Interpretation zu riskieren;
- ob er **wiederholt** wird oder nicht (Ja / Nein);
- ob er **Aktiv** oder **Deaktiviert** ist.

Dieses Lesen ist **nur lesend**: Keine Erstellung, Änderung oder Löschung eines Zeitplans ist von
Jeedom aus möglich. Alles wird in der Roborock-App verwaltet, die die einzige Referenzquelle bleibt.
Klicken Sie nach einer in der mobilen App vorgenommenen Änderung (Deaktivierung, Zeitänderung …)
erneut auf „Zeitpläne lesen“, um den aktuellen Stand auf Jeedom-Seite zu sehen — er aktualisiert sich
nicht von selbst.

Zwei Lesevorgänge innerhalb weniger als einer Minute zeigen eine Meldung an, die zum Warten auffordert:
Das ist kein Fehler, sondern derselbe Anti-Flut-Schutz wie bei den übrigen Resynchronisierungsbuttons
des Plugins.

Zeigt das Panel **„Programmations non disponibles pour ce robot“** (Zeitpläne für diesen Roboter nicht
verfügbar) an, ist das ein normales Ergebnis, kein Ausfall: Nicht alle Robotermodelle stellen diese
Information der Roborock-Cloud zur Verfügung. Der Rest des Plugins funktioniert in diesem Fall
weiterhin normal.

Verwechseln Sie diese Zeitpläne nicht mit den unten beschriebenen **Routinen („Routinen“)**: Die
Routinen sind auf Abruf von Jeedom aus ausführbare Reinigungsszenarien, die Zeitpläne sind
zeitgesteuerte, von der mobilen App verwaltete und hier nur einsehbare Auslösungen. Diese Zeitpläne
erzeugen keinen Befehl und können daher nicht in einem Jeedom-Szenario verwendet werden — das ist eine
Informationsanzeige, eine bewusste Entscheidung und kein Versehen.

## Routinen („Routinen“)

„Routinen“ sind die Reinigungsroutinen, die Sie in der Roborock-App erstellt haben. Einmal
synchronisiert, wird jede zu einem Aktionsbefehl am Gerät, der von Jeedom aus wie jeder andere Befehl
oder aus einem Szenario heraus ausgeführt werden kann.

Diese Routinen laufen über die Roborock-Cloud und funktionieren daher **auch, wenn der direkte Kanal
zum Roboter nicht verfügbar ist** — nur eine Internetverbindung auf Jeedom-Seite und ein Ihrem Konto
bekannter Roboter sind erforderlich.

### Das Panel „Routinen“

Der Reiter „Gerät“ eines Roboters enthält einen Abschnitt **„Routinen“** unter dem Block
„Roborock-Bestand“. Er zeigt an:

- die **Liste der Routinen, die Jeedom für diesen Roboter kennt**, eine pro Zeile; wurde der Name des
  Befehls in Jeedom angepasst, wird der ursprüngliche Name aus der Roborock-App in einer zweiten
  Spalte erinnert, um den Zusammenhang herzustellen;
- die Schaltfläche **„Routinen synchronisieren“** — dies ist der **einzige** Ort, an dem sie sich
  befindet, sie steht nicht mehr in der Werkzeugleiste der Seite;
- die **Synchronisierungsregel**, klar formuliert vor jedem Klick: Sie behält die in der App noch
  vorhandenen Routinen bei (gleiche Befehle, gleiche Szenarien), löscht die nicht mehr vorhandenen und
  fügt die neuen hinzu.

Ist noch keine Routine bekannt, weist das Panel explizit darauf hin, statt eine leere Liste
anzuzeigen: Starten Sie eine Synchronisierung, oder erstellen Sie zunächst eine Routine in der
Roborock-App.

Das Anzeigen dieses Panels löst weder einen Aufruf des Daemons noch der Roborock-Cloud aus: Die Liste
stammt aus dem, was Jeedom bereits weiß, ohne Kontingent zu verbrauchen.

### Was eine Synchronisierung tut

- **In der App noch vorhandene Routine** → nichts wird angerührt: gleicher Befehl, gleiche Kennung,
  identisch in einem Szenario verwendbar. Nur der Name folgt dem der App, falls dieser sich geändert
  hat — und nur, wenn Sie ihn nicht in Jeedom angepasst haben, in diesem Fall wird Ihr Name
  beibehalten.
- **Aus der App verschwundene Routine** (auf dem Handy gelöscht) → ihr Jeedom-Befehl wird **gelöscht**.
  ⚠️ Ein Szenario, das darauf verwiesen hat, verliert seinen Bezug, ohne dass Jeedom in diesem Moment
  eine Warnung ausgibt: Deshalb **nennt** der nach der Synchronisierung angezeigte Bericht jede
  gelöschte Routine, damit Sie wissen, was zu korrigieren ist.
- **Neue Routine in der App** → ein Befehl wird hinzugefügt, ohne die anderen zu berühren.

Ein Routinen-Befehl wird von Jeedom aus **nicht manuell** gelöscht: Blenden Sie ihn aus, wenn er Sie
stört, oder löschen Sie die entsprechende Routine in der App und starten Sie anschließend eine
Synchronisierung.

Zwei Synchronisierungen innerhalb weniger als einer Minute zeigen eine Meldung an, die zum Warten
auffordert: Das ist kein Fehler, sondern derselbe Anti-Flut-Schutz wie bei den übrigen
Resynchronisierungsbuttons des Plugins. Eine Synchronisierung ohne jegliche Änderung auf App-Seite ist
ein neutraler Vorgang und wird als solcher gemeldet („Aucun changement : vos usages sont déjà à jour.“
– Keine Änderung: Ihre Routinen sind bereits aktuell.).

Ist die von der Roborock-Cloud empfangene Liste **unvollständig** (abgeschnittene Antwort, oder mehr
als 64 Routinen bei diesem Roboter), wendet die Synchronisierung trotzdem die Hinzufügungen und
Umbenennungen an, **löscht aber nichts**: Vorsichtshalber wird eine unvollständige Liste nie als
„diese Routinen sind verschwunden“ interpretiert.

Wenn Sie das Plugin von einer älteren Version aktualisieren, die bestimmte Routinen als „veraltet“
markierte, löscht die erste darauffolgende Synchronisierung sie wie jede in der App nicht mehr
vorhandene Routine — keine Routine kann mehr dauerhaft in diesem Zustand verbleiben.

### Wann sie starten, und was sie kostet

Es gibt **keine automatische Synchronisierung**: Eine in der Roborock-App erstellte, umbenannte oder
gelöschte Routine erscheint (oder verschwindet) auf Jeedom-Seite erst nach einem Klick auf „Routinen
synchronisieren“. Starten Sie sie also jedes Mal, wenn Sie Ihre Routinen in der App ändern.

Sie verbraucht **weder** das Verbindungskontingent **noch** das der Gerätebestandsaufnahme (siehe
„Roborock-Kontingente“ weiter unten) — aber zwei Klicks innerhalb weniger als einer Minute werden
abgelehnt, mit der Aufforderung zu warten.

Vorbeugender Rat: Bevor Sie eine Routine in der App löschen, notieren Sie sich die Jeedom-Szenarien,
die deren Befehl verwenden. Sie verlieren ihren Bezug bei der nächsten Synchronisierung.

Ist das Konto nicht verknüpft, der Daemon angehalten, oder eine erneute Authentifizierung erforderlich,
zeigt das Panel weiterhin die Liste der bereits bekannten Routinen an, und die Schaltfläche zeigt eine
explizite Meldung: In all diesen Fällen wird **keine** Routine gelöscht.

## Dashboard-Kachel

Jeder Roboter verfügt über eine Dashboard-Kachel, die sein Foto (oder, in Ermangelung dessen, das
Plugin-Symbol), seinen Status, eine Batterieanzeige und die aktuellen Steuerungsaktionen (Starten,
Pause, Stopp, Rückkehr zur Basis, Orten) zusammenfasst.

Die auf diese Weise in der Kachel zusammengefassten Befehle erscheinen nicht mehr **separat** in der
Standardliste der Dashboard-Befehle: Sie bleiben dennoch vollständig in einem Szenario, in einer
Ansicht oder in einem benutzerdefinierten Design nutzbar, genau wie zuvor. Sie werden nicht gelöscht,
sondern nur in dieser Sammelansicht ausgeblendet.

## Karte und Räume

### Panels der Geräteseite

Der Reiter „Gerät“ eines Roboters bietet zwei zusätzliche Panels:

- **Räume** — die Zuordnung zwischen den vom Roboter erkannten Segmenten und den Raumnamen, die Sie
  in der Roborock-App vergeben haben. Eine Schaltfläche **„Räume neu synchronisieren“** liest diese
  Zuordnung erneut ein; tun Sie dies, nachdem Sie auf Roborock-Seite einen Raum hinzugefügt, gelöscht
  oder umbenannt haben.
- **Karten** — die Liste der vom Roboter gespeicherten Karten (nützlich, wenn Ihre Wohnung mehrere
  Etagen hat), mit der aktiven Karte, einem Auswahlfeld für eine andere und einer Schaltfläche
  **„Karte wechseln“**. Der Kartenwechsel ist ein langsamer Vorgang (der Roboter muss die angeforderte
  Karte neu laden): Das Plugin verweigert eine neue Wechselanfrage für zwei Minuten nach der letzten.
  **Ein Kartenwechsel macht automatisch die angezeigte Raumliste und das Kartenbild ungültig**, die
  anschließend neu synchronisiert werden.

Derselbe Reiter bietet zwei getrennte Blöcke, jeder mit eigener Schaltfläche:

- **Kartenbild** — das Bild der aktiven Karte, automatisch während der Reinigungen neu erstellt
  (höchstens einmal alle 30 Sekunden) und manuell über „Kartenbild aktualisieren“ aktualisierbar.
- **Zone und Punkt** — ein **rein informativer** Block (keine Eingabe hier), der das Koordinatensystem
  der zuletzt abgerufenen Karte anzeigt: die nutzbare Zone in Millimetern, die Position der Ladestation
  und die des Roboters zum Zeitpunkt der Karte sowie eine Umrechnungshilfe ab einem Pixel des Bildes.
  Er dient zur Vorbereitung der Werte, die in die Befehle „Eine Zone reinigen“ und „Zu einem Punkt
  fahren“ (siehe „Feinsteuerung“ unten) einzugeben sind, die **Befehle des Geräts** bleiben, keine
  Felder dieses Panels. Ohne abgerufenes Kartenbild sind nur allgemeine Grenzwerte bekannt.

### Panel „Karte“ (Startseite > JeeRoborock)

Die Karte ist ein **Panel**, keine Seite des Menüs Plugins: Sie öffnet sich über das Menü
**Startseite > JeeRoborock** und ist für jeden Benutzer mit Leserechten auf mindestens einen Roboter
zugänglich (nicht nur für Administratoren). Sie zeigt die aktive Karte des ausgewählten Roboters, deren
Zeitstempel und die Legende der erkannten Räume (Segmentnummer / Name) an und aktualisiert sich alle
30 Sekunden selbst, solange die Seite geöffnet bleibt.

Erscheint der Eintrag nicht unter **Startseite**, prüfen Sie, ob das Kästchen **„Desktop-Panel
anzeigen“** auf der Verwaltungsseite des Plugins angekreuzt ist (**Plugins > Plugin-Verwaltung >
JeeRoborock**): Es wird bei der Installation automatisch angekreuzt, bleibt aber änderbar.

## Feinsteuerung

Je nach den bei Ihrem Roboter erkannten Fähigkeiten können folgende Befehle erscheinen:

- **Saugleistung** und **Wasserdurchfluss** — ein Informationsbefehl zeigt die aktuelle Stufe an, ein
  Aktionsbefehl (Auswahlliste) ermöglicht die Wahl einer anderen unter den vom Roboter tatsächlich
  unterstützten Stufen.
- **Wischroute** und **Reinigungsmodus** (nur Saugen / nur Wischen / Saugen und Wischen) — gleiches
  Prinzip: Information + Auswahlliste als Aktion.
- **Räume reinigen** — ein Befehl pro erkanntem Raum („<Raumname> reinigen“), plus ein allgemeiner
  Befehl „Räume reinigen (Namen durch Kommas getrennt)“, der eine Liste von Namen als Freitext
  akzeptiert. Wie bei den Routinen folgt der Name des Befehls den in der Roborock-App vorgenommenen
  Umbenennungen bei der nächsten Synchronisierung — auch wenn der Raumname ein Apostroph, ein
  Kaufmanns-Und, eine Raute oder ein Prozentzeichen enthält („Salle d'eau“ (Waschraum), zum Beispiel) —
  außer wenn Sie diesen Namen manuell in Jeedom angepasst haben, in diesem Fall wird Ihr angepasster
  Name beibehalten.
- **Eine Zone reinigen** — erhält vier Koordinaten `x1,y1,x2,y2` in Millimetern und reinigt das
  entsprechende Rechteck.
- **Zu einem Punkt fahren** — erhält zwei Koordinaten `x,y` in Millimetern.

Die Koordinaten von Zone und Punkt werden in demselben Koordinatensystem ausgedrückt wie das für die
Karte verwendete (siehe „Karte und Räume“).

## Echtzeit und Aktualität

Sobald ein Roboter synchronisiert ist, aktualisiert sich sein Status automatisch, ohne Ihr Zutun:
- alle **30 Sekunden** während einer Reinigung;
- alle **60 Sekunden** im Ruhezustand.

Der Befehl **„Letzte Aktualisierung“** zeigt den Zeitstempel der zuletzt empfangenen Daten an.

Die Anzeige **„Online“** reagiert schnell: Sie wechselt zu **offline**, sobald ein periodisches
Auslesen mangels Antwort des Roboters fehlschlägt (im Ruhezustand erfolgt ein Auslesen etwa jede
Minute; etwa alle 40 Sekunden während einer Reinigung), und kehrt zu **online** zurück, sobald ein
Lesevorgang gelingt, eine Aktualisierung spontan vom Roboter empfangen wird oder eine Aktion bestätigt
wird. Die Rückkehr auf „online“ kann nur wenige Sekunden dauern (der Roboter sendet eine
Aktualisierung) oder, im ungünstigsten Fall, in dem der Roboter lange nicht erreichbar war, bis zu
etwa zehn Minuten (die Auslesevorgänge werden nach mehreren Fehlschlägen zunehmend gestreckt).

Unabhängig von diesem Mechanismus wechselt das Plugin, wenn **keine** Daten seit mehr als
**3 Minuten** erhalten werden konnten, beide Anzeigen „Online“ **und** „Verbunden“ auf **getrennt**:
Das ist ein Signal für einen nicht erreichbaren Roboter (ausgeschaltet, außerhalb des Netzwerks, oder
Roborock-Cloud nicht verfügbar), kein Fehler des Plugins selbst.

## Erneute Authentifizierung erforderlich

Ist die bei Roborock gespeicherte Sitzung abgelaufen oder widerrufen worden, zeigt das Plugin
„ré-authentification requise“ (Erneute Authentifizierung erforderlich) an (Meldung sichtbar bei den
betroffenen Befehlen und bei Aktionsversuchen).

**Das Plugin versucht nie von selbst, sich erneut zu verbinden.** Dieser Schritt erfordert das Lesen
eines an Ihr E-Mail-Postfach gesendeten Codes, was kein Automatismus für Sie erledigen kann. So kommen
Sie hier heraus:

1. Öffnen Sie die Konfiguration des Plugins.
2. Klicken Sie auf **„Code senden“**, holen Sie sich den per E-Mail empfangenen Code.
3. Geben Sie ihn ein und klicken Sie auf **„Code bestätigen“**.

Nach erfolgreicher Bestätigung läuft alles ohne weiteres Zutun normal weiter.

## Roborock-Kontingente

Die Roborock-Server erzwingen **strikte, mit der mobilen App Ihres Kontos geteilte** Kontingente: eine
begrenzte Anzahl von Verbindungen pro Minute/Stunde/Tag und eine begrenzte Anzahl von
Bestandsaufnahme-Aufrufen für Ihre Geräte in denselben Zeitfenstern.

Weist eine Meldung darauf hin, dass ein Kontingent erreicht ist, **warten Sie**: Das ist kein Fehler
des Plugins, und ein sofortiger erneuter Versuch verschlimmert die Lage nur — Sie würden auch die
Nutzung der mobilen App auf demselben Konto beeinträchtigen, bis sich der Zähler zurücksetzt. Das
Plugin startet nach einer Kontingentverweigerung nie automatisch einen erneuten Versuch.

Die Synchronisierung und die Ausführung der Routinen fallen nicht unter diese Kontingente.

## Fehlerbehebung

### Diagnosebericht

Bevor Sie um Hilfe bitten, erzeugen Sie einen Diagnosebericht: Klicken Sie in der
**Plugin-Konfiguration**, Block **„Diagnose und Support“**, auf **„Diagnosebericht erstellen“**. Der
Bericht erscheint in einem Textfeld, bereit zur Übermittlung.

Er fasst den Zustand der Umgebung zusammen (Versionen von Plugin, Jeedom und Daemon, einschließlich der
verwendeten Version der Roborock-Bibliothek), den Status der Kontoverbindung, die Liste der Roboter —
jeder identifiziert durch seine Jeedom-Gerätenummer und eine teilweise maskierte Gerätekennung —, die
kürzlich von Jeedom und dem Daemon gemeldeten Fehler sowie einen technischen Anhang. Er enthält
**nie** Anmeldedaten, Token, Roboterschlüssel, Seriennummer oder E-Mail-Adresse, gleich welchen
Inhalts; die von Ihnen vergebenen Namen Ihrer Roboter oder Räume erscheinen darin ebenfalls nicht.

Zwei Schaltflächen ermöglichen das Abrufen: **„Bericht kopieren“** (Zwischenablage) und **„Bericht
herunterladen“** (Textdatei). Funktioniert das automatische Kopieren nicht — das ist der häufigste
Fall, wenn Jeedom über HTTP statt HTTPS bereitgestellt wird —, bleibt der Text markiert: Kopieren Sie
ihn mit Strg+C. Begrenzt ein Support-Forum die Länge einer Nachricht, hängen Sie stattdessen die
heruntergeladene Datei an.

Ist der Daemon zum Zeitpunkt der Erstellung angehalten, weist der Bericht dies am Anfang darauf hin
(„Démon injoignable : rapport partiel“ – Daemon nicht erreichbar: unvollständiger Bericht) und bleibt
dennoch nutzbar: Die auf Jeedom-Seite noch bekannten Informationen (letzter Status, Zeitstempel der
letzten Kommunikation) erscheinen trotzdem. Ist er gestartet, konnte aber der technische Abschnitt
nicht erstellt werden, weist der Bericht dies durch ein anderes Banner hin („Diagnostic du démon
indisponible : rapport partiel“ – Daemon-Diagnose nicht verfügbar: unvollständiger Bericht); auch hier
bleibt der Rest des Berichts verwertbar.

Diese Aktion ist Jeedom-Administratoren vorbehalten.

### Was einer Hilfeanfrage beizufügen ist

Beschreiben Sie zusätzlich zum Bericht in Ihrer Nachricht: das **genaue Symptom** (was Sie beobachten
und bei welchem Befehl oder Bildschirm), **was Sie bereits versucht haben** und die **ungefähre
Uhrzeit**, zu der das Problem aufgetreten ist. Diese drei Angaben ermöglichen es, den Vorfall in einem
Bericht oder Protokoll wiederzufinden; der Bericht allein reicht nicht aus, um den Kontext zu erraten.

**Veröffentlichen Sie nie unverändert**, in einem Forum oder öffentlichen Ticket:

- Ihre **E-Mail-Adresse** des Roborock-Kontos oder den per E-Mail empfangenen **Code**;
- ein **Token**, eine Sitzungskennung oder jeden Wert, der wie ein technischer Schlüssel aussieht;
- den **Rohinhalt** der Protokolle des Plugins oder des Daemons (Jeedom-Menü „Analyse“ > „Logs“, oder
  Dateien unter `log/`): Im Gegensatz zum Diagnosebericht sind diese Protokolle **nicht bereinigt**;
- einen **Screenshot**, der eines dieser Elemente sichtbar machen würde.

Der über die Konfigurationsseite erzeugte Diagnosebericht ist dagegen dafür konzipiert, unverändert
übermittelt zu werden (siehe oben).

| Symptom | Wahrscheinliche Ursache | Was zu tun ist |
|---|---|---|
| Die Abhängigkeitsanzeige bleibt blockiert / rot | Installation der Python-Abhängigkeit nicht abgeschlossen oder fehlgeschlagen | Warten Sie die von Jeedom angegebene Installationsdauer ab; prüfen Sie bei anhaltendem Fehlschlag den Internetzugang des Servers und starten Sie die Installation über die Seite „Plugins“ neu |
| „Der Daemon antwortet nicht“ | Der Daemon ist nicht gestartet oder wurde gerade angehalten | Starten (oder starten Sie neu) den Daemon über die Plugin-Konfiguration |
| „Der Roboter ist offline: Er antwortet nicht auf die Roborock-Cloud“ | Der Roboter ist ausgeschaltet, außerhalb des Netzwerks, oder hat keine Verbindung zur Roborock-Cloud | Prüfen Sie, ob der Roboter eingeschaltet und mit Ihrem WLAN verbunden ist, wie in der mobilen App |
| „Das Roborock-Konto ist nicht verknüpft“ | Eine Aktion wurde angefordert, obwohl noch kein Konto verknüpft wurde | Folgen Sie dem Verfahren zur Kontoverknüpfung, Abschnitt „Ihr Roborock-Konto verknüpfen“ |
| „Die E-Mail-Adresse des Roborock-Kontos ist ungültig“ oder „Kein Roborock-Konto entspricht dieser E-Mail-Adresse“ | Die eingegebene Adresse enthält einen Fehler oder ist nicht die des Roborock-Kontos | Geben Sie die genaue in der Roborock-App verwendete Adresse ein, speichern Sie die Konfiguration und fordern Sie dann erneut einen Code an |
| Anmeldecode nie per E-Mail erhalten | Falsche E-Mail-Adresse, oder Nachricht vom E-Mail-Programm gefiltert | Prüfen Sie die gespeicherte Adresse, prüfen Sie Ihren Spam-Ordner, versuchen Sie „Code senden“ nach einigen Minuten erneut |
| „Anmeldecode ungültig oder abgelaufen“ | Der Code wurde falsch abgeschrieben oder ist abgelaufen | Fordern Sie einen neuen Code an und bestätigen Sie ihn zügig |
| „Zu viele Anfragen für einen Anmeldecode“ | Zu viele Codeanfragen in kurzer Zeit | Warten Sie einige Minuten, bevor Sie erneut einen Code anfordern |
| „Roborock-Sitzung abgelaufen“ / „Erneute Authentifizierung erforderlich“ | Die gespeicherte Sitzung ist bei Roborock nicht mehr gültig | Folgen Sie dem Verfahren „Erneute Authentifizierung erforderlich“ oben |
| „Roborock-Aufrufkontingent erreicht“ | Das mit der mobilen App geteilte Kontingent ist vorübergehend erschöpft | Warten Sie, bevor Sie es erneut versuchen; starten Sie die Aktion nicht in einer Schleife erneut |
| Ein erwarteter Befehl erscheint nicht am Gerät | Der Roboter meldet die entsprechende Fähigkeit nicht | Das ist normal: Die Befehlsliste hängt davon ab, was der Roboter angibt zu können, kein Fehler |
| „Diese Karte existiert nicht (mehr) auf diesem Roboter“ | Die angezeigte Kartenliste ist veraltet | Klicken Sie auf „Kartenliste aktualisieren“ und versuchen Sie es erneut |
| „Ein Kartenwechsel wurde gerade durchgeführt: Warten Sie zwei Minuten, bevor Sie einen weiteren starten“ | Der Kartenwechsel ist ein langsamer Vorgang, geschützt durch eine Zwei-Minuten-Sperre | Warten Sie zwei Minuten, bevor Sie einen erneuten Kartenwechsel starten |
| „Die Roboterkarte konnte nicht dekodiert werden“ | Die von der Station empfangenen Daten sind unlesbar (punktueller Vorfall auf Roboter- oder Cloud-Seite) | Versuchen Sie es später erneut; prüfen Sie bei anhaltendem Problem das Protokoll des Daemons |
| „Das Kartenbild ist zu groß, um übertragen zu werden“ | Die vom Roboter erzeugte Karte überschreitet die vom Plugin akzeptierte Speichergröße | Versuchen Sie es später erneut; besteht das Problem weiter, ist dieser Roboter nicht mit dieser Funktion kompatibel |
| „Der Roboter muss sich an der Basis befinden, um diesen Vorgang zu starten“ | Eine Wartungsaktion der Station wurde angefordert, obwohl der Roboter nicht an seiner Basis ist | Warten Sie, bis der Roboter zu seiner Basis zurückkehrt, oder starten Sie zunächst „Zurück zur Basis“ |
| „Dieser Wartungsvorgang ist auf der Station dieses Roboters nicht verfügbar“ | Die Station dieses Roboters unterstützt diese Aktion nicht | Das ist normal: Der Befehl sollte nicht erscheinen, wenn die Station es nicht zulässt; aktualisieren Sie den Status des Roboters |
| „Die von der Roborock-Cloud empfangene Routinenliste ist unvollständig: Aus Vorsicht wurde keine Routine gelöscht.“ | Die Antwort der Cloud wurde abgeschnitten, oder dieser Roboter hat mehr als 64 Routinen | Starten Sie die Synchronisierung später erneut; in der Zwischenzeit ist nichts verloren gegangen |
| „Die Roborock-Nutzungsbedingungen wurden nicht akzeptiert“ (oder „haben sich geändert“) | Roborock verlangt die (erneute) Bestätigung seiner Nutzungsbedingungen | Öffnen Sie die Roborock-App, akzeptieren Sie die vorgeschlagenen Bedingungen und versuchen Sie es dann erneut von Jeedom aus |
| „Roboter unbekannt beim Daemon“ | Das Jeedom-Gerät wird vom Daemon nicht mehr erkannt (Neustart, Roboter aus dem Konto entfernt …) | Starten Sie „Geräte synchronisieren“ erneut |
| „Die Roborock-Cloud ist nicht erreichbar“ | Jeedom erreicht die Roborock-Server nicht | Prüfen Sie den Internetzugang des Jeedom-Servers |
| Eine Meldung zu einer überschrittenen **Zeitvorgabe**, einer **fehlgeschlagenen Verbindung** oder „mehrere Kommunikationsversuche sind fehlgeschlagen“ | Der Roboter oder die Roborock-Cloud hat zu lange zum Antworten gebraucht: vorübergehende Netzwerkstörung, oder stark beanspruchter Roboter | Versuchen Sie es nach einer Minute erneut; wiederholt sich dies, prüfen Sie die WLAN-Verbindung des Roboters und den Internetzugang des Jeedom-Servers |
| „Der Roboter ist beschäftigt“, „Der Roboter hat die Aktion in seinem aktuellen Zustand abgelehnt“ oder „Der Roboter hat einen Fehler gemeldet“ | Der Roboter kann diese Anfrage in seinem aktuellen Zustand nicht ausführen (laufende Reinigung, voller Behälter, mechanischer Vorfall …) | Prüfen Sie den Status des Roboters (Befehl „Status“, oder mobile App), beheben Sie den gemeldeten Vorfall und starten Sie die Aktion dann erneut |
| „Diese Funktion ist bei diesem Robotermodell nicht verfügbar“ oder „Der Roboter erkennt diesen Befehl nicht“ | Der Roboter implementiert diese Funktion nicht, obwohl der Befehl in Jeedom existiert | Keine Manipulation wird die Situation entblockieren: Diese Funktion existiert auf dieser Hardware nicht, blenden Sie den Befehl aus, wenn er Sie stört |
| „Keine laufende Codeanfrage“ | Der Daemon hat zwischen dem Senden und der Bestätigung des Codes neu gestartet | Klicken Sie erneut auf „Code senden“ und bestätigen Sie dann den neu erhaltenen Code |
| Eine Einstellung (Saugleistung, Wasserdurchfluss, Route, Reinigungsmodus) wird nicht angewendet | Der Roboter verweigert diese Einstellung in seinem aktuellen Zustand (in der Regel: nicht im Ruhezustand) | Versuchen Sie es erneut, sobald der Roboter im Ruhezustand oder an seiner Basis ist |
| „Diese Saugleistung / dieser Wasserdurchfluss / diese Route / dieser Reinigungsmodus ist bei diesem Roboter nicht verfügbar“ | Die von Jeedom bekannte Stufenliste ist veraltet (der Roboter meldet diesen Wert nicht mehr) | Aktualisieren Sie den Status des Roboters und versuchen Sie es erneut |
| „Unbekannter Raum“, „kein bekannter Raum“ oder „mehrere Räume tragen diesen Namen“ | Der eingegebene Name entspricht keinem erkannten Raum, noch wurde kein Raum synchronisiert, oder der Name ist mehrdeutig | Synchronisieren Sie die Räume über den Reiter Gerät neu, verwenden Sie den genauen Namen aus der Roborock-App, oder den diesem Raum zugeordneten Befehl statt des allgemeinen Befehls |
| „Diese Koordinaten liegen außerhalb der bekannten Kartengrenzen“ | Die eingegebene Zone oder der Punkt überschreitet die aktuell bekannte Karte des Roboters | Prüfen Sie die Koordinaten im Block „Zone und Punkt“ des Reiters Gerät, oder aktualisieren Sie das Kartenbild |
| „Dieses Verbrauchsmaterial wird für diesen Roboter nicht erfasst“ | Der Zurücksetzungsbefehl wurde verwendet, bevor der Verschleiß dieses Verbrauchsmaterials mindestens einmal gemeldet wurde | Aktualisieren Sie den Status des Roboters, bevor Sie dieses Verbrauchsmaterial zurücksetzen |
| „Eine Synchronisierung (oder ein Lesevorgang) wurde gerade durchgeführt, warten Sie“ (Routinen, Räume oder Zeitpläne) | Eine Resynchronisierung hat bereits vor weniger als einer Minute stattgefunden | Warten Sie eine Minute, bevor Sie dieselbe Resynchronisierung erneut starten |
| „Das Protokoll wurde gerade aktualisiert: Warten Sie eine Minute, bevor Sie es erneut versuchen.“ | Die Schaltfläche „Protokoll aktualisieren“ wurde bereits vor weniger als einer Minute verwendet | Warten Sie eine Minute, bevor Sie erneut klicken |
| „Die Berichterstellung ist fehlgeschlagen.“ | Die Anfrage an Jeedom ist nicht erfolgreich: 20-Sekunden-Frist überschritten, Verbindung unterbrochen oder Fehler des Jeedom-Servers (ein angehaltener Daemon dagegen liefert einen unvollständigen Bericht, nicht diesen Fehlschlag) | Laden Sie die Konfigurationsseite neu und versuchen Sie es erneut; besteht das Problem weiter, prüfen Sie das Protokoll `jeeroborock` (Menü „Analyse“ > „Logs“) |
| „… Routine(n) konnten nicht in Jeedom gespeichert werden. Prüfen Sie das Plugin-Log.“ (im Bericht des Panels „Routinen“) | Eine bestimmte Routine konnte während der Synchronisierung auf Jeedom-Seite nicht erstellt oder aktualisiert werden, während der Rest normal verlief | Prüfen Sie das Protokoll `jeeroborock` (Menü „Analyse“ > „Logs“), um die betroffene Routine zu identifizieren, und starten Sie dann eine erneute Synchronisierung |
| „401 - Nicht autorisierter Zugriff“ beim Klick auf „Diagnosebericht erstellen“ | Ihre Jeedom-Sitzung ist abgelaufen, oder Ihr Konto hat keine Administratorrechte | Melden Sie sich erneut bei Jeedom mit einem Administratorkonto an und versuchen Sie es erneut |
| „Daemon-Diagnose nicht verfügbar: unvollständiger Bericht“ | Der Daemon ist gestartet, konnte aber den technischen Teil des Berichts nicht liefern (punktueller Vorfall) | Der Rest des Berichts bleibt verwertbar; versuchen Sie es später erneut, um den vollständigen technischen Abschnitt zu erhalten |

Für jede andere Meldung gibt der vom Plugin angezeigte Text direkt die Ursache und gegebenenfalls die
zu ergreifende Maßnahme an — es ist nie nötig, die technischen Protokolle zu öffnen, um sie zu
verstehen.

## Bekannte Einschränkungen

- Das Plugin steuert nur Roboter, die mit dem V1-Protokoll von Roborock kompatibel sind, über die
  Cloud. Ältere Roboter (Protokoll A01) werden nicht unterstützt.
- Die vom Roboter selbst erzeugten Bezeichnungen (Status, Fehler, Stationsstatus, Namen von
  Verbrauchsmaterialien) bleiben **immer auf Französisch**, unabhängig von der für die Jeedom-Oberfläche
  gewählten Sprache.
- Ein von der mobilen App aus vorgenommener Kartenwechsel wird nun automatisch im Hintergrund innerhalb
  von etwa einer Minute erkannt: Die aktive Karte, das Bild und das Koordinatensystem der Karte werden
  ohne Ihr Zutun aktualisiert (die Raumliste dagegen wird geleert und wartet auf einen Klick auf
  „Räume neu synchronisieren“). Während dieser kurzen Verzögerung kann die Konfiguration noch die
  alte Etage anzeigen, und eine bereits geöffnete Geräteseite aktualisiert sich nicht von selbst: Laden
  Sie sie neu.
- Die oben erwähnte lokale Verbindung („Was das Plugin tut, und was nicht“) kann von Jeedom aus nicht
  deaktiviert werden.
- Das Plugin zeigt die Version der **Firmware** des Roboters an (Reiter „Gerät“, bei der
  Gerätesynchronisierung aktualisiert), meldet aber nicht, dass eine Aktualisierung verfügbar ist, und
  löst sie nicht aus: Die Firmware-Aktualisierung erfolgt über die Roborock-App.
- Über **64 registrierte Routinen** für denselben Roboter hinaus fügt die Routinen-Synchronisierung
  weiterhin hinzu und benennt um, löscht aber nicht mehr automatisch aus der App verschwundene
  Routinen.
- Das Kartenbild kann **unlesbar** bleiben, wenn der Roboter nur über die oben erwähnte lokale
  Verbindung erreichbar ist, ohne den MQTT-Kanal der Cloud zu durchlaufen (Meldung „Die Roboterkarte
  konnte nicht dekodiert werden“).
- Das Auslesen der Raumnamen (Panel „Räume“ des Reiters Gerät) erfordert, dass der Roboter **online**
  ist: Es schlägt fehl, wenn der Roboter zum Zeitpunkt des Klicks nicht erreichbar ist.
- Die Kartenansicht (Panel „Startseite > JeeRoborock“) löst selbst keine Aktualisierung aus: Sie
  zeigt lediglich alle 30 Sekunden das zuletzt bekannte Bild an. Dieses Bild wird nur während der
  Reinigungen neu erstellt; im Ruhezustand kann es daher vom letzten Durchgang des Roboters stammen.
- Es gibt keine Kartenansicht in der mobilen App von Jeedom: Das Kartenpanel ist nur auf der
  Desktop-Oberfläche verfügbar.
- Die von der Dashboard-Kachel übernommenen Befehle (Batterie, Reinigt, Fehler, Verbunden, Online und
  die fünf Steuerungsaktionen) werden nur einmal ausgeblendet, bei der Erstellung der Kachel. Blenden
  Sie einen davon manuell wieder ein, blendet das Plugin ihn nie wieder aus: Ihre Wahl bleibt erhalten.
- Auf einer von einer älteren Plugin-Version aktualisierten Installation hat eine einmalige technische
  Migration möglicherweise die Historisierung des Befehls „Fehler“ reaktiviert: Wenn Sie diesen Befehl
  nicht historisieren möchten, deaktivieren Sie es manuell in seiner Konfiguration.

Diese Seite wird bei jeder neuen vom Plugin bereitgestellten Funktion aktualisiert.
