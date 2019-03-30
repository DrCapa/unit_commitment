Wir betrachten ein Portfolio basierend auf zwei **BHKWs** (chp), einem **Heizwerk** (heat plant) und einem **Wärmespeicher** (store). 

Im Ordner input sind enthalten:
* Technische Daten und Betriebskosten der Anlagen,
* Zeitreihen für Gas- und Strompreise,
* Nachfrage Wärmeleistung für einen Tag.

Das Projekt enthält 4 Python-Datein:
* model.py: Beinhaltet die Zielfunktion und Nebenbedingungen zur Beschreibung des Problems. 
* instance.py: Die Funktion run_optimisation liest die Inputzeitreihen ein, erstellt die Instanz des Modells, löst das Problem und schreibt die Ergebnisse in Zeitreihen. Ein Ordner names output wird erstellt um die Zeitreihen zu speichern.
* analysis.py: Enthält einfache Analysen und Visualisierungen der Ergebnisse. Ein Unterordner names plots wird zur Speicherung erstellt.
* main.py: Ist die auszuführende Datei.
