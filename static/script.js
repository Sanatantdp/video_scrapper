const canvas = document.querySelector("#canvas");
const loader = document.querySelector("#loader");
const context = canvas.getContext("2d");
let baseURL = "http://192.168.29.71:2500/imagedata";
const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get("id");
const type = urlParams.get("type");
// console.log(type);
if(type == "W") {
baseURL = "http://192.168.29.71:2500/imagedata";
}else if(type == "L") {
baseURL = "https://diabrilliance.com/imagedata/labgrown";
}
let totalImages = 256;
let currentImageIndex = 0;  // Start from the first image (index 0)
let images = [];
let isPlaying = false;
let isError = false;
let intervalId = null;
let drag = false;
let imagesLoaded = 0;
let loadFailed = false;
loader.innerHTML = "Loading-360";

const loadImages = async (starter=false) => {
  if (starter) {
    totalImages = 1
  }else{
    totalImages = 256;
  }
  for (let i = 0; i < totalImages; i++) {
    const img = new Image();
    img.src = `${baseURL}/${id}/${i + 1}.jpg`;
    images.push(img);
    await new Promise((resolve) => {
      img.onload = () => {
        imagesLoaded++;
        if (imagesLoaded === 1) {
          if (images[currentImageIndex]) {
            renderImage();
          }
        }if (imagesLoaded > 10 && !isPlaying) {
          play()
          loader.innerHTML = "";
        }
        if (imagesLoaded === totalImages && !starter) {
          console.log("All images loaded");
          loader.innerHTML = "";
        }
        resolve();
      };
      img.onerror = () => {
        totalImages = i;
        if (totalImages > 0) loadFailed = true;
        else {
          isError = true;
          loader.innerHTML = "Error loading images";
        }
        resolve();
      };
    });
  }
};

const renderImage = () => {
  try {
    if (!isError && context && images[currentImageIndex].complete) {
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.drawImage(images[currentImageIndex], 0, 0, canvas.width, canvas.height);
    }
  } catch (error) {
    console.error(error);
  }
};

const nextImage = () => {
  currentImageIndex = (currentImageIndex + 1) % totalImages;
  if (images[currentImageIndex]) {
    renderImage();
  }
};

const previousImage = () => {
  currentImageIndex = (currentImageIndex - 1 + totalImages) % totalImages;
  if (images[currentImageIndex]) {
    renderImage();
  }
};

const togglePlayPause = () => {
  if (isPlaying) {
    clearInterval(intervalId);
    isPlaying = false;
  } else {
     const intervalDuration = 100 * Math.max(1, Math.floor(totalImages / 256)); 
    intervalId = setInterval(nextImage, intervalDuration);
    isPlaying = true;
  }
};

const play = () =>{
   const intervalDuration = 100 * Math.max(1, Math.floor(totalImages / 256)); 
  intervalId = setInterval(nextImage, intervalDuration);
  isPlaying = true;
}

const pause = () => {
  clearInterval(intervalId);
  isPlaying = false;
}

const handleMouseMove = (event) => {
  if (drag) {
    const canvasWidth = canvas.width;
    const mouseX = event.offsetX;
    currentImageIndex = Math.floor((mouseX / canvasWidth) * totalImages) % totalImages;
    if (images[currentImageIndex]) {
      renderImage();
    }
  }
};

canvas.addEventListener("mousemove", handleMouseMove);
canvas.addEventListener("click", togglePlayPause);
canvas.addEventListener("mouseout", togglePlayPause);
canvas.addEventListener("mouseover", () => {
  if (imagesLoaded === 1) {
    if (isError) {
      loader.innerHTML = "Error loading images";
    } else {
      loader.innerHTML = "Loading-360";
      loadImages()
      // .then(() => {
      //   if (imagesLoaded > 0) {
      //     loader.innerHTML = "";
      //     togglePlayPause();
      //   }
      // });
    }
  } else {
    togglePlayPause();
  }
});

canvas.addEventListener("mousedown", () => {
  drag = true;
  canvas.style.cursor = "grabbing";
});

canvas.addEventListener("mouseup", () => {
  drag = false;
  canvas.style.cursor = "grab";
});

// Load images as soon as the script runs
loadImages(true);
