# Seismic Tools

## Building the Docker Image

To build the image you can use the following command:

```bash
docker build --build-arg SSH_KEY="$(cat <path-to-your-ssh-pub-key>)" -t seismic .
```

After this, you can extend or run the `seismic` container with the `dowser`, `dasf`, and `dasf-seismic` Python libraries already installed.