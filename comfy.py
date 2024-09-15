import json
import requests
import uuid
import time

def get_first_item(input_dict):
        return next(iter(input_dict.values()))

class ComfyClient:
    def __init__(self, workflow_file='workflow_flux_ollama.json', base_url='http://127.0.0.1:8188'):
        self.workflow_file = workflow_file
        self.base_url = base_url
        # Load the workflow JSON data once during initialization
        with open(self.workflow_file, 'r') as file:
            self.json_data = json.load(file)

    def queue_prompt(self, prompt):
        payload = {"prompt": prompt, "client_id": str(uuid.uuid4())}
        response = requests.post(f"{self.base_url}/prompt", json=payload)
        return response.json()

    def wait_for_image(self, prompt_id):
        print("Waiting for image to be generated...")
        while True:
            response = requests.get(f"{self.base_url}/history")
            try:
                return response.json()[prompt_id]
            except KeyError:
                time.sleep(1)

    def save_image(self, image_info, filename):
        response = requests.get(f"{self.base_url}/view", params=image_info)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image saved as {filename}")

    def generate_image(self, positive_prompt, seed=0):
        # Update the JSON data with the new prompt and seed
        self.json_data["67"]["inputs"]["string"] = positive_prompt
        self.json_data["25"]["inputs"]["noise_seed"] = seed
        self.json_data["79"]["inputs"]["seed"] = seed

        prompt_submit_data = self.queue_prompt(self.json_data)
        prompt_id = prompt_submit_data["prompt_id"]
        generated_image_data = self.wait_for_image(prompt_id)
        img_info = self.get_first_item(generated_image_data["outputs"])["images"][0]
        return img_info

if __name__ == "__main__":
    positive_prompt = "giant robot in a field, looking up at the dark night sky"
    client = ComfyClient()
    image_info = client.generate_image(positive_prompt)
    filename = image_info["filename"]
    client.save_image(image_info, filename)
