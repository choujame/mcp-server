import json
import os
import httpx
import logging
import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Configure logging to write to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("financial-datasets-mcp")

# Initialize FastMCP server
mcp = FastMCP("financial-datasets")

# Constants
FINANCIAL_DATASETS_API_BASE = "https://api.financialdatasets.ai"


# Helper function to make API requests
async def make_request(url: str) -> dict[str, any] | None:
    """Make a request to the Financial Datasets API with proper error handling."""
    # Load environment variables from .env file
    load_dotenv()
    
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"Error": str(e)}


@mcp.tool()
async def get_income_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get income statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the income statement (e.g. annual, quarterly, ttm)
        limit: Number of income statements to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/income-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch income statements or no income statements found."

    # Extract the income statements
    income_statements = data.get("income_statements", [])

    # Check if income statements are found
    if not income_statements:
        return "Unable to fetch income statements or no income statements found."

    # Stringify the income statements
    return json.dumps(income_statements, indent=2)


@mcp.tool()
async def get_balance_sheets(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get balance sheets for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the balance sheet (e.g. annual, quarterly, ttm)
        limit: Number of balance sheets to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/balance-sheets/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch balance sheets or no balance sheets found."

    # Extract the balance sheets
    balance_sheets = data.get("balance_sheets", [])

    # Check if balance sheets are found
    if not balance_sheets:
        return "Unable to fetch balance sheets or no balance sheets found."

    # Stringify the balance sheets
    return json.dumps(balance_sheets, indent=2)


@mcp.tool()
async def get_cash_flow_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get cash flow statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the cash flow statement (e.g. annual, quarterly, ttm)
        limit: Number of cash flow statements to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/cash-flow-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    # Extract the cash flow statements
    cash_flow_statements = data.get("cash_flow_statements", [])

    # Check if cash flow statements are found
    if not cash_flow_statements:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    # Stringify the cash flow statements
    return json.dumps(cash_flow_statements, indent=2)


@mcp.tool()
async def get_current_stock_price(ticker: str) -> str:
    """Get the current / latest price of a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch current price or no current price found."

    # Extract the current price
    snapshot = data.get("snapshot", {})

    # Check if current price is found
    if not snapshot:
        return "Unable to fetch current price or no current price found."

    # Stringify the current price
    return json.dumps(snapshot, indent=2)


@mcp.tool()
async def get_historical_stock_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical stock prices for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_company_news(ticker: str) -> str:
    """Get news for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/news/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch news or no news found."

    # Extract the news
    news = data.get("news", [])

    # Check if news are found
    if not news:
        return "Unable to fetch news or no news found."
    return json.dumps(news, indent=2)


@mcp.tool()
async def get_available_crypto_tickers() -> str:
    """
    Gets all available crypto tickers.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/tickers"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch available crypto tickers or no available crypto tickers found."

    # Extract the available crypto tickers
    tickers = data.get("tickers", [])

    # Stringify the available crypto tickers
    return json.dumps(tickers, indent=2)


@mcp.tool()
async def get_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """
    Gets historical prices for a crypto currency.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_historical_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical prices for a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_current_crypto_price(ticker: str) -> str:
    """Get the current / latest price of a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch current price or no current price found."

    # Extract the current price
    snapshot = data.get("snapshot", {})

    # Check if current price is found
    if not snapshot:
        return "Unable to fetch current price or no current price found."

    # Stringify the current price
    return json.dumps(snapshot, indent=2)


@mcp.tool()
async def get_sec_filings(
    ticker: str,
    limit: int = 10,
    filing_type: str | None = None,
) -> str:
    """Get all SEC filings for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        limit: Number of SEC filings to return (default: 10)
        filing_type: Type of SEC filing (e.g. 10-K, 10-Q, 8-K)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/filings/?ticker={ticker}&limit={limit}"
    if filing_type:
        url += f"&filing_type={filing_type}"
 
    # Call the API
    data = await make_request(url)

    # Extract the SEC filings
    filings = data.get("filings", [])

    # Check if SEC filings are found
    if not filings:
        return f"Unable to fetch SEC filings or no SEC filings found."

    # Stringify the SEC filings
    return json.dumps(filings, indent=2)

OPENAI_API_BASE = "https://api.openai.com/v1"

# 13 industrial-grade prompt templates from freestylefly/awesome-gpt-image-2
_IMAGE_TEMPLATES: dict[str, dict] = {
    "infographic": {
        "type": "infographic",
        "description": "Data visualization / infographic layout",
        "schema": {
            "type": "infographic",
            "topic": "<topic>",
            "audience": "<target audience>",
            "structure": {
                "title_area": {"title": "<main title>", "subtitle": "<subtitle>"},
                "layout": "grid | timeline | flowchart | comparison",
                "modules": [
                    {"title": "<section title>", "icon": "<icon description>", "body": "<2-3 sentences>"}
                ],
            },
            "style": {
                "aesthetic": "flat | isometric | hand-drawn | corporate",
                "palette": ["<color1>", "<color2>", "<color3>"],
                "background": "<background description>",
            },
            "constraints": {
                "aspect_ratio": "16:9 | 9:16 | 1:1",
                "text_language": "en | zh | ...",
                "no_photographs": True,
            },
        },
    },
    "poster": {
        "type": "poster",
        "description": "Marketing / event poster",
        "schema": {
            "type": "poster",
            "title": "<headline>",
            "tagline": "<sub-headline>",
            "subject": {"description": "<main visual subject>", "pose": "<pose or action>"},
            "composition": {
                "focal_point": "center | top | bottom",
                "depth": "shallow | deep",
                "camera": "wide | medium | close-up",
            },
            "style": {
                "genre": "minimalist | retro | cyberpunk | watercolor | photorealistic",
                "palette": ["<color1>", "<color2>"],
                "lighting": "dramatic | soft | neon | natural",
            },
            "text_overlay": {
                "headline_position": "top | bottom | center",
                "font_style": "serif | sans-serif | display",
            },
            "constraints": {"aspect_ratio": "2:3 | 3:4 | 9:16", "safe_zone_margin": "5%"},
        },
    },
    "ui_screenshot": {
        "type": "ui_screenshot",
        "description": "App or web UI mockup screenshot",
        "schema": {
            "type": "ui_screenshot",
            "platform": "mobile | tablet | desktop | watch",
            "app_type": "social | finance | health | productivity | ecommerce",
            "screen": {
                "name": "<screen name>",
                "components": ["navbar", "hero_card", "list_items", "cta_button", "tab_bar"],
            },
            "style": {
                "design_system": "material | cupertino | fluent | custom",
                "theme": "light | dark | auto",
                "accent_color": "<hex or color name>",
                "corner_radius": "none | small | large | pill",
            },
            "content": {
                "dummy_text": True,
                "dummy_images": True,
                "locale": "en-US | zh-CN | ja-JP",
            },
            "constraints": {
                "device_frame": True,
                "aspect_ratio": "9:19.5 | 4:3 | 16:9",
                "status_bar": True,
            },
        },
    },
    "ecommerce": {
        "type": "ecommerce",
        "description": "E-commerce product image",
        "schema": {
            "type": "ecommerce",
            "product": {
                "name": "<product name>",
                "category": "electronics | fashion | food | cosmetics | furniture",
                "color": "<product color>",
                "material": "<material description>",
            },
            "shot_type": "hero | lifestyle | flat_lay | 360 | detail",
            "background": {
                "type": "solid | gradient | contextual | transparent",
                "color": "<background color or scene>",
            },
            "lighting": {
                "type": "studio | natural | dramatic | rim",
                "shadows": "none | soft | hard",
            },
            "style": {
                "mood": "clean | luxury | playful | minimal",
                "post_processing": "none | retouched | stylized",
            },
            "constraints": {"aspect_ratio": "1:1 | 4:3 | 3:4", "white_space": "20%"},
        },
    },
    "character": {
        "type": "character",
        "description": "Character design / concept art",
        "schema": {
            "type": "character",
            "identity": {
                "name": "<character name>",
                "role": "<role or archetype>",
                "age_range": "child | teen | adult | elder",
                "gender_expression": "<description>",
            },
            "appearance": {
                "build": "slim | athletic | stocky | large",
                "hair": "<hair style and color>",
                "clothing": {"top": "<top description>", "bottom": "<bottom>", "accessories": ["<item>"]},
                "distinguishing_features": ["<feature>"],
            },
            "pose": {"stance": "neutral | action | casual", "expression": "<emotion>", "camera": "full_body | half_body | portrait"},
            "style": {
                "art_style": "anime | realistic | cartoon | pixel | chibi | painterly",
                "palette": ["<color1>", "<color2>"],
                "background": "transparent | solid | scene",
            },
            "constraints": {"reference_consistency": True, "turnaround_views": "front | side | back"},
        },
    },
    "publication_cover": {
        "type": "publication_cover",
        "description": "Book / magazine / album cover",
        "schema": {
            "type": "publication_cover",
            "publication_type": "book | magazine | album | journal | report",
            "title": "<title text>",
            "subtitle": "<subtitle or author>",
            "theme": "<conceptual theme>",
            "imagery": {
                "main_visual": "<description of main image or illustration>",
                "mood": "<emotional tone>",
                "symbolism": ["<symbol>"],
            },
            "typography": {
                "title_style": "serif | sans-serif | script | display",
                "hierarchy": ["title", "subtitle", "byline"],
                "dominant_color": "<color>",
            },
            "style": {
                "genre": "literary | genre-fiction | academic | self-help | art",
                "era": "contemporary | vintage | futuristic",
                "palette": ["<color1>", "<color2>"],
            },
            "constraints": {"aspect_ratio": "2:3 | 3:4", "bleed": "3mm", "spine_width": "<mm>"},
        },
    },
    "scene": {
        "type": "scene",
        "description": "Environment / landscape / scene illustration",
        "schema": {
            "type": "scene",
            "setting": {
                "location": "<location type>",
                "time_of_day": "dawn | morning | noon | dusk | night",
                "weather": "clear | cloudy | rainy | foggy | snowy",
                "season": "spring | summer | autumn | winter",
            },
            "composition": {
                "perspective": "eye-level | bird-eye | worm-eye | isometric",
                "depth_layers": ["foreground", "midground", "background"],
                "focal_point": "<main element>",
            },
            "atmosphere": {
                "mood": "<emotional atmosphere>",
                "lighting": "<lighting description>",
                "color_temperature": "warm | cool | neutral",
            },
            "style": {
                "art_style": "photorealistic | painterly | anime | concept-art | watercolor",
                "detail_level": "low | medium | high | ultra",
            },
            "constraints": {"aspect_ratio": "16:9 | 21:9 | 1:1 | 9:16", "no_text": True},
        },
    },
    "product_photography": {
        "type": "product_photography",
        "description": "Commercial product photography style",
        "schema": {
            "type": "product_photography",
            "product": {"name": "<product>", "brand_tone": "luxury | mass-market | artisan | tech"},
            "scene_type": "tabletop | floating | hand-held | lifestyle-context | deconstructed",
            "props": ["<prop1>", "<prop2>"],
            "surface": "<surface texture and color>",
            "lighting": {
                "setup": "three-point | rim | softbox | natural | dramatic",
                "direction": "front | side | back | overhead",
                "catch_lights": True,
            },
            "post": {"color_grade": "natural | vibrant | muted | cinematic", "retouching": "minimal | moderate | heavy"},
            "constraints": {"aspect_ratio": "1:1 | 4:5 | 3:4", "product_occupies": "60-80% of frame"},
        },
    },
    "logo": {
        "type": "logo",
        "description": "Logo / brand mark design",
        "schema": {
            "type": "logo",
            "brand_name": "<brand name>",
            "tagline": "<optional tagline>",
            "logo_type": "wordmark | lettermark | icon | combination | emblem | mascot",
            "industry": "<industry or sector>",
            "personality": ["<trait1>", "<trait2>"],
            "design": {
                "style": "geometric | organic | abstract | illustrative | typographic",
                "complexity": "simple | moderate | detailed",
                "symmetry": "symmetric | asymmetric",
            },
            "palette": {
                "primary": "<color>",
                "secondary": "<color>",
                "background": "white | black | transparent",
            },
            "constraints": {
                "scalable": True,
                "works_on_dark_and_light": True,
                "no_gradients": False,
                "aspect_ratio": "1:1 | 3:1 | 4:1",
            },
        },
    },
    "avatar": {
        "type": "avatar",
        "description": "Profile picture / avatar",
        "schema": {
            "type": "avatar",
            "subject": {
                "type": "person | animal | mascot | abstract",
                "description": "<subject description>",
                "expression": "<facial expression>",
            },
            "framing": "circular | square | hexagonal",
            "crop": "head | bust | half-body",
            "style": {
                "art_style": "photorealistic | illustrated | pixel | flat | 3D | anime",
                "background": "solid | gradient | blurred | transparent",
                "background_color": "<color>",
            },
            "constraints": {"aspect_ratio": "1:1", "minimum_detail_at_32px": True, "face_centered": True},
        },
    },
    "social_banner": {
        "type": "social_banner",
        "description": "Social media banner / cover image",
        "schema": {
            "type": "social_banner",
            "platform": "twitter | linkedin | youtube | facebook | github",
            "purpose": "personal | company | event | product | community",
            "content": {
                "headline": "<main text>",
                "subtext": "<secondary text>",
                "cta": "<call to action>",
            },
            "visual_elements": {"illustration": "<description>", "icons": ["<icon>"], "photography": False},
            "style": {
                "aesthetic": "professional | playful | bold | minimal | creative",
                "palette": ["<color1>", "<color2>"],
                "typography": "sans-serif | display | mono",
            },
            "constraints": {
                "twitter_cover": "1500x500",
                "linkedin_cover": "1584x396",
                "youtube_channel_art": "2560x1440",
                "safe_zone": "center 1546x423 for all devices",
            },
        },
    },
    "illustration": {
        "type": "illustration",
        "description": "Editorial / conceptual illustration or artwork",
        "schema": {
            "type": "illustration",
            "concept": "<central idea or narrative>",
            "style": {
                "art_style": "editorial | childrens-book | surrealist | folk | geometric | collage",
                "medium": "digital | watercolor | gouache | ink | mixed-media",
                "line_work": "none | thin | bold | expressive",
            },
            "composition": {
                "subjects": ["<subject1>", "<subject2>"],
                "relationship": "<how subjects interact>",
                "negative_space": "minimal | moderate | heavy",
            },
            "palette": {
                "mood": "vibrant | muted | monochromatic | complementary",
                "colors": ["<color1>", "<color2>", "<color3>"],
            },
            "constraints": {"aspect_ratio": "1:1 | 4:3 | 16:9 | 2:3", "no_photographs": True, "text_in_image": False},
        },
    },
    "historical_cultural": {
        "type": "historical_cultural",
        "description": "Historical / cultural scene with period-accurate detail",
        "schema": {
            "type": "historical_cultural",
            "setting": {
                "era": "<historical period>",
                "civilization": "<culture or region>",
                "location": "<specific place>",
            },
            "subject": {
                "identity": "<who or what is depicted>",
                "clothing": "<period-accurate attire>",
                "action": "<what they are doing>",
            },
            "style": {
                "art_style": "oil-painting | ukiyo-e | fresco | miniature | documentary-photo | concept-art",
                "lighting": "candlelight | daylight | dramatic | ambient",
                "detail": "high | ultra",
            },
            "accuracy": {
                "historical_accuracy": "strict | interpretive",
                "anachronism": "none | intentional",
                "references": ["<reference source>"],
            },
            "constraints": {"aspect_ratio": "4:3 | 16:9 | 2:3", "no_modern_elements": True},
        },
    },
}


async def _openai_post(endpoint: str, payload: dict) -> dict:
    """POST to OpenAI API using httpx."""
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY environment variable not set."}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{OPENAI_API_BASE}/{endpoint}",
                headers=headers,
                json=payload,
                timeout=120.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def list_image_prompt_templates() -> str:
    """List all available GPT Image 2 prompt template categories from the awesome-gpt-image-2 library.

    Returns a summary of the 13 industrial-grade template categories with their descriptions.
    Use get_image_prompt_template to retrieve the full JSON schema for a specific category.
    """
    result = [
        {"category": key, "description": val["description"]}
        for key, val in _IMAGE_TEMPLATES.items()
    ]
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_image_prompt_template(category: str) -> str:
    """Get a structured JSON prompt template for GPT Image 2 generation.

    Based on the freestylefly/awesome-gpt-image-2 Prompt-as-Code template library.
    Fill in the <placeholder> fields and pass the completed JSON as the prompt to generate_gpt_image.

    Args:
        category: Template category. Use list_image_prompt_templates to see all options.
                  Valid values: infographic, poster, ui_screenshot, ecommerce, character,
                  publication_cover, scene, product_photography, logo, avatar,
                  social_banner, illustration, historical_cultural
    """
    key = category.lower().strip()
    template = _IMAGE_TEMPLATES.get(key)
    if not template:
        available = ", ".join(_IMAGE_TEMPLATES.keys())
        return f"Unknown category '{category}'. Available categories: {available}"
    return json.dumps(template["schema"], indent=2)


@mcp.tool()
async def generate_gpt_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "medium",
    background: str = "auto",
    output_format: str = "png",
    n: int = 1,
    output_compression: int = 85,
    moderation: str = "auto",
) -> str:
    """Generate images using OpenAI's gpt-image-2 model.

    Tip: Use get_image_prompt_template to build a structured JSON prompt for best results.
    The prompt can be plain text or a JSON string following the awesome-gpt-image-2 schema.

    Args:
        prompt: Text description of the image to generate. Can be plain text or JSON from a template.
        size: Image dimensions. Common values: 1024x1024, 1536x1024 (landscape), 1024x1536 (portrait).
        quality: Generation quality — low (fastest), medium, or high (best detail).
        background: Background handling — auto, opaque, or transparent (PNG only).
        output_format: File format — png, jpeg, or webp.
        n: Number of images to generate (1–10).
        output_compression: Compression level for jpeg/webp (0=lossless, 100=max compression). Default 85.
        moderation: Content moderation strictness — auto or low.
    """
    payload: dict = {
        "model": "gpt-image-2",
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "background": background,
        "output_format": output_format,
        "n": n,
        "moderation": moderation,
        "response_format": "b64_json",
    }
    if output_format in ("jpeg", "webp"):
        payload["output_compression"] = output_compression

    data = await _openai_post("images/generations", payload)
    if "error" in data:
        return f"Error: {data['error']}"

    results = []
    for i, img in enumerate(data.get("data", [])):
        entry: dict = {"index": i, "format": output_format}
        if img.get("url"):
            entry["url"] = img["url"]
        if img.get("b64_json"):
            entry["b64_json"] = img["b64_json"]
        if img.get("revised_prompt"):
            entry["revised_prompt"] = img["revised_prompt"]
        results.append(entry)

    return json.dumps(results, indent=2)


@mcp.tool()
async def edit_gpt_image(
    image_url: str,
    prompt: str,
    size: str = "1024x1024",
    quality: str = "medium",
    n: int = 1,
) -> str:
    """Edit or transform an existing image using OpenAI's gpt-image-2 model.

    Downloads the source image from a URL and sends it to the gpt-image-2 edit endpoint.

    Args:
        image_url: Publicly accessible URL of the source image (PNG, JPEG, or WebP).
        prompt: Editing instructions describing the desired change or transformation.
        size: Output image size — 1024x1024, 1536x1024, or 1024x1536.
        quality: Generation quality — low, medium, or high.
        n: Number of edited variants to generate (1–10).
    """
    # Download the source image
    async with httpx.AsyncClient() as client:
        try:
            img_response = await client.get(image_url, timeout=30.0)
            img_response.raise_for_status()
            image_bytes = img_response.content
            content_type = img_response.headers.get("content-type", "image/png")
        except Exception as e:
            return f"Error downloading image: {str(e)}"

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY environment variable not set."

    import base64
    b64_image = base64.b64encode(image_bytes).decode()

    # Determine file extension from content type
    ext_map = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}
    ext = ext_map.get(content_type.split(";")[0].strip(), "png")

    headers = {"Authorization": f"Bearer {api_key}"}
    files = {
        "image": (f"image.{ext}", image_bytes, content_type),
    }
    form_data = {
        "model": "gpt-image-2",
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": str(n),
        "response_format": "b64_json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{OPENAI_API_BASE}/images/edits",
                headers=headers,
                data=form_data,
                files=files,
                timeout=120.0,
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            return f"Error: HTTP {e.response.status_code}: {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"

    results = []
    for i, img in enumerate(data.get("data", [])):
        entry: dict = {"index": i}
        if img.get("url"):
            entry["url"] = img["url"]
        if img.get("b64_json"):
            entry["b64_json"] = img["b64_json"]
        if img.get("revised_prompt"):
            entry["revised_prompt"] = img["revised_prompt"]
        results.append(entry)

    return json.dumps(results, indent=2)


if __name__ == "__main__":
    # Log server startup
    logger.info("Starting Financial Datasets MCP Server...")

    # Initialize and run the server
    mcp.run(transport="stdio")

    # This line won't be reached during normal operation
    logger.info("Server stopped")
