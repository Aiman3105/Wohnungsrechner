def Annuität(Kaufpreis, Eigenkapital, Provision, Kreditrahmen, Zinssatz, Kreditlaufzeit):
    Annuität = Kreditrahmen * (
                (1 + Zinssatz / 100) ** Kreditlaufzeit * (Zinssatz / 100)) / (
                           (1 + Zinssatz / 100) ** Kreditlaufzeit - 1)
    Rate_mtl = round(Annuität / 12,2)
    return Rate_mtl


def Einnahmen(Größe, Mietpreis_pro_Quadratmeter, Hausgeld):
    Einnahmen = round(Größe * Mietpreis_pro_Quadratmeter - 0.4 * Hausgeld, 2)
    return Einnahmen


def Vermögensaufbau_Steuervorteil(Kaufpreis, Kaufnebenkostensfaktor, Kreditrahmen, Annuität, Zinssatz, Kreditlaufzeit, Abschreibungsfaktor, Einnahmen, Jahre):
    offener_Kredit=Kreditrahmen
    Zinsen=offener_Kredit*Zinssatz/100
    Abgezahlt=0
    Steuervorteil=0
    Steuervorteil_gesamt = 0
    Abgezahlt_gesamt=0
    if Jahre==0:
        Abgezahlt_gesamt = 0
        Steuervorteil_gesamt= 0
    else:
        for n in range(1,Jahre+1):
            offener_Kredit = offener_Kredit - Abgezahlt
            Zinsen = offener_Kredit * Zinssatz / 100
            Abgezahlt = Annuität - Zinsen
            Steuervorteil = (Kaufpreis * (
                    1 + Kaufnebenkostensfaktor / 100) * Abschreibungsfaktor / 100 + Zinsen - 12 * Einnahmen) * 0.42
            Abgezahlt_gesamt = Abgezahlt_gesamt + Abgezahlt
            Steuervorteil_gesamt= Steuervorteil + Steuervorteil_gesamt
    return Abgezahlt_gesamt, Steuervorteil_gesamt

