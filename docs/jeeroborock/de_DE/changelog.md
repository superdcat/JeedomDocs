# Changelog JeeRoborock

>**WICHTIG**
>
>Wenn zu einer Aktualisierung keine Information angegeben ist, betrifft diese ausschließlich eine
>Aktualisierung der Dokumentation, der Übersetzung oder von Texten.

# 13.10.2026

- Neu: Modus „Nicht stören“ aus Jeedom steuerbar, wenn der Roboter ihn unterstützt: aktiviert oder nicht, Beginn und Ende des Zeitfensters sowie drei Aktionen „Aktivieren“, „Deaktivieren“ und „Zeitfenster festlegen“ (Beginn und Ende im Format HH:MM, in Szenarien nutzbar); angezeigt wird, was der Roboter tatsächlich gespeichert hat <!-- UC54 -->
- Dokumentation: der Abschnitt „Geräteeinstellungen“ beschreibt den Modus „Nicht stören“ (französische Dokumentation) <!-- UC54 -->
- Neu: Laden zu Nebentarifzeiten aus Jeedom steuerbar, wenn der Roboter es unterstützt: aktiviert oder nicht, Beginn und Ende des Zeitfensters sowie drei Aktionen „Aktivieren“, „Deaktivieren“ und „Zeitfenster festlegen“ (HH:MM, in Szenarien nutzbar); der Roboter verschiebt nur sein Laden, eine angeforderte Reinigung wird nicht blockiert <!-- UC55 -->
- Dokumentation: der Abschnitt „Geräteeinstellungen“ beschreibt das Laden zu Nebentarifzeiten (französische Dokumentation) <!-- UC55 -->
- Neu: Lautstärke der Sprachansagen des Roboters in Prozent angezeigt und aus Jeedom von 0 bis 100 einstellbar, wenn der Roboter es unterstützt: Information „Lautstärke“ und Schieberegler „Lautstärke einstellen“, in Szenarien nutzbar; der angezeigte Wert ist der vom Roboter zurückgelesene <!-- UC56 -->
- Dokumentation: der Abschnitt „Geräteeinstellungen“ beschreibt die Lautstärke (französische Dokumentation) <!-- UC56 -->
- Neu: Modi der Basisstation aus Jeedom anzeigbar und einstellbar, wenn die Station sie anbietet: Informationen „Entleerungsmodus“ und „Mopp-Waschmodus“, Listen „Entleerungsmodus einstellen“ und „Waschmodus einstellen“, in Szenarien nutzbar; der angezeigte Modus ist der vom Roboter zurückgelesene <!-- UC57 -->
- Dokumentation: der Abschnitt „Geräteeinstellungen“ beschreibt die Entleerungs- und Waschmodi der Basisstation (französische Dokumentation) <!-- UC57 -->
- Neu: die Reinigung von Räumen per Namen und die Zonenreinigung akzeptieren eine Anzahl von Durchgängen (1, 2 oder 3) in ihrem Feld „Titel“, um einen Raum oder eine Zone zwei- oder dreimal zu reinigen; ohne Wert ein einziger Durchgang wie bisher, und die Wiederholungseinstellung der Roborock-App wird nie geändert <!-- UC58 -->
- Dokumentation: das Kapitel „Feinsteuerung“ erklärt die Anzahl der Durchgänge bei Raum- und Zonenreinigung, die Fehlerbehebung deren zwei Ablehnungsmeldungen (französische Dokumentation) <!-- UC58 -->
- Neu: neue Information „Aktueller Raum“: der Name des Raums, in dem sich der Roboter befindet, abgeleitet aus seiner Position auf der Karte, ohne zusätzlichen Aufruf beim Roboter oder in der Cloud; sie lautet „Aucune pièce“ (kein Raum) außerhalb jedes Raums und „Pièce inconnue“ (unbekannter Raum), wenn Position oder Karte nicht bekannt sind, und ein Szenario löst nur bei einem echten Raumwechsel aus <!-- UC60 -->
- Korrektur: das Kartenbild bleibt nicht mehr auf der alten Position stehen, wenn der Roboter kurz nach dem letzten Lesen zu seiner Basis zurückkehrt: es wird innerhalb der folgenden Minute neu gelesen <!-- UC60 -->
- Dokumentation: der Abschnitt „Karte und Räume“ beschreibt die Information „Aktueller Raum“, ihre Werte und ihre Verzögerung, und die Fehlerbehebung behandelt den Fall, dass sie auf „Pièce inconnue“ bleibt (französische Dokumentation) <!-- UC60 -->
- Dokumentation: neuer Abschnitt „Befehle je nach Modell“ (warum ein Befehl fehlt und wie er erscheint), Eingabeformate für Zeitbereiche und Anzahl der Durchgänge, Szenario-Beispiele für Verbrauchsteile und Behälter der Station, Kindersicherung, Nicht stören, Nebenzeiten, Lautstärke, Stationsmodi, Anzahl der Durchgänge und aktuellen Raum; bekannte Einschränkungen und Fehlerbehebung ergänzt (vorerst nur auf der französischen Seite). <!-- UC119 -->
- Neu: die Seite „Karte“ zeigt neben der Karte ein Steuerfeld: Roboterauswahl (im Browser gespeichert), Reiter Gesamt, Raum und Zone (auf der Karte gezeichnetes Rechteck), Einstellungen für Saugleistung, Wasserdurchfluss und Route nur mit den Werten des Roboters, eine große Starttaste und danach Pause, Fortsetzen, Stopp und Rückkehr zur Basis, ohne die Seite zu verlassen; ein Benutzer ohne Ausführungsrecht sieht alles ausgegraut, und es wird keine zusätzliche Anfrage an die Cloud gesendet <!-- UC61 -->
- Dokumentation: der Abschnitt zum Bereich „Karte“ beschreibt das Steuerfeld: Reiter, Einstellungen, Schaltflächen, Roboter offline, Rechte und Speicherung des gewählten Roboters (französische Dokumentation) <!-- UC61 -->
- Neu: auf der Seite „Karte“ werden die Raumnamen auf der Karte angezeigt, und ein Tippen oder Klicken auf einen Raum hakt ihn im Reiter Raum an; in der Roborock-App festgelegte Sperrzonen und virtuelle Wände werden schreibgeschützt eingezeichnet; das Rechteck im Reiter Zone lässt sich vor dem Start verschieben, an einer Ecke in der Größe ändern und löschen und bleibt beim Aktualisieren der Karte erhalten <!-- UC62 -->
- Dokumentation: der Abschnitt zum Bereich „Karte“ beschreibt die interaktive Karte: Raumnamen und Raumauswahl auf der Karte, nicht wählbare oder unbekannte Räume, verschieb- und skalierbare Zone, schreibgeschützte Sperrzonen (französische Dokumentation) <!-- UC62 -->
- Neu: die Seite „Karte“ erhält einen Reiter „Station und Wartung“: Behälter leeren, Mopp waschen und trocknen, Entleerungs- und Waschmodus einstellen, Status der Station, der Wassertanks und den Verschleiß der Verbrauchsteile verfolgen, mit einem Hinweis, wenn ein Teil zu ersetzen ist oder die Station eine Störung meldet; nur die Funktionen Ihres Roboters werden angezeigt, und ein bereits laufender Vorgang kann nicht erneut gestartet werden <!-- UC63 -->
- Dokumentation: der Abschnitt zum Bereich „Karte“ beschreibt den Reiter „Station und Wartung“: Blöcke, Roboter ohne Station, laufender Vorgang, Roboter offline und Rechte (französische Dokumentation) <!-- UC63 -->
- Neu: neue Aktion „Saugen, dann wischen“ im Bereich „Karte“ und in Szenarien: der Roboter saugt zuerst nur und wischt danach nur, in der ganzen Wohnung oder in den gewählten Räumen, wartet zwischen den beiden Durchgängen, bis er an der Station wieder bereit ist, zeigt den Stand der Sequenz an, kann jederzeit abgebrochen werden und erhält danach seine ursprünglichen Einstellungen zurück; der zweite Durchgang wird nie gestartet, wenn der erste angehalten wurde oder fehlerhaft endete <!-- UC64 -->
- Dokumentation: die Dokumentation beschreibt die Aktion „Saugen, dann wischen“: Bereich, Szenario-Befehle, Warten zwischen den Durchgängen, Abbruch, Endgründe und Grenzen (französische Dokumentation) <!-- UC64 -->
- Neu: die Seite „Karte“ erhält einen Reiter „Tagesverlauf“: eine stündliche Zeitleiste pro Roboter zeigt, was er getan hat (Reinigung, Rückkehr zur Station, Laden, Entleeren, Waschen, Trocknen, Fehler, offline), hebt abgeschlossene Reinigungen hervor und kennzeichnet Zeiträume ohne Daten als „Unbekannt“; die letzten 7 Tage bleiben abrufbar, ohne Kontingent zu verbrauchen <!-- UC65 -->
- Dokumentation: die Dokumentation beschreibt den Reiter „Tagesverlauf“: Legende, Zeiträume „Unbekannt“, hervorgehobene Reinigungen, Navigation, Aufbewahrung und Einschränkungen (französische Dokumentation) <!-- UC65 -->
- Neu: Panel in der Jeedom-Mobil-App: Roboter auswählen, Karte ansehen und eine Komplett- oder Raumreinigung vom Telefon aus starten, im hellen wie im dunklen Design; die Seite Station und Wartung sowie der Tagesverlauf bleiben dem Computer vorbehalten <!-- UC66 -->
- Dokumentation: neuer Abschnitt zum mobilen Panel (Zugang, Inhalt, fehlende Funktionen) <!-- UC66 -->
- Dokumentation: manuelle Steuerung: Schritt-für-Schritt-Anleitung zum Reinigen eines Raums über das Panel, Rechtetabelle (Administrator, Ausführen, nur Lesen, kein Zugriff), neue Zeilen in der Fehlerbehebung (Rechte, Roboter offline, Raum- und Zonenauswahl, Station, Tagesverlauf, mobiles Panel, Abbrechen von „Saugen, dann Wischen“), bekannte Einschränkungen ergänzt und neuer Abschnitt „Plugin-Aktualisierung“ (vorerst nur auf der französischen Seite) <!-- UC129 -->
- Neu: Begrüßungsnachricht im Nachrichtencenter von Jeedom, nur einmal pro Version, bei der Installation wie bei jeder Aktualisierung des Plugins: installierte Version, Links zur Dokumentation, zum Market und zum Forumsthema sowie Hinweis auf die Schaltfläche „Hilfe“ zum Melden eines Fehlers und auf den beizufügenden Diagnosebericht <!-- UC67 -->
- Neu: die Schaltfläche „Hilfe“ füllt das Community-Thema mit einem eingeklappten Block „JeeRoborock-Informationen“ vor: Status von Dienst und Konto, Modell und Firmware jedes Roboters (nummeriert, ohne Namen oder Kennung), Versionen, letzter Fehler und eventuelle Quotenablehnung, ohne persönliche Daten <!-- UC68 -->

# 12.10.2026

- Korrektur: Ein ausgeschalteter, entladener oder vom WLAN getrennter Roboter verhindert nicht mehr die Steuerung der anderen Roboter des Kontos: Er wird als offline angezeigt, seine Wiederverbindungsversuche verbrauchen kein Roborock-Kontingent mehr, und er ist innerhalb von 6 Minuten nach seiner Rückkehr von selbst wieder steuerbar. <!-- UC44 -->
- Dokumentation: neuer Abschnitt „Mehrere Roboter im selben Konto“ unter „Echtzeit und Aktualität“ (französische Dokumentation). <!-- UC44 -->
- Korrektur: das Ändern der Saugleistung, der Wassermenge, der Wischroute oder des Reinigungsmodus meldet nicht mehr fälschlich „nicht angewendet“, wenn der Roboter, zum Beispiel an seiner Station, die Einstellung erst einige Sekunden später übernimmt: Das Plugin wartet jetzt bis zu etwa zwölf Sekunden, bevor es entscheidet, ohne die Antwort zu verlangsamen, wenn die Einstellung sofort übernommen wird. <!-- UC45 -->
- Dokumentation: der Abschnitt „Feinsteuerung“ erklärt die Überprüfung der Einstellungen nach dem Senden, und der Fehlerbehebungseintrag „nicht angewendet“ wurde präzisiert (französische Dokumentation). <!-- UC45 -->
- Korrektur: ein Reinigungsauftrag (Starten, Raum- oder Zonenreinigung, über das Dashboard wie über ein Szenario), der gesendet wird, während die Station den Staubbehälter entleert, wird nicht mehr als übermittelt gemeldet, obwohl der Roboter ihn ignoriert: Er wird mit einer Meldung abgelehnt, die zum erneuten Versuch nach Ende der Entleerung auffordert <!-- UC46 -->
- Dokumentation: der Abschnitt „Status und grundlegende Steuerung“ und die Fehlerbehebungstabelle erklären, warum ein Reinigungsauftrag während der Behälterentleerung abgelehnt wird <!-- UC46 -->
- Korrektur: Die Befehle „Letzte Reinigung“ aktualisieren sich nach jeder Reinigung wieder von selbst, in der Regel innerhalb weniger Minuten: Hat der Roboter die Reinigung noch nicht gespeichert oder antwortet er nicht (Wischmopp-Wäsche, Entleerung), liest das Plugin sein Protokoll bis zu fünfmal innerhalb von 30 Minuten erneut, ohne Roborock-Kontingent zu verbrauchen. <!-- UC47 -->
- Dokumentation: Abschnitt „Reinigungsprotokoll“: Zeitpunkte der automatischen Aktualisierung der letzten Reinigung (französische Dokumentation). <!-- UC47 -->
- Korrektur: Kartennamen, die von manchen Robotern kodiert übermittelt werden (S7: „%20“ statt Leerzeichen, „%E9“ statt „é“), werden jetzt im Klartext angezeigt; bei einem bereits eingerichteten Roboter einmal auf „Kartenliste aktualisieren“ im Reiter Ausrüstung klicken. <!-- UC48 -->
- Weiterentwicklung: Die Plugin-Seite nennt jetzt die Lizenz GPL v3 oder neuer (offizieller Text beigefügt) und setzt mindestens Jeedom 4.4.7 voraus, die erste Version, die die Python-Abhängigkeiten des Plugins in einer eigenen Umgebung installiert; unter Jeedom 4.4 wird die Roboter-Kachel mit dem Plugin-Symbol angezeigt. <!-- UC50 -->
- Dokumentation: Mindestversion von Jeedom (4.4.7) und Lizenz (GPL v3 oder später), Offline-Roboter bei mehreren Robotern im Konto, Einstellungen mit kurzer Verzögerung bestätigt, Reinigungsbefehl während der Behälterentleerung abgelehnt, automatische Aktualisierung der letzten Reinigung, Kartennamen im Klartext; bekannte Einschränkungen und Fehlerbehebung ergänzt. <!-- UC109 -->
- Neu: Die Verbrauchsteile der Station erscheinen als verbleibender Verschleiß in Prozent (Stationsfilter, Reinigungsbürste, Staubbeutel, je nach Station); Filter und Bürste lassen sich nach Bestätigung zurücksetzen, der Staubbeutel ist nur lesbar <!-- UC51 -->
- Dokumentation: Der Abschnitt „Ladestation, Verbrauchsteile und Wartung“ beschreibt die Verbrauchsteile der Station (französische Dokumentation) <!-- UC51 -->
- Neu: drei Ja/Nein-Informationen für Szenarien, nur angelegt, wenn Roboter und Station sie unterstützen: „Frischwassertank leer“, „Schmutzwassertank voll oder fehlt“ und „Wischmopp eingesetzt“ <!-- UC52 -->
- Dokumentation: Der Abschnitt „Ladestation, Verbrauchsteile und Wartung“ beschreibt den Zustand der Wassertanks und des Wischmopps (französische Dokumentation) <!-- UC52 -->
- Neu: Kindersicherung aus Jeedom steuerbar, wenn der Roboter sie unterstützt: eine Ja/Nein-Information „Kindersicherung“ für Szenarien und zwei Aktionen „Kindersicherung aktivieren“ / „Kindersicherung deaktivieren“; angezeigt wird der vom Roboter zurückgelesene Zustand <!-- UC53 -->
- Dokumentation: der neue Abschnitt „Geräteeinstellungen“ beschreibt die Kindersicherung (französische Dokumentation) <!-- UC53 -->

# 01.10.2026

- Korrektur: Die Schaltfläche „Routinen synchronisieren“ im Reiter „Gerät“ bleibt nicht mehr wirkungslos: Ein Klick startet die Synchronisierung wieder, und das Gerät wird anschließend von selbst neu angezeigt, wenn Routinen hinzugefügt oder entfernt wurden. <!-- UC35 -->

# 29.09.2026

- Korrektur: Die Reinigung eines Raums (Schaltfläche „Reinigen“ eines Raums oder Befehl per Namen) endet nicht mehr mit „Interner Fehler des Dienstes“: Sie wird wieder an den Roboter übertragen. Wird ein angeforderter Raum nicht erkannt, empfiehlt das Plugin nun, die Räume neu zu synchronisieren. <!-- UC24 -->

# 24.09.2026

- Korrektur: Der Diagnosebericht enthält wieder den technischen Teil, den der Daemon liefert: Er zeigt nicht mehr „Daemon-Diagnose nicht verfügbar: unvollständiger Bericht“ an, wenn der Daemon läuft. Log-Level und Fehlerverlauf des Roboters werden ebenfalls korrekt angegeben. <!-- UC30 -->

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
- Korrektur: Roboter-Kachel: Der Hinweis auf ein zu ersetzendes Verbrauchsmaterial gibt nun an, welches (Hauptbürste, Filter, Sensoren…). <!-- UC15 -->

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
