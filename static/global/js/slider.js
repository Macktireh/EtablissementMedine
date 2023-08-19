/** -------------------------------------------  Toggle Theme ------------------------------------------- */
// Access HTML elements
const themeToggle = document.querySelector(".theme");

// SVG icon
const svgDark = `
<svg width="512" height="512" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <path fill="currentColor" d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26a5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/>
</svg>
`;
const svgLight = `
<svg width="512" height="512" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <path fill="currentColor" d="M12 17q-2.075 0-3.538-1.463T7 12q0-2.075 1.463-3.538T12 7q2.075 0 3.538 1.463T17 12q0 2.075-1.463 3.538T12 17ZM2 13q-.425 0-.713-.288T1 12q0-.425.288-.713T2 11h2q.425 0 .713.288T5 12q0 .425-.288.713T4 13H2Zm18 0q-.425 0-.713-.288T19 12q0-.425.288-.713T20 11h2q.425 0 .713.288T23 12q0 .425-.288.713T22 13h-2Zm-8-8q-.425 0-.713-.288T11 4V2q0-.425.288-.713T12 1q.425 0 .713.288T13 2v2q0 .425-.288.713T12 5Zm0 18q-.425 0-.713-.288T11 22v-2q0-.425.288-.713T12 19q.425 0 .713.288T13 20v2q0 .425-.288.713T12 23ZM5.65 7.05L4.575 6q-.3-.275-.288-.7t.288-.725q.3-.3.725-.3t.7.3L7.05 5.65q.275.3.275.7t-.275.7q-.275.3-.687.288T5.65 7.05ZM18 19.425l-1.05-1.075q-.275-.3-.275-.713t.275-.687q.275-.3.688-.287t.712.287L19.425 18q.3.275.288.7t-.288.725q-.3.3-.725.3t-.7-.3ZM16.95 7.05q-.3-.275-.288-.687t.288-.713L18 4.575q.275-.3.7-.288t.725.288q.3.3.3.725t-.3.7L18.35 7.05q-.3.275-.7.275t-.7-.275ZM4.575 19.425q-.3-.3-.3-.725t.3-.7l1.075-1.05q.3-.275.712-.275t.688.275q.3.275.288.688t-.288.712L6 19.425q-.275.3-.7.288t-.725-.288Z"/>
</svg>
`;

// Toggle Theme
themeToggle.addEventListener("click", () => {
  if (themeToggle.id === "light") {
    document.querySelector("html").setAttribute("data-theme", "dark");
    themeToggle.innerHTML = svgDark;
    themeToggle.id = "dark";
  } else {
    document.querySelector("html").setAttribute("data-theme", "light");
    themeToggle.innerHTML = svgLight;
    themeToggle.id = "light";
  }
});

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
