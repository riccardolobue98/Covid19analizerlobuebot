# Covid19analizerbot
codice python  bot covid19 telegram 

Questo bot analizza dati inerenti alla diffusione del Covid-19 in tutta Italia mostrando l'andamento della diffusione del virus nel nostro paese.
All’interno vi è anche un sentiment analyzer che sulla console dell’editor permette di scegliere il tag della ricerca e su quanti tweet fare questa analisi.

I dati vengono aggiornati ogni giorno da questa pagina GitHub : https://github.com/pcm-dpc/COVID-19

Puoi trovare il codice relativo al bot qua: 
https://github.com/riccardolobue98/Covid19analizerbot

Il codice da me fornito  analizza vari file ricorrenti alla data del 16 giugno 2020 qualora si volesse utilizzare il file aggiornato scaricato dalla pagina github , https://github.com/pcm-dpc/COVID-19  ,basterà soltanto andar a sostituire all'interno dei file csv tramite il programma Excel come nominativo di regione al posto di “Valle d'Aosta” andiamo a sostituire con la seguente dicitura “Aosta”; questo  per un problema al relativo agli apici o in questo caso all'apice tra “d” e “Aosta”(A tutti gli altri dati non serve apportare modifiche).

Si raccomanda di utilizzare i file completi es.(dpc-covid19-ita-andamento-nazionale per l’andamento) nel quale sono raccolti tutti i dati inerenti al covid dal 24 febbraio fino ad oggi e non con date specifiche es.(dpc-covid19-ita-andamento-nazionale-20200224) poichè verrebbe visualizzata nel grafico e nella console soltanto una feature relativa a quel giorno con il suo relativo valore.

Per quanto riguarda i file doc convertiti da file PDF qualora si volessero utilizzare gli ultimi  file recentemente caricati sulla pagina github,nella sezione schede-riepilogative,  https://github.com/pcm-dpc/COVID-19  ,Basterà soltanto utilizzare un qualsiasi unitore e convertitore da PDF a DOCX  ed inserire il seguente file nella cartella del progetto sostituendo quindi il file DOCX  già esistente.

Ultimo punto da chiarire  , i grafici.png che vengono salvati nella cartella e inviati al bot per essere visualizzati dall'utente non essendo interattivi come quando ci vengono plottati dal codice sorgente mandandolo in run, nei png mostreranno tutte le date impasticciate tra di loro poichè sono tantissime, questo dato dalla numerosa quantità di feature plottate, ma qualora si volesse vedere piu' correttamente il grafico basterà visualizzare quello plottato dal codice sorgente sul quale potrete sbizzarrirvi nello zoommare sui vari muntini che simboleggiano il numero di positivi,guariti,deceduti,ecc... (ovviamente in base al grafico) , in quella precisa data.

Con questo vi ringrazio per aver visionato il mio progetto.

GRLB
Matricola 283101
 
