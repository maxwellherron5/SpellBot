"""
"""

class Spell:
    """
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        msg = []
        # Populating embedded message with all returned fields
        for field in self.__dict__:
            self.__dict__[field] = str(self.__dict__[field]).strip('\n')
            msg.append(f"**{field}**\n{self.__dict__[field]}")
        msg.append("\n...anything look weird here? Let me know!")
        msg = '\n'.join(msg)
        return msg
