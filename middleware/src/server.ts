import Fastify from "fastify";
import { isHexString } from "ethers";
import { getOrderState, refundOrder, settleOrder } from "./blockchain/escrow.js";
import { config, isConfigured } from "./config.js";
import { collectEvidence } from "./tinyfish/evidence.js";

type VerifyBody = {
  ulpin?: string;
  sourceUrl?: string;
  goal?: string;
};

type OrderBody = {
  orderId?: string;
};

const app = Fastify({ logger: true });

app.get("/health", async () => ({
  status: "ok",
  service: "land-market-middleware",
  tinyfishConfigured: isConfigured("TINYFISH_API_KEY"),
  chainConfigured:
    isConfigured("ESCROW_CONTRACT_ADDRESS") && isConfigured("OPERATOR_PRIVATE_KEY"),
}));

app.post<{ Body: VerifyBody }>("/verify/evidence", async (request, reply) => {
  const { ulpin, sourceUrl, goal } = request.body ?? {};

  if (typeof ulpin !== "string" || ulpin.trim().length < 3) {
    return reply.code(400).send({ error: "ulpin is required (min 3 characters)." });
  }

  try {
    return await collectEvidence({
      ulpin: ulpin.trim(),
      sourceUrl,
      goal,
    });
  } catch (error) {
    request.log.error({ err: error }, "TinyFish evidence collection failed");
    return reply.code(502).send({
      error: error instanceof Error ? error.message : "Unknown TinyFish error",
    });
  }
});

app.post<{ Body: OrderBody }>("/escrow/settle", async (request, reply) => {
  const { orderId } = request.body ?? {};

  if (typeof orderId !== "string") {
    return reply.code(400).send({ error: "orderId is required." });
  }

  try {
    return await settleOrder(orderId);
  } catch (error) {
    request.log.error({ err: error }, "Settlement failed");
    return reply.code(502).send({
      error: error instanceof Error ? error.message : "Unknown settlement error",
    });
  }
});

app.post<{ Body: OrderBody }>("/escrow/refund", async (request, reply) => {
  const { orderId } = request.body ?? {};

  if (typeof orderId !== "string") {
    return reply.code(400).send({ error: "orderId is required." });
  }

  try {
    return await refundOrder(orderId);
  } catch (error) {
    request.log.error({ err: error }, "Refund failed");
    return reply.code(502).send({
      error: error instanceof Error ? error.message : "Unknown refund error",
    });
  }
});

app.get<{ Params: { orderId: string } }>("/escrow/status/:orderId", async (request, reply) => {
  const { orderId } = request.params;

  if (typeof orderId !== "string" || !isHexString(orderId, 32)) {
    return reply.code(400).send({
      error: "orderId must be a 0x-prefixed 32-byte hex string.",
    });
  }

  try {
    return await getOrderState(orderId);
  } catch (error) {
    request.log.error({ err: error }, "Escrow status lookup failed");
    return reply.code(502).send({
      error: error instanceof Error ? error.message : "Unknown chain error",
    });
  }
});

try {
  await app.listen({ port: config.port, host: config.host });
} catch (error) {
  app.log.error(error);
  process.exit(1);
}
