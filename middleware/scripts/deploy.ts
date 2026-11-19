import { network } from "hardhat";
import { mkdirSync, writeFileSync } from "fs";
import { join } from "path";

const { ethers } = await network.create();
const [deployer] = await ethers.getSigners();

console.log(`Deploying LandMarketEscrow with operator ${deployer.address}`);

const factory = await ethers.getContractFactory("LandMarketEscrow");
const escrow = await factory.deploy(deployer.address);
await escrow.waitForDeployment();

const address = await escrow.getAddress();
const chainId = Number((await ethers.provider.getNetwork()).chainId);
const deployedAt = new Date().toISOString();
const netName = chainId === 11155111 ? "sepolia" : chainId === 31337 ? "localhost" : `chain-${chainId}`;

const artifact = {
  address,
  chainId,
  deployer: deployer.address,
  operator: deployer.address,
  deployedAt,
};

const dir = join(process.cwd(), "deployments");
mkdirSync(dir, { recursive: true });
writeFileSync(join(dir, `${netName}.json`), JSON.stringify(artifact, null, 2) + "\n");

console.log(`LandMarketEscrow deployed to ${address}`);
console.log(`Artifact written to deployments/${netName}.json`);
console.log("Set ESCROW_CONTRACT_ADDRESS in middleware/.env to this address.");
