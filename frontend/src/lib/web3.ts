import { ethers } from "ethers";
import escrowAbi from "./escrowAbi.json";
import { chainConfig } from "./chain";

export function chainOrderId(orderId: number): string {
  return ethers.id(`landmarket-order:${String(orderId)}`);
}

let providerCache: ethers.BrowserProvider | null = null;

function getProvider(): ethers.BrowserProvider | null {
  if (typeof window === "undefined" || !window.ethereum) return null;
  if (!providerCache) {
    providerCache = new ethers.BrowserProvider(
      window.ethereum as ethers.Eip1193Provider,
    );
  }
  return providerCache;
}

export async function getSigner(): Promise<ethers.Signer> {
  const provider = getProvider();
  if (!provider) {
    throw new Error("No Ethereum wallet found. Install MetaMask or a compatible wallet.");
  }
  return provider.getSigner();
}

export async function createOrder({
  orderId,
  seller,
  evidenceHash,
  valueWei,
}: {
  orderId: string;
  seller: string;
  evidenceHash: string;
  valueWei: string;
}): Promise<string> {
  const signer = await getSigner();
  const contract = new ethers.Contract(
    chainConfig.escrowAddress,
    escrowAbi,
    signer,
  );

  const tx = await contract.createOrder(orderId, seller, evidenceHash, {
    value: BigInt(valueWei),
  });

  const receipt = await tx.wait();
  if (!receipt) {
    throw new Error("createOrder: no receipt returned");
  }
  return receipt.hash;
}

export function formatWeiToEth(valueWei: string): string {
  return ethers.formatEther(valueWei);
}
