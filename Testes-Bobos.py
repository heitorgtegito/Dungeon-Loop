Atributos = {}
#  Level up = 10 atributos p/nivel
# Minimo em cada range de fase - 0-250, 250-500, 500-750, 750-1000 
Forca = 100
Destreza = 100
Constituição = 100
Sorte = 100

Atributos.update({'Força': Forca, 'Destreza': Destreza, 'Constituição': Constituição, 'Sorte': Sorte})

print(Atributos)

Forca = Forca/20
Destreza = Destreza/20
Constituição = Constituição/20
Sorte = Sorte/20
Atributos.update({'Força': Forca, 'Destreza': Destreza, 'Constituição': Constituição, 'Sorte': Sorte})

print(Atributos)

Armadura = 'Pesada'

Vida = 10 + Constituição
Vida_Atual = Vida
if Armadura == 'Leve':
    Defesa = 2 + round(Constituição/20)
elif Armadura == 'Pesada':
    Defesa = 5 + round(Constituição/15)
Defesa_Atual = Defesa

Condições = []
if 'Sangramento' in Condições:
    Vida_Atual = Vida_Atual - (Vida_Atual/50)
if 'Envenenamento' in Condições:
    Vida_Atual = Vida_Atual - (Destreza/10)
if 'Debilitado' in Condições:
    Defesa_Atual = Defesa_Atual - (Forca/10)

Status = {
    'Vida': Vida,
    'Defesa': Defesa,
    'Atributos': Atributos
}
print(Status)