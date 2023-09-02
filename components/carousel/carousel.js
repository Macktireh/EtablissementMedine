/** -------------------------------------------  Slider Carousel ------------------------------------------- */
// Access HTML elements
const carouselRow = document.querySelector(".slides-row");
const carouselSlides = document.getElementsByClassName("slide");
const dots = document.getElementsByClassName("dot");
const nextBtn = document.querySelector(".next");
const prevBtn = document.querySelector(".prev");

// Declare variables
let slideIndex = 1;

let width = carouselSlides[0].clientWidth;
carouselRow.style.transform = `translateX(-${width * slideIndex}px)`;
window.onresize = () => {
  width = carouselSlides[0].clientWidth;
  carouselRow.style.transform = `translateX(-${width * slideIndex}px)`;
};

//  Go to Next Slide
nextBtn.addEventListener("click", nextSlide);
function nextSlide() {
  if (slideIndex >= carouselSlides.length - 1) return;
  carouselRow.style.transition = "transform 0.4s ease-in-out";
  slideIndex++;
  carouselRow.style.transform = `translateX(-${width * slideIndex}px)`;
  dotsLabel();
}

//  Go to Previous Slide
prevBtn.addEventListener("click", prevSlide);
function prevSlide() {
  if (slideIndex <= 0) return;
  carouselRow.style.transition = "transform 0.4s ease-in-out";
  slideIndex--;
  carouselRow.style.transform = `translateX(-${width * slideIndex}px)`;
  dotsLabel();
}

// return to the first slide when the reaches last slide
carouselRow.addEventListener("transitionend", () => {
  if (carouselSlides[slideIndex].id === "firstImageDuplicate") {
    carouselRow.style.transition = "none";
    slideIndex = carouselSlides.length - slideIndex;
    carouselRow.style.transform = `translateX(-${width * slideIndex}px)`;
    dotsLabel();
  }
  if (carouselSlides[slideIndex].id === "lastImageDuplicate") {
    carouselRow.style.transition = "none";
    slideIndex = carouselSlides.length - 2;
    carouselRow.style.transform = `translateX(-${width * slideIndex}px)`;
    dotsLabel();
  }
});

// Auto Sliding
function autoSlide() {
  deleteInterval = setInterval(timer, 5000);
  function timer() {
    nextSlide();
  }
}
autoSlide();

// Stop Auto Sliding when mouse is over the slider
const carouselContainer = document.querySelector(".slides-container");
carouselContainer.addEventListener("mouseover", () => {
  clearInterval(deleteInterval);
});

// resume Auto Sliding when mouse is out of the slider
carouselContainer.addEventListener("mouseout", autoSlide);

function dotsLabel() {
  for (let i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  dots[slideIndex - 1].className += " active";
}
