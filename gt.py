import sys, os
from googletrans import Translator
from timeit import default_timer as timer

start = timer()
count = 0
TRcount = 0
NOcount = 0
traduzione = []
datradurre = ""
datrad_non = []

translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.it',
    ])

try:
    sourcefile = sys.argv[1]
    resultfile = sys.argv[1].replace('.srt', '')+'_tradotto.srt'
except:
    sourcefile = "sottotitolo.srt"
    resultfile = sourcefile.replace('.srt', '')+'_tradotto.srt'

print ('file sorgente:  '+ sourcefile)
print ('file risultato: '+ resultfile)

if os.path.isfile(resultfile) == True:
    os.remove(resultfile)

with open(sourcefile) as f:
    content = f.readlines()
content = [x.strip() for x in content]

for item in content:

    count += 1
    if item.isdigit() == False:
        try:
            control = item.replace(":","")
            part = control[0:4].isdigit()
        except:
            part = False
        if part != True or item =='1':
            datradurre = datradurre +' '+item
            datrad_non.append(datradurre)
            accio = ("_______"+str(item)+"________________>")
            if accio == "_______________________>":
                try:
                    translations = translator.translate(datradurre, src='en', dest='it')
                    trad = translations.text
                    parole = 0
                    a = trad.split(" ")
                    for i in a:
                        if (i!=" " and i!="<i>" and i!="</" and i!="i>" and i!="-" and i!="..."):
                            parole=parole+1
                    if parole >5 and len(trad) >40:
                        frase = range(6,parole)
                        primariga = str(a[0])+' '+str(a[1])+' '+str(a[2])+' '+str(a[3])+' '+str(a[4])+' '+str(a[5])
                        secondariga = ''
                        for x in frase:
                            secondariga = secondariga+' '+str(a[x])
                        traduzione.append(primariga)
                        traduzione.append(secondariga[1:])
                        traduzione.append(item)
                        TRcount += 1
                    else:
                        traduzione.append(trad)
                        traduzione.append(item)
                        TRcount += 1
                except:
                    for x in datrad_non:
                        traduzione.append(x)
                    traduzione.append(item)
                    NOcount += 1
                datradurre = ""
                datrad_non.clear()
        else:
            print(item)
            traduzione.append(item)
    else:
        traduzione.append(item)

print("Salvataggio file...")
with open(resultfile, 'a') as f:
    for item in traduzione:
        f.write(item+'\n')

end = timer()
tempo = "{0:.2f}".format((end - start))
print('\n')
print('\n')
print ('Totale righe _________ '+str(count))
print ('Totale traduzioni ____ '+str(TRcount))
print ('Problemi traduzioni __ '+str(NOcount))
print ('Totale tempo _________ '+tempo+'s')
print('\n')
