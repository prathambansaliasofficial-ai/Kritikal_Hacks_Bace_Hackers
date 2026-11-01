import { expect } from "chai";
import type { Contract, ContractTransactionResponse, Signer } from "ethers";
import { network } from "hardhat";

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
