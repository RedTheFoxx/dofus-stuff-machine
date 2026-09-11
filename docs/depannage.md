# Dépannage

Cette page se lit **par le message**, et non par le symptôme : cherchez ci-dessous la chaîne que vous avez sous les yeux, et vous y trouverez la surface qui l'affiche et le geste attendu. Aucun message cité ici n'a été deviné : chacun est relevé sur la fonction du produit qui l'écrit ou sur le rendu réel d'un écran, et cette provenance est contrôlée automatiquement.

L'outil a deux surfaces, et elles n'écrivent pas toujours la même chaîne : la ligne de commande de `fetcher.py` et l'interface web. Quand les deux écritures diffèrent, cette page ne lisse pas l'écart, elle cite chacune d'elles. La surface des commandes est décrite par [la page CLI](cli.md), et l'ouverture des écrans, leur clavier et leurs touches par [la page d'installation](installation.md).

Une famille de symptômes n'affiche, elle, **aucun** message : quand une frappe semble rester sans effet, il n'y a pas de chaîne à chercher ici. C'est un mécanisme, et il a sa propre rubrique, adossée au code qui le porte.

## Base absente ou vide

Une base absente n'est pas une erreur : le premier contact **crée** le fichier, et l'outil travaille alors sur une base vide, c'est-à-dire sans aucune fiche d'objet. Les quatre premiers messages ci-dessous signalent exactement cet état — une base qui existe mais qui ne porte rien. Le fichier lui-même, ses catégories et sa fenêtre de re-contrôle sont décrits en détail par [la page de la base locale](base-locale.md), et la marche à suivre est déjà écrite dans la rubrique « base absente » de [la page d'installation](installation.md) puis dans [la page CLI](cli.md) : cette page renvoie vers elles, elle ne les réécrit pas.

| Message affiché | Où il apparaît | Ce qu'il faut faire |
|-----------------|----------------|---------------------|
| `Version jeu : (aucune)` | ligne de commande, état de la base, sur une base vide | aucun enregistrement de version de jeu : c'est l'état normal d'un premier contact, pas une panne ; remplissez la base par une synchronisation |
| `Dernier check : (aucun)` | ligne de commande, état de la base, sur une base vide | aucun contrôle de version n'a encore été enregistré ; il le sera à la première synchronisation |
| `Entrées : 0` | ligne de commande, état de la base, sur une base vide | la base ne porte aucune fiche ; sur une base vide, la ligne `Par catégorie :` n'est pas écrite du tout — son absence n'est donc pas un manque |
| `Erreur : aucune version en base` | ligne de commande, commande de version, sur une base vide | la commande s'arrête et sort en erreur : il n'y a rien à lire ; remplissez d'abord la base |
| `Base locale vide et --offline : impossible de synchroniser` | ligne de commande, synchronisation en mode hors-ligne ; la ligne réellement imprimée est ce message précédé de `Erreur : ` | le mode hors-ligne interdit d'aller chercher les données : relancez la synchronisation sans l'option hors-ligne |
| `AUCUNE VERSION EN BASE` | interface web, ligne de statut de l'écran de version, sur un catalogue vide | l'écran s'ouvre sans erreur sur une base vide ; il indique seulement qu'aucune version n'est enregistrée |
| `ERREUR : AUCUNE VERSION EN BASE.` | interface web, corps du même écran de version | même état, dit dans le corps de l'écran ; rien à corriger, la base est simplement vide |
| `VERSION JEU : (aucune)` | interface web, corps de l'écran d'état de la base, sur une base vide | cette surface écrit les mêmes champs que la ligne de commande, mais en majuscules et sans accents — ce n'est pas une autre panne |
| `DERNIER CHECK : (AUCUN)` | interface web, corps de l'écran d'état de la base, sur une base vide | même remarque : la forme diffère, l'état est le même |
| `ENTREES : 0` | interface web, corps de l'écran d'état de la base, sur une base vide | aucune fiche enregistrée ; la ligne `PAR CATEGORIE :` est elle aussi absente sur une base vide |

## Saisie invalide

Ces refus tombent tous **avant** tout travail : aucune recherche, aucun calcul, aucune écriture. Ils sont rendus par la ligne de statut de l'écran — c'est là que le produit écrit ses refus — et la ligne de commande les écrit différemment, quand elle les écrit. Les identifiants et les noms que vous saisissez sont des valeurs d'exécution : cette page ne les recopie jamais.

| Message affiché | Où il apparaît | Ce qu'il faut faire |
|-----------------|----------------|---------------------|
| `SAISIE REQUISE` | interface web, ligne de statut de la recherche, quand la recherche est vide | saisissez votre texte avant de valider |
| `LIMITE INVALIDE` | interface web, ligne de statut de la recherche, quand la limite lue après la barre verticale n'est pas un nombre | corrigez la limite ; la syntaxe de la recherche est décrite par [la page du parcours simplifié](parcours-simplifie.md) |
| `AUCUN RESULTAT.` | interface web, ligne de statut **et** corps de l'écran de résultats, quand rien ne correspond | ce n'est pas une panne : reformulez la recherche, ou remplissez la base |
| `ID INVALIDE — ENTIER ATTENDU` | interface web, ligne de statut, quand l'identifiant saisi n'est pas un nombre entier | saisissez un identifiant numérique, ou revenez à la liste |
| `ÉQUIPEMENT INTROUVABLE` | interface web, ligne de statut, quand l'identifiant ne correspond à aucun objet ; le message du catalogue est rendu en majuscules et suivi de l'identifiant | cet identifiant n'existe pas dans la copie locale : vérifiez-le dans la liste, ou regardez si la base contient bien cet objet |
| `OPTION INVALIDE — SAISIR 1 A 5` | interface web, ligne de statut du menu principal | le menu principal attend un choix parmi ses cinq entrées |
| `OPTION INVALIDE — SAISIR 1 A 4` | interface web, ligne de statut de l'écran système | l'écran système a quatre entrées, pas cinq : chaque écran de menu a sa propre borne |
| `OPTION INVALIDE — SAISIR 1 A 3` | interface web, ligne de statut de l'écran de gestion de la base | cet écran n'en a que trois — encore une autre borne, mesure faite sur le rendu de chaque écran |
| `Saisissez le nom ou le numéro de votre classe.` | interface web, ligne de statut de l'étape de la classe du parcours simplifié | le refus appartient au **flux** : corrigez la saisie de cette étape ; [la page du parcours simplifié](parcours-simplifie.md) porte déjà la table des saisies et de leurs refus |
| `Exemple : feu, terre air, ou multi.` | interface web, ligne de statut de l'étape des éléments | même famille : les éléments attendus sont décrits par [la page du parcours simplifié](parcours-simplifie.md) |
| `Saisissez un niveau entre 1 et 200.` | interface web, ligne de statut de l'étape du niveau — l'étape précédente doit être renseignée, sinon l'écran vous y renvoie d'abord | la borne est celle du produit ; l'étape précédente se remplit avant celle-ci, et le calcul ne part pas tant que le niveau est hors bornes |
| `SAISIE INVALIDE` | interface web, ligne de statut du wizard avancé, à l'étape des emplacements et des filtres | la saisie attendue à cette étape est décrite par [la page du wizard avancé](wizard-avance.md) |
| `Saisie invalide — voir aide syntaxe` | ligne de commande, saisie du profil d'optimisation, quand aucun élément exploitable n'a été reconnu | corrigez la ligne saisie ; la syntaxe attendue est décrite par [la page CLI](cli.md) |

L'erreur d'arguments de l'analyseur, elle, n'est écrite par aucune des deux surfaces : elle vient de l'analyseur de la ligne de commande. [La page d'installation](installation.md) et [la page CLI](cli.md) la décrivent déjà, cette page n'en invente donc pas la forme.

## Calcul long

Le produit **n'annonce aucune durée** : ce qu'il expose, c'est un état — le calcul a commencé — et un **budget**, réglable. Aucun message de cette famille ne promet une durée d'attente, et cette page n'en promet pas davantage.

| Message affiché | Où il apparaît | Ce qu'il faut faire |
|-----------------|----------------|---------------------|
| `Calcul en cours (CP-SAT)…` | ligne de commande, juste avant le lancement du calcul | c'est le seul message d'attente du produit : laissez la commande aller au bout, elle écrit son résultat ensuite |
| `ENTREE=CALCULER` | interface web, ligne de statut de l'étape du niveau du parcours simplifié | l'interface n'écrit pas de message d'attente : elle indique par sa ligne de statut que la touche Entrée lance la recherche |
| `DUREE` | interface web, récapitulatif du wizard avancé, où le budget apparaît sous la forme d'une durée en secondes | ajustez le budget à cette étape du wizard, décrite par [la page du wizard avancé](wizard-avance.md) |
| `CALCUL TERMINE` | interface web, après le calcul | le calcul est synchrone dans l'interface : ce message n'apparaît qu'à la fin, quand le résultat est prêt |

Le budget de la ligne de commande se règle par l'option `--time-limit` ; son aide, lue sur le parseur réel, le décrit comme le temps alloué au solveur. Le même réglage existe dans le récapitulatif du wizard avancé, sous les champs de durée que [la page du wizard avancé](wizard-avance.md) détaille. Autrement dit : si un calcul vous paraît long, ce n'est pas une panne à diagnostiquer, c'est un budget à ajuster.

## Clavier inactif

Cette famille **n'affiche aucun message** : il n'y a rien à chercher dans le code, et cette page n'en invente pas. Ce que le produit porte, c'est un mécanisme, observable dans le code et dans le rendu des écrans :

- le champ de saisie est marqué `autofocus` dans le gabarit d'écran, et il n'existe que sur les écrans qui attendent une saisie ;
- au chargement de la page, le script refocalise ce champ, et un clic ailleurs dans la page est intercepté (`preventDefault`) puis suivi d'une nouvelle refocalisation (`activeElement`) : le curseur revient dans le champ ;
- la touche Entrée ne soumet le formulaire que si ce champ est bien l'élément actif ; sinon elle n'a aucun effet de saisie ;
- les écrans **sans champ de saisie** — l'état de la base, la version locale, la fin de session — laissent donc le clavier sans effet autre que leurs raccourcis.

Si une frappe ne fait rien, le premier geste est donc de vérifier que l'écran attend bien une saisie : lisez la ligne qui porte le champ entre crochets, et les touches de la barre du bas. Le pilotage clavier — le champ, sa refocalisation au clic, la barre de touches construite à l'affichage — est décrit par [la page d'installation](installation.md), qui est le seul endroit qui le détaille : cette rubrique y renvoie et ne le redéfinit pas.

## Résultat paginé

La pagination a **deux formes**, et le produit ne les écrit pas au même endroit. La ligne de **statut** ne porte le motif de page que lorsque l'écran est réellement paginé — un écran qui n'a qu'une seule page n'ajoute aucun motif à son statut ; le **corps** de l'écran, lui, porte toujours sa ligne de pagination. Un diagnostic qui exigerait le motif dans le statut d'un écran à page unique serait donc faux sur un produit correct.

| Message affiché | Où il apparaît | Ce qu'il faut faire |
|-----------------|----------------|---------------------|
| `PAGE {page}/{total}` | interface web, ligne de statut d'un écran paginé, sous la forme du numéro de page sur le nombre de pages | le motif n'apparaît que si l'écran compte plus d'une page ; utilisez les deux touches de navigation pour changer de page |
| `ENTREE=VALIDER` | interface web, ligne de statut de l'écran de liste | l'écran attend une saisie : identifiant pour ouvrir une fiche, ou les touches de page |
| `Page prec` | interface web, barre des touches, sur un écran paginé | touche de navigation vers la page précédente |
| `Page suiv` | interface web, barre des touches, sur un écran paginé | touche de navigation vers la page suivante |
| `Page suivante disponible :` | ligne de commande, après la liste, quand des objets restent à parcourir | la suite est annoncée avec son lien ; relancez la commande sur la page suivante |

Le mécanisme de pagination de l'interface — la ligne de corps, les touches de page, la barre — est déjà décrit par [la page du parcours simplifié](parcours-simplifie.md) ; cette rubrique ne fait qu'indexer les messages par lesquels le paginage se reconnaît.

## Source de vérité

- `dofus_stuff/cli.py` : les libellés de l'état de la base, le message d'attente du calcul et les messages d'arrêt de la ligne de commande.
- `dofus_stuff/sync.py` : le refus de la synchronisation hors-ligne sur une base vide.
- `dofus_stuff/web/routes.py` : les lignes de statut, les refus des écrans, la composition de la pagination et le message de fin de calcul.
- `dofus_stuff/web/optimize_wizard.py` : les refus du wizard avancé et le champ de budget du récapitulatif.
- `dofus_stuff/optimize/profile_input.py` : les refus de saisie du profil d'optimisation.
- `dofus_stuff/web/templates/screen.html` : le champ de saisie et son marquage de focus à l'affichage.
- `dofus_stuff/web/static/js/terminal.js` : la refocalisation du champ, le clic intercepté et la touche Entrée.

[Retour au sommaire](sommaire.md)
