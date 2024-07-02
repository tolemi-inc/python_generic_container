all:build-image

build-image:
	podman manifest rm python-generic:latest
	podman build --jobs=2 --platform=linux/amd64,linux/arm64 --manifest python-generic:latest .