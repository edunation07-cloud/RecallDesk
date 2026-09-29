from agent import respond, close_clients


def test(customer_id, message):
    print("\n" + "=" * 60)
    print(f"CUSTOMER: {customer_id}")
    print(f"MESSAGE: {message}")
    print("=" * 60)

    answer = respond(customer_id, message)

    print("\nRecallDesk:")
    print(answer)


# --------------------------------
# CUSTOMER 1 — TECHNICAL SUPPORT
# --------------------------------

test(
    "rahul",
    "My FastAPI application is having timeout problems."
)

test(
    "rahul",
    "What framework am I using?"
)


# --------------------------------
# CUSTOMER 2 — PAYMENT
# --------------------------------

test(
    "priya",
    "My payment failed while purchasing a subscription."
)

test(
    "priya",
    "What problem did I have earlier?"
)


# --------------------------------
# CUSTOMER 3 — LOGIN
# --------------------------------

test(
    "arjun",
    "I cannot log into my account because I forgot my password."
)

test(
    "arjun",
    "What issue was I having?"
)


# --------------------------------
# UNKNOWN INFORMATION TEST
# --------------------------------

test(
    "meera",
    "What was my previous order number?"
)


close_clients()

print("\n")
print("=" * 60)
print("ALL SCENARIOS COMPLETED")
print("=" * 60)