import os
import numpy as np
from StateEstimation import case_prepare
import time
from datetime import datetime
from AnaliseCrit import *
import json 

  #dict_meds={}       #Numero da medida -> Tipo da medida ex:"I28"
    #UMs = []           #UMs Ativadas
    #dict_UMs_meds = {} #Número da UM -> Medidas da UM
    #pmu                #Quantidade medidas de ângulo
def main():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    med_file= os.path.join(THIS_FOLDER,'medicao\ieee30_observability_PSCC_2014B_43.med')
    meds= np.loadtxt(med_file)

    net_file= os.path.join(THIS_FOLDER, 'sistemas\ieee30.txt')
    net = np.loadtxt(net_file)
 
    num_bus  = int(max(meds[i][1] for i in range(len(meds))))
    num_meds = len(meds[:,0])
    
    H_original, dict_meds, dict_UMs_meds,UMs,Adj, pmu = case_prepare(meds,net)
    G = np.transpose(H_original)@H_original
    E = np.identity(num_meds) - H_original@(np.linalg.inv(G))@np.transpose(H_original)
    k_max_meds = 5
   
     
    #Análise de Criticalidade
    _, sol_list_med_number = meas_criticalities(E, num_meds, k_max_meds, num_bus, 0)
    for key in sol_list_med_number.keys():
        lista_aux = []
        for elem in sol_list_med_number[key]:
            elementos = list(elem)
            elementos_formatados = [dict_meds[i] for i in elementos]
            lista_aux.append(elementos_formatados)
        sol_list_med_number[key] = lista_aux


    with open('data_crits_30Bus_43_meds.json', 'w') as f:
        json.dump(sol_list_med_number, f)
    # json_criticalidades = json.dumps(sol_list_med_number)
    # print(json_criticalidades)
if __name__ == "__main__":
    main()


