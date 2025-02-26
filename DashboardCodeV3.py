import pandas as pd
from datetime import datetime

class GradeStatistic:
    def __init__(self, file_path):
        self.excel_table = pd.read_excel(file_path)
        self.grades = self.excel_table['Note']

    def calculate_average_grade(self):
        return self.grades.mean()

    def get_grade_message(self, average_grade):
        if average_grade > 2.5:
            return "Unter Zieldurchschnitt"
        else:
            return "Im Zielschnitt"

    def calculate_module_progress(self, bar_length):
        all_modules = len(self.grades)
        modules_with_grade = self.grades.notna().sum()
        grade_progress = modules_with_grade / all_modules
        filled_length = int(grade_progress * bar_length)
        grade_bar = 'X' * filled_length + '-' * (bar_length - filled_length)
        return grade_bar, filled_length


class StudyProgress:
    def __init__(self, start_date_str):
        self.start_date = pd.to_datetime(start_date_str)
        self.current_date = datetime.now()

    def calculate_passed_days(self):
        return (self.current_date - self.start_date).days

    def calculate_time_progress(self, passed_days, study_days, bar_length):
        time_progress = passed_days / study_days
        filled_length = int(time_progress * bar_length)
        time_bar = 'X' * filled_length + '-' * (bar_length - filled_length)
        return time_bar, filled_length

    def compare_progress(self, time_filled_length, grade_filled_length):
        if time_filled_length > grade_filled_length:
            return "Du bist nicht mehr im Zeitplan"
        else:
            return "Du bist im Zeitplan"


class DashboardBuild:
    def __init__(self, file_path: str, bar_length: int = 30, study_days: int = 4 * 365):
        self.file_path = file_path
        self.bar_length = bar_length
        self.study_days = study_days

    def run(self):
        grade_overview = GradeStatistic(self.file_path)
        average_grade = grade_overview.calculate_average_grade()
        grade_message = grade_overview.get_grade_message(average_grade)
        print(f"Gesamtschnitt: {average_grade:.2f}")
        print(grade_message)

        start_date_str = grade_overview.excel_table['Startdatum Studium'].iloc[0]
        study_progress = StudyProgress(start_date_str)
        passed_days = study_progress.calculate_passed_days()
        print(f"Seit dem {study_progress.start_date.strftime('%d.%m.%Y')} sind {passed_days} Tage vergangen.")

        time_bar, time_filled_length = study_progress.calculate_time_progress(passed_days, self.study_days, self.bar_length)
        print(f"Vergangene Zeit: [{time_bar}]")
        grade_bar, grade_filled_length = grade_overview.calculate_module_progress(self.bar_length)
        print(f"Abgeschlossene Module: [{grade_bar}]")
        progress_message = study_progress.compare_progress(time_filled_length, grade_filled_length)
        print(progress_message)


if __name__ == "__main__":
    file_path = "NotenübersichtDashboard.xlsx"
    program = DashboardBuild(file_path)
    program.run()
