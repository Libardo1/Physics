#! /usr/bin/env python

# Cree un fichier "liste_runs.txt" par bolo a partir d'un fichier "liste_bolos.txt", et d'un repertoire de runs samba

# TODO:
# - crosscheck avec le log!

import os,re,sys
import SambaUtils,RunParams
from GlobalParams import ReadGlobalParams

################################
# LECTURE DES PARAMETRES
paramfile="params_python.txt"
if len(sys.argv) == 2 : paramfile=sys.argv[1]
gParams=ReadGlobalParams(paramfile)
sambadir=gParams['sambadir']+"/"
anadir=gParams['anadir']+"/"
bolo=gParams['bolo']
runselection=gParams['runselection'] if "runselection" in gParams else "No"
################################

if runselection!="No" :
    fullrunlist=[]
    f=open(runselection,"r")
    lines=f.readlines()
    f.close()
    for theline in lines:
        if theline.find("#")==-1 : fullrunlist.append(theline.strip())
    fullrunlist=[x for x in fullrunlist if x!=""]
else :
    toto=os.listdir(sambadir)
    fullrunlist=[x for x in toto if x[0]!="."] # virer les trucs genre .DS_store
fullrunlist.sort() # Liste dans l'ordre temporel

# Boucle sur les bolos du Run
# EDITED: bolometre fixe maintenant.
# Mais pas encore clean (nettoyer aussi avec runparams)
bololist=RunParams.ReadListeBolos(anadir)
mac=""
for bb in bololist :
    if bb.Name==bolo : mac=bb.Mac
if mac=="" : print "Did not find the bolo in the list!"
channels=RunParams.ReadBoloChannels(bolo,anadir)

letter=SambaUtils.MacLetter(mac)
runlist=[]
for run in fullrunlist :
    pp=re.search("[a-z][a-z][0-9][0-9]"+letter+"[0-9][0-9][0-9]",run)
    if pp != None :
        runlist.append(run)
print "Runs for",bolo,":",runlist
if not os.path.exists(anadir+bolo) :
    print anadir+bolo,"does not exists!"
outputfile=open(anadir+bolo+"/liste_runs.txt",'w')
outputfile.write("# Run type mod_chal1 mod_chal2 v_col1 v_col2 v_vet1 v_vet2 v_gar1 v_gar2\n")

# Recherche des parametres pour chaque run
for run in runlist :
    runtype=SambaUtils.GetRunType_Partition(sambadir+run+"/"+run+"_000")
    coefficients=[]
    for thechannel in channels :
        if thechannel == "NONE" :
            coefficients.append(0)
        else :
            # NB cas d'une voie "slow" : on cherche les consignes de la voie "ionis" correspondante
            coefficients.append(SambaUtils.GetConsigne(sambadir,run,thechannel.replace("slow","ionis")))
    ligne=[run,runtype]
    ligne.extend(["%i" % x for x in coefficients[0:2]])
    ligne.extend(["%.2f" % x for x in coefficients[2:]])
    outputfile.write(" ".join(ligne)+"\n")
outputfile.close()
    

