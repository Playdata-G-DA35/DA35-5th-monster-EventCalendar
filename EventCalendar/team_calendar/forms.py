from django import forms
import datetime

class TimeForm(forms.Form):
    current_year = datetime.datetime.now().year
    YEARS = [(y, y) for y in range(current_year - 10, current_year + 10)]
    MONTHS = [(m, m) for m in range(1, 13)]
    
    year = forms.ChoiceField(choices=YEARS, initial=current_year)
    month = forms.ChoiceField(choices=MONTHS, initial=datetime.datetime.now().month)
    MINUTES = [(f'{h:02d}:{m:02d}', f'{h:02d}:{m:02d}') for h in range(24) for m in range(0, 60, 15)]
    start_time = forms.ChoiceField(choices=MINUTES)
    end_time = forms.ChoiceField(choices=MINUTES)
    selected_day = forms.CharField(widget=forms.HiddenInput)