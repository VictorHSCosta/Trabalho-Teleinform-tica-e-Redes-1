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

async function atualizatexto() {
  const text = document.getElementById("resultado").innerText;

  try {
    const response = await fetch(`/get_bits?text=${encodeURIComponent(text)}`);

    if (response.ok) {
      const data = await response.json();
      document.getElementById("resultado").innerHTML = data.text;
    }
  } catch (error) {
    console.log(error);
  }
}
