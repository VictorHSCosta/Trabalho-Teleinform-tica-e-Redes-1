let selected;

const images = [
  { src: "../static/images/analogico/Sinal ASK.png", alt: "sinal ask" },
  { src: "../static/images/analogico/Sinal FSK.png", alt: "Sinal FSK" },
  { src: "../static/images/analogico/Sinal PSK.png", alt: "Sinal PSK" },
  { src: "../static/images/digital/Sinal Bipolar.png", alt: "sinal bipolar" },
  {
    src: "../static/images/digital/Sinal Manchester.png",
    alt: "Sinal manchester",
  },
  { src: "../static/images/digital/Sinal NRZ.png", alt: "Sinal NRZ" },
];

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
  const text = document.getElementById("entrada").value;

  if (!text) {
    document.getElementById("resultado").innerHTML = "";
    alert("Digite algo para converter");
    return;
  }

  try {
    const response = await fetch(`/get_bits?text=${encodeURIComponent(text)}`);

    if (response.ok) {
      const data = await response.json();

      document.getElementById("resultado").innerHTML = data.bits_array;
    }

    await atualizaImagem();
  } catch (error) {
    console.log(error);
  }
}

async function atualizaImagem() {
  const containerImagens = document.getElementById("container2");

  containerImagens.innerHTML = "";

  const h2 = document.createElement("h2");
  h2.innerText = "Selecione uma das imagens para enviar";
  containerImagens.appendChild(h2);

  const div = document.createElement("imagens");
  div.id = "imagens";

  images.forEach((image) => {
    const button = document.createElement("button");
    const img = document.createElement("img");
    img.src = `${image.src}?t=${new Date().getTime()}`;
    img.alt = image.alt;
    img.onclick = () => enviarImagem(image.src);
    button.appendChild(img);
    button.onclick = () => select(button);
    div.appendChild(button);
  });

  containerImagens.appendChild(div);
}

async function abrirConfiguracoes() {}
