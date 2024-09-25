**Sorties d'EddyPro, au format NETCDF, générés avec le script read_EddyPro_outputs.py** : 
+ Fichiers en `XXX_full_output.nc` : équivalent des fichiers full_output, avec en plus la hauteur de l'instrument (`instrument_height`), et $\langle u'w' \rangle$ (`wu_cov`).
  Ces deux derniers sont extraits des fichiers `metadata` et `fluxnet`. Pour des raisons pratiques, les noms de variables contenant le caractère `/` ont été changés. Ainsi, `w/ts_cov`
   devient `wts_cov`, `(z-d)/L` devient `zL`.
+ Fichiers en `XXX_spectres.nc` : fichiers contenant les spectres et cospectres sur toute la période de calcul.
  Ceux-ci se présentent sous forme de tableaux 2D : une dimension temporelle, et une dimension fréquencielle.
+ Fichiers en `XXX_ogives.nc` : idem, mais pour les ogives.
  
