# Function to handle websocket connections
async def websocket_application(scope, receive, send):
    """Function to handle websocket connections

    Args:
        scope (dict): Scope of the connection.
        receive (function): Function to receive events.
        send (function): Function to send events.
    """

    # Loop to handle websocket events
    while True:
        # Receive event
        event = await receive()

        # If event is connection event
        if event["type"] == "websocket.connect":
            # Accept the connection
            await send({"type": "websocket.accept"})

        # If event is disconnect event
        if event["type"] == "websocket.disconnect":
            # Break the loop
            break

        # If event is receive event
        if event["type"] == "websocket.receive":
            # If text is ping
            if event["text"] == "ping":
                # Send pong
                await send({"type": "websocket.send", "text": "pong!"})
