let selected;

function select(element) {
  const updateElement = selected;
  selected = element;

  try {
    updateElement.style.border = "none";
  } catch (error) {
    console.log("No element selected yet");
  }

  element.style.border = "solid 2px #000";
}
