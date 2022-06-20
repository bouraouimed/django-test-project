import datetime
from django.utils import timezone
from polls.models import Question
from test_fixtures import *
from django.test import TestCase
from django.urls import reverse
from unittest.mock import Mock, patch
from polls.synchronize import demo_synchronize_script

def test_was_published_recently_with_future_question():
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(minutes=30)
        future_question = Question(pub_date=time)
        assert future_question.was_published_recently() == False

def test_was_published_recently_with_old_question():
    """
    was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    assert old_question.was_published_recently() == False

def test_was_published_recently_with_recent_question():
    """
    was_published_recently() returns True for questions whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    assert recent_question.was_published_recently() ==  True

@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('days', [30])
def test_created_question(create_question_object):
    assert create_question_object.question_text != ""

@pytest.mark.django_db(transaction=True)
def test_get_empty_questions_list(client):
    response = client.get('/polls/api/questions/')
    assert response.status_code == 200
    assert len(response.data) == 0

@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('days', [0])
def test_get_non_empty_questions_list(client,create_question_object):
    response = client.get('/polls/api/questions/')
    assert response.status_code == 200
    assert len(response.data) > 0

@pytest.mark.django_db(transaction=True)
def test_valid_post_question(client,valid_question_object):
    response = client.post(
        '/polls/api/questions/',
        data=valid_question_object,
        content_type='application/json' 
    )
    assert response.status_code == 201

@pytest.mark.django_db(transaction=True)
def test_non_valid_post_question(client,non_valid_question_object):
    response = client.post(
        '/polls/api/questions/',
        data=non_valid_question_object,
        content_type='application/json' 
    )
    assert response.status_code == 400

@patch('polls.synchronize.requests.get')
def test_get_todos_response_ok(mock_get,create_todos_list):
    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = create_todos_list

    # Call the service, which will send a request to the server.
    response = demo_synchronize_script()

    # If the request is sent successfully, then I expect a response to be returned.
    assert response != None
    assert len(response.json()) > 0


@patch('polls.synchronize.requests.get')
def test_get_todos_response_ko(mock_get):
    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = False

    # Call the service, which will send a request to the server.
    response = demo_synchronize_script()

    # If the request is sent successfully, then I expect a response to be returned.
    assert response == None
