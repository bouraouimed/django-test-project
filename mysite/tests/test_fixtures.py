import pytest
import datetime
from django.utils import timezone

from polls.models import *

@pytest.fixture
def create_question_object(days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text="question_text", pub_date=time)
