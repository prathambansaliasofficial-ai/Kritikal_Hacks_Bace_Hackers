import { network } from "hardhat";

const { ethers } = await network.create();
const [operator, buyer, seller] = await ethers.getSigners();

const ORDER_ID = ethers.id("SMOKE-ORDER-" + Date.now());
const EVIDENCE_HASH = ethers.id("smoke-evidence-sheet");
const AMOUNT = 10_000_000_000_000_000n;

console.log(`Deploying fresh LandMarketEscrow (operator ${operator.address})`);
const factory = await ethers.getContractFactory("LandMarketEscrow");
const escrow = (await factory.deploy(operator.address)) as any;
await escrow.waitForDeployment();
const address = await escrow.getAddress();
console.log(`Escrow at ${address}`);

const sellerBefore = await ethers.provider.getBalance(seller.address);

await escrow
  .connect(buyer)
  .createOrder(ORDER_ID, seller.address, EVIDENCE_HASH, { value: AMOUNT });

const stateAfterCreate = Number(await escrow.orderState(ORDER_ID));
console.log(`orderState after createOrder: ${stateAfterCreate}`);
if (stateAfterCreate !== 1) {
  throw new Error(`Expected Funded(1), got ${stateAfterCreate}`);
}

await escrow.connect(operator).settle(ORDER_ID);

const stateAfterSettle = Number(await escrow.orderState(ORDER_ID));
console.log(`orderState after settle: ${stateAfterSettle}`);
if (stateAfterSettle !== 2) {
  throw new Error(`Expected Settled(2), got ${stateAfterSettle}`);
}

const sellerAfter = await ethers.provider.getBalance(seller.address);
console.log(`seller balance change: ${(sellerAfter - sellerBefore).toString()} wei`);
if (sellerAfter <= sellerBefore) {
  throw new Error("Seller balance did not increase after settle");
}

console.log("chain smoke: PASS");
