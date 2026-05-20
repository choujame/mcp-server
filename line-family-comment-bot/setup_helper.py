#!/usr/bin/env python3
"""
LINE Family Comment Bot Setup Helper

This script helps users set up the LINE Family Comment Bot with guided steps.
"""

import json
import os
from pathlib import Path


def generate_config_template(output_path: str = ".env.template") -> dict:
    """Generate a configuration template file.

    Args:
        output_path: Path to save the template

    Returns:
        Configuration template dictionary
    """
    template = {
        "LINE": {
            "CHANNEL_ACCESS_TOKEN": "paste_your_line_channel_access_token_here",
            "CHANNEL_SECRET": "paste_your_line_channel_secret_here",
            "CHANNEL_ID": "paste_your_line_channel_id_here",
            "BOT_MENTION_NAME": "Family Bot",
            "BOT_PERSONA_NAME": "SmallChen",
            "ELDER_A_DISPLAY_NAME": "Mom",
            "ELDER_A_ADDRESS": "媽媽",
            "ELDER_B_DISPLAY_NAME": "Dad",
            "ELDER_B_ADDRESS": "爸爸",
        },
        "N8N": {
            "BASE_URL": "http://localhost:5678",
            "API_KEY": "optional_n8n_api_key",
            "WEBHOOK_BASE_URL": "https://your-ngrok-url.ngrok.io",
        },
        "LLM": {
            "TYPE": "lm_studio|google_gemini|openai_compatible",
            "LM_STUDIO": {
                "BASE_URL": "http://localhost:1234/v1",
                "API_KEY": "lm-studio",
                "MODEL": "model-name",
            },
            "GOOGLE_GEMINI": {
                "API_KEY": "your_google_api_key",
                "MODEL": "gemini-2.0-flash",
            },
            "OPENAI_COMPATIBLE": {
                "BASE_URL": "https://api.openrouter.ai/v1",
                "API_KEY": "your_api_key",
                "MODEL": "model_name",
            },
        },
        "MEMORY": {
            "CONTEXT_WINDOW_LENGTH": 5,
            "COMMENT": "5-10 recommended, higher = more tokens used"
        }
    }

    # Save template
    with open(output_path, 'w') as f:
        json.dump(template, f, indent=2)

    print(f"✓ Config template saved to {output_path}")
    return template


def validate_config(config: dict) -> tuple[bool, list[str]]:
    """Validate configuration dictionary.

    Args:
        config: Configuration to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check LINE config
    line_config = config.get("LINE", {})
    if not line_config.get("CHANNEL_ACCESS_TOKEN") or "paste" in line_config.get("CHANNEL_ACCESS_TOKEN", ""):
        errors.append("LINE CHANNEL_ACCESS_TOKEN not configured")
    if not line_config.get("CHANNEL_SECRET") or "paste" in line_config.get("CHANNEL_SECRET", ""):
        errors.append("LINE CHANNEL_SECRET not configured")
    if not line_config.get("CHANNEL_ID") or "paste" in line_config.get("CHANNEL_ID", ""):
        errors.append("LINE CHANNEL_ID not configured")

    # Check n8n config
    n8n_config = config.get("N8N", {})
    if not n8n_config.get("BASE_URL"):
        errors.append("N8N BASE_URL not configured")

    # Check LLM config
    llm_config = config.get("LLM", {})
    llm_type = llm_config.get("TYPE", "").lower()

    if not llm_type:
        errors.append("LLM TYPE not configured")
    elif llm_type == "lm_studio":
        if not llm_config.get("LM_STUDIO", {}).get("MODEL"):
            errors.append("LM_STUDIO MODEL not configured")
    elif llm_type == "google_gemini":
        if not llm_config.get("GOOGLE_GEMINI", {}).get("API_KEY") or "your_" in llm_config.get("GOOGLE_GEMINI", {}).get("API_KEY", ""):
            errors.append("GOOGLE_GEMINI API_KEY not configured")
    elif llm_type == "openai_compatible":
        if not llm_config.get("OPENAI_COMPATIBLE", {}).get("API_KEY") or "your_" in llm_config.get("OPENAI_COMPATIBLE", {}).get("API_KEY", ""):
            errors.append("OPENAI_COMPATIBLE API_KEY not configured")

    return (len(errors) == 0, errors)


def check_workflow_file() -> bool:
    """Check if workflow file exists.

    Returns:
        True if workflow file exists
    """
    workflow_path = Path(__file__).parent / "workflows" / "LINE_FAMILY_COMMENT_BOT.public.json"
    if workflow_path.exists():
        print(f"✓ Workflow file found at {workflow_path}")
        return True
    else:
        print(f"✗ Workflow file not found at {workflow_path}")
        return False


def print_setup_instructions():
    """Print setup instructions to console."""
    instructions = """
╔════════════════════════════════════════════════════════════════╗
║         LINE Family Comment Bot Setup Instructions             ║
╚════════════════════════════════════════════════════════════════╝

📋 SETUP CHECKLIST:

1. ✓ Prepare n8n
   - Install n8n locally or use n8n Cloud
   - Open n8n in browser (http://localhost:5678)

2. ✓ Import Workflow
   - Create new workflow in n8n
   - Choose "Import from URL/JSON"
   - Import workflows/LINE_FAMILY_COMMENT_BOT.public.json

3. ✓ Setup LINE Developers
   - Go to https://developers.line.biz/console/
   - Create Messaging API channel
   - Copy and save: Channel Access Token, Channel Secret, Channel ID

4. ✓ Configure n8n (LINE Config node)
   - CHANNEL_ACCESS_TOKEN: [from LINE Developers]
   - CHANNEL_SECRET: [from LINE Developers]
   - CHANNEL_ID: [from LINE Developers]
   - BOT_MENTION_NAME: Family Bot (or your preferred name)
   - Elder names and addresses

5. ✓ Setup LLM (choose one):
   Option A - LM Studio (local, private)
     - Download LM Studio: https://lmstudio.ai/
     - Download a model (recommend 7B or smaller)
     - Start Local Server

   Option B - Google Gemini (simple, free tier available)
     - Get API key: https://ai.google.dev/
     - Use n8n Google/Gemini node

   Option C - OpenAI-compatible (if you have API key)
     - Use OpenRouter, Groq, Together, or similar
     - Configure base URL and API key

6. ✓ Setup Webhook (for local n8n)
   - Install ngrok: https://ngrok.com/
   - Run: ngrok http 5678
   - Copy the https://... URL
   - Set N8N WEBHOOK_BASE_URL in config
   - Update Webhook URL in LINE Developers

7. ✓ Test Connection
   - Enable workflow in n8n
   - Click "Verify" in LINE Developers
   - Add bot as LINE friend
   - Send test message with bot name

8. ✓ Join Family Group
   - Confirm bot responds correctly
   - Add bot to family LINE group
   - Monitor for appropriate response rate

🔐 SECURITY REMINDERS:
   ⚠ Never share CHANNEL_ACCESS_TOKEN or CHANNEL_SECRET
   ⚠ Never commit .env with real tokens to git
   ⚠ Keep family member names and IDs private
   ⚠ Use environment variables for sensitive data

📚 MORE INFORMATION:
   - docs/setup-line.md - LINE Developers setup
   - docs/setup-n8n.md - n8n configuration
   - docs/setup-llm.md - LLM options
   - docs/setup-ngrok.md - Ngrok for local webhook
   - docs/troubleshooting.md - Common issues

💡 QUICK TIPS:
   - Always test as LINE friend first before group
   - Recommended context window: 5-10 messages
   - Keep bot responses conservative in family groups
   - Free Ngrok URLs change on restart (use static domain for stability)
"""
    print(instructions)


if __name__ == "__main__":
    print_setup_instructions()

    # Generate template
    print("\n📝 Generating configuration template...")
    generate_config_template(".env.template")

    # Check workflow
    print("\n🔍 Checking project files...")
    check_workflow_file()

    print("\n✨ Setup helper ready! Follow the checklist above to get started.")
