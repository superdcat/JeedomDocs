# JeeRoborock

JeeRoborock steuert Ihre Roborock-Saugroboter von Jeedom aus über die Roborock-Cloud: Status in
Echtzeit, Reinigungsbefehle, Feinsteuerung (Saugleistung, Wasser, Route, Wartung der Station),
Reinigung nach Raum oder Zone, mehrere Karten sowie die Ausführung der in der Roborock-App
festgelegten Routinen („Routinen“).

## Was das Plugin tut, und was nicht

JeeRoborock ist freie Software, veröffentlicht unter der Lizenz **GPL v3 oder später**.

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

1. **Jeedom mindestens 4.4.7**, installiert auf einem Server mit **Debian 12 oder 13**. Diese
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

### Befehle je nach Modell

Das Plugin kennt keine Befehlsliste „pro Modell“. Es erstellt einen Befehl, wenn der Roboter oder seine
Station die entsprechende Fähigkeit **meldet**, oder wenn er **antwortet**, sobald das Plugin ihn
abfragt. Ein fehlender Befehl bedeutet also „diese Hardware meldet ihn nicht (oder noch nicht)“, nicht
„das Plugin ist defekt“. Ein Roboter mit kompletter Station hat nicht dieselbe Liste wie ein Roboter
ohne Station oder ein älterer Roboter desselben Herstellers.

**Einen fehlenden Befehl erscheinen lassen:**

1. Prüfen Sie, dass der Daemon gestartet ist, das Konto verknüpft ist und der Roboter **online** ist:
   Solange der Roboter nicht ein erstes Mal geantwortet hat, wird kein von seinen Fähigkeiten abhängiger
   Befehl erstellt.
2. Führen Sie den Befehl **„Aktualisieren“** des Geräts aus, oder warten Sie: Der Status wird im
   Ruhezustand alle 60 Sekunden von selbst neu ausgelesen (alle 30 Sekunden während einer Reinigung).
   Die Befehle werden bei diesem Auslesen erstellt. Laden Sie anschließend die Seite des Geräts neu.
3. Gehen Sie nach einer Aktualisierung der Firmware des Roboters (über die Roborock-App) oder des
   Plugins genauso vor. Verwenden Sie dafür **nicht** „Geräte synchronisieren“: Diese Schaltfläche dient
   dazu, die Roboter des Kontos zu erkennen, und verbraucht Roborock-Kontingent.
4. Hat der Roboter geantwortet, dass er eine durch Abfrage gelesene Einstellung nicht kennt (Nicht
   stören, Lautstärke), fragt das Plugin nur **einmal pro Stunde** erneut ab; schlägt das Auslesen fehl
   (Roboter nicht erreichbar), versucht es nach 5 Minuten erneut. Der Befehl „Aktualisieren“ erzwingt ein
   sofortiges Auslesen.
5. Unmittelbar nach „Aktualisieren“ können die letzten Einstellungen der Liste (Lautstärke, Modi der
   Station) fehlen, wenn die Zeit für das Auslesen nicht gereicht hat: Führen Sie „Aktualisieren“ erneut
   aus, oder warten Sie eine Minute.

Das Plugin löscht von sich aus keinen bereits erstellten Befehl.

| Fähigkeit | Betroffene Befehle | Bedingung für das Erscheinen |
|---|---|---|
| Verbrauchsmaterialien der Station | „Verbleibende Lebensdauer Stationsfilter“, „Verbleibende Lebensdauer Reinigungsbürste“, „Verbleibende Lebensdauer Staubbeutel“ und, außer beim Staubbeutel, ihre Aktion „Zurücksetzen…“ | Die Station besitzt die Ausstattung (Mopp-Wäsche für den Filter, Reinigungsbürste, automatische Entleerung für den Staubbeutel) **und** der Roboter meldet den Zähler. Etwa stündlich neu ausgelesen, oder bei „Aktualisieren“ |
| Tanks und Wischmopp | „Frischwassertank leer“, „Schmutzwassertank voll oder fehlt“, „Wischmopp eingesetzt“ | Tank: Die Station wäscht die Wischmopps. Wischmopp: Der Roboter meldet, den Wassermodus zu unterstützen. Beim nächsten Auslesen des Status erstellt |
| Kindersicherung | „Kindersicherung“, „Kindersicherung aktivieren“, „Kindersicherung deaktivieren“ | Der Roboter meldet, diese Einstellung zu unterstützen. Beim nächsten Auslesen des Status erstellt |
| Nicht stören | Information, Beginn, Ende, drei Aktionen | Der Roboter antwortet auf das Auslesen des Modus. Jede Minute neu ausgelesen; bei „Aktualisieren“ sofort |
| Nebentarifzeiten | Information, Beginn, Ende, drei Aktionen | Der Roboter meldet die Funktion. Beim nächsten Auslesen des Status erstellt |
| Lautstärke | „Lautstärke“, „Lautstärke einstellen“ | Der Roboter antwortet auf das Auslesen der Lautstärke. Jede Minute neu ausgelesen; bei „Aktualisieren“ sofort |
| Modi der Station | „Entleerungsmodus“ und „Entleerungsmodus einstellen“; „Mopp-Waschmodus“ und „Waschmodus einstellen“ | Die Station meldet die automatische Entleerung (Entleerungsmodus) oder die Mopp-Wäsche (Waschmodus). Beim nächsten Auslesen des Status erstellt |
| Anzahl der Durchgänge | Kein eigener Befehl: ein Parameter der Aktionen „Räume reinigen“ und „Eine Zone reinigen“ | Der Roboter gibt in seinem Status an, Wiederholungen zu unterstützen. Dann lautet die Feldbezeichnung „Anzahl der Durchgänge (1 bis 3)“; andernfalls hat das Feld keine Bezeichnung, und eine Zahl 2 oder 3 wird vom Plugin grundsätzlich abgelehnt |
| Aktueller Raum | „Aktueller Raum“ | Ein Kartenbild wurde gelesen, die Karte ist in Räume unterteilt und die Position des Roboters ist verwertbar. Erstes Bild: beim ersten Auslesen, danach während einer Reinigung oder nach einem Statuswechsel |

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

**Während der Behälter geleert wird.** Wenn die Station den Staubbehälter leert (Roboterstatus „Vidage du bac à poussière“, d. h. Staubbehälter wird geleert), berücksichtigt der Roboter keinen Reinigungsbefehl. Das Plugin verweigert ihn dann, statt ohne Wirkung „ok“ zu antworten: Das betrifft „Starten“, „Räume reinigen“, die Befehle „<Raumname> reinigen“ und „Eine Zone reinigen“. Die angezeigte Meldung lautet „Le robot vide son bac à poussière : l'ordre de nettoyage n'a pas été envoyé. Réessayez dans un instant, quand le vidage sera terminé (robot de nouveau en charge).“ (Der Roboter leert seinen Staubbehälter: Der Reinigungsbefehl wurde nicht gesendet. Versuchen Sie es gleich noch einmal, wenn das Leeren beendet ist (Roboter wieder in Ladung).) In einem Szenario schlägt die Aktion genauso fehl. Die anderen Befehle (Pause, Stopp, Zurück zur Basis, Lokalisieren, Zu einem Punkt fahren) sind nicht betroffen, ebenso wenig die Routinen, die von der Roborock-Cloud ausgeführt werden. Kann das Plugin den Status des Roboters unmittelbar vor dem Befehl nicht auslesen, wird der Befehl normal gesendet.

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

Je nach Ausstattung Ihrer Station und sofern der Roboter den Zähler meldet, erscheinen drei zusätzliche
Verschleißanzeigen, ebenfalls als verbleibender Prozentsatz:

- „Verbleibende Lebensdauer Stationsfilter“: Stationen, die den Wischmopp waschen;
- „Verbleibende Lebensdauer Reinigungsbürste“: Stationen, die eine besitzen (in der Praxis einige
  Stationen der Oberklasse);
- „Verbleibende Lebensdauer Staubbeutel“: Stationen mit automatischer Entleerung.

Ohne Station oder mit einer einfachen Station erscheinen diese Befehle nicht. Der Stationsfilter und die
Reinigungsbürste haben jeweils eine Aktion „Stationsfilter zurücksetzen“ bzw. „Reinigungsbürste
zurücksetzen“, mit Bestätigung, wie die anderen. Der Staubbeutel hat im Plugin kein Zurücksetzen
(schreibgeschützt): Setzen Sie ihn anderswo zurück (Roborock-App), folgt der Wert beim nächsten Auslesen.

Diese Werte werden etwa einmal pro Stunde neu ausgelesen, sofort mit dem Befehl „Aktualisieren“ und nach
einem Zurücksetzen. Die Prozentwerte können leicht von denen der Roborock-App abweichen.

**Beispiel für ein Szenario**: Auslöser auf den Befehl „Verbleibende Lebensdauer Stationsfilter“,
Bedingung „kleiner als 10“, Aktion „Benachrichtigung senden“ („Denken Sie daran, den Filter der Station
zu ersetzen“). Starten Sie nach dem Austausch die Aktion „Stationsfilter zurücksetzen“ (sie verlangt eine
Bestätigung): Legen Sie sie nicht in ein automatisches Szenario, denn der Zähler würde auf 100 %
zurückspringen, ohne dass das Teil ersetzt wurde.

Drei Ja/Nein-Informationen, die in einem Szenario verwendbar sind, beschreiben außerdem den Zustand von
Wasser und Wischmopp:

- „Frischwassertank leer“ und „Schmutzwassertank voll oder fehlt“: nur, wenn Ihre Station die
  Wischmopps wäscht. „Ja“ weist auf eine zu prüfende Situation hin (den Tank füllen, den Behälter leeren
  oder wieder einsetzen). Der Roboter unterscheidet einen vollen Schmutzwassertank nicht von einem
  fehlenden, daher die Bezeichnung;
- „Wischmopp eingesetzt“: nur, wenn Ihr Roboter mit einem Wischmopp ausgestattet ist.

Diese Informationen sind von „Wassermangel“ getrennt: Der Roboter meldet sie separat, und sie können
gleichzeitig angezeigt werden. Sie werden mit dem Status des Roboters aktualisiert (etwa eine Minute im
Ruhezustand) oder sofort mit „Aktualisieren“. Ist ein Wert vorübergehend nicht verfügbar, bleibt der
zuletzt bekannte Wert erhalten.

**Beispiel für ein Szenario**: Auslöser auf „Frischwassertank leer“ oder „Schmutzwassertank voll oder
fehlt“ (Wert „Ja“), Aktion „Benachrichtigung senden“ („Prüfen Sie den Tank oder den Behälter der
Station“). Eine Bedingung auf „Wischmopp eingesetzt“ (Wert „Nein“) verhindert, dass eine Reinigung mit
Wischen gestartet wird, wenn der Wischmopp nicht angebracht ist.

### Einstellungen des Geräts

Die **Kindersicherung** deaktiviert die physischen Tasten des Roboters (praktisch gegen ein zu neugieriges
Kind oder Tier). Ihr sind drei Befehle gewidmet:

- „Kindersicherung“: Ja/Nein-Information, als Szenariobedingung verwendbar (zum Beispiel, um die Sperre
  nur zu aktivieren, wenn sie es nicht schon ist);
- „Kindersicherung aktivieren“ und „Kindersicherung deaktivieren“: zwei Aktionen.

Diese Befehle erscheinen **nur, wenn Ihr Roboter meldet, diese Einstellung zu unterstützen**. Andernfalls
existiert keiner der drei: Das ist keine Störung, zwei Roboter haben nicht dieselbe Befehlsliste.

Nach einem Befehl liest das Plugin den Status des Roboters erneut aus, um zu prüfen, dass er ihn
übernommen hat, wie bei den unter „Feinsteuerung“ beschriebenen Einstellungen (bis zu etwa zwölf
Sekunden, ohne den Befehl erneut zu senden). Der Befehl „Kindersicherung“ zeigt nur an, was der Roboter
tatsächlich übernommen hat, nie den angeforderten Wert. Die möglichen Meldungen:

| Meldung | Bedeutung |
| --- | --- |
| „Kindersicherung aktiviert.“ / „Kindersicherung deaktiviert.“ | Der Roboter hat den Befehl übernommen: Der zurückgelesene Zustand entspricht. |
| „Aktivierung (oder Deaktivierung) der Kindersicherung an den Roboter gesendet (Anwendung nicht bestätigt).“ | Der Befehl wurde gesendet, aber der Zustand konnte nicht zurückgelesen werden, oder ein anderer Kindersicherungs-Befehl hat ihn während der Prüfung ersetzt. Der angezeigte Zustand bleibt der alte. |
| „Der Roboter hat den Befehl zur Kindersicherung nicht übernommen: Der zurückgelesene Zustand entspricht nicht der Anforderung.“ | Der Roboter antwortet, hat die Einstellung aber nach Ablauf der Frist nicht übernommen. Der angezeigte Zustand ist der vom Roboter zurückgelesene. |
| Ablehnung durch den Roboter | Der Roboter hat den Befehl abgelehnt; die Meldung gibt dies an. |
| Roboter offline | Der Roboter antwortet nicht (ausgeschaltet, außer Reichweite); der Befehl wird nicht übernommen. |

Das Plugin sendet einen Befehl nie von selbst erneut: Starten Sie ihn bei einem Fehlschlag selbst neu.

**Beispiel für ein Szenario**: Wenn am Ende der Reinigung („Reinigung läuft“ wechselt auf „Nein“) die
Bedingung „Kindersicherung“ den Wert „Nein“ hat, starten Sie die Aktion „Kindersicherung aktivieren“.

Eine Änderung in der Roborock-App (oder über die Taste des Roboters) wird dem Plugin nicht gemeldet: Sie
erscheint in „Kindersicherung“ nach etwa einer Minute oder sofort mit dem Befehl „Aktualisieren“.

**Warten Sie einige Sekunden zwischen zwei Kindersicherungs-Befehlen.** Ein Befehl, der weniger als
5 Sekunden nach dem Ende des vorherigen (einschließlich Prüfung) an denselben Roboter gesendet wird, wird
mit der Meldung „Ein Befehl zur Kindersicherung wurde gerade an diesen Roboter gesendet: Warten Sie
einige Sekunden, bevor Sie einen weiteren senden.“ abgelehnt. Planen Sie in einem Szenario eine Pause von
mindestens 5 Sekunden zwischen zwei Kindersicherungs-Aktionen ein.

#### Nicht stören

Der Modus **Nicht stören** verhindert, dass der Roboter während eines Zeitfensters (zum Beispiel nachts)
startet oder spricht. Ihm sind sechs Befehle gewidmet:

| Befehl | Typ | Aufgabe |
| --- | --- | --- |
| Nicht stören | Ja/Nein-Information | Zeigt an, ob der Modus aktiviert ist, als Szenariobedingung verwendbar |
| Beginn Nicht stören | Textinformation | Beginn des Zeitfensters, im Format HH:MM |
| Ende Nicht stören | Textinformation | Ende des Zeitfensters, im Format HH:MM |
| Nicht stören aktivieren | Aktion | Aktiviert den Modus mit dem vom Roboter gespeicherten Zeitfenster |
| Nicht stören deaktivieren | Aktion | Deaktiviert den Modus |
| Zeitfenster für Nicht stören festlegen | Aktion mit zwei Feldern, Beginn und Ende | Speichert das Zeitfenster und aktiviert den Modus |

Diese Befehle erscheinen **nur, wenn der Roboter auf das Auslesen des Modus antwortet**. Sie werden
spätestens etwa eine Minute, nachdem der Roboter erreichbar ist, erstellt, oder sofort mit
„Aktualisieren“. Fehlen sie, ist das keine Störung: Zwei Roboter haben nicht dieselbe Befehlsliste.

Die Uhrzeiten werden in der **lokalen Zeit des Roboters** angegeben, wie in der Roborock-App.

**Das Zeitfenster festlegen**: Füllen Sie die Felder Beginn und Ende im Format HH:MM zwischen 00:00 und
23:59 aus. Eine einstellige Uhrzeit wie 7:30 wird akzeptiert und zu 07:30 normalisiert. Die Aktion ist in
einem Szenario verwendbar: Das Feld **Titel** erhält den Beginn, das Feld **Nachricht** das Ende (ihre
Eingabehilfen tragen die Bezeichnungen „Beginn (HH:MM)“ und „Ende (HH:MM)“). Ein Zeitfenster, das
Mitternacht überschreitet, wird akzeptiert (zum Beispiel 22:00 → 07:00). Ein Beginn, der dem Ende
entspricht, wird abgelehnt. Das Festlegen des Zeitfensters **aktiviert auch den Modus**.

| Eingabe (Beginn → Ende) | Ergebnis |
|---|---|
| 22:00 → 07:00 oder 7:30 → 22:15 | Gültig (Zeitfenster über Mitternacht, oder einstellige Uhrzeit zu 07:30 normalisiert) |
| 00:00 → 23:59 | Gültig |
| 24:00 → 07:00, 22:60 → 07:00 | Abgelehnt: Stunde oder Minute außerhalb der Grenzen |
| 22h00 → 07h00, 2200 → 0700, 22:5 → 07:00 | Abgelehnt: Das Format muss HH:MM sein (zweistellige Minuten, Trennzeichen „:“) |
| (leeres Feld) → 07:00 | Abgelehnt: Ein Feld ist leer |
| 22:00 → 22:00 | Abgelehnt: Beginn entspricht dem Ende |

**Beispiel für ein Szenario**: Starten Sie jeden Abend um 21 Uhr die Aktion „Zeitfenster für Nicht stören
festlegen“ mit Beginn 22:00 und Ende 07:00. Um die Ansagen tagsüber abzuschalten, verwenden Sie besser
„Nicht stören aktivieren“ / „Nicht stören deaktivieren“ für das bereits gespeicherte Zeitfenster.

**Aktivieren** wendet das vom Roboter bereits gespeicherte Zeitfenster erneut an. Liefert der Roboter
keines zurück, wird die Aktion abgelehnt: Verwenden Sie dann „Zeitfenster für Nicht stören festlegen“.
**Deaktivieren** behält normalerweise das gespeicherte Zeitfenster bei, aber dieses Verhalten hängt vom
Roboter ab und ist noch zu bestätigen: Wenn Sie anschließend auf „Aktivieren“ zählen, prüfen Sie „Beginn
Nicht stören“ und „Ende Nicht stören“.

Nach einem Befehl liest das Plugin den Status des Roboters erneut aus, um zu prüfen, dass er ihn
übernommen hat (einige Sekunden, ohne den Befehl erneut zu senden). Die Informationsbefehle zeigen nur
an, was der Roboter tatsächlich übernommen hat. Die möglichen Meldungen:

| Meldung | Bedeutung |
| --- | --- |
| „Nicht stören aktiviert.“ / „Nicht stören deaktiviert.“ / „Zeitfenster für Nicht stören angewendet.“ | Der Roboter hat den Befehl übernommen: Der zurückgelesene Zustand entspricht. |
| „Aktivierung (oder Deaktivierung) von Nicht stören an den Roboter gesendet (Anwendung nicht bestätigt).“ / „Zeitfenster für Nicht stören an den Roboter gesendet (Anwendung nicht bestätigt).“ | Der Befehl wurde gesendet, aber der Zustand konnte nicht zurückgelesen werden. Der angezeigte Zustand bleibt der alte. |
| „Der Roboter hat den Nicht-stören-Befehl nicht angewendet: Der zurückgelesene Zustand entspricht nicht der Anforderung.“ | Der Roboter antwortet, hat die Einstellung aber nach Ablauf der Frist nicht übernommen. |
| „Ungültiges Zeitfenster: Geben Sie Beginn und Ende im Format HH:MM zwischen 00:00 und 23:59 an.“ | Ein Feld ist leer oder fehlerhaft. Korrigieren Sie es. |
| „Ungültiges Zeitfenster: Beginn und Ende des Nicht-stören-Zeitfensters müssen unterschiedlich sein.“ | Beginn und Ende sind identisch. |
| „Der Roboter hat kein verwertbares Nicht-stören-Zeitfenster zurückgegeben: Legen Sie das Zeitfenster fest, wodurch der Modus ebenfalls aktiviert wird.“ | „Aktivieren“ hat kein Zeitfenster, das erneut angewendet werden könnte: Verwenden Sie „Zeitfenster für Nicht stören festlegen“. |
| „An diesen Roboter wurde gerade ein Nicht-stören-Befehl gesendet: Warten Sie einige Sekunden, bevor Sie einen weiteren senden.“ | Zwei Befehle zu kurz hintereinander. |
| Ablehnung durch den Roboter / Roboter offline | Der Roboter hat den Befehl abgelehnt oder antwortet nicht; der Befehl wird nicht übernommen. |

Das Plugin sendet einen Befehl nie von selbst erneut: Starten Sie ihn bei einem Fehlschlag selbst neu.

Eine Änderung in der Roborock-App wird dem Plugin nicht gemeldet: Sie erscheint in Jeedom nach etwa einer
Minute oder sofort mit „Aktualisieren“.

**Warten Sie mindestens 5 Sekunden zwischen zwei Nicht-stören-Befehlen** an demselben Roboter, sonst wird
der letzte abgelehnt (Meldung „Warten“). Planen Sie in einem Szenario eine Pause von mindestens
5 Sekunden zwischen zwei Nicht-stören-Aktionen ein.

#### Nebentarifzeiten

Das **Laden zu Nebentarifzeiten** lässt den Roboter das gewählte Zeitfenster abwarten (zum Beispiel nachts,
bei ermäßigtem Stromtarif), um **seinen Akku zu laden**. Es verzögert nur das Laden: Eine von Ihnen
angeforderte Reinigung blockiert es nicht. Ihm sind sechs Befehle gewidmet:

| Befehl | Typ | Aufgabe |
| --- | --- | --- |
| Laden zu Nebentarifzeiten | Ja/Nein-Information | Zeigt an, ob die Funktion aktiviert ist, als Szenariobedingung verwendbar |
| Beginn der Nebentarifzeiten | Textinformation | Beginn des Zeitfensters, im Format HH:MM |
| Ende der Nebentarifzeiten | Textinformation | Ende des Zeitfensters, im Format HH:MM |
| Laden zu Nebentarifzeiten aktivieren | Aktion | Aktiviert die Funktion mit dem vom Roboter gespeicherten Zeitfenster |
| Laden zu Nebentarifzeiten deaktivieren | Aktion | Deaktiviert die Funktion |
| Zeitfenster der Nebentarifzeiten festlegen | Aktion mit zwei Feldern, Beginn (HH:MM) und Ende (HH:MM) | Speichert das Zeitfenster und aktiviert die Funktion |

Diese Befehle erscheinen **nur, wenn der Roboter die Funktion meldet**. Sie werden spätestens etwa eine
Minute, nachdem der Roboter erreichbar ist, erstellt, oder sofort mit „Aktualisieren“. Fehlen sie, ist
das keine Störung: Zwei Roboter haben nicht dieselbe Befehlsliste.

Die Uhrzeiten werden in der **lokalen Zeit des Roboters** angegeben, wie in der Roborock-App.

**Das Zeitfenster festlegen**: Füllen Sie die Felder Beginn und Ende im Format HH:MM zwischen 00:00 und
23:59 aus. Eine einstellige Uhrzeit wie 7:30 wird akzeptiert und zu 07:30 normalisiert. Die Aktion ist in
einem Szenario mit diesen beiden Feldern verwendbar. Ein Zeitfenster, das Mitternacht überschreitet, wird
akzeptiert (zum Beispiel 23:00 → 07:00). Ein Beginn, der dem Ende entspricht, wird abgelehnt. Das
Festlegen des Zeitfensters **aktiviert auch das Laden zu Nebentarifzeiten**. In einem Szenario erhält das
Feld **Titel** den Beginn und das Feld **Nachricht** das Ende (Eingabehilfen „Beginn (HH:MM)“ und „Ende
(HH:MM)“). Es gelten dieselben Eingaberegeln wie bei „Nicht stören“:

| Eingabe (Beginn → Ende) | Ergebnis |
|---|---|
| 23:00 → 07:00 oder 7:30 → 22:15 | Gültig (die zweite wird zu 07:30 normalisiert) |
| 24:00 → 07:00, 23:60 → 07:00 | Abgelehnt: Stunde oder Minute außerhalb der Grenzen |
| 23h00 → 07h00, 2300 → 0700, 23:5 → 07:00 | Abgelehnt: Das Format muss HH:MM sein |
| (leeres Feld) → 07:00 | Abgelehnt: Ein Feld ist leer |
| 23:00 → 23:00 | Abgelehnt: Beginn entspricht dem Ende |

**Beispiel für ein Szenario**: Starten Sie einmal pro Woche „Zeitfenster der Nebentarifzeiten festlegen“
mit Beginn 23:00 und Ende 07:00, um das Zeitfenster an Ihren Stromvertrag anzugleichen; oder lösen Sie
„Laden zu Nebentarifzeiten aktivieren“ aus, wenn Ihr Szenario für das Verlassen der Wohnung abläuft.

**Aktivieren** wendet das vom Roboter bereits gespeicherte Zeitfenster erneut an. Liefert der Roboter
keines zurück, wird die Aktion abgelehnt: Verwenden Sie dann „Zeitfenster der Nebentarifzeiten
festlegen“. **Deaktivieren** behält normalerweise das gespeicherte Zeitfenster bei, aber dieses Verhalten
hängt vom Roboter ab und ist noch zu bestätigen: Wenn Sie anschließend auf „Aktivieren“ zählen, prüfen
Sie „Beginn der Nebentarifzeiten“ und „Ende der Nebentarifzeiten“.

Nach einem Befehl liest das Plugin den Status des Roboters erneut aus, um zu prüfen, dass er ihn
übernommen hat (einige Sekunden, ohne den Befehl erneut zu senden). Die Informationsbefehle zeigen nur
an, was der Roboter tatsächlich übernommen hat. Die möglichen Meldungen:

| Meldung | Bedeutung |
| --- | --- |
| „Laden zu Nebentarifzeiten aktiviert.“ / „Laden zu Nebentarifzeiten deaktiviert.“ / „Zeitfenster der Nebentarifzeiten angewendet.“ | Der Roboter hat den Befehl übernommen: Der zurückgelesene Zustand entspricht. |
| „Aktivierung (oder Deaktivierung) des Ladens zu Nebentarifzeiten an den Roboter gesendet (Anwendung nicht bestätigt).“ / „Zeitfenster der Nebentarifzeiten an den Roboter gesendet (Anwendung nicht bestätigt).“ | Der Befehl wurde gesendet, aber der Zustand konnte nicht zurückgelesen werden. Der angezeigte Zustand bleibt der alte. |
| „Der Roboter hat den Befehl zum Laden zu Nebentarifzeiten nicht angewendet: Der zurückgelesene Zustand entspricht nicht der Anforderung.“ | Der Roboter antwortet, hat die Einstellung aber nach Ablauf der Frist nicht übernommen. |
| „Ungültiges Zeitfenster: Geben Sie Beginn und Ende im Format HH:MM zwischen 00:00 und 23:59 an.“ | Ein Feld ist leer oder fehlerhaft. Korrigieren Sie es. |
| „Ungültiges Zeitfenster: Beginn und Ende der Nebentarifzeiten müssen unterschiedlich sein.“ | Beginn und Ende sind identisch. |
| „Der Roboter hat kein verwertbares Zeitfenster für Nebentarifzeiten zurückgegeben: Legen Sie das Zeitfenster fest, wodurch auch das Laden zu Nebentarifzeiten aktiviert wird.“ | „Aktivieren“ hat kein Zeitfenster, das erneut angewendet werden könnte: Verwenden Sie „Zeitfenster der Nebentarifzeiten festlegen“. |
| „Ein Befehl zum Laden zu Nebentarifzeiten wurde soeben an diesen Roboter gesendet: Warten Sie einige Sekunden, bevor Sie einen weiteren senden.“ | Zwei Befehle zu kurz hintereinander. |
| Ablehnung durch den Roboter / Roboter offline | Der Roboter hat den Befehl abgelehnt oder antwortet nicht; der Befehl wird nicht übernommen. |

Das Plugin sendet einen Befehl nie von selbst erneut: Starten Sie ihn bei einem Fehlschlag selbst neu.

Eine Änderung in der Roborock-App wird dem Plugin nicht gemeldet: Sie erscheint in Jeedom nach etwa einer
Minute oder sofort mit „Aktualisieren“.

**Warten Sie mindestens 5 Sekunden zwischen zwei Befehlen zu den Nebentarifzeiten** an demselben
Roboter, sonst wird der letzte abgelehnt (Meldung „Warten“). Diese Pause ist unabhängig von der bei
„Nicht stören“: Ein Nicht-stören-Befehl verzögert keinen Befehl zu den Nebentarifzeiten. Planen Sie in
einem Szenario eine Pause von mindestens 5 Sekunden zwischen zwei Aktionen zu den Nebentarifzeiten ein.

#### Lautstärke

Die **Lautstärke** ist die der Sprachansagen des Roboters („Reinigung gestartet“, „Rückkehr zur
Station“ …), von 0 bis 100 %. Ihr sind zwei Befehle gewidmet:

| Befehl | Typ | Aufgabe |
| --- | --- | --- |
| Lautstärke | Numerische Information (%) | Vom Roboter zurückgelesene Lautstärke, als Szenariobedingung verwendbar |
| Lautstärke einstellen | Aktion mit Schieberegler von 0 bis 100 | Sendet die angeforderte Lautstärke an den Roboter |

In einem Szenario akzeptiert „Lautstärke einstellen“ einen Wert (zum Beispiel 40) oder einen Ausdruck
(zum Beispiel eine Berechnung ausgehend von einem anderen Befehl).

Diese Befehle erscheinen **nur, wenn der Roboter auf das Auslesen der Lautstärke antwortet**. Sie werden
spätestens etwa eine Minute, nachdem der Roboter erreichbar ist, erstellt, oder sofort mit
„Aktualisieren“. Fehlen sie, ist das keine Störung: Zwei Roboter haben nicht dieselbe Befehlsliste.

**Akzeptierte Werte**: eine ganze Zahl von 0 bis 100, einschließlich 0 (0 schaltet die Ansagen ab). Ein
leerer, dezimaler (50.5) oder außerhalb der Grenzen liegender Wert (-1, 101) wird mit der Meldung
„Ungültige Lautstärke: Geben Sie eine ganze Zahl zwischen 0 und 100 an.“ abgelehnt, ohne etwas an den
Roboter zu senden.

Nach einem Befehl liest das Plugin die Lautstärke des Roboters erneut aus, um zu prüfen, dass er sie
übernommen hat (einige Sekunden, ohne den Befehl erneut zu senden). Der Befehl „Lautstärke“ zeigt nur an,
was der Roboter tatsächlich übernommen hat. Die möglichen Meldungen:

| Meldung | Bedeutung |
| --- | --- |
| „Lautstärke angewendet.“ | Der Roboter hat den Befehl übernommen: Die zurückgelesene Lautstärke entspricht. |
| „Lautstärkeeinstellung an den Roboter gesendet (Anwendung nicht bestätigt).“ | Der Befehl wurde gesendet, aber die Lautstärke konnte nicht zurückgelesen werden. Der angezeigte Wert bleibt der alte. |
| „Der Roboter hat die angeforderte Lautstärke nicht angewendet: Die zurückgelesene Lautstärke entspricht nicht der Anforderung.“ | Der Roboter antwortet, hat aber einen anderen Wert übernommen. „Lautstärke“ zeigt den zurückgelesenen Wert. |
| „Eine Lautstärkeeinstellung wurde soeben an diesen Roboter gesendet: Warten Sie einige Sekunden, bevor Sie eine weitere senden.“ | Zwei Einstellungen zu kurz hintereinander. |
| Ablehnung durch den Roboter / Roboter offline | Der Roboter hat den Befehl abgelehnt oder antwortet nicht; der Befehl wird nicht übernommen. |

Das Plugin sendet einen Befehl nie von selbst erneut: Starten Sie ihn bei einem Fehlschlag selbst neu. Um
die neue Lautstärke zu hören, führen Sie den Befehl „Orten“ aus.

**Beispiel für ein Szenario**: Starten Sie um 22 Uhr „Lautstärke einstellen“ mit dem Wert 20; um 8 Uhr mit
dem Wert 50. Um die Lautstärke zu halbieren, übergeben Sie einen Ausdruck ausgehend vom
Informationsbefehl „Lautstärke“ (zum Beispiel `round(#[Salon][Robot][Volume]#/2)`, fiktiver Gerätename:
Das Ergebnis muss eine ganze Zahl von 0 bis 100 sein, sonst wird der Befehl abgelehnt, daher das
`round`).

**Die Position des Schiebereglers von „Lautstärke einstellen“ zeigt den zuletzt von Jeedom gesendeten
Wert, nicht zwangsläufig die tatsächliche Lautstärke des Roboters, und folgt einer in der Roborock-App
vorgenommenen Änderung nicht. Maßgeblich ist die Information „Lautstärke“.**

Eine Änderung in der Roborock-App wird dem Plugin nicht gemeldet: Sie erscheint in „Lautstärke“ nach etwa
einer Minute oder sofort mit „Aktualisieren“.

**Warten Sie mindestens 5 Sekunden zwischen zwei Lautstärkeeinstellungen** an demselben Roboter, sonst
wird die letzte abgelehnt (Meldung „Warten“). Planen Sie in einem Szenario eine Pause von mindestens
5 Sekunden zwischen zwei Aktionen „Lautstärke einstellen“ ein.

#### Entleerungsmodus

Der **Entleerungsmodus** legt fest, mit welcher Intensität die Station den Staubbehälter des Roboters
leert. Ihm sind zwei Befehle gewidmet:

| Befehl | Typ | Aufgabe |
| --- | --- | --- |
| Entleerungsmodus | Textinformation | An der Station zurückgelesener Modus, als Szenariobedingung verwendbar |
| Entleerungsmodus einstellen | Aktion vom Typ Liste | Sendet den gewählten Modus an die Station |

Diese Befehle erscheinen **nur, wenn die Station diese Einstellung meldet** (automatische Entleerung des
Behälters): Ein Roboter ohne Station oder mit einer Station, die den Behälter nicht leert, hat keinen
davon. Sie werden spätestens etwa eine Minute, nachdem der Roboter erreichbar ist, erstellt, oder sofort
mit „Aktualisieren“. Fehlen sie, ist das keine Störung: Zwei Roboter haben nicht dieselbe Befehlsliste.

**Angebotene Modi**: Intelligent, Léger (Leicht), Équilibré (Ausgewogen), Max. Diese Liste stammt aus
der vom Plugin verwendeten Bibliothek und ist für alle Stationen gleich: Vergleichen Sie sie mit der der
Roborock-App. Liefert die Station einen Code, den das Plugin nicht kennt, zeigt „Entleerungsmodus“
„Mode inconnu (N)“ (Unbekannter Modus (N)) an, wobei N dieser Code ist.

In einem Szenario wird „Entleerungsmodus einstellen“ über den **Code des Modus** gewählt (und nicht über
seine Bezeichnung), wie bei den anderen Befehlen vom Typ Liste des Plugins.

Nach einem Befehl liest das Plugin den Modus der Station erneut aus, um zu prüfen, dass er übernommen
wurde (einige Sekunden, ohne den Befehl erneut zu senden). „Entleerungsmodus“ zeigt nur an, was die
Station tatsächlich übernommen hat. Die möglichen Meldungen:

| Meldung | Bedeutung |
| --- | --- |
| „Entleerungsmodus auf ‚…‘ eingestellt.“ | Die Station hat den Befehl übernommen: Der zurückgelesene Modus entspricht. |
| „Entleerungsmodus ‚…‘ an den Roboter übertragen (Anwendung nicht bestätigt).“ | Der Befehl wurde gesendet, aber der Modus konnte nicht zurückgelesen werden. Der angezeigte Wert bleibt der alte. |
| „Die Basisstation hat den angeforderten Entleerungsmodus nicht übernommen: Der zurückgelesene Modus entspricht nicht der Anforderung.“ | Die Station antwortet, hat aber einen anderen Modus übernommen. „Entleerungsmodus“ zeigt den zurückgelesenen Modus. |
| „Dieser Entleerungsmodus ist an der Basisstation dieses Roboters nicht verfügbar: Aktualisieren Sie den Status, bevor Sie es erneut versuchen.“ | Der angeforderte Modus ist für diese Station nicht bekannt. |
| „Eine Einstellung des Entleerungsmodus wurde soeben an diesen Roboter gesendet: Warten Sie einige Sekunden, bevor Sie eine weitere senden.“ | Zwei Einstellungen zu kurz hintereinander. |
| Ablehnung durch den Roboter / Roboter offline | Der Roboter hat den Befehl abgelehnt oder antwortet nicht; der Befehl wird nicht übernommen. |

Das Plugin sendet einen Befehl nie von selbst erneut: Starten Sie ihn bei einem Fehlschlag selbst neu. Die
Entleerungseinstellung konnte nicht bei allen Robotern geprüft werden: Akzeptiert Ihre Station sie nicht,
zeigt Ihnen dies die obige Ablehnungsmeldung an.

**Beispiel für ein Szenario**: Auslöser „Entleerungsmodus“ mit dem Wert „Max“; Aktion „Entleerungsmodus
einstellen“ mit dem Code des Modus „Équilibré“ (die Codes sind die aus der Liste des Befehls), um zum
üblichen Modus zurückzukehren.

Eine Änderung in der Roborock-App wird dem Plugin nicht gemeldet: Sie erscheint in „Entleerungsmodus“
nach etwa einer Minute oder sofort mit „Aktualisieren“.

**Warten Sie mindestens 5 Sekunden zwischen zwei Einstellungen des Entleerungsmodus** an demselben
Roboter, sonst wird die letzte abgelehnt (Meldung „Warten“). Planen Sie in einem Szenario eine Pause von
mindestens 5 Sekunden zwischen zwei Aktionen „Entleerungsmodus einstellen“ ein.

#### Mopp-Waschmodus

Der **Waschmodus** legt die Intensität fest, mit der die Station den Wischmopp wäscht. Ihm sind zwei
Befehle gewidmet:

| Befehl | Typ | Aufgabe |
| --- | --- | --- |
| Mopp-Waschmodus | Textinformation | An der Station zurückgelesener Modus, als Szenariobedingung verwendbar |
| Waschmodus einstellen | Aktion vom Typ Liste | Sendet den gewählten Modus an die Station |

Diese Befehle erscheinen **nur, wenn die Station diese Einstellung meldet**: Ein Roboter ohne Waschstation
hat keinen davon. Sie werden spätestens etwa eine Minute, nachdem der Roboter erreichbar ist, erstellt,
oder sofort mit „Aktualisieren“. Fehlen sie, ist das keine Störung.

**Angebotene Modi**: Léger (Leicht), Équilibré (Ausgewogen), Profond (Tief), dazu je nach Roboter
**Très profond** (Sehr tief) oder **Intelligent**. Wie bei der Entleerung vergleichen Sie mit der
Roborock-App. Ein nicht erkannter Code wird als „Mode inconnu (N)“ angezeigt.

In einem Szenario wird „Waschmodus einstellen“ über den **Code des Modus** gewählt, nicht über seine
Bezeichnung.

Nach einem Befehl liest das Plugin den Modus der Station erneut aus. Die möglichen Meldungen sind dieselben
wie bei der Entleerung, mit „Waschen“ statt „Entleeren“: „Waschmodus auf ‚…‘ eingestellt.“,
„Waschmodus ‚…‘ an den Roboter übertragen (Anwendung nicht bestätigt).“, „Die Basisstation hat den
angeforderten Waschmodus nicht übernommen …“, „Dieser Waschmodus ist an der Basisstation dieses Roboters
nicht verfügbar …“ und „Eine Einstellung des Waschmodus wurde soeben an diesen Roboter gesendet: Warten
Sie einige Sekunden …“. Das Plugin sendet einen Befehl nie von selbst erneut. Diese Einstellung wurde
nicht bei allen Robotern geprüft: Bei einer Ablehnung zeigt die Meldung dies an.

**Beispiel für ein Szenario**: Hat nach einer Reinigung mit Wischen „Mopp-Waschmodus“ den Wert „Léger“,
starten Sie vor der nächsten geplanten Reinigung „Waschmodus einstellen“ mit dem Code des Modus
„Équilibré“.

Eine Änderung in der Roborock-App erscheint nach etwa einer Minute oder sofort mit „Aktualisieren“.

**Warten Sie mindestens 5 Sekunden zwischen zwei Einstellungen des Waschmodus** an demselben Roboter,
sonst wird die letzte abgelehnt. Diese Pause ist unabhängig von der beim Entleerungsmodus.

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
- die letzte Reinigung aktualisiert sich auch von selbst, ohne Ihr Zutun: Das Plugin liest das Protokoll
  erneut aus, sobald der Roboter seine Reinigung beendet hat (einschließlich Waschen und Leeren an der
  Station), dann, solange diese Reinigung dort nicht erscheint, etwa 1, 3, 8 und 18 Minuten später
  (mindestens 5 Minuten Abstand nach einem fehlgeschlagenen Auslesen). Rechnen Sie mit einigen Sekunden
  bis zu einigen Minuten, höchstens 30 Minuten; war der Roboter während dieser ganzen Zeit nicht
  erreichbar, erfolgt bei seiner Rückkehr ein letztes Auslesen. Danach hört das Plugin bis zur nächsten
  Reinigung auf, es zu versuchen; die Schaltfläche „Protokoll aktualisieren“ bleibt verfügbar.

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

Die Kartennamen werden **im Klartext** angezeigt, auch bei Robotern, die sie codiert übermitteln
(Roborock S7: „%20“ statt Leerzeichen, „%E9“ statt „é“). Erscheint ein bereits gespeicherter Name noch
codiert, klicken Sie einmal auf **„Kartenliste aktualisieren“** (oder
wechseln Sie die Karte): Er wird im Klartext neu geschrieben, ohne weiteres Zutun.

Derselbe Reiter bietet zwei getrennte Blöcke, jeder mit eigener Schaltfläche:

- **Kartenbild** — das Bild der aktiven Karte, automatisch während der Reinigungen neu erstellt
  (höchstens einmal alle 30 Sekunden) und manuell über „Kartenbild aktualisieren“ aktualisierbar.
- **Zone und Punkt** — ein **rein informativer** Block (keine Eingabe hier), der das Koordinatensystem
  der zuletzt abgerufenen Karte anzeigt: die nutzbare Zone in Millimetern, die Position der Ladestation
  und die des Roboters zum Zeitpunkt der Karte sowie eine Umrechnungshilfe ab einem Pixel des Bildes.
  Er dient zur Vorbereitung der Werte, die in die Befehle „Eine Zone reinigen“ und „Zu einem Punkt
  fahren“ (siehe „Feinsteuerung“ unten) einzugeben sind, die **Befehle des Geräts** bleiben, keine
  Felder dieses Panels. Ohne abgerufenes Kartenbild sind nur allgemeine Grenzwerte bekannt.

### Raum, in dem sich der Roboter befindet

Der Informationsbefehl **„Aktueller Raum“** gibt den Namen des Raums an, in dem sich der Roboter befindet.

- **Woher der Wert stammt**: Er wird aus der Position des Roboters auf dem Kartenbild abgeleitet, das das
  Plugin bereits gelesen hat. Er erfordert keinen zusätzlichen Aufruf beim Roboter oder bei der
  Roborock-Cloud.
- **Verzögerung**: Während einer Reinigung wird der Wert etwa alle 30 Sekunden neu berechnet. Im
  Ruhezustand wird er spätestens etwa eine Minute nach einem Statuswechsel neu gelesen (zum Beispiel
  die Rückkehr zur Basis).
- **Besondere Werte** (fest, immer auf Französisch, unverändert als Konstanten in einer Szenariobedingung
  verwendbar):
  - **„Aucune pièce“** (Kein Raum): Der Roboter befindet sich außerhalb jedes bekannten Raums (nicht
    abgegrenzter Flur, Basis außerhalb eines Raums …).
  - **„Pièce inconnue“** (Unbekannter Raum): Die Position oder die aktive Karte ist nicht bekannt, die
    Räume wurden noch nicht synchronisiert, oder die Karte hat sich gerade geändert.
- **Alter**: Fahren Sie über die Kachel, um die beiden Zeitstempel zu lesen. Das Wertdatum ist das des
  Betretens des Raums; das Erfassungsdatum ist das des zuletzt verarbeiteten Kartenbilds. Ein
  stillstehender Roboter wirkt daher „alt“: Das ist normal.
- **Szenarien**: Ein Szenario wird nur bei einem **echten Raumwechsel** ausgelöst, nicht bei jedem
  Auslesen.
  **Beispiel für ein Szenario**: Auslöser auf den Befehl „Aktueller Raum“, Bedingung „ist gleich Cuisine“
  (fiktiver Name: Verwenden Sie den genauen Namen Ihres Raums), Aktion „Benachrichtigung senden“. Das
  Szenario startet nur, wenn der Roboter den Raum betritt.
- **Fehlender Befehl**: Er wird nicht erstellt, wenn die Karte nicht in Räume unterteilt ist oder die
  Position des Roboters nicht verwertbar ist. Er erscheint von selbst, sobald das erste verwertbare Bild
  vorliegt.
- **Roboter offline**: Der zuletzt bekannte Wert bleibt erhalten.
- **Nach einem Kartenwechsel** wechselt der Wert auf „Pièce inconnue“, bis Sie auf **„Räume neu
  synchronisieren“** klicken. Gehen Sie ebenso vor, nachdem Sie Ihre Räume in der Roborock-App neu
  unterteilt haben.

### Panel „Karte“ (Startseite > JeeRoborock)

Die Karte ist ein **Panel**, keine Seite des Menüs Plugins: Sie öffnet sich über das Menü
**Startseite > JeeRoborock** und ist für jeden Benutzer mit Leserechten auf mindestens einen Roboter
zugänglich (nicht nur für Administratoren). Sie zeigt die aktive Karte des ausgewählten Roboters, deren
Zeitstempel und die Legende der erkannten Räume (Segmentnummer / Name) an und aktualisiert sich alle
30 Sekunden selbst, solange die Seite geöffnet bleibt.

Erscheint der Eintrag nicht unter **Startseite**, prüfen Sie, ob das Kästchen **„Desktop-Panel
anzeigen“** auf der Verwaltungsseite des Plugins angekreuzt ist (**Plugins > Plugin-Verwaltung >
JeeRoborock**): Es wird bei der Installation automatisch angekreuzt, bleibt aber änderbar.

Die Seite hat drei Reiter: **Karte und Steuerung** (standardmäßig geöffnet), **Station und Wartung** und
**Tagesverlauf**.

#### Steuerungspanel

Rechts neben der Karte ermöglicht ein Panel, den **ausgewählten Roboter zu steuern**, ohne die Seite zu
verlassen. Es aktualisiert sich, ohne die Seite neu zu laden, und stellt keine zusätzliche Anfrage an die
Roborock-Cloud.

- **Status**: Status des Roboters, Akku und, während einer Reinigung, Fortschritt.
- **Reiter Gesamt, Raum und Bereich**: Ein Reiterwechsel startet nichts.
  - **Gesamt**: reinigt die gesamte Wohnung.
  - **Raum**: Haken Sie einen oder mehrere Räume an. Ein Raum wird nicht angeboten, wenn sein Name fehlt,
    doppelt vorkommt oder ein Komma enthält: Benennen Sie ihn in der Roborock-App um und synchronisieren
    Sie die Räume anschließend erneut. Die Anzahl der Räume pro Befehl ist begrenzt: Starten Sie die
    Reinigung darüber hinaus in mehreren Durchgängen.
  - **Bereich**: Klicken und ziehen Sie auf der Karte, um ein Rechteck zu zeichnen. Ein zu kleiner oder
    über die Karte hinausragender Bereich wird vor dem Senden abgelehnt. Der Reiter ist inaktiv, wenn die
    Karte nicht verfügbar ist.
- **Einstellungen**: Saugleistung, Wasserdurchfluss und Route. Es werden nur die Werte **Ihres** Roboters
  angeboten, und eine Einstellung, die er nicht unterstützt, wird nicht angezeigt. Der angezeigte Wert ist
  der, den der Roboter tatsächlich übernommen hat.
- **Hauptschaltfläche**: „Alles reinigen“, „N Räume reinigen“ oder „Bereich reinigen“, je nach Reiter.
  Während einer Reinigung weicht sie **Pause** (oder **Fortsetzen**), **Stoppen** und **Zur Station
  zurückkehren**.
- **Roboter offline**: Die Befehle sind inaktiv, mit einem Hinweis. Die letzte Karte bleibt sichtbar.

**Einen Raum reinigen, Schritt für Schritt.**

1. Öffnen Sie **Startseite > JeeRoborock**. Fehlt der Eintrag, siehe oben das Kästchen **Desktop-Panel
   anzeigen**.
2. Haben Sie mehrere Roboter, wählen Sie Ihren in der Liste **Roboter** oben auf der Seite. Bei nur einem
   Roboter gibt es keine Liste.
3. Warten Sie, bis Karte und Status angezeigt werden. Weist ein Hinweis darauf hin, dass der Roboter offline
   ist oder Sie nicht berechtigt sind, ihn zu steuern, bleiben die Schaltflächen inaktiv (siehe
   Fehlerbehebung).
4. Öffnen Sie im Steuerungspanel den Reiter **Raum**.
5. Haken Sie den Raum in der Liste an, oder tippen Sie ihn auf der Karte an: Er wird hervorgehoben. Haken
   Sie bei Bedarf mehrere an. In diesem Schritt wird nichts an den Roboter gesendet.
6. Stellen Sie auf Wunsch Saugleistung, Wasserdurchfluss und Route ein.
7. Klicken Sie auf die Hauptschaltfläche **1 Raum reinigen** (oder **N Räume reinigen**). Dieser Klick, und
   nur er, sendet den Befehl.
8. Verfolgen Sie Status und Fortschritt oben im Panel. Verwenden Sie bei Bedarf **Pause**, **Stoppen**
   oder **Zur Station zurückkehren**.

Erscheint der Raum nicht in der Liste, oder bleibt die Schaltfläche inaktiv, sehen Sie in der Tabelle der
Fehlerbehebung nach.

**Interaktive Karte.** Die Karte selbst dient zum Auswählen und Zeichnen. Es wird nichts an den Roboter
gesendet, solange Sie nicht auf die Hauptschaltfläche geklickt haben.

- **Raumnamen**: Jeder Raum trägt seinen Namen, auf der Karte geschrieben. Ein Raum ohne Namen wird als
  „Unbenannter Raum“ angezeigt. Erlaubt die Karte keine Abgrenzung der Räume, weist eine Meldung darauf
  hin: Wählen Sie die Räume dann in der Liste des Reiters Raum aus.
- **Einen Raum auswählen**: Tippen oder klicken Sie auf einen Raum, um ihn auszuwählen (er wird
  hervorgehoben), und tippen Sie ihn erneut an, um die Auswahl aufzuheben. Die Auswahl ist dieselbe wie die
  der Liste des Reiters Raum: Das Anhaken oder Abwählen auf einer Seite aktualisiert die andere. Sie können
  mehrere Räume auswählen.
- **Nicht wählbare Räume**: Ein Raum ohne Namen, mit doppeltem Namen oder mit einem Namen, der ein Komma
  enthält, behält seine Beschriftung, aber seine Auswahl wird mit einer Erklärung abgelehnt. Benennen Sie
  ihn in der Roborock-App um und synchronisieren Sie die Räume anschließend über die Seite des Geräts
  erneut.
- **Raum auf der aktuellen Karte unbekannt**: Nach einer neuen Raumunterteilung oder einem Etagenwechsel
  kann ein bereits angehakter Raum auf der Karte nicht mehr existieren. Er wird als „Raum auf der
  aktuellen Karte unbekannt“ gekennzeichnet, und die Start-Schaltfläche bleibt inaktiv, solange er
  angehakt ist. Entfernen Sie das Häkchen, oder synchronisieren Sie die Räume über die Seite des Geräts
  erneut.
- **Veraltete Karte**: Ist die angezeigte Karte ein altes Bild (Roboter nicht erreichbar), ist die Auswahl
  auf der Karte nicht möglich („Veraltete Karte: Auswahl nicht möglich“). Ohne jede Karte sind die Reiter
  Raum und Bereich inaktiv.
- **Einen Bereich zeichnen** (Reiter Bereich): Klicken und ziehen Sie, um ein Rechteck zu zeichnen. Ziehen
  Sie es, um es zu verschieben, ziehen Sie an einer Ecke, um die Größe zu ändern, oder klicken Sie auf
  **Bereich löschen**, um es zu entfernen. Das Rechteck bleibt beim Aktualisieren der Karte erhalten,
  außer wenn der Roboter die Kartenetage wechselt oder Sie den Roboter wechseln.
- **Sperrzonen und virtuelle Wände**: Die in der Roborock-App definierten werden mit einer Legende auf der
  Karte eingezeichnet. Sie sind **schreibgeschützt**: Sie werden hier weder erstellt noch geändert. Eine
  in der App vorgenommene Änderung erscheint erst beim nächsten Abruf der Karte. Hat Ihr Roboter keine,
  oder liefert er keine, wird nichts eingezeichnet, und es erscheint keine Meldung. Ein Bereich, den Sie
  auf eine Sperrzone zeichnen, wird vom Plugin nicht blockiert.
- **Touchscreen**: Antippen, Zeichnen und Verschieben funktionieren auf Tablet und Smartphone.

**Berechtigungen.** Ein Befehl wird nur bei Ihrem Klick gesendet, und nur wenn Jeedom Ihnen erlaubt, die
Befehle des Roboters auszuführen. Die Berechtigungen werden in der Benutzerverwaltung von Jeedom
eingestellt, Roboter für Roboter. Das Profil „Benutzer“ hat standardmäßig alle Rechte: Zum Einschränken
verwenden Sie ein eingeschränktes Profil. Ein auf einem Befehl gesetzter Zugangscode oder eine
Bestätigung werden beachtet.

| Ihre Situation | Was Sie sehen | Was Sie tun können |
|---|---|---|
| Administrator | Alle aktivierten Roboter | Alles |
| Ausführungsrecht für den Roboter | Der Roboter, seine Karte, sein Status, die Station und der Tagesverlauf | Alles: auswählen, zeichnen, starten, Pause, Stopp, Station |
| Nur Lesen | Der Roboter, seine Karte, sein Status, die Station und der Tagesverlauf, mit dem Hinweis „Sie sind nicht berechtigt, diesen Roboter zu steuern.“ | Ansehen, Räume auswählen und einen Bereich zeichnen (es wird nichts gesendet). Alle Aktionsschaltflächen sind inaktiv. |
| Kein Recht für den Roboter | Nichts: Der Roboter steht nicht in der Liste | Nichts. Ist kein Roboter zugänglich, zeigt die Seite „Kein Roborock-Roboter mit Ihrem Konto zugänglich.“ an |

Ein in Jeedom **deaktivierter** Roboter wird niemandem angeboten, auch Administratoren nicht. Ein direkter
Link auf einen Roboter, den Sie nicht lesen dürfen, wird ignoriert. Die Anzeige von Karte, Panel und
Zeitleiste kostet keinen Aufruf der Roborock-Cloud.

**Gemerkter Roboter.** Der gewählte Roboter wird in Ihrem Browser gespeichert (nicht von Gerät zu Gerät).
Ein direkter Link auf einen bestimmten Roboter (Parameter der Adresse) hat Vorrang vor dieser Wahl.

**Vorsicht.** Wenn Sie gerade eine Raumreinigung angehalten haben, vermeiden Sie es, sofort „Alles
reinigen“ zu starten: Der Roboter kann die unterbrochene Reinigung fortsetzen, statt die gesamte Wohnung
neu zu beginnen. Prüfen Sie, was er tut; halten Sie ihn bei Bedarf an und starten Sie erneut.

**Saugen, dann wischen.** Dieser Block verkettet zwei Reinigungen auf demselben Umfang: einen **ersten
Durchgang nur saugend**, dann einen **zweiten Durchgang nur wischend**. Er erscheint nur, wenn Ihr Roboter
wischen kann (andernfalls werden weder der Block noch die entsprechenden Befehle erstellt).

- **Starten**: Im Reiter **Gesamt** bearbeitet die Schaltfläche **Saugen, dann wischen** die gesamte
  Wohnung; im Reiter **Raum** bearbeitet sie die angehakten Räume. Für den Reiter Bereich gibt es sie
  nicht. Die angeforderte Anzahl der Durchgänge (siehe „Feinsteuerung“) gilt für beide Durchgänge.
- **Angezeigter Status**: Die Zeile **Sequenz** zeigt an, wo die Verkettung steht: „Passage 1 sur 2 :
  aspiration“ (Durchgang 1 von 2: Saugen), „En attente de la base“ (Warten auf die Basis), „Passage 2 sur
  2 : lavage“ (Durchgang 2 von 2: Wischen), dann am Ende „Séquence terminée“ (Sequenz beendet), „Séquence
  annulée“ (Sequenz abgebrochen), „Séquence interrompue“ (Sequenz unterbrochen), „Le second passage n'a
  pas pu démarrer“ (Der zweite Durchgang konnte nicht starten) oder „Séquence abandonnée“ (Sequenz
  aufgegeben). Endet die Sequenz, ohne bis zum Ende zu laufen, wird darunter der **Grund** angezeigt
  (siehe Fehlerbehebung).
- **Abbrechen**: Die Schaltfläche **Sequenz abbrechen** erscheint, solange eine Sequenz aktiv ist. Sie hält
  den Roboter an, stellt seine ursprünglichen Einstellungen wieder her und verhindert den zweiten
  Durchgang.
- **Das Schließen des Panels unterbricht nichts**: Die Sequenz wird im Hintergrund vom Plugin verfolgt,
  nicht von Ihrem Browser. Öffnen Sie das Panel erneut, um den Status wiederzufinden.
- Mit dem reinen Leserecht ist der Status sichtbar, aber die Schaltflächen sind inaktiv.

#### Reiter „Station und Wartung“

Dieser Reiter fasst für den ausgewählten Roboter die Dockingstation und die Wartung zusammen. Er
aktualisiert sich wie das Steuerungspanel und **verbraucht kein Kontingent** der Roborock-Cloud. Die
Einzelheiten zu jedem Befehl stehen weiter oben im Abschnitt „Dockingstation, Verbrauchsmaterial und
Wartung“. Er besteht aus drei Blöcken; **es erscheint nur, was Ihr Roboter kann**.

- **Aktionen**: **Behälter entleeren**, **Mopp waschen**, **Mopp trocknen** und **Trocknung stoppen**
  sowie die Listen **Entleerungsmodus** und **Mopp-Waschmodus**.
- **Status**: Entleeren des Behälters, Waschen und Trocknen des Wischmopps, Frischwasser, Schmutzwasser,
  Mopp installiert, Wassermangel und **Störung der Station**. Diese Störung ist vom Fehler des Roboters
  getrennt: Ein Fehler des Roboters wird dort nicht angezeigt. Sie wird außerdem in einem roten Banner
  wiederholt, und die **letzte Aktualisierung** wird oben im Reiter angegeben.
- **Verbrauchsmaterialien**: verbleibende Lebensdauer in Prozent. Bei **10 % oder weniger** erscheint der
  Hinweis **Zu wechseln** mit einem Warnbanner. Die Schaltfläche **Zurücksetzen** setzt den Zähler nach
  einer Bestätigung auf null, auszuführen, sobald das Teil ersetzt wurde. Für den Beutel gibt es sie
  nicht.

Hat der Roboter keine Station, zeigt der Reiter **Dieser Roboter hat keine Station.** an.

**Vorgang läuft.** Solange ein Stationsvorgang läuft, sind **Entleeren**, **Waschen** und **Trocknen**
inaktiv und tragen den Hinweis „Vorgang läuft“. Das Gleiche gilt unmittelbar nach dem Senden eines
Befehls: Die Schaltfläche bleibt inaktiv, bis sich der Status ändert, höchstens **2 Minuten** lang.
**Trocknung stoppen** ist nur **während einer Trocknung** aktiv.

**Ablehnung „Roboter nicht an der Basis“.** Ein Stationsvorgang erfordert, dass sich der Roboter an
seiner Basis befindet. Andernfalls lehnt das Plugin ihn ab und weist darauf hin (siehe die Tabelle der
Fehlerbehebung). Es sendet den Befehl **nie** von selbst erneut: Bringen Sie den Roboter zur Basis und
beginnen Sie dann erneut.

**Roboter offline.** Die Schaltflächen sind inaktiv, mit einem Hinweis. Die letzten bekannten Zustände
bleiben mit dem Datum ihrer letzten Aktualisierung angezeigt.

**Berechtigungen.** Mit dem reinen Leserecht ist der Reiter nur zur Ansicht: Keine Schaltfläche ist aktiv,
und ein Hinweis erklärt dies.

#### Reiter „Tagesverlauf“

Dieser Reiter zeigt auf einer **Zeitleiste** („Frise“), was der Roboter im Lauf eines Tages getan hat: ein
Farbband, eine Farbe pro Zustand. Er ist **schreibgeschützt** und **verbraucht kein Kontingent** der
Roborock-Cloud: Er liest nur aus, was das Plugin bereits aufgezeichnet hat. Er ist nur sichtbar, wenn Sie
das **Leserecht** für den Roboter haben.

**Legende.** Jede Farbe entspricht einer Kategorie:

| Kategorie | Bedeutung |
|---|---|
| **Reinigung** | Der Roboter saugt oder wischt. |
| **Rückkehr zur Station** | Der Roboter fährt zu seiner Basis zurück. |
| **Wird geladen** | Der Roboter steht auf seiner Basis. |
| **Entleeren des Behälters** | Die Station leert den Behälter. |
| **Mopp-Waschen** | Die Station wäscht den Wischmopp. |
| **Mopp-Trocknung** | Die Station trocknet den Wischmopp. |
| **Fehler** | Der Roboter hat einen Fehler. |
| **Offline** | Der Roboter antwortet nicht. |
| **Anderer Zustand** | Jeder Zustand, der keine eigene Farbe hat. |
| **Unbekannt** | Während dieses Zeitraums wurde keine Information empfangen. |

**„Unbekannt“.** Dieser schraffierte Bereich deckt einen Zeitraum **ohne Daten** ab: Daemon gestoppt,
Jeedom ausgeschaltet. Das Plugin verlängert den letzten bekannten Zustand **nie**. Ein Zeitraum ist
„Unbekannt“, sobald **15 Minuten** lang keine Nachricht vom Roboter eingegangen ist.

**Beendete Reinigungen.** Unter der Zeitleiste hebt ein schmales dunkles Band (**Reinigung beendet**) die
Reinigungen des **Reinigungsprotokolls** hervor, die den angezeigten Tag berühren.

**Details.** Fahren Sie (Maus) über einen Zeitraum oder tippen Sie (Touchscreen) darauf, um sein Detail
unter der Zeitleiste anzuzeigen.

**Navigation.** Die Schaltflächen **Vorheriger Tag** und **Nächster Tag** wechseln den Tag. Die **letzten
7 Tage** werden aufbewahrt; ältere werden automatisch gelöscht. Die Uhrzeiten entsprechen der **Zeitzone
von Jeedom**. Ein Tag ohne Aufzeichnung zeigt **Keine Daten für diesen Tag.** an.

**Der Verlauf beginnt mit der Installation des Updates.** Das Plugin hat keine Möglichkeit, die
Vergangenheit zu rekonstruieren: Für frühere Tage gibt es keine Daten.

#### Mobiles Panel (App und mobile Version von Jeedom)

Das Steuerungspanel ist auch auf dem Smartphone verfügbar, in der mobilen Jeedom-App und in der mobilen
Web-Version von Jeedom.

**Wo man es findet.** Öffnen Sie **Startseite**, dann **Plugins**, dann **JeeRoborock**. Der eigene Reiter
des benutzerdefinierten Menüs der mobilen App ist den **Administratoren** vorbehalten: Das ist eine
Einschränkung von Jeedom, nicht des Plugins. Erscheint der Eintrag nach der Aktualisierung des Plugins
nicht, **synchronisieren Sie die App erneut**. Der Administrator kann dieses Panel in der
Plugin-Konfiguration auf Jeedom-Seite ausblenden.

**Was es enthält:**

- die Auswahl des Roboters (wenn Sie mehrere haben);
- die Karte, mit anklickbaren Räumen und Sperrzonen;
- die Reiter **Gesamt**, **Raum** und **Bereich**: Für einen Bereich zeichnen Sie das Rechteck mit dem
  Finger auf der Karte und verschieben es dann oder ändern seine Größe an den Ecken;
- die Einstellungen (Saugleistung, Wasserdurchfluss, Route), wenn der Roboter sie anbietet;
- die Schaltflächen **Pause**, **Fortsetzen**, **Stoppen** und **Zur Station zurückkehren**;
- **Saugen, dann wischen**, wenn der Roboter es erlaubt.

**Was es nicht enthält.** Die Seite **Station und Wartung**, der **Tagesverlauf** und die Tabelle der
erkannten Räume sind auf dem Smartphone nicht verfügbar: Öffnen Sie die Kartenseite von Jeedom auf einem
Computer.

**Berechtigungen.** Es sind dieselben wie am Desktop: Mit dem reinen Leserecht ist das Panel nur zur
Ansicht.

**Aktualisierungen.** Die Anzeige aktualisiert sich von selbst, solange das Panel auf dem Bildschirm ist.
Sie wird ausgesetzt, wenn die App in den Hintergrund wechselt, und setzt bei Ihrer Rückkehr fort.

**Nach einer Aktualisierung des Plugins.** Verhält sich das Panel seltsam, schließen Sie die App
vollständig und öffnen Sie sie erneut: Möglicherweise ist eine alte Version im Cache geblieben.

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
  Für eine Reinigung in mehreren Durchgängen siehe „Anzahl der Durchgänge“ unten.
- **Eine Zone reinigen** — erhält vier Koordinaten `x1,y1,x2,y2` in Millimetern und reinigt das
  entsprechende Rechteck. Die Anzahl der Durchgänge wird wie bei den Räumen eingestellt (siehe unten).
- **Anzahl der Durchgänge** (Befehle „Räume reinigen“ und „Eine Zone reinigen“) — füllen Sie das Feld
  **Nachricht** des Befehls aus und geben Sie dann 1, 2 oder 3 (in Ziffern) in das Feld **Titel** ein.
  - **Das ist ein Parameter des laufenden Befehls, keine Einstellung.** Es gibt keinen Befehl „Anzahl der
    Durchgänge“, den man ein für alle Mal einstellt: Geben Sie sie bei jedem Befehl an, sonst erfolgt ein
    einziger Durchgang. Sie wird weder vom Roboter noch vom Plugin gespeichert.
  - Leeres Feld Titel: ein einziger Durchgang, wie bisher.
  - Eine Zahl mit drei oder mehr Ziffern („100“, „2024“) oder Text („zwei“) wird ignoriert: Die Reinigung
    erfolgt in einem Durchgang, ohne Meldung.
  - 0, eine Zahl von 4 bis 99, eine vorzeichenbehaftete oder dezimale Zahl werden abgelehnt (siehe
    Fehlerbehebung).
  - Dieselbe Zahl gilt für jeden Raum des Befehls; bei einer Zone gilt sie für die Zone.

  | Feld Titel | Ergebnis |
  |---|---|
  | (leer), 1 | Ein Durchgang |
  | 2, 3 | Zwei oder drei Durchgänge |
  | 0, 4, 10, 99 | Abgelehnt: ganze Zahl von 1 bis 3 erwartet |
  | -1, +2, 2.5, 2,5 | Abgelehnt: vorzeichenbehaftete oder dezimale Zahl |
  | 100, 2024, deux, x2 | Ignoriert: ein einziger Durchgang, ohne Meldung |

  **Beispiel für ein Szenario**: Aktion „Räume reinigen“ mit „Cuisine, Salon“ (fiktive Namen) im Feld
  Nachricht und 2 im Feld Titel: Die beiden Räume werden in zwei Durchgängen gereinigt. Für die Zone
  erhält das Feld Nachricht `x1,y1,x2,y2` und das Feld Titel 2 oder 3.
  - Die Schaltflächen „<Raumname> reinigen“ führen immer einen einzigen Durchgang aus.
  - Ist das Feld Nachricht leer, behält das Feld Titel seine übliche Rolle (Raumnamen oder Koordinaten),
    trotz seiner Bezeichnung.
  - Das Feld trägt die Bezeichnung „Anzahl der Durchgänge (1 bis 3)“ nur, wenn der Roboter meldet,
    Wiederholungen zu unterstützen.
  - Die Wiederholungseinstellung der Roborock-App wird nie geändert. Ohne Anzahl der Durchgänge wendet der
    Roboter seine eigene Einstellung an, wie bisher.
  - Eine Anzahl von 2 oder 3 Durchgängen wird vom Plugin abgelehnt, wenn der Roboter, unmittelbar vor dem
    Befehl neu ausgelesen, nicht meldet, Wiederholungen zu unterstützen. Schlägt das Auslesen fehl, wird
    der Befehl gesendet, und der Roboter entscheidet.
- **Zu einem Punkt fahren** — erhält zwei Koordinaten `x,y` in Millimetern.
- **Saugen, dann wischen** — verkettet einen Durchgang nur saugend mit einem Durchgang nur wischend. Vier
  Befehle, die nur erstellt werden, wenn der Roboter wischen kann:
  - **Saugen, dann wischen (Räume durch Kommas getrennt, leer für die ganze Wohnung)** (Aktion): Feld
    **Nachricht** leer = ganze Wohnung; andernfalls Raumnamen durch Kommas getrennt (wie bei „Räume
    reinigen“). Die **Anzahl der Durchgänge** kommt in das Feld **Titel** (1 bis 3), nur für den Umfang
    „Räume“; sie gilt für beide Durchgänge. Für die ganze Wohnung gibt es keine Anzahl der Durchgänge: ein
    einziger Durchgang pro Schritt.
  - **Sequenz abbrechen** (Aktion): hält die laufende Sequenz an. Ohne aktive Sequenz antwortet sie, dass
    es nichts abzubrechen gibt.
  - **Status der Sequenz** (Information): „Aucune séquence“ (Keine Sequenz), „Passage 1 sur 2 :
    aspiration“ (Durchgang 1 von 2: Saugen), „En attente de la base“ (Warten auf die Basis), „Passage 2
    sur 2 : lavage“ (Durchgang 2 von 2: Wischen), „Séquence terminée“ (Sequenz beendet), „Séquence
    annulée“ (Sequenz abgebrochen), „Séquence interrompue“ (Sequenz unterbrochen), „Le second passage
    n'a pas pu démarrer“ (Der zweite Durchgang konnte nicht starten) oder „Séquence abandonnée“ (Sequenz
    aufgegeben).
  - **Grund für das Ende der Sequenz** (Information): „Aucun“ (Keiner) oder der Grund, aus dem die Sequenz
    angehalten wurde (siehe Fehlerbehebung). Diese beiden Informationen werden nicht historisiert.

  **Beispiel für ein Szenario**: Aktion „Saugen, dann wischen“ mit „Cuisine, Salon“ (fiktive Namen) im Feld
  Nachricht; ein zweiter Block kann warten, bis „Status der Sequenz“ den Wert „Séquence terminée“ hat.

  **Wie die Sequenz abläuft.**
  - Der zweite Durchgang startet erst, wenn das **normale Ende des ersten Durchgangs durch das Protokoll
    des Roboters bestätigt ist** und der Roboter an seiner Basis **seit 30 Sekunden stabil lädt** (die
    Zeit einer eventuellen Entleerung oder Wäsche). Ein Roboter, der gerade entleert wird, wird nie neu
    gestartet: Das Plugin wartet.
  - **Maximale Wartezeit auf die Basis: 15 Minuten** nach dem Ende des ersten Durchgangs. Danach wird der
    zweite Durchgang nicht gestartet.
  - Das Plugin prüft, dass der Roboter **tatsächlich gestartet ist**: Wird innerhalb von **2 Minuten** kein
    Start festgestellt, wird der Durchgang für wirkungslos erklärt.
  - **Maximale Dauer eines Durchgangs: 6 Stunden.** Danach wird die Sequenz angehalten.
  - Bei jedem Ende (erfolgreich, abgebrochen oder unterbrochen) werden die **ursprünglichen Einstellungen**
    des Roboters (Saugleistung, Wasserdurchfluss, Route) **wiederhergestellt**. Während der Sequenz
    ersetzt das Plugin sie durch Einstellungen „nur Saugen“ und dann „nur Wischen“.
  - **Während einer Sequenz werden andere Reinigungen abgelehnt**: Räume reinigen, eine Zone, eine Routine
    starten oder „Starten“ (außer, um eine pausierte Reinigung **fortzusetzen**). Brechen Sie zuerst die
    Sequenz ab.
  - **Stoppen** oder **Zurück zur Basis**, von Jeedom oder von der mobilen App aus, beenden die Sequenz:
    Der zweite Durchgang wird nicht gestartet.
  - **Kein automatischer neuer Versuch**: Kann der zweite Durchgang nicht starten, wird nichts erneut
    gesendet. Starten Sie die Sequenz selbst neu.
  - Eine Sequenz auf einem Roboter zu starten, der bereits reinigt (oder pausiert ist), wird abgelehnt.

Nach einer Einstellung von Saugleistung, Wasserdurchfluss, Wischroute oder Reinigungsmodus liest das
Plugin den Status des Roboters erneut aus, um zu prüfen, dass er die Einstellung übernommen hat. Es
gewährt bis zu etwa zwölf Sekunden, ohne den Befehl erneut zu senden: Übernimmt der Roboter ihn sofort,
wird die Antwort nicht verlangsamt. Die Meldung „nicht angewendet“ erscheint nur, wenn der Roboter den
Wert nach dieser Frist immer noch nicht hat. Wenn Sie zwei Einstellungen sehr schnell hintereinander am
selben Roboter vornehmen, wird nur die letzte geprüft: Die vorherige wird ohne Fehler als „transmis au
robot (application non confirmée)“ (an den Roboter übermittelt, Anwendung nicht bestätigt) gemeldet. Die
gleiche Meldung erscheint, wenn der Roboter während der Prüfung nicht mehr antwortet.

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

### Mehrere Roboter im selben Konto

Ein ausgeschalteter, entladener oder vom WLAN getrennter Roboter hindert nicht mehr daran, die anderen
Roboter Ihres Kontos zu steuern und zu überwachen: Er wird einfach als **offline** angezeigt. Die
Wiederverbindungsversuche zu diesem Roboter verbrauchen **kein** Roborock-Kontingent (siehe
„Roborock-Kontingente“).

Nach dem Wiedereinschalten ist der Roboter **von selbst** wieder steuerbar, ohne neue Authentifizierung
oder Neuinstallation. Rechnen Sie mit **höchstens 6 Minuten** nach der Rückkehr seiner Verbindung: Die
Wartezeit zwischen zwei Versuchen verlängert sich schrittweise bis auf **5 Minuten**.

In diesem kurzen Intervall kann der Roboter bereits **online** erscheinen, während seine Befehle noch als
**offline** abgelehnt werden. Warten Sie einige Minuten und versuchen Sie es dann erneut.

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
| „Le robot vide son bac à poussière : l'ordre de nettoyage n'a pas été envoyé…“ (Der Roboter leert seinen Staubbehälter: Der Reinigungsbefehl wurde nicht gesendet…) | Ein Reinigungsbefehl („Starten“, „Räume reinigen“, „<Raum> reinigen“, „Eine Zone reinigen“) wurde gegeben, während die Station den Behälter leert; der Roboter hätte ihn ignoriert | Warten Sie das Ende des Leerens ab (einige Sekunden bis eine Minute) und senden Sie den Befehl dann erneut. Warten Sie in einem Szenario, bis der Roboterstatus wieder „En charge“ (in Ladung) ist, bevor Sie ihn erneut senden |
| „Auf diesem Roboter läuft eine Sequenz ‚Saugen, dann wischen‘: Brechen Sie sie ab, bevor Sie eine weitere Reinigung starten.“ | Während einer Sequenz wurde eine Reinigung (Räume, Zone, Routine, „Starten“) angefordert | Klicken Sie auf „Sequenz abbrechen“, oder warten Sie ihr Ende ab, und starten Sie dann erneut |
| „Der Roboter hat bereits eine laufende oder pausierte Reinigung: Halten Sie sie an, bevor Sie ‚Saugen, dann wischen‘ starten.“ | Die Sequenz wurde gestartet, während der Roboter reinigte oder pausiert war | Halten Sie die Reinigung an und starten Sie dann die Sequenz erneut |
| Sequenz unterbrochen: „Der Roboter wurde während der Sequenz angehalten oder zur Station zurückgeschickt …“ | Sie (oder die mobile App) haben Stoppen oder Zurück zur Basis verwendet | Normal: Der zweite Durchgang wird nicht gestartet. Starten Sie die Sequenz bei Bedarf erneut |
| Sequenz unterbrochen: „Der Roboter ist während der Sequenz mit einem Fehler stehen geblieben …“ | Der Roboter hat einen Fehler gemeldet (blockiert, Behälter fehlt …) | Prüfen Sie den Status des Roboters, beheben Sie den Vorfall, starten Sie erneut |
| „Der Roboter hat den Reinigungsbefehl akzeptiert, ist aber nicht gestartet.“ | Innerhalb von 2 Minuten wurde kein Start festgestellt | Prüfen Sie den Status des Roboters (Behälter, laufende Entleerung …) und starten Sie dann erneut |
| „Der erste Durchgang wurde laut Protokoll des Roboters nicht normal beendet …“ | Das Protokoll des Roboters stuft den ersten Durchgang nicht als normal beendet ein | Der zweite Durchgang wird vorsichtshalber nicht gestartet: Prüfen Sie das Reinigungsprotokoll, starten Sie bei Bedarf erneut |
| „Das normale Ende des ersten Durchgangs konnte im Protokoll des Roboters innerhalb der Wartezeit nicht bestätigt werden …“ („Le second passage n'a pas pu démarrer“) | Das Protokoll des Roboters hat das Ende des ersten Durchgangs nicht innerhalb von 15 Minuten bestätigt | Das Plugin startet das Wischen nie ohne diese Bestätigung: Starten Sie die Sequenz erneut, oder starten Sie ein reines Wischen von Hand |
| „Der Roboter war nach dem ersten Durchgang innerhalb der maximalen Wartezeit nicht wieder verfügbar …“ | Nach dem ersten Durchgang ist der Roboter innerhalb von 15 Minuten nicht an seine Basis zurückgekehrt und dort geladen (seit mindestens 30 Sekunden stabil) (von der Basis genommen, Entleerung blockiert …) | Setzen Sie den Roboter wieder auf seine Basis und starten Sie die Sequenz dann erneut |
| „Der Roboter wurde außerhalb der Sequenz neu gestartet …“ | Während des Wartens auf die Basis wurde eine Reinigung gestartet (zum Beispiel über die mobile App) | Der zweite Durchgang wird nicht gestartet: Starten Sie die Sequenz erneut, sobald der Roboter an der Basis ist |
| „Der laufende Durchgang wurde nicht innerhalb der vorgesehenen Höchstdauer abgeschlossen …“ | Ein Durchgang dauert länger als 6 Stunden | Die Sequenz wird angehalten: Prüfen Sie den Roboter |
| „Das Plugin konnte den Roboter mehrere Minuten lang nicht verfolgen …“ | Roboter oder Netzwerk mehrere Minuten lang nicht erreichbar | Der Roboter kann seinen Durchgang fortgesetzt haben; seine ursprünglichen Einstellungen werden nicht wiederhergestellt: Prüfen Sie seinen Reinigungsmodus |
| „Die ursprünglichen Einstellungen des Roboters konnten nicht wiederhergestellt werden …“ | Die Wiederherstellung ist am Ende der Sequenz fehlgeschlagen | Prüfen und korrigieren Sie den Reinigungsmodus des Roboters |
| „Séquence abandonnée“ (Sequenz aufgegeben): „Die Sequenz wird vom Dämon nicht mehr verfolgt …“ | Der Daemon wurde während der Sequenz angehalten oder neu gestartet (oder der Daemon ist abgestürzt) | Der zweite Durchgang wird nicht gestartet; der Roboter kann seinen Durchgang fortgesetzt haben, und seine ursprünglichen Einstellungen werden nicht wiederhergestellt: Prüfen Sie sie und starten Sie bei Bedarf erneut |
| „Die Roborock-Sitzung des Plugins hat sich während der Sequenz geändert …“ | Das Konto wurde während der Sequenz gewechselt oder entfernt | Gleiche Folge: Einstellungen nicht wiederhergestellt, zu prüfen |
| „Auf diesem Roboter läuft keine Sequenz ‚Saugen, dann wischen‘: nichts abzubrechen.“ | **Sequenz abbrechen** wurde angefordert, obwohl keine Sequenz aktiv ist (sie war bereits beendet) | Nichts zu tun: Sehen Sie in der Zeile **Sequenz** nach |
| „Abbruch registriert: Der Roboter wird angehalten …“ | Der Abbruch wurde berücksichtigt, aber ein Befehl wird noch gesendet | Normal: Warten Sie einige Sekunden; der Status wechselt auf „Séquence annulée“ |
| „Sequenz abgebrochen, aber das Anhalten des Roboters ist fehlgeschlagen …“ oder „Sequenz abgebrochen; die ursprünglichen Einstellungen des Roboters konnten nicht wiederhergestellt werden.“ | Der Roboter hat das Anhalten nicht bestätigt, oder die Wiederherstellung seiner Einstellungen ist fehlgeschlagen | Prüfen Sie den Status des Roboters, halten Sie ihn bei Bedarf über das Panel an und kontrollieren Sie seine Einstellungen |
| Schaltfläche „Saugen, dann wischen“ fehlt | Der Roboter kann nicht wischen, oder der Reiter Bereich ist geöffnet (die Sequenz gibt es nur für Gesamt und Raum) | Normal: Öffnen Sie den Reiter Gesamt oder Raum; bei einem Roboter ohne Wischfunktion gibt es die Funktion nicht |
| „Ungültige Anzahl an Durchgängen: Geben Sie eine ganze Zahl von 1 bis 3 ein …“ | Das Feld Titel einer Raum- oder Zonenreinigung (bei ausgefülltem Feld Nachricht) enthält eine abgelehnte Zahl: 0, 4 bis 99, vorzeichenbehaftet oder dezimal | Geben Sie 1, 2 oder 3 in Ziffern ein, oder lassen Sie das Feld für einen einzigen Durchgang leer |
| „Anzahl der Durchgänge wird von diesem Roboter nicht unterstützt …“ | Es wurde eine Anzahl von 2 oder 3 Durchgängen angegeben, aber der Roboter meldet nicht, Wiederholungen zu unterstützen | Leeren Sie das Feld der Anzahl der Durchgänge: Die Reinigung erfolgt dann in einem einzigen Durchgang |
| „Ungültiges Zeitfenster: Geben Sie Beginn und Ende im Format HH:MM zwischen 00:00 und 23:59 an.“ (Nicht stören, Nebentarifzeiten) | Eines der beiden Felder von „Zeitfenster … festlegen“ ist leer, fehlerhaft (22h00, 2200, 22:5) oder außerhalb der Grenzen (24:00, 22:60) | Geben Sie beide Uhrzeiten im Format HH:MM an (7:30 wird akzeptiert), zwischen 00:00 und 23:59, und starten Sie dann erneut |
| „Ungültiges Zeitfenster: Beginn und Ende … müssen unterschiedlich sein.“ | Beginn und Ende des Zeitfensters sind identisch | Wählen Sie zwei unterschiedliche Uhrzeiten (ein Zeitfenster über Mitternacht wie 22:00 → 07:00 wird akzeptiert) |
| „Der Roboter hat kein verwertbares … Zeitfenster zurückgegeben: Legen Sie das Zeitfenster fest …“ | „Aktivieren“ (Nicht stören oder Nebentarifzeiten) hat kein gespeichertes Zeitfenster, das erneut angewendet werden könnte | Starten Sie „Zeitfenster … festlegen“ mit Beginn und Ende: Das aktiviert auch die Funktion |
| „Ungültige Lautstärke: Geben Sie eine ganze Zahl zwischen 0 und 100 an.“ | Der Wert ist leer, dezimal (50.5), negativ oder größer als 100 | Geben Sie eine ganze Zahl von 0 bis 100 an; runden Sie in einem Szenarioausdruck mit `round(...)` |
| „Dieser Entleerungsmodus (oder Waschmodus) ist an der Basisstation dieses Roboters nicht verfügbar: Aktualisieren Sie den Status, bevor Sie es erneut versuchen.“ | Der angeforderte Modus-Code ist für diese Station nicht bekannt (veraltete Liste, oder falscher Code in einem Szenario) | Starten Sie „Aktualisieren“, laden Sie die Seite des Geräts neu und wählen Sie dann einen Modus aus der Liste des Befehls |
| „Ein Befehl (oder eine Einstellung) … wurde soeben an diesen Roboter gesendet: Warten Sie einige Sekunden, bevor Sie einen weiteren senden.“ (Kindersicherung, Nicht stören, Nebentarifzeiten, Lautstärke, Entleerungsmodus, Waschmodus) | Zwei Befehle desselben Typs am selben Roboter im Abstand von weniger als 5 Sekunden | Warten Sie mindestens 5 Sekunden; fügen Sie in einem Szenario eine Pause von 5 Sekunden zwischen den beiden Aktionen ein |
| „Der Roboter (oder die Station) hat … nicht angewendet: Der zurückgelesene Zustand entspricht nicht der Anforderung.“ (Kindersicherung, Nicht stören, Nebentarifzeiten, Lautstärke, Entleerungsmodus, Waschmodus) | Der Roboter antwortet, hat die Einstellung aber nach Ablauf der Prüffrist nicht übernommen (einige Sekunden, bis zu etwa zwölf) | Kontrollieren Sie den vom entsprechenden Informationsbefehl angezeigten Wert (er zeigt, was der Roboter tatsächlich übernommen hat) und starten Sie den Befehl erneut; wiederholt sich das, versuchen Sie es bei ruhendem Roboter oder an seiner Basis |
| „Dieser Wartungsvorgang ist auf der Station dieses Roboters nicht verfügbar“ | Die Station dieses Roboters unterstützt diese Aktion nicht | Das ist normal: Der Befehl sollte nicht erscheinen, wenn die Station es nicht zulässt; aktualisieren Sie den Status des Roboters |
| „Die von der Roborock-Cloud empfangene Routinenliste ist unvollständig: Aus Vorsicht wurde keine Routine gelöscht.“ | Die Antwort der Cloud wurde abgeschnitten, oder dieser Roboter hat mehr als 64 Routinen | Starten Sie die Synchronisierung später erneut; in der Zwischenzeit ist nichts verloren gegangen |
| „Die Roborock-Nutzungsbedingungen wurden nicht akzeptiert“ (oder „haben sich geändert“) | Roborock verlangt die (erneute) Bestätigung seiner Nutzungsbedingungen | Öffnen Sie die Roborock-App, akzeptieren Sie die vorgeschlagenen Bedingungen und versuchen Sie es dann erneut von Jeedom aus |
| „Roboter unbekannt beim Daemon“ | Das Jeedom-Gerät wird vom Daemon nicht mehr erkannt (Neustart, Roboter aus dem Konto entfernt …) | Starten Sie „Geräte synchronisieren“ erneut |
| „Die Roborock-Cloud ist nicht erreichbar“ | Jeedom erreicht die Roborock-Server nicht | Prüfen Sie den Internetzugang des Jeedom-Servers |
| Eine Meldung zu einer überschrittenen **Zeitvorgabe**, einer **fehlgeschlagenen Verbindung** oder „mehrere Kommunikationsversuche sind fehlgeschlagen“ | Der Roboter oder die Roborock-Cloud hat zu lange zum Antworten gebraucht: vorübergehende Netzwerkstörung, oder stark beanspruchter Roboter | Versuchen Sie es nach einer Minute erneut; wiederholt sich dies, prüfen Sie die WLAN-Verbindung des Roboters und den Internetzugang des Jeedom-Servers |
| „Der Roboter ist beschäftigt“, „Der Roboter hat die Aktion in seinem aktuellen Zustand abgelehnt“ oder „Der Roboter hat einen Fehler gemeldet“ | Der Roboter kann diese Anfrage in seinem aktuellen Zustand nicht ausführen (laufende Reinigung, voller Behälter, mechanischer Vorfall …) | Prüfen Sie den Status des Roboters (Befehl „Status“, oder mobile App), beheben Sie den gemeldeten Vorfall und starten Sie die Aktion dann erneut |
| „Diese Funktion ist bei diesem Robotermodell nicht verfügbar“ oder „Der Roboter erkennt diesen Befehl nicht“ | Der Roboter implementiert diese Funktion nicht, obwohl der Befehl in Jeedom existiert | Keine Manipulation wird die Situation entblockieren: Diese Funktion existiert auf dieser Hardware nicht, blenden Sie den Befehl aus, wenn er Sie stört |
| „Keine laufende Codeanfrage“ | Der Daemon hat zwischen dem Senden und der Bestätigung des Codes neu gestartet | Klicken Sie erneut auf „Code senden“ und bestätigen Sie dann den neu erhaltenen Code |
| „… transmis au robot (application non confirmée).“ (an den Roboter übermittelt, Anwendung nicht bestätigt) nach einer Einstellung | Das Plugin konnte nicht prüfen, ob der Roboter den Wert übernommen hat: Unmittelbar danach wurde eine andere Einstellung am selben Roboter gesendet, oder der Roboter antwortete während der Prüfung nicht mehr. Das ist kein Fehler | Prüfen Sie den vom entsprechenden Informationsbefehl angezeigten Wert; senden Sie die Einstellung erneut, wenn er nicht stimmt |
| Eine Einstellung (Saugleistung, Wasserdurchfluss, Route, Reinigungsmodus) wird nicht angewendet | Der Roboter hat den Wert etwa zwölf Sekunden nach dem Empfang immer noch nicht übernommen: Er verweigert diese Einstellung in seinem aktuellen Zustand (in der Regel: nicht im Ruhezustand) | Versuchen Sie es erneut, sobald der Roboter im Ruhezustand oder an seiner Basis ist |
| „Diese Saugleistung / dieser Wasserdurchfluss / diese Route / dieser Reinigungsmodus ist bei diesem Roboter nicht verfügbar“ | Die von Jeedom bekannte Stufenliste ist veraltet (der Roboter meldet diesen Wert nicht mehr) | Aktualisieren Sie den Status des Roboters und versuchen Sie es erneut |
| „Sie sind nicht berechtigt, diesen Roboter zu steuern.“ (Steuerungspanel und Reiter Station und Wartung), ausgegraute Schaltflächen | Ihr Jeedom-Konto hat für diesen Roboter nur das Leserecht | Bitten Sie einen Administrator, Ihnen das Ausführungsrecht für diesen Roboter zu erteilen (Benutzerverwaltung von Jeedom) |
| „Kein Roborock-Roboter mit Ihrem Konto zugänglich.“ (oder „Gerät nicht gefunden oder nicht zugänglich.“) | Kein aktivierter Roboter, für den Ihr Konto das Leserecht hat; dieselbe Meldung erscheint auch bei einem nicht vorhandenen oder deaktivierten Roboter | Bitten Sie einen Administrator um das Leserecht, oder prüfen Sie, dass der Roboter aktiviert ist |
| „401 - Nicht autorisierter Zugriff“ beim Öffnen der Kartenseite | Ihre Jeedom-Sitzung ist abgelaufen | Melden Sie sich erneut bei Jeedom an |
| Der Eintrag JeeRoborock erscheint nicht unter Startseite | Das Kästchen **Desktop-Panel anzeigen** ist in der Plugin-Verwaltung nicht angekreuzt | Kreuzen Sie es an (siehe „Panel ‚Karte‘ (Startseite > JeeRoborock)“) |
| „Roboter offline: Die Befehle sind inaktiv, bis er wieder erreichbar ist.“ | Der Roboter antwortet nicht auf die Roborock-Cloud | Prüfen Sie seine Stromversorgung und sein WLAN; die Schaltflächen werden bei seiner Rückkehr wieder aktiv, ohne etwas neu zu laden |
| „Funktion für diesen Roboter nicht verfügbar.“ oder eine im Panel fehlende Schaltfläche | Der Roboter unterstützt diese Einstellung oder Aktion nicht | Normal: Das Panel bietet nur an, was Ihr Roboter kann |
| „Befehl vom Roboter abgelehnt.“ (ohne weitere Angabe) | Der Befehl wurde ohne genauere Meldung abgelehnt | Prüfen Sie den Status des Roboters (Behälter, Fehler, nicht an der Basis) und starten Sie dann erneut |
| Die Hauptschaltfläche bleibt inaktiv, Reiter Raum: „Für diesen Roboter ist kein Raum verfügbar: Synchronisieren Sie seine Räume über die Seite des Geräts.“ | Es wurde noch kein Raum synchronisiert | Klicken Sie im Reiter Gerät auf „Räume neu synchronisieren“ |
| „Zu viele Räume ausgewählt: Starten Sie die Reinigung in mehreren Durchgängen.“ | Die Anzahl der Räume pro Befehl ist begrenzt | Entfernen Sie Häkchen bei einigen Räumen, starten Sie in mehreren Durchgängen |
| „Einige Räume können hier nicht ausgewählt werden …“ oder „Dieser Raum kann hier nicht ausgewählt werden …“ | Der Raum hat keinen Namen, sein Name kommt doppelt vor oder enthält ein Komma | Benennen Sie ihn in der Roborock-App um und synchronisieren Sie die Räume anschließend erneut |
| „Raum auf der aktuellen Karte unbekannt: synchronisieren Sie die Räume über die Geräteseite erneut.“ | Ein angehakter Raum existiert auf der Karte nicht mehr (neue Unterteilung, Etagenwechsel) | Entfernen Sie das Häkchen, oder synchronisieren Sie die Räume erneut; die Start-Schaltfläche bleibt inaktiv, solange er angehakt ist |
| „Veraltete Karte: Auswahl nicht möglich.“ oder „Die Karte erlaubt keine Abgrenzung der Räume: wählen Sie sie in der Liste aus.“ | Die angezeigte Karte ist ein altes Bild oder enthält keine Raumkonturen | Wählen Sie die Räume in der Liste des Reiters Raum aus; die Karte erneuert sich während der Reinigungen |
| „Karte nicht verfügbar: Bereich kann nicht gezeichnet werden.“, „Bereich zu klein: Zeichnen Sie ein größeres Rechteck.“ oder „Der Bereich muss vollständig auf der Karte liegen.“ | Keine verwertbare Karte, oder das Rechteck ist zu klein oder ragt über die Karte hinaus | Zeichnen Sie ein größeres Rechteck, vollständig auf der Karte; ohne Karte reinigen Sie nach Raum oder im Reiter Gesamt |
| „Dieser Roboter hat keine Station.“ (Reiter Station und Wartung) | Der Roboter hat keine Dockingstation | Normal: nichts zu tun |
| Schaltflächen **Entleeren**, **Waschen**, **Trocknen** inaktiv, Hinweis „Vorgang läuft“ | Ein Stationsvorgang läuft, oder ein Befehl wurde gerade gesendet (höchstens 2 Minuten) | Warten Sie; **Trocknung stoppen** ist nur während einer Trocknung aktiv |
| „Störung der Station“ oder „Ein oder mehrere Verbrauchsmaterialien müssen gewechselt werden.“ | Die Station meldet eine Störung, oder ein Verbrauchsmaterial steht bei 10 % oder weniger | Beheben Sie die Störung; ersetzen Sie das Teil und verwenden Sie dann **Zurücksetzen** |
| „Keine Daten für diesen Tag.“ oder „Zeitverlauf derzeit nicht verfügbar.“ (Zeitleiste) | Für diesen Tag ist kein Zustand aufgezeichnet (Plugin erst seit Kurzem installiert, oder Tag außerhalb der letzten 7); oder das Auslesen ist fehlgeschlagen | Wechseln Sie den Tag; bei Nichtverfügbarkeit laden Sie die Seite neu. Die Meldung „Ungültiger Tag oder außerhalb des Aufbewahrungszeitraums.“ bedeutet, dass ein mehr als 7 Tage zurückliegender Tag angefordert wurde |
| Mobil: „Das Panel kann nicht geladen werden: Kehren Sie zur Startseite zurück und öffnen Sie es erneut.“ oder „Das Bedienfeld kann nicht geladen werden. Laden Sie die Seite neu.“ | Die Roboterliste oder die Skripte des Panels konnten nicht geladen werden (Netzwerk, Sitzung, alte Version im Cache) | Öffnen Sie das Panel erneut; schließen Sie bei Bedarf die Jeedom-App vollständig und öffnen Sie sie erneut |
| Mobil: „Auf dem Handy nicht verfügbar“ | Die Seite Station und Wartung, der Tagesverlauf und die Tabelle der erkannten Räume gibt es auf dem Smartphone nicht | Normal: Öffnen Sie die Kartenseite von Jeedom auf einem Computer |
| „Unbekannter Raum“, „kein bekannter Raum“ oder „mehrere Räume tragen diesen Namen“ | Der eingegebene Name entspricht keinem erkannten Raum, noch wurde kein Raum synchronisiert, oder der Name ist mehrdeutig | Synchronisieren Sie die Räume über den Reiter Gerät neu, verwenden Sie den genauen Namen aus der Roborock-App, oder den diesem Raum zugeordneten Befehl statt des allgemeinen Befehls |
| Der Befehl „Aktueller Raum“ bleibt auf „Pièce inconnue“ | Die Räume wurden nie synchronisiert, oder die aktive Karte hat sich geändert | Klicken Sie im Reiter Gerät auf „Räume neu synchronisieren“ |
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

## Aktualisierung des Plugins

Die Funktionen der manuellen Steuerung (Panel, interaktive Karte, Station, „Saugen, dann wischen“,
Tagesverlauf, mobiles Panel) erfordern nach der Aktualisierung **keine Maßnahme von Ihrer Seite**: keine
Konfiguration neu vorzunehmen, kein Gerät neu zu erstellen. Zwei Handgriffe können dennoch nützlich sein:
den Daemon neu starten (sonst erscheinen die Zustände auf der Zeitleiste als „Anderer Zustand“) und, auf
dem Smartphone, die App neu synchronisieren oder vollständig schließen.

## Bekannte Einschränkungen

- Das Plugin steuert nur Roboter, die mit dem V1-Protokoll von Roborock kompatibel sind, über die
  Cloud. Ältere Roboter (Protokoll A01) werden nicht unterstützt.
- Die vom Roboter selbst erzeugten Bezeichnungen (Status, Fehler, Stationsstatus, Namen von
  Verbrauchsmaterialien) bleiben **immer auf Französisch**, unabhängig von der für die Jeedom-Oberfläche
  gewählten Sprache. Dasselbe gilt für die Werte „Aucune pièce“ und „Pièce inconnue“ des Befehls „Aktueller Raum“.
- Ein von der mobilen App aus vorgenommener Kartenwechsel wird nun automatisch im Hintergrund innerhalb
  von etwa einer Minute erkannt: Die aktive Karte, das Bild und das Koordinatensystem der Karte werden
  ohne Ihr Zutun aktualisiert (die Raumliste dagegen wird geleert und wartet auf einen Klick auf
  „Räume neu synchronisieren“). Während dieser kurzen Verzögerung kann die Konfiguration noch die
  alte Etage anzeigen, und eine bereits geöffnete Geräteseite aktualisiert sich nicht von selbst: Laden
  Sie sie neu. Ebenso kann der Befehl „Aktueller Raum“ kurzzeitig (höchstens eine Minute) einen Raum
  der alten Etage anzeigen und wechselt dann auf „Pièce inconnue“, bis die Räume neu synchronisiert wurden.
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
- Ein ausgeschalteter oder vom WLAN getrennter Roboter, der sich wieder verbindet, ist von selbst wieder
  steuerbar, aber nach einer Verzögerung von bis zu **6 Minuten** (siehe „Mehrere Roboter im selben
  Konto“): Diese Verzögerung ist nicht einstellbar.
- Die Verweigerung eines Reinigungsbefehls während des Leerens des Behälters betrifft nur den Status
  „Vidage du bac à poussière“ (Staubbehälter wird geleert): Die anderen Zustände der Station (Waschen,
  Trocknen) lösen diese Verweigerung nicht aus. Sie betrifft weder die Routinen noch „Zu einem Punkt
  fahren“. Kein Befehl wird in eine Warteschlange gestellt: Es liegt an Ihnen (oder Ihrem Szenario), ihn
  erneut zu senden.
- Die automatische Aktualisierung der letzten Reinigung ist **begrenzt**: höchstens fünf Auslesungen
  innerhalb von 30 Minuten nach dem Ende der Reinigung. Danach hört das Plugin auf, es zu versuchen;
  nutzen Sie „Protokoll aktualisieren“.
- Ein bereits in codierter Form gespeicherter Kartenname (vor dem Plugin-Update) bleibt codiert bis zum
  ersten „Kartenliste aktualisieren“ oder Kartenwechsel.
- Das Auslesen der Raumnamen (Panel „Räume“ des Reiters Gerät) erfordert, dass der Roboter **online**
  ist: Es schlägt fehl, wenn der Roboter zum Zeitpunkt des Klicks nicht erreichbar ist.
- Die Kartenansicht (Panel „Startseite > JeeRoborock“) löst von sich aus nichts aus (ein Befehl wird nur
  bei Ihrem Klick im Steuerungspanel gesendet) und startet keine Aktualisierung: Sie zeigt lediglich
  alle 30 Sekunden das zuletzt bekannte Bild an. Dieses Bild wird nur während der Reinigungen neu
  erstellt; im Ruhezustand kann es daher vom letzten Durchgang des Roboters stammen.
- Mobiles Panel: **reduzierte** Version des Steuerungspanels. Weder die Seite Station und Wartung noch
  der Tagesverlauf noch die Tabelle der erkannten Räume sind auf dem Smartphone verfügbar: Sie gibt es nur
  auf dem Computer. Der eigene Reiter des benutzerdefinierten Menüs der Jeedom-App ist den Administratoren
  vorbehalten. Das Panel wurde nicht auf allen Smartphones erprobt: Ein Gerät kann Darstellungsfehler
  zeigen.
- **Sperrzonen und virtuelle Wände**: auf der Karte **schreibgeschützt** angezeigt. Um sie zu erstellen,
  zu verschieben oder zu löschen, verwenden Sie die Roborock-App; das Plugin blockiert einen auf eine
  Sperrzone gezeichneten Bereich nicht.
- **Roboter offline**: Das Panel, die Seite Station und Wartung und die Verkettung „Saugen, dann wischen“
  nehmen keinen neuen Befehl an. Nur **Sequenz abbrechen** bleibt während einer Sequenz möglich. Die
  letzten Zustände und die letzte Karte bleiben angezeigt.
- **Zwei Roboter, zwei Sequenzen**: Jeder Roboter hat seine eigene Sequenz „Saugen, dann wischen“, die
  unabhängig von der des anderen verfolgt und abgebrochen wird.
- **Station und Wartung**: Bei einem Roboter **ohne Station** zeigt der Reiter nur „Dieser Roboter hat
  keine Station.“ an. Bei einem Roboter mit Station erscheinen nur die Aktionen und Zustände, die dieser
  Roboter beherrscht.
- **Tagesverlauf**: Die Zeitleiste wird aus den Zuständen rekonstruiert, die das **Plugin selbst
  aufgezeichnet hat** (es wird nichts bei der Roborock-Cloud abgefragt). Sie enthält keine Daten vor der
  Installation des Updates. Nur die **letzten 7 Tage** werden aufbewahrt; ältere werden gelöscht. Ab einer
  sehr hohen Anzahl von Aufzeichnungen für denselben Tag endet die Aufzeichnung dieses Tages: Das Ende der
  Zeitleiste dieses Tages bleibt leer.
- Zeitleiste „Tagesverlauf“: **„Offline“** bedeutet, dass der Roboter **nicht antwortet**; eine einzige
  überschrittene Frist genügt, es handelt sich nicht zwangsläufig um einen langen Ausfall.
- Auf der Zeitleiste erscheinen eine **Pause** während einer Reinigung, die **Fahrt zu einem Ziel**, die
  **Kartierung** und das **Anbringen oder Abnehmen des Wischmopps** als **Anderer Zustand**. Das
  **Trocknen**, das während des Ladens stattfindet, erscheint als **Wird geladen**: „Mopp-Trocknung“
  deckt nur das Trocknen ab, das der Roboter als solches meldet.
- Nach einer Aktualisierung des Plugins erscheinen die Zustände auf der Zeitleiste als **Anderer
  Zustand**, solange der **Daemon nicht neu gestartet wurde**. Starten Sie den Daemon neu.
- Die Genauigkeit von **„Unbekannt“** liegt in der Größenordnung von **einigen Minuten**: Der Beginn kann
  dem tatsächlichen Ausfall um einige Minuten vorausgehen. Ein Ausfall von **weniger als 15 Minuten** ohne
  Neustart des Daemons erscheint nicht.
- Nur die **10 letzten Reinigungen** des Protokolls können auf der Zeitleiste hervorgehoben werden.
- Die von der Dashboard-Kachel übernommenen Befehle (Batterie, Reinigt, Fehler, Verbunden, Online und
  die fünf Steuerungsaktionen) werden nur einmal ausgeblendet, bei der Erstellung der Kachel. Blenden
  Sie einen davon manuell wieder ein, blendet das Plugin ihn nie wieder aus: Ihre Wahl bleibt erhalten.
- Auf einer von einer älteren Plugin-Version aktualisierten Installation hat eine einmalige technische
  Migration möglicherweise die Historisierung des Befehls „Fehler“ reaktiviert: Wenn Sie diesen Befehl
  nicht historisieren möchten, deaktivieren Sie es manuell in seiner Konfiguration.
- Nur der **Roborock Qrevo Curv** ist getestet. Die durch die Parität mit Home Assistant hinzugefügten
  Fähigkeiten (Verbrauchsmaterialien und Tanks der Station, Kindersicherung, Nicht stören,
  Nebentarifzeiten, Lautstärke, Modi der Station, Anzahl der Durchgänge, aktueller Raum) haben bei einem
  anderen Modell, einschließlich des Roborock S7, **keinerlei Garantie**: Das Plugin erstellt die Befehle,
  die der Roboter meldet oder auf die er antwortet, ohne deren tatsächliche Wirkung auf jeder Hardware
  prüfen zu können. Ein akzeptierter Befehl kann vom Roboter abgelehnt werden; dies wird dann gemeldet
  (siehe Fehlerbehebung).
- Die Verschleißanzeige des **Staubbeutels** der Station ist schreibgeschützt: Das Plugin hat keine Aktion,
  um sie zurückzusetzen. Die Prozentwerte der Verbrauchsmaterialien können leicht von denen der App
  abweichen.
- Die Einstellungen des Geräts (Kindersicherung, Nicht stören, Nebentarifzeiten, Lautstärke, Modi der
  Station) werden dem Plugin **nicht gepusht**: Eine Änderung in der Roborock-App oder über die Taste des
  Roboters erscheint in Jeedom erst beim nächsten Auslesen (etwa eine Minute, oder „Aktualisieren“).
- Das Plugin sendet einen Einstellungsbefehl nach einer Ablehnung oder einem Fehlschlag **nie** von selbst
  erneut: Starten Sie ihn selbst neu. Zwei Befehle desselben Typs am selben Roboter müssen mindestens
  5 Sekunden Abstand haben.
- „Deaktivieren“ bei Nicht stören oder den Nebentarifzeiten behält normalerweise das gespeicherte
  Zeitfenster bei, aber dieses Verhalten hängt vom Roboter ab und ist nicht bestätigt.
- Die Anzahl der Durchgänge ist ein Parameter jedes Reinigungsbefehls nach Raum oder Zone, nie eine
  gespeicherte Einstellung. Bei einer Zone konnte nicht bei allen Modellen bestätigt werden, wie der
  Roboter den Wiederholungswert auslegt: Ergibt „2“ bei Ihrem Roboter keine zwei Durchgänge, melden Sie
  dies. Die Schaltflächen „<Raumname> reinigen“ bleiben bei einem einzigen Durchgang.
- Die Listen der Entleerungs- und Waschmodi stammen aus der vom Plugin verwendeten Bibliothek, nicht von
  der Station: Ein Modus der Roborock-App kann fehlen, ein angebotener Modus kann von der Station
  abgelehnt werden. Ein unbekannter Modus-Code wird als „Mode inconnu (N)“ angezeigt.
- Der Befehl „Aktueller Raum“ hängt vom zuletzt gelesenen Kartenbild ab: Im Ruhezustand kann er etwa eine
  Minute Verzögerung haben, und er behält seinen letzten Wert, wenn der Roboter offline ist. Nach einem in
  der App vorgenommenen Kartenwechsel kann er kurzzeitig einen Raum der alten Etage anzeigen, bevor er auf
  „Pièce inconnue“ wechselt (siehe oben).

- **Saugen, dann wischen**: Ändern Sie während einer Sequenz eine Einstellung des Roboters (Saugleistung,
  Wasserdurchfluss, Route), wird sie von der Wiederherstellung am Ende **überschrieben**. Hört das Plugin
  auf, die Sequenz zu verfolgen („Séquence abandonnée“, Neustart des Daemons), oder wird das Konto
  gewechselt, werden die ursprünglichen Einstellungen **nicht wiederhergestellt**: Prüfen Sie sie. Eine
  während eines Durchgangs über die **mobile App** gestartete Reinigung wird vom Plugin nicht abgelehnt:
  Sie wird nachträglich festgestellt, und die Sequenz endet, ohne den zweiten Durchgang zu starten. Meldet
  der Roboter den Reinigungszustand nicht, kann ein Ende des Durchgangs unerkannt bleiben: Die Sequenz
  endet dann nach 6 Stunden. Ein benutzerdefinierter oder „intelligenter“ ursprünglicher Modus wird auf die
  nächstliegende Standardeinstellung wiederhergestellt.

Diese Seite wird bei jeder neuen vom Plugin bereitgestellten Funktion aktualisiert.
