# We want to design a GPU credit system for employees. Each employee can receive
# GPU credits and spend them later. Credits have expiration times.
# The system must support three core operations:
# 	1.	Grant credits
# 	•	Add some number of credits to an employee.
# 	•	Each grant comes with an expiration time.
# 	2.	Spend credits
# 	•	An employee uses some number of credits.
# 	•	Expired credits cannot be used.
# 	3.	Query balance at a given time
# 	•	Ask: “What is this employee’s available credit balance at time T?”
# 	•	The balance should consider:
# 	•	All grants and spends that happened on or before T.
# 	•	Credit expiration (expired grants no longer count).
#
# Additional constraints:
# 	•	Every operation (grant, spend, query) has a timestamp.
# 	•	The system must apply operations strictly in timestamp order, not arrival order.
# 	•	Requests can arrive in any order, but logical processing must follow time.
# 	•	Once credits are expired at time T, they are no longer usable for spends at or after T.
#
# The two tricky parts are:
# 	1.	If a user tries to spend more credits than they currently have at that time, we create a “debt”:
# 	•	The user’s logical balance becomes negative.
# 	•	Future credit grants must first pay off this debt before increasing their usable balance.
# 	2.	For multiple operations with the same timestamp:
# 	•	Spending happens before granting at that timestamp.
# 	•	So at time t, you must apply:
# 	1.	All spends at t,
# 	2.	Then all grants at t.
# 	•	This is easy to overlook but changes the outcome.
# Interfaces:
# grant(user, amount, expiry, timestamp)
# spend(user, amount, timestamp)
# query(user, timestamp)

# Overall Ideas
# 1. Sort all events by timestamp ASC (if timestamp ties, SPEND > GRANT > QUERY)
#    - Reject expired events
# 2. Apply operations in sequence
# 3. For each user, maintain a state:
#    - debt (>=0): a sum of credits overspent historically
#    - active_credits: a min-heap ordered by expiry_time of non-expired credit “lots” (amount_remaining, expiry_time)
#    - balance = sum(active_credits) - debt

