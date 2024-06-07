# Define variables for image name and version
IMAGE_NAME = isagog-userauth
IMAGE_VERSION = 0.1.0

# Detect the platform
ARCH = $(shell uname -m)
ifeq ($(ARCH),arm64)
    PLATFORM = linux/arm64
else
    PLATFORM = linux/amd64
endif

# Docker build command
build:
	docker build --platform $(PLATFORM) -t $(IMAGE_NAME):$(IMAGE_VERSION) .

# Docker run command
run:
	docker run --platform $(PLATFORM) -p 8000:8000 $(IMAGE_NAME):$(IMAGE_VERSION)

# Clean command to remove the image
clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_VERSION)
