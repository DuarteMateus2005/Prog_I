def novaPartida(n):
    if isinstance(n,int) and n>4 and n<27:
        return (n,())
    return (26,())

def eFim(partida):
    dim = partida[0]
    jogadas = partida[1]
    if len(jogadas) > 0 and ((jogadas[-1][0] == 0 and jogadas[-1][1] == 0) or (jogadas[-1][0] == dim-1 and jogadas[-1][1] == dim-1)):
        return True
    return False

def eValida(partida,jogada):
    dim = partida[0]
    if not isinstance(jogada,tuple) or len(jogada)!=2 or not isinstance(jogada[0],int) or not isinstance(jogada[1],int) or eFim(partida):
        return False
    elif jogada[0]>=dim or jogada[1]>=dim or jogada[0]<0 or jogada[1]<0:
        return False
    elif len(partida[1])==0:
        #if (jogada[0]==0 and jogada[1]==0) or (jogada[0]==dim-1 and jogada[1]==dim-1):
        #    return False #Não se aceita ganhar logo o jogo
        return True
    elif abs(partida[1][-1][0]-jogada[0])>1 or abs(partida[1][-1][1]-jogada[1])>1:
        return False
    elif jogada in partida[1]:
        return False
    else:
        return True
    
def fazerJogada(partida,jogada):
    if eValida(partida,jogada):
        return (partida[0],partida[1]+(jogada,))
    return (partida[0],partida[1])

def vencedor(partida):
    if eFim(partida):
        jogadas = partida[1]
        if jogadas[-1][0] == 0:
            return 1
        else:
            return 2
    return 0
        
def proximasJogadas(partida):
    res = []
    dim =partida[0]
    if len(partida[1]) == 0:
        for n in range(dim):
            for i in range(dim):
                #if not((n==0 and i==0) or (n==dim-1 and i==dim-1)):
                res = res + [(n,i)]
        return res
    elif eFim(partida):
        return res
    else:
        ultimaJogada = partida[1][-1]
        for n in range(-1,2):
            for i in range(-1,2):
                potencialJogada = (ultimaJogada[0]+n,ultimaJogada[1]+i)
                if eValida(partida,potencialJogada):
                    res = res + [potencialJogada]
    return res

def imprimir(partida):
    def tabuleiroInicial(n):
        return [[0 for _ in range(n)] for _ in range(n)]
    def descod(n):
        if n == 0:
            return '.'
        elif n==1:
            return '#'
        else:
            return 'O'
    def construirTabuleiro(partida):
        dim = partida[0]
        jogadas = partida[1]
        t = tabuleiroInicial(dim)
        for n in range(len(jogadas)):
            if n == len(jogadas)-1:
                t[jogadas[n][0]][jogadas[n][1]] = 2
            else:
                t[jogadas[n][0]][jogadas[n][1]] = 1
        return t
    t = construirTabuleiro(partida)
    res = ''
    for n in range(partida[0],0,-1):
        if n >= 10:
            res = res + f"{n}│"
        else:
           res = res + f" {n}│" 
        for i in range(partida[0]):
            if n == partida[0] and i == partida[0]-1 and t[n-1][i] == 0:
                res += '2'
            elif n == 1 and i == 0 and t[0][0] == 0:
                res += '1'
            else:
                res += descod(t[n-1][i])
            if i < partida[0]-1:
                res+= ' '
        res += '\n'
    res += '  └'
    for _ in range(2*partida[0]-1):
        res += '─'
    res += '\n'
    res += '   '
    for n in range(97, 97 + partida[0]):
        res+= chr(n)
        if n < 96 + partida[0]:
            res+= ' '
    res += '\n'
    return res

def imprimirLances(partida):
    res = ''
    nJogadas = len(partida[1])-1
    nLinhas = min(10,nJogadas)+1
    for n in range(1,nLinhas):
        jogadaImprimir = n
        while jogadaImprimir <= nJogadas:
            if jogadaImprimir>=10 and jogadaImprimir<100:
                res+=' '
            elif jogadaImprimir<10:
                res+='  '
            res+=f'{jogadaImprimir}. '
            res+= chr(97+partida[1][jogadaImprimir][1])
            if partida[1][jogadaImprimir][0]+1 <10:    
                res+= f'{partida[1][jogadaImprimir][0]+1} '
            else:
                res+= f'{partida[1][jogadaImprimir][0]+1}'
            jogadaImprimir+=10
            if(jogadaImprimir <= nJogadas):
                res+=' '
        res+='\n'
    return res

partida = novaPartida(25)
jogadas = [(1,i) for i in range(23)] +[(2,22)] + [(2,21-i) for i in range(21)]+[(3,0)]+[(3,i) for i in range(1,21)]+[(i,20) for i in range(4,25)]
jogadas+=[(24,19)]+[(24-i,19) for i in range(1,20)]