# Define variables for image name and version
IMAGE_NAME = isagog-userauth
IMAGE_VERSION = 0.1.1

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
run: ensure-container
	docker run --name $(IMAGE_NAME) --platform $(PLATFORM) -p 8000:8000 $(IMAGE_NAME):$(IMAGE_VERSION)

# Clean command to remove the image and any associated containers
clean: stop-containers
	docker rmi $(IMAGE_NAME):$(IMAGE_VERSION)

# Stop and remove any running containers using the image
stop-containers:
	@if docker ps -a --format '{{.Names}}' | grep -Eq "^$(IMAGE_NAME)$$"; then \
		docker stop $(IMAGE_NAME); \
		docker rm $(IMAGE_NAME); \
	fi

# Ensure image exists
ensure-image:
	@if ! docker image inspect $(IMAGE_NAME):$(IMAGE_VERSION) > /dev/null 2>&1; then \
		$(MAKE) build; \
	fi

# Ensure container is not running
ensure-container: ensure-image
	@if docker ps -a --format '{{.Names}}' | grep -Eq "^$(IMAGE_NAME)$$"; then \
		docker stop $(IMAGE_NAME); \
		docker rm $(IMAGE_NAME); \
	fi
