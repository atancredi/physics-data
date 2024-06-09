#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define m 1
#define t0 0
#define x0 10
#define columns 3

//Definisco le strutture
struct corpo{
    double x;
    double v;
    double gamma;
};

struct tempo{
    int Tmax;
    double dt;
};

struct flag{
    int verbose;
    int print;
    int graphs;
};

//Definisco i prototipi delle funzioni
double phi(double x, double v, double gamma);
double costante(struct corpo corpo);
void verlet(struct corpo corpo, struct tempo tempo, struct flag flag, int plot);
void verlet_puntob(struct corpo corpo, struct tempo tempo);
void rungekutta(struct corpo corpo, struct tempo tempo, struct flag flag, int plot);
void rungekutta_puntob(struct corpo corpo, struct tempo tempo);
void plot_fit(double *x, double *y, int n);

int main(int argc, char *argv[]){
    
    //pulisco il terminale
    system("clear");
    
    struct corpo corpo;
    struct tempo tempo;
    struct flag flag;
    
    //Sezione 1: Controllo degli argomenti passati da riga di comando (v0, dt, Tmax)
    int expected_arguments = 3;
    expected_arguments += 1; //Il primo elemento di argv è il nome del file stesso
    if((argc == 2 && strcmp(argv[1], "help") == 0) || argc != expected_arguments){
        //Se richiedo aiuto o se il numero di argomenti non è quello giusto mostro un messaggio d'errore
        printf("Usage: v0 deltat Tmax\n");
        printf("Inserire gli argomenti separati da spazio, con il punto per indicare le cifre decimali\n");
        exit(-1);
    }else{
        //Condizioni iniziali
        corpo.x = x0;
        corpo.v = -(atof(argv[1]));
        tempo.dt = atof(argv[2]);
        tempo.Tmax = atof(argv[3]);
    }
    
    //Sezione 2: Chiedo all'utente se vuole stampare il punto b del problema e quale algoritmo vuole usare
    //e anche se vuole introdurre il termine d'attrito e se vuole stampare il punto d del problema
    //chiedo inoltre se voglio non stampare affatto il testo o i grafici
    int puntob = -1, puntod, algoritmo, errore = -1;
    corpo.gamma = -1;
    flag.print = -1;
    flag.graphs = -1;
    printf("Termine di attrito? (0 per non inserirlo)\n");
    while(corpo.gamma < 0) scanf(" %lf", &corpo.gamma);
    printf("\n");
    if(corpo.gamma == 0){
        printf("Vuoi stampare anche il punto b) della consegna? 1: si, 0: no\n");
        while(puntob != 1 && puntob != 0) scanf(" %d", &puntob);
        printf("\n");
        printf("Vuoi stampare anche il punto d) della consegna? 1: si, 0: no\n");
        while(puntod != 1 && puntod != 0) scanf(" %d", &puntod);
        printf("\n");
    }else{
        printf("\n");
    }
    printf("Che algoritmo uso? 1: Verlet, 2: Runge Kutta II\n");
    while(algoritmo != 1 && algoritmo != 2) scanf(" %d", &algoritmo);
    printf("\n");
    
    if(gamma == 0){
        printf("Effettuo lo studio dell'errore? 1: si, 0:no\n");
        while(errore != 1 && errore != 0) scanf(" %d", &errore);
        printf("\n");
    }
    
    printf("Stampo i grafici? 1: si, 0: no\n");
    while(flag.graphs != 1 && flag.graphs != 0) scanf(" %d", &flag.graphs);
    printf("\n");
    
    //Sezione 3: Algoritmo di Verlet
    if(algoritmo == 1){
        printf("Algoritmo di Verlet\n");
        flag.print = 1;
        verlet(corpo, tempo, flag, 1); //lo faccio una prima volta con la v0 definita dall'utente
        printf("\n");
        
        if(puntob == 1){
            printf("Stampo i grafici del punto b) del problema con l'algoritmo di Verlet\n");
            verlet_puntob(corpo, tempo);
            printf("\n");
        }
    
    }
    
    //Condizioni iniziali
    corpo.x = x0;
    corpo.v = -(atof(argv[1]));
    tempo.dt = atof(argv[2]);
    tempo.Tmax = atof(argv[3]);
    
    //Sezione 3b: Algoritmo di Runge Kutta
    if(algoritmo == 2){
        printf("Algoritmo di Runge Kutta II\n");
        flag.print = 1;
        rungekutta(corpo, tempo, flag, 1); //lo faccio una prima volta con la v0 definita dall'utente
        printf("\n");
        
        if(puntob == 1){
            printf("Stampo i grafici del punto b) del problema con l'algoritmo di Verlet\n");
            rungekutta_puntob(corpo, tempo);
            printf("\n");
        }
    }
    
    //Studio dell'errore
    if(errore == 1){
        double dt_start = 0.5;
        int n = 10; //precisione dello studio dell'errore
        double costanti[n], dts[n];
        
        flag.print = 0;
        flag.verbose = 1;
        
        for(int i = 0; i<n; i++){
            corpo.x = x0;
            corpo.v = -(atof(argv[1]));
            tempo.Tmax = atof(argv[3]);
            tempo.dt = dt_start;
            
            double ezero = costante(corpo);
            
            printf("\nIt. per dt=%lf\n",tempo.dt);
            if(algoritmo == 1) verlet(corpo, tempo, flag, 0);
            else if(algoritmo == 2) rungekutta(corpo, tempo, flag, 0);
            
            double efinal = costante(corpo);
            
            costanti[i] = (efinal - ezero) / ezero;
            
            dts[i] = dt_start;
            
            dt_start = dt_start/2;
        }
        
        plot_fit(dts, costanti, n);
        
    }
    
    //punto d del problema
    if(puntod == 1){
        flag.print = 0;
        flag.verbose = 0;
        corpo.x = x0;
        corpo.v = -1;
        tempo.dt = atof(argv[2]);
        tempo.Tmax = atof(argv[3]); 
        if(algoritmo == 1){
            verlet(corpo, tempo, flag, 0);
        }else if(algoritmo == 2){
            rungekutta(corpo, tempo, flag, 0);
        }
    }
}

double phi(double x, double v, double gamma){
    if(x == 0 || x < 0){
        //x è fuori dal dominio della funzione
        printf("x non appartiene alle condizioni di esistenza per phi \n");
        exit(-1);
    }
    if(gamma == 0){
        return exp(-x/2)*log(x)*(log(x)-(4/x));
    }else if(gamma > 0){
        return exp(-x/2)*log(x)*(log(x)-(4/x)) - (gamma * v);
    }
}

double costante(struct corpo corpo){
    return 0.5 * pow(corpo.v,2) + 2*pow(log(corpo.x),2) * exp(-corpo.x / 2);
}

void verlet(struct corpo corpo, struct tempo tempo, struct flag flag, int plot){
    //Numero di passi:
    int nPassi = (tempo.Tmax/tempo.dt + 0.5);
    
    //Dichiaro l'array
    double **verlet_values = (double **)malloc(nPassi * sizeof(double));
    for (int i=0; i<=nPassi; i++) verlet_values[i] = (double *)malloc(columns * sizeof(double));
    
    int puntoc = 0;
    double v0 = corpo.v;
    
    //Ciclo iterativo
    double t = 0;
    for(int i = 0; i<nPassi; i++){
        double xnp = corpo.x + corpo.v * tempo.dt + 0.5 * phi(corpo.x, corpo.v, corpo.gamma) * pow(tempo.dt, 2);
        double vnp = corpo.v + tempo.dt * (phi(corpo.x, corpo.v, corpo.gamma) + phi(xnp, corpo.v, corpo.gamma))/2;
        //aggiorno le variabili
        corpo.x = xnp;
        corpo.v = vnp;
        
        //punto c e d della consegna
        if(corpo.x > 0.999 && corpo.x < 1.001){
            puntoc += 1;
            if(flag.print == 0){printf("%.14lf\t%.14lf\t%.14lf\n", t, corpo.x, corpo.v);}
        }
        if(flag.print == 1){
            printf("%.14lf\t%.14lf\t%.14lf\n", t, corpo.x, corpo.v);
        }
        if(flag.verbose == 1){
            double percentage;
            percentage = (t / tempo.Tmax) * 100;
            if(percentage/10 == (int)percentage/10) printf("%f\n", percentage + 10);
        }
        if(flag.graphs == 1){
            verlet_values[i][0] = t;
            verlet_values[i][1] = xnp;
            verlet_values[i][2] = vnp;
        }
        t = tempo.dt * i;
    }
    
    if(flag.graphs == 1){
        //genero il grafico x su t se passo il valore 1 all'argomento plot
        double x[nPassi], y[nPassi], v[nPassi];
        for(int i=0;i<nPassi;i++){ x[i] = verlet_values[i][0]; };
        for(int i=0;i<nPassi;i++){ y[i] = verlet_values[i][1]; };
        for(int i=0;i<nPassi;i++){ v[i] = verlet_values[i][2]; };
        if(plot == 1){
            //Apro una pipe di sistema e ci dialogo con gnuplot
            FILE *p = popen("gnuplot -persist", "w");
            fprintf(p, "plot '-' w lines title 'pos su t'\n");
            for(int i = 0; i < nPassi; i++) fprintf(p, "%.14lf %.14lf\n", x[i], y[i]);
            fprintf(p, "e\n");
            pclose(p);
            FILE *q = popen("gnuplot -persist", "w");
            fprintf(q, "plot '-' w lines title 'vel su t'\n");
            for(int i = 0; i < nPassi; i++) fprintf(q, "%.14lf %.14lf\n", x[i], v[i]);
            fprintf(q, "e\n");
            pclose(q);
            FILE *k = popen("gnuplot -persist", "w");
            fprintf(k, "plot '-' w lines title 'Spazio delle fasi'\n");
            for(int i = 0; i < nPassi; i++) fprintf(p, "%.14lf %.14lf\n", v[i], y[i]);
            fprintf(k, "e\n");
            pclose(k);
        }
    }
    //libero l'array
    free(verlet_values);
    
    if(puntoc != 0 && flag.print == 1){
        printf("\nX raggiunto %d volte con v0 = %.14lf\n", puntoc, v0);
    }else if(puntoc == 0 && flag.print == 1){
        printf("\nX non raggiunto con v0 = %.14lf", v0);
    }
}

void verlet_puntob(struct corpo corpo, struct tempo tempo){
    //Condizioni iniziali
    corpo.x = x0;
    corpo.v = -(0.1);
    //Numero di passi:
    int nPassi = (tempo.Tmax/tempo.dt + 0.5);
    //Dichiaro l'array
    double **verlet_values = (double **)malloc(nPassi * sizeof(double));
    for (int i=0; i<nPassi; i++) verlet_values[i] = (double *)malloc(columns * sizeof(double));
    //Ciclo iterativo
    double t = 0;
    for(int i = 0; i<nPassi; i++){
        double xnp = corpo.x + corpo.v * tempo.dt + 0.5 * phi(corpo.x, corpo.v, corpo.gamma) * pow(tempo.dt, 2);
        double vnp = corpo.v + tempo.dt * (phi(corpo.x, corpo.v, corpo.gamma) + phi(xnp, corpo.v, corpo.gamma))/2;
        //aggiorno le variabili
        corpo.x = xnp;
        corpo.v = vnp;
        //stampo
        //printf("%.14lf\t%.14lf\t%.14lf\n", t, corpo.x, corpo.v); silenzio l'output per non creare confusione
        verlet_values[i][0] = t;
        verlet_values[i][1] = xnp;
        verlet_values[i][2] = vnp;
        t += tempo.dt;
    }
    
    //genero il grafico x su t se passo il valore 1 all'argomento plot
    double x[nPassi], y[nPassi];
    for(int i=0;i<nPassi;i++){ x[i] = verlet_values[i][0]; };
    for(int i=0;i<nPassi;i++){ y[i] = verlet_values[i][1]; };
    
    //Seconda esecuzione
    corpo.x = x0;
    corpo.v = -(1.2);
    //Dichiaro l'array
    double **verlet_values2 = (double **)malloc(nPassi * sizeof(double));
    for (int i=0; i<nPassi; i++) verlet_values2[i] = (double *)malloc(columns * sizeof(double));
    //Ciclo iterativo
    t = 0;
    for(int i = 0; i<nPassi; i++){
        double xnp2 = corpo.x + corpo.v * tempo.dt + 0.5 * phi(corpo.x, corpo.v, corpo.gamma) * pow(tempo.dt, 2);
        double vnp2 = corpo.v + tempo.dt * (phi(corpo.x, corpo.v, corpo.gamma) + phi(xnp2, corpo.v, corpo.gamma))/2;
        //aggiorno le variabili
        corpo.x = xnp2;
        corpo.v = vnp2;
        //stampo
        printf("%.14lf\t%.14lf\t%.14lf\n", t, corpo.x, corpo.v);
        verlet_values2[i][0] = t;
        verlet_values2[i][1] = xnp2;
        verlet_values2[i][2] = vnp2;
        t += tempo.dt;
    }
    
    //genero il grafico x su t se passo il valore 1 all'argomento plot
    double x2[nPassi], y2[nPassi];
    for(int i=0;i<nPassi;i++){ x2[i] = verlet_values2[i][0]; };
    for(int i=0;i<nPassi;i++){ y2[i] = verlet_values2[i][1]; };
    
    //Apro una pipe di sistema e ci dialogo con gnuplot
    FILE *p = popen("gnuplot -persist", "w");
    fprintf(p, "plot '-' w lines linecolor rgb 'red' title 'v0 = 0.1', '-' w lines linecolor rgb 'blue' title 'v0 = 1.2'\n");
    for(int i = 0; i < nPassi; i++) fprintf(p, "%.14lf %.14lf\n", x[i], y[i]);
    fprintf(p, "e\n");
    for(int i = 0; i < nPassi; i++) fprintf(p, "%.14lf %.14lf\n", x2[i], y2[i]);
    fprintf(p, "e\n");
    
    pclose(p);
    //libero l'array
    free(verlet_values);
    free(verlet_values2);
}

void rungekutta(struct corpo corpo, struct tempo tempo, struct flag flag, int plot){
    //Numero di passi:
    int nPassi = (tempo.Tmax/tempo.dt + 0.5);
    
    //Dichiaro l'array
    double **rungekutta_values = (double **)malloc(nPassi * sizeof(double));
    for (int i=0; i<=nPassi; i++) rungekutta_values[i] = (double *)malloc(columns * sizeof(double));
    
    int puntoc = 0;
    double v0 = corpo.v;
    
    //Ciclo iterativo
    double t = 0;
    double as, dx, dv;
    for(int i = 0; i<nPassi; i++){
        
        dx = corpo.v * tempo.dt;
        dv = phi(corpo.x, corpo.v, corpo.gamma) * tempo.dt;
        as = corpo.x + 0.5 * dx;
        double xnp = corpo.x + (corpo.v + dv/2) * tempo.dt;
        double vnp = corpo.v + phi(as, corpo.v, corpo.gamma) * tempo.dt;
        
        //Aggiornamento variabili
        corpo.x = xnp;
        corpo.v = vnp;
        
        //punto c della consegna
        if(corpo.x > 0.999 && corpo.x < 1.001){
            puntoc += 1;
            if(flag.print == 0){printf("%.14lf\t%.14lf\t%.14lf\n", t, corpo.x, corpo.v);}
        }
        if(flag.print == 1){
            printf("%.14lf\t%.14lf\t%.14lf\n", t, corpo.x, corpo.v);
        }
        if(flag.verbose == 1){
            double percentage;
            percentage = (t / tempo.Tmax) * 100;
            if(percentage/10 == (int)percentage/10) printf("%f\n", percentage + 10);
        }
        if(flag.graphs == 1){
            rungekutta_values[i][0] = t;
            rungekutta_values[i][1] = xnp;
            rungekutta_values[i][2] = vnp;
        }
        t = tempo.dt * i;
    }
    
    if(flag.graphs == 1){
        //genero il grafico x su t se passo il valore 1 all'argomento plot
        double x[nPassi], y[nPassi], v[nPassi];
        for(int i=0;i<nPassi;i++){ x[i] = rungekutta_values[i][0]; };
        for(int i=0;i<nPassi;i++){ y[i] = rungekutta_values[i][1]; };
        for(int i=0;i<nPassi;i++){ v[i] = rungekutta_values[i][2]; };
        if(plot == 1){
            //Apro una pipe di sistema e ci dialogo con gnuplot
            FILE *p = popen("gnuplot -persist", "w");
            fprintf(p, "plot '-' w lines title 'pos su t'\n");
            for(int i = 0; i < nPassi; i++) fprintf(p, "%.14lf %.14lf\n", x[i], y[i]);
            fprintf(p, "e\n");
            pclose(p);
            FILE *q = popen("gnuplot -persist", "w");
            fprintf(q, "plot '-' w lines title 'vel su t'\n");
            for(int i = 0; i < nPassi; i++) fprintf(q, "%.14lf %.14lf\n", x[i], v[i]);
            fprintf(q, "e\n");
            pclose(q);
            FILE *k = popen("gnuplot -persist", "w");
            fprintf(k, "plot '-' w lines title 'Spazio delle fasi'\n");
            for(int i = 0; i < nPassi; i++) fprintf(p, "%.14lf %.14lf\n", v[i], y[i]);
            fprintf(k, "e\n");
            pclose(k);
        }
    }
    //libero l'array
    free(rungekutta_values); 
    
    if(puntoc != 0 && flag.print == 1){
        printf("\nX raggiunto %d volte con v0 = %.14lf\n", puntoc, v0);
    }else if(puntoc == 0 && flag.print == 1){
        printf("\nX non raggiunto con v0 = %.14lf", v0);
    }
}

void rungekutta_puntob(struct corpo corpo, struct tempo tempo){
    //Condizioni iniziali
    corpo.x = x0;
    corpo.v = -(0.1);
    //Numero di passi:
    int nPassi = (tempo.Tmax/tempo.dt + 0.5);
    //Dichiaro l'array
    double **rungekutta_values = (double **)malloc(nPassi * sizeof(double));
    for (int i=0; i<nPassi; i++) rungekutta_values[i] = (double *)malloc(columns * sizeof(double));
    //Ciclo iterativo
    double t = 0;
    double as, dx, dv;
    for(int i = 0; i<nPassi; i++){
        dx = corpo.v * tempo.dt;
        dv = phi(corpo.x, corpo.v, corpo.gamma) * tempo.dt;
        as = corpo.x + 0.5 * dx;
        double xnp = corpo.x + (corpo.v + dv/2) * tempo.dt;
        double vnp = corpo.v + phi(as, corpo.v, corpo.gamma) * tempo.dt;
        //aggiorno le variabili
        corpo.x = xnp;
        corpo.v = vnp;
        //stampo
        //printf("%.14lf\t%.14lf\t%.14lf\n", t, corpo.x, corpo.v); silenzio l'output per non creare confusione
        rungekutta_values[i][0] = t;
        rungekutta_values[i][1] = xnp;
        rungekutta_values[i][2] = vnp;
        t += tempo.dt;
    }
    
    //genero il grafico x su t se passo il valore 1 all'argomento plot
    double x[nPassi], y[nPassi];
    for(int i=0;i<nPassi;i++){ x[i] = rungekutta_values[i][0]; };
    for(int i=0;i<nPassi;i++){ y[i] = rungekutta_values[i][1]; };
    
    //Seconda esecuzione
    corpo.x = x0;
    corpo.v = -(1.2);
    //Dichiaro l'array
    double **rungekutta_values2 = (double **)malloc(nPassi * sizeof(double));
    for (int i=0; i<nPassi; i++) rungekutta_values2[i] = (double *)malloc(columns * sizeof(double));
    //Ciclo iterativo
    t = 0;
    double as2, dx2, dv2;
    for(int i = 0; i<nPassi; i++){
        dx2 = corpo.v * tempo.dt;
        dv2 = phi(corpo.x, corpo.v, corpo.gamma) * tempo.dt;
        as2 = corpo.x + 0.5 * dx;
        double xnp2 = corpo.x + (corpo.v + dv2/2) * tempo.dt;
        double vnp2 = corpo.v + phi(as2, corpo.v, corpo.gamma) * tempo.dt;
        //aggiorno le variabili
        corpo.x = xnp2;
        corpo.v = vnp2;
        //stampo
        printf("%.14lf\t%.14lf\t%.14lf\n", t, corpo.x, corpo.v);
        rungekutta_values2[i][0] = t;
        rungekutta_values2[i][1] = xnp2;
        rungekutta_values2[i][2] = vnp2;
        t += tempo.dt;
    }
    
    //genero il grafico x su t se passo il valore 1 all'argomento plot
    double x2[nPassi], y2[nPassi];
    for(int i=0;i<nPassi;i++){ x2[i] = rungekutta_values2[i][0]; };
    for(int i=0;i<nPassi;i++){ y2[i] = rungekutta_values2[i][1]; };
    
    //Apro una pipe di sistema e ci dialogo con gnuplot
    FILE *p = popen("gnuplot -persist", "w");
    fprintf(p, "plot '-' w lines linecolor rgb 'red' title 'v0 = 0.1', '-' w lines linecolor rgb 'blue' title 'v0 = 1.2'\n");
    for(int i = 0; i < nPassi; i++) fprintf(p, "%.14lf %.14lf\n", x[i], y[i]);
    fprintf(p, "e\n");
    for(int i = 0; i < nPassi; i++) fprintf(p, "%.14lf %.14lf\n", x2[i], y2[i]);
    fprintf(p, "e\n");
    
    pclose(p);
    //libero l'array
    free(rungekutta_values);
    free(rungekutta_values2);
}

void plot_fit(double *x, double *y, int n) {
    //Apro una pipe di sistema e ci dialogo con gnuplot
    FILE *p = popen("gnuplot -persist", "w");
    fprintf(p,"f(x)=a*x**b\n");
    
    fprintf(p, "fit f(x) '-' via a,b\n");
    for(int i = 0; i < n; i++) fprintf(p, "%.14lf %.14lf\n", x[i], y[i]);
    fprintf(p, "e\n");
    fprintf(p, "plot f(x) w lines\n");
    fprintf(p, "plot '-'\n");
    for(int i = 0; i < n; i++) fprintf(p, "%.14lf %.14lf\n", x[i], y[i]);
    fprintf(p, "e\n");
    fprintf(p, "replot\n");
    pclose(p);
}