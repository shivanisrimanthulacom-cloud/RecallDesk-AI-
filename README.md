# RecallDesk AI

A beginner-friendly Streamlit prototype for a customer-support assistant that demonstrates remembering basic customer details.

## Current features
- Chat-style interface
- Demo memory for name, preferred support channel, and order reference
- Customer-memory panel
- Clear/reset control
- Runs without paid API keys

## Important limitation
This starter uses **temporary Streamlit session memory only**. It does **not** connect to Hindsight Cloud, and it does not use an LLM. The interface labels this clearly. Do not describe this version as having a working Hindsight integration.

## Run locally
1. Install Python 3.10 or newer.
2. In this folder, run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
3. Open the local URL Streamlit prints.

## Demo flow
1. Send: `Hi, my name is Maya. I prefer email support, and I need help with my order delivery.`
2. Ask: `What is my name, and how do I prefer to receive support?`
3. Ask: `What do you remember?`
4. Use **Clear chat and demo memory** to reset.

## Hindsight integration
To complete the hackathon requirement, connect this app to your Hindsight Cloud instance using the current official Hindsight SDK/API documentation. Store credentials in Replit Secrets or environment variables—never paste API keys into source code or public repositories. Then replace the in-session `respond()` memory logic with Hindsight retain/recall calls, and test that facts persist across separate sessions. Verify the SDK's current methods and endpoint from official documentation before implementing.
