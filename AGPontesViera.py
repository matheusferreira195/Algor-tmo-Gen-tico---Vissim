# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:00:10 2016

@author: Bolsista_Manoel
"""
from __future__ import print_function

import win32com.client as com #Importando pacotes
import os
import random
import pandas as pd
import time
import datetime  
#Inicialização e setup inicial do Vissim

start_time = time.time()
print("Pacotes carregados!")
Vissim = com.Dispatch("Vissim.Vissim") #Abrindo o Vissim
print("Vissim aberto")
Path_of_COM_Basic_Commands_network = os.getcwd() #Formando o caminho de abertura
EXEMPLOP = os.path.join(Path_of_COM_Basic_Commands_network, 'PontesVieira_atual.inpx')#diretório do arquivo de rede
flag = False 
Vissim.LoadNet(EXEMPLOP, flag) #Carregando o arquivo
print('Arquivo de rede carregado!')

#Configurações da Simulação
replicacao=3#input("Insira o numero de replicacoes...")
ind=10#input("Insira o numero de individuos por populacao...")
seed=42#input("Insira a Seed Inicial...")
delta=10#input("Insira o incremento...")
#velesp=(u.35/127  )#input("Qual a velocidade esperada...")
geracoes=10#input('Quantas geracoes voce deseja...')
divers=2#input("De quantas em quantas geracoes vai ocorrer a diversidade?")
hoje_bruto = str(datetime.datetime.now())
print(hoje_bruto)
hoje = (hoje_bruto.replace(":",""))
print(hoje)
#Criação das listas das primeiras variáveis aleatórias
bxmult=range(ind)
ax=range(ind)
bxadd=range(ind)
sleepprob=range(ind)
sleepdur=range(ind)
minheadw=range(ind)
safedist=range(ind)
#Criação das classes de velocidades desiredspeed
w=[5,12,15,20,25,30,40,50,60,70,80,85,90,100,120,130,140,1001,1002,1003,1004,1005,1007,1008,1009,1010,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1040,1041,1042,1043,1044,1045,1046,1047]
listdes=(w[5:10])
print(listdes)
desspeeddist=range(ind)
#Intervalos de tempo em que serão coletadas amostras
intervalos = ['300-1200','1200-2100','2100-3000','3000-3900']

#classe para printar a progressbar
'''import progressbar  as pb
class progress_timer:

    def __init__(self, n_iter, description="Something"):
        self.n_iter         = n_iter
        self.iter           = 0
        self.description    = description + ': '
        self.timer          = None
        self.initialize()

    def initialize(self):
        #initialize timer
        widgets = [self.description, pb.Percentage(), ' ',   
                   pb.Bar(marker=pb.RotatingMarker(markers='#')), ' ', pb.ETA()]
        self.timer = pb.ProgressBar(widgets=widgets, maxval=self.n_iter).start()

    def update(self, q=1):
        #update timer
        self.timer.update(self.iter)
        self.iter += q

    def finish(self):
        #end timer
        self.timer.finish()
pt = progress_timer(description= 'Progresso das Simulações',n_iter=geracoes*replicacao*ind)'''

#########################################################################################

#Criação das variáveis aleatórias em suas respectivas listas pré-criadas
for x in range(ind):
    desspeeddist[x]=random.choice(list(listdes))
    bxmult[x]=round(random.uniform(1,8),1)
    bxadd[x]=round(random.uniform(1,8),1)
    ax[x]=round(random.uniform(1,4),1)
    sleepdur[x]=round(random.uniform(0,1),1)
    sleepprob[x]=round(random.uniform(0,0.1),3)
    minheadw[x]=round(random.uniform(0.5,3),1)
    safedist[x]=round(random.uniform(0.2,0.8),1)
    #upperbound[x]=round(random.uniform(50,70),1)'''
    
#Agregação das listas das variáveis aleatórias em DataFrame
df_inputs=pd.DataFrame({'ax':ax,'bxmult':bxmult,'bxadd':bxadd,'desspeeddist':desspeeddist,'sleepprob':sleepprob,'sleepdur':sleepdur,'minheadw':minheadw,'safedist':safedist})
erro_inicial_superior=500000000000000 #Estabelecendo variaveis que auxiliarao no calculo de erros
erro_inicial_inferior=0
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
erroparcial=[]
v_parcial=[]
v_esperadas = pd.read_csv('v_esperadas.csv', header=0, sep=';') 
matriz_er=range(4)
matriz_v =range(4)
vels=range(16)
ers=range(16)
lista_agregacao=[] #buffl
df_resumido = pd.DataFrame(columns=['G','I','Vel_Media']) #resump (G=geracao, I=individuo)
lista_agregacao_resumido =[] #buffresumol
indivm=0
indivp=0
lista_erro_geracao=range(ind) #listaerger
df_alfa = pd.DataFrame(columns=['G','Erro_Medio']) #alfa
lista_agregacao_alfa =[] #buffalfa
lista_agregacao_ordenados =[] #arrumadosbuffer
lista_erro_parcial=[] #erroparcial
lista_velocidade_parcial=[] #v_parcial
lista_vel_obs = pd.read_csv('v_esperadas.csv', header=0, sep=';') #v_esperadas
print(lista_vel_obs)
lista_storage_velobs=list(range(16))
for coluna in range(4):
    for linha in range(4):
        lista_storage_velobs[coluna*4+linha]=lista_vel_obs['esperada%s' %coluna][linha]
print(lista_storage_velobs)
lista_erros=range(4) #matriz_er
lista_velocidades =range(4) #matriz_v
lista_storage_vel=range(16) #vels
lista_storage_erros=range(16) #ers


def simulacao(bxadd,seed0,ax,delta_seed,rep,bxmult,g,i,desspeeddist,sleepdur,sleepprob,minhdwy,safdist): #Estabelecendo uma funcao para a simulacao
    #Inputs: a=bxadd, b=Semente inicial, c=Ax, d=Incremento da semente, e=Numero de replicacoes por individuo, f=bxmult, g = geracao, i= tag do individuo, h=desspeeddist, j=duraçãodosleep, k=probabilidade de sleep
    #Outputs: listadel e listavel com valores do delay e velocidade media dessa simulacao+Escreve no arquivo csv ou valores de cada semente
    for l in range(replicacao):
        #Vissim.Net.PriorityRules[0].ConflictMarkers[0].SetAttValue("MinGapTime", a)
        #print("Seed definida:{}".format(b))
        
        #Definindo Parâmetros Específicos de simulação
        
        Vissim.Simulation.SetAttValue('RandSeed', seed0)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('W74ax',ax)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('W74bxAdd', bxadd)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('W74bxMult', bxmult)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('SleepDur', sleepdur)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('SleepProb', sleepprob)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('MinHdwy', minhdwy)
        Vissim.Net.DrivingBehaviors[0].SetAttValue('SafDistFactLnChg', safdist)     
        #Vissim.Net.DrivingBehaviors[0].SetAttValue('W74bxMult', f)
        #----------------------------------------------------------------
        End_of_simulation = 3900 # simulation second [s] #Define a duração da simulação completa em segundos        
        Vissim.Simulation.SetAttValue('SimPeriod', End_of_simulation)
        Vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
        Vissim.SuspendUpdateGUI();
        #Definindo as configurações de velocidade para cada classe de veículo (Veh_composition_number)
        Veh_composition_number = 2 
        Rel_Flows = Vissim.Net.VehicleCompositions.ItemByKey(Veh_composition_number).VehCompRelFlows.GetAll()
        Rel_Flows[0].SetAttValue('DesSpeedDistr',desspeeddist) # Changing the desired speed distribution
        Veh_composition_number = 2
        Rel_Flows = Vissim.Net.VehicleCompositions.ItemByKey(Veh_composition_number).VehCompRelFlows.GetAll()
        Rel_Flows[1].SetAttValue('DesSpeedDistr',desspeeddist) # Changing the desired speed distribution
        Veh_composition_number = 3
        Rel_Flows = Vissim.Net.VehicleCompositions.ItemByKey(Veh_composition_number).VehCompRelFlows.GetAll()
        Rel_Flows[0].SetAttValue('DesSpeedDistr',desspeeddist) # Changing the desired speed distribution
        #----------------------------------------------------------------
        
        Vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode",1) #Ativando Quick Mode
        Vissim.Simulation.RunContinuous() #Iniciando Simulação
        
        #Loop para fazer medições de velocidade(vn),tempo (TTn) e distancia(Dist) para um intervalo de tempo (segundo argumento de TravTm)
        #Atentar que cada loop percorre um Travel Time collector por vez
        for tt in range(4):
            Veh_TT_measurement_number = (tt+1)
            Veh_TT_measurement = Vissim.Net.VehicleTravelTimeMeasurements.ItemByKey(Veh_TT_measurement_number)
            
            TT1= Veh_TT_measurement.AttValue('TravTm(Current,1,All)')
            TT2= Veh_TT_measurement.AttValue('TravTm(Current,2,All)')
            TT3= Veh_TT_measurement.AttValue('TravTm(Current,3,All)')
            TT4= Veh_TT_measurement.AttValue('TravTm(Current,4,All)')
            print([TT1,TT2,TT3,TT4])
            Dist= Veh_TT_measurement.AttValue('Dist') #Distancia de um travel time collector
            #print(Dist)
            
            v1=Dist/TT1 #Velocidade média dos veículos no primeiro intervalo de tempo 
            v2=Dist/TT2
            v3=Dist/TT3
            v4=Dist/TT4
            vtemp=(v1+v2+v3+v4)/4 #Velocidade média dos veículos no trecho considerado (média dos 4 intervalos de tempo)
            
            #Erro relativo ao encontrado em campo, em função do intervalo de tempo e conforme planilha v_esperadas.csv
            er1 = (abs(lista_vel_obs['esperada%s' %tt][0]-v1))/v1 
            er2 = (abs(lista_vel_obs['esperada%s' %tt][1]-v2))/v2
            er3 = (abs(lista_vel_obs['esperada%s' %tt][2]-v3))/v3
            er4 = (abs(lista_vel_obs['esperada%s' %tt][3]-v4))/v4
            #-----------------------------------------------------

            lista_erros[tt] = (er1+er2+er3+er4)/4 #Inxerto da média dos erros na matriz matriz_er
            lista_velocidades[tt] = vtemp #Inxerto da média das velocidades médias na matriz matriz_v 

            #Inxerto das velocidades de cada trecho em uma lista para posterior alocação no DataFrame "temp"
            lista_storage_vel[tt*4]=v1
            lista_storage_vel[tt*4+1]=v2
            lista_storage_vel[tt*4+2]=v3
            lista_storage_vel[tt*4+3]=v4
            #----------------------------------------------------
            
            #Inxerto dos erros de cada trecho em uma lista para posterior alocação no DataFrame "temp"
            lista_storage_erros[tt*4]=er1
            lista_storage_erros[tt*4+1]=er2
            lista_storage_erros[tt*4+2]=er3
            lista_storage_erros[tt*4+3]=er4
            #---------------------------------------------------
            
            #Inxerto da média dos erros médios de cada trecho, junto com a média das velocidades médias
            
            if tt == 3: 
                er=(lista_erros[0]+lista_erros[1]+lista_erros[2]+lista_erros[3])/4 #vai para o dataframe                
                v = (lista_velocidades[0]+lista_velocidades[1]+lista_velocidades[2]+lista_velocidades[3])/4 #vai para o dataframe
                listaer[l]=er #vai para o cálculo da próxima geração
                listavel[l]=v  #vai para o cálculo da próxima geração
            #---------------------------------------------------
            
        print('geracao %.1f, individuo %.1f, replicacao %.1f' % (g,i,l))
        
        #Tranferência dos dados para um dataframe e posterior impressão na Dados_raw.csv
        temp = pd.DataFrame([[(g+1),(i+1),(l+1),seed0,ax,bxadd,bxmult,desspeeddist,sleepdur,sleepprob,minhdwy,safdist,v,er,
                              lista_storage_erros[0],lista_storage_erros[1],
                              lista_storage_erros[2],lista_storage_erros[3],lista_storage_erros[4],lista_storage_erros[5],
                              lista_storage_erros[6],lista_storage_erros[7],lista_storage_erros[8],lista_storage_erros[9],
                              lista_storage_erros[10],lista_storage_erros[11],lista_storage_erros[12],lista_storage_erros[13],
                              lista_storage_erros[14],lista_storage_erros[15],lista_storage_velobs[0],lista_storage_velobs[1],
                              lista_storage_velobs[2],lista_storage_velobs[3],lista_storage_velobs[4],lista_storage_velobs[5],
                              lista_storage_velobs[6],lista_storage_velobs[7],lista_storage_velobs[8],lista_storage_velobs[9],
                              lista_storage_velobs[10],lista_storage_velobs[11],lista_storage_velobs[12],lista_storage_velobs[13],
                              lista_storage_velobs[14],lista_storage_velobs[15],lista_storage_vel[0],lista_storage_vel[1],
                              lista_storage_vel[2],lista_storage_vel[3],lista_storage_vel[4],lista_storage_vel[5],
                              lista_storage_vel[6],lista_storage_vel[7],lista_storage_vel[8],lista_storage_vel[9],
                              lista_storage_vel[10],lista_storage_vel[11],lista_storage_vel[12],lista_storage_vel[13],
                              lista_storage_vel[14],lista_storage_vel[15]]], 
                              columns = ['G','Ind','replicacao', 'Semente', 'ax', 'bxadd','bxmult',
                              'desspeeddist','SleepDur','SleepProb','MinHeadway','SafeDistFactLnChg',
                              'Vel_Ind.(??)','ErroTotal','ErroT1','ErroT2','ErroT3','ErroT4','ErroT5',
                              'ErroT6','ErroT7','ErroT8','ErroT9','ErroT10','ErroT11','ErroT12','ErroT13','ErroT14','ErroT15',
                              'ErroT16','V_obs1','V_obs2','V_obs3','V_obs4','V_obs5','V_obs6','V_obs7','V_obs8','V_obs9',
                              'V_obs10','V_obs11','V_obs12','V_obs13','V_obs14','V_obs15','V_obs16','V1','V2','V3','V4','V5',
                              'V6','V7','V8','V9','V10','V11','V12','V13','V14','V15','V16'])
        lista_agregacao.append(temp)
        seed0+=delta_seed      
        appended_data = pd.concat(lista_agregacao,ignore_index = True)
        appended_data.to_csv('Dados_raw_%s.csv' %hoje,sep=';',float_format='%.3f') 
        #-------------------------------------------------------
        
        #No último indivíduo, é organizado os erros em ordem decrescente e impresso o dataframe para Dados_Ordenados.csv       
        if i == (ind-1):
            temp1 = appended_data[appended_data['G']== g]
            arrumados = temp1.sort(columns='ErroTotal', ascending = True)
            #print(arrumados)
            lista_agregacao_ordenados.append(arrumados)
       #print(arrumadosbuffer)
      
        if g == (geracoes-1):
            appended_arrumados = pd.concat(lista_agregacao_ordenados,ignore_index = True)
            appended_arrumados.to_csv('Dados_Ordenados_%s.csv' % hoje,sep=';',float_format='%.3f')
        #-------------------------------------------------------
        
'''       pt.update()
pt.finish()    '''
global A    

#Loop que chamará a função "simulação" e encontrará os alfas e os predados da primeira geração
for i in range(ind):
    #Definição das listas de velocidade, erros e delay
    listavel=range(replicacao)
    listadel=range(replicacao)
    listaer=range(replicacao)
    Random_Seed=seed
    
    simulacao(df_inputs['bxadd'][i],seed,df_inputs['ax'][i],delta,replicacao,df_inputs['bxmult'][i],0,i,int(df_inputs['desspeeddist'][i]),df_inputs['sleepdur'][i],
              df_inputs['sleepprob'][i],df_inputs['minheadw'][i],df_inputs['safedist'][i])
    print(listavel)
    print(listaer)
    #matriz matvd e matvd1 criada com os dados de velocidade fornecidos pela função na listavel e listaer    
    df_velocidades=pd.DataFrame({'Vel':listavel}) #matvd
    df_erros=pd.DataFrame({'er':listaer}) #matvd1
    print(df_velocidades)
    print(df_erros)
    #-----------------------------------------------------------
    
    #print(matvd)
    #velmedia e ermedia calculados como a média das colunas de 'Vel' e 'er' das matvd e matvd1
    velocidades_medias=pd.DataFrame.mean(df_velocidades)['Vel'] #velmedia
    erros_medios=pd.DataFrame.mean(df_erros)['er'] #ermedia
    #----------------------------------------------------------

    lista_erro_geracao[i]=erros_medios    #Criação da lista de erros por geração para fins de seleção

    Random_Seed+=delta
    #mape=(velmedia-velesp)/velmedia
    
    #print(velmedia)
    #definindo os melhores e piores individuos, baseados nos valores iniciais de erro
    if (abs(erro_inicial_superior))>erros_medios:
        erro_inicial_superior=erros_medios
        vmelhor=velocidades_medias
        indivm=i
        A = erro_inicial_superior
        
    if erros_medios>(abs(erro_inicial_inferior)):
        erro_inicial_inferior=erros_medios
        vpior=velocidades_medias
        indivp=i
        
    #exportando os dados no dataframe    
    temp = pd.DataFrame([[0,i,df_inputs['ax'][i],df_inputs['bxadd'][i],df_inputs['bxmult'][i],int(df_inputs['desspeeddist'][i]),df_inputs['sleepdur'][i],
              df_inputs['sleepprob'][i],df_inputs['minheadw'][i],df_inputs['safedist'][i],velocidades_medias,erros_medios]],columns=['Geracao','Individuo','ax', 'bxadd','bxmult',
                              'desspeeddist','SleepDur','SleepProb','MinHeadway','SafeDistFactLnChg','Vel_Media(??)','Erro'])
    lista_agregacao_resumido.append(temp)
    
tempalfa = pd.DataFrame([[0,A]],columns=['Geracao','ErroM'])
lista_agregacao_alfa.append(tempalfa)
alfas = pd.concat(lista_agregacao_alfa,ignore_index=True)
aresumo = pd.concat(lista_agregacao_resumido,ignore_index=True)
#-----------------------------------------------



#print(aresumo)    
#    dados.write('Velocidade Media; %f\n' % (velmedia)) #Escrevendo os valores medios no arquivo csv
#    dados.write('Delay Medio; %f\n' % (delmedia))
#    
#dados.write('O melhor individuo dessa populacao foi o individuo numero %.0f com velocidade de %.2f e delay de %.2f;\n' % (indivm, vmelhor, dmelhor))
#dados.write('O pior individuo dessa populacao foi o individuo numero  %.0f com velocidade de %.2f e delay de %.2f;\n' % (indivp, vpior, dpior))
#print(mape)



#Loop que definirá o melhor e o pior indivíduo das gerações subsequentes

for geracao in range(geracoes-1):
    if abs(erro_inicial_superior)*100 < 10: #encerra o código se o erro for menor que 10%
        break
    
    #Reestabelecendo os erros maximos e minimos para a filtragem dessa geracao
    erro_inicial_superior=500000000000000 
    erro_inicial_inferior=0
    #---------------------------------------------
    
    l=range(len(lista_erro_geracao))
    #print(l)
    
    #Cria duplicata da lista_erro_geracao para auxiliar no loop de filtragem dos maiores erros
    
    for erro in range(len(l)):
        l[erro]=lista_erro_geracao[erro]
    #print(l)
    #--------------------------------------------
    
    #Organizando a lista de erros do maior para o menor
    lista_erro_geracao.sort(reverse=True)
    lista_erro_checagem_maiores=lista_erro_geracao[0:int(ind*0.2)] #checagem
    lista_erro_maiores=range(int((ind*0.2))) #listaindic
    #--------------------------------------------
    
    #Separa os maiores erros numa lista_erro_maiores 
    for erro in range(int((ind*0.2))):
        for indice in range(len(lista_erro_geracao)):
            if lista_erro_checagem_maiores[erro]==l[indice]:
                lista_erro_maiores[erro]=indice
    #-------------------------------------------- 

    '''if float(r)/15 == int(r/15):
        Vissim = None
        Vissim = com.Dispatch("Vissim.Vissim") #Abrindo o Vissim
        print("Vissim aberto")
        Path_of_COM_Basic_Commands_network = os.getcwd() #Formando o caminho de abertura
        EXEMPLOP = os.path.join(Path_of_COM_Basic_Commands_network, 'PontesVieira_atual.inpx')#a mulher do sapo ficou estranha, checar RedeSD
        flag = False 
        Vissim.LoadNet(EXEMPLOP, flag)    '''
        
    #Verificação de quando ocorre a "diversidade"
    
    if float((geracao+1))/divers != int((geracao+1)/divers):
        
        #Loop que percorre todos os indivíduos da geração onde ocorre diversidade
        for q in range(ind): 
        #Condições da diversidade: se o indivíduo não for alfa, há 50% de chance de um novo aleatório ser posto no seu lugar, mudando seus atributos
            if q!=indivm:
                if random.random()<.5:
                    df_inputs['ax'][q]=df_inputs['ax'][indivm]
                if random.random()<.5:
                    df_inputs['bxmult'][q]=df_inputs['bxmult'][indivm]
                if random.random()<.5:
                    df_inputs['bxadd'][q]=df_inputs['bxadd'][indivm]
                if random.random()<.5:
                    df_inputs['desspeeddist'][q]=df_inputs['desspeeddist'][indivm]
                if random.random()<.5:
                    df_inputs['sleepprob'][q]=df_inputs['sleepprob'][indivm] 
                if random.random()<.5:
                    df_inputs['sleepdur'][q]=df_inputs['sleepdur'][indivm]
                if random.random()<.5:
                    df_inputs['minheadw'][q]=df_inputs['minheadw'][indivm] 
                if random.random()<.5:
                    df_inputs['safedist'][q]=df_inputs['safedist'][indivm] 
        #-------------------------------------------------
        
    #Condição para casos onde não ocorre "diversidade"
    else:
        for q in range(ind): 
            
            
            if q!=indivm:
                #Se o indivíduo não for alfa e estiver na lista dos maiores erros, será "predado": substituido por outro aleatório
                if q in lista_erro_maiores:
                    df_inputs['bxmult'][q]=round(random.uniform(1,8),1)
                    df_inputs['bxadd'][q]=round(random.uniform(1,8),1)
                    df_inputs['ax'][q]=round(random.uniform(1,4),1)
                    df_inputs['desspeeddist'][q]=random.choice(listdes)#meme choose
                    df_inputs['sleepdur'][q]=round(random.uniform(0,1),1)
                    df_inputs['sleepprob'][q]=round(random.uniform(0,0.1),3)
                    df_inputs['minheadw'][q]=round(random.uniform(0.5,3),1)
                    df_inputs['safedist'][q]=round(random.uniform(0.2,0.8),1)
               
                    #Se o indivíduo não for alfa e não estiver na lista dos maiores erros, terá 50% de chance de se "reproduzir" com o alfa,
                    #ou seja, copiar seus genes de alfa
                else:
                    if random.random()<.5:
                        df_inputs['ax'][q]=df_inputs['ax'][indivm]
                    if random.random()<.5:
                        df_inputs['bxmult'][q]=df_inputs['bxmult'][indivm]
                    if random.random()<.5:
                        df_inputs['bxadd'][q]=df_inputs['bxadd'][indivm]
                    if random.random()<.5:
                        df_inputs['desspeeddist'][q]=df_inputs['desspeeddist'][indivm]
                    if random.random()<.5:
                        df_inputs['sleepprob'][q]=df_inputs['sleepprob'][indivm] 
                    if random.random()<.5:
                        df_inputs['sleepdur'][q]=df_inputs['sleepdur'][indivm]
                    if random.random()<.5:
                        df_inputs['minheadw'][q]=df_inputs['minheadw'][indivm] 
                    if random.random()<.5:
                        df_inputs['safedist'][q]=df_inputs['safedist'][indivm]
            
            #Aparentemente, refaz o que o "else" anterior faz, com 20% de chance de receber genes aleatórios
            if random.random()<.2 and q!=indivm:
                df_inputs['ax'][q]=round(random.uniform(1,4),1)
            if random.random()<.2 and q!=indivm:
                df_inputs['bxadd'][q]=round(random.uniform(1,8),1)
            if random.random()<.2 and q!=indivm:
                df_inputs['bxmult'][q]=round(random.uniform(1,8),1)
            if random.random()<.2 and q!=indivm:
                df_inputs['desspeeddist'][q]=random.choice(listdes)
            if random.random()<.2 and q!=indivm:
                df_inputs['sleepdur'][q]=round(random.uniform(0,1),1)
            if random.random()<.2 and q!=indivm:
                df_inputs['sleepprob'][q]=round(random.uniform(0,0.1),3)
            if random.random()<.2 and q!=indivm:
                df_inputs['minheadw'][q]=round(random.uniform(0.5,3),1)
            if random.random()<.2 and q!=indivm:
                df_inputs['safedist'][q]=round(random.uniform(0.2,0.8),1)
                
    #Percorre os indivíduos criados e chama a função "simulação" para obter os novos resultados           
    for j in range(ind): 
        listavel={}
        simulacao(df_inputs['bxadd'][j],seed,df_inputs['ax'][j],delta,replicacao,df_inputs['bxmult'][j],geracao+1,j,int(df_inputs['desspeeddist'][j]),df_inputs['sleepdur'][j],
                  df_inputs['sleepprob'][j],df_inputs['minheadw'][j],df_inputs['safedist'][j])
        df_velocidades=pd.DataFrame({'Vel':listavel})
        velocidades_medias=pd.DataFrame.mean(df_velocidades)['Vel']
        df_erros=pd.DataFrame({'er':listaer})
        erros_medios=pd.DataFrame.mean(df_erros)['er']
        lista_erro_geracao[i]=erros_medios

        #mape=(velmedia-velesp)/velmedia
        #print(velmedia)
        if (abs(erro_inicial_superior))>erros_medios:
            erro_inicial_superior=erros_medios
            vmelhor=velocidades_medias
            indivm=j
            A = erro_inicial_superior
        if erros_medios>(abs(erro_inicial_inferior)):
            erro_inicial_inferior=erros_medios
            vpior=velocidades_medias
            indivp=j 
        temp = pd.DataFrame([[geracao+1,j,df_inputs['ax'][j],df_inputs['bxadd'][j],df_inputs['bxmult'][j],int(df_inputs['desspeeddist'][j]),df_inputs['sleepdur'][j],
                  df_inputs['sleepprob'][j],df_inputs['minheadw'][j],df_inputs['safedist'][j],velocidades_medias,erros_medios]],columns=['Geracao','Individuo','ax', 'bxadd','bxmult',
                              'desspeeddist','SleepDur','SleepProb','MinHeadway','SafeDistFactLnChg','Vel_Media(??)','Erro'])
        lista_agregacao_resumido.append(temp)
        
    tempalfa = pd.DataFrame([[geracao+1,A]],columns=['Geracao','ErroM'])
    lista_agregacao_alfa.append(tempalfa)
    alfas = pd.concat(lista_agregacao_alfa,ignore_index=True)
    aresumo = pd.concat(lista_agregacao_resumido,ignore_index = True)
    aresumo.to_csv('Dados_light_%s.csv' % hoje ,sep=';',float_format='%.8f')
    alfas.to_csv('Dados_Alfas_%s.csv' % hoje,sep=';',float_format='%.8f')    
    
sheet_name = 'GraficodosAlfasPV'
writer     = pd.ExcelWriter('Progressao_dos_Alfas_%s.xlsx' % hoje, engine='xlsxwriter')
alfas.to_excel(writer, sheet_name=sheet_name)
workbook  = writer.book
worksheet = writer.sheets[sheet_name]
chart = workbook.add_chart({'type': 'scatter'})
ln=len(alfas['Geracao'])
chart.add_series({
        'categories': ['GraficodosAlfasPV', 1, 1, ln, 1],
        'values':     ['GraficodosAlfasPV', 1, 2, ln, 2],
        'line':       {'width': 1.00},

    })
chart.set_x_axis({'name': 'Geracao', 'date_axis': False})
chart.set_y_axis({'name': 'Erro', 'major_gridlines': {'visible': False}})
worksheet.insert_chart('H2', chart)
writer.save()
Vissim = None
print(time.time()-start_time)
print("C'est fini")
