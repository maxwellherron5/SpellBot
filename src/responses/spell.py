"""
"""

import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

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
        return "\n".join(msg)
    
    def build_output(self):
        msg = []
        for field in self.__dict__:
            self.__dict__[field] = str(self.__dict__[field]).strip('\n')
            msg.append(f"**{field}**\n{self.__dict__[field]}\n")
        final_message = ""
        messages_extended = []
        for field in msg:
            if len(final_message + field) < 2000:
                final_message += field
            elif len(field) > 2000:
                messages_extended.append(final_message)
                messages_extended.extend([field[i:i+2000] for i in range(0, len(field), 2000)])
                final_message = ""
            else:
                messages_extended.append(final_message)
                final_message = ""
        if final_message:
            messages_extended.append(final_message)
        return messages_extended
