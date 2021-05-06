"""
"""

class Spell:
    """
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        output_str = ""
        for prop in self.__dict__:
            output_str += f"{prop}: {self.__dict__[prop]}"
        return output_str
