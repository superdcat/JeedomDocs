# Badger Fork

## Description

Ce plugin permet de connecter des lecteurs de badges (RFID/NFC) utilisant le protocole Wiegand (8/26/34). Ce plug-in nécessite un composant tiers (Arduino ou ESP) comme interface entre le lecteur et le réseau local. Le lecteur prévient Jeedom à chaque badge ou code présenté ; Jeedom décide, journalise, et vos scénarios agissent.

Le plugin n'a **ni dépendance ni démon** : il est entièrement en PHP. Il s'installe **depuis le Market Jeedom** (Plugins > Gestion des plugins > Market, recherchez **Badger Fork**, puis activez-le).

## Par où commencer ?

| Vous êtes… | Allez à… |
|---|---|
| **Débutant** : vous n'avez jamais flashé une carte Arduino ni câblé un lecteur de badges | [Débuter pas à pas](debuter.md) : un tutoriel en 8 étapes, de l'achat du matériel à la première porte ouverte |
| **Utilisateur averti ou contributeur** : vous cherchez un détail (cartes, capacités, appairage, posture de sécurité des lecteurs, protocole, mode debug, compatibilité) | [Référence technique](reference.md) |
| **Soucieux de sécurité** : vous voulez savoir ce que protège le plugin, débloquer un lecteur, régler l'inclusion ou les codes | [**Sécurité de vos lecteurs**](securite.md) : ce que chaque mesure protège (et ne protège pas), réglages par défaut, mise à jour sans surprise |
| **En panne** | [Dépannage détaillé](depannage.md) |
| **Vous utilisez déjà l'ancien plugin Badger** | [Procédure de migration](migration.md) |

> **Vos lecteurs actuels continuent de fonctionner sans rien changer.** Ne désinstallez pas l'ancien plugin Badger avant d'avoir suivi la [procédure de migration](migration.md).

> ⚠️ **Un lecteur v0 (sketch d'origine) reste usurpable depuis le réseau local**, et son code circule en clair : seul un reflash avec le sketch v1 appairé et signé y remédie. Lisez [Sécurité de vos lecteurs](securite.md).

## Autres pages

- [Sécurité de vos lecteurs](securite.md) : ce que protège chaque mesure, réglages par défaut, mise à jour, débloquer un lecteur, inclusion, codes, filtrage par IP, dossiers (Apache, nginx).
- [Configuration du plugin](configuration.md) : matériel d'origine, équipements, lecteurs, badges et codes.
- [Fonctionnement et utilisation des équipements](fonctionement.md) : scénarios, blocage après échecs, codes temporaires.
- [Infos techniques](techtips.md) : technologie Wiegand, clavier à code, sources.
- [Cartes et sketch v1](cartes-et-sketch-v1.md) : cartes prises en charge, câblage, flash.
- [Protocole v1 des lecteurs](protocole-v1.md) : contrat complet du protocole.
- [Changelog](changelog.md) : l'historique des évolutions.

## Où sont passées les sections de l'ancienne page d'accueil ?

Elles sont toutes dans la [référence technique](reference.md) : [mode debug](reference.md#mode-debug), [version, firmware et capacités](reference.md#fiche-lecteur), [appairage](reference.md#appairage), [posture de sécurité des lecteurs](reference.md#posture-securite) et [configuration du sketch d'un lecteur v1](reference.md#configuration-sketch).
