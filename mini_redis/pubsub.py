# mini_redis/pubsub.py

class PubSub:
    def __init__(self):
        self.channels = {}

    def subscribe(self, client_id, channel):
        subscribers = self.channels.get(channel)

        if subscribers is None:
            subscribers = []
            self.channels[channel] = subscribers

        if client_id not in subscribers:
            subscribers.append(client_id)

        return len(subscribers)

    def unsubscribe(self, client_id, channel):
        subscribers = self.channels.get(channel)

        if subscribers is None:
            return False

        if client_id not in subscribers:
            return False

        subscribers.remove(client_id)

        if not subscribers:
            del self.channels[channel]

        return True

    def publish(self, channel, message):
        subscribers = self.channels.get(channel)

        if subscribers is None:
            return 0

        return len(subscribers)

    def subscribers(self, channel):
        subscribers = self.channels.get(channel)

        if subscribers is None:
            return []

        return subscribers[:]