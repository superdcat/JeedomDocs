# Changelog SmartClim

> **IMPORTANT**
>
> S'il n'y a pas d'information sur une mise à jour, c'est que celle-ci concerne uniquement de la mise à
> jour de documentation, de traduction ou de texte.

# En cours de développement

**Le développement du plugin est terminé.** Toutes les fonctionnalités de la feuille de route initiale
sont écrites : pilotage des climatiseurs par les trois transports (AUX Home, Broadlink LAN et AUX Cloud /
AC Freedom), choix automatique ou manuel du transport avec repli en cas d'échec, fonctions de confort,
oscillations, sécurité enfant, widget de tableau de bord, page-panneau, scan unifié des trois sources,
relais temps réel du cloud historique, et documentation utilisateur.

> ⚠️ **Développé ne veut pas dire validé.** Une partie de ces fonctions n'a pas encore pu être essayée sur
> un climatiseur réel. SmartClim reconstitue des protocoles que le fabricant n'a jamais publiés : seule
> une mesure sur du matériel permet de confirmer qu'une fonction répond réellement comme prévu.

État de la validation à ce jour :

- **AUX Home** — le service en ligne le plus récent du fabricant, celui qu'utilise l'application mobile du
  même nom — est **validé sur un climatiseur réel** : découverte, lecture de l'état, marche/arrêt, mode,
  température de consigne et vitesse de ventilation.
- **Broadlink LAN** — le dialogue direct avec le climatiseur sur votre réseau domestique, sans Internet —
  et **AUX Cloud (AC Freedom)** — le service en ligne plus ancien, utilisé notamment hors d'Europe et par
  les appareils de génération précédente — ont été construits et vérifiés contre des implémentations open
  source de référence, mais **n'ont pas encore été essayés sur un climatiseur réel**.
- Les **fonctions de confort** (afficheur, mode veille, ioniseur/santé, nettoyage automatique,
  anti-moisissure), les **oscillations** et la **sécurité enfant** sont développées, mais restent
  **volontairement inactives** tant qu'une mesure sur matériel n'a pas confirmé la lecture de leur état :
  aucune de ces commandes n'apparaît aujourd'hui sur vos équipements. Le plugin préfère ne rien afficher
  plutôt qu'afficher une valeur dont il n'est pas sûr.
- Le **relais temps réel** du cloud historique n'a pas été essayé sur un compte réel. Il n'est jamais
  nécessaire au pilotage : le plugin fonctionne pleinement sans lui.

Vos retours d'expérience — succès comme échecs — sont ce qui fait avancer cette liste. Le chapitre
« Limites connues » de la documentation détaille chacun de ces points, et le chapitre « Signaler un
problème » explique quelles informations joindre.
