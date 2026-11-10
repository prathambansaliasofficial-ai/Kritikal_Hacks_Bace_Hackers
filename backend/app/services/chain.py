from __future__ import annotations

from Crypto.Hash import keccak


def keccak256(data: bytes) -> str:
    """Return keccak-256 of ``data`` as a ``0x``-prefixed lowercase hex string.

    Used to compute ``chain_order_id`` per docs/decisions.md section 5:
    ``chain_order_id = keccak256(utf8("landmarket-order:" + str(order.id)))``.
    """
    return "0x" + keccak.new(digest_bits=256, data=data).hexdigest()
