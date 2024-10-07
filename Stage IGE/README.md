# Fichiers de travail
Ce repertoire regroupe tous les fichiers utilisés pendant mon stage.

## Notebooks Python
- `Grachev_T2_TO5.ipynb`
- `SEB_net_T2R.ipynb`
- `Stabilite_T2_TO5-V2.ipynb`
- `Stabilite_T2_TO5-V3.ipynb`
- `Visualisation_snowfox_T2.ipynb`
- `Variabilite_flux.ipynb`
- `flux_T2_Left.ipynb`
- `flux_T2_Right.ipynb`
-  `flux_T2_TO5.ipynb`
-  `rose_des_vents_IGE.ipynb`
-  `comparaison_flux_brut_vs_EC.ipynb`
## Librairies (dont je suis l'auteur)
- `MRD_vX.py` : Implémentation de l'algorithme de MRD, et détection du gap spectral, cf *[Vickers and Mahrt 2003]*.
  Selon les versions, l'algorithme de détection du gap spectral est modifié. Les exemples associés sont dans `MRD_vX_test.py`/`MRD_vX_test.ipynb`. Le jeu de données utilisé est disponible [ici](http://servdap.legi.grenoble-inp.fr/opendap/hyrax/meige/22_TP_TMA/TP09_CLA_MONTAGNE/DATA_2023_3oct/sonicdata_2023_03_10.nc.dmr.html) (il s'agit d'un TP de M2).

  **A FAIRE : écrire une version définitive (et documentée) avec exemple. De nombreuses fonctions sont inutiles et doivent être supprimées. Rajouter les fonctions écrites dans `Stabilité_T2_TO5.ipynb` (tracé de spectres, utilisation de Xarray).** 

- `Bulk.py` : Calcul des flux de chaleurs turbulents à l'aide de la méthode du Bulk aérodynamique (cf thèse de Maxime Litt, p55), calcul des rugosités de surface à partir des flux obtenus par EddyCovariance (à l'aide des formules précedentes). Quelques fonctions statistiques aussi ($RMSE$, $R^2$, etc...).
  **A FAIRE : Documenter !!**

## Programmes utilitaires
- `fusion_dat_to_netcdf.py` : Regroupement des fichiers de données brutes en un seul fichier NETCDF4. Utilisé pour les calculs de MRD.
  **Instructions dans les commentaires en début de programme !**
- `read_EddyPro_Output_v2.py` : Lecture des fichiers de sortie d'EddyPro (`full_output`, spectres, ogives), récupération de certaines variables dans d'autres fichiers de sortie ($\langle u'w'\rangle$ dans fichier `fluxnet` par exemple), conversion en fichiers NETCDF.
  **Instructions dans les commentaires en début de programme ! Le code fonctionne bien mais mérite d'être amélioré. Je peux toujours le faire sur demande ...**
## Projets EddyPro

## Bibliographie

## Fichiers de données

## Infos en Vrac

## Librairies nécessaires : 
Tous les programmes sont écrits en **Python 3**. A part la bibliothèque standard, les librairies suivantes sont utilisés : 
- Librairies de calcul scientifique de base : numpy/scipy/matplotlib.
- Librairies de manipulation de données : pandas, xarray. Perso, j'utilise surtout xarray (documentation très bien faite [ici](https://docs.xarray.dev/en/stable/index.html) !)
- Parseur de chaines de caractère : [scanf](https://pypi.org/project/scanf/).
- Barres de progression : [tqdm](https://tqdm.github.io/)
- Tracé de roses des vents : [windrose](https://python-windrose.github.io/windrose/)

## Conditions d'utilisation
Faites ce que vous voulez de ces fichiers, a deux détails près :
- Pas d'utilisation commerciale (même si on me verse une partie des bénéfices !)
- Pas d'utilisation à des fins malveillantes.
