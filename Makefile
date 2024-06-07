# Define the version
VERSION := 0.1.1

# Define the image name
IMAGE_NAME := isagog_users

# Default target: list all available targets
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build   - Build the Docker image"
	@echo "  push    - Push the Docker image to a registry"
	@echo "  publish - Publish on PyPI"

# Build the Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

# Push the Docker image (optional, if you want to push to a registry)
.PHONY: push
push:
	docker push $(IMAGE_NAME):$(VERSION)

# Build and publish the package using Poetry
.PHONY: publish
publish:
	poetry build
	poetry publish

# Set the default target to 'help'
.DEFAULT_GOAL := help

# Set the default target to 'help'
.DEFAULT_GOAL := help
