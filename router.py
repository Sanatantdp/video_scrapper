from urllib.parse import parse_qs, urlparse
import base64
import json
import time
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import os
from fastapi.responses import JSONResponse
from getjson import get_json_files
from fastapi.responses import FileResponse

app_router = APIRouter()


# Route to serve vision360.html
@app_router.get("/video.html", response_class=HTMLResponse)
async def serve_vedio_html(type: str, id: str):
    """
    Serve the vedio.html file, preserving query parameter ?id,type.
    """
    return FileResponse(f"{os.getcwd()}/video.html")


# Route to serve vision360.html
@app_router.get("/vision360.html", response_class=HTMLResponse)
async def serve_vision360_html(moviename: str | None = None):
    """
    Serve the vision360.html file, preserving query parameter ?d.
    """

    html_path = "vision360.html"  # Adjust if using home.html
    try:

        get_json_files(moviename)
        time.sleep(3)
        with open(html_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>HTML file not found</h1>", status_code=404)


@app_router.post("/upload-base64")
async def upload_base64(request: Request):
    try:

        start_time = time.time()
        data = await request.json()
        base64_str = data.get("data")
        movie_name = data.get('moviename')
        if 'https' not in movie_name:
            movie_name = f"https://{movie_name}"
        print(movie_name)
        if '=' in movie_name:
            diamond_id = movie_name.split('=')[1]
        else:
            diamond_id = movie_name.split('/')[-1]

        imaged_dir = os.path.join(os.getcwd(), "imaged")
        imagedata_dir = os.path.join(os.getcwd(), 'imagedata')
        imagedata_diamond_dir = os.path.join(imagedata_dir, diamond_id)

        os.makedirs(imagedata_diamond_dir, exist_ok=True)
        existing_files = [f for f in os.listdir(
            imagedata_diamond_dir) if f.endswith(".jpg")]
        json_folder = os.path.join(imaged_dir, diamond_id)
        json_0_file = os.path.join(json_folder, '0.json')
        with open(json_0_file, 'r') as file:
            data_image = json.load(file)
        if data_image['image'] == base64_str and len(existing_files) > 1:
            exit()

        if not base64_str:
            return JSONResponse(content={"error": "No base64 data provided"}, status_code=400)

        image_data = base64.b64decode(base64_str)

        indexes = sorted([
            int(f.split(".")[0]) for f in existing_files
            if f.split(".")[0].isdigit()
        ])

        if indexes:
            next_index = indexes[-1] + 1

        else:
            next_index = 1
        print('next_index', next_index)
        filename = os.path.join(imagedata_diamond_dir, f"{next_index}.jpg")

        with open(filename, "wb") as f:
            f.write(image_data)
        end_time = time.time()
        print('time_inter', end_time-start_time)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app_router.get("/health")
async def health_check():
    return {"status": "healthy"}
#
