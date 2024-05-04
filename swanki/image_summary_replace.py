import os
import re
import requests
from dotenv import load_dotenv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}


def get_file_content(file_path: str) -> str:
    """
    Returns the content of a file if it exists, otherwise returns an empty string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:  # Ensure UTF-8 encoding
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return ""


def summarize_image(
    image_url: str, context: str, attempt: int = 0, max_attempts: int = 20
) -> str:
    """
    Summarizes the image using OpenAI's API with additional context.
    Implements exponential backoff in case of a 429 response (Too Many Requests).
    Returns a text summary of the image or an empty string if the summary cannot be generated.
    """
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Given the following contextual information from the paper, what's in this image? "
                        + context,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": "high"},
                    },
                ],
            }
        ],
        "max_tokens": 500,
    }

    backoff_factor = 2
    base_wait_time = 5
    fixed_delay = 2

    try:
        time.sleep(fixed_delay)  # Fixed delay before each request
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response.raise_for_status()
        response_json = response.json()
        summary = (
            response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        )
        return summary if summary else "Image summary could not be generated."
    except requests.exceptions.RequestException as e:
        if (
            isinstance(e, requests.exceptions.HTTPError)
            and e.response.status_code == 429
        ):
            if attempt < max_attempts:
                wait_time = base_wait_time * (backoff_factor**attempt)
                print(
                    f"Rate limit exceeded for {image_url}, waiting {wait_time} seconds before retrying (attempt {attempt + 1}/{max_attempts})..."
                )
                time.sleep(wait_time)
                return summarize_image(image_url, context, attempt + 1, max_attempts)
            else:
                print(f"Max retry attempts reached for {image_url}. Skipping.")
        else:
            print(f"Request failed for {image_url}: {type(e).__name__} - {str(e)}")
    except Exception as e:
        print(
            f"Unexpected error occurred for {image_url}: {type(e).__name__} - {str(e)}"
        )

    return "Failed to generate image summary."


def process_markdown_file(
    md_file: str, source_dir: str, target_dir: str, md_files: list, i: int
) -> None:
    file_path = os.path.join(source_dir, md_file)
    curr_content = get_file_content(file_path)
    if not curr_content:
        print(f"Skipping {md_file} due to empty content or read error.")
        return

    prev_content = (
        get_file_content(os.path.join(source_dir, md_files[i - 1])) if i > 0 else ""
    )
    next_content = (
        get_file_content(os.path.join(source_dir, md_files[i + 1]))
        if i < len(md_files) - 1
        else ""
    )
    context = f"{prev_content}\n\n{curr_content}\n\n{next_content}"

    image_url_pattern = re.compile(r"!\[\]\((https://cdn.mathpix.com/[^)]+)\)")
    image_urls = image_url_pattern.findall(curr_content)
    if not image_urls:
        print(f"No images found in {md_file}. Skipping image summarization.")
        return

    print(f"Found {len(image_urls)} images in {md_file}.")
    for j, image_url in enumerate(image_urls):
        summary = summarize_image(image_url, context)
        summary_text = f"ChatGPT figure/image summary: {summary}"
        summary_file = f"page-{i+1}_{j+1}.md"
        with open(
            os.path.join(target_dir, summary_file), "w", encoding="utf-8"
        ) as file:  # Ensure UTF-8 encoding
            file.write(summary_text)


def process_images_summaries(source_dir: str, target_dir: str, max_workers: int = 5):
    os.makedirs(target_dir, exist_ok=True)
    md_files = sorted([f for f in os.listdir(source_dir) if f.endswith(".md")])

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, md_file in enumerate(md_files):
            future = executor.submit(
                process_markdown_file, md_file, source_dir, target_dir, md_files, i
            )
            futures.append(future)

        for future in as_completed(futures):
            future.result()
