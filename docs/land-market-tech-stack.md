# Land Market: How the Tech Stack Works

A plain-language guide for team members. It explains what each part of the system does and how a request moves through it.

---

## The Big Picture

Land Market lets citizens list, buy and sell land. Every trade is checked automatically, and the result is recorded on a public blockchain so anyone can verify it.

The system has **5 layers**, plus the **Government Portals** that supply official data:

| Layer | Name | Job in one line |
|-------|------|-----------------|
| 1 | Users | The people who use the system |
| 2 | Frontend | The screens people see and tap |
| 3 | Backend | The brain: runs checks, stores data |
| 4 | TinyFish | An automated agent that fetches official data from government websites |
| – | Government Portals | The official sources of land records (7 portals; demo data in the prototype) |
| 5 | Blockchain | The permanent, public record and the escrow |

---

## Layer by Layer

### Layer 1: Users
- **Land Owner / Buyer (Citizen):** Browses the map, places buy or sell orders.
- **Government Officer:** Enters a land parcel's **ULPIN** (the unique land parcel ID) to start verification of that land.

### Layer 2: Frontend
- Built with **React + TypeScript + MapLibre**.
- Handles ULPIN login, KYC + OTP (identity verification), the interactive map, the Market screen and the order screen.
- It does not make decisions. It collects input and sends it to the backend with `fetch()` API calls.

### Layer 3: Backend
- Built with **FastAPI (Python)**.
- Contains the **Hardcoded Trade Rules (no AI)**. These are fixed rules, so the result is predictable and auditable. Every trade runs through **6 checks**:
  1. **Listed?** Is the land officially listed?
  2. **Bundle intact?** Is the land bundle complete and unchanged?
  3. **KYC wallet?** Is the user's wallet identity-verified?
  4. **Zoning OK?** Does the zoning allow this use or trade?
  5. **Funds in escrow?** Is the buyer's money locked in escrow?
  6. **Match?** Does the buy order match the sell order?
- Stores everything in **PostgreSQL + PostGIS** (a database with map/location support): the ALU grid, bundles, the order book and evidence records.

### Layer 4: TinyFish
An automation service the backend uses to gather official information. It has three tools:
- **Web Agent:** Opens the government portals and navigates them like a person would.
- **Fetch:** Pulls the page data (zoning info and PDF documents).
- **Search:** Looks up reference rates (for example, standard land values).

### Government Portals
- 7 official portals hold the land data.
- **In the prototype, these use demo data, not live government records.**

### Layer 5: Blockchain
- A **Solidity smart contract** on a **testnet** (a practice network, not real money).
- Handles **escrow** (holding the buyer's funds), **`settle()`** (completing the trade), **events**, and the **evidence hash** (a fingerprint of the evidence sheet).
- Writes to a **Public Audit Trail** that anyone can verify.

---

## Flow A: Verifying a Land Parcel

*Triggered by a Government Officer. This decides whether land can be listed.*

| Step | What happens |
|------|--------------|
| **A1** | Officer enters the **ULPIN** in the frontend. |
| **A2** | Frontend sends it to the backend via an API call. |
| **A3** | Backend gives TinyFish a goal **in plain English** (e.g., "check zoning for this parcel"). |
| **A4** | TinyFish's Web Agent **opens the government portals**. |
| **A5a** | **Fetch** pulls zoning data and PDFs from the portals. |
| **A5b** | **Search** pulls reference rates. |
| **A6** | TinyFish returns **structured JSON** (clean, organized data) to the backend. |
| **A7** | Backend saves a **21-field evidence sheet** to the database. |

### The Decision: "Clean result?"
- **Yes:** **Auto-pass.** The land can be listed.
- **No** (CAPTCHA blocked, data mismatch, or missing data): the case goes to the **Human Officer Queue** for manual review.

---

## Flow B: Placing and Settling a Trade

*Triggered by a Citizen. This is how a trade actually happens.*

| Step | What happens |
|------|--------------|
| **B1** | Citizen taps **Market** and **places an order**. |
| **B2** | Frontend sends the order to the backend via an API call. |
| **B3** | Backend **runs the 6 checks** (Listed, Bundle intact, KYC wallet, Zoning OK, Funds in escrow, Match). |
| **B4** | If all pass, the backend calls **`settle()`** on the smart contract. |
| **B5** | The contract emits an **event + evidence hash** to the **Public Audit Trail**. |
| **B6** | The **transaction hash** is returned to the backend, then **shown to the user** as proof. |

---

## Key Points to Remember

1. **No AI makes trade decisions.** The 6 checks are fixed, hardcoded rules. TinyFish only *gathers data*.
2. **Humans stay in the loop.** Anything unclear (CAPTCHA, mismatch, gap) goes to a human officer.
3. **Everything is auditable.** Each trade leaves an evidence sheet in the database and a hash on the blockchain.
4. **This is a prototype.** Government data is demo data and the blockchain is a testnet.

---

## Quick Glossary

| Term | Meaning |
|------|---------|
| **ULPIN** | Unique Land Parcel Identification Number |
| **KYC** | Know Your Customer, identity verification |
| **OTP** | One-time password sent to the user's phone |
| **Escrow** | Funds held safely until the trade completes |
| **Smart contract** | Code on a blockchain that runs automatically and cannot be quietly altered |
| **Testnet** | A practice blockchain network with no real money |
| **Evidence hash** | A digital fingerprint proving the evidence sheet hasn't been changed |
| **Transaction hash** | A unique receipt ID for a blockchain transaction |
| **PostGIS** | A database extension that stores map and location data |
| **ALU grid** | The land-unit grid used to divide land in the system (confirm exact definition with the tech lead) |
