import json
import requests
import uuid
import os, time
import websocket

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": str(uuid.uuid4())}
    response = requests.post("http://127.0.0.1:8188/prompt", json=p)
    return response.json()

def wait_for_image(prompt_id):
    print("Waiting for image to be generated..")
    while True:
        response = requests.get("http://localhost:8188/history")
        try:
            return response.json()[prompt_id]
        except KeyError:
            time.sleep(1)

def save_image(image_info, filename):
    response = requests.get("http://localhost:8188/view", params=image_info)
    with open(filename, 'wb') as f:
        f.write(response.content)

def get_first_item(input_dict: dict):
    return list(input_dict.values())[0]

#Juggernaut_X_RunDiffusion_Hyper.safetensors
#zavychromaxl_v21.safetensors
#Juggernaut-X-RunDiffusion-NSFW.safetensors
#Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors

def generate_image(positive1:str, negative1="", model="Juggernaut-X-RunDiffusion-NSFW.safetensors", steps=45, seed=0, cfg=6):
    json_data = None
    with open('workflow_flux_ollama.json', 'r') as file:
        json_data = json.load(file)
    
    json_data["67"]["inputs"]["string"] = positive1
    json_data["25"]["inputs"]["noise_seed"] = seed
    json_data["79"]["inputs"]["seed"] = seed

    prompt_submit_data = queue_prompt(json_data)
    prompt_id = prompt_submit_data["prompt_id"]
    generated_image_data = wait_for_image(prompt_id)
    img_folder_info = get_first_item(generated_image_data["outputs"])["images"][0]
    return img_folder_info

def upload_image(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
        files = {
            'image': (os.path.basename(image_path), image_data, 'image/png')
        }
        response = requests.post("http://localhost:8188/upload/image", files=files)
        return response





if __name__ == "__main__":
    pos1 = "giant robot in a field, looking up at the dark night sky"
    #pos2 = "classic illustration, scifi illustration, John Berkey, grand, humans for scale, Vincent Di Fate, Paul Lehr, simon stalenhag"
    #neg1 = "watermark, nsfw, hdr, cropped, blurry, draft, centered, front view, text, words"
    #generate_image(pos1, pos2, neg1, steps=50, filepath="wungus.png", model="sdxl_protovision.safetensors", lora="ClassipeintXL.safetensors")
    img = generate_image(pos1)
    #{'filename': 'ComfyUI_temp_eauln_00001_.png', 'subfolder': '', 'type': 'temp'}
    filename = img["filename"]
    save_image(img, filename)