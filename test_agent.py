from agent import respond, close_clients


print("\n--- CUSTOMER A ---")

response = respond(
    "rahul",
    "Hi, my FastAPI application is having timeout problems."
)

print("\nRecallDesk:")
print(response)


print("\n--- CUSTOMER A FOLLOW-UP ---")

response = respond(
    "rahul",
    "What framework am I using?"
)

print("\nRecallDesk:")
print(response)


print("\n--- CUSTOMER B ---")

response = respond(
    "priya",
    "What framework am I using?"
)

print("\nRecallDesk:")
print(response)

close_clients()