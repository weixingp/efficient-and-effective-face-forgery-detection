import asyncio
import functools
import json

import mmcv
import websockets
from pytube import YouTube

from model.model import FaceForgeryDetector, FaceRecognitionCNN


def download_video(url):
    video = mmcv.VideoReader(url)
    return video


def get_yt_video_url(link):
    try:
        yt = YouTube(link)
        stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()

        if stream.fps:
            frames = yt.length * int(stream.fps)
        else:
            frames = yt.length * 30

        duration_m, duration_s = divmod(yt.length, 60)
        size = stream.filesize / 1_000_000

        temp = {
            "url": stream.url,
            "duration": f"{duration_m}m {duration_s}s",
            "resolution": stream.resolution,
            "size": round(size, 2),
            "total_frames": frames,
            "title": yt.title,
            "yt_embed": yt.embed_url,
        }
        return temp
    except Exception as ex:
        print(repr(ex))
        return None


async def app(websocket, model: FaceForgeryDetector):
    # Handshake
    handshake = await websocket.recv()
    if handshake != "start":
        return
    await websocket.send("okay")
    print(f"Connected from {websocket.remote_address[0]}")

    while True:
        # Download video
        youtube_link = await websocket.recv()
        res = {
            "status": "processing",
            "action": "Downloading video..."
        }
        await websocket.send(json.dumps(res))
        info = get_yt_video_url(youtube_link)
        if not info:
            res = {
                "status": "error",
                "reason": "Invalid URL"
            }
            await websocket.send(json.dumps(res))
            continue

        video = download_video(info["url"])

        # Extract faces
        res = {
            "status": "processing",
            "action": "Extracting faces..."
        }
        await websocket.send(json.dumps(res))

        images = model.extract_faces(video, count=100)

        # Predict using model
        res = {
            "status": "processing",
            "action": "Predicting..."
        }
        await websocket.send(json.dumps(res))
        preds = model.predict(images)

        # Done
        res = {
            "status": "success",
            "real": preds.count(1),
            "fake": preds.count(0),
            "info": info,
        }
        await websocket.send(json.dumps(res))

    print("Disconnected")


async def main():
    base = FaceRecognitionCNN()
    model = FaceForgeryDetector(model_path="./model/model.pth")
    print("accepting websocket requests...")
    async with websockets.serve(
            functools.partial(app, model=model),
            "localhost",
            8765
    ):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
