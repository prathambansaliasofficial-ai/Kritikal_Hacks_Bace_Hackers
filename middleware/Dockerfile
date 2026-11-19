# syntax=docker/dockerfile:1
# Middleware production image. Secrets (TINYFISH_API_KEY, OPERATOR_PRIVATE_KEY,
# ESCROW_CONTRACT_ADDRESS, CHAIN_RPC_URL) MUST be injected via environment at
# runtime and are never baked into this image.
FROM node:20-slim AS builder
WORKDIR /app
ENV NODE_ENV=production
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json hardhat.config.ts ./
COPY src ./src
COPY scripts ./scripts
COPY test ./test
RUN npx tsc -p tsconfig.json --outDir dist --noEmit false

FROM node:20-slim AS runtime
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=8090 HOST=0.0.0.0
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY --from=builder /app/dist ./dist
EXPOSE 8090
CMD ["node", "dist/server.js"]
