
var swiper = new Swiper(".slide-content", {
  slidesPerView: 4,
  spaceBetween: 25,
  centerSlides: true,
  // autoplay: {
  //   delay: 1000,
  // },
  fade: true,
  loop: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    460: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    960: {
      slidesPerView: 3,
    },
    1280: {
      slidesPerView: 4,
    }
  }
})







// class Carousel {
//   static isDragging = false;
//   static isAutoPlay = true;
//   static startX;
//   static startScrollLeft;
//   static timeoutId;

//   constructor(warapperId) {
//     this.warapper = document.getElementById(warapperId);
//     console.log(this.warapper);
//     this.carousel = this.warapper.querySelector(".slides-product");
//     this.arrowBtns = this.warapper.querySelectorAll(".span-arrow");
//     this.firstCardWidth =
//       this.carousel.querySelector(".product-card").offsetWidth;
//     // const carouselChildrens = [...this.carousel.children];

//     this.carousel.classList.add("no-transition");
//     this.carousel.scrollLeft = this.carousel.offsetWidth;
//     this.carousel.classList.remove("no-transition");

//     this.arrowBtns.forEach((btn) => {
//       btn.addEventListener("click", () => {
//         this.carousel.scrollLeft +=
//           btn.id == "left"
//             ? -this.firstCardWidth - 55
//             : this.firstCardWidth + 55;
//       });
//     });

//     const dragStart = (e) => {
//       isDragging = true;
//       this.carousel.classList.add("dragging");
//       // Records the initial cursor and scroll position of the carousel
//       startX = e.pageX;
//       startScrollLeft = this.carousel.scrollLeft;
//     };

//     const dragging = (e) => {
//       if (!isDragging) return; // if isDragging is false return from here
//       // Updates the scroll position of the carousel based on the cursor movement
//       this.carousel.scrollLeft = startScrollLeft - (e.pageX - startX);
//     };

//     const infiniteScroll = () => {
//       // If the carousel is at the beginning, scroll to the end
//       if (carousel.scrollLeft === 0) {
//         this.carousel.classList.add("no-transition");
//         this.carousel.scrollLeft =
//           this.carousel.scrollWidth - 2 * this.carousel.offsetWidth;
//         this.carousel.classList.remove("no-transition");
//       }
//       // If the carousel is at the end, scroll to the beginning
//       else if (
//         Math.ceil(this.carousel.scrollLeft) ===
//         this.carousel.scrollWidth - this.carousel.offsetWidth
//       ) {
//         this.carousel.classList.add("no-transition");
//         this.carousel.scrollLeft = this.carousel.offsetWidth;
//         this.carousel.classList.remove("no-transition");
//       }

//       // Clear existing timeout & start autoplay if mouse is not hovering over carousel
//       clearTimeout(timeoutId);
//       if (!this.wrapper.matches(":hover")) autoPlay();
//     };

//     const autoPlay = () => {
//       if (window.innerWidth < 800 || !isAutoPlay) return; // Return if window is smaller than 800 or isAutoPlay is false
//       // Autoplay the carousel after every 2500 ms
//       timeoutId = setTimeout(
//         () => (this.carousel.scrollLeft += this.firstCardWidth + 55),
//         4000
//       );
//     };
//     autoPlay();

//     this.carousel.addEventListener("mousedown", dragStart);
//     this.carousel.addEventListener("mousemove", dragging);
//     document.addEventListener("mouseup", dragStop);
//     this.carousel.addEventListener("scroll", infiniteScroll);
//     this.wrapper.addEventListener("mouseenter", () => clearTimeout(timeoutId));
//     this.wrapper.addEventListener("mouseleave", autoPlay);
//   }

//   scrollHiheToDuplicate() {
//     this.carousel.classList.add("no-transition");
//     this.carousel.scrollLeft = this.carousel.offsetWidth;
//     this.carousel.classList.remove("no-transition");
//   }
// }
