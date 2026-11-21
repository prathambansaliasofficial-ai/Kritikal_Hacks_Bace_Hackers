export const chainConfig = {
  chainId: Number(import.meta.env.VITE_CHAIN_ID ?? 31337),
  chainName: import.meta.env.VITE_CHAIN_NAME ?? "Hardhat Local",
  escrowAddress: import.meta.env.VITE_ESCROW_ADDRESS ?? "",
  explorerUrl: import.meta.env.VITE_EXPLORER_URL ?? "",
};

// DEMO PAYMENT MODE: simulated escrow, no wallet, no gas, no payment gateway.
// Set VITE_DEMO_PAYMENT=true and VITE_DEMO_BUYER_WALLET (a KYC-verified buyer).
export const isDemoPayment = import.meta.env.VITE_DEMO_PAYMENT === "true";
export const demoBuyerWallet: string = import.meta.env.VITE_DEMO_BUYER_WALLET ?? "";

export const isChainConfigured =
  isDemoPayment || Boolean(chainConfig.escrowAddress);

export const chainWarning = isChainConfigured
  ? null
  : "Escrow contract address not configured. Set VITE_ESCROW_ADDRESS and restart the dev server.";
