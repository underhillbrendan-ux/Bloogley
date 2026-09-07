# 🤖 Bloogley — AI Personal Robot

> An open-source, flexible personal robot powered by open-weight & multi-model AI routing via **OpenRouter**.

Bloogley is an AI-powered personal robotic assistant designed to combine hardware interaction, localized decision-making, and dynamic LLM power. By leveraging **OpenRouter**, Bloogley seamlessly accesses top-tier open-source and proprietary AI models through a unified endpoint—giving it adaptive conversational skills, task planning, and multimodal reasoning without vendor lock-in.

---

## ✨ Features

- **Multi-Model Intelligence:** Interfaced via [OpenRouter](https://openrouter.ai/) to swap between open-source LLMs (e.g., Llama 3, Mistral, Qwen) or frontier models depending on the task complexity.
- **Hardware Interaction:** Controls actuators, sensors, and robotics modules through Python/Node scripts.
- **Voice & Perception (Optional):** Integrated modular pipeline for speech-to-text (STT) and text-to-speech (TTS) interaction.
- **Open-Source Stack:** Built on lightweight, community-driven tools to ensure full local customization and transparency.

---

## 🛠️ Architecture Overview

```text
       ┌────────────────┐
       │   User Voice / │
       │ Text Input     │
       └───────┬────────┘
               │
               ▼
   ┌───────────────────────┐
   │    Bloogley Core      │  <─── Local Robotics Control
   │ (Orchestration Engine)│  <─── Hardware Drivers / Sensors
   └───────────┬───────────┘
               │
               │ REST / WebSocket
               ▼
   ┌───────────────────────┐
   │    OpenRouter API     │  <─── Routing Layer
   └───────────┬───────────┘
               │
     ┌─────────┼──────────┐
     ▼         ▼          ▼
 [Llama 3] [Mistral] [Qwen / DeepSeek]
🚀 Quick Start
Prerequisites
Python (v3.9 or higher) or Node.js (v18 or higher)

OpenRouter API Key: Get one at openrouter.ai

Installation
Clone the repository:

Bash
git clone [https://github.com/underhillbrendan-ux/Bloogley.git](https://github.com/underhillbrendan-ux/Bloogley.git)
cd Bloogley
Install dependencies:

If using Python:

Bash
pip install -r requirements.txt
If using Node.js:

Bash
npm install
Configure Environment Variables:
Create a .env file in the root directory and add your API credentials:

Code snippet
OPENROUTER_API_KEY=your_openrouter_api_key_here
# Optional configurations
MODEL_NAME=meta-llama/llama-3.3-70b-instruct
SITE_URL=[https://github.com/underhillbrendan-ux/Bloogley](https://github.com/underhillbrendan-ux/Bloogley)
SITE_NAME=Bloogley Robot
Run Bloogley:

Bash
python main.py
# or
npm start
⚙️ OpenRouter Setup
Bloogley routes its reasoning and conversation through OpenRouter. To customize the AI model used by Bloogley:

Open your configuration file (config.json or .env).

Set the MODEL_NAME to your preferred model available on OpenRouter, for example:

meta-llama/llama-3.3-70b-instruct (balanced open-source reasoning)

mistralai/mistral-large (strong instruct capability)

deepseek/deepseek-r1 (high-efficiency reasoning)

🤝 Contributing
Contributions, issues, and feature requests are welcome!

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git checkout -b feature/AmazingFeature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE for more information.

👤 Author
Brendan Underhill

GitHub: @underhillbrendan-ux


<FollowUp label="Would you like help adding a licensing file or setting up a GitHub Actions workflow for this repo?" query="Yes, show me how to add a license file and a basic GitHub Actions workflow for testing the Bloogley repository."/>