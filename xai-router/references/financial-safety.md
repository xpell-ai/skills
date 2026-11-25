# Financial safety

## Metering and uncertain outcomes

- Trace dispatch admission, durable operation identity, reservation, provider evidence, usage, ledger and account projection through the selected repository. Verify the writer's durability and fencing, atomic updates and effective pricing. Preserve history and idempotency across retries, crashes and concurrent calls.
- A timeout or lost acknowledgement can leave a charge possible. Inspect durable operation state before retrying anything. Preserve an uncertain operation's identity and hold, block paid redispatch, and reconcile only from verified evidence. Report confirmed customer debit, held credits and external provider cost as separate values. Missing provider evidence leaves external cost unknown.
- In the atomic exception path, independent operations can proceed only within the verified exposure, balance and quota gates. Dependent operations still require their predecessor. Follow the runbook for escalation and supported, separately approved disposition. Age alone does not release a hold. An administrative goodwill release preserves the uncertainty and audit.
- Use explicit XC amounts and canonical integer subunits. Reconcile any USD figure against its purpose and effective configuration. Console display and provider-cost settlement can use different rates.

## Credit grants

The reviewed atomic Router rejects legacy `add-credits` with `E_XAI_ATOMIC_OPERATION_UNSUPPORTED`. A visible Console action, an email allowlist, or a signed admin role cannot enable an unsupported operation. Gate any live grant on a reviewed supported path, verified actor, explicit account and amount, reason, stable idempotency, atomic ledger/projection, readback and separate authorization. Exercise ordinary-user denial, duplicate delivery, concurrency, rollback and ledger conservation on disposable storage. Preserve balances, holds and prior audit entries. Direct SQLite edits, synthetic usage and hidden overrides bypass the accounting boundary.

**Historical lessons.** An uncertain dispatch retained a reservation without a confirmed customer debit. A later Console grant repair improved account selection and structured errors while the atomic grant guard remained in force. Use the linked live task evidence in authorized Knowledge to establish the present state of any hold, grant implementation, or activation.

Sources in Router: `docs/transaction-exceptions.md`, `docs/atomic-accounting-r2b.md`, `docs/operator-recovery-r3c1.md`, `server/src/modules/XAIRouter/XCreditsAmount.ts`, and the current Router module, atomic repositories, and tests.
