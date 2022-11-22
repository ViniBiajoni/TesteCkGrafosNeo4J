import numpy as np
import pandas as pd
import os
import subprocess
import time

def meas_criticalities(E,nmed,kmax,nbar,type_exec):
    
    #Prepara e Executa Analise de Crits Medidas em C
    nrows= int(nmed)
    ncols= int(nmed)
    vector = np.reshape(E, (1, nrows*ncols))
    f = open("E_teste.txt", "w+")
    f.write("%d " % (int(nbar)))
    f.write("%d " % (int(nmed)))
    f.write("%d\n" % (int(kmax)))
    for m in range(nrows):
        for n in range(ncols):
            f.write("%1.15f " % (vector[0,m*ncols + n]))
        f.write("\n")
    f.close() 

    ##########################################Pós-processo análise Ck-meds######################################## 
    if os.path.exists("Crits.csv"):
      os.remove("Crits.csv") 
    else:
      print("The file does not exist yet")

    if type_exec == 0:
        subprocess.Popen([r"GPU_BF_comp.exe"])
        finished = False
        while finished == False:
            if (os.access("Crits.csv",os.R_OK)):
                finished = True
        file_crits= 'Crits.csv'
        colNames=['Criticalidades']
        crits =  pd.read_csv(file_crits,names=colNames)
        j=0
        card = []
        integer_list = []
        ############################Monta Dicionario por Cardinalidade c/ as Criticalidades de Medidas########################################
        crits = pd.read_csv(file_crits,names=colNames) # leitura nova para considerar o fim do print do csv
        for c in crits['Criticalidades']:
            temp=c.split()
            integer_map = map(int, temp)
            integer_list.append(list(integer_map))
            card.append(len(integer_list[j]))
            j=j+1
            card_max= max(card)

        keys = list(range(kmax))
        sol_list_med_number = {key: [] for key in keys}
        sol_list_med_str = {key: [] for key in keys} #create the list with the criticalities strings
        for ck in integer_list:
            tupla=[]
            temp =[]
            for i in ck:
                tupla.append(i)

            sol_list_med_number[len(ck)-1].append(set(tupla))
        #############################Number of Criticalities per Cardinality################
        number_of_cks_meds = [card.count(i+1) for i in range(kmax)]

    if type_exec == 1:
        if os.path.exists("CritsBase.txt"):
            os.remove("CritsBase.txt") 
        else:
            print("The file does not exist yet")
        subprocess.Popen([r"CPU_BF_simp.exe"])
        finished = False
        while finished == False:
            if os.path.exists("CritsBase.txt"):
                if kmax == 6 or nbar > 30:
                    time.sleep(5)
                break 
        time.sleep(1)
        sol_list_med_number = []
        sol_list_med_str = []
        number_of_cks_meds = np.loadtxt("CritsBase.txt")
    
    return number_of_cks_meds, sol_list_med_number