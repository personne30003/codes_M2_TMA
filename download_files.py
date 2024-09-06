"""
Script permettant de télécharger les fichiers ncdf du TP Coriolis en local à partir d'openDAP.
Auteur : aucune importance ...
Dépendances : xarray, netCDF4
On télécharge d'abord les fichiers un à un, puis on les fusionne pour avoir deux fichiers ncdf
contenant:
          -les données sous forme brutes (fichiers de la forme "EXP_XX_tot.nc")
          -les vitesses moyennes ainsi que leurs fluctuations,pareil pour les dérivées spatiales et la vorticité, ainsi
           que les trois composantes du tenseur de Reynolds (fichiers de la forme "EXP_XX_moy_f.nc")
Instructions pour l'utiliser : 
           -Créer un répertoire pour le TP, puis créér des sous-répertoires pour les expériences ("donnees_EXP23" par exemple)
           -Placer le fichier contenant ce script dans le répertoire pour le TP.
           -Modifier la variable "experience" pour l'experience dont vous voulez télécharger les fichiers.
           -Si les fichiers ncdf de l'experience ont déjà été téléchargés, mettre la variable "fait" à la valeur "False"
           -Si vous ne voulez pas télécharger l'intégralité des 1000 fichiers, mettez la variable "i_final_tel" à la valeur de votre choix.
            De même, si la connexion coupe, vous pouvez modifier la variable "i_initial_tel" à la dernière valeur pour laquelle ça a coupé.
           -Executer. Selon la qualité de la connexion internet, le téléchargement peut prendre des heures. Le reste ne prend que
            quelques minutes...

"""
import netCDF4 as nc
import xarray as xr
import time
import os
#paramètres
experience="EXP23"
fait=False#à changer
i_initial_tel=1
i_final_tel=505
i_initial_tot=i_initial_tel
i_final_tot=i_final_tel

adresse=r"http://servdap.legi.grenoble-inp.fr/opendap/hyrax/meige/22_TP_TMA/TP04_CORIOLIS/DATA/"+experience+r"/im.civ-images.png.civ-images.png.civ.mproj/"
file_path=os.getcwd()+r'/donnees_'+experience

ds_sauvegarde=xr.Dataset()
noms=[("img_"+str(j)+"_1.nc") for j in range(i_initial_tot,i_final_tot+1)]
print("bienvenue "+os.environ.get("USERNAME"))
print("repertoire de stockage :  "+file_path)

if fait==False:
    print("debut telechargement : ")
    t1=time.time()
    for i in range(i_initial_tel,i_final_tel+1):
        t2=time.time()
        nom="img_"+str(i)+"_1.nc"
        ds_temp=xr.open_dataset(adresse+nom)
        ds_temp.to_netcdf(file_path+r'/'+nom)
        print("fichier "+str(i)+" telecharge")
        print("temps pris : "+str((time.time()-t2)/60)+" min")
        if i == i_final_tel :
            fait=True
            print("tous les fichiers telecharges")
            print("temps pris "+str((time.time()-t1)/60)+" min")
if fait== True:
    print("fusion en un seul fichier : ")
    t3=time.time()
    ds_init=xr.open_dataset(adresse+noms[0])
    ds_init.expand_dims('t',axis=2)
    ds_liste=[]
    ds_liste.append(ds_init)
    for i in range(0,len(noms)):
        ds_i=xr.open_dataset(file_path+r'/'+noms[i])
        ds_i.expand_dims('t',axis=2)
        ds_liste.append(ds_i)
    ds_sauvegarde=xr.concat(ds_liste,dim='t')
print("tous les fichiers sont fusionnés en un seul")
print("temps pris : "+str((time.time()-t3)/60)+" minutes")
print("creation du fichier")
nom_fichier=experience+"_tot.nc"
ds_sauvegarde.to_netcdf(file_path+r'/'+nom_fichier)
print("fait")
print("test : ")
r=xr.open_dataset(file_path+"/"+nom_fichier)
print(r)
print("calcul des moyennes et des fluctuations")
U=ds_sauvegarde['U'][:]#dataArray
V=ds_sauvegarde['V'][:]

DUDX=ds_sauvegarde['DUDX'][:]
DUDY=ds_sauvegarde['DUDY'][:]
DVDX=ds_sauvegarde['DVDX'][:]
DVDY=ds_sauvegarde['DVDY'][:]
rot=ds_sauvegarde['curl'][:]
t4=time.time()
U_moy=U.mean(dim='t')
V_moy=V.mean(dim='t')

DUDX_moy=DUDX.mean(dim='t')
DUDY_moy=DUDY.mean(dim='t')
DVDY_moy=DVDY.mean(dim='t')
DVDX_moy=DVDX.mean(dim='t')
rot_moy=rot.mean(dim='t')
nb_t=ds_sauvegarde.coords['t'].size
U_f=U#initialisation de tableaux de meme taille que U et V
V_f=U
DUDX_f=U;DUDY_f=U
DVDX_f=U;DVDY_f=U
rot_f=U
for i in range(0,nb_t):
    U_t=U.isel(t=i)
    V_t=V.isel(t=i)

    DUDX_t=DUDX.isel(t=i)
    DVDX_t=DVDX.isel(t=i)
    DUDY_t=DUDY.isel(t=i)
    DVDY_t=DVDY.isel(t=i)
    rot_t=rot.isel(t=i)
    U_f[dict(t=i)]=U_t-U_moy
    V_f[dict(t=i)]=V_t-V_moy

    DUDX_f[dict(t=i)]=DUDX_t-DUDX_moy
    DVDX_f[dict(t=i)]=DVDX_t-DVDX_moy
    DUDY_f[dict(t=i)]=DUDY_t-DUDY_moy
    DVDY_f[dict(t=i)]=DVDY_t-DVDY_moy
    rot_f[dict(t=i)]=rot_t-rot_moy
#calcul des composantes du tenseur de Reynolds
R_UU=(U_f**2).mean(dim='t')
R_VV=(V_f**2).mean(dim='t')
R_UV=(U_f*V_f).mean(dim='t')
print("fait")
print("temps pris : "+str((time.time()-t4)/60)+" min")
print("creation d'un autre fichier : ")
ds_seconde=xr.Dataset()
U_f_ds=U_f.to_dataset(name="U_f");U_f_ds.attrs=dict(description="fluctuations U",units="cm/s")
V_f_ds=V_f.to_dataset(name="V_f");V_f_ds.attrs=dict(description="fluctuations V",units="cm/s")

DUDX_f_ds=DUDX_f.to_dataset(name="DUDX_f");DUDX_f_ds.attrs=dict(description="fluctuations DUDX",units="/s")
DVDX_f_ds=DVDX_f.to_dataset(name="DVDX_f");DVDX_f_ds.attrs=dict(description="fluctuations DVDX",units="/s")
DUDY_f_ds=DUDY_f.to_dataset(name="DUDY_f");DUDY_f_ds.attrs=dict(description="fluctuations DUDY",units="/s")
DVDY_f_ds=DVDY_f.to_dataset(name="DVDY_f");DVDY_f_ds.attrs=dict(description="fluctuations DVDY",units="/s")
rot_f_ds=rot_f.to_dataset(name="rot_f");rot_f_ds.attrs=dict(description="fluctuations rot",units="/s")
U_moy_ds=U_moy.to_dataset(name="U_m");U_moy_ds.attrs=dict(description="U moyenne",units="cm/s")
V_moy_ds=V_moy.to_dataset(name="V_m");V_moy_ds.attrs=dict(description="V moyenne",units="cm/s")

DUDX_moy_ds=DUDX_moy.to_dataset(name="DUDX_m");DUDX_moy_ds.attrs=dict(description="DUDX moyen",units="/s")
DVDX_moy_ds=DVDX_moy.to_dataset(name="DVDX_m");DVDX_moy_ds.attrs=dict(description="DVDX moyen",units="/s")
DUDY_moy_ds=DUDY_moy.to_dataset(name="DUDY_m");DUDY_moy_ds.attrs=dict(description="DUDY moyen",units="/s")
DVDY_moy_ds=DVDY_moy.to_dataset(name="DVDY_m");DVDY_moy_ds.attrs=dict(description="DVDY moyen",units="/s")
rot_moy_ds=rot_moy.to_dataset(name="rot_m");rot_moy_ds.attrs=dict(description="rot moyen",units="/s")
R_UU_ds=R_UU.to_dataset(name="R_UU");R_UU_ds.attrs=dict(description="cov(U,U)",units="(cm/s)**2")
R_VV_ds=R_VV.to_dataset(name="R_VV");R_VV_ds.attrs=dict(description="cov(V,V)",units="(cm/s)**2")
R_UV_ds=R_UV.to_dataset(name="R_UV");R_UV_ds.attrs=dict(description="cov(U,V)",units="(cm/s)**2")
#on met tout dans le Dataset créé
ds_seconde=ds_seconde.assign(U_moy_ds)
ds_seconde=ds_seconde.assign(V_moy_ds)
ds_seconde=ds_seconde.assign(R_UU_ds)
ds_seconde=ds_seconde.assign(R_VV_ds)
ds_seconde=ds_seconde.assign(R_UV_ds)

ds_seconde=ds_seconde.assign(DUDX_moy_ds)
ds_seconde=ds_seconde.assign(DUDY_moy_ds)
ds_seconde=ds_seconde.assign(DVDX_moy_ds)
ds_seconde=ds_seconde.assign(DVDY_moy_ds)
ds_seconde=ds_seconde.assign(rot_moy_ds)
ds_seconde=ds_seconde.assign(U_f_ds)
ds_seconde=ds_seconde.assign(V_f_ds)

ds_seconde=ds_seconde.assign(DUDX_f_ds)
ds_seconde=ds_seconde.assign(DUDY_f_ds)
ds_seconde=ds_seconde.assign(DVDX_f_ds)
ds_seconde=ds_seconde.assign(DVDY_f_ds)
ds_seconde=ds_seconde.assign(rot_f_ds)
nom_fichier2=experience+"_moy_f.nc"
ds_seconde.to_netcdf(file_path+r'/'+nom_fichier2)
print("fait")
print("temps pris "+str((time.time()-t4)/60)+" min")
print("test")
r=nc.Dataset(file_path+"/"+nom_fichier2,'r')
print(r)
print("au revoir !")
