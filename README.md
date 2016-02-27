# SpotiQue API

In this repository you've got API. It's purpose is to manage getting and inserting tracks into queue.

It also is responsible for WebSocket connections from frontend.

## Installation

For development, use vagrant with ansible provisioning from different repository

For production (raspberryPi) use ansible provisioning, from the same repo.

If you don't want to use that, just run `pip install -r requirements.txt`.

## Running

    gunicorn api:app -k aiohttp.worker.GunicornWebWorker -b localhost:5000
