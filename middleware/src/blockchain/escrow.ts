import { Contract, JsonRpcProvider, Provider, Wallet, isHexString } from "ethers";
import { requireEnv } from "../config.js";

const ESCROW_ABI = [
  "function settle(bytes32 orderId) external",
  "function refund(bytes32 orderId) external",
  "function orderState(bytes32 orderId) external view returns (uint8)",
  "event TradeSettled(bytes32 indexed orderId, address indexed seller, uint256 amount, bytes32 evidenceHash)",
];

export type SettleResult = {
  orderId: string;
  txHash: string;
  blockNumber: number | null;
  status: number | null;
};

export type OrderStateResult = {
  orderId: string;
  state: number;
  label: string;
};

const ORDER_STATE_LABELS: Record<number, string> = {
  0: "None",
  1: "Funded",
  2: "Settled",
  3: "Refunded",
};

function assertOrderId(orderId: string): void {
  if (!isHexString(orderId, 32)) {
    throw new Error("orderId must be a 0x-prefixed 32-byte hex string.");
  }
}

function getSignerContract(provider?: Provider): Contract {
  const rpc = provider ?? new JsonRpcProvider(process.env.CHAIN_RPC_URL ?? "http://127.0.0.1:8545");
  const wallet = new Wallet(requireEnv("OPERATOR_PRIVATE_KEY"), rpc);
  return new Contract(requireEnv("ESCROW_CONTRACT_ADDRESS"), ESCROW_ABI, wallet);
}

/** Backend-authorized settlement. Call only after the six trade checks pass. */
export async function settleOrder(orderId: string, provider?: Provider): Promise<SettleResult> {
  assertOrderId(orderId);
  const contract = getSignerContract(provider);

  const transaction = await contract.settle(orderId);
  const receipt = await transaction.wait();

  return {
    orderId,
    txHash: receipt?.hash ?? transaction.hash,
    blockNumber: receipt?.blockNumber ?? null,
    status: receipt?.status ?? null,
  };
}

/** Returns escrowed funds when checks fail or the case goes to manual review. */
export async function refundOrder(orderId: string, provider?: Provider): Promise<SettleResult> {
  assertOrderId(orderId);
  const contract = getSignerContract(provider);

  const transaction = await contract.refund(orderId);
  const receipt = await transaction.wait();

  return {
    orderId,
    txHash: receipt?.hash ?? transaction.hash,
    blockNumber: receipt?.blockNumber ?? null,
    status: receipt?.status ?? null,
  };
}

/** Reads on-chain orderState (0 None, 1 Funded, 2 Settled, 3 Refunded). */
export async function getOrderState(orderId: string, provider?: Provider): Promise<OrderStateResult> {
  assertOrderId(orderId);
  const contract = getSignerContract(provider);

  const state = await contract.orderState(orderId);
  const stateNum = Number(state);
  return {
    orderId,
    state: stateNum,
    label: ORDER_STATE_LABELS[stateNum] ?? "Unknown",
  };
}
