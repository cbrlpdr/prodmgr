class Setor:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.prodAtual = 0

class Funcionario:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

class Tarefa:
    def __init__(self, func, setor, prod):
        self.func = int(func)
        self.setor = int(setor)
        self.prod = int(prod)

class Banco:
    def __init__(self, file):
        self.file = file
    
    
    def getRows(self, table):
        rows = []
        path=self.file+"/"+table+".txt"
        f = open(path,'r')
        
        for line in f:
            if(not line.startswith('#')):
                lineSplit = line.split(',')
                if(table=="setor"):
                    obj = Setor(lineSplit[0],lineSplit[1])
                elif(table=="funcionario"):
                    obj = Funcionario(lineSplit[0],lineSplit[1])
                elif(table=="tarefa"):
                    obj = Tarefa(lineSplit[0],lineSplit[1],lineSplit[2])
                else:
                    print("ERROR: TABLE NOT FOUND")
                rows.append(obj)
        return rows

def returnProd(func,setor,tarefas):
    for row in tarefas:
        if (row.func==func and row.setor==setor):
            return row.prod
    return -1

def measureProductivity(timestamp, maxTime, cromossomo, tarefas, setores):
    currentTime=timestamp
    ind=0

    listProdL=[0,0,0,0]
    listProdM=[0,0,0,0]
    listProdE=[0,0,0,0]
    qtde=[0,0,0,0]

    
    
    for i in range(len(cromossomo)):
        gene=cromossomo[i]
        for j in range(len(gene)):
            if(gene[j]==1):
                listProdL[j]+=returnProd(i+1,gene[j],tarefas)
            elif (gene[j]==2):
                listProdM[j]+=returnProd(i+1,gene[j],tarefas)
            elif gene[j]==3:
                listProdE[j]+=returnProd(i+1,gene[j],tarefas)
            

    while(currentTime<=maxTime):
        #Processo de troca de setor
        prodLimpeza = listProdL[ind]
        prodMontagem = listProdM[ind]
        prodEmbalagem = listProdE[ind]
        
        #Processo de envio (de um setor para o outro)

        qtde[0]+=prodLimpeza

        if(qtde[1]>=prodEmbalagem):
            qtde[1]-=prodEmbalagem
            qtde[2]+=prodEmbalagem
        else:
            qtde[2]+=qtde[1]
            qtde[1]=0

        if(qtde[0]>=prodMontagem):
            qtde[0]-=prodMontagem
            qtde[1]+=prodMontagem
        else:
            qtde[1]+=qtde[0]
            qtde[0]=prodLimpeza

        print("currentTime: "+str(currentTime)+" min, faltam "+str(maxTime-currentTime)+" min!")
        print("   - Limpeza produz "+str(prodLimpeza)+", tem "+str(qtde[0]))
        print("   - Montagem produz "+str(prodMontagem)+", tem "+str(qtde[1]))
        print("   - Embalagem produz "+str(prodEmbalagem)+", tem "+str(qtde[2]))

        currentTime+=timestamp
        ind+=1

        input()
    print("ACABOU PORRA VAI PRA CASA >:(")
    return qtde[3]

#-----------------------------------------------------------
timestamp=10
maxTime=40
currentTime=0

banco = Banco("db")
setores = banco.getRows("setor")
funcionario = banco.getRows("funcionario")
tarefas = banco.getRows("tarefa")
crom1=[[1,2,2,3], [1,1,3,3], [1,2,3,3]]
crom2=[[1,2,2,3], [1,2,2,3], [1,2,2,3]]
measureProductivity(timestamp,maxTime,crom2,tarefas,setores)
print(setores[0].prodAtual)



