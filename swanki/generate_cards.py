from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import glob

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path=dotenv_path)


def generate_text_cards(
    md_file_path: str, num_cards: int, output_dir: str = "swanki-out"
):
    """
    Generates text-based Anki cards from a markdown file.

    Args:
        md_file_path (str): Path to the markdown file to process
        num_cards (int): Number of Anki cards to generate
        output_dir (str): Base output directory
    """
    # Read the Markdown file content
    with open(md_file_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_role_content = """ You are a high level academic or expert in your field. I want you to be concise, exacting, and express doubt if there is uncertainty in reported information. For math, use as much latex for representing equations as possible and be diligent in explaining variables and major concepts.

    When writing latex use '$' for inline math and '$$' for multiline math.

    If there are any proofs or derivations please include the step by step derivation.

    Try to to focus on the text in the middle of the paper chunk. If you can't find good questions in the middle, then look at the beginning or end.

    Note that you can add tags separated by commas, that are period delimited going from broad topic to narrow topic. Add up to 2 periods if necessary, and make the words in-between slugified. Try to add up to 3 tags per question. Here are 3 example cards. The first card shows how to display latex and structure front and back of cards. The second shows how to create a cloze card. The card itself describes this. The last card shows how you can add extra information to the front of the card with the % sign by putting extra text before the % sign:
  
  
    ## A question or demand. The front side of the card
  
    Here is the card answer.
  
    $$
    \hat{\theta}_{\mathrm{MAP}}=\operatorname{argmax}_{\theta} p(\theta \mid \mathbf{x}_{1: n})
    $$
  
    - #algorithms, #probability.maximum-a-posteriori
  
    ## You can also create cloze cards like this where c1 indicates that {{c1:: these words will be hidden}} and if I use {{c2:: they will be hidden on different cards}}. This card illustrates the difference between hiding one and many.
    
    ## Putting extra information on front
  
    You can add extra details here like a code block. Anything before the `%` sign will be on the front of the card. That means this text will be on the front of the card and the code block will be on the back of the card. Use this if the context of the card is very long.
    
    %
  
    ```python
    x = 5
    print(x)
    ```
    
    NEVER DO THE FOLLOWING:
    - Never Use a header other than ## H2
    - Never leave the tags list empty
    - Never write tags in multiple bulleted lines
    - Never use numbers in tags
    - Never include information that should be on the back of the card before a % sign
    - Never make a card with reference to a figure since there is no image to reference
    - Never add any extra information
    - Never use '---' to delimit cards. The next card can start with ## H2 header.
    
    ALWAYS FOLLOW THESE:
    - Always have only one bullet for tags
    - Always avoid using % sign if possible
    - Only use % sign if there are a lot of equations needed for front of card context, otherwise just put the context on the front of the card in the ## section.
    - Always Remember anything before % sign is on front of cart
    - Always just print the cards no extra text about what you are doing, who you are, what you are about to do, etc.
    - Always try to keep cards short following the atomic principle of card creation, but make sure you include all necessary context for the card to be standalone. This is the most important part! If you include terms or information on the front of the card you must explain it it's meaning if it is necessary for understanding the question. If you introduce variables explain them. If you introduce special vocabulary necessary for understanding the question or demand, then explain it. Without proper context questions will be impossible to understand for the learner. 
    
    
    """

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_role_content},
            {
                "role": "user",
                "content": f"Write {num_cards} using the VsCode Anki format. Here is chunk of a paper to generate questions from. Focus on scientific details and math equations for the cards. Make sure to add plenty of contextual information to the front of the card and plenty of explanation to the back of the card. E.g., If you mention a variable or equation in the question you should state the latex equation as additional context. Relate the card to other ideas in the paper if possible, don't force it. Here is the paper chunk {md_content}. Again rember to write {num_cards} cards.",
            },
        ],
    )

    # Create the output directory if it doesn't exist
    gen_md_dir = os.path.join(output_dir, "gen-md")
    os.makedirs(gen_md_dir, exist_ok=True)

    # Extract the base filename without extension and directory
    base_filename = os.path.splitext(os.path.basename(md_file_path))[0]

    # Construct the output filename based on the base_filename
    output_md_path = os.path.join(gen_md_dir, f"{base_filename}.md")

    # Write the completion to a Markdown file
    with open(output_md_path, "w", encoding="utf-8") as output_file:
        output_file.write(completion.choices[0].message.content)

    print(f"Generated Markdown file saved to {output_md_path}")


def generate_image_description(image_url: str) -> str:
    """
    Generates a description for the given image URL using OpenAI's GPT model.
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    payload = {
        "model": "gpt-4o",
        "prompt": f"Describe the following image: {image_url}",
        "max_tokens": 300,
        "temperature": 0.5,
    }

    response = requests.post(
        "https://api.openai.com/v1/completions", headers=headers, json=payload
    )

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["text"].strip()
    else:
        print(f"Error: {response.text}")
        return "Description could not be generated due to an error."


def process_image_hyperlinks_dir(input_dir: str, output_dir: str):
    """
    Processes each hyperlink text file in the input directory, generates descriptions,
    and writes Markdown files to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for hyperlink_file in glob.glob(os.path.join(input_dir, "*.txt")):
        print(f"Processing: {hyperlink_file}")
        with open(hyperlink_file, "r") as file:
            image_urls = file.readlines()

        base_name = os.path.basename(hyperlink_file)
        page_number = base_name.split("-")[1].split(".")[0]
        output_file_path = os.path.join(output_dir, f"page-{page_number}.md")

        with open(output_file_path, "w") as md_file:
            for url in image_urls:
                url = url.strip()
                if url:  # Ensure URL is not empty
                    description = generate_image_description(url)
                    md_file.write(
                        f"## Image Description\n\n![]({url})\n\nDescription: {description}\n\n"
                    )

        print(f"Generated Markdown file saved to {output_file_path}")


if __name__ == "__main__":
    input_dir = "swanki-out/image-hyperlinks"
    output_dir = "swanki-out/gen-pic-md"
    process_image_hyperlinks_dir(input_dir, output_dir)

# if __name__ == "__main__":
#     generate_text_cards(
#         md_file_path="swanki-out/clean-md-singles/page-1.md",
#         num_cards=2,
#     )
