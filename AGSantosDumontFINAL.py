# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 10:45:44 2016

@author: Bolsista_Manoel
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 09:33:55 2016

@author: Bolsista_Manoel
"""
# 
#8/11/2016
"""
Created on Mon Oct 03 15:57:12 2016

@author: Bolsistas
"""
import win32com.client as com #Importando pacotes
import os
import random
import pandas as pd
import time
start_time = time.time()
print("Pacotes carregados!")
Vissim = com.Dispatch("Vissim.Vissim.800") #Abrindo o Vissim
print("Vissim aberto")
Path_of_COM_Basic_Commands_network = os.getcwd() #Formando o caminho de abertura
EXEMPLOP = os.path.join(Path_of_COM_Basic_Commands_network, 'RedeSD.inpx')#a mulher do sapo ficou estranha, checar RedeSD
flag = False 
Vissim.LoadNet(EXEMPLOP, flag) #Carregando o arquivo
print('Arquivo carregado!')
#Simulacao
replicacao=2#input("Insira o numero de replicacoes...") #Estabelecendo as variaveis inputadas
ind=3#input("Insira o numero de individuos por populacao...")#foram 10 individuos
sodeh=42#input("Insira a Seed Inicial...")
y=10#input("Insira o incremento...")
velesp=(496.35/127)#input("Qual a velocidade esperada...") MUDANÇA FEITA NOVA REDE
geracoes=2#input('Quantas geracoes voce deseja...')
divers=2#input("De quantas em quantas geracoes vai ocorrer a diversidade?")
bxmult=range(ind)
ax=range(ind)
bxadd=range(ind)
sleepprob=range(ind)
sleepdur=range(ind)
minheadw=range(ind)
safedist=range(ind)
w=[5,12,15,20,25,30,40,50,60,70,80,85,90,100,120,130,140,1001,1002,1003,1004,1005,1007,1008,1009,1010,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1040,1041,1042,1043,1044,1045,1046,1047]
listdes=w[5:10]

desspeeddist=range(ind)
intervalos = ['300-1200','1200-2100','2100-3000','3000-3900']
for x in range(ind):
    desspeeddist[x]=random.choice(listdes)
    bxmult[x]=round(random.uniform(1,8),1)
    bxadd[x]=round(random.uniform(1,8),1)
    ax[x]=round(random.uniform(1,4),1)
    sleepdur[x]=round(random.uniform(0,1),1)
    sleepprob[x]=round(random.uniform(0,0.1),3)
    minheadw[x]=round(random.uniform(0.5,3),1)
    safedist[x]=round(random.uniform(0.2,0.8),1)

    #upperbound[x]=round(random.uniform(50,70),1)
mat=pd.DataFrame({'ax':ax,'bxmult':bxmult,'bxadd':bxadd,'desspeeddist':desspeeddist,'sleepprob':sleepprob,'sleepdur':sleepdur,'minheadw':minheadw,'safedist':safedist})
errof=500000000000000 #Estabelecendo variaveis que auxiliarao no calculo de erros
errof2=0
#GERAL=pd.DataFrame(columns=['Geracao','Individuo','Semente','  Distancia entre Veiculos','  bxadd','bxmult','desspeeddist','  Velocidade do Individuo'])
buffl=[] 
resumo = pd.DataFrame(columns=['Geracao','Individuo','Media Velocidade'])
buffresumol =[]
indivm=0
indivp=0
listaerger=range(ind)
alfa = pd.DataFrame(columns=['Geracao','ErroM'])
buffalfa =[]
arrumadosbuffer =[]
def simulacao(a,b,c,d,e,f,g,i,h,j,k,x,z): #Estabelecendo uma funcao para a simulacao
    #Inputs: a=bxadd, b=Semente inicial, c=Ax, d=Incremento da semente, e=Numero de replicacoes por individuo, f=bxmult, g = geracao, i= tag do individuo, h=desspeeddist, j=duraçãodosleep, k=probabilidade de sleep
    #Outputs: listadel e listavel com valores do delay e velocidade media dessa simulacao+Escreve no arquivo csv ou valores de cada semente
    for l in range(replicacao):
        #Vissim.Net.PriorityRules[0].ConflictMarkers[0].SetAttValue("MinGapTime", a)
        #print("Seed definida:{}".format(b))
        Vissim.Simulation.SetAttValue('RandSeed', b)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('W74ax', c)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('W74bxAdd', a)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('W74bxMult', f)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('SleepDur', j)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('SleepProb', k)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('MinHdwy', x)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('SafDistFactLnChg', z)

        #Vissim.Net.DrivingBehaviors[0].SetAttValue('W74bxMult', f)
        End_of_simulation = 3900 # simulation second [s]

        Vissim.Simulation.SetAttValue('SimPeriod', End_of_simulation)
        Veh_composition_number = 2
        Rel_Flows = Vissim.Net.VehicleCompositions.ItemByKey(Veh_composition_number).VehCompRelFlows.GetAll()
        Rel_Flows[0].SetAttValue('DesSpeedDistr',h) # Changing the desired speed distribution
        Veh_composition_number = 2
        Rel_Flows = Vissim.Net.VehicleCompositions.ItemByKey(Veh_composition_number).VehCompRelFlows.GetAll()
        Rel_Flows[1].SetAttValue('DesSpeedDistr',h) # Changing the desired speed distribution
        Veh_composition_number = 3
        Rel_Flows = Vissim.Net.VehicleCompositions.ItemByKey(Veh_composition_number).VehCompRelFlows.GetAll()
        Rel_Flows[0].SetAttValue('DesSpeedDistr',h) # Changing the desired speed distribution
        #print("Simulacao Iniciada")
        Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode",1)            
        Vissim.Simulation.RunContinuous()
        Veh_TT_measurement_number = 1
        Veh_TT_measurement = Vissim.Net.VehicleTravelTimeMeasurements.ItemByKey(Veh_TT_measurement_number)   
        TT1= Veh_TT_measurement.AttValue('TravTm(Current,1,All)')
        TT2= Veh_TT_measurement.AttValue('TravTm(Current,2,All)')
        TT3= Veh_TT_measurement.AttValue('TravTm(Current,3,All)')
        TT4= Veh_TT_measurement.AttValue('TravTm(Current,4,All)')
        Dist= Veh_TT_measurement.AttValue('Dist')
        #print(Dist)
        #print(TT1)
        v1=Dist/TT1#alterar pra distancia correta, alterar o 100
        v2=Dist/TT2
        v3=Dist/TT3
        v4=Dist/TT4
        v=(v1+v2+v3+v4)/4
        er1 = (abs(velesp-v1))/v1
        er2 = (abs(velesp-v2))/v2
        er3 = (abs(velesp-v3))/v3
        er4 = (abs(velesp-v4))/v4
        er = (er1+er2+er3+er4)/4    
        listaer[l]=er
        listavel[l]=v
        print('geracao %.1f, individuo %.1f' % (g,i))
        temp = pd.DataFrame([[g,i,b,c,a,f,h,j,k,x,z,v,er,er1,er2,er3,er4,v1,v2,v3,v4]], columns = ['Geracao','Individuo', 'Semente', 'Distancia entre Veiculos', 'bxadd','bxmult','desspeeddist','SleepDur','SleepProb','MinHeadway','SafeDistFactLnChg', '  Velocidade do Individuo','ErroTotal','Erro1','Erro2','Erro3','Erro4','V1','V2','V3','V4'])
        buffl.append(temp)
        b+=d      
        appended_data = pd.concat(buffl,ignore_index = True)
        appended_data.to_csv('outputSantosDumont.csv',sep=';',float_format='%.3f')        
        if i == (ind-1):
            temp1 = appended_data[appended_data['Geracao']== g]
            arrumados = temp1.sort(columns='ErroTotal', ascending = True)
            #print(arrumados)
            arrumadosbuffer.append(arrumados)
      #  print(arrumadosbuffer)
        if g == (geracoes-1):
            appended_arrumados = pd.concat(arrumadosbuffer,ignore_index = True)
            appended_arrumados.to_csv('emordemsantosdumont.csv',sep=';',float_format='%.3f')

global A       
for i in range(ind): #Lista que calculara a media do Delay e da Velocidade por individuo
    listavel=range(replicacao)
    listadel=range(replicacao)
    listaer=range(replicacao)
    Random_Seed=sodeh
    simulacao(mat['bxadd'][i],sodeh,mat['ax'][i],y,replicacao,mat['bxmult'][i],0,i,int(mat['desspeeddist'][i]),mat['sleepdur'][i],mat['sleepprob'][i],mat['minheadw'][i],mat['safedist'][i])
    matvd=pd.DataFrame({'Vel':listavel})
    matvd1=pd.DataFrame({'er':listaer})
    #print(matvd)    
    velmedia=pd.DataFrame.mean(matvd)['Vel']
    ermedia=pd.DataFrame.mean(matvd1)['er']
    listaerger[i]=ermedia
    Random_Seed+=y
    mape=(velmedia-velesp)/velmedia
    
    #print(velmedia)
    if (abs(errof))>ermedia:
        errof=ermedia
        vmelhor=velmedia
        indivm=i
        A = errof
    if ermedia>(abs(errof2)):
        errof2=ermedia
        vpior=velmedia
        indivp=i
    temp = pd.DataFrame([[0,i,velmedia,velesp,ermedia]],columns=['Geracao','Individuo','Media Velocidade','Velocidade Esperada','Erro'])
    buffresumol.append(temp)
tempalfa = pd.DataFrame([[0,A]],columns=['Geracao','ErroM'])
buffalfa.append(tempalfa)
alfas = pd.concat(buffalfa,ignore_index=True)

aresumo = pd.concat(buffresumol,ignore_index=True)
#print(aresumo)    
#    dados.write('Velocidade Media; %f\n' % (velmedia)) #Escrevendo os valores medios no arquivo csv
#    dados.write('Delay Medio; %f\n' % (delmedia))
#    
#dados.write('O melhor individuo dessa populacao foi o individuo numero %.0f com velocidade de %.2f e delay de %.2f;\n' % (indivm, vmelhor, dmelhor))
#dados.write('O pior individuo dessa populacao foi o individuo numero  %.0f com velocidade de %.2f e delay de %.2f;\n' % (indivp, vpior, dpior))
#print(mape)

for r in range(geracoes-1):
    if abs(errof)*100 < 1 or r==20:
        break
    #checagem a cada numero predefinido de geracoes para predatismo e 
    errof=500000000000000 #Reestabelecendo os erros maximos e minimos para a filtragem dessa geracao
    errof2=0
    l=range(len(listaerger))
    for dd in range(len(l)):
        l[dd]=listaerger[dd]
    listaerger.sort(reverse=True)
    checagem=listaerger[0:int(ind*0.2)]
    listaindic=range(int((ind*0.2)))
    for kk in range(int((ind*0.2))):
        for indic in range(len(listaerger)):
            if checagem[kk]==l[indic]:
                listaindic[kk]=indic     

    if (r+1)/divers != int((r+1)/divers):
        for q in range(ind): #A.G. -> Melhor individuo continua, Pior morre; Outros tres cruzam com o melhor; Novo individuo aparece gerado randomicamente
            if q!=indivm:
                if random.random()<.5:
                    mat['ax'][q]=mat['ax'][indivm]
                if random.random()<.5:
                    mat['bxmult'][q]=mat['bxmult'][indivm]
                if random.random()<.5:
                    mat['bxadd'][q]=mat['bxadd'][indivm]
                if random.random()<.5:
                    mat['desspeeddist'][q]=mat['desspeeddist'][indivm]
                if random.random()<.5:
                    mat['sleepprob'][q]=mat['sleepprob'][indivm] 
                if random.random()<.5:
                    mat['sleepdur'][q]=mat['sleepdur'][indivm]
                if random.random()<.5:
                    mat['minheadw'][q]=mat['minheadw'][indivm] 
                if random.random()<.5:
                    mat['safedist'][q]=mat['safedist'][indivm]                      
# nesse laco o melhor individuo sobrevive e cruza com os demais
    else:
        for q in range(ind): #A.G. -> Melhor individuo continua, Pior morre; Outros tres cruzam com o melhor; Novo individuo aparece gerado randomicamente
            if q!=indivm:
                if q in listaindic:
                    mat['bxmult'][q]=round(random.uniform(1,8),1)
                    mat['bxadd'][q]=round(random.uniform(1,8),1)
                    mat['ax'][q]=round(random.uniform(1,4),1)
                    mat['desspeeddist'][q]=random.choice(listdes)#meme choose
                    mat['sleepdur'][q]=round(random.uniform(0,1),1)
                    mat['sleepprob'][q]=round(random.uniform(0,0.1),3)
                    mat['minheadw'][q]=round(random.uniform(0.5,3),1)
                    mat['safedist'][q]=round(random.uniform(0.2,0.8),1)
                else:
                    if random.random()<.5:
                        mat['ax'][q]=mat['ax'][indivm]
                    if random.random()<.5:
                        mat['bxmult'][q]=mat['bxmult'][indivm]
                    if random.random()<.5:
                        mat['bxadd'][q]=mat['bxadd'][indivm]
                    if random.random()<.5:
                        mat['desspeeddist'][q]=mat['desspeeddist'][indivm]
                    if random.random()<.5:
                        mat['sleepprob'][q]=mat['sleepprob'][indivm] 
                    if random.random()<.5:
                        mat['sleepdur'][q]=mat['sleepdur'][indivm]
                    if random.random()<.5:
                        mat['minheadw'][q]=mat['minheadw'][indivm] 
                    if random.random()<.5:
                        mat['safedist'][q]=mat['safedist'][indivm]
            if random.random()<.2 and q!=indivm:
                mat['ax'][q]=round(random.uniform(1,4),1)
            if random.random()<.2 and q!=indivm:
                mat['bxadd'][q]=round(random.uniform(1,8),1)
            if random.random()<.2 and q!=indivm:
                mat['bxmult'][q]=round(random.uniform(1,8),1)
            if random.random()<.2 and q!=indivm:
                mat['desspeeddist'][q]=random.choice(listdes)#you again
            if random.random()<.2 and q!=indivm:
                mat['sleepdur'][q]=round(random.uniform(0,1),1)
            if random.random()<.2 and q!=indivm:
                mat['sleepprob'][q]=round(random.uniform(0,0.1),3)#you again
            if random.random()<.2 and q!=indivm:
                mat['minheadw'][q]=round(random.uniform(0.5,3),1)
            if random.random()<.2 and q!=indivm:
                mat['safedist'][q]=round(random.uniform(0.2,0.8),1)#you again
    for j in range(ind): 
        listavel={}
        simulacao(mat['bxadd'][j],sodeh,mat['ax'][j],y,replicacao,mat['bxmult'][j],r+1,j,int(mat['desspeeddist'][j]),mat['sleepdur'][j],mat['sleepprob'][j],mat['minheadw'][j],mat['safedist'][j])
        matvd=pd.DataFrame({'Vel':listavel})
        velmedia=pd.DataFrame.mean(matvd)['Vel']
        matvd1=pd.DataFrame({'er':listaer})
        ermedia=pd.DataFrame.mean(matvd1)['er']
        listaerger[i]=ermedia

        mape=(velmedia-velesp)/velmedia
        #print(velmedia)
        if (abs(errof))>ermedia:
            errof=ermedia
            vmelhor=velmedia
            indivm=j
            A = errof
        if ermedia>(abs(errof2)):
            errof2=ermedia
            vpior=velmedia
            indivp=j 
        temp = pd.DataFrame([[r+1,j,velmedia,ermedia]],columns=['Geracao','Individuo','Media Velocidade','Erro'])
        buffresumol.append(temp)
    tempalfa = pd.DataFrame([[r+1,A]],columns=['Geracao','ErroM'])
    buffalfa.append(tempalfa)
    alfas = pd.concat(buffalfa,ignore_index=True)
    aresumo = pd.concat(buffresumol,ignore_index = True)
    aresumo.to_csv('ResumoSD.csv',sep=';',float_format='%.8f')
    alfas.to_csv('ResumoAlfas.csv',sep=';',float_format='%.8f')    
    
sheet_name = 'GraficodosAlfasSD'
writer     = pd.ExcelWriter('GraficodosAlfasSD.xlsx', engine='xlsxwriter')
alfas.to_excel(writer, sheet_name=sheet_name)
workbook  = writer.book
worksheet = writer.sheets[sheet_name]
chart = workbook.add_chart({'type': 'scatter'})
ln=len(alfas['Geracao'])
chart.add_series({
        'categories': ['GraficodosAlfasSD', 1, 1, ln, 1],
        'values':     ['GraficodosAlfasSD', 1, 2, ln, 2],
        'line':       {'width': 1.00},

    })
chart.set_x_axis({'name': 'Geracao', 'date_axis': False})
chart.set_y_axis({'name': 'Erro', 'major_gridlines': {'visible': False}})
worksheet.insert_chart('H2', chart)
writer.save()
Vissim = None
print(time.time()-start_time)
print("C'est fini")
