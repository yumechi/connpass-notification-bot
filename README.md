# connpass-notification-bot
Connpassの参加者増減をトラックするbotを作りたい

# .env.json5 sample

```json5
{
    "your connpass event url": {
        "send_to": [
            {
                "type": "slack",
                "enable": true,
                "token": "your bot auth token",
                "channel_name": "bot-test",
            },
            {
                "type": "slack",
                "enable": false,
                "token": "your bot auth token",
                "channel_name": "connpass_notification",
            },
        ],
        "title": "your event name",
    },
}
```

# feature

- [ ] save DB
- [ ] participants diff
- [ ] send other chat service
    - [ ] gitter
    - [ ] discord
    - [ ] line ?
- [ ] real time chat
