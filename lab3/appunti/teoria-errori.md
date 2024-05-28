## Errore e incertezza
##### Errore casuale
Il risultato di una misura meno la media che dovrebbe risultare da un infinito numero di misure dello stesso misurando fatte in condizioni di ripetitività.
##### Errore sistematico
Differenza tra la media che dovrebbe risultare da un infinito numero di misure dello stesso misurando fatte in condizioni di ripetitività ed il valore del misurando. L’errore sistematico è pertanto l’errore di misura meno l’errore casuale. L’errore sistematico e le sue cause non possono essere completamente noti. Spesso gli errori sistematici sono quelli che derivano da errori di taratura degli strumenti o dell’apparato sperimentale o dalla mancanza di imparzialità dell’osservatore.

L’organizzazione internazionale di metrologia legale (OIML, 1968) definisce l’errore sistematico come un errore che nel corso di un certo numero di misure, fatte nelle stesse condizioni, dello stesso valore di una data quantità, rimane costante in valore assoluto e segno o varia secondo una legge definita quando cambiano le condizioni. È evidente che gli errori sistematici limitano l’accuratezza della misura: quanto più si riescono ad eliminare gli errori sistematici, tanto più la misura è accurata.

##### Incertezza (di misura)
Intervallo al quale contribuiscono varie componenti che possono sostanzialmente essere distinte in due categorie: quelle che sono valutate con metodi statistici e quelle che sono valutate con altri metodi.

Bisognerebbe sempre tenere in mente la differenza tra errore ed incertezza. Per esempio il risultato di una misura dopo correzioni per compensare effetti sistematici individuati può essere molto vicino (anche se non si può sapere di quanto) al valore incognito del misurando, ed avere così un errore trascurabile, ma avere una incertezza grande.

## Propagazione degli errori

Siano due grandezze misurate direttamente $a$, $b$:
$$a = (a_0 \pm \Delta a)$$
$$b = (b_0 \pm \Delta b)$$
##### Somma $S=a+b$
$$S_0 = a_0+b_0$$
$$\Delta S = \Delta a + \Delta b$$
##### Differenza $D = a-b$
$$D_0 = a_0-b_0$$
$$\Delta D = \Delta a + \Delta b$$
##### Prodotto $P = a\cdot b$
$$P_0 = a_0\cdot b_0$$
$$\Delta P = a_0\Delta b + b_0\Delta a$$
Valida nelle condizioni in cui le incertezze sono molto minori delle grandezze misurate, ovvero la situazione tipica in laboratorio.

##### Potenza $P = a^n$
$$P_0 = a_0^n$$
$$\Delta P = na_0^{n-1}\Delta a$$

##### Moltiplicazione per un numero puro $M = c\cdot a$ ($\Delta c =0$)
$$M_0 = c\cdot a_0$$
$$\Delta M = c\Delta a + a\Delta c=c\Delta a$$
##### Quoziente $Q = \frac{a}{b}$
$$Q_0 = \frac{a_0}{b_0}$$
$$\Delta Q = \frac{a_0\Delta b + b_0\Delta a}{b_0^2}$$

### Caso generale
Voglio calcolare l'incertezza su una grandezza $G = f(a,b,...)$
$$G_0=f(a_0,b_0,...)$$
$$\Delta G^2 = (\frac{\partial f}{\partial a}(a_0,b_0))^2\cdot \Delta a^2 + (\frac{\partial f}{\partial b}(a_0,b_0))^2\cdot \Delta b^2 + ...$$
## Errore relativo

Quasi sempre quando si misura una generica grandezza a è fisicamente più significativo il rapporto tra l’errore e la grandezza stessa, $\frac{\Delta a}{a}$ , piuttosto che l’errore assoluto $\Delta a$. Tale rapporto viene chiamato errore relativo.

Sia una grandezza del tipo $G=a^nb^mc^p$
L'errore relativo si scrive semplicemente
$$\frac{\Delta G}{G_0}=|n\frac{\Delta a}{a_0}|+|m\frac{\Delta b}{b_0}|+|p\frac{\Delta c}{c_0}|$$
Da questa formula si deduce che è inutile cercare di ridurre l’errore relativo su una delle grandezze nel caso in cui esso sia già molto più piccolo degli errori relativi sulle altre (questi ultimi domineranno comunque sull’errore complessivo).

## Cifre significative e convenzioni di scrittura

Per il best value della misura bisogna troncare all'ultima potenza di 10 dell'errore (per eccesso o per difetto).

- La cifra più significativa è quella più a sinistra diversa da zero.  
- La cifra meno significativa è quella più a destra.  
- Tutte le cifre comprese fra la più e la meno significativa sono cifre significative.

Se non c’è la virgola decimale la cifra meno significativa è quella più a destra diversa da zero. In questo caso il numero $10$ ha solo una cifra significativa. Se lo volessi riportare con due cifre significative dovrei scrivere $10.0$

**in generale si riportano tutte le cifre fino alla prima influenzata dall’errore inclusa**, soprattutto se si propagano gli errori tramite l'errore massimo (casi scritti in precedenza). Se invece si usano metodi più sofisticati per trattare gli errori si usa scrivere la misura fino alla seconda cifra affetta da errore e quindi l'errore con due cifre significative.

In altre parole la convenzione per le cifre significative di errore è **non più di una**. Questo a meno che rimuovere l'ultima cifra significativa non introduca una discrepanza sull'errore relativo maggiore del $20\%$.

$$10.0 \pm 5.2 \rightarrow 10.0 \pm 5$$
Questo va bene perchè introduco una discrepanza minore del 20% sull'errore relativo. Invece quest'altro caso non va bene:
$$10.0 \pm 1.4$$
Se levassi il $.4$ introdurrei una discrepanza maggiore del 20% sull'errore relativo.


### Esempi
Indicando con una sottolineatura la cifra meno significativa, e con una sopralineatura la cifra più significativa, si ha:
$$\bar{3}11\underline{5} $$ 
$$\bar{3}212.\underline{5} $$
$$0.0\bar{3}2\underline{5} $$
$$\bar{3}21.0\underline{5}$$
$$0.0\bar{3}0\underline{0} $$
$$\bar{3}00.0\underline{0} $$
$$\bar{3}0.03\underline{0} $$

$(500.42\pm32.5)$ -> **SBAGLIATO**
$(500.42 \pm 30)$ -> **CORRETTO**

#### ASSOLUTAMENTE NO
$$1.257 \pm 0.324$$

##### Errore massimo nel prodotto arrotondando
Considero due quantità che, in qualche unità di misura, valgono:
$$a = 1.25432$$
$$b = 9.35$$
Le arrotondo rispettivamente a
$$a_0=1.25$$
$$b_0=9.4$$
- calcolo il prodotto con i numeri originali
	$p=a\cdot b=11.727892$
- calcolo il prodotto con i numeri arrotondati
	$p_0=a_0\cdot b_0=11.750$
- la differenza tra i due prodotti vale
	$p-p_0=0.022$
- l'errore e' sulla quarta cifra significativa, quindi
	$p_0 = 11.75 \pm 0.02$
	oppure anche
	$p_0=11.750\pm 0.022$
- Se non si riporta l'errore, siccome solo tre cifre sono 'sicure' si scrive
	$p_0=11.7$
	dove si intende
	$11.65 < p_0 < 11.75$
##### fonti
Misure ed analisi dei dati - Baldini, Martinelli - 2014