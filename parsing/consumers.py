from channels import Group

# Channels consumers


def ws_connect(message):
    """Add client to group on connect"""
    Group('pool').add(message.reply_channel)


def ws_disconnect(message):
    """Remove client from group on disconnect"""
    Group('pool').discard(message.reply_channel)
