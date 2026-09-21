<!-- mini_redis/STACK_QUEUE_DEQUE.md -->

# Stack / Queue / Deque

## Stack

LIFO(Last In, First Out) 구조이다.

- push: 데이터 삽입
- pop: 마지막 데이터 삭제
- peek: 마지막 데이터 조회

연결 리스트의 앞쪽에서 삽입과 삭제를 수행하면 O(1)로 구현할 수 있다.

## Queue

FIFO(First In, First Out) 구조이다.

- enqueue: 데이터 삽입
- dequeue: 데이터 삭제
- front: 가장 먼저 들어온 데이터 조회

연결 리스트의 뒤쪽에 삽입하고 앞쪽에서 삭제하면 O(1)로 구현할 수 있다.

## Deque

Double Ended Queue의 약자로 양쪽 끝에서 삽입과 삭제가 가능한 자료구조이다.

- 앞쪽 삽입
- 뒤쪽 삽입
- 앞쪽 삭제
- 뒤쪽 삭제

이중 연결 리스트를 이용하면 주요 연산을 O(1)로 구현할 수 있다.

## 관계

```text
Stack
→ 한쪽에서 삽입/삭제

Queue
→ 한쪽에서 삽입, 반대쪽에서 삭제

Deque
→ 양쪽에서 삽입/삭제