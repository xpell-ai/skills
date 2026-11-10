# TelegramChannel V0.1

Use this reference only for behavior currently implemented in `@xpell/agent-channels`.

## Source of Truth

- `packages/xagent-channels/package.json`
- `packages/xagent-channels/src/index.ts`
- `packages/xagent-channels/src/telegram/index.ts`
- `packages/xagent-channels/src/telegram/TelegramChannel.ts`
- `packages/xagent-channels/src/telegram/TelegramBotApiClient.ts`
- `packages/xagent-channels/src/telegram/normalize.ts`
- `packages/xagent-channels/src/telegram/TelegramError.ts`
- `packages/xagent-channels/tests/telegram.test.mjs`
- `packages/xagent-channels/tests/xnode.integration.test.mjs`

## Imports and Construction

The provider subpath is canonical and the package root currently re-exports the implemented Telegram surface:

```ts
import {
  TelegramChannel,
  createTelegramWebhookPath,
} from "@xpell/agent-channels/telegram";
```

`TelegramChannelConfig` contains only:

```ts
type TelegramChannelConfig = {
  _id: string;
  _bot_token: string;
  _webhook_secret: string;
};
```

Tests may inject `_fetch` and `_now` through `TelegramChannelDependencies`. These dependencies make provider behavior deterministic and network-free; they are not provider configuration.

`TelegramChannel` implements `XChannel`, reports `_provider = "telegram"`, holds credentials in private fields, and performs no startup network call. `start(runtime)` validates the ID, Bot token shape, webhook secret, and runtime, then creates the Bot API client. Invalid configuration becomes safe `not_ready` status. Start and stop are idempotent; there is no retry worker.

## XNode Composition

```ts
import { XAgent } from "@xpell/agent";
import {
  TelegramChannel,
  createTelegramWebhookPath,
} from "@xpell/agent-channels/telegram";
import { XNode } from "@xpell/node";

const telegram = new TelegramChannel({
  _id: "telegram-customers",
  _bot_token: process.env.TELEGRAM_BOT_TOKEN!,
  _webhook_secret: process.env.TELEGRAM_WEBHOOK_SECRET!,
});

const agent = new XAgent({
  _name: "centrum",
  _channels: [telegram],
});

const route = telegram.createRouteContributor({
  _path: createTelegramWebhookPath(agent._name, telegram._id),
});

const node = new XNode();
await node.start({ _routes: [route], _modules: [agent] });
```

The deterministic helper produces:

```text
/webhooks/telegram/{agent_name}/{channel_id}
```

The host owns the exact path and supplies the route contributor through generic XNode `_routes`. The path is routing information, not authentication. Do not make XNode import Telegram or XAgent.

## Webhook Ingress

```text
Telegram POST
→ TelegramChannel route handler
→ verify X-Telegram-Bot-Api-Secret-Token
→ normalize supported text update
→ bound XChannelRuntime.receive()
→ _x.execute(agent.receive-message)
→ XAgent.onMessage()
```

Current route behavior:

- Exact static route paths only; parameterized/wildcard provider paths are rejected by this adapter.
- Secret comparison uses hashes and timing-safe comparison.
- Unauthorized input returns `401` and never reaches Agent code.
- An authenticated request while the Channel is not ready returns `503` with `retry-after: 1`.
- Unsupported update kinds and non-text messages return `200` as ignored.
- Malformed supported text updates return `400`.
- Agent or outbound processing failure returns `502` so Telegram can retry.
- Successful synchronous processing returns `200`.

The host remains responsible for HTTPS and Telegram `setWebhook`, including configuring the same secret token.

## Normalization

Only `update.message` with non-empty text is normalized. Telegram numeric IDs become strings:

- `message.from.id` → `_external_user_id`
- `message.chat.id` → `_external_conversation_id`
- `message.message_id` → `_external_message_id`
- `message.text` → `_text`
- `message.date` seconds → `_timestamp` milliseconds
- `reply_to_message.message_id` → `_reply_to_external_message_id`

Raw Telegram payloads and provider metadata do not cross the Channel boundary. `_channel_id` is not read from Telegram; the bound runtime injects it.

## Outbound Bot API Mapping

`send()` requires the Channel to be ready and maps:

- `_external_conversation_id` → `sendMessage.chat_id`
- `_text` → `sendMessage.text`
- `_reply_to_external_message_id` → `reply_parameters.message_id`

A successful Bot API response returns `_accepted: true`, the Telegram message ID as a string, and `_accepted_at`. This records provider acceptance only, not delivery or reading.

Provider bodies, credentials, and raw errors are never returned. Current provider error codes are:

- `E_TELEGRAM_CHANNEL_INVALID`
- `E_TELEGRAM_CHANNEL_NOT_READY`
- `E_TELEGRAM_CHANNEL_BAD_UPDATE`
- `E_TELEGRAM_CHANNEL_BAD_MESSAGE`
- `E_TELEGRAM_CHANNEL_SEND_FAILED`
- `E_TELEGRAM_WEBHOOK_UNAUTHORIZED`
- `E_TELEGRAM_WEBHOOK_PROCESSING_FAILED`

When sending through XAgent, provider exceptions are normalized again to the generic safe Agent send failure contract.

## Current Non-Goals

Telegram V0.1 does not implement polling, media, files, callback queries, inline keyboards, command frameworks, group administration, broadcasts, edits, reactions, payments, or delivery receipts.

Neither this package nor the Telegram adapter provides persistence, customers/users, Channel identity mapping, conversations, history, messages, memory, CRM, loyalty, campaigns, XAI behavior, capability installation, a provider/bot registry, queues, schedulers, or product-specific logic.

Future providers such as WhatsApp, Messenger, or Instagram generally belong in `@xpell/agent-channels`, not `@xpell/agent`, unless the package architecture is deliberately changed first.
