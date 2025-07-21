import Back_end
from Back_end import Annuität, Einnahmen, Vermögensaufbau_Steuervorteil
import streamlit as st

# Initialwerte (falls nicht in session_state)
if "mehr_felder" not in st.session_state:
    st.session_state.mehr_felder = False

if "Kaufnebenkostensfaktor" not in st.session_state:
    st.session_state.Kaufnebenkostensfaktor = 9.0
if "Provision" not in st.session_state:
    st.session_state.Provision = 3.57
if "Abschreibungsfaktor" not in st.session_state:
    st.session_state.Abschreibungsfaktor = 2.0

# Toggle Button
if st.button("Weitere Eingaben anzeigen/ausblenden"):
    st.session_state.mehr_felder = not st.session_state.mehr_felder

# Kredit – sichtbare Eingaben
st.subheader("Kredit")
col1, col2, col3 = st.columns(3)
with col1:
    Kaufpreis = st.number_input("Kaufpreis: ", step=1)
    Eigenkapital = st.number_input("Eigenkapital: ", step=500)

with col2:
    Kreditlaufzeit = st.number_input("Kreditlaufzeit: ", step=1, value=30)
    Jahre = st.number_input("Betrachtungszeitraum: ",
                            step=1)

with col3:
    Zinssatz = st.number_input("Zinssatz [%]: ", value=4.0)


# Wohnung – Eingaben
st.subheader("Wohnung")
col21, col22, col23 = st.columns(3)
with col21:
    Größe = st.number_input("Größe [m²]: ", step=1)
with col22:
    Mietpreis_pro_Quadratmeter = st.number_input("Quadratmeterpreis [€/m²]: ", step=1)
with col23:
    Hausgeld = st.number_input("Hausgeld: ", step=1)

# Erweiterte Eingaben (optional sichtbar)



if st.session_state.mehr_felder:
    st.subheader("Weitere Eingabemöglichkeiten")
    col11, col12, col13 = st.columns(3)
    with col11:
        st.session_state.Kaufnebenkostensfaktor = st.number_input(
            "Kaufnebenkosten [%]:",
            value=st.session_state.Kaufnebenkostensfaktor,
            key="input_kaufnebenkosten",
            step=0.1,
            format="%.2f"
        )
    with col12:
        st.session_state.Provision = st.number_input(
            "Provision [%]:",
            value=st.session_state.Provision,
            key="input_provision",
            step=0.01,
            format="%.2f"
        )
    with col13:
        st.session_state.Abschreibungsfaktor = st.number_input(
            "Abschreibungsfaktor [%]:",
            value=st.session_state.Abschreibungsfaktor,
            key="input_abschreibung",
            step=0.1,
            format="%.2f"
        )



# Berechnung nur, wenn Pflichtfelder gesetzt sind
if Kaufpreis > 0 and Zinssatz > 0 and Kreditlaufzeit > 0:
    # Werte aus Session State lesen
    Kaufnebenkostensfaktor = st.session_state.Kaufnebenkostensfaktor
    Provision = st.session_state.Provision
    Abschreibungsfaktor = st.session_state.Abschreibungsfaktor

    Kreditrahmen = Kaufpreis + (Kaufnebenkostensfaktor / 100 * Kaufpreis) + (Provision * Kaufpreis / 100) - Eigenkapital
    mtl_Rate = Annuität(Kaufpreis, Eigenkapital, Provision, Kreditrahmen, Zinssatz, Kreditlaufzeit)
    Annuitaet_gesamt = mtl_Rate * 12
    Einnahmen_gesamt = Einnahmen(Größe, Mietpreis_pro_Quadratmeter, Hausgeld)

    st.subheader("Ergebnis:")
    Vermögensaufbau, Steuerersparnis = Vermögensaufbau_Steuervorteil(
        Kaufpreis,
        Kaufnebenkostensfaktor,
        Kreditrahmen,
        Annuitaet_gesamt,
        Zinssatz,
        Kreditlaufzeit,
        Abschreibungsfaktor,
        Einnahmen_gesamt,
        Jahre
    )

    Cashflow_mtl = round(Einnahmen_gesamt - mtl_Rate, 2)
    Abgezahlt_gesamt = round(Vermögensaufbau, 2)
    Steuerersparnis_gesamt = round(Steuerersparnis, 2)

    col41, col42, col43, col44 = st.columns(4)

    with col41:
        st.metric("💰 Cashflow / Monat", f"{Cashflow_mtl} €")

    with col42:
        st.metric("🏦 Monatliche Rate", f"{mtl_Rate} €")

    with col43:
        st.metric("📈 Vermögenszuwachs", f"{Abgezahlt_gesamt} €")

    with col44:
        st.metric("💸 Steuervorteil", f"{Steuerersparnis_gesamt} €")
