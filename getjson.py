import requests
import os
import re


def get_json_files(movie_name):
    try:
        if 'https' not in movie_name:
            movie_name = f"https://{movie_name}"

        if '=' in movie_name:
            diamond_id = movie_name.split('=')[1]
        else:
            diamond_id = movie_name.split('/')[-1]
        imaged_dir = os.path.join(os.getcwd(), "imaged")
        imagedata_dir = os.path.join(os.getcwd(), "imagedata")
        imaged_dimaond_dir = os.path.join(imaged_dir, diamond_id)
        os.makedirs(imaged_dimaond_dir, exist_ok=True)
        imagedata_diamond_dir = os.path.join(imagedata_dir, diamond_id)
        os.makedirs(imagedata_diamond_dir, exist_ok=True)
        movie_name = movie_name.lower()

        # movie_url = movie_name.split('vision360.html')[0].lower()
        movie_url = re.split(r'vision360\.html|view\.html',
                             movie_name, flags=re.IGNORECASE)[0].lower()

        v360_url = f"{movie_url}imaged/{diamond_id}/"
        print(v360_url)
        for i in range(0, 8):

            json_0 = f"{v360_url}{i}.json"

            # Send GET request to the JSON URL
            response = requests.get(json_0)
            response.raise_for_status()  # Raise an error if the request failed

            if response.status_code == 200:
                os.makedirs(imaged_dimaond_dir, exist_ok=True)
                with open(f"{imaged_dimaond_dir}/{i}.json", "w") as json_file:
                    json_file.write(response.text)
            elif response.status_code != 200:
                print('failed to downloads 0.json')
                break

            print(f"{i}.json file download successfully.")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    get_json_files("")
