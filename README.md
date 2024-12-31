# Neural Style Transfer App

A simple Flask app that allows you to apply Neural Style Transfer (NST) on images using a pre-trained TensorFlow model.

## Installation

### Clone the repository

```bash
git clone https://github.com/enigmatronix13/Neural-Style-Transfer.git
```
```bash
cd Neural-Style-Transfer
```

### Build the Docker image

```bash
docker build -t neural-style-transfer .
```

### Run the Docker container

```bash
docker run -p 5000:5000 neural-style-transfer
```


## Usage

1. Open `http://127.0.0.1:5000` in your browser.
2. Upload a **content image** and a **style image**.
3. Download the stylized image after processing.
