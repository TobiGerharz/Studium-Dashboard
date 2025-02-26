import pandas as pd
from datetime import datetime

class GradeStatistic:
    def __init__(self, file_path):
        # Laden der Excel Datei
        self.excel_table = pd.read_excel(file_path)
        # Extrahierung der Noten
        self.grades = self.excel_table['Note']

    def calculate_average_grade(self):
        # Berechnung des Durchschnitts aller Noten
        return self.grades.mean()

    def get_grade_message(self, average_grade):
        # Ausgabe der Nachricht zum Zielschnitt
        if average_grade > 2.5:
            return "Unter Zieldurchschnitt"
        else:
            return "Im Zielschnitt"

    def calculate_module_progress(self, bar_length):
        # Berechnung des Fortschritts der abgeschlossenen Module
        all_modules = len(self.grades)  # Gesamtanzahl der Module
        modules_with_grade = self.grades.notna().sum()  # Anzahl der abgeschlossenen Module
        grade_progress = modules_with_grade / all_modules  # Fortschritt in Prozent
        filled_length = int(grade_progress * bar_length)  # Länge der Fortschrittsanzeige
        grade_bar = 'X' * filled_length + '-' * (bar_length - filled_length)  # Erstelle Fortschrittsbalken
        return grade_bar, filled_length

class StudyProgress:
    def __init__(self, start_date_str):
        # Startdatum des Studiums als Datum-Objekt
        self.start_date = pd.to_datetime(start_date_str)
        self.current_date = datetime.now()

    def calculate_passed_days(self):
        # Berechnung der Anzahl der vergangenen Tage seit Studienbeginn
        return (self.current_date - self.start_date).days

    def calculate_time_progress(self, passed_days, study_days, bar_length):
        # Berechnung des Zeitfortschritts des Studiums
        time_progress = passed_days / study_days  # Anteil der vergangenen Zeit
        filled_length = int(time_progress * bar_length)  # Länge der Fortschrittsanzeige
        time_bar = 'X' * filled_length + '-' * (bar_length - filled_length)  # Fortschrittsbalken für die Zeit
        return time_bar, filled_length

    def compare_progress(self, time_filled_length, grade_filled_length):
        # Vergleicht den Zeitfortschritt mit dem Notenfortschritt
        if time_filled_length > grade_filled_length:
            return "Du bist nicht mehr im Zeitplan"
        else:
            return "Du bist im Zeitplan"

class DashboardBuild:
    def __init__(self, file_path: str, bar_length: int = 30, study_days: int = 4 * 365):
        # Initialisierung des Dashboards mit den eingegebenen Werten
        self.file_path = file_path
        self.bar_length = bar_length  # Länge des Fortschrittsbalkens
        self.study_days = study_days  # Gesamtdauer des Studiums in Tagen (4 Jahre)

    def run(self):
        # Erstellung der Instanz der GradeStatistic-Klasse
        grade_overview = GradeStatistic(self.file_path)
        
        # Berechnung des Notendurchschnitts und Ausgabe einer passenden Nachricht
        average_grade = grade_overview.calculate_average_grade()
        grade_message = grade_overview.get_grade_message(average_grade)
        print(f"Gesamtschnitt: {average_grade:.2f}")
        print(grade_message)

        # Auslesen des Studienstartdatum aus der Excel-Datei
        start_date_str = grade_overview.excel_table['Startdatum Studium'].iloc[0]
        study_progress = StudyProgress(start_date_str)
        
        # Berechnung der vergangenen Tage seit Studienbeginn
        passed_days = study_progress.calculate_passed_days()
        print(f"Seit dem {study_progress.start_date.strftime('%d.%m.%Y')} sind {passed_days} Tage vergangen.")
        
        # Berechnung und Ausgabe des Zeitfortschritts
        time_bar, time_filled_length = study_progress.calculate_time_progress(passed_days, self.study_days, self.bar_length)
        print(f"Vergangene Zeit: [{time_bar}]")
        
        # Berechnung und Ausgabe des Studienfortschritts
        grade_bar, grade_filled_length = grade_overview.calculate_module_progress(self.bar_length)
        print(f"Abgeschlossene Module: [{grade_bar}]")
        
        # Vergleich Zeitfortschritt mit dem Studienfortschritt
        progress_message = study_progress.compare_progress(time_filled_length, grade_filled_length)
        print(progress_message)

if __name__ == "__main__":
    # Datei mit den Noten einlesen und das Dashboard starten
    file_path = "NotenübersichtDashboard.xlsx"
    program = DashboardBuild(file_path)
    program.run()
