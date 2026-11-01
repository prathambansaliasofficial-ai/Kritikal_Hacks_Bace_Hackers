// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

/// @title LandMarketEscrow
/// @notice Prototype escrow for Land Market trades. Funds are held until the
///         backend operator confirms the six trade checks and calls settle().
///         This contract is not a land-title registry.
contract LandMarketEscrow {
    enum OrderState {
        None,
        Funded,
        Settled,
        Refunded
    }

    struct Order {
        address seller;
        address buyer;
        uint256 amount;
        bytes32 evidenceHash;
        OrderState state;
    }

    /// @notice Backend service account allowed to settle or refund orders.
    address public immutable operator;

    mapping(bytes32 orderId => Order) public orders;

    event OrderCreated(
        bytes32 indexed orderId,
        address indexed buyer,
        address indexed seller,
        uint256 amount,
        bytes32 evidenceHash
    );
    event TradeSettled(
        bytes32 indexed orderId,
        address indexed seller,
        uint256 amount,
        bytes32 evidenceHash
    );
    event OrderRefunded(bytes32 indexed orderId, address indexed buyer, uint256 amount);

    error NotOperator();
    error InvalidAmount();
    error InvalidSeller();
    error OrderAlreadyExists();
    error OrderNotFunded();
    error TransferFailed();

    modifier onlyOperator() {
        if (msg.sender != operator) revert NotOperator();
        _;
    }

    constructor(address operator_) {
        if (operator_ == address(0)) revert InvalidSeller();
        operator = operator_;
    }

    /// @notice Buyer funds an order. The evidence hash anchors the 21-field sheet.
    function createOrder(bytes32 orderId, address seller, bytes32 evidenceHash) external payable {
        if (msg.value == 0) revert InvalidAmount();
        if (seller == address(0) || seller == msg.sender) revert InvalidSeller();
        if (orders[orderId].state != OrderState.None) revert OrderAlreadyExists();

        orders[orderId] = Order({
            seller: seller,
            buyer: msg.sender,
            amount: msg.value,
            evidenceHash: evidenceHash,
            state: OrderState.Funded
        });

        emit OrderCreated(orderId, msg.sender, seller, msg.value, evidenceHash);
    }

    /// @notice Operator releases escrowed funds after the backend rules pass.
    function settle(bytes32 orderId) external onlyOperator {
        Order storage order = orders[orderId];
        if (order.state != OrderState.Funded) revert OrderNotFunded();

        // Checks-effects-interactions: update state before the external call.
        order.state = OrderState.Settled;

        (bool sent, ) = payable(order.seller).call{value: order.amount}("");
        if (!sent) revert TransferFailed();

        emit TradeSettled(orderId, order.seller, order.amount, order.evidenceHash);
    }

    /// @notice Operator returns escrowed funds (failed checks, timeout, manual review).
    function refund(bytes32 orderId) external onlyOperator {
        Order storage order = orders[orderId];
        if (order.state != OrderState.Funded) revert OrderNotFunded();

        order.state = OrderState.Refunded;

        (bool sent, ) = payable(order.buyer).call{value: order.amount}("");
        if (!sent) revert TransferFailed();

        emit OrderRefunded(orderId, order.buyer, order.amount);
    }

    function orderState(bytes32 orderId) external view returns (OrderState) {
        return orders[orderId].state;
    }
}
