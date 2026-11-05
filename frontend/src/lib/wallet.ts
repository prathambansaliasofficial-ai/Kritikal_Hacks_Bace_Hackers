import { chainConfig } from "./chain";

export type WalletState =
  | { phase: "no-wallet" }
  | { phase: "connecting" }
  | { phase: "connected"; account: string; chainId: number }
  | { phase: "error"; message: string };

declare global {
  interface Window {
    ethereum?: ExternalProvider;
  }
}

export interface ExternalProvider {
  request?: (args: {
    method: string;
    params?: unknown[];
  }) => Promise<unknown>;
  on?: (event: string, handler: (...args: unknown[]) => void) => void;
  removeListener?: (
    event: string,
    handler: (...args: unknown[]) => void,
  ) => void;
}

export function shortenAddress(address: string): string {
  if (!address) return "";
  return `${address.slice(0, 6)}…${address.slice(-4)}`;
}

function isEthereumAvailable(): boolean {
  return typeof window !== "undefined" && !!window.ethereum;
}

export async function connectWallet(): Promise<string> {
  if (!isEthereumAvailable()) {
    throw new Error(
      "No Ethereum wallet found. Install MetaMask or a compatible wallet.",
    );
  }

  const ethereum = window.ethereum!;

  try {
    const accounts = (await ethereum.request?.({
      method: "eth_requestAccounts",
    })) as string[];

    if (!accounts || accounts.length === 0) {
      throw new Error("No accounts returned by wallet.");
    }

    await switchToConfiguredChain();

    return accounts[0];
  } catch (err) {
    throw new Error(
      err instanceof Error ? err.message : "Failed to connect wallet.",
    );
  }
}

export async function switchToConfiguredChain(): Promise<void> {
  if (!isEthereumAvailable()) {
    throw new Error("No Ethereum wallet found.");
  }

  const ethereum = window.ethereum!;

  try {
    await ethereum.request?.({
      method: "wallet_switchEthereumChain",
      params: [{ chainId: `0x${chainConfig.chainId.toString(16)}` }],
    });
  } catch (err: any) {
    if (err?.code === 4902) {
      await ethereum.request?.({
        method: "wallet_addEthereumChain",
        params: [
          {
            chainId: `0x${chainConfig.chainId.toString(16)}`,
            chainName: chainConfig.chainName,
            nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
            rpcUrls: ["http://127.0.0.1:8545"],
            blockExplorerUrls: chainConfig.explorerUrl
              ? [chainConfig.explorerUrl]
              : [],
          },
        ],
      });
    } else {
      throw new Error(
        err instanceof Error ? err.message : "Failed to switch chain.",
      );
    }
  }
}

export function onAccountsChanged(
  cb: (account: string | null) => void,
): () => void {
  if (!isEthereumAvailable()) {
    cb(null);
    return () => {};
  }

  const ethereum = window.ethereum!;
  const handler = ((accounts: unknown[]) => {
    cb((accounts as string[])[0] ?? null);
  }) as (...args: unknown[]) => void;

  ethereum.on?.("accountsChanged", handler);
  return () => {
    ethereum.removeListener?.("accountsChanged", handler);
  };
}
