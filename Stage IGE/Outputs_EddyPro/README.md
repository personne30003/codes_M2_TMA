**Sorties d'EddyPro, au format NETCDF, générés avec `read_EddyPro_outputs.py` :**
## Généralités
+ Fichiers en `XXX_full_output.nc` : équivalent des fichiers full_output, avec en plus la hauteur de l'instrument (`instrument_height`), et $\langle u'w' \rangle$ (`wu_cov`).
  Ces deux derniers sont extraits des fichiers `METADATA` et `fluxnet`. Pour des raisons pratiques, les noms de variables contenant le caractère `/` ont été changés. Ainsi, `w/ts_cov`
   devient `wts_cov`, `(z-d)/L` devient `zL`. Attention, je n'ai pas créé de fichier `METADATA` en sortie pour toutes les stations (c'est pas rigoureux de ma part, je sais), donc `instrument_height` n'est pas toujours présent.
+ Fichiers en `XXX_spectres.nc` : fichiers contenant les spectres et cospectres sur toute la période de calcul.
  Ceux-ci se présentent sous forme de tableaux 2D : une dimension temporelle, et une dimension fréquencielle. Pour gagner de la place en mémoire, toutes les colonnes vides (remplies de `NAN`) sont supprimées.
+ Fichiers en `XXX_ogives.nc` : idem, mais pour les ogives.
## Liste des fichiers
Sauf mention du contraire, tous les calculs ont été effectués sur la semaine du $1^{ier}$ au 9 Septembre 2023.
+ Calculs sur T2 :
   + `T2_TO5_i_2min`, $i=1,2,3$ (resp. $z=1,2,4.14m$): Flux et spectres calculés sur T2, au niveau $i$, **AVEC** corrections spectrales, calculés sur **2 minutes**
   + `T2_TO5_i_2min-new`, $i=1,2,3$ (resp. $z=1,2,4.14m$): Flux et spectres calculés sur T2, au niveau $i$, **SANS** corrections spectrales, calculés sur **2 minutes**
   + `T2_TO5_i_30min`, $i=1,2,3$ (resp. $z=1,2,4.14m$): Flux et spectres calculés sur T2, au niveau $i$, **AVEC** corrections spectrales, calculés sur **30 minutes**
   + `T2_TO5_i_30min-new`, $i=1,2,3$ (resp. $z=1,2,4.14m$): Flux et spectres calculés sur T2, au niveau $i$, **SANS** corrections spectrales, calculés sur **30 minutes**
+ Calculs sur T2 Right :
   + `T2_RE_bas_30min` : Flux et spectres calculés sur T2 Right, en $z=1m$, sur **30 minutes**. Flux d'humidité disponibles.
   + `T2_RE_bas_30min` : Idem mais sur 2min.
   + `T2_RE_bas_all_final_30min` : Idem que `T2_RE_bas_30min`, mais sur toute la période de mesures (du 18 aout au 9 septembre).
   + `T2_RE_haut_30min` : Flux et spectres calculés sur T2 Right, en $z=2m$, sur **30 minutes**.
   + `T2_RE_haut_30min` : Idem mais sur 2min.
