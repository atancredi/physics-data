#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/////////////////////////////////////////////////////////
//Per ora, implemento un solo algoritmo per aggiungere //
//comandi di maggiore interesse quali argomenti        //
//da riga di comando, strutture e allocazioni          //
//dinamiche di memoria                                 //
/////////////////////////////////////////////////////////

//DICHIARO LE STRUTTURE
struct point{
    double x;
    double y;
};

//DICHIARO I PROTOTIPI DELLE FUNZIONI

int main(int argc, char *argv[]){
    
    //Dichiaro le variabili che mi aspetto di ricevere dalla riga di comando
    
    //SCHEMA DI CONTROLLO DELL'INPUT
    int expected_args = 5;
    //se non ho inserito abbastanza argomenti
        //controllo se ce ne sono solo due
            //se il secondo è help stampo un messaggio di aiuto
            //se il secondo è auto eseguo il programma con dei valori predefiniti
        //se ci sono due argomenti ma non sono nè help nè auto o se ce ne sono più di due ma meno di expected_args quitto
    //se ho inserito abbastanza argomenti assegno i valori alle variabili scorrendo in argv[]
    
    
    //RUNNO IL CODICE PRINCIPALE
}