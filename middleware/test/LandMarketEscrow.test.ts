import { expect } from "chai";
import type { Contract, ContractTransactionResponse, Signer } from "ethers";
import { Wallet } from "ethers";
import { network } from "hardhat";
import { getOrderState, refundOrder, settleOrder } from "../src/blockchain/escrow.js";

type EscrowContract = {
  interface: Contract["interface"];
  waitForDeployment(): Promise<unknown>;
  getAddress(): Promise<string>;
  connect(signer: Signer): EscrowContract;
  createOrder(
    orderId: string,
    seller: string,
    evidenceHash: string,
    overrides: { value: bigint },
  ): Promise<ContractTransactionResponse>;
  settle(orderId: string): Promise<ContractTransactionResponse>;
  refund(orderId: string): Promise<ContractTransactionResponse>;
  orderState(orderId: string): Promise<bigint>;
};

// Hardhat local chain account #0 (dev key only, never mainnet).
const OPERATOR_DEV_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80";

describe("middleware escrow functions", function () {
  this.timeout(60_000);

  async function deployWithOperator() {
    const { ethers } = await network.create();
    const signers = await ethers.getSigners();
    const operatorWallet = new Wallet(OPERATOR_DEV_KEY, ethers.provider);
    expect(operatorWallet.address).to.equal(signers[0].address);

    const factory = await ethers.getContractFactory("LandMarketEscrow");
    const escrow = (await factory.deploy(operatorWallet.address)) as unknown as EscrowContract;
    await escrow.waitForDeployment();

    const address = await escrow.getAddress();
    const buyer = signers[1];
    const seller = signers[2];

    process.env.ESCROW_CONTRACT_ADDRESS = address;
    process.env.OPERATOR_PRIVATE_KEY = OPERATOR_DEV_KEY;

    return { ethers, escrow, operatorWallet, buyer, seller, address };
  }

  it("reads orderState through getOrderState: None -> Funded -> Settled", async function () {
    const { ethers, escrow, buyer, seller } = await deployWithOperator();
    const orderId = ethers.id("ORDER-STATUS-1");
    const evidenceHash = ethers.id("evidence-sheet-status-1");
    const amount = ethers.parseEther("1");

    await expect(
      escrow.connect(buyer).createOrder(orderId, seller.address, evidenceHash, { value: amount }),
    ).to.emit(escrow, "OrderCreated");

    const before = await getOrderState(orderId, ethers.provider);
    expect(before.state).to.equal(1);
    expect(before.label).to.equal("Funded");

    await settleOrder(orderId, ethers.provider);

    const after = await getOrderState(orderId, ethers.provider);
    expect(after.state).to.equal(2);
    expect(after.label).to.equal("Settled");
    expect(after.orderId).to.equal(orderId);
  });

  it("refund moves order to Refunded", async function () {
    const { ethers, escrow, buyer, seller } = await deployWithOperator();
    const orderId = ethers.id("ORDER-STATUS-2");
    const evidenceHash = ethers.id("evidence-sheet-status-2");
    const amount = ethers.parseEther("0.5");

    await escrow
      .connect(buyer)
      .createOrder(orderId, seller.address, evidenceHash, { value: amount });

    const funded = await getOrderState(orderId, ethers.provider);
    expect(funded.state).to.equal(1);

    await refundOrder(orderId, ethers.provider);

    const refunded = await getOrderState(orderId, ethers.provider);
    expect(refunded.state).to.equal(3);
    expect(refunded.label).to.equal("Refunded");
  });

  it("rejects a non-32-byte orderId", async function () {
    const { ethers } = await deployWithOperator();
    for (const bad of ["0x123", "not-hex"]) {
      let threw = false;
      try {
        await getOrderState(bad, ethers.provider);
      } catch (e) {
        threw = true;
        expect((e as Error).message).to.include("0x-prefixed 32-byte");
      }
      expect(threw).to.equal(true);
    }
  });

  afterEach(function () {
    delete process.env.ESCROW_CONTRACT_ADDRESS;
    delete process.env.OPERATOR_PRIVATE_KEY;
  });
});

describe("LandMarketEscrow", function () {
  async function deployFixture() {
    const { ethers } = await network.create();
    const [operator, buyer, seller, stranger] = await ethers.getSigners();
    const factory = await ethers.getContractFactory("LandMarketEscrow");
    const escrow = (await factory.deploy(operator.address)) as unknown as EscrowContract;
    await escrow.waitForDeployment();
    return { ethers, escrow, operator, buyer, seller, stranger };
  }

  it("holds funds and lets the operator settle", async function () {
    const { ethers, escrow, operator, buyer, seller } = await deployFixture();
    const orderId = ethers.id("ORDER-1");
    const evidenceHash = ethers.id("evidence-sheet-1");
    const amount = ethers.parseEther("1");

    await expect(
      escrow.connect(buyer).createOrder(orderId, seller.address, evidenceHash, { value: amount }),
    )
      .to.emit(escrow, "OrderCreated")
      .withArgs(orderId, buyer.address, seller.address, amount, evidenceHash);

    const sellerBefore = await ethers.provider.getBalance(seller.address);

    await expect(escrow.connect(operator).settle(orderId))
      .to.emit(escrow, "TradeSettled")
      .withArgs(orderId, seller.address, amount, evidenceHash);

    expect(await ethers.provider.getBalance(seller.address)).to.equal(
      sellerBefore + amount,
    );
    expect(await escrow.orderState(orderId)).to.equal(2n);
  });

  it("rejects settlement from anyone except the operator", async function () {
    const { ethers, escrow, buyer, seller, stranger } = await deployFixture();
    const orderId = ethers.id("ORDER-2");

    await escrow
      .connect(buyer)
      .createOrder(orderId, seller.address, ethers.id("evidence"), {
        value: ethers.parseEther("0.5"),
      });

    await expect(escrow.connect(stranger).settle(orderId))
      .to.be.revertedWithCustomError(escrow, "NotOperator");
  });

  it("refunds the buyer from the operator", async function () {
    const { ethers, escrow, operator, buyer, seller } = await deployFixture();
    const orderId = ethers.id("ORDER-3");
    const amount = ethers.parseEther("0.25");

    await escrow
      .connect(buyer)
      .createOrder(orderId, seller.address, ethers.id("evidence"), { value: amount });

    const buyerBefore = await ethers.provider.getBalance(buyer.address);

    await expect(escrow.connect(operator).refund(orderId))
      .to.emit(escrow, "OrderRefunded")
      .withArgs(orderId, buyer.address, amount);

    expect(await ethers.provider.getBalance(buyer.address)).to.equal(
      buyerBefore + amount,
    );
    expect(await escrow.orderState(orderId)).to.equal(3n);
  });

  it("does not allow the same order to settle twice", async function () {
    const { ethers, escrow, operator, buyer, seller } = await deployFixture();
    const orderId = ethers.id("ORDER-4");

    await escrow
      .connect(buyer)
      .createOrder(orderId, seller.address, ethers.id("evidence"), {
        value: ethers.parseEther("0.1"),
      });

    await escrow.connect(operator).settle(orderId);

    await expect(escrow.connect(operator).settle(orderId))
      .to.be.revertedWithCustomError(escrow, "OrderNotFunded");
  });
});
