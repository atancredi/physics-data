Per trovare la funzione di trasferimento di un circuito con amplificatori operazionali, segui questi passaggi:

### 1. Analisi del Circuito

Analizza il circuito passo dopo passo, considerando le leggi di Kirchhoff (KVL e KCL - V indica le tensioni (maglie) e C le correnti (nodi)) e le proprietà degli amplificatori operazionali, come la virtuale equipotenza dei nodi di ingresso e il fatto che l'impedenza di ingresso è molto alta (ideale infinita) e quella di uscita è molto bassa (ideale zero).

### 2. Scrittura delle Equazioni

Scrivi le equazioni che descrivono il comportamento del circuito utilizzando KVL e KCL. Queste equazioni sono solitamente in forma differenziale.

### 3. Determinazione della Funzione di Trasferimento

La funzione di trasferimento $H(s)$ di un sistema è definita come il rapporto tra la trasformata di Laplace dell'uscita e la trasformata di Laplace dell'ingresso, assumendo condizioni iniziali nulle. Matematicamente, è espressa come:
$$H(s)=\frac{V_{out}(s)}{V_{in}(s)}$$

### Esempio di Funzione di Trasferimento

Supponiamo di avere un circuito semplice con un amplificatore operazionale in configurazione invertente con un resistore $R_1$ in ingresso e un resistore $R_f$​ nel feedback.

1. **Scrivi l'equazione di KCL al nodo invertente:** 
	$$\frac{V_{in}-V_-}{R_1}+\frac{V_{out}-V_-}{R_f}=0$$
2. **Usa la proprietà della retroazione ideale $V_-=0$
	$$\frac{V_{in}}{R_1}+\frac{V_{out}}{R_f}=0$$
3. **Isola $V_{out}$:**
    $$V_{out}=-\frac{R_f}{R_1}V_{in}$$

Quindi, la funzione di trasferimento è:
$$H(s)=-\frac{R_f}{R_1}$$

### 4. Trovare i Poli della Funzione di Trasferimento

Per trovare i poli della funzione di trasferimento, risolvi il denominatore di $H(s)$ - un polinomio in $s$, impostandolo uguale a zero. I poli sono le radici di $D(s)$, cioè i valori di $s=j\omega$ che soddisfano: $D(s)=0$

### 5. Studio dei Poli

Una volta trovati i poli, puoi studiarne la posizione nel piano complesso $s$. I poli determinano la stabilità e la risposta dinamica del sistema. Ecco alcune considerazioni:

- **Poli sul semipiano sinistro (Re(s) < 0):** Il sistema è stabile.
- **Poli sul semipiano destro (Re(s) > 0):** Il sistema è instabile.
- **Poli sull'asse immaginario (Re(s) = 0):** Il sistema è marginalmente stabile (ossia, potrebbe oscillare).

### 6. Andamento della Funzione di Trasferimento

L'andamento della funzione di trasferimento può essere studiato considerando la risposta in frequenza del sistema. Puoi analizzare il comportamento in bassa frequenza ($s\approx 0$ ), in alta frequenza ( $s\rightarrow \infty$ ), e vicino ai poli e agli zeri della funzione di trasferimento.

1. **Risposta in frequenza:** Analizza la risposta in frequenza $H(j\omega)$ della funzione di trasferimento. Questo mostra come il sistema risponde alle diverse frequenze di ingresso.
    
2. **Diagrammi di Bode:** Usa i diagrammi di Bode per visualizzare il guadagno (in dB) e la fase (in gradi) della funzione di trasferimento in funzione della frequenza. I diagrammi di Bode sono utili per identificare le frequenze di taglio, i poli, gli zeri e le bande passanti del sistema.
    
3. **Stabilità e risposta temporale:** La posizione dei poli determina la stabilità e la risposta temporale del sistema. Poli con parte reale negativa indicano una risposta esponenziale decrescente (stabile), mentre poli con parte reale positiva indicano una risposta crescente (instabile). Poli immaginari puri indicano una risposta sinusoidale (oscillazioni).
    
