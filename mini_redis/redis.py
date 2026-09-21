# mini_redis/redis.py

import time

from entry import Entry
from hashmap import HashMap
from linked_list import DoublyLinkedList
from heap import MinHeap
from pubsub import PubSub


class MiniRedis:
    def __init__(self):
        self.store = HashMap()
        self.lru = DoublyLinkedList()
        self.ttl_heap = MinHeap()

        self.maxmemory = 0
        self.used_memory = 0
        self.evicted_keys = 0

        self.pubsub = PubSub()
        self.client_id = "cli"

    def execute(self, args):
        if not args:
            return ""

        command = args[0].upper()

        commands = {
            "SET": self._set,
            "GET": self._get,
            "DEL": self._del,
            "EXISTS": self._exists,
            "DBSIZE": self._dbsize,
            "KEYS": self._keys,
            "CONFIG": self._config,
            "INFO": self._info,
            "EXPIRE": self._expire,
            "TTL": self._ttl,
            "PUBLISH": self._publish,
            "SUBSCRIBE": self._subscribe,
        }

        handler = commands.get(command)

        if handler is None:
            return f"(error) ERR unknown command '{args[0]}'"

        try:
            return handler(args[1:])
        except ValueError:
            return "(error) ERR value is not an integer or out of range"

    def _check_args(self, args, count, command):
        if len(args) != count:
            return (
                f"(error) ERR wrong number of arguments "
                f"for '{command.lower()}' command"
            )

        return None

    def _set(self, args):
        error = self._check_args(args, 2, "SET")
        if error:
            return error

        key, value = args

        new_size = len(key.encode("utf-8")) + len(value.encode("utf-8"))

        if self.maxmemory > 0 and new_size > self.maxmemory:
            return (
                "(error) OOM command not allowed when "
                "used_memory > 'maxmemory'"
            )

        self._purge_expired()

        old_entry = self.store.get(key)

        if old_entry is not None:
            self._remove_entry(old_entry)

        entry = Entry(key, value)
        self.store.put(key, entry)

        entry.lru_node = self.lru.insert_front(entry)

        self.used_memory += entry.memory_size()

        self._evict_if_needed()

        return "OK"

    def _get(self, args):
        error = self._check_args(args, 1, "GET")
        if error:
            return error

        key = args[0]

        if self._check_expired(key):
            return "(nil)"

        entry = self.store.get(key)

        if entry is None:
            return "(nil)"

        self.lru.move_to_front(entry.lru_node)

        return f'"{entry.value}"'

    def _del(self, args):
        error = self._check_args(args, 1, "DEL")
        if error:
            return error

        key = args[0]

        if self._check_expired(key):
            return "(integer) 0"

        entry = self.store.get(key)

        if entry is None:
            return "(integer) 0"

        self._remove_entry(entry)

        return "(integer) 1"

    def _exists(self, args):
        error = self._check_args(args, 1, "EXISTS")
        if error:
            return error

        key = args[0]

        if self._check_expired(key):
            return "(integer) 0"

        return f"(integer) {1 if self.store.contains(key) else 0}"

    def _dbsize(self, args):
        error = self._check_args(args, 0, "DBSIZE")
        if error:
            return error

        self._purge_expired()

        return f"(integer) {self.store.size()}"

    def _keys(self, args):
        error = self._check_args(args, 0, "KEYS")
        if error:
            return error

        self._purge_expired()

        keys = self.store.keys()

        if not keys:
            return "(empty array)"

        return "\n".join(
            f'{i}. "{key}"'
            for i, key in enumerate(keys, 1)
        )

    def _config(self, args):
        if len(args) != 3 or args[0].upper() != "SET":
            if len(args) == 0:
                return (
                    "(error) ERR wrong number of arguments "
                    "for 'config' command"
                )

            return (
                "(error) ERR wrong number of arguments "
                "for 'config' command"
            )

        if args[1].lower() != "maxmemory":
            return f"(error) ERR unknown configuration parameter '{args[1]}'"

        try:
            value = int(args[2])

            if value < 0:
                raise ValueError

        except ValueError:
            return "(error) ERR value is not an integer or out of range"

        self.maxmemory = value

        return "OK"

    def _info(self, args):
        if len(args) != 1 or args[0].lower() != "memory":
            return "(error) ERR wrong number of arguments for 'info' command"

        self._purge_expired()

        return (
            f"used_memory:{self.used_memory}\n"
            f"maxmemory:{self.maxmemory}\n"
            f"evicted_keys:{self.evicted_keys}"
        )

    def _expire(self, args):
        error = self._check_args(args, 2, "EXPIRE")
        if error:
            return error

        key = args[0]

        try:
            seconds = int(args[1])
        except ValueError:
            return "(error) ERR value is not an integer or out of range"

        if self._check_expired(key):
            return "(integer) 0"

        entry = self.store.get(key)

        if entry is None:
            return "(integer) 0"

        if seconds <= 0:
            self._remove_entry(entry)
            return "(integer) 1"

        entry.expire_at = time.time() + seconds
        self.ttl_heap.push((entry.expire_at, key))

        return "(integer) 1"

    def _ttl(self, args):
        error = self._check_args(args, 1, "TTL")
        if error:
            return error

        key = args[0]

        if self._check_expired(key):
            return "(integer) -2"

        entry = self.store.get(key)

        if entry is None:
            return "(integer) -2"

        if entry.expire_at is None:
            return "(integer) -1"

        remaining = int(entry.expire_at - time.time())

        if remaining < 0:
            self._remove_entry(entry)
            return "(integer) -2"

        return f"(integer) {remaining}"

    def _publish(self, args):
        error = self._check_args(args, 2, "PUBLISH")
        if error:
            return error

        channel, message = args
        count = self.pubsub.publish(channel, message)

        return f"(integer) {count}"

    def _subscribe(self, args):
        error = self._check_args(args, 1, "SUBSCRIBE")
        if error:
            return error

        channel = args[0]
        count = self.pubsub.subscribe(self.client_id, channel)

        return f"subscribe {channel} {count}"

    def _check_expired(self, key):
        entry = self.store.get(key)

        if entry is None:
            return True

        if entry.expire_at is None:
            return False

        if entry.expire_at <= time.time():
            self._remove_entry(entry)
            return True

        return False

    def _purge_expired(self):
        now = time.time()

        while self.ttl_heap.size() > 0:
            item = self.ttl_heap.peek()
            expire_at, key = item

            if expire_at > now:
                break

            self.ttl_heap.pop()

            entry = self.store.get(key)

            if entry is None:
                continue

            if entry.expire_at != expire_at:
                continue

            self._remove_entry(entry)

    def _remove_entry(self, entry):
        self.store.remove(entry.key)

        if entry.lru_node is not None:
            self.lru.remove_node(entry.lru_node)
            entry.lru_node = None

        self.used_memory -= entry.memory_size()

        if self.used_memory < 0:
            self.used_memory = 0

        entry.expire_at = None

    def _evict_if_needed(self):
        if self.maxmemory == 0:
            return

        while self.used_memory > self.maxmemory:
            entry = self.lru.remove_back()

            if entry is None:
                break

            self.store.remove(entry.key)

            self.used_memory -= entry.memory_size()

            if self.used_memory < 0:
                self.used_memory = 0

            entry.lru_node = None
            entry.expire_at = None

            self.evicted_keys += 1