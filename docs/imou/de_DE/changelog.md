# Änderungsprotokoll IMOU-Plugin

>**WICHTIG**
>
>Wenn es keine Information zur Aktualisierung gibt, betrifft diese ausschließlich Aktualisierungen der Dokumentation, der Übersetzung oder des Textes.

# 1.0

Erste vollständige Version, nach Funktionsbereich:

- **Sockel**: Konfiguration (appId/appSecret/datacenter verschlüsselt), Verbindungstest, Kameraerkennung und
  -synchronisierung (Anpassungen erhalten, selektive Synchronisierung pro Befehl).
- **Steuerung**: Ein-/Ausschalten, Überwachung (Bewegungserkennung), Scheinwerfer/Licht, Sirene (über das
  IoT-Modell „Things"), PTZ (Richtungsfeld + Zoom), Nachtsicht, Bildeinstellungen
  (Spiegelung, WDR, OSD, LED).
- **Video & Bilder**: Live-Stream (Live-Frames), Vollbildanzeige, Seite „Kamera-Panel",
  Kamera-Vorschaubild (Quelle nach Wahl).
- **Alarme & Erkennung**: letztes Ereignis (Bewegung/Mensch), Erkennungsempfindlichkeit, Schärfungspläne
  (Voreinstellungen), Personen-/KI-Erkennung.
- **Geräteverwaltung**: Anzeige des Modellcodes (nur technischer Code), Neustart, Batterieüberwachung
  & Aufwecken schlafender Geräte.
- **Zugangskontrolle**: Video-Türklingel, Türöffnung (kompatible Hardware).
- **Speicher**: SD-Karten-Status (Vorhandensein, Belegung, Kapazität) + Formatierung; Cloud-Abonnementstatus
  (nur lesbar, standardmäßig deaktiviert — aktivieren, wenn Sie ein IMOU-Cloud-Abonnement haben).
- **Supervision & Robustheit**: Online-Status / Gesundheit, Fehlerbehandlung und Wiederholungsversuche,
  Aufrufstatistiken und Kontingent mit Warnung, automatische Regulierung der Aktualisierungsfrequenz,
  Schätzung des Datenverbrauchs des Live-Streams.

# 0.1

- Erste Version (in Entwicklung).
