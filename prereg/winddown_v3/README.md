# Pre-registration: out-of-sample wind-down vocabulary (v3)

The wind-down vocabulary used in Finding 05 (v1/v2) was written after reading GM's filings and
was never frozen, so its rise in GM's robotaxi passages is descriptive, not independent evidence.
v3 replaces it with a list derived only from three non-GM exits from autonomous-vehicle
businesses: Uber's sale of ATG to Aurora, Lyft's sale of Level 5 to Woven Planet, and Ford's
exit from Argo AI.

Order of record (each step is a separate commit or a server-timestamped message):

1. This folder: the protocol for deriving the list (`PHASE_A.md`) and the plan for applying it
   and for re-testing the Finding 05 breakpoint (`PHASE_BC.md`), committed before anything ran.
2. A Desktop session that never receives GM results or the old list follows `PHASE_A.md`
   (fetched from this commit and checked by sha256), freezes the list, commits it locally and
   posts the commit SHA, hash and full file in the project thread.
3. The frozen file is mirrored here, byte-identical, before any GM scoring starts.
4. A separate session applies the frozen list to GM following `PHASE_BC.md`. The list is not
   edited after this point. If it does not fire on GM, that is the published result.
