import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import time
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as mpl
import tweepy,csv,re
from textblob import TextBlob






###################################################### SENTIMENT ################################################




class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        # autenticazione
        consumerKey = 'iIkJ52sdYqzSsgJrNR2ZX1RWq'
        consumerSecret = 'YZ9ti7yHsqQFu4EKYx4wCapna3B6HaEjYDpBhNr6PdKMITfMs5'
        accessToken = '2151668340-xcQz8BuA7XdLyRuLfEKVs4fN8D4BwrfDHUjFTWQ'
        accessTokenSecret = '4B0XuPZtpMhXQgOshSUqjeUawI2h49ihl27GUTHum8ON2'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input per il termine o tag da cercare e il numero di tweet da cercare
        searchTerm = input("Inserisci una parola o un tag di riferimento per i tweet ( preferibilmente in inglese ) ==> ")
        NoOfTerms = int(input("Su quanti tweet vuoi basarti ? ==> "))

        # ricerca dei tweet
        self.tweets = tweepy.Cursor(api.search, q=searchTerm).items(NoOfTerms)

        # Apro/creo un file a cui aggiungere i dati
        csvFile = open('Risultati_Sentiment_Twitter.csv', 'a')

        # Uso la scrittura su csv
        csvWriter = csv.writer(csvFile)


        # creazione di alcune variabili per memorizzare informazioni
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0


        # iterazioni attraverso i tweet recuperati
        for tweet in self.tweets:
            #Uso il metodo append . Uso la codifica UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))

            analysis = TextBlob(tweet.text)
            print(analysis.sentiment)  # printo la polarità dei tweet
            polarity += analysis.sentiment.polarity  # sommo le polarità per trovare la media in seguito

            if (analysis.sentiment.polarity == 0):  # aggiungo un valore per ogni reazione delle persone , e userò questi dati quando calcolerò la loro media
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Scrivo su CSV e chiudo il file CSV
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # trovaro la media in base a come reagiscono le persone
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # trovare la reazione media
        polarity = polarity / NoOfTerms

        # stampo i dati
        print("Le persone hanno reagito in questo modo al " + searchTerm + " analizzando gli ultimi " + str(NoOfTerms) + " tweet !")
        print()
        print("I dati calcolati sono risultati principalmente : ")

        #condizioni inerenti alla polaritò
        if (polarity == 0):
            print("Neutrali")
        elif (polarity > 0 and polarity <= 0.3):
            print("Poco positivo")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positivo")
        elif (polarity > 0.6 and polarity <= 1):
            print("Molto positivo")
        elif (polarity > -0.3 and polarity <= 0):
            print("Poco negativo")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negativo")
        elif (polarity > -1 and polarity <= -0.6):
            print("Molto negativo")

        print()
        print("Le percentuali nel dettaglio: ")
        print(str(positive) + "% la gente pensa sia una cosa positiva")
        print(str(wpositive) + "% la gente pensa sia una cosa poco positiva")
        print(str(spositive) + "% la gente pensa sia una cosa molto positiva")
        print(str(negative) + "% la gente pensa sia una cosa negativa")
        print(str(wnegative) + "% la gente pensa sia una cosa poco negativa")
        print(str(snegative) + "% la gente pensa sia una cosa molto negativa")
        print(str(neutral) + "% la gente che la pensa in modo neutrale")

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


    def cleanTweet(self, tweet):
        # Rimuovo i Link, i caratteri speciali ed altro dai tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # Una funzione che calcola la percentuale per il grafico
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    # Una funzione che usa le percentuali per andare a plottare il grafico a torta con diversi colori
    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positivo [' + str(positive) + '%]', 'Poco positivo [' + str(wpositive) + '%]','Molto positivo [' + str(spositive) + '%]', 'Neutrali [' + str(neutral) + '%]',
                  'Negativo [' + str(negative) + '%]', 'Poco negativo [' + str(wnegative) + '%]', 'Molto negativo [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('Le persone hanno reagito in questo modo al ' + searchTerm + 'analizzando gli ultimi ' + str(noOfSearchTerms) + ' Tweet!')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('grafico_sentiment.png')
        plt.show()




if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()


#################################################################################################################


#-----------------------------------FUNZIONE ANDAMENTO-----------------------------------#

df = pd.read_csv('COVID-19-master\dati-andamento-nazionale\dpc-covid19-ita-andamento-nazionale.csv')#dataframe dome caricare il file csv

print(df.head())


dftotale_positivi = pd.DataFrame(df, columns=['data', 'totale_positivi'])

g1andamento = sns.scatterplot(data=dftotale_positivi, x='data', y='totale_positivi')

plt.savefig('totale_positivi.png')



#plottiamo i dati 
plt.show()


dfdimessi_guariti = pd.DataFrame(df, columns=['data', 'dimessi_guariti'])

g2andamento = sns.scatterplot(data=dfdimessi_guariti, x='data', y='dimessi_guariti')

plt.savefig('dimessi_guariti.png')



plt.show()

dfdeceduti = pd.DataFrame(df, columns=['data', 'deceduti'])

g3andamento = sns.scatterplot(data=dfdeceduti, x='data', y='deceduti')

plt.savefig('deceduti.png')



plt.show()


#-----------------------------------FUNZIONE FORNITURE STATO----------------------------------#

df = pd.read_csv('COVID-19-master\dati-contratti-dpc-forniture\dpc-covid19-dati-contratti-dpc-forniture.csv',  index_col=0, skip_blank_lines=False)#dataframe dome caricare il file csv

print(df.head())

X = df

print(X)

dfforniture = pd.DataFrame(X, columns=['categoria', 'prezzo_unitario', 'quantita', 'data_atto_negoziale'])

print(dfforniture)

csv = dfforniture.to_csv('forniture.txt')
















#-----------------------------------FUNZIONE ADAMENTO REGIONE----------------------------------#

df = pd.read_csv('COVID-19-master\dati-regioni\dpc-covid19-ita-regioni.csv')#dataframe dome caricare il file csv

print(df.head())

dftotale_positivi_regione = pd.DataFrame(df, columns=['data', 'denominazione_regione', 'totale_positivi'])

print(dftotale_positivi_regione)

#################################################### sicilia ###################################################
dfsicilia=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Sicilia')]

print(dfsicilia)

gsicilia = sns.scatterplot(data=dfsicilia, x='data', y='totale_positivi')

plt.savefig('andamento_sicilia.png')

#plottiamo i dati 
plt.show()
#################################################### sardegna ###################################################
dfsardegna=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Sardegna')]

print(dfsardegna)

gsardegna = sns.scatterplot(data=dfsardegna, x='data', y='totale_positivi')

plt.savefig('andamento_sardegna.png')

#plottiamo i dati 
plt.show()
#################################################### calabria ###################################################
dfcalabria=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Calabria')]

print(dfcalabria)

gcalabria = sns.scatterplot(data=dfcalabria, x='data', y='totale_positivi')

plt.savefig('andamento_calabria.png')

#plottiamo i dati 
plt.show()
#################################################### basilicata ###################################################
dfbasilicata=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Basilicata')]

print(dfbasilicata)

gbasilicata = sns.scatterplot(data=dfbasilicata, x='data', y='totale_positivi')

plt.savefig('andamento_basilicata.png')

#plottiamo i dati 
plt.show()
#################################################### campania  ###################################################
dfcampania=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Campania')]

print(dfcampania)

gcampania = sns.scatterplot(data=dfcampania, x='data', y='totale_positivi')

plt.savefig('andamento_campania.png')

#plottiamo i dati 
plt.show()
#################################################### puglia ###################################################
dfpuglia=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Puglia')]

print(dfpuglia)

gpuglia = sns.scatterplot(data=dfpuglia, x='data', y='totale_positivi')

plt.savefig('andamento_puglia.png')

#plottiamo i dati 
plt.show()
#################################################### molise ###################################################
dfmolise=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Molise')]

print(dfmolise)

gmolise = sns.scatterplot(data=dfmolise, x='data', y='totale_positivi')

plt.savefig('andamento_molise.png')

#plottiamo i dati
plt.show()
#################################################### lazio ###################################################
dflazio=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Lazio')]

print(dflazio)

glazio = sns.scatterplot(data=dflazio, x='data', y='totale_positivi')

plt.savefig('andamento_lazio.png')

#plottiamo i dati 
plt.show()
#################################################### abruzzo ###################################################
dfabruzzo=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Abruzzo')]

print(dfabruzzo)

gabruzzo = sns.scatterplot(data=dfabruzzo, x='data', y='totale_positivi')

plt.savefig('andamento_abruzzo.png')

#plottiamo i dati 
plt.show()
#################################################### marche ###################################################
dfmarche=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Marche')]

print(dfmarche)

gmarche = sns.scatterplot(data=dfmarche, x='data', y='totale_positivi')

plt.savefig('andamento_marche.png')

#plottiamo i dati
plt.show()
#################################################### umbria ###################################################
dfumbria=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Umbria')]

print(dfumbria)

gumbria = sns.scatterplot(data=dfumbria, x='data', y='totale_positivi')

plt.savefig('andamento_umbria.png')

#plottiamo i dati 
plt.show()
#################################################### toscana ###################################################
dftoscana=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Toscana')]

print(dftoscana)

gtoscana = sns.scatterplot(data=dftoscana, x='data', y='totale_positivi')

plt.savefig('andamento_toscana.png')

#plottiamo i dati
plt.show()
#################################################### emilia-romagna ###################################################
dfemiliaromagna=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Emilia-Romagna')]

print(dfemiliaromagna)

gemiliaromagna = sns.scatterplot(data=dfemiliaromagna, x='data', y='totale_positivi')

plt.savefig('andamento_emiliaromagna.png')

#plottiamo i dati
plt.show()
#################################################### liguria ###################################################
dfliguria=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Liguria')]

print(dfliguria)

gliguria = sns.scatterplot(data=dfliguria, x='data', y='totale_positivi')

plt.savefig('andamento_liguria.png')

#plottiamo i dati 
plt.show()
#################################################### Piemonte ###################################################
dfPiemonte=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Piemonte')]

print(dfPiemonte)

gPiemonte = sns.scatterplot(data=dfPiemonte, x='data', y='totale_positivi')

plt.savefig('andamento_Piemonte.png')

#plottiamo i dati 
plt.show()
#################################################### valle d'aosta ###################################################
dfvalledaosta=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Aosta')]

print(dfvalledaosta)

gvalledaosta = sns.scatterplot(data=dfvalledaosta, x='data', y='totale_positivi')

plt.savefig('andamento_valledaosta.png')

#plottiamo i dati
plt.show()
#################################################### Lombardia ###################################################
dfLombardia=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Lombardia')]

print(dfLombardia)

gLombardia = sns.scatterplot(data=dfLombardia, x='data', y='totale_positivi')

plt.savefig('andamento_Lombardia.png')

#plottiamo i dati dopo
plt.show()
#################################################### Trentino ###################################################
dfTrento=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Trento')]

print(dfTrento)

gTrento = sns.scatterplot(data=dfTrento, x='data', y='totale_positivi')

plt.savefig('andamento_Trentino.png')

#plottiamo i dati
plt.show()
#################################################### Friuli Venezia Giulia ###################################################
dfFriuli_Venezia_Giulia=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Friuli Venezia Giulia')]

print(dfFriuli_Venezia_Giulia)

gFriuli_Venezia_Giulia= sns.scatterplot(data=dfFriuli_Venezia_Giulia, x='data', y='totale_positivi')

plt.savefig('andamento_Friuli_Venezia_Giulia.png')

#plottiamo i dati 
plt.show()
#################################################### Veneto ###################################################
dfVeneto=dftotale_positivi_regione[dftotale_positivi_regione['denominazione_regione'].str.contains('Veneto')]

print(dfVeneto)

gVeneto = sns.scatterplot(data=dfVeneto, x='data', y='totale_positivi')

plt.savefig('andamento_Veneto.png')

#plottiamo i dati 
plt.show()





















#-----------------------------------FUNZIONE ADAMENTO PROVINCIA----------------------------------#

df = pd.read_csv('COVID-19-master\dati-province\dpc-covid19-ita-province.csv')#dataframe dome caricare il file csv

print(df.head())

dftotale_positivi_province = pd.DataFrame(df, columns=['data', 'denominazione_regione', 'denominazione_provincia', 'totale_casi'])

print(dftotale_positivi_province)

#################################################### sicilia ###################################################
dfsiciliaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Sicilia')]

print(dfsiciliaprovince)

gsiciliaprovince = sns.scatterplot(data=dfsiciliaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_siciliaprovince.png')

#plottiamo i dati 
plt.show()
#################################################### sardegna ###################################################
dfsardegnaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Sardegna')]

print(dfsardegnaprovince)

gsardegnaprovince = sns.scatterplot(data=dfsardegnaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_sardegnaprovince.png')

#plottiamo i dati 
plt.show()
#################################################### calabria ###################################################
dfcalabriaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Calabria')]

print(dfcalabriaprovince)

gcalabriaprovince = sns.scatterplot(data=dfcalabriaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_calabriaprovince.png')

#plottiamo i dati
plt.show()
#################################################### basilicata ###################################################
dfbasilicataprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Basilicata')]

print(dfbasilicataprovince)

gbasilicataprovince = sns.scatterplot(data=dfbasilicataprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_basilicataprovince.png')

#plottiamo i dati 
plt.show()
#################################################### campania  ###################################################
dfcampaniaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Campania')]

print(dfcampaniaprovince)

gcampaniaprovince = sns.scatterplot(data=dfcampaniaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_campaniaprovince.png')

#plottiamo i dati
plt.show()
#################################################### puglia ###################################################
dfpugliaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Puglia')]

print(dfpugliaprovince)

gpugliaprovince = sns.scatterplot(data=dfpugliaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_pugliaprovince.png')

#plottiamo i dati 
plt.show()
#################################################### molise ###################################################
dfmoliseprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Molise')]

print(dfmoliseprovince)

gmoliseprovince = sns.scatterplot(data=dfmoliseprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_moliseprovince.png')

#plottiamo i dati
plt.show()
#################################################### lazio ###################################################
dflazioprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Lazio')]

print(dflazioprovince)

glazioprovince = sns.scatterplot(data=dflazioprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_lazioprovince.png')

#plottiamo i dati
plt.show()
#################################################### abruzzo ###################################################
dfabruzzoprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Abruzzo')]

print(dfabruzzoprovince)

gabruzzoprovince = sns.scatterplot(data=dfabruzzoprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_abruzzoprovince.png')

#plottiamo i dati 
plt.show()
#################################################### marche ###################################################
dfmarcheprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Marche')]

print(dfmarcheprovince)

gmarcheprovince = sns.scatterplot(data=dfmarcheprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_marcheprovince.png')

#plottiamo i dati 
plt.show()
#################################################### umbria ###################################################
dfumbriaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Umbria')]

print(dfumbriaprovince)

gumbriaprovince = sns.scatterplot(data=dfumbriaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_umbriaprovince.png')

#plottiamo i dati 
plt.show()
#################################################### toscana ###################################################
dftoscanaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Toscana')]

print(dftoscanaprovince)

gtoscanaprovince = sns.scatterplot(data=dftoscanaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_toscanaprovince.png')

#plottiamo i dati 
plt.show()
#################################################### emilia-romagna ###################################################
dfemiliaromagnaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Emilia-Romagna')]

print(dfemiliaromagnaprovince)

gemiliaromagnaprovince = sns.scatterplot(data=dfemiliaromagnaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_emiliaromagnaprovince.png')

#plottiamo i dati dopo 
plt.show()
#################################################### liguria ###################################################
dfliguriaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Liguria')]

print(dfliguriaprovince)

gliguriaprovince = sns.scatterplot(data=dfliguriaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_liguriaprovince.png')

#plottiamo i dati dopo 
plt.show()
#################################################### Piemonte ###################################################
dfPiemonteprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Piemonte')]

print(dfPiemonteprovince)

gPiemonteprovince = sns.scatterplot(data=dfPiemonteprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_Piemonteprovince.png')

#plottiamo i dati 
plt.show()
#################################################### valle d'aosta ###################################################
dfvalledaostaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Aosta')]

print(dfvalledaostaprovince)

gvalledaostaprovince = sns.scatterplot(data=dfvalledaostaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_valledaostaprovince.png')

#plottiamo i dati 
plt.show()
#################################################### Lombardia ###################################################
dfLombardiaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Lombardia')]

print(dfLombardiaprovince)

gLombardiaprovince = sns.scatterplot(data=dfLombardiaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_Lombardiaprovince.png')

#plottiamo i dati
plt.show()
#################################################### Trentino ###################################################
dfTrentoprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Trento')]

print(dfTrentoprovince)

gTrentoprovince = sns.scatterplot(data=dfTrentoprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_Trentinoprovince.png')

#plottiamo i dati 
plt.show()
#################################################### Friuli Venezia Giulia ###################################################
dfFriuli_Venezia_Giuliaprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Friuli Venezia Giulia')]

print(dfFriuli_Venezia_Giuliaprovince)

gFriuli_Venezia_Giuliaprovince= sns.scatterplot(data=dfFriuli_Venezia_Giuliaprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_Friuli_Venezia_Giuliaprovince.png')

#plottiamo i dati

plt.show()
#################################################### Veneto ###################################################
dfVenetoprovince=dftotale_positivi_province[dftotale_positivi_province['denominazione_regione'].str.contains('Veneto')]

print(dfVenetoprovince)

gVenetoprovince = sns.scatterplot(data=dfVenetoprovince, x='denominazione_provincia', y='totale_casi')

plt.savefig('andamento_Venetoprovince.png')

#plottiamo i dati 

plt.show()











##########################################################################


TOKEN = "1192422660:AAHL9Q1VVpcajhP_6XKY6Y6_j8dv5mZp9dE" # token bot


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Info', callback_data='info')],
        [InlineKeyboardButton(text='Andamento', callback_data='andamento'),
         InlineKeyboardButton(text='Forniturestato', callback_data='forniturestato')],
        [InlineKeyboardButton(text='Tassorischioregione', callback_data='tassorischioregione')],
        [InlineKeyboardButton(text='Tassorischioprovinci', callback_data='tassorischioprovincia'),
         InlineKeyboardButton(text='Pdfdatiregione', callback_data='pdfdatiregione')],
        [InlineKeyboardButton(text='Pdfdatiprovincia', callback_data='pdfdatiprovincia')],
        [InlineKeyboardButton(text='Sentiment_Analysis_Coronavirus', callback_data='sentiment_analysis_coronavirus')]

    ])
    bot.sendMessage(chat_id, 'Seleziona ciò che ti interessa consultare ', reply_markup=keyboard)


def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, chat_id, query_data)






    if query_data == 'info':

        bot.sendMessage(chat_id, 'Ecco la descrizione dei comandi di questo bot :')
        bot.sendMessage(chat_id, 'andamento - Restituisce dei grafici tramite la libreria matplotlib estrapolati da dataframe che hanno come base dei  file csv nel quale vengono mostrati gli andamenti delle positività,guarigioni,morti in Italia sino ad oggi.(I file cvs vi si possono aggiornare quotidianamente da una fonte di github nel quale vengono caricati ogni giorno)')
        bot.sendMessage(chat_id, 'forniturestato - Restituisce le informazioni sulle forniture emesse dallo stato sino ad oggi. Queste informazioni vengono salvate su file di tipo TXT e integrano i fornitori, la tipologia di prodotto, il prezzo unitario del bene e la data nel quale è stato fatto il contratto')
        bot.sendMessage(chat_id, 'tassorischioregione - Restituisce dei grafici tramite la libreria matplotlib estrapolati da dataframe che hanno come base dei file csv nel quale vengono mostrati gli andamenti delle positività,guarigioni,morti in comparazione tra tutte le regioni d’Italia sino ad oggi.')
        bot.sendMessage(chat_id, 'tassorischioprovincia - Viene restituito il picco dei positivi in quella precisa provincia(poiché i dati all’interno dei csv Caricati dalla fonte non integrano la quantità dei guariti o dei deceduti).')
        bot.sendMessage(chat_id, 'pdfdatiregione - Restituisce  un file pdf convertito in word che mostra i dati in forma tabellare delle positività,guarigioni,morti,,i recoverati con sintomi  ,positivi in terapia intensiva e quelli in isolamento di tutte le regioni sino ad oggi')
        bot.sendMessage(chat_id, 'pdfdatiprovincia - Restituisce  un file pdf convertito in word che mostra i dati in forma tabellare delle positività di tutte le province d’Italia  sino ad oggi ')
        bot.sendMessage(chat_id,'sentiment_analysis_coronavirus - Restituisce il grafico della sentiment analysis inerente al corona coronavirus , calcolato sulla base di un certo numero di tweet postati dalle persone su twitter ')

    elif query_data == 'sentiment_analysis_coronavirus':


        f = open('grafico_sentiment.png', 'rb')
        response = bot.sendPhoto(chat_id, f)

        bot.sendMessage(chat_id, 'Questa è il grafico della sentiment analysis inerente al corona coronavirus')


    elif query_data == 'andamento':


        f = open('totale_positivi.png', 'rb')
        response = bot.sendPhoto(chat_id, f)

        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi')

        f = open('dimessi_guariti.png', 'rb')
        response = bot.sendPhoto(chat_id, f)

        bot.sendMessage(chat_id, 'Questa è la variazione dei guariti  sino ad oggi')

        f = open('deceduti.png', 'rb')
        response = bot.sendPhoto(chat_id, f)

        bot.sendMessage(chat_id, 'Questa è la variazione dei deceduti  sino ad oggi')




    elif query_data == 'forniturestato':



        bot.sendMessage(chat_id, 'Queste sono le forniture finanziate dallo stato italiano sino ad oggi ')


        bot.sendDocument(chat_id, open('forniture.txt'))



    elif query_data == 'tassorischioregione':


        ###################### andamento_sicilia ######################################

        f = open('andamento_sicilia.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (SICILIA)')
        ###################### andamento_sardegna ######################################

        f = open('andamento_sardegna.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (SARDEGNA)')
        ###################### andamento_calabria ######################################

        f = open('andamento_calabria.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (CALABRIA)')
        ###################### andamento_basilicata ######################################

        f = open('andamento_basilicata.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (BASILICATA)')
        ###################### andamento_campania ######################################

        f = open('andamento_campania.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (CAMPANIA)')
        ###################### andamento_puglia ######################################

        f = open('andamento_puglia.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (PUGLIA)')
        ###################### andamento_molise ######################################

        f = open('andamento_molise.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (MOLISE)')
        ###################### andamento_lazio ######################################

        f = open('andamento_lazio.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (LAZIO)')
        ###################### andamento_abruzzo ######################################

        f = open('andamento_abruzzo.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (ABRUZZO)')
        ###################### andamento_marche ######################################

        f = open('andamento_marche.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (MARCHE)')
        ###################### andamento_umbria ######################################

        f = open('andamento_umbria.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (UMBRIA)')
        ###################### andamento_toscana ######################################

        f = open('andamento_toscana.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (TOSCANA)')
        ###################### andamento_emiliaromagna ######################################

        f = open('andamento_emiliaromagna.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (EMILIA ROMAGNA)')
        ###################### andamento_liguria ######################################

        f = open('andamento_liguria.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (LIGURIA)')
        ###################### andamento_Piemonte ######################################

        f = open('andamento_Piemonte.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (PIEMONTE)')
        ###################### andamento_valledaosta ######################################

        f = open('andamento_valledaosta.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (VALLE D AOSTA)')
        ###################### andamento_Lombardia ######################################

        f = open('andamento_Lombardia.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (LOMBARDIA)')
        ###################### andamento_Trentino ######################################

        f = open('andamento_Trentino.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (TRENTINO ALTO ADIGE)')
        ###################### andamento_Friuli_Venezia_Giulia ######################################

        f = open('andamento_Friuli_Venezia_Giulia.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (FRIULI VENEZIA GIULIA)')
        ###################### andamento_Veneto ######################################

        f = open('andamento_Veneto.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa è la variazione dei positivi  sino ad oggi (VENETO)')



    elif query_data == 'tassorischioprovincia':

        ###################### andamento_sicilia ######################################

        f = open('andamento_siciliaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi  (SICILIA)')
        ###################### andamento_sardegna ######################################

        f = open('andamento_sardegnaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (SARDEGNA)')
        ###################### andamento_calabria ######################################

        f = open('andamento_calabriaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (CALABRIA)')
        ###################### andamento_basilicata ######################################

        f = open('andamento_basilicataprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (BASILICATA)')
        ###################### andamento_campania ######################################

        f = open('andamento_campaniaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (CAMPANIA)')
        ###################### andamento_puglia ######################################

        f = open('andamento_pugliaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (PUGLIA)')
        ###################### andamento_molise ######################################

        f = open('andamento_moliseprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (MOLISE)')
        ###################### andamento_lazio ######################################

        f = open('andamento_lazioprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (LAZIO)')
        ###################### andamento_abruzzo ######################################

        f = open('andamento_abruzzoprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (ABRUZZO)')
        ###################### andamento_marche ######################################

        f = open('andamento_marcheprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (MARCHE)')
        ###################### andamento_umbria ######################################

        f = open('andamento_umbriaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (UMBRIA)')
        ###################### andamento_toscana ######################################

        f = open('andamento_toscanaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (TOSCANA)')
        ###################### andamento_emiliaromagna ######################################

        f = open('andamento_emiliaromagnaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (EMILIA ROMAGNA)')
        ###################### andamento_liguria ######################################

        f = open('andamento_liguriaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (LIGURIA)')
        ###################### andamento_Piemonte ######################################

        f = open('andamento_Piemonteprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (PIEMONTE)')
        ###################### andamento_valledaosta ######################################

        f = open('andamento_valledaostaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (VALLE D AOSTA)')
        ###################### andamento_Lombardia ######################################

        f = open('andamento_Lombardiaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (LOMBARDIA)')
        ###################### andamento_Trentino ######################################

        f = open('andamento_Trentinoprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (TRENTINO ALTO ADIGE)')
        ###################### andamento_Friuli_Venezia_Giulia ######################################

        f = open('andamento_Friuli_Venezia_Giuliaprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (FRIULI VENEZIA GIULIA)')
        ###################### andamento_Veneto ######################################

        f = open('andamento_Venetoprovince.png', 'rb')
        response = bot.sendPhoto(chat_id, f)
        bot.sendMessage(chat_id, 'Questa sono i picchi di persone positive raggiunti dalle varie province italiane che hanno registrato positivi (VENETO)')


    elif query_data == 'pdfdatiregione':

       

        bot.sendMessage(chat_id, 'Queste è il file DOC dei dati di ogni regione durante il COVID')

        bot.sendDocument(chat_id=chat_id, document=open('regioni.docx', 'rb'))
        #bot.sendDocument(chat_id, open('COVID-19-master\schede-riepilogative\Regioni\dpc-covid19-ita-scheda-regioni-20200615.pdf'))


    elif query_data == 'pdfdatiprovincia':

        bot.sendMessage(chat_id, 'Queste è il file DOC dei dati di ogni provincia durante il COVID ')

        #bot.sendDocument(chat_id, document=open('COVID-19-master\schede-riepilogative\Province\dpc-covid19-ita-scheda-province-20200615.pdf, rb'))
        bot.sendDocument(chat_id=chat_id, document=open('province.docx', 'rb'))

bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('In attesa di un comando da parte di un utente telegram ...')

while 1:
    time.sleep(10)

