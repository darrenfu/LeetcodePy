# Problem Statement: Implement a distributed lock using Redis that can be used
# to coordinate access to shared resources across multiple processes/machines.
# The lock should support timeout and automatic release.
#
# A Redis-backed distributed lock to coordinate access to shared resources
# across multiple processes and machines.
# Key properties:
# 	•	Provide mutual exclusion (only one holder at a time)
# 	•	Auto-release if the holder dies (via TTL)
# 	•	Support acquisition timeout (client gives up after some time)
# 	•	Be reasonably safe under common failure modes (GC pauses, process crash,
# network blips)
#
# Problem:
# We want a coarse-grained coordination primitive so multiple processes/machines
# can serialize access to some shared resource (e.g. running a maintenance job,
# updating a shared structure, doing a migration).
#
# GOTCHA:
# Redis uses Lua scripts for lock release because Redis itself doesn’t expose a
# built-in atomic primitive to compare a stored token and delete a key. A
# release operation must atomically check ownership and delete the key;
# otherwise, a client could accidentally delete another client’s lock in race
# conditions involving TTL expiration and re-acquisition. Lua scripts provide
# an easy, extensible way to compose multi-step operations atomically with
# strong replication semantics and without introducing new commands or API
# complexity into Redis.
#
# SET key value NX PX ttl (a mutual exclusion + TTL in a single atomic op)
# •	NX → only succeed if key does not exist (mutex).
# •	PX ttl → set TTL automatically (auto-release).
# Lua script - Check that I still own the lock” + “delete/extend it
# ```
# if redis.call("get",KEYS[1]) == ARGV[1]
#     then
# return redis.call("del",KEYS[1])
# else
# return 0
# end
# ```
#
# Core idea #1: Each acquisition has a unique identity (token)
# Critical design choice:
# the lock value is not just “locked” – it’s a unique token.
# Why?
# Without a token, if client A holds the lock and its TTL expires just as A
# tries to release it, and client B acquires in the meantime:
# >> A’s naive DEL key would delete B’s lock → corruption.
#
# Core idea #2: Lock lifecycle is 3 phases
# Lock has a simple lifecycle:
# Acquire > Hold > Release or timeout
#
# Core idea #3: Use TTL as the safety valve, not as a precise clock
#
# Redis gives you pragmatic, best-effort mutual exclusion, not linearizable,
# durable, fencing-safe locks.
# To achieve formally correct distributed locks, you need a system built on
# consensus (Raft/Paxos), persistent ordering, and fencing semantics.
#
# Persistent ordering
# It means that all operations (like acquiring a lock) are
# written into a replicated, durable, totally ordered log that all nodes agree
# on. Every operation has a globally consistent position in the log (log index or
# term), and this order survives failures, restarts, and failovers.
#
# Fencing semantics
# It means that every successful lock acquisition returns a monotonically
# increasing sequence number (fencing token). Any resource guarded by the lock
# must reject operations that come with an older token.

# TODO