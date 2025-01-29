let select;

function selectElement(element) {
  legacy = select;
  select = element;

  try {
    legacy.style.backgroundColor = "transparent";
    legacy.style.color = "#000";
  } catch (error) {
    console.log("No element selected yet");
  }

  element.style.backgroundColor = "#00ca9e";
  element.style.color = "#fff";
}
