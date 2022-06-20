import pytest
import datetime
from django.utils import timezone

from polls.models import *

@pytest.fixture
def create_question_object(days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text="question_text", pub_date=time)

@pytest.fixture
def create_todos_list():
    return [
        {
            'userId': 1,
            'id': 1,
            'title': 'Poll Test',
            'completed': False 
        }
    ]

@pytest.fixture
def valid_question_object():
    return {
        "question_text": "Test Question 2",
        "pub_date": "2022-05-25T03:12:08Z"
    }

@pytest.fixture
def non_valid_question_object():
    return {
        "pub_date": "2022-05-25T03:12:08Z"
    } 