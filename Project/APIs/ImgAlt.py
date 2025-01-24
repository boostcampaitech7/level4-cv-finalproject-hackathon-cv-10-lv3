from transformers import AutoProcessor, AutoModelForVision2Seq
from transformers.image_utils import load_image
import torch

def generate_alt_text(image_path: str) -> str:
    """
    Generate alternative text for the input image using a Vision-Language Model.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: Generated text describing the image.
    """
    # Set device
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    # Load processor and model
    processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-Instruct")
    model = AutoModelForVision2Seq.from_pretrained(
        "HuggingFaceTB/SmolVLM-Instruct",
        torch_dtype=torch.bfloat16,
        _attn_implementation="eager"
    ).to(DEVICE)

    # Load the image
    image = load_image(image_path)

    # Prepare the message template
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "Can you describe this image in one paragraph? Please explain by focusing more on large and clear objects than on small elements or blurry backgrounds."}
            ]
        },
    ]

    # Generate prompt and input tensors
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image], return_tensors="pt").to(DEVICE)

    # Generate the text
    generated_ids = model.generate(**inputs, max_new_tokens=350)
    generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)

    # Return the generated text
    return generated_texts[0]


def img_alt(image_number):
    image_path = f"/data/ephemeral/home/clova/img/image{image_number}.jpg"
    output_path = f"/data/ephemeral/home/clova/img/image{image_number}_alt_text.txt"

    # Generate alt text
    alt_text = generate_alt_text(image_path)
    alt_text = alt_text.split('\n')[1][11:]
    # Save alt text to file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(alt_text)
    print(f"Alternative text saved to {output_path}")

    return alt_text
