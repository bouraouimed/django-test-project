import requests

def demo_synchronize_script():
    """
    This is a sample script that consumes an external API
    """
    response = requests.get('http://jsonplaceholder.typicode.com/todos')
    if response.ok:
        return response
    else:
        return None
