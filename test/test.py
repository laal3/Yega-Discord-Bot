import inspect
import os
from os import listdir

def get_name(func):
    
    print(func.__name__)
        
    return func
    

@get_name
def yee():
    print(listdir(os.path.dirname("/permissions")))