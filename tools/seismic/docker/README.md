# Docker Seismic Image

This directory contains the Docker image for the Seismic processing experiments.
The image is based on both the Dowser Docker image, as well on DASF.

## Building the Docker Image

To build the image you can use the following command:

```bash
docker build -t seismic .
```

After this, you can extend or run the `seismic` container with the `dowser`, `dasf`, and `dasf-seismic` Python libraries already installed.