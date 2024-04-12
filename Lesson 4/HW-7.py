import datetime

class CourtCase:
    def __init__(self, case_number: str, *args, **kwargs):
        self.case_number = case_number
        self.case_participants = kwargs.get('case_participants', [])
        self.listening_datetimes = kwargs.get('listening_datetimes', [])
        self.is_finished = kwargs.get('is_finished', False)
        self.verdict = kwargs.get('verdict', '')

    def set_a_listening_datetime(self, date_time: datetime.datetime):
        self.listening_datetimes.append(date_time)

    def add_participant(self, inn: str):
        self.case_participants.append(inn)

    def remove_participant(self, inn: str):

        if inn in self.case_participants:
            self.case_participants.remove(inn)
        else:
            print(f"Participant INN {inn} not found.")

    def make_a_decision(self, verdict: str):
        self.verdict = verdict
        self.is_finished = True