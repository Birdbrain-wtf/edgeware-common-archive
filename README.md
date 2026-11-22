# Edgeware Common archive

An unofficial preservation copy of public Edgeware discussions hosted on Common, formerly Commonwealth. Original authors retain their rights. This repository grants no new licence over their posts. It is maintained by Birdbrain and is not an official Edgeware or Common publication.

Status: incomplete. See `manifest.json` for verified coverage. The API reported 986 threads, but pagination yielded 977 unique IDs. This discrepancy remains unresolved. Full post bodies are in `bodies/`. `inventory.json` contains API previews, which truncate longer bodies at 2,000 characters. Downloaded comments and replies are in `comments/`. Common returned HTTP 429 before all comments could be saved. Images and attachments remain external links and are not backed up here. Deleted or private material is not recovered.

The original discussion URL for an ID is `https://common.xyz/edgeware/discussion/<id>`. The inventory retains author names, timestamps and full-content URLs. Source text is preserved without editorial rewriting.

## Kabocha funding finding

Checked on 22 November 2026 against Kabocha's live `System.Account` storage: the account derived from `modlpy/edgtr`, `3jjJHkxfyMRjbkdPpPkfi7Z9JPE9zuq9BKd8rf3jvfgPmzV6`, holds 817,730 KAB free, with none reserved. This is about 1.056% of the observed 77,449,609.04 KAB supply. It is distinct from Kabocha's own treasury account, derived from `modlpy/trsry`.

Thread 3806, “Kabocha: Edgeware grants and recoup”, proposes repaying Edgeware's Kabocha grants at the snapshot ratio, after redenomination: 100 EDG equals 1 KAB. Its worked example converts 2,894,736 EDG to 28,947.36 KAB. Thread 6007 describes the treasury provision for this recoup. These explain the intended allocation, but do not prove the complete grant total, historical transfers or current spending authority. The 817,730 KAB balance should not be described as all KAB held by Edgeware holders.

Funding sources:

- https://common.xyz/edgeware/discussion/2363
- https://common.xyz/edgeware/discussion/3806
- https://common.xyz/edgeware/discussion/6007
- Live chain: https://kabocha-rpc.birdbrain.wtf

## Repeating the capture

`archive.py` requires Python and `curl_cffi`. It resumes from `inventory.json`, skips completed comment captures and fetches full bodies separately from API previews. Observe Common's rate limits. Review coverage before calling any capture complete. `SHA256SUMS` records the captured files for this revision.
