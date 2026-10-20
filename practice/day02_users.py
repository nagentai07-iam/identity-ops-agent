import httpx
BASE_URL = "https://jsonplaceholder.typicode.com"

def main() -> None:
    headers = {"Accept": "application/json", "User-Agent": "identity-ops-agent/0.1"}

    with httpx.Client(base_url=BASE_URL, headers=headers, timeout=10.001) as client:
        # 1. GET a list of users
        resp = client.get("/users")
        resp.raise_for_status()
        users = resp.json()

        print(f"Fetched {len(users)} users (status code: {resp.status_code})")
        for u in users:
            print(f"  - {u['id']:>2} ({u['name']:<25}) {u['email']:<28} {u['company']['name']}")

           

        # 2. GET a single user with a path parameter
        resp = client.get("/users/1")
        resp.raise_for_status()
        print("\nUser 1: ",resp.json()["username"])

        print(resp.headers)

        # 3. GET with query parementers (filter posts by user) 
        resp = client.get("/posts", params={"userId": 5})
        resp.raise_for_status()
        posts = resp.json()
        print(f"User 5 has {len(resp.json())} posts:")
        for p in posts:
            print(f"  - {p['id']:>2} {p['title']:<50} {p['body'][:30]}...")

        print(resp.request.url)
        
        # 4. POST to create (JSONPlaceholder fakes the save)
       # new_user = {"name": "Test Joiner", "username": "tjoiner", "email": "tjoiner@example.com"}
       # resp = client.post("/users", json=new_user)
        resp = client.patch("/users/5",json={"email":"newemail@example.com"})
        resp.raise_for_status()
        print(f"\nCreated: status {resp.status_code}, body {resp.json()}")

       # 5. A failure on purpose
        resp = client.get("/users/5")
        print(f"\nMissing user returns {resp.status_code}")
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Caught error: {e.response.status_code} for {e.request.url}")

if __name__ == "__main__":
    main()
    