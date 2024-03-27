all:build-image

build-image:
	podman manifest rm python_generic:latest
	podman build --jobs=2 --platform=linux/amd64,linux/arm64 --manifest python_generic:latest .