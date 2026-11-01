import { network } from "hardhat";

const { ethers } = await network.create();
const [deployer] = await ethers.getSigners();

console.log(`Deploying LandMarketEscrow with operator ${deployer.address}`);

const factory = await ethers.getContractFactory("LandMarketEscrow");
const escrow = await factory.deploy(deployer.address);
await escrow.waitForDeployment();

const address = await escrow.getAddress();
console.log(`LandMarketEscrow deployed to ${address}`);
console.log("Set ESCROW_CONTRACT_ADDRESS in middleware/.env to this address.");
