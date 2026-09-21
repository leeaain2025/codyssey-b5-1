# mini_redis/main.py

from parser import parse_command
from redis import MiniRedis


def main():
    redis = MiniRedis()

    while True:
        try:
            line = input("mini-redis> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line.strip():
            continue

        args = parse_command(line)

        if args is None:
            print("(error) ERR syntax error")
            continue

        if not args:
            continue

        command = args[0].lower()

        if command in ("exit", "quit"):
            break

        result = redis.execute(args)

        if result:
            print(result)


if __name__ == "__main__":
    main()