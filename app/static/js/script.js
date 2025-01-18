let selected;

//variaveis e constantes

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

//funcoes js

async function MenuErro(abrir) {
  const container3 = document.getElementById("container3");
  if (abrir) {
    container3.style.display = "flex";
    container3.style.flexDirection = "column";
    return;
  }
  container3.style.display = "none";
}

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
    const containerImagens = document.getElementById("container2");
    containerImagens.innerHTML = "";
    MenuErro(false);
    return;
  }

  try {
    const response = await fetch(`/get_bits?text=${encodeURIComponent(text)}`);

    if (response.ok) {
      const data = await response.json();

      document.getElementById("resultado").innerHTML = data.bits_array;
    }

    await atualizaImagem();
    MenuErro(true);
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

async function enviarImagem(src) {
  if (!selected) {
    alert("Selecione uma imagem para enviar");
    return;
  }

  const bits = document.getElementById("resultado").innerText;

  if (!bits) {
    alert("Digite algo para converter");
    return;
  }

  const erro = document.getElementById("erro").value;

  if (erro) {
    alert("Digite um valor de erro");
    return;
  }

  if (erro < 0 || erro > 100) {
    alert("Digite um valor de erro entre 0 e 100");
    return;
  }
}
