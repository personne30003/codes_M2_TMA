# +
import numpy as np
import netCDF4 as nc
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import MRD_v3 as MRD
import time as clk
w_i=np.array([1,3,2,5,1,2,1,3])
phi_i=np.array([1,5,3,2,5,4,3,2])
print("test fonction MRD : ")
print(f"w_i:{w_i}")
print(f"phi_i{phi_i}")
print(f"MRD(w_i,phi_i) {MRD.MRD(w_i,phi_i,get_timescale=True)}")
print("test MRD_segments sur données TP CLA")
t0=clk.time()
print("chargement des données")
file_path=r'C:\\Users\evanl\Documents\TP_CLA\sonicdata_2023_03_10.nc.nc4'
r2 = nc.Dataset(file_path, 'r', format='NETCDF4')
#print(r2)
time=pd.to_datetime(r2['time'][:])
temp_csat=r2['temp_csat'][:]
w_csat=r2['w_csat'][:]
freq_ech=20.0
duree_segments='60min'#durée des segments EN MINUTES
N_ech_segments=int(duree_segments.strip('min'))*60*int(freq_ech)
tmin=np.datetime64("2023-10-06 23:00:00")
tmax=np.datetime64("2023-10-07 08:00:00")

def slice_segments(array,taille_segments,equals=True):
    N_a=len(array)
    #print(f"N_a : {N_a}")
    N_seg=N_a//taille_segments
    #print(f"N_seg {N_seg}")
    reste =N_a% taille_segments
    cpt=0
    res=[]
    while cpt <=N_seg:
        res.append(array[taille_segments*cpt:taille_segments*(cpt+1)])
        cpt+=1
        #print(f" cpt : {cpt}")
    if (reste!=0) and (equals==True): 
        res[-1]=np.append(res[-1],[np.nan for i in range(len(res[-1]),taille_segments)])
    return np.array(res)

serie_Ts=pd.Series(temp_csat,index=time,name="T").truncate(before=tmin,after=tmax)
serie_w=pd.Series(w_csat,index=time,name="w").truncate(before=tmin,after=tmax)

Ts=slice_segments(serie_Ts.values,N_ech_segments)
print(f"segments Ts {Ts}")
w=slice_segments(serie_w.values,N_ech_segments)
print(f"fait en {clk.time() -t0} s")
print(f"nombre segments {len(Ts)}")
print("calcul spectre MRD flux de chaleur vertical wTs")
t0=clk.time()
MRD_wT=MRD.MRD_segments(w,Ts,name=('w','Ts'),f_ech=freq_ech,bar_progress=True,filtrage=False)
#print(f"MRD_wT[0]['temps'] {MRD_wT[0]['temps']}")
#print(f"len(MRD_wT[0]['temps']) {len(MRD_wT[0]['temps'])}")

#print(f"MRD_wT[0]['wTs'][0] {MRD_wT[0]['wTs']}")
#print(f"len(MRD_wT[0]['wTs'][0]) {len(MRD_wT[0]['wTs'][0])}")
print(f"MRD_wT {MRD_wT}")
print(f"fait en {clk.time() -t0}")
t0=clk.time()
print("calcul des moyennes et des barres d'erreurs")
spectres_moy=MRD.spectre_moy(MRD_wT)
spectres_med=MRD.spectre_median(MRD_wT)
#print(f" cospectre {cospectre}")
print(f"fait en {clk.time() -t0}")
print("tracé")
pic_cospectre_moy,gap_cospectre_moy=MRD.gap_spectral_moy(MRD_wT,'wTs',filtre=True)

pic_cospectre,gap_cospectre=pic_spectral_algo(cospectre_moy['wTs'],cospectre_moy['wTs_cum'],cospectre_moy['temps'])
pic_spectre,gap_spectre=pic_spectral_algo(spectres_moy['w'],spectres_moy['w_cum'],spectres_moy['temps'])

fig=plt.figure()
MRD.plot_spectre_segments(spectres_moy,'wTs',xlabel='temps (s)',ylabel=r"co_spectre $K\cdot m\cdot s^{-1}$")
MRD.plot_spectre(spectres_moy,'wTs',ecolor='k',color='k',capthick=10)
plt.axvline(gap_cospectre_moy,label="gap moyen="+str(gap_cospectre_moy)+" s", color='k')
plt.axvline(pic_cospectre_moy,label="pic moyen="+str(pic_cospectre_moy)+" s", color='tab:gray')
#plt.axvline(gap_cospectre,label="gap spectre moyen="+str(gap_cospectre)+" s", color='tab:gray')
#plt.axvline(pic_cospectre,label="pic turbulence="+str(pic_cospectre)+" s", color='k')
plt.legend()

fig=plt.figure()
MRD.plot_spectre_segments(spectres_moy,'wTs_cum',xlabel='temps (s)',ylabel=r"flux $K\cdot m\cdot s^{-1}$")
plt.xscale('log')
plt.xlabel('temps (s)')
plt.ylabel(r"flux $K\cdot m\cdot s^{-1}$")

#gap_spectre=new_gap_spectral(spectres_moy,'w')
pic_spectre_moy,gap_spectre_moy=gap_spectral_moy(MRD_wT,'w')
fig=plt.figure()
MRD.plot_spectre_segments(MRD_wT,'w',xlabel='temps (s)',ylabel=r"spectre $m^{2}\cdot s^{-2}$")
plt.xscale('log')
plt.xlabel('temps (s)')
plt.ylabel(r"spectre $m^{2}\cdot s^{-2}$")
plt.axvline(gap_spectre_moy,label="gap moyen="+str(gap_spectre_moy)+" s",color='k')
plt.axvline(pic_spectre_moy,label="pic moyen="+str(pic_spectre_moy)+" s",color='tab:gray')
#plt.axvline(pic_spectre,label="pic turbulence="+str(pic_spectre)+" s", color='k')
#plt.axvline(gap_spectre,label="gap="+str(gap_spectre)+" s",color='tab:gray')
plt.legend()

fig=plt.figure()
MRD.plot_spectre_segments(MRD_wT,'w_cum',xlabel='temps (s)',ylabel=r"spectre $m^{2}\cdot s^{-2}$")
plt.xscale('log')
plt.xlabel('temps (s)')
plt.ylabel(r"spectre $m^{2}\cdot s^{-2}$")
# -


