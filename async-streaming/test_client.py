import httpx
import asyncio

BASE_URL = "http://localhost:8000"

#test1---Regular Async Chat---
async def test_regular():
    print("===Regular Async Chat===")
    async with httpx.AsyncClient() as client:
        response=await client.post(
            f"{BASE_URL}/chat",
            json={"message":"What is FastAPI in one sentence?"},
            timeout=30

        )

        data=response.json()
        print(data["response"])
        print(f"Tokens Used:{data['usage']}")


#test2---Streaming Chat---
async def test_streaming():
    print("\n===Streaming Chat===")
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{BASE_URL}/chat/stream",
            json={"message":"Explain async programming in 3 sentences."},
            timeout=30

        ) as response:
            async for chunk in response.aiter_text():
                print(chunk,end="",flush=True)
    print("\n")

async def main():
    await test_regular()
    await test_streaming() 

asyncio.run(main())                           