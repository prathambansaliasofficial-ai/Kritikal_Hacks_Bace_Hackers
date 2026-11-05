export const chainConfig = {
  chainId: Number(import.meta.env.VITE_CHAIN_ID ?? 31337),
  chainName: import.meta.env.VITE_CHAIN_NAME ?? "Hardhat Local",
  escrowAddress: import.meta.env.VITE_ESCROW_ADDRESS ?? "",
  explorerUrl: import.meta.env.VITE_EXPLORER_URL ?? "",
};

export const isChainConfigured = Boolean(chainConfig.escrowAddress);

export const chainWarning = isChainConfigured
  ? null
  : "Escrow contract address not configured. Set VITE_ESCROW_ADDRESS and restart the dev server.";
