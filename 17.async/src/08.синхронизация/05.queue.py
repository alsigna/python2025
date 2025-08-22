import asyncio

pq = asyncio.PriorityQueue()
fifo = asyncio.Queue()
lifo = asyncio.LifoQueue()


async def pq_demo() -> None:
    # await pq.put((2, "C"))
    # await pq.put((1, "A"))
    # await pq.put((1, "B"))
    # await pq.put((3, "D"))

    await pq.put("C")
    await pq.put("A")
    await pq.put("B")
    await pq.put("D")

    print(await pq.get())
    print(await pq.get())
    print(await pq.get())
    print(await pq.get())


async def fifo_demo() -> None:
    await fifo.put("A")
    await fifo.put("B")
    await fifo.put("C")
    await fifo.put("D")

    print(await fifo.get())
    print(await fifo.get())
    print(await fifo.get())
    print(await fifo.get())


async def lifo_demo() -> None:
    await lifo.put("D")
    await lifo.put("C")
    await lifo.put("B")
    await lifo.put("A")

    print(await lifo.get())
    print(await lifo.get())
    print(await lifo.get())
    print(await lifo.get())


async def main():
    print("= PQ =")
    await pq_demo()
    print("= FIFO =")
    await fifo_demo()
    print("= LIFO =")
    await lifo_demo()


asyncio.run(main())
