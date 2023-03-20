const container = document.getElementById("error404");

window.onmousemove = (e) => {
  let x = -e.clientX / 5;
  let y = -e.clientY / 5;
  if (container) {
    container.style.backgroundPositionX = x + "px";
    container.style.backgroundPositionY = y + "px";
  }
};
