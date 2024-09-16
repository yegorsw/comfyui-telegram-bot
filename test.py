from comfy import ComfyClient

if __name__ == "__main__":
    positive_prompt = "giant robot in a field, looking up at the dark night sky"
    client = ComfyClient()
    image_info = client.generate_image(positive_prompt)
    filename = image_info["filename"]
    client.save_image(image_info, filename)