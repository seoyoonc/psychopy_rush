import exception

class NotFiveSupportImagesError(Exception):
    def __init__(self, num_images, message=""):
        self.num_images = num_images
        super().__init__(message or f"{self.num_images} support images found.")

    def __str__(self):
        return f"NotFiveSupportImagesError: {self.args[0]}"
    

class NotEnoughImagesError(Exception):
    def __init__(self, required, found, message=""):
        self.required = required
        self.found = found
        super().__init__(message or f"Required {self.required} images, but found {self.found}.")

    def __str__(self):
        return f"NotEnoughImagesError: {self.args[0]}"