# Market Router: Market Neutral Provider

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Website](https://img.shields.io/badge/Visit-marketrouter.ai-blue)](https://marketrouter.ai)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/GroupLang.svg?style=social&label=Follow%20%40GroupLang)](https://twitter.com/GroupLang)

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This system acts as a counterpart to the [Market Neutral Requester](https://github.com/GroupLang/neutral-portfolio-requester), focusing on analyzing sector-specific news to generate actionable insights for stock decisions. It utilizes the [Market Router API](https://marketrouter.ai/) for all interactions and integrates with an OpenAI completions endpoint to process news inputs supplied by the requester, subsequently generating investment recommendations.

<p align="center">
  <img src="https://github.com/user-attachments/assets/9b29a7bc-5b89-4c67-9336-2249f0569d00" alt="MarketNeutral (10)" width="500">
</p>

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/GroupLang/market-neutral-provider.git
   cd market-neutral-provider
   ```

2. **Install required libraries**

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up environment space**

   Copy the sample environment file and configure it as per your requirements.

   ```bash
   [ ! -f .env ] && cp .env.template .env
   ```


## Configuration

- **Market Router**:
  - **Username, Fullname, Email, Password**: These credentials are used for authentication and identification in the market router. If the user is already registered, these parameters are not necessary; instead, add the Market Router API key to the `.env` file as `MARKET_ROUTER_API_KEY`.
  - **Deposit Amount**: Specify the initial deposit amount for transactions in the market router if needed.

- **Proposal**:
  - **Endpoint**: Define the API endpoint for proposal submissions. Used by market router when requester calls `completions` endpoint in order to obtain OpenAI wrapper response.
  - **Max Bid**: Determines the maximum bid amount for proposals. If set to None, a gpt-4o-mini model will decide the appropriate bid based on the instance's background. This part of the configuration directly impacts the economic considerations of the proposals.

These configuration variables are stored in the config file, ensuring the Market Neutral Provider can effectively interact with the Market Router by managing its proposals and financial transactions.

## Usage

**Market Router Scripts:**

1. **Register User Script**

   ```bash
   python -m market_router.scripts.register
   ```

   This command registers a new user with the Market Router API. If `MARKET_ROUTER_API_KEY` exists (indicating prior registration), this script is unnecessary.

2. **Create API Key Script**

   ```bash
   python -m market_router.scripts.api_key
   ```

   This command generates a new API key for the user, allowing them to authenticate subsequent requests.

3. **Deposit Script**

   ```bash
   python -m market_router.scripts.deposit
   ```

   This command facilitates depositing funds into a Market Router account, as specified in the `deposit_amount` configuration.

4. **Create Proposal Script**

   ```bash
   python -m market_router.scripts.proposal
   ```

   This script submits proposals to the Market Router using configured `endpoint` and `max_bid` settings, detailing the financial and operational parameters for engagements.

**API Services Scripts:**

1. **Model Response Script**

   ```bash
   python -m api.services.model_response --model_args='{"messages": [{"role": "user", "content": "Test OpenAI Wrapper"}], "model": "gpt-3.5-turbo", "temperature": 0.5}'
   ```

   This command generates simulated responses from the model, designed to test the API's capability to process and respond to input accurately under controlled settings.

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact the maintainers at [support@marketrouter.ai](mailto:support@marketrouter.ai).
