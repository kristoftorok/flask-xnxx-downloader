# Flask XNXX Downloader

This is a simple Flask web application for downloading videos from xnxx.com at the best available quality.

## Installation

The easiest way to run this app is by using Docker to build an image from the provided Dockerfile.

Clone the repository:

```bash
git clone https://github.com/kristoftorok/flask-xnxx-downloader
cd flask-xnxx-downloader
```

Build the Docker image:

```bash
docker build -t xndownload .
```

Run the Docker container:

```bash
docker run -p 8000:8000 xndownload
```

This will start the app on **http://localhost:8000**.


## Environment Variables

The app doesn’t require any environment variables by default. However, you can adjust the following settings for Gunicorn:

```bash
GUNICORN_WORKERS=5    # Number of worker processes for handling requests
GUNICORN_THREADS=2    # Number of threads per worker
```

## Mount Points

You can set a local directory as a mount point to store downloaded videos persistently. Videos are saved in /tmp/videos/ with hashed filenames based on their titles:

```bash
/tmp/videos/<hashed_title>.mp4
```

Example:

```bash
docker run -p 8000:8000 --name xndownload -v ./videos:/tmp/videos xndownload
```

Make sure you have set the necessary permissions on your local directory to allow the application to write to this directory.
If you're not sure set the follwing permissions to your local directory:

```bash
chmod -R 777 ./videos
```


> [!NOTE]
> The app does not delete the downloaded videos automatically. It’s recommended to clean up downloaded files regularly as needed, but it's up to you.

## Usage

To download a video, replace the xnxx.com part of the video URL with your app’s instance URL (e.g., http://localhost:8000).

For example, if you watched a video at:

https://xnxx.com/123456789/abc-123-xyz

To download it, simply go to:

http://localhost:8000/123456789/abc-123-xyz

The application will process your request and start the download. 

> [!NOTE]
> This may take some time as the backend first downloads the video to /tmp/videos/ and then serves it to your browser.

## That's it!

Happy downloading! :)