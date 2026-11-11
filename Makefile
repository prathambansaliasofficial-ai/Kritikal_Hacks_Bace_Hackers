.PHONY: node deploy:local chain:smoke chain dev mid check install

node: ## Start local Hardhat node (terminal 1)
	npm --prefix middleware run node

deploy:local: ## Deploy escrow to local chain (terminal 2)
	npm --prefix middleware run deploy:local

chain:smoke: ## Run createOrder -> settle -> orderState smoke test
	npm --prefix middleware run chain:smoke

chain: deploy:local chain:smoke ## Full local chain flow: deploy + smoke (node must be running)

dev: ## Start middleware API (http://127.0.0.1:8090)
	npm --prefix middleware run dev

mid: ## typecheck + compile + test for middleware
	npm --prefix middleware run typecheck
	npm --prefix middleware run compile
	npm --prefix middleware test

install: ## Install middleware dependencies
	npm --prefix middleware install

check: ## Middleware quality gate (typecheck, test, compile, prod audit)
	npm --prefix middleware run typecheck
	npm --prefix middleware test
	npm --prefix middleware run compile
	npm --prefix middleware audit --omit=dev
