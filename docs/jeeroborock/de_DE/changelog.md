# Changelog JeeRoborock

>**WICHTIG**
>
>Wenn zu einer Aktualisierung keine Information angegeben ist, betrifft diese ausschließlich eine
>Aktualisierung der Dokumentation, der Übersetzung oder von Texten.

Das Plugin befindet sich in Version **0.x**. Es wird auf einem **Roborock Qrevo Curv** (Protokoll V1)
entwickelt und getestet: Die unten aufgeführten Funktionen sind auf dieser Hardware einsatzbereit und
sollten es auch auf den anderen V1-Robotern des Kontos sein, wobei jeder Befehl nur erstellt wird,
wenn der Roboter die entsprechende Fähigkeit meldet.

Das Plugin hält sich an die **Kontingente der Roborock-Cloud**, die mit der mobilen App geteilt
werden: Die Erkennung der Roboter und die Synchronisierungen (Routinen, Räume, Karten) erfolgen **auf
Abruf**, und kein Verbindungsversuch wird automatisch wiederholt.

## Was funktioniert

**Konto und Installation**

- Installation der Abhängigkeit `python-roborock` und dedizierter Daemon, mit Überwachung seines
  Status.
- Authentifizierung bei der Roborock-Cloud über einen **per E-Mail erhaltenen Einmalcode**: Es wird
  kein Passwort abgefragt oder gespeichert.
- Schaltfläche „Verbindung testen“, auf der Konfigurationsseite angezeigter Kontostatus und die
  explizite Meldung „Erneute Authentifizierung erforderlich“, wenn die Sitzung verloren geht.

**Geräte und Status**

- Erkennung der Roboter des Kontos und Erstellung eines Geräts pro Roboter, illustriert mit dem Foto
  des Modells. Ein Roboter entspricht immer nur einem einzigen Jeedom-Gerät: Jeder Duplizierungsversuch
  wird mit einer expliziten Meldung abgelehnt.
- Gemeldete Informationen: Status, Batterie, Reinigt, Fehler (Bezeichnung und Code), gereinigte
  Fläche, Reinigungsdauer, Fortschritt, Online, Verbunden, letzte Aktualisierung.
- Dockingstation: Staubentleerung, Wischmopp-Wäsche, Wischmopp-Trocknung, Stationsfehler,
  Wassermangel.
- Verbrauchsmaterial: verbleibender Verschleiß in % für Hauptbürste, Seitenbürste, Filter, Sensoren
  und Wischwalze.
- Aktuelle Einstellungen als Anzeige: Saugleistung, Wasserdurchfluss, Wischroute, Reinigungsmodus.
- Aktualisierung **in Echtzeit** durch den Daemon (30 s während der Reinigung, 60 s im Ruhezustand),
  und Umschaltung auf „getrennt“, wenn die Daten veralten.
- Dashboard-Kachel (Desktop und Mobil), die Foto, Status, Batterie und Steuerungsaktionen
  zusammenfasst.

**Steuerung**

- Grundaktionen: Starten, Pausieren, Stoppen, Zurück zur Basis, Orten, Aktualisieren.
- In der mobilen App definierte Routinen („Routinen“): ein Aktionsbefehl pro Routine, verwaltet über
  das Panel „Routinen“ des Reiters Gerät (Liste der bekannten Routinen, Synchronisierung auf Abruf).
- Einstellungen: Saugleistung, Wasserdurchfluss, Wischroute, Reinigungsmodus.
- Wartung an der Station: Wischmopp waschen, trocknen, Trocknen stoppen, Behälter leeren.
- Reinigung nach Raum (ein Befehl pro Raum, plus ein allgemeiner Befehl nach Namen), Reinigung einer
  rechteckigen Zone und Fahrt zu einem Punkt.
- Zurücksetzung des Verschleißzählers jedes Verbrauchsmaterials, mit Bestätigung.

**Karte**

- Bestandsaufnahme der benannten Räume und der gespeicherten Karten (Etagen), Wechsel der aktiven
  Karte, über den Reiter Gerät. Ein von der mobilen App aus vorgenommener Etagenwechsel wird ebenfalls
  automatisch verfolgt, ohne Ihr Zutun.
- Panel „Karte“ (Menü **Startseite**), zugänglich für Nicht-Administratoren: Kartenbild, Datum der
  letzten Aktualisierung, Legende der Räume, automatische Aktualisierung.

**Protokoll, Statistiken und Zeitpläne**

- Letzte Reinigung (Beginn, Dauer, Fläche, Endgrund, Fehler) und Verlaufspanel der 10 letzten
  Reinigungen, mit Aktualisierungsschaltfläche.
- Vier standardmäßig historisierte kumulierte Zähler: Gesamtdauer, Gesamtfläche, Anzahl der
  Reinigungen, Anzahl der Behälterentleerungen.
- In der mobilen App erstellte Zeitpläne, schreibgeschützt über den Reiter Gerät einsehbar.

**Dokumentation**

- Vollständige Hilfeseite des Plugins: Installation, Kontoverknüpfung, Geräte und Befehle, Routinen,
  Karte, Feinsteuerung, erneute Authentifizierung, Kontingente und Fehlerbehebungsleitfaden.
  Verfügbar auf Französisch, Englisch, Deutsch und Spanisch.

**Diagnose und Support**

- Diagnosebericht, mit einem Klick über die Plugin-Konfiguration erzeugt, ohne sensible Daten, zum
  Kopieren oder Herunterladen für eine Support-Anfrage.

## Was nicht vorgesehen ist

Das Plugin zeigt nicht den Kanal an, über den jeder Roboter erreicht wird (lokale Verbindung oder
Cloud), und verfolgt oder aktualisiert die Firmware nicht: Diese beiden Funktionen wurden
zurückgestellt. Die Firmware-Aktualisierung erfolgt über die Roborock-App.

# 23.09.2026

- Korrektur: Die Schaltfläche „Starten“ setzt nun eine pausierte Reinigung fort, statt einen
  vollständigen Zyklus neu zu starten, auch bei einer Reinigung nach Raum oder Zone.
- Korrektur: Eine abgelaufene Roborock-Sitzung wird nun auch bei der Synchronisierung der Routinen,
  deren Ausführung, dem Lesen der Räume und dem Verbindungstest erkannt: Das Plugin zeigt „Erneute
  Authentifizierung erforderlich“ statt eines allgemeinen Fehlers an. <!-- UC36 -->
- Neu: neuer Diagnosebericht in der Plugin-Konfiguration: Status von Daemon, Konto und Robotern,
  Version von python-roborock und aktuelle Fehler, ohne jegliche Kennung, Token, Seriennummer oder
  E-Mail-Adresse, mit einem Klick zu kopieren oder herunterzuladen. <!-- UC30 -->
- Dokumentation: Die Dokumentation des Plugins erklärt, wie ein Diagnosebericht für eine
  Support-Anfrage erstellt und übermittelt wird. <!-- UC30 -->
- Dokumentation: Die Dokumentation stellt klar, dass das Plugin auch bei einem versuchten lokalen
  Verbindungsaufbau zum Roboter von der Roborock-Cloud abhängig bleibt, gibt an, was einer
  Hilfeanfrage beizufügen ist und was nie veröffentlicht werden darf, und ergänzt den
  Fehlerbehebungsleitfaden um den Diagnosebericht. <!-- UC59 -->
- Weiterentwicklung: Die Routinen haben ihr eigenes Panel „Routinen“ im Reiter Gerät des Roboters:
  Liste der bekannten Routinen, Synchronisierungsschaltfläche und vor dem Klick angezeigte Regel; eine
  in der Roborock-App gelöschte Routine wird nun in Jeedom gelöscht statt als veraltet markiert, und
  der Bericht nennt sie. <!-- UC35 -->
- Korrektur: Ein in Jeedom angepasster Routinenname wird bei der zweiten Synchronisierung nicht mehr
  vom Namen der Roborock-App überschrieben. <!-- UC35 -->
- Dokumentation: Abschnitt zu den Routinen neu geschrieben (Panel „Routinen“, Synchronisierungsregel,
  Fall, in dem nichts gelöscht wird). <!-- UC35 -->
- Dokumentation der Routinen ergänzt: wann ihre Synchronisierung zu starten ist, was sie kostet (kein
  Kontingent), was bei einem Fehlschlag passiert, und Hinweis, dass die Schaltfläche zur
  Gerätesynchronisierung die Routinen nicht synchronisiert. <!-- UC89 -->
- Korrektur: Ein von der Roborock-App aus vorgenommener Etagenwechsel wird nun von Jeedom innerhalb
  einer Minute erkannt: Die aktive Karte wird aktualisiert, und die Raumliste, das Bild und das
  Koordinatensystem der alten Etage werden ungültig gemacht wie bei einem von Jeedom aus vorgenommenen
  Wechsel. <!-- UC38 -->
- Dokumentation: Die Dokumentation beschreibt die automatische Verfolgung eines von der mobilen App
  aus vorgenommenen Etagenwechsels und seine verbleibenden Einschränkungen. <!-- UC38 -->
- Korrektur: Der Name eines Raumbefehls, der ein Apostroph, ein Kaufmanns-Und, eine Raute oder ein
  Prozentzeichen enthält, folgt nun den in der Roborock-App vorgenommenen Umbenennungen, unter
  Beibehaltung eines in Jeedom angepassten Namens. <!-- UC39 -->
- Korrektur: Ein Roboter kann nicht mehr zwei Jeedom-Geräten zugeordnet werden: Die Schaltfläche
  „Duplizieren“ wird entfernt, und jeder Versuch wird mit einer Meldung abgelehnt, die das vorhandene
  Gerät nennt. <!-- UC39 -->
- Korrektur: Lange und akzentuierte Namen von Räumen, Routinen, Karten und Robotern werden nicht mehr
  mitten in einem Zeichen abgeschnitten. <!-- UC39 -->
- Dokumentation: Die Dokumentation stellt klar, dass ein Roboter einem einzigen Jeedom-Gerät entspricht
  und dass der Name der Raumbefehle den in der App vorgenommenen Umbenennungen folgt. <!-- UC39 -->
- Korrektur: Die Anzeige „Online“ folgt nun tatsächlich dem Verbindungsverlust und der -rückkehr des
  Roboters, ein unbekannter Stationsfehler wird als „Erreur de station non reconnue“ (Nicht erkannter
  Stationsfehler) statt als „Aucune“ (Keine) angezeigt, und die nicht vom Roboter gepushten Felder
  (Station, Fläche, Fortschritt) bleiben nicht mehr eingefroren, wenn der Roboter viele Aktualisierungen
  sendet. <!-- UC40 -->
- Dokumentation: Die Dokumentation unterscheidet nun zwischen den Anzeigen „Online“ und „Verbunden“
  und erwähnt die Bezeichnung „Erreur de station non reconnue“ (Nicht erkannter Stationsfehler).
  <!-- UC40 -->
- Weiterentwicklung: interne Härtung: Das Plugin verweigert eine ungewöhnlich umfangreiche
  Aktualisierung von seinem Daemon, die Quelldatei des Konfigurationsformulars ist über das Web nicht
  mehr zugänglich, der Daemon meldet beim Start eine nicht geprüfte Version der Kartenrender-Bibliothek
  oder ein nicht gedrosseltes Protokoll der Roborock-Bibliothek, und das vom Plugin-Vorlage geerbte
  Beispielfenster wird entfernt. <!-- UC41 -->
- Korrektur: Zwei schnelle Klicks (oder zwei Tabs) auf dieselbe Synchronisierungsschaltfläche —
  Routinen, Räume, Karten, Kartenbild, Protokoll, Zeitpläne — gehen nicht mehr beide durch: Der zweite
  wird mit der üblichen Meldung für zu nahe beieinanderliegende Anfragen abgelehnt. <!-- UC42 -->
- Dokumentation: Die bekannten Einschränkungen werden ergänzt (unlesbare Karte bei ausschließlich
  lokaler Verbindung, Räume nur bei online befindlichem Roboter lesbar, Kartenansicht im Ruhezustand
  nicht aktualisiert, keine Kartenansicht auf Mobilgeräten, wieder eingeblendete Kachelbefehle nie
  erneut ausgeblendet, nach einer alten Aktualisierung reaktivierte Historisierung des Fehlers), die
  Fehlerbehebung deckt den teilweisen Fehlschlag einer Routinen-Synchronisierung ab, und die
  Funktionsübersicht nennt das Panel „Routinen“ und die Verfolgung eines auf dem Mobilgerät
  vorgenommenen Etagenwechsels. <!-- UC99 -->
- Dokumentation: Die Hilfeseite und der Changelog sind nun auch auf Englisch, Deutsch und Spanisch
  verfügbar. <!-- UC99 -->

# 22.09.2026

- Weiterentwicklung: Auf der Konfigurationsseite des Plugins wird der Anmeldecode nun direkt unter der
  E-Mail-Adresse eingegeben, vor dem Kontostatus, in der Reihenfolge, in der der Vorgang abläuft.
  <!-- UC04 -->
- Weiterentwicklung: Ein Hinweis weist darauf hin, dass die Konfiguration nach Eingabe der E-Mail
  gespeichert werden muss, bevor ein Code angefordert wird. <!-- UC04 -->
- Dokumentation: Vollständige Hilfeseite des Plugins — Installation, Verknüpfung des Roborock-Kontos
  per E-Mail-Code, Geräte und Befehle, Routinen, Dashboard-Kachel, Karte und Räume, Feinsteuerung,
  Echtzeit, erneute Authentifizierung, Roborock-Kontingente und Fehlerbehebungsleitfaden. <!-- UC49 -->
- Neu: Die letzte Reinigung (Beginn, Dauer, Fläche, Endgrund und eventueller Fehler) wird nun am Gerät
  gemeldet, mit einem über die Roboterseite einsehbaren Verlauf der 10 letzten Reinigungen und einer
  Schaltfläche zu dessen Aktualisierung. <!-- UC26 -->
- Dokumentation: Die Dokumentation des Plugins beschreibt das Reinigungsprotokoll: die gemeldeten
  Informationen, das Verlaufspanel und die Regel der Aktualisierungsschaltfläche. <!-- UC26 -->
- Neu: vier kumulierte Statistiken pro Roboter (Gesamtdauer der Reinigung, gesamte gereinigte Fläche,
  Anzahl der Reinigungen, Anzahl der Behälterentleerungen), standardmäßig historisiert, um deren
  Entwicklung über die Zeit zu verfolgen. <!-- UC27 -->
- Dokumentation: Die Dokumentation des Plugins beschreibt die kumulierten Statistiken: die vier Zähler,
  ihre standardmäßige Historisierung und das Verhalten nach einem Zurücksetzen über die Roborock-App.
  <!-- UC27 -->
- Neu: Die in der Roborock-App definierten Reinigungszeitpläne sind von Jeedom aus schreibgeschützt
  einsehbar: Wiederholung und aktiver oder inaktiver Status jedes einzelnen. <!-- UC28 -->
- Dokumentation: Der Fehlerbehebungsleitfaden der Hilfeseite deckt nun alle Meldungen ab, die eine
  Aktion Ihrerseits erfordern: nicht verknüpftes Konto, abgelehnte E-Mail-Adresse, überschrittene
  Frist, beschäftigter Roboter, am Roboter nicht verfügbare Einstellung und zu naher Kartenwechsel.
  <!-- UC49 -->

# 21.09.2026

**Dokumentation**

- Die Dokumentation und der Changelog werden veröffentlicht unter
  [jeedomdocs.decastro.fr/jeeroborock](https://jeedomdocs.decastro.fr/jeeroborock/).
- Einheitlicher Changelog für alle Versionen: Der „Beta“-Changelog entfällt.

**Karte und Räume**

- Bestandsaufnahme der **benannten Räume** des Kontos, mit Zuordnung zu den Segmenten des Roboters,
  in einem Panel „Räume“ des Reiters Gerät.
- **Mehrere Karten (Etagen)**: Liste der gespeicherten Karten, aktive Karte und Kartenwechsel. Ein
  Kartenwechsel macht die Raumliste und das Bild ungültig, die anschließend neu synchronisiert werden.
- **Kartenbild**, automatisch vom Daemon abgerufen und aktualisiert.
- Neues Panel **„Karte“** (Menü Startseite), erste Oberfläche des Plugins, die für
  Nicht-Administratoren zugänglich ist: Kartenbild, Zeitstempel, Legende der Räume und Aktualisierung
  alle 30 Sekunden. Das Bild wird nicht mehr über eine direkte URL bereitgestellt: Jeder Zugriff prüft
  die Rechte des Benutzers am Gerät.

**Feinsteuerung**

- **Saugleistung**: Anzeige und Einstellbefehl, begrenzt auf die vom Roboter tatsächlich unterstützten
  Stufen.
- **Wasserdurchfluss** des Wischmopps: Anzeige und Einstellbefehl.
- **Wischroute** und **Reinigungsmodus** (nur Saugen, nur Wischen, Saugen und Wischen): Anzeigen und
  Einstellbefehle.
- **Wartung an der Station**: „Wischmopp waschen“, „Wischmopp trocknen“, „Trocknen stoppen“,
  „Behälter leeren“. Diese Aktionen werden nur erstellt, wenn die Station dies zulässt, und werden mit
  einer klaren Meldung abgelehnt, wenn der Roboter nicht an seiner Basis ist.
- **Reinigung nach Raum**: ein Befehl pro Raum der Wohnung, plus ein allgemeiner Befehl „Räume
  reinigen (Namen durch Kommas getrennt)“. Die Befehle folgen der Umbenennung der Räume in der mobilen
  App.
- **Reinigung einer Zone** (x1,y1,x2,y2 in mm) und **Fahrt zu einem Punkt** (x,y in mm), mit
  Validierung der Koordinaten vor dem Senden an den Roboter.

**Visuelle Identität**

- Plugin-Symbol, abgeleitet vom Roborock-Logo.

# 20.09.2026

- **Detaillierte Fehler**: Fehlerbezeichnung auf Französisch, zugehöriger Code, Wert „Aucune“ (Keine),
  wenn der Roboter nichts meldet, und Historisierung des Fehlers. Ein der Bibliothek unbekannter Fehler
  wird nicht mehr als „kein Fehler“ dargestellt.
- **Dashboard-Kachel** des Roboters (Desktop und Mobil): Foto, Status, Batterieanzeige und die fünf
  Steuerungsaktionen, ohne jeglichen Cloud-Aufruf bei der Anzeige. Die von der Kachel übernommenen
  Befehle sind ausgeblendet, bleiben aber über Szenarien, Ansichten und Designs ausführbar.
- **Foto des Roboters** als Illustration des Geräts (Geräteliste und Konfigurationsseite).
- Korrekturen bei der Meldung von Ereignissen.

# 19.09.2026

- **Echtzeit**: Der Daemon trägt den Aktualisierungstakt (30 s während der Reinigung, 60 s im
  Ruhezustand) und empfängt die vom Roboter gepushten Aktualisierungen. Der Jeedom-Cron wird zu einem
  Aktualitäts-Wachhund und schaltet den Roboter nach mehr als 3 Minuten ohne Daten auf „getrennt“.
- **Robustheit und erneute Authentifizierung**: expliziter und dauerhafter Status „Erneute
  Authentifizierung erforderlich“, progressive Wartezeiten bei den Sonden und beim Neustart des
  Daemons, sowie Härtung der Protokollierung (kein Geheimnis in den Logs, unabhängig von der Stufe).
- **Verbrauchsmaterial**: verbleibender Verschleiß in % für die fünf tatsächlich vom Roboter gemeldeten
  Verbrauchsmaterialien, und ein Zurücksetzungsbefehl pro Verbrauchsmaterial.
- **Status der Dockingstation**: Staubentleerung, Wischmopp-Wäsche, Wischmopp-Trocknung,
  Stationsfehler mit zugehörigem Code, Wassermangel. Diese Informationen werden nur erstellt, wenn die
  Station sie bereitstellt.
- Korrekturen am Daemon: Start, Senden des Codes per E-Mail, Hinzufügen eines Geräts.

# 18.09.2026

- **Brücke von PHP zum Daemon**: einzelner lokaler Kanal, mit Übersetzung der Fehlercodes des Daemons
  ins Französische.
- **Authentifizierung** bei der Roborock-Cloud über einen per E-Mail erhaltenen Einmalcode.
- Schaltfläche **„Verbindung testen“** und Anzeige des Kontostatus auf der Konfigurationsseite des
  Plugins.
- **Erkennung der Roboter** des Kontos und Erstellung eines Geräts pro Roboter.
- **Informationsbefehle**: Status, Batterie, Reinigt, Fehler, gereinigte Fläche, Reinigungsdauer,
  Fortschritt, Online, Verbunden, letzte Aktualisierung.
- **Aktionsbefehle**: Starten, Pausieren, Stoppen, Zurück zur Basis, Orten, Aktualisieren.
- **Routinen („Routinen“)**: Synchronisierung der in der mobilen App definierten Routinen und ein
  Aktionsbefehl pro Routine. Sie laufen über die Roborock-Cloud und funktionieren daher auch, wenn der
  Roboter nicht direkt erreichbar ist.

# 17.09.2026

- Erste Version: Konfigurationsseite des Plugins (E-Mail des Roborock-Kontos, Port des lokalen Kanals
  des Daemons), Installation der Abhängigkeit `python-roborock` und Lebenszyklus des Daemons.
